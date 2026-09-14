def format_inr(amount: float) -> str:
    """Format an amount using Indian digit grouping."""
    rounded_amount = round(amount, 2)
    integer_part, _, decimal_part = f"{rounded_amount:.2f}".partition(".")
    sign = "-" if integer_part.startswith("-") else ""
    digits = integer_part.lstrip("-")
    if len(digits) > 3:
        last_three = digits[-3:]
        remaining = digits[:-3]
        groups = []
        while remaining:
            groups.insert(0, remaining[-2:])
            remaining = remaining[:-2]
        digits = ",".join(groups + [last_three])
    return f"{sign}₹{digits}.{decimal_part}"


class Calculator:
    @staticmethod
    def multiply(a: int, b: int) -> int:
        """
        Multiply two integers.

        Args:
            a (int): The first integer.
            b (int): The second integer.

        Returns:
            int: The product of a and b.
        """
        return a * b
    
    @staticmethod
    def calculate_total(*x: float) -> float:
        """
        Calculate sum of the given list of numbers

        Args:
            x (list): List of floating numbers

        Returns:
            float: The sum of numbers in the list x
        """
        return sum(x)
    
    @staticmethod
    def calculate_daily_budget(total: float, days: int) -> float:
        """
        Calculate daily budget

        Args:
            total (float): Total cost.
            days (int): Total number of days

        Returns:
            float: Expense for a single day
        """
        return total / days if days > 0 else 0
    
    
