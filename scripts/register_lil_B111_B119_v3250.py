"""Register 150 guarded reviews after the complete V3204 cumulative stack."""
import os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import lil_B111_B119_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B111_B119_registration_v3250')
PROFILE='all-routes-unified-v3251'
PARENT=Path('out/all_routes_combined_v3204_candidate.nds')
DOC=Path('translations/lil_B111_B119_editorial_manuscript_v6.json')
VOICE=Path('translations/lil_B111_B119_actor_style_manuscript_v5.json')
MAP=Path('translations/lil_B111_B119_editorial_relocation_map_v1.json')

if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists()
    rp,builder=Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py')
    raw,before=rp.read_bytes(),builder.read_bytes();registry=read(rp)
    assert PROFILE not in registry['profiles'] and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
    parent=NdsImage.open(PARENT);base=NdsImage.open('out/raphael_natural_v2_accepted_base.nds');doc,mapping=map(read,[DOC,MAP])
    assert sha(PARENT.read_bytes())==doc['current_ROM_sha256']
    deps={str(DOC),str(VOICE),str(MAP),str(Path(owned.__file__)),__file__,'dk4tool/dialogue/lil_B111_B119_profile.py','dk4tool/dialogue/lil_B111_B119_layout_v2.py','dk4tool/dialogue/layout.py','dk4tool/dialogue/encoder.py','dk4tool/dialogue/qa.py','dk4tool/dialogue/review.py','docs/editorial_testing_scope_v1870.md',
        'work/analysis/lil_B111_B119_reference_approval_v3246/approval_receipt.json',
        'work/analysis/lil_B111_B119_loader_v3241/whole_SC2_and_nine_selected_blocks_initial_entry_proof.json',
        'scripts/research_lil_B111_B119_relocation_v3239b.py','scripts/prepare_lil_B111_B119_research_v3240b.py','scripts/verify_lil_B111_B119_loader_v3241.py','scripts/verify_lil_B111_B119_references_v3242.py','scripts/prove_lil_B111_B119_relocated_controls_v3243d.py','scripts/reconcile_lil_B111_B119_sampling_v3245.py','scripts/seal_lil_B111_B119_references_v3246.py','scripts/prove_lil_B111_B119_controls_v3219.py','scripts/verify_lil_B111_B119_fonts_v3234c.py','scripts/verify_lil_B111_B119_FE_v3231.py','scripts/reconcile_lil_B111_B119_FE_v3235.py','scripts/verify_lil_relocated_copy_boundary_v3244.py','scripts/lil_kuhn_china_FE_painter_v2909.py','scripts/approve_lil_B111_B119_fonts_v3236.py','scripts/author_lil_B111_B119_v3225.py','scripts/refine_lil_grandfather_prose_v3228.py','scripts/refine_lil_B111_B119_flow_v3232.py','scripts/lil_monk_rescue_jade_prose_v3222.py','scripts/lil_cacao_tablet_Benazir_prose_v3223.py','scripts/lil_figurehead_tribal_trends_prose_v3224.py'}
    deps.update(doc[k] for k in ['source_context','control_contract','branch_proof','whole_exchange_context_notes','native_font_proof','representative_proof','historical_representative_sheet_review','prior_current_sheet_review','final_padding_proof','relocated_control_proof','item_terminology_reconciliation','actor_voice_contract','effective_current_comparison','appended_copy_classification','unowned_copy_proof','native_progressive_proof','native_FE_proof'])
    deps.update(mapping[k] for k in ['source_plan','source_census'])
    for path in list(deps):
        if Path(path).suffix=='.json':
            item=read(path)
            for key in ['evidence','hashes']:
                if isinstance(item.get(key),dict):deps.update(p for p in item[key] if Path(p).is_file())
    font=read(doc['native_font_proof']);deps.update(s['path'] for s in font['all20_review_sheets']);deps.update(c['preview'] for c in font['cases'])
    for p in [doc['historical_representative_sheet_review'],doc['prior_current_sheet_review']]:deps.add(read(p)['sheet'])
    for p in read(doc['native_FE_proof'])['cases']:deps.update([p['native_plane'],p['preview']])
    conf=dict(format='dk4-lil-B111-B119-editorial-release-v1',manuscript=str(DOC),actor_styles=str(VOICE),reference_map=str(MAP),required_runtime_arm9_sha256=sha(parent.read_file('/__arm9__.bin')),source_SC2_sha256=mapping['source_SC2_sha256'],target_SC2_sha256=mapping['target_SC2_sha256'],canonical_SC2_sha256=mapping['canonical_SC2_sha256'],clean_SC2_sha256=mapping['clean_SC2_sha256'],clean_ROM='work/clean.nds',clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),dependencies={p:sha(Path(p).read_bytes()) for p in sorted(deps)})
    ROOT.mkdir(parents=True);positive=ROOT/'positive_config.json';save(positive,conf)
    test=NdsImage.open(PARENT);proof=owned.apply_release(test,base,positive)
    assert test.read_file(owned.PATH)==Path('work/analysis/lil_B111_B119_relocation_v3239b/SC2_RESEARCH_ONLY.DK4').read_bytes()
    assert test.read_file('/__arm9__.bin')==parent.read_file('/__arm9__.bin') and len(proof['changed_records'])==150
    save(ROOT/'positive_reconstruction.json',proof);negatives=[]
    def reject(label,image,baseline,config):
        initial=(image.read_file(owned.PATH),image.read_file('/__arm9__.bin'))
        try:owned.apply_release(image,baseline,config)
        except (AssertionError,ValueError) as error:
            assert (image.read_file(owned.PATH),image.read_file('/__arm9__.bin'))==initial
            negatives.append(dict(case=label,rejected_before_mutation=True,error=str(error)))
        else:raise AssertionError(label)
    reject('repeated_application',test,base,positive)
    for label,path in [('wrong_SC2',owned.PATH),('wrong_ARM9','/__arm9__.bin')]:
        im=NdsImage.open(PARENT);data=bytearray(im.read_file(path));data[256]^=1;im.replace_file(path,bytes(data));reject(label,im,base,positive)
    badbase=NdsImage.open('out/raphael_natural_v2_accepted_base.nds');data=bytearray(badbase.read_file(owned.PATH));data[32]^=1;badbase.replace_file(owned.PATH,bytes(data));reject('wrong_canonical',NdsImage.open(PARENT),badbase,positive)
    def speech(d,prefix):return next(r for r in d['records'] if r.get('source_presentation_prefix_hex')==prefix)
    def modal(d):return next(r for r in d['records'] if r['kind']=='system-FE')
    def named(d,macro):return next(r for r in d['records'] if '{MACRO:'+macro+'}' in r['english'])
    def style(d,prefix):return next(r for r in d['records'] if r['virtual_formatter_prefix_hex']==prefix)
    def tag_change(d,prefix,new):
        r=style(d,prefix);r['english']=r['english'].replace('{SPEAKER:'+prefix.upper()+'}',new)
    def copy_spec(d):return next(b for b in d['blocks'] if b['block']==115)
    changes=[
        ('missing_format_review',DOC,'manuscript',lambda d:d['records'][0]['review'].update(formatting=False)),
        ('wrong_Japanese_source',DOC,'manuscript',lambda d:d['records'][0].update(source_hex='00')),
        ('wrong_consumer',DOC,'manuscript',lambda d:d['records'][0].update(native_display_consumer='original_FE_modal_5473C_mode1')),
        ('missing_actor_state',DOC,'manuscript',lambda d:speech(d,'89').update(english=speech(d,'89')['english'].replace('{SPEAKER:89}',''))),
        ('wrong_actor_state',DOC,'manuscript',lambda d:speech(d,'89').update(english=speech(d,'89')['english'].replace('SPEAKER:89','SPEAKER:02'))),
        ('invented_macro',DOC,'manuscript',lambda d:d['records'][0].update(english=d['records'][0]['english']+' {MACRO:FI}')),
        ('changed_approved_prose',DOC,'manuscript',lambda d:d['records'][0].update(english=d['records'][0]['english']+' Fine.')),
        ('missing_source_FI',DOC,'manuscript',lambda d:named(d,'FI').update(english=named(d,'FI')['english'].replace('{MACRO:FI}','Lil'))),
        ('missing_source_FO',DOC,'manuscript',lambda d:named(d,'FO').update(english=named(d,'FO')['english'].replace('{MACRO:FO}','Argot Co.'))),
        ('wrong_complete_preamble',DOC,'manuscript',lambda d:d['records'][0].update(source_complete_preamble_hex='0040ffff005c')),
        ('wrong_source_bound_formatter',DOC,'manuscript',lambda d:d.update(native_formatter_module='dk4tool/dialogue/encoder.py')),
        ('CF_captain_selector_changed',DOC,'manuscript',lambda d:speech(d,'cf').update(english=speech(d,'cf')['english'].replace('SPEAKER:CF','SPEAKER:02'))),
        ('FE_wrong_consumer',DOC,'manuscript',lambda d:modal(d).update(native_display_consumer='original_progressive_54020')),
        ('FE_converted_selector',DOC,'manuscript',lambda d:modal(d).update(source_hex='f8f2'+modal(d)['source_hex'][2:])),
        ('FE_invented_name_macro',DOC,'manuscript',lambda d:modal(d).update(english=modal(d)['english']+' {MACRO:FI}')),
        ('FE_invented_speaker_label',DOC,'manuscript',lambda d:modal(d).update(english=modal(d)['english'].replace('}','}Villager: ',1))),
        ('style_missing_format_review',VOICE,'actor_styles',lambda d:d['records'][0]['review'].update(formatting=False)),
        ('style_prefix_marked_physical',VOICE,'actor_styles',lambda d:d['records'][0].update(virtual_formatter_prefix_is_not_part_of_stored_alternative_text=False)),
        ('style_virtual_prefix_in_physical_body',VOICE,'actor_styles',lambda d:d['records'][0].update(compiled_stored_alternative_hex=d['records'][0]['compiled_hex'])),
        ('style_alias_slot_deleted',VOICE,'actor_styles',lambda d:next(r for r in d['records'] if len(r['style_indices'])>1)['style_indices'].pop()),
        ('style_wrong_source_role',VOICE,'actor_styles',lambda d:d['records'][0].update(source_selector=207)),
        ('style_changed_approved_prose',VOICE,'actor_styles',lambda d:d['records'][0].update(english=d['records'][0]['english']+' Well.')),
        ('style_unreviewed_alternative_missing',VOICE,'actor_styles',lambda d:d['records'].pop()),
        ('style_false_allD0_metadata',VOICE,'actor_styles',lambda d:d['records'][0].update(virtual_formatter_prefix_hex='d0')),
        ('missing_reference_approval',MAP,'reference_map',lambda d:d.update(external_references_complete=False)),
        ('wrong_mapped_command',MAP,'reference_map',lambda d:d['blocks'][0]['mapped_native_commands'][0].update(new_offset=10)),
        ('wrong_relative_target',MAP,'reference_map',lambda d:d['blocks'][0]['relative_skip_fixups'][0].update(new_matched_skip_target=0)),
        ('missing_predicate_query_approval',MAP,'reference_map',lambda d:d.update(all15_relocated_predicate_pairs_and_one_event319_query_preserve_source_operands_results_and_mapped_cursor=False)),
        ('style_map_alias_changed',MAP,'reference_map',lambda d:next(c for b in d['blocks'] for c in b['actor_style_commands'])['new_style_offsets'].__setitem__(0,2)),
        ('style_map_header_changed',MAP,'reference_map',lambda d:next(c for b in d['blocks'] for c in b['actor_style_commands']).update(target_hex='01'+next(c for b in d['blocks'] for c in b['actor_style_commands'])['target_hex'][2:])),
        ('missing_native_style_gate',MAP,'reference_map',lambda d:d.update(all6_actor_style_objects48_slots34_strings_aliases_and_actual5_virtual_prefixes_verified=False)),
        ('unowned_copy_digest_changed',MAP,'reference_map',lambda d:copy_spec(d)['unowned_appended_copy'].update(sha256='0'*64)),
        ('unowned_copy_offset_changed',MAP,'reference_map',lambda d:copy_spec(d)['unowned_appended_copy'].update(new_offset=0)),
        ('unowned_copy_size_changed',MAP,'reference_map',lambda d:copy_spec(d)['unowned_appended_copy'].update(bytes=1884)),
        ('missing_unowned_copy_gate',MAP,'reference_map',lambda d:d.update(unowned1886byte_copy_preserved_and_original_VM_return_before_copy_verified=False)),
        ('canonical_Maria32_credit_not_pending',MAP,'reference_map',lambda d:d.update(canonical_Maria_SC3_B97_32_targets_still_pending_uncredited=False)),
        ('query_event_changed',MAP,'reference_map',lambda d:d['original_event_queries'][0].update(event=320)),
        ('query_removed',MAP,'reference_map',lambda d:d.update(original_event_queries=[])),
        ('false_active_physical_scope',MAP,'reference_map',lambda d:d.update(all116_active_speech_targets_and148_physical_speeches_preserved=False)),
        ('invented_choice_scope',MAP,'reference_map',lambda d:d.update(no_player_choice_objects=False)),
    ]
    for prefix in ['d0','d1','d6','d7','dc']:
        changes.append(('missing_actual_virtual_'+prefix,VOICE,'actor_styles',lambda d,p=prefix:tag_change(d,p,'')))
        changes.append(('wrong_actual_virtual_'+prefix,VOICE,'actor_styles',lambda d,p=prefix:tag_change(d,p,'{SPEAKER:CF}')))
    for label,path,key,mutate in changes:
        value=read(path);mutate(value);mp=ROOT/(label+'.json');save(mp,value);cfg=deepcopy(conf);cfg[key]=str(mp);cfg['dependencies'][str(mp)]=sha(mp.read_bytes())
        if key=='reference_map':
            for doc_key,original_path in [('manuscript',DOC),('actor_styles',VOICE)]:
                d=read(original_path);d.update(reference_map=str(mp),reference_map_sha256=sha(mp.read_bytes()));p2=ROOT/(label+'_'+doc_key+'.json');save(p2,d);cfg[doc_key]=str(p2);cfg['dependencies'][str(p2)]=sha(p2.read_bytes())
        cp=ROOT/(label+'_config.json');save(cp,cfg);reject(label,NdsImage.open(PARENT),base,cp)
    assert len(changes)==50 and len(negatives)==54
    save(ROOT/'negative_cases.json',dict(cases=negatives,all_rejected_before_mutation=True))
    stage=b'''    lil_cultural = profile_config.get('lil_B111_B119_editorial')
    if lil_cultural:
        from dk4tool.patch.lil_B111_B119_editorial import apply_release as apply_lil_cultural

        lil_cultural_report = apply_lil_cultural(candidate, baseline, lil_cultural)
        grouped.setdefault('/data/SC2.DK4', [])
        changed_records.setdefault('/data/SC2.DK4', []).extend(row['id'] for row in lil_cultural_report['changed_records'])
        relocation_checks.setdefault('/data/SC2.DK4', {})['lil_B111_B119_editorial'] = {
            'release_config': lil_cultural,
            'release_config_sha256': sha256(Path(lil_cultural).read_bytes()),
            'proof': lil_cultural_report}
        for cultural_key in ('manuscript', 'actor_styles'):
            cultural_batch = Path(lil_cultural_report[cultural_key])
            if cultural_batch in release_batches:
                raise ValueError('B111-B119 must run once after the complete V3204 stack')
            release_batches.append(cultural_batch)

'''
    anchor=b'    # Lexically valid "% o"';assert before.count(anchor)==1 and b"profile_config.get('lil_B111_B119_editorial')" not in before
    after=before.replace(anchor,stage+anchor);compile(after,str(builder),'exec')
    (ROOT/'registry_before_raw.json').write_bytes(raw);(ROOT/'builder_before.py').write_bytes(before);(ROOT/'builder_added_optional_stage.bin').write_bytes(stage)
    save(owned.CONFIG,conf);profile=deepcopy(registry['profiles']['all-routes-unified-v3204'])
    profile.update(lil_B111_B119_editorial=owned.CONFIG,description='Complete V3204 cumulative stack plus150 contextual Lil B111-B119 reviews.',note='47revisions/103justified retentions;116speech/34stored alternatives,6variable-selector4100objects/48aliases.150nativeplanes/1200logical-compiled/600final macro cases;305physicalcommands/148physicalspeech/64spans/320skipcases/15predicates/event319;336loaders/twoparents/threeentrycensuses. Exact1886byte unownedMaria copy survives movedreturn0;canonicalSC3B97Maria32 queued uncredited. All20sheets viewed orhash-exact;only46rowcountnotes. Actual shared display rules inherited byexact runtime/data;nonewselected scene/nameplate/earnedprogress/fullroute/hardware claim. Registered build/exactcleanpatch/freshstartup pending. Experimental;preserve everyROM/translation;no promotion.')
    registry['profiles'][PROFILE]=profile;assert rp.read_bytes()==raw and builder.read_bytes()==before
    pending=rp.with_name('release_stack_v3250_pending.json');assert not pending.exists();save(pending,registry);builder.write_bytes(after);os.replace(pending,rp)
    restored=deepcopy(read(rp));restored['profiles'].pop(PROFILE);assert restored==read(ROOT/'registry_before_raw.json') and builder.read_bytes().replace(stage,b'',1)==before
    save(ROOT/'registration_receipt.json',dict(profile=PROFILE,parent_profile='all-routes-unified-v3204',config=owned.CONFIG,config_sha256=sha(Path(owned.CONFIG).read_bytes()),negative_cases=54,all114accepted_layers_previous_profiles_and_V1492_promotion_unchanged=True,only_one_optional_stage_and_one_experimental_profile_added=True,release_stack_sha256=sha(rp.read_bytes()),builder_sha256=sha(builder.read_bytes()),no_ROM_created_or_promoted=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('RegisteredV3251 optional150-object/two-manuscript stage afterfullV3204;54negative cases reject before mutation. Previousprofiles/114acceptedlayers preserved.')
