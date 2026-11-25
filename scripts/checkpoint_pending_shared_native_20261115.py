"""Bound native callers of the stored Online and scene-label copies."""

from collections import Counter
from hashlib import sha256
from itertools import pairwise
from pathlib import Path
from struct import iter_unpack, pack, unpack_from

from capstone import CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB, Cs
from ndspy.code import MainCodeFile
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL, STAGE
from dk4tool.patch.pirate_report_bearings_v1 import TABLES as PIRATE_TABLES
from dk4tool.patch.reviewed_item_cards import item_table
from dk4tool.patch.special_battle_target_names_v1 import TABLE as BATTLE_TARGET_TABLE
from dk4tool.script.common_message_table import (
    DIRECTORY_OFFSET,
    TABLE_OFFSET,
    common_message_entries,
)
from scripts import register_square_shop_captions_20261115 as current
from scripts.inventory_native_common_calls import TARGETS
from scripts.probe_button_prompt_native import call, machine
from scripts.reconcile_common_scene_labels_20261115 import gallery_titles
from scripts.reconcile_online_promotional_current_20261115 import replay as observed
from scripts.review_source_item_cards_and_coin_v1 import COUNT as SOURCE_CARD_COUNT
from scripts.review_source_item_cards_and_coin_v1 import FIRST as FIRST_SOURCE_CARD
from scripts.review_source_item_cards_and_coin_v1 import GETTER as SOURCE_CARD_GETTER
from scripts.review_source_item_cards_and_coin_v1 import LOOKUP
from scripts.seal_shared_text_source_v1 import reference

base = current.base
ROOT = Path('translations/editorial_checkpoints/SharedText_20261110_v1')
OUTPUT = ROOT / 'pending_shared_native_scope_20261115_v1.json'
MAP = ROOT / 'online_gallery_owner_reconciliation_20261114_v2.json'
OPENING = ROOT / 'opening_scene_labels_20261115_v1.json'
SCENES = Path('translations/common_scene_labels_manuscript_v2.json')
ONLINE = Path('translations/common_online_promotional_manuscript_v3.json')
GALLERY = Path('releases/all_routes_editorial_20261111_visible_gallery_captions_candidate/verification/registered_caption_review.json')
ROUTING = Path('work/analysis/event_still_routing_v426/routing_proof.json')
LEGACY = Path('work/current_amsterdam_square_20261114_v1/legacy_register_flow_exploration.json')
VOICE_ENTRIES = {BASE + n for n in (0x53BD8, 0x53CB0, 0x53D44, 0x53EC0, 0x53F0C)}
ENTRY_POINTS = set(TARGETS) | VOICE_ENTRIES | {0x020590F0, 0x020BF328}
NUMBER_USES = {
    3316: ((0x5A00C, 0x5A028, 0x5A040, 0x5A144, 0x5A160), 0x5A16C,
           'Stack frame allocation and restoration. The loaded value is added to or subtracted from SP.'),
    3436: ((0x64648, 0x64708, 0x64798), (0x646A0, 0x64758, 0x64820),
           'Object field offset. The next instruction forms the field address relative to r4 or r5.'),
    3516: ((0x6389C, 0x639D4), 0x639E0,
           'Stack frame allocation and restoration for the routine at 02063898.'),
    3547: ((0x01328, 0x7B8EC, 0xF6FE0), (0x01414, 0x7BB60, 0xF72B4),
           'Numeric parameter 0xDDB paired with 0x1555 at 020E1B20. It is passed to the arithmetic routine at 020DFC08.'),
    3588: ((0xC0D68, 0xC15FC, 0xC42A8, 0xC4530, 0xC4774),
           (0xC0F68, 0xC2028, 0xC43D4, 0xC4654, 0xC4938),
           'Object-relative offset to the table of five 0x74-byte elements.'),
    3601: ((0x6F6D4,), 0x6F7A4,
           'Input wait parameter. 020C9A5C compares it with 3600, then uses the flag to select the input/timeout loop.'),
}


def sha(raw):
    return sha256(raw).hexdigest()


