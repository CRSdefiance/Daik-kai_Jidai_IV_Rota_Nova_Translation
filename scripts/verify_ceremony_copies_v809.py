"""Every original COMMON cold/warm copy,including full post-NUL spans."""

import sys
from pathlib import Path
from types import FunctionType

from dk4tool.patch.grand_race_menu_release import sha
from scripts import verify_schemes_copies_v776 as frozen
from scripts.prepare_ceremony_common_v809 import ROOT
from scripts.verify_village_wrap_v608 import read,save


if __name__=='__main__':
    env={**frozen.main.__globals__,'SOURCE':ROOT,'ROOT':ROOT/'native_copies'}
    sys.argv=[__file__,'--first-block','0','--last-block','40']
    FunctionType(frozen.main.__code__,env)()
    reports=[read(ROOT/f'native_copies/native_copies_block_{n:02d}.json') for n in range(41)]
    plan=read(ROOT/'prospective_common_repack.json')
    assert all(r['COMMON_sha256']==plan['target_COMMON_sha256'] and r['ARM9_sha256']==plan['target_ARM9_sha256'] for r in reports)
    cases=[c for r in reports for c in r['cases']]
    assert {(c['message_id'],c['cold_cache']) for c in cases}=={(n,cold) for n in range(3668) for cold in (False,True)}
    assert all(c['complete_native_copy']['entire_native_span_including_post_NUL_payload_exact'] for c in cases)
    save(ROOT/'complete_native_copies.json',dict(count=len(cases),blocks=41,
        every3668_selection_warm_and_cold_full_span_verified=True,
        COMMON_sha256=plan['target_COMMON_sha256'],ARM9_sha256=plan['target_ARM9_sha256'],
        SDK_IO_boundary_bridged_not_physical_gameplay=True,
        frozen_verifier_sha256=sha(Path(frozen.__file__).read_bytes()),
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('All7336 complete guarded native copies pass across41 blocks.',flush=True)
