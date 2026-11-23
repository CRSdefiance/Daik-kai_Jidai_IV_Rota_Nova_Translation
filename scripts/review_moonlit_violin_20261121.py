"""Review both accounts of the violin encounter and verify its movie requests."""

from collections import Counter
from pathlib import Path
from types import FunctionType

from dk4tool.graphics.fls import FlsArchive
from scripts import checkpoint_story_still_commands_20261120 as story
from scripts import prepare_london_guild_assignments_20261118 as pairing
from scripts import reconcile_shared_display_20261121 as shared
from scripts import register_search_forage_wrap_20261121 as parent
from scripts import research_graphics_file_open_v301 as movies
from scripts.review_company_name_dialogue_20261121 import ACTORS, GATES, TOKEN, logical


base, native = parent.base, parent.native
ROOT = Path("work/moonlit_violin_dialogue_20261121")
SOURCE = ROOT / "paired_source.json"
OUTPUT = shared.OUTPUT.with_name("moonlit_violin_context_20261121_v1.json")
ARTWORK = shared.OUTPUT.with_name("scene_caption_artwork_20261119_v1.json")
MOVIE = "/FLS/M23.fls"
COMPANION = "/evstill/evstill014.pxl"
BLOCKS = ((51,), (143,), (), ())
CONTEXT = (
    "Rafael plays the violin in a quiet place and notices Sera listening. Hodram arrives, examines Rafael without recognizing him, and leaves with Sera.",
    "Hodram looks for Sera at the tavern, waits, then goes outside. He finds her with Rafael after the violin interlude and brings her back.",
)

# Source record index, meaning, editorial reason.
NOTES = """
51 6|Rafael remarks on the quiet place and trails off about doing something for the first time in a while.|Keep his unfinished thought before the movie reveals the instrument and remove the short final row.
51 18|Rafael notices something.|Keep the first bracketed thought as he becomes aware of a listener.
51 24|Sera smiles.|The action cue leaves the two strangers unintroduced.
51 28|Rafael is puzzled and wonders who she is.|Keep both the wordless surprise and the private question.
51 32|A quiet pause follows.|The registered speakerless pause gives Hodram's entrance room.
51 37|Hodram calls Sera by name.|The brief call identifies whom he came to find.
51 41|Rafael reacts to another person's arrival.|The repeated private interjection fits his second surprise.
51 46|Sera recognizes Hodram aloud.|Keep the familiar name with the small exclamation.
51 50|Hodram wonders who the stranger is and rejects the idea they know one another.|Phrase this as speculation to match Hodram's account of the same encounter.
51 54|Rafael has nothing to say as Hodram looks at him.|Keep his silence before Hodram reacts.
51 59|Hodram considers what he sees.|The short murmur leads into Sera's question.
51 63|Sera asks what is on Hodram's mind by saying his name.|The single-name question is all she says.
51 67|Hodram tells Sera to leave with him.|The concise directive preserves his manner.
51 71|Sera agrees to go.|The simple assent ends their exchange.
51 75|Rafael calls Sera beautiful in retrospect and wonders what country she is a princess of.|Keep both the admiration and his speculation in informal inner speech.
51 86|Rafael thinks he recognized the soldier beside her as a member of the Swedish navy.|Keep his uncertainty and the service he recalls.
143 5|Hodram looks for Sera and calls her name.|The short call makes her absence immediately apparent.
143 8|Hodram wonders where Sera has gone.|The direct question gives the tavernkeeper a reason to speak.
143 17|The tavernkeeper asks if the customer is looking for someone.|The casual question suits the setting.
143 23|The present crewmate asks what is the matter.|The question responds to Hodram looking around and leaves room for his dismissal.
143 30|Hodram dismisses the concern and expects her back while he drinks.|Keep the expectation and the length of his wait.
143 33|Hodram waits in silence over three beats.|Keep the sequence of three silent beats.
143 37|Hodram notices she is taking her time.|His restrained impatience follows the silence.
143 40|He waits another moment.|Keep the pause before his irritation surfaces.
143 44|Hodram expresses exasperation about Sera.|The quiet remark leads into the decision to look for her.
143 49|Hodram asks aloud where Sera is.|The direct address suits his search.
143 53|Something catches Hodram's attention.|Retain his wordless question before the interlude.
143 66|Hodram pauses before approaching.|The pause leaves the observation unspoken.
143 71|Hodram calls Sera by name.|Match his entrance in Rafael's account.
143 75|Sera recognizes Hodram, using the player's given name.|Keep the live name exactly where it is called for.
143 79|Rafael remains silent.|Keep his brief reaction between Sera's greeting and Hodram sizing him up.
143 84|Hodram wonders if she knows the stranger, then decides that cannot be.|Give his private conclusion the weight of the Japanese without adding Rafael's route-specific opening question.
143 87|Rafael smiles.|Match the capitalization of other standalone action cues.
143 92|Hodram pauses and makes a short considering sound.|Keep the moment before Sera prompts him.
143 96|Sera asks what he is thinking by saying the player's given name.|Retain the substitution and question mark as one brief prompt.
143 100|Hodram tells Sera to come with him.|Match the same command in Rafael's version.
143 104|Sera agrees to go.|Match her simple assent in Rafael's version.
"""
EDITS = {
    (51, 6): ("It's quiet here. All right. It's been a while...", ("It's been a while...",)),
    (51, 50): ("Who is he? Does she know him? No, that can't be.", ("Does she know him?", "No, that can't be.")),
    (143, 23): ("Is something wrong?", ()),
    (143, 84): ("Does she know him? No, that can't be.", ("Does she know him?", "No, that can't be.")),
    (143, 87): ("(Smiles)", ()),
}


