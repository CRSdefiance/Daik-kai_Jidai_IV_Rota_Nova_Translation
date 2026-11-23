"""Review and compile the four Istanbul tobacco exchanges from the clean source."""

from argparse import ArgumentParser
from pathlib import Path
from types import FunctionType, SimpleNamespace

from PIL import Image, ImageDraw

from scripts import register_osaka_glass_20261122 as parent
from scripts import review_osaka_glass_followup_20261122 as template
from scripts import stage_rafael_deck_tutorial_followup_20261122 as established


base, native = parent.base, parent.native
VOYAGE = Path("work/analysis/istanbul_tobacco_gameplay_20261122")
ROOT = VOYAGE / "editorial_v2"
MANUSCRIPT, PROOF, SHEET = ROOT / "contextual_review.json", ROOT / "stored_proof.json", ROOT / "native_pages.png"
ROM = ROOT / "Istanbul_Tobacco_Lil_STAGED.nds"
PATCH, REBUILT = ROOT / "translation.xdelta", ROOT / "clean_rebuilt.nds"
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
EVENTS = Path("translations/editorial_checkpoints/SharedText_20261110_v1/town_trend_event_entries_20261121_v1.json")
PRIOR = Path("releases/all_routes_editorial_20261121_havana_calicut_istanbul_trends_candidate/verification/registered_review.json")
TOWN, BLOCKS, SPEAKERS = 22, (204, 196, 192, 165), {153: "Sailor", 115: "Port Worker", 254: "System"}
CONTEXT = "In Istanbul's Square, a sailor asks about tobacco. The port worker turns the question back on him, teases him about never smoking, and offers him some. The sailor goes from curious to self-conscious and then agrees. The game forecasts a possible tobacco trend."
NOTES = (
    ("The sailor casually asks the port worker if he has ever smoked tobacco.",
     "The plain question starts a familiar conversation about whether the other person has tried it."),
    ("The worker wonders if the sailor himself still hasn't smoked.",
     "The worker turns the question around, and the short wording cues the sailor's honest answer."),
    ("The sailor admits he still hasn't smoked because the chance never came up.",
     "The short admission explains his inexperience without making it sound like a refusal."),
    ("The worker exclaims that it's already fashionable and teases him that he must be just about the only one in town who hasn't smoked.",
     "Keep the worker's incredulity and casual exaggeration as part of the peer pressure."),
    ("The sailor stammers, asks if the worker really thinks so, and says he wants to try it too.",
     "The hesitant question answers the worker's teasing claim before the sailor shares his own curiosity."),
    ("The worker confirms his opinion, offers the sailor a try, and tells him to follow.",
     "The brisk offer becomes an invitation to act. It keeps the worker's confidence and direct tone."),
    ("The sailor stammers his agreement.",
     "The short, hesitant acceptance carries the nervous beat from his previous line."),
    ("The impersonal notice predicts that tobacco may become fashionable in Istanbul.",
     "The forecast preserves uncertainty and keeps the specific commodity and town. The worker's claim is his own impression."),
)
REVISIONS = {
    2: ("No chance yet, to be honest.", "No. I haven't had the chance.",
        "The sailor is answering a yes-or-no question. A direct admission and explanation sound like a natural reply."),
    4: ("R-really? I'd like to try it, too.", "Y-you think so? I'd like to try it, too.",
        "The sailor asks whether the worker thinks he is alone in this and then admits his curiosity. Keep the stammer and the shift to wanting a try. Keep his entire expression of interest together on the second line."),
}


