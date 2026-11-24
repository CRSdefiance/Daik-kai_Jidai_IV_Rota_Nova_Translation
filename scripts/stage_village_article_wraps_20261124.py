"""Reflow the three remaining Promised Words article breaks."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import register_village_clue_punctuation_20261124 as parent
from scripts import stage_village_clue_punctuation_20261124 as former
from scripts.source_locked_derivation_v5118 import checked_text


ARM, COMMON, RELEASE = former.ARM, former.COMMON, parent.RELEASE
ROOT = Path("E:/Rota Nova translations/Generated/work/editorial_20261124_village_article_wraps")
ROM = ROOT / "Village_Article_Wraps_STAGED.nds"
STORED, OUT = ROOT / "stored_proof.json", ROOT / "village_article_wrap_review_20261124.json"
PATCH, REBUILT, PATCH_PROOF = (ROOT / name for name in ("translation.xdelta", "clean_rebuilt.nds", "clean_patch_proof.json"))
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
played = SimpleNamespace(RELEASE=RELEASE)
PHRASES = {
    2: ("the bell-shaped rock", "jutting out into the sea."),
    6: ("the Frenchman", "visited this land."),
    22: ("the mountain of fire in Kamchatka.",),
}


def build_edits(arm, clean, image, manuscript):
    code = former.MainCodeFile(arm, former.BASE)
    pool = bytes(code.sections[3].data)
    target = bytearray(pool)
    prior = former.read(parent.REVIEW)
    reviews = {row["id"]: row for row in prior["records"]}
    last_layouts = {row["index"]: row for row in former.read(former.OUT)["native_cases"]}
    compiler = FunctionType(former.compiled_clue.__code__, vars(former) | dict(PHRASES=PHRASES))
    assert prior["candidate_sha256"] == former.sha256(image.rom.save()).hexdigest()
    rows, edits, layouts = [], [], []
    for entry in manuscript["records"]:
        if entry["kind"] != "CLUE" or entry["index"] not in PHRASES:
            continue
        index = entry["index"]
        record = reviews[entry["id"]]
        source, current = (record[k] for k in ("source_reference", "registered_reference"))
        assert source["exact_hex"] == entry["source_hex"]
        field = entry["field"]
        old_pointer = former.unpack_from("<I", clean, field)[0]
        pointer = former.unpack_from("<I", arm, field)[0]
        assert old_pointer == source["native_text_address"] and pointer == current["native_text_address"]
        assert former.cstring(clean, old_pointer - former.BASE).hex() == source["exact_hex"]
        offset = pointer - former.POOL
        before = former.cstring(pool, offset)
        assert before.hex() == current["exact_hex"]
        assert before.decode("ascii") == last_layouts[index]["new_argument"]
        english, argument, proposed = compiler(entry)
        new = argument.encode("ascii")
        assert len(new) == len(before) and new != before and pool[offset + len(before)] == 0
        assert english == record["english"] == " ".join((former.AFTER % before.decode("ascii")).split())
        assert all(not line.rstrip().endswith(" the") for line in proposed.splitlines())
        size = len(before) + 1
        target[offset:offset + size] = new + b"\0"
        edits.append(dict(id=entry["id"], field=field, pointer=pointer, pool_offset=offset, extent=size,
                          before_hex=(before + b"\0").hex(), after_hex=(new + b"\0").hex()))
        layouts.append(dict(index=index, answer=last_layouts[index]["answer"], previous=former.AFTER % before.decode("ascii"),
                            old_argument=before.decode("ascii"), new_argument=argument, proposed=proposed))
        reason = f"Keep {PHRASES[index][0].rstrip('.')} together so the definite article leads directly into its noun phrase."
        rows.append(record | dict(current_reference=current, installed_reference=current | dict(exact_hex=new.hex()),
                                  localization_note=reason))
        rows[-1].pop("registered_reference")
    assert len(rows) == len(edits) == len(layouts) == 3
    source = getsource(former.exclusive_owners)
    start, end = source.index("    template,"), source.index("    found =")
    scope = vars(former).copy()
    exec(compile(checked_text(source, {source[start:end]: ""}), __file__ + "::clue-pointers", "exec"), scope)
    owners = scope["exclusive_owners"](image, edits, arm)
    code.sections[3].data = target
    installed = bytes(code.save())
    for edit in edits:
        offset, size = edit["pool_offset"], edit["extent"]
        target[offset:offset + size] = bytes.fromhex(edit["before_hex"])
    assert bytes(target) == pool
    code.sections[3].data = target
    assert bytes(code.save()) == arm and former.cache_plan(installed) == former.cache_plan(arm)
    return installed, rows, edits, owners, layouts


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("stage", "patch", "startup"))
    action = cli.parse_args().action
    if action == "stage":
        scope = vars(former) | globals() | dict(parent=SimpleNamespace(trend=parent.parent.trend, template=parent.template))
        FunctionType(former.stage.__code__, scope)()
    else:
        scope = vars(former.release_checks) | globals()
        FunctionType(former.release_checks.release_check.__code__, scope)(former.read(STORED), action)
