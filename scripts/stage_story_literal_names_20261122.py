"""Stage the literal story-name fix and verify first-pass and non-story behavior."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import FunctionType

from dk4tool.patch import story_expanded_names as patch
from scripts import stage_rafael_deck_tutorial_followup_20261122 as precedent
from scripts import trace_story_name_display_20261122 as trace
from scripts.source_locked_derivation_v5118 import checked_text


base, native, parent = trace.base, trace.native, trace.current
ROOT = parent.stage.run.ROOT / "literal_substitutions"
ROM = ROOT / "Story_Literal_Names_STAGED.nds"
PROOF = ROOT / "stored_proof.json"
PATCH, REBUILT = ROOT / "translation.xdelta", ROOT / "clean_rebuilt.nds"
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
FIELDS = {"first": b"Hodram", "middle": b"Joakim", "last": b"Bergstrom", "company": b"Bergstrom Fleet"}


source = checked_text(getsource(trace.observe), {
    "    if direct:\n        assert selector == 18": "",
    "    actor_root = get(0xCB184)":
        "    for site in PATCH_SITES:\n"
        "        cpu.mem_write(BASE + site, arm[site:site+4])\n"
        "    actor_root = get(0xCB184)",
    "    cpu.reg_write(UC_ARM_REG_R0, actor if direct else selector)\n    cpu.reg_write(UC_ARM_REG_R1, INPUT)":
        "    cpu.reg_write(UC_ARM_REG_R0, (actor if selector==18 else INPUT) if direct else selector)\n"
        "    cpu.reg_write(UC_ARM_REG_R1, INPUT if not direct or selector==18 else 0)",
})
scope = vars(trace) | {"PATCH_SITES": patch.FRAMES}
exec(compile(source, __file__ + "::story-and-direct-callers", "exec"), scope)
observe = scope["observe"]


def verify_prepared(before, after, note, raw, stored):
    names = {r["field"]: r for r in note["all_four_actor_fields"]}
    expected_caller = {18: 0x020242F4, 254: 0x0202431C, 255: 0x0202433C}

    # These model variants are used only in isolated CPU checks.
    def override(replacements):
        b = bytearray(raw)
        for field, value in replacements.items():
            at = names[field]["address"] - trace.BASE
            width = names[field]["native_byte_capacity"]
            assert len(value) < width
            b[at:at+width] = value.ljust(width, b"\0")
        return bytes(b)

    default = override(FIELDS)
    mixed = override({
        "first": "イFIFA".encode("cp932"), "middle": b"FOII",
        "last": "森FIFAFOFU".encode("cp932"), "company": b"FOFIFAFU Company"})
    widest = override({"first": b"R"*14+b"FI", "middle": b"M"*14+b"FO",
                       "last": b"L"*14+b"FA", "company": b"C"*16+b"FU"})
    paragraphs = (
        ("stored Charles speech", raw, stored, True),
        ("all four sequences", raw, b"FI / FA / FO / FU", True),
        ("mixed kana and Latin fields", mixed, b"FI / FA / FO / FU", True),
        ("maximum field widths, first", widest, b"I saw FI.", True),
        ("maximum field widths, surname", widest, b"I saw FA.", True),
        ("maximum field widths, full", widest, b"I saw FO.", True),
        ("maximum field widths, company", widest, b"I saw FU.", True),
        ("default fields", default, b"I saw FI.\n FA sent FO to FU.", False),
        ("ordinary body", raw, b"First, look over here!\n I know what to do.", False),
    )
    cases, controls = [], []
    for selector in trace.FIRST:
        for label, memory, text, changed in paragraphs:
            old, new = [observe(arm, memory, text, selector) for arm in (before, after)]
            assert old["caller"] == new["caller"] == expected_caller[selector]
            assert old["saved_frames"] == new["saved_frames"]
            assert new["first"] == old["first"] == old["formatter_input"] == new["formatter_input"]
            assert new["output"] == new["first"]
            assert (old["output"] != new["output"]) == changed, (selector,label,old,new)
            cases.append(dict(mode=selector, case=label, stored=text.hex(),
                first=new["first"].hex(), before=old["output"].hex(), after=new["output"].hex(),
                first_owner=new["caller"], observed_saved_frames=new["saved_frames"],
                captured_actor_model_exact=True))
        for text in (b"Hello FA!", b"FI / FA / FO / FU", b"We are ready.\n All hands to your stations!"):
            old, new = [observe(arm, raw, text, selector, direct=True) for arm in (before, after)]
            assert old == new and new["first"] == text
            if b"FA" in text:
                assert new["output"] != text
            controls.append(dict(mode=selector, raw=text.hex(), display=new["output"].hex(),
                                 direct_caller_control_exact=True))
    witness, = [r for r in cases if r["case"] == "stored Charles speech" and r["mode"] == 18]
    exact_layout = bytes.fromhex(note["first_expanded_hex"])
    incorrect = bytes.fromhex(note["visible_nested_expansion_hex"])
    assert bytes.fromhex(witness["before"]) == exact_layout.replace(b"BergstromFIFAFOF",incorrect,1)
    assert bytes.fromhex(witness["after"]) == exact_layout
    return cases, controls


def stage():
    assert not ROOT.exists()
    note, raw = trace.read_finding()
    previous = base.load(parent.RELEASE)
    assert base.digest(parent.ROM) == previous["candidate_sha256"]
    assert base.digest(parent.MANIFEST) == previous["manifest_sha256"]
    assert base.digest(base.REGISTRY) == previous["registry_sha256"]
    assert base.digest(native.CLEAN) == previous["clean_input_sha256"]
    image, clean = map(base.NdsImage.open, (parent.ROM, native.CLEAN))
    old = native.files(image)
    arm = old[native.ARM]
    assert native.digest(arm) == previous["target_ARM9_sha256"]
    source = note["exact_record"]["current_ref"]
    archive = old[source["file_path"]]
    bound = native.IlnkContainer.parse(archive).blocks[source["block"]]
    payload = bytes.fromhex(source["exact_stored_hex"])
    at = source["offset"]
    assert bound[at:at+len(payload)] == payload
    assert native.digest(bound) == source["block_sha256"]

    deletion = base.load(parent.VERIFY / "stored_proof.json")["source_bound_helper"]
    revised, owned = patch.stage(arm, clean.read_file(native.ARM), deletion)
    cases, controls = verify_prepared(arm, revised, note, raw, payload[1:])
    image.replace_file(native.ARM,revised)
    new = native.files(image)
    assert old.keys() == new.keys() and {p for p in old if old[p] != new[p]} == {native.ARM}
    result = bytes(image.rom.save())
    image.replace_file(native.ARM,arm)
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir()
    ROM.write_bytes(result)
    base.save(PROOF,dict(candidate_sha256=base.digest(ROM), predecessor_sha256=base.digest(parent.ROM),
        target_ARM9_sha256=native.digest(revised), whole_parent_inverse=True, preserved_name_deletion_helper=deletion,
        protected_story_frames=owned, actual_finding=str(trace.FINDING), actual_finding_sha256=base.digest(trace.FINDING),
        all_native_story_cases=cases, unrelated_direct_cases=controls, native_UI_construction_bridged=True,
        story_and_common_file_bytes_exact=True, natural_gameplay_pending=True))
    print(f"Staged {base.digest(ROM)}. {len(cases)} story and {len(controls)} independent caller cases passed.")


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action",choices=("stage","patch","startup"))
    action=cli.parse_args().action
    if action=="stage":
        stage()
    else:
        existing=getattr(precedent,action)
        FunctionType(existing.__code__,existing.__globals__|globals())()

