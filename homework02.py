X, O, _ = 1, 0, None

TEST_BOARD = (
    O, X, O,
    X, O, X,
    X, O, X
)
O_WINS, X_WINS, UNDEFINED, DRAW = range(4)

def slice3(bord):
    win_comb = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)] #определение всех вариантов победы
    return win_comb

def outcome(bord):
    try:
        win = slice3(bord)
        winner = bord[[i for i in win if bord[i[0]] == bord[i[1]] == bord[i[2]]][0][0]] #ищем комбинации соответствующие победе и определяем кому она досталась
        if winner == 1:
            return("X_WINS")
        else:
            return("O_WINS")
    except:
        if (bord.count(1) + bord.count(0)) == 9:
            return("DRAW")
        else:
            return("UNDEFINED")

if __name__ == "__main__":
    import doctest
    doctest.testmod()
