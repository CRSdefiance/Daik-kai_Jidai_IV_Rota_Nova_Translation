"""Clear the now-qualified style/caption pending metadata before once-only credit."""
from scripts.complete_hodram_B211_B230_registered_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    "('formatting_visual_stored_gameplay_andregistered_release_pending','registered_release_andcompletion_credit_pending')":
        "('formatting_visual_stored_gameplay_andregistered_release_pending','registered_release_andcompletion_credit_pending','native_style_dispatch_andall_five_review_gates_pending','all_five_review_gates_pending')",
})
if __name__=='__main__':exec(compile(source,__file__+'::same-credit-clears-qualified-compound-gate-metadata','exec'),globals())
