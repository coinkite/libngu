try:
    # Desktop: make test vectors
    from ecdsa import SigningKey
    from ecdsa.util import sigencode_string
    from ecdsa.curves import SECP256k1, BRAINPOOLP256r1, NIST256p
    from hashlib import sha256

    with open('test_ec_gen.py', 'wt') as fd:
        print("import gc, ngu  # auto-gen", file=fd)
        print("for i in range(3):", file=fd)

        pks = [ b'\x55'*32, b'\x0f'+(b'\xff'*31)]
        md = b'MSG1'*8
        for pk in pks:
            for name, c in [ ('SECP256K1', SECP256k1), 
                                ('BP256R1', BRAINPOOLP256r1), 
                                ('NIST_P256', NIST256p) ]:
                
                print('  print("test: %s sign")' % name, file=fd)
                print('  cur = ngu.ec.curve(ngu.ec.%s)' % name, file=fd)

                key = SigningKey.from_string(pk, curve=c, hashfunc=sha256)
                sig = key.sign_digest_deterministic(md, hashfunc=sha256, sigencode=sigencode_string)

                print('  assert cur.sign(%r, %r) == %r' % (pk, md, sig), file=fd)

                pub = key.get_verifying_key().to_string()
                print('  print("test: %s verify")' % name, file=fd)
                print('  assert cur.verify(%r, %r, %r) == True' % (b'\x04'+pub, sig, md), file=fd)
                print('  assert cur.verify(%r, %r, %r) == False' % (b'\x04'+pub, sig[0:-2]+bytes(2), md), file=fd)

                print('  del cur', file=fd)

        print("  gc.collect()", file=fd)
        print("print('PASS - %s')" % fd.name, file=fd)
        print("run code now in: %s" % fd.name)

    import sys
    sys.exit(0)
except ImportError: 
    pass

# Embedded tests

import gc
import ngu

names = [i for i in dir(ngu.ec) if i[0].isupper() and i[0].isalpha]
#print("Curves: " + ', '.join(names))
assert len(names) == 3

# instance each one
for n in names:
    grp = ngu.ec.curve(getattr(ngu.ec, n))
    del grp
    gc.collect()

try:
    ngu.ec.curve(3847)
    assert False
except RuntimeError:
    pass

try:
    ngu.ec.curve(ngu.ec.SECP256K1).verify('\x04'*65, bytes(64), bytes(32))
except ValueError as exc:
    assert 'pubkey vs. curve' in str(exc)

print('PASS - test_ec')
