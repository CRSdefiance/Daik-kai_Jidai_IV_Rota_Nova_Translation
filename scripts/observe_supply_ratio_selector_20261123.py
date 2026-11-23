"""Accept the resupply mix prompt and trace the original ratio dialog."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import observe_market_context_v2112 as native
from scripts import replay_port_resupply_options_20261119 as history
from scripts.reconcile_editorial_acceptance_20261123 import digest, read
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = Path(".codex-release-work/supply_ratio_selector_20261123_v6")
RELEASE = Path("releases/all_routes_editorial_20261123_sound_play_stop_candidate/verification/registered_release_verification.json")
ACCEPT, DESCRIPTOR, PAINTER = 0x02060500, 0x02086390, 0x020D5404
TARGETS = (ACCEPT, DESCRIPTOR, PAINTER)
JAPANESE_LABEL, ENGLISH_HEADING = (0x0214A110, 0x0214A44C)
FRAMES = (3200, 3550, 3750, 3950, 4200, 4450, 4700, 4950, 5200, 5500, 5750, 6000)


def observer(rom, folder):
    env = vars(native) | dict(ROOT=folder, ROM=rom, TARGETS=TARGETS, __file__=__file__,
        ACCEPT=ACCEPT, DESCRIPTOR=DESCRIPTOR, PAINTER=PAINTER, TEXT=(JAPANESE_LABEL, ENGLISH_HEADING))
    setup = checked_text(getsource(native.prepare_contract), {"for pc in(REQUEST,FONT):": "for pc in TARGETS:"})
    exec(compile(setup, __file__ + "::ratio-observer-contract", "exec"), env)
    env["prepare_contract"]()
    source = getsource(native.Observer)
    start = source.index("    if frame<31000:return")
    end = source.index("   except BaseException as exc:", start)
    body = '''    if pc==PAINTER and v[5] not in TEXT:return
    if pc==DESCRIPTOR:
     pointer=v[6];assert pointer==0x02119808
     text_pointer,=struct.unpack('<I',ct.string_at(self.wram+pointer+4-0x02000000,4))
     assert text_pointer==TEXT[0]
    elif pc==PAINTER:
     pointer=None;text_pointer=v[5]
    else:
     pointer=None;text_pointer=None
     assert pc==ACCEPT and v[4]==0x191
    key=(pc,pointer,text_pointer)
    if key in self.seen:return
    self.seen.add(key)
    value=ct.string_at(self.wram+text_pointer-0x02000000,32).split(b'\\0',1)[0] if text_pointer else b''
    self.rows.append(dict(frame=frame,PC=pc,descriptor_address=pointer,text_pointer=text_pointer,text_hex=value.hex()))
'''
    exec(compile(source[:start] + body + source[end:], __file__ + "::ratio-use", "exec"), env)
    return env["Observer"]


def replay(root, stage=None):
    receipt = read(RELEASE)
    rom = Path(receipt["candidate"])
    assert digest(rom) == receipt["candidate_sha256"]
    assert digest("translations/release_stack.json") == receipt["registry_sha256"]
    release = RELEASE
    if stage:
        release = stage
        proposed = read(stage)
        assert proposed["predecessor_sha256"] == receipt["candidate_sha256"]
        assert proposed["clean_input_sha256"] == receipt["clean_input_sha256"]
        rom = Path(proposed["candidate"])
        assert digest(rom) == proposed["candidate_sha256"]
        receipt = proposed
    current = SimpleNamespace(RELEASE=release, ROM=rom, native=history.current.native)
    source = checked_text(getsource(history.run), {
        'buttons = [(3601, "B"), (4901, "B")] if mode == "mix" else [(3601, "A"), (4001, "A"), (4901, "B")]':
        'buttons = [(3601, "B"), (4051, "A"), (4301, "L"), (4551, "R"), (4801, "L"), (5051, "A"), (5601, "B")]',
        "    try:\n        fixture_adapter.set_condition": "    try:\n        harness.ct = Loader()\n        fixture_adapter.set_condition",
        "        fixture_adapter.set_condition, sys.stdin, sys.argv = old, old_stdin, old_argv":
        "        harness.ct = original_loader\n        fixture_adapter.set_condition, sys.stdin, sys.argv = old, old_stdin, old_argv",
    })
    hooks, original_loader = [], history.harness.ct
    cls = observer(rom, root / "observer")

    class Loader:
        def __getattr__(self, name):
            return getattr(original_loader, name)

        def CDLL(self, path, *args, **kwargs):
            core = original_loader.CDLL(path, *args, **kwargs)
            if str(path).lower().endswith("desmume_libretro.dll"):
                trace = cls(core, root / "observer")
                trace.install()
                hooks.append(trace)
                tick = core.retro_run

                def advance():
                    trace.header[0] += 1
                    tick()

                core.retro_run = advance
            return core

    fixture = checked_text(getsource(history.state_for), {
        'earlier = base.NdsImage.open("out/all_routes_combined_v762_candidate.nds").read_file(current.native.ARM)':
            'earlier = base.NdsImage.open("work/clean.nds").read_file(current.native.ARM)',
        'fixture_source_sha256=base.digest(__file__))':
            'fixture_source_sha256=base.digest(__file__), clean_ARM9_sha256=current.native.digest(earlier))',
    })
    assert digest("work/clean.nds") == receipt["clean_input_sha256"]
    clean, installed = (history.base.NdsImage.open(path).read_file(current.native.ARM)
                        for path in ("work/clean.nds", rom))
    for start, stop in ((0xCB160, 0xCB16C), (0x397D8, 0x39800)):
        assert clean[start:stop] == installed[start:stop]
    env = vars(history) | dict(current=current, ROOT=root, FRAMES=FRAMES, Loader=Loader,
                                original_loader=original_loader, __file__=__file__)
    exec(compile(fixture, __file__ + "::clean-bound-supply-fixture", "exec"), env)
    exec(compile(source, __file__ + "::qualified-ratio-replay", "exec"), env)
    try:
        env["run"]("mix")
    finally:
        for trace in hooks:
            trace.close()
            trace.save()
    report = read(root / "mix/capture/capture_report.json")
    assert report["ROM_sha256"] == receipt["candidate_sha256"] and report["cold_boot"]
    assert not report["callback_errors"] and not report["savestate_loaded"]
    print(f"Captured the Copenhagen supply-ratio control sequence on {rom.name}.")


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT)
    parser.add_argument("--stage", type=Path)
    args = parser.parse_args()
    replay(args.output, args.stage)