def review(packet):
    actors = base.load(ACTORS)["records"]
    notes = {}
    for line in NOTES.strip().splitlines():
        ref, meaning, reason = line.split("|")
        notes[tuple(map(int, ref.split()))] = (meaning, reason)
    records = []
    for group in packet["groups"]:
        route, block, path = (group[k] for k in ("route", "block", "file_path"))
        for row in group["records"]:
            index, selector = row["source_record_index"], row["selector"]
            key = block, index
            meaning, reason = notes.pop(key)
            previous = logical(row["current_English"])
            wording, phrases = EDITS.get(key, (previous, ()))
            assert row["native_command_word"] == 0x4000 and row["slots"] == []
            assert TOKEN.findall(wording) == TOKEN.findall(previous) == TOKEN.findall(row["Japanese"])
            refs = {side: dict(file_path=path, block=block, offset=row[f"{side}_offset"],
                command_offset=row[f"{side}_command_offset"], archive_sha256=group[f"{side}_archive_sha256"],
                block_sha256=group[f"{side}_block_sha256"],
                exact_stored_hex=bytes([selector]).hex() + row[f"{side}_body_hex"])
                for side in ("source", "current")}
            refs["source"]["record_index"] = index
            speaker = "Speakerless pause" if selector == 254 else actors[selector]["current_consumers"][0]["text"]
            records.append(dict(id=f"DK4_MES_B{block}_R{index:04}", file_path=path, route=route, block=block,
                kind="progressive", native_command_word=0x4000, source_selector=selector, native_slots=[],
                source_reference=refs["source"], current_reference=refs["current"],
                source_hex=refs["source"]["exact_stored_hex"], current_hex=refs["current"]["exact_stored_hex"],
                Japanese=row["Japanese"], english=wording, previous_English=previous, context=CONTEXT[route],
                speaker=speaker, source_meaning=meaning, localization_note=reason, protected_phrases=list(phrases),
                finding="prose" if key in EDITS else "retention", decision="revision" if key in EDITS else "retention",
                review=dict.fromkeys(GATES, True) | {"formatting": False}))
    assert not notes and len(records) == 37
    return records


