"""Review the two company-name scenes and preserve their four FE continuations."""

from collections import Counter
from pathlib import Path
from struct import pack_into

from dk4tool.dialogue.review import REQUIRED_REVIEW_GATES
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import prepare_company_name_companion_scenes_20261121 as paired
from scripts.review_company_name_dialogue_20261121 import ACTORS, TOKEN
from scripts.stage_late_trade_exchanges_20261118 import plan_progressive


base, native, stage, parent = paired.base, paired.native, paired.stage, paired.parent
ROOT = paired.ROOT / "staged_v2"
ROM, PROOF = ROOT / "Company_Companion_Scenes_STAGED.nds", ROOT / "stored_proof.json"
REVIEW = paired.ROOT / "contextual_review_v2.json"
EVIDENCE_ROOT = Path("out/company_companion_evidence_20261121_v2")
CONTEXT = {
    "gerhard_recruitment": "Rafael, Claudio and Janus visit Gerhard and ask him to return to sea. Claudio names Vels and explains why they came; Gerhard admits taking him in and resigning after the mutiny.",
    "gerhard_lesson": "Gerhard teaches the crew how to use broadside fire and boarding. The parallel lesson alternatives give the original controls, room and skill requirements, then their distinct stat rewards.",
    "maria_story": "Samwell asks why people fear Maria. Ian and the alternate speaker distinguish fear from strict discipline. The deserter wins a victory and still answers for abandoning his crew. Richard tries to retell the story after the others have heard it.",
}
NOTES = """
84 71|Rafael wonders whether this is the right place.|The brief question begins the visit tentatively.
84 76|Claudio thinks it is the place.|The understated reply leads into the knock.
84 80|There is a knock at the door.|Keep the action cue before Gerhard answers.
84 85|Gerhard asks who is at the door.|The pause fits his unhurried response.
84 89|Rafael greets him politely and starts to name his company before being interrupted.|The interrupted introduction keeps the company name and does not attach additional periods to it.
84 93|Claudio identifies the admiral and gives his own name and profession.|The quick interruption introduces both speakers without assuming they have met.
84 97|Gerhard is intrigued by a navigator and asks why they came.|He acknowledges the profession before asking their business.
84 100|Janus says they came because they heard Gerhard was a fine navigator and starts asking to speak with him.|Name Gerhard's navigation skill and let the unfinished request lead into Gerhard's answer.
84 103|Gerhard says that was long ago and now he lives ashore.|The contrast gives Rafael a reason to ask him back to sea.
84 106|Rafael asks whether Gerhard would sail again.|Use the ordinary expression for a polite invitation to return to sailing.
84 110|Gerhard refuses.|The one-word refusal leaves Claudio room to press him.
84 114|Claudio says it will not be that easy and brings up Vels.|The abrupt change of subject challenges Gerhard with a known name.
84 117|Gerhard stays silent.|Keep his reaction before Claudio presses again.
84 121|Claudio names him as the man Gerhard let get away.|The short accusation leaves the surprise to Rafael.
84 125|Rafael reacts with shock and wants an explanation.|The repeated question preserves the stumble.
84 130|Gerhard is silent again.|Keep the pause while the crew waits for an answer.
84 134|Janus asks Claudio to explain.|His urgent response follows Rafael's disbelief.
84 137|Claudio identifies Gerhard as an admiral who led a powerful private pirate-hunting fleet.|Keep his past command and his name with the following explanation.
84 140|The fleet suppressed pirate activity from the North Sea to the Mediterranean.|The range and reason for the lull both remain explicit.
84 143|Rafael is surprised by Gerhard's strength.|His emphatic question follows Claudio's account.
84 147|Gerhard's fleet once captured a large band of pirates that included Vels.|Keep Vels's presence as the disclosure.
84 151|Janus is astonished.|The reaction gives Gerhard the floor.
84 155|Gerhard asks Claudio to stop and admits Rafael's group to hear the rest.|His direct invitation marks the change in speaker and setting.
84 160|Gerhard saw potential in young Vels and took him in to train him.|The reason for the mentorship matters before the betrayal.
84 164|Janus is shocked a pirate was the admiral's student.|The incomplete thought preserves his disbelief.
84 167|Vels mutinied and fled when given a ship, and Gerhard resigned.|The order of the events and Gerhard's choice to resign are clear.
84 458|Gerhard teaches the crew to stay out of the enemy's broadside and maneuver around the bow or stern.|Keep the three maneuvers and the reason for them.
84 461|Rafael acknowledges the lesson.|The pause shows he is listening.
84 466|Gunners fire while the player maneuvers. An officer with high Aim improves a Gun Battery.|Keep the skill and room names and their effect.
84 470|A battle uses the normal course and sail controls. Guns fire automatically when enemies enter range.|Keep the two matched instructional pages and their sentence boundary.
84 473|Gerhard suggests refitting a hold into Quarters for boarding.|Keep the Shipyard operation and installed room label.
84 476|More sailors and an officer with high Swords in Quarters make boarding stronger.|The option remains advice and the role stays Boarding Leader.
84 480|Select an officer with high Swords and assign them to Quarters.|The imperative is the actionable instruction that follows Gerhard's advice.
84 483|Ships that touch board automatically, and the Boarding Leader is useful.|The trigger and the officer's role remain explicit.
84 487|Gerhard finishes explaining.|His short conclusion yields the floor to Rafael.
84 491|Rafael says he needs real battle experience and thanks him.|The next step is learning by doing.
84 507|The original given name receives Stamina, Agility and Spirit increases.|All three stats and the substitution stay intact.
84 511|Gerhard accepts the response.|The dry assessment suits his teaching style.
84 539|The normal course and sail controls still apply in a fight, with automatic firing in range.|Keep the duplicate lesson in its complete two-page form.
84 542|The player can refit a hold into Quarters at a town Shipyard.|Preserve the same operation as in the other alternative.
84 545|More sailors and a strong sword fighter assigned to Quarters improve boarding.|Keep the same roles and skill terms across both alternatives.
84 549|Select an officer with high Swords and assign them to Quarters.|Retain the actionable wording shared with the other lesson.
84 552|Contact starts a boarding battle automatically, with help from the Boarding Leader.|Keep the native trigger and the same role wording.
84 556|Gerhard finishes the lesson and asks whether Rafael follows.|His direct question invites Rafael's response.
84 560|Rafael thanks him and says they must gain real combat experience.|The response marks readiness to apply the lesson.
84 566|The original given name receives a Wits increase.|Keep the correct stat and substitution.
84 571|Gerhard accepts the choice to learn aboard ship.|The reply is the alternative to his direct lesson.
84 577|The original given name receives a Luck increase.|The distinct branch reward stays separate.
116 7|Samwell gets Ian's attention.|The familiar address fits a private question.
116 11|Ian asks what he wants.|The terse opening invites the question directly.
116 15|Samwell asks whether Maria is as frightening as people say.|The question preserves what others say and his own differing impression.
116 24|Ian says Maria is strict about rewards and punishments and that Samwell joined too late to know.|The distinction from fear previews the next story.
116 30|The alternative speaker makes the same distinction.|Retain the familiar phrasing for Jam's voice.
116 36|Ian introduces a past incident.|Keep the pause into the story panels.
116 41|An officer deserted during a battle with wokou pirates, leaving allies surrounded.|Both existing pages keep the two acts and the reason for desertion.
116 44|Their side suffered a defeat and many soldiers and officers were killed or captured.|Keep both outcomes and the severity of the defeat.
116 48|The deserter realized he would have no place when he returned.|The pause motivates the man's next action.
116 51|He raided the celebrating Japanese fleet's flagship alone and took the enemy commander's head, reversing the defeat.|The complete two-panel account preserves the risk and change of outcome.
116 54|Samwell reacts in astonishment.|This brief response follows the reversal.
116 58|Maria was prepared to give the returning man an important position and gold for the victory.|Keep the two rewards and their military cause before the sentence.
116 61|She promptly charged him with desertion in battle and sentenced him to death.|The reward and conviction remain distinct.
116 64|Samwell falls silent.|The silence leaves room to explain Maria's decision.
116 68|Maria gave the gold to his family and promised them a permanent pension on officer terms.|Both forms of compensation and the family relationship remain explicit.
116 72|The man thanked her in tears and accepted execution.|The ending preserves his reaction without an invented absolution.
116 82|Ian remembers Maria looking both terrifying and deeply sad.|The contrast is his response to the apparent harshness.
116 87|The alternate speaker recalls Maria's frightening bearing and profound grief.|The measured alternate preserves the same emotional distinction.
116 93|Samwell is surprised by what he had not known.|The quiet reaction closes Ian's account.
116 102|Richard hears them discussing the admiral and offers a detailed account.|He arrives after the real story, which sets up the rebuff.
116 106|Samwell politely says he has heard it already.|The understated refusal contrasts with Richard's insistence.
116 110|Richard claims his account would give deeper insight into Maria's feelings and the high ideals her faction pursues.|Keep his self-important insistence as one spoken paragraph and the interrupted mention of the faction's ideals.
116 113|Samwell cuts him off by announcing he is going to bed.|The abrupt departure lets the interruption land.
116 116|Ian says good night.|His concise reply follows Samwell out.
116 128|The alternate farewell is formal.|Keep the character's deliberate politeness even while leaving.
116 135|Richard tries to keep them from leaving before hearing his story.|His unfinished appeal ends the comic interruption.
"""
REVISIONS = {
    (84, 100): ("We heard you're a fine navigator. Can we...", ("Can we...",)),
    (84, 106): ("Would you go back to sea?", ()),
    (116, 110): ("No, no! I'd do far better at explaining the admiral's feelings and the lofty ideals FO strives for...",
        ("far better", "the admiral's feelings", "the lofty ideals", "FO strives for...")),
}


