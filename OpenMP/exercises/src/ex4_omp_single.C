#include "StopWatch.h"
#include <omp.h>
#include <iostream>
#include <thread>
#include <chrono>

using namespace std::chrono;

#define MAX omp_get_max_threads()

int main(){
    StopWatch stopwatch;
    
    const long maxIteration = 100000;
    bool debug_output=true;

    // This is needed to allow the presence of a parallel for nested in another parallel region
    omp_set_nested(1);

    int outputCounter = 0;
    bool done = false;

    #pragma omp parallel shared(outputCounter,done) num_threads(2)
    {
        #pragma omp master
        {
            if ( omp_get_thread_num()==0 ){ 
                if(debug_output) printf("monitor th_id: %d, n_th: %d\n",omp_get_thread_num(), omp_get_num_threads());
                while(!done){
                    printf("%d/%ld\r",outputCounter,maxIteration);
                    std::this_thread::sleep_for (microseconds(50));
                }
                printf("%d/%ld\n",outputCounter,maxIteration);
            }
        }

        #pragma omp single nowait
        {
            if(debug_output) printf("computing th_id: %d, n_th: %d\n",omp_get_thread_num(), omp_get_num_threads());
            #pragma omp parallel for num_threads(MAX)
            for( int i=0; i<maxIteration; i++){
                // This sleep emulates some heavy computation... Feel free to add yours!
                std::this_thread::sleep_for (microseconds(1000));

            #pragma omp atomic update
                    outputCounter++;
            }
        }
        done = true;
    }

    return 0;
}