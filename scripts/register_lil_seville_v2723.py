"""Validate and register one optional stage after the full V2674 stack."""
import os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import lil_seville_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Seville_registration_v2723')
PROFILE='all-routes-unified-v2724'
PARENT=Path('out/all_routes_combined_v2674_candidate.nds')
DOC=Path('translations/lil_seville_encounter_editorial_manuscript_v4.json')
CHOICE=Path('translations/lil_seville_choices_editorial_draft_v3.json')
MAP=Path('translations/lil_seville_editorial_relocation_map_v1.json')

if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists()
    rp=Path('translations/release_stack.json');builder=Path('scripts/build_integrated_release.py')
    raw,before=rp.read_bytes(),builder.read_bytes();registry=read(rp)
    assert PROFILE not in registry['profiles'] and len(registry['accepted_layers'])==114
    assert registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
    parent=NdsImage.open(PARENT);baseline=NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    mapping,doc=read(MAP),read(DOC)
    assert sha(PARENT.read_bytes())==doc['current_ROM_sha256']
    deps={str(DOC),str(CHOICE),str(MAP),str(Path(owned.__file__)),__file__,
        'dk4tool/dialogue/lil_seville_profile.py','dk4tool/dialogue/review.py','dk4tool/dialogue/encoder.py',
        doc['native_font_proof'],doc['native_progressive_proof'],doc['native_FE_proof'],doc['native_choice_proof'],
        doc['source_context'],doc['control_contract'],doc['branch_proof'],
        doc['representative_proof'],doc['representative_sheet_review'],mapping['source_plan'],mapping['source_census'],
        'work/analysis/lil_Seville_reference_approval_v2722/approval_receipt.json',
        'work/analysis/lil_Seville_research_v2718/research_image_receipt.json',
        'work/analysis/lil_Seville_loader_v2719/whole_SC2_and_B28_B29_initial_entry_proof.json',
        'docs/editorial_testing_scope_v1870.md'}
    for path in list(deps):
        if Path(path).suffix=='.json':
            item=read(path)
            for key in ['evidence','hashes']:
                if isinstance(item.get(key),dict):deps.update(p for p in item[key] if Path(p).is_file())
    sheet=read(doc['representative_sheet_review']);deps.add(sheet['sheet'])
    conf=dict(format='dk4-lil-seville-editorial-release-v1',manuscript=str(DOC),choices=str(CHOICE),reference_map=str(MAP),
        required_runtime_arm9_sha256=sha(parent.read_file('/__arm9__.bin')),
        source_SC2_sha256=mapping['source_SC2_sha256'],target_SC2_sha256=mapping['target_SC2_sha256'],
        canonical_SC2_sha256=mapping['canonical_SC2_sha256'],clean_SC2_sha256=mapping['clean_SC2_sha256'],
        clean_ROM='work/clean.nds',clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),
        dependencies={p:sha(Path(p).read_bytes()) for p in sorted(deps)})
    ROOT.mkdir(parents=True);positive=ROOT/'positive_config.json';save(positive,conf)
    test=NdsImage.open(PARENT);proof=owned.apply_release(test,baseline,positive)
    assert test.read_file(owned.PATH)==Path('work/analysis/lil_Seville_relocation_v2716/SC2_RESEARCH_ONLY.DK4').read_bytes()
    assert test.read_file('/__arm9__.bin')==parent.read_file('/__arm9__.bin')
    save(ROOT/'positive_reconstruction.json',proof);negative=[]
    def reject(label,image,base,config):
        initial=(image.read_file(owned.PATH),image.read_file('/__arm9__.bin'))
        try:owned.apply_release(image,base,config)
        except (AssertionError,ValueError):
            assert (image.read_file(owned.PATH),image.read_file('/__arm9__.bin'))==initial
            negative.append(dict(case=label,rejected_before_mutation=True))
        else:raise AssertionError(label)
    reject('repeated_application',test,baseline,positive)
    for label,path in [('wrong_SC2',owned.PATH),('wrong_ARM9','/__arm9__.bin')]:
        image=NdsImage.open(PARENT);data=bytearray(image.read_file(path));data[256]^=1;image.replace_file(path,bytes(data));reject(label,image,baseline,positive)
    base=NdsImage.open('out/raphael_natural_v2_accepted_base.nds');data=bytearray(base.read_file(owned.PATH));data[32]^=1;base.replace_file(owned.PATH,bytes(data));reject('wrong_canonical',NdsImage.open(PARENT),base,positive)
    mutations=[('missing_format_review',str(DOC),'manuscript',lambda d:d['records'][0]['review'].update(formatting=False)),
        ('wrong_Japanese_source',str(DOC),'manuscript',lambda d:d['records'][0].update(source_hex='00')),
        ('wrong_consumer',str(DOC),'manuscript',lambda d:d['records'][0].update(native_display_consumer='original_FE_modal_5473C_mode1')),
        ('missing_speaker',str(DOC),'manuscript',lambda d:d['records'][0].update(english='You are here.')),
        ('invented_macro',str(DOC),'manuscript',lambda d:d['records'][0].update(english='{SPEAKER:1F}{MACRO:FI}You are here.')),
        ('changed_font_approved_prose',str(DOC),'manuscript',lambda d:d['records'][0].update(english='{SPEAKER:1F}You are here.')),
        ('choice_result_swapped',str(CHOICE),'choices',lambda d:d['records'][0].update(option_index=1)),
        ('choice_authored_alignment',str(CHOICE),'choices',lambda d:d['records'][0].update(english=' All right.')),
        ('missing_reference_approval',str(MAP),'reference_map',lambda d:d.update(external_references_complete=False)),
        ('wrong_command_map',str(MAP),'reference_map',lambda d:d['blocks'][0]['mapped_native_commands'][0].update(new_offset=10)),
        ('wrong_relative_target',str(MAP),'reference_map',lambda d:d['blocks'][0]['relative_skip_fixups'][0].update(new_matched_skip_target=152))]
    for label,path,key,mutate in mutations:
        data=read(path);mutate(data);mp=ROOT/(label+'.json');save(mp,data)
        cfg=deepcopy(conf);cfg[key]=str(mp);cfg['dependencies'][str(mp)]=sha(mp.read_bytes());cp=ROOT/(label+'_config.json');save(cp,cfg)
        reject(label,NdsImage.open(PARENT),baseline,cp)
    assert len(negative)==15;save(ROOT/'negative_cases.json',dict(cases=negative,all_rejected_before_mutation=True))
    stage=b'''    lil_seville = profile_config.get('lil_seville_editorial')
    if lil_seville:
        from dk4tool.patch.lil_seville_editorial import apply_release as apply_lil_seville

        lil_seville_report = apply_lil_seville(candidate, baseline, lil_seville)
        grouped.setdefault('/data/SC2.DK4', [])
        changed_records.setdefault('/data/SC2.DK4', []).extend(row['id'] for row in lil_seville_report['changed_records'])
        relocation_checks.setdefault('/data/SC2.DK4', {})['lil_seville_editorial'] = {
            'release_config': lil_seville,
            'release_config_sha256': sha256(Path(lil_seville).read_bytes()),
            'proof': lil_seville_report}
        for seville_key in ('manuscript', 'choices'):
            seville_batch = Path(lil_seville_report[seville_key])
            if seville_batch in release_batches:
                raise ValueError('Seville must run once after the complete V2674 stack')
            release_batches.append(seville_batch)

'''
    anchor=b'    # Lexically valid "% o"'
    assert before.count(anchor)==1 and b"profile_config.get('lil_seville_editorial')" not in before
    after=before.replace(anchor,stage+anchor);compile(after,str(builder),'exec')
    (ROOT/'registry_before_raw.json').write_bytes(raw);(ROOT/'builder_before.py').write_bytes(before);(ROOT/'builder_added_optional_stage.bin').write_bytes(stage)
    save(owned.CONFIG,conf)
    profile=deepcopy(registry['profiles']['all-routes-unified-v2674']);profile.update(lil_seville_editorial=owned.CONFIG,
        description='Complete V2674 cumulative stack plus Lil Seville B28/B29 contextual review:18speech/system paragraphs and two typed replies.',
        note='17prose revisions,3justified retentions. Source-bound current native fonts,144macro and72final-padding alignment calls,69commands,28relative sites,336loaders/two-parent-modes and representative shared gameplay rules approved. No individual Seville activation claimed. Registered build,clean patch,current startup pending. Experimental;preserve every ROM;no promotion.')
    registry['profiles'][PROFILE]=profile
    assert rp.read_bytes()==raw and builder.read_bytes()==before
    pending=rp.with_name('release_stack_v2723_pending.json');assert not pending.exists();save(pending,registry)
    builder.write_bytes(after);os.replace(pending,rp)
    restored=deepcopy(read(rp));restored['profiles'].pop(PROFILE)
    assert restored==read(ROOT/'registry_before_raw.json') and builder.read_bytes().replace(stage,b'',1)==before
    save(ROOT/'registration_receipt.json',dict(profile=PROFILE,parent_profile='all-routes-unified-v2674',config=owned.CONFIG,
        config_sha256=sha(Path(owned.CONFIG).read_bytes()),negative_cases=len(negative),
        all114accepted_layers_previous_profiles_and_V1492_promotion_unchanged=True,
        only_one_optional_stage_and_one_experimental_profile_added=True,
        release_stack_sha256=sha(rp.read_bytes()),builder_sha256=sha(builder.read_bytes()),
        no_ROM_created_or_promoted=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Registered V2724 optional Seville stage after fullV2674;15 negative cases reject before mutation;all previous profiles preserved.')
