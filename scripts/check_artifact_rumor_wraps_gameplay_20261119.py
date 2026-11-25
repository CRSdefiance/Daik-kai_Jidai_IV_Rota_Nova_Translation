"""Verify the live King's Shield page and unaffected Guild transition frames."""

from pathlib import Path
from struct import unpack_from
from types import FunctionType

from PIL import ImageChops

from scripts import check_twisted_horn_rumor_gameplay_20261119 as prior
from scripts import replay_artifact_rumor_wraps_20261119 as replay
from scripts import stage_artifact_rumor_wraps_20261119 as stage

base = stage.base
PROOF = stage.ROOT / 'initialized_gameplay.json'


def main():
    assert not PROOF.exists()
    files = (stage.PROOF, replay.RECEIPT, replay.PARENT_CAPTURE, replay.CAPTURE / 'capture_report.json',
             replay.ROOT / 'inputs.json', replay.ROOT / 'requests.json')
    stored, fixture, old, new, inputs, requests = map(base.load, files)
    assert base.digest(stage.ROM) == stored['candidate_sha256'] == fixture['candidate_sha256'] == new['ROM_sha256']
    assert stored['predecessor_sha256'] == fixture['original_ROM_sha256'] == old['ROM_sha256'] == base.digest(stage.parent.ROM)
    assert all(base.digest(path) == sha for path, sha in fixture['evidence'].items())
    assert new['frames'] == replay.END and new['scripted_input_schedule'] == inputs
    assert inputs == [r for r in old['scripted_input_schedule'] if r['start'] + r['duration'] <= replay.END]
    assert old['core_DLL_sha256'] == new['core_DLL_sha256'] and old['core_options'] == new['core_options']
    for dossier in (old, new):
        assert dossier['cold_boot'] and not dossier['savestate_loaded'] and not dossier['callback_errors']
        assert not any(value for key, value in dossier.items() if key.startswith('synthetic_'))
    donors = [r['battery_save_preloaded'] for r in (old, new)]
    assert all(d['copied_byte_exact_before_cold_boot'] and base.digest(d['source']) == d['source_sha256'] for d in donors)
    assert donors[0]['source_sha256'] == donors[1]['source_sha256']
    assert fixture['runtime_table_restored'] and not fixture['natural_selection'] and fixture['no_rom_code_text_or_script_fixture']
    assert requests['all_host_slots_restored_and_core_file_exact'] and not requests['errors'] and not requests['mismatches']
    observed = [r for r in requests['source_requests'] if replay.INSERT <= r['frame'] < replay.RESTORE and r['message_ID'] >= 3658]
    assert fixture['actual_COMMON_requests'] == observed and len(observed) == 2
    assert {r['message_ID'] for r in observed} == {replay.ID}
    expected_ops = (dict(frame=replay.INSERT, address=replay.TABLE, before=replay.FIRST_SLOT,
                         after=replay.SHIELD, all_other_WRAM_exact=True),
                    dict(frame=replay.RESTORE, address=replay.TABLE, before=replay.SHIELD,
                         after=replay.FIRST_SLOT, all_other_WRAM_exact=True))
    assert tuple(fixture['temporary_runtime_input']) == expected_ops

    evidence = {str(p): base.digest(p) for p in files}
    snapshots = {r['frame']: r for r in new['read_only_capture_RAM_snapshots']}
    for frame, expected in ((replay.INSERT - 1, replay.FIRST_SLOT), (prior.FRAME, replay.SHIELD), (57220, replay.FIRST_SLOT)):
        snapshot = snapshots[frame]
        raw = Path(snapshot['path']).read_bytes()
        assert snapshot['read_only_export'] and base.digest(snapshot['path']) == snapshot['sha256']
        assert unpack_from('<I', raw, replay.TABLE - 0x02000000)[0] == expected
        evidence[snapshot['path']] = snapshot['sha256']

    frames = [{s['frame']: s for s in r['frames_captured']} for r in (old, new)]
    changed = [frame for frame in replay.FRAMES if frames[0][frame]['framebuffer_sha256'] != frames[1][frame]['framebuffer_sha256']]
    assert changed == [prior.FRAME], changed
    unchanged = sorted(set(replay.FRAMES) - set(changed))
    for frame in unchanged:
        for photo in (r[frame] for r in frames):
            assert base.digest(photo['path']) == photo['PNG_sha256']
            evidence[photo['path']] = photo['PNG_sha256']
    rom = base.NdsImage.open(stage.ROM)
    arm, font = (rom.read_file(p) for p in (stage.ARM, '/GRP/KANJI.FNT'))
    raster, _, _ = stage.golden.fleet.portrait.font_tools(rom)
    row, = (r for r in stored['records'] if r['message_ID'] == replay.ID)
    frame, hold = prior.verify_hold(new, frames[1], bytes.fromhex(row['staged_hex']), row['visible_lines'], arm, font,
        raster, 'read_only_capture_RAM_snapshots', evidence)
    old_frame = prior.portrait_sheet.deck.captured(frames[0][prior.FRAME])
    bounds = ImageChops.difference(old_frame, frame).getbbox()
    x, y, right, bottom = bounds
    assert prior.CROP[0] <= x < right <= prior.CROP[2] and prior.CROP[1] <= y < bottom <= prior.CROP[3]
    prompt = prior.portrait_sheet.deck.captured(frames[1][57220])
    sheet = FunctionType(prior.portrait_sheet.sheet.__code__, vars(prior.portrait_sheet) | {'ROOT': stage.ROOT})([
        ("King's Shield / complete rumor", frame), ('Guild purchase prompt / original return', prompt)])
    base.save(PROOF, dict(candidate_sha256=stored['candidate_sha256'], predecessor_sha256=stored['predecessor_sha256'],
        initialized_gameplay=True, natural_selection=False, hardware=False, observed_message_ID=replay.ID,
        observed_hold=hold, unchanged_frames=unchanged, purchase_prompt_frame=57220, item_list_frame=57460,
        full_native_glyph_masks_equal=True, live_expanded_and_wrapped_bytes_verified=True,
        runtime_table_restored=True, other_revised_messages_checked_offline=[3661, 3664],
        sheets=[sheet], evidence=evidence))
    print("The King's Shield complete glyphs and Guild return verified. Rose Quartz and Witch Idol remain offline checks.")


if __name__ == '__main__':
    main()
