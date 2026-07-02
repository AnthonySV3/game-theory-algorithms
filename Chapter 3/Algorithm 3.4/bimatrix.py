from itertools import combinations

import numpy as np

from nash_equilibria import NashEquilibria


class Bimatrix:
    """A two-player game defined by payoff matrices A (row player) and B (column player)."""

    def __init__(self, A, B):
        self.A = A
        self.B = B

    @property
    def num_rows(self):
        return len(self.A)

    @property
    def num_cols(self):
        return len(self.A[0]) if self.A else 0

    def print_a(self):
        _print_matrix(self.A)

    def print_b(self):
        _print_matrix(self.B)

    # Algorithm 3.4
    def support_enumeration_equilibria(self, eps=1e-9):
        NEs = []
        A = np.array(self.A, dtype=float)
        B = np.array(self.B, dtype=float)
        maxK = min(self.num_rows, self.num_cols)
        M = list(range(self.num_rows))
        N = list(range(self.num_cols))
        for k in range(1, maxK + 1):
            for I in combinations(M, k):
                for J in combinations(N, k):
                    coefficients1 = []
                    constants1 = []
                    for j in J:
                        coefficientsrow = []
                        for i in I:
                            coefficientsrow.append(self.B[i][j])
                        coefficientsrow.append(1)
                        coefficients1.append(coefficientsrow)
                        constants1.append(0)
                    total_prob_row = [1] * len(I)
                    total_prob_row.append(0)
                    coefficients1.append(total_prob_row)
                    constants1.append(1)

                    coefficients2 = []
                    constants2 = []
                    for i in I:
                        coefficientsrow = []
                        for j in J:
                            coefficientsrow.append(self.A[i][j])
                        coefficientsrow.append(1)
                        coefficients2.append(coefficientsrow)
                        constants2.append(0)
                    total_prob_row = [1] * len(J)
                    total_prob_row.append(0)
                    coefficients2.append(total_prob_row)
                    constants2.append(1)

                    # Solve both linear systems. A singular matrix means the
                    # support is degenerate, so skip it.
                    try:
                        sol1 = np.linalg.solve(
                            np.array(coefficients1, dtype=float),
                            np.array(constants1, dtype=float),
                        )
                        sol2 = np.linalg.solve(
                            np.array(coefficients2, dtype=float),
                            np.array(constants2, dtype=float),
                        )
                    except np.linalg.LinAlgError:
                        continue

                    # The last entry of each solution is the indifference value;
                    # the rest are the probabilities over the support.
                    x = sol1[:len(I)]  # row player's probabilities over I
                    y = sol2[:len(J)]  # column player's probabilities over J

                    # Probabilities on the support must be non-negative.
                    if np.any(x < -eps) or np.any(y < -eps):
                        continue

                    # Expand to full mixed strategies (zero off the support).
                    dist_a = np.zeros(self.num_rows)
                    dist_a[list(I)] = x
                    dist_b = np.zeros(self.num_cols)
                    dist_b[list(J)] = y

                    # Best-response check: no unplayed action may beat the
                    # payoff earned on the support.
                    row_payoffs = A @ dist_b
                    col_payoffs = dist_a @ B
                    if np.any(row_payoffs > row_payoffs[I[0]] + eps):
                        continue
                    if np.any(col_payoffs > col_payoffs[J[0]] + eps):
                        continue

                    NEs.append(NashEquilibria(dist_a.tolist(), dist_b.tolist()))
        return NEs


def _print_matrix(matrix):
    for row in matrix:
        print(" ".join(_format(value) for value in row))


def _format(value):
    # Show integers without a trailing ".0" for readability.
    if value == int(value):
        return str(int(value))
    return str(value)
