"""Freeze all82 reviewed bodies,ten scoped names and exact source/native/actual evidence."""
import sys
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts import plan_Hodram_B54_B60_v8802d as private
from scripts.review_Hodram_B54_B60_actual_v8825 import PROOFS as ACTUAL_PROOFS
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B54_B60_policy_v8830')
DOC=Path('translations/hodram_B54_B60_editorial_manuscript_v4.json')
NAMES=Path('translations/hodram_B54_B60_speaker_name_review_v2.json')
PLAN=private.ROOT/'automatic_plans.json'
APPROVAL=Path('work/analysis/Hodram_B54_B60_format_v8826/formatting_approval.json')
METADATA=Path('work/analysis/Hodram_B54_B60_metadata_v8829/explicit_route_binding.json')
ACTUAL=Path('work/analysis/Hodram_B54_B60_actual_review_v8825/qualified_actual_review.json')
CONTRACT=Path('translations/hodram_B54_B60_native_contract_v1.json')
BASE=Path('dk4tool/dialogue')
OUTPUTS={k:BASE/f'hodram_B54_B60_{k}_v1.py' for k in ['profile','layout','plan','names']}
PROOFS={**ACTUAL_PROOFS,'actual_review':str(ACTUAL),'metadata':str(METADATA),'approval':str(APPROVAL),
 'source_controls':'work/analysis/Hodram_B54_B60_source_controls_v8791/source_controls.json',
 'source_names':'work/analysis/Hodram_B54_B60_names_v8792/ten_source_identities_current_getters_voices_andplanes.json',
 'source_clean_names':'work/analysis/Hodram_B54_B60_clean_names_v8793/twenty_clean_full_andprogressive_compositions_current_binding.json',
 'source_display':'work/analysis/Hodram_B54_B60_source_display_v8794/82_complete_source_dispatches_alignments_pages_andmacro_binding.json',
 'source_context':'work/analysis/Hodram_B54_B60_clean_context_v8795/complete_clean_linked_15_37_65_128_142_context_before_B54_B60_English.json',
 'source_paths':'work/analysis/Hodram_B58_source_paths_v8796/all64_structural_paths_49utterance_memberships_unforced_opening_reference.json',
 'source_macros':'work/analysis/Hodram_B54_B60_source_macros_v8797b/FI_given_FA_surname_original_virtual_getter_trace.json',
 'source_view':'work/analysis/Hodram_B54_B60_source_review_v8798b/source_context_names_display_review_before_current_English.json',
 'current':'work/analysis/Hodram_B54_B60_current_v8799/current_effective.json',
 'logical':'work/analysis/Hodram_B54_B60_logical_v8801/logical_paragraphs.json',
 'plan':str(PLAN),'pages':'work/analysis/Hodram_B54_B60_pages_v8804/compiled_native_pages.json',
 'native_view':'work/analysis/Hodram_B54_B60_native_view_v8805/all82_native_English_direct_view_andboundary_review.json'}

