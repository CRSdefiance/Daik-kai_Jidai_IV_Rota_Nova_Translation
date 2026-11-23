"""Bind the native COMMON archive readers and the guarded crew role cases."""

from pathlib import Path
from struct import iter_unpack, unpack_from

from ndspy.rom import NintendoDSRom
from dk4tool.patch.common_single_cache_v861 import CACHE_AT, ORIGINAL, SINGLE
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0

from scripts import checkpoint_pending_shared_native_20261115 as inventory
from scripts import checkpoint_shared_selector_ranges_20261115 as prior
from scripts import register_save_location_labels_20261119 as current
from scripts.probe_button_prompt_native import BASE, VIEW, call, machine

base = current.base
OUTPUT = Path("translations/editorial_checkpoints/SharedText_20261110_v1/shared_reader_and_crew_bypasses_20261119_v1.json")
BINDINGS = current.stage.ROOT / "shared_text_current_binding.json"
REGIONS = (0x14186C,0x1435CF)
PATH = b"\\COMMON\\MESFILE.DK4\0"
LITERALS = {0x535D0:0x21435BC,0x535D4:0x2141910,0x535D8:0x214186E,0x5365C:0x214186C}
READS = {0x5353C:0x535D0,0x5356C:0x535D4,0x53584:0x535D8,0x53628:0x5365C}
ROLE_ENTRY = (
    (0x12600,0x1268C,1571,(1885,1886,1887,1888)),
    (0x1278C,0x12818,1361,(1881,1882,1883,1884)),
    (0x12720,0x12770,1571,()),
    (0x128B4,0x12904,1361,()),
)


def references(path):
    rom = NintendoDSRom.fromFile(path)
    lo,hi = (BASE+n for n in REGIONS)
    aligned, filenames = [], []
    for name,address,raw in inventory.components(rom):
        for i,(word,) in enumerate(iter_unpack("<I",raw[:len(raw)&~3])):
            if lo <= word < hi:
                aligned.append((name,address+4*i,word))
        for at in inventory.find(raw.upper(),PATH):
            filenames.append((name,address+at))
    assert aligned == [("ARM9 section 0",BASE+k,v) for k,v in LITERALS.items()]
    assert filenames == [("ARM9 section 0",0x21435BC)]
    arm = rom.arm9
    # Identify every aligned PC-relative ARM load of these four literal words.
    uses = {}
    for index,(word,) in enumerate(iter_unpack("<I",arm[:len(arm)&~3])):
        if word & 0x0F7F0000 != 0x051F0000:
            continue
        loc=index*4
        delta=word&0xFFF
        literal=loc+8+(delta if word&0x800000 else -delta)
        if literal in LITERALS:
            uses[loc]=literal
    assert uses == READS
    return dict(aligned_archive_range_pointer_words=aligned,archive_name_locations=filenames,
        archive_range=[lo,hi],literal_readers=[dict(PC=BASE+k,pointer_word=BASE+v,
            exact_opcode=bytes(arm[k:k+4]).hex()) for k,v in uses.items()])


def role_expectation(index,items,first,special):
    if special and 25<=index<=27:
        return special[index-25+bool(items)]
    return first+index


