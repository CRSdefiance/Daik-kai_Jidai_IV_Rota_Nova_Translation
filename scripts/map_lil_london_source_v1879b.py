"""Source-first complete London B26 exchange, actors and native substitutions."""
import struct
from pathlib import Path
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_PC
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.inventory_lil_lessons_v1717 import inventory
from scripts.native_call_abi_v764 import call
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_London_source_v1879b')
ROM = Path('out/all_routes_combined_v1875_candidate.nds')
CONTEXT = Path('work/analysis/lil_destination_contexts_v1847/source_destinations_and_original_random_query_classification.json')
INV = Path('work/analysis/lil_after_Amsterdam_inventory_v1846/all336_states_and_original_town_eligibility.json')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193/lil_Stockholm_revised_run_v1864_RESEARCH_ONLY')
SNAP = CAP/'frame_062850_arm9_ram.bin'
BASE = 0x02000000

if __name__ == '__main__':
    assert not ROOT.exists()
    context, inv = map(read,(CONTEXT,INV))
    image, clean = NdsImage.open(ROM),NdsImage.open('work/clean.nds')
    arm = image.read_file('/__arm9__.bin')
    assert sha(ROM.read_bytes()) == read(ROM.with_suffix('.manifest.json'))['candidate_sha256']
    old_parent = NdsImage.open('out/all_routes_combined_v1841_candidate.nds')
    assert arm == old_parent.read_file('/__arm9__.bin')
    source = IlnkContainer.parse(clean.read_file('/data/SC2.DK4')).blocks[26]
    current = IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[26]
    assert current == IlnkContainer.parse(old_parent.read_file('/data/SC2.DK4')).blocks[26]
    assert image.read_file('/data/EV2.DK4') == clean.read_file('/data/EV2.DK4')
    old, speeches = inventory(clean.read_file('/__arm9__.bin'),source)
    now, current_speeches = inventory(arm,current)
    assert len(speeches) == len(current_speeches) == 111
    shape = lambda rs:[(r['word'],r['offset'],r['native_extent'],r['ancestor_0100_offsets']) for r in rs]
    assert shape(old) == shape(now)
    raw = SNAP.read_bytes()
    assert len(raw) == 0x400000
    report = read(CAP/'capture_report.json')
    assert report['ROM_sha256'] == sha(ROM.read_bytes())
    assert any(r['frame']==62850 and r['sha256']==sha(raw) for r in report['read_only_pause_RAM_snapshots'])
    cpu,get = get_machine(arm,raw)
    actors = get(0xCB184)
    captain = actors+0x19E4
    assert get(0x7F244) == get(0x2E58C) == 2
    hook = cpu.hook_add(UC_HOOK_CODE,lambda c,a,z,d:c.reg_write(UC_ARM_REG_PC,0x027E0000),begin=BASE+0x242CC,end=BASE+0x242CC)
    rows,speaker_map = [],{}
    try:
        for index,(a,b) in enumerate(zip(speeches,current_speeches,strict=True)):
            at,where = a['offset']+5,b['offset']+5
            original = source[at:source.index(b'\0',at)]
            value = current[where:current.index(b'\0',where)]
            prefix = original[0]
            assert value[0] == prefix
            assert source[at-5:at+1] == current[where-5:where+1] == bytes.fromhex('0040ffff00')+bytes([prefix])
            assert prefix in (2,9,14,16,20,28,0x97,0xfe),('unknown source classification',prefix)
            actor_ID = get(0x2434C,prefix) if prefix < 0x20 else None
            assert actor_ID == prefix if prefix < 0x20 else actor_ID is None
            actor = captain if actor_ID in (2,None) else actors+4+actor_ID*32
            if str(prefix) not in speaker_map and actor_ID is None:
                speaker_map[str(prefix)] = dict(actor_ID=None,native_full_name='Unresolved presentation '+hex(prefix),display_speaker_unverified=True,macro_actor_captain_probe_only=True)
            if str(prefix) not in speaker_map:
                catalog,name_get = get_machine(arm,raw)
                vt = struct.unpack('<I',catalog.mem_read(actor,4))[0]
                name_fn = struct.unpack('<I',catalog.mem_read(vt+8,4))[0]
                assert name_fn == 0x0207EDD4
                pointer = name_get(name_fn-BASE,actor)
                name = bytes(catalog.mem_read(pointer,100)).split(b'\0')[0].decode('cp932')
                catalog_after = bytes(catalog.mem_read(BASE,0x400000))
                delta = [dict(address=BASE+i,before=x,after=y) for i,(x,y) in enumerate(zip(raw,catalog_after,strict=True)) if x!=y]
                speaker_map[str(prefix)] = dict(actor_ID=actor_ID,native_full_name=name,name_getter=name_fn,
                    name_cache_delta_on_separate_disposable_copy=delta,name_getter_not_claimed_pure=True)
            name = speaker_map[str(prefix)]['native_full_name']
            text = value[1:]
            assert len(text) < 2048
            cpu.mem_write(0x02660000-16,b'\xa5'*2080)
            cpu.mem_write(0x02660000,text+b'\0')
            guarded = bytes(cpu.mem_read(0x02660000-16,2080))
            cpu.mem_write(0x02662000-16,b'\xa5'*4128)
            call(cpu,0x242C8,(0x02662000,0x02660000,actor),instruction_limit=400000)
            expanded = bytes(cpu.mem_read(0x02662000,4096)).split(b'\0')[0]
            assert bytes(cpu.mem_read(BASE,0x400000)) == raw
            assert bytes(cpu.mem_read(0x02660000-16,2080)) == guarded
            assert bytes(cpu.mem_read(0x02662000-16,16)) == b'\xa5'*16
            assert bytes(cpu.mem_read(0x02662000+len(expanded)+1,4095-len(expanded))) == b'\xa5'*(4095-len(expanded))
            record = source[:at].count(b'\0')
            rows.append(dict(id=f'DK4_MES_B26_R{record:04d}',file_path='/data/SC2.DK4',block=26,record_index=record,
                source_reference=dict(offset=at,bytes=len(original),header_offset=at-5),
                current_reference=dict(offset=where,bytes=len(value),header_offset=where-5,record_index=current[:where].count(b'\0')),
                source_hex=original.hex(),current_text_hex=value.hex(),
                source_complete_preamble_hex=source[at-5:at+1].hex(),source_presentation_prefix_hex=f'{prefix:02x}',
                source_Japanese=original[1:].decode('cp932'),current_stored_English=value[1:].decode('cp932'),
                current_native_macro_English=expanded.decode('cp932'),current_native_macro_output_hex=expanded.hex(),
                speaker=name,macro_probe_actor_ID=actor_ID,native_command_extent=a['native_extent'],
                ancestor_0100_offsets=a['ancestor_0100_offsets'],spoken_sequence_index=index,
                original_macro_entire4MiB_input_output_guards_and_ABI_preserved=True))
    finally:
        cpu.hook_del(hook)
    for i,row in enumerate(rows):
        row['previous_spoken_ID'] = rows[i-1]['id'] if i else None
        row['next_spoken_ID'] = rows[i+1]['id'] if i+1<len(rows) else None
    ROOT.mkdir(parents=True)
    save(ROOT/'all111_clean_current_native_source_context.json',dict(
        candidate=str(ROM),candidate_sha256=sha(ROM.read_bytes()),source_clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),
        ARM9_sha256=sha(arm),file_path='/data/SC2.DK4',block=26,clean_block_sha256=sha(source),current_block_sha256=sha(current),
        clean_block_bytes=len(source),current_block_bytes=len(current),all_clean_native_commands=old,
        all_current_native_commands=now,all_command_offsets_extents_nested_ancestors_and_complete_headers_match=True,
        records=rows,native_speaker_catalog=speaker_map,source_event26=inv['all336_original_events'][26],
        offline_original_London_context=next(r for r in context['original_source_destination_cases'] if r['event_ID']==26),
        source_context_proof=str(CONTEXT),source_context_proof_sha256=sha(CONTEXT.read_bytes()),
        exact_B26_and_runtime_inherit_prior_offline_context_not_current_live_eligibility_claim=True,
        macro_snapshot=str(SNAP),macro_snapshot_sha256=sha(raw),
        actual_London_activation_portraits_display_and_return_unverified=True,
        structural_inventory_not_a_gameplay_claim=True,no_ROM_or_ledger_completion_change=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(commands=len(old),speeches=len(rows),speaker_names={k:v['native_full_name'] for k,v in speaker_map.items()}))

