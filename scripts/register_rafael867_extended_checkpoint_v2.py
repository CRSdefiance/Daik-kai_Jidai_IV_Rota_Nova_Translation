"""Register a qualified351 append after the exact verified516 canonical prefix."""
import os
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha
from scripts.registered_canonical_extension_resume_v2 import STAGES,qualify,stage_source


def main():
    root=Path('work/analysis/Rafael867_registered_extended_resume_v2_20261105')
    config_path=Path('translations/rafael867_canonical_extension_resume_v2.json')
    assert not root.exists() and not config_path.exists()
    prep_path=Path('work/analysis/Rafael351_registered_preparation_v3_20261105/registered_preparation.json')
    qualification_path=Path('work/analysis/Rafael351_release_qualification_v3_20261105/qualification.json')
    prep,qualification=map(load,[prep_path,qualification_path])
    registry_path=Path('translations/release_stack.json');before=registry_path.read_bytes()
    assert sha(before)==prep['registry_sha256']==qualification['registry_sha256']
    stack=load(registry_path)
    profile_name='all-routes-rafael867-extended-checkpoint-v2-20261105'
    assert profile_name not in stack['profiles']
    profile=deepcopy(stack['profiles'][prep['profile']])
    profile['canonical_checkpoint_resume']=str(config_path)
    stack['profiles'][profile_name]=profile
    spec=load('translations/rafael351_registered_successor_spec_v3.json')
    release_path=Path(spec['parent_release']);release=load(release_path)
    source_manifest=load(release['manifest'])
    canonical_manifest=Path(source_manifest['production_pipeline']['canonical_manifest'])
    canonical_ROM=Path(source_manifest['production_pipeline']['canonical_stage'])
    assert sha(canonical_ROM.read_bytes())==prep['canonical_parent_sha256']
    dependencies=[Path(__file__),Path('scripts/registered_canonical_extension_resume_v2.py'),
        Path('scripts/registered_canonical_checkpoint_resume_v1.py'),Path('scripts/build_integrated_release.py'),
        prep_path,qualification_path,release_path,Path(release['manifest']),canonical_manifest,
        Path(spec['parent_release']).parent/'own_registered_startup_verification.json',
        *[Path('scripts/resume_extended_release_with_'+s+'_v2.py') for s in STAGES]]
    root.mkdir(parents=True);(root/'release_stack_before.json').write_bytes(before)
    config=dict(configuration=str(config_path),profile=profile_name,prepared_profile=prep['profile'],
        source_profile=prep['previous_profile'],previous_registry=str(root/'release_stack_before.json'),previous_registry_sha256=sha(before),
        source_registry=str(prep_path.parent/'release_stack_before.json'),parent_release=str(release_path),
        preparation=str(prep_path),qualification=str(qualification_path),canonical_ROM=str(canonical_ROM),
        canonical_manifest=str(canonical_manifest),new_extension_specs=prep['new_extension_specs'],
        dependencies={str(p):sha(p.read_bytes()) for p in dependencies},new_credit=0)
    save(config_path,config)
    positive=qualify(config,stack)
    negatives=[]
    for kind in ['wrong-profile','missing-resume-registration','changed-accepted-layers','changed-previous-profile',
        'changed-registered-stage','reordered-extension','wrong-source-registry','wrong-canonical-ROM',
        'wrong-canonical-manifest','changed-dependency']:
        bad,wrong=deepcopy(config),deepcopy(stack)
        if kind=='wrong-profile':bad['prepared_profile']=prep['previous_profile']
        elif kind=='missing-resume-registration':del wrong['profiles'][profile_name]['canonical_checkpoint_resume']
        elif kind=='changed-accepted-layers':wrong['accepted_layers']=[]
        elif kind=='changed-previous-profile':wrong['profiles'][prep['previous_profile']]['note']+=' altered'
        elif kind=='changed-registered-stage':wrong['profiles'][profile_name]['owned_Fernan_name_field']='bad.json'
        elif kind=='reordered-extension':bad['new_extension_specs'][0]['parent_ROM_sha256']='0'*64
        elif kind=='wrong-source-registry':bad['source_registry']=str(root/'release_stack_before.json')
        elif kind=='wrong-canonical-ROM':bad['canonical_ROM']=release['candidate']
        elif kind=='wrong-canonical-manifest':bad['canonical_manifest']=release['manifest']
        elif kind=='changed-dependency':bad['dependencies'][str(dependencies[0])]='0'*64
        try:qualify(bad,wrong)
        except (AssertionError,KeyError,ValueError) as error:
            negatives.append(dict(case=kind,exception=type(error).__name__,rejected_before_publication=True))
        else:raise AssertionError('Unexpected acceptance:'+kind)
    save(root/'checkpoint_qualification.json',dict(positive=positive,negative_cases=negatives,
        all_original_final_contracts_andstage_guards_preserved=True,
        stage_source_derivations={s:sha(stage_source(s).encode('utf-8')) for s in STAGES},new_credit=0))
    assert registry_path.read_bytes()==before
    pending=registry_path.with_name('release_stack.Rafael867_extended_resume_v2.pending.json');assert not pending.exists()
    save(pending,stack);os.replace(pending,registry_path)
    finalprep=deepcopy(prep)
    finalprep.update(profile=profile_name,registry_sha256=sha(registry_path.read_bytes()),
        original_preparation=str(prep_path),original_preparation_sha256=sha(prep_path.read_bytes()),
        canonical_checkpoint_resume=str(config_path),canonical_checkpoint_resume_sha256=sha(config_path.read_bytes()))
    save(root/'registered_preparation.json',finalprep)
    finalqualification=deepcopy(qualification)
    finalqualification.update(profile=profile_name,registry_sha256=sha(registry_path.read_bytes()),
        preparation=str(root/'registered_preparation.json'),preparation_sha256=sha((root/'registered_preparation.json').read_bytes()),
        original_qualification=str(qualification_path),original_qualification_sha256=sha(qualification_path.read_bytes()),
        checkpoint_qualification=str(root/'checkpoint_qualification.json'),
        checkpoint_qualification_sha256=sha((root/'checkpoint_qualification.json').read_bytes()))
    save(root/'qualification.json',finalqualification)
    print('Registered867 extended-checkpoint profile:verified672-entry prefix plus351 source-bound append;ten resume negatives rejected. All originalfinal contracts/eight stages required;no credit orpromotion.')


if __name__=='__main__':main()
