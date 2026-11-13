"""Read and gloss the complete32-speech B175 encounter before earlier English."""
from copy import deepcopy
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B175_clean_context_v4502')
INVENTORY=Path('work/analysis/lil_B161_B180_clean_scope_v3910/complete_clean_B161_B180_next_exchange_inventory.json')
CONTEXT=(
    'Read B175 as one complete32-speech exchange. Lil notices a familiar person;source09 looks,then the FE-speaking woman recognizes Lil from an earlier encounter. '
    'Lil identifies her as the woman pirate from before;the woman remarks on unexpectedly meeting here. SourceB7 threatens the two visitors for coming alone, '
    'and09 realizes they have been surrounded unnoticed. Lil accuses the woman of cowardly numbers;sourceB8 angrily calls her a brat,09 worries about her picking a fight here,andB7 urges surrender. '
    'The woman orders her people to stop;B9 questions that decision. She rebukes them as pirates with pride rather than common thugs. Lil privately revises her impression. '
    'Keep the change from recognition to danger,outnumbered defiance and the woman asserting her own standard. Bind09/B7/B8/B9 native names and voices later;do not assign identities from an English draft. '
    'The source address お嬢ちゃんたち is a speaker-owned diminutive directed at the two;resolve its contextual force after binding09 rather than inventing the companion\'s gender. '
    'No city,venue name,formal pirate rank,previous battle outcome or number of surrounding pirates is stated.\n\n'
    'The woman says she does not intend to kill Lil here and will settle matters at sea as a pirate,warning Lil not to run then. This is her stated future challenge,not an actual attack or a claim that Lil is also a pirate. '
    'Lil defiantly refuses to run. The woman likes her nerve and asks her name;Lil supplies source FI andFA. The woman teases the surprisingly cute 提督 andthen notices something. '
    'Bind the project\'s approved role terminology separately;the source form does not authorize adding a new commission,navy or official rank. Lil interprets the pause defensively. '
    'The woman comments on the good sword Lil carries,says it seems ill-suited to her andthreatens to take it for herself someday. Lil is confused;the woman declines to explain andorders her men to leave. '
    'Do not name the woman or sword,add a power,price,inheritance,ownership transfer or completed theft,or turn the sword comment into a physical-size claim. '
    'Keep the delayed notice,unexplained significance andfuture threat. Her crew\'s response is a rough cheer/acknowledgment,not an added Captain title.\n\n'
    'After the departure,09 is relieved andsays this time seemed hopeless. Lil insists it is better to act confidently with people like that. '
    '09 remarks on the woman\'s intimidating presence,teasing that Lil is scary too butthe pirate is even more so. Lil protests the unnecessary jab,then admits the challenge to settle things at sea is pretty cool. '
    '09 objects that she is too carefree:the pirate will keep chasing them from now on. That is the companion\'s worried interpretation,not a proven game-state flag or an already observed pursuit. '
    'Lil confidently says things will work out andshe will not lose;09 closes with affectionate/exasperated recognition of her fierce competitiveness. '
    'Preserve recognition,danger,rough banter,pirate pride,defiance,sword mystery,relief,teasing,admiration andworry as an emotional progression. Add no romance,kinship,ally status,formal duel terms or completed combat.\n\n'
    'The source contains23 progressive speeches andnine genuine FE system-paper speeches,five FI/FA tokens total (FI4,FA1),noFO,no typed menu/style,no predicate,no relative branch,no A000 andno2000 pause. '
    'Preserve both original declared endwords andC200. Exact source controls,anonymous FE identity/portrait ownership,current macro expansion,static names,approved terminology,native planes andactual transitions require separate binding. '
    'No current English is read by this producer andno editorial or completion credit is added.'
)
MEANINGS={
    6:'Lil wonders whether she recognizes that person. Preserve uncertain familiarity rather than immediate named recognition;the following exchange identifies the earlier pirate encounter.',
    10:'Source09 looks to see whom Lil means. Preserve the brief curious response without supplying a name or a relationship before native binding.',
    14:'The FE-speaking woman recognizes Lil as the person from the earlier encounter. Preserve spontaneous recognition andthe unfinished reference without naming a date,place or outcome.',
    18:'Lil suddenly recognizes her as the woman pirate from that earlier time. Preserve the startled/faltering recognition andpirate identification;do not invent the woman\'s name.',
    21:'The woman remarks that she never expected to meet Lil in a place like this. Preserve surprise without naming the location or implying a planned meeting.',
    24:'SourceB7 taunts the two visitors for having the nerve to come here alone,andasks whether they expect to leave unharmed. Preserve the threat,two-person isolation andspeaker-owned お嬢ちゃんたち diminutive;resolve09\'s identity/gender later andadd no headcount or injury.',
    28:'Source09 realizes they have been surrounded without noticing it,addressing FI andasking what to do. Preserve fear,the unnoticed encirclement andthe actual FI runtime substitution,not a fixed name or Captain title.',
    32:'Lil accuses the woman of using cowardly tactics by surrounding them with many people. Keep it as Lil\'s angry question/accusation,not narrator-confirmed proof that the woman ordered the ambush.',
    36:'SourceB8 angrily reacts to Lil\'s accusation andcalls her a brat. Preserve rough indignation without adding profanity,a physical attack or a new rank.',
    40:'Source09 addresses FI in exasperation andworries about what Lil hopes to accomplish by picking a fight here. Preserve the name macro andanxious objection,not an instruction to attack.',
    44:'SourceB7 laughs roughly andtells the two to give up/resign themselves. Preserve the threatening surrender demand without inventing an arrest,death or completed capture.',
    47:'The woman sharply orders her own people to stop. Preserve the abrupt authority andtarget of the rebuke,not an order for Lil to surrender.',
    51:'SourceB9 asks whether the woman is sure/is all right with that. Preserve the questioning deference without adding an explicit permission to kill or an official Captain address.',
    55:'The woman says she has told them repeatedly that they are not common thugs andshould have pride as pirates. Preserve her rebuke andpirate standard without declaring them lawful,merciful in every situation or members of a named organization.',
    59:'Lil privately reacts with interest to what this reveals about the woman. Preserve the aside andreassessment without adding admiration as a confirmed alliance,friendship or moral verdict.',
    63:'The woman says she has no intention of killing Lil here. As a pirate,she will settle matters at sea,andwarns Lil not to run when that time comes. Preserve killing as the stated intent she rejects here,the future sea challenge andwarning;do not invent immediate combat,formal duel terms or Lil\'s pirate status.',
    66:'Lil emphatically says she will not run,as if that should be obvious. Preserve her bold refusal without claiming an actual battle or a successful escape.',
    69:'The woman responds approvingly to Lil\'s bold words,says she likes her nerve andasks her name. Preserve the shift from confrontation to grudging interest,not a friendship or recruitment offer.',
    73:'Lil gives her first andfamily names using the exact FI andFA substitutions,with the Japanese separator between them. Preserve both runtime tokens andtheir order;bind natural approved English name spacing separately,without inventing a title.',
    77:'The woman comments on the surprisingly cute 提督,then abruptly notices something. Preserve teasing andthe distinct surprised pause before her sword observation. Bind approved role terminology later;do not invent a formal navy commission or notice the sword before this beat.',
    81:'Lil defensively asks what the woman means andwhether she has another complaint. Preserve her irritation andmisreading of the pause,not knowledge of the sword\'s significance.',
    84:'The woman tells Lil she carries a good sword,says it seems not to suit/be worthy of her andthreatens to take it for herself someday. Preserve the woman\'s assessment andfuture intention,not a measured size,named treasure,sword power or completed transfer.',
    88:'Lil asks what the woman is talking about. Preserve her genuine confusion;do not insert an explanation of the sword or a demand to hand it over.',
    92:'The woman says it is fine if Lil does not understand,then calls her men to withdraw. Preserve the dismissive refusal to explain anddeparture order without inventing a destination or formal rank.',
    95:'SourceB7 gives a loud rough cheer/acknowledgment to the departure order. Preserve the energetic response without adding an unspoken Captain address or new action.',
    99:'Source09 expresses relief at being safe andsays this time seemed hopeless. Preserve the relieved uncertainty andfear without inventing a specific earlier near-death episode.',
    102:'Lil says it is better to act tough/confidently with people like that. Preserve her self-assured explanation as her attitude,not a universal narrator guarantee or a threat to kill them.',
    105:'Source09 remarks on the woman\'s overwhelming presence,andteases FI that Lil is frightening too butthe woman is even more so. Preserve the FI substitution,comparison andhesitant joking tone without changing it into a literal combat-stat comparison.',
    109:'Lil protests that the companion\'s jab was unnecessary,then says the woman\'s proposal to settle things at sea is pretty cool. Preserve irritation turning to youthful admiration for that challenge,not agreement to formal duel rules or approval of all piracy.',
    113:'Source09 objects to cool andsays Lil is too carefree,because the pirate will keep chasing them from now on. Preserve this worried future interpretation without asserting actual pursuit or a newly earned event flag.',
    117:'Lil confidently says things will somehow work out andshe will not lose. Preserve optimistic defiance without supplying a plan,guaranteed victory or completed combat.',
    120:'Source09 closes by remarking on how strong Lil\'s competitive spirit is. Preserve the affectionate/exasperated reaction to her confidence,not a new romantic or family relationship.',
}

