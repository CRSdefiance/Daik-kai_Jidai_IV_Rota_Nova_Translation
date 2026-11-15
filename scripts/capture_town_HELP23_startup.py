"""Capture the planned Town Help identity; final registered equality remains mandatory."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/capture_shared_tutorial_name_data_startup.py').read_text(encoding='utf-8'),{
 'Shared_tutorial_name_data_identity_coldboot_20261104':'Town_HELP23_identity_coldboot_20261104',
 'Shared_tutorial_name_data_release_v4_20261104/registered_preparation.json':'Town_HELP23_release_20261104/registered_preparation.json',
 'Rafael_B36_B41_release_verified_20261104/own_registered_startup_verification.json':'Early_HELP23_release_verified_20261104/own_registered_startup_verification.json',
 "prep['reference_ROM']":"prep['final_ROM']",
})
exec(compile(source,__file__+'::same-own-identity-Rafael-coldboot-TownHelp23','exec'),globals())
