from bimatrix_parser import parse_bimatrix


def main():
    game = parse_bimatrix("stag_hunt.txt")
    game.print_a()
    print()
    game.print_b()

    print(game.support_enumeration_equilibria())


if __name__ == "__main__":
    main()
