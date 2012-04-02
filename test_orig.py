#before

CONSTANT = 1

def req1():
	return 'old'

def req2():
	def ret():
		return 'old'
	return ret()

class Requirement(object):
	def __init__(self):
		self.val = 'old'

#implemented

class Foo(object):
	def __init__(self):
		self.val = 'old'
	
#after

#inheritance
class Inheritor1(Foo):
	def __init__(self):
		Foo.__init__(self)

class Inheritor2(Foo):
	def __init__(self):
		super(Inheritor2, self).__init__(self)

class Inheritor3(Foo):
	def __init__(self):
		super().__init__(self)

#methods
def user1():
	return Foo().val

#closure
def user2():
	def ret():
		return Foo().val
	return ret()
