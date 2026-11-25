"""Materialize and exercise the verified Rafael Deck lesson on the cumulative build."""

from argparse import ArgumentParser
from inspect import getsource
import sys

from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from scripts import compile_rafael_deck_tutorial_followup_20261122_v2 as compiled
from scripts import register_rafael_tradehouse_festival_20261121 as startup_reference
from scripts import replay_rafael_deck_after_trade_20261119 as ordinary
from scripts import verify_rafael_deck_tutorial_followup_20261122_v2 as render
from scripts.source_locked_derivation_v5118 import checked_text


base,native,parent = compiled.base,compiled.native,compiled.current
ROOT = compiled.draft.ROOT/"staged"
ROM = ROOT/"Rafael_Deck_Lesson_STAGED.nds"
PROOF = ROOT/"stored_proof.json"
PATCH, REBUILT = ROOT/"translation.xdelta",ROOT/"clean_rebuilt.nds"
STARTUP_CAPTURE = ROOT/"startup/capture/capture_report.json"
ARCHIVE = compiled.draft.FILE


def build():
    assert not ROOT.exists()
    proof,previous,visual = map(base.load,(compiled.PROOF,parent.RELEASE,compiled.draft.ROOT/"visual_review_v2.json"))
    assert base.digest(parent.ROM)==previous["candidate_sha256"]==proof["predecessor_sha256"]
    assert base.digest(base.REGISTRY)==previous["registry_sha256"]
    assert base.digest(parent.MANIFEST)==previous["manifest_sha256"]
    assert base.digest(native.CLEAN)==previous["clean_input_sha256"]
    assert base.digest(compiled.REVIEW)==proof["draft_sha256"]
    assert visual["compiled_candidate_SHA256"]==proof["proposed_ROM_sha256"]
    assert visual["native_proof_sha256"]==base.digest(render.PROOF) and visual["viewed_sheet_sha256"]==base.digest(render.SHEET)
    image = base.NdsImage.open(parent.ROM)
    before = native.files(image)
    bank = native.IlnkContainer.parse(before[ARCHIVE])
    old = bank.blocks[43]
    assert native.digest(old)==proof["predecessor_block_sha256"]
    bank.blocks[43] = compiled.TARGET.read_bytes()
    assert native.digest(bank.blocks[43])==proof["compiled_block_sha256"]
    packed = bank.to_bytes()
    assert native.digest(packed)==proof["compiled_archive_sha256"]
    image.replace_file(ARCHIVE,packed)
    installed = native.files(image)
    assert installed.keys()==before.keys() and {p for p in before if before[p]!=installed[p]}=={ARCHIVE}
    output=bytes(image.rom.save())
    assert native.digest(output)==proof["proposed_ROM_sha256"]
    image.replace_file(ARCHIVE,before[ARCHIVE])
    assert bytes(image.rom.save())==parent.ROM.read_bytes()
    ROOT.mkdir()
    ROM.write_bytes(output)
    base.save(PROOF,proof | dict(candidate_sha256=base.digest(ROM),candidate=str(ROM),
        stage_input_sha256=base.digest(compiled.PROOF),ROM_file_written=True,
        native_proof_sha256=base.digest(render.PROOF),direct_visual_sha256=base.digest(compiled.draft.ROOT/"visual_review_v2.json")))
    print(f"Staged {base.digest(ROM)} from the exact previously rendered block.")


def patch():
    proof=base.load(PROOF)
    assert base.digest(ROM)==proof["candidate_sha256"]
    assert base.digest(native.CLEAN)==base.load(parent.RELEASE)["clean_input_sha256"]
    assert not PATCH.exists() and not REBUILT.exists()
    make_xdelta(native.CLEAN,ROM,PATCH)
    apply_xdelta(native.CLEAN,PATCH,REBUILT)
    assert REBUILT.read_bytes()==ROM.read_bytes()
    print(f"Exact clean-input patch {base.digest(PATCH)}")


def startup():
    prior=base.load(parent.STARTUP_CAPTURE)
    candidate=base.load(PROOF)["candidate_sha256"]
    assert base.digest(ROM)==candidate
    assert prior["ROM_sha256"]==base.digest(parent.ROM) and prior["frames"]==31000
    assert prior["cold_boot"] and not prior["savestate_loaded"] and prior["scripted_start_frame"]==-1
    donor=prior["battery_save_preloaded"]
    assert base.digest(donor["source"])==donor["source_sha256"]
    directory=STARTUP_CAPTURE.parent.parent
    directory.mkdir()
    inputs=directory/"inputs.json"
    base.save(inputs,prior["scripted_input_schedule"])
    argv=sys.argv
    try:
        sys.argv=["headless_desmume_v193.py","--rom",str(ROM),"--out",str(STARTUP_CAPTURE.parent),
            "--frames","31000","--inputs-json",str(inputs),"--press-start","-1","--touchscreen",
            "--battery-save",donor["source"],"--capture-every","999999","--dump-ram",
            "--capture-at",*map(str,startup_reference.START_FRAMES)]
        ordinary.harness.main()
    finally:
        sys.argv=argv
    assert base.digest(donor["source"])==donor["source_sha256"]
    assert base.load(STARTUP_CAPTURE)["ROM_sha256"]==candidate


def replay():
    older=base.load(ordinary.PRIOR)
    assert older["candidate_sha256"]==base.load(ordinary.parent.RELEASE)["candidate_sha256"]
    assert base.digest(ordinary.INPUTS)==older["evidence"][str(ordinary.INPUTS)]
    source=checked_text(getsource(ordinary.capture),{
        """    if case == 'current':
        rom, proof = parent.ROM, parent.RELEASE
    else:
        from scripts import stage_rafael_deck_after_trade_20261119 as build
        rom, proof = build.ROM, build.PROOF""":"    rom, proof = STAGED_ROM, STAGED_PROOF",
        "    assert prior['candidate_sha256'] == base.digest(parent.ROM)":
            "    assert prior['candidate_sha256'] == base.load(parent.RELEASE)['candidate_sha256']",
    })
    env=vars(ordinary) | dict(STAGED_ROM=ROM,STAGED_PROOF=PROOF,ROOT=ROOT/"ordinary_deck")
    exec(compile(source,__file__+"::same-ordinary-Lisbon-controls","exec"),env)
    env["capture"]("after")


if __name__=="__main__":
    parser=ArgumentParser(description=__doc__)
    parser.add_argument("action",choices=("build","replay","startup","patch"))
    globals()[parser.parse_args().action]()

