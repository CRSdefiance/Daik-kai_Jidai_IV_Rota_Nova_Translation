"""Register200 guarded speech/FE/choice reviews after fullV3103."""
import os
from pathlib import Path
from copy import deepcopy
from dk4tool.patch import lil_crew_items_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Crew_Items_registration_v3143')
PROFILE='all-routes-unified-v3144'
PARENT=Path('out/all_routes_combined_v3103_candidate.nds')
DOC=Path('translations/lil_crew_items_editorial_manuscript_v8.json')
MAP=Path('translations/lil_crew_items_editorial_relocation_map_v1.json')
CHOICE=Path('translations/lil_crew_items_choice_manuscript_v3.json')

if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists()
    rp,builder=Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py')
    raw,before=rp.read_bytes(),builder.read_bytes();registry=read(rp)
    assert PROFILE not in registry['profiles'] and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
    parent=NdsImage.open(PARENT);base=NdsImage.open('out/raphael_natural_v2_accepted_base.nds');doc,mapping=read(DOC),read(MAP)
    assert sha(PARENT.read_bytes())==doc['current_ROM_sha256']
    deps={str(DOC),str(CHOICE),str(MAP),str(Path(owned.__file__)),__file__,
        'dk4tool/dialogue/lil_crew_items_profile.py','dk4tool/dialogue/encoder.py','dk4tool/dialogue/qa.py','dk4tool/dialogue/review.py','dk4tool/dialogue/lil_crew_items_layout_v2.py','dk4tool/dialogue/layout.py',
        doc['source_context'],doc['control_contract'],doc['branch_proof'],doc['native_font_proof'],doc['representative_proof'],
        doc['historical_representative_sheet_review'],doc['prior_current_sheet_review'],doc['final_padding_proof'],
        mapping['source_plan'],mapping['source_census'],
        'work/analysis/lil_Crew_Items_reference_approval_v3142/approval_receipt.json',
        'work/analysis/lil_Crew_Items_loader_v3139/whole_SC2_and_fourteen_selected_blocks_initial_entry_proof.json',
        'scripts/research_lil_crew_items_relocation_v3137.py','scripts/prepare_lil_crew_items_research_v3138.py',
        'scripts/verify_lil_crew_items_loader_v3139.py','scripts/verify_lil_crew_items_references_v3140.py',
        'scripts/reconcile_lil_crew_items_sampling_v3141b.py','scripts/seal_lil_crew_items_references_v3142.py',
        'scripts/prove_lil_crew_items_controls_v3114.py','scripts/verify_lil_crew_items_fonts_v3133.py',
        'docs/editorial_testing_scope_v1870.md'}
    font=read(doc['native_font_proof']);deps.update(doc[k] for k in ['native_progressive_proof','native_FE_proof','native_choice_proof'])
    for native in read(doc['native_choice_proof'])['menus']:deps.add(native['proof'])
    deps.add(doc['item_terminology_reconciliation'])
    deps.update(['scripts/author_lil_crew_items_v3121.py','scripts/refine_lil_crew_items_v3124.py','scripts/refine_lil_crew_items_final_v3126.py','scripts/refine_lil_crew_items_visual_v3131.py','scripts/prove_lil_crew_items_choices_v3130.py'])
    deps.update(['scripts/lil_islands_miracles_food_prose_v3117.py','scripts/lil_sword_ninja_amber_prose_v3118.py','scripts/lil_julio_samwell_items_prose_v3119.py','scripts/lil_telescope_pot_muramasa_prose_v3120.py'])
    deps.add(doc['whole_exchange_context_notes'])
    for p in list(deps):
        if Path(p).suffix=='.json':
            item=read(p)
            for key in ['evidence','hashes']:
                if isinstance(item.get(key),dict):deps.update(p for p in item[key] if Path(p).is_file())
    for p in [doc['historical_representative_sheet_review'],doc['prior_current_sheet_review']]:deps.add(read(p)['sheet'])
    deps.update(s['path'] for s in font['all26_review_sheets'])
    for panel in read(doc['native_FE_proof'])['cases']:deps.update([panel['native_plane'],panel['preview']])
    deps.update(['scripts/verify_lil_crew_items_FE_v3129.py','scripts/lil_kuhn_china_FE_painter_v2909.py','scripts/approve_lil_crew_items_fonts_v3134.py'])
    conf=dict(format='dk4-lil-crew-items-editorial-release-v1',manuscript=str(DOC),choices=str(CHOICE),reference_map=str(MAP),
        required_runtime_arm9_sha256=sha(parent.read_file('/__arm9__.bin')),source_SC2_sha256=mapping['source_SC2_sha256'],target_SC2_sha256=mapping['target_SC2_sha256'],
        canonical_SC2_sha256=mapping['canonical_SC2_sha256'],clean_SC2_sha256=mapping['clean_SC2_sha256'],clean_ROM='work/clean.nds',clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),
        dependencies={p:sha(Path(p).read_bytes()) for p in sorted(deps)})
    ROOT.mkdir(parents=True);positive=ROOT/'positive_config.json';save(positive,conf)
    test=NdsImage.open(PARENT);proof=owned.apply_release(test,base,positive)
    assert test.read_file(owned.PATH)==Path('work/analysis/lil_Crew_Items_relocation_v3137/SC2_RESEARCH_ONLY.DK4').read_bytes()
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
    def worker(d):return next(r for r in d['records'] if r['source_presentation_prefix_hex']=='6c')
    def named(d):return next(r for r in d['records'] if '{MACRO:FI}' in r['english'])
    changes=[('missing_format_review',str(DOC),'manuscript',lambda d:d['records'][0]['review'].update(formatting=False)),
        ('wrong_Japanese_source',str(DOC),'manuscript',lambda d:d['records'][0].update(source_hex='00')),
        ('wrong_consumer',str(DOC),'manuscript',lambda d:d['records'][0].update(native_display_consumer='original_FE_modal_5473C_mode1')),
        ('missing_printable_speaker',str(DOC),'manuscript',lambda d:worker(d).update(english=worker(d)['english'].replace('{SPEAKER:6C}',''))),
        ('wrong_printable_speaker',str(DOC),'manuscript',lambda d:worker(d).update(english=worker(d)['english'].replace('SPEAKER:6C','SPEAKER:02'))),
        ('invented_macro',str(DOC),'manuscript',lambda d:d['records'][0].update(english=d['records'][0]['english']+' {MACRO:FI}')),
        ('changed_approved_prose',str(DOC),'manuscript',lambda d:d['records'][0].update(english='{SPEAKER:04}My fleet was destroyed.')),
        ('missing_source_name_macro',str(DOC),'manuscript',lambda d:named(d).update(english=named(d)['english'].replace('{MACRO:FI}','Lil'))),
        ('wrong_complete_preamble',str(DOC),'manuscript',lambda d:d['records'][0].update(source_complete_preamble_hex='0040ffff005c')),
        ('missing_reference_approval',str(MAP),'reference_map',lambda d:d.update(external_references_complete=False)),
        ('wrong_mapped_command',str(MAP),'reference_map',lambda d:d['blocks'][0]['mapped_native_commands'][0].update(new_offset=10)),
        ('wrong_relative_target',str(MAP),'reference_map',lambda d:next(b for b in d['blocks'] if b['relative_skip_fixups'])['relative_skip_fixups'][0].update(new_matched_skip_target=0)),
        ('missing_relocated_predicate_approval',str(MAP),'reference_map',lambda d:d.update(no_predicate_or_event_query_commands_in_selected_blocks=False)),
        ('choice_result_swapped',str(CHOICE),'choices',lambda d:d['records'][0].update(option_index=1)),
        ('choice_authored_padding',str(CHOICE),'choices',lambda d:d['records'][0].update(english=' Be generous.')),
        ('changed_approved_choice',str(CHOICE),'choices',lambda d:d['records'][0].update(english='Pay me again!')),
        ('wrong_source_bound_formatter',str(DOC),'manuscript',lambda d:d.update(native_formatter_module='dk4tool/dialogue/encoder.py'))]
    def FErow(d):return next(r for r in d['records'] if r['kind']=='system-FE')
    def retainer(d):return next(r for r in d['records'] if r['source_presentation_prefix_hex']=='bc')
    changes.extend([
        ('FE_wrong_consumer',str(DOC),'manuscript',lambda d:FErow(d).update(native_display_consumer='original_progressive_54020')),
        ('FE_invented_name_macro',str(DOC),'manuscript',lambda d:FErow(d).update(english=FErow(d)['english']+' {MACRO:FI}')),
        ('FE_converted_selector',str(DOC),'manuscript',lambda d:FErow(d).update(source_hex='f8f2'+FErow(d)['source_hex'][2:])),
        ('FE_as_ordinary_actor',str(DOC),'manuscript',lambda d:FErow(d).update(english=FErow(d)['english'].replace('SPEAKER:FE','SPEAKER:02'))),
        ('FE_invented_speaker_label',str(DOC),'manuscript',lambda d:FErow(d).update(english=FErow(d)['english'].replace('}', '}Sailor: ',1))),
        ('missing_BC_actor_state',str(DOC),'manuscript',lambda d:retainer(d).update(english=retainer(d)['english'].replace('{SPEAKER:BC}',''))),
        ('wrong_legal_BC_actor',str(DOC),'manuscript',lambda d:retainer(d).update(english=retainer(d)['english'].replace('SPEAKER:BC','SPEAKER:02')))])
    def FEname(d):return next(r for r in d['records'] if r['kind']=='system-FE' and '{MACRO:FI}' in r['english'])
    def FEFernando(d):return next(r for r in d['records'] if r['kind']=='system-FE' and 'Fernando' in r['english'])
    changes.extend([
        ('FE_missing_source_FI',str(DOC),'manuscript',lambda d:FEname(d).update(english=FEname(d)['english'].replace('{MACRO:FI}','Lil'))),
        ('FE_stat_term_swapped',str(DOC),'manuscript',lambda d:FEname(d).update(english=FEname(d)['english'].replace('Luck','Spirit'))),
        ('FE_named_subject_replaced',str(DOC),'manuscript',lambda d:FEFernando(d).update(english=FEFernando(d)['english'].replace("Fernando's",'His')))])
    for label,path,key,mutate in changes:
        value=read(path);mutate(value);mp=ROOT/(label+'.json');save(mp,value)
        cfg=deepcopy(conf);cfg[key]=str(mp);cfg['dependencies'][str(mp)]=sha(mp.read_bytes());cp=ROOT/(label+'_config.json');save(cp,cfg)
        reject(label,NdsImage.open(PARENT),base,cp)
    assert len(negative)==31;save(ROOT/'negative_cases.json',dict(cases=negative,all_rejected_before_mutation=True))
    stage=b'''    lil_crew_items = profile_config.get('lil_crew_items_editorial')
    if lil_crew_items:
        from dk4tool.patch.lil_crew_items_editorial import apply_release as apply_lil_crew_items

        lil_crew_items_report = apply_lil_crew_items(candidate, baseline, lil_crew_items)
        grouped.setdefault('/data/SC2.DK4', [])
        changed_records.setdefault('/data/SC2.DK4', []).extend(row['id'] for row in lil_crew_items_report['changed_records'])
        relocation_checks.setdefault('/data/SC2.DK4', {})['lil_crew_items_editorial'] = {
            'release_config': lil_crew_items,
            'release_config_sha256': sha256(Path(lil_crew_items).read_bytes()),
            'proof': lil_crew_items_report}
        for crew_items_key in ('manuscript', 'choices'):
            crew_items_batch = Path(lil_crew_items_report[crew_items_key])
            if crew_items_batch in release_batches:
                raise ValueError('Crew/Items must run once after the complete V3103 stack')
            release_batches.append(crew_items_batch)

'''
    anchor=b'    # Lexically valid "% o"';assert before.count(anchor)==1 and b"profile_config.get('lil_crew_items_editorial')" not in before
    after=before.replace(anchor,stage+anchor);compile(after,str(builder),'exec')
    (ROOT/'registry_before_raw.json').write_bytes(raw);(ROOT/'builder_before.py').write_bytes(before);(ROOT/'builder_added_optional_stage.bin').write_bytes(stage)
    save(owned.CONFIG,conf)
    profile=deepcopy(registry['profiles']['all-routes-unified-v3103']);profile.update(lil_crew_items_editorial=owned.CONFIG,
        description='Full V3103 cumulative stack plus200 contextual crew and item reviews across14SC2blocks.',
        note='123revisions/77justifiedretentions;191ordinary/sevenFE/two choices.198nativeplanes/1584logical-compiled/792finalparity macro cases;8menuplanes/6VMreturns.268commands/fourrelative spans/20relocatedcases/no predicates orqueries/336wholeloaders/two parentmodes/threeentrycensuses. All26sheets viewed oridentical;64rowcount-onlynotes. Preserve source beliefs/rumors/uncertainty,ten approveditem names,Luck/Spirit distinction,two nullactorFI substitutions,three unlabeledmonkey calls,Julio granddaughter relationship,source ninja death consequence andAthena/Minerva character dialogue. Source generic Katzbalger staysgeneric. No invented kinship,rank,confirmedrumors or earneditems/stats. Sharedactual rules inheritbyexactbytes. No selectedscene/newnameplate/fullroute orhardware claim. Registeredbuild/exactcleanpatch/currentstartup pending. Experimental;preserve everyROM/translation;no promotion.')
    registry['profiles'][PROFILE]=profile
    assert rp.read_bytes()==raw and builder.read_bytes()==before
    pending=rp.with_name('release_stack_v3143_pending.json');assert not pending.exists();save(pending,registry)
    builder.write_bytes(after);os.replace(pending,rp)
    restored=deepcopy(read(rp));restored['profiles'].pop(PROFILE)
    assert restored==read(ROOT/'registry_before_raw.json') and builder.read_bytes().replace(stage,b'',1)==before
    save(ROOT/'registration_receipt.json',dict(profile=PROFILE,parent_profile='all-routes-unified-v3103',config=owned.CONFIG,config_sha256=sha(Path(owned.CONFIG).read_bytes()),
        negative_cases=31,all114accepted_layers_previous_profiles_and_V1492_promotion_unchanged=True,only_one_optional_stage_and_one_experimental_profile_added=True,
        release_stack_sha256=sha(rp.read_bytes()),builder_sha256=sha(builder.read_bytes()),no_ROM_created_or_promoted=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('RegisteredV3144 optional200-object stage after fullV3103;31negative cases reject before mutation;all previous profiles/114accepted layers preserved.')
