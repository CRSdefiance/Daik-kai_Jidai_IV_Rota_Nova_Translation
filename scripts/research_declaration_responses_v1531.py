"""Correct1530's DMA label and execute all eight original actor speech pipelines."""
from pathlib import Path
from copy import deepcopy
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.retreat_transfer_editorial import current_entries
from scripts.probe_battle_aftermath_fonts_v1256 import consumer
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/declaration_responses_context_v1531')
SOURCE = Path('work/analysis/declaration_responses_source_v1530/original_NPC_declaration_response_packet.json')

if __name__ == '__main__':
    assert not ROOT.exists()
    original_packet = read(SOURCE)
    rom = NdsImage.open(original_packet['candidate'])
    assert sha(Path(original_packet['candidate']).read_bytes()) == original_packet['candidate_sha256']
    arm, common = rom.read_file('/__arm9__.bin'), rom.read_file('/COMMON/MESFILE.DK4')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    entries = current_entries(common, arm)
    snapshot = original_packet['actual2205_reference']['snapshot']
    raw = Path(snapshot['path']).read_bytes()
    assert sha(raw) == snapshot['sha256']
    md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    op = lambda pc: next(md.disasm(clean[pc - 0x02000000:pc - 0x02000000 + 4], pc)).op_str
    assert op(0x0206F024) == 'r1, [pc, #0x94]'
    assert op(0x0206F028) == 'r0, r6' and op(0x0206F02C) == '#0x2053f0c'
    assert arm[0x6EE90:0x6F0C8] == clean[0x6EE90:0x6F0C8]
    assert arm[0x53F0C:0x53F9C] == clean[0x53F0C:0x53F9C]
    assert arm[0xE2838:0xE28C8] == clean[0xE2838:0xE28C8]
    cpu, get = get_machine(arm, raw)
    company = get(0xCB160) + 4 + 4 * 76
    actor = get(0x3CD2C, company)
    assert actor == get(0xCB184) + 4 + 28 * 32 and get(0x7EE08, actor) == 28
    representatives = {}
    for item in original_packet['all207_existing_actor_choices']:
        representatives.setdefault(item['source_voice'], item)
        if item['existing_actor_ID'] == 28:
            representatives[item['source_voice']] = item
    assert set(representatives) == set(range(8))
    probes = []
    for voice, item in sorted(representatives.items()):
        n = item['message_ID']
        assert entries[n].text.count(b'%') == 0
        native = consumer(arm, common, raw, {'patches': []}, 0x53F0C, item['actor_object'], 0x021184E0)
        assert native['parent'] == 0x02053F40 and native['selector_offset'] == 0x274
        assert native['selector'] == 0x021184E0 and native['input_hex'] == entries[n].text.hex()
        probes.append({**item, 'native_pipeline': native, 'current_lines': [s.decode('cp932') for s in bytes.fromhex(native['formatted_hex']).split(b'\n')],
            'no_source_runtime_argument': True, 'CPU_only_file_success_and_UI_construction_boundaries': True})
    context = deepcopy(original_packet)
    context.pop('original_UI_constructor_call')
    context.pop('original_UI_constructor')
    context.update(supersedes=str(SOURCE), supersedes_sha256=sha(SOURCE.read_bytes()),
        source_literal_load=0x0206F024, original_speech_call=0x0206F02C,
        original_entry=0x02053F0C, original_parent=0x02053F40, selector_stack_offset=0x274,
        source_table=0x021184E0, native_argument_count=0,
        original_company4_leader_getter=0x0203CD2C, original_actual_leader_object=actor,
        current_all8_original_actor_pipelines=probes,
        snapshot=snapshot['path'], snapshot_sha256=snapshot['sha256'],
        source_context='After the original unknown/named/ready declaration confirmation accepts new hostilities,the target company leader returned by3CD2C speaks through original6F024/6F02C/53F0C/table021184E0. The eight rows are alternative voices,not a sequence. There are no runtime printf arguments or source speech macros. Original relation/hostility setters follow the speech;normal play then enters battle. The actual company4 leader is James Clifford28,voice4,selected2205.',
        erratum='V1530 incorrectly labelled6F0A4/E2838 as the dialogue constructor. E2838 is the original DMA transfer routine after battle-state setup. The table literal is loaded at6F024 and direct actor speech is called at6F02C. The actual2205/actor28/table evidence and original source bytes are unchanged.',
        prose_native_layout_registered_build_and_revised_gameplay_still_pending=True,
        producer_sha256=sha(Path(__file__).read_bytes()), full_goal_complete=False)
    ROOT.mkdir(parents=True)
    target = ROOT / 'source_and_original_actor_context.json'
    save(target, context)
    ledger_path = Path('translations/editorial_review_current_v1.json')
    ledger = read(ledger_path)
    ledger['next_declaration_response_source_packet'].update(context=str(target), context_sha256=sha(target.read_bytes()),
        status='original-direct-actor-context-mapped;prose-formatting-review-pending',
        DMA_constructor_label_erratum=context['erratum'])
    ledger['research_checkpoints'].append({'id': 'V1531-NPC-declaration-original-actor-context', 'proof': str(target),
        'source_prose_reviews_added': 0, 'completed_entries_added': 0, 'full_goal_complete': False})
    save(ledger_path, ledger)
    Path('docs/declaration_responses_v1531_context.md').write_text(
        '# V1531 original declaration-response context\n\n' + context['erratum'] + '\n\n' + context['source_context'] +
        '\n\nAll8 original actor-selection/loader/printf/macro/formatter probes pass with explicit CPU file-success and UI-construction boundaries. '
        'They do not establish revised gameplay or formatting approval. All207 source actor choices remain exact. '
        'The separate fear/sea table2209-2216 remains outside this eight-message batch. No coverage credit yet.\n', encoding='utf-8')
    print('Corrected original call6F02C/53F0C;8 source actor pipelines and actual company4 leader28/voice4/2205 mapped. No review credit yet.')
