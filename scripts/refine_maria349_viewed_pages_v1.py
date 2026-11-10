"""Keep complete final clauses together after directly reviewing all347 native pages."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/Maria_B275_B285_clean_20261110')

def main():
    before=ROOT/'formatting_v1/page_phrase_preferences_v3.json'
    after=ROOT/'formatting_v1/page_phrase_preferences_v4.json'
    assert not after.exists()
    prefs=load(before); manuscript=ROOT/'formatting_v1/formatting_input.json'
    rows={r['id']:r for r in load(manuscript)['records']}
    clauses={
        'DK4_MES_B275_R0128':"Kept telling me a lout like me had no business going near such distinguished guests.",
        'SC3_B280_STYLE_8_300':"They're in a village far northeast of China, aren't they?",
        'SC3_B280_STYLE_8_498':"Shall we head for that village far northeast of China?",
    }
    for ident,clause in clauses.items():
        row=rows[ident];assert clause in row['english'] and ident not in prefs['records']
        prefs['records'][ident]=dict(bindings={k:sha(row[k].encode('utf-8')) for k in ['source_hex','current_hex','english']},
            reason='Direct native-page review found a short trailing fragment. Preserve every word and both pages, moving the complete final sentence to page two rather than splitting its noun/location phrase.',page_clause=clause)
    prefs.update(previous_preferences=str(before),previous_preferences_sha256=digest(before),
        directly_viewed_native_baseline=str(ROOT/'native_body_v1/compiled_native_pages.json'),
        directly_viewed_native_baseline_sha256=digest(ROOT/'native_body_v1/compiled_native_pages.json'),
        three_visual_page_boundary_findings=list(clauses),no_prose_font_width_runtime_orcontrol_changes=True)
    save(after,prefs)

if __name__=='__main__':main()
