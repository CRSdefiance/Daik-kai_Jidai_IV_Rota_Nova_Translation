"""Read/gloss the complete27-speech clean B172 exchange before predecessor English."""
from copy import deepcopy
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B172_clean_context_v4361')
INVENTORY=Path('work/analysis/lil_B161_B180_clean_scope_v3910/complete_clean_B161_B180_next_exchange_inventory.json')
CONTEXT='''Read B172 as one complete27-speech exchange:the source-named ユリアン and 美華 banter while Lil overhears,then Lil speaks to 美華 after the man rushes away. Their familiar flirting does not establish a romantic partnership,marriage,kinship,an official rank or a named prior date. Bind approved current spellings from the original names/catalogue before choosing spoken English names;until then these clean glosses retain the Japanese names. His extravagant declaration that he lives for her radiant smile and that her smile supplies his power are romantic hyperbole and characterization,not literal life dependence or a numeric skill effect. Lil's initially incredulous aside about saying such a line so confidently establishes her dry skepticism. 美華 does not acknowledge Lil until after the man's departure and Lil's tentative interruption;do not invent that the aside starts a three-way argument.
His confusion at not receiving her usual smile leads to an anxious question about whether she no longer likes him. She denies that explanation and says his words normally cheer her up,but lately she cannot stop thinking about something she desperately wants. Preserve the change from flirtation to preoccupation,not an invented illness,insomnia,anger,betrayal or breakup. He asks what she wants. She names 新羅の金冠 and says its name sounds mysterious and that it is apparently very precious. 新羅 refers to Silla,but bind the exact reviewed item title later and add no history,treasure location,material purity,power or country exposition. He thinks it sounds expensive,wonders whether he can afford it and asks where it is sold. She says it apparently is not sold in shops and that she has heard it is in 京城. Preserve hearsay and uncertainty and bind the approved town name later;do not invent a specific shop,ruin,temple,palace,city district or coordinate.
The absence of a shop gives him a sudden idea of an unstated place. She asks if he has a lead;he confidently promises to obtain the crown quickly and restore her smile. He then asks whether she will go on a date with him once he gets it. This is an explicit conditional date request;retain that intent without making it sexual or converting it into an existing relationship. Her reply points out that he has not found it yet and is getting ahead of himself,then says she will think about it. That is a qualified response,not agreement to a date. He excitedly treats it as a promise,asks her not to forget and rushes off toward 京城. Preserve this intentional mismatch between her hedge and his enthusiasm. She starts to say she is counting on him,then notices he has already gone;keep the comic interruption and do not invent a promise she actually made.
Lil then tentatively interrupts. 美華 welcomes her and apologizes for not noticing. Lil admits she overheard and asks what the named crown actually is. 美華 says she was told but forgot,and only remembers that it is extremely beautiful. Do not turn her vague secondhand memory into a firsthand sighting,an established description or secret lore. Lil becomes curious and wants to see it too. 美華 offers to show it to Lil if she gets it;do not specify who will obtain it or claim she already owns it. Lil declines because she intends to find it herself,and confirms the city previously mentioned. 美華 says it seems to be there but she does not know where within the city. Lil says that is enough and plans to ask people while searching once she arrives. This is a general search plan,not a completed journey,a precise lead,an earned quest flag or a competition explicitly declared in the source. 美華 closes by asking Lil to show it to her when Lil obtains it:preserve the reversal of the earlier offer and the light comic give-and-take.
All27 clean speeches are read/glossed as this whole exchange before predecessor English comparison. Source selectors02/1A/C9 are executable actors2/26/201,not literal printable dialogue. There are no FI/FA/FO substitutions,FE panels,typed choices,relative sites,membership predicates or2000 pauses. Preserve all38 commands and11 nonspeech leaves:6000,45FF,6329,4651,6340,4620,632A,C200,A000,6240 and one tail end1880. The A000 raw bytes are00a0ffff010cc960;record hex words0C01/60C9 without inferring a packed quest/recruitment meaning. Unlike the earlier B170 effect order,this source places C200 before A000 and6240. Their actual consumers,names,presentation,entry conditions,native layout,return and registered integration remain to be bound. No English manuscript,ROM,ledger credit or completed review is created by this clean-source lead. Keep every wider editorial family open;graphics and the later older-record technical re-audit stay separate.'''

