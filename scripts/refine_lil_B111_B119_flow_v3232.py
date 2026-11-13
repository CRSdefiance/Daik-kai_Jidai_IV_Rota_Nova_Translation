"""Preserve all reviewed prose; keep one visually split idiom together."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B111_B119_refinement_v3232')
OLD=Path('dk4tool/dialogue/lil_B111_B119_layout_v1.py')
NEW=Path('dk4tool/dialogue/lil_B111_B119_layout_v2.py')

if __name__=='__main__':
    assert not ROOT.exists() and not NEW.exists()
    text=OLD.read_text(encoding='utf-8')
    anchor='PROTECTED_BOUNDARIES=frozenset({'
    assert text.count(anchor)==1
    NEW.write_text(text.replace(anchor,anchor+"('sharp','tongue'),"),encoding='utf-8')
    sheets=[]
    for path in [Path('work/analysis/lil_B111_B119_fonts_v3230b/current_macro_QA_and_progressive_font_proof.json'),Path('work/analysis/lil_B111_B119_FE_v3231/current_FE_macro_font_and_typed_paper_proof.json')]:
        for s in read(path)['review_sheets']:
            assert sha(Path(s['path']).read_bytes())==s['sha256']
            sheets.append({**s,'review':'viewed complete native rendered sheet'})
    assert len(sheets)==20
    ROOT.mkdir(parents=True)
    save(ROOT/'native_visual_findings_and_successor_receipt.json',dict(
        all19_progressive_and1_FE_sheets_viewed=True,review_sheets=sheets,
        concrete_finding=dict(id='DK4_MES_B111_R0112',finding='Camille idiom sharp tongue splits between rows on sheet4; keep the established idiom together.',resolution='Add this exact pair only to the local successor planner; preserve logical English and source meaning.'),
        justified_format_retentions=[
            dict(id='DK_VOICE_B117_C448_T386',reason='We can make / this into a figurehead! Look! is readable and preserves the source potential reuse rather than asserting original identity; no new protected verb-object rule or prose shortening is warranted.'),
            dict(id='DK4_MES_B118_R0020',reason='The complete source-unlabeled 24,000-gold notice is legible on one native FE line with first and final glyphs intact.'),
            dict(scope='remaining viewed sheets',reason='Complete glyphs and readable paragraph progression, including deliberate silences, all conditional style voices and unexpanded source macros; retain reviewed words.')],
        previous_formatter=str(OLD),previous_formatter_sha256=sha(OLD.read_bytes()),
        successor_formatter=str(NEW),successor_formatter_sha256=sha(NEW.read_bytes()),
        no_prose_source_or_global_helper_change=True,no_ROM_registry_ledger_or_editorial_credit=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    old=Path('scripts/prepare_lil_B111_B119_layout_v3229.py')
    new=Path('scripts/prepare_lil_B111_B119_layout_v3233.py')
    assert not new.exists()
    script=old.read_text(encoding='utf-8')
    swaps={
        'lil_B111_B119_layout_v3229':'lil_B111_B119_layout_v3233',
        'lil_B111_B119_layout_v1':'lil_B111_B119_layout_v2',
        "INPUTS=[Path('translations/lil_B111_B119_editorial_manuscript_v2.json'),\n        Path('translations/lil_B111_B119_actor_style_manuscript_v1.json')]":"INPUTS=[Path('translations/lil_B111_B119_editorial_manuscript_v3.json'),\n        Path('translations/lil_B111_B119_actor_style_manuscript_v2.json')]",
        "OUTPUTS=[Path('translations/lil_B111_B119_editorial_manuscript_v3.json'),\n         Path('translations/lil_B111_B119_actor_style_manuscript_v2.json')]":"OUTPUTS=[Path('translations/lil_B111_B119_editorial_manuscript_v4.json'),\n         Path('translations/lil_B111_B119_actor_style_manuscript_v3.json')]"}
    for a,b in swaps.items():
        assert a in script,a
        script=script.replace(a,b)
    anchor="            raw=bytes.fromhex(row['source_hex']);prefix=row['source_selector']"
    assert script.count(anchor)==1
    script=script.replace(anchor,"""            if row.get('qa_waiver_reason'):
                suffix=' '+row['qa_waiver_reason']
                assert row['localization_note'].endswith(suffix)
                row['localization_note']=row['localization_note'][:-len(suffix)]
            row.pop('qa_waivers',None);row.pop('qa_waiver_reason',None)
"""+anchor)
    new.write_text(script,encoding='utf-8')
    print('All20 sheets viewed; one local sharp-tongue flow refinement, all words retained. Layout successor prepared.')
