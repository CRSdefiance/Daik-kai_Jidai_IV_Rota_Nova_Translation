"""Review sea-inspection names and restore the full Ghost Ship class label."""

from hashlib import sha256
from pathlib import Path
from struct import pack_into, unpack_from

from ndspy.code import MainCodeFile
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R8, UC_ARM_REG_SP

from scripts import replay_special_target_labels_20261115 as replay
from scripts.execute_map_entity_tooltip_copy import BASE, STACK, format_copy
from scripts.inventory_map_tooltip_classes import COUNT, SOURCE_STRIDE, TABLE
from scripts.probe_button_prompt_native import call
from scripts.probe_map_entity_tooltip_raster import expected_glyphs
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.verify_release_baseline import files

base, parent, ROOT = replay.base, replay.parent, replay.ROOT
ARM, CLEAN = parent.stage.ARM, parent.stage.CLEAN
ROM, STORED = ROOT / 'Special_Target_Labels_RESEARCH_ONLY.nds', ROOT / 'staged.json'
REVIEW = Path('translations/editorial_checkpoints/SharedText_20261110_v1/special_target_labels_20261115_v1.json')
NAME_FIELD = TABLE + 38 * SOURCE_STRIDE
STORED_GHOST = 0x0215BF98
ALIAS_GHOST_SHIP = 0x01FFFD6F
CATEGORY_FIELD, ACTOR_181 = 0x705E8, 0x120B80 + 181 * 32
GATES = ('source', 'context', 'localization', 'naturalness', 'formatting')
SPECIAL = {
    34: ('化魚', 'Monster Fish', 'The creature is a monstrous fish.',
         'Monster Fish keeps the particular creature distinct from the general category Monster.'),
    35: ('大イカ', 'Giant Squid', 'The creature is a giant squid.',
         'Keep the word Giant, since size is part of the Japanese name.'),
    36: ('サメ', 'Shark', 'The target is a shark.',
         'The singular Shark fits the individual target the player selected.'),
    37: ('鯨', 'Whale', 'The class is a whale.',
         'Keep the general class label Whale. The separate model is named White Whale.'),
    38: ('幽霊船', 'Ghost Ship', 'The target class is a ghost ship.',
         'Restore the ship in the class label and match the wording already used by the special victory report.'),
}


def digest(raw):
    return sha256(raw).hexdigest()


def pointer(arm, offset):
    return unpack_from('<I', arm, offset)[0]


def c_string(cpu, address, encoding):
    raw, nul, _ = bytes(cpu.mem_read(address, 64)).partition(b'\0')
    assert nul and raw
    return {'address': address, 'text': raw.decode(encoding), 'hex_with_NUL': (raw + nul).hex()}


def patch(arm, clean):
    assert COUNT == 39
    assert pointer(arm, NAME_FIELD) == pointer(clean, NAME_FIELD) == STORED_GHOST
    assert clean[STORED_GHOST - BASE:STORED_GHOST - BASE + 7] == '幽霊船'.encode('cp932') + b'\0'
    assert arm[STORED_GHOST - BASE:STORED_GHOST - BASE + 6] == b'Ghost\0'
    main = MainCodeFile(arm, BASE)
    assert len(main.sections) == 6 and bytes(main.save()) == arm
    alias = next(s for s in main.sections if s.ramAddress <= ALIAS_GHOST_SHIP < s.ramAddress + len(s.data))
    at = ALIAS_GHOST_SHIP - alias.ramAddress
    assert bytes(alias.data[at:at + 11]) == b'Ghost Ship\0'
    changed = bytearray(arm)
    pack_into('<I', changed, NAME_FIELD, ALIAS_GHOST_SHIP)
    target = bytes(changed)
    loaded = MainCodeFile(target, BASE)
    assert len(loaded.sections) == 6 and bytes(loaded.save()) == target
    pack_into('<I', changed, NAME_FIELD, STORED_GHOST)
    assert bytes(changed) == arm
    return target


