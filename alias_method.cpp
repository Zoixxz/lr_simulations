#include <bits/stdc++.h>
#include <gmp.h>
#include <gmpxx.h>
#include <mpfr.h>
#include "rng.cpp"

// ----------------------- ALIAS METHOD -----------------------
constexpr int PREC = 32*7; // precision in bits

struct AliasTable {
    std::vector<double> prob;
    std::vector<int> alias;
};

// the sum needs to be high precision here, because it requires a much larger number of significant digits than the individual properties, which can be treated as doubles later
AliasTable build_alias_table(double exponent, int r_max) {
    // Initialize the sum of probabilities with high precision
    mpf_class prob_sum(0.0, PREC);
    std::vector<mpf_class> high_prec_probs(r_max);

    // Initialize MPFR variable
    mpfr_t term;
    mpfr_init2(term, PREC);

    // Compute high precision probabilities
    for(int r = 1; r <= r_max; r++) {
        mpfr_set_ui(term, r, MPFR_RNDN);                  
        mpfr_log(term, term, MPFR_RNDN);              
        mpfr_mul_d(term, term, -exponent, MPFR_RNDN);    
        mpfr_exp(term, term, MPFR_RNDN);         
        
        mpf_class prob;                         
        mpfr_get_f(prob.get_mpf_t(), term, MPFR_RNDN);   

        prob_sum += prob;                      
        high_prec_probs[r - 1] = prob;
    }

    // Clear MPFR variable after usage
    mpfr_clear(term);

    // Normalize probabilities and scale by r_max
    for(int i = 0; i < r_max; i++) {
        high_prec_probs[i] /= prob_sum;
        high_prec_probs[i] *= static_cast<double>(r_max);
    }

    // Cast high precision probabilities to double
    std::vector<double> scaled_p(r_max);
    for(int i = 0; i < r_max; i++) {
        scaled_p[i] = high_prec_probs[i].get_d();
    }

    // Initialize alias table
    AliasTable at;
    at.prob.resize(r_max, 0.0);
    at.alias.resize(r_max, 0);

    // Initialize small and large lists as vectors of indices
    std::vector<int> small;
    std::vector<int> large;

    // Classify probabilities into small and large
    for(int i = 0; i < r_max; i++) {
        if(scaled_p[i] < 1.0) {
            small.push_back(i);
        } else {
            large.push_back(i);
        }
    }

    // Alias method algorithm
    while(!small.empty() && !large.empty()) {
        int l = small.back();
        small.pop_back();

        int g = large.back();
        large.pop_back();

        at.prob[l] = scaled_p[l];
        at.alias[l] = g;

        scaled_p[g] -= (1.0 - at.prob[l]);

        if(scaled_p[g] < 1.0) {
            small.push_back(g);
        } else {
            large.push_back(g);
        }
    }

    // Assign remaining probabilities
    while(!large.empty()) {
        int g = large.back();
        large.pop_back();
        at.prob[g] = 1.0;
        at.alias[g] = g;
    }

    while(!small.empty()) {
        int l = small.back();
        small.pop_back();
        at.prob[l] = 1.0;
        at.alias[l] = l;
    }

    return at;
}

inline int sample_r(const AliasTable& at, rngWrapper& RNG, int r_max) {
    // Sample r using the alias method
    int i = RNG.generate_int(r_max);
    double u = RNG.generate_double();

    int r;
    if(u < at.prob[i]) {
        r = i + 1;
    } else {
        r = at.alias[i] + 1;
    }

    return r;
}