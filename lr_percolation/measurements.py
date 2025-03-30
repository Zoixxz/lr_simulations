from union_find import UnionFind

def measurements(uf: UnionFind, L: int) -> tuple[float, float]: # returns (QG, S)
    """
    compute the spread of the cluster size (Q_G) - eq (6) and S form the paper
    https://arxiv.org/pdf/1610.00200
    """
    unique_roots = set()
    for i in range(L*L):
        unique_roots.add(uf.find(i))
    # square sum
    sq_sum = 0
    cube_sum = 0 
    for r in unique_roots:  # ideally compute all measurements here
        sq_sum += uf.size[r]**2
        cube_sum += uf.size[r]**4
    return cube_sum / (sq_sum ** 2), sq_sum / (L*L)