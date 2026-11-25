"""Freeze five sparse Lil speech revisions and one owned surname span without changing global compilers."""
import ast,sys
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Gerhard_policy_v8236')
DOC=Path('translations/gerhard_surname_consistency_manuscript_v2.json')
CONTRACT=Path('translations/gerhard_surname_native_contract_v1.json')
PROFILE=Path('dk4tool/dialogue/gerhard_surname_profile_v1.py')
FORMATTER=Path('dk4tool/dialogue/gerhard_surname_layout_v1.py')
PLANNER=Path('dk4tool/dialogue/gerhard_surname_plan_v1.py')
PLAN=Path('work/analysis/Gerhard_layout_v8205/5_automatic_Lil_plans_full_native_width.json')
CURRENT=Path('work/analysis/Gerhard_surname_five_v8199/five_prior_completed_source_current_refs_andwhole295_source_context_receipt.json')
APPROVAL=Path('work/analysis/Gerhard_actual_approval_v8233/scoped_actual_format_approval.json')
REFERENCE=Path('work/analysis/Gerhard_reference_v8215/research_image_receipt.json')
OWNERSHIP=Path('work/analysis/Gerhard_name_ownership_v8203/current12_byte_surname_owned_original20_contains_protected_Blades.json')

NAME_CODE='''
def validate_name_records(doc):
    d=contract();rows=doc.get("name_records")
    if not isinstance(rows,list) or len(rows)!=1 or not isinstance(rows[0],dict):
        raise ValueError("Exactly one owned Gerhard surname record required")
    row=rows[0];binding=d["name_bindings"][0]
    if not isinstance(row.get("review"),dict) or not all(row["review"].get(g) is True for g in d["review_gates"]):
        raise ValueError("All five individual Gerhard name gates required")
    if any(row.get(k)!=v for k,v in binding["approved_fields"].items()):
        raise ValueError("Exact approved surname source/context/owned12-byte span required")
    return d

def validate_name_transition(source,target):
    d=contract();span=d["owned_name_span"];at=span["offset"];old=bytes.fromhex(span["current_hex"]);new=bytes.fromhex(span["target_hex"])
    if not isinstance(source,bytes) or not isinstance(target,bytes) or len(source)!=len(target):
        raise ValueError("Complete equal-size ARM9 byte strings required")
    if span["bytes"]!=12 or len(old)!=12 or len(new)!=12 or source[at:at+12]!=old or target[at:at+12]!=new:
        raise ValueError("Exact terminated owned12-byte surname replacement required")
    if source[:at]!=target[:at] or source[at+12:]!=target[at+12:]:
        raise ValueError("Unowned ARM9 bytes or protected Blades changed")
    neighbor=d["protected_neighbor"];begin=neighbor["offset"];raw=bytes.fromhex(neighbor["current_hex"])
    if neighbor["bytes"]!=8 or source[begin:begin+8]!=raw or target[begin:begin+8]!=raw or raw!=b"Blades\\0\\0":
        raise ValueError("Exact independently referenced Blades neighbor required")
    for ref in d["name_andneighbor_pointer_references"]:
        field=ref["pointer_field_offset"];value=bytes.fromhex(ref["field_bytes"])
        if source[field:field+4]!=value or target[field:field+4]!=value:
            raise ValueError("Protected name/item pointer field changed")
    for relative in range(1,12):
        pointer=(d["owned_name_address"]+relative).to_bytes(4,"little")
        if pointer in source or pointer in target:raise ValueError("Interior surname literal pointer alias")
    if sha(source)!=d["runtime_component_hashes"]["/__arm9__.bin"] or sha(target)!=d["target_runtime_component_hashes"]["/__arm9__.bin"]:
        raise ValueError("Exact source andtarget surname ARM9 hashes required")
    return dict(bytes=12,protected_Blades_exact=True,all_other_ARM9_bytes_andpointer_fields_exact=True,
        whole_ARM9_inverse_exact=True,literal_pointer_census_not_arbitrary_dynamic_alias_proof=True)
'''

def as_source(text):
    compile(text,'<frozen-Gerhard-policy>','exec')
    return text

