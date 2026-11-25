"""Replay representative Maria dialogue through the native initialized scene."""

from argparse import ArgumentParser
from pathlib import Path
from struct import pack_into

from scripts import replay_maria_opening_wraps_20261114 as established
from scripts import stage_maria_B18_B20_20261122 as stage
from scripts import verify_maria_B18_B20_20261122 as display
from scripts.maria_existing_unlock_contract_v7680 import HISTORICAL, validate_capture, validate_fixture


base, native = stage.base, stage.native
ROOT = stage.ROOT / "focused_gameplay"
ROM = ROOT / "Maria_B18_B20_FOCUSED_ONLY.nds"
SETUP, INPUTS = ROOT / "fixture_receipt.json", ROOT / "inputs.json"
LIVE, REPORT = ROOT / "verified_gameplay.json", ROOT / "after/capture_report.json"
PLAY_ORDER = tuple(f"DK4_MES_B19_R{index:04d}" for index in (5,8,191,195,199))
FRAME_COUNT = 8851
RETURN_FRAMES = (3900, 8400, 8600)


def prepare():
    assert not ROOT.exists()
    proof = base.load(stage.PROOF)
    assert proof["candidate_sha256"] == base.digest(stage.ROM) and proof["whole_parent_inverse"]
    cold = base.load(established.stage.CAPTURE)
    validate_capture(cold)
    clean, image = map(base.NdsImage.open, (native.CLEAN, stage.ROM))
    inventory, _, _ = native.scoped_inventory()
    arm, clean_arm = image.read_file(native.ARM), clean.read_file(native.ARM)
    path = stage.review.ARCHIVE
    bank = native.IlnkContainer.parse(image.read_file(path))
    original = bank.to_bytes()
    host, clean_host = bank.blocks[33], native.IlnkContainer.parse(clean.read_file(path)).blocks[33]
    clean_commands, clean_texts = inventory(clean_arm, clean_host)
    clean_end = clean_texts[-1]["offset"] + clean_texts[-1]["native_extent"]
    clean_tail = [cmd["whole_command_hex"] for cmd in clean_commands if cmd["offset"] >= clean_end]
    host_commands, host_texts = inventory(arm, host)
    host_end = host_texts[-1]["offset"] + host_texts[-1]["native_extent"]
    assert host[:4] == clean_host[:4] and host[6:34] == clean_host[6:34]
    assert len([cmd for cmd in host_commands if cmd["offset"] < 34]) == 7
    assert [cmd["whole_command_hex"] for cmd in host_commands if cmd["offset"] >= host_end] == clean_tail
    assert clean_tail[0] == "4062" and clean_tail[-1] == "00000000"
    stored = {ident: (g["block"],cmd) for g in proof["groups"] for cmd in g["commands"] for ident in cmd["record_ids"]}
    payload = bytearray(host[:34])
    excerpts = []
    for ident in PLAY_ORDER:
        block, cmd = stored[ident]
        raw, at = bytes.fromhex(cmd["stored"]), cmd["stored_offset"]
        assert cmd["word"] == 0x4000 and bank.blocks[block][at:at + len(raw)] == raw
        payload.extend(raw)
        excerpts.append(dict(id=ident,block=block,offset=at,command=raw.hex()))
    payload.extend(b"".join(bytes.fromhex(cmd) for cmd in clean_tail))
    pack_into("<H", payload, 4, len(payload) - 8)
    replacement = bytes(payload) + bytes(-len(payload) % 4)
    assert len(replacement) <= 0x2400
    commands, speeches = inventory(arm, replacement)
    assert [speech["whole_command_hex"] for speech in speeches] == [row["command"] for row in excerpts]
    assert [cmd["whole_command_hex"] for cmd in commands[-len(clean_tail):]] == clean_tail
    bank.blocks[33] = replacement
    image.replace_file(path,bank.to_bytes())
    ROOT.mkdir()
    image.save(ROM)
    image.replace_file(path,original)
    assert bytes(image.rom.save()) == stage.ROM.read_bytes()
    unlock = base.load(HISTORICAL)
    unlock_file = ROOT / "unlock_fixture.json"
    digest = base.digest(ROM)
    unlock.update(production_ROM=str(ROM),production_ROM_sha256=digest,
                  current_test_scope="Focused initialized Maria dialogue through the existing unlock fixture.")
    base.save(unlock_file,unlock)
    validate_fixture(unlock_file)
    schedule = cold["scripted_input_schedule"] + [
        dict(start=frame,duration=16,buttons=["A"]) for frame in range(4200,8101,325)]
    base.save(INPUTS,schedule)
    base.save(SETUP,dict(candidate_sha256=proof["candidate_sha256"], proof_sha256=base.digest(stage.PROOF),
        fixture_ROMs={"after":dict(path=str(ROM),sha256=digest,unlock=str(unlock_file),unlock_sha256=base.digest(unlock_file))},
        excerpts=excerpts,host_block=33,original_host_exit=clean_tail,natural_event_eligibility_observed=False,
        restored_ROM_exact=True))


