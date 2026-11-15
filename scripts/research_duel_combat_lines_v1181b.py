"""Source inventory for30 combat barks/special lines; no prose approvals."""
from dataclasses import asdict
from pathlib import Path
import struct
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from dk4tool.patch.duel_editorial import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/duel_combat_source_v1181b')
IDS = (*range(1957, 1973), *range(1980, 1994))
BASE = 0x02000000


def main():
    assert not ROOT.exists()
    source_path, current_path = Path('work/clean.nds'), Path('out/all_routes_combined_v1166_candidate.nds')
    source, current = NdsImage.open(source_path), NdsImage.open(current_path)
    assert sha(source_path.read_bytes()) == 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    assert sha(current_path.read_bytes()) == '19109464a37c8acfe7ccf802fed712cc0bd413600b304546668fb5475801ac26'
    clean, arm = source.read_file('/__arm9__.bin'), current.read_file('/__arm9__.bin')
    jp = common_message_entries(source.read_file('/COMMON/MESFILE.DK4'), clean)
    en = current_entries(current.read_file('/COMMON/MESFILE.DK4'), arm)
    records = []
    for number in IDS:
        records.append({'message_ID': number,
            'source_reference': {k: v for k, v in asdict(jp[number]).items() if k != 'text'},
            'source_hex': jp[number].text.hex(), 'source_Japanese': jp[number].text.decode('cp932'),
            'current_reference': {k: v for k, v in asdict(en[number]).items() if k != 'text'},
            'current_hex': en[number].text.hex(), 'current_English': en[number].text.decode('cp932'),
            'original_string_substitutions': jp[number].text.count(b'%s'),
            'source_context_gloss_localization_and_formatting_review_pending': True})
    catalog_path = Path('work/analysis/duel_scope_names_v1117b/source_name_layout_catalogue.json')
    catalog = read(catalog_path)
    raw = Path(catalog['snapshot']).read_bytes()
    assert sha(raw) == catalog['snapshot_sha256']
    cpu, get = get_machine(arm, raw)
    tables = []
    for family, table, numbers in (('positive_bark', 0x02117560, tuple(range(1957, 1965))),
                                    ('negative_bark', 0x021175C0, tuple(range(1965, 1973)))):
        assert struct.unpack_from('<8i', clean, table-BASE) == numbers
        assert arm[table-BASE:table-BASE+32] == clean[table-BASE:table-BASE+32]
        selections = []
        for actor in catalog['names']:
            voice = get(0x7E988, actor['object'])
            number = get(0x53F4C, actor['object'], table)
            assert number == numbers[voice]
            selections.append({'slot': actor['actor_slot'], 'actor_ID': actor['actor_ID'],
                'voice': voice, 'message_ID': number})
        assert len(selections) == 208 and {r['message_ID'] for r in selections} == set(numbers)
        tables.append({'family': family, 'table': table, 'numbers': list(numbers),
            'all208_source_native_voice_selections': selections,
            'source_aligned_pointer_references': [BASE+i for i in range(0, len(clean)-3, 4)
                if clean[i:i+4] == struct.pack('<I', table)],
            'null_actor_fallback_ID': get(0x53F4C, 0, table)})
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    # Decode each ARM word so literal data cannot stop the source census.
    # These are instruction leads; enclosing-function review remains required.
    code = [instruction for at in range(0xE000,0x10010,4)
            for instruction in decoder.disasm(clean[at:at+4],BASE+at)]
    calls, immediates = [], []
    for index, instruction in enumerate(code):
        if instruction.mnemonic == 'bl' and instruction.op_str in ('#0x200d458', '#0x200d4d0'):
            lo, hi = max(0, index-14), min(len(code), index+3)
            calls.append({'address': instruction.address, 'target': int(instruction.op_str[1:], 16),
                'source_instructions': [f'{i.address:08X} {i.mnemonic} {i.op_str}' for i in code[lo:hi]]})
        if instruction.mnemonic in ('mov', 'movs') and instruction.op_str.startswith('r3, #'):
            value = int(instruction.op_str.split('#')[1], 0)
            if value in IDS:
                immediates.append({'instruction': instruction.address, 'message_ID': value})
    special_refs = [{'message_ID': n, 'aligned_value_references_are_leads_not_proven_callers':
        [BASE+i for i in range(0, len(clean)-3, 4) if clean[i:i+4] == struct.pack('<I', n)]}
        for n in range(1980, 1994)]
    assert arm[0xD458:0xD540] == clean[0xD458:0xD540]
    assert arm[0xE8CC:0x10010] == clean[0xE8CC:0x10010]
    ROOT.mkdir(parents=True)
    proof = ROOT/'source_context_inventory.json'
    save(proof, {'candidate': str(current_path), 'candidate_sha256': sha(current_path.read_bytes()),
        'clean_ROM_sha256': sha(source_path.read_bytes()), 'records': records, 'voice_tables': tables,
        'all416_original_source_voice_selections': True,
        'native_D458_D4D0_call_windows': calls,
        'raw_ARM_word_census_requires_enclosing_function_and_literal_pool_review':True, 'numeric_R3_immediate_leads': immediates,
        'special_move_value_reference_leads': special_refs,
        'source_duel_logic_E8CC_to10010_and_wrappers_exact_in_V1166': True,
        'thirty_lines_are_additional_to_completed20_and_pending13_escape_notices': True,
        'special_technique_speakers_intent_and_ShiraKi_school_name_require_source_context_review': True,
        'native_consumer_scope_layout_new_prose_and_actual_samples_not_approved_by_inventory': True,
        'no_ROM_manuscript_or_completion_credit_change': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print(f'Next30 combat lines inventoried:416 original voice selections,{len(calls)} native call windows; no prose or completion credit.', flush=True)


if __name__ == '__main__':
    main()
