"""Registered cumulative inheritance and clean-input whole-ROM reconstruction."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    path=Path('scripts/verify_town_trade_port_release_v2172.py');source=path.read_text()
    changes=[
        ('from dk4tool.patch import town_trade_port_contextual_editorial as owned','from dk4tool.patch import surrender_advice_contextual_v1 as owned'),
        ('town_trade_port_release_v2172','surrender_advice_release_v2675'),
        ('town_trade_port_registration_v2170','surrender_advice_registration_v2673'),
        ('all_routes_combined_v2171_candidate.nds','all_routes_combined_v2674_candidate.nds'),
        ('all_routes_combined_v2143_candidate.nds','all_routes_combined_v2284_candidate.nds'),
        ('all-routes-unified-v2171','all-routes-unified-v2674'),
        ('all-routes-unified-v2143','all-routes-unified-v2284'),
        ('town_trade_port_contextual_editorial','surrender_advice_contextual'),
        ('==492','==494'),('all492_manifest','all494_manifest'),('manifest_batches=492','manifest_batches=494'),
        ('exact_to_V2143','exact_to_V2284')]
    for old,new in changes:assert old in source,old;source=source.replace(old,new)
    env={'__name__':'__main__','__file__':__file__};exec(compile(source,__file__,'exec'),env)
    save(env['ROOT']/'successor_provenance.json',dict(template=str(path),template_sha256=sha(path.read_bytes()),
        effective_source_sha256=sha(source.encode()),source_locked_stage_full_cumulative_ancestry_components_shape_and_clean_patch_guards_preserved=True,
        V1492_promotion_guard_preserved=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
