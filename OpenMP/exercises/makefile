ifeq ($(OS),Windows_NT)
    CXX=.
else
    UNAME_S := $(shell uname -s)
    ifeq ($(UNAME_S),Linux)
        CXX=g++
    endif
    ifeq ($(UNAME_S),Darwin)
        CXX=g++
    endif
endif

CXX_FLAGS=-O3 -fopenmp -I./include

$(shell mkdir -p bin)

all : sequential omp_parallel_pi omp_parallel_for_pi omp_sections omp_single omp_hello_world omp_hello_world_printf

sequential : src/ex0_reference_sequential_pi.C
	$(CXX) $(CXX_FLAGS) src/ex0_reference_sequential_pi.C -o ./bin/reference_sequential_pi

omp_parallel_pi : src/ex1_omp_parallel_pi.C
	$(CXX) $(CXX_FLAGS) src/ex1_omp_parallel_pi.C -o ./bin/omp_parallel_pi

omp_parallel_for_pi : src/ex2_omp_parallel_for_pi.C
	$(CXX) $(CXX_FLAGS) src/ex2_omp_parallel_for_pi.C -o ./bin/omp_parallel_for_pi

omp_hello_world : src/ex3_hello_world.C
	$(CXX) $(CXX_FLAGS) src/ex3_hello_world.C -o ./bin/omp_hello_world

omp_hello_world_printf : src/ex3_hello_world_printf.C
	$(CXX) $(CXX_FLAGS) src/ex3_hello_world_printf.C -o ./bin/omp_hello_world_printf

omp_sections : src/ex4_omp_sections.C
	$(CXX) $(CXX_FLAGS) src/ex4_omp_sections.C -o ./bin/omp_sections

omp_single : src/ex4_omp_single.C
	$(CXX) $(CXX_FLAGS) src/ex4_omp_single.C -o ./bin/omp_single

clean : 
	rm -rf ./bin/*