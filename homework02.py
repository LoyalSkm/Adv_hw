X, O, _  = 1, 0, None

TEST_BOARD = (
    O, X, X,
    O, None, X,
    X, O, O
)
O_WINS, X_WINS, UNDEFINED, DRAW = range(4)


def slice3(bord):
    wind_comb1 = [bord[0: 3], bord[3: 6], bord[6: 9], bord[0: 9: 3], bord[1: 9: 3], bord[2: 9: 3], bord[0:9:4], bord[2:7:2]]
    return wind_comb1
def outcome(bord):
    if None in bord:
        return UNDEFINED

    for i in slice3(bord):
        if i[0] == i[1] == i[2]:
            if i[0] == 1:
                return X_WINS
            else:
                return O_WINS
    return DRAW

if __name__ == "__main__":
    import doctest
    doctest.testmod()