def native_catalog(ctx, clean, arm):
    cpu, get, provider = ctx.machine(ctx.arm, ctx.common, ctx.raw, ctx.plan)
    class_root, model_root, actor_root = [get(fn) for fn in (0xCB154, 0xCB148, 0xCB184)]
    original = [c_string(cpu, get(0x1FD74, class_root + 4 + i * 64), 'ascii') for i in range(COUNT)]
    assert pointer(ctx.arm, CATEGORY_FIELD) == pointer(ctx.arm, ACTOR_181)
    actor = actor_root + 4 + 181 * 32
    category = c_string(cpu, pointer(ctx.arm, CATEGORY_FIELD), 'ascii')
    assert [get(f, actor) for f in (0x7ED88, 0x7EDD4)] == [category['address']] * 2
    assert category['text'] == 'Monster'
    fleet = get(0xCB1A8) + 4 + 39 * 132
    assert bytes(cpu.mem_read(fleet + 8, 1)) == b'\xb5'
    cpu.reg_write(UC_ARM_REG_SP, STACK)
    cpu.reg_write(UC_ARM_REG_R8, fleet)
    cpu.emu_start(BASE + 0x70424, BASE + 0x70470, count=100)
    assert cpu.reg_read(UC_ARM_REG_R8) == category['address']

    # The original initializer writes the new pointer into its existing class object.
    ghost = class_root + 4 + 38 * 64
    prior = bytes(cpu.mem_read(ghost, 64))
    assert c_string(cpu, ALIAS_GHOST_SHIP, 'ascii')['text'] == 'Ghost Ship'
    cpu.mem_write(BASE + NAME_FIELD, arm[NAME_FIELD:NAME_FIELD + 4])
    call(cpu, 0xCD3D0, (ghost,))
    restored = bytearray(cpu.mem_read(ghost, 64))
    assert unpack_from('<I', restored, 8)[0] == ALIAS_GHOST_SHIP
    pack_into('<I', restored, 8, STORED_GHOST)
    assert bytes(restored) == prior
    assert get(0x1FD74, ghost) == ALIAS_GHOST_SHIP
    current = [c_string(cpu, get(0x1FD74, class_root + 4 + i * 64), 'ascii') for i in range(COUNT)]
    assert [i for i, (a, b) in enumerate(zip(original, current, strict=True)) if a != b] == [38]
    models = {i: c_string(cpu, model_root + 4 + (i + 115) * 140 + 8, 'cp932') for i in SPECIAL}
    assert models[37]['text'] == '白鯨' and models[38]['text'] == 'Ghost'
    assert not provider.opens and not provider.reads
    assert bytes(cpu.mem_read(ctx.actor_root, 0x1A04)) == ctx.actor_bytes
    ctx.calls.clear()
    return original, current, models, category


def native_layout(arm, name, label):
    expected = f'{name}\n  {label} class'.encode('ascii')
    body = format_copy(arm, 0x705F0, [name.encode('ascii'), label.encode('ascii')], expected)
    text = expected.decode('ascii')
    glyphs = expected_glyphs(text)
    width = max(map(len, text.split('\n'))) * 6
    assert width <= 256 and all(g['x'] + 6 <= width for g in glyphs if g['code'] != 32)
    return {'text': text, 'copy': body, 'glyph_expectations': glyphs, 'width': width, 'height': 24}


