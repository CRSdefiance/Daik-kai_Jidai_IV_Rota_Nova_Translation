"""Own planned two-layer Help identity capture; final registered equality remains mandatory."""
from scripts import capture_shipyard_HELP37_startup as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous.source,{
    'Shipyard_HELP37_identity_coldboot_20261104':'Sea22_Fleet66_identity_coldboot_20261105',
    'Shipyard_HELP37_release_v2_20261104/registered_preparation.json':'Sea22_Fleet66_release_v2_20261104/registered_preparation.json',
    'Town_HELP23_release_verified_20261104/own_registered_startup_verification.json':'Shipyard_HELP37_release_verified_20261104/own_registered_startup_verification.json',
})
exec(compile(source,__file__+'::same-own-final-identity-Rafael-coldboot-for-two-ordered-Help-layers','exec'),globals())
