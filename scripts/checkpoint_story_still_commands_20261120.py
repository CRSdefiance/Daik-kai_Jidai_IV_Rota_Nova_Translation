"""Tie stored scene labels to actual clean and installed story-still operands."""

import inspect
import re
from collections import Counter, defaultdict
from pathlib import Path
from struct import pack, unpack_from

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_SP

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from scripts import checkpoint_shared_display_owners_20261119 as owners
from scripts import checkpoint_shared_display_worklist_20261120 as worklist
from scripts import register_tavern_help_20261120 as registered
from scripts import research_wedding_command_v676 as interpreter


BOOK = owners.BOOK
ARTWORK = BOOK / 'scene_caption_artwork_20261119_v1.json'
OUTPUT = BOOK / 'story_still_commands_20261120_v1.json'
# Scan every byte first so the boundary check can reject text and operand coincidences.
POSSIBLE = re.compile(rb'(?=.\x46.[\x80-\xff])', re.DOTALL)


def explicit_walk():
    """Keep the proven command walk with a deterministic unmatched branch result."""
    source = inspect.getsource(interpreter.walk)
    changes = {
        '(RESULT, OWNER, LENGTH), instruction_limit=20000':
            '(RESULT, OWNER, LENGTH, 0xFFFFFFFF), instruction_limit=20000',
        "block[:4] == b'CS\\0\\1'":
            "block[:4] in (b'CS\\0\\1', b'CS\\1\\1')",
    }
    for old, new in changes.items():
        assert source.count(old) == 1
        source = source.replace(old, new)
    namespace = dict(vars(interpreter))
    exec(compile(source, __file__, 'exec'), namespace)
    return namespace['walk']


def commands(walk, arm, block):
    candidates = {match.start() for match in POSSIBLE.finditer(block, 8)}
    found, unknown = {}, []
    if not candidates:
        return candidates, found, unknown

    def visit(start, end, ancestors):
        body = block[start:end]
        window = block[:4] + pack('<2H', len(body), 0) + body
        trace = walk(arm, window)
        still_calls = defaultdict(list)
        for bridge in trace['opaque_effect_bridges']:
            if bridge['PC'] == 0x02028AA8:
                still_calls[start + bridge['source_offset'] - 8].append(bridge)
        for row in trace['rows']:
            offset = start + row['offset'] - 8
            extent = row['native_extent']
            word = row['word']
            if offset in candidates and word >> 8 == 0x46:
                assert extent == 4 and row['result'][:8] == '03000000'
                operand = unpack_from('<H', block, offset + 2)[0]
                call, = still_calls[offset]
                assert call['LR'] == 0x02029FB8 and call['args'][1] == operand & 0xFF
                found[offset] = dict(
                    byte_offset=offset, opcode=f'{word:04X}', operand=f'{operand:04X}',
                    image_index=operand & 0xFF, ancestor_0100_offsets=ancestors,
                    command_hex=block[offset:offset + extent].hex(), native_scene_call=call['PC'],
                )
            if word == 0x0100:
                assert extent == 4 + unpack_from('<H', block, offset + 2)[0]
                if any(offset + 4 <= at < offset + extent for at in candidates):
                    visit(offset + 4, offset + extent, [*ancestors, offset])
        if trace['error'] is not None:
            stop = start + trace['stopped_offset'] - 8
            unresolved = sorted(at for at in candidates if stop <= at < end)
            if unresolved:
                unknown.append(dict(
                    byte_offsets=unresolved, error=trace['error'],
                    stopped_at=stop, window_end=end, ancestor_0100_offsets=ancestors,
                ))

    limit = 8 + unpack_from('<H', block, 4)[0]
    assert block[:4] in (b'CS\0\1', b'CS\1\1') and limit <= len(block) and not any(block[limit:])
    visit(8, limit, [])
    return candidates, found, unknown