def author(packet):
    notes = {}
    for line in NOTES.strip().splitlines():
        key, meaning, reason = line.split("|", 2)
        notes[tuple(map(int, key.split()))] = (meaning, reason)
    actors = base.load(ACTORS)["records"]
    rows = []
    for group in packet["groups"]:
        route, block, path = [group[k] for k in ("route", "block", "file_path")]
        for data in group["records"]:
            index = data["source_reference"]["record_index"]
            key = (block, index)
            if key not in notes:
                continue
            previous = data["current_English"]
            english, phrases = REVISIONS.get(key, (previous, ()))
            meaning, rationale = notes[key]
            scope = "maria_story" if block == 116 else "gerhard_recruitment" if index < 450 else "gerhard_lesson"
            selector = data["source_selector"]
            assert TOKEN.findall(data["Japanese"]) == TOKEN.findall(previous) == TOKEN.findall(english)
            assert (english != previous) == (key in REVISIONS)
            speaker = "Speakerless narrative or tutorial" if selector == 254 else actors[selector]["current_consumers"][0]["text"]
            rows.append(data | dict(id=f"DK4_MES_B{block}_R{index:04}", route=route, block=block, file_path=path,
                speaker=speaker, context=CONTEXT[scope], source_meaning=meaning,
                previous_English=previous, english=english, localization_note=rationale, protected_phrases=list(phrases),
                native_command_word=0x4000, decision="revision" if key in REVISIONS else "retention",
                review=dict.fromkeys(sorted(REQUIRED_REVIEW_GATES), True) | {"formatting": False}))
    assert len(rows) == len(notes)
    return rows