def main():
    assert not STORED.exists() and not REVIEW.exists() and not ROM.exists()
    r = base.load(parent.RELEASE)
    assert base.digest(base.REGISTRY) == r['registry_sha256'] and base.digest(CLEAN) == r['clean_input_sha256']
    ctx = RegisteredRuntime(parent.RELEASE, r['own_registered_startup'], captain=3)
    clean = base.NdsImage.open(CLEAN).read_file(ARM)
    arm = patch(ctx.arm, clean)
    for start, stop in ((0x70424, 0x70498), (0xCD3D0, 0xCD488), (0x7ED88, 0x7EE08), (0x1FD74, 0x1FD7C)):
        assert clean[start:stop] == ctx.arm[start:stop]
    original, current, models, category = native_catalog(ctx, clean, arm)
    rows = []
    for i, (japanese, english, meaning, note) in SPECIAL.items():
        field = TABLE + i * SOURCE_STRIDE
        p = pointer(clean, field) - BASE
        assert clean[p:clean.index(0, p)].decode('cp932') == japanese
        assert current[i]['text'] == english
        rows.append({'id': f'MAP_CREATURE_CLASS_{i}', 'speaker': 'Sea inspection tooltip', 'class_index': i,
                     'source_reference': {'file_path': ARM, 'pointer_field': field, 'offset': p,
                                          'hex_with_NUL': (japanese.encode('cp932') + b'\0').hex()},
                     'Japanese': japanese, 'english': english, 'source_meaning': meaning, 'localization_note': note,
                     'context': 'Info Mode names the class of the selected target beneath its category.',
                     'current_reference': original[i], 'staged_reference': current[i], 'model_reference': models[i],
                     'decision': 'revision' if i == 38 else 'retention',
                     'review': dict.fromkeys(GATES, True) | {'formatting': False}})
    source_offset = pointer(clean, CATEGORY_FIELD) - BASE
    source_actor = pointer(clean, ACTOR_181) - BASE
    assert all(clean[i:clean.index(0, i)] == '怪物'.encode('cp932') for i in (source_offset, source_actor))
    rows.append({'id': 'MAP_ENTITY_TOOLTIP_MONSTER', 'actor_ID': 181, 'speaker': 'Sea inspection tooltip',
                 'Japanese': '怪物', 'english': 'Monster', 'source_meaning': 'The category used for a monster target.',
                 'context': 'Info Mode shows the category first. The runtime getters for actor 181 point to the same English string.',
                 'localization_note': 'Keep the generic category Monster above the particular creature or ghost ship class.',
                 'source_reference': {'map_pointer_field': CATEGORY_FIELD, 'map_offset': source_offset,
                                      'actor_pointer_field': ACTOR_181, 'actor_offset': source_actor},
                 'current_reference': category, 'decision': 'retention', 'review': dict.fromkeys(GATES, True) | {'formatting': False}})
    checks = [native_layout(ctx.arm, category['text'], original[38]['text']),
              native_layout(arm, category['text'], current[38]['text'])]
    ROOT.mkdir(parents=True, exist_ok=True)
    image = base.NdsImage.open(parent.ROM)
    before = files(image)
    image.replace_file(ARM, arm)
    after = files(image)
    assert before.keys() == after.keys() and {p for p in before if before[p] != after[p]} == {ARM}
    image.save(ROM)
    image.replace_file(ARM, ctx.arm)
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    candidate = base.digest(ROM)
    base.save(REVIEW, {'translation_policy': 'natural-dialogue-v2', 'target_locale': 'en-US',
                      'encoder': 'dialogue-relocatable-v1', 'review_gates': list(GATES), 'records': rows,
                      'candidate_sha256': candidate, 'runtime': ctx.receipt(), 'class_count': COUNT,
                      'display_checks': checks, 'scene_activation_pending': True})
    base.save(STORED, {'candidate_sha256': candidate, 'previous_sha256': r['candidate_sha256'],
                      'target_ARM9_sha256': digest(arm), 'field': NAME_FIELD, 'old_pointer': STORED_GHOST,
                      'new_pointer': ALIAS_GHOST_SHIP, 'whole_parent_inverse': True, 'review_sha256': base.digest(REVIEW)})
    print('Staged Ghost Ship with a single class pointer revision. All 38 other native class names match.')


if __name__ == '__main__':
    main()
