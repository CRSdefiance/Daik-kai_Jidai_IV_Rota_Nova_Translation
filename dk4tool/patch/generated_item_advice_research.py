"""Include all twenty native generated maps in the terminated paragraph table."""

import copy
import struct

from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL, STAGE, cache_plan, wrapper
from dk4tool.script.common_message_table import common_message_entries
from scripts.probe_common_display_name_hook import branch_link

SOURCE = 'd5f49394f4bf6dad6647226b6bcf0f505e5a87bff75100ac486f398c857c92fc'
COMMON = 'ea978f466496f8593f13fb97f17b9bac174beea5665c57f1f5e358b2808776c9'


def transform(source, common, original_plan):
    if sha(source) != SOURCE or sha(common) != COMMON:
        raise ValueError('Exact parent-repaired item source and unchanged COMMON required')
    code = MainCodeFile(source, BASE)
    before = [bytes(s.data) for s in code.sections]
    cache_plan(source)
    packed = bytearray(before[3][:-48])
    helpers = {r['kind']: r for r in original_plan['main_pool_helpers']}
    getter = helpers['advice_lookup']['start']
    relative = getter - POOL
    table = struct.unpack_from('<I', packed, relative + 44)[0]
    if (struct.unpack_from('<I', packed, relative + 20)[0] != 0xE35400C6
            or table != original_plan['advice_table']
            or len(original_plan['item_advice_projection']) != 198):
        raise ValueError('Original 198-entry paragraph getter/table differs')
    pointers = list(struct.unpack_from('<198I', packed, table - POOL))
    entries = common_message_entries(common, source, clean=False)
    extra = []
    paragraph = b'Map fragment. Collect all four.'
    paragraph_pointer = POOL + len(packed)
    packed.extend(paragraph + b'\0\0')
    for index in range(198, 218):
        original = entries[index + 0xAFF].text
        if b' '.join(original.split()) != paragraph:
            raise ValueError('Generated map COMMON paragraph is not the mapped single line')
        pointers.append(paragraph_pointer)
        extra.append({'message_id': index + 0xAFF, 'source_hex': original.hex(),
                      'logical': paragraph.decode('ascii'), 'compiled': paragraph.decode('ascii'),
                      'pointer': paragraph_pointer})
    packed.extend(bytes((-len(packed)) % 4))
    new_table = POOL + len(packed)
    packed.extend(struct.pack('<218I', *pointers))
    struct.pack_into('<I', packed, relative + 20, 0xE35400DA)
    struct.pack_into('<I', packed, relative + 44, new_table)
    packed.extend(bytes((-len(packed)) % 32))
    size = len(packed) + 64
    entry, copy_entry = STAGE + len(packed), STAGE + size
    packed.extend(wrapper(entry, copy_entry, size, source))
    code.sections[3].data = packed + before[3][-48:-4] + struct.pack('<I', size)
    struct.pack_into('<I', code.sections[0].data, 0x8E4, branch_link(BASE + 0x8E4, entry))
    struct.pack_into('<I', code.sections[0].data, 0xE45DC, POOL + size)
    saved = bytes(code.save())
    loaded = MainCodeFile(saved, BASE)
    restored = bytearray(loaded.sections[0].data)
    for field in (0x8E4, 0xE45DC):
        restored[field:field + 4] = before[0][field:field + 4]
    at = code.codeSettingsOffs
    restored[at:at + 12] = before[0][at:at + 12]
    prefix = bytearray(loaded.sections[3].data[:len(before[3]) - 48])
    for offset in (relative + 20, relative + 44):
        prefix[offset:offset + 4] = before[3][offset:offset + 4]
    if (bytes(restored) != before[0] or any(bytes(loaded.sections[i].data) != before[i] for i in (1, 2))
            or bytes(prefix) != before[3][:-48]):
        raise ValueError('Generated map repair changes unrelated code/text/parent positions')
    plan = copy.deepcopy(original_plan)
    plan.update(source_arm9_sha256=sha(source), target_arm9_sha256=sha(saved),
                advice_table=new_table, pool_payload_bytes=size,
                pool_used_bytes=size, cache_entry=entry,
                final_pool_span=[POOL, POOL + size], staging_span=[STAGE, STAGE + size + 48],
                copy_entry=copy_entry, item_advice_projection=plan['item_advice_projection'] + extra,
                generated_map_repair={'old_advice_count': 198, 'new_advice_count': 218,
                                      'prior_presentation_bytes_preserved': len(before[3]) - 48,
                                      'changed_prefix_fields': [getter + 20, getter + 44],
                                      'cache': cache_plan(saved),
                                      'reason': 'Native generated maps 198..217 use single strings; the multiline helper requires compiler-terminated paragraphs.'},
                status='218-item-paragraph-research-verification-pending')
    return saved, plan
