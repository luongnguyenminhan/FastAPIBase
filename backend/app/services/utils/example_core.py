class MathOperations:
    @staticmethod
    def add(x: float, y: float) -> float:
        """Add two numbers"""
        return x + y
    
    @staticmethod
    def subtract(x: float, y: float) -> float:
        """Subtract second number from first number"""
        return x - y
    
    @staticmethod
    def multiply(x: float, y: float) -> float:
        """Multiply two numbers"""
        return x * y
    
    @staticmethod
    def divide(x: float, y: float) -> float:
        """Divide first number by second number"""
        if y == 0:
            raise ValueError("Cannot divide by zero")
        return x / y
    
    @staticmethod
    def power(x: float, y: float) -> float:
        """Raise first number to the power of second number"""
        return x ** y
