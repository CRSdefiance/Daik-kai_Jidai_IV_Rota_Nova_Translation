"""Review the hostess town fields and test their original name-panel inputs offline."""

from hashlib import sha256
from pathlib import Path
from struct import pack, unpack, unpack_from

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R5, UC_ARM_REG_SL, UC_ARM_REG_SP

from dk4tool.patch.owned_name_fields_v2 import plan_arm9_name_fields
from scripts import register_square_rumors_20261115 as current
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.preflight_shared_dynamic_notice_wrap_v1 import font_tools
from scripts.probe_button_prompt_native import STACK
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.stage_mutiny_review_v1 import portrait_sheets, render_portrait


base, stage = current.base, current.stage
ROOT = Path('work/barmaid_town_labels_20261115_v1')
REVIEW = Path('translations/editorial_checkpoints/SharedText_20261110_v1/barmaid_town_labels_20261115_v1.json')
DOC = Path('docs/editorial_barmaid_town_labels_20261115.md')
BASE, TABLE = 0x02000000, 0x120B80
GATES = ('source', 'context', 'localization', 'naturalness', 'formatting')
EDIT = {195: ('Nelly', 'Alexandria', 25), 204: ('Verisa', 'Sao Jorge', 29)}
VARIANTS = {200: ('Jakarta', 'Batavia', 'The clean alias says Jakarta. The separate town name says Batavia. Preserve both as authored.'),
            206: ('Bahamas', 'Havana', 'The clean alias names the Bahamas. The ordinary port name is Havana. Preserve the broader label.')}
CALLERS = ((0x151DC, 0x1520C, UC_ARM_REG_SL, 40), (0x153C4, 0x153F4, UC_ARM_REG_R5, 28))
SPANS = ((0x79D8, 0x7A28), (0x151DC, 0x15254), (0x153C4, 0x15470), (0x7EA48, 0x7EB3C), (0x7ED88, 0x7EE20),
         (0x7EE20, 0x7EEB0), (0xCDAB4, 0xCDAC4), (0x148414, 0x148448))


def read_pointer(cpu, at):
    return unpack('<I', bytes(cpu.mem_read(at, 4)))[0]


def read_text(cpu, at):
    return bytes(cpu.mem_read(at, 96)).split(b'\0', 1)[0].decode('cp932')


def read_static(arm, field):
    pointer = unpack_from('<I', arm, field)[0]
    assert BASE <= pointer < BASE + len(arm)
    offset = pointer - BASE
    end = arm.index(0, offset, offset + 40)
    text = arm[offset:end]
    return dict(pointer=pointer, source_ARM9_field_offset=field, offset=offset, hex=text.hex(), text=text.decode('cp932'))


def draw_input(cpu, obj, begin, call, register, capacity):
    observed = []

    def prepare(u, pc, size, _):
        if pc != BASE + 0xD5404:
            return
        pointer = u.reg_read(UC_ARM_REG_R1)
        context = u.reg_read(UC_ARM_REG_R0)
        assert context == u.reg_read(UC_ARM_REG_SP)
        x, y = unpack('<2I', bytes(u.mem_read(context + 0x24, 8)))
        observed.append((pc, pointer, x, y))
        u.emu_stop()

    cpu.mem_write(STACK, bytes(0x48))
    cpu.reg_write(UC_ARM_REG_SP, STACK)
    cpu.reg_write(register, obj)
    handle = cpu.hook_add(UC_HOOK_CODE, prepare, begin=BASE + 0xD5404, end=BASE + 0xD5404)
    try:
        cpu.emu_start(BASE + begin, BASE + call + 4, count=10000)
    finally:
        cpu.hook_del(handle)
    (pc, ptr, x, y), = observed
    assert pc == cpu.reg_read(UC_ARM_REG_PC) and (x, y) == (0, 24)
    text = read_text(cpu, ptr)
    count = len(text.encode('cp932'))
    assert count <= capacity
    return dict(original_draw_call=BASE + call, visible_input=text, original_origin=[x, y], measured_cells=count,
        source_branch_limit_cells=capacity, computed_width_px=count * 6, stopped_before_draw_call=True)


