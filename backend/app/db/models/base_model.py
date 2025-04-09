from datetime import datetime

from pydantic import ConfigDict
from pytz import timezone
from sqlalchemy import Column, Integer, DateTime, Boolean, String, Text, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class BaseModel(Base):
    """
    Base model class for all database models

    Attributes:
        id (int): The primary key of the model
        create_date (DateTime): The creation date of the model
        update_date (DateTime): The last update date of the model
        is_deleted (bool): The deletion status of the model
    """
    __abstract__ = True

    model_config = ConfigDict(arbitrary_types_allowed=True)

    id = Column(Integer, primary_key=True, index=True)
    create_date = Column(DateTime, default=datetime.now(timezone("Asia/Ho_Chi_Minh")))
    update_date = Column(DateTime, nullable=True)
    is_deleted = Column(Boolean, default=False)

    def dict(self):
        """
        Convert model instance to dictionary

        Returns:
            dict: A dictionary representation of the model instance
        """
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Users(BaseModel):
    """
    User model class

    Attributes:
        google_email (str): The Google email of the user
        display_name (str): The display name of the user
        avatar_url (str): The avatar URL of the user
        role (str): The role of the user
    """
    __tablename__ = "users"

    google_email = Column(String(100), unique=True, nullable=False)
    display_name = Column(String(100), nullable=False)
    avatar_url = Column(String(255), nullable=True)
    role = Column(String(50), default="user")

    login_logs = relationship("LoginLogs", back_populates="user")
    activity_logs = relationship("ActivityLogs", back_populates="user")
    chat_sessions = relationship("ChatSessions", back_populates="user")
    usage_limits = relationship("UsageLimits", back_populates="user")
    subscriptions = relationship("Subscriptions", back_populates="user")

class LoginLogs(BaseModel):
    """
    Login logs model class

    Attributes:
        user_id (int): The ID of the user
        login_time (datetime): The login time
        ip_address (str): The IP address
        device_info (str): The device information
    """
    __tablename__ = "login_logs"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    login_time = Column(DateTime, default=datetime.now(timezone("Asia/Ho_Chi_Minh")))
    ip_address = Column(String(50), nullable=True)
    device_info = Column(String(255), nullable=True)

    user = relationship("Users", back_populates="login_logs")

class ActivityLogs(BaseModel):
    """
    Activity logs model class

    Attributes:
        user_id (int): The ID of the user
        activity_type (str): The type of activity
        description (str): The description of the activity
    """
    __tablename__ = "activity_logs"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    activity_type = Column(String(50), nullable=False)
    description = Column(String(255), nullable=True)

    user = relationship("Users", back_populates="activity_logs")

class ChatSessions(BaseModel):
    """
    Chat sessions model class

    Attributes:
        user_id (int): The ID of the user
        started_at (datetime): The start time of the session
        ended_at (datetime): The end time of the session
        session_status (str): The status of the session
    """
    __tablename__ = "chat_sessions"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    started_at = Column(DateTime, default=datetime.now(timezone("Asia/Ho_Chi_Minh")))
    ended_at = Column(DateTime, nullable=True)
    session_status = Column(String(50), default="active")

    user = relationship("Users", back_populates="chat_sessions")
    chat_messages = relationship("ChatMessages", back_populates="session")
    generated_slides = relationship("GeneratedSlides", back_populates="session")

class ChatMessages(BaseModel):
    """
    Chat messages model class

    Attributes:
        session_id (int): The ID of the chat session
        sender (str): The sender of the message
        message_content (str): The content of the message
        timestamp (datetime): The timestamp of the message
    """
    __tablename__ = "chat_messages"

    session_id = Column(Integer, ForeignKey("chat_sessions.id"), nullable=False)
    sender = Column(String(50), nullable=False)
    message_content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.now(timezone("Asia/Ho_Chi_Minh")))

    session = relationship("ChatSessions", back_populates="chat_messages")

