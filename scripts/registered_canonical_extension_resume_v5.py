"""Preserve all prefix/stage guards while dispatching callable nested drivers."""
from scripts.registered_canonical_extension_resume_v4 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    'scripts.registered_canonical_extension_resume_v4 import resume_checkpoint':
        'scripts.registered_canonical_extension_resume_v5 import resume_checkpoint',
    "'scripts/resume_extended_release_with_'+prior+'_v4.py'":
        "'scripts/resume_extended_release_with_'+prior+'_v5.py'",
})
exec(compile(source,__file__+'::same-prefix-and-stage-guards-callable-nested-entries','exec'),globals())
