import multiprocessing as mp
from typing import Tuple, List
from functools import partial
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
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
    # X = floor( ln(u) / ln(1-p) ),  i.e. P(X=k) = (1-p)^k * p # floor since +1 in loop
    # floor for X in N_0
    # ceil for X in N (better choice)
    return math.floor(math.log(u) / math.log(1 - p))


def lr_percolation_2D(L: int,
                      alpha: float, 
                      beta: float, 
                      seed: int=None) -> UnionFind:
    """
    2D long-range percolation with skip-based sampling.
    Probability p_l = min(1, beta / l^(2 + alpha)).
    
    Returns a UnionFind object describing the clusters.
    """
    # Create a dedicated random number generator with the specified seed
    rng = random.Random(seed)
    
    uf = UnionFind(L*L)
    
    def idx(x, y):
        return x*L + y
    
    for dx in range(L):
        for dy in range(L):
            if dx == 0 and dy == 0:
                continue
            # TODO: could implement the L^p norm sampling
            # TODO: could this be implemented in a "generic way" for arbitrary d's
            wrap_x = min(dx, L - dx)
            wrap_y = min(dy, L - dy)
            # dist = math.sqrt(wrap_x**2 + wrap_y**2) # euclidean
            # dist = max(abs(wrap_x), abs(wrap_y))  # l infinity
            dist = abs(wrap_x) + abs(wrap_y)  # l 1 distance
            if dist < 1e-12:
                continue
            
            p = beta / (dist**(2.0 + alpha))  # need to handle
            if p > 1.0:
                p = 1.0
            
            i = 0
            while i < L*L:
                step = geometric_skip(p, rng)
                i += step
                if i >= L*L:
                    break
                
                x1, y1 = divmod(i, L)
                x2 = (x1 + dx) % L
                y2 = (y1 + dy) % L
                uf.union(i, idx(x2, y2))
                
                i += 1
    return uf

def Q_G(uf: UnionFind, L: int) -> tuple[float, float]: # returns (QG, S)
    """
    compute the spread of the cluster size
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


def single_mc_sample(L: int, sigma: float, beta: float, seed: int=None) -> tuple[float, float]:
    """
    Run a single Monte Carlo sample and return Q_G and S values
    """
    uf = lr_percolation_2D(L, sigma, beta, seed=seed)
    q_g, s = Q_G(uf, L)
    return q_g, s


def mc_sum_of_squares(L: int,
                      sigma: float, 
                      beta: float, 
                      n_samples: int=10, 
                      seed: int=None,
                      show_progress: bool=False
) -> tuple[float, float]:
    """
    Monte Carlo estimate of the expectation of
      (1/(L*L)) * sum_{r in roots} (size[r])^2
    across n_samples independent LR percolation configurations.
    
    Returns (mean_value, list_of_values).
    """
    q_g_samples = np.zeros(n_samples)
    s_samples = np.zeros(n_samples)
    
    #  show progress
    sample_range = tqdm(range(n_samples), desc=f"L={L}, β={beta:.4f} samples", leave=False) if show_progress else range(n_samples)
    
    for i in sample_range:
        # use a different seed for each sample 
        sample_seed = None if seed is None else seed + i
        q_g, s = single_mc_sample(L, sigma, beta, seed=sample_seed)
        q_g_samples[i] = q_g
        s_samples[i] = s
    
    q_g_mean = np.average(q_g_samples)
    s_mean = np.average(s_samples)
    return q_g_mean, s_mean


def process_single_beta(args):
    """
    Process a single beta value and return results
    passing args for interop with parallel function
    """
    beta, L, sigma, num_samples, seed = args
    qg, s = mc_sum_of_squares(L, sigma, beta,
                             n_samples=num_samples,
                             seed=seed)
    return beta, qg, s


def process_L_values_parallel(L: int, 
                              sigma: float, 
                              betas: List[float],
                              num_samples: int, 
                              base_seed: int=42) -> Tuple[List[float], List[float], List[float]]:
    """Process all beta values for a given L in parallel with progress bar"""
    # Create arguments with unique seeds for each beta value
    args_list = [(beta, L, sigma, num_samples, base_seed + i) for i, beta in enumerate(betas)]
    
    # Create a pool of workers
    with mp.Pool(processes=mp.cpu_count()) as pool:
        results = list(tqdm(
            pool.imap(process_single_beta, args_list), 
            total=len(betas),
            desc=f"Processing L={L}",
            leave=True
        ))
    
    results.sort(key=lambda x: x[0])  # results by beta to ensure correct order
    
    betas_out, qgs, ss = zip(*results)
    
    return list(betas_out), list(qgs), list(ss)


if __name__ == "__main__":
    # Set a global seed for reproducibility
    global_seed = np.random.randint(2**32 - 1) # change to non-random if needed for debugging
    np.random.seed(global_seed)
    random.seed(global_seed)
        
    # List of different L values (side lengths of torus)
    L_values = [50, 100, 200]  
    alpha = 10
    num_samples = 100  # number of Monte Carlo samples
        
    # Setup the plot
    plt.figure(figsize=(10, 6))
    colors = ['blue', 'red', 'green', 'purple', 'orange']  # Colors for different L values
        
    # 1. Run for different L values:
    betas = list(np.arange(0.01 , 0.5, 0.01))
        
    # Create overall progress bar for L values
    for i, L in enumerate(tqdm(L_values, desc="Overall progress", position=0)):
        print(f"\nProcessing L = {L}...")
        
        # Use a different seed derived from global_seed for each L value
        L_seed = global_seed + (i * 1000)
        
        _, qgs, ss = process_L_values_parallel(L, alpha, betas, num_samples, base_seed=L_seed)
        
        # Plot results
        plt.plot(betas, qgs, color=colors[i % len(colors)], linestyle='-', linewidth=1)
        plt.scatter(betas, qgs, s=10, color=colors[i % len(colors)], label=f'L = {L}')
        
    # Add legend, labels, and title
    plt.legend(loc='best')
    plt.xlabel('Beta')
    plt.ylabel('qg')
    plt.title(f'Results for Different L Values (Seed: {global_seed}), alpha={alpha}')
    plt.grid(True, alpha=0.3)
        
    # Save the plot with the seed in the filename
    plt.savefig(f'percolation_results_seed_{global_seed}_alpha_{alpha}.png')
    plt.show()