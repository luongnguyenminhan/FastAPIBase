"""
Math Operations Utility

This file defines the MathOperations class, which provides static methods for basic mathematical operations.
It includes methods for addition, subtraction, multiplication, division, and exponentiation.

Dependencies:
- None

Author: Minh An
Last Modified: 21 Jan 2024
Version: 1.0.0
"""


class MathOperations:
    """
    Utility class for basic mathematical operations
    """

    @staticmethod
    def add(x: float, y: float) -> float:
        """
        Add two numbers

        Args:
            x (float): The first number
            y (float): The second number

        Returns:
            float: The sum of the two numbers
        """
        return x + y

    @staticmethod
    def subtract(x: float, y: float) -> float:
        """
        Subtract second number from first number

        Args:
            x (float): The first number
            y (float): The second number

        Returns:
            float: The difference between the two numbers
        """
        return x - y

    @staticmethod
    def multiply(x: float, y: float) -> float:
        """
        Multiply two numbers

        Args:
            x (float): The first number
            y (float): The second number

        Returns:
            float: The product of the two numbers
        """
        return x * y

    @staticmethod
    def divide(x: float, y: float) -> float:
        """
        Divide first number by second number

        Args:
            x (float): The first number
            y (float): The second number

        Returns:
            float: The quotient of the two numbers

        Raises:
            ValueError: If the second number is zero
        """
        if y == 0:
            raise ValueError("Cannot divide by zero")
        return x / y

    @staticmethod
    def power(x: float, y: float) -> float:
        """
        Raise first number to the power of second number

        Args:
            x (float): The base number
            y (float): The exponent

        Returns:
            float: The result of raising the base to the exponent
        """
        return x ** y
