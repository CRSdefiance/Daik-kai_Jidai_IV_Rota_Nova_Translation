"""Freeze the three approved B50 source/current/final units and exact native/actual policy."""
import sys
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts import plan_Hodram_B50_v8491b as private
from scripts.approve_Hodram_B50_format_v8511 import PROOFS as prior_paths
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B50_policy_v8514')
DOC=Path('translations/hodram_B50_editorial_manuscript_v4.json')
NAMES=Path('translations/hodram_B50_speaker_name_review_v2.json')
PLAN=private.ROOT/'automatic_plans.json'
APPROVAL=Path('work/analysis/Hodram_B50_format_v8511/formatting_approval.json')
CONTRACT=Path('translations/hodram_B50_native_contract_v1.json')
PROFILE=Path('dk4tool/dialogue/hodram_B50_profile_v1.py')
FORMATTER=Path('dk4tool/dialogue/hodram_B50_layout_v1.py')
PLANNER=Path('dk4tool/dialogue/hodram_B50_plan_v1.py')
NAME_POLICY=Path('dk4tool/dialogue/hodram_B50_names_v1.py')

if __name__=='__main__':
    outputs=[CONTRACT,PROFILE,FORMATTER,PLANNER,NAME_POLICY]
    assert not ROOT.exists() and all(not p.exists() for p in outputs)
    doc,names,plan,approval=map(read,[DOC,NAMES,PLAN,APPROVAL]);reloc=read(prior_paths['relocation'])
    assert approval['manuscript_sha256']==sha(DOC.read_bytes()) and approval['names_sha256']==sha(NAMES.read_bytes()) and approval['all3_five_gates_true']
    assert len(doc['records'])==3 and doc['typed_choice_objects']==0 and doc['revised']==2 and doc['retained']==1
    assert all(all(r['review'].values()) for r in doc['records']+names['records'])
    assert approval['actual_frames']==20002 and approval['complete_holds']==50 and approval['FE_original_paint_two_snapshots_six_VRAM_palette_RGB_holds']
    assert not plan['failures'] and len(plan['records'])==3 and doc['source_current_final_references_complete']
    group=reloc['groups'][0];assert group['block']==50 and len(group['all_target_commands'])==12 and not group['relative_fixups']
    image=NdsImage.open(doc['current_ROM']);assert sha(Path(doc['current_ROM']).read_bytes())==doc['current_ROM_sha256']
    bindings={};infos=0
    for row,p in zip(doc['records'],plan['records'],strict=True):
        assert row['id']==p['id'] and row['english']==row['logical_English']==p['logical_English']==' '.join(p['lines'])
        assert row['compiled_hex']==p['encoded_hex'] and row['planned_English_markup']==p['planning_record']['english']
        assert p['expected_native_pages']==1 and p['max_total_rows']==4 and row['qa_waivers']==row['qa_waiver_scope']==[]
        assert all(i['severity']=='info' and i['code']=='line-break-count' for i in p['base_QA']['issues']);infos+=len(p['base_QA']['issues'])
        bindings[row['id']]=dict(file_path='/data/SC1.DK4',route=1,route_identity='Hodram',block=50,source_block_hashes=[group['clean_block_sha256'],group['source_block_sha256']],source_reference=row['source_reference'],current_reference=row['current_reference'],final_reference=row['final_reference'],source_complete_preamble_hex=row['source_complete_preamble_hex'],compiler_source_hex=row['source_hex'],predecessor_record_hex=row['current_hex'],source_selector=row['source_selector'],source_kind=row['kind'],consumer='FE-paper' if row['source_selector']==254 else 'progressive',planning_record={k:p['planning_record'][k] for k in ['id','english','kind','source_hex','source_selector']},compiled_hex=p['encoded_hex'],lines=p['lines'],maximum_total_rows=4,native_page_count=1,row_count_reason='Use the original full216px usable width andpreserve every reviewed word onone complete native page.',ordinary_wrap_reasons=[row['localization_note'],row['native_body_review_reason']],base_QA_issues=p['base_QA']['issues'],qa_waivers=[],qa_waiver_reason=None,qa_waiver_scope=[],approved_fields=deepcopy(row))
    assert infos==3 and {b['source_selector'] for b in bindings.values()}=={2,254}
    assert sum(b['source_selector']==254 for b in bindings.values())==1 and doc['source_macro_counts']==dict(FI=0,FA=0,FO=0)
    template_path=Path('dk4tool/dialogue/hodram_outcomes_profile_v1.py');template=template_path.read_text(encoding='utf-8')
    oldmetrics=template.split('metrics_source="',1)[1].split('")',1)[0]
    profile=checked_text(template,{
        'translations/hodram_outcomes_native_contract_v1.json':CONTRACT.as_posix(),
        '83b3770866e46df47dd0e5b6e6170da1454d3ccde77199abc9676941360774e3':'CONTRACT_DIGEST',
        'Hodram-outcomes':'Hodram-B50','Hodram B47/B48':'Hodram B50',
        'len(d["record_bindings"])!=6':'len(d["record_bindings"])!=3','d["complete_native_pages"]!=6':'d["complete_native_pages"]!=3',
        'six-paragraph/six-page':'three-paragraph/three-page',
        '{"FI":1,"FA":0,"FO":0}':'{"FI":0,"FA":0,"FO":0}',
        oldmetrics:'Exact complete registeredV8475/captain1 runtime andsource02/FE sixbyte preambles. Full216usablewidth,two progressive pages plusoriginal FE228x48/288stride/6x12/16pitch;FI6FA9FO15 andzero source macros. Three native/stored pages,three line-count infos,zero warnings orwaivers. Actual20002frames in two complete initialized opening fixtures;allthree source andEnglish pages/50completeholds passfullglyphs,headers/absentFEheader,portrait,item148layout0 show-hide andnormalends4739/4737[0,0]. FE-before6302 remains original;two paint snapshots/six same-run bitmap,palette,VRAM andRGBholds pass. Two one-frame speech-duration differences,no measured boundaryPRNG orUIrequest differences,butfinal seeds3867090476/3028864251 differ and4of89laterRGB pairs differ. Five checked components/wholeactors/captain1 match;rawcalendar stays uninterpreted. Not naturalactivation,original location,earnedinventory,customnames,fullroute,hardware,everyframe causality,futurePRNG-outcome orbroadsimulation equivalence.',
    })
    layout_path=Path('dk4tool/dialogue/hodram_outcomes_layout_v1.py');layout=checked_text(layout_path.read_text(encoding='utf-8'),{'hodram_outcomes':'hodram_B50','Hodram-outcomes':'Hodram-B50'})
    planner_path=Path('dk4tool/dialogue/hodram_outcomes_plan_v1.py');planner=checked_text(planner_path.read_text(encoding='utf-8'),{
        'plan_Hodram_B47_B48_v8323':'plan_Hodram_B50_v8491b',
        'work/analysis/Hodram_B47_B48_layout_v8323/six_automatic_plans_original_usable_width_distinct_FE_all_QA_preserved.json':PLAN.as_posix(),
        '97420058ab399bbeeb7ba052a27c346365519b19b3f55a525ea55fdd77cbf7e6':sha(PLAN.read_bytes()),
    })
    names_path=Path('dk4tool/dialogue/hodram_B49_names_v2.py');name_policy=checked_text(names_path.read_text(encoding='utf-8'),{
        'hodram_B49_profile_v2':'hodram_B50_profile_v1','B49 names:':'B50 names:',
        "[(r['actor_ID'],r['current_name']) for r in review['records']]!=[(1,'Hodram'),(2,'Lil Argot')]":"[(r['actor_ID'],r['current']) for r in review['records']]!=[(2,'Lil Argot')]",
        'exact two approved identities required':'exact scoped approved Lil identity required',
        "review['system_FE_record_IDs']!=['DK4_MES_B49_R0081'] or not review['FE_has_no_personal_actor254_name_orvoice']":"not review['no_FE_personal_actor_name']",
        'Exact scoped Hodram/Lil identities':'Exact scoped Lil identity',
    })
    for p,code in [(PROFILE,profile.replace('CONTRACT_DIGEST','0'*64)),(FORMATTER,layout),(PLANNER,planner),(NAME_POLICY,name_policy)]:compile(code,str(p),'exec')
    deps={DOC,NAMES,PLAN,APPROVAL,Path(__file__),Path(private.__file__),template_path,layout_path,planner_path,names_path}|{Path(p) for p in prior_paths.values()}
    for name,module in list(sys.modules.items()):
        if not(name.startswith('scripts.') or name.startswith('dk4tool.')):continue
        path=getattr(module,'__file__',None)
        if path and Path(path).suffix=='.py':deps.add(Path(path))
        for value in vars(module).values():
            if isinstance(value,Path) and value.suffix not in ['.nds','.xdelta'] and value.is_file() and not any(s in value.as_posix() for s in ['editorial_review_current_v1.json','release_stack.json','rom_retention_pins.json','docs/']):deps.add(value)
    deps={p for p in deps if p.resolve()!=Path('scripts/build_integrated_release.py').resolve()}
    modelpath=Path('work/analysis/Hodram_B50_models_v8506/native_models.json');models=read(modelpath);deps.add(modelpath)
    for rows in models['native_models'].values():
        for row in rows:
            for page in row['pages']:
                for key in ['native_plane','physical_plane']:
                    if key in page:
                        path=Path(page[key]);assert sha(path.read_bytes())==page[key+'_sha256'];deps.add(path)
    for row in models['name_planes']:
        path=Path(row['native_plane']);assert sha(path.read_bytes())==row['native_plane_sha256'];deps.add(path)
    for s in approval['measured_limits']['directly_viewed_sheets']:
        path=Path(s['path']);assert sha(path.read_bytes())==s['sha256'];deps.add(path)
    for path,text in [(FORMATTER,layout),(PLANNER,planner),(NAME_POLICY,name_policy)]:path.write_text(text,encoding='utf-8');deps.add(path)
    normalized={p.resolve() for p in deps};assert all(p.is_file() for p in normalized)
    assert not any(p==Path('scripts/build_integrated_release.py').resolve() for p in normalized)
    runtime={p:sha(image.read_file(p)) for p in ['/__arm9__.bin','/COMMON/MESFILE.DK4','/GRP/KANJI.FNT','/data/EV1.DK4']}
    save(CONTRACT,dict(format='Hodram-B50-source-native-contract-v1',record_bindings=bindings,choice_bindings={},review_gates=doc['review_gates'],batch_binding={k:doc[k] for k in ['translation_policy','target_locale','encoder','review_gates','file_path','route','route_identity','blocks']},runtime_component_hashes=runtime,measured_macro_ascii_lengths=dict(FI=6,FA=9,FO=15),source_macro_counts=dict(FI=0,FA=0,FO=0),physical_native_rows_per_page=4,physical_progressive_viewport=[216,64],physical_FE_bitmap=[228,48],physical_FE_stride=288,usable_text_width_px=216,complete_native_pages=3,name_review_binding=names,explicit_complete_registered_predecessor=dict(profile='all-routes-unified-v8475',candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],ARM9_sha256=runtime['/__arm9__.bin'],Gerhard_correction='translations/gerhard_surname_editorial_release_v2.json',Gerhard_correction_sha256=sha(Path('translations/gerhard_surname_editorial_release_v2.json').read_bytes()),B49_correction='translations/hodram_B49_editorial_release_v3.json',B49_correction_sha256=sha(Path('translations/hodram_B49_editorial_release_v3.json').read_bytes())),dependencies={str(p):sha(p.read_bytes()) for p in sorted(normalized)},individual_row_count_infos=3,exact_warning_exception_count=0,all3_source_current_final_context_prose_names_native_stored_actual_FE_VRAM_andmeasured_scope_bound=True,policy_validation_independent_production_atomic_registered_integration_pending=True,new_credit=0,full_goal_complete=False))
    PROFILE.write_text(profile.replace('CONTRACT_DIGEST',sha(CONTRACT.read_bytes())),encoding='utf-8');ROOT.mkdir(parents=True)
    save(ROOT/'frozen_contract.json',dict(contract=str(CONTRACT),contract_sha256=sha(CONTRACT.read_bytes()),manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),modules={str(p):sha(p.read_bytes()) for p in [PROFILE,FORMATTER,PLANNER,NAME_POLICY]},records=3,typed_choices=0,single_pages=3,scoped_names=1,source_FE=1,source_macro_counts=dict(FI=0,FA=0,FO=0),infos=3,warnings=0,waivers=0,dependency_count=len(normalized),integrated_builder_not_accidentally_pinned=True,source_locked_templates={str(p):sha(p.read_bytes()) for p in [template_path,layout_path,planner_path,names_path]},all_native_high_integer_constants_preserved_in_each_derived_module=True,all_prior_artifacts_preserved_no_global_profile_font_QA_guard_orprose_change=True,new_credit=0,full_goal_complete=False))
    print('Frozen B50:3speech pages/nochoice/one scopedLil name/zero macros/3infos/0warnings/waivers;dependencies',len(normalized),'.Policy/production/atomic/registered release pending;zero credit.')
