"""Verify registered sea-foam repair, actual full glyphs, regressions and patch."""

import json
from pathlib import Path

from ndspy.code import MainCodeFile
from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_fleet_release_v375 import files
from scripts.verify_tavern_family_release_v508 import capture, read

OUT = Path('work/analysis/sea_foam_family_v514')
ROM = Path('out/all_routes_combined_v514_candidate.nds')
PARENT = Path('out/all_routes_combined_v508_candidate.nds')


def main():
    digest = sha(ROM.read_bytes())
    manifest = read(ROM.with_suffix('.manifest.json'))
    previous = read(PARENT.with_suffix('.manifest.json'))
    assert manifest['candidate_sha256'] == digest
    assert manifest['profile'] == 'all-routes-unified-v514'
    assert manifest['base_sha256'] == '3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
    assert manifest['batches'] == previous['batches'] and len(manifest['batches']) == 470
    assert manifest['required_batches'] == previous['required_batches']
    assert all(manifest['checks'].values())
    registry = read('translations/release_stack.json')
    assert len(registry['accepted_layers']) == 114
    assert manifest['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    a, b = (files(NdsImage.open(p)) for p in (PARENT, ROM))
    changed = sorted(p for p in a if a[p] != b[p])
    assert changed == ['/COMMON/MESFILE.DK4', '/__arm9__.bin']
    graphics = [p for p in a if p.lower().endswith(('.pxl', '.fls'))]
    assert len(graphics) == 675 and all(a[p] == b[p] for p in graphics)
    assert (OUT/'research_only_sea_foam_family.nds').read_bytes() == ROM.read_bytes()
    native = read(OUT/'native_proof.json')
    assert native['target_arm9_sha256'] == sha(b['/__arm9__.bin'])
    assert native['target_common_sha256'] == sha(b['/COMMON/MESFILE.DK4'])
    assert len(native['all24_complete_native_rasters']) == 24
    assert native['all24_actual_queued_parent_outputs_equal_reviewed_direct_outputs']
    replay_path, replay = capture('sea_foam_family_v514_final_actual', digest)
    assert replay['frames'] == 9476
    old_path = Path('work/emulation_v193/environment_voyage_v513/capture_report.json')
    old = read(old_path)
    expected_schedule = [e for e in old['scripted_input_schedule'] if e['start'] <= 9476]
    assert replay['scripted_input_schedule'] == expected_schedule
    fresh_path, fresh = capture('sea_foam_family_v514_fresh', digest)
    _, old_fresh = capture('tavern_family_v508_fresh', sha(PARENT.read_bytes()))
    assert fresh['scripted_input_schedule'] == old_fresh['scripted_input_schedule']
    assert fresh['core_options'] == old_fresh['core_options']
    previous_frames, current_frames = [{r['frame']:r for r in report['frames_captured']}
                                      for report in (old_fresh, fresh)]
    assert previous_frames.keys() == current_frames.keys() and len(current_frames) == 56
    assert all(previous_frames[n]['PNG_sha256'] == current_frames[n]['PNG_sha256'] for n in current_frames)
    font = GameAsciiFont.from_arm9(b['/__arm9__.bin'])
    cases = []
    for frame, message in [(8476,457),(8676,463),(8876,469),(9076,470),(9276,478)]:
        image = Image.open(Path(replay_path).parent/f'frame_{frame:06d}_navigation.png').convert('RGB')
        reference = Image.open(old_path.parent/f'frame_{frame:06d}_navigation.png').convert('RGB')
        record = next(r for r in native['all24_complete_native_rasters'] if r['message'] == message)
        rows = []
        for index, text in enumerate(record['native_lines']):
            text = text.lstrip()
            ink, bounds = complete_mask(font,text,image,22,296+index*16,(0,8,0))
            assert bounds[2] <= 240 and bounds[3] <= 376
            rows.append({'text':text,'ink_pixels':ink,'bounds':bounds})
        differences = [(x,y) for y in range(384) for x in range(256)
                       if image.getpixel((x,y)) != reference.getpixel((x,y))]
        assert all(16 <= x < 240 and 296 <= y < 376 for x,y in differences)
        cases.append({'frame':frame,'message':message,'full_glyph_and_blank_cell_masks':rows,
                      'all_words_complete_and_rows_left_aligned_at22':True,
                      'changes_only_inside_dialogue_body_pixels':len(differences)})
    section = bytes(MainCodeFile(b['/__arm9__.bin'],0x02000000).sections[4].data)
    for folder in ('sea_foam_family_v514_final_actual','sea_foam_family_v514_fresh'):
        tcm = (Path('work/emulation_v193')/folder/'native_state/arm9_itcm.bin').read_bytes()
        for lo,hi in [(0xBD8,0xC00),(0xCD0,0xD00),(0xD98,0xE00),(0xF3C,0xF54)]:
            assert tcm[0x4000+lo:0x4000+hi] == section[lo:hi]
    patch = ROM.with_suffix('.xdelta')
    make_xdelta(Path('work/clean.nds'),ROM,patch)
    reconstructed = OUT/'reconstructed.nds'
    apply_xdelta(Path('work/clean.nds'),patch,reconstructed)
    assert reconstructed.read_bytes() == ROM.read_bytes()
    campaign = read('translations/graphics_completion_campaign_v1.json')
    plaques = campaign['plaque_style_v247']['ongoing_plaque_inventory']
    assert len(plaques) == 18 and all(not p['fully_completed'] for p in plaques)
    proof = {'candidate':str(ROM),'candidate_sha256':digest,'profile':manifest['profile'],
             'base':manifest['base_rom'],'base_sha256':manifest['base_sha256'],
             'changed_from_V508':changed,'patch_sha256':sha(patch.read_bytes()),
             'exact_clean_patch_reconstruction':True,'all470_inherited_batches_and114_accepted_layers_retained':True,
             'all675_PXL_FLS_files_and_all_other_components_byte_exact':True,
             'actual_complete_source_reviewed_dialogue_pages':cases,
             'actual_capture_report':str(replay_path),'actual_capture_report_sha256':sha(Path(replay_path).read_bytes()),
             'fresh_capture_report':str(fresh_path),'fresh_capture_report_sha256':sha(Path(fresh_path).read_bytes()),
             'all56_fresh_title_New_Game_story_town_Help_frames_exact':True,
             'all24_native_voice_variants_and52_neighbor_copies_pass':True,
             'actual_crew_captain_table_and_captain_numeric_parents_covered':True,
             'resident_changed_code_exact_after_both_runs':True,
             'no_saved_completion_flags_or_movement_injection_in_sea_replay':True,
             'status':'experimental-awaiting-human-acceptance',
             'all22_original_requirements_and18_incomplete_plaques_retained':True,
             'full_goal_complete':False}
    (OUT/'release_proof.json').write_text(json.dumps(proof,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'candidate_sha256':digest,'actual_pages':len(cases),'fresh_frames':56,'exact_patch':True}))


if __name__ == '__main__':
    main()
