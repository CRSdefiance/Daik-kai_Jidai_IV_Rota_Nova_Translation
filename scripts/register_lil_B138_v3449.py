"""Register44 guarded reviews after the complete V3416 cumulative stack."""
import os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import lil_B138_editorial_v1 as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B138_registration_v3449')
PROFILE='all-routes-unified-v3450'
PARENT=Path('out/all_routes_combined_v3416_candidate.nds')
DOC=Path('translations/lil_B138_editorial_manuscript_v8.json')
MENU=None
MAP=Path('translations/lil_B138_editorial_relocation_map_v2.json')
if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists()
    rp,builder=Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py');raw,before=rp.read_bytes(),builder.read_bytes();registry=read(rp)
    assert PROFILE not in registry['profiles'] and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
    parent=NdsImage.open(PARENT);base=NdsImage.open('out/raphael_natural_v2_accepted_base.nds');doc,mapping=map(read,[DOC,MAP]);assert sha(PARENT.read_bytes())==doc['current_ROM_sha256']
    deps={str(DOC),str(MAP),str(Path(owned.__file__)),__file__,'dk4tool/dialogue/lil_B138_profile.py','dk4tool/dialogue/lil_B138_layout_v2.py','dk4tool/dialogue/layout.py','dk4tool/dialogue/encoder.py','dk4tool/dialogue/qa.py','dk4tool/dialogue/review.py','docs/editorial_testing_scope_v1870.md','work/analysis/lil_B138_reference_approval_v3446c/approval_receipt.json','work/analysis/lil_B138_loader_v3443b/whole_SC2_and_one_selected_block_initial_entry_proof.json','work/analysis/editorial_handoff_verification_v3448b/verified_handoff.json'}
    deps.update(doc[k] for k in ['source_context','control_contract','branch_proof','whole_exchange_context_notes','native_font_proof','representative_proof','historical_representative_sheet_review','prior_current_sheet_review','final_padding_proof','relocated_control_proof','item_terminology_reconciliation','actor_voice_contract','effective_current_comparison','native_progressive_proof'])
    deps.update(mapping[k] for k in ['source_plan','source_census'])
    deps.update(['scripts/research_lil_B138_relocation_v3441.py', 'scripts/prepare_lil_B138_research_v3442b.py', 'scripts/verify_lil_B138_loader_v3443b.py', 'scripts/verify_lil_B138_references_v3444b.py', 'scripts/prove_lil_B138_relocated_controls_v3445b.py', 'scripts/seal_lil_B138_references_v3446.py', 'scripts/correct_lil_B138_reference_metadata_v3448c.py', 'scripts/verify_editorial_handoff_v3448b.py', 'scripts/verify_lil_B138_fonts_v3437.py', 'scripts/approve_lil_B138_native_v3438.py', 'scripts/author_lil_B138_v3432.py', 'scripts/lil_B138_dignity_prose_v3432.py', 'scripts/read_lil_B138_clean_context_v3428.py', 'scripts/reconcile_lil_B138_terms_v3429.py', 'scripts/refine_lil_B138_company_complaint_v3434.py', 'scripts/refine_lil_B138_phrase_flow_v3436.py', 'scripts/prove_lil_B138_conditional_contract_v3426d.py', 'scripts/prove_lil_B138_controls_v3426e.py', 'scripts/prove_lil_crew_items_controls_v3114.py'])
    for path in list(deps):
        if Path(path).suffix=='.json':
            item=read(path)
            for key in ['evidence','hashes']:
                if isinstance(item.get(key),dict):deps.update(p for p in item[key] if Path(p).is_file())
    font=read(doc['native_font_proof']);deps.update(s['path'] for s in font['review_sheets']);deps.update(c['preview'] for c in font['cases'])
    for p in [doc['historical_representative_sheet_review'],doc['prior_current_sheet_review']]:deps.add(read(p)['sheet'])
    conf=dict(format='dk4-lil-B138-editorial-release-v1',manuscript=str(DOC),choices=None,reference_map=str(MAP),required_runtime_arm9_sha256=sha(parent.read_file('/__arm9__.bin')),source_SC2_sha256=mapping['source_SC2_sha256'],target_SC2_sha256=mapping['target_SC2_sha256'],canonical_SC2_sha256=mapping['canonical_SC2_sha256'],clean_SC2_sha256=mapping['clean_SC2_sha256'],clean_ROM='work/clean.nds',clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),dependencies={p:sha(Path(p).read_bytes()) for p in sorted(deps)})
    ROOT.mkdir(parents=True);positive=ROOT/'positive_config.json';save(positive,conf)
    test=NdsImage.open(PARENT);proof=owned.apply_release(test,base,positive)
    assert test.read_file(owned.PATH)==Path('work/analysis/lil_B138_relocation_v3441/SC2_RESEARCH_ONLY.DK4').read_bytes() and test.read_file('/__arm9__.bin')==parent.read_file('/__arm9__.bin') and len(proof['changed_records'])==44
    save(ROOT/'positive_reconstruction.json',proof);negatives=[]
    def reject(label,image,baseline,config):
        initial=(image.read_file(owned.PATH),image.read_file('/__arm9__.bin'))
        try:owned.apply_release(image,baseline,config)
        except (AssertionError,ValueError) as error:
            assert (image.read_file(owned.PATH),image.read_file('/__arm9__.bin'))==initial;negatives.append(dict(case=label,rejected_before_mutation=True,error=str(error)))
        else:raise AssertionError(label)
    reject('repeated_application',test,base,positive)
    for label,path in [('wrong_SC2',owned.PATH),('wrong_ARM9','/__arm9__.bin')]:
        im=NdsImage.open(PARENT);data=bytearray(im.read_file(path));data[256]^=1;im.replace_file(path,bytes(data));reject(label,im,base,positive)
    badbase=NdsImage.open('out/raphael_natural_v2_accepted_base.nds');data=bytearray(badbase.read_file(owned.PATH));data[32]^=1;badbase.replace_file(owned.PATH,bytes(data));reject('wrong_canonical',NdsImage.open(PARENT),badbase,positive)
    def named(d):return next(r for r in d['records'] if '{MACRO:FO}' in r['english'])
    CONTROL=Path(doc['relocated_control_proof'])
    def ian(d):return next(r for r in d['records'] if r['source_selector']==21)
    def question(d):return next(r for r in d['records'] if r['id']=='DK4_MES_B138_R0078')
    def raw2(d):return next(p for p in d['relocated_predicate_pairs'] if p['cases'][0]['source_command_hex']=='0080ffff200301a1')
    changes=[
      ('missing_format_review',DOC,'manuscript',lambda d:d['records'][0]['review'].update(formatting=False)),
      ('wrong_Japanese_source',DOC,'manuscript',lambda d:d['records'][0].update(source_hex='00')),
      ('wrong_current_body',DOC,'manuscript',lambda d:d['records'][0].update(current_hex='00')),
      ('wrong_consumer',DOC,'manuscript',lambda d:d['records'][0].update(native_display_consumer='original_FE_modal_5473C_mode1')),
      ('missing_actor_state',DOC,'manuscript',lambda d:d['records'][0].update(english=d['records'][0]['english'].split('}',1)[1])),
      ('wrong_actor_state',DOC,'manuscript',lambda d:d['records'][0].update(english=d['records'][0]['english'].replace('SPEAKER:02','SPEAKER:0E'))),
      ('invented_macro',DOC,'manuscript',lambda d:d['records'][0].update(english=d['records'][0]['english']+' {MACRO:FI}')),
      ('changed_approved_prose',DOC,'manuscript',lambda d:d['records'][0].update(english=d['records'][0]['english']+' Fine.')),
      ('missing_source_FO',DOC,'manuscript',lambda d:named(d).update(english=named(d)['english'].replace('{MACRO:FO}','Argot Co.'))),
      ('wrong_complete_preamble',DOC,'manuscript',lambda d:d['records'][0].update(source_complete_preamble_hex='0040ffff000e')),
      ('wrong_formatter',DOC,'manuscript',lambda d:d.update(native_formatter_module='dk4tool/dialogue/encoder.py')),
      ('missing_speech',DOC,'manuscript',lambda d:d['records'].pop()),
      ('source00_outside_scope',DOC,'manuscript',lambda d:d['records'][0].update(source_selector=0)),
      ('manual_layout',DOC,'manuscript',lambda d:d['records'][0].update(english=d['records'][0]['english']+'{LB}')),
      ('embedded_NUL',DOC,'manuscript',lambda d:d['records'][0].update(english=d['records'][0]['english']+'{HEX:00}')),
      ('missing_reference_approval',MAP,'reference_map',lambda d:d.update(external_references_complete=False)),
      ('wrong_mapped_command',MAP,'reference_map',lambda d:d['blocks'][0]['mapped_native_commands'][0].update(new_offset=10)),
      ('wrong_relative_target',MAP,'reference_map',lambda d:d['blocks'][0]['relative_skip_fixups'][0].update(new_matched_skip_target=0)),
      ('missing_predicate_gate',MAP,'reference_map',lambda d:d.update(all10_predicates_and1_query_current_relocated_results_and_source_operands_equal=False)),
      ('false_speech_scope',MAP,'reference_map',lambda d:d.update(all44_active_speech_targets_preserved=False)),
      ('false_source_kind_scope',MAP,'reference_map',lambda d:d.update(no_FE_source00_2100_2000_dynamic_or4100_objects=False)),
      ('invented_query',MAP,'reference_map',lambda d:d.update(original_event_queries=[dict(event=1)])),
      ('wrong_entry',MAP,'reference_map',lambda d:d.update(entry_point_offset=12)),
      ('wrong_target_hash',MAP,'reference_map',lambda d:d.update(target_SC2_sha256='0'*64)),
    ]
    changes.extend([
      ('missing_original_query',MAP,'reference_map',lambda d:d.update(original_event_queries=[])),
      ('changed_query_operand',MAP,'reference_map',lambda d:d['original_event_queries'][0].update(source_command_hex='00818a00')),
      ('lost_static_Ian21',DOC,'manuscript',lambda d:ian(d).update(source_selector=20)),
      ('changed_wordless_question',DOC,'manuscript',lambda d:question(d).update(english='{SPEAKER:02}!')),
      ('changed_raw_result2',CONTROL,'relocated_control_proof',lambda d:[p['native_result'].__setitem__(1,1) for p in raw2(d)['cases']]),
      ('missing_portable_predicate_constants',CONTROL,'relocated_control_proof',lambda d:d['portable_source_owned_adapters'].update(predicate='def predicate(): pass')),
      ('wrong_source_result_constant',CONTROL,'relocated_control_proof',lambda d:d['source_predicate_result_constants'].update({'0080ffff200301a1':1})),
    ])
    for label,path,key,mutate in changes:
        value=read(path);mutate(value);mp=ROOT/(label+'.json');save(mp,value);cfg=deepcopy(conf);cfg[key]=str(mp);cfg['dependencies'][str(mp)]=sha(mp.read_bytes())
        if key=='reference_map':
            for doc_key,original_path in [('manuscript',DOC)]:
                d=read(original_path);d.update(reference_map=str(mp),reference_map_sha256=sha(mp.read_bytes()));p2=ROOT/(label+'_'+doc_key+'.json');save(p2,d);cfg[doc_key]=str(p2);cfg['dependencies'][str(p2)]=sha(p2.read_bytes())
        if key=='relocated_control_proof':
            d=read(DOC);d.update(relocated_control_proof=str(mp),relocated_control_proof_sha256=sha(mp.read_bytes()));p2=ROOT/(label+'_manuscript.json');save(p2,d);cfg['manuscript']=str(p2);cfg['dependencies'][str(p2)]=sha(p2.read_bytes())
        cp=ROOT/(label+'_config.json');save(cp,cfg);reject(label,NdsImage.open(PARENT),base,cp)
    assert len(changes)==31 and len(negatives)==35
    save(ROOT/'negative_cases.json',dict(cases=negatives,all_rejected_before_mutation=True))
    stage=b'''    lil_more = profile_config.get('lil_B138_editorial')
    if lil_more:
        from dk4tool.patch.lil_B138_editorial_v1 import apply_release as apply_lil_more

        lil_more_report = apply_lil_more(candidate, baseline, lil_more)
        grouped.setdefault('/data/SC2.DK4', [])
        changed_records.setdefault('/data/SC2.DK4', []).extend(row['id'] for row in lil_more_report['changed_records'])
        relocation_checks.setdefault('/data/SC2.DK4', {})['lil_B138_editorial'] = {
            'release_config': lil_more,
            'release_config_sha256': sha256(Path(lil_more).read_bytes()),
            'proof': lil_more_report}
        for more_key in ('manuscript',):
            more_batch = Path(lil_more_report[more_key])
            if more_batch in release_batches:
                raise ValueError('B138 must run once after the complete V3416 stack')
            release_batches.append(more_batch)

'''
    anchor=b'    # Lexically valid "% o"';assert before.count(anchor)==1 and b"profile_config.get('lil_B138_editorial')" not in before
    after=before.replace(anchor,stage+anchor);compile(after,str(builder),'exec')
    import ast
    imports=[n.module for n in ast.walk(ast.parse('if True:\n'+stage.decode('utf-8'))) if isinstance(n,ast.ImportFrom)]
    assert imports==[owned.__name__],(imports,owned.__name__)
    assert stage.count(owned.__name__.encode())==1
    (ROOT/'registry_before_raw.json').write_bytes(raw);(ROOT/'builder_before.py').write_bytes(before);(ROOT/'builder_added_optional_stage.bin').write_bytes(stage)
    save(owned.CONFIG,conf);profile=deepcopy(registry['profiles']['all-routes-unified-v3416'])
    profile.update(lil_B138_editorial=owned.CONFIG,description='Complete V3416 cumulative stack plus44 contextual B138 reviews.',note='16 revisions/28 justified retentions;44 progressive speeches,seven static actors/FO1,ten raw predicates/one query137,111 commands/45 spans/225 skips.44 planes/352 logical-compiled/176 final macro cases,six viewed/hash-exact sheets,21 narrow row-count notes. Source raw result2,wordless questions and map/leaf descriptions preserved.35 compiler rejection tests before mutation. Registered build/exact clean patch/fresh startup pending. Experimental;no promotion;preserve every ROM/translation.')
    registry['profiles'][PROFILE]=profile;assert rp.read_bytes()==raw and builder.read_bytes()==before
    pending=rp.with_name('release_stack_v3449_pending.json');assert not pending.exists();save(pending,registry);builder.write_bytes(after);os.replace(pending,rp)
    restored=deepcopy(read(rp));restored['profiles'].pop(PROFILE);assert restored==read(ROOT/'registry_before_raw.json') and builder.read_bytes().replace(stage,b'',1)==before
    save(ROOT/'registration_receipt.json',dict(profile=PROFILE,parent_profile='all-routes-unified-v3416',config=owned.CONFIG,config_sha256=sha(Path(owned.CONFIG).read_bytes()),negative_cases=35,stage_key='lil_B138_editorial',compiler=str(Path(owned.__file__)),compiler_sha256=sha(Path(owned.__file__).read_bytes()),stage_import_module=owned.__name__,all114accepted_layers_previous_profiles_and_V1492_promotion_unchanged=True,only_one_optional_stage_and_one_experimental_profile_added=True,release_stack_sha256=sha(rp.read_bytes()),builder_sha256=sha(builder.read_bytes()),no_ROM_created_or_promoted=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Registered V3450 B138 stage;35 compiler negatives reject before mutation. Exact hook imports the positively reconstructed compiler. Full V3416/114 accepted layers/V1492 preserved.')
