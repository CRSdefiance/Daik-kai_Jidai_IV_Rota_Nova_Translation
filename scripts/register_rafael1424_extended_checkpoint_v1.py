"""Register the checked 557 append over the verified 673-entry canonical prefix."""
from scripts.register_rafael867_extended_checkpoint_v3 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text
from pathlib import Path

source=checked_text(previous,{
    'scripts.registered_canonical_extension_resume_v3 import STAGES,qualify,stage_source':
        'scripts.registered_canonical_extension_resume_v4 import STAGES,qualify,stage_source',
    'Rafael867_registered_extended_resume_v3_20261105':'Rafael1424_registered_extended_resume_v1_20261105',
    'rafael867_canonical_extension_resume_v3.json':'rafael1424_canonical_extension_resume_v1.json',
    'all-routes-rafael867-extended-checkpoint-v3-20261105':'all-routes-rafael1424-extended-checkpoint-20261105',
    'Rafael351_registered_preparation_v3_20261105':'Rafael557_registered_preparation_v1_20261105',
    'Rafael351_release_qualification_v3_20261105':'Rafael557_release_qualification_v1_20261105',
    'rafael351_registered_successor_spec_v3.json':'rafael557_registered_successor_spec_v1.json',
    "prepared_registry='work/analysis/Rafael867_registered_extended_resume_v2_20261105/release_stack_before.json',prepared_registry_sha256=prep['registry_sha256'],":
        "prepared_registry=str(root/'release_stack_before.json'),prepared_registry_sha256=prep['registry_sha256'],expected_prefix_entries=673,",
    "Path('scripts/registered_canonical_extension_resume_v3.py'),":
        "Path('scripts/registered_canonical_extension_resume_v4.py'),Path('scripts/registered_canonical_extension_resume_v3.py'),",
    "Path('scripts/resume_extended_release_with_'+s+'_v3.py')":"Path('scripts/resume_extended_release_with_'+s+'_v4.py')",
    'release_stack.Rafael867_extended_resume_v3.pending.json':'release_stack.Rafael1424_extended_resume_v1.pending.json',
    'Registered867 extended-checkpoint profile:verified672-entry prefix plus351 source-bound append':
        'Registered Rafael1424 profile: verified 673-entry prefix plus the 557-record source-bound append',
})
if __name__=='__main__':
    from dk4tool.patch.late_editorial_extensions_v1 import BUILDER_STAGE
    block=checked_text('def source_block():\n'+BUILDER_STAGE,{"profile_config.get('late_editorial_extensions', [])":"pending_registered_extensions"}).split('\n',1)[1]
    raw=Path('scripts/build_integrated_release.py').read_text(encoding='utf-8')
    tail=raw[raw.index('    # Lexically valid "% o"'):raw.index('\n\nif __name__ == "__main__":')]
    compile('def complete_registered_checkpoint():\n'+block+tail,'original-extension-and-final-contract-preflight','exec')
    exec(compile(source,__file__+'::same-qualified-registration-preserving-prior-profiles','exec'),globals())
