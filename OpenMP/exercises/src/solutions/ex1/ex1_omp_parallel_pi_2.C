//---------------------------------------------------------------------
// This program is made to compute pi numerical value.
// It will numerically compute the integral of
//
//                   4/(1+x*x)
//
// from 0 to 1 using variable number of steps.
// The value of this integral is pi. The knowing of pi is quite 
// precise and the result can be compared to the "real" value.
//
// This parallel program uses omp parallel
// It uses a timer class defined in a separate header file.
//
// History: 
// Written by Gabriele Gaetano Fronzé, 01/18.
// Based on Tim Mattson implementation, 11/99.
//---------------------------------------------------------------------

#include "StopWatch.h"
#include <omp.h>
#include <iostream>
#include "common.h"
#include <vector>
#include <numeric>

int main()
{
    StopWatch stopWatch;

    double pi, sum = 0.0;
    double step = 1.0/(double) common::num_steps; //x-step
    int n_threads=1;

    std::vector<double> sums;

    #pragma omp parallel firstprivate(step)
    {
        n_threads = omp_get_num_threads();

        uint thread_id = omp_get_thread_num();
        
        #pragma omp single
            sums.resize(n_threads);

        for (unsigned long long i=thread_id; i<common::num_steps; i+=n_threads) {
            double x = (i - 0.5) * step; //computing the x value
            sums[thread_id] += 4.0 / (1.0 + x * x); //adding to the cumulus
        }
    }

    pi = step * std::accumulate(sums.begin(), sums.end(), 0.);

    common::print_results(pi,n_threads);

    return 0;
    
}
