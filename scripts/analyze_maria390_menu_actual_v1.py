"""Keep complete live-menu guards for Maria and an initial menu before the first speech."""
from scripts.analyze_rafael_B201_B220_menu_actual_v1 import source as previous
from scripts.analyze_maria301_display_v1 import verified_existing_unlock
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    " and not report.get('battery_save_preloaded')":' and verified_existing_unlock(report)',
    "prev=next(r for r in reversed(speech) if r['fixture_offset']<declared['fixture_offset'])":
        "prev=next((r for r in reversed(speech) if r['fixture_offset']<declared['fixture_offset']),None)",
    "left=max(r['frame'] for r in ordered if r['id']==prev['id'])":
        "left=max(r['frame'] for r in ordered if r['id']==prev['id']) if prev else 3000",
    "preceding_speech=prev['id'],following_speech=follow['id']":
        "preceding_speech=prev['id'] if prev else None,initial_menu_before_first_selected_speech=prev is None,following_speech=follow['id']",
    'observed_each_menu_between_its_own_exact_preceding_and_following_speech=True,':
        'all_menus_matched_within_exact_following_andavailable_preceding_speech_intervals=True,initial_menu_lower_bound3000_has_no_preceding_speech_claim=True,',
})
if __name__=='__main__':exec(compile(source,__file__+'::same-complete-caption-pixels-centering-background-bands-andordinary-A-returns-Maria','exec'),globals())
