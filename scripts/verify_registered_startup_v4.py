"""Own final startup with exact reviewed RGB reuse and the next-field inverse."""
from dk4tool.patch.owned_name_fields_v2 import plan_arm9_name_fields
from scripts import verify_registered_startup_v3 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous.source,{
    "profile['owned_name_fields']":"profile['owned_name_fields_next']",
})
exec(compile(source,__file__+'::own-startup-with-preserved-prior-and-next-name-fields','exec'),globals())