if __name__=='__main__':
    assert not ROOT.exists() and not CONTRACT.exists() and all(not p.exists() for p in OUTPUTS.values())
    doc,names,plan,approval,metadata,actual=map(read,[DOC,NAMES,PLAN,APPROVAL,METADATA,ACTUAL]);data={k:read(p) for k,p in PROOFS.items()}
    assert metadata['manuscript_sha256']==sha(DOC.read_bytes()) and metadata['predecessor_sha256']==approval['manuscript_sha256']
    assert approval['all82_five_gates_true'] and approval['names_sha256']==sha(NAMES.read_bytes())
    assert len(doc['records'])==82 and not doc['typed_choice_records'] and doc['typed_choice_objects']==0 and doc['source_FE_panels']==1
    assert doc['revised']==46 and doc['retained']==36 and doc['route']==1 and doc['route_identity']=='Hodram' and doc['blocks']==list(range(54,61)) and doc['registered_predecessor_profile']=='all-routes-unified-v8778'
    assert doc['records']==read(doc['predecessor_manuscript'])['records'] and all(all(r['review'].values()) for r in doc['records']+names['records'])
    assert (actual['total_runs'],actual['total_frames'],actual['total_holds'])==(14,130014,676) and len(actual['actual_unique_text_IDs'])==63 and len(actual['offline_only_text_IDs'])==19
    assert data['reference']['only_changed_blocks']==list(range(54,61)) and data['references']['external_references_complete']
    assert not plan['failures'] and len(plan['records'])==82 and doc['source_current_final_references_complete']
    image=NdsImage.open(doc['current_ROM']);assert sha(Path(doc['current_ROM']).read_bytes())==doc['current_ROM_sha256']
    groups={g['block']:g for g in data['relocation']['groups']};assert set(groups)==set(range(54,61))
    assert sum(len(g['all_target_commands']) for g in groups.values())==152 and sum(len(g['relative_fixups']) for g in groups.values())==24
    bindings={}
    for row,p in zip(doc['records'],plan['records'],strict=True):
        group=groups[row['block']]
        assert row['id']==p['id'] and row['english']==row['logical_English']==p['logical_English']==' '.join(p['lines'])
        assert row['compiled_hex']==p['encoded_hex'] and row['planned_English_markup']==p['planning_record']['english']
        assert p['expected_native_pages']==row['expected_native_pages'] in [1,2] and p['max_total_rows'] in [4,8]
        assert row['qa_waivers']==row['qa_waiver_scope']==[] and not any(i['severity'] in ['error','warning'] for i in p['base_QA']['issues'])
        assert bytes.fromhex(row['stored_hex'])==bytes.fromhex(row['compiled_hex'])+(b' ' if row['compiler_owned_parity_space'] else b'')
        bindings[row['id']]=dict(file_path='/data/SC1.DK4',route=1,route_identity='Hodram',block=row['block'],source_block_hashes=[group['clean_block_sha256'],group['source_block_sha256']],
            source_reference=row['source_reference'],current_reference=row['current_reference'],final_reference=row['final_reference'],source_complete_preamble_hex=row['source_complete_preamble_hex'],
            compiler_source_hex=row['source_hex'],predecessor_record_hex=row['current_hex'],source_selector=row['source_selector'],source_kind=row['kind'],consumer='FE-paper' if row['source_selector']==254 else 'progressive',
            planning_record={k:p['planning_record'][k] for k in ['id','english','kind','source_hex','source_selector']},compiled_hex=p['encoded_hex'],stored_hex=row['stored_hex'],compiler_owned_parity_space=row['compiler_owned_parity_space'],
            lines=p['lines'],maximum_total_rows=p['max_total_rows'],native_page_count=p['expected_native_pages'],
            row_count_reason=row['native_body_review_reason'],ordinary_wrap_reasons=[row['localization_note'],row['native_body_review_reason']],
            base_QA_issues=deepcopy(p['base_QA']['issues']),qa_waivers=[],qa_waiver_reason=None,qa_waiver_scope=[],approved_fields=deepcopy(row))
    assert {b['source_selector'] for b in bindings.values()}=={1,20,23,24,36,84,113,114,119,141,254}
    assert sum(b['native_page_count'] for b in bindings.values())==85 and sum(b['compiler_owned_parity_space'] for b in bindings.values())==40
    templates={k:BASE/f'hodram_B31_B53_{k}_v1.py' for k in OUTPUTS}
    template=templates['profile'].read_text('utf-8');old_digest=template.split('CONTRACT_SHA="',1)[1].split('"',1)[0];oldmetrics=template.split('metrics_source="',1)[1].split('")',1)[0]
    metrics=('Exact registeredV8778/captain1;82original preambles/152commands/seven blocks/24relatives/sixqueries/33nonprosecontrols/seven distinct fullnormalends andtails. '
        'Full216px usable width,84progressive pages plusoneFE228x48/288stride/6x12/16pitch. Three English records use two pages. FI6/FA9/FO15 withsourceFI3/FA4/FO0;source-captain virtual slots prove given/surname semantics. '
        'Six exact source-bound ellipsis/question reactions.24original QAinfos,zero errors/warnings/waivers. Forty compiler-owned parity tails preserve the85viewed fullnative planes. '
        'Independent block/archive/wholeNDS inverses;325fresh loads,14fresh plus636exactreused parentmodes;source/current/finalrefs andunchanged caller units bound. '
        'Twelve initialized whole-script coldboots116012frames/580holds/129pageoccurrences observe63unique utterances;19remainoffline including18B58conditionals andB55. '
        'B56 actual FE contexts/palette/bitmap/VRAM/RGB andabsentheader pass. B59 originalresource show-hide sequence andall7corresponding upperpanels match. '
        'B60 focused14002frames shares theoriginal prefix throughA6400;81callbacks beforeA6640 matchtheir ownlongrun fullmemory/CPU/TCM. At7001 all5sampled components/wholeactors/captain/calendar match. '
        'All long/focused duration,RNG,RGB,followingcommand andB60lateactor differences remain;no immediate-return mainRAM snapshot,causal diagnosis orfuture equivalence claim. '
        'Ten progressive labels retain source/contextual names;8actual,20and113offline here. Geronimo/Alonso sharedde/fullcatalogue/all207/customnames/widercontexts remainopen. '
        'No natural eventactivation,original location,earned chronology,forced predicates/roster/flags/results,fullroute orhardware claim.')
    texts={}
    texts['profile']=checked_text(template,{'translations/hodram_B31_B53_native_contract_v1.json':CONTRACT.as_posix(),old_digest:'CONTRACT_DIGEST',
        'Hodram-B31-B53':'Hodram-B54-B60','Hodram B31/B53':'Hodram B54-B60','len(d["record_bindings"])!=3':'len(d["record_bindings"])!=82',
        'd["complete_native_pages"]!=3':'d["complete_native_pages"]!=85','three-paragraph/three-page':'82-paragraph/85-page',
        'd["source_macro_counts"]!={"FI":0,"FA":0,"FO":0}':'d["source_macro_counts"]!={"FI":3,"FA":4,"FO":0}',oldmetrics:metrics})
    texts['layout']=checked_text(templates['layout'].read_text('utf-8'),{'hodram_B31_B53_profile_v1':'hodram_B54_B60_profile_v1','hodram_B31_B53_plan_v1':'hodram_B54_B60_plan_v1','Hodram-B31-B53':'Hodram-B54-B60'})
    plan_template=templates['plan'].read_text('utf-8');old_plan_digest=plan_template.split('PLAN_SHA="',1)[1].split('"',1)[0]
    texts['plan']=checked_text(plan_template,{'plan_Hodram_B31_B53_v8725':'plan_Hodram_B54_B60_v8802d','work/analysis/Hodram_B31_B53_layout_v8725/automatic_plans.json':PLAN.as_posix(),old_plan_digest:sha(PLAN.read_bytes())})
    texts['names']='''"""Exact ten scoped progressive identities;fullcatalogue/all207/custom names remain open."""
from dk4tool.dialogue.hodram_B54_B60_profile_v1 import contract

def validate_scoped_names(review):
    expected=contract()['name_review_binding']
    if review!=expected:raise ValueError('B54-B60 names:exact source-qualified review andnative/actual scope required')
    if [r['actor_ID'] for r in review['records']]!=[1,20,23,24,36,84,113,114,119,141]:
        raise ValueError('B54-B60 names:exact ten approved scoped identities required')
    for row in review['records']:
        if not all(row['review'].get(g) is True for g in ['source','context','localization','naturalness','formatting']):
            raise ValueError('B54-B60 names:allfive individual scoped gates required')
    if not review['wider_catalogue_UI_all207_names_roles_aliases_customnames_andother_contexts_still_open'] or not review['full_name_shared_de_ownership_deployment_andconsumers_still_open']:
        raise ValueError('B54-B60 names:exact scoped preservation andopen full-name limits required')
    if review['actual_progressive_actor_IDs']!=[1,23,24,36,84,114,119,141] or review['offline_progressive_actor_IDs']!=[20,113] or review['new_credit']!=0:
        raise ValueError('B54-B60 names:exact actual/offline scope andzero duplicate credit required')
    return expected
'''
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
                for key in ['native_plane','physical_plane']:
                    if key in page:
                        path=Path(page[key]);assert sha(path.read_bytes())==page[key+'_sha256'];deps.add(path)
    for row in data['models']['name_planes']:
        path=Path(row['native_plane']);assert sha(path.read_bytes())==row['native_plane_sha256'];deps.add(path)
    run_bindings=[*actual['runs']]
    for version in ['clean_Japanese','revised_English']:
        path=Path('work/analysis/Hodram_B60_boundary_focus_runs_v8822')/f'route1_B60_{version}'/'terminal.json';run_bindings.append(dict(terminal=str(path),terminal_sha256=sha(path.read_bytes())))
    for run in run_bindings:
        path=Path(run['terminal']);assert sha(path.read_bytes())==run['terminal_sha256'];deps.add(path);terminal=read(path);report=read(terminal['report'])
        for key in ['report','observer','run_plan']:
            path=Path(terminal[key]);assert sha(path.read_bytes())==terminal[key+'_sha256'];deps.add(path)
        for photo in report['frames_captured']:
            path=Path(photo['path']);assert sha(path.read_bytes())==photo['PNG_sha256'];deps.add(path)
        snap=report['read_only_RAM_snapshot'];path=Path(snap['path']);assert sha(path.read_bytes())==snap['sha256'];deps.add(path)
    for sheet in actual['viewed_sheets']:
        path=Path(sheet['path']);assert sha(path.read_bytes())==sheet['sha256'];deps.add(path)
    # FE exact typed snapshots andheld RAM/VRAM/bitmap dependencies are not just PNGs.
    def collect_refs(value):
        if isinstance(value,dict):
            if isinstance(value.get('path'),str) and isinstance(value.get('sha256'),str):
                path=Path(value['path'])
                if path.is_file() and path.suffix not in ['.nds','.xdelta']:assert sha(path.read_bytes())==value['sha256'];deps.add(path)
            for v in value.values():collect_refs(v)
        elif isinstance(value,list):
            for v in value:collect_refs(v)
    collect_refs(data['B56_FE'])
    for key in ['layout','plan','names']:OUTPUTS[key].write_text(texts[key],encoding='utf-8');deps.add(OUTPUTS[key])
    excluded={Path(p).resolve() for p in ['scripts/build_integrated_release.py','translations/editorial_review_current_v1.json','translations/release_stack.json','translations/rom_retention_pins.json']}
    normalized={p.resolve() for p in deps if p.resolve() not in excluded and p.suffix not in ['.nds','.xdelta']};assert all(p.is_file() for p in normalized)
    runtime={p:sha(image.read_file(p)) for p in ['/__arm9__.bin','/COMMON/MESFILE.DK4','/GRP/KANJI.FNT','/data/EV1.DK4']}
    save(CONTRACT,dict(format='Hodram-B54-B60-source-native-contract-v1',record_bindings=bindings,choice_bindings={},review_gates=doc['review_gates'],batch_binding={k:deepcopy(v) for k,v in doc.items() if k!='records'},
        runtime_component_hashes=runtime,measured_macro_ascii_lengths=dict(FI=6,FA=9,FO=15),source_macro_counts=dict(FI=3,FA=4,FO=0),
        physical_native_rows_per_page=4,physical_progressive_viewport=[216,64],physical_FE_logical_viewport=[228,48],physical_FE_stride=288,usable_text_width_px=216,complete_native_pages=85,
        source_control_binding=dict(commands=152,complete_preambles=82,relatives=24,queries=6,nonprose_controls=33,source_FE_panels=1,
            exact_groups=deepcopy(data['source_controls']['groups']),exact_relocation_groups=deepcopy(data['relocation']['groups']),normal_end_existing_resultword_independent_of_interpreter_r3=True),
        name_review_binding=names,explicit_complete_registered_predecessor=dict(profile='all-routes-unified-v8778',candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],ARM9_sha256=runtime['/__arm9__.bin']),
        dependencies={str(p):sha(p.read_bytes()) for p in sorted(normalized)},individual_row_count_infos=24,exact_warning_exception_count=0,
        observed_actual_speech_IDs=actual['actual_unique_text_IDs'],unvisited_conditional_text_IDs=actual['offline_only_text_IDs'],actual_scope=deepcopy(actual),
        exact_source_current_final_context_prose_names_native_stored_representative_actual_andmeasured_scope_bound=True,
        policy_validation_independent_production_atomic_registered_integration_pending=True,new_credit=0,full_goal_complete=False))
    OUTPUTS['profile'].write_text(texts['profile'].replace('CONTRACT_DIGEST',sha(CONTRACT.read_bytes())),encoding='utf-8')
    ROOT.mkdir(parents=True);save(ROOT/'frozen_contract.json',dict(contract=str(CONTRACT),contract_sha256=sha(CONTRACT.read_bytes()),manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),
        modules={str(p):sha(p.read_bytes()) for p in OUTPUTS.values()},records=82,blocks=list(range(54,61)),typed_choices=0,complete_native_pages=85,scoped_names=10,source_FE=1,
        source_macro_counts=dict(FI=3,FA=4,FO=0),infos=24,warnings=0,waivers=0,dependency_count=len(normalized),
        integrated_builder_registry_ledger_pins_not_accidentally_pinned=True,source_locked_templates={str(p):sha(p.read_bytes()) for p in templates.values()},
        all_native_high_integer_constants_preserved_in_each_derived_module=True,all_approved_batch_keys_rows_andname_scope_bound_exactly=True,
        all_prior_artifacts_preserved_no_global_profile_font_QA_guard_orprose_change=True,new_credit=0,full_goal_complete=False))
    print(f'Frozen82records/85pages/10names/24QAinfos;{len(normalized)} immutabledependencies;zero errors/warnings/waivers.Production/integration pending.',flush=True)
