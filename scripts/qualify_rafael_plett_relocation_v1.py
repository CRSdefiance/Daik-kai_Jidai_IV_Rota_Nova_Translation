"""Qualify actor 65's surname in existing, explicitly derived staged alignment padding."""
from pathlib import Path
import struct

from ndspy.code import MainCodeFile

from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL, STAGE, cache_plan
from dk4tool.patch.owned_name_fields_v2 import plan_arm9_name_fields
from dk4tool.rom.nds import NdsImage
from scripts.qualify_rafael_B261_B280_surnames_v1 import CLEAN, OUT
from scripts.write_rafael_B261_B280_contextual_v1 import LABELS, load, save, sha


REGISTRY = Path('translations/release_stack.json')
ITEM = Path('translations/shachihoko_item116_editorial_release_v1.json')
OWNERSHIP = OUT / 'ownership_verification.json'
FIXED = OUT / 'jacob_portunto_native_proposal.json'
REFERENCE = OUT / 'plett_and_jacob_plan_v1'


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def raw_hits(data, start, end):
    hits = []
    for value in range(start, end):
        word = struct.pack('<I', value)
        offset = data.find(word)
        while offset >= 0:
            hits.append((offset, value))
            offset = data.find(word, offset + 1)
    return sorted(hits)


def plan_surnames(arm, proposal, clean):
    require(proposal['format'] == 'dk4-rafael-B261-B280-surnames-v1', 'Scoped surname format required')
    require(sha(arm) == proposal['runtime']['ARM9_sha256'], 'Exact registered ARM9 required')
    require(sha(clean) == proposal['clean_ARM9_sha256'], 'Exact clean ARM9 required')
    plett, jacob = proposal['fields']
    require(plett == proposal['qualified_plett'], 'Exact individually reviewed Plett field required')
    require((plett['actor'], jacob['actor'], plett['column'], jacob['column']) == (65, 68, 4, 4), 'Only the two surnames are owned')
    require(all(plett['review'][gate] for gate in ('source', 'context', 'localization', 'naturalness')), 'Plett editorial gates required')
    fixed, fixed_proof = plan_arm9_name_fields(arm, {**proposal, 'format': 'dk4-owned-name-fields-proposal-v2',
                                                    'fields': [jacob]}, clean)
    old = bytes.fromhex(plett['source_hex'])
    field, pointer, at = (plett[key] for key in ('table_field_offset', 'pointer', 'physical_offset'))
    require((field, pointer, at, old) == (1184676, BASE + 1424360, 1424360, b'Perot'), 'Exact source surname location required')
    require(arm[at:at+16] == b'Perot\0\0\0Sakura\0\0', 'Original surname and adjacent Sakura must be exact')
    require(clean[at:at+8] == 'ペロー'.encode('cp932') + b'\0\0', 'Clean surname identity differs')
    require(raw_hits(arm, pointer, pointer + 8) == [(field, pointer)], 'Unexpected original slot pointer')
    target = (plett['target_text'] + '\0').encode('ascii')
    require(target == b'Perrault\0', 'Exact approved English surname required')

    plan = proposal['source_owned_item_alignment']
    span_start, span_end = plan['newly_appended_source_owned_text_span']
    item_text = bytes.fromhex(plan['compiled_paragraph_hex'])
    parsed = MainCodeFile(arm, BASE)
    staged = bytes(parsed.sections[3].data)
    stage_offset = arm.find(staged)
    require(stage_offset >= 0 and arm.find(staged, stage_offset + 1) < 0, 'Unique complete staged data')
    cache = cache_plan(arm)
    wrapper_start = cache['entry'] - STAGE
    require(cache['payload_bytes'] == 123264 and (span_start, span_end, wrapper_start) == (123040, 123176, 123200),
            'Current exact item and cache geometry required')
    require(staged[span_start:span_end] == item_text and item_text.endswith(b'\0\0'), 'Complete item prose required')
    require(not any(staged[span_end:wrapper_start]), 'The entire recorded alignment reserve must still be zero')
    require(struct.unpack_from('<I', staged, plan['active_compiled_pointer_field_payload_offset'])[0] == POOL + span_start,
            'Original item pointer must still reference the prose')
    require(span_end % 4 == 0 and span_end + len(target) < wrapper_start, 'Aligned bounded surname allocation required')
    address = POOL + span_end
    require(not raw_hits(arm, address, POOL + wrapper_start), 'Unexpected reference into the item alignment reserve')

    new_at = stage_offset + span_end
    result = bytearray(fixed)
    struct.pack_into('<I', result, field, address)
    result[new_at:new_at + len(target)] = target
    result = bytes(result)
    out = MainCodeFile(result, BASE)
    require(cache_plan(result) == cache and bytes(out.sections[3].data[wrapper_start:]) == staged[wrapper_start:],
            'Existing cache, copy and heap geometry must remain exact')
    require(bytes(out.sections[3].data[span_start:span_end]) == item_text, 'Item prose must remain exact')
    require(raw_hits(result, address, POOL + wrapper_start) == [(field, address)], 'Only actor 65 may reference the new slot')
    table = struct.unpack_from('<I', arm, 0xCDAC0)[0] - BASE
    fields = [table + 32 * actor + column for actor in range(207) for column in (0, 4, 8)]
    require([f for f in fields if arm[f:f+4] != result[f:f+4]] == [field], 'Exactly one of 621 pointers may change')
    require([(s.ramAddress, s.bssSize, len(s.data)) for s in out.sections] ==
            [(s.ramAddress, s.bssSize, len(s.data)) for s in parsed.sections], 'Section and BSS extents must remain exact')
    inverse = bytearray(result)
    for offset, extent in ((field, 4), (new_at, len(target)), (jacob['physical_offset'], jacob['owned_bytes'])):
        inverse[offset:offset+extent] = arm[offset:offset+extent]
    require(bytes(inverse) == arm, 'Exact complete ARM9 inverse required')
    return result, dict(
        fixed_jacob_proof=fixed_proof, parent_ARM9_sha256=sha(arm), target_ARM9_sha256=sha(result),
        old_surname_slot=[at, at+8], old_surname_and_adjacent_Sakura_preserved=True, actor65_pointer_field=field,
        new_surname_physical_span=[new_at, new_at+len(target)], new_surname_runtime_pointer=address,
        reused_alignment_reserve=[span_end, wrapper_start], source_item_text_span=[span_start, span_end],
        only_one_of_621_pointers_changed=True, cache_plan=cache, original_item_pointer_copy_code_heap_and_section_geometry_exact=True,
        all_unowned_bytes_exact=True, complete_parent_inverse_exact=True, new_credit=0,
    )


