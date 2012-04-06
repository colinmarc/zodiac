zodiac - unite monkey and snake
=================================

zodiac makes monkeypatching really easy in python. It lets you weave parts of the original module with a patch module that you write. It was written for python 3, but also works in 2.7.

what?
----

let's say you are monkeypatching [socket][]. You can write a patch module, `mysocket.py`:

	import socket as _real

	class socket(_real.socket):
		def __init__(self, *args, **kwargs):
			print("passthrough!")
			super().__init__()

	def something_new():
		print("new function")

This lets you create a patched module based on the original module, with only the parts you want overridden.

	>>> from zodiac import build_patch
	>>> mysocket = build_patch('socket', 'mysocket')
	>>>	s = mysocket.socket()
	passthrough!
	>>> s
	<mysocket.socket object, fd=3, family=2, type=1, proto=0>

Other parts of the original module will also use your patch!

	>>> conn = mysocket.create_connection(('python.org', 9599))
	passthrough!

Patching globally is simple.

	>>> from zodiac import monkeypatch
	>>> monkeypatch('socket', 'mysocket')
	>>> import socket
	>>> s = socket.socket()
	passthrough!
	>>> socket.something_new()
	new function

Check out the tests for more examples. 

why is this different?
----------------------

The way monkeypatching is done currently in some projects involves a lot of reproduced code. Without zodiac, you could write a patch module similar to the one before, importing functions like `create_connection` from the system `socket` library to match the interface.

	import socket as _real
	create_connection = _real.create_connection #et cetera

	class socket(_real.socket):
		def __init__(self, *args, **kwargs):
			print("passthrough!")
			super().__init__()

But this breaks, because `create_connection` uses the socket class that was around when it was defined, and not ours:

	>>> import mysocket as socket
	>>> conn = mysocket.create_connection(('python.org', 9599))
	>>> #hm, no passthrough

So what these libraries do is copy the `create_connection` code wholesale from the system module, and don't change a thing. But by redefining it, it uses our socket:

	import socket as _real

	class socket(_real.socket):
		def __init__(self, *args, **kwargs):
			print("passthrough!")
			super().__init__()

	def create_connection(...):
		#copy pasta of python socket.create_connection code

This works, but ties you to the original code, but has obvious problems. You're tied to the original code, and maintaining between different versions of system code is a nightmare! zodiac "rebases" those functions that you would have to redefine into the namespace of the new module, which is populated with whatever you overrode in your patch. So your patches can be clean and concise.

installation
------------

zodiac requires python 2.7 or higher. Clone, cd into the directory, and then

    python setup.py install


[socket]: http://docs.python.org/py3k/library/socket.html

