def babylonian_square_root(number: float, rounds: int) -> float:
    # check type of number and rounds
    if not isinstance(number, (int, float)):
        raise Exception('Can only calculate the root of a number (int or float')

    if not isinstance(rounds, int):
        raise Exception('The number of rounds has to be an int greater than zero!')

    # Check that number and rounds are greater than 0
    if number <= 0:
        raise Exception('Number has to be greater than 0!')

    if rounds < 0:
        raise Exception('The number of rounds has to be greater than 0!')

    # Calculate square root
    sqr: float = number

    for _i in range(rounds):
        sqr = 1 / 2 * (sqr + (number / sqr))

    return sqr
