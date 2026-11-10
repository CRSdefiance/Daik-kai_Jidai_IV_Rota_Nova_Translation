"""Run the registered exact source-bound percent-guard successor."""
from scripts.run_registered_extension_resume_with_gc_v5 import source as previous,restoration,restoration_path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    "DRIVER=Path('scripts/resume_extended_release_with_Fernan_field_v5.py')":
        "DRIVER=Path('scripts/resume_extended_release_with_Fernan_field_v6.py')",
    'from scripts.registered_canonical_extension_resume_v5 import STAGES':
        'from scripts.registered_canonical_extension_resume_v6 import STAGES',
    "Path('scripts/registered_canonical_extension_resume_v5.py'),":
        "Path('scripts/registered_canonical_extension_resume_v5.py'),Path('scripts/registered_canonical_extension_resume_v6.py'),Path('dk4tool/script/format_safety_relocated_v1.py'),",
    "Path('scripts/resume_extended_release_with_'+stage+'_v5.py')":
        "Path('scripts/resume_extended_release_with_'+stage+'_v6.py')",
    'no_test_skip_rewrite_orrelaxed_release_contract=True':
        'no_test_skip_or_relaxed_release_contract=True,source_bound_percent_record_lookup_derivation_only=True',
})
if __name__=='__main__':exec(compile(source,__file__+'::same-locked-stages-exact-source-percent-guard','exec'),globals())
