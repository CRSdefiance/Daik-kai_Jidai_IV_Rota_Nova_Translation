"""Stage the contextual Inn stay, rumor and information exchanges."""

from collections import defaultdict
from inspect import getsource
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.dialogue.review import REQUIRED_REVIEW_GATES, validate_natural_dialogue_batch
from scripts import probe_tavern_continuation_layout_v768 as shared_format
from scripts import register_hostess_conversations_20261119 as parent
from scripts import stage_departure_warnings_20261119 as port
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_shipyard_gameplay_v760 import independent_font

base, native, workflow = port.base, port.native, port.workflow
ARM, COMMON, CLEAN, PENDING = port.ARM, port.COMMON, port.CLEAN, port.PENDING
ROOT = Path("work/inn_conversations_20261119/staged_v2")
ROM, PROOF = ROOT/"Inn_Conversations_STAGED.nds", ROOT/"staged.json"
HISTORY = Path("translations/palace_inn_contextual_final_review_v2.json")
LAYOUTS = Path("work/analysis/palace_inn_layouts_v2255")
MATRIX = LAYOUTS/"all54_current_native_layouts.json"
FORMATTER = LAYOUTS/"effective_formatter.py"
EDITS = {
    1179: ("It's 1 gold coin for each night. How many nights will you stay?",
           "The innkeeper gives the unchanged nightly price and asks for the number of nights. The two complete thoughts now occupy separate lines."),
    1182: ("Over in %s, I hear the price of %s has plummeted.",
           "The innkeeper introduces the news as hearsay before reporting the price crash, keeping the town and goods in their native order. The next reply identifies the company that lost money."),
    1195: ("%s, I hear %s fought %s's fleet and won a great victory!",
           "The innkeeper passes along the victorious fleet rumor with an enthusiastic ending. The three original substitutions keep the date and identify the two sides."),
    1196: ("%s, I hear %s took on %s's fleet and got beaten back.",
           "The companion rumor gives the date and preserves who attacked and who repelled them. The hearsay cue works with both this and the victory variant."),
}
RETENTIONS = {
    1177: "That'll be sounds like a spoken price quote and keeps the single coin for the one-night confirmation.",
    1178: "The warm farewell suits the transition from confirmation to rest.",
    1180: "Then ties the confirmation to the player's choice, with all three original night counts preserved.",
    1181: "The short good wishes follow the agreed multi-night stay naturally.",
    1183: "The town-and-goods rumor comes first. This follow-up makes the affected company's loss specific and keeps it hearsay.",
    1184: "The word all preserves the buyout, with someone leaving the buyer unidentified as in the source.",
    1185: "Missing out follows the buyout clearly and keeps the affected company's frustration rather than making the innkeeper angry.",
    1186: "The straightforward report opening suits the first officer voice and hands over to the information panel.",
    1187: "Obtained preserves the more ceremonious voice and the formal address to the captain.",
    1188: "Looked into and for you sound conversational and keep the officer's proactive work.",
    1189: "Oh, by the way preserves the speaker's casual change of subject without supplying a title the source omits.",
    1190: "Checking up on preserves this voice's more familiar delivery without claiming a new discovery.",
    1191: "I've got keeps the plainspoken assurance. The following panel supplies the substance.",
    1192: "Did some digging and the exclamation keep this voice's eagerness without adding an address.",
    1193: "The deliberate, formal wording distinguishes the last alternate report from the casual and exuberant voices.",
    1194: "The innkeeper gives the straightforward reason the stay cannot proceed. The line introduces no extra condition.",
    1197: "The attack and the innkeeper's disapproval are distinct beats. The town is the target here.",
    1198: "Serves them right preserves the reaction to the failed raid. The innkeeper makes no new claim about casualties.",
    1199: "The surprised question fits a guest interrupting an ongoing stay and keeps already at the natural end of the question.",
}
CONTEXTS = {
    (1177,1178): "The innkeeper quotes the fee for a one-night stay and wishes the guest well if they accept.",
    (1179,1180,1181,1194,1199): "The innkeeper offers a longer stay, confirms the chosen duration, then welcomes the guest. Insufficient funds and an interrupted stay have their own responses.",
    (1182,1183): "The innkeeper first reports the crash in one market and then names the company rumored to have lost money.",
    (1184,1185): "The first reply describes the market buyout. The next describes the company that missed its chance.",
    tuple(range(1186,1194)): "These independent crew voices introduce the same kind of information panel after the officer has made inquiries.",
    (1195,1196): "The innkeeper dates a rumor of fleet combat. The winning and repelled outcomes are alternatives.",
    (1197,1198): "The innkeeper dates a rumor of a town raid, condemning the attack or taking satisfaction in its failure.",
}