def reassemble(source, current, matching, rows, scan, arm, reserve):
    commands, _ = scan(arm, current)
    offsets = [c["offset"] for c in commands] + [stage.logical_end(current)]
    positions = {p: i for i, p in enumerate(offsets)}
    raw = [current[a:b] for a, b in zip(offsets[:-1], offsets[1:], strict=True)]
    by_offset = {r["current_reference"]["command_offset"]: r for r in rows if r["decision"] == "revision"}
    parts, plans = [], {}
    for cmd, old in zip(commands, raw, strict=True):
        row = by_offset.get(cmd["offset"])
        if row is None:
            parts.append(old)
            continue
        original = bytes.fromhex(row["source_reference"]["exact_command_hex"])
        source_offset = row["source_reference"]["command_offset"]
        assert source[source_offset:source_offset+len(original)] == original
        assert old == bytes.fromhex(row["current_reference"]["exact_command_hex"])
        assert old[:6] == original[:6] and old[5] < 207
        before = old[6:old.index(0, 6)]
        body, plan = plan_progressive(row, old[5], before, original[6:original.index(0, 6)])
        if reserve:
            assert len(body) <= len(before) and len(before) - len(body) <= 1
            body = body.ljust(len(before), b" ")
        updated = old[:6] + body + b"\0"
        parts.append(updated + bytes(-len(updated) % 2))
        plans[row["id"]] = plan
    assert len(plans) == len(by_offset)

    target_offsets, pos = [], 8
    for command in parts:
        target_offsets.append(pos)
        pos += len(command)
    target_offsets.append(pos)
    jumps = {}
    for i, (old, cmd) in enumerate(zip(raw, commands, strict=True)):
        if cmd["word"] not in stage.RELATIVE:
            continue
        index = positions[stage.jump(old, offsets[i])]
        delta = target_offsets[index] - target_offsets[i] - 4
        data = bytearray(old)
        assert 0 <= delta <= 65535 and delta % 2 == 0
        pack_into("<H", data, 2, delta)
        parts[i] = bytes(data)
        jumps[i] = index
    leader = bytearray(current[:8])
    assert pos < 0x2400
    pack_into("<H", leader, 4, pos - 8)
    target = bytes(leader) + b"".join(parts) + bytes(-pos % 4)
    installed, _ = scan(arm, target)
    assert [c["offset"] for c in installed] + [stage.logical_end(target)] == target_offsets
    assert [c["word"] for c in installed] == [c["word"] for c in commands]
    for i, (old, new) in enumerate(zip(commands, installed, strict=True)):
        assert [target_offsets[positions[k]] for k in old["ancestor_0100_offsets"]] == new["ancestor_0100_offsets"]
        assert target_offsets[positions[old["offset"] + old["native_extent"]]] == new["offset"] + new["native_extent"]
        if i in jumps:
            assert stage.jump(parts[i], new["offset"]) == target_offsets[jumps[i]]
        elif old["offset"] not in by_offset:
            assert parts[i] == raw[i]
    for at in matching["continuations"]:
        old = int(at)
        i = positions[old]
        assert target_offsets[i] == old and parts[i] == raw[i]
    assert current[:8] + b"".join(raw) + current[stage.logical_end(current):] == current
    mapping = {old: new for old, new in zip(offsets, target_offsets, strict=True)}
    for row in rows:
        row["target_pages"] = [dict(offset=mapping[p["offset"]], exact_command_hex=parts[positions[p["offset"]]].hex())
                               for p in row["installed_pages"]]
    return target, plans


