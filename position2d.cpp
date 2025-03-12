#include <bits/stdc++.h>

constexpr double NORM_P = std::numeric_limits<double>::infinity();

struct Position2D {
    int x;
    int y;

    bool operator==(const Position2D& other) const {
        return x == other.x && y == other.y;
    }

    bool operator!=(const Position2D& other) const {
        return !(*this == other);
    }
};

inline double norm_2D(const Position2D& pos) {
    if (NORM_P == std::numeric_limits<double>::infinity()) {
        return static_cast<double>(std::max(std::abs(pos.x), std::abs(pos.y)));
    }

    double sum = 0.0;
    sum += std::pow(std::abs(static_cast<double>(pos.x)), NORM_P);
    sum += std::pow(std::abs(static_cast<double>(pos.y)), NORM_P);
    return std::pow(sum, 1.0 / NORM_P);
}