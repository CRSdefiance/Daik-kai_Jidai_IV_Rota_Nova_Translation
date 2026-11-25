"""Register159 guarded reviews after the complete V3251 cumulative stack."""
import os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import lil_B122_B127_editorial_v2 as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B122_B127_registration_v3299b')
PROFILE='all-routes-unified-v3300'
PARENT=Path('out/all_routes_combined_v3251_candidate.nds')
DOC=Path('translations/lil_B122_B127_editorial_manuscript_v6.json')
MENU=Path('translations/lil_B122_B127_choice_manuscript_v5.json')
MAP=Path('translations/lil_B122_B127_editorial_relocation_map_v1.json')
if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists()
    rp,builder=Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py');raw,before=rp.read_bytes(),builder.read_bytes();registry=read(rp)
    assert PROFILE not in registry['profiles'] and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
    parent=NdsImage.open(PARENT);base=NdsImage.open('out/raphael_natural_v2_accepted_base.nds');doc,mapping=map(read,[DOC,MAP]);assert sha(PARENT.read_bytes())==doc['current_ROM_sha256']
    deps={str(DOC),str(MENU),str(MAP),str(Path(owned.__file__)),__file__,'dk4tool/dialogue/lil_B122_B127_profile_v2.py','dk4tool/dialogue/lil_B122_B127_layout_v2.py','dk4tool/dialogue/layout.py','dk4tool/dialogue/encoder.py','dk4tool/dialogue/qa.py','dk4tool/dialogue/review.py','docs/editorial_testing_scope_v1870.md','work/analysis/lil_B122_B127_reference_approval_v3295/approval_receipt.json','work/analysis/lil_B122_B127_loader_v3290/whole_SC2_and_six_selected_blocks_initial_entry_proof.json','work/analysis/editorial_handoff_verification_v3297/verified_handoff.json'}
    deps.update(doc[k] for k in ['source_context','control_contract','branch_proof','whole_exchange_context_notes','native_font_proof','representative_proof','historical_representative_sheet_review','prior_current_sheet_review','final_padding_proof','relocated_control_proof','item_terminology_reconciliation','actor_voice_contract','effective_current_comparison','original2000_wait_proof','conditional_return_proof','native_progressive_proof','native_FE_proof','native_choice_proof'])
    deps.update(mapping[k] for k in ['source_plan','source_census'])
    for p in ['scripts/research_lil_B122_B127_relocation_v3288b.py','scripts/prepare_lil_B122_B127_research_v3289b.py','scripts/verify_lil_B122_B127_loader_v3290.py','scripts/verify_lil_B122_B127_references_v3291.py','scripts/prove_lil_B122_B127_relocated_controls_v3292.py','scripts/prove_lil_trade_branch_return_v3293.py','scripts/reconcile_lil_B122_B127_sampling_v3294.py','scripts/seal_lil_B122_B127_references_v3295.py','scripts/verify_lil_B122_B127_fonts_v3283.py','scripts/verify_lil_B122_B127_FE_v3284.py','scripts/prove_lil_B122_B127_choices_v3279.py','scripts/approve_lil_B122_B127_native_v3285.py','scripts/author_lil_B122_B127_v3272.py','scripts/lil_Clifford_Christina_taverns_prose_v3269.py','scripts/lil_moral_doubts_Guiding_Staff_prose_v3270.py','scripts/lil_trade_lesson_Fernando_cards_prose_v3271a.py','scripts/refine_lil_three_native_wraps_v3274c.py','scripts/lil_kuhn_china_FE_painter_v2909.py']:deps.add(p)
    for path in list(deps):
        if Path(path).suffix=='.json':
            item=read(path)
            for key in ['evidence','hashes']:
                if isinstance(item.get(key),dict):deps.update(p for p in item[key] if Path(p).is_file())
    font=read(doc['native_font_proof']);deps.update(s['path'] for s in font['review_sheets']);deps.update(c['preview'] for c in font['cases'])
    for p in [doc['historical_representative_sheet_review'],doc['prior_current_sheet_review']]:deps.add(read(p)['sheet'])
    for p in read(doc['native_FE_proof'])['cases']:deps.update([p['native_plane'],p['preview']])
    conf=dict(format='dk4-lil-B122-B127-editorial-release-v1',manuscript=str(DOC),choices=str(MENU),reference_map=str(MAP),required_runtime_arm9_sha256=sha(parent.read_file('/__arm9__.bin')),source_SC2_sha256=mapping['source_SC2_sha256'],target_SC2_sha256=mapping['target_SC2_sha256'],canonical_SC2_sha256=mapping['canonical_SC2_sha256'],clean_SC2_sha256=mapping['clean_SC2_sha256'],clean_ROM='work/clean.nds',clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),dependencies={p:sha(Path(p).read_bytes()) for p in sorted(deps)})
    ROOT.mkdir(parents=True);positive=ROOT/'positive_config.json';save(positive,conf)
    test=NdsImage.open(PARENT);proof=owned.apply_release(test,base,positive)
    assert test.read_file(owned.PATH)==Path('work/analysis/lil_B122_B127_relocation_v3288b/SC2_RESEARCH_ONLY.DK4').read_bytes() and test.read_file('/__arm9__.bin')==parent.read_file('/__arm9__.bin') and len(proof['changed_records'])==159
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
    def modal(d):return next(r for r in d['records'] if r['kind']=='system-FE')
    def named(d):return next(r for r in d['records'] if '{MACRO:FI}' in r['english'])
    def b126(d):return next(b for b in d['blocks'] if b['block']==126)
    def pause(d):return d['blocks'][0]['original2000_pause_and_resume_maps'][0]
    def choice(d):return next(c for b in d['blocks'] for c in b['choice_commands'])
    changes=[
      ('missing_format_review',DOC,'manuscript',lambda d:d['records'][0]['review'].update(formatting=False)),
      ('wrong_Japanese_source',DOC,'manuscript',lambda d:d['records'][0].update(source_hex='00')),
      ('wrong_consumer',DOC,'manuscript',lambda d:d['records'][0].update(native_display_consumer='original_FE_modal_5473C_mode1')),
      ('missing_actor_state',DOC,'manuscript',lambda d:d['records'][0].update(english=d['records'][0]['english'].split('}',1)[1])),
      ('wrong_actor_state',DOC,'manuscript',lambda d:d['records'][0].update(english=d['records'][0]['english'].replace('SPEAKER:97','SPEAKER:02'))),
      ('invented_macro',DOC,'manuscript',lambda d:d['records'][0].update(english=d['records'][0]['english']+' {MACRO:FI}')),
      ('changed_approved_prose',DOC,'manuscript',lambda d:d['records'][0].update(english=d['records'][0]['english']+' Fine.')),
      ('missing_source_FI',DOC,'manuscript',lambda d:named(d).update(english=named(d)['english'].replace('{MACRO:FI}','Lil'))),
      ('wrong_complete_preamble',DOC,'manuscript',lambda d:d['records'][0].update(source_complete_preamble_hex='0040ffff005c')),
      ('wrong_formatter',DOC,'manuscript',lambda d:d.update(native_formatter_module='dk4tool/dialogue/encoder.py')),
      ('missing_speech',DOC,'manuscript',lambda d:d['records'].pop()),
      ('FE_wrong_consumer',DOC,'manuscript',lambda d:modal(d).update(native_display_consumer='original_progressive_54020')),
      ('FE_converted_selector',DOC,'manuscript',lambda d:modal(d).update(source_hex='f8f2'+modal(d)['source_hex'][2:])),
      ('FE_invented_macro',DOC,'manuscript',lambda d:modal(d).update(english=modal(d)['english']+' {MACRO:FI}')),
      ('FE_invented_label',DOC,'manuscript',lambda d:modal(d).update(english=modal(d)['english'].replace('}','}Clifford: ',1))),
      ('choice_missing_format_review',MENU,'choices',lambda d:d['records'][0]['review'].update(formatting=False)),
      ('choice_missing_label',MENU,'choices',lambda d:d['records'].pop()),
      ('choice_duplicate_index',MENU,'choices',lambda d:d['records'][0].update(option_index=1)),
      ('choice_changed_prose',MENU,'choices',lambda d:d['records'][0].update(english='Yes.')),
      ('choice_manual_layout',MENU,'choices',lambda d:d['records'][0].update(english=d['records'][0]['english']+'{LB}')),
      ('choice_wrong_source',MENU,'choices',lambda d:d['records'][0].update(source_hex='00')),
      ('choice_wrong_current_reference',MENU,'choices',lambda d:d['records'][0]['current_reference'].update(offset=0)),
      ('choice_wrong_compiled',MENU,'choices',lambda d:d['records'][0].update(compiled_hex='41')),
      ('choice_wrong_whole_object',MENU,'choices',lambda d:d['records'][0].update(typed_target_object_hex='0021')),
      ('missing_reference_approval',MAP,'reference_map',lambda d:d.update(external_references_complete=False)),
      ('wrong_mapped_command',MAP,'reference_map',lambda d:d['blocks'][0]['mapped_native_commands'][0].update(new_offset=10)),
      ('wrong_relative_target',MAP,'reference_map',lambda d:d['blocks'][0]['relative_skip_fixups'][0].update(new_matched_skip_target=0)),
      ('missing_predicate_gate',MAP,'reference_map',lambda d:d.update(all14_relocated_predicate_pairs_preserve_source_operands_results_and_unowned_RAM=False)),
      ('false_speech_scope',MAP,'reference_map',lambda d:d.update(all155_active_speech_targets_preserved=False)),
      ('missing_menu_gate',MAP,'reference_map',lambda d:d.update(two2100_objects_four_labels_and_source_indices_0_1_cancel_verified=False)),
      ('missing_pause_gate',MAP,'reference_map',lambda d:d.update(two_original2000_pause_words_and_mapped_resume_boundaries_verified=False)),
      ('missing_return_gate',MAP,'reference_map',lambda d:d.update(trade_choice0_tutorial_choice1_already_know_branch_and_return0_both_VM_modes_verified=False)),
      ('unexpected_dynamic_scope',MAP,'reference_map',lambda d:d.update(no_dynamic_selector_or4100_objects=False)),
      ('invented_query',MAP,'reference_map',lambda d:d.update(original_event_queries=[dict(event=1)])),
      ('pause_deleted',MAP,'reference_map',lambda d:d['blocks'][0]['original2000_pause_and_resume_maps'].pop()),
      ('pause_old_offset_changed',MAP,'reference_map',lambda d:pause(d).update(old_offset=0)),
      ('pause_new_offset_changed',MAP,'reference_map',lambda d:pause(d).update(new_offset=0)),
      ('pause_resume_changed',MAP,'reference_map',lambda d:pause(d).update(target_resume=0)),
      ('pause_source_resume_changed',MAP,'reference_map',lambda d:pause(d).update(source_resume=0)),
      ('menu_wrong_label_reference',MAP,'reference_map',lambda d:choice(d)['label_references'][0].update(new_offset=0)),
      ('menu_wrong_whole_opcode',MAP,'reference_map',lambda d:choice(d).update(target_hex='0022'+choice(d)['target_hex'][4:])),
      ('menu_reference_index_changed',MAP,'reference_map',lambda d:choice(d)['label_references'][0].update(option_index=1)),
      ('menu_deleted',MAP,'reference_map',lambda d:next(b for b in d['blocks'] if b['choice_commands'])['choice_commands'].clear()),
      ('return_mapped_extent_changed',MAP,'reference_map',lambda d:next(c for c in b126(d)['mapped_native_commands'] if c['old_offset']==336).update(new_native_extent=2)),
      ('wrong_entry',MAP,'reference_map',lambda d:d.update(entry_point_offset=12)),
      ('wrong_target_hash',MAP,'reference_map',lambda d:d.update(target_SC2_sha256='0'*64)),
    ]
    for label,path,key,mutate in changes:
        value=read(path);mutate(value);mp=ROOT/(label+'.json');save(mp,value);cfg=deepcopy(conf);cfg[key]=str(mp);cfg['dependencies'][str(mp)]=sha(mp.read_bytes())
        if key=='reference_map':
            for doc_key,original_path in [('manuscript',DOC),('choices',MENU)]:
                d=read(original_path);d.update(reference_map=str(mp),reference_map_sha256=sha(mp.read_bytes()));p2=ROOT/(label+'_'+doc_key+'.json');save(p2,d);cfg[doc_key]=str(p2);cfg['dependencies'][str(p2)]=sha(p2.read_bytes())
        cp=ROOT/(label+'_config.json');save(cp,cfg);reject(label,NdsImage.open(PARENT),base,cp)
    assert len(changes)==46 and len(negatives)==50
    save(ROOT/'negative_cases.json',dict(cases=negatives,all_rejected_before_mutation=True))
    stage=b'''    lil_more = profile_config.get('lil_B122_B127_editorial')
    if lil_more:
        from dk4tool.patch.lil_B122_B127_editorial_v2 import apply_release as apply_lil_more

        lil_more_report = apply_lil_more(candidate, baseline, lil_more)
        grouped.setdefault('/data/SC2.DK4', [])
        changed_records.setdefault('/data/SC2.DK4', []).extend(row['id'] for row in lil_more_report['changed_records'])
        relocation_checks.setdefault('/data/SC2.DK4', {})['lil_B122_B127_editorial'] = {
            'release_config': lil_more,
            'release_config_sha256': sha256(Path(lil_more).read_bytes()),
            'proof': lil_more_report}
        for more_key in ('manuscript', 'choices'):
            more_batch = Path(lil_more_report[more_key])
            if more_batch in release_batches:
                raise ValueError('B122-B127 must run once after the complete V3251 stack')
            release_batches.append(more_batch)

'''
    anchor=b'    # Lexically valid "% o"';assert before.count(anchor)==1 and b"profile_config.get('lil_B122_B127_editorial')" not in before
    after=before.replace(anchor,stage+anchor);compile(after,str(builder),'exec')
    (ROOT/'registry_before_raw.json').write_bytes(raw);(ROOT/'builder_before.py').write_bytes(before);(ROOT/'builder_added_optional_stage.bin').write_bytes(stage)
    save(owned.CONFIG,conf);profile=deepcopy(registry['profiles']['all-routes-unified-v3251'])
    profile.update(lil_B122_B127_editorial=owned.CONFIG,description='Complete V3251 cumulative stack plus159 contextual Lil B122-B127 reviews.',note='55revisions/104justified retentions;155speech/4labels,2two-optionmenus/2source2000pauses.155nativeplanes/1240logical-compiled/620finalmacrocases;312commands/64spans/320skipcases/14predicates;336loaders/twoparents/threeentrycensuses. Bothpause/resumeboundaries andB126choice-control/return0 pass.All23sheets viewed orhash-exact;68rowcount-only notes.Shared actual rules inherited byexact runtime/data;no newselectedscene/nameplate/earnedprogress/fullroute/hardware claim. Registered build/exactcleanpatch/freshstartup pending. Experimental;preserve everyROM/translation;no promotion.')
    registry['profiles'][PROFILE]=profile;assert rp.read_bytes()==raw and builder.read_bytes()==before
    pending=rp.with_name('release_stack_v3299b_pending.json');assert not pending.exists();save(pending,registry);builder.write_bytes(after);os.replace(pending,rp)
    restored=deepcopy(read(rp));restored['profiles'].pop(PROFILE);assert restored==read(ROOT/'registry_before_raw.json') and builder.read_bytes().replace(stage,b'',1)==before
    save(ROOT/'registration_receipt.json',dict(profile=PROFILE,parent_profile='all-routes-unified-v3251',config=owned.CONFIG,config_sha256=sha(Path(owned.CONFIG).read_bytes()),negative_cases=50,all114accepted_layers_previous_profiles_and_V1492_promotion_unchanged=True,only_one_optional_stage_and_one_experimental_profile_added=True,release_stack_sha256=sha(rp.read_bytes()),builder_sha256=sha(builder.read_bytes()),no_ROM_created_or_promoted=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('RegisteredV3300 optional159-object/two-manuscript stage afterfullV3251;50 negative cases reject before mutation. Previousprofiles/114acceptedlayers preserved.')
