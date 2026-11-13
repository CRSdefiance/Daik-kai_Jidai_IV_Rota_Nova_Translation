"""Record the389-page direct review and source-bound phrase/page layout candidates."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.prepare_hodram_B311_B324_formatting_v1 import ROOT, FORMATTING

INITIAL = ROOT / 'automatic_plans_v1/automatic_plans.json'
NATIVE = ROOT / 'native_initial_v1/compiled_native_pages.json'
PREFERENCES = ROOT / 'formatting_v1/visual_preferences_v1.json'
VIEW = ROOT / 'initial_visual_review_v1.json'

def main():
    assert not VIEW.exists() and not PREFERENCES.exists()
    doc, plan, native, sheets = map(load, [FORMATTING, INITIAL, NATIVE,
        ROOT/'initial_body_sheets_v1/contact_manifest.json'])
    assert len(native['records']) == 387 and native['pages'] == len(sheets['pages']) == 389
    assert len(sheets['sheets']) == 22 and all(digest(s['path']) == s['sha256'] for s in sheets['sheets'])
    rows = {r['id']: r for r in doc['records']}
    preferences = deepcopy(load(ROOT/'formatting_v1/initial_preferences.json'))
    findings = {}
    def prefer(ident, reason, **options):
        row = rows[ident]
        assert ident not in findings
        value = {**options, 'reason': reason,
                 'bindings': {k: sha(row[k].encode()) for k in ['source_hex', 'current_hex', 'english']}}
        preferences['records'][ident] = findings[ident] = value
    def ordinary(b, r, phrase, **options):
        prefer(f'DK4_MES_B{b}_R{r:04d}', phrase, **options)
    def style(b, command, offset, phrase, **options):
        prefer(f'SC1_B{b}_STYLE_{command}_{offset}', phrase, **options)
    ordinary(312, 6, 'Keep tell-you together and avoid the fragmented four-row forgotten-message lead-in.',
             one_page=True, required_pairs=[['tell','you'], ['slipped','my'], ['my','mind']])
    for offset in [40, 226]:
        style(313, 24, offset, 'Keep the complete get-lost phrase together in the map warning.',
              one_page=True, required_pairs=[["we'll",'get'], ['get','lost']])
    for command in [856, 1252]:
        for offset in [0, 88]:
            style(313, command, offset, 'Keep count-on-you together rather than splitting the reassurance’s verb phrase.',
                  one_page=True, required_pairs=[['count','on'], ['on','you']])
        for offset in [136, 278]:
            style(313, command, offset, 'Keep Reliable-as-ever together rather than a separate Reliable fragment.',
                  one_page=True, required_pairs=[['reliable','as'], ['as','ever']])
        style(313, command, 182, 'Keep the admiral address with A-fine-job and preserve count-on-you.',
              one_page=True, required_pairs=[['job','admiral'], ['count','on'], ['on','you']])
    for offset in [80, 202]:
        style(313, 2118, offset, 'Keep the repeated nice-and-quiet caution continuous.',
              one_page=True, required_pairs=[['nice','and'], ['and','quiet']])
    ordinary(314, 10, 'Keep heard-of together in the item question while retaining the full title and celadon detail.',
             one_page=True, required_pairs=[['heard','of'], ['goryeo','incense'], ['incense','burner']])
    ordinary(314, 14, 'Keep try-it-just-once together instead of a continuation beginning it-just-once.',
             one_page=True, required_pairs=[['try','it'], ['it','just'], ['just','once']])
    ordinary(315, 10, 'Keep tell-your-fortune together in the offered reading.',
             one_page=True, required_pairs=[['tell','your'], ['your','fortune']])
    ordinary(315, 26, 'Keep the looking-for phrase attached to its subject instead of a row ending youre.',
             one_page=True, required_pairs=[["you're",'looking'], ['looking','for']])
    ordinary(316, 214, 'Test the fog-to-clear phrase without a detached to-clear row; do not shorten the weather judgment.',
             one_page=True, required_pairs=[['fog','to'], ['to','clear']])
    ordinary(318, 94, 'Keep Castor-Company together and give the complete What-are-you-doing-here question an uninterrupted clause.',
             one_page=True, required_pairs=[['castor','company'], ['what','are'], ['are','you'], ['you','doing'], ['doing','here']])
    ordinary(318, 109, 'Keep look-for and along-the-way together in Rafael’s explanation.',
             one_page=True, required_pairs=[['look','for'], ['along','the'], ['the','way']])
    ordinary(318, 117, 'Keep come-along together in the guide’s explanation.',
             one_page=True, required_pairs=[['come','along']])
    style(318, 96, 0, 'Keep ancient-city and place-like-this continuous in the amazed observation.',
          one_page=True, required_pairs=[['ancient','city'], ['place','like'], ['like','this']])
    style(318, 96, 266, 'Keep way-out-here together in the youthful discovery.',
          one_page=True, required_pairs=[['way','out'], ['out','here']])
    ordinary(319, 28, 'Keep the short would-you question tag with the end of the preceding clause.',
             one_page=True, required_pairs=[['him','would'], ['would','you']])
    ordinary(320, 5, 'Keep the complete Where-are-you-from question together instead of stranding Where.',
             one_page=True, required_pairs=[['where','are'], ['are','you'], ['you','from']])
    ordinary(320, 24, 'Keep Something-about together in the vague personal hearsay account.',
             one_page=True, required_pairs=[['something','about']])
    ordinary(320, 28, 'Keep give-you together in the barter offer.',
             one_page=True, required_pairs=[['give','you']])
    style(322, 8, 112, 'Keep survey-party together in the formal disembarkation announcement.',
          one_page=True, required_pairs=[['survey','party']])
    ordinary(324, 13, 'Keep the complete village-survival sentence on the same page, avoiding a page containing only wiped-out.',
             one_page=False, page_clause="Thanks to him, our village wasn't wiped out.",
             required_pairs=[['wiped','out']])
    ordinary(324, 24, 'Keep Something-about and mineral-poison continuous in the witness’s uncertain account.',
             one_page=True, required_pairs=[['something','about'], ['mineral','poison']])
    ordinary(324, 73, 'Keep experimental-material together in Charles’s discovery rumor.',
             one_page=True, required_pairs=[['experimental','material']])
    ordinary(324, 77, 'Keep obtain-that-material together rather than a sparse final object row.',
             one_page=True, required_pairs=[['obtain','that'], ['that','material']])
    ordinary(324, 81, 'Keep Now-if and use-it together without a dangling it before the muttered hesitation.',
             one_page=True, required_pairs=[['now','if'], ['use','it']])
    ordinary(324, 102, 'Keep same-sickness together when revealing the monk’s illness.',
             one_page=True, required_pairs=[['same','sickness']])
    ordinary(324, 129, 'Keep continue-his-work together in the request to carry on the research.',
             one_page=True, required_pairs=[['continue','his'], ['his','work']])
    ordinary(324, 144, 'Keep investigate-it together in Charles’s enthusiastic promise.',
             one_page=True, required_pairs=[['investigate','it']])
    ordinary(324, 148, 'Keep the full closing research-freedom sentence on one page instead of starting the next page to-your-hearts-content.',
             one_page=False, page_clause="You can research to your heart's content.",
             required_pairs=[['in','command'], ['command','of'], ['your',"heart's"], ["heart's",'content']])
    menu_paths = [ROOT/f'native_objects_v1/two/{key}/native_caption_review.png'
                  for key in ['B311_C1086','B311_C1306','B316_C674','B316_C934','B317_C764']]
    menu_paths.append(ROOT/'native_objects_v1/three/native_caption_review_1.png')
    name_proof = ROOT/'name_planes_v1/native_name_planes.json'
    names = load(name_proof)
    assert names['scoped_actors'] == 11 and names['distinct_strings'] == 10
    name_sheets = names['review_sheets']
    assert len(name_sheets) == 1 and digest(name_sheets[0]['path']) == name_sheets[0]['sha256']
    save(ROOT/'scoped_names_visual_approval_v1.json', dict(scoped_actors=11, distinct_strings=10,
        all_ten_progressive_name_strings_directly_viewed=True, review_sheets=name_sheets,
        native_name_proof=str(name_proof), native_name_proof_sha256=digest(name_proof),
        complete_leading_trailing_glyphs_font_andbounds_pass=True, actual_headers_unvisited=True,
        full_catalogue_UI_andother_middle_field_consumers_unvisited=True, new_credit=0))
    save(PREFERENCES, preferences)
    save(VIEW, dict(all389_initial_body_pages_directly_viewed=True, body_sheets=sheets['sheets'],
        all_six_menu_sheets_directly_viewed=True, menu_sheets=[dict(path=str(p), sha256=digest(p)) for p in menu_paths],
        all_ten_scoped_name_strings_directly_viewed=True, scoped_name_visual_approval=str(ROOT/'scoped_names_visual_approval_v1.json'),
        initial_glyphs_leading_trailing_characters_andfont_consistent=True,
        individual_fullsize_page_recheck='SC1_B317_STYLE_1114_230 p1: complete the-ruins continuation confirmed in individual image and exact native events; no missing glyph.',
        observed_layout_candidates=findings, candidate_count=len(findings),
        every_candidate_requires_final_disposition_andfresh_changed_layout_checks=True,
        other_layouts_retained_reason='Complete brief replies, natural ordinary continuations and readable balanced rows already work; retain formatter-owned boundaries without adding dramatic pauses.',
        initial_native_proof=str(NATIVE), initial_native_proof_sha256=digest(NATIVE),
        offline_only=True, actual_new_batch_gameplay=False, new_credit=0,
        evidence={str(p): digest(p) for p in [FORMATTING, INITIAL, NATIVE, PREFERENCES, name_proof, Path(__file__)]}))
    print('Viewed389 body pages, six menus and ten names; saved', len(findings), 'layout candidates, zero credit.')

if __name__ == '__main__':
    main()
