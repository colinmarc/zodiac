import sys
import builtins
import imp

class MonkeyPatchingError(Exception):
	pass

def monkeypatch(source, dest):
	source_module = __import__(source)
	dest_module = __import__(dest)
	imports = getattr(source_module, '__imports__', [])
	implements = getattr(source_module, '__implements__', [])
	
	missing = set(dir(dest_module)) - set(dir(source_module)) - set(implements) - set(imports)
	if missing:
		error = "{0} items not implemented or imported: \n\t{1}"
		raise MonkeyPatchingError(error.format(len(missing), '\n\t'.join(missing)))

	setattr(dest_module, '__monkeypatched__', True)
	for name in imports:
		thing = getattr(source_module, name)
		if not thing:
			raise MonkeyPatchingError("invalid import: {0}".format(name))

		setattr(dest_module, name, thing)

	sys.modules[dest] = dest_module

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

	new_dict = {}
	for name, item in cls.__dict__:
		new_item = getattr(target, name, False)	
		if item:
			if isinstance(item, type):
				rebase_class(item, new_dict)
			elif isinstance(item, types.FunctionType)
				rebase_function(item, new_dict)
		else:
			new_dict[name] = item

	new_cls = type(new_name, new_bases, new_dict)

def build_patch():
	mod = imp.new_module(__target__)
	mod._real = __import__(__target__)
	
	for name in _real.__all__:
		val = getattr(_real, name)
		if isinstance(name, (int, str, bytes)):
			setattr(mod, name, val)

	for name in __before__:
		setattr(mod, name, getattr(_real, name))

	for name in __implements__:
		setattr(mod, name, globals()[name])
	
	for name in __after__:
		obj = getattr(_real, name)

		if isinstance(obj, types.FunctionType):

		setattr(mod, name, obj)

	return mod

def diff(source, dest):
	pass

def test(name, test_name=None):
	pass
	