if __name__=='__main__':
    assert not ROOT.exists() and all(not p.exists() for p in [CONTRACT,PROFILE,FORMATTER,PLANNER])
    doc,plan,current,approval,reference,ownership=map(read,[DOC,PLAN,CURRENT,APPROVAL,REFERENCE,OWNERSHIP])
    assert approval['manuscript_sha256']==sha(DOC.read_bytes()) and approval['individual_five_gate_body_records']==5
    assert approval['individual_five_gate_owned_name_records']==1 and approval['complete_actual_body_holds']==30 and approval['relevant_actual_name_holds']==262
    assert len(approval['directly_viewed_sheets'])==11 and all(s['directly_viewed'] for s in approval['directly_viewed_sheets'])
    assert not plan['failures'] and len(doc['records'])==len(plan['records'])==5 and len(doc['name_records'])==1
    parent=NdsImage.open(reference['parent']);target=NdsImage.open(reference['research_ROM']);clean=NdsImage.open('work/clean.nds')
    assert sha(Path(reference['parent']).read_bytes())==reference['parent_sha256']==doc['current_ROM_sha256']
    assert sha(Path(reference['research_ROM']).read_bytes())==reference['research_ROM_sha256']
    parent_bank=IlnkContainer.parse(parent.read_file(doc['file_path'])).blocks
    clean_bank=IlnkContainer.parse(clean.read_file(doc['file_path'])).blocks
    target_bank=IlnkContainer.parse(target.read_file(doc['file_path'])).blocks
    deps={DOC,PLAN,CURRENT,APPROVAL,REFERENCE,OWNERSHIP,Path(__file__),Path('scripts/source_locked_derivation_v5118.py')}
    for path,digest in doc['evidence'].items():assert sha(Path(path).read_bytes())==digest;deps.add(Path(path))
    for sheet in approval['directly_viewed_sheets']:
        p=Path(sheet['path']);assert sha(p.read_bytes())==sheet['sha256'];deps.add(p)
    # Import the reviewed planner only after its hash-bearing input proof is bound.
    from scripts import plan_Gerhard_layout_v8205 as owned_plan
    for name,module in list(sys.modules.items()):
        path=getattr(module,'__file__',None)
        if path and (name.startswith('scripts.plan_') or name.startswith('dk4tool.dialogue.')) and Path(path).suffix=='.py':deps.add(Path(path))
    bindings={};reasons={
        'DK4_MES_B27_R0091':'Two readable rows retain the courteous acknowledgment andcomplete Gerhard Adernkatz identity.',
        'DK4_MES_B27_R0094':'The complete address andpirate-hunter recognition remain coherent across two rows.',
        'DK4_MES_B74_R0060':'Separate complete exclamations keep It\'s been together without anauthored break.',
        'DK4_MES_B74_R0185':'Measured FI expands toLil;the fullGerhard Adernkatz name stays intact onrow2.',
        'DK4_MES_B74_R0260':'Celebration/address andcomplete thanks/request fit two natural rows;allwords retained.',
    }
    for row,p in zip(doc['records'],plan['records'],strict=True):
        ident=row['id'];assert ident==p['id'] and all(row['review'][g] is True for g in doc['review_gates'])
        assert row['compiled_hex']==p['encoded_hex'] and row['english']==p['logical_English'] and row['source_hex']==p['source_hex']
        assert p['expected_native_pages']==1 and p['max_total_rows']==4 and not row['qa_waivers']
        assert not any(i['severity'] in ['warning','error'] for i in p['base_QA']['issues'])
        number=row['block'];source=bytes.fromhex(row['source_hex']);old=bytes.fromhex(row['current_hex'])
        a,b=row['source_reference']['offset'],row['current_reference']['offset']
        assert clean_bank[number][a:a+len(source)]==source and parent_bank[number][b:b+len(old)]==old
        assert clean_bank[number][a-5:a+1].hex()==parent_bank[number][b-5:b+1].hex()==row['source_complete_preamble_hex']
        bindings[ident]=dict(approved_fields=deepcopy(row),compiler_source_hex=row['source_hex'],source_selector=row['source_selector'],file_path=row['file_path'],block=number,
            source_block_hashes=sorted({sha(clean_bank[number]),sha(parent_bank[number]),sha(target_bank[number])}),planning_record=deepcopy(p['planning_record']),
            compiled_hex=p['encoded_hex'],lines=p['lines'],formatted_markup=p['formatted_markup'],base_QA_issues=p['base_QA']['issues'],
            native_page_count=1,maximum_total_rows=4,row_count_reason=reasons[ident],ordinary_wrap_reasons=reasons[ident],
            qa_waivers=[],qa_waiver_reason=None,qa_waiver_scope=None,consumer='progressive')
    paths=['/__arm9__.bin','/COMMON/MESFILE.DK4','/GRP/KANJI.FNT','/data/EV2.DK4','/data/SC2.DK4']
    contract=dict(format='dk4-Gerhard-surname-native-contract-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        review_gates=doc['review_gates'],record_bindings=bindings,choice_bindings={},physical_native_rows_per_page=4,complete_native_pages=5,
        measured_macro_ascii_lengths=dict(FI=3,FA=5,FO=9),source_macro_counts=dict(FI=1,FA=0,FO=0),
        batch_binding={k:deepcopy(doc[k]) for k in ['format','translation_policy','target_locale','encoder','review_gates','file_path','route','route_identity','blocks','current_ROM','current_ROM_sha256','revised','retained']},
        name_bindings=[dict(approved_fields=deepcopy(doc['name_records'][0]))],owned_name_span=ownership['current_owned_name_span'],
        protected_neighbor=ownership['protected_neighbor'],owned_name_address=ownership['current_literal_pointer_references'][0]['target_pointer'],
        name_andneighbor_pointer_references=ownership['current_literal_pointer_references']+ownership['protected_neighbor_literal_pointer_references'],
        runtime_component_hashes={p:sha(parent.read_file(p)) for p in paths},target_runtime_component_hashes={p:sha(target.read_file(p)) for p in paths},
        parent_ROM=reference['parent'],parent_ROM_sha256=reference['parent_sha256'],target_ROM=reference['research_ROM'],target_ROM_sha256=reference['research_ROM_sha256'],
        dependencies={str(p):sha(p.read_bytes()) for p in sorted(deps,key=str)},all14_other_consistent_occurrences_and20final_consumers_protected=True,
        full_source_context295_andscoped_actual30_body262_name_holds_bound=True,full_Hodram28_andall207_names_not_approved_here=True,
        all_recorded_actual_fixture_timing_RNG_components_bytes_calendar_RGB_andlater_reaudit_limits_preserved=True,
        no_new_source_prose_completed_revision_orretention_credit=True,full_goal_complete=False)
    profile=Path('dk4tool/dialogue/rafael_B50_profile_v1.py').read_text('utf8')
    metric=next(n.value for n in ast.walk(ast.parse(profile)) if isinstance(n,ast.keyword) and n.arg=='metrics_source').value
    newmetric='Exact sparse Gerhard surname correction:five SC2B27/B74 progressive speeches,oneowned12-byte ARM9 name,Blades8 protected. Lil3/Argot5/ArgotCo9,FI1/noFAFO,216px/6pxASCII/12pxCP932/fourrows,complete native/stored/actual glyphs andnames. WholeB27 actual35of51 andcaptain0laterSC0B44 fixturelimit;wholeB74 actual75of79/defaultchoice0;introdisplay8 bypassesoutercondition explicitly. Thirty bodyholds/262nameholds/117sceneRGBpairs;alltiming,RNG,component,byte,calendar,RGB andfixturelimits retained. Fullsourcecontrols/207names/fullgoal remainseparate;no globalfont/profile/guard change.'
    profile=checked_text(profile,{
        'translations/rafael_B50_native_contract_v1.json':str(CONTRACT).replace('\\','/'),
        '1a8751c931336a73ddea449bd671eaafb1291e2d4b75d4be9a46d0b912e44872':'CONTRACT_SHA_PLACEHOLDER',
        'Rafael-B50':'Gerhard-surname','Rafael B50':'Gerhard surname',
        'len(d["record_bindings"])!=28':'len(d["record_bindings"])!=5','d["complete_native_pages"]!=28':'d["complete_native_pages"]!=5',
        'twenty-eight-paragraph/twenty-eight-page/no-menu':'five-sparse-paragraph/five-page/no-new-menu',
        '{"FI":6,"FA":6,"FO":10}':'{"FI":3,"FA":5,"FO":9}',
        '{"FI":1,"FA":2,"FO":0}':'{"FI":1,"FA":0,"FO":0}',
        'get_dialogue_profile("raphael-story-live")':'get_dialogue_profile("lil-story-deep-route-live")',
        'base.macro_ascii_lengths["FI"]!=7':'base.macro_ascii_lengths["FI"]!=3',
        '{"FI":36,"FA":36,"FO":60,"I":12}':'{"FI":18,"FA":30,"FO":54,"I":12}',
        '{0,2,9}':'{1,9,16}',metric:newmetric,
        'sha(arm)!=ARM9_SHA':'sha(arm) not in [ARM9_SHA,TARGET_ARM9_SHA]',
        'ARM9_SHA="2b6aaaa499d634be9afc255d1c39b64ef0f578283c9768c525b31e34499abd0a"':
        'ARM9_SHA="2b6aaaa499d634be9afc255d1c39b64ef0f578283c9768c525b31e34499abd0a"\nTARGET_ARM9_SHA="'+reference['research_ARM9_sha256']+'"',
        '''def validate_runtime(image):
    d=contract()
    for path,digest in d["runtime_component_hashes"].items():''':
        '''def validate_runtime(image,phase="parent"):
    d=contract()
    if phase not in ["parent","target"]:raise ValueError("Exact parent ortarget runtime phase required")
    for path,digest in d["runtime_component_hashes" if phase=="parent" else "target_runtime_component_hashes"].items():''',
        '''    if doc.get("typed_choice_records"):
        raise ValueError("No B50 typed menu records authorized")
    return d''':
        '''    if doc.get("typed_choice_records"):
        raise ValueError("No new surname-revisit typed menu records authorized")
    validate_name_records(doc)
    return d''',
    })+NAME_CODE
    formatter=checked_text(Path('dk4tool/dialogue/rafael_B50_layout_v1.py').read_text('utf8'),{
        'Rafael-B50':'Gerhard-surname','B50':'surname',
        'rafael_B50_profile_v1':'gerhard_surname_profile_v1','rafael_B50_plan_v1':'gerhard_surname_plan_v1',
    })
    planner=checked_text(Path('dk4tool/dialogue/rafael_B50_plan_v1.py').read_text('utf8'),{
        'plan_Rafael_B50_layout_v8140b':'plan_Gerhard_layout_v8205',
        'Rafael_B50_layout_v8140b/28_automatic_plans_full_native_width_exact_source00_02_09_FA2_FI1.json':'Gerhard_layout_v8205/5_automatic_Lil_plans_full_native_width.json',
        '726e32b6b4196c1a9c8bf2fc8774f8c38861a5a04002ef11feea6d8ba6b2650d':sha(PLAN.read_bytes()),
        'Exact source-owned automatic B50 planner;00 preamble separate from guarded NUL-free text.':'Exact source-owned sparse Lil planner;native01/09/10 prefixes andguarded NUL-free text.',
    })
    ROOT.mkdir(parents=True);save(CONTRACT,contract);profile=profile.replace('CONTRACT_SHA_PLACEHOLDER',sha(CONTRACT.read_bytes()))
    for path,text in [(PROFILE,profile),(FORMATTER,formatter),(PLANNER,planner)]:path.write_text(as_source(text),encoding='utf8')
    save(ROOT/'frozen_policy_receipt.json',dict(contract=str(CONTRACT),contract_sha256=sha(CONTRACT.read_bytes()),profile=str(PROFILE),profile_sha256=sha(PROFILE.read_bytes()),
        formatter=str(FORMATTER),formatter_sha256=sha(FORMATTER.read_bytes()),planner=str(PLANNER),planner_sha256=sha(PLANNER.read_bytes()),
        body_records=5,owned_name_records=1,all_original_global_profiles_compilers_andnative_addresses_preserved=True,
        no_new_menu_text_no_FE_or00_scope_extension=True,all_source_prose_format_bounds_andprotected_Blades_bound=True,
        actual_changing_policy_tests_independent_reference_seal_atomic_stage_andregistered_release_pending=True,
        new_credit=0,new_emulator_runs=0,full_goal_complete=False))
    print('Frozen5-body/one12-byte surname contract andprivate Lil profile/layout/planner;globalcompilers unchanged.Policytests pending.')
