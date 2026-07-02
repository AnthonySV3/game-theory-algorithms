from bimatrix import Bimatrix


def parse_bimatrix(path):
    """Parse a bimatrix file into a Bimatrix.

    Format:
        <rows> <columns>
        matrix A  (rows lines, each with columns values)
        <blank line>
        matrix B  (rows lines, each with columns values)
    """
    with open(path, "r") as f:
        lines = [line.split() for line in f if line.strip()]

    if not lines or len(lines[0]) < 2:
        raise ValueError("Expected '<rows> <columns>' on the first line")

    rows = int(lines[0][0])
    cols = int(lines[0][1])
    if rows <= 0 or cols <= 0:
        raise ValueError(f"Rows and columns must be positive: {rows}x{cols}")

    expected = 1 + 2 * rows
    if len(lines) != expected:
        raise ValueError(
            f"Expected {2 * rows} matrix rows for a {rows}x{cols} game, "
            f"found {len(lines) - 1}"
        )

    A = _read_matrix(lines[1:1 + rows], cols, "A")
    B = _read_matrix(lines[1 + rows:1 + 2 * rows], cols, "B")
    return Bimatrix(A, B)


def _read_matrix(row_tokens, cols, name):
    matrix = []
    for i, tokens in enumerate(row_tokens):
        if len(tokens) != cols:
            raise ValueError(
                f"Matrix {name} row {i} has {len(tokens)} values, expected {cols}"
            )
        matrix.append([float(token) for token in tokens])
    return matrix