def physical_renderers(image):
    raster, _, _ = port.font_tools(image)
    source = getsource(independent_font)
    original = "(row * 16 + y) * 228"
    assert source.count(original) == 1
    adjusted = source.replace(original, "(row * 16 + y + (len(code) == 1)) * 228")
    scope = vars(__import__(independent_font.__module__, fromlist=["independent_font"])).copy()
    exec(compile(adjusted, __file__ + "::physical-reference", "exec"), scope)
    return raster, scope["independent_font"], native.digest(adjusted.encode())


def main():
    assert not ROOT.exists()
    release, ledger = map(base.load, (parent.RELEASE,base.LEDGER))
    assert base.digest(base.REGISTRY)==release["registry_sha256"]
    assert base.digest(parent.ROM)==release["candidate_sha256"]==ledger["current_integrated_candidate"]["sha256"]
    assert base.digest(CLEAN)==release["clean_input_sha256"]
    runtime = workflow.RegisteredRuntime(parent.RELEASE,release["own_registered_startup"],captain=3)
    arm, common = runtime.arm, runtime.common
    clean = base.NdsImage.open(CLEAN)
    original_arm = clean.read_file(ARM)
    clean_entries = workflow.common_message_entries(clean.read_file(COMMON),original_arm)
    directory = native.digest(arm[workflow.DIRECTORY_OFFSET:workflow.TABLE_OFFSET])
    previous = workflow.owned_entries(common,arm,directory)
    credited = {(r["file_path"],r["id"]) for r in ledger[base.CONTEXT]["integrated_record_keys"]}
    historical = {r["message_ID"]:r for r in base.load(HISTORY)["records"] if 1177<=r["message_ID"]<=1199}
    assert sorted(historical)==sorted(EDITS.keys()|RETENTIONS.keys())==list(range(1177,1200))
    edits = {n:b" "+words.encode("ascii") for n,(words,_) in EDITS.items()}
    assert all(previous[n].text.startswith(b" ") and len(text)<=len(previous[n].text) for n,text in edits.items())
    after, entries, allocation = port.owned_deployment(common,arm,previous,edits)
    assert all(workflow.reference(entries[r["message_ID"]])==r["current_reference"] and
        entries[r["message_ID"]].text.hex()==r["current_hex"] for r in base.load(PENDING)["records"])

    changed = workflow.with_components(runtime,arm,after)
    cpu,get,provider = changed.machine(arm,after,changed.raw,changed.plan)
    machine,_ = get_machine(arm,runtime.raw)
    scope = vars(shared_format).copy()
    exec(compile(FORMATTER.read_text(encoding="utf-8"),str(FORMATTER),"exec"),scope)
    format_case = scope["format_case"]
    variants = defaultdict(list)
    for case in base.load(MATRIX)["cases"]:
        if case["id"] in historical:
            variants[case["id"]].append(case)
    assert set(variants)==set(historical) and sum(map(len,variants.values()))==1169
    raster, independent, oracle_hash = physical_renderers(runtime.image)
    kanji = runtime.image.read_file("/GRP/KANJI.FNT")
    rows, previews = [], []
    for n,prior in historical.items():
        old,new,source = previous[n],entries[n],clean_entries[n]
        before = old.text.decode("ascii").strip()
        assert prior["english"].removesuffix("{PAD}")==before
        assert (COMMON,prior["id"]) in credited and prior["source_hex"]==source.text.hex()
        words,reason = EDITS[n] if n in EDITS else (before,RETENTIONS[n])
        assert new.text==b" "+words.encode("ascii")
        args = len(prior["source_native_arguments"])
        assert source.text.count(b"%s")==old.text.count(b"%s")==new.text.count(b"%s")==args
        assert prior["English_argument_source_indices"]==list(range(args))
        assert bytes(cpu.mem_read(get(0x5528C,n),len(new.text)+1))==new.text+b"\0"
        cases, shapes = [], defaultdict(list)
        for previous_case in variants[n]:
            values = tuple(bytes.fromhex(v) for v in previous_case["source_values_hex"])
            case = format_case(machine,prior|{"english":words},values)
            assert not case["findings"] and 1<=len(case["lines"])<=4
            if n not in EDITS:
                assert case["formatted_hex"]==previous_case["formatted_hex"]
            else:
                shape = (len(case["lines"]),any(not v.isascii() for v in values))
                shapes[shape].append(case)
            cases.append(case)
        for same_shape in shapes.values():
            case = max(same_shape,key=lambda c:len(bytes.fromhex(c["formatted_hex"])))
            formatted = bytes.fromhex(case["formatted_hex"])
            events = []
            plane,used = raster(arm,formatted,0x01FFCE40-0x02000000,size=(228,64),complete=False,
                instruction_limit=2000000,glyph_events=events)
            assert used==len(formatted) and plane==independent(arm,kanji,case["lines"])
            assert [g["code"] for g in events if g["code"]!=32]==port.glyph_codes(formatted)
            assert all(0<=g["x"]<=228-(12 if g["code"]>255 else 6) and 0<=g["y"]<=52 for g in events)
            assert sorted({g["y"] for g in events})==list(range(0,16*len(case["lines"]),16))
            case["native_physical_plane_sha256"]=native.digest(plane)
            tile = Image.frombytes("L",(228,64),bytes(0 if p==1 else 180 if p else 255 for p in plane))
            previews.append((f"{n}   {len(case['lines'])} rows",tile))
        context, = (label for group,label in CONTEXTS.items() if n in group)
        rows.append(dict(id=prior["id"],message_ID=n,file_path=COMMON,speaker=prior["speaker"],
            context=context,source_meaning=prior["source_meaning"],decision="revision" if n in EDITS else "retention",
            localization_note=reason,english=words,previous_English=before,clean_Japanese=source.text.decode("cp932"),
            source_hex=source.text.hex(),current_hex=old.text.hex(),staged_hex=new.text.hex(),
            source_reference=workflow.reference(source),current_reference=workflow.reference(old),staged_reference=workflow.reference(new),
            native_binding=prior["native_binding"],native_arguments_in_order=prior["source_native_arguments"],
            layout_cases=cases,review=dict.fromkeys(REQUIRED_REVIEW_GATES,True)))
    assert provider.reads and bytes(cpu.mem_read(runtime.actor_root,0x1A04))==runtime.actor_bytes
    image = base.NdsImage.open(parent.ROM)
    image.replace_file(COMMON,after)
    target = bytes(image.rom.save())
    image.replace_file(COMMON,common)
    assert bytes(image.rom.save())==parent.ROM.read_bytes()
    review = dict(translation_policy="natural-dialogue-v2",target_locale="en-US",encoder="dialogue-relocatable-v1",
        review_gates=sorted(REQUIRED_REVIEW_GATES),candidate_sha256=native.digest(target),records=rows)
    validate_natural_dialogue_batch(review)
    ROOT.mkdir(parents=True)
    ROM.write_bytes(target)
    assert base.digest(ROM)==review["candidate_sha256"]
    sheets = []
    for start in range(0,len(previews),8):
        batch = previews[start:start+8]
        canvas = Image.new("RGB",(932,152*((len(batch)+1)//2)),"#263238")
        draw = ImageDraw.Draw(canvas)
        for i,(label,tile) in enumerate(batch):
            x,y = 466*(i%2),152*(i//2)
            draw.text((x+5,y+3),label,fill="white")
            canvas.paste(tile.resize((456,128),Image.Resampling.NEAREST),(x+5,y+21))
        sheet = ROOT/f"inn_native_pages_{start//8+1}.png"
        canvas.save(sheet)
        sheets.append(dict(path=str(sheet),sha256=base.digest(sheet)))
    base.save(PROOF,review|dict(parent_sha256=release["candidate_sha256"],clean_input_sha256=release["clean_input_sha256"],
        target_COMMON_sha256=native.digest(after),entire_parent_inverse=True,allocation=allocation,
        native_layout_cases=1169,screenshot_pitch_oracle_sha256=oracle_hash,sheets=sheets,
        source_proofs={str(p):base.digest(p) for p in (parent.RELEASE,HISTORY,MATRIX,FORMATTER,PENDING,Path(__file__))}))
    print(f"Reviewed 23 Inn records, checked 1,169 native layouts and rendered {len(previews)} changed pages.")


if __name__ == "__main__":
    main()