MEANINGS={
    7:'The man addresses 美華 and extravagantly says he lives for her radiant,overflowing smile. Preserve the flattering romantic hyperbole without making it literal dependence or establishing a relationship.',
    11:'美華 gently reacts to ユリアン with a familiar you-again-style address and trailing pause. Preserve the mild familiar response without inventing a laugh,blush,rank or biological relationship.',
    15:'Lil pauses,then marvels incredulously that he can say a line like that so openly/confidently. Keep her dry aside and embarrassment at the florid talk without inventing a public confrontation.',
    18:'The man is confused because she normally smiles at this point,and asks whether she has stopped liking him. Preserve his expectation,anxiety and question,not a confirmed rejection.',
    22:'She denies that explanation. Normally hearing his words perks her up,but this time she trails off. Preserve the reassurance and unfinished lead into her preoccupation.',
    26:'She confides that there is something she desperately wants,and lately she cannot get it out of her head,waking or sleeping. Preserve the persistent longing without diagnosing insomnia or illness.',
    30:'He addresses 美華 and says such an expression does not suit her,then asks what she wants so badly. Keep his solicitude and question without asserting that he knows the object already.',
    34:'She names 新羅の金冠,asks whether the name sounds mysterious,and says it is apparently very precious. Preserve the title and hearsay,without adding historical background or magical powers.',
    38:'He thinks it sounds expensive,wonders if he can afford it and asks where it is sold. Preserve his tentative affordability concern,not an actual purchase or a fixed price.',
    41:'She explains that it apparently is not sold in stores,and that she has heard it is in 京城. Preserve both uncertain reports and the named city without adding a precise location.',
    44:'He repeats that it is not sold in stores,pauses in sudden realization and decides it must be at an unstated place. Preserve his idea and certainty as his own,without naming a shop,ruin or temple.',
    47:'She asks in pleased surprise whether he has an idea where it could be. Preserve the question rather than turning the lead into confirmed knowledge.',
    51:'He tells her to leave it to him and promises to get 新羅の金冠 as quickly as possible and restore her smile. Keep his enthusiastic pledge as future intent,not an accomplished result.',
    55:'He playfully says her smile is the source of his power,then asks whether she will go on a date with him once he gets the crown. Preserve the hyperbole and explicit conditional request without claiming agreement.',
    58:'She points out he has not found it yet and is getting ahead of himself,then says she will think about it. Preserve the qualification:the source does not promise a date.',
    62:'He celebrates,treats her qualified reply as a promise,asks her not to forget,and says he is going to 京城 right away. Preserve his overeager interpretation and haste without changing her prior response.',
    65:'She starts to say she is counting on him,then notices he has already left. Preserve the interrupted thought and comic departure beat.',
    68:'Lil tentatively gets her attention with a trailing opening. Preserve the hesitant interruption without adding an introduction or title.',
    72:'The woman welcomes Lil and apologizes for not noticing her earlier. Preserve the simple welcome and apology without inventing a prior relationship.',
    75:'Lil says she overheard the conversation and asks what 新羅の金冠 actually is. Preserve the admission and curiosity without giving Lil existing knowledge of the object.',
    78:'The woman is unsure:she was told but forgot,and remembers only that it is extremely beautiful. Keep her vague secondhand memory rather than making it a firsthand sighting or detailed description.',
    82:'Lil responds thoughtfully and says she has become a little interested in seeing it too. Preserve the developing curiosity after her earlier skepticism.',
    85:'The woman notices Lil is interested too and offers to show it to her if she gets it. Keep the conditional offer without supplying who will find it or claiming present ownership.',
    88:'Lil declines firmly because she intends to find it herself,and confirms that the woman said it was in 京城. Preserve her independent resolve and the question about the city.',
    92:'The woman says it seems to be in 京城,but she does not know where in the city. Preserve the uncertainty and limited extent of the lead.',
    96:'Lil says that is enough information and plans to ask people and search once she gets there. Preserve her confident future search plan without adding coordinates,a specific informant or completed progress.',
    100:'The woman asks Lil to show it to her if Lil obtains it. Preserve the reversal of the earlier offer and light closing request without inventing a transfer or reward.',
}