def capture():
    from inspect import getsource
    from scripts.source_locked_derivation_v5118 import checked_text
    original = established.capture
    code = checked_text(getsource(original), {
        'range(4350, 8251, 25)': 'range(4450, 8301, 125)',
    })
    scope = original.__globals__ | globals()
    exec(compile(code,__file__+"::Maria-initialized-capture","exec"),scope)
    scope["capture"]("after")


def verify():
    from PIL import Image, ImageDraw

    assert not LIVE.exists()
    report, fixture, shown = map(base.load,(REPORT,SETUP,display.PROOF))
    validate_capture(report)
    assert report["ROM_sha256"] == fixture["fixture_ROMs"]["after"]["sha256"] == base.digest(ROM)
    assert report["frames"] == FRAME_COUNT and report["scripted_input_schedule"] == base.load(INPUTS)
    assert fixture["candidate_sha256"] == shown["candidate_sha256"] == base.digest(stage.ROM)
    tools = established.precedent.verify.__globals__["previous"].previous.prior
    photos = tools.photos(report)
    samples = [(frame, receipt, img, tools.body_masks(img))
               for frame,(receipt,img) in sorted(photos.items()) if 4450 <= frame <= 8300]
    candidate = base.NdsImage.open(stage.ROM)
    release = base.load(stage.parent.RELEASE)
    ctx = native.RegisteredRuntime(stage.parent.RELEASE,release["own_registered_startup"],captain=3)
    assert all(ctx.image.read_file(path) == candidate.read_file(path) for path in display.display.ASSETS)
    expand, paint = display.display.original_expander(), display.display.clipped_renderer(ctx)
    font = candidate.read_file("/GRP/KANJI.FNT")
    records = {row["id"]:row for row in shown["records"]}
    observations, pictures, cursor = [], [], 0
    for ident in PLAY_ORDER:
        record = records[ident]
        raw = bytes.fromhex(record["body_hex"])
        if record["layouts"]:
            layout, = [entry for entry in record["layouts"] if entry["scope"] == "registered default"]
            pages = layout["pages"]
        else:
            cases = ctx.execute(expand,raw[1:],raw[0])["cases"]
            expanded, = {case["output_hex"] for case in cases}
            result = paint(ctx.arm,font,bytes.fromhex(expanded))
            assert result["complete_consumed_bytes"] == len(bytes.fromhex(expanded))
            pages = result["pages"]
        for index,page in enumerate(pages,1):
            expected = tools.prior.masks(bytes.fromhex(page["native_plane_hex"]))
            for frame,receipt,img,masks in samples:
                if frame > cursor + 140 and masks == expected:
                    break
            else:
                raise AssertionError((ident,index,cursor))
            cursor = frame
            observations.append(dict(id=ident,page=index,frame=frame,capture=receipt,
                candidate_body_hex=record["body_hex"],plane_sha256=native.digest(bytes.fromhex(page["native_plane_hex"]))))
            pictures.append((f"{ident} page {index}", img.convert("RGB").crop((0,192,256,384))))
    assert cursor < RETURN_FRAMES[1]
    for frame in RETURN_FRAMES[1:]:
        pictures.append((f"Return frame {frame}", photos[frame][1].convert("RGB").crop((0,192,256,384))))
    sheets = []
    for index in range(0,len(pictures),6):
        group = pictures[index:index+6]
        sheet = Image.new("RGB",(1024,410*((len(group)+1)//2)),"#243139")
        labels = ImageDraw.Draw(sheet)
        for n,(tag,picture) in enumerate(group):
            x,y = 512*(n%2),410*(n//2)
            labels.text((x+4,y+3),tag,fill="#ffffff")
            sheet.paste(picture.resize((512,384), Image.Resampling.NEAREST),(x,y+20))
        out = ROOT/f"maria_B18_B20_gameplay_{index//6+1}.png"
        sheet.save(out)
        sheets.append(dict(path=str(out),sha256=base.digest(out)))
    base.save(LIVE,dict(candidate_sha256=shown["candidate_sha256"], observations=observations,
        observed_ids=list(PLAY_ORDER), observed_speech_pages=len(observations), sheets=sheets,
        page_transitions={"mutiny": [row["frame"] for row in observations[:2]],
                          "Aziza's father": [row["frame"] for row in observations[2:]]},
        initialized_excerpts=True,natural_story_triggers_claimed=False,
        return_frames={str(frame):photos[frame][0] for frame in RETURN_FRAMES[1:]},
        report_sha256=base.digest(REPORT)))
    print(f"Verified {len(observations)} speech pages in the initialized Maria replay.")



if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action",choices=("prepare","capture","verify"))
    globals()[parser.parse_args().action]()

