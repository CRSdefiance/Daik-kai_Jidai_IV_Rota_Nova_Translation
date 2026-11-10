"""Preserve the stopped preparer; correct only its replacement-source quoting before any registration."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_fixture_registered_repair_v8376b');assert not root.exists();s=Path('scripts/prepare_Hodram_fixture_registered_tools_v8376.py').read_text('utf8');a=s.index('    newblock=');b=s.index('    results.append',a)
    code='''    anchor='    # Lexically valid "% o"';text=before.decode('utf8');assert text.count(anchor)==1 and text.count(LEGACY_STAGE)==1 and STAGE not in text
    digest=frozen['dependencies'][str(builder.resolve())];assert validate_builder_bytes(before,digest)['owned_stage_version']=='preserved-v2'
    frozen_builder=before.replace(LEGACY_STAGE.encode(),b'',1);assert sha(frozen_builder)==digest
    after=checked_text(text,{LEGACY_STAGE:STAGE}).encode('utf8')
    assert after.replace(STAGE.encode(),b'',1)==frozen_builder and validate_builder_bytes(after,digest)['owned_stage_version']=='current-v3'
'''
    d=derive('scripts/prepare_Hodram_fixture_registered_tools_v8376.py','scripts/prepare_Hodram_fixture_registered_tools_v8376b.py',{s[a:b]:'    newblock='+repr(code)+'\n','Hodram_fixture_registered_tools_v8376':'Hodram_fixture_registered_tools_v8376b'})
    root.mkdir(parents=True);save(root/'replacement_source_quoting_only.json',dict(derivation=d,prior_preparer_failed_before_writing_any_registration_target=True,no_builder_registry_ROM_orcredit_change=True,new_credit=0,full_goal_complete=False))