def crew_cases(arm):
    cpu = machine(arm)
    role,seen,table_selects=0,[],[]
    def track(u,pc,size,_):
        if pc==0x0205528C:
            seen.append(u.reg_read(UC_ARM_REG_R0))
            u.reg_write(UC_ARM_REG_R0,VIEW)
        elif pc in (0x02053C6C,0x02053F4C):
            table_selects.append(pc)
            u.emu_stop()
            return
        elif pc==0x02081F54:
            u.reg_write(UC_ARM_REG_R0,role)
        elif pc in (0x020CB1A8,0x020CB190):
            u.reg_write(UC_ARM_REG_R0,VIEW)
        else:
            return
        u.reg_write(UC_ARM_REG_PC,u.reg_read(UC_ARM_REG_LR))
    cpu.hook_add(UC_HOOK_CODE,track)
    results=[]
    for entry,site,first,special in ROLE_ENTRY:
        for role in (12,16,24):
            keys=set()
            count=0
            for index in range(207):
                for flags in ((0,4) if index==27 else (0,)):
                    cpu.mem_write(VIEW+0x1A5,bytes([flags]))
                    seen.clear()
                    call(cpu,entry,(index,))
                    expected=[] if role==24 else [role_expectation(index,flags,first,special)]
                    assert seen==expected and not table_selects,(entry,role,index,flags,seen,expected)
                    if role==24:
                        assert cpu.reg_read(UC_ARM_REG_R0)==0
                    else:
                        assert cpu.reg_read(UC_ARM_REG_R0)==VIEW
                    keys.update(seen)
                    count+=1
            results.append(dict(full_selector_entry=BASE+entry,role_table_lookup_site=BASE+site,
                supplied_role_from_original_role_getter=role,exact_actor_id_domain=[0,206],
                both_item_states_for_actor_27=True,cases=count,table_selector_executed=False,
                request_keys=sorted(keys),result="no text request" if role==24 else "actor-index message"))
    return results


def main():
    assert not OUTPUT.exists()
    release = base.load(current.RELEASE)
    current_binding = base.load(BINDINGS)
    assert base.digest(current.ROM)==current_binding["candidate_sha256"]==release["candidate_sha256"]
    assert base.digest(base.REGISTRY)==release["registry_sha256"]
    assert base.digest(current.stage.CLEAN)==release["clean_input_sha256"]
    en,ja=(base.NdsImage.open(p).read_file(current.stage.ARM) for p in (current.ROM,current.stage.CLEAN))
    prior_records = base.load(prior.OUTPUT)["crew_role_tables"]
    assert {row["call_site"] for row in prior_records}=={BASE+site for _,site,_,_ in ROLE_ENTRY}
    clean_refs,current_refs = map(references,(current.stage.CLEAN,current.ROM))
    assert clean_refs==current_refs
    for lo,hi in ((0x534F4,0x535E0),(0x53628,0x53660),(0x5528C,0x552A4),(0x12600,0x12920)):
        assert en[lo:hi]==ja[lo:hi]
    assert ja[CACHE_AT:CACHE_AT+8]==ORIGINAL and en[CACHE_AT:CACHE_AT+8]==SINGLE
    clean_crew,current_crew=map(crew_cases,(ja,en))
    assert clean_crew==current_crew and len(current_crew)==12
    keys={n for row in current_crew for n in row["request_keys"]}
    pending={r["message_ID"] for r in current_binding["records"]}
    assert len(pending)==276 and not keys.intersection(pending)
    still_open=[]
    for r in prior_records:
        nulls=set(r["null_roles"])
        assert {12,16} <= nulls
        still_open.append(dict(table_call_site=r["call_site"],original_null_roles=sorted(nulls),
            bypasses_verified=[12,16],remaining_null_inputs=sorted(nulls-{12,16})))
    assert sum(len(r["remaining_null_inputs"]) for r in still_open)==14

    base.save(OUTPUT,dict(candidate_sha256=release["candidate_sha256"],clean_sha256=release["clean_input_sha256"],
        bounded_filename_and_literal_ownership=current_refs,
        original_getter_copier_and_block_selector_match_clean=True, accepted_single_cache_entry=SINGLE.hex(),offline_crew_cases=current_crew,
        total_clean_and_current_actor_cases=2*sum(r["cases"] for r in current_crew),
        remainder=still_open,pending_checked_against_outputs=len(pending),pending_key_hits=[],
        display_owners_newly_proven=0,gameplay_runs=0,hardware=False,
        scope="Aligned exact archive literals and verified role-12, role-16 and unassigned inputs. Indirect or computed archive routes remain outside this check.",
        full_goal_complete=False,new_editorial_credit=0,
        evidence={str(p):base.digest(p) for p in (BINDINGS,prior.OUTPUT,current.RELEASE,Path(__file__))}))
    print("Closed eight null-role branches and four unassigned guards. No pending COMMON keys were selected.")


if __name__=="__main__":
    main()

