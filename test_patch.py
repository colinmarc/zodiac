import test_orig as _real

class Foo(_real.Foo):

	def __init__(self):
		self.val = 'new'

	def req2(self):
		return _real.req1()

	def req3(self):
		return _real.Requirement().val

def new1():
	return _real.req1()

def new2():
	return Foo().val

