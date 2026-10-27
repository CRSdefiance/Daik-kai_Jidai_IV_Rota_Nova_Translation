"""Finalize source730 with full native arguments, complete glyphs and compact UI."""

import subprocess
import sys
from copy import deepcopy
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.category_dialogue_editorial import compile_template, transform
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.prepare_product_pitches_v747 import native_layout, wrapper_dispatch
from scripts.verify_category_lookup_v754 import ROOT, cpu_for
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_village_wrap_v608 import read, save

MANUSCRIPT=Path('translations/category_dialogue_manuscript_v1.json')
CONFIG=Path('translations/category_dialogue_editorial_release_v1.json')


def main():
    assert not MANUSCRIPT.exists() and not CONFIG.exists()
    current_path=Path('out/all_routes_combined_v753_candidate.nds');current=NdsImage.open(current_path)
    clean=NdsImage.open('work/clean.nds');canonical=NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    path='/COMMON/MESFILE.DK4';common,arm=current.read_file(path),current.read_file('/__arm9__.bin')
    before=common_message_entries(common,arm,clean=False)
    row=deepcopy(next(r for r in read('translations/town_events_editorial_manuscript_v1.json')['records'] if r['message_id']==730))
    row.update({'current_text_hex':before[730].text.hex(),'current_English':before[730].text.decode('cp932'),
        'english':'Something in the %s market is sure to catch on soon.{PAD}',
        'speaker':'Square shopkeeper, original contextual town actor',
        'context':'Original5FB54 future-trend branch with value below25 and its random choice0 selects730. Original5FC40 reads the selected product category byte, calls C5BA0 and supplies its result to direct portrait730. The exact returnPC205FC48 now selects full names; all five other direct callers and Square caption callers retain compact strings.',
        'source_meaning':'One unspecified individual good within the supplied category is certain to become popular in the future; the prediction does not apply to all goods in that category.',
        'localization_note':'Something in the category market is natural merchant advice for an unspecified future hit. Retain certainty and the near-future sense without inventing a product identity. Expand abbreviated category arguments Seasonings, Delicacy, Precious Metals, Jewelry, Medicine and Sundries. Other already complete English category words remain unchanged. The actual menu words and all source substitutions remain exact.',
        'decision':'revise','review':dict.fromkeys(('source','context','localization','naturalness','formatting'),True),
        'status':'source-context-native-reviewed-gameplay-pending'})
    doc={'format':'dk4-common-entry-manuscript-v1','translation_policy':'natural-dialogue-v2','encoder':'dialogue-fixed-v1',
        'target_locale':'en-US','review_gates':['source','context','localization','naturalness','formatting'],'file_path':path,
        'source_clean_COMMON_sha256':sha(clean.read_file(path)),'source_canonical_COMMON_sha256':sha(canonical.read_file(path)),
        'source_ROM_sha256':sha(clean.source.read_bytes()),'current_ROM_sha256':sha(current_path.read_bytes()),'records':[row],
        'status':'experimental-native-reviewed-gameplay-pending'}
    target_common,target_arm,repack=transform(common,arm,doc)
    (ROOT/'lookup_research_ARM9.bin').write_bytes(target_arm);save(ROOT/'lookup_ownership.json',repack['lookup'])
    subprocess.run([sys.executable,'scripts/verify_category_lookup_v754.py'],check=True)
    abi=read(ROOT/'lookup_native_ABI.json');assert abi['target_ARM9_sha256']==sha(target_arm)
    assert wrapper_dispatch(arm)==wrapper_dispatch(target_arm)
    cpu=cpu_for(target_arm);font=GameAsciiFont.from_arm9(target_arm);checks=[]
    sheet=Image.new('RGB',(1400,1100),'#30343c');draw=ImageDraw.Draw(sheet)
    for n,argument in enumerate(abi['all18_original730_caller_arguments']):
        text=argument['original730_caller_argument']
        formatted,lines=native_layout(cpu,compile_template(row['english']),730,(text,))
        assert len(lines)==1 or len(lines[-1])>8
        pixels=raster(target_arm,formatted,0x01FFCE40-0x02000000,size=(228,64),instruction_limit=1000000)
        expected=bytearray(228*64)
        for yline,line in enumerate(lines):
            for col,char in enumerate(line):
                glyph=font.decode(char)
                for y in range(11):
                    for x in range(6):
                        if glyph.getpixel((x,y)):expected[(16*yline+y)*228+6+col*6+x]=1
        assert pixels==bytes(expected)
        preview=ROOT/f'native_category_{n:02d}.png';Image.frombytes('L',(228,64),bytes(0 if p else 255 for p in pixels)).save(preview)
        xx,yy=(n%3)*466,(n//3)*180;draw.text((xx+4,yy+4),f'{n}: {text}',fill='white')
        sheet.paste(Image.open(preview).convert('RGB').resize((456,128),Image.Resampling.NEAREST),(xx+4,yy+20))
        checks.append({'category':n,'full_argument':text,'lines':lines,'formatted_hex':formatted.hex(),
            'every_glyph_blank_cell_first_last_character_and_bounds_exact':True,'preview':str(preview),'preview_sha256':sha(preview.read_bytes())})
    sheet.save(ROOT/'all18_dialogue_previews_2x.png')
    # The original Japanese category strings bind every unchanged/expanded term.
    clean_arm=clean.read_file('/__arm9__.bin');source_labels=[]
    import struct
    for i in range(18):
        pointer=struct.unpack_from('<I',clean_arm,0x11B444+i*4)[0]-0x02000000
        source_labels.append({'category':i,'Japanese':clean_arm[pointer:clean_arm.index(0,pointer)].decode('cp932'),
            'compact_English':abi['all108_getter_cases'][i]['before'],'dialogue_English':checks[i]['full_argument']})
    save(MANUSCRIPT,doc)
    save(ROOT/'native_review.json',{'all18_complete_dialogue_font_planes':checks,'source_category_labels':source_labels,
        'all18340_dispatch_cases_unchanged':True,'all18_Square_caption_planes_and108_lookup_cases_bound_to_target':True,
        'lookup_native_ABI_sha256':sha((ROOT/'lookup_native_ABI.json').read_bytes()),'repack':repack,
        'producer_sha256':sha(Path(__file__).read_bytes()),'gameplay_pending':True,'full_goal_complete':False})
    save(ROOT/'source_context_packet.json',{'records':[row],'source_category_labels':source_labels,
        'original288_trend_selection_cases':'work/analysis/town_events_v750/native_context.json',
        'original_trend_report_sha256':sha(Path('work/analysis/town_events_v750/native_context.json').read_bytes()),'full_goal_complete':False})
    (ROOT/'research_COMMON.bin').write_bytes(target_common);(ROOT/'research_ARM9.bin').write_bytes(target_arm)
    save(CONFIG,{'format':'dk4-category-dialogue-editorial-v1','source_common_sha256':sha(common),'source_arm9_sha256':sha(arm),
        'target_common_sha256':sha(target_common),'target_arm9_sha256':sha(target_arm),'manuscript':str(MANUSCRIPT),
        'manuscript_sha256':sha(MANUSCRIPT.read_bytes()),'dependencies':{str(p):sha(p.read_bytes()) for p in (
            Path('dk4tool/patch/category_dialogue_editorial.py'),Path('dk4tool/patch/category_dialogue_lookup.py'),
            Path('dk4tool/patch/town_stock_rows.py'),Path('dk4tool/script/common_native_repack.py'),ROOT/'native_review.json',ROOT/'lookup_native_ABI.json')}})
    registry_path=Path('translations/release_stack.json');registry=read(registry_path);assert 'all-routes-unified-v754' not in registry['profiles']
    save(ROOT/'release_stack_before_V754.json',registry)
    profile=deepcopy(registry['profiles']['all-routes-unified-v753']);profile.update({'category_dialogue_editorial':str(CONFIG),'status':'experimental',
        'description':'Complete V753 plus source-reviewed730 with full category arguments and all compact UI/category/Square labels preserved. Gameplay verification pending.'})
    registry['profiles']['all-routes-unified-v754']=profile;save(registry_path,registry)
    print('V754 registered:730 full category names;18 complete font planes and unchanged native menu captions verified.',flush=True)


if __name__=='__main__':main()
