"""Keep native current binding while distinguishing incidental screenshots from ROM exposure."""
from scripts import extract_editorial_current_v4 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous.source, {
    "assert meanings['meanings'] == len(meanings['records']) and all(r['earlier_English_unconsulted'] for r in meanings['records'])":
    """assert meanings['meanings'] == len(meanings['records']) and all(r['current_ROM_English_unconsulted'] for r in meanings['records'])
    sealed=Path(meanings['all_drafts_sealed'])
    assert sha(sealed.read_bytes())==meanings['all_drafts_sha256']
    assert load(sealed)['all435_drafts_saved_before_current_ROM_dialogue_extraction']
    assert meanings['incidental_earlier_screenshot_exposure_disclosed']""",
})
exec(compile(source, __file__ + '::same-binding-explicit-current-ROM-gate-and-sealed-drafts', 'exec'), globals())
