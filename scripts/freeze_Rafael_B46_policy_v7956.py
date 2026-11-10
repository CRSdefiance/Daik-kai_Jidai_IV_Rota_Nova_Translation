"""Freeze approved B46 prose and both typed choices without changing base guards."""
from pathlib import Path
from scripts import freeze_Rafael_B45_policy_v7901 as previous
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read, save
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.dialogue.rafael_B45_profile_v1 import contract as prior_contract

ROOT = Path('work/analysis/Rafael_B46_policy_v7956')
DOC = Path('translations/rafael_B46_editorial_manuscript_v3.json')
NAMES = Path('translations/rafael_B46_speaker_name_review_v2.json')
PLAN = Path('work/analysis/Rafael_B46_layout_v7932/24_automatic_plans_full_native_width_zero_preamble_separate_body.json')
CURRENT = Path('work/analysis/Rafael_B46_current_v7927/all24_speeches2_choices_source_current_refs_before_new_English_manuscript.json')
NATIVE = Path('work/analysis/Rafael_B46_pages_v7933/24_complete_native_pages96_compiled_alignments12_FE.json')
APPROVAL = Path('work/analysis/Rafael_B46_actual_approval_v7953/26_source_context_native_actual_approved_policy_release_pending.json')
CHOICE = Path('work/analysis/Rafael_B46_choice_planes_v7934/two_labels8_native_style_planes_trimmed_native_width_andthree_returns.json')
CONTRACT = Path('translations/rafael_B46_native_contract_v1.json')
PROFILE = Path('dk4tool/dialogue/rafael_B46_profile_v1.py')
FORMATTER = Path('dk4tool/dialogue/rafael_B46_layout_v1.py')
PLANNER = Path('dk4tool/dialogue/rafael_B46_plan_v1.py')
CHOICES = Path('dk4tool/dialogue/rafael_B46_choices_v1.py')
GATES = ['source', 'context', 'localization', 'naturalness', 'formatting']
BOUND_FIELDS = [
    'id', 'file_path', 'block', 'kind', 'english', 'source_hex', 'current_hex',
    'source_reference', 'current_reference', 'speaker', 'source_meaning',
    'context', 'localization_note', 'decision', 'editorial_decision',
    'retention_reason', 'editorial_finding',
]

