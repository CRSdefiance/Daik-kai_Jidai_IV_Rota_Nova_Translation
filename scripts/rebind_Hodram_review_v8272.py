"""Rebind unchanged28prose/native bodies to registered V8259;retain all historical decisions andexact QA."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.gerhard_surname_profile_v1 import validate_name_transition
from scripts.audit_native_given_name_table import string
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_current_review_binding_v8272')
OLD=Path('translations/hodram_B137_B45_B46_editorial_manuscript_v2.json')
DOC=Path('translations/hodram_B137_B45_B46_editorial_manuscript_v3.json')
OLD_NAMES=Path('translations/hodram_B137_B45_B46_speaker_name_review_v2.json')
NAMES=Path('translations/hodram_B137_B45_B46_speaker_name_review_v3.json')
CURRENT=Path('work/analysis/Hodram_B137_B45_B46_current_v8239/28_exact_clean_current_refs_after_whole_source_glosses.json')
EFFECTIVE=Path('work/analysis/Hodram_B137_B45_B46_effective_v8240/all28_effective_English_templates56_original_dispatches_no_FE.json')
PLAN=Path('work/analysis/Hodram_B137_B45_B46_layout_v8245/28_automatic_Hodram_plans_full_native_width.json')
VIEW=Path('work/analysis/Hodram_B137_B45_B46_native_review_v8247/28_native_pages_directly_viewed_two_exact_boundary_reviews.json')
TARGET_NAMES=Path('work/analysis/Hodram_target_names_v8271/six_current_identities12_getters6_native_nameplanes_own_captain1_context.json')
RELEASE=Path('work/analysis/Gerhard_surname_release_v8260/registered_release_verification.json')
INPUT=Path('work/analysis/current_V8259_Hodram_native_v8270/current_native_input.json')
if __name__=='__main__':
    assert not ROOT.exists() and not DOC.exists() and not NAMES.exists()
    old,oldnames,current,effective,plan,view,names,release,inp=map(read,[OLD,OLD_NAMES,CURRENT,EFFECTIVE,PLAN,VIEW,TARGET_NAMES,RELEASE,INPUT])
    assert names['candidate_sha256']==inp['current_ROM_sha256']==release['candidate_sha256'] and names['actual_captain']==1
    assert names['source_macro_counts']==dict(FI=0,FA=0,FO=0) and len(names['name_planes'])==6
    assert view['manuscript_sha256']==sha(OLD.read_bytes()) and len(view['original_warnings'])==2 and len(view['original_infos'])==5
    assert sha(Path(names['review_sheet']['path']).read_bytes())==names['review_sheet']['sha256']
    previous,image=NdsImage.open(old['current_ROM']),NdsImage.open(inp['current_ROM'])
    arm=image.read_file('/__arm9__.bin');inverse=validate_name_transition(previous.read_file('/__arm9__.bin'),arm)
    assert image.read_file('/data/SC1.DK4')==previous.read_file('/data/SC1.DK4') and image.read_file('/data/EV1.DK4')==previous.read_file('/data/EV1.DK4')
    assert image.read_file('/COMMON/MESFILE.DK4')==previous.read_file('/COMMON/MESFILE.DK4') and image.read_file('/GRP/KANJI.FNT')==previous.read_file('/GRP/KANJI.FNT')
    bank=IlnkContainer.parse(image.read_file('/data/SC1.DK4')).blocks
    rebound=deepcopy(current);rebound.update(current_ROM=inp['current_ROM'],current_ROM_sha256=inp['current_ROM_sha256'],current_ARM9_sha256=sha(arm),
        current_COMMON_sha256=sha(image.read_file('/COMMON/MESFILE.DK4')),previous_exact_reference_packet=str(CURRENT),previous_exact_reference_packet_sha256=sha(CURRENT.read_bytes()),
        own_current_Hodram_input=str(INPUT),own_current_Hodram_input_sha256=sha(INPUT.read_bytes()),
        all28_current_storage_refs_andall60_commands_byte_exact_to_prior_mapping=True,
        all28_effective_templates_exact_reuse_from_original56_dispatches_not56fresh_calls=True,
        effective_template_proof=str(EFFECTIVE),effective_template_proof_sha256=sha(EFFECTIVE.read_bytes()),
        Gerhard_registered_Adernkatz_dependency_fulfilled=True,name_asset_dependency=release['profile'])
    for group in rebound['groups']:assert bytes.fromhex(group['current_block_hex'])==bank[group['block']]
    doc=deepcopy(old);doc.update(prior_manuscript=str(OLD),prior_manuscript_sha256=sha(OLD.read_bytes()),current_ROM=inp['current_ROM'],current_ROM_sha256=inp['current_ROM_sha256'],
        current_ARM9_sha256=sha(arm),current_COMMON_sha256=inp['current_COMMON_sha256'],current_archive_sha256=sha(image.read_file('/data/SC1.DK4')),names_packet=str(NAMES),
        required_registered_name_asset=dict(profile=release['profile'],candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],ARM9_sha256=release['ARM9_sha256'],
            registration=release['verified_registration_receipt'],registration_sha256=release['verified_registration_receipt_sha256']),
        own_current_native_input=str(INPUT),own_current_native_input_sha256=sha(INPUT.read_bytes()),
        current_name_andbody_code_font_pool_andSC1_rebinding_by_exact_inverse=True)
    warnings={r['id']:r for r in view['original_warnings']}
    for row,earlier,p in zip(doc['records'],old['records'],plan['records'],strict=True):
        assert row['id']==earlier['id']==p['id'] and row['english']==earlier['english']==' '.join(p['lines'])
        ref=row['current_reference'];raw=bytes.fromhex(row['current_hex']);assert bank[row['block']][ref['offset']:ref['offset']+len(raw)+1]==raw+b'\0'
        assert bank[row['block']][ref['header_offset']:ref['offset']+1].hex()==row['source_complete_preamble_hex']
        row.update(compiled_hex=p['encoded_hex'],planned_English_markup=p['planning_record']['english'],formatted_markup=p['formatted_markup'],all_original_QA_issues=p['base_QA']['issues'],native_page_count=1,
            qa_waivers=['weak-line-ending'] if row['id'] in warnings else [],qa_waiver_reason=warnings[row['id']]['reason'] if row['id'] in warnings else None,
            qa_waiver_scope=dict(id=row['id'],source_hex=row['source_hex'],compiled_hex=p['encoded_hex'],exact_issue=warnings[row['id']]['issue'],generated_lines=p['lines']) if row['id'] in warnings else None,
            current_reference_ROM=inp['current_ROM'],current_reference_ROM_sha256=inp['current_ROM_sha256'],current_ARM9_name_dependency_registered=True,
            current_body_source_refs_preambles_andeffective_template_exact_to_previous_mapping=True,
            original_prose_andindividual_reasons_unchanged=True,native_body_plane_exact_code_font_binding_reused=True)
        assert not row['review']['formatting']
    namedoc=deepcopy(oldnames)
    for row in namedoc['records']:
        actor=row['actor_ID'];row['original_getters']=[r for r in names['native_twelve_progressive_andfull_getters']['rows'] if r['actor_ID']==actor]
        fields=[]
        for field in row['current_fields']:
            at=field['table_field'];pointer=int.from_bytes(arm[at:at+4],'little')
            fields.append(dict(kind=field['kind'],table_field=at,table_field_hex=arm[at:at+4].hex(),**string(arm,pointer)))
        row['current_fields']=fields
        if actor==16:
            row.update(prior_surname_decision='revision-now-integrated-in-V8259',decision='retention',
                retention_reason='Retain the registered Gerhard Adernkatz forゲルハルト/アーデルンカッツ. Whole295-speech name-context review andregistered six-consumer correction already resolved the spelling. The Hodram apology/staffing exchange uses the same identity without a new rank,kinship orbiography;no further name asset change isneeded.')
        row.update(native_name_plane=next(r for r in names['name_planes'] if r['actor_ID']==actor),
            current_registered_candidate=inp['current_ROM'],current_registered_candidate_sha256=inp['current_ROM_sha256'],
            actual_new_scene_headers_not_yet_observed=True,native_full_glyph_planes_bounds_andactual_headers_pending=False,
            current_six_native_nameplanes_directly_viewed=True,actual_Hodram_B137_B45_B46_headers_still_pending=True,new_name_asset_change=False)
        assert not row['review']['formatting']
    namedoc.update(prior_review=str(OLD_NAMES),prior_review_sha256=sha(OLD_NAMES.read_bytes()),native_name_proof=str(TARGET_NAMES),native_name_proof_sha256=sha(TARGET_NAMES.read_bytes()),
        current_ROM=inp['current_ROM'],current_ROM_sha256=inp['current_ROM_sha256'],six_current_nameplanes_directly_viewed=True,
        surname_source_localization_decision_resolved_assets_andformatting_pending=False,surname_asset_registered_in_V8259_actual_Hodram_headers_pending=True,
        source_only_body_phase_no_current_Hodram_B137_B45_B46_dialogue_English_consulted=False,
        five_individual_retentions_one_source_based_surname_revision_allformatting_pending=False,
        six_current_individual_retentions_no_new_asset_all_Hodram_formatting_gates_pending=True)
    ROOT.mkdir(parents=True);save(NAMES,namedoc);save(DOC,doc)
    packet=ROOT/'28_exact_current_refs_registered_name_dependency_andnative_reuse.json';save(packet,rebound)
    save(ROOT/'current_review_andnative_reuse_receipt.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),names=str(NAMES),names_sha256=sha(NAMES.read_bytes()),
        current_packet=str(packet),current_packet_sha256=sha(packet.read_bytes()),candidate=inp['current_ROM'],candidate_sha256=inp['current_ROM_sha256'],
        complete_ARM9_name_inverse=inverse,SC1_EV1_COMMON_font_andall_ARM9_except_owned_name_exact=True,
        no_repeated_112_compiled_body_cases_when_exact_code_font_body_andphase_provenance_rebind=True,
        all28_prose_andindividual_reasons_unchanged_16revisions12retentions=True,
        original_two_exact_warning_exceptions_andfive_infos_preserved=True,
        six_native_nameplanes_directly_viewed=True,no_Hodram_scene_orcatalogue_UI_customname_hardware_coverage_claim=True,
        all28_dialogue_andall6_name_formatting_gates_remain_false=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [OLD,OLD_NAMES,CURRENT,EFFECTIVE,PLAN,VIEW,TARGET_NAMES,RELEASE,INPUT,Path(__file__)]}))
    print('ReboundHodram28/sixnames toV8259:proseexact/16rev12ret,source-current refs and112nativebody cases reusedbywholeinverse;two warnings/fiveinfos retained.Allformattingfalse.')
