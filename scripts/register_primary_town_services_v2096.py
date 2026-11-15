"""Register source-guarded primary-town84 after every frozen V2047 stage."""
from pathlib import Path
from copy import deepcopy
import os
from dk4tool.patch import primary_town_services_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.checkpoint_primary_town_v2094 import PROOFS
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/town_services_registration_v2096')
PROFILE='all-routes-unified-v2097'
DOC=Path('translations/primary_town_services_contextual_editorial_manuscript_v5.json')
PARENT=Path('out/all_routes_combined_v2047_candidate.nds')
if __name__=='__main__':
 assert not ROOT.exists()and not Path(owned.CONFIG).exists();ROOT.mkdir(parents=True)
 image=NdsImage.open(PARENT);baseline=NdsImage.open('out/raphael_natural_v2_accepted_base.nds');plan_path=Path(PROOFS[11]);plan=read(plan_path)
 assert sha(PARENT.read_bytes())=='096945ba367a10edbe3e116e49072734a7b6373fdda2b07083c828f72292e227'
 verification=dict(status=PROOFS[2],selector=PROOFS[3],routes=PROOFS[4],fonts=PROOFS[5],modal=PROOFS[6],references=PROOFS[7],names=PROOFS[8],name_pixels=PROOFS[9],style=PROOFS[10],copies=PROOFS[12])
 files={str(DOC),str(Path(owned.__file__)),*PROOFS,'translations/primary_town_services_contextual_editorial_manuscript_v4.json','work/analysis/town_services_formatting_v2095/offline_formatting_approval.json',__file__,'scripts/primary_town_runtime_v2077.py','scripts/primary_town_runtime_v2080.py','scripts/prepare_primary_town_payload_v2092b.py','scripts/verify_primary_town_copies_v2093.py','dk4tool/dialogue/review.py','dk4tool/patch/common_single_cache_v861.py','dk4tool/patch/duel_editorial.py'}
 files.add(read(PROOFS[1])['research_ARM9']);files.update([plan['target_ARM9'],plan['target_COMMON']])
 visual=read(PROOFS[9]);files.add(visual['style_sheet']);files.update(r['source_preview']for r in visual['style_cases'])
 conf=dict(format='dk4-primary-town-services-editorial-v1',manuscript=str(DOC),payload_plan=str(plan_path),source_COMMON_sha256=plan['source_COMMON_sha256'],source_ARM9_sha256=plan['source_ARM9_sha256'],target_COMMON_sha256=plan['target_COMMON_sha256'],target_ARM9_sha256=plan['target_ARM9_sha256'],canonical_COMMON_sha256=sha(baseline.read_file(owned.PATH)),verification=verification,dependencies={p:sha(Path(p).read_bytes())for p in sorted(files)})
 test_config=ROOT/'positive_config.json';save(test_config,conf);proof=owned.apply_release(image,baseline,test_config)
 assert image.read_file(owned.PATH)==Path(plan['target_COMMON']).read_bytes()and image.read_file('/__arm9__.bin')==Path(plan['target_ARM9']).read_bytes();save(ROOT/'positive_reconstruction.json',proof)
 negatives=[]
 def reject(label,candidate,base,config):
  before=(candidate.read_file(owned.PATH),candidate.read_file('/__arm9__.bin'))
  try:owned.apply_release(candidate,base,config)
  except(ValueError,AssertionError)as error:
   assert before==(candidate.read_file(owned.PATH),candidate.read_file('/__arm9__.bin'));negatives.append(dict(case=label,error=str(error),no_partial_mutation=True))
  else:raise AssertionError('Accepted invalid layer: '+label)
 reject('repeat_application',image,baseline,test_config)
 for label,file in [('wrong_runtime','/__arm9__.bin'),('wrong_COMMON',owned.PATH)]:
  wrong=NdsImage.open(PARENT);raw=bytearray(wrong.read_file(file));raw[256]^=1;wrong.replace_file(file,bytes(raw));reject(label,wrong,baseline,test_config)
 wrong=NdsImage.open('out/raphael_natural_v2_accepted_base.nds');raw=bytearray(wrong.read_file(owned.PATH));raw[32]^=1;wrong.replace_file(owned.PATH,bytes(raw));reject('wrong_canonical',NdsImage.open(PARENT),wrong,test_config)
 mutations=[('unreviewed_formatting',lambda d:d['records'][0]['review'].update(formatting=False)),('changed_Japanese',lambda d:d['records'][0].update(source_hex='00')),('wrong_current',lambda d:d['records'][0].update(current_hex='00')),('authored_linebreak',lambda d:d['records'][0].update(english='Complete\nwords.{PAD}')),('added_printf',lambda d:d['records'][0].update(english='Complete words %s.{PAD}')),('changed_prose_after_proof',lambda d:d['records'][0].update(english='Different complete words.{PAD}')),('missing_waiver_reason',lambda d:next(r for r in d['records']if r['message_id']==25).update(qa_waiver_reason=''))]
 for label,mutate in mutations:
  changed=deepcopy(read(DOC));mutate(changed);path=ROOT/(label+'_manuscript.json');save(path,changed);config=deepcopy(conf);config['manuscript']=str(path);config['dependencies'][str(path)]=sha(path.read_bytes());cp=ROOT/(label+'_config.json');save(cp,config);reject(label,NdsImage.open(PARENT),baseline,cp)
 assert len(negatives)==11;save(ROOT/'negative_cases.json',dict(cases=negatives,all_reject_before_candidate_mutation=True))
 rp,builder=Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py');registry_raw,before=rp.read_bytes(),builder.read_bytes();registry=read(rp);assert PROFILE not in registry['profiles']and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
 stage=b'''    primary_town_services = profile_config.get('primary_town_services_editorial')
    if primary_town_services:
        from dk4tool.patch.primary_town_services_editorial import apply_release as apply_primary_town_services

        town_report = apply_primary_town_services(candidate, baseline, primary_town_services)
        for town_path in ('/COMMON/MESFILE.DK4', '/__arm9__.bin'):
            grouped.setdefault(town_path, [])
            relocation_checks.setdefault(town_path, {})['primary_town_services_editorial'] = {
                'release_config': primary_town_services,
                'release_config_sha256': sha256(Path(primary_town_services).read_bytes()),
                'proof': town_report}
        changed_records.setdefault('/COMMON/MESFILE.DK4', []).extend(row['id'] for row in town_report['changed_records'])
        changed_records.setdefault('/__arm9__.bin', []).append('PRIMARY_TOWN84_SOURCE_BOUND_LITERAL_ROUTES_AND_COMMON0_DIRECTORY')
        town_batch = Path(town_report['manuscript'])
        if town_batch in release_batches:
            raise ValueError('Primary town layer must run after all frozen cumulative stages')
        release_batches.append(town_batch)

'''
 anchor=b'    # Lexically valid "% o"';assert before.count(anchor)==1 and b"profile_config.get('primary_town_services_editorial')"not in before
 after=before.replace(anchor,stage+anchor,1);compile(after,str(builder),'exec')
 (ROOT/'registry_before_raw.json').write_bytes(registry_raw);(ROOT/'builder_before.py').write_bytes(before);(ROOT/'builder_added_optional_stage.bin').write_bytes(stage)
 save(owned.CONFIG,conf);profile=deepcopy(registry['profiles']['all-routes-unified-v2047']);profile.update(primary_town_services_editorial=owned.CONFIG,status='experimental',description='Complete V2047 cumulative stack plus source-reviewed primary town services84 and bounded native display routing.',note='Native tests pass;representative revised town and release verification pending. No promotion. Preserve all ROMs.')
 registry['profiles'][PROFILE]=profile;assert rp.read_bytes()==registry_raw and builder.read_bytes()==before
 temp=rp.with_name('release_stack_v2096_pending.json');assert not temp.exists();save(temp,registry);builder.write_bytes(after);os.replace(temp,rp)
 restored=deepcopy(read(rp));restored['profiles'].pop(PROFILE);assert restored==read(ROOT/'registry_before_raw.json')and builder.read_bytes().replace(stage,b'',1)==before
 save(ROOT/'registration_receipt.json',dict(profile=PROFILE,parent_profile='all-routes-unified-v2047',config=owned.CONFIG,config_sha256=sha(Path(owned.CONFIG).read_bytes()),all114_accepted_layers_unchanged=True,only_added_one_optional_late_stage_and_one_experimental_profile=True,negative_cases=11,release_stack_sha256=sha(rp.read_bytes()),builder_sha256=sha(builder.read_bytes()),producer_sha256=sha(Path(__file__).read_bytes()),no_ROM_created_or_promoted_here=True,full_goal_complete=False));print(dict(profile=PROFILE,negative_cases=11,registered_experimental=True))
