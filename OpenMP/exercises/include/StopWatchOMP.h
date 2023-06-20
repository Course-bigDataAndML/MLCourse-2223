//---------------------------------------------------------------------
// This simple class wraps around omp_get_wtime().
// It uses a standard destructor to print data whenever out-of-scope.
// use it by creating a StopWatch object in the scope you want to measure
//
// History: 
// Written by Gabriele Gaetano Fronzé, 01/18.
//---------------------------------------------------------------------

#include <omp.h>
#include <iostream>

using namespace std::chrono;

class StopWatch{
    
public:
    StopWatch(){
        start = omp_get_wtime();
    }

    ~StopWatch(){
        std::cout << "Elapsed time: " << omp_get_wtime() - start << " seconds." << std::endl;
    }

private:
    double start;
};
