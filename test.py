from zodiac import monkeypatch
monkeypatch('test_patch', 'test_orig')

import orig

assert orig.req1 == 'orig'

assert Foo().val == 'new'
assert Foo().req2() == 'new'
assert Foo().req3() == 'new'

assert orig.Inheritor1().val() == 'new'
assert orig.Inheritor2().val() == 'new'
assert orig.Inheritor3().val() == 'new'

assert user1() == 'new'
assert user2() == 'new'
