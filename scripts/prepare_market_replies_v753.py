"""Source review, complete font planes and registered Market reply integration."""

from copy import deepcopy
from pathlib import Path

from ndspy.code import MainCodeFile
from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.market_replies_editorial import IDS, transform
from dk4tool.patch.shop_business_editorial import compile_paragraph
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.prepare_product_pitches_v747 import native_layout, wrapper_dispatch
from scripts.probe_button_prompt_native import BASE, machine
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_village_wrap_v608 import read, save

ROOT=Path('work/analysis/market_replies_v753')
MANUSCRIPT=Path('translations/market_replies_manuscript_v1.json')
CONFIG=Path('translations/market_replies_editorial_release_v1.json')
TEXT={
    747:"Thanks. We'll put it to good use.",
    748:"Huh? Sorry, but that's not enough to work with. Come back when you've earned more.",
    749:"Your cargo holds are full! You'll have to buy less.",
    753:"You don't have enough money.",
    762:"You can't trade without a market share, but you still want to invest? That's generous of you. How much will you put in?",
    763:"You're going to invest? I knew you were different from the rest! How much will you put in?",
    764:"You don't have enough money. This isn't a charity. You'll have to pay if you want a look.",
    765:"I'll give you a little extra market share, too. Don't worry. I'll take care of it.",
    766:"Come back anytime.",
}
GLOSSES={
    747:'The merchant appreciates the investment and says it will be put to effective use.',
    748:'Surprised apology that the available amount will not suffice; asks the player to return after earning more.',
    749:'Cargo holds are full; the player must reduce what they are buying.',
    753:'The player does not have enough money.',
    762:'Despite having no market share and therefore being unable to trade, the player wants to invest. The merchant praises this admirable generosity and asks how much.',
    763:'The player offers to invest. The merchant flatters them as different from the others and asks the investment amount.',
    764:'Insufficient money. This is not charity; without payment the merchant cannot show what is requested.',
    765:'As an additional favor the merchant will give a little preferential treatment on market share and reassures the player it will be handled well. Investment is not stated as the cause.',
    766:'Merchant farewell, looking forward to the player doing business again.',
}
NOTES={
    747:'Retain the natural thanks and effective-use promise. Collective business we remains appropriate; no effect size is invented.',
    748:'Restore the surprised reaction and inability to proceed. Not enough to work with preserves the objection without inventing how far below the exact threshold the available money is.',
    749:'Restore the explicit full-holds warning and polite directive in natural sales language. Buy less covers reducing quantity or the selected goods.',
    753:'Retain the complete natural funds warning; the familiar direct address does not need a separate English you there.',
    762:'Restore the source rule that trade requires share and its admiring kitoku rather than the old merely unusual. Preserve the question about amount and omit no trade/investment condition.',
    763:'Restore the omitted merchant flattery and invitation to invest. Different from the rest is the source praise, not a factual claim about a player trait or faction.',
    764:'Restore the blunt charity refusal and pay-to-see condition. Keep the object implicit as in Japanese; the source price branch confirms this is a paid viewing request, without adding the identity of a report.',
    765:'Remove the invented Since you are investing condition. The Japanese only offers additional preferential market share and reassurance. Do not infer an unproven bonus amount or eligibility trigger from adjacent records.',
    766:'Retain the idiomatic merchant farewell. It naturally conveys a wish for repeat business without a literal request for help.',
}


