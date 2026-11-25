"""Bind the ending-save exchange and the separate legacy memory-card text."""

from hashlib import sha256
from pathlib import Path
from struct import unpack_from

from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts import observe_ending_save_20261120 as replay
from scripts import register_save_dialogue_followup_20261119 as save_review
from scripts import register_save_location_labels_20261119 as location_review
from scripts.seal_shared_text_source_v1 import ARM, CLEAN, COMMON, reference
from scripts.verify_captain_biographies_v1 import captured, shots
from scripts.verify_confirmed_name_widget_pixels_v198 import GameAsciiFont, complete_mask
from scripts.verify_save_location_labels_20261119 import DOCKED, HEADING, exact_mask


base, current = replay.base, replay.current
BOOK = Path('translations/editorial_checkpoints/SharedText_20261110_v1')
OUTPUT = BOOK / 'ending_save_scope_20261120_v1.json'
PENDING = BOOK / 'shared_display_worklist_20261120_v1.json'
LEGACY = BOOK / 'legacy_dialogue_review_20261115_v1.json'
GATES = ('source', 'context', 'localization', 'naturalness', 'formatting')
BASE = 0x02000000


def sha(data):
    return sha256(data).hexdigest()


def arm_record(key, pointer_offset, source, arm, expected, reason, context, arguments=()):
    spans = []
    for binary in (source, arm):
        address, = unpack_from('<I', binary, pointer_offset)
        offset = address - BASE
        end = binary.index(0, offset, offset + 128)
        assert all(binary[offset:end]) and end < offset + 128
        spans.append((dict(ARM9_sha256=sha(binary), pointer_field=BASE + pointer_offset,
                           runtime_pointer=address, offset=offset, bytes_with_terminator=end + 1 - offset),
                      binary[offset:end + 1]))
    (src, japanese), (dest, english) = spans
    assert english == expected.encode('ascii') + b'\0'
    assert japanese.count(b'%s') == english.count(b'%s') == len(arguments)
    return dict(id=key, file_path=ARM, decision='retention', source_reference=src, current_reference=dest,
                source_hex=japanese.hex(), current_hex=english.hex(), clean_Japanese=japanese[:-1].decode('cp932'),
                english=expected, context=context, localization_note=reason,
                runtime_substitutions=list(arguments), review=dict.fromkeys(GATES, True))


def common_record(number, clean, candidate):
    source, current_entry = clean[number], candidate[number]
    return dict(message_ID=number, file_path=COMMON, source_reference=reference(source),
                current_reference=reference(current_entry), source_hex=source.text.hex(),
                current_hex=current_entry.text.hex(), clean_Japanese=source.text.decode('cp932'),
                current_English=current_entry.text.decode('cp932'))


