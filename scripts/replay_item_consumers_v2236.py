"""Fresh current Guild/NPC and role wrappers with actual registered paragraphs."""
import inspect
from pathlib import Path
from scripts import verify_item_consumers_v788 as original
from scripts.verify_personal_gameplay_v841 import get_machine
from dk4tool.patch.town_trade_port_contextual_reference_v1 import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/item_consumers_v2236')
CURRENT=Path('out/all_routes_combined_v2171_candidate.nds')
CONTEXT=Path('work/analysis/item_context_v2235')
if __name__=='__main__':
    assert not ROOT.exists();ROOT.mkdir(parents=True)
    program=inspect.getsource(original.main)
    a=program.index("    plan = read(ROOT/'prospective_common_repack.json')")
    b=program.index("    clean = NdsImage.open('work/clean.nds')",a)
    prefix="""    rom=NdsImage.open(CURRENT)
    arm,common=rom.read_file('/__arm9__.bin'),rom.read_file('/COMMON/MESFILE.DK4')
    entries=current_entries(common,arm)
    snapshot=read(CONTEXT/'native_context.json')['pre_fixture_snapshot']
    raw=Path(snapshot['path']).read_bytes()
    assert sha(raw)==snapshot['sha256']
    cpu,_=get_machine(arm,raw)
    plan={'source_ROM_sha256':sha(CURRENT.read_bytes())}
"""
    program=program[:a]+prefix+program[b:]
    old="assert context['producer_sha256'] == sha(Path('scripts/context_item_diplomacy_v784.py').read_bytes())"
    new="assert context['producer_sha256'] == sha(Path('scripts/replay_item_context_v2235.py').read_bytes())"
    assert program.count(old)==1;program=program.replace(old,new)
    snapshot=read(CONTEXT/'native_context.json')['pre_fixture_snapshot']
    env={**original.__dict__,'ROOT':ROOT,'CURRENT':CURRENT,'CONTEXT':CONTEXT,'MANUSCRIPT':Path('translations/item_diplomacy_editorial_manuscript_v2.json'),'RAM':Path(snapshot['path']),'get_machine':get_machine,'current_entries':current_entries,'__file__':__file__}
    exec(compile(program,__file__,'exec'),env);env['main']()
    save(ROOT/'current_replay_provenance.json',dict(original=str(Path(original.__file__)),original_sha256=sha(Path(original.__file__).read_bytes()),effective_source_sha256=sha(program.encode()),current_ROM=str(CURRENT),current_snapshot=snapshot,original_wrappers_providers_argument_order_and_null_branch_unchanged=True,only_message_lookup_boundary_supplied_from_actual_current_entries=True,legacy2235_stdout_still_Japanese_sentence_superseded_by_its_explicit_current_English_JSON_labels=True,no_ROM_or_runtime_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
