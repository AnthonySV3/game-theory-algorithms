class NashEquilibria:
    """A mixed-strategy profile: dist_a over the row player's actions,
    dist_b over the column player's actions."""

    def __init__(self, dist_a, dist_b):
        self.dist_a = dist_a
        self.dist_b = dist_b

    def __repr__(self):
        return f"NashEquilibria(dist_a={self.dist_a}, dist_b={self.dist_b})"
