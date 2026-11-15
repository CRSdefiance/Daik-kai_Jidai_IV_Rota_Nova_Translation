"""Whole-exchange re-review and exact current native proof for four earlier leads."""
from copy import deepcopy
from pathlib import Path
import struct
from PIL import Image,ImageDraw
from ndspy.code import MainCodeFile
from dk4tool.dialogue.earlier_market_letters_reflow_v1 import compile_letter
from dk4tool.dialogue.common_portrait_reflow import compile_paragraph as prototype
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.prepare_shop_business_release_v745 import selectors
from scripts.verify_market_context_v753 import selections,SPANS as FUNDS_SPANS
from scripts.review_market_stock_v755 import fragments,SPANS as STOCK_SPANS
from scripts.review_early_shop_breaks_v4763e import reference,expected_plane
from scripts.primary_town_native_font_v2102 import font_tools,glyph_codes
from scripts.prepare_product_pitches_v747 import native_layout
from scripts.probe_button_prompt_native import machine,BASE,STACK
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.market_contract_editorial import INVESTMENT

ROOT=Path('work/analysis/earlier_common_wraps_review_v4977c')
CURRENT=Path('out/all_routes_combined_v4966_candidate.nds')
GLOSSES=Path('work/analysis/earlier_common_wraps_glosses_v4976/four_clean_source_glosses_before_English.json')
REASONS={
    682:('retain-wording-and-layout',
        'Business? naturally repeats the inquiry. Least of my worries expresses the more pressing concern,and the peace wish stays courteous and prospective. No specific battle,location or actor identity is added.',
        'Retain three rows. The full opening sentence exceeds34 cells;the existing first break keeps of my worries together. The prototype fills line1 more but splits my / worries and does not save a row. Maximum filling is not an editorial requirement.'),
    764:('retain-wording-and-layout',
        'The blunt funds warning,charity objection and pay-to-see condition form a natural refusal. A look leaves the source object implicit;the original paid-viewing branch confirms payment without inventing a report name or an investment transaction.',
        'Retain three rows. The complete opening sentence occupies line1 and the next sentence begins cleanly on line2. The prototype moves This to line1,then separates This / isn\'t without saving a row;that is less readable.'),
    774:('retain-wording-reflow',
        'Oh,I know! conveys the sudden idea,and the offer explicitly preserves a letter of introduction and thanks for the popular goods. Us is the merchant business receiving the goods,not an invented relationship. No large-quantity qualifier is imported from775.',
        'Use three full-width rows instead of four. The complete-word soft wrap after for connects naturally to selling on the next row. The letter of introduction continues into the original small-town explanation779 and farewell766. Preserve every word and exact NUL position.'),
    775:('retain-wording-reflow',
        'And preserves the additional offer. Letter of recommendation,so many popular goods and the gratitude retain the distinct source facts. Its following780 explanation concerns any town;do not import779\'s small-town restriction.',
        'Use three full-width rows instead of four. The complete-word for boundary is a reviewed ordinary soft wrap. Two generated even pre-LF allocation spaces keep the native draw phase;remaining terminal padding must stay within35 final cells. No editable break or padding is authored.'),
}

