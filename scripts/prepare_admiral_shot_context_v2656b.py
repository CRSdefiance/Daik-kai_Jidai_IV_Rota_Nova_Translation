"""Preserve2656 refusal;use authoritative file-qualified historical keys."""
from pathlib import Path
if __name__=='__main__':
 source=Path('scripts/prepare_admiral_shot_context_v2656.py').read_text();source=source.replace('from scripts.verify_village_wrap_v608 import read,save','from scripts.verify_village_wrap_v608 import read,save\nfrom scripts.reconcile_contextual_mood_retentions_v2482 import historical_key').replace("(r.get('file_path','/COMMON/MESFILE.DK4'),r['id'])for f","historical_key(r)for f").replace('admiral_shot_context_v2656','admiral_shot_context_v2656b');exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
