"""Preserve derivation history and give the unexecuted completion producer its correct label."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT = Path('work/analysis/lil_B169_completion_tools_v4255b')
if __name__ == '__main__':
    assert not ROOT.exists()
    tools = [derive('scripts/complete_lil_B169_v4255.py','scripts/complete_lil_B169_v4255b.py',{
        'Stage B168 completion only after':'Stage B169 completion only after',
    })]
    tools.append(derive('scripts/pin_lil_B168_v4208.py','scripts/pin_lil_B169_v4255.py',{
        'all_routes_combined_v4204':'all_routes_combined_v4251',
        'lil_B168_reference_v4193':'lil_B169_reference_v4236',
        'lil_B168_display_v4198':'lil_B169_display_v4241',
        'lil_B168_release_v4205':'lil_B169_release_v4252',
        'B168 V4204':'B169 V4251',
        '    save(target, pins)':"    import json,os\n    data=(json.dumps(pins,ensure_ascii=False,indent=2)+'\\n').replace('\\n','\\r\\n').encode('utf-8')\n    assert len(data)>=target.stat().st_size\n    with target.open('r+b') as stream:\n        stream.write(data)\n        stream.flush()\n        os.fsync(stream.fileno())",
    }))
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(tools=tools,
        execution_notes=[
            dict(kind='unexecuted-derived-compiler-access',producer='scripts/prepare_lil_B169_compiler_v4249.py',
                 correction='scripts/prepare_lil_B169_compiler_v4249b.py',ROM_or_registry_change=False),
            dict(kind='registration-prerequisite-path-key-failure',producer='scripts/register_lil_B169_v4250.py',
                 observed_error="KeyError:translations\\release_stack.json",correction='scripts/register_lil_B169_v4250b.py',ROM_or_registry_change=False),
            dict(kind='premature-release-verifier-attempt',producer='scripts/verify_lil_B169_release_v4252.py',
                 observed_error='V4251 manifest not yet present while cumulative builder session55280 was still live.',
                 subsequent_action='Polled the same build handle until returncode0;then reran the unchanged verifier under a terminal-receipt gate.',
                 ROM_or_registry_change=False),
        ],all_prior_producers_preserved=True,no_completion_orcredit_change_before_gates=True,full_goal_complete=False))
    print('Correctly labelled completion successor and CRLF-preserving ROM pins prepared;earlier producers/failure notes retained.')
