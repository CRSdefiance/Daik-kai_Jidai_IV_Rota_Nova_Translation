"""Find uncredited clean SC0 speech, physical styles and menu captions without rerendering."""
import re
import struct
from collections import Counter, defaultdict
from pathlib import Path

from dk4tool.dialogue.reviewed_choice_object_v2 import labels
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory


ROOT = Path('work/analysis/Rafael_source_coverage_20261106_v2')
LEDGER = Path('translations/editorial_review_current_v1.json')
RELEASE = Path('work/rafael4903_release_v1/registered_release_verification.json')
ARCHIVE = '/data/SC0.DK4'


def source_location(row):
    ref = row.get('source_reference', {})
    match = re.search(r'_B(\d+)_', row['id'])
    block = row.get('block', ref.get('block', int(match[1]) if match else None))
    raw = row.get('source_hex', ref.get('hex'))
    offset = ref.get('offset', ref.get('offset_in_block'))
    return block, offset, raw


def main():
    assert not ROOT.exists()
    ledger, release = map(load, (LEDGER, RELEASE))
    assert ledger['records_editorially_completed'] == 16748 and not ledger['full_goal_complete']
    assert digest('translations/release_stack.json') == release['registry_sha256']
    clean = Path('work/clean.nds')
    assert digest(clean) == 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    image = NdsImage.open(clean)
    archive, arm = image.read_file(ARCHIVE), image.read_file('/__arm9__.bin')
    blocks = IlnkContainer.parse(archive).blocks
    keys = {(r['file_path'], r['id']) for r in ledger['contextual_story_natural_dialogue_pass_v1871']['integrated_record_keys']}
    by_key, by_position, evidence, unbound = defaultdict(list), defaultdict(list), {}, []
    for family in ledger['completed_editorial_families']:
        rows = family['records']
        if not isinstance(rows, list):
            final = Path(family['final_review'])
            value = load(final)
            if family.get('final_review_sha256'):
                assert digest(final) == family['final_review_sha256']
            evidence[str(final)] = digest(final)
            rows = value['records']
        for row in rows:
            if row.get('file_path') != ARCHIVE:
                continue
            key = (row.get('file_path'), row['id'])
            if key[0] != ARCHIVE or key not in keys:
                continue
            block, offset, raw = source_location(row)
            binding = dict(id=row['id'], family=family['id'], block=block, offset=offset, source_hex=raw)
            by_key[key].append(binding)
            if block is not None and offset is not None and raw is not None:
                value = bytes.fromhex(raw)
                if blocks[block][offset:offset+len(value)] == value:
                    by_position[(block, offset, raw)].append(binding)
                else:
                    unbound.append({**binding, 'reason': 'legacy source reference does not match clean bytes at its stated position'})
            else:
                unbound.append({**binding, 'reason': 'legacy record lacks a complete source position'})

    # Existing clean packets already hold the complete nested command inventory.
    # Reuse them only when their clean archive and exact group bytes still agree.
    packets = sorted(set(Path('work').glob('Rafael_*/clean_source_packet.json')) |
                     set(Path('work/analysis').glob('Rafael_*/clean_source_packet.json')) |
                     {Path('work/analysis/Rafael_source_coverage_20261106_v1/residual_clean_source_packet.json')})
    cached = {}
    for path in packets:
        if path.is_dir():
            path = path / 'clean_source_packet.json'
        if not path.is_file():
            continue
        packet = load(path)
        if packet.get('file_path') != ARCHIVE or packet.get('source_ROM_sha256') != digest(clean):
            continue
        if packet.get('source_archive_sha256') != __import__('hashlib').sha256(archive).hexdigest():
            continue
        used = False
        for group in packet['groups']:
            n = group['block']
            assert bytes.fromhex(group['clean_block_hex']) == blocks[n]
            commands = group['all_source_commands']
            if n in cached:
                assert cached[n] == commands
            cached[n] = commands
            used = True
        if used:
            evidence[str(path)] = digest(path)
    inventory, _, _ = scoped_inventory()
    records, failures, groups, source_counts = [], [], [], Counter()
    fresh = []
    for n, block in enumerate(blocks):
        try:
            commands = cached.get(n)
            if commands is None:
                commands, _ = inventory(arm, block)
                fresh.append(n)
            assert all(block[c['offset']:c['offset']+c['native_extent']].hex() == c['whole_command_hex'] for c in commands)
            local = []
            for command in commands:
                at, word = command['offset'], command['word']
                raw = bytes.fromhex(command['whole_command_hex'])
                values = []
                if word == 0x4000:
                    start = at + 5
                    body = block[start:block.index(0, start+1)]
                    values = [(f'DK4_MES_B{n}_R{block[:start].count(bytes([0])):04d}', start, body, 'ordinary-speech')]
                elif word == 0x4100:
                    for rel in sorted(set(struct.unpack_from('<8H', raw, 2))):
                        start = at + 20 + rel
                        body = block[start:block.index(0, start)]
                        values.append((f'SC0_B{n}_STYLE_{at}_{rel}', start, body, 'physical-style-alternative'))
                elif word in (0x2100, 0x2200):
                    captions = labels(raw)
                    offsets = struct.unpack_from('<' + str(len(captions)) + 'H', raw, 2)
                    for index, body in enumerate(captions):
                        start = at + 2 + 2*len(captions) + offsets[index]
                        values.append((f'SC0_B{n}_CHOICE_{at}_{index}', start, body, 'typed-menu-caption'))
                for ident, start, body, kind in values:
                    assert block[start:start+len(body)] == body
                    position = (n, start, body.hex())
                    exact = by_position.get(position, [])
                    keyed = by_key.get((ARCHIVE, ident), [])
                    if keyed:
                        # A key alone does not repair an incomplete old source reference.
                        exact = [r for r in exact if r['id'] == ident] or exact
                    row = dict(id=ident, file_path=ARCHIVE, block=n, kind=kind,
                        source_reference=dict(block=n, command_offset=at, offset=start, length=len(body)),
                        source_hex=body.hex(), source_Japanese=(body[1:] if word==0x4000 else body).decode('cp932'),
                        exact_credited_source_bindings=exact, covered=bool(exact),
                        existing_key_without_exact_source_binding=bool(keyed) and not bool(exact))
                    records.append(row); local.append(row); source_counts[kind] += 1
            if any(not r['covered'] for r in local):
                groups.append(dict(block=n, file_path=ARCHIVE, clean_block_hex=block.hex(),
                    all_source_commands=commands, records=local,
                    missing_source_objects=sum(not r['covered'] for r in local)))
        except Exception as exc:
            failures.append(dict(block=n, error_type=type(exc).__name__, error=str(exc), not_assumed_covered=True))
        if n % 50 == 0:
            print(f'SC0 {n}/{len(blocks)}; uncovered objects {sum(not r["covered"] for r in records)}; failures {len(failures)}', flush=True)
    ROOT.mkdir(parents=True)
    uncovered = [r for r in records if not r['covered']]
    save(ROOT/'coverage.json', dict(source_ROM=str(clean), source_ROM_sha256=digest(clean),
        source_archive_sha256=__import__('hashlib').sha256(archive).hexdigest(), release=str(RELEASE),
        release_sha256=digest(RELEASE), ledger=str(LEDGER), ledger_sha256=digest(LEDGER),
        blocks=len(blocks), reused_packet_blocks=sorted(cached), freshly_inventoried_blocks=fresh,
        object_counts=dict(source_counts), records=records, missing=uncovered, inventory_failures=failures,
        legacy_source_bindings_not_exact=unbound, source_packets=evidence,
        dialogue_typed_styles_only_not_full_player_facing_or_reachability_census=True,
        numeric_adjacency_not_conversation_chronology=True, no_credit_or_ROM_mutation=True,
        new_credit=0, full_goal_complete=False, producer_sha256=digest(__file__)))
    save(ROOT/'residual_clean_source_packet.json', dict(route=0, file_path=ARCHIVE, groups=groups,
        source_ROM=str(clean), source_ROM_sha256=digest(clean),
        source_archive_sha256=__import__('hashlib').sha256(archive).hexdigest(),
        source_ARM9_sha256=__import__('hashlib').sha256(arm).hexdigest(),
        records=len(uncovered), source_only_not_current_English=True, new_credit=0))
    print(dict(objects=dict(source_counts), uncovered=len(uncovered), blocks_with_missing=[g['block'] for g in groups],
               failures=failures, legacy_source_binding_issues=len(unbound)), flush=True)


if __name__ == '__main__':
    main()
