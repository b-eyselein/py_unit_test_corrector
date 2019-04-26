def ggt(a: int, b: int) -> int:
    # UTT-2-2
    if not isinstance(b, int):
        raise Exception('Both numbers have to be an int!')

    # UTT-3-2
    if a <= 0:
        raise Exception('Both numbers have to be greater than 0!')

    # UTT-4-2
    if b <= 0:
        raise Exception('Both numbers have to be greater than 0!')

    while b != 0:
        h: int = a % b
        a = b
        b = h
    return a
