def caching_fibonacci():
    # Initialize cache dictionary
    cache = {}

    def fibonacci(n):
        # Base cases
        if n <= 0:
            return 0
        if n == 1:
            return 1

        # Check if value exists in cache
        if n in cache:
            return cache[n]

        # Calculate and cache the value
        cache[n] = fibonacci(n - 1) + fibonacci(n - 2)
        return cache[n]

    return fibonacci


if __name__ == "__main__":
    # Example usage
    fib = caching_fibonacci()
    print(fib(10))  # 55
    print(fib(15))  # 610
