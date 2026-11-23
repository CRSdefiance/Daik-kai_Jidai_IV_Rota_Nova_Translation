"""Localize supply arguments in sailing dialogue without changing the resource menu labels."""

from argparse import ArgumentParser
from pathlib import Path
from re import escape, finditer
from struct import iter_unpack, pack, unpack_from
from types import FunctionType

from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts import checkpoint_ship_emergency_review_v1 as source
from scripts import register_istanbul_tobacco_20261122 as parent
from scripts import replay_ceuta_sea_encounters_20261122 as voyage
from scripts import stage_rafael_deck_tutorial_followup_20261122 as established
from scripts import stage_ship_emergency_review_v1 as ship
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.seal_shared_text_source_v1 import reference
from scripts.stage_expedition_report_wraps_20261115 import owned_deployment


base, native = parent.base, parent.native
ARM, COMMON = source.ARM, source.COMMON
ROOT = voyage.ROOT / "staged"
ROM = ROOT / "Sailing_Supply_Alerts_STAGED.nds"
PROOF, MANUSCRIPT, NATIVE = ROOT / "stored_proof.json", ROOT / "contextual_review.json", ROOT / "native_pages.json"
PATCH, REBUILT = ROOT / "translation.xdelta", ROOT / "clean_rebuilt.nds"
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
PRIOR = Path("releases/all_routes_editorial_20261111_ship_emergency_candidate/verification/registered_review.json")
PENDING = Path("translations/editorial_checkpoints/SharedText_20261110_v1/shared_display_worklist_20261121_v3.json")
IDS = tuple(range(601,614))
REVISED = 607
NEW_TEXT = "O-oh no! We're out of %s!"
BASE = source.BASE
GET = 0xA4C24
POINTERS = 0xA4C34
SLOT = 0x151624
BEFORE = bytes.fromhex("90850000904897c600000000")
AFTER = b"water\0food\0\0"
OLD_POINTERS = (0x02387CAC,0x02387CB4)
NEW_POINTERS = (BASE+SLOT,BASE+SLOT+6)
ROUTINE_CALLS = (0x78278,0x81E9C)
NOTES = (
    "Keep the direct, urgent warning about the last of the supply. The sentence reads naturally with the common noun in lowercase.",
    "The measured full sentence reports that the named supply is gone and suits this voice.",
    "The familiar first-person report is clear, and the contraction suits a hurried announcement.",
    "The direct statement emphasizes that nothing remains in this speaker's matter-of-fact voice.",
    "Keep the clipped, urgent warning. It sounds right in the middle of sailing.",
    "The older speaker's dismay comes through in 'gone and run out,' without adding a consequence.",
    "Restore the startled stammer in the original exclamation, then let the younger sailor state the emergency directly.",
    "The emphatic first-person report states the shortage without inventing a remedy.",
    "Keep the groan, dizzy spell, hunger, and trailing fear. The distressed speech progresses in four audible beats.",
    "The formal report puts the cause before the decision to stop automatic travel.",
    "The pause separates a realization about the shortage from the terse confirmation that travel is stopping.",
    "The older speaker states the cause and then tells the crew they will stop. The two sentences keep those actions clear.",
    "Keep the young speaker's realization in the tag and the decision to stop in the first person.",
)


def logical(payload):
    return " ".join(payload.decode("ascii").split())


def references_to(files, address):
    literal = escape(pack("<I",address))
    return [(p,m.start()) for p,data in files.items() for m in finditer(literal,data)]


