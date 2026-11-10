"""Supply fixture navigation separately from the recorded controller schedule."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/recommendation_runner_tools_v4984c');assert not root.exists()
    a=derive('scripts/observe_recommendation_v4984.py','scripts/observe_recommendation_v4984c.py',{
        'recommendation_actual_v4984_':'recommendation_actual_v4984c_',
    })
    b=derive('scripts/run_recommendation_focus_v4984b.py','scripts/run_recommendation_focus_v4984c.py',{
        'import argparse,ctypes as ct,sys':'import argparse,ctypes as ct,sys,io,json',
        'observe_recommendation_v4984 as observed':'observe_recommendation_v4984c as observed',
        'recommendation775_v4984_':'recommendation775_v4984c_',
        "    assert any(r.get('market_fixture')=={'mode':'edge'} and r['start']==3200 for r in schedule)":
        "    fixture_commands=[dict(until=12001,market_fixture={'mode':'edge'}),dict(stop=True)]\n    save(root/'predeclared_fixture_navigation.json',fixture_commands)",
        "'--battery-save',str(donor),'--allow-market-fixtures','--touchscreen'":"'--battery-save',str(donor),'--allow-market-fixtures','--pause-at','3200','--dump-pause-ram','--touchscreen'",
        "    try:\n        from scripts import recommendation_harness_v4984b as adapter":
        "    previous_stdin=sys.stdin;sys.stdin=io.StringIO(''.join(json.dumps(command)+'\\n' for command in fixture_commands))\n    try:\n        from scripts import recommendation_harness_v4984b as adapter",
        '        harness.ct=previous':'        harness.ct=previous;sys.stdin=previous_stdin',
    })
    root.mkdir(parents=True);save(root/'prepared_tools.json',dict(tools=[a,b],stopped_source_contract_root_preserved=True,
        original_harness_fixture_API_uses_navigation_not_controller_input_events=True,no_emulator_run_before_stopped_assertion=True))
