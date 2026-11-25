"""Avoid unescaped context apostrophes in the generated authoring source."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
OLD=Path('scripts/review_battle_cooking_livestock_v2399.py')
if __name__=='__main__':
 source=OLD.read_text();assert 'Sera24\\u0027s Galley' in source and 'characters\\u0027 intent' in source;source=source.replace('Sera24\\u0027s Galley','Sera24 Galley').replace('characters\\u0027 intent','characters intent').replace('battle_cooking_livestock_editorial_v2399','battle_cooking_livestock_editorial_v2399b');exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
 save('work/analysis/battle_cooking_livestock_editorial_v2399b/successor_provenance.json',dict(original=str(OLD),original_sha256=sha(OLD.read_bytes()),initial_failure_before_manuscript_or_ledger_output=True,reason='Apostrophes in inserted context prose broke the generated single-quoted source literal. This successor uses equivalent context wording without those apostrophes;all25 source glosses,English retentions and reasons are unchanged.',producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
