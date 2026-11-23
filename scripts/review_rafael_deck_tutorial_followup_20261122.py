"""Review the whole clean-Japanese Rafael Deck lesson against the current build."""

from collections import Counter
from dataclasses import replace
from pathlib import Path

from dk4tool.dialogue.encoder import encode_relocatable_dialogue
from dk4tool.dialogue.profiles import get_dialogue_profile
from scripts import checkpoint_story_glyph_consistency_20261115 as glyph
from scripts import register_ship_room_names_20261122 as current
from scripts import reconcile_shared_display_20261121 as shared
from scripts.checkpoint_flagged_phrase_and_julio_20261119 import native
from scripts.review_london_guild_assignments_20261118 import TOKEN, logical
from scripts.stage_london_guild_assignments_20261118 import plan_progressive


base = current.base
ROOT = Path("work/analysis/rafael_deck_tutorial_followup_20261122")
OUTPUT = ROOT / "contextual_review.json"
GLYPHS = ROOT / "current_glyph_inventory.json"
FILE = "/data/SC0.DK4"
BLOCK = 43
CONTEXT = ("Julio checks Rafael is following before walking him through Deck View. He starts with the captain, "
           "then describes the jobs that keep a ship moving and which sailors help with navigation, observation "
           "and negotiations. An anonymous system panel tells the player how to open the screen.")

# Complete source exchange, in command order. A blank proposal preserves the current wording.
DECISIONS = {
    7: ("Julio checks whether Rafael has understood, then turns to what people like Julio do aboard ship.",
        "Still with me? Now let me show you what the crew does aboard ship.",
        "Keep his friendly check-in and shift to the ship's crew, including Julio."),
    11: ("An admiral is responsible for assigning people to their duties.",
         None,"His plain explanation preserves the distinction between the admiral and the captain."),
    14: ("Giving each crew member a duty helps the voyage go smoothly. Julio is about to demonstrate this on the Deck screen.",
         "Give everyone a job so the voyage goes smoothly. Let's make those assignments in Deck View.",
         "Make the instruction lead naturally into the demonstration and keep the exact menu label."),
    17: ("Rafael is the captain. Without a captain a ship stays put. It cannot pick a destination on its own.",
         "First, you're the captain, FI. A ship can't sail without a captain. It can't set a course on its own.",
         "Julio's matter-of-fact joke still treats the ship as if it might choose for itself. Set a course avoids the current break between where and to go. Keep the player's given name."),
    20: ("The Sail Handler adjusts the sails relative to the wind. The ship needs one per mast.",
         "Next is the Sail Handler. They angle the sails to suit the wind. You'll need one for each mast.",
         "Keep the job, the angle and the per-mast staffing rule. The direct address follows Julio's captain instruction."),
    23: ("The Helmsman is especially important when the ship needs to turn quickly.",
         None,"The direct advice gives the role its practical purpose and sets up the battle example."),
    27: ("A skilled Helmsman can move the ship quickly into a favorable position in a sea battle.",
         None,"The concrete battle example explains why the Helmsman matters. It keeps speed and positioning distinct."),
    30: ("A ship can sail without a First Mate. Assigning one enables talks with other factions and slows fatigue during a voyage. The contribution is easily overlooked.",
         "A First Mate is optional. They let you negotiate with other factions and keep the crew from tiring as fast at sea. An unsung hero.",
         "Keep the two benefits, use the established faction term and preserve Julio's affectionate aside."),
    33: ("A Surveyor lets the fleet use Auto Move and see its latitude and longitude. Julio calls the work important.",
         None,"It names both benefits clearly and sounds like Julio explaining a job he respects."),
    37: ("At sea, the Lookout reports other ships' affiliations and the situation in towns.",
         None,"Tells you who other ships belong to and what's happening maintains the two distinct reports in ordinary speech."),
    40: ("Those jobs should be enough simply to set sail. Julio encourages Rafael to learn about the rest himself.",
         None,"The invitation to experiment closes the spoken lesson and leads into the system panel."),
    45: ("Press X, choose Deck View from the menu and use it to change crew members' assignments.",
         "Press X and choose Deck View from the menu. You can change your crew's assignments there.",
         "Preserve the button, menu path and action. The concise second sentence matches Julio's description of crew assignments."),
}


def fmt(src, current_raw, text, selector, idx):
    if selector!=254:
        phrases = {7:("aboard ship",),14:("Deck View",),17:("set a course","on its own"),
                   20:("Sail Handler","each mast"),30:("First Mate","at sea")}[idx]
        row = dict(english=text,protected_phrases=phrases,id=f"DK4_MES_B43_R{idx:04}")
        _, plan = plan_progressive(row,selector,current_raw[1:],src[1:])
        return plan | dict(fit_is_preliminary=True)

    profile = get_dialogue_profile("raphael-story-live")
    profile = replace(profile, name="rafael-deck-lesson-preflight", balanced_wrapping=True,
        literal_prefix_policy="native-guard-v255",
        macro_widths=profile.macro_widths | {"FI":36},
        macro_ascii_lengths=profile.macro_ascii_lengths | {"FI":6},
        window_width_px=228 if selector==254 else 216)
    assert not TOKEN.search(text)
    encoded = encode_relocatable_dialogue(src[1:],text,profile)
    assert all(d.severity=="warning" for d in encoded.diagnostics)
    return dict(encoded_hex=(bytes([selector])+encoded.encoded).hex(),formatted_markup=encoded.formatted_markup,
        diagnostics=[d.code for d in encoded.diagnostics],fit_is_preliminary=True)


