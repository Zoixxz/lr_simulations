#include <bits/stdc++.h>
#include "position2d.cpp"

inline size_t pos_index_2D(const Position2D& pos, const int L_real) {
    return static_cast<size_t>(pos.x + L_real)
         + static_cast<size_t>(pos.y + L_real) * (2ULL * L_real + 1ULL);
}

inline void set_visited_2D(std::vector<uint8_t>& visited, const Position2D& pos, const int L_real) {
    const size_t index = pos_index_2D(pos, L_real);
    const size_t byte_index = index >> 3;  
    const uint8_t bit_mask = static_cast<uint8_t>(1U << (index & 7U));
    visited[byte_index] |= bit_mask;
}

inline void clear_visited_2D(std::vector<uint8_t>& visited, const Position2D& pos, const int L_real) {
    const size_t index = pos_index_2D(pos, L_real);
    const size_t byte_index = index >> 3; 
    const uint8_t bit_mask = static_cast<uint8_t>(~(1U << (index & 7U)));
    visited[byte_index] &= bit_mask;
}

inline bool is_visited_2D(const std::vector<uint8_t>& visited, const Position2D& pos, const int L_real) {
    const size_t index = pos_index_2D(pos, L_real);
    const size_t byte_index = index >> 3; 
    const uint8_t bit_mask = static_cast<uint8_t>(1U << (index & 7U));
    return (visited[byte_index] & bit_mask) != 0;
}

int L_real = 2 << 10; // whatever lattice size

// here is the hashmap
const size_t grid_size = static_cast<size_t>(2ULL * L_real + 1ULL) * (2ULL * L_real + 1ULL);
const size_t byte_size = (grid_size + 7ULL) >> 3;
std::vector<uint8_t> visited(byte_size, 0);