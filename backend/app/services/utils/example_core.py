import json
import os
import re
from typing import Dict

from backend.app.services.utils.OTPUtils.OTPEmailVerifyUtil import SendEmail
import tiktoken
from dotenv import load_dotenv  # type: ignore
from google import genai



load_dotenv()

# Add price constants
INPUT_PRICE_PER_MILLION = 1.25  # $1.25 per million tokens
OUTPUT_PRICE_PER_MILLION = 5.0  # $5.00 per million tokens
CONTEXT_PRICE_PER_MILLION = 0.3125  # $0.3125 per million tokens


def calculate_price(input_tokens: int, output_tokens: int, context_tokens: int = 0) -> float:
    """Calculate total price based on token usage.
    
    Args:
        input_tokens (int): Number of input tokens
        output_tokens (int): Number of output tokens
        context_tokens (int): Number of context tokens
        
    Returns:
        float: Total price in USD
    """
    input_price = (input_tokens / 1_000_000) * INPUT_PRICE_PER_MILLION
    output_price = (output_tokens / 1_000_000) * OUTPUT_PRICE_PER_MILLION
    context_price = (context_tokens / 1_000_000) * CONTEXT_PRICE_PER_MILLION
    return input_price + output_price + context_price



def parse_json_from_response(response: str) -> Dict:
    """_summary_

    Args:
        response (str): _description_

    Returns:
        Dict: _description_
    """

    try:
        parsed_response = json.loads(response)
    except json.JSONDecodeError:
        try:
            new_response = response.split("```")[1][5:]
            parsed_response = json.loads(new_response)
        except json.JSONDecodeError:
            pattern = r'(json)\s*({.*})'
            match = re.search(pattern, response, re.DOTALL | re.IGNORECASE)

            if match:
                parsed_response = json.loads(match.group(2))
            else:
                parsed_response = {}
    return parsed_response


def count_tokens(text: str, model: str = "gpt-4") -> int:
    """Count the number of tokens in a text string.
    
    Args:
        text (str): The text to count tokens for
        model (str): The model to use for counting tokens
        
    Returns:
        int: Number of tokens
    """
    if "gemini" in model.lower():
        # Gemini approximates tokens as ~4 characters per token
        return len(text) // 4
    else:
        encoding = tiktoken.encoding_for_model(model)
        return len(encoding.encode(text))


class MeetingAnalyzer:
    def __init__(self):
        self.meeting_id = None
        self.id = 0
        self.SendEmail = SendEmail()
        self.filename = None
        self._init_agent()

    def set_id(self, id, meeting_id):
        self.id = id
        self.filename = f"Meeting_note_{id}.docx"
        self.meeting_id = meeting_id

    def get_id(self):
        return self.id

    def _init_agent(self):
        model_name = "model/gemini-2.0-flash-exp"
        service = "gemini"

        self.llm = self._init_model(service, model_name)
        self.secretary = MeetingSecretary(self.llm)
        self.con_sum = ConversationSummarizer(self.llm)

    @staticmethod
    def _init_model(service, model_id):
        client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
        return client

    async def complete(self, transcript: str, email: str = None, authen: bool = False):
        await self.secretary.process(transcript=transcript)
        result = await self.secretary.get_result()
        if email:
            self.SendEmail.send_meeting_note_to_email(email=email, note=result['meeting_note'])
        return result  # Return the complete result object instead of just meeting_note

    async def complete_summarizer(self, conversation: str):
        await self.con_sum.process(conversation=conversation)
        result = await self.con_sum.get_result()
        return result  # Return the complete result object

