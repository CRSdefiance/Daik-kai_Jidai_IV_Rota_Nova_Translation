"""Read/gloss all33 clean B170 speeches before exposing predecessor English."""
from copy import deepcopy
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_B170_clean_context_v4257')
INVENTORY = Path('work/analysis/lil_B161_B180_clean_scope_v3910/complete_clean_B161_B180_next_exchange_inventory.json')
CONTEXT = '''B170 is one complete33-speech collision,argument,apology,flattery and invitation exchange. Selector02 is Lil;selector19hex/25decimal is the other speaker,whose original nameplate/catalogue and approved English spelling must be freshly bound before authoring. The other speaker eventually introduces herself as イファ. Start with Lil's startled cry,then the other speaker's hurried apology. Lil objects that she has collided with her and expects more;the other speaker insists she apologized,finds Lil persistent and says she has no time for this. Lil angrily challenges her wording and orders her closer. The speaker abruptly accepts fault and apologizes,disarming Lil. Her familiar お姉さん address to this stranger carries no proved sister relationship or exact age. Localize it naturally without creating family,rank or romance. The compliment that Lil is actually kind and the impressed response to her Admiral/fleet claim flatter Lil into helping;do not assert secret manipulative motives as narrator fact.
Lil offers advice,explicitly says she is an Admiral and explains that she leads FO at sea. Preserve FO exactly;this source supplies the Admiral claim here rather than making it an inherited rank for every speaker. Lil had thought the other speaker merely a cheeky brat but now sees a likable side;this is her changing characterization,not a narrator's numeric age. Lil asks what is wrong and suggests money as a question,not an established debt. The speaker ran away from her teacher/master and wants to go out into the world. She was training in 道術,Daoist/Taoist arts,and became fed up with constant scolding. Retain this cultural discipline;bind existing reviewed terminology before choosing final localized wording. The teacher's gender,personal name,school,nationality,rank and techniques are not supplied. Add no physical abuse,expulsion,crime,romantic escape,spell list or numerical skill level.
She does not want to quit training because then she could not prove herself to/show up her teacher. Instead she wants to travel the world,keep training and become much stronger. This is a resolve to improve and vindicate herself,not an announced intention to kill her teacher or a literal combat/revenge quest. Lil is baffled by the Daoist discipline but sympathizes with the desire to prove the teacher wrong. The speaker celebrates being understood and asks for passage aboard Lil's ship. Lil cautions that going to sea is not a game and asks whether she has the resolve never to be beaten by others. The speaker reassures her by citing harsh training she has already endured. Lil sees that her decision is firm,agrees and asks her name. The speaker gives イファ and asks Lil's. Lil gives FI and encourages her to work hard and prove herself to her teacher. Preserve FI exactly and both the firm-resolution test and encouraging final acceptance;invent no fee,job assignment,item,reward,family bond,nationality,named port or earned recruitment state.
All33 speeches are read as one exchange before older English exposure. Source bytes retain45 commands:33 progressive speeches and12 nonrelative leaves,selectors02/19,FI1/FO1,no FA,FE,typed choice,relative site or membership predicate. Preserve the two-byte2000 pause,the exact source presentation/resource words,the later A000,C200 and consecutive endwords1852/1856. Their full original consumer/effect/eligibility contracts still need fresh current binding;do not infer semantics merely from numeric words. This clean/gloss pass adds zero ledger/source-prose/completion credit. Current names,voices,terms,preambles,source entry/effects,native layout,representative behavior and registered integration remain pending. Every wider editorial family remains open;graphics and the later older-record technical re-audit stay separate.'''
MEANINGS = {
    6:'Lil gives a short startled cry at the collision. Preserve the sudden reaction without inventing an injury or particular body contact.',
    11:'The other speaker briefly apologizes and says she is in a hurry. Keep the casual,rushed apology and urgency without inventing where she is going.',
    15:'Lil protests that the speaker suddenly bumped into her and asks whether that is all she has to say. Preserve her demand for a fuller apology rather than inventing compensation.',
    19:'The speaker insists she already said she is in a hurry and already apologized properly. Preserve the defensive irritation and her own claim of having apologized.',
    22:'Lil disputes that the apology was properly made. Her pointed emphasis continues the argument without alleging a new insult.',
    26:'The speaker complains that Lil is being persistent. Preserve the exasperated dismissal and colloquial voice.',
    30:'Lil angrily demands to know what the speaker just said. Preserve the escalation and incredulity without an invented threat of specific violence.',
    34:'The speaker says she does not have time to be doing this. This attempts to end the argument,not a statement of a named emergency.',
    37:'Lil challenges what the speaker means by this,remarks on her nerve and orders her to come closer. Preserve the angry challenge and command without adding a fight or punishment.',
    41:'The speaker abruptly softens,addresses the older female stranger familiarly,accepts that she was wrong and apologizes. Preserve the reversal and hesitant appeal;お姉さん does not prove kinship.',
    45:'Lil is caught off guard by the apology,then says it is fine as long as the speaker understands. Preserve the flustered softening and conditional acceptance.',
    49:'The speaker says Lil is actually kind. Keep the friendly/flattering reassessment as her speech,not a narrator guarantee or a family relationship.',
    53:'Lil agrees with a little hesitation and boasts that people often say that about her. Preserve her vanity and newly friendly response.',
    57:'The speaker asks whether Lil will listen to her problem/give advice because she is in serious difficulty. Preserve the tentative request and problem without specifying money yet.',
    61:'Lil agrees and invites her to explain anything,boasting that she is an Admiral after all. This source explicitly supplies that rank;add no higher office or unrelated command.',
    64:'The speaker repeats Admiral as a surprised question. Preserve her surprise rather than agreement or a formal salute.',
    68:'Lil explains that she sails while leading the fleet called FO. Preserve the exact FO substitution and fleet/leadership explanation without adding ships,numbers or ownership details.',
    71:'The speaker reacts with admiration and tells Lil she is impressive. Her familiar address creates no sisterhood or romantic implication.',
    74:'Lil says she had thought the speaker just a cheeky brat but sees a likable/cute side after all. Preserve the contrast and changing mood as Lil\'s opinion;no exact age is stated.',
    78:'Lil asks what the problem is and tentatively suggests money. Keep money as a question rather than asserting debt,poverty or a payment request.',
    82:'The speaker says she ran away from her teacher/master and wants to go out into the world. Preserve the departure and broader aim;the teacher\'s gender and location remain unspecified.',
    86:'Lil says she does not quite follow and asks why the speaker ran away in the first place. Preserve confusion and the request for the original reason.',
    90:'The speaker had been training in 道術,Daoist/Taoist arts,but became fed up because her teacher constantly scolded her. Preserve the cultural discipline,training and repeated reprimands;do not invent abuse,expulsion or gender.',
    94:'She says that if she stops training now,she will not be able to prove herself to/show up her teacher. Preserve the conditional reason to continue training rather than a new violent revenge goal.',
    97:'She wants to travel around the world while continuing training and become much stronger. Preserve both travel and continued practice,not merely an escape from study.',
    100:'Lil repeats the unfamiliar Daoist-training idea with bafflement and asks what it is. Keep her lack of understanding and the cultural term without supplying a lesson the source does not give.',
    104:'Lil nevertheless says she can somewhat understand wanting to prove the teacher wrong/show the teacher up. Preserve the qualified sympathy and the same unspecified teacher referent.',
    108:'The speaker celebrates that Lil understands and asks to be allowed aboard her ship. Preserve the excited shift from sympathy to the explicit passage/joining request.',
    111:'Lil warns that going to sea is not a game and asks whether the speaker has enough determination never to lose to anyone else. Preserve the seriousness and test of resolve;invent no numeric skill prerequisite or guaranteed victory.',
    114:'The speaker reassures her by saying she has endured harsh training up to now. Preserve past endurance as the reason for confidence without inventing a particular ordeal.',
    118:'Lil judges her decision firm,agrees and asks her name. Preserve both acceptance and the request for an introduction without inventing a job or formal contract.',
    121:'The speaker gives her name as イファ and asks Lil\'s name. The approved English spelling and source-owned nameplate/catalogue still need binding;the familiar address creates no kinship.',
    125:'Lil gives FI as her own name and encourages イファ to work hard and prove herself to her teacher. Preserve FI,personal encouragement and the original motivation without adding a reward,romance or combat target.',
}

