"""Prepare the original Crown scene after Hodram's intact opening prelude."""
from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from struct import pack_into
import sys
from types import FunctionType

from scripts import replay_story_market_terms_20261119 as startup_template
from scripts import run_Hodram_scenes_v8280 as runner
from scripts import stage_hodram_mihwa_crown_20261119 as build
from scripts.source_locked_derivation_v5118 import checked_text

base, native = build.base, build.native
ROOT = build.ROOT / "crown_replay"
FIXTURE, FIXTURES = ROOT / "Hodram_Crown_RESEARCH_ONLY.nds", ROOT / "fixtures.json"
STARTUP = build.ROOT / "startup_fixture"
STARTUP_PROOF = build.ROOT / "own_startup_verification.json"
FILE = "/data/SC1.DK4"
FRAMES = 10401


def prepare():
    assert not ROOT.exists()
    stored = base.load(build.PROOF)
    assert stored["candidate_sha256"] == base.digest(build.ROM)
    image = base.NdsImage.open(build.ROM)
    clean = base.NdsImage.open(native.CLEAN)
    archive = native.IlnkContainer.parse(image.read_file(FILE))
    original = image.read_file(FILE)
    original_host, scene = (archive.blocks[n] for n in (42, 89))
    clean_host = native.IlnkContainer.parse(clean.read_file(FILE)).blocks[42]
    inventory, _, _ = native.scoped_inventory()
    arm = image.read_file(native.ARM)
    host_commands, speeches = inventory(arm, original_host)
    first = speeches[0]["offset"]
    prelude = original_host[8:first]
    assert first == 42 and prelude == clean_host[8:first]
    initializers = [r for r in host_commands if r["offset"] < first]
    assert len(initializers) == 8 and len(prelude) == 34
    assert (original_host[:4], original_host[6:8]) == (scene[:4], scene[6:8])
    logical = bytearray(original_host[:8] + prelude + scene[8:build.logical_end(scene)])
    pack_into("<H", logical, 4, len(logical) - 8)
    new_host = bytes(logical) + bytes(-len(logical) % 4)
    parsed, text = inventory(arm, new_host)
    assert parsed[-1]["word"] == 0 and len(text) == 18
    group, = stored["groups"]
    assert native.digest(scene) == group["after"]
    records = []
    for row, shifted in zip(group["commands"], parsed[len(initializers):], strict=True):
        at, data = row["stored_offset"] + len(prelude), bytes.fromhex(row["stored"])
        assert shifted["offset"] == at and shifted["word"] == row["word"]
        assert new_host[at:at + len(data)] == data
        assert bytes.fromhex(shifted["whole_command_hex"]).startswith(data)
        if row["word"] == 0x4000:
            ident, = row["record_ids"]
            records.append(dict(id=ident, source_selector=data[5], fixture_command_offset=at))
    assert len(records) == 18

    ROOT.mkdir()
    archive.blocks[42] = new_host
    image.replace_file(FILE, archive.to_bytes())
    FIXTURE.write_bytes(bytes(image.rom.save()))
    reread = base.NdsImage.open(FIXTURE)
    assert reread.read_file(FILE) == archive.to_bytes()
    reread.replace_file(FILE, original)
    assert bytes(reread.rom.save()) == build.ROM.read_bytes()
    base.save(FIXTURES, dict(candidate_sha256=stored["candidate_sha256"], exact_candidate_inverse=True,
                            fixtures=[dict(route=1, version="revised_English", source_block=89, fixture_block=42,
                                           source_file=FILE, research_ROM=str(FIXTURE), research_ROM_sha256=base.digest(FIXTURE),
                                           original_opening_prelude_commands=initializers, all_original_exchange_commands=group["commands"],
                                           original_text_records=records, all_fixture_commands=parsed)]))
    print("Prepared 18 original Hodram speech commands behind the verified opening prelude.")


def capture():
    source = checked_text(Path(runner.__file__).read_text(encoding="utf-8"), {
        "ROOT=Path('work/analysis/Hodram_scene_runs_v8280')": "ROOT=OUTPUT",
        "FIXTURES=Path('work/analysis/Hodram_scene_fixtures_v8279/six_complete_clean_revised_SC1_scripts_original_Hodram_prelude_fixtures.json')": "FIXTURES=MANIFEST",
        "choices=[137,45,46]": "choices=[89]",
        "frames={137:24001,45:10001,46:16001}[block]": "frames=FRAME_LIMIT",
        "cap=Path('E:/Rota Nova translations/Generated/work/emulation_v193')/f'Hodram_B{block}_route{route}_{version}_v8280'": "cap=folder/'capture'",
    })
    previous = sys.argv
    try:
        sys.argv = [__file__, "--route", "1", "--block", "89", "--version", "revised_English"]
        scope = dict(__file__=__file__, __name__="__main__", OUTPUT=ROOT, MANIFEST=FIXTURES, FRAME_LIMIT=FRAMES)
        exec(compile(source, __file__ + "::original_hodram_observer", "exec"), scope)
    finally:
        sys.argv = previous


def startup():
    scope = vars(startup_template) | globals() | {
        "boot": startup_template.boot, "startup_audit": startup_template.startup_audit,
    }
    FunctionType(startup_template.startup.__code__, scope)()


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "capture", "startup"))
    globals()[parser.parse_args().action]()
