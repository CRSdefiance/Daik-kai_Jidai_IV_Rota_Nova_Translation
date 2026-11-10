"""Materialize the five complete speech-only blocks with native controls and inverses."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save
from scripts.rebuild_rafael_B141_B160_reviewed_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

A=Path('work/analysis')
DOC=Path('translations/rafael_B161_B165_formatting_manuscript_v1.json')
PLAN=A/'Rafael_B161_B165_automatic_layout_v3_20261105/automatic_plans.json'
NATIVE=A/'Rafael_B161_B165_native_v1_20261105/compiled_native_pages.json'
PACKET=A/'Rafael_B161_B165_current1607_20261105/current_effective.json'
NAMES=A/'Rafael_B161_B165_name_planes_v1_20261105/native_name_planes.json'
IDENTITY=PACKET.with_name('names_and_terms_v1.json')
INPUTS=A/'Rafael_B161_B165_storage_inputs_v1_20261105'
TEMPLATE=Path('scripts/rebuild_reviewed_editorial_batch_v4.py')


def prepare():
    assert not INPUTS.exists()
    doc,plan,native,packet,names,identity=map(load,[DOC,PLAN,NATIVE,PACKET,NAMES,IDENTITY])
    assert doc['runtime']==native['runtime']==packet['runtime']==names['runtime']==identity['runtime']
    assert native['manuscript_sha256']==plan['manuscript_sha256']==sha(DOC.read_bytes())
    assert native['plan_sha256']==sha(PLAN.read_bytes())
    assert len(doc['records'])==len(native['records'])==67 and native['pages']==68
    assert native['fresh_compiled_alignments']==268 and native['all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass']
    assert native['complete_consumption_andpagination_exact'] and native['FE_actual_glyph_row_membership_checked']
    assert names['scoped_actors']==names['distinct_strings']==8
    assert names['all_scoped_progressive_names_ASCII_complete_andfit_native216px']
    for group in packet['groups']:
        for side in ('source','current'):
            assert not any(c['word'] in (0x2100,0x2200,0x4100) for c in group[f'all_{side}_commands'])
    sheets=native['review_sheets']+names['review_sheets']
    for row in sheets:
        assert sha(Path(row['path']).read_bytes())==row['sha256']
    INPUTS.mkdir()
    shared=dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),
        runtime=doc['runtime'],plan=str(PLAN),plan_sha256=sha(PLAN.read_bytes()),new_credit=0)
    save(INPUTS/'menu.json',{**shared,'offline_visual_approved':True,'direct_view_pending':False,
        'menus':[],'typed_labels':0,'complete_clean_current_census_proves_no_choice_objects':True})
    save(INPUTS/'styles.json',{**shared,'objects':[],'complete_clean_current_census_proves_no4100_objects':True})
    save(INPUTS/'visual_review.json',{**shared,'body_pages':68,'scoped_name_count':8,'all_body_and_name_sheets_directly_viewed':True,
        'sheets':sheets,'actual_gameplay':False,'native':str(NATIVE),'native_sha256':sha(NATIVE.read_bytes()),
        'names':str(NAMES),'names_sha256':sha(NAMES.read_bytes()),
        'evidence':{str(p):sha(p.read_bytes()) for p in [DOC,PLAN,NATIVE,PACKET,NAMES,IDENTITY,Path(__file__)]}})
    print('Bound final 68 viewed speech pages, eight viewed nameplates and the no-menu/style census.')


source=checked_text(previous,{
    "len(doc['records'])==557":"len(doc['records'])==67",
    "==len(native['records'])==549":"==len(native['records'])==67",
    '==(549,0,8)':'==(67,0,0)',
    'len(changed)==20':'len(changed)==5',
    'speech_count=549':'speech_count=67',
    'total_rendered_speech_count=549':'total_rendered_speech_count=67',
    'typed_choice_count=8,compound_objects=4':'typed_choice_count=0,compound_objects=0',
    'ordinary_speeches=549':'ordinary_speeches=67',
    'menu_labels=8,changed_blocks=20':'menu_labels=0,changed_blocks=5',
    'Rafael B141-B160 complete557-object source-bound reconstruction':'Rafael B161-B165 complete67-speech source-bound reconstruction',
    'args=parser.parse_args();assert not args.out.exists()':
        "args=parser.parse_args();assert not args.out.exists()\n    assert load(INPUTS/'visual_review.json')['all_body_and_name_sheets_directly_viewed']",
})
if __name__=='__main__':
    import sys
    if sys.argv[1:]==['--prepare']:
        prepare()
    else:
        exec(compile(source,__file__+'::same-source-bound-block-rebuild-no-menu-or-style','exec'),globals())