def inventory(rom, walk, cache):
    arm = rom.read_file('/__arm9__.bin')
    arm_hash = interpreter.sha(arm)
    event_commands, archives = {}, {}
    for directory in ('data', 'testdata'):
        for route in range(4):
            path = f'/{directory}/SC{route}.DK4'
            archive = rom.read_file(path)
            blocks = IlnkContainer.parse(archive).blocks
            stats = Counter(blocks=len(blocks))
            errors = []
            for number, block in enumerate(blocks):
                # Hash full ARM9 and block so reuse cannot hide a relevant change.
                key = arm_hash, block
                if key not in cache:
                    cache[key] = commands(walk, arm, block)
                possible, positives, unresolved = cache[key]
                stats['raw_candidates'] += len(possible)
                stats['native_still_commands'] += len(positives)
                unknown_at = {at for error in unresolved for at in error['byte_offsets']}
                stats['unresolved_candidates'] += len(unknown_at)
                stats['rejected_lookalikes'] += len(possible - positives.keys() - unknown_at)
                if positives:
                    block_hash = interpreter.sha(block)
                    event_commands[path, number] = [
                        dict(row, path=path, block=number, block_sha256=block_hash)
                        for _, row in sorted(positives.items())
                    ]
                errors.extend(dict(error, block=number) for error in unresolved)
            archives[path] = dict(archive_sha256=interpreter.sha(archive),
                                  counts=dict(stats), unresolved=errors)
            print(path, dict(stats), flush=True)
    return event_commands, archives


def image_requests(arm, indices):
    """Follow both original scene-parent branches through the filename read."""
    cpu = owners.machine(arm)
    requests = []
    mode = owners.STREAM

    def hook(uc, pc, _size, _user):
        if pc in (owners.GETTER, owners.COPIER):
            raise AssertionError(f'Image preparation requested COMMON text at {pc:#x}')
        if pc == 0x02021C14:
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
        elif pc == 0x020D4170:
            uc.reg_write(UC_ARM_REG_R0, owners.VIEW)
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
        elif pc == 0x020B7158:
            assert uc.reg_read(UC_ARM_REG_R0) == owners.VIEW
            addr = uc.reg_read(UC_ARM_REG_R1)
            requests.append(bytes(uc.mem_read(addr, 32)).split(b'\0', 1)[0].decode('ascii'))
            uc.emu_stop()

    hook_handle = cpu.hook_add(UC_HOOK_CODE, hook)
    try:
        for index in indices:
            for flags in ((0, 0, 0), (1, 0, 1)):
                cpu.mem_write(mode, pack('<3I', *flags))
                cpu.reg_write(UC_ARM_REG_R0, owners.OWNER)
                cpu.reg_write(UC_ARM_REG_R1, index)
                cpu.reg_write(UC_ARM_REG_R2, mode)
                cpu.reg_write(UC_ARM_REG_SP, owners.STACK)
                old_count = len(requests)
                cpu.emu_start(0x02028AA8, 0x02028BAC, count=10000)
                assert len(requests) == old_count + 1 and cpu.reg_read(UC_ARM_REG_PC) == 0x020B7158
                assert requests[-1] == f'/evstill/evstill{index:03d}.pxl'
    finally:
        cpu.hook_del(hook_handle)
    return len(requests)


def scene_labels(images, artwork):
    shared = registered.base.load(worklist.OUTPUT)
    clean, installed = images['clean'], images['installed']
    common, arm_path = worklist.COMMON, worklist.ARM
    workflow = worklist.current.stage.workflow
    arm = installed.read_file(arm_path)
    directory_hash = workflow.digest(arm[workflow.DIRECTORY_OFFSET:workflow.TABLE_OFFSET])
    current_rows = workflow.owned_entries(installed.read_file(common), arm, directory_hash)
    clean_rows = workflow.common_message_entries(clean.read_file(common), clean.read_file(arm_path))
    references = {}
    for row in shared['records']:
        key = row['message_ID']
        assert workflow.reference(current_rows[key]) == row['current_reference']
        assert workflow.reference(clean_rows[key]) == row['source_reference']
        assert current_rows[key].text.hex() == row['current_hex']
        assert clean_rows[key].text.hex() == row['source_hex']
        if row['kind'] == 'scene':
            references[key] = row
    assert set(references) == {r['message_ID'] for r in artwork['records']}
    return references


