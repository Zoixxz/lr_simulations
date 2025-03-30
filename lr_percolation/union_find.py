# union_find.py
# contains data structure for fast evaluation of cluster sized

# Union find by vertex size
class UnionFind:
    """
    Union-Find (Disjoint Set) data structure with
    union by size and path compression.
    
    For i == find(i), size[i] gives the size of that cluster.
    """
    def __init__(self, n: int):
        self.parent: list = list(range(n))
        self.size: list = [1]*n   # valid only for root indices
    
    def find(self, a: int) -> int:
        while self.parent[a] != a:
            self.parent[a] = self.parent[self.parent[a]]  # path compression
            a = self.parent[a]
        return a
    
    def union(self, a: int, b: int) -> None:
        ra = self.find(a)
        rb = self.find(b)
        if ra != rb:
            # append smaller to larger tree
            if self.size[ra] < self.size[rb]:
                ra, rb = rb, ra
            self.parent[rb] = ra
            self.size[ra] += self.size[rb]


# TODO union find by edge size