"""Keep every native guard and save a durable receipt after each completed record."""
from scripts import check_editorial_compiled_pages_scope_reuse_v1 as prior
from scripts.check_editorial_compiled_pages_scope_reuse_v1 import qualified_current_native_context
from scripts.check_editorial_compiled_pages_v6 import check_FE_rows
from scripts.check_editorial_compiled_pages_v7 import validate_documented_layouts
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(prior.source,{
    "                complete_native_English_display=rendered))":
        """                complete_native_English_display=rendered))
            save(args.out/(row['id']+'_checked_record.json'),dict(record=rows[-1],runtime=ctx.receipt(),font_sha256=sha(font),
                manuscript=str(args.manuscript),manuscript_sha256=sha(args.manuscript.read_bytes()),
                plan=str(args.plan),plan_sha256=sha(args.plan.read_bytes()),native_context_reuse=scope_reuse,
                original_complete_record_native_assertions_passed_before_checkpoint=True,
                actual_gameplay=False,new_credit=0,producer_sha256=sha(Path(__file__).read_bytes())))""",
})
env={**vars(prior),**globals(),'__file__':__file__}
exec(compile(source,__file__+'::same-native-checks-durable-completed-record-checkpoints','exec'),env)
