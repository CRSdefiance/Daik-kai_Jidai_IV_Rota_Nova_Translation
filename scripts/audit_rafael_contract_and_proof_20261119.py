"""Audit the contract lesson pages, original return and cumulative startup."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path

from PIL import Image

from scripts import audit_naturalist_aliases_and_shield_20261119 as inherited
from scripts import audit_Rafael_B45_actual_v7895b as historical
from scripts import replay_rafael_contract_and_proof_20261119 as play
from scripts import verify_rafael_contract_and_proof_20261119 as offline
from scripts.source_locked_derivation_v5118 import checked_text

base, build = play.base, play.build
PROOF = play.ROOT / "verified_contract_lesson.json"
SHARE = play.ROOT / "verified_market_share_notice.json"
STARTUP = build.ROOT / "own_startup_verification.json"


def gameplay():
    source = checked_text(getsource(inherited.gameplay), {
        'terminal["frames"] == 40001': 'terminal["frames"] == play.FRAMES',
        'plan["displayed_original_block"] == 48': 'plan["displayed_original_block"] == 45',
        '"DK4_MES_B48_"': '"DK4_MES_B45_"',
        'assert len(revised) in {16, 17}': 'assert len(revised) == 4',
        '        assert not offsets or at == offsets[-1][0] + offsets[-1][1]':
            '        assert not offsets or at > offsets[-1][0]',
        '    assert exit_frame is not None and len(speeches) == len(set(speeches))':
            '    assert exit_frame is not None and len(speeches) == len(set(speeches)) == 12',
        '    required = {"DK4_MES_B48_R0167", "DK4_MES_B48_R0431", "DK4_MES_B48_R0438"}':
            '    required = set(revised)',
        '    assert not omitted or len(holds) >= 10': '    assert not omitted and len(holds) == 4',
        'athens_playback_': 'contract_playback_',
        'revised Athens pages, both revised modal notices and the original return.':
            'revised contract lesson pages and the original return.',
    })
    env = vars(inherited) | globals()
    exec(compile(source, __file__ + "::contract-playback", "exec"), env)
    env["gameplay"]()


def retained_share():
    assert not SHARE.exists()
    ident = "DK4_MES_B45_R0052"
    term = base.load(play.ROOT / "route0_English/terminal.json")
    assert all(base.digest(term[key]) == term[key + "_sha256"] for key in ("report", "observer"))
    fixture, = base.load(play.FIXTURES)["fixtures"]
    anchor, = (r for r in fixture["original_text_records"] if r["id"] == ident)
    group, = (g for g in base.load(build.PROOF)["groups"] if g["block"] == 45)
    command, = (c for c in group["commands"] if ident in c["record_ids"])
    old, = (r for r in base.load(historical.NATIVE)["records"] if r["id"] == ident)
    raw = bytes.fromhex(command["stored"])
    assert command["stored"] == command["current"]
    assert raw[5:raw.index(0, 6)] == bytes.fromhex(old["compiled_hex"]) + b" "
    assert b"Castor Co.'s market share in Ceuta" in bytes.fromhex(old["expanded_native_hex"])
    page, = old["pages"]
    plane = Path(page["native_plane"]).read_bytes()
    assert len(plane) == 228 * 48 and build.native.digest(plane) == page["native_plane_sha256"]
    expected = {(i % 228, (i // 228) // 12 * 16 + (i // 228) % 12) for i, ink in enumerate(plane) if ink}

    trace = base.load(term["observer"])
    event, = (r for r in trace["rows"] if r["kind"] == "after_command"
              and r["source"].get("instruction_offset") == anchor["fixture_command_offset"]
              and r["source"].get("block") == 44 and r["source"].get("route") == 0)
    assert event["source"]["whole_resident_payload_exact_ROM"]
    assert event["CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback"]
    start, end = trace["rows"][event["entry_row"]]["frame"], event["frame"]
    evidence = {term[k]: term[k + "_sha256"] for k in ("report", "observer")}
    evidence.update({str(historical.NATIVE): base.digest(historical.NATIVE), page["native_plane"]: page["native_plane_sha256"]})
    for shot in base.load(term["report"])["frames_captured"]:
        if not start + 20 < shot["frame"] < end - 4:
            continue
        assert base.digest(shot["path"]) == shot["PNG_sha256"]
        with Image.open(shot["path"]) as f:
            image = f.convert("RGB")
        masks = historical.masks(image, 228)
        if masks[(0, 8, 0)] != expected or masks[(98, 97, 98)] or masks[(197, 198, 197)]:
            continue
        assert all(image.getpixel((x, y)) != (98, 97, 98) for y in range(276, 289) for x in range(14, 244))
        base.save(SHARE, dict(candidate_sha256=base.digest(build.ROM), capture=shot,
            id=ident, exact_retained_command=True, prior_complete_bitmap_equal=True,
            actual_company="Castor Co.", displayed_share="20 percent", absent_nameplate=True, evidence=evidence))
        print("The retained market-share notice showed Castor Co. and 20 percent with the original blank nameplate.")
        return
    raise AssertionError((ident, start, end))


def startup():
    from types import FunctionType

    FunctionType(inherited.startup.__code__, vars(inherited) | globals())()


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("gameplay", "retained_share", "startup"))
    globals()[parser.parse_args().action]()
