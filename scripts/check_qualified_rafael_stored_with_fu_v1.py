"""Keep complete stored consumer guards and bind the qualified full-name macro."""
from scripts import check_qualified_rafael_stored_batch_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

check_FE_rows=previous.check_FE_rows
progressive_expand=previous.progressive_expand
FE_expand=previous.FE_expand
source=checked_text(previous.source,{
    ".replace(b'FO',b'Castor Co.')":".replace(b'FO',b'Castor Co.').replace(b'FU',b'Rafael Castor')",
    "macros['source_owned_progressive_adapter']":"native['source_owned_progressive_macro_adapter']",
    "    progressive_env=dict(progressive_expand.__globals__)":
        "    assert identity['macro_ascii_lengths']==dict(FI=6,FA=6,FO=10,FU=13) and identity['macro_widths']['FU']==78\n    progressive_env={**progressive_expand.__globals__,'DYNAMIC_BINDINGS':native['dynamic_role_bindings']}",
})
exec(compile(source,__file__+'::same-complete-stored-consumers-qualified-FU-andoriginal-scratch-ring-guards','exec'),globals())