def proof_for_run(label, release):
    folder = replay.ROOT / label
    capture = folder / 'capture/capture_report.json'
    requests = folder / 'requests.json'
    contract = folder / 'source_contract.json'
    journal = folder / 'capture/navigation_command_journal.json'
    commands = folder / 'commands.json'
    report, trace, constraints, nav, supplied = map(base.load, (capture, requests, contract, journal, commands))
    assert report['ROM_sha256'] == nav['ROM_sha256'] == release['candidate_sha256']
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert not report['earned_completion_verified'] and not report['hardware_device_verification']
    fixture, = report['synthetic_ending_fixtures']
    assert fixture['changes'] == [dict(address=0x022796BC, before=1, after=4)]
    assert len(nav['commands_received']) == len(supplied)
    assert [r['command'] for r in nav['commands_received']] == supplied
    assert all(r['validation_passed'] for r in nav['commands_received'])
    assert report['frames'] == nav['last_command_frame']
    assert report['scripted_input_schedule'][:4] == base.load(replay.HISTORY / 'rafael_inputs.json')
    assert not trace['errors'] and trace['mismatches'] == 0 and trace['all_host_slots_restored_and_core_file_exact']
    assert trace['source_contract_sha256'] == base.digest(contract)
    assert constraints['ARM9_sha256'] == release['target_ARM9_sha256']
    assert {r['PC'] for r in constraints['targets']} == replay.TRACE_ARGUMENTS.keys()
    calls = trace['source_requests']
    ids = [r for r in calls if r['PC'] in replay.observe.REQUESTS]
    assert sorted((r['PC'], r['message_ID'], r['caller_LR']) for r in ids) == [
        (0x020534F4, 316, 0x02054680), (0x0205528C, 316, 0x02054680)]
    call_sites = [(r['frame'], r['PC'], r['caller_LR']) for r in calls if r['PC'] not in replay.observe.REQUESTS]
    assert call_sites == [(11258, replay.PROMPT, 0x0203E2FC)] + (
        [] if label == 'no' else [(12414, replay.SAVE, 0x0203E310)])
    donor = report['battery_save_preloaded']
    assert donor['copied_byte_exact_before_cold_boot'] and base.digest(donor['source']) == donor['source_sha256']
    original, output = (Path(donor[k]).read_bytes() for k in ('source', 'destination'))
    metadata_changes = []
    if label == 'confirm':
        assert len(original) == len(output) == donor['bytes']
        assert original[:0xA000] == output[:0xA000] and original[0x14000:0x3C000] == output[0x14000:0x3C000]
        assert original[0xA000:0x14000] == b'\xff' * 0xA000 and output[0xA000:0xA004] == b'DK4R'
        assert original[0x3C000:0x3C004] == output[0x3C000:0x3C004] == b'DK4R'
        metadata_changes = [(i, original[i], output[i]) for i in range(0x3C000, len(original)) if original[i] != output[i]]
        assert metadata_changes == [(0x3C004, 118, 120), (0x3C03C, 0, 1), (0x3C043, 0, 1)]
    else:
        assert original == output
    return report, dict(observed_COMMON=ids, observed_wrapper_entries=call_sites, test_save=donor,
                        final_save_sha256=sha(output), changed_save_bytes=sum(a != b for a, b in zip(original, output, strict=True)),
                        system_save_metadata_changes=metadata_changes,
                        evidence={str(p): base.digest(p) for p in (capture, requests, contract, journal, commands)})


