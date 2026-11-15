"""Record direct visual findings and preserve the first immutable prose packet."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

BASE=Path('work/analysis/Hodram_B91_B110_visual_20261101')
OLD=Path('translations/hodram_B91_B110_editorial_manuscript_v1.json')
NEW=Path('translations/hodram_B91_B110_editorial_manuscript_v2.json')

if __name__=='__main__':
    assert not NEW.exists() and not (BASE/'initial_visual_review.json').exists()
    pending=load(BASE/'visual_coverage_pending.json')
    assert len(pending['review_sheets'])==17 and pending['pages']==216
    for sheet in pending['review_sheets']:
        assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    findings={
        'DK4_MES_B95_R0026':'Page1 ends I carried; keep the complete attachment sentence on page2.',
        'DK4_MES_B100_R0021':'How mysterious is stranded on page2. The source confirmation question can read See the bee in this amber? rather than the redundant Look, can you see; preserve the poetic description and wonder.',
        'DK4_MES_B102_R0041':'The Cape of Good Hope is split and page1 ends That\'s all. Keep the place name and the complete final sentence coherent.',
        'DK4_MES_B103_R0038':'Page1 ends I\'ll and page2 has let you know. Keep the complete conditional offer together.',
        'DK4_MES_B104_R0013':'Page1 ends moon\'s uneven and page2 has surface in detail. Keep the complete attributed second sentence on page2.',
    }
    retained={
        'DK4_MES_B101_R0060':'Page1 completes the uncertain Mediterranean/Black Sea question. Page2 is the complete admission of no serious prior search; its trailing but intentionally leads to the next speech. No authored break.',
        'DK4_MES_B110_R0047':'Page1 completes the warning and commitment condition. Page2 poses the complete resolve challenge. No sentence fragment or short tag, and no authored dramatic break.',
    }
    save(BASE/'initial_visual_review.json',dict(
        status='all initial unique pages directly viewed; five specific refinements pending',
        pending_receipt_sha256=sha((BASE/'visual_coverage_pending.json').read_bytes()),
        directly_viewed_sheets=pending['review_sheets'],fresh_unique_pages=199,
        previously_approved_exact_planes=11,duplicate_new_planes=6,pages=216,
        first_last_glyphs_andfont_consistent=True,clipping_orbounds_findings=0,
        findings=findings,two_page_retentions=retained,actual_gameplay=False,new_credit=0))
    doc=deepcopy(load(OLD));row=next(r for r in doc['records'] if r['id']=='DK4_MES_B100_R0021')
    before=row['english'];after=before.replace('Look, can you see the bee','See the bee',1)
    assert before.startswith('Look, can you see the bee') and row['decision']=='revision'
    reason='Render the source pointing/confirmation question 見えるでしょう as See the bee in this amber?; avoid a redundant attention cue plus an ability question. Retain the bee, thousands of years, sepia miniature universe and expression of wonder.'
    row.update(english=after,logical_English=after,planned_English_markup=row['planned_English_markup'].split('}',1)[0]+'}'+after)
    row['localization_note']+=' '+reason;row['finding']+=' '+reason
    doc.update(previous_manuscript=str(OLD),previous_manuscript_sha256=sha(OLD.read_bytes()),
        visual_refinement_reference=str(BASE/'initial_visual_review.json'),
        automatic_page_coherence_findings=findings,automatic_page_coherence_retentions=retained)
    doc['post_prose_refinements'].append(dict(id=row['id'],before=before,after=after,reason=reason))
    assert doc['revised']==129 and doc['retained']==82 and all(not r['review']['formatting'] for r in doc['records'])
    save(NEW,doc)
    print(dict(objects=211,revisions=129,retentions=82,initial_pages_directly_viewed=216,findings=5,formatting_approved=0))
