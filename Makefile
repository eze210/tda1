CC = g++

CFLAGS= --std=c++11 -Wall -Werror -pedantic
DBG_FLAGS= -O0 -ggdb
OPT_FLAGS= -O3 -g0

target:
	$(CC) $(CFLAGS) $(OPT_FLAGS) main.cpp -o heap
	chmod +x heap

gdb:
	$(CC) $(CFLAGS) $(DBG_FLAGS) main.cpp -o heap
	chmod +x heap

clean:
	rm heap
