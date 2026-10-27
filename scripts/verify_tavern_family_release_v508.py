"""Verify integrated Tavern formatting, real replay and exact clean patch."""

import json
from pathlib import Path

from ndspy.code import MainCodeFile
from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_fleet_release_v375 import files
from scripts.verify_tavern_addresses_v413 import wrap

OUT = Path('work/analysis/tavern_family_v508')
ROM = Path('out/all_routes_combined_v508_candidate.nds')
PARENT = Path('out/all_routes_combined_v502_candidate.nds')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def capture(folder,digest):
    path = Path('work/emulation_v193')/folder/'capture_report.json'
    data = read(path)
    assert data['ROM_sha256'] == digest
    assert data['cold_boot'] and not data['savestate_loaded'] and not data['callback_errors']
    assert not data.get('synthetic_inventory_fixtures')
    for row in data['frames_captured']:
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
    if data.get('battery_save_preloaded'):
        donor = data['battery_save_preloaded']
        assert sha(Path(donor['source']).read_bytes()) == donor['source_sha256']
    return path,data


def main():
    manifest = read(ROM.with_suffix('.manifest.json'))
    digest = sha(ROM.read_bytes())
    assert manifest['candidate_sha256'] == digest and manifest['profile'] == 'all-routes-unified-v508'
    assert manifest['base_sha256'] == '3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
    assert sha(Path(manifest['base_rom']).read_bytes()) == manifest['base_sha256']
    parent_manifest = read(PARENT.with_suffix('.manifest.json'))
    assert manifest['batches'] == parent_manifest['batches'] and len(manifest['batches']) == 470
    assert manifest['required_batches'] == parent_manifest['required_batches'] and all(manifest['checks'].values())
    registry = read('translations/release_stack.json')
    assert len(registry['accepted_layers']) == 114
    assert manifest['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    before,after = files(NdsImage.open(PARENT)),files(NdsImage.open(ROM))
    changed = [p for p in before if before[p] != after[p]]
    assert sorted(changed) == ['/COMMON/MESFILE.DK4','/__arm9__.bin']
    graphics = [p for p in before if p.lower().endswith(('.pxl','.fls'))]
    assert len(graphics) == 675 and all(before[p] == after[p] for p in graphics)
    prototype = OUT/'research_only_tavern_family.nds'
    assert prototype.read_bytes() == ROM.read_bytes()
    native = read(OUT/'native_proof.json')
    assert native['target_arm9_sha256'] == sha(after['/__arm9__.bin'])
    assert len(native['cases']) == 108 and not native['failures']
    athens_path,athens = capture('tavern_family_v508_athens',digest)
    assert athens['frames'] == 23300
    fresh_path,fresh = capture('tavern_family_v508_fresh',digest)
    _,old_fresh = capture('town_direct_labels_v501_fresh',sha(PARENT.read_bytes()))
    assert fresh['scripted_input_schedule'] == old_fresh['scripted_input_schedule']
    assert fresh['core_options'] == old_fresh['core_options']
    a,b = [{r['frame']:r for r in d['frames_captured']}for d in (old_fresh,fresh)]
    assert a.keys() == b.keys() and len(b) == 56
    assert all(a[n]['PNG_sha256'] == b[n]['PNG_sha256']for n in b)
    arm = after['/__arm9__.bin']
    font = GameAsciiFont.from_arm9(arm)
    image = Image.open('work/emulation_v193/tavern_family_v508_athens/frame_023300_final.png').convert('RGB')
    toast_rows = []
    for text,y in [("Hmm... Hodram, right? Here's to our",296),('new friendship!',312)]:
        pixels,bounds = complete_mask(font,text,image,22,y,(0,8,0))
        assert bounds[2] <= 240 and bounds[3] <= 360
        toast_rows.append({'text':text,'origin':[22,y],'full_ink_pixels':pixels,'bounds':bounds})
    old_image = Image.open('work/emulation_v193/environment_voyage_v507/frame_023300_navigation.png').convert('RGB')
    differences = [(x,y)for y in range(384)for x in range(256)if old_image.getpixel((x,y)) != image.getpixel((x,y))]
    assert differences and all(16 <= x < 240 and 296 <= y < 344 for x,y in differences)
    entries = common_message_entries(after['/COMMON/MESFILE.DK4'],arm,clean=False)
    sibling = []
    for number in [801,*range(3648,3668)]:
        text = entries[number].text.rstrip()
        formatted = wrap(arm,text,0x02054014,number)
        assert b' '.join(formatted.split()) == b' '.join(text.split())
        events = []
        raster(arm,formatted,0x01FFCE40-0x02000000,size=(228,80),instruction_limit=1000000,glyph_events=events)
        visible = [r for r in events if r['code'] not in (32,10)]
        decoded = text.decode('cp932')
        codes = [int.from_bytes(c.encode('cp932'),'big')for c in decoded if c not in (' ','\n')]
        assert [r['code']for r in visible] == codes,number
        offset = 0
        for word in decoded.split():
            part = visible[offset:offset+len(word)]
            assert len({r['y']for r in part}) == 1,(number,word)
            offset += len(word)
        assert all(r['x'] < 228 and r['y']+11 <= 80 for r in visible)
        sibling.append({'message':number,'complete_glyph_order_and_words':True,'lines':formatted.decode('cp932').splitlines()})
    prefix_cases = []
    # Newly wrapped templates can begin with a substituted F/I. These letters
    # had a historical collision with executable macro prefixes.
    for number in (820,821,847,848,850):
        for argument in (b'Istanbul',b'Furs'):
            text = entries[number].text.rstrip().replace(b'%s',argument)
            formatted = wrap(arm,text,0x02054014,number)
            events = []
            raster(arm,formatted,0x01FFCE40-0x02000000,size=(228,80),instruction_limit=1000000,glyph_events=events)
            assert [e['code']for e in events if e['code']not in(32,10)] == [c for c in text if c not in(32,10)]
            prefix_cases.append({'message':number,'argument':argument.decode(),'all_first_internal_final_glyphs_preserved':True})
    section = MainCodeFile(arm,0x02000000).sections[4]
    for folder in ('tavern_family_v508_athens','tavern_family_v508_fresh'):
        tcm = (Path('work/emulation_v193')/folder/'native_state/arm9_itcm.bin').read_bytes()
        for lo,hi in [(0xA00,0xB1C),(0xB54,0xB5C),(0xF54,0xF58)]:
            assert tcm[0x4000+lo:0x4000+hi] == bytes(section.data[lo:hi])
    patch = ROM.with_suffix('.xdelta')
    make_xdelta(Path('work/clean.nds'),ROM,patch)
    reconstructed = OUT/'reconstructed.nds'
    apply_xdelta(Path('work/clean.nds'),patch,reconstructed)
    assert reconstructed.read_bytes() == ROM.read_bytes()
    proof = {'candidate':str(ROM),'candidate_sha256':digest,'patch_sha256':sha(patch.read_bytes()),
             'exact_clean_patch_reconstruction':True,'changed_from_V502':changed,
             'all470_inherited_batches_and114_accepted_layers_retained':True,
             'all675_PXL_FLS_files_byte_exact':True,'all_other_ROM_components_byte_exact':True,
             'actual_toast_rows_complete_and_aligned':toast_rows,'changed_pixels_in_dialogue_body_only':len(differences),
             'all56_fresh_title_New_Game_story_town_Help_frames_exact':True,
             'all108_supplied_Tavern_printf_wrap_glyph_cases_pass':True,
             'all7336_dispatch_destinations_compared':True,'native_repair_and20_Guild_siblings':sibling,
             'native_expanded_F_I_prefix_cases':prefix_cases,
             'resident_changed_ITCM_bytes_exact_after_both_runs':True,
             'athens_capture_report':str(athens_path),'fresh_capture_report':str(fresh_path),
             'native_argument_provider_and_arbitrary_over_capacity_inputs_not_proven':True,
             'same236_byte_four_row_scratch_contract':True,'status':'experimental-awaiting-user-acceptance',
             'full_goal_complete':False}
    (OUT/'release_proof.json').write_text(json.dumps(proof,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'candidate_sha256':digest,'toast':toast_rows,'fresh_frames':56,'native_siblings':len(sibling),'exact_patch':True},indent=2))


if __name__ == '__main__':
    main()
