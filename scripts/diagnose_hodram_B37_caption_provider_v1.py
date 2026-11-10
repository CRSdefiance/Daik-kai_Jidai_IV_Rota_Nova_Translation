"""Preserve the exact provider assertion with explicit expected/actual label evidence."""
from scripts import check_editorial_two_choice_scope_reuse_v1 as prior
from scripts.check_editorial_compiled_pages_scope_reuse_v1 import qualified_current_native_context
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(prior.source,{
    "            assert result['labels']==expected":
        "            assert result['labels']==expected,(name,alignment,expected,result['labels'],len(raw))",
})
env={**vars(prior),**globals(),'__file__':__file__}
exec(compile(source,__file__+'::same-provider-guard-explicit-failure-evidence','exec'),env)
