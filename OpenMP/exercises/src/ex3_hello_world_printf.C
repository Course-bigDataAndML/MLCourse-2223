//---------------------------------------------------------------------
// Super basic OpenMP Hello world!
//
// History: 
// Written by Gabriele Gaetano Fronzé, 04/20.
//---------------------------------------------------------------------

#include <omp.h>
#include <cstdio>

int main() {
  printf("Hey there! Running with %d threads...\n\n", omp_get_max_threads());
  
  #pragma omp parallel
  {
    printf("Hello from thread %d!\n", omp_get_thread_num());
  }  
}