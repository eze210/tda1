CXX = g++
CXXFLAGS= -std=c++11 -Wall -Werror -pedantic -pedantic-errors
DBG_FLAGS= -O0 -ggdb -DDEBUG -fno-inline
OPT_FLAGS= -O3 -g0

.PHONY: all clean

objects=$(patsubst %.cpp,%.o,$(wildcard *.cpp))

all: $(objects)
	$(CXX) $(CXXFLAGS) $(OPT_FLAGS) $(objects) -o heap
	chmod +x heap

gdb: $(objects)
	$(CXX) $(CXXFLAGS) $(DBG_FLAGS) $(objects) -o heap
	chmod +x heap

clean:
	rm $(objects) heap
