"""Keep the approved words together in two original Square rumor panels."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace

from ndspy.code import MainCodeFile,loadOverlayTable

from scripts import register_square_shop_names_20261122 as parent
from scripts import register_square_rumor_followup_20261122 as prior
from scripts import stage_square_country_briefings_20261115 as town
from scripts import replay_square_rumors_20261115 as play
from scripts import stage_rafael_deck_tutorial_followup_20261122 as precedent
from scripts.stage_shared_notices_storage_v1 import relocate
from scripts.source_locked_derivation_v5118 import checked_text
from dk4tool.patch.square_caption_cells import assemble
from dk4tool.patch.main_pool_cache_visibility import cache_plan


base,native = parent.base,parent.native
ARM,COMMON,CLEAN = town.ARM,town.COMMON,town.CLEAN
ROOT = Path("work/analysis/square_rumor_wraps_20261122")
ROM,PROOF = ROOT/"Square_Rumor_Wraps_STAGED.nds",ROOT/"stored_proof.json"
PATCH,REBUILT = ROOT/"translation.xdelta",ROOT/"clean_rebuilt.nds"
STARTUP_CAPTURE = ROOT/"startup/capture/capture_report.json"
BASE,ITCM,STUB,TAIL,STOP = 0x02000000,0x01FFC000,0x01FFC664,0x01FFC684,0x01FFC694
WRAP,FALLBACK,LITERAL = 0x01FFCF78,0x02157084,0x01FF9FAC
PROMOTION = f"add ip,ip,#13; cmp ip,#6; bls {WRAP}; b {FALLBACK}"
PHRASES = {710:("Times certainly have changed!",),713:("in the Indian Ocean.",)}
NOTES = {
    710:"Keep the shopkeeper's surprise about young women going to sea to trade. The reaction sentence now occupies its own line.",
    713:"Keep Albuquerque's rank, the ancestor's reputation, fleet command and hearsay. Keep the phrase in the Indian Ocean together.",
}
FRAMES = (5600,5900,6050,6250)
FOCUSED = ROOT/"selected_rumors"


def transform(image,arm):
    code = MainCodeFile(arm,BASE)
    itcm = code.sections[4].data
    assert code.sections[4].ramAddress==ITCM and bytes(code.save())==arm
    first,tail = STUB-ITCM,TAIL-ITCM
    stock = assemble(f"sub ip,r3,#688; cmp ip,#53; bls {WRAP}; "+PROMOTION,STUB)
    assert len(stock)==28 and bytes(itcm[first:first+28])==stock
    assert itcm[0x194:0x198]==bytes.fromhex("80c6ff01")
    assert itcm[0x680:0x684]==bytes(4) and itcm[tail:STOP-ITCM]==bytes(STOP-TAIL)
    assert bytes(itcm[0xF40:0xF54])==bytes.fromhex("b4c09fe50c0053e1b3ffff1a74329de5c3fdffea")
    assert bytes(itcm[0xFFC:0x1000])==bytes.fromhex("14400502")
    # Unlike the neighboring four-byte Market scratch word, this span has no prior reference.
    units = [(s.ramAddress,bytes(s.data)) for s in code.sections]
    units += [(s.ramAddress,bytes(s.data)) for s in loadOverlayTable(image.rom.arm9OverlayTable,
        lambda _, i:image.rom.files[i]).values()]
    for origin,data in units:
        assert all((value.to_bytes(4,"little") not in data) for value in range(TAIL,STOP))
        for pos in range(0,len(data)-3,4):
            word = int.from_bytes(data[pos:pos+4],"little")
            if word&0x0E000000==0x0A000000 and word>>28!=15:
                step = ((word&0xFFFFFF)^0x800000)-0x800000
                assert not TAIL <= origin+pos+8+4*step < STOP
    payload = assemble(f"sub ip,r3,#688; cmp ip,#22; cmpne ip,#25; beq {LITERAL}; cmp ip,#53; bls {WRAP}; b {TAIL}",STUB)
    tail_payload = assemble(PROMOTION,TAIL)
    assert len(payload)==len(stock) and len(tail_payload)==STOP-TAIL
    itcm[first:first+28],itcm[tail:STOP-ITCM] = payload,tail_payload
    revised = bytes(code.save())
    assert cache_plan(arm)==cache_plan(revised) and itcm[0x680:0x684]==bytes(4)
    itcm[first:first+28],itcm[tail:STOP-ITCM] = stock,bytes(STOP-TAIL)
    assert bytes(code.save())==arm
    return revised,dict(entry=STUB,relocated_tail=[TAIL,STOP],original=stock.hex(),
        entry_hex=payload.hex(),tail_hex=tail_payload.hex(),market_scratch_exact=True,
        source_literals_and_branches_into_tail_absent=True,whole_ARM9_inverse=True)


def stage():
    assert not ROOT.exists()
    meta,previous_review = map(base.load,(parent.RELEASE,prior.REVIEW))
    assert base.digest(parent.ROM)==meta["candidate_sha256"]
    assert base.digest(base.REGISTRY)==meta["registry_sha256"] and base.digest(parent.MANIFEST)==meta["manifest_sha256"]
    assert base.digest(CLEAN)==meta["clean_input_sha256"]
    ctx = town.RegisteredRuntime(parent.RELEASE,meta["own_registered_startup"],captain=3)
    image,clean = map(base.NdsImage.open,(parent.ROM,CLEAN))
    originals = native.files(image)
    arm,common = originals[ARM],originals[COMMON]
    assert arm==ctx.arm and common==ctx.common
    revised,scope = transform(image,arm)
    directory = native.digest(arm[town.DIRECTORY_OFFSET:town.TABLE_OFFSET])
    before = town.owned_entries(common,arm,directory)
    jp = town.common_message_entries(clean.read_file(COMMON),clean.read_file(ARM))
    existing = {r["message_ID"]:r for r in previous_review["records"]}
    assert len(existing)==21 and previous_review["unchanged_wrap_leads"]==sorted(PHRASES)
    rows = {}
    for key in PHRASES:
        r=existing[key]
        assert r["installed_hex"]==before[key].text.hex() and r["source_hex"]==jp[key].text.hex()
        assert r["english"]==" ".join(before[key].text.decode("ascii").split())
        assert r["preserved_runtime_arguments"]==[] and all(r["review"].values())
        rows[key] = r | dict(current_reference=town.reference(before[key]),current_hex=before[key].text.hex(),
            previous_English=r["english"],decision="revision",change_class="wrap_only",
            localization_note=NOTES[key],protected_phrases=PHRASES[key])
    wrap = FunctionType(town.compile_layouts.__code__,town.compile_layouts.__globals__ | dict(PHRASES=PHRASES))
    authored = wrap(rows)
    assert all(b"\n  " in value and b"%" not in value for value in authored.values())
    allocate = FunctionType(relocate.__code__,relocate.__globals__ | {"DIRECTORY":directory})
    deployed,target_arm,installed,allocation = allocate(common,revised,rows,authored)
    assert allocation["changed_visible_templates"]==list(PHRASES)
    assert allocation["complete_COMMON_and_ARM9_table_inverse"] and allocation["all_unselected_native_copy_spans_exact"]
    bound = town.with_components(ctx,target_arm,deployed)
    cpu,get,provider = bound.machine(target_arm,deployed,bound.raw,bound.plan)
    earlier,_,_ = ctx.machine(arm,common,ctx.raw,ctx.plan)
    control_keys = (674,*range(675,683),687,*range(688,730),741)
    pictures = []
    renderer,_,_ = town.font_tools(ctx.image)
    kanji = ctx.image.read_file("/GRP/KANJI.FNT")
    for key in control_keys:
        text = before[key].text
        args = ("Tea","Clove")[:text.count(b"%s")]
        assert text.count(b"%")==len(args), (key,text)
        a = town.native_layout(earlier,text,key,args)
        new = town.native_layout(cpu,installed[key].text,key,args)
        if key not in PHRASES:
            assert a==new
            continue
        p = get(0x5528C,key)
        body,lines = new
        assert body==authored[key] and bytes(cpu.mem_read(p,len(body)+1))==body+b"\0"
        assert 1<len(lines)<=4 and a[1]!=lines and " ".join(lines)==rows[key]["english"]
        assert all(any(phrase in line for line in lines) for phrase in PHRASES[key])
        for label,code,value in (("Before",arm,a[0]),("After",target_arm,body)):
            pixels,glyphs = town.render_portrait(renderer,code,kanji,value)
            assert [g["code"] for g in glyphs]==town.glyph_codes(value)
            pictures.append((f"{key} {label}",pixels))
            if label=="After":
                rows[key].update(before_lines=a[1],visible_lines=lines,installed_hex=body.hex(),
                    native_plane_hex=bytes(pixels).hex(),registered_reference=town.reference(installed[key]))
    assert provider.reads and len(pictures)==4
    assert bytes(cpu.mem_read(bound.actor_root,0x1A04))==bound.actor_bytes
    for path,data in ((ARM,target_arm),(COMMON,deployed)):
        image.replace_file(path,data)
    final = native.files(image)
    assert originals.keys()==final.keys() and {p for p in originals if originals[p]!=final[p]}=={ARM,COMMON}
    checks = parent.bind_registered_story_percent_guard(parent.guard_spec())(native.files(clean),final)
    assert checks["total_exact_source_bound_relocated_leading25_count"]==7
    result = bytes(image.rom.save())
    for path in (ARM,COMMON):
        image.replace_file(path,originals[path])
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir()
    ROM.write_bytes(result)
    candidate = base.digest(ROM)
    for row in rows.values():
        row["registered_reference"].update(candidate_sha256=candidate,file_path=COMMON,
            archive_sha256=native.digest(deployed),exact_stored_hex=row["installed_hex"])
    sheets = town.portrait_sheets(ROOT,pictures)
    base.save(PROOF,dict(candidate_sha256=candidate,predecessor_sha256=meta["candidate_sha256"],
        target_ARM9_sha256=native.digest(target_arm),target_COMMON_sha256=native.digest(deployed),
        clean_sha256=meta["clean_input_sha256"],whole_parent_inverse=True,records=list(rows.values()),
        allocations=allocation,native_scope=scope,source25=checks,unchanged_formatter_control_keys=[n for n in control_keys if n not in PHRASES],
        sheets={r["path"]:r["sha256"] for r in sheets}))
    print(f"Staged {candidate}. Both phrase groups and all {len(control_keys)-2} neighboring controls passed.",flush=True)


def focus(region):
    proof = base.load(PROOF)
    assert region in (1,4) and proof["candidate_sha256"]==base.digest(ROM)
    digest = proof["target_ARM9_sha256"]
    config = dict(source_arm9_sha256=digest,target_arm9_sha256=digest)
    binding = checked_text(getsource(play.fixture.assign),{
        "request in ({'region': 0}, {'region': 20})":"request in ({'region': 1}, {'region': 4})",
        "struct.pack('<I', 2)":"struct.pack('<I', 38691)",
        "for _ in range(3)]":"for _ in range(9)]",
        "draws == [0, 1, 3]":"draws == [3]*9",
        "'source_RNG_seed': 2":"'source_RNG_seed': 38691",
        "'first_three_original_random4_results'":"'first_nine_original_random4_results'",
    })
    scoped = vars(play.fixture) | {"read":lambda _:config}
    exec(compile(binding,__file__+"::regional-fixture","exec"),scoped)
    FOCUSED.mkdir(exist_ok=True)
    stage_data = SimpleNamespace(ROM=ROM,ROOT=FOCUSED,STORED=PROOF)
    entry = lambda _:play.history(0)
    fixture = lambda n:lambda arm,raw,enabled:scoped["assign"](arm,raw,{"region":n})
    replay = FunctionType(play.main.__code__,play.main.__globals__ | dict(
        stage=stage_data,FRAMES=FRAMES,history=entry,region_fixture=fixture))
    replay(str(region))


if __name__=="__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action",choices=("stage","patch","startup","1","4"))
    action = cli.parse_args().action
    if action=="stage":
        stage()
    elif action in ("1","4"):
        focus(int(action))
    else:
        inherited = getattr(precedent,action)
        FunctionType(inherited.__code__,inherited.__globals__ | globals())()
