"""Current525 printf/day-unit/wrap cases and complete font geometry samples."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/refit_spoken_layouts_v2280');OLD=Path('scripts/probe_refit_dialogue_layout_v833.py')
if __name__=='__main__':
 assert not ROOT.exists();ROOT.mkdir(parents=True);source=OLD.read_text();snapshot=read('work/analysis/item_context_v2235/native_context.json')['pre_fixture_snapshot']
 assert sha(Path(snapshot['path']).read_bytes())==snapshot['sha256']
 changes={
 'from scripts.context_refit_dialogue_v832 import ROM':"from ndspy.code import MainCodeFile\nROM=Path('out/all_routes_combined_v2171_candidate.nds')",
 'from scripts.review_refit_dialogue_v832 import MANUSCRIPT':"MANUSCRIPT=Path('translations/refit_contextual_editorial_manuscript_v1.json')",
 'ROOT = runtime.ROOT':"ROOT=Path('work/analysis/refit_spoken_layouts_v2280')",
 "    arm = (ROOT / 'ARM9_RESEARCH_ONLY.bin').read_bytes()":"    arm = Path('work/analysis/refit_spritsail_payload_v2278/ARM9_RESEARCH_ONLY.bin').read_bytes()",
 "    proof = read(ROOT / 'native_runtime_verification.json')\n    assert proof['research_ARM9_sha256'] == sha(arm)\n    plan = read(ROOT / 'runtime_plan.json')":"    assert read('work/analysis/refit_spritsail_payload_v2278/payload_plan.json')['target_ARM9_sha256']==sha(arm)",
 "    raw_path = Path('work/emulation_v193/refit_editorial_v831_after/frame_020000_arm9_ram.bin')":"    raw_path = Path("+repr(snapshot['path'])+")",
 "    rows = read(MANUSCRIPT)['records']":"    rows = [r for r in read(MANUSCRIPT)['records']if 1256<=r['message_id']<=1267]\n    assert len(rows)==12",
 "                for patch in plan['patches']:\n                    cpu.mem_write(patch['address'], bytes.fromhex(patch['target_hex']))":"                for section in MainCodeFile(arm,BASE).sections:\n                    cpu.mem_write(section.ramAddress,bytes(section.data))"
 }
 for old,new in changes.items():assert source.count(old)==1,old;source=source.replace(old,new)
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
 current=read(ROOT/'native_layout_matrix.json');old=read('work/analysis/refit_dialogue_runtime_v833/native_layout_matrix.json')
 assert current['count']==old['count']==525
 assert all((a['message_id'],a['number'],a['formatted_hex'])==(b['message_id'],b['number'],b['formatted_hex'])for a,b in zip(current['cases'],old['cases'],strict=True))
 save(ROOT/'successor_probe_provenance.json',dict(original=str(OLD),original_sha256=sha(OLD.read_bytes()),effective_source_sha256=sha(source.encode()),current_genuine_preinteraction_snapshot=snapshot,research_current_ARM9_sections_installed_over_captured_globals=True,supplied_parent_table_ID_stack_and_number_inputs_are_CPU_controls=True,duration_thunk_supplies_original_registered_return_address_and_stops_at_return=True,all525_current_complete_outputs_equal_historical_matrix=True,old_runtime_not_reinstalled=True,not_new_gameplay_or_GPU=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
