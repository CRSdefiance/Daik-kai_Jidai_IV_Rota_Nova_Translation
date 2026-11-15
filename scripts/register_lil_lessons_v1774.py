"""Register reviewed branching lessons after the entire frozen V1711 stack."""
from copy import deepcopy
import os
from pathlib import Path
from dk4tool.patch import lil_lessons_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_lessons_release_v1774')
PROFILE='all-routes-unified-v1775'

if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists()
    parent=Path('out/all_routes_combined_v1711_candidate.nds');base_path=Path('out/raphael_natural_v2_accepted_base.nds')
    assert sha(parent.read_bytes())=='251594f89f950f1deb68d6359b6861d6f4a96eb8e9a9045c148d6d6cb64b1201'
    assert sha(base_path.read_bytes())=='3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
    image,base,clean=NdsImage.open(parent),NdsImage.open(base_path),NdsImage.open('work/clean.nds')
    manuscript=Path('translations/lil_lessons_editorial_manuscript_v5.json');doc=read(manuscript)
    choices=Path('translations/lil_lesson_choices_editorial_draft_v2.json');choice_doc=read(choices)
    map_path=Path('translations/lil_lessons_editorial_relocation_map_v1.json');mapping=read(map_path)
    research=read('work/analysis/lil_lessons_research_v1761/research_image_receipt.json')
    assert mapping['external_references_complete']
    files={str(manuscript),str(choices),str(map_path),'dk4tool/patch/lil_lessons_editorial.py',
        'dk4tool/dialogue/profiles.py','dk4tool/dialogue/layout.py','dk4tool/dialogue/encoder.py',
        'dk4tool/dialogue/codec.py','dk4tool/dialogue/review.py','translations/lil_opening_editorial_release_v1.json',
        doc['source_context'],doc['native_font_proof'],doc['actual_context_FE_proof'],doc['visual_review'],
        choice_doc['native_label_pointer_proof'],choice_doc['original_choice_UI_proof'],choice_doc['visual_review'],
        'scripts/approve_lil_lessons_references_v1773.py','scripts/verify_lil_sailing_choice0_v1772c.py',__file__}
    files.update(mapping['evidence'])
    font=read(doc['native_font_proof']);files.update(r['preview']for r in font['cases'])
    for r in read(doc['actual_context_FE_proof'])['reviewed_cases']:files.add(r['display_preview'])
    for path in mapping['evidence']:
        proof=read(path)
        for r in proof.get('actual_review_sheets',[]):files.add(r['path'])
    config={'format':'dk4-lil-lessons-editorial-release-v1','manuscript':str(manuscript),'choices':str(choices),
        'reference_map':str(map_path),'source_SC2_sha256':sha(image.read_file(owned.PATH)),
        'target_SC2_sha256':research['SC2_sha256'],'canonical_SC2_sha256':sha(base.read_file(owned.PATH)),
        'clean_ROM':'work/clean.nds','clean_ROM_sha256':sha(Path('work/clean.nds').read_bytes()),
        'clean_SC2_sha256':sha(clean.read_file(owned.PATH)),
        'required_runtime_arm9_sha256':sha(image.read_file('/__arm9__.bin')),
        'dependencies':{name:sha(Path(name).read_bytes())for name in sorted(files)}}
    rp,builder=Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py')
    registry_raw,before=rp.read_bytes(),builder.read_bytes();registry=read(rp)
    assert PROFILE not in registry['profiles'] and len(registry['accepted_layers'])==114
    assert registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
    assert b"profile_config.get('lil_lessons_editorial')" not in before
    stage=b'''    lil_lessons_editorial = profile_config.get('lil_lessons_editorial')
    if lil_lessons_editorial:
        from dk4tool.patch.lil_lessons_editorial import apply_release as apply_lil_lessons_editorial

        lesson_report = apply_lil_lessons_editorial(candidate, baseline, lil_lessons_editorial)
        file_path = '/data/SC2.DK4'
        grouped.setdefault(file_path, [])
        changed_records.setdefault(file_path, []).extend(row['id'] for row in lesson_report['changed_records'])
        relocation_checks.setdefault(file_path, {})['lil_lessons_editorial'] = {
            'release_config': lil_lessons_editorial,
            'release_config_sha256': sha256(Path(lil_lessons_editorial).read_bytes()),
            'proof': lesson_report}
        for name in ('manuscript', 'choices'):
            lesson_batch = Path(lesson_report[name])
            if lesson_batch in release_batches:
                raise ValueError('Lil lessons must run only after the frozen cumulative stages')
            release_batches.append(lesson_batch)

'''
    anchor=b'    # Lexically valid "% o"';assert before.count(anchor)==1
    at=before.index(anchor);after=before[:at]+stage+before[at:];compile(after,str(builder),'exec')
    ROOT.mkdir(parents=True)
    (ROOT/'registry_before_raw.json').write_bytes(registry_raw);(ROOT/'builder_before.py').write_bytes(before)
    (ROOT/'builder_added_optional_stage.bin').write_bytes(stage)
    save(owned.CONFIG,config)
    plan=owned.apply_release(image,base,owned.CONFIG)
    assert sha(image.read_file(owned.PATH))==research['SC2_sha256']
    assert [(b['block'],b['growth_bytes'])for b in plan['blocks']]==[(120,240),(23,284)]
    save(ROOT/'native_source_release_plan.json',plan)
    negatives=[]
    def reject(label,working,baseline,conf,fragment):
        before_bytes=working.read_file(owned.PATH);runtime=working.read_file('/__arm9__.bin')
        try:owned.apply_release(working,baseline,conf)
        except ValueError as error:
            assert fragment in str(error),(label,str(error))
            assert working.read_file(owned.PATH)==before_bytes and working.read_file('/__arm9__.bin')==runtime
            negatives.append({'case':label,'rejection':str(error),'no_partial_script_or_runtime_mutation':True})
        else:raise AssertionError('Invalid lesson release accepted:'+label)
    reject('repeat_application',image,base,owned.CONFIG,'current/canonical source')
    wrong=NdsImage.open(parent);arm=bytearray(wrong.read_file('/__arm9__.bin'));arm[0x100]^=1;wrong.replace_file('/__arm9__.bin',bytes(arm))
    reject('wrong_runtime',wrong,base,owned.CONFIG,'proven native runtime')
    wrong_base=NdsImage.open(base_path);script=bytearray(wrong_base.read_file(owned.PATH));script[20]^=1;wrong_base.replace_file(owned.PATH,bytes(script))
    reject('wrong_canonical_source',NdsImage.open(parent),wrong_base,owned.CONFIG,'current/canonical source')
    def altered(label,field,document,mutator,fragment):
        changed=deepcopy(document);mutator(changed);path=ROOT/(label+'.json');save(path,changed)
        conf=deepcopy(config);conf[field]=str(path);conf['dependencies'][str(path)]=sha(path.read_bytes())
        cp=ROOT/(label+'_config.json');save(cp,conf)
        reject(label,NdsImage.open(parent),base,cp,fragment)
    altered('incomplete_map','reference_map',mapping,lambda d:d.update(external_references_complete=False),'complete source reference map')
    altered('wrong_relative_destination','reference_map',mapping,
        lambda d:d['blocks'][0]['relative_skip_fixups'][0].update(new_matched_skip_target=d['blocks'][0]['relative_skip_fixups'][0]['new_matched_skip_target']+2),
        'relative operand or destination')
    altered('unreviewed_formatting','manuscript',doc,lambda d:d['records'][0]['review'].update(formatting=False),'per-record source')
    altered('wrong_source_speaker','manuscript',doc,
        lambda d:d['records'][0].update(source_hex='09'+d['records'][0]['source_hex'][2:]),'Japanese/current speech or speaker')
    altered('changed_choice_label','choices',choice_doc,lambda d:d['records'][0].update(english='Sure!'),'approved typed choice object')
    profile=deepcopy(registry['profiles']['all-routes-unified-v1711'])
    profile.update(lil_lessons_editorial=owned.CONFIG,status='experimental',
        description='Complete V1711 stack plus60 reviewed Lil lesson speeches/system panels and4 typed choice labels.',
        note='SC2 B120 +240 andB23 +284 bytes only;all124 nested commands36 relative operands,native choice consumers andboth responses each verified.55 individual actual speech IDs,5 explicit identical native equivalents. Registered build/patch/startup gates pending. V1492 remains promoted.')
    registry['profiles'][PROFILE]=profile
    assert rp.read_bytes()==registry_raw and builder.read_bytes()==before
    temporary=rp.with_name('release_stack_v1774_pending.json');assert not temporary.exists()
    save(temporary,registry);assert read(temporary)==registry and rp.read_bytes()==registry_raw
    builder.write_bytes(after);os.replace(temporary,rp)
    restored=deepcopy(read(rp));restored['profiles'].pop(PROFILE)
    assert restored==read(ROOT/'registry_before_raw.json') and builder.read_bytes().replace(stage,b'',1)==before
    save(ROOT/'registration_provenance.json',{'profile':PROFILE,'source_profile':'all-routes-unified-v1711',
        'source_and_runtime_bound_post_layer':True,'full_prior_accepted_layers_profiles_batches_and_promotion_preserved':True,
        'builder_before_sha256':sha(before),'builder_after_sha256':sha(after),'registry_before_sha256':sha(registry_raw),
        'registry_after_sha256':sha(rp.read_bytes()),'negative_cases_rejected':negatives,
        'global_profiles_encoder_layout_and_old_source_guards_unchanged':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print({'experimental_profile':PROFILE,'negative_cases_rejected':len(negatives),'changed_speeches_and_choices':64,'registered_build_pending':True},flush=True)
