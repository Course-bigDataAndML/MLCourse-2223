//---------------------------------------------------------------------
// This simple class wraps around std::chrono::high_resolution_clock().
// It uses a standard destructor to print data whenever out-of-scope.
// use it by creating a StopWatch object in the scope you want to measure
//
// History: 
// Written by Gabriele Gaetano Fronzé, 01/18.
//---------------------------------------------------------------------

#include <chrono>
#include <iostream>

using namespace std::chrono;

class StopWatch{
    
public:
    StopWatch(){
        start = high_resolution_clock::now();
    }

    ~StopWatch(){
        std::cout << "Elapsed time: " << (duration_cast<duration<double> >(high_resolution_clock::now() - start)).count() << " seconds." << std::endl;
    }

private:
    high_resolution_clock::time_point start;
};
