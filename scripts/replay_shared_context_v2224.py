"""Fresh original shared consumer/selection probes on current genuine preinteraction RAM."""
from pathlib import Path
import sys
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

mode=sys.argv[1]
assert mode in('context','consumers','filters')
current="CURRENT=Path('out/all_routes_combined_v2171_candidate.nds')"
context="CONTEXT=Path('work/analysis/shared_context_v2224')"
if mode=='context':
    original=Path('scripts/context_shared_dialogue_v781.py')
    root=Path('work/analysis/shared_context_v2224')
    changes={
        'work/analysis/shared_editorial_v781':str(root).replace('\\','/'),
        'out/all_routes_combined_v780_candidate.nds':'out/all_routes_combined_v2171_candidate.nds',
        'barmaid_v780_seoul_live2/capture_report.json':'recruitment_actual_v2202_V2171/capture_report.json',
        'Role1 Barkeep, proved by the original initializer and continuation call sites':'Original role1 First Mate speech provider with native officer fallback; role-label proof is separate from the initializer and continuation call sites',
    }
else:
    original=Path(f'scripts/verify_shared_{mode}_v782.py')
    root=Path('work/analysis/shared_consumers_v2225'if mode=='consumers'else'work/analysis/shared_filters_v2226')
    old='from scripts.context_shared_dialogue_v781 import CURRENT, ROOT as CONTEXT'+(', TABLES'if mode=='consumers'else'')
    new=('from scripts.context_shared_dialogue_v781 import TABLES\n'if mode=='consumers'else'')+current+'\n'+context
    changes={old:new,'work/analysis/shared_integration_v782':str(root).replace('\\','/')}
    if mode=='consumers':
        changes['from dk4tool.script.common_message_table import common_message_entries']='from dk4tool.patch.town_trade_port_contextual_reference_v1 import current_entries as common_message_entries'
        changes[', arm, clean=False)']=', arm)'
assert not root.exists()
source=original.read_text()
for old,new in changes.items():
    assert source.count(old)>=1,(old,source.count(old))
    source=source.replace(old,new)
root.mkdir(parents=True)
exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
save(root/'fresh_current_replay_provenance.json',dict(mode=mode,original=str(original),original_sha256=sha(original.read_bytes()),effective_source_sha256=sha(source.encode()),original_native_branches_functions_and_registered_ROM_unchanged=True,current_preinteraction_snapshot_from_fixture_free_recruitment=True,CPU_boundary_contracts_and_supplied_values_not_earned_states=True,role1_corrected_from_historical_mislabel_no_dialogue_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
