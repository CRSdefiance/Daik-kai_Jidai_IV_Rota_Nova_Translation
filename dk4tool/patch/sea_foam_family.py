"""Repack complete sea-foam dialogue owners and enable guarded portrait wrapping."""

import json
from pathlib import Path

from keystone import KS_ARCH_ARM, KS_MODE_ARM, Ks
from ndspy.code import MainCodeFile

from dk4tool.dialogue.qa import audit_native_common_entry
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from dk4tool.script.common_native_repack import repack_native_records

STUB = 0x01FFCBD8
ACTIVE = 0x01FFCF78
RETURN = 0x01FFCF54
VOICE_GATE = 0x01FFCD98
NUMBER_GATE = 0x01FFCCD0
VOICE_TABLES = (0x02118800, 0x02118820, 0x02118840, 0x02116730)


def transform(common,arm,document):
    validate_natural_dialogue_batch(document)
    assert {r['message_id']for r in document['records']} == set(range(457,481))
    clean = NdsImage.open('work/clean.nds')
    source_common = clean.read_file('/COMMON/MESFILE.DK4')
    source = common_message_entries(source_common,clean.read_file('/__arm9__.bin'))
    blocks = IlnkContainer.parse(source_common).blocks
    encoded,prefixes = {},{}
    for row in document['records']:
        i = row['message_id']
        assert row['source_hex'] == source[i].text.hex()
        assert row['japanese'] == source[i].text.decode('cp932')
        text = row['english'].removesuffix('{PAD}')
        # The editor owns natural words. The COMMON encoder owns the existing
        # control-safe Latin spelling for reserved I/F glyph bytes.
        stored_text = text.replace('I','Ｉ').replace('F','Ｆ')
        raw = stored_text.encode('cp932')
        audit = audit_native_common_entry(b' '*len(raw),stored_text+'{PAD}')
        assert not [v for v in audit['issues']if v['severity']in('warning','error')],(i,audit['issues'])
        encoded[i] = raw
        owner = source[i].block,source[i].record_index
        first = next(e for e in source if(e.block,e.record_index)==owner)
        prefixes[owner] = blocks[owner[0]].split(b'\0')[owner[1]][:first.start]
    result = repack_native_records(common,arm,encoded,prefixes)
    code = MainCodeFile(result.arm9,0x02000000)
    before = [bytes(s.data)for s in code.sections]
    section = code.sections[4]
    assert section.ramAddress == 0x01FFC000 and len(section.data) == 4096
    ks = Ks(KS_ARCH_ARM,KS_MODE_ARM)
    old_asm = f'sub r3,r3,#800; cmp r3,#1; beq {ACTIVE}; sub r3,r3,#20; b {RETURN}'
    old = bytes(ks.asm(old_asm,STUB)[0])
    at = STUB-section.ramAddress
    assert before[4][at:at+20] == old and before[4][at+20:0xC00] == bytes(20)
    new_asm = f'''sub r3,r3,#448
        sub r3,r3,#9
        cmp r3,#23
        bls {ACTIVE}
        add r3,r3,#448
        add r3,r3,#9
        sub r3,r3,#820
        cmn r3,#19
        beq {ACTIVE}
        b {RETURN}'''
    new = bytes(ks.asm(new_asm,STUB)[0])
    assert len(new) == 40
    section.data[at:at+40] = new
    # Sea events use the original queued actor/voice-table parent, rather than
    # the direct numerical-message parent used by Tavern text. At this parent
    # the table argument is at sp+0x27c. Recognize only the four source tables;
    # leave the original voice selector, actor and expansion arguments intact.
    gate_asm = f'''ldr ip, table_parent
        cmp r3,ip
        beq crew_table
        ldr ip, captain_parent
        cmp r3,ip
        bne {NUMBER_GATE}
        ldr r3,[sp,#0x270]
        b captain_compare
    crew_table:
        ldr r3,[sp,#0x27c]
        ldr ip, crew_tables
        sub r3,r3,ip
        cmp r3,#0
        cmpne r3,#32
        cmpne r3,#64
        beq {ACTIVE}
        ldr r3,[sp,#0x27c]
    captain_compare:
        ldr ip, captain_table
        cmp r3,ip
        beq {ACTIVE}
        b 0x01ffcff8
    table_parent: .word 0x02053db8
    captain_parent: .word 0x02053c14
    crew_tables: .word 0x02118800
    captain_table: .word 0x02116730'''
    number_asm = f'''
        ldr ip, number_parent
        cmp r3,ip
        bne 0x01ffcff8
        ldr r3,[sp,#0x270]
        sub r3,r3,#448
        sub r3,r3,#9
        cmp r3,#23
        bls {ACTIVE}
        b 0x01ffcff8
    number_parent: .word 0x02053c5c'''
    gate = bytes(ks.asm(gate_asm,VOICE_GATE)[0])
    gate_at = VOICE_GATE-section.ramAddress
    assert len(gate) <= 104 and before[4][gate_at:gate_at+104] == bytes(104)
    branch_at = 0xF48
    old_branch = bytes(ks.asm('bne 0x01ffcff8',0x01ffcf48)[0])
    assert before[4][branch_at:branch_at+4] == old_branch
    section.data[branch_at:branch_at+4] = bytes(ks.asm(f'bne {VOICE_GATE}',0x01ffcf48)[0])
    section.data[gate_at:gate_at+len(gate)] = gate
    number = bytes(ks.asm(number_asm,NUMBER_GATE)[0])
    number_at = NUMBER_GATE-section.ramAddress
    assert len(number) <= 48 and before[4][number_at:number_at+48] == bytes(48)
    section.data[number_at:number_at+len(number)] = number
    target_arm = bytes(code.save())
    parsed = MainCodeFile(target_arm,0x02000000)
    assert all(bytes(parsed.sections[i].data) == before[i]for i in range(4))
    restored = bytearray(parsed.sections[4].data)
    restored[at:at+40] = old+bytes(20)
    restored[branch_at:branch_at+4] = old_branch
    restored[gate_at:gate_at+len(gate)] = bytes(len(gate))
    restored[number_at:number_at+len(number)] = bytes(len(number))
    assert bytes(restored) == before[4]
    after = common_message_entries(result.common,target_arm,clean=False)
    original_entries = common_message_entries(common,arm,clean=False)
    for a,b in zip(original_entries,after):
        assert b.text.rstrip() == encoded.get(a.message_id,a.text).rstrip()
        assert(a.message_id,a.block,a.record_index)==(b.message_id,b.block,b.record_index)
    return result.common,target_arm,{
        'changed_records':[f'COMMON_MESSAGE_{i}'for i in encoded]+['SEA_FOAM_PORTRAIT_WRAP_457_480'],
        'all24_source_entries_and_packed_owners_reviewed':True,
        'changed_native_offsets':sorted(result.changed_offsets),
        'all3668_native_message_identities_preserved':True,
        'native_cache_block_lengths_NUL_counts_and_directory_preserved':True,
        'source_alignment_prefixes_preserved':True,'portrait_parent_return':0x02054014,
        'reserved_literal_I_F_use_existing_control_safe_fullwidth_encoding':True,
        'owned_dispatch_padding_bytes_used':20,'code_or_pool_growth':0,
        'queued_voice_gate_owned_padding_bytes':len(gate),
        'queued_number_gate_owned_padding_bytes':len(number),
        'queued_voice_parent_return':0x02053DB8,'captain_voice_parent_return':0x02053C14,
        'captain_numeric_parent_return':0x02053C5C,
        'original_voice_tables':list(VOICE_TABLES),
        'status':'experimental','full_graphics_goal_complete':False}


def apply_release(common,arm,path):
    config = json.loads(Path(path).read_text(encoding='utf-8'))
    assert config['format'] == 'dk4-sea-foam-family-v1'
    assert sha(common) == config['source_common_sha256'] and sha(arm) == config['source_arm9_sha256']
    manuscript = Path(config['manuscript'])
    assert sha(manuscript.read_bytes()) == config['manuscript_sha256']
    a,b,report = transform(common,arm,json.loads(manuscript.read_text(encoding='utf-8')))
    assert sha(a) == config['target_common_sha256'] and sha(b) == config['target_arm9_sha256']
    return a,b,report
