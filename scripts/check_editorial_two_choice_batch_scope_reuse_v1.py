"""Use the same complete-menu batch runner with the guarded scoped-runtime driver."""
import inspect
from scripts import check_editorial_two_choice_batch as prior
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(inspect.getsource(prior.main),{
    "'scripts/check_editorial_two_choice_display.py'":"'scripts/check_editorial_two_choice_scope_reuse_v1.py'",
})
env={**vars(prior),'__file__':__file__}
exec(compile(source,__file__+'::same-complete-caption-subsets-and-native-receipt-join','exec'),env)

if __name__=='__main__':env['main']()
