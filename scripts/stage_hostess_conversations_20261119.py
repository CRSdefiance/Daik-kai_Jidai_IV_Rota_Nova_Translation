"""Review the complete tavern hostess interaction family and stage four replies."""

from collections import defaultdict
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.dialogue.review import REQUIRED_REVIEW_GATES, validate_natural_dialogue_batch
from scripts import register_departure_warnings_20261119 as parent
from scripts import stage_departure_warnings_20261119 as port
from scripts.verify_barmaid_scoped_layout_v780 import formatter
from scripts.verify_personal_gameplay_v841 import get_machine

base, native, workflow = port.base, port.native, port.workflow
ARM, COMMON, CLEAN = port.ARM, port.COMMON, port.CLEAN
ROOT = Path("work/hostess_conversations_20261119/staged_v1")
ROM = ROOT / "Hostess_Conversations_STAGED.nds"
PROOF = ROOT / "staged.json"
SHEET = ROOT / "hostess_reply_pages.png"
HISTORY = Path("translations/barmaid_contextual_editorial_manuscript_v1.json")
MATRIX = Path("work/analysis/barmaid_editorial_v779/layouts_v1/native_layout_matrix.json")
PENDING = port.PENDING
EDITS = {
    992: ("Stay and listen. This one's fado. La la la...",
          "Julia invites the sailor to listen, names the Portuguese song tradition and sings. The invitation sounds spoken."),
    994: ("Sorry, I've got to get home early. My little brothers and sisters are waiting.",
          "The companionable apology and everyday family terms preserve the younger brothers and sisters waiting at home."),
    1004: ("On days off, I walk in the garden. Seeing the flowers and trees puts me at ease.",
           "Keep the regular garden walks and the quiet emotional effect of seeing the plants. The speaker describes how she feels in everyday language."),
    1015: ("Men go to sea and women stay home? That's old-fashioned. Why shouldn't women go out into the world, too?",
           "The speaker challenges the expectation that women stay home. Her direct question keeps the source's invitation to reconsider that role."),
}
RETENTIONS = {
    989: "The hostess introduces herself first, confirms the captain's first name and gives a warm invitation to return.",
    990: "The question and compliment put the captain's first name first. The hostess introduces herself in the next beat.",
    991: "The brisk question turns into a personal hope for a good partner and happiness, as in the source.",
    993: "The confession sounds rueful and keeps both falling easily and the repeated disappointment.",
    995: "Nuisance conveys the practical annoyance of customers falling asleep drunk.",
    996: "Admiration of the sailors turns into a resolve to ease her parents' burden. The original city branch remains in storage.",
    997: "The playful laugh and reply keep the joke of throwing the age question back at the player.",
    998: "The invitation to settle in fits any of the ordinary chats.",
    999: "The sudden burst of affection fits the gift response. The captain's first name stays in its original argument slot.",
    1000: "The surprise at the gift's cost leads into an immediate, personal thank-you.",
    1001: "The brief pause between thanks and reassurance sounds like setting the guest at ease.",
    1002: "Mentioning Venus preserves the source comparison, and the playful laugh keeps the tone.",
    1003: "The short invitation matches the cheerful suggestion to drink and get lively.",
    1005: "The pie and invitation to stay are both explicit in the source.",
    1006: "The complaint about stinginess turns into a teasing check on the person in front of her.",
    1007: "The sung opening leads into the waiting lover's story and the difficulty of loving a sailor.",
    1008: "The eager greeting and request for stories from foreign lands match the curious voice.",
    1009: "The town's liveliness explains her affection, and the last sentence preserves her response to gloomy places.",
    1010: "The enthusiasm for ruins and the romantic prospect of glimpsing earlier lives land as distinct thoughts.",
    1011: "The fashion judgment and reluctance to go out with someone who ignores it preserve the source's bluntness.",
    1012: "The direct praise trails into the two qualities she names. The pause suits the intimate delivery.",
    1013: "The offer of a reading and the surprised follow-up keep the exchange playful.",
    1014: "The offer to spoil the tired sailor preserves the teasing cadence and the small limit.",
    1016: "The speaker describes her former unease and the unusual trust she feels in this person.",
    1017: "Admiration for sailors turns quickly into curiosity about dolphins and whales, with both questions intact.",
    1018: "The three quick questions keep her curiosity about pirates, their ships and their strength.",
    1019: "The line preserves that the animals are hunted for fur and the speaker's distress at the cruelty.",
}