if __name__=='__main__':
    assert not ROOT.exists();v=read('work/analysis/editorial_handoff_verification_v4973/verified_handoff.json')
    assert sha(CURRENT.read_bytes())==v['candidate_sha256']
    image,clean=NdsImage.open(CURRENT),NdsImage.open('work/clean.nds')
    arm,common=image.read_file('/__arm9__.bin'),image.read_file('/COMMON/MESFILE.DK4')
    ca,cc=clean.read_file('/__arm9__.bin'),clean.read_file('/COMMON/MESFILE.DK4')
    directory=read('translations/shop657_full_width_reflow_release_v1.json')['directory_sha256']
    entries=owned_entries(common,arm,directory);japanese=common_message_entries(cc,ca)
    source=read(GLOSSES);assert source['read_no_predecessor_English']
    glosses={r['message_ID']:r for r in source['records']}
    context_IDs=sorted(set(range(656,659))|set(range(682,688))|set(range(761,784)))
    context=[dict(message_ID=n,source_reference=reference(japanese[n]),source_hex=japanese[n].text.hex(),clean_Japanese=japanese[n].text.decode('cp932'),
        current_reference=reference(entries[n]),current_hex=entries[n].text.hex(),current_English=entries[n].text.decode('ascii')) for n in context_IDs]
    spans=[(0x5F9B8,0x5FB54),*FUNDS_SPANS,*STOCK_SPANS]
    differences=sorted({at for a,b in spans for at in range(a,b,4) if ca[at:at+4]!=arm[at:at+4]})
    assert differences==[0xBCA3C] and struct.unpack_from('<I',arm,0xBCA3C)[0]==INVESTMENT
    assert arm[INVESTMENT-BASE:INVESTMENT-BASE+11]==b'Investment\0'
    restored=bytearray(arm);restored[0xBCA3C:0xBCA40]=ca[0xBCA3C:0xBCA40]
    for a,b in spans:assert bytes(restored[a:b])==ca[a:b]
    a,b=selectors(ca),selectors(arm);assert a==b and len(a)==13
    f,g=selections(ca),selections(arm);assert f==g and len(f)==11
    s,t=fragments(ca),fragments(arm);assert s==t and len(s)==36
    roots=['translations/square_contextual_final_review_v1.json','translations/market_contextual_final_review_v1.json','translations/town_trade_port_contextual_final_review_v1.json']
    historical={r['message_id']:(p,r) for p in roots for r in read(p)['records'] if r.get('message_id') in REASONS}
    assert set(historical)==set(REASONS)
    cpu=machine(arm);cpu.mem_write(0x02387A20,bytes(MainCodeFile(arm,BASE).sections[3].data[:-48]));cpu.mem_write(STACK+0x27C,struct.pack('<I',0x02118480))
    raster,_,meta=font_tools(image);ROOT.mkdir(parents=True);rows=[];tiles=[]
    for n,(decision,wording_reason,layout_reason) in REASONS.items():
        old=entries[n];hp,history=historical[n];jp=japanese[n]
        historical_binding_key='current_hex' if n==764 else 'integrated_hex'
        assert old.text.hex()==history[historical_binding_key] and jp.text.hex()==history['source_hex']==glosses[n]['source_hex']
        paragraph=' '.join(old.text.decode('ascii').split());candidate,prototype_lines=prototype(paragraph)
        if n in (774,775):target,allocation=compile_letter(n,paragraph,len(old.text))
        else:target=old.text;allocation=dict(lines=[s.strip().decode('ascii') for s in old.text.split(b'\n')],unchanged_exact_layout=True)
        assert b' '.join(target.split())==b' '.join(old.text.split()) and len(target)==len(old.text)
        cases=[]
        for label,raw in [('current',old.text),('reviewed',target)]:
            formatted,lines=native_layout(cpu,raw,n,(),0x02054014)
            assert formatted==raw and lines==allocation['lines'] if label=='reviewed' else formatted==raw
            events=[];plane=raster(arm,formatted,0x01FFCE40-BASE,size=(228,64),instruction_limit=2000000,glyph_events=events)
            assert plane==expected_plane(arm,lines,1)
            assert [e['code'] for e in events if e['code']!=32]==glyph_codes(formatted)
            assert all(0<=e['x'] and e['x']+6<=228 and 0<=e['y'] and e['y']+12<=64 for e in events)
            p=ROOT/f'message{n}_{label}.png';Image.frombytes('L',(228,64),bytes(0 if x else 255 for x in plane)).save(p)
            cases.append(dict(label=label,message_ID=n,compiled_hex=raw.hex(),native_formatted_hex=formatted.hex(),lines=lines,
                whole_native_plane_sha256=sha(plane),preview=str(p),preview_sha256=sha(p.read_bytes()),glyph_events=events,
                full_independent_228x64_plane_equal=True,complete_leading_internal_final_glyphs_and_bounds=True,
                original_expansion_then_existing_wrapper_without_new_dispatch=True,all_source_bytes_consumed_one_native_page=True))
            tiles.append((str(n)+' '+label,p))
        rows.append(dict(id=f'COMMON_MESSAGE_{n}',message_id=n,source_reference=reference(jp),source_hex=jp.text.hex(),clean_Japanese=jp.text.decode('cp932'),
            source_meaning=glosses[n]['fresh_source_gloss'],whole_context_note=glosses[n]['whole_context_note'],
            current_reference=reference(old),current_hex=old.text.hex(),english=paragraph+'{PAD}',target_hex=target.hex(),
            historical_final_review=hp,historical_final_review_sha256=sha(Path(hp).read_bytes()),historical_record=deepcopy(history),historical_exact_payload_key=historical_binding_key,
            editorial_decision=decision,fresh_retained_wording_justification=wording_reason,layout_review_reason=layout_reason,
            rejected_prototype_lines=prototype_lines,allocation=allocation,native_cases=cases,review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
            actual_new_display_coverage=False,new_editorial_credit=0))
    sheet=Image.new('RGB',(936,680),'#263238');draw=ImageDraw.Draw(sheet)
    for i,(label,p) in enumerate(tiles):
        x,y=i%2*468,i//2*170;draw.text((x+4,y+4),label,fill='white');sheet.paste(Image.open(p).resize((456,128),Image.Resampling.NEAREST),(x+4,y+30))
    sp=ROOT/'all4_current_and_reviewed_native_planes.png';sheet.save(sp)
    save(ROOT/'whole_context_four_retentions_two_reflows_and8_native_planes.json',dict(format='dk4-earlier-common-wrap-context-native-review-v1',
        current_ROM=str(CURRENT),current_ROM_sha256=sha(CURRENT.read_bytes()),current_COMMON_sha256=sha(common),current_ARM9_sha256=sha(arm),
        clean_COMMON_sha256=sha(cc),directory_sha256=directory,records=rows,complete_source_current_context=context,
        conversation_groups=[dict(IDs=[656,657,658,*range(682,688)],flow='Shop inquiry selects one conditional reply;the13 supplied-state cases preserve682 for state0. These are alternatives,not consecutive speakers.'),
            dict(IDs=[764],flow='Quoted paid viewing -> insufficient funds -> blunt refusal;the11 supplied decision fragments preserve the boundary at the quoted amount.'),
            dict(IDs=list(range(774,784)),flow='774->779->766;775/778->780->766;776->777->781->766;782/783->766. Introduction/recommendation,quantity and small/any-town distinctions stay separate.')],
        original_clean_current_selector_cases=a,original_clean_current_funds_cases=f,original_clean_current_stock_letter_cases=s,
        exact_original_spans=[dict(start=a,end=b,clean_sha256=sha(ca[a:b]),current_sha256=sha(arm[a:b])) for a,b in spans],
        sole_registered_title_literal=dict(address=0x020BCA3C,clean_hex=ca[0xBCA3C:0xBCA40].hex(),current_hex=arm[0xBCA3C:0xBCA40].hex(),target=INVESTMENT,title='Investment',owner='dk4tool.patch.market_contract_editorial.relocate_providers',every_other_selected_source_word_exact=True),
        selector_getters_product_getters_and_effect_support_are_explicit_supplied_or_skipped_boundaries=True,
        no_natural_eligibility_earned_letters_complete_transaction_or_gameplay_claim=True,
        retained_exact_layout_IDs=[682,764],proposed_reflow_IDs=[774,775],changed_prose_IDs=[],
        review_sheet=str(sp),review_sheet_sha256=sha(sp.read_bytes()),visual_review_pending=True,
        source_gloss_proof=str(GLOSSES),source_gloss_proof_sha256=sha(GLOSSES.read_bytes()),native_font_tools=meta,
        dependencies={str(p):sha(Path(p).read_bytes()) for p in [*roots,Path(__file__),'dk4tool/dialogue/earlier_market_letters_reflow_v1.py']},
        new_editorial_credit=0,actual_new_emulator_runs=0,ROM_or_registry_changed=False,full_goal_complete=False))
    print(dict(reviewed=4,wording_retained=4,exact_layout_retained=[682,764],reflows=[774,775],complete_native_planes=8,
        selectors=13,funds=11,stock_letters=36,visual_review_pending=True,new_editorial_credit=0))
