"""Stage the reviewed palace, tutorial and alliance scenes over the registered candidate."""

from copy import deepcopy
from pathlib import Path

from dk4tool.script import format_safety, format_safety_relocated_v1, format_safety_relocated_v2
from scripts import review_rafael_palace_and_alliance_20261121 as review
from scripts import stage_rafael_rescue_and_lessons_20261121 as precedent
from scripts.source_locked_derivation_v5118 import checked_text


base, native, parent = review.base, review.native, review.parent
ROOT = review.ROOT / "palace_and_alliance_staged_v1"
ROM, PROOF = ROOT / "Rafael_Palace_And_Alliance_STAGED.nds", ROOT / "stored_proof.json"
OUTPUT = review.OUTPUT
GUARD_SC0, GUARD = ROOT / "source25_SC0_qualification.json", ROOT / "source25_current_qualification.json"


def qualify_format_controls(spec, clean, before, after, groups):
    """Rebind only clean actor-37 commands after the B146 layout changes."""
    old = format_safety_relocated_v2.checked_receipt(spec)
    old_sc0 = format_safety_relocated_v2.checked_receipt(old["prior_receipt"])
    previous_proof = format_safety_relocated_v2.reject_with_receipt(clean, before, old)
    path = "/data/SC0.DK4"
    block = 146
    group, = [g for g in groups if g["block"] == block and g["file_path"] == path]
    source, target = [native.IlnkContainer.parse(data[path]).blocks[block] for data in (clean, after)]
    assert (native.digest(source), native.digest(target)) == (group["source"], group["after"])
    findings = format_safety.story_percent_findings(clean[path], after[path])
    bad = {(r["block"], r["record"]) for r in findings}
    assert bad and all(n == block for n, _ in bad)
    rows = []
    for item in group["commands"]:
        if item["word"] != 0x4000 or not item["source"].startswith("0040ffff0025"):
            continue
        a, z = item["source_offset"] + 5, item["stored_offset"] + 5
        ja, en = source[a:source.index(0, a)], target[z:target.index(0, z)]
        old_index, index = source[:a].count(b"\0"), target[:z].count(b"\0")
        if (block, index) not in bad:
            continue
        assert target[z - 5:z + 1] == source[a - 5:a + 1] == b"\0@\xff\xff\0%"
        assert item["source"].startswith("0040ffff00" + ja.hex() + "00")
        assert item["stored"].startswith("0040ffff00" + en.hex() + "00")
        assert b"%" not in en[1:] and index != old_index
        ident, = item["record_ids"]
        rows.append(dict(id=ident, block=block, source_offset=a, target_offset=z, source_index=old_index,
                         target_index=index, source_hex=ja.hex(), target_hex=en.hex(), complete_preamble_hex="0040ffff0025",
                         clean_block_sha256=group["source"], target_block_sha256=group["after"]))
    assert {(r["block"], r["target_index"]) for r in rows} == bad
    assert {r["id"] for r in old_sc0["relocated_source25_records"]} <= {
        key for item in group["commands"] if item["source"].startswith("0040ffff0025") for key in item["record_ids"]}
    sc0 = dict(old_sc0, relocated_source25_records=rows, original_legacy_findings=findings)
    mapping = format_safety_relocated_v1.qualified_source_records(clean[path], after[path], sc0)
    assert mapping.keys() == bad
    sc0["validated_target_relocations"] = len(mapping)
    sc0["evidence"] = old_sc0["evidence"] | {str(p): base.digest(p) for p in
        (Path(old["prior_receipt"]["path"]), Path(spec["path"]), review.OUTPUT, Path(__file__))}
    base.save(GUARD_SC0, sc0)
    receipt = deepcopy(old)
    receipt["prior_receipt"] = dict(path=str(GUARD_SC0), sha256=base.digest(GUARD_SC0))
    receipt["source25_predecessor_receipt"] = spec
    receipt["parent_positive"] = previous_proof
    receipt["evidence"][str(GUARD_SC0)] = base.digest(GUARD_SC0)
    receipt["evidence"][str(Path(spec["path"]))] = spec["sha256"]
    negatives = []
    for field in ("source_offset", "target_index"):
        wrong = deepcopy(sc0)
        wrong["relocated_source25_records"][0][field] += 1
        try:
            format_safety_relocated_v1.qualified_source_records(clean[path], after[path], wrong)
        except AssertionError:
            negatives.append(field)
        else:
            raise AssertionError(f"Incorrect {field} passed the exact source guard")
    receipt["refreshed_rejections"] = negatives
    receipt["positive"] = format_safety_relocated_v2.reject_with_receipt(clean, after, receipt)
    base.save(GUARD, receipt)
    return format_safety_relocated_v2.bind_registered_story_percent_guard(
        dict(path=str(GUARD), sha256=base.digest(GUARD)))(clean, after)


if __name__ == "__main__":
    compiler = precedent.prior.compiler
    source = checked_text(compiler.source, {
        "    assert not ROOT.exists()": "    assert not ROM.exists() and not PROOF.exists()",
        "stage.system.native_painter(ctx)": "current_fe_painter(ctx)",
        'g for g in packet["groups"]}': 'g for g in packet["groups"] if g["block"] in review.BLOCKS[0]}',
        '    controls = bind_registered_story_percent_guard(guard)(native.files(clean), final)\n'
        '    assert controls["total_exact_source_bound_relocated_leading25_count"] == 7':
        '    ROOT.mkdir(exist_ok=True)\n    controls = qualify_format_controls(guard, native.files(clean), initial, final, verified)\n'
        '    assert controls["total_exact_source_bound_relocated_leading25_count"] >= 2',
        "    ROOT.mkdir()\n    ROM.write_bytes(payload)": "    ROM.write_bytes(payload)",
    })
    scope = compiler.env | vars(precedent.prior) | globals() | {"paired": review}
    exec(compile(source, __file__ + "::stage", "exec"), scope)
    scope["main"]()