class MeetingSecretary:
    def __init__(self, llm):
        self.system_prompt = None
        self.llm = llm
        self.meeting_note = {
            "summary": ""
        }
        self.title = ""
        self.total_tokens = 0
        self.input_tokens = 0
        self.output_tokens = 0
        self.context_tokens = 0
        self.chunk_count = 0  # Add new attribute to track chunks

    @staticmethod
    def divide_transcript(transcript: str, max_tokens: int = 1000000) -> list:
        lines = transcript.split("\n")
        blocks = []
        current_block = []
        current_tokens = 0
        total_tokens = count_tokens(transcript, model='gemini')

        print(f"\n=== Transcript Division Info ===")
        print(f"Total tokens in transcript: {total_tokens}")
        print(f"Max tokens per chunk: {max_tokens}")
        print(f"Estimated chunks needed: {(total_tokens + max_tokens - 1) // max_tokens}")
        print("============================\n")

        for line in lines:
            line_tokens = count_tokens(line, model='gemini')
            if current_tokens + line_tokens > max_tokens:
                blocks.append("\n".join(current_block))
                current_block = [line]
                current_tokens = line_tokens
            else:
                current_block.append(line)
                current_tokens += line_tokens

        if current_block:
            blocks.append("\n".join(current_block))

        print(f"\n=== Final Division Results ===")
        print(f"Number of chunks created: {len(blocks)}")
        for i, block in enumerate(blocks, 1):
            block_tokens = count_tokens(block, model='gemini')
            print(f"Chunk {i}: {block_tokens} tokens")
        print("============================\n")

        return blocks

    async def process(self, transcript: str):
        self.system_prompt = """Bạn là một trợ lý thông minh và hiệu quả trong việc ghi chú cuộc họp. Nhiệm vụ chính của bạn là tạo ra các ghi chú cuộc họp chi tiết, có tổ chức và đầy đủ thông tin từ [bản ghi âm cuộc họp]. Đảm bảo rằng các ghi chú cuộc họp của bạn đáp ứng đầy đủ các yêu cầu được đặt ra, trả lời bằng tiếng Việt gần gũi, dễ hiểu chi tiết rõ ràng."""
        try:
            transcript_blocks = self.divide_transcript(transcript)
            self.chunk_count = len(transcript_blocks)  # Store the number of chunks
            for block in transcript_blocks:
                self.meeting_note['summary'] += "\n" + await self.generate_summary(block)
        except Exception as e:
            self.meeting_note['summary'] = await self.generate_summary(transcript)
            self.chunk_count = 1  # Single chunk in case of exception

    async def generate_summary(self, transcript) -> str:
        prompt = """From the conversation below, create a detailed meeting note IN TABLE with the following structure:

## MEETING NAME
### A. INFORMATION
   #### 1. Date:
   #### 2. Attendance:
   #### 3. Agenda Outline:
   #### 4. Meeting Tone/Atmosphere:

### B. KEY POINTS
   #### 5. Goal:
   #### 6. Summary:
      - Facts: [List key facts discovered]
      - Problems: [List challenges/issues raised]
      - Solutions Proposed: [List suggested solutions]
      - Risk Factors: [List potential risks discussed]
   
### C. DECISIONS & ACTIONS
   #### 7. List of Decision Made:
      - Context of each decision
      - Impact assessment
      - Implementation timeline
   #### 8. Action Items by Attendee:
      - For each attendee:
        + Assigned tasks with deadlines
        + Dependencies
        + Expected outcomes
      - Note explicitly if attendee has no tasks
   
### D. FOLLOW-UP
   #### 9. Questions Raised:
         - Q1: [Exact question from transcript]
			- Answer: Is the question get answered or not [Exact question from transcript]
         - Q2: [Exact question from transcript]
			- Answer: Is the question get answered or not [Exact question from transcript]
         [Continue for all questions]
   #### 10. Next Steps:
       - Next meeting date/topic
       - Required preparation

PLEASE ANSWER IN VIETNAMESE
YÊU CẦU CHI TIẾT:
- LIỆT KÊ TẤT CẢ CÂU HỎI ĐƯỢC ĐẶT RA TRONG CUỘC HỌP
- PHÂN TÍCH TỪNG CÂU HỎI VÀ TRẠNG THÁI GIẢI QUYẾT
- GHI CHÚ RÕ RÀNG CÂU TRẢ LỜI HOẶC HÀNH ĐỘNG TIẾP THEO
- CHỈ TRẢ LỜI THEO CẤU TRÚC TRÊN

{transcript}"""
        prompt = prompt.replace("{transcript}", transcript)
        full_prompt = self.system_prompt + prompt

        # Count tokens before making the API call
        tokens = count_tokens(full_prompt)
        self.total_tokens += tokens
        self.input_tokens += tokens

        response = self.llm.models.generate_content(
            model='gemini-2.0-flash-exp', contents=full_prompt)
        response_tokens = count_tokens(response.text)
        self.total_tokens += response_tokens
        self.output_tokens += response_tokens
        return response.text

    async def refine_summary(self) -> str:
        note = self.meeting_note['summary']
        prompt = """Optimize the provided meeting note by strictly following these instructions:
1. Arrange the information in a logical order.
2. Consolidate duplicate information while preserving clarity, detail and completeness.
3. Remove unnecessary or redundant details.

Use the following structure **EXACTLY** for the final meeting note:

MEETING NAME
A. INFORMATION
   1. Date:
   2. Attendance:
   3. Agenda Outline:
B. ACTION
   4. Goal:
   5. Summary:
   6. List of Decisions Made:
   7. List of Action Items (Who, Task, Deadline)

Input meeting note:
{note}

**REQUIREMENTS**:
- Write the response in **Vietnamese**.
- Highlight key points such as **facts**, **problems**, and **questions**.
- Maintain accuracy, detail and conciseness. Do not response or make up the structure, or extra information
"""
        prompt = prompt.replace("{note}", note)

        # Count tokens before making the API call
        tokens = count_tokens(prompt)
        self.total_tokens += tokens
        self.input_tokens += tokens

        response = self.llm.models.generate_content(
            model='gemini-2.0-flash-exp', contents=prompt)
        response_tokens = count_tokens(response.text)
        self.total_tokens += response_tokens
        self.output_tokens += response_tokens
        return response.text

    async def get_result(self):
        if self.chunk_count > 1:
            summary = await self.refine_summary()
        else:
            summary = self.meeting_note['summary']

        price = calculate_price(self.input_tokens, self.output_tokens, self.context_tokens)
        return {
            "title": self.title,
            "meeting_note": summary,
            "token_usage": {
                "input_tokens": self.input_tokens,
                "output_tokens": self.output_tokens,
                "context_tokens": self.context_tokens,
                "total_tokens": self.total_tokens,
                "price_usd": round(price, 6)
            }
        }