def main():
    ROOT.mkdir(parents=True,exist_ok=True)
    assert not MANUSCRIPT.exists() and not CONFIG.exists()
    context=read(ROOT/'native_context.json')
    current_path=Path('out/all_routes_combined_v752_candidate.nds')
    current,clean,canonical=(NdsImage.open(p) for p in (current_path,'work/clean.nds','out/raphael_natural_v2_accepted_base.nds'))
    path='/COMMON/MESFILE.DK4'
    common,arm=current.read_file(path),current.read_file('/__arm9__.bin')
    source=common_message_entries(clean.read_file(path),clean.read_file('/__arm9__.bin'))
    accepted=common_message_entries(canonical.read_file(path),canonical.read_file('/__arm9__.bin'),clean=False)
    before=common_message_entries(common,arm,clean=False)
    records=[]
    for number in IDS:
        binding=next(b for b in context['nine_original_direct_portrait_bindings'] if b['message_id']==number)
        specific=('OriginalBC894 investment path selects763 when local share is positive,762 otherwise; available funds are compared with the native minimum before748; positive supplied amount leads747, zero leads746.' if number in (747,748,762,763)
            else 'Original Market caller and direct portrait dispatch are bound by source instructions.764 follows the unsigned available-money/quoted-price failure.765 and766 are distinct consecutive replies in a separate transaction fragment; its complete bonus eligibility is not claimed.' if number in (764,765,766)
            else 'Original Market source explicitly binds the cargo-capacity warning749 or transaction funds warning753 to the direct portrait consumer; exact whole transaction eligibility is outside this source fragment test.')
        records.append({'id':f'COMMON_MESSAGE_{number}','message_id':number,'source_hex':source[number].text.hex(),
            'japanese':source[number].text.decode('cp932'),'canonical_source_hex':accepted[number].text.hex(),
            'current_text_hex':before[number].text.hex(),'current_English':before[number].text.decode('cp932'),
            'english':TEXT[number]+'{PAD}','speaker':'Market Trader, original contextual town merchant',
            'context':specific,'source_meaning':GLOSSES[number],'localization_note':NOTES[number],
            'decision':'retain-wording' if number in (747,753,766) else 'revise',
            'source_reference':{'block':source[number].block,'record':source[number].record_index,'offset':source[number].block_offset},
            'current_reference':{'block':before[number].block,'record':before[number].record_index,'offset':before[number].block_offset},
            'native_binding':binding,'review':dict.fromkeys(('source','context','localization','naturalness','formatting'),True),
            'status':'source-context-native-font-reviewed-gameplay-and-integration-pending'})
    doc={'format':'dk4-common-entry-manuscript-v1','translation_policy':'natural-dialogue-v2','encoder':'dialogue-fixed-v1',
        'target_locale':'en-US','review_gates':['source','context','localization','naturalness','formatting'],'file_path':path,
        'source_clean_COMMON_sha256':sha(clean.read_file(path)),'source_canonical_COMMON_sha256':sha(canonical.read_file(path)),
        'source_ROM_sha256':sha(clean.source.read_bytes()),'current_ROM_sha256':sha(current_path.read_bytes()),'records':records,
        'status':'experimental-native-reviewed-gameplay-pending'}
    target_common,target_arm,repack=transform(common,arm,doc)
    assert wrapper_dispatch(arm)==wrapper_dispatch(target_arm)
    cpu=machine(target_arm);cpu.mem_write(0x02387A20,bytes(MainCodeFile(target_arm,BASE).sections[3].data[:-48]))
    font=GameAsciiFont.from_arm9(target_arm);checks=[]
    sheet=Image.new('RGB',(1400,600),'#30343c');draw=ImageDraw.Draw(sheet)
    for n,row in enumerate(records):
        number=row['message_id'];raw,generated=compile_paragraph(row['english'])
        formatted,lines=native_layout(cpu,raw,number,())
        assert lines==generated
        pixels=raster(target_arm,formatted,0x01FFCE40-BASE,size=(228,64),instruction_limit=1000000)
        expected=bytearray(228*64)
        for yline,line in enumerate(lines):
            for column,char in enumerate(line):
                glyph=font.decode(char)
                for y in range(11):
                    for x in range(6):
                        if glyph.getpixel((x,y)):expected[(16*yline+y)*228+6+column*6+x]=1
        assert pixels==bytes(expected)
        preview=ROOT/f'native_{number}.png'
        Image.frombytes('L',(228,64),bytes(0 if p else 255 for p in pixels)).save(preview)
        x,y=(n%3)*466,(n//3)*200
        draw.text((x+4,y+4),f'{number}: {row["decision"]}',fill='white')
        sheet.paste(Image.open(preview).convert('RGB').resize((456,128),Image.Resampling.NEAREST),(x+4,y+24))
        checks.append({'message_id':number,'generated_lines':lines,'formatted_hex':formatted.hex(),
            'every_glyph_blank_cell_first_last_letters_and_bounds_exact':True,'preview':str(preview),'preview_sha256':sha(preview.read_bytes())})
    sheet.save(ROOT/'all9_previews_2x.png')
    save(MANUSCRIPT,doc)
    save(ROOT/'source_context_packet.json',{'current_ROM':str(current_path),'current_ROM_sha256':sha(current_path.read_bytes()),
        'records':records,'neighbors':[{'message_id':i,'Japanese_hex':source[i].text.hex(),'current_hex':before[i].text.hex()} for i in range(746,768)],
        'not_claimed_sequential_spoken_dialogue':True,'full_goal_complete':False})
    save(ROOT/'native_review.json',{'all9_complete_font_planes':checks,'all18340_dispatch_cases_unchanged':True,
        'repack':repack,'source_context_sha256':sha((ROOT/'native_context.json').read_bytes()),
        'revised_IDs':[748,749,762,763,764,765],'retained_wording_IDs':[747,753,766],
        'producer_sha256':sha(Path(__file__).read_bytes()),'gameplay_pending':True,'full_goal_complete':False})
    (ROOT/'research_COMMON.bin').write_bytes(target_common);(ROOT/'research_ARM9.bin').write_bytes(target_arm)
    # Preserve the category investigation without treating it as an approved fix.
    save(ROOT/'category730_open_investigation.json',{'message_id':730,'status':'still-open-not-integrated',
        'current_category_getter':0x020C5BA0,'getter_source_hex':arm[0xC5BA0:0xC5BB8].hex(),
        'six_branch_callers':[0x0205FC44,0x020BE800,0x020BEF14,0x020C3DE8,0x020C3F64,0x020F2028],
        'dialogue_call_to_scope':0x0205FC44,'other_five_menu_callers_must_keep_compact_strings':True,
        'prohibited_runtime_name_tail':[0x02171E48,0x02172464],
        'prohibited_mutable_caption_buffer':[0x01FFC1A0,0x01FFC360],
        'no_verified_read_only_space_selected_yet':True,'no_ROM_change_for730':True})
    save(CONFIG,{'format':'dk4-market-replies-editorial-v1','source_common_sha256':sha(common),'source_arm9_sha256':sha(arm),
        'target_common_sha256':sha(target_common),'target_arm9_sha256':sha(target_arm),
        'manuscript':str(MANUSCRIPT),'manuscript_sha256':sha(MANUSCRIPT.read_bytes()),
        'dependencies':{str(p):sha(p.read_bytes()) for p in (Path('dk4tool/patch/market_replies_editorial.py'),
            Path('dk4tool/patch/shop_business_editorial.py'),Path('dk4tool/script/common_native_repack.py'),ROOT/'native_review.json',ROOT/'native_context.json')}})
    registry_path=Path('translations/release_stack.json');registry=read(registry_path)
    assert 'all-routes-unified-v753' not in registry['profiles'];save(ROOT/'release_stack_before_V753.json',registry)
    profile=deepcopy(registry['profiles']['all-routes-unified-v752'])
    profile.update({'market_replies_editorial':str(CONFIG),'status':'experimental',
        'description':'Complete V752 plus nine source-reviewed Market investment/error replies. Six revisions,three retained wordings.730 and further Market/shared/routes remain open.'})
    registry['profiles']['all-routes-unified-v753']=profile;save(registry_path,registry)
    print('V753 registered:9 reviewed Market replies,9 complete font planes; gameplay pending.',flush=True)


if __name__=='__main__':main()