def main():
    assert not REFERENCE.exists()
    names, ownership, fixed, item = map(load, (LABELS, OWNERSHIP, FIXED, ITEM))
    runtime = ownership['runtime']
    release = load(runtime['release_proof'])
    assert runtime == fixed['runtime'] == names['runtime']
    assert sha(REGISTRY.read_bytes()) == release['registry_sha256']
    assert Path(load(REGISTRY)['profiles'][release['profile']]['shachihoko_item116_editorial']) == ITEM
    source_item = Path(item['manuscript'])
    assert sha(source_item.read_bytes()) == item['dependencies'][str(source_item)]
    plan = load(source_item)['native_data_plan']
    parent = NdsImage.open(runtime['candidate'])
    assert sha(Path(runtime['candidate']).read_bytes()) == runtime['candidate_sha256']
    arm = parent.read_file('/__arm9__.bin')
    clean = NdsImage.open(CLEAN).read_file('/__arm9__.bin')
    actor = next(row for row in names['records'] if row['actor_ID'] == 65)
    assert actor['approved_forms']['progressive-nameplate'] == 'Plett Perrault'
    plett = {**ownership['plett'], 'target_hex': b'Perrault\0'.hex()}
    proposal = {**fixed, 'format': 'dk4-rafael-B261-B280-surnames-v1', 'fields': [plett, *fixed['fields']],
                'qualified_plett': plett, 'source_owned_item_alignment': plan, 'clean_ARM9_sha256': sha(clean)}
    target, proof = plan_surnames(arm, proposal, clean)
    lo, hi = proof['reused_alignment_reserve']
    pixel_coincidences = []
    for path, data in [(p, v) for _, p, v in parent.iter_files()] + list(parent.iter_components()):
        if path == '/__arm9__.bin':
            continue
        hits = raw_hits(data, POOL + lo, POOL + hi)
        if hits:
            assert path == '/evstill/evstill172.pxl' and hits == [(37957, 37378901)], (path, hits)
            picture = PxlImage.from_bytes(data)
            assert picture.pixels_offset <= hits[0][0] and hits[0][0] + 4 <= len(data)
            assert picture.to_bytes() == data
            pixel_coincidences.append(dict(path=path, sha256=sha(data), matches=hits,
                 pixel_offset=picture.pixels_offset, width=picture.width, height=picture.height))
    assert len(pixel_coincidences) == 1
    REFERENCE.mkdir()
    save(REFERENCE/'proposal.json', proposal)
    save(REFERENCE/'proof.json', {**proof, 'raw_ROM_byte_match_is_inside_an_exact_roundtrip_pixel_plane': pixel_coincidences,
         'all_other_raw_ROM_file_and_component_reserve_pointer_censuses_empty': True,
         'reference_only_no_ROM_written': True, 'native_consumers_and_candidate_startup_pending': True,
         'evidence': {str(path): sha(path.read_bytes()) for path in (REGISTRY, ITEM, source_item, OWNERSHIP, FIXED, LABELS)}})
    (REFERENCE/'corrected_ARM9_RESEARCH_ONLY.bin').write_bytes(target)
    print('Both surname spans and whole-ARM9 inverse passed. Plett fits the documented 24-byte alignment reserve.')


if __name__ == '__main__':
    main()