def components(rom):
    sections = MainCodeFile(rom.arm9, rom.arm9RamAddress).sections
    result = [(f'ARM9 section {i}', section.ramAddress, bytes(section.data))
              for i, section in enumerate(sections)]
    for section in sections:
        if section.ramAddress == STAGE:
            result.append(('ARM9 deployed payload', POOL, bytes(section.data[:-48])))
    result.append(('ARM7', rom.arm7RamAddress, bytes(rom.arm7)))
    for label, overlays in (('ARM9', rom.loadArm9Overlays()), ('ARM7', rom.loadArm7Overlays())):
        result.extend((f'{label} overlay {i}', ov.ramAddress, bytes(ov.data))
                      for i, ov in overlays.items())
    return result


def find(raw, needle):
    at = raw.find(needle)
    while at != -1:
        yield at
        at = raw.find(needle, at + 1)


def branch_hits(raw, address, targets):
    hits = []
    for index, (word,) in enumerate(iter_unpack('<I', raw[:len(raw) & ~3])):
        if word >> 28 == 15 or word & 0x0E000000 != 0x0A000000:
            continue
        delta = word & 0xFFFFFF
        if delta & 0x800000:
            delta -= 0x1000000
        pc = address + index * 4
        target = (pc + 8 + 4 * delta) & 0xFFFFFFFF
        if target in targets:
            hits.append((pc, target, 'arm_bl' if word & 0x01000000 else 'arm_b'))
    halves = [word for word, in iter_unpack('<H', raw[:len(raw) & ~1])]
    for index, (first, second) in enumerate(pairwise(halves)):
        if first & 0xF800 != 0xF000 or second & 0xF801 != 0xE800:
            continue
        delta = ((first & 0x7FF) << 12) | ((second & 0x7FF) << 1)
        if delta & 0x400000:
            delta -= 0x800000
        pc = address + index * 2
        target = (((pc + 4) & ~3) + delta) & 0xFFFFFFFF
        if target in targets:
            hits.append((pc, target, 'thumb_blx_immediate'))
    for target in sorted(targets):
        hits.extend((address + at, target, 'exact_pointer_word') for at in find(raw, pack('<I', target)))
    return sorted(hits)


def component_census(rom):
    result = []
    for name, address, raw in components(rom):
        hits = branch_hits(raw, address, ENTRY_POINTS)
        counts = Counter(kind for _, _, kind in hits)
        result.append({
            'component': name, 'runtime_base': address, 'size': len(raw), 'sha256': sha(raw),
            'hit_counts': dict(counts), 'non_link_or_pointer_hits': [r for r in hits if r[2] != 'arm_bl'],
            'linked_calls_outside_primary_section': [r for r in hits if r[2] == 'arm_bl' and name != 'ARM9 section 0'],
            'executed_control_hits': [r for r in hits if r[0] in (0x020BE534, 0x0205C1CC)],
            'testdata_path_matches': list(find(raw.lower(), b'testdata')),
            'main_archive_path_matches': list(find(raw.upper(), b'\\COMMON\\MESFILE.DK4\0')),
        })
    return result


def disassemble(raw, start, count):
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    return [f'{pc:08x} {mnemonic} {args}' for pc, _, mnemonic, args in
            decoder.disasm_lite(raw[start:start + count * 4], BASE + start)]


def number_uses(clean, current_arm):
    rows = []
    for ident, (instructions, literals, purpose) in NUMBER_USES.items():
        if isinstance(literals, int):
            literals = (literals,) * len(instructions)
        matches = []
        for at, literal in zip(instructions, literals, strict=True):
            word, = unpack_from('<I', clean, at)
            assert word & 0x0F7F0000 == 0x051F0000
            distance = word & 0xFFF
            assert literal == at + 8 + (distance if word & 0x800000 else -distance)
            assert unpack_from('<I', clean, literal) == (ident,)
            assert unpack_from('<I', current_arm, literal) == (ident,)
            assert clean[at:at + 8] == current_arm[at:at + 8]
            matches.append({'literal_file_offset': literal, 'disassembly': disassemble(clean, at, 6)})
        rows.append({'message_ID': ident, 'numeric_purpose': purpose, 'occurrences': matches})
    return rows


