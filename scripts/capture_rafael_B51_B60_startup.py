"""Cold boot the exact planned final identity; bind it to the registered output after build."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/capture_shared_tutorial_name_data_startup.py').read_text(encoding='utf-8'),{
    'Shared_tutorial_name_data_identity_coldboot_20261104':'Rafael_B51_B60_identity_coldboot_20261104',
    'Shared_tutorial_name_data_release_v4_20261104/registered_preparation.json':
        'Rafael_B51_B60_release_registry_v2_20261104/registered_preparation.json',
    'Rafael_B36_B41_release_verified_20261104/own_registered_startup_verification.json':
        'Shared_tutorial_name_data_release_verified_20261104/own_registered_startup_verification.json',
    "prep['reference_ROM']":"prep['final_ROM']",
})
exec(compile(source,__file__+'::same-own-identity-Rafael-coldboot-updated-final-reference','exec'),globals())