def main():
    assert not OUTPUT.exists()
    release = base.load(current.RELEASE)
    rom = current.stage.ROOT / 'clean_rebuilt.nds'
    assert base.digest(rom) == base.digest(current.ROM) == release['candidate_sha256']
    assert base.digest(CLEAN) == release['clean_input_sha256']
    assert base.digest(current.PATCH) == release['patch_sha256'] and release['clean_input_patch_byte_exact']
    assert base.digest(base.REGISTRY) == release['registry_sha256']
    old, new = map(base.NdsImage.open, (CLEAN, rom))
    source, arm = old.read_file(ARM), new.read_file(ARM)
    assert sha(arm) == release['target_ARM9_sha256']
    assert source[0x3E16C:0x3E324] == arm[0x3E16C:0x3E324]
    assert arm[0x3E2F4:0x3E310].hex() == '4f0fa0e3db5800eb000050e30200000a04108de20500a0e15c0200eb'
    archive = new.read_file(COMMON)
    assert sha(archive) == release['target_COMMON_sha256']
    stock_entries = common_message_entries(old.read_file(COMMON), source)
    installed = owned_entries(archive, arm, sha(arm[DIRECTORY_OFFSET:TABLE_OFFSET]))
    legacy, prompt = (common_record(n, stock_entries, installed) for n in (119, 316))
    prior, = [r for r in base.load(PENDING)['records'] if r['message_ID'] == 119]
    assert all(legacy[k] == prior[k] for k in ('source_reference', 'current_reference', 'source_hex', 'current_hex'))
    draft, = [r for r in base.load(LEGACY)['records'] if r['message_ID'] == 119]
    legacy.update(decision='draft revision', draft_english=draft['english'], review=draft['review'],
                  finding='Both answers use the separate DS prompt at COMMON 316. An original caller elsewhere remains unverified.')
    assert prompt['current_English'] == 'Save the ending data?'
    prompt.update(decision='retention', runtime_substitutions=[], review=dict.fromkeys(GATES, True),
                  context='Immediately after the credits. No returns to title and Yes opens the save-slot picker.',
                  localization_note='Keep the direct question. Ending data identifies what the player is saving at this point.')

    init = 'Original save-slot picker opened after accepting the ending save.'
    records = [prompt,
        arm_record('DK4_SAVE_SELECT_TITLE', 0xEF6B0, source, arm, 'Select a save slot.',
                   'A concise instruction applies equally to occupied and unused slots.', init),
        arm_record('DK4_SAVE_DOCKED', 0xEF6C4, source, arm, ' Docked',
                   'The status and leading space keep the location and its state legible on the occupied row.', init),
        arm_record('DK4_SAVE_UNUSED', 0xEFCD8, source, arm, 'Unused',
                   'The single word clearly identifies a slot with no previous save.', init),
        arm_record('DK4_SAVE_CREATE_CONFIRM', 0xEEC2C, source, arm, 'Create a new save?',
                   'The original separate agreement question reads naturally as one direct question in English.',
                   'The player selected an unused slot and can still cancel.'),
        arm_record('DK4_SAVE_PROGRESS_ACTION', 0xEF2B0, source, arm, 'Save',
                   'The action noun reads naturally in the shared progress format.',
                   'Fills the original progress format while the game writes the new save.'),
        arm_record('DK4_SAVE_PROGRESS_FORMAT', 0xEF2B8, source, arm, '%s in progress.\n Do not turn off.',
                   'The break keeps the complete status on one line and the safety instruction on the next.',
                   'The warning stays visible while the device writes the save.', ('Save or Load',))]

    samples = {}
    frames = {}
    for label in ('no', 'yes', 'save', 'confirm'):
        report, samples[label] = proof_for_run(label, release)
        frames[label] = shots(report)
    assert frames['confirm'][15200]['framebuffer_sha256'] == frames['no'][13100]['framebuffer_sha256']
    assert samples['confirm']['changed_save_bytes'] > 0
    font = GameAsciiFont.from_arm9(arm)
    holds = []
    for label in frames:
        capture = frames[label][12400]
        count, bounds = complete_mask(font, 'Save the ending data?', captured(capture), 16, 297, (0, 8, 0))
        assert count == 239
        holds.append(dict(record=316, capture=capture, bounds=bounds, complete_ink=count))
    picker = frames['yes'][13100]
    panel = captured(picker)
    for key, text, rect in (('DK4_SAVE_SELECT_TITLE', 'Select a save slot.', HEADING),
                            ('DK4_SAVE_DOCKED', 'Lisbon Docked', DOCKED),
                            ('DK4_SAVE_UNUSED', 'Unused', (5, 228, 50, 249))):
        holds.append(dict(record=key, capture=picker, **exact_mask(panel, font, text, rect)))
    for key, frame, line, x, y in (('DK4_SAVE_CREATE_CONFIRM', 14100, 'Create a new save?', 16, 297),
                                   ('DK4_SAVE_PROGRESS_FORMAT', 14280, 'Save in progress.', 56, 277),
                                   ('DK4_SAVE_PROGRESS_FORMAT', 14280, 'Do not turn off.', 56, 289)):
        capture = frames['confirm'][frame]
        count, bounds = complete_mask(font, line, captured(capture), x, y, (0, 8, 0))
        assert count > 0 and bounds[2] <= (245 if frame == 14100 else 207)
        holds.append(dict(record=key, line=line, capture=capture, bounds=bounds, complete_ink=count))
    for label, frame in (('no', 13100), ('confirm', 15200)):
        captured(frames[label][frame])

    evidence = (current.RELEASE, replay.EARLIER, PENDING, LEGACY, save_review.REVIEW,
                location_review.REVIEW, Path(replay.__file__), Path(__file__))
    base.save(OUTPUT, dict(translation_policy='natural-dialogue-v2', target_locale='en-US', review_gates=GATES,
        candidate_sha256=release['candidate_sha256'], clean_input_sha256=release['clean_input_sha256'],
        records=records, legacy_memory_card=legacy, replay=samples, native_glyph_holds=holds,
        no_title_capture=frames['no'][13100], yes_title_capture=frames['confirm'][15200],
        exact_end_selector_call_span=[0x0203E2F4, 0x0203E310], exact_orig_save_picker_pointer_checks=True,
        rendered_lines_are_single_page=True, hardware=False, naturally_earned_ending=False,
        no_ROM_change=True, new_editorial_credit=0, full_goal_complete=False,
        evidence={str(p): base.digest(p) for p in evidence}))
    print(f'{len(records)} contextual retentions; {len(holds)} glyph masks; Yes saves to the isolated unused slot.')


if __name__ == '__main__':
    main()