PROFILE_SOURCE = checked_text(previous.PROFILE_SOURCE, {
    'B45': 'B46', 'B-45': 'B-46',
} if 'B-45' in previous.PROFILE_SOURCE else {'B45': 'B46'})
PROFILE_SOURCE = checked_text(PROFILE_SOURCE, {
    '!=12 or d["choice_bindings"]': '!=24 or len(d["choice_bindings"])!=2',
    'd["complete_native_pages"]!=12': 'd["complete_native_pages"]!=24',
    'Complete twelve-paragraph/no-menu contract required': 'Complete24-speech/two-choice contract required',
    '{"FI":0,"FA":0,"FO":1}': '{"FI":0,"FA":0,"FO":0}',
    'else {0,6}': 'else {0,5,6}',
    'One-step RNG timing difference retained;future random outcomes not proved equal.':
        'Menu highlight-off phase and later measured simulation/calendar/RGB/RNG differences retained;no full causal orfuture-state equivalence claim.',
})
PROFILE_SOURCE += '''

def validate_approved_batch(doc):
    from dk4tool.dialogue.review import validate_natural_dialogue_batch
    d=contract()
    for key,value in d["batch_binding"].items():
        if doc.get(key)!=value:raise ValueError("Exact B46 approved batch metadata required:"+key)
    validate_natural_dialogue_batch(doc)
    choice_doc={**doc,"records":doc.get("typed_choice_records")}
    validate_natural_dialogue_batch(choice_doc)
    for field,bindings in [("records",d["record_bindings"]),("typed_choice_records",d["choice_bindings"])]:
        rows=doc.get(field)
        if not isinstance(rows,list) or [r.get("id") for r in rows if isinstance(r,dict)]!=list(bindings):
            raise ValueError("Exact complete ordered B46 approved records required:"+field)
        for row in rows:
            b=bindings[row["id"]]
            if any(row.get(k)!=v for k,v in b["approved_fields"].items()):
                raise ValueError("Exact B46 approved prose/source/context required:"+row["id"])
            if not isinstance(row.get("review"),dict) or not all(row["review"].get(g) is True for g in d["review_gates"]):
                raise ValueError("All five individual B46 gates required:"+row["id"])
    return d
'''
FORMATTER_SOURCE = checked_text(previous.FORMATTER_SOURCE, {'B45': 'B46'})
PLANNER_SOURCE = checked_text(previous.PLANNER_SOURCE, {
    'B45': 'B46',
    'plan_Rafael_B45_layout_v7881b': 'plan_Rafael_B46_layout_v7932',
})
CHOICES_SOURCE = '''"""Exact reviewed B46 labels in original order; native provider owns sizing."""
import struct
from dk4tool.dialogue.rafael_B46_profile_v1 import contract

def compile_choices(rows):
    d=contract();bindings=d["choice_bindings"]
    if not isinstance(rows,list) or len(rows)!=2 or any(not isinstance(r,dict) for r in rows) or [r.get("id") for r in rows]!=list(bindings):
        raise ValueError("Exact B46 two-choice source order required")
    chunks=[];offsets=[];cursor=0
    for row in rows:
        b=bindings[row["id"]]
        if any(row.get(k)!=v for k,v in b["approved_fields"].items()):
            raise ValueError("Exact B46 choice source/prose/context required:"+row["id"])
        if not isinstance(row.get("review"),dict) or not all(row["review"].get(g) is True for g in d["review_gates"]):
            raise ValueError("All five individual B46 choice gates required")
        offsets.append(cursor);chunk=row["english"].encode("ascii")+b"\\0"
        chunk+=bytes(-len(chunk)%2);chunks.append(chunk);cursor+=len(chunk)
    result=struct.pack("<3H",0x2100,*offsets)+b"".join(chunks)
    if offsets!=[0,12] or result.hex()!=d["choice_object_hex"]:
        raise ValueError("Exact B46 original-count/source-index native choice object required")
    return result
'''

