"""Exercise selected enemy, neutral and uncontracted cities with ordinary inputs."""

from inspect import getsource

from scripts import observe_current_regional_orders_20261123 as earlier


ROOT = earlier.ROOT.with_name("regional_attack_targets_area")
KEYS = (
    (7001, "DOWN"), (7401, "DOWN"), (7801, "DOWN"), (8201, "A"),
    (8601, "A"), (9001, "X"), (9401, "A"), (9801, (148, 90)), (10201, "A"),
    (10601, "A"), (11001, "A"), (11401, (63, 117)), (11801, "A"),
    (12201, "A"), (12601, "A"), (13001, (122, 103)), (13401, "A"),
    (13801, "A"), (14201, "B"),
)


def schedule(case):
    assert case == "targets"
    previous, _, _, history, donor = earlier.schedule("regional")
    inputs = [row for row in previous if row["start"] <= 6601]
    for frame, key in KEYS:
        event = dict(start=frame, duration=8, buttons=[key] if isinstance(key, str) else [])
        if not isinstance(key, str):
            event["touch"] = list(key)
        inputs.append(event)
    return inputs, [frame + 399 for frame, _ in KEYS], 14600, history, donor


def main():
    assert not (ROOT / "targets").exists()
    release = earlier.base.load(earlier.current.RELEASE)
    assert earlier.base.digest(earlier.base.REGISTRY) == release["registry_sha256"]
    scope = vars(earlier.playback) | dict(ROOT=ROOT, parent=earlier.current,
        observer=earlier.trace.scoped_observer, get_schedule=schedule,
        FOCUS=set(range(3668)), __file__=__file__)
    exec(compile(getsource(earlier.playback.main), __file__ + "::regional-attack-pick-targets", "exec"), scope)
    scope["main"]("targets")


if __name__ == "__main__":
    main()
