"""Fresh preparation after metadata-only retention schema correction;preserve failed v1 artifacts."""
from scripts import prepare_shipyard_HELP37_release as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous.source,{
 'Shipyard_HELP37_release_20261104':'Shipyard_HELP37_release_v2_20261104',
 'translations/shipyard_help37_editorial_release_v1.json':'translations/shipyard_help37_editorial_release_v2.json',
 '_shipyard_HELP37_release_v1.json':'_shipyard_HELP37_release_v2.json',
 'translations/help_shipyard37_contextual_final_review_v2.json':'translations/help_shipyard37_contextual_final_review_v3.json',
 'production_plan_v2.json':'production_plan_v3.json',
})
exec(compile(source,__file__+'::same-unchanged-eight-stage-registration-correct-retention-metadata-fresh-paths','exec'),globals())
