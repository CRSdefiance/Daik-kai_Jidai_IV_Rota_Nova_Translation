"""Register 235 guarded reviews after the full V3144 cumulative stack."""
import os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import lil_shrines_temples_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Shrines_Temples_registration_v3203')
PROFILE='all-routes-unified-v3204'
PARENT=Path('out/all_routes_combined_v3144_candidate.nds')
DOC=Path('translations/lil_shrines_temples_editorial_manuscript_v8.json')
VOICE=Path('translations/lil_shrines_temples_actor_style_manuscript_v6.json')
CHOICE=Path('translations/lil_shrines_temples_choice_manuscript_v5.json')
MAP=Path('translations/lil_shrines_temples_editorial_relocation_map_v1.json')

if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists()
    rp,builder=Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py')
    raw,before=rp.read_bytes(),builder.read_bytes();registry=read(rp)
    assert PROFILE not in registry['profiles'] and len(registry['accepted_layers'])==114
    assert registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
    parent=NdsImage.open(PARENT);base=NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    doc,mapping=map(read,[DOC,MAP])
    assert sha(PARENT.read_bytes())==doc['current_ROM_sha256']
    deps={str(DOC),str(VOICE),str(CHOICE),str(MAP),str(Path(owned.__file__)),__file__,
        'dk4tool/dialogue/lil_shrines_temples_profile.py','dk4tool/dialogue/lil_shrines_temples_layout_v2.py',
        'dk4tool/dialogue/layout.py','dk4tool/dialogue/encoder.py','dk4tool/dialogue/qa.py','dk4tool/dialogue/review.py',
        'docs/editorial_testing_scope_v1870.md',
        doc['source_context'],doc['control_contract'],doc['branch_proof'],doc['whole_exchange_context_notes'],
        doc['native_font_proof'],doc['representative_proof'],doc['historical_representative_sheet_review'],
        doc['prior_current_sheet_review'],doc['final_padding_proof'],doc['relocated_control_proof'],
        doc['item_terminology_reconciliation'],mapping['source_plan'],mapping['source_census'],
        'work/analysis/lil_Shrines_Temples_reference_approval_v3199/approval_receipt.json',
        'work/analysis/lil_Shrines_Temples_loader_v3195b/whole_SC2_and_ten_selected_blocks_initial_entry_proof.json',
        'scripts/research_lil_shrines_relocation_v3193.py','scripts/prepare_lil_shrines_research_v3194.py',
        'scripts/verify_lil_shrines_loader_v3195b.py','scripts/verify_lil_shrines_references_v3196.py',
        'scripts/prove_lil_shrines_relocated_controls_v3197.py','scripts/reconcile_lil_shrines_sampling_v3198.py',
        'scripts/seal_lil_shrines_references_v3199.py','scripts/prove_lil_shrines_temples_controls_v3168c.py',
        'scripts/verify_lil_shrines_fonts_v3183b.py','scripts/verify_lil_shrines_FE_v3180.py',
        'scripts/reconcile_lil_shrines_FE_v3184.py','scripts/lil_kuhn_china_FE_painter_v2909.py',
        'scripts/prove_lil_shrines_choices_v3188.py','scripts/approve_lil_shrines_fonts_v3190b.py',
        'scripts/author_lil_shrines_temples_v3174.py','scripts/refine_lil_shrines_prose_v3177.py',
        'scripts/refine_lil_shrines_visual_v3181.py','scripts/refine_lil_sphinx_menu_v3187.py',
        'scripts/lil_priest_cross_sphinx_prose_v3171.py','scripts/lil_cult_star_lamp_prose_v3172.py',
        'scripts/lil_beans_jar_prose_v3173.py'}
    deps.update(doc[k] for k in ['native_progressive_proof','native_FE_proof','native_choice_proof'])
    for m in read(doc['native_choice_proof'])['menus']:deps.add(m['proof'])
    for path in list(deps):
        if Path(path).suffix=='.json':
            item=read(path)
            for key in ['evidence','hashes']:
                if isinstance(item.get(key),dict):deps.update(p for p in item[key] if Path(p).is_file())
    font=read(doc['native_font_proof'])
    deps.update(s['path'] for s in font['all33_review_sheets'])
    deps.update(c['preview'] for c in font['cases'])
    for p in [doc['historical_representative_sheet_review'],doc['prior_current_sheet_review']]:deps.add(read(p)['sheet'])
    for p in read(doc['native_FE_proof'])['cases']:deps.update([p['native_plane'],p['preview']])
    conf=dict(format='dk4-lil-shrines-temples-editorial-release-v1',manuscript=str(DOC),actor_styles=str(VOICE),
        choices=str(CHOICE),reference_map=str(MAP),required_runtime_arm9_sha256=sha(parent.read_file('/__arm9__.bin')),
        source_SC2_sha256=mapping['source_SC2_sha256'],target_SC2_sha256=mapping['target_SC2_sha256'],
        canonical_SC2_sha256=mapping['canonical_SC2_sha256'],clean_SC2_sha256=mapping['clean_SC2_sha256'],
        clean_ROM='work/clean.nds',clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),
        dependencies={p:sha(Path(p).read_bytes()) for p in sorted(deps)})
    ROOT.mkdir(parents=True)
    positive=ROOT/'positive_config.json';save(positive,conf)
    test=NdsImage.open(PARENT);proof=owned.apply_release(test,base,positive)
    assert test.read_file(owned.PATH)==Path('work/analysis/lil_Shrines_Temples_relocation_v3193/SC2_RESEARCH_ONLY.DK4').read_bytes()
    assert test.read_file('/__arm9__.bin')==parent.read_file('/__arm9__.bin')
    assert len(proof['changed_records'])==235
    save(ROOT/'positive_reconstruction.json',proof)
    negatives=[]
    def reject(label,image,baseline,config):
        initial=(image.read_file(owned.PATH),image.read_file('/__arm9__.bin'))
        try:owned.apply_release(image,baseline,config)
        except (AssertionError,ValueError):
            assert (image.read_file(owned.PATH),image.read_file('/__arm9__.bin'))==initial
            negatives.append(dict(case=label,rejected_before_mutation=True))
        else:raise AssertionError(label)
    reject('repeated_application',test,base,positive)
    for label,path in [('wrong_SC2',owned.PATH),('wrong_ARM9','/__arm9__.bin')]:
        im=NdsImage.open(PARENT);data=bytearray(im.read_file(path));data[256]^=1
        im.replace_file(path,bytes(data));reject(label,im,base,positive)
    badbase=NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    data=bytearray(badbase.read_file(owned.PATH));data[32]^=1;badbase.replace_file(owned.PATH,bytes(data))
    reject('wrong_canonical',NdsImage.open(PARENT),badbase,positive)
    def speech(d,prefix):
        return next(r for r in d['records'] if r['source_presentation_prefix_hex']==prefix)
    def modal(d):return next(r for r in d['records'] if r['kind']=='system-FE')
    def named(d):return next(r for r in d['records'] if '{MACRO:FI}' in r['english'])
    changes=[
        ('missing_format_review',DOC,'manuscript',lambda d:d['records'][0]['review'].update(formatting=False)),
        ('wrong_Japanese_source',DOC,'manuscript',lambda d:d['records'][0].update(source_hex='00')),
        ('wrong_consumer',DOC,'manuscript',lambda d:d['records'][0].update(native_display_consumer='original_FE_modal_5473C_mode1')),
        ('missing_printable_actor_state',DOC,'manuscript',lambda d:speech(d,'8b').update(english=speech(d,'8b')['english'].replace('{SPEAKER:8B}',''))),
        ('wrong_printable_actor_state',DOC,'manuscript',lambda d:speech(d,'8b').update(english=speech(d,'8b')['english'].replace('SPEAKER:8B','SPEAKER:02'))),
        ('invented_macro',DOC,'manuscript',lambda d:d['records'][0].update(english=d['records'][0]['english']+' {MACRO:FI}')),
        ('changed_approved_prose',DOC,'manuscript',lambda d:d['records'][0].update(english=d['records'][0]['english']+' Fine.')),
        ('missing_source_FI',DOC,'manuscript',lambda d:named(d).update(english=named(d)['english'].replace('{MACRO:FI}','Lil'))),
        ('wrong_complete_preamble',DOC,'manuscript',lambda d:d['records'][0].update(source_complete_preamble_hex='0040ffff005c')),
        ('wrong_source_bound_formatter',DOC,'manuscript',lambda d:d.update(native_formatter_module='dk4tool/dialogue/encoder.py')),
        ('CF_captain_selector_changed',DOC,'manuscript',lambda d:speech(d,'cf').update(english=speech(d,'cf')['english'].replace('SPEAKER:CF','SPEAKER:02'))),
        ('D0_role_selector_changed',DOC,'manuscript',lambda d:speech(d,'d0').update(english=speech(d,'d0')['english'].replace('SPEAKER:D0','SPEAKER:97'))),
        ('FE_wrong_consumer',DOC,'manuscript',lambda d:modal(d).update(native_display_consumer='original_progressive_54020')),
        ('FE_converted_selector',DOC,'manuscript',lambda d:modal(d).update(source_hex='f8f2'+modal(d)['source_hex'][2:])),
        ('FE_invented_name_macro',DOC,'manuscript',lambda d:modal(d).update(english=modal(d)['english']+' {MACRO:FI}')),
        ('FE_invented_speaker_label',DOC,'manuscript',lambda d:modal(d).update(english=modal(d)['english'].replace('}','}Priest: ',1))),
        ('style_missing_format_review',VOICE,'actor_styles',lambda d:d['records'][0]['review'].update(formatting=False)),
        ('style_missing_virtual_D0',VOICE,'actor_styles',lambda d:d['records'][0].update(english=d['records'][0]['english'].replace('{SPEAKER:D0}',''))),
        ('style_wrong_virtual_actor',VOICE,'actor_styles',lambda d:d['records'][0].update(english=d['records'][0]['english'].replace('SPEAKER:D0','SPEAKER:02'))),
        ('style_prefix_marked_physical',VOICE,'actor_styles',lambda d:d['records'][0].update(virtual_formatter_prefix_is_not_part_of_stored_alternative_text=False)),
        ('style_D0_in_physical_body',VOICE,'actor_styles',lambda d:d['records'][0].update(compiled_stored_alternative_hex=d['records'][0]['compiled_hex'])),
        ('style_alias_slot_deleted',VOICE,'actor_styles',lambda d:next(r for r in d['records'] if len(r['style_indices'])>1)['style_indices'].pop()),
        ('style_wrong_source_role',VOICE,'actor_styles',lambda d:d['records'][0].update(source_selector=207)),
        ('style_changed_approved_prose',VOICE,'actor_styles',lambda d:d['records'][0].update(english=d['records'][0]['english']+' Well.')),
        ('style_unreviewed_alternative_missing',VOICE,'actor_styles',lambda d:d['records'].pop()),
        ('choice_result_swapped',CHOICE,'choices',lambda d:d['records'][0].update(option_index=1)),
        ('choice_authored_padding',CHOICE,'choices',lambda d:d['records'][0].update(english=' I know.')),
        ('choice_changed_approved_label',CHOICE,'choices',lambda d:d['records'][0].update(english='I give up.')),
        ('choice_third_answer_missing',CHOICE,'choices',lambda d:d['records'].pop(2)),
        ('choice_source_offset_wrong',CHOICE,'choices',lambda d:d['records'][2]['source_reference'].update(offset=0)),
        ('choice_missing_format_review',CHOICE,'choices',lambda d:d['records'][0]['review'].update(formatting=False)),
        ('missing_reference_approval',MAP,'reference_map',lambda d:d.update(external_references_complete=False)),
        ('wrong_mapped_command',MAP,'reference_map',lambda d:d['blocks'][0]['mapped_native_commands'][0].update(new_offset=10)),
        ('wrong_0400_target',MAP,'reference_map',lambda d:next(e for b in d['blocks'] for e in b['relative_skip_fixups'] if e['word']==0x400).update(new_matched_skip_target=0)),
        ('missing_relocated_predicate_approval',MAP,'reference_map',lambda d:d.update(all21_relocated_predicate_pairs_preserve_source_operands_and_results=False)),
        ('style_map_alias_changed',MAP,'reference_map',lambda d:next(c for b in d['blocks'] for c in b['actor_style_commands'])['new_style_offsets'].__setitem__(0,2)),
        ('style_header_selector_changed',MAP,'reference_map',lambda d:next(c for b in d['blocks'] for c in b['actor_style_commands']).update(target_hex='01'+next(c for b in d['blocks'] for c in b['actor_style_commands'])['target_hex'][2:])),
        ('choice_map_third_label_changed',MAP,'reference_map',lambda d:next(c for b in d['blocks'] for c in b['choice_commands']).update(target_hex='00')),
        ('missing_native_style_reference_gate',MAP,'reference_map',lambda d:d.update(all8_actor_style_objects64_slots56_strings_aliases_and_virtual_D0_storage_verified=False)),
        ('missing_native_three_option_gate',MAP,'reference_map',lambda d:d.update(all5_three_option_menu_objects15_labels_preserve_source_indices012_and_cancel=False)),
    ]
    for label,path,key,mutate in changes:
        value=read(path);mutate(value);mp=ROOT/(label+'.json');save(mp,value)
        cfg=deepcopy(conf);cfg[key]=str(mp);cfg['dependencies'][str(mp)]=sha(mp.read_bytes())
        if key=='reference_map':
            # Keep the cross-document binding coherent so map tests reach
            # the affected native/relocation guard rather than a path mismatch.
            for doc_key,original_path in [('manuscript',DOC),('actor_styles',VOICE),('choices',CHOICE)]:
                d=read(original_path);d.update(reference_map=str(mp),reference_map_sha256=sha(mp.read_bytes()))
                path2=ROOT/(label+'_'+doc_key+'.json');save(path2,d)
                cfg[doc_key]=str(path2);cfg['dependencies'][str(path2)]=sha(path2.read_bytes())
        cp=ROOT/(label+'_config.json');save(cp,cfg)
        reject(label,NdsImage.open(PARENT),base,cp)
    assert len(negatives)==44
    save(ROOT/'negative_cases.json',dict(cases=negatives,all_rejected_before_mutation=True))
    stage=b'''    lil_shrines = profile_config.get('lil_shrines_temples_editorial')
    if lil_shrines:
        from dk4tool.patch.lil_shrines_temples_editorial import apply_release as apply_lil_shrines

        lil_shrines_report = apply_lil_shrines(candidate, baseline, lil_shrines)
        grouped.setdefault('/data/SC2.DK4', [])
        changed_records.setdefault('/data/SC2.DK4', []).extend(row['id'] for row in lil_shrines_report['changed_records'])
        relocation_checks.setdefault('/data/SC2.DK4', {})['lil_shrines_temples_editorial'] = {
            'release_config': lil_shrines,
            'release_config_sha256': sha256(Path(lil_shrines).read_bytes()),
            'proof': lil_shrines_report}
        for shrines_key in ('manuscript', 'actor_styles', 'choices'):
            shrines_batch = Path(lil_shrines_report[shrines_key])
            if shrines_batch in release_batches:
                raise ValueError('Shrines/Temples must run once after the complete V3144 stack')
            release_batches.append(shrines_batch)

'''
    anchor=b'    # Lexically valid "% o"'
    assert before.count(anchor)==1 and b"profile_config.get('lil_shrines_temples_editorial')" not in before
    after=before.replace(anchor,stage+anchor);compile(after,str(builder),'exec')
    (ROOT/'registry_before_raw.json').write_bytes(raw);(ROOT/'builder_before.py').write_bytes(before)
    (ROOT/'builder_added_optional_stage.bin').write_bytes(stage)
    save(owned.CONFIG,conf)
    profile=deepcopy(registry['profiles']['all-routes-unified-v3144'])
    profile.update(lil_shrines_temples_editorial=owned.CONFIG,
        description='Complete V3144 cumulative stack plus235 contextual shrine and temple reviews acrossSC2 B101-B110.',
        note='117revisions/118justifiedretentions.164speeches,56storedactor-style alternatives/64aliasedslots,and15three-option labels.220nativeplanes/1760logical-compiled/880finaltarget macro cases;60menuplanes/40VMreturns.421commands/114spans/570relocatedcases/21predicatepairs/noqueries;336loaders/two-parent modes/threeentrycensuses. All33sheets viewed orhash-exact. Preserve20byte4100headers/virtualD0excludedfrombodies and8byte2200headers/count3/indices012/cancel. Source uncertainty,religious/cultural context,puzzle logic,distinct voices andeffective currentCamille catalog wording retained. Only54rowcountnotes,no glyph/weak-ending/bounds/pagination waiver. Shared actual display rules inherit byexact bytes;no selectedshrine,three-option button-gameplay,newnameplate,earnedprogress,fullroute orhardware claim. Registered build/exactcleanpatch/freshstartup pending. Experimental;preserve everyROM/translation;no promotion.')
    registry['profiles'][PROFILE]=profile
    assert rp.read_bytes()==raw and builder.read_bytes()==before
    pending=rp.with_name('release_stack_v3203_pending.json')
    assert not pending.exists();save(pending,registry)
    builder.write_bytes(after);os.replace(pending,rp)
    restored=deepcopy(read(rp));restored['profiles'].pop(PROFILE)
    assert restored==read(ROOT/'registry_before_raw.json')
    assert builder.read_bytes().replace(stage,b'',1)==before
    save(ROOT/'registration_receipt.json',dict(profile=PROFILE,parent_profile='all-routes-unified-v3144',
        config=owned.CONFIG,config_sha256=sha(Path(owned.CONFIG).read_bytes()),negative_cases=44,
        all114accepted_layers_previous_profiles_and_V1492_promotion_unchanged=True,
        only_one_optional_stage_and_one_experimental_profile_added=True,
        release_stack_sha256=sha(rp.read_bytes()),builder_sha256=sha(builder.read_bytes()),
        no_ROM_created_or_promoted=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('RegisteredV3204 optional235-object/three-manuscript stage afterfullV3144;44negative cases reject before mutation. Previous profiles/114accepted layers preserved.')
