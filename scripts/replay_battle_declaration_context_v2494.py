"""Fresh current-code voice,argument and cancellation controls on a disclosed historical model."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
OLD=Path('scripts/research_battle_declaration_context_v991c.py')
if __name__=='__main__':
 source=OLD.read_text();changes={
 'dk4tool.patch.activity_special_editorial_v987b':'dk4tool.patch.refit_contextual_spritsail_v1',
 "ROOT = Path('work/analysis/battle_declaration_v991c')":"ROOT = Path('work/analysis/battle_declaration_context_v2494')",
 "ROM = Path('out/all_routes_combined_v987_candidate.nds')":"ROM = Path('out/all_routes_combined_v2284_candidate.nds')",
 "Path('work/analysis/battle_declaration_v990/source_inventory.json')":"Path('work/analysis/battle_declaration_context_source_v2492/source_inventory.json')",
 "assert ledger['records_editorially_completed'] == 1174 and ledger['records_with_source_and_prose_pass'] == 1177":"assert ledger['records_editorially_completed'] == 2143 and ledger['contextual_story_natural_dialogue_pass_v1871']['fresh_pass_records_integrated']==1913",
 "assert report['ROM_sha256'] == sha(ROM.read_bytes())":"assert report['ROM_sha256']==sha(Path('out/all_routes_combined_v987_candidate.nds').read_bytes());assert sha(raw)==receipt['sha256']\n    historical_arm=NdsImage.open('out/all_routes_combined_v987_candidate.nds').read_file('/__arm9__.bin');assert all(historical_arm[a:b]==arm[a:b]for a,b in source_spans)",
 "'read_only_cold_boot_snapshot': receipt":"'read_only_historical_V987_cold_boot_snapshot':receipt,'historical_snapshot_not_current_ROM_gameplay':True,'all_executed_selector_spans_current_clean_and_historical_exact':True",
 }
 for a,b in changes.items():assert a in source,a;source=source.replace(a,b)
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
 save('work/analysis/battle_declaration_context_v2494/producer_binding.json',dict(original=str(OLD),original_sha256=sha(OLD.read_bytes()),effective_source_sha256=sha(source.encode()),no_historical_producer_or_ROM_edit=True,new_current_emulator_runs=0,new_editorial_credit=0,full_goal_complete=False))
