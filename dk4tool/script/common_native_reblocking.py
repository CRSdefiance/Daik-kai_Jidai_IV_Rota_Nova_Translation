"""Source-locked whole-record COMMON reblocking within the native cache limits."""
from __future__ import annotations

import hashlib
import struct
from collections import defaultdict

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.script.common_entry_tables import ITEM_TABLES
from dk4tool.script.common_message_table import (
    CODE_LOCKS,
    DIRECTORY_OFFSET,
    MESSAGE_COUNT,
    TABLE_OFFSET,
    common_message_entries,
)


def plan(common: bytes, arm9: bytes, authored: dict[int, bytes],
         first_block: int = 12, *, compact_existing_english_padding: bool = False,
         preserved: dict[int, bytes] | None = None) -> tuple[bytes, bytes, dict]:
    before = common_message_entries(common, arm9, clean=False)
    preserved = preserved or {}
    if not authored or not authored.keys() <= {e.message_id for e in before}:
        raise ValueError('Authored messages must name verified native IDs')
    container = IlnkContainer.parse(common)
    owners = defaultdict(list)
    for entry in before:
        owners[entry.block, entry.record_index].append(entry)
    targets = {(before[i].block, before[i].record_index) for i in authored}
    if (preserved.keys() & authored.keys()
            or not preserved.keys() <= {e.message_id for e in before}):
        raise ValueError('Preserved messages must be distinct verified native IDs')
    for i, raw in preserved.items():
        e = before[i]
        if raw != e.text or (e.block, e.record_index) not in targets:
            raise ValueError('Preserved packed neighbor must match the complete current span')
    if any(block < first_block for block, _ in targets):
        raise ValueError('Authored messages precede the reblocking pool')
    for owner in targets:
        if not {e.message_id for e in owners[owner]} <= authored.keys() | preserved.keys():
            raise ValueError('Every authored packed neighbor must be supplied')
    for raw in authored.values():
        if not raw or any(c in raw for c in (0, 10, 13)):
            raise ValueError('Authored text must be a nonempty CP932 paragraph')
        raw.decode('cp932')
    atoms, compacted = [], []
    item_ids = {(offset - TABLE_OFFSET) // 2 + i
                for offset, count, *_ in ITEM_TABLES.values() for i in range(count)}
    for block in range(first_block, len(container.blocks)):
        rows = container.blocks[block].split(b'\0')
        for record, raw in enumerate(rows):
            # A final empty split element is already the previous row's NUL.
            if record == len(rows) - 1 and not raw:
                continue
            old_owner = (block, record)
            entries = owners[old_owner]
            starts = {e.message_id: e.start for e in entries}
            if old_owner in targets:
                prefix = raw[:entries[0].start]
                if any(byte != 32 for byte in prefix):
                    raise ValueError('Unmapped authored alignment prefix')
                packed = bytearray(prefix)
                for e in entries:
                    starts[e.message_id] = len(packed)
                    packed.extend(authored[e.message_id] if e.message_id in authored
                                  else preserved[e.message_id])
                raw = bytes(packed)
            elif (compact_existing_english_padding and entries
                  and not any(e.message_id in item_ids for e in entries)):
                # Preserve every prefix, gap and unselected tail byte. Remove
                # only ASCII spaces after a nonempty native English selection.
                packed, cursor = bytearray(), 0
                for e in entries:
                    packed.extend(raw[cursor:e.start])
                    starts[e.message_id] = len(packed)
                    text = e.text
                    visible = text.rstrip(b' ')
                    if visible and all(32 <= ord(c) < 127 or c in 'ＩＦ' for c in visible.decode('cp932')):
                        if len(visible) != len(text):
                            compacted.append({'message_id': e.message_id,
                                              'removed_spaces': len(text) - len(visible)})
                        text = visible
                    packed.extend(text)
                    cursor = e.end
                packed.extend(raw[cursor:])
                raw = bytes(packed)
            atoms.append({'old_owner': old_owner, 'raw': raw,
                          'starts': starts, 'message_ids': [e.message_id for e in entries]})
    groups, active, size = [], [], 0
    for atom in atoms:
        atom_size = len(atom['raw']) + 1
        if atom_size > 4096:
            raise ValueError('A complete native owner exceeds cache capacity')
        if active and size + atom_size > 4096:
            groups.append(active)
            active, size = [], 0
        active.append(atom)
        size += atom_size
    if active:
        groups.append(active)
    expected_groups = 41 - first_block
    if compact_existing_english_padding:
        # Keep all original directory slots. Split whole-owner groups without
        # reordering atoms; each resulting slot must select native messages.
        while len(groups) < expected_groups:
            choices = []
            for index, group in enumerate(groups):
                total = sum(len(a['raw']) + 1 for a in group)
                left_size = 0
                for split in range(1, len(group)):
                    left_size += len(group[split - 1]['raw']) + 1
                    if (any(a['message_ids'] for a in group[:split])
                            and any(a['message_ids'] for a in group[split:])):
                        choices.append((total, -abs(total - 2 * left_size), -index, split))
            if not choices:
                raise ValueError('Cannot partition native owners into all original slots')
            _, _, negative_index, split = max(choices)
            index = -negative_index
            group = groups[index]
            groups[index:index + 1] = [group[:split], group[split:]]
    if len(groups) != expected_groups:
        total_bytes = sum(len(atom['raw']) + 1 for atom in atoms)
        capacity = expected_groups * 4096
        raise ValueError(f'Greedy plan needs {len(groups)} blocks, expected {expected_groups}; '
                         f'{total_bytes} owner bytes for {capacity} cache bytes '
                         f'({max(0, total_bytes - capacity)} total-byte shortfall); '
                         'explicit redistribution required')
    rebuilt = list(container.blocks[:first_block])
    result_arm9 = bytearray(arm9)
    relocations, first_ids = [], []
    for block, group in enumerate(groups, first_block):
        message_ids = [i for atom in group for i in atom['message_ids']]
        if not message_ids:
            raise ValueError('Native directory cannot select an empty block')
        first = min(message_ids)
        first_ids.append(first)
        position, data = 0, bytearray()
        for record, atom in enumerate(group):
            data.extend(atom['raw'] + b'\0')
            for i, local in atom['starts'].items():
                struct.pack_into('<H', result_arm9, TABLE_OFFSET + i * 2, position + local)
            relocations.append({'old_owner': atom['old_owner'], 'new_owner': [block, record],
                                'message_ids': atom['message_ids'], 'raw_hex': atom['raw'].hex().upper()})
            position += len(atom['raw']) + 1
        rebuilt.append(bytes(data))
        struct.pack_into('<HH', result_arm9, DIRECTORY_OFFSET + block * 4, first, len(data))
    # Independently emulate the proven selector/copy loop; do not reuse the
    # source mapper because this intentional directory change is not registered.
    directory = [struct.unpack_from('<HH', result_arm9, DIRECTORY_OFFSET + b * 4) for b in range(41)]
    offsets = struct.unpack_from(f'<{MESSAGE_COUNT + 1}H', result_arm9, TABLE_OFFSET)
    if offsets[-1] != 0 or [d[0] for d in directory] != sorted({d[0] for d in directory}):
        raise ValueError('Invalid relocated directory or terminal sentinel')
    max_copy = 0
    for old in before:
        i = old.message_id
        block = max(b for b, (first, _) in enumerate(directory) if first <= i)
        start, following = offsets[i:i + 2]
        limit = following if following >= start else directory[block][1]
        if not 0 <= start < limit <= len(rebuilt[block]) <= 4096:
            raise ValueError(f'Message {i}: invalid relocated copy span')
        max_copy = max(max_copy, limit - start)
        selected = rebuilt[block][start:limit].split(b'\0', 1)[0]
        if i in preserved and selected != preserved[i]:
            raise ValueError(f'Message {i}: preserved neighbor bytes changed')
        if selected.rstrip(b' ') != authored.get(i, old.text).rstrip(b' '):
            raise ValueError(f'Message {i}: leading/end characters, controls or text changed')
    # Output buffer lies between +0x2030 and +0x2230 (512 bytes), including NUL.
    if max_copy >= 512:
        raise ValueError('A relocated copy overflows the mapped output buffer')
    for lo, hi, expected in CODE_LOCKS:
        if hashlib.sha256(result_arm9[lo:hi]).hexdigest() != expected:
            raise ValueError('Executable loader/selector changed')
    expected_arm9 = bytearray(arm9)
    expected_arm9[DIRECTORY_OFFSET:TABLE_OFFSET] = result_arm9[DIRECTORY_OFFSET:TABLE_OFFSET]
    expected_arm9[TABLE_OFFSET:TABLE_OFFSET + (MESSAGE_COUNT + 1) * 2] = result_arm9[TABLE_OFFSET:TABLE_OFFSET + (MESSAGE_COUNT + 1) * 2]
    if expected_arm9 != result_arm9:
        raise ValueError('Unrelated ARM9 bytes changed')
    report = {'status': 'research-plan-verified-not-integrated',
              'all_native_messages_compared': len(before), 'authored_ids': sorted(authored),
              'preserved_untranslated_ids': sorted(preserved),
              'first_reblocked_block': first_block, 'block_sizes': list(map(len, rebuilt)),
              'max_native_copy_bytes': max_copy, 'executable_code_unchanged': True,
              'all_unrelated_selected_text_unchanged': True,
              'compacted_english_padding': compacted,
              'removed_english_padding_bytes': sum(e['removed_spaces'] for e in compacted),
              'directory_sha256': hashlib.sha256(result_arm9[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest(),
              'relocations': relocations}
    return IlnkContainer(rebuilt).to_bytes(), bytes(result_arm9), report
