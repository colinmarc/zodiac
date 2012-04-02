import sys
import builtins
import imp

class MonkeyPatchingError(Exception):
	pass

def rebase_function(f, target, new_name=None):
	if not new_name:
		new_name = f.__name__

	ns = {'__builtins__': builtins}
	ns.update(target.__dict__)

	new_f = types.FunctionType(
		f.__code__,
		ns,
		new_name,
		f.__defaults__,
		f.__closure__
	)

	setattr(target, new_name, new_f)

def rebase_class(cls, target, new_name=None):
	if not new_name:
		new_name = cls.__name__

	new_bases = []
	for base in cls.__bases__:
		new_base = getattr(target, base.__name__, False)
		if new_base and isinstance(new_base, type):
			new_bases.append(new_base)
		else:
			new_bases.append(base)

	new_cls = type(new_name, new_bases, dict())

	for name, item in cls.__dict__:
		rebase(item, new_cls, name)

def rebase(obj, target, new_name=None):
	if not new_name:
		new_name = obj.__name__

	if isinstance(obj, type):
		rebase_class(obj, target, new_name)
	elif isinstance(obj, types.FunctionType):
		rebase_function(obj, target, new_name)
	else:
		setattr(target, new_name, obj) 

def build_patch():
	mod = imp.new_module(__target__)
	mod._real = __import__(__target__)
	
	for name in _real.__all__:
		val = getattr(_real, name)
		if isinstance(name, (int, str, bytes)):
			setattr(mod, name, val)

	for name in __before__:
		rebase(getattr(_real, name), mod, name)

	for name in __implements__:
		setattr(mod, name, globals()[name])
	
	for name in __after__:
		obj = getattr(_real, name)
		rebase(obj, mod, name)

	return mod

hidden_modules = {}

def replace_module(name, replacement):
	real = sys.modules.get(name, False)
	if real:
		hidden_modules[name] = real

	sys.modules[name] = dest_module

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
	
