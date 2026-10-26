"""Read/gloss B173's complete clean exchange before predecessor English exposure."""
from copy import deepcopy
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B173_clean_context_v4410')
INVENTORY=Path('work/analysis/lil_B161_B180_clean_scope_v3910/complete_clean_B161_B180_next_exchange_inventory.json')
CONTEXT='''Read B173 as one complete11-speech exchange. Lil wonders whether someone knows about 新羅の金冠;the woman selected by source CA welcomes her. Bind that actor's approved identity and original name/voice consumers before choosing English names or a shop/tavern role. Lil tentatively asks about the crown and becomes excited when the woman has heard of it. Both speak of its beauty as reported information,not firsthand possession. The woman finds it odd that another man just asked the same question. Lil asks whether the man was ユリアン,but the woman does not remember his name;she remembers his smooth talk and thinks he went to 武寧王陵. Preserve the distinction between her uncertain recollection and Lil's later assumption that ユリアン is ahead of her. The place is described as a nearby ruin,and the crown's presence there is hearsay. The exchange develops from tentative inquiry to excitement,surprise,a tentative destination lead and Lil's competitive determination. Preserve the echo question about the named site and her vow not to lose without inventing a race rule,reward,hostility,romance,rank,biological kinship,precise distance,coordinates,confirmed ownership or actual acquisition. Bind 新羅の金冠,ユリアン and 武寧王陵 to exact current approved terminology later. B172's qualified date response remains qualified;do not insert a date promise or later B78 acquisition/transfer/location details into this conversation. The structural suffix contains two A000 objects,one8000 predicate andfour relative sites after the speeches. Preserve exact bytes and nesting;packed words and eligibility/effect semantics remain unbound in this clean lead. No predecessor English is read by this producer.'''
MEANINGS={
    6:'Lil wonders aloud whether there is anyone who knows about 新羅の金冠. Preserve the searching uncertainty and trailing thought,without supplying an informant or definite location.',
    9:'The source CA woman notices/welcomes Lil with a simple greeting. Preserve the welcome without adding a name,job,prior meeting or relationship until native identity/context binding.',
    13:'Lil hesitates about asking,then eagerly gets the woman\'s attention and asks whether she has heard of 新羅の金冠. Preserve the tentative aside followed by a direct question,not established knowledge.',
    17:'The woman cautiously says she has heard of it and asks why Lil wants to know. Preserve her guarded yes and follow-up question without making her an owner or eyewitness.',
    20:'Lil celebrates the lead,says she is looking for the crown and mentions hearing that it is very beautiful. Preserve her excited search intent and secondhand beauty report,not actual possession or sighting.',
    24:'The woman agrees that it is said to be beautiful,then remarks that it is odd because someone asked her the same thing just a little earlier. Preserve her hearsay and recent repeated question without identifying the other person yet.',
    28:'Lil reacts with surprise and asks whether that person might be named ユリアン. Preserve the tentative identification as a question,not a confirmed answer.',
    32:'The woman says she does not really remember the name,but recalls a man who was very smooth with words;it seems he went to 武寧王陵. Preserve the uncertain memory and apparently/probably departure rather than confirming his identity or present location.',
    36:'Lil repeats 武寧王陵 as a question. Preserve her need for explanation without inventing prior familiarity with the site.',
    40:'The woman explains that it is a nearby ruin and that she has heard the crown is there. Preserve the local description and report,without adding a city,country,precise distance,entrance,treasure placement or guaranteed possession.',
    44:'Lil repeats that it is a ruin,concludes that ユリアン is probably already ahead of her given what she has heard,and resolves not to lose. Preserve her inference and competitive enthusiasm as her own,not verified narration,a formal contest or hostility.',
}

if __name__=='__main__':
    assert not ROOT.exists()
    lead=deepcopy(next(b for b in read(INVENTORY)['blocks'] if b['block']==173))
    clean=Path('work/clean.nds');image=NdsImage.open(clean)
    block=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[173]
    assert sha(clean.read_bytes())=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    assert sha(block)==lead['clean_block_sha256']=='87d542a15ca09af2e1c40c8bfc950020ed1f194be90aabb9fdcc64ef62e88ecb'
    assert len(block)==768 and lead['speeches']==len(lead['records'])==11
    assert lead['source_selectors']==[2,202] and lead['source_macro_counts']=={'FI':0,'FA':0,'FO':0}
    assert lead['FE_panels']==lead['typed_menu_2100_commands']==lead['typed_actor_style_4100_commands']==0
    assert lead['relative_sites']==4
    commands=lead['complete_native_commands']
    assert len(commands)==23 and [c['offset'] for c in commands if c['word']==0]==[762]
    assert [c['word'] for c in commands if c['word']!=0x4000]==[0x6000,0x6329,0x6340,0xA000,0x8000,0x200,0x300,0x100,0xA000,0x100,0x6240,0]
    assert [(c['offset'],c['whole_command_hex']) for c in commands if c['word'] in [0xA000,0x8000]]==[
        (720,'00a0ffff010b39a2'),(728,'0080ffff000cca70'),(748,'00a0ffff010cca60')]
    for command in commands:
        at=command['offset'];assert block[at:at+command['native_extent']].hex()==command['whole_command_hex']
    assert {r['source_record_index'] for r in lead['records']}==set(MEANINGS)
    for row in lead['records']:
        at,raw=row['source_reference']['offset'],bytes.fromhex(row['source_hex'])
        assert block[at:at+len(raw)]==raw and block[at+len(raw)]==0
        assert block[at-5:at+1].hex()==row['source_complete_preamble_hex'] and raw[1:].decode('cp932')==row['source_Japanese']
        row.update(fresh_source_gloss=MEANINGS[row['source_record_index']],whole_exchange_context=CONTEXT,
            clean_source_complete_exchange_read_before_predecessor_English=True)
    ROOT.mkdir(parents=True)
    transcript=ROOT/'SC2_B173_complete_clean_exchange_and_glosses.txt';lines=[CONTEXT]
    for row in lead['records']:lines.extend(['\n'+row['id']+' selector'+format(row['source_selector'],'02X'),row['source_Japanese'],row['fresh_source_gloss']])
    transcript.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    save(ROOT/'all11_complete_B173_exchange_and_fresh_glosses.json',dict(format='dk4-editorial-clean-source-context-v1',
        source_ROM=str(clean),source_ROM_sha256=sha(clean.read_bytes()),source_SC2_sha256=sha(image.read_file('/data/SC2.DK4')),
        block=lead,total_editorial_objects=11,whole_exchange_context=CONTEXT,source_transcript=str(transcript),source_transcript_sha256=sha(transcript.read_bytes()),
        all11_clean_source_read_and_individually_glossed_before_predecessor_English=True,
        source_relative_site_count=4,source_predicate_count=1,source_A000_count=2,single_source_end_offset=762,
        current_names_voices_terms_entry_conditions_native_layout_actual_and_release_still_pending=True,
        no_predecessor_English_exposed=True,no_new_ROM_registry_ledger_orreview_credit=True,source_prose_or_completion_credit_added=0,
        new_emulator_runs=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [INVENTORY,transcript,Path(__file__)]}))
    print(dict(clean_objects=11,structural_commands=23,selectors=[2,202],FI=0,FE=0,relative_sites=4,predicates=1,A000=2,current_English_unexposed=True,ledger_credit=0,full_goal_active=True))
