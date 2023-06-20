#include <iostream>

namespace common {
    const unsigned long long num_steps = 500000000; //number of x bins

    void print_results(double pi, int n_threads){
            printf("Pi value: %.20f\n Number of steps: %llu\n Number of threads: %d\n",pi,num_steps,n_threads);
    }
}