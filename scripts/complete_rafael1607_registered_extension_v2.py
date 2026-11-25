"""Read and clear the pending key actually written by the tutorial manuscript."""
from scripts.complete_rafael1607_registered_extension_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    "if k!='registered_release_andcompletion_credit_pending'":
        "if k!='registered_release_and_completion_credit_pending'",
    'registered_release_andcompletion_credit_pending=False,new_source_credit_eligible=True':
        'registered_release_and_completion_credit_pending=False,new_source_credit_eligible=True',
})
if __name__=='__main__':
    exec(compile(source,__file__+'::same-credit-exact-tutorial-pending-key','exec'),globals())
