from typing import Callable


def generator_numbers(text: str):
    # Split text into words and convert valid numbers
    for word in text.split():
        try:
            number = float(word)
            yield number
        except ValueError:
            continue


def sum_profit(text: str, func: Callable):
    # Use generator to sum all numbers
    return sum(func(text))


if __name__ == "__main__":
    # Example usage
    text = "Загальний дохід працівника складається з декількох частин: 1000.01 як основний дохід, доповнений додатковими надходженнями 27.45 і 324.00 доларів."
    total_income = sum_profit(text, generator_numbers)
    print(f"Загальний дохід: {total_income}")  # 1351.46