class SlideTemplates(BaseModel):
    """
    Slide templates model class

    Attributes:
        template_name (str): The name of the template
        layout_data (str): The layout data of the template
        description (str): The description of the template
        tags (str): The tags of the template
        category (str): The category of the template
        priority (str): The priority of the template
    """
    __tablename__ = "slide_templates"

    template_name = Column(String(100), nullable=False)
    layout_data = Column(Text, nullable=False)
    description = Column(String(255), nullable=True)
    tags = Column(String(255), nullable=True)
    category = Column(String(50), nullable=True)
    priority = Column(String(50), nullable=True)

    generated_slides = relationship("GeneratedSlides", back_populates="template")

class GeneratedSlides(BaseModel):
    """
    Generated slides model class

    Attributes:
        session_id (int): The ID of the chat session
        template_id (int): The ID of the slide template
        slide_content (str): The content of the slide
        file_path (str): The file path of the slide
    """
    __tablename__ = "generated_slides"

    session_id = Column(Integer, ForeignKey("chat_sessions.id"), nullable=False)
    template_id = Column(Integer, ForeignKey("slide_templates.id"), nullable=False)
    slide_content = Column(Text, nullable=False)
    file_path = Column(String(255), nullable=True)

    session = relationship("ChatSessions", back_populates="generated_slides")
    template = relationship("SlideTemplates", back_populates="generated_slides")
    slide_history = relationship("SlideHistory", back_populates="slide")

class SlideHistory(BaseModel):
    """
    Slide history model class

    Attributes:
        slide_id (int): The ID of the generated slide
        version_number (int): The version number
        changes (str): The changes made
    """
    __tablename__ = "slide_history"

    slide_id = Column(Integer, ForeignKey("generated_slides.id"), nullable=False)
    version_number = Column(Integer, nullable=False)
    changes = Column(String(255), nullable=True)

    slide = relationship("GeneratedSlides", back_populates="slide_history")

class UsageLimits(BaseModel):
    """
    Usage limits model class

    Attributes:
        user_id (int): The ID of the user
        daily_generate_quota (int): The daily generate quota
        used_count (int): The used count
        last_reset (datetime): The last reset time
    """
    __tablename__ = "usage_limits"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    daily_generate_quota = Column(Integer, default=10)
    used_count = Column(Integer, default=0)
    last_reset = Column(DateTime, default=datetime.now(timezone("Asia/Ho_Chi_Minh")))

    user = relationship("Users", back_populates="usage_limits")

class SubscriptionPlans(BaseModel):
    """
    Subscription plans model class

    Attributes:
        plan_name (str): The name of the plan
        description (str): The description of the plan
        price (float): The price of the plan
        duration_days (int): The duration in days of the plan
    """
    __tablename__ = "subscription_plans"

    plan_name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    price = Column(Float, nullable=False)
    duration_days = Column(Integer, nullable=False)

    subscriptions = relationship("Subscriptions", back_populates="plan")

class Subscriptions(BaseModel):
    """
    Subscriptions model class

    Attributes:
        user_id (int): The ID of the user
        plan_id (int): The ID of the subscription plan
        start_date (datetime): The start date of the subscription
        end_date (datetime): The end date of the subscription
        status (str): The status of the subscription
    """
    __tablename__ = "subscriptions"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    plan_id = Column(Integer, ForeignKey("subscription_plans.id"), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    status = Column(String(50), default="active")

    user = relationship("Users", back_populates="subscriptions")
    plan = relationship("SubscriptionPlans", back_populates="subscriptions")
    payments = relationship("Payments", back_populates="subscription")

class Payments(BaseModel):
    """
    Payments model class

    Attributes:
        subscription_id (int): The ID of the subscription
        amount (float): The amount of the payment
        payment_method (str): The payment method
        payment_date (datetime): The payment date
        status (str): The status of the payment
    """
    __tablename__ = "payments"

    subscription_id = Column(Integer, ForeignKey("subscriptions.id"), nullable=False)
    amount = Column(Float, nullable=False)
    payment_method = Column(String(50), nullable=False)
    payment_date = Column(DateTime, default=datetime.now(timezone("Asia/Ho_Chi_Minh")))
    status = Column(String(50), default="pending")

    subscription = relationship("Subscriptions", back_populates="payments")
