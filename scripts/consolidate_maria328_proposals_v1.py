"""Consolidate disjoint individual proposals while keeping all approval gates pending."""
from copy import deepcopy
from collections import Counter
from pathlib import Path
from scripts.meaning_maria328_clean_v1 import ROOT
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest


def main():
    out = ROOT/'all328_contextual_proposals_v1.json'
    assert not out.exists()
    paths = [ROOT/'B73_B86_contextual_proposals_v1.json', ROOT/'B87_B95_contextual_proposals_v1.json']
    docs = list(map(load,paths))
    drafts_path = ROOT/'all328_independent_drafts_v1.json'
    drafts = load(drafts_path)
    rows = [deepcopy(r) for doc in docs for r in doc['records']]
    assert len(rows) == len({r['id'] for r in rows}) == 328
    assert [r['id'] for r in rows] == [r['id'] for r in drafts['records']]
    assert docs[0]['runtime'] == docs[1]['runtime']
    for doc in docs:
        for p,h in doc['evidence'].items():
            assert digest(p) == h
    for row, original in zip(rows,drafts['records'],strict=True):
        assert row['source_reference'] == original['source_reference'] and row['source_hex'] == original['source_hex']
        assert row['source_meaning'] == original['source_meaning']
        assert row['independent_English_draft'] == original['independent_English_draft']
        assert not any(row['review'].values()) and row['contextual_comparison_saved']
        assert (row['proposed_English'] == row['current_comparison_paragraph']) == (row['decision'] == 'retention')
        row['english'] = row['proposed_English']
        row['glyph_consistency_target'] = not row['current_comparison_paragraph'].isascii()
        assert row['english'].isascii() and not any(t in row['english'] for t in ['\n','{LB','{ALIGN','{PAD'])
    counts = Counter(r['decision'] for r in rows)
    glyphs = [dict(id=r['id'], block=r['block'], source_reference=r['source_reference'],
        current_reference=r['current_reference'], current_hex=r['current_hex'],
        current_text=r['current_comparison_paragraph'], proposed_English=r['english'],
        fresh_complete_native_glyph_display_check_pending=True) for r in rows if r['glyph_consistency_target']]
    assert (counts['revision'],counts['retention']) == (139,189)
    assert all(r['id'] in {g['id'] for g in glyphs} for r in rows if r['id'] in ['SC3_B95_STYLE_400_18','SC3_B95_STYLE_400_42','DK4_MES_B85_R0004'])
    kinds = Counter(r['kind'] for r in rows)
    assert kinds == dict(ordinary_speech=0) or kinds == Counter({'ordinary-speech':289,'physical-style-alternative':24,'typed-menu-caption':15})
    save(out, dict(format='dk4-contextual-dialogue-proposals-v2', translation_policy='natural-dialogue-v2',target_locale='en-US',
        records=rows, records_count=328, complete_exchanges=21, runtime=docs[0]['runtime'], blocks=sorted({r['block'] for r in rows}),
        proposed_revisions=139, justified_retentions=189, all_individual_findings_andretention_reasons_saved=True,
        clean_meanings_preceded_drafts_andcurrent_comparisons=True, independent_drafts=str(drafts_path),
        independent_drafts_sha256=digest(drafts_path), physical_speech_objects=289, physical_style_alternatives=24,
        typed_choice_captions=15, typed_choice_objects=5, style_objects=4,
        FE_source_panels=sum(r.get('source_selector')==254 for r in rows if r['kind']=='ordinary-speech'),
        dynamic_source_selectors=Counter(r['source_selector'] for r in rows if r['kind']=='ordinary-speech' and r.get('source_selector') in [207,208]),
        source_macro_counts={t:sum(r['source_macros'].get(t,0) for r in rows) for t in ['FI','FA','FO','FU']},
        glyph_targets=glyphs, all_individual_five_review_gates_pending=True,
        final_names_terms_role_consumers_complete_prose_reread_andfresh_formatting_pending=True,
        native_style_getter_cases_already_bound=32, no_new_native_page_oractual_gameplay_approval=True,
        no_new_ROM_orcredit=True, new_credit=0, full_goal_complete=False,
        evidence={str(p):digest(p) for p in [*paths,drafts_path,Path(__file__)]}))
    print('Consolidated328 proposals:139 revisions/189 retentions;',len(glyphs),'non-ASCII targets;all gates still pending.')


if __name__ == '__main__':
    main()
