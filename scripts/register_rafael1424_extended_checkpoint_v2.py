"""Preserve the pre-ROM entrypoint failure and register its checked successor."""
import runpy
from pathlib import Path
from scripts.register_rafael1424_extended_checkpoint_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    'scripts.registered_canonical_extension_resume_v4 import STAGES,qualify,stage_source':
        'scripts.registered_canonical_extension_resume_v5 import STAGES,qualify,stage_source',
    'Rafael1424_registered_extended_resume_v1_20261105':'Rafael1424_registered_extended_resume_v2_20261105',
    'rafael1424_canonical_extension_resume_v1.json':'rafael1424_canonical_extension_resume_v2.json',
    'all-routes-rafael1424-extended-checkpoint-20261105':'all-routes-rafael1424-extended-checkpoint-v2-20261105',
    "prepared_registry=str(root/'release_stack_before.json'),":
        "prepared_registry='work/analysis/Rafael1424_registered_extended_resume_v1_20261105/release_stack_before.json',",
    "Path('scripts/registered_canonical_extension_resume_v4.py'),":
        "Path('scripts/registered_canonical_extension_resume_v5.py'),Path('scripts/registered_canonical_extension_resume_v4.py'),",
    "Path('scripts/resume_extended_release_with_'+s+'_v4.py')":"Path('scripts/resume_extended_release_with_'+s+'_v5.py')",
    'release_stack.Rafael1424_extended_resume_v1.pending.json':'release_stack.Rafael1424_extended_resume_v2.pending.json',
})
if __name__=='__main__':
    from scripts.registered_canonical_extension_resume_v5 import STAGES,stage_source
    from dk4tool.patch.late_editorial_extensions_v1 import BUILDER_STAGE
    from scripts.audit_story_glyph_consistency import load
    prior=load(Path('work/analysis/Rafael1424_extended_build_gc_v1_20261105/completion.json'))
    assert prior['terminal'] and not prior['driver_completed_without_exception']
    for stage in STAGES:
        script=Path('scripts/resume_extended_release_with_'+stage+'_v5.py')
        assert callable(runpy.run_path(str(script),run_name='registered_nested_stage_preflight')['main'])
        compile(stage_source(stage),str(script)+'::original-body-preflight','exec')
    block=checked_text('def source_block():\n'+BUILDER_STAGE,{"profile_config.get('late_editorial_extensions', [])":"pending_registered_extensions"}).split('\n',1)[1]
    raw=Path('scripts/build_integrated_release.py').read_text(encoding='utf-8')
    tail=raw[raw.index('    # Lexically valid "% o"'):raw.index('\n\nif __name__ == "__main__":')]
    compile('def complete_registered_checkpoint():\n'+block+tail,'original-extension-and-final-contract-preflight','exec')
    exec(compile(source,__file__+'::same-qualification-with-all-nested-entries-preflighted','exec'),globals())
