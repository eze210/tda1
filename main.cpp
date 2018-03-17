#include "heap.h"
#include <iostream>

int elCuatroEsMuyChiquito(const int &t1, const int &t2) {
	if (t1 == t2)
		return 0;

	if (t1 == 4)
		return -1;

	if (t2 == 4)
		return 1;

	return t1 - t2;
}

int main() {
	Heap<int> heap(Heap<int>::MinHeap, elCuatroEsMuyChiquito);
	heap << 1;
	heap << 2;
	heap << 3;
	heap << 4;
	heap << 5;

	heap << 1;
	heap << 2;
	heap << 3;
	heap << 4;
	heap << 5;

	std::cout << heap << std::endl;
	
	while (!heap.isEmpty()) {
		int minimum;
		heap >> minimum;
		std::cout << "Current min: " << minimum << std::endl;
	}

	std::vector<int> unordered = {5,4 ,46 ,645 ,31 ,46 ,48 ,165 ,48};
	Heap<int>::heapsort(unordered, Heap<int>::MaxHeap);
	for (int elem : unordered) {
		std::cout << elem << " ";
	}
	std::cout << std::endl;
}
