def ggt(a: int, b: int) -> int:
    if not isinstance(a, int):
        raise Exception('Both numbers have to be an int!')

    if not isinstance(b, int):
        raise Exception('Both numbers have to be an int!')

    if a <= 0:
        raise Exception('Both numbers have to be greater than 0!')

    if b <= 0:
        raise Exception('Both numbers have to be greater than 0!')

    while b != 0:
        h: int = a % b
        a = b
        b = h
    return a