def bind_movie(clean, installed, arm_pair):
    requests = {}
    walk = story.explicit_walk()
    for version, rom, arm in zip(("source", "current"), (clean, installed), arm_pair, strict=True):
        positions = {}
        for directory, route, block in (("data", 0, 51), ("data", 1, 143), ("testdata", 0, 51),
                                         ("testdata", 1, 144)):
            path = f"/{directory}/SC{route}.DK4"
            archive = rom.read_file(path)
            scene = native.IlnkContainer.parse(archive).blocks[block]
            trace = walk(arm, scene)
            assert trace["error"] is None
            request, = [x for x in trace["native_movie_requests"] if x["args"] == [23, 0, 1, 0]]
            at = request["source_offset"]
            command, = (row for row in trace["rows"] if row["offset"] == at)
            assert command["word"] == 0x4903 and command["native_extent"] == 2
            assert scene[at:at+2] == b"\x03\x49"
            assert not any(x["PC"] in (story.owners.GETTER, story.owners.COPIER)
                           for x in trace["opaque_effect_bridges"] if x["source_offset"] == at)
            positions[path] = dict(block=block, byte_offset=at, command_hex=scene[at:at+2].hex(),
                archive_sha256=native.digest(archive), block_sha256=native.digest(scene), arguments=request["args"])
        requested = movies.generated(rom, arm, 23)
        opened, = requested["SDK_open_events"]
        assert opened["actual_path"] == MOVIE
        requests[version] = dict(commands=positions, native_filename=requested)
    data = clean.read_file(MOVIE)
    assert data == installed.read_file(MOVIE)
    asset = FlsArchive(data)
    assert asset.count == 5 and [(asset.texture(i).width, asset.texture(i).height)
                                 for i in (0, 1, 3)] == [(256, 256)] * 3
    assert clean.read_file(COMPANION) == installed.read_file(COMPANION)
    return dict(path=MOVIE, sha256=native.digest(data), texture=0, companion_path=COMPANION,
        companion_sha256=native.digest(clean.read_file(COMPANION)), native_requests=requests,
        qualification="The moonlit compositions and their story commands associate the artwork. An exact pointer from the stored Japanese caption to the movie has not been established.")


def main():
    assert not OUTPUT.exists()
    if not SOURCE.exists():
        FunctionType(pairing.main.__code__, vars(pairing) | dict(
            parent=parent, ROOT=ROOT, BLOCKS=BLOCKS, CONTEXT=CONTEXT))()
    release, ledger, packet = map(base.load, (parent.RELEASE, base.LEDGER, SOURCE))
    assert release["candidate_sha256"] == base.digest(parent.ROM) == packet["candidate_sha256"]
    assert release["candidate_sha256"] == ledger["current_integrated_candidate"]["sha256"]
    assert release["registry_sha256"] == base.digest(base.REGISTRY)
    assert release["clean_input_sha256"] == base.digest(shared.CLEAN) == packet["clean_sha256"]
    clean, current = map(base.NdsImage.open, (shared.CLEAN, parent.ROM))
    arms = tuple(rom.read_file(shared.ARM) for rom in (clean, current))
    assert native.digest(arms[1]) == release["target_ARM9_sha256"]
    source = shared.workflow.common_message_entries(clean.read_file(shared.COMMON), arms[0])
    installed = shared.entries(current)
    labels = []
    for row in base.load(ARTWORK)["records"]:
        key = row["message_ID"]
        if key not in (3410, 3411):
            continue
        above = source[key]
        assert shared.workflow.reference(above) == row["source_reference"]
        assert above.text.decode("cp932") == row["source_Japanese"]
        assert installed[key].text.hex() == row["installed_hex"]
        labels.append(dict(message_ID=key, source_reference=row["source_reference"],
            current_reference=shared.workflow.reference(installed[key]), clean_Japanese=row["source_Japanese"],
            installed_hex=installed[key].text.hex(), english=row["draft_english"],
            previous_review=row["previous_review"], editorial_decision=row["contextual_decision"]))
    assert [r["message_ID"] for r in labels] == [3410, 3411]
    rows = review(packet)
    movie = bind_movie(clean, current, arms)
    base.save(OUTPUT, dict(previous_sha256=release["candidate_sha256"], clean_sha256=release["clean_input_sha256"],
        previous_registry_sha256=release["registry_sha256"], source_packet=str(SOURCE),
        source_packet_sha256=base.digest(SOURCE), records=rows, decisions=dict(Counter(r["decision"] for r in rows)),
        translation_policy="natural-dialogue-v2", target_locale="en-US", encoder="dialogue-relocatable-v1",
        review_gates=GATES, new_coverage_credit=0, actual_gameplay=False, artwork=movie, stored_labels=labels))
    print(f"Reviewed {len(rows)} dialogue records and verified the native M23 movie requests.")


if __name__ == "__main__":
    main()
