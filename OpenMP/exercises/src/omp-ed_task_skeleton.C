//---------------------------------------------------------------------
// This brief file is the skeleton of any embarassingly parallel task.
// Such tasks can easily scale using OpenMP!
//
// History: 
// Written by Gabriele Gaetano Fronzé, 04/20.
//---------------------------------------------------------------------

// The main include: OpenMP header
#include <omp.h>

// Here are some includes needed by your software...
#include <iostream>
#include <unistd.h>
#include <array>
#include <vector>

#define inputClass int
#define outputClass int

outputClass myImpressiveFunction(inputClass input){
  outputClass out;

  sleep(1); // This is a sleep for 1 second, representing some real heavy tasks performed on the input!

  return out;
}

int main()
{
    // Here are some initializations
    // Assuming input size is known (200)
    std::array<inputClass, 200> inputdata;
    int max_steps = inputdata.size(); // This is 200, useful when using a variable size vector instead

    // Make sure the output is ready before starting.
    // OpenMP expects a C-like access pattern, so you must forget emplace and push back unles you know what you're doing
    std::vector<outputClass> outputdata;
    outputdata.resize(max_steps);

    // As easy as it sounds
    #pragma omp parallel for
    // Run your function on your data. This is a 1:1 mapping operation
    for (uint i=0; i<=max_steps; i++) {
        outputdata[i] = myImpressiveFunction(inputdata[i]);
    }

    // Do something with your output...
    
    return 0;
}
