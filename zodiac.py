import sys
import builtins
import types
import imp

class MonkeyPatchingError(Exception):
	pass

def _create_closure_cell(obj):
	def ret(): obj
	return ret.__closure__[0]

def rebase_function(f, target, new_name=None, ns=None):
	if not new_name:
		new_name = f.__name__
	ns = ns or dict()

	if f.__closure__:
		new_closure = []
		for c in f.__closure__:
			name = getattr(c.cell_contents, '__name__', False)
			if name and name in ns:
				new_closure.append(_create_closure_cell(ns[name]))
			else:
				new_closure.append(c)
		new_closure = tuple(new_closure)
	else:
		new_closure = f.__closure__

	new_f = types.FunctionType(
		f.__code__,
		ns,
		new_name,
		f.__defaults__,
		new_closure
	)

	setattr(target, new_name, new_f)

def rebase_class(cls, target, new_name=None, ns=None):
	if not new_name:
		new_name = cls.__name__
	ns = ns or dict()

	new_bases = []
	for base in cls.__bases__:
		new_base = getattr(target, base.__name__, False)
		if new_base and isinstance(new_base, type):
			new_bases.append(new_base)
		else:
			new_bases.append(base)
	new_bases = tuple(new_bases)

	new_cls = type(new_name, new_bases, dict())
	ns[new_name] = new_cls
	new_cls._my_class = new_cls

	for name, item in cls.__dict__.items():
		if name in ('__dict__', '__bases__', '__weakref__', '__name__', '__module__', '__doc__'): continue
		rebase(item, new_cls, name, ns)

	setattr(target, new_name, new_cls)

def rebase(obj, target, new_name=None, ns=None):

	if isinstance(obj, type):
		rebase_class(obj, target, new_name, ns)
	elif isinstance(obj, types.FunctionType):
		rebase_function(obj, target, new_name, ns)
	else:
		setattr(target, new_name, obj) 

def build_patch(patch):
	mod = imp.new_module(patch.__target__)
	mod.__builtins__ = builtins
	real = __import__(patch.__target__)
	
	for name in real.__dict__:
		if name.startswith('_'): continue

		val = getattr(real, name)
		if isinstance(name, (int, str, bytes)):
			setattr(mod, name, val)

	for name in patch.__before__:
		rebase(getattr(real, name), mod, name, mod.__dict__)

	for name in patch.__implements__:
		setattr(mod, name, getattr(patch, name))
	
	for name in patch.__after__:
		obj = getattr(real, name)
		rebase(obj, mod, name, mod.__dict__)

	return mod

hidden_modules = {}

def replace_module(name, replacement):
	real = sys.modules.get(name, False)
	if real:
		hidden_modules[name] = real

	sys.modules[name] = replacement

def restore_module(name):
	sys.modules[name] = hidden_modules[name]
	del hidden_modules[name]

def monkeypatch(source, dest):
	source_module = build_patch(__import__(source))
	replace_module(dest, source_module)

def diff(source, dest):
	pass

def test(name, test_name=None):
	pass
	
