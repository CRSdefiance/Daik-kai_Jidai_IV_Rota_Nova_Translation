from types import FunctionType
from scripts import stage_help_market_terms_20261119 as stage
from scripts import audit_square_shop_followup_20261119 as audit
from scripts import replay_ceuta_lesson_20261119 as boot
from scripts import replay_sea_hazard_dialogue_20261119 as boot_entry
from scripts import replay_square_shop_followup_20261119 as prior_play

if __name__ == "__main__":
    play = type("Startup", (), {"STARTUP": stage.ROOT / "startup_fixture"})
    run = FunctionType(boot_entry.previous.startup.__code__, vars(boot_entry.previous) |
                       {"stage": stage, "STARTUP": play.STARTUP})
    run()
    verify = FunctionType(audit.startup.__code__, vars(audit) |
                          {"build": stage, "play": play, "STARTUP": stage.ROOT / "own_startup_verification.json"})
    verify()
