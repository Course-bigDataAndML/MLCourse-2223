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
// This parallel version uses omp parallel for.
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

int main()
{
    StopWatch stopWatch;

    double pi, sum = 0.0;
    double step = 1.0/(double) common::num_steps; //x-step
    int n_threads=1;

    #pragma omp parallel 
    {
        n_threads = omp_get_num_threads()

        #pragma omp for
        for (unsigned long long i=1; i<=common::num_steps; i++) {
            double x = (i - 0.5) * step; //computing the x value
            sum += 4.0 / (1.0 + x * x); //adding to the cumulus
        }
    }

    pi = step * sum;

    common::print_results(pi, n_threads);
    
    return 0;
    
}