def printed_id(cpu, start, args, wrapper, register):
    ids = []

    def observe(core, _address, _size, _):
        ids.append(core.reg_read(register))
        core.reg_write(UC_ARM_REG_PC, core.reg_read(UC_ARM_REG_LR))

    hook = cpu.hook_add(UC_HOOK_CODE, observe, begin=wrapper, end=wrapper)
    try:
        call(cpu, start - BASE, args)
    finally:
        cpu.hook_del(hook)
    ident, = ids
    return ident


def aliases(clean, current_arm):
    shared = ((0x58F4C, 0x59138), (0xBE51C, 0xBE53C), (0xBF328, 0xBF338))
    assert all(clean[lo:hi] == current_arm[lo:hi] for lo, hi in shared)
    shelf_instructions = disassemble(clean, 0xBE51C, 7)
    assert shelf_instructions[-2:] == ['020be530 sub r1, r6, #0x15', '020be534 bl #0x20bf328']
    assert branch_hits(clean, BASE, {0x020BF328}) == [(0x020BE534, 0x020BF328, 'arm_bl')]
    probes = (*range(-1, 256), -(2**31), 2**31 - 1)
    results = []
    for arm in (clean, current_arm):
        cpu = machine(arm)
        first = [printed_id(cpu, 0x02058F4C, (0, n & 0xFFFFFFFF, 0),
                            0x02053FE4, UC_ARM_REG_R1) for n in probes]
        second = [printed_id(cpu, 0x020BF328, (0, n), 0x020546B8, UC_ARM_REG_R0)
                  for n in range(0x91 - 0x15)]
        assert second == list(range(137, 261))
        results.append((first, second))
    assert results[0] == results[1]
    first, second = results[0]
    return [
        {'entry': 0x02058F4C, 'indirect_target': 0x02053FE4, 'cases': len(probes),
         'observed_ids': sorted(set(first)), 'default_id': first[0]},
        {'entry': 0x020BF328, 'indirect_target': 0x020546B8, 'sole_direct_caller': 0x020BE534,
         'cases': len(second), 'observed_ids': second, 'caller_guard_instructions': shelf_instructions},
    ]


def deployed_text_routes(clean, active, scans):
    arm = active.read_file(current.stage.ARM)
    decoded = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
    thumb_calls = [
        edge for row in scans for edge in row['non_link_or_pointer_hits']
        if edge[2] == 'thumb_blx_immediate'
    ]
    assert thumb_calls == [(0x0200DB0A, 0x0205528C, 'thumb_blx_immediate'),
                           (0x0207E3DE, 0x0205528C, 'thumb_blx_immediate')]
    thumb = []
    for pc, target, _ in thumb_calls:
        at = pc - BASE
        setup, branch = list(decoded.disasm(arm[at - 2:at + 4], pc - 2))
        assert branch.mnemonic == 'blx' and branch.op_str == f'#{target:#x}'
        if pc == 0x0200DB0A:
            assert setup.mnemonic == 'ldr' and setup.op_str == 'r0, [pc, #0x2c]'
            literal = ((pc - 2 + 4) & ~3) + 0x2C
            ident, = unpack_from('<I', arm, literal - BASE)
            assert ident == 1931
        else:
            assert setup.mnemonic == 'movs' and setup.op_str == 'r0, #0x61'
            ident, literal = 97, None
        thumb.append({'call_site': pc, 'target': target, 'message_ID': ident, 'literal': literal})
    existing = clean.read_file(current.stage.ARM)
    tables = []
    for address in (*PIRATE_TABLES, BATTLE_TARGET_TABLE):
        at = address - BASE
        words = unpack_from('<8i', arm, at)
        assert arm[at:at + 32] == existing[at:at + 32]
        tables.append({'table_address': address, 'candidate_ids': [n for n in words if n >= 0]})
    staged = [edge for row in scans for edge in row['linked_calls_outside_primary_section']]
    assert staged == [(SOURCE_CARD_GETTER + 8, 0x0205528C, 'arm_bl')]
    supported_edges = [edge for _, at, raw in components(active.rom)
                       for edge in branch_hits(raw, at, {SOURCE_CARD_GETTER})]
    assert supported_edges == [(BASE + pc, SOURCE_CARD_GETTER, 'arm_bl') for pc in LOOKUP]
    _, _, item_pointers = item_table(arm)
    assert all(unpack_from('<I', existing, off) == unpack_from('<I', arm, off) == (FIRST_SOURCE_CARD,)
               for off in (0x4D890, 0x4E53C))
    assert SOURCE_CARD_COUNT == 20 and len(item_pointers) == 218
    return {'thumb_direct': thumb, 'registered_bearing_and_battle_target_tables': tables,
            'source_card_original_supported_ids': [FIRST_SOURCE_CARD, FIRST_SOURCE_CARD + len(item_pointers) - 1],
            'source_card_origins': [edge[0] for edge in supported_edges]}


