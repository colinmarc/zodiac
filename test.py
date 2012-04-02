from zodiac import monkeypatch
monkeypatch('test_patch', 'test_orig')

import test_orig as mod

assert mod.req1() == 'old'

assert mod.Foo().val == 'new'
assert mod.Foo().req2() == 'old'
assert mod.Foo().req3() == 'old'

assert mod.new1() == 'old'
assert mod.new2() == 'new'

assert mod.Inheritor1().val == 'new'
assert mod.Inheritor2().val == 'new'
assert mod.Inheritor3().val == 'new'

assert mod.user1() == 'new'
assert mod.user2() == 'new'
