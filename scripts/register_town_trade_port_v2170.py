"""Register61 contextual entries after the frozen V2143 cumulative stack."""
from pathlib import Path
from copy import deepcopy
import os
from dk4tool.patch import town_trade_port_contextual_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/town_trade_port_registration_v2170');PROFILE='all-routes-unified-v2171';DOC=Path('translations/town_trade_port_contextual_editorial_manuscript_v2.json');PARENT=Path('out/all_routes_combined_v2143_candidate.nds')
if __name__=='__main__':
 assert not ROOT.exists()and not Path(owned.CONFIG).exists();ROOT.mkdir(parents=True);image=NdsImage.open(PARENT);baseline=NdsImage.open('out/raphael_natural_v2_accepted_base.nds');planpath=Path('work/analysis/town_trade_port_payload_v2165/native_payload_plan.json');plan=read(planpath);assert sha(PARENT.read_bytes())=='1178174c47e31b2814a3d1a43b5389a1790d12299e5bb667ad244a012cd44cf1'
 verification=dict(formatting='work/analysis/town_trade_port_formatting_v2169/offline_formatting_approval.json',fonts='work/analysis/town_trade_port_fonts_v2167/all_native_layout_inheritance_and_full_font_samples.json',predicates='work/analysis/town_trend_selector_v2164/all_eight_parent_lowword_fullword_stack_and_R2_ABI.json',references='work/analysis/town_trend_references_v2166/all_unit_references_and_ARMv5_instruction_audit.json',copies='work/analysis/town_trade_port_copies_v2168/all_native_copies_and_prefix_cache_sequence.json',modal='work/analysis/yard_modal_actual_verification_v2158/actual267_native_geometry_direct_font_and_foreground.json')
 files={str(DOC),str(Path(owned.__file__)),str(planpath),plan['runtime_plan'],plan['target_ARM9'],plan['target_COMMON'],__file__,*verification.values(),'scripts/town_trend_balanced_runtime_v2162.py','scripts/verify_town_trend_selector_v2164.py','scripts/verify_town_trade_port_fonts_v2167.py','scripts/prepare_town_trade_port_payload_v2165.py','scripts/audit_town_trend_references_v2166.py','scripts/verify_town_trade_port_copies_v2168.py','translations/town_trade_port_contextual_editorial_manuscript_v1.json','work/analysis/town_trade_port_context_v2150b/clean_graphs_current_typed_arguments_and_companion_roles.json','work/analysis/town_trade_port_source_v2149/all61_clean_current_context_catalog.json','work/analysis/town_services_runtime_v2080/runtime_plan.json','work/analysis/recruitment_owned_v772/owned_runtime_plan.json','dk4tool/dialogue/review.py','dk4tool/patch/duel_editorial.py'}
 files.update(r['path']for r in read(verification['fonts'])['physical_sheets'])
 conf=dict(format='dk4-town-trade-port-contextual-editorial-v1',manuscript=str(DOC),payload_plan=str(planpath),source_COMMON_sha256=plan['source_COMMON_sha256'],source_ARM9_sha256=plan['source_ARM9_sha256'],target_COMMON_sha256=plan['target_COMMON_sha256'],target_ARM9_sha256=plan['target_ARM9_sha256'],canonical_COMMON_sha256=sha(baseline.read_file(owned.PATH)),verification=verification,dependencies={p:sha(Path(p).read_bytes())for p in sorted(files)})
 cp=ROOT/'positive_config.json';save(cp,conf);proof=owned.apply_release(image,baseline,cp);assert image.read_file(owned.PATH)==Path(plan['target_COMMON']).read_bytes()and image.read_file('/__arm9__.bin')==Path(plan['target_ARM9']).read_bytes();save(ROOT/'positive_reconstruction.json',proof);negatives=[]
 def reject(label,candidate,base,path):
  before=(candidate.read_file(owned.PATH),candidate.read_file('/__arm9__.bin'))
  try:owned.apply_release(candidate,base,path)
  except(ValueError,AssertionError)as error:assert before==(candidate.read_file(owned.PATH),candidate.read_file('/__arm9__.bin'));negatives.append(dict(case=label,error=str(error),no_partial_mutation=True))
  else:raise AssertionError('Accepted invalid layer: '+label)
 reject('repeat_application',image,baseline,cp)
 for label,file in[('wrong_runtime','/__arm9__.bin'),('wrong_COMMON',owned.PATH)]:
  wrong=NdsImage.open(PARENT);raw=bytearray(wrong.read_file(file));raw[256]^=1;wrong.replace_file(file,bytes(raw));reject(label,wrong,baseline,cp)
 wrong=NdsImage.open('out/raphael_natural_v2_accepted_base.nds');raw=bytearray(wrong.read_file(owned.PATH));raw[32]^=1;wrong.replace_file(owned.PATH,bytes(raw));reject('wrong_canonical',NdsImage.open(PARENT),wrong,cp)
 mutations=[('unreviewed_formatting',lambda d:d['records'][0]['review'].update(formatting=False)),('changed_Japanese',lambda d:d['records'][0].update(source_hex='00')),('wrong_current',lambda d:d['records'][0].update(current_hex='00')),('authored_linebreak',lambda d:next(r for r in d['records']if r['message_id']==654).update(english='Brought %s?\nSell your stock.{PAD}')),('added_printf',lambda d:next(r for r in d['records']if r['message_id']==654).update(english='Sell %s and %s at the Market.{PAD}')),('changed_prose_after_proof',lambda d:next(r for r in d['records']if r['message_id']==654).update(english='Please sell %s at the Market soon.{PAD}')),('changed_retention',lambda d:d['records'][0].update(english='No more ships can be sold.{PAD}'))]
 for label,mutate in mutations:
  changed=deepcopy(read(DOC));mutate(changed);p=ROOT/(label+'_manuscript.json');save(p,changed);c=deepcopy(conf);c['manuscript']=str(p);c['dependencies'][str(p)]=sha(p.read_bytes());q=ROOT/(label+'_config.json');save(q,c);reject(label,NdsImage.open(PARENT),baseline,q)
 for label in('selector_allocation_growth','missing_R2_save'):
  r=deepcopy(read(plan['runtime_plan']));patch=next(p for p in r['patches']if p['address']==(0x02147B9C if label=='selector_allocation_growth'else 0x02132020));patch['target_hex']=patch['target_hex']+'00'if label=='selector_allocation_growth'else patch['source_hex'];rp=ROOT/(label+'_runtime.json');save(rp,r);p=deepcopy(plan);p.update(runtime_plan=str(rp),runtime_plan_sha256=sha(rp.read_bytes()),runtime_patches=r['patches']);pp=ROOT/(label+'_plan.json');save(pp,p);c=deepcopy(conf);c['payload_plan']=str(pp);c['dependencies'][str(pp)]=sha(pp.read_bytes());c['dependencies'][str(rp)]=sha(rp.read_bytes());q=ROOT/(label+'_config.json');save(q,c);reject(label,NdsImage.open(PARENT),baseline,q)
 assert len(negatives)==13;save(ROOT/'negative_cases.json',dict(cases=negatives,all_reject_before_candidate_mutation=True))
 registry_path=Path('translations/release_stack.json');builder=Path('scripts/build_integrated_release.py');registry_raw=registry_path.read_bytes();before=builder.read_bytes();registry=read(registry_path);assert PROFILE not in registry['profiles']and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
 stage=b'''    town_trade_port = profile_config.get('town_trade_port_contextual_editorial')
    if town_trade_port:
        from dk4tool.patch.town_trade_port_contextual_editorial import apply_release as apply_town_trade_port

        trade_report = apply_town_trade_port(candidate, baseline, town_trade_port)
        for trade_path in ('/COMMON/MESFILE.DK4', '/__arm9__.bin'):
            grouped.setdefault(trade_path, [])
            relocation_checks.setdefault(trade_path, {})['town_trade_port_contextual_editorial'] = {
                'release_config': town_trade_port,
                'release_config_sha256': sha256(Path(town_trade_port).read_bytes()),
                'proof': trade_report}
        changed_records.setdefault('/COMMON/MESFILE.DK4', []).extend(row['id'] for row in trade_report['changed_records'])
        changed_records.setdefault('/__arm9__.bin', []).append('TREND654655_OWNED_SELECTOR_CODEC_STACK_BRIDGES_AND_COMMON7_METADATA')
        trade_batch = Path(trade_report['manuscript'])
        if trade_batch in release_batches:
            raise ValueError('Shared trade and Port layer must run after frozen cumulative stages')
        release_batches.append(trade_batch)

'''
 anchor=b'    # Lexically valid "% o"';assert before.count(anchor)==1 and b"profile_config.get('town_trade_port_contextual_editorial')"not in before;after=before.replace(anchor,stage+anchor,1);compile(after,str(builder),'exec');(ROOT/'registry_before_raw.json').write_bytes(registry_raw);(ROOT/'builder_before.py').write_bytes(before);(ROOT/'builder_added_optional_stage.bin').write_bytes(stage)
 save(owned.CONFIG,conf);profile=deepcopy(registry['profiles']['all-routes-unified-v2143']);profile.update(town_trade_port_contextual_editorial=owned.CONFIG,status='experimental',description='Complete V2143 stack plus61fresh shared-town contextual reviews,two trend revisions andbounded existing-selector balanced wrapping.',note='Offline native/reference/font/copy checks pass;revisedtrend gameplay,registered release andexactpatch pending atregistration. No promotion. Preserve allROMs.');registry['profiles'][PROFILE]=profile
 assert registry_path.read_bytes()==registry_raw and builder.read_bytes()==before;temp=registry_path.with_name('release_stack_v2170_pending.json');assert not temp.exists();save(temp,registry);builder.write_bytes(after);os.replace(temp,registry_path);restored=deepcopy(read(registry_path));restored['profiles'].pop(PROFILE);assert restored==read(ROOT/'registry_before_raw.json')and builder.read_bytes().replace(stage,b'',1)==before
 save(ROOT/'registration_receipt.json',dict(profile=PROFILE,parent_profile='all-routes-unified-v2143',config=owned.CONFIG,config_sha256=sha(Path(owned.CONFIG).read_bytes()),all114_accepted_layers_and_previous_profiles_unchanged=True,only_added_one_optional_late_stage_and_one_experimental_profile=True,negative_cases=13,release_stack_sha256=sha(registry_path.read_bytes()),builder_sha256=sha(builder.read_bytes()),producer_sha256=sha(Path(__file__).read_bytes()),no_ROM_created_or_promoted_here=True,full_goal_complete=False));print(dict(profile=PROFILE,negative_cases=13,registered_experimental=True))
