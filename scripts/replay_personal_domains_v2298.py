"""Current source-bound Deck cooldowns and all25 Cabin helper selections."""
from pathlib import Path
import inspect
from scripts import verify_personal_activity_gate_v838 as activity
from scripts import verify_personal_cabin_context_v841 as cabin
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/personal_domains_v2298')
if __name__=='__main__':
 assert not ROOT.exists();ROOT.mkdir(parents=True);snapshot=read('work/analysis/personal_context_v2297/native_context.json')['genuine_current_preinteraction_snapshot'];assert sha(Path(snapshot['path']).read_bytes())==snapshot['sha256'];provenance=[]
 for module,label,changes in[(activity,'activity',{
  "Path('out/all_routes_combined_v838_candidate.nds')":"Path('out/all_routes_combined_v2284_candidate.nds')",
  "snapshot = CAP / 'frame_011200_arm9_ram.bin'":"snapshot = Path("+repr(snapshot['path'])+")",
  "print('Original Deck-entry gate:11 native threshold cases pass. Dockside time0 cannot activate;icon IDs are not room assignments.', flush=True)":"print('Current original Deck-entry gate:11 CPU boundary cases pass;six icon conversions remain distinct from room assignments.',flush=True)"
 }),(cabin,'cabin',{
  "Path('out/all_routes_combined_v838_candidate.nds')":"Path('out/all_routes_combined_v2284_candidate.nds')",
  "Path('E:/Rota Nova translations/Generated/work/emulation_v193/personal_cabin_v840_838_Charles_after/frame_003800_arm9_ram.bin')":"Path("+repr(snapshot['path'])+")"
 })]:
  source=inspect.getsource(module.main)
  for old,new in changes.items():assert source.count(old)==1,old;source=source.replace(old,new)
  env={**module.__dict__,'ROOT':ROOT,'__file__':__file__};exec(compile(source,__file__,'exec'),env);env['main']();provenance.append(dict(kind=label,original=str(Path(module.__file__)),original_sha256=sha(Path(module.__file__).read_bytes()),effective_function_sha256=sha(source.encode())))
 assert len(read(ROOT/'original_activity_entry_gate.json')['eleven_original_native_threshold_cases'])==11 and len(read(ROOT/'ordinary_Cabin_context_verification.json')['all25_original_Cabin_role_helper_selections'])==25
 save(ROOT/'successor_provenance.json',dict(genuine_current_preinteraction_snapshot=snapshot,current_ROM='out/all_routes_combined_v2284_candidate.nds',sources=provenance,activity_age_sea_calendar_and_Cabin_role_assignments_are_isolated_CPU_inputs=True,no_live_RAM_code_save_or_gameplay_fixtures=True,all25_Cabin_helpers_not_all25_full_health_mood_selector_or_actual_visit_claim=True,actual_controller_has_native_Cabin_type12_at_slot12=True,source_role12_and16_comment_paths_are_context_not_new_ownership_claims=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
