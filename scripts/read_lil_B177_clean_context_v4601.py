"""Read/gloss all ten B177 tomato-fashion speeches before predecessor English."""
from copy import deepcopy
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B177_clean_context_v4601')
INVENTORY=Path('work/analysis/lil_B161_B180_clean_scope_v3910/complete_clean_B161_B180_next_exchange_inventory.json')
CONTEXT=(
    'Read B177 as a complete ten-speech comic exchange. AE repeats tomatoes and declares that the coming age belongs to them. '
    'AF doubts whether such bright-red food will be the thing. AE loves that red precisely because it stirs passion and recalls '
    'the consuming love of her younger days. AF offers a reserved pause and politely detached acknowledgment. AE abruptly '
    'turns from reminiscence to business:prepare tomato dishes and start selling them at once. AF agrees. AE emphasizes not '
    'letting this tomato fashion pass them by. AF gives a casual repeated acknowledgment. AE encourages the effort and ends '
    'with the same elaborate self-satisfied laugh. An impersonal FE notice then predicts that tomatoes seem likely to catch '
    'on in ジェノヴァ. Preserve enthusiasm,color-based skepticism,passionate reminiscence,deadpan politeness,practical orders, '
    'compliance,exhortation,offhand acknowledgment and grand confidence,then the shift to impersonal prospective news.\n\n'
    'The native AE/AF names and voices remain to bind;source selectors alone are not permission to copy a character name '
    'from predecessor English. The recollection is AE\'s own youthful romance;it identifies no lover and proves no romance, '
    'marriage or kinship with AF. 身を焦がすような恋 is consuming/burning romantic passion,not literal injury or a named affair. '
    'Preserve the red and the stirring of passion;do not substitute B176\'s taste-based argument. AF\'s skeptical red-food '
    'question does not assert that tomatoes are poisonous,unsafe or inedible. Add no historical food taboo. The detached '
    'よかったですね can sound dry in this exchange;do not turn it into enthusiastic shared nostalgia,flirtation or a new insult. '
    'The brief 分かりました is polite compliance;later へいへい is casual/resigned repeated acknowledgment.\n\n'
    'The immediate instruction concerns cooking tomato dishes and putting them on sale,not buying a stated quantity, '
    'already making money,shipping cargo or completing a sale. AE treats the tomato fashion as an opportunity in her own '
    'speech;the closing narrator retains しそう as prospective likelihood rather than an already earned or guaranteed boom. '
    'The city is explicit only in that closing notice. Do not assign the earlier scene a location,make an unsupported '
    'chronological connection to B176,or infer noble rank/employment hierarchy from the elaborate laugh and imperatives.\n\n'
    'There are nine progressive speeches with static selectorsAE/AF and one impersonal FE notice. FI/FA/FO counts arezero. '
    'All13 source commands form a linear structural stream:leading A0008 raw00a0ffff01090fa1,ten speeches,C200480 and a '
    'single four-byte end482,logical486/stored488. No relative site,predicate,2000 pause,resource,presentation word or typed '
    'choice exists. Preserve all commands and complete preambles without guessing packed effect operands or claiming '
    'natural event selection or earned fashion state. This producer reads no predecessor English and adds no review credit.'
)
MEANINGS={
    6:'AE enthusiastically repeats tomatoes and declares that the coming age is theirs. Preserve the grand future-fashion claim,not an established boom or completed success.',
    9:'AF questions the claim and skeptically asks whether food this bright red is really the thing. Preserve the color,the food reference and doubtful questions without adding poison,inedibility or historical food lore.',
    12:'AE says the red is precisely what is good:it arouses passion. With an emotional sigh,she says it reminds her of the consuming romance of her youth. Preserve the red,passion and personal remembrance;name no lover and invent no present relationship or literal burning injury.',
    16:'After a pause,AF says in effect,is that so;good for you. Preserve the detached,polite acknowledgment in response to AE\'s reminiscence;no enthusiastic shared past,flirtation or extra insult.',
    20:'AE orders AF to prepare tomato dishes and put them on sale right away. Preserve both cooking and starting to sell,the immediacy and imperative;do not claim the work or sale is already completed.',
    23:'AF gives a short polite acknowledgment that the instruction is understood. Preserve compliance and its register contrast with the later casual repeated reply.',
    27:'AE affirms and instructs AF to make sure they do not miss this tomato fashion. Preserve the speaker\'s commercial urgency and opportunity without upgrading her claim into an impersonal confirmed boom or adding profit,quantity or cargo facts.',
    30:'AF gives the casual repeated acknowledgment へいへい. Preserve the offhand/resigned compliance and repeated rhythm rather than a newly invented rank,title or relationship address.',
    34:'AE closes with encouragement to do one\'s best and the elaborate self-satisfied laugh. Preserve the confidence and encouragement,not a threat,royal identity or additional punchline.',
    37:'The impersonal FE notice predicts that tomatoes seem likely to become fashionable in ジェノヴァ. Preserve the explicit city and prospective しそう likelihood;no existing boom,earned flag or completed transaction is asserted.',
}

