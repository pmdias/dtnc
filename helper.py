class Arc:
	def __init__(self, new_id):
		self.arc_id = new_id
		self.tail = 0 # Arc from
		self.head = 0 # Arc to
		self.lower = 0 # Arc lower capacity
		self.upper = 0 # Arc upper capacity
		self.cost = 0 # Arc cost

def new_name(s, index):
	return s + str(index)