class ConversationSummarizer:
    def __init__(self, llm):
        self.system_prompt = None
        self.llm = llm
        self.content = {
            "detail_content": "",
        }
        self.total_tokens = 0
        self.input_tokens = 0
        self.output_tokens = 0
        self.context_tokens = 0

    async def process(self, conversation: str):
        self.system_prompt = """
Role: You are an AI Assistant
Action: Summarize the conversation between a customer, an admin, and a chatbot.
Context: Analyze the discussion to capture each participant's intent, the details of the conversation, and the services or products involved.
## Instructions for LLM:
1. Follow the structure strictly do not modify the format, structure, or wording of the conversation prompt.
2. Respond in Vietnamese.
3. Provide a well-structured and informative summary of the conversation based on the context provided. 
4. The response must be logically organized, clear, and specific to the conversation context.
65. The response must contain ["# Titile", "## I. Tóm tắt nội dung", "## II. Dịch vụ đề cập", "## III. Hành động tiếp theo", "## IV. Đề xuất hành động tiếp theo", "## V. Nhãn phân loại nội dung trao đổi"].

Format: Provide a detailed and clear summary in Vietnamese following the structure below. Use bullet points (*) and avoid formatting such as bold or italic. Strictly adhere to the format.

# Title: Maximum 50-character brief summary of the conversation.

## I. Tóm tắt nội dung:
Provide a detailed summary of the key points discussed, including the customer's needs, issues encountered, and specific questions asked, display in bullet points using *.

## II. Dịch vụ đề cập:
Mention all services and products discussed in the conversation.

## III. Hành động tiếp theo:
Outline specific next steps discussed, such as follow-ups, demos, or requests for additional information.

## IV. Đề xuất hành động tiếp theo:
Based on the summary, suggest specific follow-up actions to enhance customer satisfaction and address the needs identified in the conversation.

## V. Nhãn phân loại nội dung trao đổi:
Label the conversation with tags in each of the following categories, using the most specific options possible in the pattern {* <Number>. <Type>:<Tag>} and must contain all 5 tags:

   * 1. Kết quả cuộc trò chuyện:<Chốt đơn thành công/Chưa chốt đơn/Cần liên hệ lại/Đang xử lý/Đã giải quyết/Đang chờ phản hồi khách hàng>.
   * 2. Mức độ hài lòng của khách hàng:<Hài lòng/Không hài lòng/Phản hồi tiêu cực/Phản hồi tích cực/Cần hỗ trợ thêm>.
   * 3. Nội dung cuộc trò chuyện:<Tư vấn sản phẩm/Tư vấn dịch vụ/Giải đáp thắc mắc/Hỗ trợ kỹ thuật/Tư vấn bán hàng/Hướng dẫn sử dụng/Yêu cầu thông tin khuyến mãi>.
   * 4. Phản hồi khách hàng:<Quan tâm/Không quan tâm/Đang cân nhắc/Đã quyết định mua/Không phản hồi>.
   * 5. Yêu cầu và hỗ trợ:<Yêu cầu thông tin bổ sung/Yêu cầu báo giá/Yêu cầu hỗ trợ kỹ thuật>.
"""
        self.content['detail_content'] = await self.generate_detail_content(conversation)

    async def generate_detail_content(self, conversation: str) -> str:
        prompt = f"""{self.system_prompt}\n\nConversation:\n{conversation}\n\nSummary:"""

        tokens = count_tokens(prompt)
        self.total_tokens += tokens
        self.input_tokens += tokens

        response = self.llm.models.generate_content(
            model='gemini-2.0-flash-exp', contents=prompt)
        response_tokens = count_tokens(response.text)
        self.total_tokens += response_tokens
        self.output_tokens += response_tokens
        return response.text

    async def get_result(self):
        price = calculate_price(self.input_tokens, self.output_tokens, self.context_tokens)
        return {
            "conversation_summary": self.content['detail_content'],
            "token_usage": {
                "input_tokens": self.input_tokens,
                "output_tokens": self.output_tokens,
                "context_tokens": self.context_tokens,
                "total_tokens": self.total_tokens,
                "price_usd": round(price, 6)
            }
        }
