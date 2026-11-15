"""Freeze reviewed Hodram28 paragraphs, six names and exact source/native/actual scope."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.rafael_B50_profile_v1 import contract as prior_contract
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_three_block_policy_v8287')
DOC=Path('translations/hodram_B137_B45_B46_editorial_manuscript_v4.json')
NAMES=Path('translations/hodram_B137_B45_B46_speaker_name_review_v4.json')
PLAN=Path('work/analysis/Hodram_B137_B45_B46_layout_v8245/28_automatic_Hodram_plans_full_native_width.json')
RELOC=Path('work/analysis/Hodram_three_block_relocation_v8273/three_blocks28_speeches8_relative_sites40_native_cases_full_inverses.json')
APPROVAL=Path('work/analysis/Hodram_display_review_v8284/display_review_receipt.json')
CONTRACT=Path('translations/hodram_three_blocks_native_contract_v1.json')
PROFILE=Path('dk4tool/dialogue/hodram_three_blocks_profile_v1.py')
FORMATTER=Path('dk4tool/dialogue/hodram_three_blocks_layout_v1.py')
PLANNER=Path('dk4tool/dialogue/hodram_three_blocks_plan_v1.py')

if __name__=='__main__':
    assert not ROOT.exists() and all(not p.exists() for p in [CONTRACT,PROFILE,FORMATTER,PLANNER])
    doc,names,plan,reloc,approval=map(read,[DOC,NAMES,PLAN,RELOC,APPROVAL])
    assert len(doc['records'])==28 and doc['revised']==16 and doc['retained']==12 and not plan['failures']
    assert approval['manuscript_sha256']==sha(DOC.read_bytes()) and approval['name_review_sha256']==sha(NAMES.read_bytes())
    assert approval['all28_five_per_record_gates_true'] and approval['actual_complete_body_andname_holds_both_versions']==262
    assert all(all(r['review'].values()) for r in doc['records']+names['records'])
    assert plan['measured_default_macro_lengths']==dict(FI=6,FA=9,FO=15) and plan['source_macro_totals']==dict(FI=0,FA=0,FO=0)
    image=NdsImage.open(doc['current_ROM']);assert sha(Path(doc['current_ROM']).read_bytes())==doc['current_ROM_sha256']
    assert sha(image.read_file('/__arm9__.bin'))=='12ebaf3f3ce558e731c4c972ae90696392a351426cf147fbf3bd830dd1d82d1b'
    dependencies={Path(p) for p in prior_contract()['dependencies']}
    dependencies|={DOC,NAMES,PLAN,RELOC,APPROVAL,Path(__file__),Path('scripts/plan_Hodram_B137_B45_B46_v8245.py')}
    checkpoint=read('work/analysis/Hodram_display_checkpoint_v8285b/staged_checkpoint.json')
    ledger_pending=read('translations/editorial_review_current_v1.json')['Hodram28_stored_names_actual_display_approved_pending_frozen_policy_atomic_registered_v8285b']
    for p in ledger_pending['all_proofs'].values():dependencies.add(Path(p))
    for s in approval['all12_actual_review_sheets']:assert sha(Path(s['path']).read_bytes())==s['sha256'];dependencies.add(Path(s['path']))
    stored=read(ledger_pending['all_proofs']['stored']);native_names=read(ledger_pending['all_proofs']['names_native'])
    source_models=read(ledger_pending['all_proofs']['models'])
    for rows in source_models['native_models'].values():
        for row in rows:
            for page in row['pages']:dependencies.add(Path(page['native_plane']));assert sha(Path(page['native_plane']).read_bytes())==page['native_plane_sha256']
    for name in native_names['name_planes']:dependencies.add(Path(name['native_plane']));assert sha(Path(name['native_plane']).read_bytes())==name['native_plane_sha256']
    bindings={};infos=0;warnings=0
    for row,p in zip(doc['records'],plan['records'],strict=True):
        assert row['id']==p['id'] and row['logical_English']==row['english']==p['logical_English']
        assert row['planned_English_markup']==p['planning_record']['english'] and row['compiled_hex']==p['encoded_hex']
        assert p['expected_native_pages']==1 and p['max_total_rows']==4 and not any(i['severity']=='error' for i in p['base_QA']['issues'])
        issues=[i for i in p['base_QA']['issues'] if i['severity']=='warning'];warnings+=len(issues)
        if row['qa_waivers']:
            assert row['qa_waivers']==['weak-line-ending'] and row['qa_waiver_reason'] and issues==[row['qa_waiver_scope']['exact_issue']]
            scope=row['qa_waiver_scope'];assert scope['id']==row['id'] and scope['source_hex']==row['source_hex'] and scope['compiled_hex']==row['compiled_hex']
            assert scope['logical_English']==row['logical_English']
        else:assert not issues and not row['qa_waiver_scope']
        info=any(i['code']=='line-break-count' for i in p['base_QA']['issues']);infos+=info
        group=next(g for g in reloc['groups'] if g['block']==row['block'])
        bindings[row['id']]=dict(file_path=row['file_path'],route=1,route_identity='Hodram',block=row['block'],
            source_block_hashes=[group['clean_block_sha256'],group['source_block_sha256']],
            source_reference=row['source_reference'],current_reference=row['current_reference'],source_complete_preamble_hex=row['source_complete_preamble_hex'],
            compiler_source_hex=row['source_hex'],predecessor_record_hex=row['current_hex'],source_selector=row['source_selector'],source_kind=row['kind'],consumer='progressive',
            planning_record={k:p['planning_record'][k] for k in ['id','english','kind','source_hex','source_selector']},compiled_hex=p['encoded_hex'],lines=p['lines'],maximum_total_rows=4,native_page_count=1,
            row_count_reason='Use full native width for the complete reviewed paragraph; its changed row count preserves all words on one native page.' if info else None,
            ordinary_wrap_reasons=[row['localization_note'],row['qa_waiver_reason']] if row['qa_waivers'] else [row['localization_note']],
            base_QA_issues=p['base_QA']['issues'],qa_waivers=row['qa_waivers'],qa_waiver_reason=row['qa_waiver_reason'],qa_waiver_scope=row['qa_waiver_scope'],approved_fields=deepcopy(row))
    assert infos==5 and warnings==2 and {b['source_selector'] for b in bindings.values()}=={1,2,9,16,18,113}
    template=Path('dk4tool/dialogue/rafael_B50_profile_v1.py').read_text(encoding='utf8')
    metrics=template.split('metrics_source="',1)[1].split('")',1)[0]
    profile=checked_text(template,{
        'translations/rafael_B50_native_contract_v1.json':CONTRACT.as_posix(),
        '1a8751c931336a73ddea449bd671eaafb1291e2d4b75d4be9a46d0b912e44872':'CONTRACT_DIGEST',
        '2b6aaaa499d634be9afc255d1c39b64ef0f578283c9768c525b31e34499abd0a':'12ebaf3f3ce558e731c4c972ae90696392a351426cf147fbf3bd830dd1d82d1b',
        'Rafael B50':'Hodram B137/B45/B46','Rafael-B50':'Hodram-three-blocks','B50':'Hodram-three-blocks',
        '{"FI":6,"FA":6,"FO":10}':'{"FI":6,"FA":9,"FO":15}',
        '{"FI":1,"FA":2,"FO":0}':'{"FI":0,"FA":0,"FO":0}',
        'raphael-story-live':'hodram-story-live','base.macro_ascii_lengths["FI"]!=7':'base.macro_ascii_lengths!={"FI":6,"FA":9,"FO":15}',
        '{"FI":36,"FA":36,"FO":60,"I":12}':'{"FI":36,"FA":54,"FO":90,"I":12}',
        'else {0,2,9}':'else {1,2,9,16,18,113}',
        'Original global Rafael profile required':'Original global Hodram profile required',
        'Exact measured Rafael macros required':'Exact measured Hodram macros required',
        'and2b6 runtime':'and12eb runtime',
        metrics:'Exact registered V8259 Hodram captain1:216px/four rows,28single native pages;source01/02/09/10/12/71 with complete sixbyte preambles. Default FI6/FA9/FO15,zero source macros. Three source ellipsis records retained. Full compiled/stored andactual body/name masks,all28source/revised passages andsix names in disclosed whole-script fixtures,original4800/layout0/4700 andnormalvaluecarry verified. Two exact weak-boundary exceptions andfive infos retained. B137 laterfixture captain0/SC0B44 isnot normal Hodram continuity;all measured timing/RNG/UI/component/calendar/RGB limits remain. No global font/profile/guard changes,allattainable effect-path,fullroute orhardware claim.',
    })
    layout=checked_text(Path('dk4tool/dialogue/rafael_B50_layout_v1.py').read_text(encoding='utf8'),{
        'rafael_B50':'hodram_three_blocks','Rafael-B50':'Hodram-three-blocks','B50':'Hodram-three-blocks',
    })
    planner=checked_text(Path('dk4tool/dialogue/rafael_B50_plan_v1.py').read_text(encoding='utf8'),{
        'plan_Rafael_B50_layout_v8140b':'plan_Hodram_B137_B45_B46_v8245',
        'work/analysis/Rafael_B50_layout_v8140b/28_automatic_plans_full_native_width_exact_source00_02_09_FA2_FI1.json':PLAN.as_posix(),
        '726e32b6b4196c1a9c8bf2fc8774f8c38861a5a04002ef11feea6d8ba6b2650d':sha(PLAN.read_bytes()),
        'B50 planner;00 preamble separate from guarded NUL-free text':'Hodram planner;complete source preamble separate from guarded NUL-free body',
    })
    for path,code in [(PROFILE,profile.replace('CONTRACT_DIGEST','0'*64)),(FORMATTER,layout),(PLANNER,planner)]:compile(code,str(path),'exec')
    for path,code in [(FORMATTER,layout),(PLANNER,planner)]:path.write_text(code,encoding='utf8');dependencies.add(path)
    runtime={p:sha(image.read_file(p)) for p in ['/__arm9__.bin','/COMMON/MESFILE.DK4','/GRP/KANJI.FNT','/data/EV1.DK4']}
    save(CONTRACT,dict(format='Hodram-three-blocks-source-native-contract-v1',record_bindings=bindings,choice_bindings={},review_gates=doc['review_gates'],
        batch_binding={k:doc[k] for k in ['translation_policy','target_locale','encoder','review_gates','file_path','route','route_identity','blocks']},
        runtime_component_hashes=runtime,measured_macro_ascii_lengths=dict(FI=6,FA=9,FO=15),source_macro_counts=dict(FI=0,FA=0,FO=0),
        physical_native_rows_per_page=4,physical_progressive_viewport=[216,64],usable_text_width_px=216,complete_native_pages=28,
        source_bound_ellipsis_records=plan['source_bound_three_ellipsis_records'],name_review_binding=names,
        explicit_registered_Gerhard_dependency=dict(candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],ARM9_sha256=runtime['/__arm9__.bin'],
            correction='translations/gerhard_surname_editorial_release_v2.json',correction_sha256=sha(Path('translations/gerhard_surname_editorial_release_v2.json').read_bytes())),
        dependencies={str(p):sha(p.read_bytes()) for p in sorted(dependencies)},individual_row_count_infos=5,exact_warning_exception_count=2,
        all28_source_context_native_stored_actual_checks_bound=True,all60commands8relatives_andoriginal4800_layout0_hide4700_valuecarry_bound=True,
        all_measured_fixture_scope_andtiming_RNG_component_RGB_limits_retained=True,
        frozen_policy_validation_independent_atomic_registered_release_pending=True,new_credit=0,full_goal_complete=False))
    PROFILE.write_text(profile.replace('CONTRACT_DIGEST',sha(CONTRACT.read_bytes())),encoding='utf8')
    ROOT.mkdir(parents=True);save(ROOT/'frozen28_paragraphs_three_silences_six_names_five_infos_two_warnings.json',dict(contract=str(CONTRACT),contract_sha256=sha(CONTRACT.read_bytes()),
        modules={str(p):sha(p.read_bytes()) for p in [PROFILE,FORMATTER,PLANNER]},records=28,single_pages=28,source_silences=3,scoped_names=6,
        source_default_macro_lengths=dict(FI=6,FA=9,FO=15),source_macro_counts=dict(FI=0,FA=0,FO=0),
        all_original_diagnostics_retained_five_infos_two_exact_waivers=True,dependency_count=len(dependencies),
        native_policy_derivation_source_files={str(p):sha(p.read_bytes()) for p in [Path('dk4tool/dialogue/rafael_B50_profile_v1.py'),Path('dk4tool/dialogue/rafael_B50_layout_v1.py'),Path('dk4tool/dialogue/rafael_B50_plan_v1.py')]},
        policy_challenges_independent_atomic_registered_release_pending=True,new_credit=0,full_goal_complete=False))
    print('Frozen Hodram28:three source silences/six names/zero macros/five infos/two narrow warnings. Policy challenges andatomic release pending.')
