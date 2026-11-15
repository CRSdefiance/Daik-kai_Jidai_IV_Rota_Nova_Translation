"""Record exact dialogue and native display in the observed town visits."""

from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts import observe_current_town_replays_20261114 as capture
from scripts import stage_tavern_influence_20261114 as stage
from scripts.checkpoint_market_shared_consumers_20261114 import font_mask
from scripts.review_sound_bgm_titles_v1 import reference

base = stage.base
OUTPUT = Path("translations/editorial_checkpoints/SharedText_20261110_v1/observed_town_replays_20261114_v1.json")
CONTEXT = {
    "nagasaki": "Maria checks a tavern and then asks the innkeeper about a single night. She turns down the quoted price.",
    "istanbul": "Hodram orders drinks in the tavern. The barkeep gives a regional rumor, calls the attendant, quotes another drink and gives a nearby-town tip after another order.",
    "amsterdam": "Lil opens the market after the starting sequence, browses the cheese trade and backs out of the pending deal.",
}
LINES = {
    "nagasaki": (
        (51,4751,("Welcome! What will you have?",), "The barkeep greets the customer and asks for an order. The short, friendly question leads naturally into the drink menu."),
        (63,5551,("Welcome! Come in.",), "The brief greeting suits an innkeeper inviting a guest inside before offering the overnight choices."),
        (1177,6351,("That'll be 1 gold coin.",), "The quote preserves the one-coin amount and reads conversationally before the player confirms or refuses."),
    ),
    "istanbul": (
        (51,3751,("Welcome! What will you have?",), "The same barkeep greeting is natural before the ordinary drink order."),
        (53,4551,("5 coins.",), "The short price matches the five-coin drink and the barkeep's matter-of-fact delivery."),
        (821,4951,("Hayreddin of Alexandria is","an influential pirate around here."), "Revise the stiff 'an influential pirate' phrase while retaining the local influence and all three substitutions."),
        (55,5351,("Hey, Faticia! We've got a customer!",), "The barkeep calls the attendant using the supplied name and announces the customer. The familiar call sounds natural."),
        (56,5751,("On it!",), "The attendant promptly answers the summons. The expression fits the quick affirmative response."),
        (59,6151,("Here, have another drink.",), "The offer retains the original friendly pressure and leaves the player a Yes/No choice."),
        (61,6551,("Ten coins.",), "The spoken quote preserves the new ten-coin price for the follow-up drink."),
        (827,6951,("Hmm... Hodram, right? Here's to our","new friendship!"), "The name check and toast are intact. 'New friendship' makes their relationship sound closer than the source introduction. Revisit this wording with the companion's complete drink exchange."),
        (53,7751,("5 coins.",), "An ordinary repeat order has the same five-coin quote as the first."),
        (823,8151,("Have you heard of Ragusa? It's","a town near here."), "The barkeep asks whether the player knows the supplied town, then gives its approximate proximity in a conversational tone."),
        (55,8551,("Hey, Faticia! We've got a customer!",), "The barkeep's repeat call keeps the same name substitution and address."),
        (57,8951,("Welcome!",), "The attendant's separate greeting fits this arrival. It remains distinct from her earlier reply to the barkeep."),
    ),
    "amsterdam": (
        (8,9701,("Need help?",), "The trader's short greeting fits the ordinary market interaction and leads into the available services."),
    ),
}
FOLLOWUPS = {821: "registered_revision_under_test", 827: "prose_followup"}


