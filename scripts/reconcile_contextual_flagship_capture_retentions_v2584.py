"""Reconcile five unchanged reports against both original and precision owners."""
from pathlib import Path
outer=Path('scripts/reconcile_contextual_aftermath_fled_retentions_v2544.py').read_text();needle="exec(compile(source,__file__,'exec'),globals())";assert outer.count(needle)==1
env={};exec(compile(outer.replace(needle,'captured=source'),__file__,'exec'),env);source=env['captured']
changes={
 'aftermath_fled':'flagship_capture',
 "fonts['complete_native_font_cases']==6 and len(fonts['all6_original_role1_pipelines'])==6":"fonts['complete_native_font_cases']==8 and len(fonts['all8_original_role1_pipelines'])==8",
 'original-53D44-role1-fled-victory-portrait':'original-53D44-logical-role1-flagship-capture-portrait',
 "history['only2046_has_individual_historical_activation_other5_use_family_sample']":"history['only2011_has_individual_historical_activation_other4_use_family_sample']",
 "history['no_inputs5773_through10982']":"history['no_fixtures_after4800']",
 '0x02117900':'0x02117740','font_previews=count':'font_previews=spec["font_previews"]',
 'historical_report_and_sailing_return_transitions':'historical_capture_rewards_cargo_and_sailing_transitions',
 'flight-report/dismissal':'capture-report/rewards/cargo/sailing',
 'pre-duel-fixtures-flight-report-and-sailing-return':'sole-own-ship-position-fixture-capture-rewards-cargo-and-sailing',
}
for a,b in changes.items():assert a in source,a;source=source.replace(a,b)
a=source.index(" stage=manifest['relocations']");b=source.index(' rom,clean=',a)
source=source[:a]+""" owners=doc['registered_prose_owner_bindings'];assert len(owners)==2
 binding=dict(registered_prose_owner_bindings=owners,selected_contextual_native_IDs=ids,new_revisions=0)
 registered_evidence=[];prior={};owner_by_ID={}
 for owner in owners:
  stage=manifest['relocations']['/COMMON/MESFILE.DK4'][owner['stage']];configpath=Path(stage['release_config']);config=read(configpath);registeredpath=Path(config['manuscript'])
  assert str(configpath)==owner['registered_config'] and str(registeredpath)==owner['registered_manuscript']
  assert sha(configpath.read_bytes())==stage['release_config_sha256']==owner['registered_config_sha256'] and sha(registeredpath.read_bytes())==config['dependencies'][str(registeredpath)]==owner['registered_manuscript_sha256']
  assert stage['proof']['native_IDs']==owner['registered_stage_native_IDs'] and set(owner['selected_IDs'])<=set(stage['proof']['native_IDs'])
  module,attribute=owner['compiler'].rsplit('.',1);own_compiler=getattr(import_module(module),attribute)
  registered_evidence.extend((configpath,registeredpath))
  for row in read(registeredpath)['records']:
   n=row['message_id']
   if n in owner['selected_IDs']:assert n not in prior;prior[n]=row;owner_by_ID[n]=owner['stage'];assert import_module(spec['compiler']).compiled(row)==own_compiler(row)
 assert sorted(prior)==ids and owner_by_ID=={2011:'battle_aftermath_editorial',2012:'battle_aftermath_editorial',2013:'battle_aftermath_editorial',2014:'battle_aftermath_editorial',2015:'flagship_capture_precision'}
"""+source[b:]
source=source.replace("prior={r['message_id']:r for r in read(registeredpath)['records']};",'')
source=source.replace("n=r['message_id'];assert r['source_hex']","n=r['message_id'];assert r['registered_prose_owner']==owner_by_ID[n];assert r['source_hex']")
source=source.replace('manifestpath,registrypath,configpath,registeredpath,','manifestpath,registrypath,*registered_evidence,')
exec(compile(source,__file__,'exec'),globals())