def snapshot_review(ctx, clean):
    cpu, get, provider = ctx.machine(ctx.arm, ctx.common, ctx.raw, ctx.plan)
    assert unpack_from('<I', clean, 0xCDAC0)[0] == BASE + TABLE
    towns = get(0xCB178)
    rows, proposed = [], []
    for town_id in range(114):
        table_row = get(0x79D8, town_id)
        if not table_row:
            continue
        actor, source_town, tail = bytes(cpu.mem_read(table_row, 3))
        assert source_town == town_id and 186 <= actor <= 206
        assert bytes(cpu.mem_read(table_row, 3)) == clean[table_row - BASE:table_row - BASE + 3]
        obj = ctx.actor_root + 4 + 32 * actor
        name_table = TABLE + 32 * actor
        source_name = read_static(clean, name_table)
        source_city = read_static(clean, name_table + 4) | {'column': 4}
        city_ptr = get(0x7EAF4, obj)
        assert city_ptr == unpack_from('<I', ctx.arm, name_table + 4)[0]
        vtable = read_pointer(cpu, obj)
        assert vtable == BASE + 0x148414 and read_pointer(cpu, vtable + 0x24) == BASE + 0x7EAF4
        primary = read_text(cpu, get(0x7EB0C, obj))
        alias = read_text(cpu, city_ptr)
        short_name = read_text(cpu, get(0x7ED88, obj))
        catalog_name = read_text(cpu, get(0x7EDD4, obj))
        assert short_name == catalog_name == primary
        joined = read_text(cpu, get(0x7EA8C, obj))
        assert joined == primary + ' ' + alias
        town = towns + 4 + 108 * town_id
        port = get(read_pointer(cpu, read_pointer(cpu, town) + 8) - BASE, town)
        port_label = read_text(cpu, port)
        assert port_label.isascii()
        decision = 'revision' if actor in EDIT else 'retention'
        if actor in EDIT:
            assert (primary, port_label, town_id) == EDIT[actor] and alias == source_city['text']
            assert BASE <= city_ptr <= BASE + len(ctx.arm) - 0x20 and city_ptr == source_city['pointer']
            reason = ('Use the English name returned by the original port getter for the same Japanese town. '
                      'The label identifies the hostess’s town alongside her personal name.')
            at = city_ptr - BASE
            old = alias.encode('cp932')
            assert ctx.arm[at:at + len(old) + 1] == clean[at:at + len(old) + 1] == old + b'\0'
            for delta in range(len(old)):
                word = pack('<I', city_ptr + delta)
                first = ctx.arm.find(word)
                if delta == 0:
                    assert first == name_table + 4 and ctx.arm.find(word, first + 1) == -1
                else:
                    assert first == -1
            target = port_label.encode('ascii').ljust(len(old), b'\0')
            assert len(target) == len(old)
            proposed.append(dict(actor=actor, column=4, table_field_offset=name_table + 4, pointer=city_ptr,
                physical_offset=at, source_hex=old.hex(), target_hex=target.hex(), owned_bytes=len(old),
                current_text=alias, target_text=port_label, source_clean_component=source_city,
                following16_hex=ctx.arm[at + len(old):at + len(old) + 16].hex(), reason=reason,
                review=dict.fromkeys(GATES, True), aligned_ARM9_references=[dict(offset=name_table + 4, pointer=city_ptr)],
                owners=[dict(actor=actor, column=4, pointer=city_ptr, field_offset=name_table + 4)]))
        elif actor in VARIANTS:
            a, p, reason = VARIANTS[actor]
            assert (alias, port_label) == (a, p)
        else:
            assert alias == port_label
            reason = f'Keep {alias}. The source associates {primary} with this town, and the localized label agrees with the current port name.'
        rows.append(dict(actor=actor, town_ID=town_id, source_lookup_table=table_row, runtime_actor=obj,
            source_name=source_name, source_city_label=source_city, current_city_label=alias,
            current_ALIGNED_field=name_table + 4, current_pointer=city_ptr, current_hex=alias.encode('cp932').hex(),
            English_city_label=port_label if actor in EDIT else alias, current_primary=primary, current_joined=joined,
            dialogue_name=short_name, list_name=catalog_name, active_town_label=port_label, active_town_pointer=port,
            reason=reason, decision=decision, review=dict.fromkeys(GATES, True) | {'formatting': False}))
    assert {row['actor'] for row in rows} == set(range(186, 207)) and len(rows) == 21
    assert {p['actor'] for p in proposed} == set(EDIT)
    assert bytes(cpu.mem_read(ctx.actor_root, 0x1A04)) == ctx.actor_bytes and not provider.reads
    return rows, proposed


