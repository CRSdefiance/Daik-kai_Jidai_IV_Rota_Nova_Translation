"""Numeric/table/call-site leads for883-907; no caller approval from adjacency."""

import struct
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from capstone.arm import ARM_OP_IMM, ARM_OP_MEM, ARM_REG_PC

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import save

BASE = 0x02000000
ROOT = Path('work/analysis/tavern_recruitment_editorial_v771')
CURRENT = Path('out/all_routes_combined_v770_candidate.nds')


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    clean, now = [NdsImage.open(p).read_file('/__arm9__.bin') for p in ('work/clean.nds', CURRENT)]
    cs = Cs(CS_ARCH_ARM, CS_MODE_ARM); cs.detail = True; cs.skipdata = True
    refs = {n: {'aligned_word_locations': [], 'immediate_instructions': [], 'literal_loads': []} for n in range(883, 908)}
    for at in range(0, 0x170000, 4):
        value = struct.unpack_from('<I', clean, at)[0]
        if value in refs: refs[value]['aligned_word_locations'].append(BASE + at)
    instructions = list(cs.disasm(clean[0x50000:0x70000], BASE + 0x50000))
    for i in instructions:
        if not i.id: continue
        for operand in i.operands:
            if operand.type == ARM_OP_IMM and operand.imm in refs and i.mnemonic not in ('b', 'bl', 'blx'):
                refs[operand.imm]['immediate_instructions'].append({'pc': i.address, 'instruction': i.mnemonic + ' ' + i.op_str})
        if i.mnemonic.startswith('ldr') and len(i.operands) > 1 and i.operands[1].type == ARM_OP_MEM and i.operands[1].mem.base == ARM_REG_PC:
            at = i.address + 8 + i.operands[1].mem.disp
            if BASE <= at < BASE + len(clean) - 4:
                value = struct.unpack_from('<I', clean, at - BASE)[0]
                if value in refs: refs[value]['literal_loads'].append({'pc': i.address, 'field': at, 'instruction': i.mnemonic + ' ' + i.op_str})
    groups = []
    for values in ((883, -1, 884, 885, 886, 887, 888, 889), (890, -1, 891, 892, 893, 894, 895, 896), (897, -1, 898, 899, 900, 901, 902, 903)):
        raw = struct.pack(f'<{len(values)}i', *values)
        start = 0
        while (at := clean.find(raw, start)) >= 0:
            pointer = BASE + at
            links = [BASE + p for p in range(0, 0x170000, 4) if struct.unpack_from('<I', clean, p)[0] == pointer]
            groups.append({'IDs': values, 'address': pointer, 'pointer_fields': links, 'current_table_unchanged': now[at:at + len(raw)] == raw})
            start = at + 1
    addresses = sorted({r['pc'] for row in refs.values() for key in ('immediate_instructions', 'literal_loads') for r in row[key]})
    clips = []
    for at in addresses:
        lo, hi = max(BASE + 0x50000, at - 80), min(BASE + 0x70000, at + 88)
        clips.append({'lead_pc': at, 'lo': lo, 'hi': hi, 'source_current_code_equal': clean[lo - BASE:hi - BASE] == now[lo - BASE:hi - BASE],
            'source_disassembly': [{'pc': i.address, 'instruction': i.mnemonic + ' ' + i.op_str} for i in cs.disasm(clean[lo - BASE:hi - BASE], lo)]})
    save(ROOT / 'caller_leads.json', {'source_ARM9_sha256': sha(clean), 'current_ARM9_sha256': sha(now), 'message_leads': refs,
        'independent_voice_tables': groups, 'code_lead_clips': clips,
        'scope': 'Leads only: numeric occurrence and physical adjacency do not establish a caller or argument contract.',
        'producer_sha256': sha(Path(__file__).read_bytes())})
    print('Voice table leads', groups, flush=True)
    for n, row in refs.items():
        print(n, 'words', [hex(x) for x in row['aligned_word_locations']], 'MOV', row['immediate_instructions'], 'LDR', row['literal_loads'], flush=True)


if __name__ == '__main__': main()
