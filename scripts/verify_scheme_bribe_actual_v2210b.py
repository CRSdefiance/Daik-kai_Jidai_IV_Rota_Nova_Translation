"""6400 is the visible scheme menu after A, not a second hold of introduction909."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

original=Path('scripts/verify_scheme_bribe_actual_v2210.py')
source=original.read_text()
for old,new in (
    ('scheme_bribe_actual_verification_v2210', 'scheme_bribe_actual_verification_v2210b'),
    ('909:(6000,6400)', '909:(6000,)'),
    ('len(holds)==10', 'len(holds)==9'),
    ('for f in(6800,8800,10400,12400,12800,13200):', 'for f in(6400,6800,8800,10400,12400,12800,13200):'),
    ('ten_scheme_bribe_holds', 'nine_scheme_bribe_holds'),
    ('six_scheme_bribe_transitions', 'seven_scheme_bribe_transitions'),
    ('all10_full_foregrounds', 'all9_full_foregrounds'),
):
    assert source.count(old)==1,old
    source=source.replace(old,new)
env={'__name__':'__main__','__file__':__file__}
exec(compile(source,__file__,'exec'),env)
save(env['ROOT']/'hold_scope_correction.json',dict(original_verifier=str(original),original_verifier_sha256=sha(original.read_bytes()),effective_source_sha256=sha(source.encode()),frame6400_actual_scheme_menu_viewed=True,frame8400_actual915_speech_viewed=True,nine_complete_holds_for5_IDs=True,seven_menu_return_frames=True,earlier_failed_hold_assumption_preserved=True,no_ROM_capture_or_runtime_repair=True))
