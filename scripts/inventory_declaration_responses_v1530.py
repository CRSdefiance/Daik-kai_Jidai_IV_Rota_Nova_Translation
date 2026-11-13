"""Next source packet: eight original NPC war responses, not the following fear table."""
import struct
from copy import deepcopy
from dataclasses import asdict
from pathlib import Path
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from dk4tool.patch.retreat_transfer_editorial import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/declaration_responses_source_v1530')
ROM = Path('out/all_routes_combined_v1520_candidate.nds')
BASE, TABLE, FEAR_TABLE = 0x02000000, 0x021184E0, 0x021186E0
IDS = list(range(2201, 2209))

if __name__ == '__main__':
    assert not ROOT.exists()
    clean, rom = NdsImage.open('work/clean.nds'), NdsImage.open(ROM)
    original, arm = clean.read_file('/__arm9__.bin'), rom.read_file('/__arm9__.bin')
    common = rom.read_file('/COMMON/MESFILE.DK4')
    jp = common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'), original)
    en = current_entries(common, arm)
    ledger_path = Path('translations/editorial_review_current_v1.json')
    ledger = read(ledger_path)
    before = deepcopy(ledger)
    done = {n for f in ledger['completed_editorial_families'] for n in f.get('native_message_IDs', [])}
    assert not set(IDS) & (done | set(ledger['reviewed_but_incomplete_COMMON_IDs']))
    assert list(struct.unpack_from('<8i', original, TABLE - BASE)) == IDS
    assert list(struct.unpack_from('<8i', original, FEAR_TABLE - BASE)) == list(range(2209, 2217))
    assert arm[TABLE - BASE:TABLE - BASE + 32] == original[TABLE - BASE:TABLE - BASE + 32]
    assert arm[FEAR_TABLE - BASE:FEAR_TABLE - BASE + 32] == original[FEAR_TABLE - BASE:FEAR_TABLE - BASE + 32]
    md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    code = []
    for lo, hi in [(0x6EE00, 0x6F0C4), (0x6F600, 0x6F7A4), (0x53F4C, 0x53F9C), (0x7E988, 0x7E9A0)]:
        assert original[lo:hi] == arm[lo:hi]
        code.append({'span': [BASE + lo, BASE + hi], 'sha256': sha(original[lo:hi]),
            'instructions': [{'address': i.address, 'mnemonic': i.mnemonic, 'operands': i.op_str}
                             for i in md.disasm(original[lo:hi], BASE + lo)]})
    literal_references = []
    for table, literal in [(TABLE, 0x0206F0C0), (FEAR_TABLE, 0x0206F7A0)]:
        assert struct.unpack_from('<I', original, literal - BASE)[0] == table
        loads = []
        for at in range(0, 0x110000, 4):
            word = struct.unpack_from('<I', original, at)[0]
            if word & 0x0F7F0000 != 0x051F0000:
                continue
            target = BASE + at + 8 + ((word & 0xFFF) if word & 0x00800000 else -(word & 0xFFF))
            if target == literal:
                instruction = next(md.disasm(original[at:at + 4], BASE + at))
                loads.append({'pc': BASE + at, 'mnemonic': instruction.mnemonic, 'operands': instruction.op_str})
        assert loads
        literal_references.append({'table': table, 'literal': literal, 'original_literal_loads': loads})
    assert next(md.disasm(original[0x6F0A4:0x6F0A8], 0x0206F0A4)).op_str == '#0x20e2838'
    actual_path = Path('work/analysis/retreat_transfer_control_verified_v1525/actual_declaration_defeat_and_transfer_return.json')
    actual = read(actual_path)
    report_path = Path(actual['terminal_report'])
    report = read(report_path)
    assert sha(report_path.read_bytes()) == actual['terminal_report_sha256']
    assert report['ROM_sha256'] == sha(ROM.read_bytes()) and report['frames'] == 9200
    snapshot = next(r for r in report['read_only_pause_RAM_snapshots'] if r['frame'] == 6150)
    raw = Path(snapshot['path']).read_bytes()
    assert sha(raw) == snapshot['sha256']
    cpu, get = get_machine(arm, raw)
    actors, captain = get(0xCB184), get(0x7F244)
    actor = actors + 4 + 28 * 32
    assert get(0x7EE08, actor) == 28 and get(0x7E988, actor) == 4 and get(0x53F4C, actor, TABLE) == 2205
    owner = struct.unpack_from('<I', arm, 0x552A0)[0] - BASE
    template = raw[owner + 0x2030:owner + 0x2230].split(b'\0')[0]
    assert template == en[2205].text
    choices = []
    for identity in range(207):
        obj = actors + 0x19E4 if identity == captain else actors + 4 + 32 * identity
        assert get(0x7EE08, obj) == identity
        voice, number = get(0x7E988, obj), get(0x53F4C, obj, TABLE)
        assert number == IDS[voice]
        choices.append({'existing_actor_ID': identity, 'actor_object': obj, 'source_voice': voice, 'message_ID': number})
    records = []
    for n in range(2197, 2217):
        records.append({'message_id': n, 'selected_war_response': n in IDS,
            'separate_fear_or_sea_phenomenon_table_not_a_war_response': n >= 2209,
            'source_reference': {k: v for k, v in asdict(jp[n]).items() if k != 'text'},
            'source_hex': jp[n].text.hex(), 'source_Japanese': jp[n].text.decode('cp932'),
            'current_reference': {k: v for k, v in asdict(en[n]).items() if k != 'text'},
            'current_text_hex': en[n].text.hex(), 'current_English': en[n].text.decode('cp932')})
    ROOT.mkdir(parents=True)
    packet = ROOT / 'original_NPC_declaration_response_packet.json'
    save(packet, {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
        'clean_ROM_sha256': sha(Path('work/clean.nds').read_bytes()), 'ARM9_sha256': sha(arm), 'COMMON_sha256': sha(common),
        'native_message_IDs_selected': IDS, 'source_voice_table': TABLE, 'source_signed_voice_members': IDS,
        'source_literal': 0x0206F0C0, 'original_UI_constructor_call': 0x0206F0A4, 'original_UI_constructor': 0x020E2838,
        'literal_references': literal_references, 'source_code_spans': code, 'all207_existing_actor_choices': choices,
        'actual2205_reference': {'snapshot': snapshot, 'actual_event_audit': str(actual_path),
            'actual_event_audit_sha256': sha(actual_path.read_bytes()), 'existing_actor_ID': 28, 'source_voice': 4,
            'native_selected_message_ID': 2205, 'resident_template_hex': template.hex(),
            'normal_unknown_faction_Yes_response_and_following_original_battle_verified': True},
        'records_and_neighbors': records,
        'findings_to_review': [
            '2202 current English omits the original interception-preparation instruction.',
            '2203 current crushing threat is stronger than the source determination not to lose.',
            '2205 actual James Clifford reaction omits the source challenge and boast; review the complete source voice.',
            '2206 and2207 use fullwidth Latin I; map this UI consumer before ordinary ASCII/macro/wrap changes.',
            '2209 belongs to separate table021186E0,not war table021184E0;source does not mention war but current English adds it. Investigate the original second-table consumer before correction.'
        ],
        'remaining_gates': 'Complete original UI actor selection/printf/macro/wrap context,faithful prose review,native fonts/visuals,registered build and revised original event. No source/prose or completion credit yet.',
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    ledger['next_declaration_response_source_packet'] = {'packet': str(packet), 'sha256': sha(packet.read_bytes()),
        'native_message_IDs': IDS, 'status': 'source-inventory-actual2205-bound;consumer-prose-formatting-review-pending',
        'source_prose_reviews_added': 0, 'completed_entries_added': 0}
    ledger['research_checkpoints'].append({'id': 'V1530-NPC-declaration-response8-source-packet', 'proof': str(packet),
        'source_prose_reviews_added': 0, 'completed_entries_added': 0, 'full_goal_complete': False})
    for key in ['records_editorially_completed', 'records_revised_and_integrated', 'records_with_source_and_prose_pass',
        'reviewed_but_incomplete_COMMON_IDs', 'current_native_relocation_reference', 'current_integrated_candidate',
        'source_pins', 'unresolved_graphics_work', 'older_record_reaudit_after_full_editorial_goal']:
        assert ledger[key] == before[key], key
    save(ledger_path, ledger)
    Path('docs/declaration_responses_v1530_source_packet.md').write_text(
        '# V1530 next NPC declaration-response packet\n\n'
        'Eight original voice alternatives2201-2208 belong to table021184E0 and the original6F0A4/E2838 UI constructor. '
        'All207 existing actor selections pass. Actual V1520 frame6150 binds James Clifford28/voice4/2205 to the resident template '
        'and normal unknown-faction declaration/battle sequence. Prose and original UI macro/wrap behavior are not approved yet.\n\n'
        'The following2209-2216 table is separate (021186E0).2209 Japanese expresses fear about returning alive;current English adds war. '
        'Do not merge it into the eight war responses. Its original UI consumer and surrounding sea-related event remain to be mapped. '
        'Other leads include omitted interception in2202,stronger aggression in2203,shortened2205 and fullwidth I in2206/2207.\n\n'
        'Packet: `' + str(packet) + '`. No coverage/completion credit:1330 complete,1474 source/prose,144 reviewed-incomplete COMMON. '
        'Broader shared/routes/raw prose and separate graphics/all18 plaques remain open. V1520 experimental,V1492 promoted.\n', encoding='utf-8')
    print('Next eight war responses mapped to table/207 actors/actual2205;separate2209 fear-table mistranslation lead retained. No new review credit.')
