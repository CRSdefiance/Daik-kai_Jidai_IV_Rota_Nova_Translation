"""Register a source-qualified fix for the pre-ROM percent check mismatch."""
import runpy
from pathlib import Path
from scripts.register_rafael1424_extended_checkpoint_v2 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

PERCENT_PROOF=Path('work/analysis/Rafael557_story_percent_relocation_v1_20261105/qualification.json')
source=checked_text(previous,{
    'scripts.registered_canonical_extension_resume_v5 import STAGES,qualify,stage_source':
        'scripts.registered_canonical_extension_resume_v6 import STAGES,qualify,stage_source',
    'Rafael1424_registered_extended_resume_v2_20261105':'Rafael1424_registered_extended_resume_v3_20261105',
    'rafael1424_canonical_extension_resume_v2.json':'rafael1424_canonical_extension_resume_v3.json',
    'all-routes-rafael1424-extended-checkpoint-v2-20261105':'all-routes-rafael1424-extended-checkpoint-v3-20261105',
    'release_stack.Rafael1424_extended_resume_v2.pending.json':'release_stack.Rafael1424_extended_resume_v3.pending.json',
    "Path('scripts/registered_canonical_extension_resume_v5.py'),":
        "Path('scripts/registered_canonical_extension_resume_v6.py'),Path('scripts/registered_canonical_extension_resume_v5.py'),"
        "PERCENT_PROOF,Path('dk4tool/script/format_safety_relocated_v1.py'),Path('dk4tool/script/format_safety.py'),",
    "Path('scripts/resume_extended_release_with_'+s+'_v5.py')":"Path('scripts/resume_extended_release_with_'+s+'_v6.py')",
    "expected_prefix_entries=673,":"expected_prefix_entries=673,\n        percent_relocation_guard=dict(path=str(PERCENT_PROOF),sha256=sha(PERCENT_PROOF.read_bytes())),",
})
if __name__=='__main__':
    from scripts.registered_canonical_extension_resume_v6 import STAGES,stage_source,derive_tail
    from dk4tool.patch.late_editorial_extensions_v1 import BUILDER_STAGE
    from scripts.audit_story_glyph_consistency import load
    prior=load(Path('work/analysis/Rafael1424_extended_build_gc_v2_20261105/completion.json'))
    assert prior['terminal'] and not prior['driver_completed_without_exception']
    for stage in STAGES:
        script=Path('scripts/resume_extended_release_with_'+stage+'_v6.py')
        assert callable(runpy.run_path(str(script),run_name='registered_nested_stage_preflight')['main'])
        compile(stage_source(stage),str(script)+'::original-body-preflight','exec')
    block=checked_text('def source_block():\n'+BUILDER_STAGE,{"profile_config.get('late_editorial_extensions', [])":"pending_registered_extensions"}).split('\n',1)[1]
    raw=Path('scripts/build_integrated_release.py').read_text(encoding='utf-8')
    tail=raw[raw.index('    # Lexically valid "% o"'):raw.index('\n\nif __name__ == "__main__":')]
    compile('def complete_registered_checkpoint():\n'+block+derive_tail(tail),'qualified-final-contract-preflight','exec')
    exec(compile(source,__file__+'::same-registration-plus-exact-percent-guard-proof','exec'),globals())
