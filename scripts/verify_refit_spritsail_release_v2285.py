"""Registered cumulative inheritance and exact clean-input reconstruction."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
OLD=Path('scripts/verify_town_trade_port_release_v2172.py')
if __name__=='__main__':
 source=OLD.read_text();changes=[
 ('from dk4tool.patch import town_trade_port_contextual_editorial as owned','from dk4tool.patch import refit_contextual_spritsail_v1 as owned'),
 ('town_trade_port_release_v2172','refit_spritsail_release_v2285'),
 ('town_trade_port_registration_v2170','refit_spritsail_registration_v2283'),
 ('all_routes_combined_v2171_candidate.nds','all_routes_combined_v2284_candidate.nds'),
 ('all_routes_combined_v2143_candidate.nds','all_routes_combined_v2171_candidate.nds'),
 ('all-routes-unified-v2171','all-routes-unified-v2284'),
 ('all-routes-unified-v2143','all-routes-unified-v2171'),
 ('town_trade_port_contextual_editorial','refit_contextual_spritsail'),
 ('492','493'),('exact_to_V2143','exact_to_V2171')]
 for old,new in changes:assert old in source,old;source=source.replace(old,new)
 env={'__name__':'__main__','__file__':__file__};exec(compile(source,__file__,'exec'),env)
 save(env['ROOT']/'successor_provenance.json',dict(original=str(OLD),original_sha256=sha(OLD.read_bytes()),effective_source_sha256=sha(source.encode()),all_complete_manifest_profile_baseline_file_component_section_and_exact_clean_patch_assertions_preserved=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