def test_proposals(ctx, clean, rows, proposed):
    target, proof = plan_arm9_name_fields(ctx.arm,
        dict(format='dk4-owned-name-fields-proposal-v2', runtime=ctx.receipt(), fields=proposed), clean)
    plan = {'patches': [dict(address=f['pointer'], source_hex=f['source_hex'], target_hex=f['target_hex']) for f in proposed]}
    cpu, get, provider = ctx.machine(ctx.arm, ctx.common, ctx.raw, ctx.plan)
    renderer, _, font = font_tools(ctx.image)
    kanji = ctx.image.read_file('/GRP/KANJI.FNT')
    pages, stages = [], {}
    for version in ('current', 'proposed'):
        if version == 'proposed':
            for f in plan['patches']:
                old, new = (bytes.fromhex(f[k]) for k in ('source_hex', 'target_hex'))
                assert bytes(cpu.mem_read(f['address'], len(old) + 1)) == old + b'\0'
                cpu.mem_write(f['address'], new)
        for row in rows:
            actor, obj = row['actor'], row['runtime_actor']
            city = row['current_city_label'] if version == 'current' else row['English_city_label']
            assert read_text(cpu, get(0x7EAF4, obj)) == city
            for method in (0x7EB0C, 0x7ED88, 0x7EDD4):
                assert read_text(cpu, get(method, obj)) == row['current_primary']
            joined = row['current_primary'] + ' ' + city
            assert read_text(cpu, get(0x7EA48, obj)) == read_text(cpu, get(0x7EA8C, obj)) == joined
            cases = [draw_input(cpu, obj, *spec) for spec in CALLERS]
            assert all(case['visible_input'] == joined for case in cases)
            assert all(case['computed_width_px'] <= 168 and len(joined.splitlines()) == 1 for case in cases)
            if actor in EDIT:
                form = row.setdefault('full_name_panel_inputs', {})
                form[version] = cases
                pixels, glyphs = render_portrait(renderer, ctx.arm, kanji, joined.encode('cp932'))
                assert len(glyphs) == len(joined) - joined.count(' ')
                pages.append((f'{actor} {version}', pixels))
        stages[version] = dict(actors=21, original_panel_inputs=42, full_name_getters=42, unchanged_short_getters=63)
    assert bytes(cpu.mem_read(ctx.actor_root, 0x1A04)) == ctx.actor_bytes and not provider.reads
    return target, proof, font, stages, pages


def main():
    assert not ROOT.exists() and not REVIEW.exists() and not DOC.exists()
    release = base.load(current.RELEASE)
    ctx = RegisteredRuntime(current.RELEASE, release['own_registered_startup'], captain=3)
    assert base.digest(stage.CLEAN) == release['clean_input_sha256'] and base.digest(base.REGISTRY) == release['registry_sha256']
    clean = base.NdsImage.open(stage.CLEAN).read_file(stage.ARM)
    assert all(ctx.arm[lo:hi] == clean[lo:hi] for lo, hi in SPANS)
    rows, proposed = snapshot_review(ctx, clean)
    target, proof, font, stages, pages = test_proposals(ctx, clean, rows, proposed)
    ROOT.mkdir()
    arm_path = ROOT / 'barmaid_town_labels_RESEARCH_ONLY_ARM9.bin'
    arm_path.write_bytes(target)
    assert base.digest(arm_path) == proof['target_ARM9_sha256']
    sheets = portrait_sheets(ROOT, pages)
    base.save(REVIEW, dict(candidate_sha256=release['candidate_sha256'], clean_sha256=release['clean_input_sha256'],
        translation_policy='natural-dialogue-v2', target_locale='en-US', review_gates=GATES, records=rows,
        initialized_native_cases=stages, native_fixture=ctx.receipt(), original_code_spans=SPANS,
        proposal=proposed, planned_ARM9=proof, research_ARM9=str(arm_path), font=font, sheets=sheets,
        offline_rendered_name_reference_only=True, actual_name_widget_triggers='unverified', new_dialogue_credit=0))
    print('21 hostess city fields, two exact corrections, and 84 original name-panel draw inputs checked.')


if __name__ == '__main__':
    main()
