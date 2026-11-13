"""Keep complete native menu pixels, cursor, background and A-return checks with exact receipt keys."""
from scripts.analyze_maria390_menu_actual_v1 import source as previous
from scripts.analyze_maria301_display_v1 import verified_existing_unlock
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(previous,{"exact['native_receipt']":"exact['proof']","exact['native_receipt_sha256']":"exact['proof_sha256']"})
if __name__=='__main__':exec(compile(source,__file__+'::same-live-caption-centering-cursor-background-input-andreturn-guards','exec'),globals())
