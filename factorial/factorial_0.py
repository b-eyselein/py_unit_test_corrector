def factorial(n: int) -> int:
    if not isinstance(n, int):
        raise Exception("n must be an integer!")

    if n < 0:
        raise Exception("n must be positive!")

    fac: int = 1

    for i in range(1, n + 1):
        fac *= i

    return fac
