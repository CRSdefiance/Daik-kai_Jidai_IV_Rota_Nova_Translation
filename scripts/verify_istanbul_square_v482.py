"""Genuine Istanbul Square: four complete signs, focus bounds and activations."""

import json
from pathlib import Path

from PIL import Image
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import call, machine
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask

ROOT = Path('work/analysis/istanbul_square_v482')
CAPTURE = Path('work/emulation_v193/istanbul_square_v482')


def main():
    report_path = CAPTURE / 'capture_report.json'
    report = json.loads(report_path.read_text(encoding='utf-8'))
    rom_path = Path(report['ROM'])
    assert sha(rom_path.read_bytes()) == report['ROM_sha256'] == '1d513b81762499f0fd6a2edeeabb182a69c334756fc9261f70c07a0110984b9e'
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert not report.get('synthetic_inventory_fixtures') and report['frames'] == 5900
    donor = report['battery_save_preloaded']
    assert sha(Path(donor['source']).read_bytes()) == donor['source_sha256']
    for row in report['frames_captured']:
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
    rom = NdsImage.open(rom_path)
    arm = rom.read_file('/__arm9__.bin')
    font = GameAsciiFont.from_arm9(arm)
    original = machine(NdsImage.open('work/clean.nds').read_file('/__arm9__.bin'))

    def capture(frame):
        row = next(r for r in report['frames_captured'] if r['frame'] == frame)
        return Image.open(row['path']).convert('RGB'), row

    labels = [(2, '珍味', 'Delic. Shop'), (5, '酒類', 'Liquor Shop'),
              (12, '宝石', 'Gems Shop'), (8, '繊維', 'Fiber Shop')]
    source_terms = []
    for category, japanese, label in labels:
        call(original, 0xC5BA0, (category,))
        pointer = original.reg_read(UC_ARM_REG_R0)
        assert bytes(original.mem_read(pointer, 64)).split(b'\0')[0].decode('cp932') == japanese
        source_terms.append({'category': category, 'Japanese': japanese, 'visible_label': label})
    cases, images = [], []
    for frame, selected in ((4500,0),(4600,1),(4700,2),(4800,3)):
        image, row = capture(frame)
        images.append(image)
        complete = []
        for index, (_, _, text) in enumerate(labels):
            y = 214 + index * 32
            expected = {(120+n*5+x,y+gy) for n,c in enumerate(text)
                        for gy in range(11) for x in range(6) if font.decode(c).getpixel((x,gy))}
            actual = {(x,yy) for yy in range(y,y+12) for x in range(120,184)
                      if image.getpixel((x,yy)) == (230,230,230)}
            assert actual == expected
            top = 208 + index * 32
            if index == selected:
                for yy in range(top-2,top+26):
                    for x in range(170,186):
                        assert image.getpixel((x,yy)) == ((230,230,230) if (x,yy) in expected else (0,165,172))
                assert image.getpixel((186,top+4)) == (123,121,98)
            else:
                assert image.getpixel((180,top+4)) == (57,56,57)
            complete.append({'label':text,'ink_pixels':len(expected),'first_and_final_glyphs_and_blank_cells_exact':True,
                             'selected':index==selected})
        cases.append({'frame':frame,'capture':row,'complete_signs':complete,'focus_extent_preserves_original_border':True})
    for image in images[1:]:
        changes = [(i%256,i//256) for i,(a,b) in enumerate(zip(images[0].get_flattened_data(),image.get_flattened_data())) if a!=b]
        assert changes and all(86 <= x < 186 and 206 <= y < 334 for x,y in changes)
    dialogue = []
    for frame in (5200,5600,5900):
        image, row = capture(frame)
        masks = []
        for text,y in [('Business? Fair. I wish a good',296),('opportunity would arise.',312)]:
            ink,bounds = complete_mask(font,text,image,22,y,(0,8,0))
            masks.append({'text':text,'ink_pixels':ink,'bounds':bounds})
        dialogue.append({'frame':frame,'capture':row,'complete_lines':masks,'both_line_origins_x22':True})
    proof = {'candidate':str(rom_path),'candidate_sha256':report['ROM_sha256'],
             'report':str(report_path),'report_sha256':sha(report_path.read_bytes()),
             'source_terms':source_terms,'four_complete_selection_states':cases,'three_complete_shop_dialogues':dialogue,
             'all_four_activations_visually_reviewed_frames':[4900,5200,5600,5900],
             'original_donor_save_preserved':True,'ordinary_controls_no_inventory_fixture':True,
             'Trends_overlay_dismissed_before_sign_verification':True,'goal_complete':False,
             'remaining':['Other cities/categories and historical prose wording remain open.',
                          'Delic. abbreviates delicacies; full wording needs a separately verified layout.',
                          'All18 plaques and all22 historical requirements remain in the audit.']}
    ROOT.mkdir(parents=True,exist_ok=True)
    (ROOT/'square_proof.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'actual_city':'Istanbul','complete_selection_states':len(cases),'complete_dialogues':len(dialogue)}))


if __name__ == '__main__':
    main()
