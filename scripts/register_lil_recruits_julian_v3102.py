"""Register199 guarded speech/FE/choice reviews after fullV3066."""
import os
from pathlib import Path
from copy import deepcopy
from dk4tool.patch import lil_recruits_julian_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Recruits_Julian_registration_v3102')
PROFILE='all-routes-unified-v3103'
PARENT=Path('out/all_routes_combined_v3066_candidate.nds')
DOC=Path('translations/lil_recruits_julian_editorial_manuscript_v5.json')
MAP=Path('translations/lil_recruits_julian_editorial_relocation_map_v1.json')
CHOICE=Path('translations/lil_recruits_julian_choice_manuscript_v4.json')

if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists()
    rp,builder=Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py')
    raw,before=rp.read_bytes(),builder.read_bytes();registry=read(rp)
    assert PROFILE not in registry['profiles'] and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
    parent=NdsImage.open(PARENT);base=NdsImage.open('out/raphael_natural_v2_accepted_base.nds');doc,mapping=read(DOC),read(MAP)
    assert sha(PARENT.read_bytes())==doc['current_ROM_sha256']
    deps={str(DOC),str(CHOICE),str(MAP),str(Path(owned.__file__)),__file__,
        'dk4tool/dialogue/lil_recruits_julian_profile.py','dk4tool/dialogue/encoder.py','dk4tool/dialogue/qa.py','dk4tool/dialogue/review.py','dk4tool/dialogue/lil_recruits_julian_layout_v1.py','dk4tool/dialogue/layout.py',
        doc['source_context'],doc['control_contract'],doc['branch_proof'],doc['native_font_proof'],doc['representative_proof'],
        doc['historical_representative_sheet_review'],doc['prior_current_sheet_review'],doc['final_padding_proof'],
        mapping['source_plan'],mapping['source_census'],
        'work/analysis/lil_Recruits_Julian_reference_approval_v3101/approval_receipt.json',
        'work/analysis/lil_Recruits_Julian_loader_v3098/whole_SC2_and_five_selected_blocks_initial_entry_proof.json',
        'scripts/research_lil_recruits_julian_relocation_v3096.py','scripts/prepare_lil_recruits_julian_research_v3097.py',
        'scripts/verify_lil_recruits_julian_loader_v3098.py','scripts/verify_lil_recruits_julian_references_v3099.py',
        'scripts/reconcile_lil_recruits_julian_sampling_v3100.py','scripts/seal_lil_recruits_julian_references_v3101.py',
        'scripts/prove_lil_recruits_julian_controls_v3074.py','scripts/verify_lil_recruits_julian_fonts_v3088.py',
        'docs/editorial_testing_scope_v1870.md'}
    font=read(doc['native_font_proof']);deps.update(doc[k] for k in ['native_progressive_proof','native_FE_proof','native_choice_proof'])
    for native in read(doc['native_choice_proof'])['menus']:deps.add(native['proof'])
    deps.add(doc['item_terminology_reconciliation'])
    deps.update(['scripts/author_lil_recruits_julian_v3083.py','scripts/refine_lil_recruits_julian_v3086.py','scripts/refine_lil_janus_choice_v3091.py','scripts/prove_lil_recruits_julian_choices_v3092.py'])
    deps.update(['scripts/lil_janus_recruitment_prose_v3079.py','scripts/lil_charles_recruitment_prose_v3080.py','scripts/lil_yukihisa_recruitment_prose_v3081.py','scripts/lil_julian_prose_v3082.py'])
    for p in list(deps):
        if Path(p).suffix=='.json':
            item=read(p)
            for key in ['evidence','hashes']:
                if isinstance(item.get(key),dict):deps.update(p for p in item[key] if Path(p).is_file())
    for p in [doc['historical_representative_sheet_review'],doc['prior_current_sheet_review']]:deps.add(read(p)['sheet'])
    deps.update(s['path'] for s in font['all27_review_sheets'])
    for panel in read(doc['native_FE_proof'])['cases']:deps.update([panel['native_plane'],panel['preview']])
    deps.update(['scripts/verify_lil_recruits_julian_FE_v3089.py','scripts/lil_kuhn_china_FE_painter_v2909.py','scripts/approve_lil_recruits_julian_fonts_v3093.py'])
    conf=dict(format='dk4-lil-recruits-julian-editorial-release-v1',manuscript=str(DOC),choices=str(CHOICE),reference_map=str(MAP),
        required_runtime_arm9_sha256=sha(parent.read_file('/__arm9__.bin')),source_SC2_sha256=mapping['source_SC2_sha256'],target_SC2_sha256=mapping['target_SC2_sha256'],
        canonical_SC2_sha256=mapping['canonical_SC2_sha256'],clean_SC2_sha256=mapping['clean_SC2_sha256'],clean_ROM='work/clean.nds',clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),
        dependencies={p:sha(Path(p).read_bytes()) for p in sorted(deps)})
    ROOT.mkdir(parents=True);positive=ROOT/'positive_config.json';save(positive,conf)
    test=NdsImage.open(PARENT);proof=owned.apply_release(test,base,positive)
    assert test.read_file(owned.PATH)==Path('work/analysis/lil_Recruits_Julian_relocation_v3096/SC2_RESEARCH_ONLY.DK4').read_bytes()
    assert test.read_file('/__arm9__.bin')==parent.read_file('/__arm9__.bin');save(ROOT/'positive_reconstruction.json',proof)
    negative=[]
    def reject(label,image,baseline,config):
        initial=(image.read_file(owned.PATH),image.read_file('/__arm9__.bin'))
        try:owned.apply_release(image,baseline,config)
        except (AssertionError,ValueError):
            assert (image.read_file(owned.PATH),image.read_file('/__arm9__.bin'))==initial
            negative.append(dict(case=label,rejected_before_mutation=True))
        else:raise AssertionError(label)
    reject('repeated_application',test,base,positive)
    for label,path in [('wrong_SC2',owned.PATH),('wrong_ARM9','/__arm9__.bin')]:
        image=NdsImage.open(PARENT);data=bytearray(image.read_file(path));data[256]^=1;image.replace_file(path,bytes(data));reject(label,image,base,positive)
    badbase=NdsImage.open('out/raphael_natural_v2_accepted_base.nds');data=bytearray(badbase.read_file(owned.PATH));data[32]^=1;badbase.replace_file(owned.PATH,bytes(data));reject('wrong_canonical',NdsImage.open(PARENT),badbase,positive)
    def worker(d):return next(r for r in d['records'] if r['source_presentation_prefix_hex']=='6d')
    def named(d):return next(r for r in d['records'] if '{MACRO:FI}' in r['english'])
    changes=[('missing_format_review',str(DOC),'manuscript',lambda d:d['records'][0]['review'].update(formatting=False)),
        ('wrong_Japanese_source',str(DOC),'manuscript',lambda d:d['records'][0].update(source_hex='00')),
        ('wrong_consumer',str(DOC),'manuscript',lambda d:d['records'][0].update(native_display_consumer='original_FE_modal_5473C_mode1')),
        ('missing_printable_speaker',str(DOC),'manuscript',lambda d:worker(d).update(english=worker(d)['english'].replace('{SPEAKER:6D}',''))),
        ('wrong_printable_speaker',str(DOC),'manuscript',lambda d:worker(d).update(english=worker(d)['english'].replace('SPEAKER:6D','SPEAKER:02'))),
        ('invented_macro',str(DOC),'manuscript',lambda d:d['records'][0].update(english=d['records'][0]['english']+' {MACRO:FI}')),
        ('changed_approved_prose',str(DOC),'manuscript',lambda d:d['records'][0].update(english='{SPEAKER:04}My fleet was destroyed.')),
        ('missing_source_name_macro',str(DOC),'manuscript',lambda d:named(d).update(english=named(d)['english'].replace('{MACRO:FI}','Lil'))),
        ('wrong_complete_preamble',str(DOC),'manuscript',lambda d:d['records'][0].update(source_complete_preamble_hex='0040ffff005c')),
        ('missing_reference_approval',str(MAP),'reference_map',lambda d:d.update(external_references_complete=False)),
        ('wrong_mapped_command',str(MAP),'reference_map',lambda d:d['blocks'][0]['mapped_native_commands'][0].update(new_offset=10)),
        ('wrong_relative_target',str(MAP),'reference_map',lambda d:d['blocks'][0]['relative_skip_fixups'][0].update(new_matched_skip_target=0)),
        ('missing_relocated_predicate_approval',str(MAP),'reference_map',lambda d:d.update(all16_relocated_native_predicates_preserve_source_semantics_and_mapped_cursor=False)),
        ('choice_result_swapped',str(CHOICE),'choices',lambda d:d['records'][0].update(option_index=1)),
        ('choice_authored_padding',str(CHOICE),'choices',lambda d:d['records'][0].update(english=' Be generous.')),
        ('changed_approved_choice',str(CHOICE),'choices',lambda d:d['records'][0].update(english='Pay me again!')),
        ('wrong_source_bound_formatter',str(DOC),'manuscript',lambda d:d.update(native_formatter_module='dk4tool/dialogue/encoder.py'))]
    def FErow(d):return next(r for r in d['records'] if r['kind']=='system-FE')
    def retainer(d):return next(r for r in d['records'] if r['source_presentation_prefix_hex']=='9e')
    changes.extend([
        ('FE_wrong_consumer',str(DOC),'manuscript',lambda d:FErow(d).update(native_display_consumer='original_progressive_54020')),
        ('FE_invented_name_macro',str(DOC),'manuscript',lambda d:FErow(d).update(english=FErow(d)['english']+' {MACRO:FI}')),
        ('FE_converted_selector',str(DOC),'manuscript',lambda d:FErow(d).update(source_hex='f8f2'+FErow(d)['source_hex'][2:])),
        ('FE_as_ordinary_actor',str(DOC),'manuscript',lambda d:FErow(d).update(english=FErow(d)['english'].replace('SPEAKER:FE','SPEAKER:02'))),
        ('FE_invented_speaker_label',str(DOC),'manuscript',lambda d:FErow(d).update(english=FErow(d)['english'].replace('}Take','}Janus: Take'))),
        ('missing_9E_actor_state',str(DOC),'manuscript',lambda d:retainer(d).update(english=retainer(d)['english'].replace('{SPEAKER:9E}',''))),
        ('wrong_legal_9E_actor',str(DOC),'manuscript',lambda d:retainer(d).update(english=retainer(d)['english'].replace('SPEAKER:9E','SPEAKER:02')))])
    for label,path,key,mutate in changes:
        value=read(path);mutate(value);mp=ROOT/(label+'.json');save(mp,value)
        cfg=deepcopy(conf);cfg[key]=str(mp);cfg['dependencies'][str(mp)]=sha(mp.read_bytes());cp=ROOT/(label+'_config.json');save(cp,cfg)
        reject(label,NdsImage.open(PARENT),base,cp)
    assert len(negative)==28;save(ROOT/'negative_cases.json',dict(cases=negative,all_rejected_before_mutation=True))
    stage=b'''    lil_recruits_julian = profile_config.get('lil_recruits_julian_editorial')
    if lil_recruits_julian:
        from dk4tool.patch.lil_recruits_julian_editorial import apply_release as apply_lil_recruits_julian

        lil_recruits_julian_report = apply_lil_recruits_julian(candidate, baseline, lil_recruits_julian)
        grouped.setdefault('/data/SC2.DK4', [])
        changed_records.setdefault('/data/SC2.DK4', []).extend(row['id'] for row in lil_recruits_julian_report['changed_records'])
        relocation_checks.setdefault('/data/SC2.DK4', {})['lil_recruits_julian_editorial'] = {
            'release_config': lil_recruits_julian,
            'release_config_sha256': sha256(Path(lil_recruits_julian).read_bytes()),
            'proof': lil_recruits_julian_report}
        for recruits_julian_key in ('manuscript', 'choices'):
            recruits_julian_batch = Path(lil_recruits_julian_report[recruits_julian_key])
            if recruits_julian_batch in release_batches:
                raise ValueError('Recruits/Julian must run once after the complete V3066 stack')
            release_batches.append(recruits_julian_batch)

'''
    anchor=b'    # Lexically valid "% o"';assert before.count(anchor)==1 and b"profile_config.get('lil_recruits_julian_editorial')" not in before
    after=before.replace(anchor,stage+anchor);compile(after,str(builder),'exec')
    (ROOT/'registry_before_raw.json').write_bytes(raw);(ROOT/'builder_before.py').write_bytes(before);(ROOT/'builder_added_optional_stage.bin').write_bytes(stage)
    save(owned.CONFIG,conf)
    profile=deepcopy(registry['profiles']['all-routes-unified-v3066']);profile.update(lil_recruits_julian_editorial=owned.CONFIG,
        description='Full V3066 cumulative stack plus199 contextual recruitment/Julian reviews across fiveSC2blocks.',
        note='158revisions/41justifiedretentions;196ordinary/one unlabeledFE/two choices.197nativeplanes/1576logical-compiled/788finalparity macro cases;8menuplanes/6VMreturns.372commands/68relative sites/340relocatedcases/16predicates/noqueries/336wholeloaders/twoparents/threeentrycensuses. All27sheets viewed;74rowcount-onlynotes. Preserve Janus repairs/debts/self-correction,Charles Academy letter/bomb-science joke,Yukihisa back-of-blade/personal resolve,Julian Silla Gold Crown/Mihwa/Luo Yuli/family. Faithful twenty-cell refusal resolves the current114px tightly fitted leading-Y finding without runtime changes ormanualpadding;failedproducers preserved. Sharedactualrules inheritbyexactbytes. No selected-scene,newnameplate or earnedprogress claim. Registeredbuild/exactcleanpatch/currentstartup pending. Experimental;preserve everyROM/translation;no promotion.')
    registry['profiles'][PROFILE]=profile
    assert rp.read_bytes()==raw and builder.read_bytes()==before
    pending=rp.with_name('release_stack_v3102_pending.json');assert not pending.exists();save(pending,registry)
    builder.write_bytes(after);os.replace(pending,rp)
    restored=deepcopy(read(rp));restored['profiles'].pop(PROFILE)
    assert restored==read(ROOT/'registry_before_raw.json') and builder.read_bytes().replace(stage,b'',1)==before
    save(ROOT/'registration_receipt.json',dict(profile=PROFILE,parent_profile='all-routes-unified-v3066',config=owned.CONFIG,config_sha256=sha(Path(owned.CONFIG).read_bytes()),
        negative_cases=28,all114accepted_layers_previous_profiles_and_V1492_promotion_unchanged=True,only_one_optional_stage_and_one_experimental_profile_added=True,
        release_stack_sha256=sha(rp.read_bytes()),builder_sha256=sha(builder.read_bytes()),no_ROM_created_or_promoted=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('RegisteredV3103 optional199-object stage after fullV3066;28negative cases reject before mutation;all previous profiles/114accepted layers preserved.')
