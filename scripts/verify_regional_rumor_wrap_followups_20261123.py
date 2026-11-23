"""Verify the revised rumors through the ordinary Square entrances."""

from inspect import getsource
from types import SimpleNamespace

from scripts import stage_regional_rumor_wrap_followups_20261123 as staged
from scripts import verify_current_regional_towns_20261123 as observed
from scripts import verify_square_rumor_followup_20261122 as prior
from scripts.source_locked_derivation_v5118 import checked_text


stage = SimpleNamespace(**(vars(staged) | {"regional": staged.prior.regional}))
LIVE = stage.ROOT / "ordinary_dialogue.json"
SHEET = stage.ROOT / "regional_ordinary.png"
scope = vars(prior) | globals()
source = checked_text(getsource(prior.verify), {
    'stage.regional.OUTPUT': 'observed.OUT',
    'prior["actual_cold_boot_saved_gameplay"]': 'prior["ordinary_battery_save_gameplay"]',
    'prior["original_town_dialogue"][city]': 'prior["town_visits"][city]["verified_common"]',
    'original["current_hex"]': 'original["installed_hex"]',
    'revised_offline_only_records=[725]': 'revised_offline_only_records=[]',
})
exec(compile(source, __file__ + "::ordinary-square-rumors", "exec"), scope)


if __name__ == "__main__":
    scope["verify"]()