def main():
    assert not ROOT.exists() and not REVIEW.exists()
    packet, release = map(base.load, (paired.OUTPUT, parent.RELEASE))
    assert packet["candidate_sha256"] == release["candidate_sha256"] == base.digest(parent.ROM)
    assert release["registry_sha256"] == base.digest(base.REGISTRY)
    rows = author(packet)
    scan, _, _ = native.scoped_inventory()
    clean, source, target = [base.NdsImage.open(p) for p in (native.CLEAN, parent.ROM, parent.ROM)]
    assert base.digest(native.CLEAN) == release["clean_input_sha256"]
    before = native.files(source)
    arm = before[native.ARM]
    groups, inverse = [], {}
    for group in packet["groups"]:
        path, block = group["file_path"], group["block"]
        old_archive = before[path]
        bank = native.IlnkContainer.parse(old_archive)
        old = bank.blocks[block]
        clean_block = native.IlnkContainer.parse(clean.read_file(path)).blocks[block]
        assert native.digest(old) == group["current_block_sha256"]
        assert native.digest(clean_block) == group["source_block_sha256"]
        written, plans = reassemble(clean_block, old, group, [r for r in rows if r["file_path"] == path], scan, arm, block == 84)
        bank.blocks[block] = written
        target.replace_file(path, bank.to_bytes())
        bank.blocks[block] = old
        assert bank.to_bytes() == old_archive
        inverse[path] = old_archive
        groups.append(dict(path=path, block=block, before=native.digest(old), after=native.digest(written), plans=plans,
                           preceding_continuations_unchanged=group["continuations"]))
    after = native.files(target)
    assert before.keys() == after.keys() and {k for k in before if before[k] != after[k]} == inverse.keys()
    guard = base.load(base.REGISTRY)["profiles"][release["profile"]]["source25_multiarchive_guard"]
    controls = bind_registered_story_percent_guard(guard)(native.files(clean), after)
    assert controls["total_exact_source_bound_relocated_leading25_count"] == 7 and not any(controls["source_bound_new_command_counts"].values())
    output = bytes(target.rom.save())
    for path, exact in inverse.items():
        target.replace_file(path, exact)
    assert bytes(target.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir()
    ROM.write_bytes(output)
    base.save(REVIEW, dict(translation_policy="natural-dialogue-v2", target_locale="en-US", encoder="dialogue-relocatable-v1",
        review_gates=sorted(REQUIRED_REVIEW_GATES), records=rows, decisions=dict(Counter(r["decision"] for r in rows)),
        source_packet=str(paired.OUTPUT), source_packet_sha256=base.digest(paired.OUTPUT), new_coverage_credit=0))
    base.save(PROOF, dict(candidate_sha256=base.digest(ROM), predecessor_sha256=release["candidate_sha256"],
        manuscript_sha256=base.digest(REVIEW), groups=groups, whole_parent_inverse=True, story_format_guard=controls))
    print(f"Staged {len(REVISIONS)} changes across {len(rows)} decisions with four continuation pages byte-exact.")


if __name__ == "__main__":
    main()
