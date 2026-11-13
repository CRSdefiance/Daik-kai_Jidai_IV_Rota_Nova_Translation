"""Successor: generated probe strings use actual NUL terminators, never backslash-zero."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
original=Path('scripts/verify_recruitment_scheme_layouts_v2203.py')
source=original.read_text().replace("work/analysis/recruitment_scheme_layouts_v2203'","work/analysis/recruitment_scheme_layouts_v2203b'")
bad="b'"+chr(92)*4+"0'"
assert source.count(bad)==4
source=source.replace(bad,'bytes(1)')
env={'__name__':'__main__','__file__':__file__}
exec(compile(source,__file__,'exec'),env)
(env['ROOT']/'effective_formatter.py').write_text(env['source'],encoding='utf-8')
save(env['ROOT']/'probe_terminator_correction.json',dict(original=str(original),original_sha256=sha(original.read_bytes()),effective_program_sha256=sha(source.encode()),generated_probe_terminators_use_real_NUL=True,current_native_functions_and_ROM_unchanged=True,prior_failed_probe_preserved=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
