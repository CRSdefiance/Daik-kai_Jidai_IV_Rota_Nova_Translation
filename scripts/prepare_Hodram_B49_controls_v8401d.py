"""Bind the hide call's carried input pointer to the exact script relocation."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save

OLD="        assert result['original_picture_boundary_calls']==original['original_picture_boundary_calls']"
NEW="""        expected=[]
            for call in original['original_picture_boundary_calls']:
                relocated={**call,'args':list(call['args'])}
                if word==0x4700:
                    assert call['descriptor'] is None and call['layout'] is None
                    relocated['args'][3]+=after['offset']-before['offset']
                expected.append(relocated)
            assert result['original_picture_boundary_calls']==expected
            result['original_unrelocated_boundary_calls']=original['original_picture_boundary_calls']
            result['hide_carried_script_pointer_relocated_by_exact_command_delta']=word==0x4700"""

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B49_controls_tools_v8401d');assert not root.exists()
    diagnostic=Path('work/analysis/Hodram_B49_picture_probe_v8401c/differences.json');d=read(diagnostic)
    assert len(d['cases'])==4
    for c in d['cases']:
        a,b=c['source'][0],c['target'][0]
        if a['descriptor'] is None:
            assert a['args'][:3]==b['args'][:3] and b['args'][3]-a['args'][3]==c['target_offset']-c['source_offset']
        else:assert a==b
    result=derive('scripts/prove_Hodram_B49_controls_v8401b.py','scripts/prove_Hodram_B49_controls_v8401d.py',{'Hodram_B49_controls_v8401b':'Hodram_B49_controls_v8401d',OLD:NEW})
    root.mkdir(parents=True);save(root/'derivation.json',dict(derivation=result,diagnostic=str(diagnostic),prior_stopped_verifiers_preserved=True,hide_r3_exact_command_delta_verified=True,no_native_value_discarded_oropaque_body_claimed=True,no_prose_ROM_guard_oraddress_change=True))
