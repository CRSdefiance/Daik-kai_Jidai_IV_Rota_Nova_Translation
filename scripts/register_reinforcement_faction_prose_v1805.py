"""Register a six-paragraph exact-slot late layer after all V1775 stages."""
from copy import deepcopy
from pathlib import Path
import os
from dk4tool.patch import reinforcement_faction_prose as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET,TABLE_OFFSET
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/reinforcement_faction_release_v1805')
PROFILE='all-routes-unified-v1807'
PARENT=Path('out/all_routes_combined_v1775_candidate.nds')
DOC=Path('translations/reinforcement_sniping_editorial_manuscript_v4.json')

if __name__=='__main__':
    assert not ROOT.exists()and not Path(owned.CONFIG).exists()
    image=NdsImage.open(PARENT);base=NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    assert sha(PARENT.read_bytes())=='6bc6b6bb01f9ea0e763ee1d6c4c3f2bcb1c7c8cca3be3dd54bd43903045cb55a'
    arm=image.read_file('/__arm9__.bin');common=image.read_file(owned.PATH);doc=read(DOC)
    directory=sha(arm[DIRECTORY_OFFSET:TABLE_OFFSET]);target,plan=owned.transform(common,arm,doc,directory)
    assert len(plan['changed_records'])==6
    files={str(DOC),str(Path(owned.__file__)),__file__,'scripts/reinforcement_sniping_layout_v1024.py',
        'dk4tool/patch/common_single_cache_v861.py','dk4tool/dialogue/review.py',
        doc['successor_native_format_proof'],doc['successor_visual_review_proof'],doc['unchanged14_current_format_proof'],
        'scripts/approve_reinforcement_prose_v1803.py','scripts/revise_reinforcement_faction_prose_v1802.py',
        'translations/reinforcement_sniping_editorial_manuscript_v2.json'}
    for proof,key in ((read(doc['successor_native_format_proof']),'all120_cases'),
                      (read(doc['unchanged14_current_format_proof']),'fresh_current_complete_native_font_samples')):
        files.update(r['preview']for r in proof[key]);files.update(r['path']for r in proof['review_sheets'])
    config={'format':'dk4-reinforcement-faction-prose-v1','manuscript':str(DOC),
        'source_COMMON_sha256':sha(common),'target_COMMON_sha256':sha(target),'required_ARM9_sha256':sha(arm),
        'canonical_COMMON_sha256':sha(base.read_file(owned.PATH)),'directory_sha256':directory,
        'clean_ROM':'work/clean.nds','clean_ROM_sha256':sha(Path('work/clean.nds').read_bytes()),
        'dependencies':{p:sha(Path(p).read_bytes())for p in sorted(files)}}
    rp,builder=Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py')
    registry_raw,before=rp.read_bytes(),builder.read_bytes();registry=read(rp)
    assert PROFILE not in registry['profiles']and len(registry['accepted_layers'])==114
    assert registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
    stage=b'''    reinforcement_faction_prose = profile_config.get('reinforcement_faction_prose')
    if reinforcement_faction_prose:
        from dk4tool.patch.reinforcement_faction_prose import apply_release as apply_reinforcement_faction_prose

        faction_report = apply_reinforcement_faction_prose(candidate, baseline, reinforcement_faction_prose)
        file_path = '/COMMON/MESFILE.DK4'
        grouped.setdefault(file_path, [])
        changed_records.setdefault(file_path, []).extend(row['id'] for row in faction_report['changed_records'])
        relocation_checks.setdefault(file_path, {})['reinforcement_faction_prose'] = {
            'release_config': reinforcement_faction_prose,
            'release_config_sha256': sha256(Path(reinforcement_faction_prose).read_bytes()),
            'proof': faction_report}
        faction_batch = Path(faction_report['manuscript'])
        if faction_batch in release_batches:
            raise ValueError('Faction prose must run only after the frozen cumulative stages')
        release_batches.append(faction_batch)

'''
    anchor=b'    # Lexically valid "% o"';assert before.count(anchor)==1
    assert b"profile_config.get('reinforcement_faction_prose')"not in before
    at=before.index(anchor);after=before[:at]+stage+before[at:];compile(after,str(builder),'exec')
    ROOT.mkdir(parents=True);(ROOT/'registry_before_raw.json').write_bytes(registry_raw)
    (ROOT/'builder_before.py').write_bytes(before);(ROOT/'builder_added_optional_stage.bin').write_bytes(stage)
    save(owned.CONFIG,config);proof=owned.apply_release(image,base);assert image.read_file(owned.PATH)==target
    save(ROOT/'source_bound_late_layer_plan.json',proof)
    negatives=[]
    def reject(label,working,baseline,conf):
        c,a=working.read_file(owned.PATH),working.read_file('/__arm9__.bin')
        try:owned.apply_release(working,baseline,conf)
        except(ValueError,AssertionError)as error:
            assert working.read_file(owned.PATH)==c and working.read_file('/__arm9__.bin')==a
            negatives.append({'case':label,'rejection':str(error),'no_partial_mutation':True})
        else:raise AssertionError('Accepted invalid release:'+label)
    reject('repeat_application',image,base,owned.CONFIG)
    wrong=NdsImage.open(PARENT);a=bytearray(arm);a[256]^=1;wrong.replace_file('/__arm9__.bin',bytes(a))
    reject('wrong_runtime',wrong,base,owned.CONFIG)
    wrong=NdsImage.open('out/raphael_natural_v2_accepted_base.nds');c=bytearray(wrong.read_file(owned.PATH));c[32]^=1;wrong.replace_file(owned.PATH,bytes(c))
    reject('wrong_canonical_source',NdsImage.open(PARENT),wrong,owned.CONFIG)
    for label,mutator in [('unreviewed_formatting',lambda d:d['records'][0]['review'].update(formatting=False)),
        ('changed_Japanese',lambda d:d['records'][0].update(source_hex='00')),
        ('wrong_current_paragraph',lambda d:d['records'][0].update(current_text_hex='00')),
        ('oversized_paragraph',lambda d:d['records'][0].update(english='Admiral! '+('Complete source words. '*6)))]:
        changed=deepcopy(doc);mutator(changed);p=ROOT/(label+'.json');save(p,changed)
        conf=deepcopy(config);conf['manuscript']=str(p);conf['dependencies'][str(p)]=sha(p.read_bytes())
        cp=ROOT/(label+'_config.json');save(cp,conf);reject(label,NdsImage.open(PARENT),base,cp)
    profile=deepcopy(registry['profiles']['all-routes-unified-v1775'])
    profile.update(reinforcement_faction_prose=owned.CONFIG,status='experimental',
        description='Complete V1775 stack plus six natural faction assistance paragraphs in original native allocations.',
        note='Only COMMON1911-1916 text changes;native offsets/copy extents,ARM9,fonts,graphics andall other messages exact. Full gameplay review pending;V1492 remains promoted.')
    registry['profiles'][PROFILE]=profile
    assert rp.read_bytes()==registry_raw and builder.read_bytes()==before
    tmp=rp.with_name('release_stack_v1805_pending.json');assert not tmp.exists();save(tmp,registry)
    builder.write_bytes(after);os.replace(tmp,rp)
    restored=deepcopy(read(rp));restored['profiles'].pop(PROFILE);assert restored==read(ROOT/'registry_before_raw.json')
    assert builder.read_bytes().replace(stage,b'',1)==before
    save(ROOT/'registration_provenance.json',{'profile':PROFILE,'source_profile':'all-routes-unified-v1775',
        'all_prior_profiles_accepted_layers_batches_and_promotion_preserved':True,'negative_cases':negatives,
        'builder_before_sha256':sha(before),'builder_after_sha256':sha(after),'registry_before_sha256':sha(registry_raw),
        'registry_after_sha256':sha(rp.read_bytes()),'only_new_optional_stage_before_existing_final_guards':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print({'profile':PROFILE,'six_exact_allocation_paragraphs':6,'negative_cases':len(negatives),'registered_build_pending':True},flush=True)