if __name__ == '__main__':
    assert not ROOT.exists()
    lead=deepcopy(next(b for b in read(INVENTORY)['blocks'] if b['block']==170))
    clean=Path('work/clean.nds')
    image=NdsImage.open(clean)
    block=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[170]
    assert sha(clean.read_bytes())=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    assert sha(block)==lead['clean_block_sha256']=='e0926b0d4f96d701b614d3f236d2caf68fd79c774d0e7df6c696fea99818f3e3'
    assert len(block)==1860 and lead['speeches']==len(lead['records'])==33
    assert lead['source_selectors']==[2,25] and lead['source_macro_counts']=={'FI':1,'FA':0,'FO':1}
    assert lead['FE_panels']==lead['typed_menu_2100_commands']==lead['typed_actor_style_4100_commands']==lead['relative_sites']==0
    assert len(lead['complete_native_commands'])==45
    assert [c['offset'] for c in lead['complete_native_commands'] if c['word']==0]==[1852,1856]
    assert [c['offset'] for c in lead['complete_native_commands'] if c['word']==0x2000]==[36]
    for c in lead['complete_native_commands']:
        at=c['offset']
        assert block[at:at+c['native_extent']].hex()==c['whole_command_hex']
    assert {r['source_record_index'] for r in lead['records']}==set(MEANINGS)
    for row in lead['records']:
        at,raw=row['source_reference']['offset'],bytes.fromhex(row['source_hex'])
        assert block[at:at+len(raw)]==raw and block[at+len(raw)]==0
        assert block[at-5:at+1].hex()==row['source_complete_preamble_hex']
        assert raw[1:].decode('cp932')==row['source_Japanese']
        row.update(fresh_source_gloss=MEANINGS[row['source_record_index']],whole_exchange_context=CONTEXT,
                   clean_source_complete_exchange_read_before_predecessor_English=True)
    ROOT.mkdir(parents=True)
    transcript=ROOT/'SC2_B170_complete_clean_exchange_and_glosses.txt'
    lines=[CONTEXT]
    for row in lead['records']:
        lines.extend(['\n'+row['id']+' selector'+format(row['source_selector'],'02X'),row['source_Japanese'],row['fresh_source_gloss']])
    transcript.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    save(ROOT/'all33_complete_B170_exchange_and_fresh_glosses.json',dict(format='dk4-editorial-clean-source-context-v1',
        source_ROM=str(clean),source_ROM_sha256=sha(clean.read_bytes()),source_SC2_sha256=sha(image.read_file('/data/SC2.DK4')),
        block=lead,total_editorial_objects=33,whole_exchange_context=CONTEXT,source_transcript=str(transcript),
        source_transcript_sha256=sha(transcript.read_bytes()),all33_clean_source_read_and_individually_glossed_before_predecessor_English=True,
        current_names_voices_terms_entry_conditions_macros_native_layout_actual_and_release_still_pending=True,
        no_predecessor_English_exposed=True,no_new_ROM_registry_ledger_orreview_credit=True,source_prose_or_completion_credit_added=0,
        new_emulator_runs=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [INVENTORY,transcript,Path(__file__)]}))
    print(dict(clean_objects=33,commands=45,selectors=[2,25],FI=1,FO=1,FE=0,menus=0,current_English_unexposed=True,ledger_credit=0,full_goal_active=True))