def exact_online_dependencies(clean, active):
    book = base.load(ONLINE)
    earlier = observed.current
    assert base.digest(earlier.ROM) == book['candidate_sha256']
    previous = base.NdsImage.open(earlier.ROM)
    src, old, now = (r.read_file(current.stage.ARM) for r in (clean, previous, active))
    assert GameAsciiFont.from_arm9(old).glyphs == GameAsciiFont.from_arm9(now).glyphs
    assert book['actual_tested_paths_COMMON_requests'] == 0
    groups = ('actual_independent_guide_pages', 'actual_independent_about_extras_pages')
    pages = []
    for family in groups:
        for row in book[family]:
            at = row['pointer'] - BASE
            field = row['ARM9_field']
            assert unpack_from('<I', now, field) == unpack_from('<I', old, field) == (row['pointer'],)
            payload = old[at:old.index(0, at) + 1]
            assert payload.isascii() and payload == now[at:at + len(payload)]
            if 'source_artwork' in row:
                art = active.read_file(row['source_artwork'])
                assert sha(art) == row['same_artwork_sha256']
                assert payload[:-1].decode('ascii') == row['English']
                source_at = at
            else:
                source_at = row['clean_ARM9_offset']
            original = src[source_at:src.index(0, source_at)]
            assert original.decode('cp932') == row['clean_Japanese']
            pages.append({'case': row['id'], 'frame': row['frame'], 'current_pointer': row['pointer'],
                          'current_text_sha256': sha(payload), 'clean_source_offset': source_at})
    assert len(pages) == 19
    return pages


def records(source, stored, scope_paths):
    owner = {r['message_ID']: r for r in base.load(MAP)['maps']}
    scene = {r['message_ID']: r for r in base.load(SCENES)['records']}
    online = {r['message_ID']: r for r in base.load(ONLINE)['records']}
    opening = {r['message_ID']: r for r in base.load(OPENING)['records']}
    assert set(owner) == (set(scene) | set(online))
    selected = []
    for n, mapped in sorted(owner.items()):
        original, active = source[n], stored[n]
        assert original.text == active.text == bytes.fromhex(mapped['stored_hex'])
        editorial = scene[n] if n in scene else online[n]
        handling = 'source-artwork context'
        if mapped['independent_exact_Gallery_captions']:
            handling = 'exact Japanese duplicate of an independently reviewed Gallery caption'
        elif n in online:
            handling = 'related to an independently reviewed Online or About Extras page'
        elif n in opening and not opening[n]['artwork_association']:
            handling = 'opening label with unresolved artwork mapping'
        selected.append({
            'message_ID': n, 'source_reference': reference(original), 'current_reference': reference(active),
            'stored_hex': active.text.hex(), 'source_Japanese': active.text.decode('cp932'),
            'editorial_work': str(SCENES if n in scene else ONLINE),
            'wording_decision': editorial['decision'], 'review_gates': editorial['review'],
            'localized_draft': editorial['english'], 'localization_note': editorial['localization_note'],
            'classification_basis': handling,
            'independent_display_evidence': scope_paths.get(n), 'legacy_display_owner': 'open',
            'artwork_context': scene[n]['artwork'] if n in scene else None,
            'opening_artwork_context': opening[n]['artwork_association'] if n in opening else None,
        })
    return selected


