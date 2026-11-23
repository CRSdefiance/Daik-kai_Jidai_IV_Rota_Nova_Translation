"""Verify the festival picture dialogue and its surrounding gameplay transitions."""

from hashlib import sha256
from inspect import getsource

from scripts import check_rafael_pereira_village_gameplay_20261121 as prior
from scripts import replay_rafael_tradehouse_festival_20261121 as replay
from scripts import verify_rafael_tradehouse_festival_20261121 as native_check
from scripts.source_locked_derivation_v5118 import checked_text


stage, base, native, town = replay.stage, replay.base, replay.native, prior.town
PROOF = replay.ROOT / "verified_gameplay.json"
REFERENCE_ROOT = stage.ROOT.with_name("staged_v2")
REFERENCE_GAMEPLAY = REFERENCE_ROOT / "focused_gameplay"
REPORT = REFERENCE_GAMEPLAY / "capture_extended/capture_report.json"


def qualify_fixture(fixture, image):
    prior_rom = REFERENCE_ROOT / stage.ROM.name
    old, new = map(base.load, (REFERENCE_ROOT / stage.PROOF.name, stage.PROOF))
    assert fixture["candidate_sha256"] == old["candidate_sha256"] == base.digest(prior_rom)
    assert new["candidate_sha256"] == base.digest(stage.ROM)
    initial = base.NdsImage.open(prior_rom)
    assert all(initial.read_file(path) == image.read_file(path) for path in native_check.display.ASSETS)
    final = native.IlnkContainer.parse(image.read_file(replay.PATH)).blocks
    assert native.IlnkContainer.parse(initial.read_file(replay.PATH)).blocks[44] == final[44]
    earlier = {(g["block"], c["stored_offset"]): c for g in old["groups"] for c in g["commands"]}
    registered = {(g["block"], c["source_offset"]): c for g in new["groups"] for c in g["commands"]}
    for copy in fixture["copied"]:
        block = copy["block"]
        source = earlier[block, copy["actual_block_offset"]]
        target = registered[block, source["source_offset"]]
        offset, raw = target["stored_offset"], bytes.fromhex(copy["hex"])
        assert source["stored"] == target["stored"] == copy["hex"]
        assert final[block][offset:offset + len(raw)] == raw
    assert [g["commands"][-1]["stored"] for g in old["groups"]] == [g["commands"][-1]["stored"] for g in new["groups"]]


source = checked_text(getsource(prior.main), {
    '    fixture_path, inputs = (replay.ROOT / part for part in ("fixture.json", "inputs.json"))':
        '    fixture_path, inputs = REFERENCE_GAMEPLAY / "fixture.json", REFERENCE_GAMEPLAY / "inputs_extended.json"',
    '(fixture_path, replay.REPORT, native_check.PROOF, stage.OUTPUT)':
        '(fixture_path, REPORT, native_check.PROOF, stage.OUTPUT)',
    'candidate == proof["candidate_sha256"] == fixture["candidate_sha256"] == base.digest(stage.ROOT / "clean_rebuilt.nds")':
        'candidate == proof["candidate_sha256"] == base.digest(stage.ROOT / "clean_rebuilt.nds")',
    '    assert fixture["original_scene_branches_unexecuted"] and not fixture["natural_activation"]':
        '    assert fixture["original_scene_branches_unexecuted"] and not fixture["natural_activation"]\n'
        '    assert fixture["original_festival_picture_commands_copied_byte_exact"]',
    '''    bank = native.IlnkContainer.parse(image.read_file(replay.prior.PATH)).blocks
    assert all(bank[x["block"]][x["actual_block_offset"]:][:len(bytes.fromhex(x["hex"]))].hex() == x["hex"]
               for x in fixture["copied"])''':
        '    qualify_fixture(fixture, image)',
    '''    holds, pictures, absent = [], [], []
    for (block, index), frame in zip(replay.SEQUENCE, replay.FRAMES[:-1], strict=True):''':
        '''    holds, pictures = [], []
    frames = iter(replay.FRAMES[:-1])
    for block, index in replay.SEQUENCE:''',
    '        captured, image = town.read_frame(captures, frame)\n': '',
    '''            assert receipt["retained_system_panel"]
            raw = bytes.fromhex(row["current_hex"])[1:]''':
        '''            assert receipt["festival_FE"]
            raw = bytes.fromhex(receipt["expanded_hex"])''',
    '''                raw = bytes.fromhex(row["current_hex"])[1:]
                assert not any(token in raw for token in (b"FI", b"FA", b"FO"))''':
        '''                encoded = bytes.fromhex(row["current_hex"])[1:].decode("ascii")
                raw = stage.review.TOKEN.sub(lambda m: proof["default_names"][m[0]], encoded).encode("ascii")''',
    '"pereira_village_gameplay_': '"tradehouse_festival_gameplay_',
    '    sheets = []': '    replay.ROOT.mkdir()\n    sheets = []',
    '''        if not panel.panel.mask_check(plane, 228 if is_fe else 216, image):
            absent.append((ident, frame))
            continue''':
        '''        for frame in frames:
            captured, image = town.read_frame(captures, frame)
            if panel.panel.mask_check(plane, 228 if is_fe else 216, image):
                break
        else:
            raise AssertionError((ident, holds[-1]["id"] if holds else None))''',
    '    assert not absent, absent':
        '''    assert sum(row["system_FE"] for row in holds) == 5
    upper = {ident: sha256(image.crop((0, 0, 256, 192)).tobytes()).hexdigest()
             for ident, image in pictures if ident in ("DK4_MES_B69_R0052", "DK4_MES_B69_R0078", "DK4_MES_B69_R0100")}
    assert upper["DK4_MES_B69_R0052"] != upper["DK4_MES_B69_R0078"]
    assert upper["DK4_MES_B69_R0100"] == upper["DK4_MES_B69_R0052"]''',
    'exact_native_glyph_matches=True, hardware_verified=False, holds=holds, final_hold=final,': 
        'exact_native_glyph_matches=True, hardware_verified=False, holds=holds, final_hold=final,\n'
        '        original_picture_switches_copied_and_exercised=True, festival_top_screen_sha256=upper,\n'
        '        preceding_stage_emulator_proof_reused=True, reference_rom_sha256=fixture["candidate_sha256"],',
    'including the 500,000 military-funds notice.': 'including all five festival picture panels.',
    '(fixture_path, replay.REPORT, inputs, native_check.PROOF, fixture["fixture_ROM"])':
        '(fixture_path, REPORT, inputs, native_check.PROOF, fixture["fixture_ROM"], REFERENCE_ROOT / stage.PROOF.name)',
})
scope = vars(prior) | globals()
exec(compile(source, __file__ + "::live-festival-comparison", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
