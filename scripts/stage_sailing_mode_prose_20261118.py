"""Reword the three sailing mode instructions inside their existing sprite banks."""

from inspect import getsource
from pathlib import Path
from struct import unpack_from

from ndspy.code import MainCodeFile

from dk4tool.patch import sailing_panel_graphics as panels
from scripts import register_all_routes_final_flagged_wraps_20261118 as parent
from scripts.source_locked_derivation_v5118 import checked_text

base, native = parent.base, parent.native
ROOT = Path("work/sailing_mode_prose_20261118/research_v1")
ROM, PROOF = ROOT / "Sailing_Mode_Prose_RESEARCH_ONLY.nds", ROOT / "stored_proof.json"
ORIGINAL = Path("translations/sailing_mode_panels_manuscript_v1.json")
OWNERS = Path("work/analysis/sailing_panels_v217/preparation.json")
DRAFT = ROOT / "review.json"
TEXT = (
    ("To see details about a town or ship, select it on screen.",
     ("select it on screen.",),
     "Put the action and its purpose in one sentence. The second line keeps the complete selection instruction."),
    ("Press A to search. You may find water, food, items, or other supplies. Find nothing? Crew fatigue goes up by 3. Sailors may desert or be attacked by wild animals during a search.",
     ("food, items, or other supplies.", "Find nothing? Crew fatigue goes up by 3.",
      "Sailors may desert or be attacked", "by wild animals during a search."),
     "Keep the exact three-point cost tied to an unsuccessful search. A separate sentence gives the risks of searching in general."),
    ("Pick a fleet or town on screen. Attacking starts a war with its faction and sharply reduces goodwill. You can't declare war on allied fleets.",
     ("Pick a fleet or town on screen.", "Attacking starts a war with its faction",
      "and sharply reduces goodwill.", "You can't declare war on allied fleets."),
     "Give the target selection first, then state the consequence and keep the alliance restriction limited to fleets."),
)


def words_at_width(prose, phrases):
    chunks = [prose]
    for phrase in phrases:
        assert prose.count(phrase) == 1 and len(phrase) <= 40
        chunk, = [i for i, s in enumerate(chunks) if phrase in s]
        first, last = chunks[chunk].split(phrase, 1)
        chunks[chunk:chunk+1] = [first, phrase, last]
    units = [word for chunk in chunks if chunk for word in ([chunk] if chunk in phrases else chunk.split())]
    lines = []
    for unit in units:
        if lines and len(lines[-1]) + len(unit) + 1 <= 40:
            lines[-1] += " " + unit
        else:
            lines.append(unit)
    assert " ".join(lines) == prose
    return lines


def encoded(arm, draft):
    source = checked_text(getsource(panels.encode_panels), {
        "textwrap.wrap(prose, width=40, break_long_words=False, break_on_hyphens=False)":
            'words_at_width(prose, record["protected_phrases"])',
    })
    scope = vars(panels) | globals()
    exec(compile(source, __file__ + "::native-panel-width", "exec"), scope)
    return scope["encode_panels"](arm, draft)


