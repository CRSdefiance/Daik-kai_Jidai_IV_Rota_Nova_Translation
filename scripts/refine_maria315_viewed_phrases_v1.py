"""Keep seven directly reviewed phrases together without changing their prose."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path('work/Maria_B286_B302_clean_20261110')


def main():
    before = ROOT/'formatting_v1/question_page_preference_v1.json'
    after = ROOT/'formatting_v1/viewed_phrase_preferences_v2.json'
    assert not after.exists()
    manuscript = ROOT/'formatting_v1/formatting_input.json'
    prefs = load(before)
    rows = {r['id']: r for r in load(manuscript)['records']}
    findings = {
        'SC3_B292_STYLE_24_106': ([['like', 'this']], 'Keep the jungle comparison like this together.'),
        'SC3_B292_STYLE_2054_202': ([['out', 'of']], 'Keep out of together in the relieved jungle-exit report.'),
        'DK4_MES_B294_R0024': ([['preach', 'to']], 'Keep preach to together so its object is easy to follow.'),
        'DK4_MES_B296_R0078': ([['ghost', 'ship']], 'Keep the compound ghost ship together.'),
        'DK4_MES_B296_R0123': ([['ancient', 'city'], ['city', 'map'], ['join', 'you']], 'Keep the installed Ancient City Map title and join you together.'),
        'DK4_MES_B298_R0012': ([['proofs', "aren't"], ["aren't", 'you']], 'Attach the short question tag to Proofs rather than leaving the tag on its own line.'),
        'DK4_MES_B298_R0041': ([['give', 'up'], ['up', 'on']], 'Keep the complete give up on phrase together.'),
    }
    for ident, (pairs, reason) in findings.items():
        row = rows[ident]
        assert ident not in prefs['records']
        prefs['records'][ident] = dict(
            bindings={k: sha(row[k].encode('utf-8')) for k in ['source_hex', 'current_hex', 'english']},
            reason='Direct native-page review: '+reason+' Preserve every word and the single native page.',
            one_page=True, required_pairs=pairs)
    prefs.update(previous_preferences=str(before), previous_preferences_sha256=digest(before),
        directly_viewed_native_baseline=str(ROOT/'native_body_v1/compiled_native_pages.json'),
        directly_viewed_native_baseline_sha256=digest(ROOT/'native_body_v1/compiled_native_pages.json'),
        direct_visual_receipt=str(ROOT/'native_body_v1/direct_visual_review_v1.json'),
        direct_visual_receipt_sha256=digest(ROOT/'native_body_v1/direct_visual_review_v1.json'),
        seven_phrase_findings=list(findings), no_prose_font_width_runtime_orcontrol_changes=True)
    save(after, prefs)


if __name__ == '__main__':
    main()
