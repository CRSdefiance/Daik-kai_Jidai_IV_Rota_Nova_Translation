"""Replay the same ordinary Azores approach and enter the recorded English answer."""

from inspect import getsource
from pathlib import Path
from string import ascii_letters
from types import SimpleNamespace

from scripts import observe_online_gallery_common_v1 as playback
from scripts import observe_setup_save_common_v1 as trace
from scripts.observe_lisbon_azores_voyage_20261123 import DONOR, RELEASE, ROOT
from scripts.reconcile_editorial_acceptance_20261123 import digest, read
from scripts.source_locked_derivation_v5118 import checked_text


ANSWER = "Terceira"
OBSERVED = ROOT / "capture/capture_report.json"
OUTPUT = ROOT.with_name("lisbon_azores_words_v2")
ANSWER_SOURCE = Path("translations/village_promised_words_manuscript_v1.json")


def schedule(case):
    assert case == "correct"
    prior = read(OBSERVED)
    assert prior["ROM_sha256"] == read(RELEASE)["candidate_sha256"]
    assert prior["cold_boot"] and not prior["savestate_loaded"] and not prior["callback_errors"]
    assert not any(value for key, value in prior.items() if key.startswith("synthetic_"))
    donor = prior["battery_save_preloaded"]
    assert digest(DONOR) == digest(donor["source"]) == donor["source_sha256"]
    entry, = [row for row in read(ANSWER_SOURCE)["records"] if row["kind"] == "ANSWER" and row["index"] == 13]
    assert entry["english"] == ANSWER
    events = [e for e in prior["scripted_input_schedule"] if e["start"] <= 9841]
    events.append(dict(start=10221, buttons=[], touch=[164, 134], duration=8))
    cursor = 10291
    frames = [8550, 9300, 9620, 10120, 10340]
    for letter in ANSWER:
        index = ascii_letters.index(letter)
        events.extend((
            dict(start=cursor, buttons=["A"], duration=8),
            dict(start=cursor + 80, buttons=[], touch=[62 + index % 10 * 14, 30 + index // 10 * 14], duration=8),
        ))
        frames.append(cursor + 150)
        cursor += 155
    for button, wait in (("X", 240), ("A", 280), ("A", 280), ("A", 280)):
        events.append(dict(start=cursor, buttons=[button], duration=8))
        frames.append(cursor + wait - 5)
        cursor += wait
    return events, frames, cursor + 20, OBSERVED, donor


def main():
    assert not OUTPUT.exists()
    release = read(RELEASE)
    assert digest("translations/release_stack.json") == release["registry_sha256"]
    parent = SimpleNamespace(ROM=Path(release["candidate"]), RELEASE=RELEASE)
    source = checked_text(getsource(playback.main), {
        "'--capture-at', *map(str, frames)]": "'--dump-capture-ram', '--capture-at', *map(str, frames)]",
    })
    scope = vars(playback) | dict(ROOT=OUTPUT, parent=parent, observer=trace.scoped_observer,
        get_schedule=schedule, FOCUS=set(range(3668)), __file__=__file__)
    exec(compile(source, __file__ + "::ordinary-promised-words", "exec"), scope)
    scope["main"]("correct")


if __name__ == "__main__":
    main()