def main():
    assert not OUTPUT.exists()
    release = base.load(current.RELEASE)
    assert base.digest(current.ROM) == release['candidate_sha256']
    assert base.digest(current.stage.CLEAN) == release['clean_input_sha256']
    assert base.digest(base.REGISTRY) == release['registry_sha256']
    clean, active = map(base.NdsImage.open, (current.stage.CLEAN, current.ROM))
    source_arm, target_arm = (r.read_file(current.stage.ARM) for r in (clean, active))
    source_common, target_common = (r.read_file(current.parent.stage.COMMON) for r in (clean, active))
    source = common_message_entries(source_common, source_arm)
    stored = owned_entries(target_common, target_arm, sha(target_arm[DIRECTORY_OFFSET:TABLE_OFFSET]))
    prior = base.load(LEGACY)
    assert len(prior['confirmed_positive_control_296_callers']) == 3
    by_source, *_ = gallery_titles(source_arm, target_arm, base.load(ROUTING), base.load(GALLERY)['records'])
    assert len(by_source) >= 123
    owners = base.load(MAP)['maps']
    scope = {row['message_ID']: row['independent_exact_Gallery_captions']
             or row['independently_displayed_Online_or_Extras_owner'] for row in owners}
    by_record = records(source, stored, scope)
    assert len(by_record) == 245 and sum(bool(row['independent_display_evidence']) for row in by_record) == 154
    numeric = number_uses(source_arm, target_arm)
    dispatch = aliases(source_arm, target_arm)
    pending = set(prior['pending_ids'])
    assert pending.isdisjoint(ident for family in dispatch for ident in family['observed_ids'])
    scans = {label: component_census(rom) for label, rom in (('clean', clean.rom), ('current', active.rom))}
    for result in scans.values():
        overlay, = (row for row in result if row['component'] == 'ARM9 overlay 0')
        assert overlay['size'] == 6208 and not overlay['hit_counts']
        assert not any(row['testdata_path_matches'] for row in result)
    assert scans['clean'][-1]['sha256'] == scans['current'][-1]['sha256']
    routed = deployed_text_routes(clean, active, scans['current'])
    assert pending.isdisjoint(row['message_ID'] for row in routed['thumb_direct'])
    assert pending.isdisjoint(n for table in routed['registered_bearing_and_battle_target_tables']
                              for n in table['candidate_ids'])
    first_card, last_card = routed['source_card_original_supported_ids']
    assert pending.isdisjoint(range(first_card, last_card + 1))
    menu_pages = exact_online_dependencies(clean, active)
    base.save(OUTPUT, {
        'candidate_sha256': release['candidate_sha256'], 'source_sha256': release['clean_input_sha256'],
        'records': by_record, 'numeric_collisions': numeric, 'native_indirect_cases': dispatch,
        'component_scans': scans, 'current_thumb_and_owned_table_routes': routed,
        'carried_forward_observed_menu_pages': menu_pages, 'exact_registered_gallery_captions': 164,
        'read_only': True, 'new_gameplay_runs': 0,
        'unresolved_primary_paths': len(prior['unresolved_candidate_calls']),
        'limits': ('The executable census checks direct encodings and exact stored pointers. Computed targets, '
                   'script or data-driven indirect calls and unobserved events still need separate evidence.'),
        'evidence': {str(path): base.digest(path) for path in
                     (MAP, OPENING, SCENES, ONLINE, GALLERY, ROUTING, LEGACY, current.RELEASE, Path(__file__))},
        'new_dialogue_credit': 0, 'remaining_shared_keys': len(prior['pending_ids']), 'full_goal_complete': False,
    })
    print(f'{len(by_record)} stored copies rebound; {sum(len(r["occurrences"]) for r in numeric)} numeric collisions; '
          f'{sum(r["cases"] for r in dispatch)} indirect producer checks per ROM.')


if __name__ == '__main__':
    main()
