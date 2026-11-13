"""Freeze sixteen approved B49 units,scoped native consumers andexact automatic compiler/QA evidence."""
import sys
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts import plan_Hodram_B49_layout_v8394 as private
from scripts.approve_Hodram_B49_format_v8423 import PROOFS as prior_paths
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B49_policy_v8424')
DOC=Path('translations/hodram_B49_editorial_manuscript_v3.json')
NAMES=Path('translations/hodram_B49_speaker_name_review_v2.json')
PLAN=private.ROOT/'automatic_plans.json'
APPROVAL=Path('work/analysis/Hodram_B49_format_v8423/formatting_approval.json')
CONTRACT=Path('translations/hodram_B49_native_contract_v1.json')
PROFILE=Path('dk4tool/dialogue/hodram_B49_profile_v1.py')
FORMATTER=Path('dk4tool/dialogue/hodram_B49_layout_v1.py')
PLANNER=Path('dk4tool/dialogue/hodram_B49_plan_v1.py')
CHOICES=Path('dk4tool/dialogue/hodram_B49_choices_v1.py')
NAME_POLICY=Path('dk4tool/dialogue/hodram_B49_names_v1.py')

NAME_SOURCE='''"""Exact scoped Hodram/Lil identities;all207 actors/custom-name consumers remain outside this binding."""
from dk4tool.dialogue.hodram_B49_profile_v1 import contract

def validate_scoped_names(review):
    expected=contract()['name_review_binding']
    if review!=expected:raise ValueError('B49 names:exact source-qualified review andnative/actual scope required')
    if [(r['actor_ID'],r['current_name']) for r in review['records']]!=[(1,'Hodram'),(2,'Lil Argot')]:
        raise ValueError('B49 names:exact two approved identities required')
    for row in review['records']:
        if not all(row['review'].get(g) is True for g in ['source','context','localization','naturalness','formatting']):
            raise ValueError('B49 names:allfive individual scoped gates required')
    if review['system_FE_record_IDs']!=['DK4_MES_B49_R0081'] or not review['FE_has_no_personal_actor254_name_orvoice']:
        raise ValueError('B49 names:original FE hasno personal actor254 name orvoice')
    return expected
'''