def direct_calls(arm, destination):
    hits = []
    for index,(word,) in enumerate(iter_unpack("<I",arm[:len(arm)//4*4])):
        if word >> 24 & 15 not in (10,11):
            continue
        displ = ((word & 0xFFFFFF) ^ 0x800000) - 0x800000
        at = 4 * index
        if BASE+at+8+4*displ == destination:
            hits.append(at)
    return tuple(hits)


def project(clean, current):
    clean_arm, arm = clean[ARM], current[ARM]
    assert clean_arm[GET:POINTERS] == arm[GET:POINTERS] == bytes.fromhex("000050e304009f0504009f151eff2fe1")
    assert unpack_from("<2I",clean_arm,POINTERS) == (BASE+SLOT,BASE+SLOT+4)
    assert unpack_from("<2I",arm,POINTERS) == OLD_POINTERS
    assert clean_arm[SLOT:SLOT+len(BEFORE)] == arm[SLOT:SLOT+len(BEFORE)] == BEFORE
    assert direct_calls(clean_arm,BASE+GET) == direct_calls(arm,BASE+GET) == ROUTINE_CALLS
    assert references_to(clean,BASE+GET) == references_to(current,BASE+GET) == []
    for offset in range(len(BEFORE)):
        expected = {0:[(ARM,POINTERS)],4:[(ARM,POINTERS+4)]}.get(offset,[])
        assert references_to(clean,BASE+SLOT+offset) == expected
        assert references_to(current,BASE+SLOT+offset) == []
    for site in ROUTINE_CALLS:
        assert arm[site-8:site+8] == clean_arm[site-8:site+8]
    target = bytearray(arm)
    target[POINTERS:POINTERS+8] = pack("<2I",*NEW_POINTERS)
    target[SLOT:SLOT+len(AFTER)] = AFTER
    assert len(target) == len(arm)
    target = bytes(target)
    assert target[DIRECTORY_OFFSET:TABLE_OFFSET] == arm[DIRECTORY_OFFSET:TABLE_OFFSET]
    inverse = bytearray(target)
    inverse[POINTERS:POINTERS+8] = arm[POINTERS:POINTERS+8]
    inverse[SLOT:SLOT+len(BEFORE)] = BEFORE
    assert inverse == arm
    return target, dict(getter=BASE+GET, call_sites=[BASE+s for s in ROUTINE_CALLS],
        original_pointers=list(OLD_POINTERS), new_pointers=list(NEW_POINTERS), literal_word_offset=POINTERS,
        japanese_text_slot={"offset":SLOT, "before":BEFORE.hex(), "after":AFTER.hex()},
        adjacent_bytes_exact=True, shared_menu_label_bytes_unchanged=True)


def stage():
    assert not ROOT.exists()
    previous = base.load(parent.RELEASE)
    assert base.digest(parent.ROM) == previous["candidate_sha256"]
    assert base.digest(parent.MANIFEST) == previous["manifest_sha256"]
    assert base.digest(base.REGISTRY) == previous["registry_sha256"]
    assert base.digest(native.CLEAN) == previous["clean_input_sha256"]
    source_image,image = map(base.NdsImage.open,(native.CLEAN,parent.ROM))
    clean,current = map(native.files,(source_image,image))
    arm, shared = current[ARM],current[COMMON]
    assert native.digest(arm) == previous["target_ARM9_sha256"]
    assert native.digest(shared) == previous["target_COMMON_sha256"]
    arm_target,owner = project(clean,current)
    directory = native.digest(arm[DIRECTORY_OFFSET:TABLE_OFFSET])
    old = owned_entries(shared,arm,directory)
    jp = common_message_entries(clean[COMMON],clean[ARM])
    shared_target,rebound,allocations = owned_deployment(shared,arm_target,old,{REVISED:NEW_TEXT.encode("ascii")})
    assert [a.message_id for a,b in zip(old,rebound,strict=True) if a.text != b.text] == [REVISED]
    pending = base.load(PENDING)["records"]
    assert len(pending)==276
    assert all(reference(rebound[r["message_ID"]]) == r["current_reference"]
               and rebound[r["message_ID"]].text.hex() == r["current_hex"] for r in pending)
    prior = {r["message_ID"]:r for r in base.load(PRIOR)["records"]}
    records = []
    for n,why in zip(IDS,NOTES,strict=True):
        source_row,old_row,new_row = jp[n],old[n],rebound[n]
        past = prior[n]
        assert past["source_hex"] == source_row.text.hex() and past["source_reference"] == reference(source_row)
        assert past["registered_reference"]["exact_stored_hex"] == old_row.text.hex() and all(past["review"].values())
        assert past["english"] == logical(old_row.text)
        assert source_row.text.count(b"%s") == old_row.text.count(b"%s") == new_row.text.count(b"%s") == len(past["original_substitutions"])
        assert only_s_argument(source_row.text) and only_s_argument(new_row.text)
        if n==REVISED:
            assert "た、大変だよ！" in source_row.text.decode("cp932") and b"O-oh no!" in new_row.text
        records.append(dict(id=past["id"], message_ID=n,file_path=COMMON,
            speaker=past["speaker"],context=past["context"],source_meaning=past["source_meaning"],localization_note=why,
            clean_Japanese=source_row.text.decode("cp932"),english=logical(new_row.text),previous_English=logical(old_row.text),
            decision="revision" if n==REVISED else "retention",single_supply_display_argument_lowercase=n!=609,
            source_hex=source_row.text.hex(),current_hex=old_row.text.hex(),installed_hex=new_row.text.hex(),
            source_reference=reference(source_row),current_reference=reference(old_row),installed_reference=reference(new_row),
            original_substitutions=past["original_substitutions"],
            review={gate:gate!="formatting" for gate in source.GATES}))
    image.replace_file(ARM,arm_target)
    image.replace_file(COMMON,shared_target)
    target = native.files(image)
    assert current.keys()==target.keys() and {p for p in current if current[p]!=target[p]}=={ARM,COMMON}
    body = bytes(image.rom.save())
    image.replace_file(ARM,arm)
    image.replace_file(COMMON,shared)
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir()
    ROM.write_bytes(body)
    base.save(MANUSCRIPT,dict(translation_policy="natural-dialogue-v2",encoder="dialogue-relocatable-v1",
         target_locale="en-US",review_gates=source.GATES,records=records,previous_registered_review=str(PRIOR),
         previous_registered_review_sha256=base.digest(PRIOR),new_contextual_records=0,full_goal_complete=False))
    base.save(PROOF,dict(candidate_sha256=base.digest(ROM),predecessor_sha256=previous["candidate_sha256"],
         target_components={p:native.digest(target[p]) for p in (ARM,COMMON)},source_bound_sailing_supply_text=owner,
         whole_parent_inverse=True,stored_template_allocations=allocations,unchanged_alternate_display_records=276,
         manuscript_sha256=base.digest(MANUSCRIPT)))


def only_s_argument(raw):
    return raw.count(b"%")==raw.count(b"%s")


def verify_native():
    from scripts.preflight_shared_dynamic_notice_wrap_v1 import font_tools
    from scripts.preflight_shared_crew_notices_v1 import with_components
    from scripts.stage_mutiny_review_v1 import portrait_sheets,render_portrait

    proof,draft,release = map(base.load,(PROOF,MANUSCRIPT,parent.RELEASE))
    assert base.digest(ROM)==proof["candidate_sha256"] and base.digest(MANUSCRIPT)==proof["manuscript_sha256"]
    before = RegisteredRuntime(parent.RELEASE,release["own_registered_startup"],captain=3)
    target = base.NdsImage.open(ROM)
    after = with_components(before,target.read_file(ARM),target.read_file(COMMON))
    # Copy the two changed resident data fields into the otherwise exact registered context.
    raw = bytearray(after.raw)
    for offset,size in ((POINTERS,8),(SLOT,len(AFTER))):
        assert raw[offset:offset+size] == before.arm[offset:offset+size]
        raw[offset:offset+size] = after.arm[offset:offset+size]
    after.raw = bytes(raw)
    pairs = []
    for ctx,expected in ((before,(b"Water",b"Food")),(after,(b"water",b"food"))):
        cpu,get,_ = ctx.machine(ctx.arm,ctx.common,ctx.raw,ctx.plan)
        pointers = tuple(get(GET,i) for i in (0,1))
        args = tuple(bytes(cpu.mem_read(ptr,len(value)+1)) for ptr,value in zip(pointers,expected,strict=True))
        assert args == tuple(value+b"\0" for value in expected)
        assert pointers == (OLD_POINTERS if ctx is before else NEW_POINTERS)
        assert tuple(bytes(cpu.mem_read(ptr,len(value)+1)) for ptr,value in zip(OLD_POINTERS,(b"Water",b"Food"),strict=True)) == (b"Water\0",b"Food\0")
        ctx.calls.clear()
        pairs.append((pointers,expected))
    paper,_,font = font_tools(target)
    kanji = target.read_file("/GRP/KANJI.FNT")
    historical = base.load(source.OUTPUT)
    groups = {n:g for g in historical["exact_native_groups"] for n in range(g["first_ID"],g["last_ID"]+1)}
    format_case = ship.with_arguments()
    pages, cases = [], []
    for row in draft["records"]:
        number = row["message_ID"]
        if number == 609:
            continue
        group = groups[number]
        actor = next(i for i,_,n in group["original_voice_choices"] if n==number)
        options = ((label,) for label in pairs[1][1]) if number<609 else (
            (label,b"automatic travel") for label in (*pairs[1][1],b"water and food"))
        for args in options:
            body = bytes.fromhex(row["installed_hex"])
            result = format_case(after,row,group,body,actor,args)
            prepared = result.pop("display")
            plain = body % args
            assert b" ".join(prepared.split()) == b" ".join(plain.split())
            if number>=610:
                assert prepared == plain
            pixels,glyphs = render_portrait(paper,after.arm,kanji,prepared)
            assert [g["code"] for g in glyphs][0] == plain.lstrip()[0]
            assert [g["code"] for g in glyphs][-1] == plain.rstrip()[-1]
            lines = [line.strip() for line in prepared.decode("ascii").splitlines()]
            assert 1 <= len(lines) <= 2 and all(1 <= len(line) <= 36 for line in lines)
            pages.append((f"{number} {' / '.join(x.decode('ascii') for x in args)}",pixels))
            cases.append(dict(message_ID=number,arguments=[arg.decode("ascii") for arg in args],prepared_hex=prepared.hex(),
                lines=lines,native_glyphs=len(glyphs),native_plane_sha256=native.digest(pixels),
                exact_first_and_last=True,full_raster_and_bounds=True,source_derived_voice_table=result))
    assert len(cases)==28
    sheets=portrait_sheets(ROOT,pages)
    base.save(NATIVE,dict(candidate_sha256=proof["candidate_sha256"],stored_proof_sha256=base.digest(PROOF),
        all_supply_modes_and_voice_cases=cases,retained_title_case_menu_strings=True,exact_actual_getter_pointers=pairs[1][0],
        earlier_voice_contract=str(source.OUTPUT),earlier_voice_contract_sha256=base.digest(source.OUTPUT),formatting_sheets=sheets,
        automatic_travel_checked_offline=True))


if __name__ == "__main__":
    cli=ArgumentParser(description=__doc__)
    cli.add_argument("action",choices=("stage","native","patch","startup"))
    action=cli.parse_args().action
    if action=="stage":
        stage()
    elif action=="native":
        verify_native()
    else:
        task=getattr(established,action)
        FunctionType(task.__code__,task.__globals__|globals())()

