"""Freeze the approved two-block prose, names and exact native/actual evidence."""
import sys
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts import plan_Hodram_B31_B53_v8725 as private
from scripts.review_Hodram_B31_B53_actual_v8744 import PROOFS as ACTUAL_PROOFS
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_B31_B53_policy_v8749')
DOC=Path('translations/hodram_B31_B53_editorial_manuscript_v5.json')
NAMES=Path('translations/hodram_B31_B53_speaker_name_review_v3.json')
PLAN=private.ROOT/'automatic_plans.json'
APPROVAL=Path('work/analysis/Hodram_B31_B53_format_v8745b/formatting_approval.json')
METADATA=Path('work/analysis/Hodram_B31_B53_metadata_v8748/explicit_route_binding.json')
ACTUAL=Path('work/analysis/Hodram_B31_B53_actual_review_v8744/qualified_actual_review.json')
CONTRACT=Path('translations/hodram_B31_B53_native_contract_v1.json')
BASE=Path('dk4tool/dialogue')
OUTPUTS={k:BASE/f'hodram_B31_B53_{k}_v1.py' for k in ['profile','layout','plan','names']}
PROOFS={**ACTUAL_PROOFS,'actual_review':str(ACTUAL),'metadata':str(METADATA),'approval':str(APPROVAL)}

