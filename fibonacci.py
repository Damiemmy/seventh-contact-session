def fibonacci(count: int):
    """Yield the first `count` numbers in the Fibonacci sequence."""
    if count < 0:
        raise ValueError("Count cannot be negative.")

    first, second = 0, 1
    for _ in range(count):
        yield first
        first, second = second, first + second


def main():
    try:
        count = int(input("How many Fibonacci numbers should be generated? "))
        if count < 0:
            print("Please enter zero or a positive number.")
            return

        print(f"\nFirst {count} Fibonacci number(s):")
        print(", ".join(str(number) for number in fibonacci(count)))
    except ValueError:
        print("Invalid input. Please enter a whole number.")


if __name__ == "__main__":
    main()