def main():
    base = registered.base
    release, ledger, artwork = map(base.load, (registered.RELEASE, base.LEDGER, ARTWORK))
    head = ledger['current_integrated_candidate']
    assert base.digest(base.REGISTRY) == release['registry_sha256']
    assert base.digest(registered.ROM) == head['sha256'] == release['candidate_sha256']
    clean = registered.stage.CLEAN
    assert base.digest(clean) == release['clean_input_sha256']
    assert not OUTPUT.exists()
    walk = explicit_walk()
    images = {'clean': NdsImage.open(clean), 'installed': NdsImage.open(registered.ROM)}
    stored_rows = scene_labels(images, artwork)
    cache = {}
    inventories, archive_results = {}, {}
    for version, rom in images.items():
        print(version, flush=True)
        inventories[version], archive_results[version] = inventory(rom, walk, cache)

    matches = defaultdict(list)
    differing_blocks = []
    for key in sorted(inventories['clean'].keys() | inventories['installed'].keys()):
        left = inventories['clean'].get(key, [])
        right = inventories['installed'].get(key, [])
        if [r['command_hex'] for r in left] != [r['command_hex'] for r in right]:
            differing_blocks.append(dict(path=key[0], block=key[1], source=left, current=right))
            continue
        for source, current in zip(left, right, strict=True):
            matches[source['image_index']].append(dict(source=source, current=current))

    asset_rows = []
    for index, locations in sorted(matches.items()):
        path = f'/evstill/evstill{index:03d}.pxl'
        hashes = {version: interpreter.sha(rom.read_file(path)) for version, rom in images.items()}
        asset_rows.append(dict(image_index=index, filename=path, asset_hashes=hashes, commands=locations))
    requests = {v: image_requests(rom.read_file('/__arm9__.bin'), sorted(matches)) for v, rom in images.items()}

    labels = []
    for row in artwork['records']:
        before = stored_rows[row['message_ID']]
        assert row['installed_hex'] == before['current_hex'] and row['source_reference'] == before['source_reference']
        index = row['image_index']
        labels.append(dict(
            message_ID=row['message_ID'], source_reference=before['source_reference'],
            current_reference=before['current_reference'], exact_installed_hex=before['current_hex'],
            Japanese=row['source_Japanese'], editorial_decision=row['contextual_decision'],
            English_manuscript=row['draft_english'], artwork_association=row['disposition'],
            image_index=index, data_command_count=sum(r['source']['path'].startswith('/data/')
                                                       for r in matches.get(index, ())),
            testdata_command_count=sum(r['source']['path'].startswith('/testdata/')
                                          for r in matches.get(index, ())),
            stored_COMMON_display_gate='open; the verified still command requests the image by filename',
        ))

    payload = dict(
        clean_sha256=release['clean_input_sha256'], candidate_sha256=head['sha256'],
        registry_sha256=release['registry_sha256'], artwork_receipt=str(ARTWORK),
        artwork_receipt_sha256=base.digest(ARTWORK), command_walk_sha256=base.digest(Path(interpreter.__file__)),
        shared_worklist_sha256=base.digest(worklist.OUTPUT),
        archive_results=archive_results, assets=asset_rows, differing_blocks=differing_blocks, labels=labels,
        native_scene_parent_file_requests=requests,
        counts=dict(both_versions_matching_assets=len(asset_rows),
                    matching_data_commands=sum(r['source']['path'].startswith('/data/')
                                               for rows in matches.values() for r in rows),
                    matching_testdata_commands=sum(r['source']['path'].startswith('/testdata/')
                                                   for rows in matches.values() for r in rows),
                    COMMON_labels_with_real_data_commands=sum(bool(r['data_command_count']) for r in labels)),
        scope='Original interpreter command extents with scene effects bridged. Filename formatter runs '
              'to its file-read boundary without COMMON requests. Neither script branch eligibility '
              'nor alternate archive selection was exercised in gameplay.',
        new_editorial_credit=0, new_gameplay_runs=0,
    )
    print(payload['counts'], 'different blocks', len(differing_blocks), flush=True)
    base.save(OUTPUT, payload)


if __name__ == '__main__':
    main()
