def maximum(l, n):
	max_index = 0

	for x in range(1, n+1):
		if (l[x] > l[max_index]):
			max_index = x

	return max_index 

def swap(l, n1, n2):
	l[n1], l[n2] = l[n2], l[n1]

def insertion_sort(l):
	n = len(l) - 1
	while n > 0:
		max_index = maximum(l, n)
		swap(l, n, max_index)
		n -= 1

def selection_sort(l):
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