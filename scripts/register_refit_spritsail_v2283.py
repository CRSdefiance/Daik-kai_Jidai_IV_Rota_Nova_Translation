"""Register bounded Refit terminology successor after the complete V2171 stack."""
from pathlib import Path
from copy import deepcopy
import os
from dk4tool.patch import refit_contextual_spritsail_v1 as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/refit_spritsail_registration_v2283');PROFILE='all-routes-unified-v2284';PARENT=Path('out/all_routes_combined_v2171_candidate.nds');DOC=Path('translations/refit_contextual_editorial_manuscript_v2.json')
if __name__=='__main__':
 assert not ROOT.exists()and not Path(owned.CONFIG).exists();ROOT.mkdir(parents=True);registry_path=Path('translations/release_stack.json');builder=Path('scripts/build_integrated_release.py');raw=registry_path.read_bytes();before=builder.read_bytes();registry=read(registry_path);assert PROFILE not in registry['profiles']and len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
 assert sha(PARENT.read_bytes())=='4df01b870562dc04d623fb5c0011d38100bc4062371d32ad2be12f352292260a'
 planpath=Path('work/analysis/refit_spritsail_payload_v2278/payload_plan.json');plan=read(planpath);approval='work/analysis/refit_offline_approval_v2282b/offline_approval.json';fontpath='work/analysis/refit_help_fonts_v2279/native_font_verification.json'
 deps={str(DOC),str(Path(owned.__file__)),__file__,str(planpath),plan['target_ARM9'],plan['target_COMMON'],approval,fontpath,'work/analysis/refit_spoken_layouts_v2280c/native_layout_matrix.json','work/analysis/refit_spoken_layouts_v2280c/native_font_proof.json','work/analysis/refit_current_actual_verification_v2281c/actual_and_logical_proof.json','work/analysis/refit_editorial_context_v2277/spritsail_source_decision.json','work/analysis/refit_context_v2274/native_context.json','work/analysis/refit_context_v2274/current_replay_provenance.json','scripts/review_refit_context_v2277.py','scripts/prepare_refit_spritsail_payload_v2278.py','scripts/probe_refit_help_fonts_v2279.py','scripts/probe_refit_spoken_layouts_v2280c.py','scripts/verify_refit_current_actual_v2281c.py','scripts/approve_refit_offline_v2282b.py','dk4tool/dialogue/refit_help.py','dk4tool/dialogue/review.py','dk4tool/patch/duel_editorial.py','translations/refit_contextual_editorial_manuscript_v1.json'}
 approved=read(approval);deps.update(r['path']for r in approved['all10_help_spoken_and_current_actual_sheets_viewed']);deps.add(approved['label_controlled_native168x108_font_cropped_preview']);canonical=NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
 conf=dict(format='dk4-refit-contextual-spritsail-v1',manuscript=str(DOC),payload_plan=str(planpath),offline_approval=approval,help_fonts=fontpath,directory_sha256=plan['directory_sha256'],source_ARM9_sha256=plan['source_ARM9_sha256'],source_COMMON_sha256=plan['source_COMMON_sha256'],target_ARM9_sha256=plan['target_ARM9_sha256'],target_COMMON_sha256=plan['target_COMMON_sha256'],canonical_COMMON_sha256=sha(canonical.read_file(owned.PATH)),dependencies={p:sha(Path(p).read_bytes())for p in sorted(deps)})
 cp=ROOT/'positive_config.json';save(cp,conf);image=NdsImage.open(PARENT);proof=owned.apply_release(image,canonical,cp);assert image.read_file(owned.PATH)==Path(plan['target_COMMON']).read_bytes()and image.read_file('/__arm9__.bin')==Path(plan['target_ARM9']).read_bytes();save(ROOT/'positive_reconstruction.json',proof);negatives=[]
 def reject(label,candidate,base,path):
  prior=(candidate.read_file(owned.PATH),candidate.read_file('/__arm9__.bin'))
  try:owned.apply_release(candidate,base,path)
  except(ValueError,AssertionError):assert prior==(candidate.read_file(owned.PATH),candidate.read_file('/__arm9__.bin'));negatives.append(dict(case=label,rejected_before_mutation=True))
  else:raise AssertionError(label)
 reject('repeat_application',image,canonical,cp)
 for label,p in(('wrong_ARM9','/__arm9__.bin'),('wrong_COMMON',owned.PATH)):
  wrong=NdsImage.open(PARENT);data=bytearray(wrong.read_file(p));data[256]^=1;wrong.replace_file(p,bytes(data));reject(label,wrong,canonical,cp)
 wrong=NdsImage.open('out/raphael_natural_v2_accepted_base.nds');data=bytearray(wrong.read_file(owned.PATH));data[32]^=1;wrong.replace_file(owned.PATH,bytes(data));reject('wrong_canonical',NdsImage.open(PARENT),wrong,cp)
 for label,mutate in [('unreviewed_record',lambda d:d['records'][0]['review'].update(formatting=False)),('wrong_Japanese',lambda d:d['records'][0].update(source_hex='00')),('changed_retention',lambda d:d['records'][0].update(english='Officers here recover.')),('changed_prose_after_proof',lambda d:next(r for r in d['records']if r['message_id']==1268).update(english='A spritsail improves performance.'))]:
  doc=deepcopy(read(DOC));mutate(doc);p=ROOT/(label+'_manuscript.json');save(p,doc);config=deepcopy(conf);config['manuscript']=str(p);config['dependencies'][str(p)]=sha(p.read_bytes());q=ROOT/(label+'_config.json');save(q,config);reject(label,NdsImage.open(PARENT),canonical,q)
 assert len(negatives)==8;save(ROOT/'negative_cases.json',dict(cases=negatives,all_rejected_before_candidate_mutation=True))
 stage=b'''    refit_context = profile_config.get('refit_contextual_spritsail')
    if refit_context:
        from dk4tool.patch.refit_contextual_spritsail_v1 import apply_release as apply_refit_context

        refit_context_report = apply_refit_context(candidate, baseline, refit_context)
        for refit_path in ('/COMMON/MESFILE.DK4', '/__arm9__.bin'):
            grouped.setdefault(refit_path, [])
            relocation_checks.setdefault(refit_path, {})['refit_contextual_spritsail'] = {
                'release_config': refit_context,
                'release_config_sha256': sha256(Path(refit_context).read_bytes()),
                'proof': refit_context_report}
        changed_records.setdefault('/COMMON/MESFILE.DK4', []).extend(row['id'] for row in refit_context_report['changed_records'])
        changed_records.setdefault('/__arm9__.bin', []).append('REFIT_SPRITSAIL_OWNED_COMPONENT_LABEL_133234_133240')
        refit_context_batch = Path(refit_context_report['manuscript'])
        if refit_context_batch in release_batches:
            raise ValueError('Refit terminology successor must run after the complete cumulative stack')
        release_batches.append(refit_context_batch)

'''
 anchor=b'    # Lexically valid "% o"';assert before.count(anchor)==1 and b"profile_config.get('refit_contextual_spritsail')"not in before;after=before.replace(anchor,stage+anchor);compile(after,str(builder),'exec');(ROOT/'registry_before_raw.json').write_bytes(raw);(ROOT/'builder_before.py').write_bytes(before);(ROOT/'builder_added_optional_stage.bin').write_bytes(stage)
 save(owned.CONFIG,conf);profile=deepcopy(registry['profiles']['all-routes-unified-v2171']);profile.update(refit_contextual_spritsail=owned.CONFIG,status='experimental',description='Complete V2171 cumulative stack plus source-bound spritsail wording in two Refit help paragraphs and matching owned component label.',note='All43 Refit contextual records reviewed;41 retentions,two revisions. Offline native checks pass. Registered build,exact clean-input patch and revised actual widget/help/startup samples remain pending. No promotion;preserve every ROM.');registry['profiles'][PROFILE]=profile
 assert registry_path.read_bytes()==raw and builder.read_bytes()==before;temp=registry_path.with_name('release_stack_v2283_pending.json');assert not temp.exists();save(temp,registry);builder.write_bytes(after);os.replace(temp,registry_path);restored=deepcopy(read(registry_path));restored['profiles'].pop(PROFILE);assert restored==read(ROOT/'registry_before_raw.json')and builder.read_bytes().replace(stage,b'',1)==before
 save(ROOT/'registration_receipt.json',dict(profile=PROFILE,parent_profile='all-routes-unified-v2171',config=owned.CONFIG,config_sha256=sha(Path(owned.CONFIG).read_bytes()),all114accepted_layers_previous_profiles_and_promoted_state_unchanged=True,only_one_optional_stage_and_one_experimental_profile_added=True,negative_cases=8,release_stack_sha256=sha(registry_path.read_bytes()),builder_sha256=sha(builder.read_bytes()),label_controlled_preview_viewed=True,actual_component_widget_and_revised_help_pending=True,no_ROM_created_or_promoted_here=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print(dict(profile=PROFILE,negative_cases=8,registered_experimental=True))
