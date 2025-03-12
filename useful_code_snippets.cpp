#include <bits/stdc++.h>
#include "pcg_random.hpp"
#include "rng.cpp"
#include "position2d.cpp"

// ----------------------- POSITION SAMPLING 2D -----------------------
inline Position2D get_next_pos_2D_infL(const Position2D& curr_pos, rngWrapper& RNG, int r) {
     // Total number of possible vectors with L-infty norm r in 2D
    size_t total_vectors = 8 * r;

    // Generate a random index in [0, total_vectors - 1]
    size_t k = RNG.generate_int(total_vectors);

    int x, y;
    // Determine which quadrant or axis the vector falls into
    if (k < 2 * (2 * r + 1)) {
        // Case 1: x = r or x = -r
        // Each has (2r + 1) possible y values from -r to r
        int sign = (k < (2 * r + 1)) ? 1 : -1;
        y = -r + static_cast<int>(k % (2 * r + 1));
        x = sign * r;
    }
    else {
        // Case 2: y = r or y = -r
        // Each has (2r - 1) possible x values from -r + 1 to r - 1
        k -= 2 * (2 * r + 1);
        int sign = (k < (2 * r - 1)) ? 1 : -1;
        x = -r + 1 + static_cast<int>(k % (2 * r - 1));
        y = sign * r;
    }

    return {curr_pos.x + x, curr_pos.y + y};
}