if __name__=='__main__':
    assert not ROOT.exists()
    lead=deepcopy(next(b for b in read(INVENTORY)['blocks'] if b['block']==172))
    clean=Path('work/clean.nds');image=NdsImage.open(clean);block=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[172]
    assert sha(clean.read_bytes())=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    assert sha(block)==lead['clean_block_sha256']=='feb4596dcc453b242d6e13aedb93aa1908699ea00f2d23750ff230be457ca59e'
    assert len(block)==1884 and lead['speeches']==len(lead['records'])==27
    assert lead['source_selectors']==[2,26,201] and lead['source_macro_counts']=={'FI':0,'FA':0,'FO':0}
    assert lead['FE_panels']==lead['typed_menu_2100_commands']==lead['typed_actor_style_4100_commands']==lead['relative_sites']==0
    commands=lead['complete_native_commands']
    assert len(commands)==38 and [c['offset'] for c in commands if c['word']==0]==[1880]
    assert [c['word'] for c in commands if c['word']!=0x4000]==[0x6000,0x45FF,0x6329,0x4651,0x6340,0x4620,0x632A,0xC200,0xA000,0x6240,0]
    assert not any(c['word'] in [0x2000,0x8000] for c in commands)
    assert next(c['whole_command_hex'] for c in commands if c['word']==0xA000)=='00a0ffff010cc960'
    for c in commands:
        at=c['offset'];assert block[at:at+c['native_extent']].hex()==c['whole_command_hex']
    assert {r['source_record_index'] for r in lead['records']}==set(MEANINGS)
    for row in lead['records']:
        at,raw=row['source_reference']['offset'],bytes.fromhex(row['source_hex'])
        assert block[at:at+len(raw)]==raw and block[at+len(raw)]==0
        assert block[at-5:at+1].hex()==row['source_complete_preamble_hex'] and raw[1:].decode('cp932')==row['source_Japanese']
        row.update(fresh_source_gloss=MEANINGS[row['source_record_index']],whole_exchange_context=CONTEXT,
            clean_source_complete_exchange_read_before_predecessor_English=True)
    ROOT.mkdir(parents=True);transcript=ROOT/'SC2_B172_complete_clean_exchange_and_glosses.txt';lines=[CONTEXT]
    for row in lead['records']:lines.extend(['\n'+row['id']+' selector'+format(row['source_selector'],'02X'),row['source_Japanese'],row['fresh_source_gloss']])
    transcript.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    save(ROOT/'all27_complete_B172_exchange_and_fresh_glosses.json',dict(format='dk4-editorial-clean-source-context-v1',
        source_ROM=str(clean),source_ROM_sha256=sha(clean.read_bytes()),source_SC2_sha256=sha(image.read_file('/data/SC2.DK4')),
        block=lead,total_editorial_objects=27,whole_exchange_context=CONTEXT,source_transcript=str(transcript),source_transcript_sha256=sha(transcript.read_bytes()),
        all27_clean_source_read_and_individually_glossed_before_predecessor_English=True,
        current_names_voices_terms_entry_conditions_native_layout_actual_and_release_still_pending=True,
        no_predecessor_English_exposed=True,no_new_ROM_registry_ledger_orreview_credit=True,source_prose_or_completion_credit_added=0,
        new_emulator_runs=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [INVENTORY,transcript,Path(__file__)]}))
    print(dict(clean_objects=27,commands=38,selectors=[2,26,201],FI=0,FE=0,menus=0,current_English_unexposed=True,ledger_credit=0,full_goal_active=True))
