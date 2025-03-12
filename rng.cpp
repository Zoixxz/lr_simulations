#include <bits/stdc++.h>
#include "pcg_random.hpp"

// ----------------------- RNG -----------------------
struct rngWrapper {
    using rng_type = pcg64_fast;
    rng_type rng;

    rngWrapper(uint64_t seed) : rng(seed) {}

    // Generate double in range [0, 1)
    inline double generate_double() {
        return (rng() >> 11) * (1.0 / (static_cast<double>(1ULL << 53)));
    }

    // Generate an int in range [0, n)
    inline size_t generate_int(size_t n) {
        return rng() % n;
    }
};