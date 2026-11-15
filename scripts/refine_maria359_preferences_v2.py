"""Resolve weak endings without widening bounds or adding a page for a number phrase."""
from pathlib import Path
from copy import deepcopy
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Maria_B253_B274_clean_20261110')

def main():
    before=ROOT/'formatting_v1/page_phrase_preferences_v1.json';out=before.with_name('page_phrase_preferences_v2.json');assert not out.exists()
    prefs=deepcopy(load(before));r=prefs['records']
    r['DK4_MES_B254_R0012']['required_pairs']=[['an','instant']]
    r['DK4_MES_B254_R0012']['reason']+=' Keep an instant together so the one-page plan cannot strand its article.'
    for ident in ['DK4_MES_B254_R0069','DK4_MES_B255_R0028']:
        r[ident]['required_pairs'].append(['a','month'])
        r[ident]['reason']+=' Preserve a month as a phrase; do not accept an article-ending row.'
    removed=r.pop('DK4_MES_B266_R0035')
    prefs.update(previous_preferences=str(before),previous_preferences_sha256=digest(before),
        contextual_layout_retentions=[dict(id='DK4_MES_B266_R0035',
            reason='Retain the initial four-row complete argument. Forcing both forty days and demand stick together adds a fifth row and an avoidable second page. The existing complete-word break between forty and days preserves both numbers clearly within one native page; no bounds, weak-ending or glyph guard is waived.',
            rejected_preference=removed)],
        London_two_page_tradeoff='Keep the complete final strange-people statement on the second page. The original first sentence must occupy four native rows to align that boundary; those shorter rows are a scoped continuity tradeoff, not a narrower viewport or prose shortening.')
    save(out,prefs);print('Resolved three weak endings; retained the complete courier argument on one page.')

if __name__=='__main__':main()
