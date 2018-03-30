import heap 

def maximum(l, n):
	max_index = 0

	for x in range(1, n+1):
		if (l[x] > l[max_index]):
			max_index = x

	return max_index 

def swap(l, n1, n2):
	l[n1], l[n2] = l[n2], l[n1]

def selection_sort(l):
	n = len(l) - 1
	while n > 0:
		max_index = maximum(l, n)
		swap(l, n, max_index)
		n -= 1

def insertion_sort(l):
	for i in range(len(l)):
		j = i - 1
		while (j >= 0 and l[j] < l[i]):
			j -= 1
		if (l[j] < l[i]):
			swap(l, i, j)

def merge(l1, l2):
	l = []
	i = 0
	j = 0

	while (i < len(l1) and j < len(l2)):
		if (l1[i] < l2[j]):
			l.append(l1[i])
			i += 1
		else:
			l.append(l2[j])
			j += 1
	
	return l + l1[i:] + l2[j:] #syntactic sugar

def mergesort(l):
	if (len(l) <= 1):
		return l
	m = len(l)//2
	left = mergesort(l[:m])
	right = mergesort(l[m:])
	return merge(left, right)

def quicksort(l):
	_quicksort(l, 0, len(l) - 1)

def _quicksort(l, start, end):
	if (start >= end):
		return

	start_lesser = start
	pivot = start

	for x in range (start + 1, end + 1):
		if (l[x] < l[pivot]):
			start_lesser += 1
			if (x != start_lesser):
				swap(l, x, start_lesser)

	if (pivot != start_lesser):
		swap(l, pivot, start_lesser)

	_quicksort(l, start, start_lesser - 1)
	_quicksort(l, start_lesser + 1, end)

def comp(elem1, elem2):
	if elem1 > elem2:
		return -1
	elif elem1 == elem2:
		return 0
	else:
		return 1

def heapsort(l):
	heap.MaxHeap(comp, l).heapsort()
	return l

if __name__ == '__main__':
	l = [10,2,1,6,7,7,15,4,4,3,9]
	heapsort(l)
	print(l)