if __name__=='__main__':
    assert not ROOT.exists()
    lead=deepcopy(next(b for b in read(INVENTORY)['blocks'] if b['block']==177))
    clean=Path('work/clean.nds');im=NdsImage.open(clean)
    block=IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[177]
    assert sha(clean.read_bytes())=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    assert sha(block)==lead['clean_block_sha256']=='42bb6680bf654047f411c22c3a5e7fbcab2cc7cc23327a5297797aa85fb77935'
    assert len(block)==488 and lead['speeches']==len(lead['records'])==10
    assert lead['source_selectors']==[174,175,254] and lead['source_macro_counts']=={'FI':0,'FA':0,'FO':0}
    assert lead['FE_panels']==1 and lead['relative_sites']==lead['typed_menu_2100_commands']==lead['typed_actor_style_4100_commands']==0
    commands=lead['complete_native_commands'];assert len(commands)==13
    assert [(c['offset'],c['whole_command_hex']) for c in commands if c['word']!=0x4000]==[(8,'00a0ffff01090fa1'),(480,'00c2'),(482,'00000000')]
    assert not any(c['word'] in [0x100,0x200,0x300,0x400,0x8000,0x8100,0x2000] or c['word']&0xFF00==0x6300 for c in commands)
    for c in commands:
        at=c['offset'];assert block[at:at+c['native_extent']].hex()==c['whole_command_hex']
    assert {r['source_record_index'] for r in lead['records']}==set(MEANINGS)
    for r in lead['records']:
        at=r['source_reference']['offset'];raw=bytes.fromhex(r['source_hex'])
        assert block[at:at+len(raw)]==raw and block[at+len(raw)]==0
        assert block[at-5:at+1].hex()==r['source_complete_preamble_hex'] and raw[1:].decode('cp932')==r['source_Japanese']
        r.update(fresh_source_gloss=MEANINGS[r['source_record_index']],whole_exchange_context=CONTEXT,
            clean_source_complete_exchange_read_before_predecessor_English=True)
    ROOT.mkdir(parents=True)
    transcript=ROOT/'SC2_B177_complete_clean_exchange_and_glosses.txt';lines=[CONTEXT]
    for r in lead['records']:
        lines.extend(['\n'+r['id']+' selector'+format(r['source_selector'],'02X'),r['source_Japanese'],r['fresh_source_gloss']])
    transcript.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    save(ROOT/'all10_complete_B177_exchange_and_fresh_glosses.json',dict(format='dk4-editorial-clean-source-context-v1',source_ROM=str(clean),
        source_ROM_sha256=sha(clean.read_bytes()),source_SC2_sha256=sha(im.read_file('/data/SC2.DK4')),block=lead,total_editorial_objects=10,
        whole_exchange_context=CONTEXT,source_transcript=str(transcript),source_transcript_sha256=sha(transcript.read_bytes()),
        all10_clean_source_read_and_individually_glossed_before_predecessor_English=True,source_progressive_speeches=9,source_FE_speeches=1,
        source_relative_site_count=0,source_predicate_count=0,source_A000_count=1,source_C200_count=1,source_declared_end_offsets=[482],
        source_static_actor_selectors=[174,175],source_FE_notice_is_impersonal_prospective_city_commodity_fashion=True,
        AE_AF_names_voices_city_food_and_complete_native_controls_to_bind=True,
        current_names_voices_terms_entry_conditions_native_layout_actual_and_release_still_pending=True,no_predecessor_English_exposed=True,
        no_new_ROM_registry_ledger_orreview_credit=True,source_prose_or_completion_credit_added=0,new_emulator_runs=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [INVENTORY,transcript,Path(__file__)]}))
    print(dict(clean_objects=10,progressive=9,FE=1,commands=13,selectors=[174,175,254],FI=0,FA=0,FO=0,A000=1,C200=1,end=482,current_English_unexposed=True,credit=0))
