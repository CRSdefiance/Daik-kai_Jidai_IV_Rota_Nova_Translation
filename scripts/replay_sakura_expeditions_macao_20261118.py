"""Replay Rafael excerpts and Maria's original Macao inquiry in initialized openings."""

from argparse import ArgumentParser
from types import FunctionType, SimpleNamespace

from scripts import replay_rafael_mosque_20261118 as rafael
from scripts import replay_ruins_clues_and_guides_20261118 as maria
from scripts import stage_sakura_expeditions_macao_20261118 as stage
from scripts.source_locked_derivation_v5118 import checked_text

base, native = stage.base, stage.native
ROOT = stage.ROOT / "rafael_initialized"
ROM = ROOT / "Rafael_Sakura_Excerpts_RESEARCH_ONLY.nds"
SETUP = ROOT / "fixture.json"
LIVE = ROOT / "verified.json"
LAST = 8201
EXCERPTS = (
    (321, (6, 9, 22, 26)),
    (322, (35, 39, 44, 65)),
    (323, (48, 68, 73, 90, 100)),
    (327, (102, 113, 181, 194)),
)

rafael_scope = rafael.scope | globals()
for text, label in ((rafael.prep, "source-owned-Rafael-excerpts"), (rafael.audit, "matched-native-pixels")):
    exec(compile(text, __file__ + "::" + label, "exec"), rafael_scope)
rafael_capture = FunctionType(rafael.capture.__code__, rafael_scope)
startup = FunctionType(rafael.startup.__code__, rafael_scope)

maria_root = stage.ROOT / "macao_replay"
maria_rom = maria_root / "Maria_Macao_RESEARCH_ONLY.nds"
maria_fixture = maria_root / "fixture.json"
maria_live = maria_root / "verified.json"
maria_scope = maria.scope | {
    "ROOT": maria_root, "ROM": maria_rom, "FIXTURE": maria_fixture,
    "stage": stage, "FOREST": 276, "FIRST": 8,
}
maria_prep = checked_text(maria.prepare_source, {
    "Maria's map guide with initialized setup and the original two paths beyond the dead end.":
        "The complete original Macao inquiry, played in the initialized Maria opening.",
    "omitted_map_gate=True": "omitted_map_gate=False",
    '== "00000080"': '== "00000000"',
})
exec(compile(maria_prep, __file__ + "::complete-original-Macao-entry", "exec"), maria_scope)
maria_capture = FunctionType(maria.capture.__code__, maria_scope)
MACAO = SimpleNamespace(ROOT=maria_root, ROM=maria_rom, FIXTURE=maria_fixture, LIVE=maria_live)

if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "prepare_macao", "rafael", "macao", "verify_rafael", "startup"))
    action = parser.parse_args().action
    if action == "prepare":
        rafael_scope["prepare"]()
        maria_scope["prepare"]()
    elif action == "prepare_macao":
        maria_scope["prepare"]()
    elif action == "rafael":
        rafael_capture()
    elif action == "macao":
        maria_capture("live", [(n,"A") for n in range(4200, 10001, 350)], 10301)
    elif action == "verify_rafael":
        rafael_scope["verify"]()
    else:
        startup()