if __name__=='__main__':
    outputs=[CONTRACT,PROFILE,FORMATTER,PLANNER,CHOICES,NAME_POLICY]
    assert not ROOT.exists() and all(not p.exists() for p in outputs)
    doc,names,plan,approval=map(read,[DOC,NAMES,PLAN,APPROVAL]);reloc=read(prior_paths['relocation'])
    assert approval['manuscript_sha256']==sha(DOC.read_bytes()) and approval['names_sha256']==sha(NAMES.read_bytes()) and approval['all16_five_gates_true']
    assert len(doc['records'])==14 and len(doc['typed_choice_records'])==2 and doc['revised']==7 and doc['retained']==9
    assert all(all(r['review'].values()) for r in doc['records']+doc['typed_choice_records']+names['records'])
    assert approval['total_actual_frames']==69868 and approval['actual_tail_complete_holds']==134 and approval['FE_original_paint_two_snapshots_four_VRAM_palette_RGB_holds']
    assert not plan['failures'] and len(plan['records'])==14 and doc['source_current_final_references_complete']
    group=reloc['groups'][0];assert group['block']==49
    image=NdsImage.open(doc['current_ROM']);assert sha(Path(doc['current_ROM']).read_bytes())==doc['current_ROM_sha256']
    bindings={};infos=0
    for row,p in zip(doc['records'],plan['records'],strict=True):
        assert row['id']==p['id'] and row['english']==row['logical_English']==p['logical_English']==' '.join(p['lines'])
        assert row['compiled_hex']==p['encoded_hex'] and row['planned_English_markup']==p['planning_record']['english']
        assert p['expected_native_pages']==1 and p['max_total_rows']==4 and row['qa_waivers']==row['qa_waiver_scope']==[]
        assert all(i['severity']=='info' and i['code']=='line-break-count' for i in p['base_QA']['issues']);infos+=len(p['base_QA']['issues'])
        bindings[row['id']]=dict(file_path='/data/SC1.DK4',route=1,route_identity='Hodram',block=49,source_block_hashes=[group['clean_block_sha256'],group['source_block_sha256']],source_reference=row['source_reference'],current_reference=row['current_reference'],final_reference=row['final_reference'],source_complete_preamble_hex=row['source_complete_preamble_hex'],compiler_source_hex=row['source_hex'],predecessor_record_hex=row['current_hex'],source_selector=row['source_selector'],source_kind=row['kind'],consumer='FE-paper' if row['source_selector']==254 else 'progressive',planning_record={k:p['planning_record'][k] for k in ['id','english','kind','source_hex','source_selector']},compiled_hex=p['encoded_hex'],lines=p['lines'],maximum_total_rows=4,native_page_count=1,row_count_reason='Full216px usable width;allreviewed words preserved onone complete native page.',ordinary_wrap_reasons=[row['localization_note'],row['native_body_review_reason']],base_QA_issues=p['base_QA']['issues'],qa_waivers=[],qa_waiver_reason=None,qa_waiver_scope=[],approved_fields=deepcopy(row))
    assert infos==7 and {b['source_selector'] for b in bindings.values()}=={1,2,254}
    assert sum(b['source_selector']==254 for b in bindings.values())==1 and doc['source_macro_counts']==dict(FI=0,FA=0,FO=0)
    choice_bindings={r['id']:dict(file_path=r['file_path'],block=49,source_reference=r['source_reference'],current_reference=r['current_reference'],final_reference=r['final_reference'],approved_fields=deepcopy(r)) for r in doc['typed_choice_records']}
    assert list(choice_bindings)==['DK4_MES_B49_R0048','DK4_MES_B49_R0050']
    template=Path('dk4tool/dialogue/hodram_outcomes_profile_v1.py').read_text('utf8')
    oldmetrics=template.split('metrics_source="',1)[1].split('")',1)[0]
    oldvalidate=template[template.index('def validate_approved_batch(doc):'):]
    choice_profile=Path('dk4tool/dialogue/rafael_B46_profile_v1.py').read_text('utf8')
    validate=checked_text(choice_profile[choice_profile.index('def validate_approved_batch(doc):'):],{'B46':'Hodram-B49'})
    profile=checked_text(template,{
        'translations/hodram_outcomes_native_contract_v1.json':CONTRACT.as_posix(),
        '83b3770866e46df47dd0e5b6e6170da1454d3ccde77199abc9676941360774e3':'CONTRACT_DIGEST',
        'Hodram-outcomes':'Hodram-B49','Hodram B47/B48':'Hodram B49',
        'len(d["record_bindings"])!=6 or d["choice_bindings"]':'len(d["record_bindings"])!=14 or len(d["choice_bindings"])!=2',
        'd["complete_native_pages"]!=6':'d["complete_native_pages"]!=14',
        'Complete six-paragraph/six-page/no-menu contract required':'Complete14-speech/14-page/two-choice contract required',
        '{"FI":1,"FA":0,"FO":0}':'{"FI":0,"FA":0,"FO":0}',
        'else {2}':'else {r["source_selector"]}',
        oldmetrics:'Exact complete registeredV8377/captain1 runtime andsource1/2/FE preambles. Full216usablewidth,13progressive pages plusoriginalFE228x48/288stride/6x12/16pitch;FI6FA9FO15,zero source macros. Fourteen complete native/stored pages,seven line-count infos,zero warnings/waivers. Two exact source-bound ellipses andone source-qualified New/World ordinaryboundary;no global exceptions. Actual69868frames includes20002whole-script initialized fixtures,40004bounded-tail choices and9862focusedFE frames. All14unique speech displays/bothmenus passcompleteglyphs,owned surfaces,headers/absentFEheader andnormalreturns. Measured timing,boundary/final PRNG andlaterRGB differences remain;five sampled components/actors match. Not natural activation,earned inventory/trade eligibility,original location,customnames,fullroute,hardware,everyframe causality orfuture-outcome equivalence.',
        oldvalidate:validate,
    })
    layout=checked_text(Path('dk4tool/dialogue/hodram_outcomes_layout_v1.py').read_text('utf8'),{'hodram_outcomes':'hodram_B49','Hodram-outcomes':'Hodram-B49'})
    planner=checked_text(Path('dk4tool/dialogue/hodram_outcomes_plan_v1.py').read_text('utf8'),{
        'plan_Hodram_B47_B48_v8323':'plan_Hodram_B49_layout_v8394',
        'work/analysis/Hodram_B47_B48_layout_v8323/six_automatic_plans_original_usable_width_distinct_FE_all_QA_preserved.json':PLAN.as_posix(),
        '97420058ab399bbeeb7ba052a27c346365519b19b3f55a525ea55fdd77cbf7e6':sha(PLAN.read_bytes()),
    })
    choices=checked_text(Path('dk4tool/dialogue/rafael_B46_choices_v1.py').read_text('utf8'),{'rafael_B46':'hodram_B49','B46':'Hodram-B49'})
    for path,text in [(PROFILE,profile.replace('CONTRACT_DIGEST','0'*64)),(FORMATTER,layout),(PLANNER,planner),(CHOICES,choices),(NAME_POLICY,NAME_SOURCE)]:compile(text,str(path),'exec')
    deps={DOC,NAMES,PLAN,APPROVAL,Path(__file__),Path(private.__file__)}|{Path(p) for p in prior_paths.values()}
    for name,module in list(sys.modules.items()):
        if not(name.startswith('scripts.') or name.startswith('dk4tool.')):continue
        path=getattr(module,'__file__',None)
        if path and Path(path).suffix=='.py':deps.add(Path(path))
        for value in vars(module).values():
            if isinstance(value,Path) and value.suffix not in ['.nds','.xdelta'] and value.is_file() and not any(s in value.as_posix() for s in ['editorial_review_current_v1.json','release_stack.json','rom_retention_pins.json','docs/']):deps.add(value)
    # The registered predecessor's immutable release proof owns its full stack.
    # Never pin the mutable integrated builder as a text dependency: the later
    # production stage separately guards the exact additive builder inverse.
    deps={p for p in deps if p.resolve()!=Path('scripts/build_integrated_release.py').resolve()}
    models=read('work/analysis/Hodram_B49_models_v8408/native_models.json');deps.add(Path('work/analysis/Hodram_B49_models_v8408/native_models.json'))
    for rows in models['native_models'].values():
        for row in rows:
            for page in row['pages']:
                for key in ['native_plane','physical_plane']:
                    if key in page:
                        path=Path(page[key]);assert sha(path.read_bytes())==page[key+'_sha256'];deps.add(path)
    for row in models['name_planes']:
        path=Path(row['native_plane']);assert sha(path.read_bytes())==row['native_plane_sha256'];deps.add(path)
    for s in approval['directly_viewed_sheets']:
        path=Path(s['path']);assert sha(path.read_bytes())==s['sha256'];deps.add(path)
    for path,text in [(FORMATTER,layout),(PLANNER,planner),(CHOICES,choices),(NAME_POLICY,NAME_SOURCE)]:path.write_text(text,encoding='utf8');deps.add(path)
    normalized={p.resolve() for p in deps};assert all(p.is_file() for p in normalized)
    runtime={p:sha(image.read_file(p)) for p in ['/__arm9__.bin','/COMMON/MESFILE.DK4','/GRP/KANJI.FNT','/data/EV1.DK4']}
    save(CONTRACT,dict(format='Hodram-B49-source-native-contract-v1',record_bindings=bindings,choice_bindings=choice_bindings,choice_object_hex=group['choice_commands'][0]['target_hex'],review_gates=doc['review_gates'],batch_binding={k:doc[k] for k in ['translation_policy','target_locale','encoder','review_gates','file_path','route','route_identity','blocks']},runtime_component_hashes=runtime,measured_macro_ascii_lengths=dict(FI=6,FA=9,FO=15),source_macro_counts=dict(FI=0,FA=0,FO=0),physical_native_rows_per_page=4,physical_progressive_viewport=[216,64],physical_FE_bitmap=[228,48],physical_FE_stride=288,usable_text_width_px=216,complete_native_pages=14,name_review_binding=names,source_bound_ellipsis_bindings=plan['source_bound_ellipsis_bindings'],ordinary_boundary_bindings=plan['ordinary_boundary_bindings'],explicit_complete_registered_predecessor=dict(profile='all-routes-unified-v8377',candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],ARM9_sha256=runtime['/__arm9__.bin'],Gerhard_correction='translations/gerhard_surname_editorial_release_v2.json',Gerhard_correction_sha256=sha(Path('translations/gerhard_surname_editorial_release_v2.json').read_bytes())),dependencies={str(p):sha(p.read_bytes()) for p in sorted(normalized)},individual_row_count_infos=7,exact_warning_exception_count=0,all16_source_current_final_context_prose_names_native_stored_actual_menu_FE_VRAM_andmeasured_scope_bound=True,policy_validation_independent_production_atomic_registered_integration_pending=True,new_credit=0,full_goal_complete=False))
    PROFILE.write_text(profile.replace('CONTRACT_DIGEST',sha(CONTRACT.read_bytes())),encoding='utf8');ROOT.mkdir(parents=True)
    save(ROOT/'frozen_contract.json',dict(contract=str(CONTRACT),contract_sha256=sha(CONTRACT.read_bytes()),modules={str(p):sha(p.read_bytes()) for p in [PROFILE,FORMATTER,PLANNER,CHOICES,NAME_POLICY]},records=14,typed_choices=2,single_pages=14,scoped_names=2,source_FE=1,source_macro_counts=dict(FI=0,FA=0,FO=0),infos=7,warnings=0,waivers=0,dependency_count=len(normalized),integrated_builder_not_accidentally_pinned=True,all_prior_artifacts_preserved_no_global_profile_font_QA_guard_orprose_change=True,new_credit=0,full_goal_complete=False))
    print('Frozen B49:14speech pages+2typedchoices/two scoped names/zero macros/7infos/0warnings/waivers;dependencies',len(normalized),'.Policy validation/atomic/registered release pending;zero credit.')
