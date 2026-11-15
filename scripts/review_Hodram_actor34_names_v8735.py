"""Scoped source-based retention of actor34 names; do not replace game names with lore."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_actor34_name_review_v8735')
OLD_NAMES=Path('translations/hodram_B31_B53_speaker_name_review_v1.json')
NAMES=Path('translations/hodram_B31_B53_speaker_name_review_v2.json')
OLD_DOC=Path('translations/hodram_B31_B53_editorial_manuscript_v2.json')
DOC=Path('translations/hodram_B31_B53_editorial_manuscript_v3.json')
SOURCE=Path('work/analysis/Hodram_actor34_clean_name_composition_v8732/clean_source_full_andprogressive_name_composition.json')
PLANES=Path('work/analysis/Hodram_actor34_source_name_planes_v8733b/source_complete_names_andcurrent_reuse.json')
INDEPENDENT=Path('work/analysis/Hodram_B31_B53_independent_v8734/independent_reconstruction.json')
if __name__=='__main__':
    assert not ROOT.exists() and not NAMES.exists() and not DOC.exists()
    oldnames,old,source,planes,independent=map(read,[OLD_NAMES,OLD_DOC,SOURCE,PLANES,INDEPENDENT])
    assert planes['source_sha256']==sha(SOURCE.read_bytes()) and source['source_middle_field_is_actually_composed_byoriginal_full_getter_not_automatically_unused']
    sheet=planes['review_sheet'];assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    assert [(r['text'],r['rows']) for r in planes['source_name_planes']]==[('バルバロッサ・ハイレディン',1),('バルバロッサ・ファーズル・ハイレディン',2)]
    assert independent['manuscript_sha256']==sha(OLD_DOC.read_bytes()) and independent['whole_target_blocks_andarchive_byte_equal_to_sparse_rebuild']
    names=deepcopy(oldnames);row=names['records'][0];assert row['actor_ID']==34 and row['speaker']=='Barbarossa Hayreddin'
    original_finding=deepcopy(names.pop('full_name_open_finding'))
    resolution=dict(actor_ID=34,decision='scoped-retention',progressive_name='Barbarossa Hayreddin',full_name_editorial_spelling='Barbarossa Fazul Hayreddin',
        exact_current_full_getter='Barbarossa Ｆazul Hayreddin',exact_current_middle_hex='8265617a756c',
        source_progressive='バルバロッサ・ハイレディン',source_full='バルバロッサ・ファーズル・ハイレディン',
        reason='Retain the established Barbarossa and Hayreddin components and the game\'s given-then-surname order, now verified through the actual original clean progressive getter. Retain Fazul as the established, plausible romanization of ファーズル: the original full getter actually inserts that source middle field between the same two components. Removing it would discard source content; replacing or reordering it from historical biography would introduce a different naming authority. These are proper-name components, not a translated rank, blood relationship or new biography. A dialogue mention of Hayreddin can naturally use the shorter verified component without changing his complete speaker identity.',
        native_storage_note='The current full getter stores the initial F as full-width Ｆ. Retain those exact existing bytes in this dialogue batch. The unchanged native current literal plane displays every component completely in one row; no claim is made that its internal character encoding is an editorial spelling distinction. No name assets, global metrics or controls are changed.',
        source_plane_qualification='The original Japanese full getter has19 CP932 glyphs. In the explicitly tested216px name-style canvas its final ン wraps to a second row at[0,16], with complete native and independent pixels. The initial one-row test8733 stopped on that source fact and is preserved. Successor8733b checks every exact glyph and position under the same geometry; it does not widen the canvas or waive a missing character. This literal test is not a measurement or observation of the actual full-catalogue UI.',
        clean_consumer_proof=str(SOURCE),clean_consumer_proof_sha256=sha(SOURCE.read_bytes()),source_current_native_planes=str(PLANES),source_current_native_planes_sha256=sha(PLANES.read_bytes()),
        directly_viewed_source_current_sheet=sheet,source_middle_field_andprogressive_order_questions_resolved=True,
        actual_B31_progressive_header_andrelevant_catalogue_UI_coverage_still_unobserved=True,
        full207_names_roles_aliases_customnames_andother_consumer_scope_still_open=True,name_asset_bytes_changed=0)
    row.update(decision='scoped-retention',reason=resolution['reason'],full_name_resolution=resolution,
        review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),actual_scene_header_andfull_editorial_name_decision_pending=False,
        actual_scene_header_andfinal_formatting_pending=True)
    names.update(prior_review=str(OLD_NAMES),prior_review_sha256=sha(OLD_NAMES.read_bytes()),prior_full_name_open_finding=original_finding,full_name_resolution=resolution,
        source_full_name_composition_andscoped_editorial_retention_complete=True,actual_headers_formatting_andwider_catalogue_UI_pending=True)
    save(NAMES,names)
    doc=deepcopy(old);doc.update(predecessor_manuscript=str(OLD_DOC),predecessor_manuscript_sha256=sha(OLD_DOC.read_bytes()),names_packet=str(NAMES),names_packet_sha256=sha(NAMES.read_bytes()),
        names_actor34_fullreview_still_pending=False,scoped_name_source_composition_andfour_prose_gates_complete=True,
        wider_catalogue_UI_full207_names_andactual_B31_B53_headers_not_approved=True,
        status='contextual-prose-native-stored-andscoped-names-reviewed-independent-actual-policy-release-pending')
    assert doc['records']==old['records'] and doc['typed_choice_records']==old['typed_choice_records']
    save(DOC,doc);ROOT.mkdir(parents=True)
    save(ROOT/'scoped_name_retention_andunchanged_prose.json',dict(names=str(NAMES),names_sha256=sha(NAMES.read_bytes()),manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),
        prior_names=str(OLD_NAMES),prior_names_sha256=sha(OLD_NAMES.read_bytes()),prior_manuscript=str(OLD_DOC),prior_manuscript_sha256=sha(OLD_DOC.read_bytes()),
        resolution=resolution,all3_approved_prose_records_compiledbytes_exact_source_current_refs_andreview_gates_unchanged=True,
        actor34_and113_four_prose_name_gates_true_formatting_false=True,all_prior_native_stored_proofs_bind_identical_records_not_replayed=True,
        no_ROM_name_asset_registry_orcredit_change=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [OLD_NAMES,NAMES,OLD_DOC,DOC,SOURCE,PLANES,INDEPENDENT,Path(__file__)]}))
    print('Actor34 scoped names retained fromactual clean getter composition,including Fazul. Existing mixed-width storage exact;fullcatalogue UI/all207 remain open. Three prose records unchanged;formatting/actual/release pending.',flush=True)