if __name__=='__main__':
    assert not ROOT.exists() and not CONTRACT.exists() and all(not p.exists() for p in OUTPUTS.values())
    doc,names,plan,approval,metadata,actual=map(read,[DOC,NAMES,PLAN,APPROVAL,METADATA,ACTUAL])
    data={k:read(p) for k,p in PROOFS.items()}
    assert metadata['manuscript_sha256']==sha(DOC.read_bytes()) and metadata['predecessor_sha256']==approval['manuscript_sha256']
    assert approval['all3_five_gates_true'] and approval['names_sha256']==sha(NAMES.read_bytes())
    assert len(doc['records'])==3 and not doc['typed_choice_records'] and doc['typed_choice_objects']==doc['source_FE_panels']==0 and doc['revised']==3 and doc['retained']==0
    assert doc['route']==1 and doc['route_identity']=='Hodram' and doc['blocks']==[31,53] and doc['registered_predecessor_profile']=='all-routes-unified-v8704'
    assert doc['records']==read(doc['predecessor_manuscript'])['records'] and all(all(r['review'].values()) for r in doc['records']+names['records'])
    assert (actual['total_runs'],actual['total_frames'],actual['total_holds'])==(4,24004,76) and actual['offline_only_text_IDs']==['DK4_MES_B31_R0013']
    assert data['reference']['only_changed_blocks']==[31,53] and data['references']['external_references_complete']
    assert not plan['failures'] and len(plan['records'])==3 and doc['source_current_final_references_complete']
    image=NdsImage.open(doc['current_ROM']);assert sha(Path(doc['current_ROM']).read_bytes())==doc['current_ROM_sha256']
    groups={g['block']:g for g in data['relocation']['groups']};assert set(groups)=={31,53}
    assert sum(len(g['all_target_commands']) for g in groups.values())==18 and sum(len(g['relative_fixups']) for g in groups.values())==4
    bindings={}
    for row,p in zip(doc['records'],plan['records'],strict=True):
        group=groups[row['block']]
        assert row['id']==p['id'] and row['english']==row['logical_English']==p['logical_English']==' '.join(p['lines'])
        assert row['compiled_hex']==p['encoded_hex'] and row['planned_English_markup']==p['planning_record']['english']
        assert p['expected_native_pages']==1 and p['max_total_rows']==4 and row['qa_waivers']==row['qa_waiver_scope']==[] and not p['base_QA']['issues']
        assert row['compiled_hex']==row['stored_hex'] and not row['compiler_owned_parity_space']
        bindings[row['id']]=dict(file_path='/data/SC1.DK4',route=1,route_identity='Hodram',block=row['block'],
            source_block_hashes=[group['clean_block_sha256'],group['source_block_sha256']],
            source_reference=row['source_reference'],current_reference=row['current_reference'],final_reference=row['final_reference'],
            source_complete_preamble_hex=row['source_complete_preamble_hex'],compiler_source_hex=row['source_hex'],predecessor_record_hex=row['current_hex'],
            source_selector=row['source_selector'],source_kind=row['kind'],consumer='progressive',
            planning_record={k:p['planning_record'][k] for k in ['id','english','kind','source_hex','source_selector']},
            compiled_hex=p['encoded_hex'],stored_hex=row['stored_hex'],compiler_owned_parity_space=False,
            lines=p['lines'],maximum_total_rows=4,native_page_count=1,row_count_reason='Use original full216px width and retain every reviewed word on its complete native page.',
            ordinary_wrap_reasons=[row['localization_note'],row['native_body_review_reason']],base_QA_issues=[],qa_waivers=[],qa_waiver_reason=None,qa_waiver_scope=[],approved_fields=deepcopy(row))
    assert {b['source_selector'] for b in bindings.values()}=={34,113}
    templates={k:BASE/f'hodram_B51_{k}_v1.py' for k in OUTPUTS}
    template=templates['profile'].read_text('utf-8');oldmetrics=template.split('metrics_source="',1)[1].split('")',1)[0]
    metrics=('Exact registeredV8704/captain1 runtime andoriginal22/71 six-byte preambles. Full216px width, three native/stored singlepages, FI6/FA9/FO15 withzero source macros,zero QAissues/warnings/waivers. '
        'Two complete blocks18commands/four relatives/one rawquery/eight opaquecontrols/two normalends,independent block/archive/wholeNDS inverses,325loads650parentmodes andcomplete unchanged caller census arebound. '
        'Four initialized whole-block coldboots24004frames/76complete body-name holds/fourpageoccurrences verify long B31 andB53warning;shortB31 remains offline-only,never force selected. '
        'Actual normalreturns B31[0,1]at4016 andB53[0,0]at4013 matchbothlanguages. Normalend preserves the existing parserresult secondword independently ofinterpreter r3;50source seededends and50unchanged callerfragments bind separatechannels. '
        'Only three decodedlength differences remain;commandduration/UIrequest/boundaryRNG/followingcommands match. Allfive finalcomponents/wholeactors/captain1/rawcalendar/finalseed3325064553 and68laterRGBpairs matchthrough6001frames. '
        'Actor34 source getters include the actual Fazul middlefield;retain sourced components/order andexisting mixedwidth storage. Actual progressive34/113 headers areverified;fullcatalogueUI/all207/customnames remainopen. '
        'No natural eventactivation,original location,earnedchronology,opaque effectsemantic invention,everyframecausality,broad future simulation,fullroute orhardware claim.')
    texts={}
    texts['profile']=checked_text(template,{
        'translations/hodram_B51_native_contract_v1.json':CONTRACT.as_posix(),
        '3f33f5ecacde7938594b8018836d6c58ce4711d9d819d6aef2a72a6edceab57d':'CONTRACT_DIGEST',
        'Hodram-B51':'Hodram-B31-B53','Hodram B51':'Hodram B31/B53',
        'len(d["record_bindings"])!=5':'len(d["record_bindings"])!=3','d["complete_native_pages"]!=5':'d["complete_native_pages"]!=3',
        'five-paragraph/five-page':'three-paragraph/three-page',oldmetrics:metrics,
        '    for key,value in d["batch_binding"].items():':'    if set(doc)!=set(d["batch_binding"])|{"records"}:raise ValueError("Exact complete approved batch keys required")\n    for key,value in d["batch_binding"].items():',
        'if any(row.get(k)!=v for k,v in b["approved_fields"].items()):':'if row!=b["approved_fields"]:',
    })
    texts['layout']=checked_text(templates['layout'].read_text('utf-8'),{
        'hodram_B51_profile_v1':'hodram_B31_B53_profile_v1','hodram_B51_plan_v1':'hodram_B31_B53_plan_v1','Hodram-B51':'Hodram-B31-B53'})
    texts['plan']=checked_text(templates['plan'].read_text('utf-8'),{
        'plan_Hodram_B51_v8562':'plan_Hodram_B31_B53_v8725','work/analysis/Hodram_B51_layout_v8562/automatic_plans.json':PLAN.as_posix(),
        '3e4e9f12b6d2fb7c5bc8a99ce772b9d15c6a3bc70ac7d1d205a883d0562af24b':sha(PLAN.read_bytes()),
    })
    texts['names']=checked_text(templates['names'].read_text('utf-8'),{
        'Exact four source-qualified identities':'Exact two source-qualified identities','hodram_B51_profile_v1':'hodram_B31_B53_profile_v1','B51 names:':'B31/B53 names:',
        "[(1,'Hodram Bergstrom'),(16,'Gerhard Adernkatz'),(18,'Charles Rochefort'),(113,'Port Worker')]":"[(34,'Barbarossa Hayreddin'),(113,'Port Worker')]",
        'exact four approved scoped identities required':'exact two approved scoped identities required',
        "not review['no_new_name_asset_orall207_name_review_credit'] or review['scoped_actor_IDs']!=[1,16,18,113]":"review['new_name_asset_changes']!=0 or not review['wider_catalogue_UI_all207_names_roles_aliases_customnames_andother_contexts_still_open'] or not review['full_name_resolution']['actual_B31_progressive_header_verified'] or not review['full_name_resolution']['full_catalogue_UI_still_unobserved']",
    })
    for key,text in texts.items():compile(text.replace('CONTRACT_DIGEST','0'*64),str(OUTPUTS[key]),'exec')
    deps={DOC,NAMES,PLAN,APPROVAL,METADATA,ACTUAL,Path(__file__),Path(private.__file__),*templates.values(),*map(Path,PROOFS.values())}
    for packet in data.values():
        for p,h in packet.get('evidence',{}).items():
            path=Path(p)
            if isinstance(h,str) and len(h)==64:
                assert sha(path.read_bytes())==h
                if path.suffix not in ['.nds','.xdelta']:deps.add(path)
    for name,module in list(sys.modules.items()):
        if not (name.startswith('scripts.') or name.startswith('dk4tool.')):continue
        p=getattr(module,'__file__',None)
        if p and Path(p).suffix=='.py':deps.add(Path(p))
        for value in vars(module).values():
            if isinstance(value,Path) and value.suffix not in ['.nds','.xdelta'] and value.is_file() and not any(s in value.as_posix() for s in ['editorial_review_current_v1.json','release_stack.json','rom_retention_pins.json','docs/']):deps.add(value)
    for rows in data['models']['native_models'].values():
        for row in rows:
            for page in row['pages']:
                path=Path(page['native_plane']);assert sha(path.read_bytes())==page['native_plane_sha256'];deps.add(path)
    for row in data['models']['name_planes']:
        path=Path(row['native_plane']);assert sha(path.read_bytes())==row['native_plane_sha256'];deps.add(path)
    for run in actual['run_bindings']:
        terminal=read(run['terminal']);assert sha(Path(run['terminal']).read_bytes())==run['terminal_sha256']
        report=read(terminal['report'])
        for photo in report['frames_captured']:
            path=Path(photo['path']);assert sha(path.read_bytes())==photo['PNG_sha256'];deps.add(path)
        snap=report['read_only_RAM_snapshot'];path=Path(snap['path']);assert sha(path.read_bytes())==snap['sha256'];deps.add(path)
    for sheet in actual['directly_viewed_dialogue_andtransition_sheets']:
        path=Path(sheet['path']);assert sha(path.read_bytes())==sheet['sha256'];deps.add(path)
    for key in ['layout','plan','names']:OUTPUTS[key].write_text(texts[key],encoding='utf-8');deps.add(OUTPUTS[key])
    excluded={Path('scripts/build_integrated_release.py').resolve(),Path('translations/editorial_review_current_v1.json').resolve(),Path('translations/release_stack.json').resolve(),Path('translations/rom_retention_pins.json').resolve()}
    normalized={p.resolve() for p in deps if p.resolve() not in excluded and p.suffix not in ['.nds','.xdelta']};assert all(p.is_file() for p in normalized)
    runtime={p:sha(image.read_file(p)) for p in ['/__arm9__.bin','/COMMON/MESFILE.DK4','/GRP/KANJI.FNT','/data/EV1.DK4']}
    save(CONTRACT,dict(format='Hodram-B31-B53-source-native-contract-v1',record_bindings=bindings,choice_bindings={},review_gates=doc['review_gates'],
        batch_binding={k:deepcopy(v) for k,v in doc.items() if k!='records'},runtime_component_hashes=runtime,measured_macro_ascii_lengths=dict(FI=6,FA=9,FO=15),source_macro_counts=dict(FI=0,FA=0,FO=0),
        physical_native_rows_per_page=4,physical_progressive_viewport=[216,64],usable_text_width_px=216,complete_native_pages=3,
        source_control_binding=dict(commands=18,complete_preambles=3,relatives=4,queries=1,opaque_controls=8,source_FE_panels=0,
            exact_groups=deepcopy(data['source_controls']['groups']),exact_relocation_groups=deepcopy(data['relocation']['groups']),
            normal_end_existing_resultword_independent_of_interpreter_r3=True,qualified_actual_channel_proof=PROOFS['audit_correction']),
        name_review_binding=names,explicit_complete_registered_predecessor=dict(profile='all-routes-unified-v8704',candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],
            ARM9_sha256=runtime['/__arm9__.bin'],shared_late_hook_after_B51_contains_complete_B52=True),
        dependencies={str(p):sha(p.read_bytes()) for p in sorted(normalized)},individual_row_count_infos=0,exact_warning_exception_count=0,
        observed_actual_speech_IDs=actual['actual_unique_text_IDs'],unvisited_conditional_text_IDs=actual['offline_only_text_IDs'],
        actual_scope=deepcopy(actual),exact_source_current_final_context_prose_names_native_stored_representative_actual_andmeasured_scope_bound=True,
        policy_validation_independent_production_atomic_registered_integration_pending=True,new_credit=0,full_goal_complete=False))
    OUTPUTS['profile'].write_text(texts['profile'].replace('CONTRACT_DIGEST',sha(CONTRACT.read_bytes())),encoding='utf-8')
    ROOT.mkdir(parents=True);save(ROOT/'frozen_contract.json',dict(contract=str(CONTRACT),contract_sha256=sha(CONTRACT.read_bytes()),manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),
        modules={str(p):sha(p.read_bytes()) for p in OUTPUTS.values()},records=3,blocks=[31,53],typed_choices=0,single_pages=3,scoped_names=2,source_FE=0,
        source_macro_counts=dict(FI=0,FA=0,FO=0),infos=0,warnings=0,waivers=0,dependency_count=len(normalized),
        integrated_builder_registry_ledger_pins_not_accidentally_pinned=True,source_locked_templates={str(p):sha(p.read_bytes()) for p in templates.values()},
        all_native_high_integer_constants_preserved_in_each_derived_module=True,all_approved_batch_keys_rows_andname_scope_bound_exactly=True,
        all_prior_artifacts_preserved_no_global_profile_font_QA_guard_orprose_change=True,new_credit=0,full_goal_complete=False))
    print(f'Frozen B31/B53:three pages/two names/zero QAissues;{len(normalized)} immutable dependencies. Policy/production/atomic/registered work pending;zero credit.',flush=True)
