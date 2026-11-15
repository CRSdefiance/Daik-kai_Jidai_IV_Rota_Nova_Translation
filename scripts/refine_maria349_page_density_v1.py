"""Retain fuller first pages while moving complete closing phrases to page two."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Maria_B275_B285_clean_20261110')

def main():
    before=ROOT/'formatting_v1/page_phrase_preferences_v4.json'
    after=ROOT/'formatting_v1/page_phrase_preferences_v5.json';assert not after.exists()
    prefs=load(before)
    changes={
        'DK4_MES_B275_R0128':('had no business going near such distinguished guests.',[['like','me']]),
        'SC3_B280_STYLE_8_300':("far northeast of China, aren't they?",[['far','northeast'],['of','china']]),
        'SC3_B280_STYLE_8_498':('that village far northeast of China?',[['far','northeast'],['of','china']]),
    }
    for ident,(clause,pairs) in changes.items():
        item=prefs['records'][ident];item.update(page_clause=clause,required_pairs=pairs,
            reason='The directly viewed whole-sentence page split made the required four-row first page too sparse. Keep more text on page one and move the complete final verb/location phrase to page two; preserve every word, runtime and native guard.')
    prefs.update(previous_preferences=str(before),previous_preferences_sha256=digest(before),
        rejected_sparse_first_page_native_proof=str(ROOT/'native_changed_v1/compiled_native_pages.json'),
        rejected_sparse_first_page_native_proof_sha256=digest(ROOT/'native_changed_v1/compiled_native_pages.json'))
    save(after,prefs)

if __name__=='__main__':main()
