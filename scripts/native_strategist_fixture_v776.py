"""The mapped three-byte assignment on exact V773/V776,without stat cheats."""

from types import FunctionType

from dk4tool.patch.grand_race_menu_release import sha
from scripts import native_strategist_fixture_v624 as original
from scripts.verify_village_wrap_v608 import read

BASELINE='9e54d5456e1de352c2cdf574a8cca5bcb93fbbbd0414fdb38b627b1278617d92'


def assign(arm,raw,request):
    expected=read('work/analysis/tavern_schemes_integration_v776/prospective_common_repack.json')['target_ARM9_sha256']
    if sha(arm) not in (BASELINE,expected) or len(raw)!=0x400000 or request is not True:
        raise ValueError('Exact V773/V776 and declared three-byte strategist assignment required')
    env=dict(original.__dict__)
    env['ARM']=sha(arm)
    after,proof=FunctionType(original.assign.__code__,env)(arm,raw,True)
    changed={i for i,(a,b) in enumerate(zip(raw,after,strict=True)) if a!=b}
    assert changed=={r['address']-0x02000000 for r in proof['changes']} and len(changed)==3
    proof['all_other4MiB_bytes_exact']=True
    proof['stats_XP_money_location_calendar_unchanged']=True
    return after,proof


def assign_expert(arm,raw,request):
    raise ValueError('Only the source-mapped three-byte assignment is enabled in this fixture')
