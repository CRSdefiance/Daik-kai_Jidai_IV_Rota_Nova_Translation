"""Freeze six reviewed outcomes, exact mixed native consumers and every approved row/diagnostic."""
import sys
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts import plan_Hodram_B47_B48_v8323 as private
from scripts.prepare_Hodram_outcome_checkpoint_v8341 import PROOFS as prior_paths
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_outcome_policy_v8345')
DOC=Path('translations/hodram_B47_B48_editorial_manuscript_v4.json')
NAMES=Path('translations/hodram_B47_B48_speaker_name_review_v2.json')
PLAN=private.ROOT/'six_automatic_plans_original_usable_width_distinct_FE_all_QA_preserved.json'
BINDING=Path('work/analysis/Hodram_outcome_current_binding_v8343/source_current_final_reference_binding.json')
REBUILD=Path('work/analysis/Hodram_outcome_independent_rebuild_v8344/six_records15_commands_two_clean_source_inverses_entire_tested_ROM_equal.json')
CONTRACT=Path('translations/hodram_outcomes_native_contract_v1.json')
PROFILE=Path('dk4tool/dialogue/hodram_outcomes_profile_v1.py')
FORMATTER=Path('dk4tool/dialogue/hodram_outcomes_layout_v1.py')
PLANNER=Path('dk4tool/dialogue/hodram_outcomes_plan_v1.py')
if __name__=='__main__':
    assert not ROOT.exists() and all(not p.exists() for p in [CONTRACT,PROFILE,FORMATTER,PLANNER])
    doc,names,plan,binding,rebuild=map(read,[DOC,NAMES,PLAN,BINDING,REBUILD]);approval=read(prior_paths['display']);reloc=read(prior_paths['relocation'])
    assert len(doc['records'])==6 and doc['revised']==doc['retained']==3 and all(all(r['review'].values()) for r in doc['records']+names['records'])
    assert binding['manuscript_sha256']==rebuild['manuscript_sha256']==sha(DOC.read_bytes()) and binding['name_review_sha256']==sha(NAMES.read_bytes())
    assert approval['manuscript_sha256']==binding['approved_predecessor_manuscript_sha256'] and approval['name_review_sha256']==sha(NAMES.read_bytes()) and approval['actual_complete_body_header_orFE_absent_header_holds']==100
    assert not plan['failures'] and len(plan['records'])==6 and rebuild['independent_sparse_source_reconstruction_matches_commandwise_research_archive_andentire_tested_ROM']
    image=NdsImage.open(doc['current_ROM']);assert sha(Path(doc['current_ROM']).read_bytes())==doc['current_ROM_sha256']==rebuild['candidate_sha256']
    bindings={};infos=0
    for row,p in zip(doc['records'],plan['records'],strict=True):
        assert row['id']==p['id'] and row['english']==row['logical_English']==p['logical_English']==' '.join(p['lines']) and row['planned_English_markup']==p['planning_record']['english'] and row['compiled_hex']==p['encoded_hex']
        assert p['expected_native_pages']==1 and p['max_total_rows']==4 and row['qa_waivers']==row['qa_waiver_scope']==[] and all(i['severity']=='info' for i in p['base_QA']['issues'])
        assert sum(i['code']=='line-break-count' for i in p['base_QA']['issues'])==1;infos+=1;group=next(g for g in reloc['groups'] if g['block']==row['block'])
        bindings[row['id']]=dict(file_path=row['file_path'],route=1,route_identity='Hodram',block=row['block'],source_block_hashes=[group['clean_block_sha256'],group['source_block_sha256']],
            source_reference=row['source_reference'],current_reference=row['current_reference'],source_complete_preamble_hex=row['source_complete_preamble_hex'],compiler_source_hex=row['source_hex'],predecessor_record_hex=row['current_hex'],source_selector=row['source_selector'],source_kind=row['kind'],consumer='FE-paper' if row['source_selector']==254 else 'progressive',
            planning_record={k:p['planning_record'][k] for k in ['id','english','kind','source_hex','source_selector']},compiled_hex=p['encoded_hex'],lines=p['lines'],maximum_total_rows=4,native_page_count=1,
            row_count_reason='Use the original full usable width and preserve every reviewed word on one complete native page.',ordinary_wrap_reasons=[row['localization_note'],row['native_body_review_reason']],base_QA_issues=p['base_QA']['issues'],qa_waivers=[],qa_waiver_reason=None,qa_waiver_scope=[],approved_fields=deepcopy(row))
    assert infos==6 and {b['source_selector'] for b in bindings.values()}=={2,254} and sum(b['source_selector']==254 for b in bindings.values())==1
    assert {m:sum(bytes.fromhex(r['source_hex'])[1:].count(m.encode()) for r in doc['records']) for m in ['FI','FA','FO']}==dict(FI=1,FA=0,FO=0)
    template=Path('dk4tool/dialogue/hodram_three_blocks_profile_v1.py').read_text('utf8');oldmetrics=template.split('metrics_source="',1)[1].split('")',1)[0]
    profile=checked_text(template,{
        'translations/hodram_three_blocks_native_contract_v1.json':CONTRACT.as_posix(),
        '15f677bd433171fc5b8feac2dd198547a693b948638433c474789dd72aa49462':'CONTRACT_DIGEST',
        'Hodram-three-blocks':'Hodram-outcomes','Hodram B137/B45/B46':'Hodram B47/B48',
        'len(d["record_bindings"])!=28':'len(d["record_bindings"])!=6','d["complete_native_pages"]!=28':'d["complete_native_pages"]!=6',
        'twenty-eight-paragraph/twenty-eight-page':'six-paragraph/six-page',
        '{"FI":0,"FA":0,"FO":0}':'{"FI":1,"FA":0,"FO":0}',
        'else {1,2,9,16,18,113}':'else {2}',
        oldmetrics:'Exact registered V8300 Hodram captain1:five progressive216px pages andone original FE228x48 bitmap with216px usablewidth,288stride/6x12/16physicalpitch;source02/FE sixbyte preambles. Default FI6/FA9/FO15,one sourceFI. Allsix complete native/stored pages and100 actual body/name orFE-absent-header holds;live FE descriptors/palette/bankD VRAM match independent nativeplanes. Six line-count infos,zero warnings orwaivers. Four whole-script initialized fixtures40004frames plus8002focusedFE frames are not naturaloptional activation. B48 source4495/English4494 returns[0,0];script-boundary seeds equal,butfinalB48 seeds differ and13of93laterRGB pairs differ. Allfive checked final components/actors/captain1 match. No everyframe causal,future-outcome,broad simulation,fullroute orhardware claim.',
    })
    layout=checked_text(Path('dk4tool/dialogue/hodram_three_blocks_layout_v1.py').read_text('utf8'),{'hodram_three_blocks':'hodram_outcomes','Hodram-three-blocks':'Hodram-outcomes'})
    planner=checked_text(Path('dk4tool/dialogue/hodram_three_blocks_plan_v1.py').read_text('utf8'),{
        'plan_Hodram_B137_B45_B46_v8245':'plan_Hodram_B47_B48_v8323',
        'work/analysis/Hodram_B137_B45_B46_layout_v8245/28_automatic_Hodram_plans_full_native_width.json':PLAN.as_posix(),
        '01dc71ce720fd5241dd4b1cdbd81dda8206156008377a1dceb182ed1a7108dc5':sha(PLAN.read_bytes()),
        'source_word_boundary_pairs':'coherent_pairs','source_coherent_phrase_pairs':'coherent_pairs','source_owned_plan_adapter':'source_owned_planner',
    })
    for p,code in [(PROFILE,profile.replace('CONTRACT_DIGEST','0'*64)),(FORMATTER,layout),(PLANNER,planner)]:compile(code,str(p),'exec')
    dependencies={DOC,NAMES,PLAN,BINDING,REBUILD,Path(__file__),Path(private.__file__),Path('dk4tool/patch/hodram_outcome_rebuild_v1.py'),Path('dk4tool/patch/hodram_outcome_references_v1.py')}
    dependencies.update(Path(p) for p in prior_paths.values())
    # Pin imported project code and the immutable global data files it reads.
    # Parent release verification independently owns the complete prior stack;
    # unrelated historical editorial contracts are not recursively inherited.
    for name,module in list(sys.modules.items()):
        if not (name.startswith('scripts.') or name.startswith('dk4tool.')):continue
        path=getattr(module,'__file__',None)
        if path and Path(path).suffix=='.py':dependencies.add(Path(path))
        for value in vars(module).values():
            if isinstance(value,Path) and value.suffix not in ['.nds','.xdelta'] and value.is_file() and not any(s in value.as_posix() for s in ['editorial_review_current_v1.json','release_stack.json','rom_retention_pins.json','docs/']):dependencies.add(value)
    for sheet in approval['all10_actual_comparison_andlater_difference_sheets_directly_viewed']:
        assert sha(Path(sheet['path']).read_bytes())==sheet['sha256'];dependencies.add(Path(sheet['path']))
    models=read(prior_paths['models'])
    for rows in models['native_models'].values():
        for row in rows:
            for page in row['pages']:
                for key in ['native_plane','physical_plane']:
                    if key in page:
                        path=Path(page[key]);assert sha(path.read_bytes())==page[key+'_sha256'];dependencies.add(path)
    for name in models['name_planes']:
        path=Path(name['native_plane']);assert sha(path.read_bytes())==name['native_plane_sha256'];dependencies.add(path)
    for p,code in [(FORMATTER,layout),(PLANNER,planner)]:p.write_text(code,encoding='utf8');dependencies.add(p)
    normalized={p.resolve() for p in dependencies};assert all(p.is_file() for p in normalized)
    runtime={p:sha(image.read_file(p)) for p in ['/__arm9__.bin','/COMMON/MESFILE.DK4','/GRP/KANJI.FNT','/data/EV1.DK4']}
    save(CONTRACT,dict(format='Hodram-outcomes-source-native-contract-v1',record_bindings=bindings,choice_bindings={},review_gates=doc['review_gates'],batch_binding={k:doc[k] for k in ['translation_policy','target_locale','encoder','review_gates','file_path','route','route_identity','blocks']},runtime_component_hashes=runtime,
        measured_macro_ascii_lengths=dict(FI=6,FA=9,FO=15),source_macro_counts=dict(FI=1,FA=0,FO=0),physical_native_rows_per_page=4,physical_progressive_viewport=[216,64],physical_FE_bitmap=[228,48],physical_FE_stride=288,usable_text_width_px=216,complete_native_pages=6,name_review_binding=names,
        explicit_registered_Gerhard_dependency=dict(candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],ARM9_sha256=runtime['/__arm9__.bin'],correction='translations/gerhard_surname_editorial_release_v2.json',correction_sha256=sha(Path('translations/gerhard_surname_editorial_release_v2.json').read_bytes())),
        dependencies={str(p):sha(p.read_bytes()) for p in sorted(normalized)},individual_row_count_infos=6,exact_warning_exception_count=0,
        all_source_current_final_refs_context_prose_names_native_stored_actual_FE_VRAM_andlater_difference_scope_bound=True,policy_validation_independent_actual_atomic_registered_integration_pending=True,new_credit=0,full_goal_complete=False))
    PROFILE.write_text(profile.replace('CONTRACT_DIGEST',sha(CONTRACT.read_bytes())),encoding='utf8');ROOT.mkdir(parents=True)
    save(ROOT/'frozen_six_mixed_consumer_paragraphs_Lil_name_one_FI_six_infos_zero_waivers.json',dict(contract=str(CONTRACT),contract_sha256=sha(CONTRACT.read_bytes()),modules={str(p):sha(p.read_bytes()) for p in [PROFILE,FORMATTER,PLANNER]},records=6,single_pages=6,scoped_names=1,source_FE=1,source_macro_counts=dict(FI=1,FA=0,FO=0),infos=6,warnings=0,dependency_count=len(normalized),
        all_prior_artifacts_immutable_no_global_profile_orfont_guard_change=True,new_credit=0,full_goal_complete=False))
    print('Frozen6:five progressive/one originalFE/one FI/one scopedLil name/six infos/zero waivers;dependencies',len(normalized),'.Policy andatomic validation pending;zero credit.')
