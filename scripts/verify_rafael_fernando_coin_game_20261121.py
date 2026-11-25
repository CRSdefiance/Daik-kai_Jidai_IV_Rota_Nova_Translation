"""Verify the stored Fernando dialogue, substitution stress cases and retained menu."""
from inspect import getsource

from scripts import stage_rafael_fernando_coin_game_20261121 as stage
from scripts import verify_rafael_refit_sailing_lessons_20261121 as template
from scripts.source_locked_derivation_v5118 import checked_text


base, native, display, menu = stage.base, stage.native, template.display, template.menu
ROOT = stage.ROOT / "native_display_v2"
PROOF = ROOT / "native_display.json"


main_source = checked_text(getsource(template.main), {
    'prior = earlier_proof["initialized_dependencies"]["0"]':
        'assert earlier_proof["candidate_sha256"] == release["candidate_sha256"]\n'
        '    prior = earlier_proof["reused_initialized_dependency"]',
    'assert prior["candidate_sha256"] == release["candidate_sha256"]':
        'assert prior["candidate_sha256"] == release["predecessor"]["candidate_sha256"]',
    'len(records) == 62 and [m["block"] for m in menus] == [179, 180]':
        'len(records) == 65 and [m["block"] for m in menus] == [178]',
    'assert speech == 34 and len(pictures) == 37': 'assert speech == 34 and len(pictures) == 43',
    'native_caption_count=4, native_menu_count=2': 'native_caption_count=2, native_menu_count=1',
    'given-name stress cases, and four retained captions.': 'nine given-name stress pages, and two retained captions.',
})
scope = vars(template) | globals()
for source in (getsource(template.captions), main_source):
    exec(compile(source, __file__, "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