def main():
    assert not ROOT.exists()
    release = base.load(current.RELEASE)
    sha = base.digest(current.ROM)
    assert sha==release["candidate_sha256"] and base.digest(base.REGISTRY)==release["registry_sha256"]
    assert base.digest(current.native.CLEAN)==release["clean_input_sha256"]
    ja,en = map(base.NdsImage.open,(current.native.CLEAN,current.ROM))
    inventory,_,_ = native.scoped_inventory()
    clean_archives, active_archives = [], []
    for route in range(4):
        path = f"/data/SC{route}.DK4"
        j,e = (image.read_file(path) for image in (ja,en))
        assert native.digest(e)==release[f"target_SC{route}_sha256"]
        clean_archives.append(native.IlnkContainer.parse(j).blocks)
        active_archives.append(native.IlnkContainer.parse(e).blocks)

    def exact(image, block):
        arm = image.read_file(shared.ARM)
        commands,speeches = native.raw_speeches(arm,block,inventory)
        return commands,native.references(commands,speeches)

    js,es = clean_archives[0][BLOCK],active_archives[0][BLOCK]
    (j_cmd,j_speech),(e_cmd,e_speech) = exact(ja,js),exact(en,es)
    assert [c["word"] for c in j_cmd]==[c["word"] for c in e_cmd]
    assert len(j_speech)==len(e_speech)==len(DECISIONS)
    reviews = []
    for source,installed in zip(j_speech,e_speech,strict=True):
        idx = source["record_index"]
        selector = source["selector"]
        assert source["complete_preamble_hex"]==installed["complete_preamble_hex"]
        assert selector==installed["selector"] and selector in (6,254)
        source_raw, old_raw = map(lambda r: bytes.fromhex(r["raw_hex"]),(source,installed))
        japanese = source_raw[1:].decode("cp932")
        previous = logical(old_raw[1:].decode("ascii"))
        gloss,proposal,note = DECISIONS[idx]
        english = proposal or previous
        assert (proposal is None or proposal != previous) and english.isascii()
        assert TOKEN.findall(japanese)==TOKEN.findall(previous)==TOKEN.findall(english)
        reviews.append(dict(id=f"DK4_MES_B43_R{idx:04}",file_path=FILE,route=0,block=BLOCK,
            source_selector=selector,native_command_word=0x4000,kind="FE" if selector==254 else "progressive",
            speaker="Julio Erneco" if selector==6 else "System",context=CONTEXT,
            Japanese=japanese,source_meaning=gloss,localization_note=note,english=english,previous_English=previous,
            source_hex=source["raw_hex"],current_hex=installed["raw_hex"],
            source_reference=source | {"block_sha256":native.digest(js)},
            current_reference=installed | {"block_sha256":native.digest(es),"candidate_sha256":sha},
            decision="revision" if proposal else "retention",
            draft_auto_layout=fmt(source_raw,old_raw,english,selector,idx) if proposal else None,
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False)))
    assert [r["source_reference"]["record_index"] for r in reviews]==list(DECISIONS)
    first, = (r for r in reviews if r["source_reference"]["record_index"]==17)
    assert b"where \n to go" in bytes.fromhex(first["current_hex"])
    assert bytes.fromhex(first["current_hex"]).startswith(b"\x06F")

    checks, wide = [], []
    for route,blocks in enumerate(active_archives):
        count = 0
        for block,blob in enumerate(blocks):
            for m in glyph.HEADER.finditer(blob):
                count += 1
                text = glyph.decoded(m[0][6:])
                if glyph.WIDE.search(text):
                    wide.append(dict(route=route,block=block,body_offset=m.start()+6,exact=m[0].hex()))
        checks.append(count)
    assert not wide
    common = shared.entries(en)
    common_wide = [row for row in common if glyph.ASCII.search(glyph.decoded(row.text)) and
        glyph.WIDE.search(glyph.decoded(row.text))]
    assert len(common_wide)==1 and common_wide[0].message_id==318
    draft = glyph.OUTPUT.with_name("exhibition_quit_warning_20261115_v2.json")
    legacy = base.load(draft)["exhibition_warning"]
    assert legacy["current_hex"]==common_wide[0].text.hex()
    bind = dict(translation_policy="natural-dialogue-v2",target_locale="en-US",encoder="dialogue-relocatable-v1",
        review_gates=["source","context","localization","naturalness","formatting"],previous_sha256=sha,
        previous_registry_sha256=release["registry_sha256"],records=reviews,
        findings=dict(Counter(row["decision"] for row in reviews)),new_contextual_credit=0,
        formatting_and_registration_pending=True,full_goal_complete=False)
    assert all(all(r['review'][gate] for gate in bind['review_gates'][:-1]) for r in reviews)
    ROOT.mkdir()
    base.save(OUTPUT,bind)
    base.save(GLYPHS,dict(candidate_sha256=sha,story_header_matches_by_route=checks,sampled_header_matches=sum(checks),
        mixed_width_latin_candidates_in_matched_story_bodies=wide,mapped_common_entries=len(common),common_mixed_lead=legacy,
        common_mixed_lead_draft=str(draft),common_mixed_lead_draft_sha256=base.digest(draft),full_goal_complete=False,
        Julio_initial_F_in_current_exact_reference=first["current_reference"],actual_replay_added=False))
    print(f"Recorded {len(reviews)} Deck lesson decisions and checked {sum(checks):,} stored story header matches.",flush=True)


if __name__ == "__main__":
    main()

