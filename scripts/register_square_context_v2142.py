"""Register source-guarded Square89 after every frozen V2097 stage."""
from pathlib import Path
from copy import deepcopy
import os
from dk4tool.patch import square_contextual_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/square_registration_v2142');PROFILE='all-routes-unified-v2143';DOC=Path('translations/square_contextual_editorial_manuscript_v3.json');PARENT=Path('out/all_routes_combined_v2097_candidate.nds')
if __name__=='__main__':
 assert not ROOT.exists()and not Path(owned.CONFIG).exists();ROOT.mkdir(parents=True)
 image=NdsImage.open(PARENT);baseline=NdsImage.open('out/raphael_natural_v2_accepted_base.nds');plan_path=Path('work/analysis/square_context_payload_v2124/native_payload_plan.json');plan=read(plan_path)
 assert sha(PARENT.read_bytes())=='488b1a8e62b4354586feb196acdd057facc6ff6ef0ce2d54386010c898d76f45'
 verification=dict(copies='work/analysis/square_context_copies_v2126/all_native_copies_and_prefix_cache_sequence.json',formatting='work/analysis/square_formatting_v2140/offline_formatting_approval.json',control='work/analysis/production_compact_capacity_v2138/all307_production_native_font_cases.json',arguments='work/analysis/square_context_arguments_v2133/all_runtime_native_argument_layouts.json',ordinary='work/analysis/square_context_actual_verification_v2129/ordinary_Square_actual_verification.json',promoter='work/analysis/promoter_pixels_v2139/unchanged_view_four_line_actual_pixel_binding.json')
 files={str(DOC),str(Path(owned.__file__)),str(plan_path),__file__,*verification.values(),plan['target_ARM9'],plan['target_COMMON'],'translations/square_contextual_editorial_manuscript_v1.json','translations/square_contextual_editorial_manuscript_v2.json','work/analysis/square_context_source_v2108/market656_764_clean_current_context_catalog.json','work/analysis/square_relationship_source_v2131/clean_story_relationship_context.json','dk4tool/dialogue/review.py','dk4tool/patch/duel_editorial.py'}
 # The source catalog retains its original market-prefixed directory.
 files.remove('work/analysis/square_context_source_v2108/market656_764_clean_current_context_catalog.json');files.add('work/analysis/market_context_source_v2108/market656_764_clean_current_context_catalog.json')
 conf=dict(format='dk4-square-contextual-editorial-v1',manuscript=str(DOC),payload_plan=str(plan_path),source_COMMON_sha256=plan['source_COMMON_sha256'],source_ARM9_sha256=plan['source_ARM9_sha256'],target_COMMON_sha256=plan['target_COMMON_sha256'],target_ARM9_sha256=plan['target_ARM9_sha256'],canonical_COMMON_sha256=sha(baseline.read_file(owned.PATH)),verification=verification,dependencies={p:sha(Path(p).read_bytes())for p in sorted(files)})
 test_config=ROOT/'positive_config.json';save(test_config,conf);proof=owned.apply_release(image,baseline,test_config);assert image.read_file(owned.PATH)==Path(plan['target_COMMON']).read_bytes()and image.read_file('/__arm9__.bin')==Path(plan['target_ARM9']).read_bytes();save(ROOT/'positive_reconstruction.json',proof)
 negatives=[]
 def reject(label,candidate,base,config):
  before=(candidate.read_file(owned.PATH),candidate.read_file('/__arm9__.bin'))
  try:owned.apply_release(candidate,base,config)
  except(ValueError,AssertionError)as error:assert before==(candidate.read_file(owned.PATH),candidate.read_file('/__arm9__.bin'));negatives.append(dict(case=label,error=str(error),no_partial_mutation=True))
  else:raise AssertionError('Accepted invalid layer: '+label)
 reject('repeat_application',image,baseline,test_config)
 for label,file in [('wrong_runtime','/__arm9__.bin'),('wrong_COMMON',owned.PATH)]:
  wrong=NdsImage.open(PARENT);raw=bytearray(wrong.read_file(file));raw[256]^=1;wrong.replace_file(file,bytes(raw));reject(label,wrong,baseline,test_config)
 wrong=NdsImage.open('out/raphael_natural_v2_accepted_base.nds');raw=bytearray(wrong.read_file(owned.PATH));raw[32]^=1;wrong.replace_file(owned.PATH,bytes(raw));reject('wrong_canonical',NdsImage.open(PARENT),wrong,test_config)
 mutations=[('unreviewed_formatting',lambda d:d['records'][0]['review'].update(formatting=False)),('changed_Japanese',lambda d:d['records'][0].update(source_hex='00')),('wrong_current',lambda d:d['records'][0].update(current_hex='00')),('authored_linebreak',lambda d:next(r for r in d['records']if r['message_id']==698).update(english='Complete\nwords.{PAD}')),('added_printf',lambda d:next(r for r in d['records']if r['message_id']==698).update(english='Complete words %s.{PAD}')),('changed_prose_after_proof',lambda d:next(r for r in d['records']if r['message_id']==698).update(english='Different complete words.{PAD}')),('changed_retention',lambda d:d['records'][0].update(english='Different complete words.{PAD}'))]
 for label,mutate in mutations:
  changed=deepcopy(read(DOC));mutate(changed);path=ROOT/(label+'_manuscript.json');save(path,changed);config=deepcopy(conf);config['manuscript']=str(path);config['dependencies'][str(path)]=sha(path.read_bytes());cp=ROOT/(label+'_config.json');save(cp,config);reject(label,NdsImage.open(PARENT),baseline,cp)
 assert len(negatives)==11;save(ROOT/'negative_cases.json',dict(cases=negatives,all_reject_before_candidate_mutation=True))
 rp,builder=Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py');registry_raw,before=rp.read_bytes(),builder.read_bytes();registry=read(rp);assert PROFILE not in registry['profiles']and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
 stage=b'''    square_context = profile_config.get('square_contextual_editorial')
    if square_context:
        from dk4tool.patch.square_contextual_editorial import apply_release as apply_square_context

        square_report = apply_square_context(candidate, baseline, square_context)
        for square_path in ('/COMMON/MESFILE.DK4', '/__arm9__.bin'):
            grouped.setdefault(square_path, [])
            relocation_checks.setdefault(square_path, {})['square_contextual_editorial'] = {
                'release_config': square_context,
                'release_config_sha256': sha256(Path(square_context).read_bytes()),
                'proof': square_report}
        changed_records.setdefault('/COMMON/MESFILE.DK4', []).extend(row['id'] for row in square_report['changed_records'])
        changed_records.setdefault('/__arm9__.bin', []).append('SQUARE_FOUR_PARAGRAPHS_COMMON8_9_METADATA_ONLY')
        square_batch = Path(square_report['manuscript'])
        if square_batch in release_batches:
            raise ValueError('Square layer must run after all frozen cumulative stages')
        release_batches.append(square_batch)

'''
 anchor=b'    # Lexically valid "% o"';assert before.count(anchor)==1 and b"profile_config.get('square_contextual_editorial')"not in before;after=before.replace(anchor,stage+anchor,1);compile(after,str(builder),'exec')
 (ROOT/'registry_before_raw.json').write_bytes(registry_raw);(ROOT/'builder_before.py').write_bytes(before);(ROOT/'builder_added_optional_stage.bin').write_bytes(stage)
 save(owned.CONFIG,conf);profile=deepcopy(registry['profiles']['all-routes-unified-v2097']);profile.update(square_contextual_editorial=owned.CONFIG,status='experimental',description='Complete V2097 cumulative stack plus four contextual Square revisions and85 justified retentions;original display geometry andruntime unchanged.',note='Offline native/source/copy checks pass;representative revised Square andrelease verification pending. No promotion. Preserve all ROMs.')
 registry['profiles'][PROFILE]=profile;assert rp.read_bytes()==registry_raw and builder.read_bytes()==before;temp=rp.with_name('release_stack_v2142_pending.json');assert not temp.exists();save(temp,registry);builder.write_bytes(after);os.replace(temp,rp)
 restored=deepcopy(read(rp));restored['profiles'].pop(PROFILE);assert restored==read(ROOT/'registry_before_raw.json')and builder.read_bytes().replace(stage,b'',1)==before
 save(ROOT/'registration_receipt.json',dict(profile=PROFILE,parent_profile='all-routes-unified-v2097',config=owned.CONFIG,config_sha256=sha(Path(owned.CONFIG).read_bytes()),all114_accepted_layers_unchanged=True,only_added_one_optional_late_stage_and_one_experimental_profile=True,negative_cases=11,release_stack_sha256=sha(rp.read_bytes()),builder_sha256=sha(builder.read_bytes()),producer_sha256=sha(Path(__file__).read_bytes()),no_ROM_created_or_promoted_here=True,full_goal_complete=False));print(dict(profile=PROFILE,negative_cases=11,registered_experimental=True))
