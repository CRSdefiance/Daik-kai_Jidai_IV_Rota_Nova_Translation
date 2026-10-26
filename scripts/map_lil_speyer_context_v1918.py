"""Original Speyer predicate, speaker selectors and macro context on copied RAM."""
import struct
from pathlib import Path
from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import (UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2,
    UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7,
    UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11)
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_call_abi_v764 import call
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_Speyer_context_v1918')
INV = Path('work/analysis/lil_after_London_inventory_v1913/all336_states_and_original_London_town_eligibility.json')
PACKET = Path('work/analysis/lil_followups_after_London_v1914/source_followup_packets_and_random_query_classification.json')
DOC = Path('translations/lil_speyer_encounter_editorial_manuscript_v1.json')
BASE = 0x02000000
SCRATCH = 0x02640000

if __name__ == '__main__':
    assert not ROOT.exists()
    inv, packet, doc = map(read,(INV,PACKET,DOC))
    rom = Path(inv['candidate'])
    image, clean = NdsImage.open(rom), NdsImage.open('work/clean.nds')
    arm, cleanarm = image.read_file('/__arm9__.bin'), clean.read_file('/__arm9__.bin')
    assert sha(arm) == '500b7d6cea559d7252ae4e67f94540e67739428823a17cf26842b6827712a41e'
    assert sha(rom.read_bytes()) == inv['candidate_sha256'] == packet['candidate_sha256']
    spans = [(0x220D8,0x22ECC),(0x23840,0x23A28),(0x24274,0x242C8),
        (0x242CC,0x24310),(0x24314,0x24330),(0x24334,0x243A0),(0x54020,0x54060)]
    assert all(arm[a:b] == cleanarm[a:b] for a,b in spans)
    ev = image.read_file('/data/EV2.DK4')
    assert ev == clean.read_file('/data/EV2.DK4')
    raw = Path(inv['snapshot']).read_bytes()
    assert sha(raw) == inv['snapshot_sha256'] == packet['snapshot_sha256']
    header = raw.find(ev[:96])
    assert header >= 0 and raw.find(ev[:96],header+1) < 0
    owner = BASE+header-0x34
    cpu,get = get_machine(arm,raw)
    fleet = get(0xCB1A8)+4+2*132
    assert get(0x2E58C) == get(0x7F244) == 2
    assert get(0x34674,fleet) == 0
    town = get(0xCB178)+4+5*108
    assert get(0xB5600,town) == 5
    namecpu,nameget = get_machine(arm,raw)
    vt = struct.unpack('<I',namecpu.mem_read(town,4))[0]
    fn = struct.unpack('<I',namecpu.mem_read(vt+8,4))[0]
    nameptr = nameget(fn-BASE,town)
    townname = bytes(namecpu.mem_read(nameptr,100)).split(b'\0')[0].decode('cp932')
    assert townname == 'Hamburg'
    cpu.mem_write(fleet+0x3C,b'\x05')
    cpu.mem_write(owner+0x2454,struct.pack('<3I',7,5,3))
    get(0xCC9A8,SCRATCH+0x80,get(0xCB1B4))
    before = bytes(cpu.mem_read(BASE,0x400000))
    changes = [dict(address=BASE+i,before=a,after=b) for i,(a,b) in enumerate(zip(raw,before,strict=True)) if a!=b]
    allowed = {fleet+0x3C,*range(owner+0x2454,owner+0x2460)}
    assert all(r['address'] in allowed for r in changes)
    trace, writes = [], []
    regs = (UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,
        UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11)
    def observe(c,address,size,data):
        if BASE+0x220D8 <= address < BASE+0x22ECC:
            trace.append(dict(PC=address,word=struct.unpack('<I',c.mem_read(address,4))[0],
                registers=[c.reg_read(r) for r in regs]))
    def write(c,access,address,size,value,data):
        if BASE <= address < BASE+0x400000:
            writes.append(dict(PC=c.reg_read(UC_ARM_REG_PC),address=address,bytes=size,value=value))
    cpu.hook_add(UC_HOOK_CODE,observe)
    cpu.hook_add(UC_HOOK_MEM_WRITE,write)
    result = get(0x220D8,owner,inv['all336_original_events'][128]['actual_native_event_pointer'],SCRATCH+0x80,0)
    after = bytes(cpu.mem_read(BASE,0x400000))
    assert result in (0,1) and after == before and not writes
    # Map each ordinary actor selector and its original macro context. This does
    # not claim a live portrait/nameplate for the new scene.
    actorscpu,query = get_machine(arm,raw)
    actors = query(0xCB184)
    assert bytes(actorscpu.mem_read(BASE,0x400000)) == raw
    catalog = {}
    rows = []
    blocks = IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks
    jap = IlnkContainer.parse(clean.read_file('/data/SC2.DK4')).blocks
    for r in doc['records']:
        prefix = int(r['source_presentation_prefix_hex'],16)
        assert prefix < 0xCF
        cpu,get = get_machine(arm,raw)
        actor_ID = get(0x2434C,prefix)
        assert actor_ID == prefix and bytes(cpu.mem_read(BASE,0x400000)) == raw
        actor = actors+0x19E4 if prefix == 2 else actors+4+prefix*32
        if prefix not in catalog:
            cat,q = get_machine(arm,raw)
            vt = struct.unpack('<I',cat.mem_read(actor,4))[0]
            fn = struct.unpack('<I',cat.mem_read(vt+8,4))[0]
            assert fn == BASE+0x7EDD4
            pointer = q(fn-BASE,actor)
            name = bytes(cat.mem_read(pointer,100)).split(b'\0')[0].decode('cp932')
            changed = bytes(cat.mem_read(BASE,0x400000))
            catalog[prefix] = dict(prefix_hex=f'{prefix:02x}',native_actor_ID=actor_ID,
                native_full_name=name,native_actor_pointer=actor,name_getter=fn,
                name_cache_delta_on_separate_disposable_copy=[dict(address=BASE+i,before=a,after=b)
                    for i,(a,b) in enumerate(zip(raw,changed,strict=True)) if a!=b],
                name_getter_not_claimed_pure=True,actual_scene_portrait_nameplate_unverified=True)
        ja,at = r['source_reference']['offset'],r['current_reference']['offset']
        source,prior = bytes.fromhex(r['source_hex']),bytes.fromhex(r['current_text_hex'])
        assert jap[r['block']][ja:ja+len(source)] == source
        assert blocks[r['block']][at:at+len(prior)] == prior
        assert jap[r['block']][ja-5:ja+1] == blocks[r['block']][at-5:at+1] == bytes.fromhex('0040ffff00')+bytes([prefix])
        cpu.mem_write(0x02660000-16,b'\xa5'*2080)
        cpu.mem_write(0x02660000,prior[1:]+b'\0')
        guarded = bytes(cpu.mem_read(0x02660000-16,2080))
        cpu.mem_write(0x02662000-16,b'\xa5'*4128)
        hook = cpu.hook_add(UC_HOOK_CODE,lambda c,a,z,d:c.reg_write(UC_ARM_REG_PC,0x027E0000),
            begin=BASE+0x242CC,end=BASE+0x242CC)
        try:call(cpu,0x242C8,(0x02662000,0x02660000,actor),instruction_limit=400000)
        finally:cpu.hook_del(hook)
        expanded = bytes(cpu.mem_read(0x02662000,4096)).split(b'\0')[0]
        assert bytes(cpu.mem_read(BASE,0x400000)) == raw
        assert bytes(cpu.mem_read(0x02660000-16,2080)) == guarded
        assert bytes(cpu.mem_read(0x02662000-16,16)) == b'\xa5'*16
        assert bytes(cpu.mem_read(0x02662000+len(expanded)+1,4095-len(expanded))) == b'\xa5'*(4095-len(expanded))
        rows.append(dict(id=r['id'],block=r['block'],source_reference=r['source_reference'],
            current_reference=r['current_reference'],source_complete_preamble_hex=r['source_complete_preamble_hex'],
            prefix_hex=f'{prefix:02x}',native_actor_ID=actor_ID,native_macro_actor_pointer=actor,
            native_macro_English=expanded.decode('cp932'),native_macro_output_hex=expanded.hex(),
            original_macro_entire4MiB_and_input_output_guards_preserved=True))
    ROOT.mkdir(parents=True)
    save(ROOT/'original_Hamburg_predicate_and57_macro_contexts.json',dict(candidate=str(rom),
        candidate_sha256=sha(rom.read_bytes()),ARM9_sha256=sha(arm),EV2_sha256=sha(ev),
        snapshot=inv['snapshot'],snapshot_sha256=sha(raw),source_context=str(PACKET),source_context_sha256=sha(PACKET.read_bytes()),
        manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),
        exact_original_runtime_spans=[dict(start=BASE+a,end_exclusive=BASE+b,sha256=sha(arm[a:b])) for a,b in spans],
        registered_macro_wrappers_not_included_in_claimed_clean_control_spans=True,
        event128=dict(original_event=inv['all336_original_events'][128],native_town_name=townname,
            offline_category_town_subtype=[7,5,3],offline_input_changes=changes,
            full_original_predicate_result=result,all4MiB_unchanged_and_no_write_callbacks=True,
            original_predicate_trace=trace,no_outer_scheduler_or_live_activation_claim=True),
        native_speaker_catalog=catalog,records=rows,new_scene_actual_presentation_and_choices_unverified=True,
        no_ROM_live_RAM_ledger_orcompletion_changes=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(Hamburg_event128_original_predicate=result,offline_input_changed_bytes=len(changes),
        pure_original_query=True,native_actor_names={k:v['native_full_name'] for k,v in catalog.items()},
        complete_source_preambles_and_macro_guards=len(rows),actual_scene_unverified=True))