if __name__ == '__main__':
    assert not ROOT.exists() and all(not p.exists() for p in [CONTRACT, PROFILE, FORMATTER, PLANNER, CHOICES])
    doc,names,plan,current,native,approval,choice = map(read,[DOC,NAMES,PLAN,CURRENT,NATIVE,APPROVAL,CHOICE])
    assert approval['manuscript_sha256']==sha(DOC.read_bytes()) and approval['names_sha256']==sha(NAMES.read_bytes())
    assert native['plan_sha256']==sha(PLAN.read_bytes()) and not plan['failures']
    assert approval['all26_individual_source_context_prose_andformat_gates_true']
    assert approval['actual_complete_holds']==214 and approval['actual_speech_occurrences']==58
    assert approval['all37_original_commands_observed_across_both_paths_each_language']
    assert approval['source_only_menu4930_highlight_off_andcrosslanguage_phase_limit_retained']
    assert approval['actual_later_models_persistent_objects_actors_andaccept_calendar_differences_preserved']
    assert approval['disclosed_opening_ROM_entry_fixture_not_natural_B46_activation_original_location_fullroute_orhardware']
    assert len(approval['directly_viewed_sheets'])==14 and all(s['directly_viewed'] for s in approval['directly_viewed_sheets'])
    old=prior_contract()
    deps={Path(p) for p in old['dependencies']} | {DOC,NAMES,PLAN,CURRENT,NATIVE,APPROVAL,CHOICE,Path(__file__),Path(previous.__file__)}
    for key in ['actual_proof','actual_menu_proof','comparison','RNG_measurement']:
        p=Path(approval[key]);assert sha(p.read_bytes())==approval[key+'_sha256'];deps.add(p)
    for s in approval['directly_viewed_sheets']:
        p=Path(s['path']);assert sha(p.read_bytes())==s['sha256'];deps.add(p)
    image=NdsImage.open(current['current_ROM'])
    assert sha(Path(current['current_ROM']).read_bytes())==current['current_ROM_sha256']
    group=current['groups'][0]
    bindings={}
    for row,p,n,c in zip(doc['records'],plan['records'],native['records'],current['records'],strict=True):
        assert row['id']==p['id']==n['id']==c['id'] and row['english']==p['planning_record']['english']
        assert row['source_hex']==p['source_hex']==c['source_hex'] and row['current_hex']==c['current_hex']
        assert row['compiled_hex']==p['encoded_hex']==n['compiled_hex']
        assert all(row['review'][g] is True for g in GATES)
        assert len(n['pages'])==p['expected_native_pages']==1
        assert not any(i['severity'] in ['warning','error'] for i in p['base_QA']['issues'])
        row_info=any(i['code']=='line-break-count' for i in p['base_QA']['issues'])
        assert row['row_count_reason']
        fields=BOUND_FIELDS+['source_complete_preamble_hex','source_selector','compiled_hex']
        bindings[row['id']]=dict(
            file_path=row['file_path'],route=0,route_identity='Rafael',block=46,
            source_block_hashes=[group['clean_block_sha256'],group['current_block_sha256']],
            source_header_hex=group['source_header_hex'],current_header_hex=group['current_header_hex'],
            source_reference=row['source_reference'],current_reference=row['current_reference'],
            source_complete_preamble_hex=row['source_complete_preamble_hex'],compiler_source_hex=row['source_hex'],
            predecessor_record_hex=row['current_hex'],source_selector=row['source_selector'],source_kind=row['kind'],
            consumer='FE-paper' if row['source_selector']==254 else 'progressive',
            planning_record={k:p['planning_record'][k] for k in ['id','english','kind','source_hex','source_selector']},
            compiled_hex=p['encoded_hex'],lines=p['lines'],maximum_total_rows=4,native_page_count=1,
            row_count_reason=row['row_count_reason'] if row_info else None,
            ordinary_wrap_reasons=[row['row_count_reason']],base_QA_issues=p['base_QA']['issues'],
            approved_fields={k:row[k] for k in fields})
        for pg in n['pages']:
            for pathkey,hashkey in [('native_plane','native_plane_sha256'),('preview','preview_sha256')]:
                path=Path(pg[pathkey]);assert sha(path.read_bytes())==pg[hashkey];deps.add(path)
    assert len(bindings)==24 and sum(b['source_selector']==0 for b in bindings.values())==4
    assert sum(b['source_selector']==254 for b in bindings.values())==12
    infos=sum(bool(b['row_count_reason']) for b in bindings.values());assert infos==14
    choices={}
    for idx,(row,c) in enumerate(zip(doc['typed_choice_records'],current['typed_choice_records'],strict=True)):
        assert row['id']==c['id'] and row['option_index']==idx and row['command_offset']==256
        assert row['source_hex']==c['source_hex'] and row['current_hex']==c['current_hex']
        assert all(row['review'][g] is True for g in GATES)
        assert row['english'].encode('ascii').hex()==row['compiled_hex']
        fields=BOUND_FIELDS+['option_index','command_offset','source_terminator_hex','current_command_offset','compiled_hex']
        choices[row['id']]=dict(option_index=idx,approved_fields={k:row[k] for k in fields})
    assert len(choices)==2 and choice['target_menu_bytes']==30 and choice['previous_menu_bytes']==36
    menuhex=choice['target_menu_object_hex']
    assert all(r['target_menu_object_hex']==menuhex for r in doc['typed_choice_records'])
    for path in [
        'scripts/plan_Rafael_B46_layout_v7932.py',
        'work/analysis/Rafael_B46_stored_v7939/all24_stored_bodies44_fresh52_reused_alignments_exact_viewed_planes.json',
        'work/analysis/Rafael_B46_stored_v7939/two_stored_menu_labels_exact8_viewed_planes_two_header_alignments.json',
        'work/analysis/Rafael_B46_relocated_controls_v7940/24_stored_dispatches_two_choices20_relative_cases25_seeded_ends.json',
        'work/analysis/Rafael_B46_relocation_v7938/one_block24_speeches2_choices4_fixups20_cases_exact_full_inverse.json',
        'work/analysis/Rafael_B46_loaders_v7942/343_whole_native_loads_cache_hits686_initial_parent_modes.json',
        'work/analysis/Rafael_B46_reference_census_v7943/all37_commands_four_relative_sites_two_choices_EV0_entry_shipped_callers.json',
    ]:deps.add(Path(path))
    planner=PLANNER_SOURCE.replace('PLAN_PATH',PLAN.as_posix()).replace('PLAN_DIGEST',sha(PLAN.read_bytes()))
    profile=PROFILE_SOURCE.replace('CONTRACT_PATH',CONTRACT.as_posix())
    sources=[(PLANNER,planner),(FORMATTER,FORMATTER_SOURCE),(CHOICES,CHOICES_SOURCE)]
    for path,text in sources+[(PROFILE,profile.replace('CONTRACT_DIGEST','0'*64))]:compile(text,str(path),'exec')
    for path,text in sources:path.write_text(text,encoding='utf8');deps.add(path)
    runtime={p:sha(image.read_file(p)) for p in ['/__arm9__.bin','/COMMON/MESFILE.DK4','/GRP/KANJI.FNT','/data/EV0.DK4']}
    save(CONTRACT,dict(
        format='Rafael-B46-source-native-contract-v1',record_bindings=bindings,choice_bindings=choices,
        choice_object_hex=menuhex,review_gates=GATES,
        batch_binding={k:doc[k] for k in ['translation_policy','target_locale','encoder','review_gates','file_path','route','route_identity','block']},
        source_block_hashes=[group['clean_block_sha256'],group['current_block_sha256']],
        runtime_component_hashes=runtime,measured_macro_ascii_lengths=dict(FI=6,FA=6,FO=10),source_macro_counts=dict(FI=0,FA=0,FO=0),
        physical_native_rows_per_page=4,physical_progressive_viewport=[216,64],FE_logical_bitmap=[228,48],FE_physical_bitmap=[228,64],
        usable_text_width_px=216,complete_native_pages=24,dependencies={str(p):sha(p.read_bytes()) for p in sorted(deps)},
        all26_source_context_native_stored_andactual_checks_bound=True,
        all_original_base_QA_issues_preserved_no_warning_removal_orwaivers=True,individual_row_count_infos=infos,
        exact_original_source00_preambles_andbody_NUL_rejection_preserved=True,
        actual_highlight_off_andlater_simulation_calendar_RGB_RNG_differences_retained=True,
        frozen_policy_validation_atomic_andregistered_release_pending=True,new_credit=0,full_goal_complete=False))
    PROFILE.write_text(profile.replace('CONTRACT_DIGEST',sha(CONTRACT.read_bytes())),encoding='utf8')
    ROOT.mkdir(parents=True)
    save(ROOT/'prepared24_speeches2_choices_exact_native_policy.json',dict(
        contract=str(CONTRACT),contract_sha256=sha(CONTRACT.read_bytes()),
        files={str(p):sha(p.read_bytes()) for p in [PROFILE,FORMATTER,PLANNER,CHOICES]},
        source_locked_template=str(previous.__file__),source_locked_template_sha256=sha(Path(previous.__file__).read_bytes()),
        records=24,choices=2,row_count_infos=infos,zero_warning_waivers=True,
        all_five_per_record_gates_true_actual_andmeasured_limits_bound=True,
        policy_challenges_atomic_production_andregistered_release_pending=True,new_credit=0,full_goal_complete=False))
    print('Frozen B46:24 speeches,2 choices,14 unchanged row-count infos;policy challenges andatomic integration pending.')
