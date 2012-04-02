
__target__ = 'orig'

__before__ = [
	'req1',
	'Requirement'
]

__implements = [
	'Foo',
	'new1',
	'new2'
]

__after__ = [
	'Inheritor1',
	'Inheritor2',
	'Inheritor3',
	'user1',
	'user2'
]

class Foo(_real.Foo):
	def __init__(self):
		self.val = 'new'

	def req2(self):
		return _real.req1()

	def req3(self):
		return _real.Requirement().val

def new1():
	return req1()

def new2():
	return Foo().val()