def stage():
    assert not ROOT.exists()
    release, prior, events = map(base.load, (parent.RELEASE, PRIOR, EVENTS))
    predecessor = base.digest(parent.ROM)
    assert predecessor == release["candidate_sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(parent.MANIFEST) == release["manifest_sha256"]
    assert base.digest(native.CLEAN) == release["clean_input_sha256"]
    clean, english = map(base.NdsImage.open, (native.CLEAN, parent.ROM))
    clean_arm, arm = [rom.read_file(native.ARM) for rom in (clean, english)]
    assert native.digest(arm) == release["target_ARM9_sha256"]
    before = native.files(english)
    runtime = SimpleNamespace(image=english, arm=arm)
    draw, fe = template.clipped_renderer(runtime), template.current_fe_painter(runtime)
    glyphs = english.read_file("/GRP/KANJI.FNT")
    inventory, _, _ = native.scoped_inventory()
    rebuild = template.compiler.rebuild_function()
    rows, changed, previews, bindings = [], {}, [], []
    for route, index in enumerate(BLOCKS):
        path = f"/data/SC{route}.DK4"
        event_file = f"/data/EV{route}.DK4"
        entry, = [r for r in events["routes"][route]["entries"] if r["script_block"] == index]
        assert entry["date_fields_hex"] == "ff1fffff" and entry["town"] == TOWN
        event_at, event_size = entry["event_record_offset"], len(bytes.fromhex(entry["record_hex"]))
        assert english.read_file(event_file) == clean.read_file(event_file)
        assert english.read_file(event_file)[event_at:event_at + event_size].hex() == entry["record_hex"]
        jp_bank = native.IlnkContainer.parse(clean.read_file(path))
        en_bank = native.IlnkContainer.parse(before[path])
        source, old = jp_bank.blocks[index], en_bank.blocks[index]
        earlier = [r for r in prior["records"] if (r["file_path"], r["block"]) == (path, index)]
        src, cur = [native.references(*native.raw_speeches(a, b, inventory)) for a, b in ((clean_arm, source), (arm, old))]
        assert len(src) == len(cur) == len(earlier) == len(NOTES) == 8
        group = []
        for n, (j, e, p, (meaning, why)) in enumerate(zip(src, cur, earlier, NOTES, strict=True)):
            assert j["raw_hex"] == p["source_hex"] and e["raw_hex"] == p["registered_reference"]["exact_stored_hex"]
            selector = j["selector"]
            assert selector == e["selector"] == p["source_selector"] and p["speaker"] == SPEAKERS[selector]
            assert j["complete_preamble_hex"] == e["complete_preamble_hex"] and all(p["review"].values())
            jp = bytes.fromhex(j["raw_hex"])[1:].decode("cp932")
            previous = " ".join(bytes.fromhex(e["raw_hex"])[1:].decode("ascii").split())
            assert previous == p["english"]
            revised = route == 2 and n in REVISIONS
            proposed = previous
            if revised:
                old_text, proposed, why = REVISIONS[n]
                assert previous == old_text
            group.append(dict(id=p["id"], route=route, block=index, file_path=path,
                source_selector=selector, kind="system-FE" if selector == 254 else "progressive",
                native_command_word=0x4000, speaker=p["speaker"], context=CONTEXT, Japanese=jp,
                source_meaning=meaning, english=proposed, previous_English=previous,
                localization_note=why, source_hex=j["raw_hex"], current_hex=e["raw_hex"],
                protected_phrases=["I'd like to try it, too."] if revised and n == 4 else [],
                source_reference=j | dict(file_path=path, block=index, block_sha256=native.digest(source)),
                current_reference=e | dict(file_path=path, block=index, block_sha256=native.digest(old)),
                prior_approved_reference=p["registered_reference"],
                decision="revision" if revised else "retention",
                review=dict(source=True, context=True, localization=True, naturalness=True, formatting=False)))
        rows.extend(group)
        bindings.append(dict(route=route, event=entry, event_archive=event_file, event_sha256=native.digest(before[event_file]),
                             source_block_sha256=native.digest(source), installed_block_sha256=native.digest(old)))
        if route != 2:
            continue
        target, commands, plans = rebuild(group, source, old, inventory, clean_arm, arm, fe)
        edits = [c for c in commands if c["stored"] != c["current"]]
        revision_ids = [r["id"] for r in group if r["decision"] == "revision"]
        assert [c["record_ids"] for c in edits] == [[ident] for ident in revision_ids]
        for cmd, ident in zip(edits, revision_ids, strict=True):
            raw = bytes.fromhex(cmd["stored"])
            at = cmd["stored_offset"]
            assert target[at:at+len(raw)] == raw and raw[5] == 153
            body = raw[6:raw.index(0, 6)]
            result = draw(arm, glyphs, body)
            page, = result["pages"]
            assert result["complete_consumed_bytes"] == len(body) and page["native_independent_plane_equal"]
            previews.append(dict(id=ident, native_plane_hex=page["native_plane_hex"], body_hex=body.hex(), plan=plans[ident]))
        en_bank.blocks[index] = target
        packed = en_bank.to_bytes()
        new_bank = native.IlnkContainer.parse(packed)
        en_bank.blocks[index] = old
        assert en_bank.to_bytes() == before[path]
        assert [n for n, (a, b) in enumerate(zip(en_bank.blocks, new_bank.blocks, strict=True)) if a != b] == [index]
        english.replace_file(path, packed)
        changed[path] = dict(block=index, before=native.digest(before[path]), after=native.digest(packed),
                             target_block=native.digest(target), commands=commands, plans=plans)

    assert len(rows) == 32 and len(previews) == 2
    after = native.files(english)
    assert before.keys() == after.keys() and {p for p in before if before[p] != after[p]} == set(changed) == {"/data/SC2.DK4"}
    final = bytes(english.rom.save())
    for path in changed:
        english.replace_file(path, before[path])
    assert bytes(english.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir()
    ROM.write_bytes(final)
    base.save(MANUSCRIPT, dict(translation_policy="natural-dialogue-v2", encoder="dialogue-relocatable-v1", target_locale="en-US",
        review_gates=["source", "context", "localization", "naturalness", "formatting"], records=rows,
        prior_review=str(PRIOR), prior_review_sha256=base.digest(PRIOR), predecessor_sha256=predecessor,
        source_event_archive_binding=str(EVENTS), source_event_archive_binding_sha256=base.digest(EVENTS),
        proposed_changes=2, justified_retentions=30, new_contextual_credit=0, full_goal_complete=False))
    canvas = Image.new("RGB",(892,157),"#263238")
    labels = ImageDraw.Draw(canvas)
    for i,row in enumerate(previews):
        x = i * 446
        labels.text((x+6,4),row["id"],fill="white")
        ink = bytes(0 if n else 250 for n in bytes.fromhex(row["native_plane_hex"]))
        canvas.paste(Image.frombytes("L",(216,64),ink).resize((432,128),Image.Resampling.NEAREST),(x+6,21))
    canvas.save(SHEET)
    base.save(PROOF, dict(candidate_sha256=base.digest(ROM), predecessor_sha256=predecessor, changed=changed,
        whole_parent_inverse=True, manuscript_sha256=base.digest(MANUSCRIPT), original_town_entries=bindings,
        native_pages=previews, sheet=str(SHEET), sheet_sha256=base.digest(SHEET)))


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("stage", "patch", "startup"))
    action = cli.parse_args().action
    if action == "stage":
        stage()
    else:
        method = getattr(established, action)
        FunctionType(method.__code__, method.__globals__ | globals())()

