"""Use bias780 after rejecting768's collision with historical high-word keys.

V1442 failed before output:normalized role8120/8140 collided with special numeric
status routes. Bias780 is disjoint for every historical/new admitted key. The
exact same3 memberships occupy180 of188 bytes;the gate uses168 of172 bytes.
"""
import inspect
from types import FunctionType
from keystone import Ks,KS_ARCH_ARM,KS_MODE_THUMB
from scripts import ship_loss_surrender_runtime_v1442 as previous
from scripts.ship_loss_surrender_runtime_v1442 import BASE,SOURCE,CONTRACTS,GATE,TABLE_BYTES,GATE_BYTES,NEW_KEYS,contract_rows

def rebased(fn,*args):
    source = inspect.getsource(fn)
    assert source.count('else 384')==1
    env = dict(previous.codec.__dict__)
    exec(compile(source.replace('else 384','else 780'),__file__,'exec'),env)
    return env[fn.__name__](*args)

def table():
    value = rebased(previous.codec.encode,contract_rows())
    rows,end = rebased(previous.codec.decode,value)
    assert rows==contract_rows() and end==len(value)==180
    return value+bytes(TABLE_BYTES-len(value))

def gate():
    _,assembly = previous.codec.gate()
    for old,new in [
        ('movs r7,#2\nlsls r7,r7,#8\nsubs r3,r3,r7','movs r7,#116\nsubs r3,r3,r7'),
        ('ready:\nsubs r3,#192\nsubs r3,#192','ready:\nmovs r7,#195\nlsls r7,r7,#2\nsubs r3,r3,r7'),
        ('movs r4,#229\nlsls r4,r4,#1','movs r4,#31\nlsls r4,r4,#1')]:
        assert assembly.count(old)==1,old
        assembly = assembly.replace(old,new)
    specials = {842-780,905-780,906-780,1028-780,1029-780}
    for p,o,h,values in contract_rows():
        if h:
            shift = 4 if p==0x02053C14 else 5
            assert not {(v>>shift)-896 for v in values}&specials
    code = bytes(Ks(KS_ARCH_ARM,KS_MODE_THUMB).asm(assembly,GATE)[0])
    assert len(code)==168
    return code+b'\xc0\x46'*2,assembly

def apply(arm):
    bound = FunctionType(previous.apply.__code__,{**previous.__dict__,'table':table,'gate':gate},argdefs=previous.apply.__defaults__)
    target,plan = bound(arm)
    plan.update(encoded_table_bytes=180,native_gate_bytes=168,numeric_encoding_bias=780,
        rejected768_bias_historical_status_collisions=['role8120','role8140'],
        all_prior_and_new_keys_disjoint_from_numeric_special_dispatch_values=True)
    return target,plan
