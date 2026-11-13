"""Next packet: eight separate fear/awe responses, including a false war reference."""
import struct
from copy import deepcopy
from dataclasses import asdict
from pathlib import Path
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from dk4tool.patch.declaration_responses_editorial import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.probe_battle_aftermath_fonts_v1256 import consumer
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/sea_responses_source_v1551')
ROM = Path('out/all_routes_combined_v1542_candidate.nds')
BASE, TABLE = 0x02000000, 0x021186E0
IDS = list(range(2209, 2217))

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
    completed = {n for f in ledger['completed_editorial_families'] for n in f.get('native_message_IDs', [])}
    assert not set(IDS) & (completed | set(ledger['reviewed_but_incomplete_COMMON_IDs']))
    assert list(struct.unpack_from('<8i', original, TABLE - BASE)) == IDS
    assert original[TABLE - BASE:TABLE - BASE + 32] == arm[TABLE - BASE:TABLE - BASE + 32]
    md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    op = lambda pc: next(md.disasm(original[pc - BASE:pc - BASE + 4], pc)).op_str
    assert op(0x0206F66C) == 'r1, [pc, #0x12c]'
    assert op(0x0206F670) == 'r0, #7' and op(0x0206F674) == '#0x2053d44'
    assert struct.unpack_from('<I', original, 0x6F7A0)[0] == TABLE
    code = []
    for lo, hi in [(0x6F4D4, 0x6F7A4), (0xAB9B8, 0xAB9D0), (0x53D44, 0x53DCC), (0x53F4C, 0x53F9C)]:
        assert original[lo:hi] == arm[lo:hi]
        code.append({'span': [BASE + lo, BASE + hi], 'sha256': sha(original[lo:hi]),
            'instructions': [{'address': i.address, 'mnemonic': i.mnemonic, 'operands': i.op_str}
                             for i in md.disasm(original[lo:hi], BASE + lo)]})
    actual_path = Path('work/analysis/declaration_responses_control_verified_v1547/actual_declaration_defeat_and_transfer_return.json')
    actual = read(actual_path)
    report = read(actual['terminal_report'])
    assert sha(Path(actual['terminal_report']).read_bytes()) == actual['terminal_report_sha256']
    assert report['ROM_sha256'] == sha(ROM.read_bytes())
    snapshot = next(r for r in report['read_only_pause_RAM_snapshots'] if r['frame'] == 6150)
    raw = Path(snapshot['path']).read_bytes()
    assert sha(raw) == snapshot['sha256']
    cpu, get = get_machine(arm, raw)
    actors, captain = get(0xCB184), get(0x7F244)
    duty = get(0xCB1A8) + 0x2090
    identity = get(0x82478, duty, 7)
    actor = actors + 0x19E4 if identity == captain else actors + 4 + 32 * identity
    assert get(0x7EE08, actor) == identity
    voice, number = get(0x7E988, actor), get(0x53F4C, actor, TABLE)
    assert number == IDS[voice]
    native = consumer(arm, common, raw, {'patches': []}, 0x53D44, 7, TABLE)
    assert native['parent'] == 0x02053DB8 and native['selector_offset'] == 0x27C
    assert native['input_hex'] == en[number].text.hex()
    choices = []
    for actor_id in range(207):
        obj = actors + 0x19E4 if actor_id == captain else actors + 4 + 32 * actor_id
        assert get(0x7EE08, obj) == actor_id
        v, n = get(0x7E988, obj), get(0x53F4C, obj, TABLE)
        assert n == IDS[v]
        choices.append({'existing_actor_ID': actor_id, 'actor_object': obj, 'source_voice': v, 'message_ID': n})
    records = []
    for n in range(2206, 2220):
        records.append({'message_id': n, 'selected_separate_fear_awe_response': n in IDS,
            'source_reference': {k: v for k, v in asdict(jp[n]).items() if k != 'text'},
            'source_hex': jp[n].text.hex(), 'source_Japanese': jp[n].text.decode('cp932'),
            'current_reference': {k: v for k, v in asdict(en[n]).items() if k != 'text'},
            'current_text_hex': en[n].text.hex(), 'current_English': en[n].text.decode('cp932')})
    ROOT.mkdir(parents=True)
    packet = ROOT / 'original_fear_awe_source_packet.json'
    save(packet, {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
        'clean_ROM_sha256': sha(Path('work/clean.nds').read_bytes()), 'ARM9_sha256': sha(arm), 'COMMON_sha256': sha(common),
        'native_message_IDs_selected': IDS, 'source_table': TABLE, 'source_signed_voice_members': IDS,
        'source_literal': 0x0206F7A0, 'source_literal_load': 0x0206F66C, 'original_speech_call': 0x0206F674,
        'original_entry': 0x02053D44, 'original_parent': 0x02053DB8, 'selector_stack_offset': 0x27C, 'original_role': 7,
        'source_code_spans': code, 'all207_existing_actor_choices': choices,
        'current_CPU_role7_probe': {'snapshot': snapshot, 'selected_existing_actor_ID': identity, 'selected_voice': voice,
            'selected_ID': number, 'native_pipeline': native, 'CPU_only_not_an_observed_fear_awe_gameplay_event': True},
        'source_branch_context': 'Original6F610 target branch callsAB9B8;nonzero result or original virtual target type0x26 selects6F66C/table021186E0/logical role7. The eight responses express fear or awe at something seen at sea. This is a different caller/table from NPC declaration responses2201-2208. Exact target flag/type ownership and an ordinary special-target event still need source/gameplay mapping;do not infer a particular creature species or inject a numeric message.',
        'findings_to_review': [
            '2209 adds W-we are at war although clean Japanese only expresses panic and asks whether the speakers can return alive.',
            '2210 and2211 are clipped fragments;review the complete source surprise and unprecedented sight.',
            '2212 asks how such a thing can be in the sea,not simply that it lives there.',
            '2215 current So scary is a fragment;retain the frightened cry in natural spoken English.',
            'Preserve2213 monster reaction,2214 doubt about beating the thing,and2216 sea-mystery sense without inventing a species,outcome or battle declaration.'
        ], 'records_and_neighbors': records, 'source_context_prose_formatting_registered_release_and_original_event_still_pending': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    ledger['next_sea_fear_awe_source_packet'] = {'packet': str(packet), 'sha256': sha(packet.read_bytes()), 'native_message_IDs': IDS,
        'status': 'source-inventory-role7-consumer-mapped;target-branch-prose-formatting-original-event-pending',
        'source_prose_reviews_added': 0, 'completed_entries_added': 0}
    ledger['research_checkpoints'].append({'id': 'V1551-separate-sea-fear-awe8-source-packet', 'proof': str(packet),
        'source_prose_reviews_added': 0, 'completed_entries_added': 0, 'full_goal_complete': False})
    for k in ['records_editorially_completed', 'records_revised_and_integrated', 'records_with_source_and_prose_pass',
        'reviewed_but_incomplete_COMMON_IDs', 'current_native_relocation_reference', 'current_integrated_candidate',
        'source_pins', 'unresolved_graphics_work', 'older_record_reaudit_after_full_editorial_goal']:
        assert ledger[k] == before[k], k
    save(ledger_path, ledger)
    Path('docs/sea_responses_v1551_source_packet.md').write_text('# V1551 separate sea fear/awe packet\n\n'
        'Eight alternatives2209-2216 belong to table021186E0 and original6F66C/6F674/53D44/logical role7,parent53DB8/SP27C. '
        'All207 original actor choices and a CPU-only current role7 selection/loader/printf/macro/formatter probe pass. The snapshot is from the audited declaration run; '
        'it does not show this special-target event. Original branch ownership/target type,complete context/prose/native layout/registered integration and original gameplay remain pending.\n\n'
        '2209 incorrectly adds war to a Japanese expression of panic and fear about returning alive. Other lines express sea-related awe,surprise,monster imagery and doubt about winning. '
        'Do not merge these into the now-complete NPC war responses or invent a specific creature species. No new source/prose or completion credit. '
        'Counts1338 complete,1482 source/prose,144 reviewed-incomplete COMMON;full editorial/graphics goals active. Packet: `' + str(packet) + '`.\n', encoding='utf-8')
    print('Next fear/awe8 source packet:original role7 caller/207 actor choices mapped;false-war lead retained;no gameplay or review credit.')
