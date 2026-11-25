"""Bind any sealed source-first batch without making a blanket historical-exposure claim."""
from scripts import extract_editorial_current_v5 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous.source, {
    "assert load(sealed)['all435_drafts_saved_before_current_ROM_dialogue_extraction']":
        "assert load(sealed)['source_meanings_andlogical_drafts_sealed_before_current_ROM_English_extraction_in_this_intake']",
    "assert meanings['incidental_earlier_screenshot_exposure_disclosed']":
        "assert meanings['no_blanket_prior_English_exposure_claim']",
})
exec(compile(source, __file__ + '::same-native-current-binding-generic-sealed-drafts', 'exec'), globals())
