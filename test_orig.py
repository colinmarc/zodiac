import sys

CONSTANT = 1

#existing
def req1():
	return 'old'

def req2():
	def ret():
		return 'old'
	return ret()

class Requirement(object):
	def __init__(self):
		self.val = 'old'

class Foo(object):
	def __init__(self):
		self.val = 'old'
	
#inheritance
class Inheritor1(Foo):
	def __init__(self):
		super(Inheritor1, self).__init__()

class Inheritor2(Foo):
	def __init__(self):
		Foo.__init__(self)

if sys.version_info[0] >= 3:
	class Inheritor3(Foo):
		def __init__(self):
			super().__init__()
else:
	Inheritor3 = Inheritor2

#methods
def user1():
	return Foo().val

#closure
def user2():
	def ret():
		return Foo().val
	return ret()