def main():
    assert not ROOT.exists()
    release, ledger = map(base.load, (parent.RELEASE, base.LEDGER))
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(parent.ROM) == release["candidate_sha256"] == ledger["current_integrated_candidate"]["sha256"]
    assert base.digest(CLEAN) == release["clean_input_sha256"]
    runtime = workflow.RegisteredRuntime(parent.RELEASE,release["own_registered_startup"],captain=3)
    arm, common = runtime.arm, runtime.common
    clean = base.NdsImage.open(CLEAN)
    ja = clean.read_file(ARM)
    clean_entries = workflow.common_message_entries(clean.read_file(COMMON),ja)
    directory = native.digest(arm[workflow.DIRECTORY_OFFSET:workflow.TABLE_OFFSET])
    previous = workflow.owned_entries(common,arm,directory)
    history = {r["message_id"]:r for r in base.load(HISTORY)["records"]}
    credited = {(r["file_path"],r["id"]) for r in ledger[base.CONTEXT]["integrated_record_keys"]}
    assert list(range(989,1020)) == sorted(EDITS.keys()|RETENTIONS.keys()) == sorted(history)
    for start,end in ((0x58F4C,0x5964C),(0x5964C,0x59800)):
        assert arm[start:end] == ja[start:end]
    edits = {n:b" "+v[0].encode("ascii") for n,v in EDITS.items()}
    assert all(len(t)<=len(previous[n].text) and previous[n].text.startswith(b" ") for n,t in edits.items())
    after, entries, allocation = port.owned_deployment(common,arm,previous,edits)
    assert all(workflow.reference(entries[r["message_ID"]])==r["current_reference"] and
        entries[r["message_ID"]].text.hex()==r["current_hex"] for r in base.load(PENDING)["records"])

    changed = workflow.with_components(runtime,arm,after)
    cpu,get,provider = changed.machine(arm,after,changed.raw,changed.plan)
    model,_ = get_machine(arm,runtime.raw)
    format_case,_ = formatter()
    variants = defaultdict(list)
    for case in base.load(MATRIX)["cases"]:
        variants[case["id"]].append(tuple(bytes.fromhex(v) for v in case["source_values_hex"]))
    assert len(variants)==31 and sum(map(len,variants.values()))==273

    raster, independent, font = port.font_tools(runtime.image)
    kanji = runtime.image.read_file("/GRP/KANJI.FNT")
    sheet = Image.new("RGB",(466,122*len(EDITS)),"#263238")
    draw = ImageDraw.Draw(sheet)
    rows = []
    for n in sorted(history):
        old, new, source, prior = previous[n], entries[n], clean_entries[n], history[n]
        assert (COMMON,prior["id"]) in credited and prior["source_hex"] == source.text.hex()
        previous_words = old.text.decode("ascii").strip()
        assert previous_words==prior["english"].removesuffix("{PAD}")
        words,note = EDITS[n] if n in EDITS else (previous_words,RETENTIONS[n])
        args = int(n in (989,990))*2 + int(n==999)
        assert source.text.count(b"%s")==old.text.count(b"%s")==new.text.count(b"%s")==args
        assert prior["English_argument_source_indices"]==list(range(args))
        assert bytes(cpu.mem_read(get(0x5528C,n),len(new.text)+1))==new.text+b"\0"
        assert new.text==b" "+words.encode("ascii")
        cases = []
        for values in variants[n]:
            case = format_case(model,prior|{"english":words},values)
            if n not in EDITS:
                assert case["findings"] in ([],["weak_line_end"])
            else:
                assert not values and not case["findings"]
                old_case = format_case(model,prior,values)
                lines,plane=port.render(arm,bytes.fromhex(case["formatted_hex"]),raster,independent,kanji)
                assert lines==case["lines"] and " ".join(lines)==words
                y=list(EDITS).index(n)*122
                draw.text((5,y+4),f"{n} revised",fill="white")
                tile=Image.frombytes("L",(228,48),bytes(0 if p else 255 for p in plane))
                sheet.paste(tile.resize((456,96),Image.Resampling.NEAREST),(5,y+21))
                case["native_plane_sha256"]=native.digest(plane)
                case["previous_visible_lines"]=old_case["lines"]
            cases.append(case)
        row=dict(id=prior["id"],message_ID=n,file_path=COMMON,speaker=prior["speaker"],context=prior["context"],
            source_meaning=prior["source_meaning"],localization_note=note,decision="revision" if n in EDITS else "retention",
            english=words,previous_English=previous_words,clean_Japanese=source.text.decode("cp932"),
            source_hex=source.text.hex(),current_hex=old.text.hex(),staged_hex=new.text.hex(),
            source_reference=workflow.reference(source),current_reference=workflow.reference(old),staged_reference=workflow.reference(new),
            native_name_argument_order=prior["source_native_arguments"],source_selections=prior["native_catalog_selections"],
            original_direct_dispatch=0x02054014,layout_cases=cases,review=dict.fromkeys(REQUIRED_REVIEW_GATES,True))
        rows.append(row)
    assert provider.reads and bytes(cpu.mem_read(runtime.actor_root,0x1A04))==runtime.actor_bytes
    image=base.NdsImage.open(parent.ROM)
    image.replace_file(COMMON,after)
    data=bytes(image.rom.save())
    image.replace_file(COMMON,common)
    assert bytes(image.rom.save())==parent.ROM.read_bytes()
    ROOT.mkdir(parents=True)
    ROM.write_bytes(data)
    sheet.save(SHEET)
    review=dict(translation_policy="natural-dialogue-v2",target_locale="en-US",encoder="dialogue-relocatable-v1",
        review_gates=sorted(REQUIRED_REVIEW_GATES),candidate_sha256=base.digest(ROM),records=rows)
    validate_natural_dialogue_batch(review)
    base.save(PROOF,review|dict(parent_sha256=release["candidate_sha256"],clean_input_sha256=release["clean_input_sha256"],
        target_COMMON_sha256=native.digest(after),entire_parent_inverse=True,allocation=allocation,font=font,
        visual_layout_cases=273,sheets=[dict(path=str(SHEET),sha256=base.digest(SHEET))],
        source_proofs={str(p):base.digest(p) for p in (parent.RELEASE,HISTORY,MATRIX,PENDING,Path(__file__))}))
    print("Reviewed 31 hostess replies and all 273 native layouts.")


if __name__ == "__main__":
    main()