def prepare():
    assert not ROOT.exists()
    release = base.load(parent.RELEASE)
    assert base.digest(parent.ROM) == release["candidate_sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(native.CLEAN) == release["clean_input_sha256"]
    image, clean = map(base.NdsImage.open, (parent.ROM, native.CLEAN))
    arm, old_arm = (im.read_file(native.ARM) for im in (image, clean))
    assert native.digest(arm) == release["target_ARM9_sha256"]
    draft, history = map(base.load, (ORIGINAL, OWNERS))
    accepted = base.load(Path("translations/sailing_panel_graphics_release_v2.json"))
    assert base.digest(ORIGINAL) == accepted["manuscript_sha256"]
    live_proof = base.load(Path("translations/sailing_mode_panels_native_review_v217.json"))
    assert base.digest(live_proof["live_proof"]) == live_proof["live_proof_sha256"]
    prior_proof = Path(accepted["native_proof"])
    assert base.digest(prior_proof) == accepted["native_proof_sha256"]
    assert base.load(prior_proof)["plan"] == history
    staged = bytearray(arm)
    stage, = [s for s in MainCodeFile(arm, panels.BASE).sections if s.ramAddress == panels.STAGE]
    old_panels = history["panels"]
    for rec, old, (english, phrases, reason) in zip(draft["records"], old_panels, TEXT, strict=True):
        offset, size = int(rec["source_address"], 16) - panels.BASE, rec["source_allocation_bytes_including_NUL"]
        pointer_at = int(rec["pointer_site"], 16) - panels.BASE
        assert source_pointer_at(arm, pointer_at) == source_pointer_at(old_arm, pointer_at) == old["source_pointer"]
        exact = arm[offset:offset + size]
        assert exact == old_arm[offset:offset + size] and exact.endswith(b"\x00")
        assert rec["english"] == " ".join(old["lines"])
        rec.update(source_hex=exact.hex(), previous_English=rec["english"], english=english,
                   protected_phrases=list(phrases), localization_note=reason,
                   review=dict(source=True, context=True, localization=True, naturalness=True, formatting=False))
    compiled = encoded(arm, draft)
    positions, inverse = [], bytearray(arm)
    for row, old, fresh in zip(draft["records"], old_panels, compiled, strict=True):
        n = old["packed_bytes"]
        i = old["packed_pointer"] - panels.POOL
        expected = bytes(stage.data[i:i + n])
        assert native.digest(expected) == old["packed_sha256"]
        file_at = arm.find(expected)
        assert file_at >= 0 and arm.find(expected, file_at + 1) == -1 and len(fresh["packed"]) <= n
        replacement = fresh["packed"].ljust(n, b"\0")
        staged[file_at:file_at+n] = replacement
        packed = dict(file_path=native.ARM, offset=file_at, runtime_pointer=old["packed_pointer"],
                      bytes=n, previous_sha256=native.digest(expected), revised_sha256=native.digest(replacement))
        row.update(current_reference=packed, source_reference=dict(file_path=native.ARM,
            address=old["source_pointer"], literal_address=int(row["pointer_site"], 16),
            exact_clean_hex=row["source_hex"]), decision="revision")
        positions.append((file_at, i, expected, replacement))
    for file_at, _, expected, replacement in positions:
        assert staged[file_at:file_at+len(replacement)] == replacement
    entire = bytes(staged)
    inverse[:] = entire
    for file_at, _, expected, _ in positions:
        inverse[file_at:file_at+len(expected)] = expected
    assert bytes(inverse) == arm
    sec_new, = [s for s in MainCodeFile(entire, panels.BASE).sections if s.ramAddress == panels.STAGE]
    assert len(stage.data) == len(sec_new.data)
    old_blob = bytes(stage.data)
    restored = bytearray(sec_new.data)
    entries = history["entry"] - panels.POOL
    helper_inputs = [old | {"packed": expected} for old, (_, _, expected, _) in zip(old_panels, positions, strict=True)]
    helper = panels.helper(history["entry"], helper_inputs)
    assert sec_new.data[entries:entries+len(helper)] == helper == old_blob[entries:entries+len(helper)]
    for _, i, expected, replacement in positions:
        assert restored[i:i + len(expected)] == replacement
        restored[i:i + len(expected)] = expected
    assert bytes(restored) == old_blob

    initial = native.files(image)
    image.replace_file(native.ARM, entire)
    modified = native.files(image)
    assert {p for p in initial if initial[p] != modified[p]} == {native.ARM}
    payload = bytes(image.rom.save())
    image.replace_file(native.ARM, arm)
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir(parents=True)
    ROM.write_bytes(payload)
    saved = base.digest(ROM)
    draft.update(translation_policy="natural-dialogue-v2", previous_sha256=release["candidate_sha256"],
                 candidate_sha256=saved, new_editorial_credit=0, formatting_pending=True)
    base.save(DRAFT, draft)
    proof = dict(candidate_sha256=saved, predecessor_sha256=release["candidate_sha256"],
                 target_ARM9_sha256=native.digest(entire), preserved_renderer_and_same_allocations=True,
                 entire_parent_inverse=True, source_pins={str(p):base.digest(p) for p in (ORIGINAL, OWNERS, prior_proof)},
                 rows=[{k: v for k, v in p.items() if k != "packed"} for p in compiled])
    base.save(PROOF, proof)
    print([x["lines"] for x in compiled])
    print(f"Staged the three existing text panels in {saved}.")


def source_pointer_at(arm, offset):
    return unpack_from("<I", arm, offset)[0]


if __name__ == "__main__":
    prepare()
