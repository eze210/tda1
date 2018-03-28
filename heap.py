
class MaxHeap(object):

	def __init__(self, comparison_callback, data = None):
		self.comparison_callback = comparison_callback
		self.data = data | []
		self.heapify()

	def heapify(self):
		for x in range ((self.size()//2) - 1, -1, -1):
			self.downheap(x)

	def add(self, elem):
		position = len(self.data);
		self.data.append(elem)
		self.upheap(position)

	def upheap(self, pos):
		if pos == 0:
			return

		parent_index = self.parent(pos)
		if not self.do_satisfy_invariant(pos, parent_index):
			self.data[pos], self.data[parent_index] = self.data[parent_index], self.data[pos]
			self.upheap(parent_index)

	def downheap_child_index(self, pos):
		left = self.left_child(pos)
		right = self.right_child(pos)

		if right >= self.size():
			return left;

		if self.comparison_callback(self.data[left], self.data[right]) >= 0:
			return left
		else:
			return right

	def downheap(self, pos):
		if self.is_leaf(pos):
			return
		to_swap = self.downheap_child_index(pos);

		if not self.do_satisfy_invariant(to_swap, pos):
			self.data[pos], self.data[to_swap] = self.data[to_swap], self.data[pos]
			self.downheap(to_swap);			

	def do_satisfy_invariant(self, idx1, idx2):
		parent = idx1 if idx1 < idx2 else idx2;
		child = idx1 if idx1 > idx2 else idx2;

		return (self.comparison_callback(self.data[parent], self.data[child]) >= 0);

	def top(self):
		return self.data[0]

	def pop(self):
		elem = self.data[0]
		if self.size() > 1:
			self.data[0] = self.data.pop()
			self.downheap(0)
		else:
			self.data.pop()
		return elem

	def parent(self, pos):
		return (pos - 1) // 2;

	def left_child(self, pos):
		return 2 * pos + 1

	def right_child(self, pos):
		return 2 * pos + 2

	def is_leaf(self, pos):
		return (self.right_child(pos) >= self.size()) and (self.left_child(pos) >= self.size())

	def size(self):
		return len(self.data)

	def _swap(self, n1, n2):
		self.data[n1], self.data[n2] = self.data[n2], self.data[n1]

	def __repr__(self):
		return repr(self.data)

def comp(elem1, elem2):
	if elem1 < elem2:
		return -1
	elif elem1 == elem2:
		return 0
	else:
		return 1

if __name__ ==  '__main__':
	h = MaxHeap(comp)
	h.add(1)
	h.add(2)
	h.add(3)
	h.add(4)
	h.add(1)
	h.add(2)
	h.add(1)
	h.add(3)
	h.add(4)

	while h.size() > 0:
		print(h.pop())

