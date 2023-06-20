//---------------------------------------------------------------------
// Super basic OpenMP Hello world!
//
// History: 
// Written by Gabriele Gaetano Fronzé, 04/20.
//---------------------------------------------------------------------

#include <omp.h>
#include <iostream>

int main() {
  std::cout << "Hey there! Running with " << omp_get_max_threads() << " threads...\n\n";
  
  #pragma omp parallel
  {
    std::cout << "Hello from thread " << omp_get_thread_num() << "!\n";
  }  
}