if __name__=='__main__':
    assert not ROOT.exists()
    lead=deepcopy(next(b for b in read(INVENTORY)['blocks'] if b['block']==175))
    clean=Path('work/clean.nds');image=NdsImage.open(clean);block=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[175]
    assert sha(clean.read_bytes())=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    assert sha(block)==lead['clean_block_sha256']=='3bf9d6678ada4a07930036b5b76a5b498eb7492088ae000124ee6c286852dc1e'
    assert len(block)==1712 and lead['speeches']==len(lead['records'])==32
    assert lead['source_selectors']==[2,9,183,184,185,254] and lead['source_macro_counts']=={'FI':4,'FA':1,'FO':0}
    assert lead['FE_panels']==9 and lead['typed_menu_2100_commands']==lead['typed_actor_style_4100_commands']==lead['relative_sites']==0
    commands=lead['complete_native_commands'];assert len(commands)==39
    assert [c['offset'] for c in commands if c['word']==0]==[1702,1706]
    assert [(c['offset'],c['whole_command_hex']) for c in commands if c['word']!=0x4000]==[
        (8,'0060'),(10,'4463'),(72,'9646ca80'),(1264,'35467d80'),(1700,'00c2'),(1702,'00000000'),(1706,'00000000')]
    assert not any(c['word'] in [0x100,0x200,0x300,0x400,0x8000,0x8100,0xA000,0x2000] for c in commands)
    for c in commands:
        at=c['offset'];assert block[at:at+c['native_extent']].hex()==c['whole_command_hex']
    assert {r['source_record_index'] for r in lead['records']}==set(MEANINGS)
    for row in lead['records']:
        at,raw=row['source_reference']['offset'],bytes.fromhex(row['source_hex'])
        assert block[at:at+len(raw)]==raw and block[at+len(raw)]==0
        assert block[at-5:at+1].hex()==row['source_complete_preamble_hex'] and raw[1:].decode('cp932')==row['source_Japanese']
        row.update(fresh_source_gloss=MEANINGS[row['source_record_index']],whole_exchange_context=CONTEXT,
            clean_source_complete_exchange_read_before_predecessor_English=True)
    ROOT.mkdir(parents=True);transcript=ROOT/'SC2_B175_complete_clean_exchange_and_glosses.txt';lines=[CONTEXT]
    for row in lead['records']:lines.extend(['\n'+row['id']+' selector'+format(row['source_selector'],'02X'),row['source_Japanese'],row['fresh_source_gloss']])
    transcript.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    save(ROOT/'all32_complete_B175_exchange_and_fresh_glosses.json',dict(format='dk4-editorial-clean-source-context-v1',
        source_ROM=str(clean),source_ROM_sha256=sha(clean.read_bytes()),source_SC2_sha256=sha(image.read_file('/data/SC2.DK4')),
        block=lead,total_editorial_objects=32,whole_exchange_context=CONTEXT,source_transcript=str(transcript),source_transcript_sha256=sha(transcript.read_bytes()),
        all32_clean_source_read_and_individually_glossed_before_predecessor_English=True,
        source_progressive_speeches=23,source_FE_speeches=9,source_relative_site_count=0,source_predicate_count=0,source_A000_count=0,
        source_C200_count=1,source_declared_end_offsets=[1702,1706],source_static_actor_selectors=[2,9,183,184,185],
        FE_anonymous_woman_identity_and_portrait_ownership_to_bind=True,source09_identity_and_diminutive_address_context_to_bind=True,
        current_names_voices_terms_entry_conditions_native_layout_actual_and_release_still_pending=True,
        no_predecessor_English_exposed=True,no_new_ROM_registry_ledger_orreview_credit=True,source_prose_or_completion_credit_added=0,
        new_emulator_runs=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [INVENTORY,transcript,Path(__file__)]}))
    print(dict(clean_objects=32,progressive=23,FE=9,structural_commands=39,selectors=[2,9,183,184,185,254],
        FI=4,FA=1,FO=0,relative_sites=0,predicates=0,A000=0,C200=1,ends=[1702,1706],
        current_English_unexposed=True,ledger_credit=0,full_goal_active=True))
