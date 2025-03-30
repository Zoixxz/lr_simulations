import math
import random
from union_find import UnionFind

def geometric_skip(p: float, rng: random.Random) -> int:
    """
    Return the number of failures before the first success,
    for a Bernoulli(p) RV
    
    p >= 1 => skip=0 (always success).
    p <= epsilon => skip=large (never success).
    Otherwise uses log-based approach for a geometric distribution.
    
    Uses the provided random number generator for reproducibility.
    """
    if p >= 1.0:
        return 0
    if p <= 1e-15: # epsilon cutoff  (floating point shenanigans)
        return 10**10  # effectively 'infinite'
    u = rng.random()
    # X = floor( ln(u) / ln(1-p) ),  i.e. P(X=k) = (1-p)^k * p
    return int(math.floor(math.log(u) / math.log(1 - p)))


def lr_percolation_2D(N: int,
                      alpha: float, 
                      beta: float, 
                      seed: int=None) -> UnionFind:
    """
    2D long-range percolation with skip-based sampling.
    Probability p_l = min(1, beta / l^(2 + alpha)).
    
    Returns a UnionFind object describing the clusters.
    """
    # dedicated RNG /w specified seed
    rng = random.Random(seed)
    
    uf = UnionFind(N*N)
    
    def idx(x, y):
        return x*N + y
    
    for dx in range(N):
        for dy in range(N):
            if dx == 0 and dy == 0:
                continue
            
            wrap_x = min(dx, N - dx)
            wrap_y = min(dy, N - dy)
            # dist = math.sqrt(wrap_x**2 + wrap_y**2) # euclidean
            # dist = max(abs(wrap_x), abs(wrap_y))  # l infinity
            dist = abs(wrap_x) + abs(wrap_y)  # l 1 distance
            if dist < 1e-12:
                continue
            
            p = beta / (dist**(2.0 + alpha))  # need to handle
            if p > 1.0:
                p = 1.0
            
            i = 0
            while i < N*N:
                step = geometric_skip(p, rng)
                i += step
                if i >= N*N:
                    break
                
                x1, y1 = divmod(i, N)
                x2 = (x1 + dx) % N
                y2 = (y1 + dy) % N
                uf.union(i, idx(x2, y2))
                
                i += 1
    return uf