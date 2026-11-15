"""Keep the complete516 verifier and additionally audit explicit checkpoint provenance."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

previous = Path('scripts/verify_rafael516_registered_release_v1.py')
source = checked_text(previous.read_text(encoding='utf-8'), {
    "    assert m['profile'] == terminal['profile'] == prep['profile'] == qualification['profile']":
        """    assert m['profile'] == terminal['profile'] == prep['profile'] == qualification['profile']
    from scripts.registered_canonical_checkpoint_resume_v1 import qualify,stage_source,STAGES
    assert terminal['explicit_registered_canonical_checkpoint_reuse']
    resume_path=Path(registry['profiles'][m['profile']]['canonical_checkpoint_resume'])
    resume_config=load(resume_path)
    assert sha(resume_path.read_bytes())==prep['canonical_checkpoint_resume_sha256']
    resume= m['canonical_checkpoint_resume']
    assert resume['configuration']==str(resume_path) and resume['configuration_sha256']==sha(resume_path.read_bytes())
    assert resume['qualification']==qualify(resume_config,registry)
    assert resume['explicit_versioned_continuation_not_a_new_canonical_builder_run']
    assert resume['original_profile']==resume_config['source_profile']
    assert resume['original_release_stack_sha256']==resume_config['previous_registry_sha256']
    assert resume['original_ROM']==resume_config['canonical_ROM']
    assert resume['original_ROM_sha256']==resume_config['canonical_ROM_sha256']
    assert sha(Path(resume['original_manifest']).read_bytes())==resume['original_manifest_sha256']
    assert sha(Path(resume['original_terminal']).read_bytes())==resume['original_terminal_sha256']
    assert resume['stage_source_derivations']=={s:sha(stage_source(s).encode('utf-8')) for s in STAGES}
    resume_qualification_path=Path(qualification['checkpoint_qualification'])
    assert sha(resume_qualification_path.read_bytes())==qualification['checkpoint_qualification_sha256']
    resume_qualification=load(resume_qualification_path)
    assert len(resume_qualification['negative_cases'])==10
    assert all(x['rejected_before_publication'] for x in resume_qualification['negative_cases'])
    assert resume_qualification['all_eight_original_stage_bodies_preserved']
    assert resume_qualification['stage_source_derivations']==resume['stage_source_derivations']""",
})

if __name__ == '__main__':
    exec(compile(source, __file__ + '::complete-original516-verification-plus-explicit-resume-audit', 'exec'), globals())
