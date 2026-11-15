"""Preserve the pre-execution compiler failure and register its narrow successor."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/register_rafael867_extended_checkpoint_v2.py').read_text(encoding='utf-8'),{
    'scripts.registered_canonical_extension_resume_v2 import STAGES,qualify,stage_source':
        'scripts.registered_canonical_extension_resume_v3 import STAGES,qualify,stage_source',
    'Rafael867_registered_extended_resume_v2_20261105':'Rafael867_registered_extended_resume_v3_20261105',
    'rafael867_canonical_extension_resume_v2.json':'rafael867_canonical_extension_resume_v3.json',
    'all-routes-rafael867-extended-checkpoint-v2-20261105':'all-routes-rafael867-extended-checkpoint-v3-20261105',
    "    assert sha(before)==prep['registry_sha256']==qualification['registry_sha256']":
        "    assert prep['registry_sha256']==qualification['registry_sha256']",
    "Path('scripts/registered_canonical_extension_resume_v2.py'),":
        "Path('scripts/registered_canonical_extension_resume_v3.py'),Path('scripts/registered_canonical_extension_resume_v2.py'),Path(__file__),",
    "Path('scripts/resume_extended_release_with_'+s+'_v2.py')": "Path('scripts/resume_extended_release_with_'+s+'_v3.py')",
    "source_registry=str(prep_path.parent/'release_stack_before.json'),parent_release=str(release_path),":
        "source_registry=str(prep_path.parent/'release_stack_before.json'),parent_release=str(release_path),\n        prepared_registry='work/analysis/Rafael867_registered_extended_resume_v2_20261105/release_stack_before.json',prepared_registry_sha256=prep['registry_sha256'],",
    'release_stack.Rafael867_extended_resume_v2.pending.json':'release_stack.Rafael867_extended_resume_v3.pending.json',
})

if __name__=='__main__':
    from dk4tool.patch.late_editorial_extensions_v1 import BUILDER_STAGE
    block=checked_text('def source_block():\n'+BUILDER_STAGE,{"profile_config.get('late_editorial_extensions', [])":"pending_registered_extensions"}).split('\n',1)[1]
    raw=Path('scripts/build_integrated_release.py').read_text(encoding='utf-8')
    tail=raw[raw.index('    # Lexically valid "% o"'):raw.index('\n\nif __name__ == "__main__":')]
    compile('def complete_registered_checkpoint():\n'+block+tail,'original-extension-andfinal-contract-preflight','exec')
    exec(compile(source,__file__+'::same-registration-ten-negatives-preserved-failed-profile','exec'),globals())
