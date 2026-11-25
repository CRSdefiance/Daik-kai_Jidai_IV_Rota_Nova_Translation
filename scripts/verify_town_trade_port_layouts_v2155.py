"""Current native layouts for reviewed town prose and typed/name stress."""
from pathlib import Path
from itertools import product
import inspect
import struct
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.probe_button_prompt_native import BASE
from scripts.probe_shipyard_runtime_v759 import layout as original_layout
from scripts.verify_village_wrap_v608 import read, save
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path('work/analysis/town_trade_port_layouts_v2155')
DOC = Path('translations/town_trade_port_contextual_editorial_manuscript_v1.json')
PLAN = Path('work/analysis/town_trade_port_payload_v2153/native_payload_plan.json')

def number(value):
    return str(value).translate(str.maketrans('0123456789', '０１２３４５６７８９')).encode('cp932')

if __name__ == '__main__':
    assert not ROOT.exists()
    ROOT.mkdir(parents=True)
    doc, plan = read(DOC), read(PLAN)
    arm = Path(plan['target_ARM9']).read_bytes()
    common = Path(plan['target_COMMON']).read_bytes()
    entries = owned_entries(common, arm, plan['directory_sha256'])
    report = read('E:/Rota Nova translations/Generated/work/emulation_v193/promoter_context_live_v2144_V2143/capture_report.json')
    snapshot = next(row for row in report['read_only_pause_RAM_snapshots'] if row['frame'] == 3200)
    raw = Path(snapshot['path']).read_bytes()
    assert sha(raw) == snapshot['sha256']
    cpu, _ = get_machine(arm, raw)
    for patch in plan['metadata_patches']:
        cpu.mem_write(patch['address'], bytes.fromhex(patch['target_hex']))
    products = []
    native, get = get_machine(arm, raw)
    root = get(0xCB124) + 4
    for index in range(124):
        obj = root + 16 * index
        vtable = struct.unpack('<I', native.mem_read(obj, 4))[0]
        getter = struct.unpack('<I', native.mem_read(vtable + 8, 4))[0]
        pointer = get(getter - BASE, obj)
        name = bytes(native.mem_read(pointer, 80)).split(b'\0')[0]
        assert name.isascii() and 0 < len(name) < 40
        products.append(dict(index=index, name=name.decode('ascii'), object=obj, getter=getter))
    previous_names = read('work/analysis/square_context_arguments_v2133/current_native_runtime_name_catalog.json')['products']
    assert [row['name'] for row in products] == [row['name'] for row in previous_names]
    source = inspect.getsource(original_layout)
    environment = dict(original_layout.__globals__)
    environment['YESNO'] = (789, 800, 802, 803, 804, 806, 812, 813, 816, 817, 1246)
    exec(compile(source, __file__, 'exec'), environment)
    layout = environment['layout']
    previous = read('work/analysis/shipyard_editorial_v759/typed_literal_runtime_RESEARCH/native_layout_matrix.json')
    assert previous['count'] == 1124
    yard = {number: [] for number in range(784, 805)}
    for case in previous['cases']:
        yard[case['id']].append(tuple(bytes.fromhex(value) for value in case['values_hex']))
    jobs, modal = [], []
    for row in doc['records']:
        message = row['message_id']
        text = entries[message].text
        if message == 267:
            assert text == row['english'].removesuffix('{PAD}').encode('ascii') and len(text) <= 36
            modal.append(dict(message_ID=message, stored_hex=text.hex(), distinct_modal_display_inheritance_pending=True))
            continue
        if message in yard:
            variants = yard[message]
        elif message in (653, 654, 655, 768, 770):
            variants = [(row['name'].encode(),) for row in products]
        elif message in (767, 769):
            variants = [(a['name'].encode(), b['name'].encode()) for a, b in product(products, products)]
        elif message == 808:
            names = ('Hodram', 'Rafael', 'Lil', 'Maria', 'Camille', 'FALCON', 'ICARUS', 'FIONA', 'FORTUNE', 'FURY',
                     'ABCDEFGHIJKLMNOPQRSTUVW', 'A B C D E F G H I J K L', 'ＡＢＣＤＥＦＧＨＩ')
            variants = [(name.encode('cp932'),) for name in names]
        elif message in (1245, 1246):
            variants = [(number(value),) for value in (0, 1, 2, 9, 1000, 21400, 2147483647)]
        else:
            variants = [()]
        assert variants
        jobs.extend((message, text, values) for values in variants)
    results, findings, samples, shapes = [], [], [], set()
    for index, (message, text, values) in enumerate(jobs):
        result = layout(cpu, text, message, values)
        assert not any(flag in result['findings'] for flag in ('four_row_whole_word_bound', 'singular_quantity_grammar')), (message, values, result)
        result.update(index=index, message_ID=message, template_hex=text.hex(), source_parent_and_literal_name_path_not_forced=True)
        results.append(result)
        if result['findings']:
            findings.append(dict(index=index, message_ID=message, values_hex=result['values_hex'], lines=result['lines'], findings=result['findings']))
        name = values[0].hex() if message in (803, 804, 808) else None
        shape = (message, len(result['lines']), tuple(len(line.encode('cp932')) % 2 for line in result['lines']),
                 any(any(byte >= 128 for byte in value) for value in values), name)
        if shape not in shapes:
            shapes.add(shape)
            samples.append(index)
        if index % 5000 == 0:
            print(dict(layout_index=index, total=len(jobs)), flush=True)
    assert {row['message_ID'] for row in results} == set(plan['selected_IDs']) - {267}
    save(ROOT / 'all_native_typed_product_name_layouts.json', dict(
        ARM9_sha256=sha(arm), COMMON_sha256=sha(common), source_snapshot=snapshot,
        manuscript=str(DOC), manuscript_sha256=sha(DOC.read_bytes()),
        payload_plan=str(PLAN), payload_plan_sha256=sha(PLAN.read_bytes()), products=products,
        cases=results, total=len(results), retained_Yard_case_inputs=1124,
        all_ordered124_product_pair_stress_for767_and769=True,
        product_pair_stress_not_eligibility_or_earned_visit_claim=True,
        all_product_names_source_native_getters_exact_to_previous_catalog=True,
        all_source_argument_orders_full_printf_and_output_guards_native_ABI_pass=True,
        all_layouts_at_most4rows35cells_complete=True, style_findings=findings,
        representative_full_font_case_indices=samples, distinct_modal_267=modal,
        formatting_and_full_font_gates_not_approved_here=True, physical_and_production_font_samples_pending=True,
        effective_layout_driver_sha256=sha(source.encode()), producer_sha256=sha(Path(__file__).read_bytes()), full_goal_complete=False))
    print(dict(cases=len(results), full_font_samples=len(samples), style_findings=len(findings), modal267_pending=True), flush=True)
