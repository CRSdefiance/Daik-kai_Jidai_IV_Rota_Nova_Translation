"""Use finalized observer journal and retain the63rd unpaired terminal image."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
OLD=Path('scripts/verify_refit_current_actual_v2281.py')
if __name__=='__main__':
 source=OLD.read_text();changes={
 "refit_current_actual_verification_v2281'":"refit_current_actual_verification_v2281c'",
 'and len(shots)==62 and shots.keys()==oldshots.keys()':'and len(shots)==63 and shots.keys()==oldshots.keys()|{20601}',
 'for f in shots],six_paired':'for f in oldshots],unpaired_extra_terminal_frame=20601,six_paired',
 'work/analysis/refit_actual_v2276/live_requests.json':'E:/Rota Nova translations/Generated/work/emulation_v193/refit_actual_v2276_V2171/refit_observer/requests.json',
 "assert obs['terminal']and not obs['errors']":"assert read('work/analysis/refit_actual_v2276/terminal.json')['terminal']and obs['all_host_slots_restored_and_core_file_exact']and not obs['errors']and not obs['mismatches']"
 }
 for old,new in changes.items():assert source.count(old)==1,old;source=source.replace(old,new)
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
 save('work/analysis/refit_current_actual_verification_v2281c/successor_provenance.json',dict(failed_producers=['scripts/verify_refit_current_actual_v2281.py','scripts/verify_refit_current_actual_v2281b.py'],first_failure='Preflight expected62 images; current20601frame run includes extra final frame20601.',second_failure='The live progress journal intentionally remains partial. Completion is in the separate terminal receipt and finalized observer requests journal.',finalized_journal_checks_errors_mismatches_host_slots_and_core_file=True,extra_terminal_frame_retained_without_historical_pair=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
