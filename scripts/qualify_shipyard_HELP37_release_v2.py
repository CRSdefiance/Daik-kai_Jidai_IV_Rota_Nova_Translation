"""Same full qualification against the fresh retention-schema-correct preparation."""
from scripts import qualify_shipyard_HELP37_release as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous.source,{
 'Shipyard_HELP37_release_qualification_20261104':'Shipyard_HELP37_release_qualification_v2_20261104',
 'Shipyard_HELP37_release_20261104':'Shipyard_HELP37_release_v2_20261104',
})
exec(compile(source,__file__+'::same-source-controls-andall-stage-contract-tests-onfresh-preparation','exec'),globals())
