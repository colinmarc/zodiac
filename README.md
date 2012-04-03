zodiac - unite monkey and snake
=================================

zodiac makes monkeypatching really easy in python 2.7-3.x. It lets you weave parts of the original module with a patch module that you write.

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

You can create a patched module with just the parts you want overridden.

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
	>>> socket.mycrazyfunction()
	new function

Check out the tests for more examples. 

[socket]: http://docs.python.org/py3k/library/socket.html

