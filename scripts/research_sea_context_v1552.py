"""Bind the special inspection branch to original creature/ghost classes and role7."""
import struct
from copy import deepcopy
from pathlib import Path
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read, save

SOURCE = Path('work/analysis/sea_responses_source_v1551/original_fear_awe_source_packet.json')
ROOT = Path('work/analysis/sea_responses_context_v1552')
BASE = 0x02000000

if __name__ == '__main__':
    assert not ROOT.exists()
    packet = read(SOURCE)
    rom, clean = NdsImage.open(packet['candidate']), NdsImage.open('work/clean.nds')
    arm, original = rom.read_file('/__arm9__.bin'), clean.read_file('/__arm9__.bin')
    snapshot = packet['current_CPU_role7_probe']['snapshot']
    raw = Path(snapshot['path']).read_bytes()
    assert sha(raw) == snapshot['sha256']
    cpu, get = get_machine(arm, raw)
    classes, models, world, fleets = [get(f) for f in [0xCB154, 0xCB148, 0xCB19C, 0xCB1A8]]
    source_names = []
    for index, expected in [(34, '化魚'), (35, '大イカ'), (36, 'サメ'), (37, '鯨'), (38, '幽霊船')]:
        field = 0x11C7A8 + index * 56
        offset = struct.unpack_from('<I', original, field)[0] - BASE
        japanese = original[offset:original.index(0, offset)].decode('cp932')
        assert japanese == expected
        obj = classes + 4 + index * 64
        vt = struct.unpack('<I', cpu.mem_read(obj, 4))[0]
        getter = struct.unpack('<I', cpu.mem_read(vt + 4, 4))[0]
        assert getter == BASE + 0x1FD74
        pointer = get(getter - BASE, obj)
        current = bytes(cpu.mem_read(pointer, 64)).split(b'\0')[0]
        source_names.append({'source_class_index': index, 'source_Japanese': japanese, 'source_pointer_field': BASE + field,
            'source_text_hex': original[offset:original.index(0, offset)].hex(), 'original_runtime_class': obj,
            'original_virtual_name_getter': getter, 'current_name_pointer': pointer,
            'current_name_hex': current.hex(), 'current_class_name': current.decode('cp932')})
    special_models = []
    for index, expected_kind in [(149, 34), (150, 35), (151, 36), (152, 37), (153, 38)]:
        obj = models + 4 + index * 140
        vt = struct.unpack('<I', cpu.mem_read(obj, 4))[0]
        name_getter, type_getter = [struct.unpack('<I', cpu.mem_read(vt + o, 4))[0] for o in [4, 8]]
        kind = get(type_getter - BASE, obj)
        assert kind == expected_kind
        pointer = get(name_getter - BASE, obj)
        name = bytes(cpu.mem_read(pointer, 64)).split(b'\0')[0]
        special_models.append({'original_model_index': index, 'object': obj, 'class_index': kind,
            'original_virtual_name_getter': name_getter, 'original_virtual_type_getter': type_getter,
            'stored_name_hex': name.hex(), 'stored_name': name.decode('cp932'),
            'stored_Hull_Crew': [get(0x183A0, obj), get(0x181BC, obj)]})
    mobile_rows = []
    for slot in range(20):
        obj = get(0x55850, world, slot)
        assert obj == world + 4 + slot * 28
        vt = struct.unpack('<I', cpu.mem_read(obj, 4))[0]
        type_getter = struct.unpack('<I', cpu.mem_read(vt + 8, 4))[0]
        kind = get(type_getter - BASE, obj)
        flag = get(0xAB9B8, obj)
        assert bool(flag) == (kind >= 34 and kind != 38)
        mobile_rows.append({'slot': slot, 'object': obj, 'native_type': kind, 'native_AB9B8_flag': flag,
            'source_NULL_type40_is_not_an_active_creature': kind == 40,
            'active': bool(get(0x564C8, obj))})
    fleet_rows = []
    for fleet_id in range(63):
        fleet = fleets + 4 + fleet_id * 132
        for slot in range(5):
            model = get(0x36C94, fleet + 12 + slot * 8)
            found = next((r for r in special_models if r['object'] == model), None)
            if not found:
                continue
            fleet_rows.append({'original_fleet_ID': fleet_id, 'original_company_ID': get(0x35320, fleet),
                'original_town_or_sea': get(0x34674, fleet), 'slot': slot, 'model': model,
                'model_index': found['original_model_index'], 'mobile': get(0x36C70, fleet + 12 + slot * 8),
                'stored_map_point': list(struct.unpack('<2i', cpu.mem_read(fleet + 0x34, 8)))})
    md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    code = []
    for lo, hi in [(0xAB128, 0xAB18C), (0xAB9B8, 0xABA00), (0x55850, 0x55874), (0x6F610, 0x6F680), (0x82478, 0x825E4)]:
        assert arm[lo:hi] == original[lo:hi]
        code.append({'span': [BASE + lo, BASE + hi], 'sha256': sha(original[lo:hi]),
            'instructions': [{'address': i.address, 'mnemonic': i.mnemonic, 'operands': i.op_str}
                             for i in md.disasm(original[lo:hi], BASE + lo)]})
    context = deepcopy(packet)
    context.update(supersedes=str(SOURCE), supersedes_sha256=sha(SOURCE.read_bytes()),
        source_class_names=source_names, original_preinitialized_special_models=special_models,
        current_20_mobile_slots=mobile_rows, existing_special_fleet_links=fleet_rows, original_additional_code_spans=code,
        snapshot=snapshot['path'], snapshot_sha256=snapshot['sha256'],
        source_context='The original sea-target inspection parent6F4D4 takes the normal non-combat inspection branch. For a selected live target whose model type is34-37 (Monster Fish,Giant Squid,Shark,Whale) or38 (Ghost Ship),6F66C/6F674 invokes logical role7 through53D44/table021186E0. AB9B8 excludes38 but the following explicit type38 branch includes it. The eight messages are alternative voices reacting to the sight,not a war declaration and not a sequential conversation. They name no species and supply no printf arguments or executable speech macros. Ordinary hostile declaration takes the separate6F70C/6F720 branch. Actual special-target inspection and normal dismissal/return still require gameplay evidence.',
        taxonomy_bound_to_original_class_names_no_species_invention=True,
        census_limits='Only20 source-bounded mobile slots and63 source-bounded fleets. Only five proven initialized special models149-153 are examined;the exploratory model154 and fleet63 probes crossed initialized/source ownership bounds and failed or produced non-fleet data. No bytes were changed and those probes receive no ownership/event credit.',
        broader_label_lead='Class38 current Ghost corresponds to Japanese Ghost Ship;review its actual caption context before changing the inherited label. No label edit or approval is made here.',
        no_gameplay_event_or_prose_formatting_completion_credit=True,
        producer_sha256=sha(Path(__file__).read_bytes()), full_goal_complete=False)
    ROOT.mkdir(parents=True)
    target = ROOT / 'source_and_original_inspection_context.json'
    save(target, context)
    ledger_path = Path('translations/editorial_review_current_v1.json')
    ledger = read(ledger_path)
    ledger['next_sea_fear_awe_source_packet'].update(context=str(target), context_sha256=sha(target.read_bytes()),
        status='source-creature-ghost-inspection-role7-context-mapped;prose-formatting-gameplay-pending')
    ledger['research_checkpoints'].append({'id': 'V1552-creature-ghost-inspection-context', 'proof': str(target),
        'source_prose_reviews_added': 0, 'completed_entries_added': 0, 'full_goal_complete': False})
    save(ledger_path, ledger)
    Path('docs/sea_responses_v1552_context.md').write_text('# V1552 creature and ghost inspection context\n\n' + context['source_context'] +
        '\n\nFive original initialized special models149-153 and all five class names are bound through original runtime getters to clean Japanese. '
        'The current save has an inactive Monster Fish link in fleet39,with no live mobile;no special-target encounter is observed. '
        'The current role7 is Charles18/voice0 and selects2209 in CPU-only research. The false war reference is unsupported by both Japanese and this consumer. '
        'A source-bounded live fixture or an ordinary spawn remains to be established;no numeric message injection or earned event credit.\n\n' +
        context['census_limits'] + '\n\n' + context['broader_label_lead'] + '\n', encoding='utf-8')
    print('Creature/ghost classes34-38 and original role7 inspection mapped;five existing models and inactive fleet39 identified;no event/review credit.')
