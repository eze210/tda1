#ifndef HEAP_H_
#define HEAP_H_

#include <vector>
#include <ostream>

template <typename T> class Heap {
public:
	typedef uint64_t index_t;

	typedef enum {
		MinHeap,
		MaxHeap
	} HeapType;

	/** Shoud return:
	 *		- a negative number if t1 < t2
	 *		- a positive number if t1 > t2
	 *		- zero if t1 == t2
	 */
	typedef int (*ComparisonCallback)(const T &t1, const T &t2); 

	Heap(HeapType type = MinHeap, ComparisonCallback cmp = defaultComparisonCallback) :
		type(type),
		compare(cmp) {
	}

	Heap<T> &operator<<(const T &element) {
		index_t newElementIndex = vector.size();
		vector.push_back(element);
		if (newElementIndex > 0)
			upheap(newElementIndex);

		return *this;
	}

	Heap<T> &operator>>(T &element) {
		element = vector[0];
		vector[0] = vector.back();
		vector.pop_back();
		downheap(0);
		return *this;
	}

	friend std::ostream& operator<<(std::ostream& os, const Heap<T>& heap) {
		size_t numberOfElementsInCurrentLevel = 0;
		size_t maxElementsInCurrentLevel = 1;
		for (const T &elem : heap.vector) {
			os << elem << " ";
			++numberOfElementsInCurrentLevel;
			if (numberOfElementsInCurrentLevel == maxElementsInCurrentLevel) {
				os << "\n";
				numberOfElementsInCurrentLevel = 0;
				maxElementsInCurrentLevel *= 2;
			}
		}
		return os;
	}

	bool isEmpty() {
		return vector.empty();
	}

	size_t size() {
		return vector.size();
	}

	const T& top() {
		return vector[0];
	}

	void heapify() {
		/* idx MUST be signed to make break condition false */
		for (int64_t idx = size() - 1; idx >= 0; --idx) 
			downheap(idx);
	}

	static void heapsort(std::vector<T> &vector, HeapType type=MinHeap) {
		Heap<T> auxHeap(vector, type);
		size_t numElems = auxHeap.size();
		for (size_t i = 0; i < numElems; ++i) {
			auxHeap >> vector[i];
		}
	}


private:
	std::vector<T> vector;

	HeapType type;

	ComparisonCallback compare;

	static index_t leftChild(index_t i) {
		return 2 * i + 1;
	}

	static index_t rightChild(index_t i) {
		return 2 * i + 2;
	}
	
	static index_t parent(index_t i) {
		return (i - 1) / 2;
	}

	void swapElems(index_t index1, index_t index2) {
		T aux = vector[index1];
		vector[index1] = vector[index2];
		vector[index2] = aux;
	}

	index_t downHeapChildIdx(index_t parent) {
		index_t left = leftChild(parent),
				right = rightChild(parent);

		/* there is only one child */
		if (right >= size())
			return left;

		if (type == MinHeap)
			return (compare(vector[left], vector[right]) <= 0) ? left : right;
		else
			return (compare(vector[left], vector[right]) >= 0) ? left : right;
	}

	bool doSatisfyInvariant(index_t idx1, index_t idx2) {
		index_t parent = idx1 < idx2 ? idx1 : idx2;
		index_t child = idx1 > idx2 ? idx1 : idx2;

		if (type == MinHeap)
			return (compare(vector[parent], vector[child]) <= 0);
		else
			return (compare(vector[parent], vector[child]) >= 0);
	}

	void upheap(index_t i) {
		if (i == 0)
			return;

		index_t parentIndex = parent(i);
		if (!doSatisfyInvariant(i, parentIndex)) {
			swapElems(i, parentIndex);
			upheap(parentIndex);
		}
	}

	bool isLeaf(index_t i) {
		return (rightChild(i) >= size() && leftChild(i) >= size());
	}

	void downheap(index_t i) {
		if (isLeaf(i))
			return;
		index_t toSwap = downHeapChildIdx(i);

		if (!doSatisfyInvariant(toSwap, i)) {
			swapElems(i, toSwap);
			downheap(toSwap);			
		}
	}

	Heap(std::vector<T> &data,
		 HeapType type = MinHeap,
		 ComparisonCallback cmp = defaultComparisonCallback) :
		vector(data),
		type(type),
		compare(cmp) {
		heapify();
	}

	static int defaultComparisonCallback(const T &t1, const T &t2) {
		if (t1 < t2)
			return -1;

		else if (t2 < t1)
			return 1;

		else
			return 0;
	}
};

#endif
