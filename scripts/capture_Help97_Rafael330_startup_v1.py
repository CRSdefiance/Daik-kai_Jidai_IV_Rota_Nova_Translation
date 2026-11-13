"""Capture the exact planned cumulative identity once;registered equality remains mandatory."""
from scripts import capture_sea22_fleet66_startup as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous.source,{
    'Sea22_Fleet66_identity_coldboot_20261105':'Help97_Rafael330_identity_coldboot_20261105',
    'Sea22_Fleet66_release_v2_20261104/registered_preparation.json':'Help97_Rafael330_release_v2_20261105/registered_preparation.json',
    'Shipyard_HELP37_release_verified_20261104/own_registered_startup_verification.json':
        'Sea22_Fleet66_release_verified_20261105/own_registered_startup_verification.json',
})
exec(compile(source,__file__+'::same-own-Rafael-initialized-coldboot-exact-three-layer-planned-identity','exec'),globals())
