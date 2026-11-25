"""Bind the two source middle components and propose only their fixed owned spans."""
from pathlib import Path
from types import FunctionType
import sys
from scripts import bind_clean_editorial_name_fields_v2 as binder
from scripts.audit_story_glyph_consistency import save as original_save
from scripts.source_locked_derivation_v5118 import checked_text

SOURCE=Path('work/analysis/Rafael_early_story_B36_B41_B51_B60_clean_20261104/B36_B41_clean_name_fields_v1.json')


def save_after_review(path,doc):
    doc['earlier_English_dialogue_unconsulted']=False
    doc['source_field_read_after_current_dialogue_comparison']=True
    original_save(path,doc)


if __name__=='__main__':
    assert not SOURCE.exists()
    old=sys.argv
    sys.argv=[__file__,'--packet','work/analysis/Rafael_early_story_B36_B41_B51_B60_clean_20261104/B36_B41_selected_source_packet_v1.json','--out',str(SOURCE)]
    try:
        FunctionType(binder.main.__code__,{**binder.main.__globals__,'save':save_after_review,'__file__':__file__},argdefs=binder.main.__defaults__)()
    finally:sys.argv=old

source=checked_text(Path('scripts/propose_editorial_name_fields.py').read_text(encoding='utf-8'),{
    'from scripts.registered_editorial_runtime import RegisteredRuntime':'from scripts.registered_editorial_runtime_v2 import RegisteredRuntime',
    'work/analysis/Hodram_B91_B110_name_fields_20261101':'work/analysis/Rafael_B36_B41_name_field_proposals_20261104',
    'work/analysis/Hodram_B81_B89_release_verified_20261101/registered_release_verification.json':'work/analysis/Hodram_B191_B210_release_verified_20261104/registered_release_verification.json',
    "STARTUP=RELEASE.with_name('own_registered_startup_verification.json')":
        "STARTUP=Path('work/analysis/Rafael_early_tutorial_registered_context_20261104/registered_Rafael_context_v1.json')",
    'work/analysis/Hodram_B91_B110_clean_20261101/clean_name_fields.json':str(SOURCE).replace('\\','/'),
    'ctx=RegisteredRuntime(RELEASE,STARTUP)':'ctx=RegisteredRuntime(RELEASE,STARTUP,captain=0)',
    "specs=[(20,0,'Ｆernando','Fernando','latin-width-normalization',\n        'Retain the already established Fernando Dias spelling;normalize only the mismatched full-width initial F.'),\n        (22,8,'ダ','da','source-name-component-romanization',\n        'Render the explicit source name componentダ as da,retaining Samwell andKhan. It is part of the full name,not a new title,rank,nationality orbiography;progressive Samwell Khan is unchanged.')]":
        """specs=[(31,8,'デ','de','source-name-component-romanization',
        'Render the explicit source middle component デ as Spanish de while preserving Pedro andValdes. The full catalogue consumer includes it;the source progressive consumer omits it. No rank orrelationship is added.'),
        (34,8,'Ｆazul','Fazul','latin-width-normalization',
        'Preserve the established Fazul middle-name spelling from source ファーズル andnormalize only its full-width initial F. Barbarossa andHayreddin andall source component ordering remain. No new biography orrank.')]""",
})
exec(compile(source,__file__+'::same-complete-owned-name-span-inventory-explicit-Rafael','exec'),globals())