def main():
    assert not OUTPUT.exists()
    release = base.load(stage.parent.RELEASE)
    assert base.digest(stage.parent.ROM) == release["candidate_sha256"]
    assert base.digest(stage.CLEAN) == release["clean_input_sha256"]
    clean, rom = map(base.NdsImage.open, (stage.CLEAN,stage.parent.ROM))
    arm = rom.read_file(stage.ARM)
    original = common_message_entries(clean.read_file(stage.COMMON),clean.read_file(stage.ARM))
    live = owned_entries(rom.read_file(stage.COMMON),arm,stage.parent.source.current.assets.edit.digest(arm[DIRECTORY_OFFSET:TABLE_OFFSET]))
    covered = {}
    font = GameAsciiFont.from_arm9(arm)
    ledger = base.load(base.LEDGER)
    pending = set(ledger["pending_shared_consumer_checkpoint_20261114"]["remaining_legacy_keys"])
    for city, entries in LINES.items():
        folder = capture.ROOT/city
        report,trace,terminal = (base.load(folder/p) for p in ("capture/capture_report.json","requests.json","terminal.json"))
        events,frames,end,_,donor = capture.schedule(city)
        assert report["ROM_sha256"] == terminal["ROM_sha256"] == release["candidate_sha256"]
        assert report["frames"] == end and report["scripted_input_schedule"] == events
        assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
        assert not any(v for k,v in report.items() if k.startswith("synthetic_"))
        assert trace["all_host_slots_restored_and_core_file_exact"] and not trace["errors"] and not trace["mismatches"]
        calls = trace["source_requests"]
        assert len(calls)%2==0
        by_frame = {r["frame"]:r for r in report["frames_captured"] if r["frame"] in frames}
        if donor:
            save = report["battery_save_preloaded"]
            assert save["copied_byte_exact_before_cold_boot"] and save["source_sha256"] == donor["source_sha256"]
            assert save["source_sha256"] == base.digest(save["source"])
        else:
            assert report.get("battery_save_preloaded") is None
        observations = []
        for number, frame, lines, note in entries:
            found = [r for r in calls if r["message_ID"]==number and 0<frame-r["frame"]<180]
            assert [r["PC"] for r in found]==[0x0205528C,0x020534F4],(city, number,frame,found)
            assert found[0]["frame"] == found[1]["frame"]
            panel = by_frame[frame]
            assert base.digest(panel["path"]) == panel["PNG_sha256"]
            image = Image.open(panel["path"]).convert("RGB")
            offsets = (22,16) if city!="amsterdam" else (22,16)
            counts = []
            for i,line in enumerate(lines):
                y=296+i*16
                for x in offsets:
                    try:
                        count=font_mask(image,font,line,x,y+1,(16,y,244,y+16),(0,8,0))
                    except AssertionError:
                        continue
                    counts.append(count)
                    break
                else:
                    raise AssertionError((city,number,frame,line))
            assert all(image.getpixel((x,y))!=(0,8,0) for x in range(16,244)
                       for y in range(296+len(lines)*16,344))
            a,b = original[number],live[number]
            status = FOLLOWUPS.get(number,"retention")
            row = dict(id=f"COMMON_MESSAGE_{number}",file_path=stage.COMMON,
                clean_reference=reference(a),current_reference=reference(b),clean_hex=a.text.hex(),current_hex=b.text.hex(),
                Japanese=a.text.decode("cp932"),English=b.text.decode("ascii"), complete_exchange=CONTEXT[city],
                localization_note=note,decision=status,expanded_visible_lines=lines,original_requests=found,
                observed_page=panel,complete_line_ink_counts=counts,
                review=dict.fromkeys(stage.GATES,True) | {"localization": status=="retention","naturalness":status=="retention"})
            observations.append(row)
        covered[city] = dict(context=CONTEXT[city],cases=observations,
            distinct_selected_keys=sorted({r["message_ID"] for r in calls}),capture="ordinary emulator inputs",
            existing_save=donor,known_pending_keys_selected=sorted({r["message_ID"] for r in calls}&pending),
            evidence={str(folder/p):base.digest(folder/p) for p in ("capture/capture_report.json","requests.json","terminal.json")})
    base.save(OUTPUT,dict(candidate_sha256=release["candidate_sha256"],clean_sha256=release["clean_input_sha256"],
        current_town_observations=covered,old_review_count_preserved=True,hardware=False,new_dialogue_credit=0))
    print("Verified",sum(len(row["cases"]) for row in covered.values()),"complete town dialogue holds.")


if __name__ == "__main__":
    main()
