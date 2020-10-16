from binascii import b2a_hex
from hmac import HMAC

try:
    from uhashlib import sha256, sha1
    import ngu
    sha512 = ngu.hash.sha512
except ImportError:
    from hashlib import sha256, sha1, sha512

hmac_sha1 = lambda key, msg=None: HMAC(key, msg, sha1, (20, 64)).digest()
hmac_sha256 = lambda key, msg=None: HMAC(key, msg, sha256, (32, 64)).digest()
hmac_sha512 = lambda key, msg=None: HMAC(key, msg, sha512, (64, 128)).digest()

assert b2a_hex(hmac_sha1(b'ab'*16, b'hello')) == b'6ffb8c2e3e85677f02913c480a44486018db0552'
assert b2a_hex(hmac_sha256(b'ab'*16, b'hello')) == b'254ac1adfb14b1de23b5bfc5d1a7d2a0ca0ebcdc2676fed0b81b121912ce6a67'
assert b2a_hex(hmac_sha512(b'ab'*16, b'hello')) == b'435c32af24b24c1c47257e5f055dccb743f732b0723a4ff014cdf0c9a8500b087e01a85033f0a109c5841c1362e783e0776e8e45f9c09c070025fa35fe9d8160'
