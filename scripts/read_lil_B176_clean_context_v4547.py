"""Read/gloss all ten B176 banana-fad speeches before predecessor English exposure."""
from copy import deepcopy
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B176_clean_context_v4547')
INVENTORY=Path('work/analysis/lil_B161_B180_clean_scope_v3910/complete_clean_B161_B180_next_exchange_inventory.json')
CONTEXT=(
    'Read B176 as one complete ten-speech comic exchange. SourceAE enthusiastically repeats bananas and declares them the coming fashion. '
    'SourceAF echoes bananas as a doubtful question. AE insists that their taste will be a success;AF remains politely unconvinced. '
    'AE turns that hesitation into an imperious claim that if she says they will succeed,they will. AF gives in and asks what to do. '
    'AE orders AF to buy as many bananas as possible;AF responds with an offhand repeated acknowledgment. AE repeats the grand prediction '
    'and ends with a distinctive self-satisfied laugh. The closing FE notice predicts that bananas seem likely to become fashionable in セビリア. '
    'Preserve enthusiasm,doubt,insistence,compliance,purchase order,offhand response and extravagant confidence as a complete progression, '
    'then the shift to impersonal prospective news. Native AE/AF names,voices,ownership and approved city/commodity wording remain to bind. '
    'Do not name the speakers from an older English draft,assign a royal or military rank,or infer marriage,kinship,employment or a formal servant relationship. '
    'The feminine/assertive register and elaborate laugh characterize the first speaker without proving noble status. The second speaker moves '
    'from polite uncertainty to casual acquiescence;do not flatten every reply into the same formal yes.\n\n'
    'Here いける concerns the taste catching on/succeeding as a fashion,not being physically edible,safe to eat,or already sold profitably. '
    'The purchase order is as many as can be bought,not an invented quantity,price,available capital,ship-hold capacity or cargo transaction '
    'already completed. Keep the first speaker\'s certainty as her own boast and the FE notice\'s しそう as prospective likelihood, '
    'not a narrator-confirmed existing boom or observed earned state. The notice names セビリア only at the close;do not insert it into earlier '
    'speeches or assign the conversation an unproven location. Preserve bananas as the concrete subject and the humor of an age-of-bananas '
    'proclamation without adding sexual innuendo or a new joke.\n\n'
    'The clean source has nine progressive speeches with static selectorsAE/AF and one genuine FE impersonal notice. There are no FI/FA/FO '
    'tokens,typed choices,relative sites,predicates or2000 pauses. Its complete13-command stream begins with opaque A000 at8 raw00a0ffff010a0da1 '
    'and ends with C200 at384 and a four-byte endword at386,logical end390/stored392. Preserve the effect and every complete preamble. '
    'Do not interpret packed A000 operands or turn source prose into a claim that its action/event has been naturally selected. '
    'No current English is read by this producer and no source/prose or completion credit is added.'
)
MEANINGS={
    6:'SourceAE emphatically repeats bananas and declares that the coming era belongs to them. Preserve the enthusiastic,grand future-fashion prediction without adding a location,quantity,profit or established boom.',
    9:'SourceAF repeats bananas as a politely doubtful question. Keep the brief skeptical echo and its contrast with AE\'s certainty;do not invent refusal or a rank/address.',
    13:'AE affirms the choice and insists that this taste will certainly succeed/catch on. Preserve the taste as her reason and her personal confidence;いける is not a food-safety assessment or a completed sale.',
    17:'AF cautiously questions whether that is really so. Preserve the reserved doubt in そうですかね rather than treating it as enthusiastic agreement or a blunt insult.',
    21:'AE insists that it is so and that if she says it will succeed,it will. Preserve her imperious self-certainty as a speaker-owned boast,not a narrator guarantee or a verified market result.',
    24:'AF gives in/acknowledges and then asks what to do. Preserve the move from doubt to compliance and the practical question without inventing a formal boss or servant relationship.',
    27:'AE orders AF to go and buy as many bananas as possible. Preserve the concrete fruit and the maximal purchase instruction without adding a numeric quantity,price,hold capacity or completed purchase.',
    31:'AF gives a casual repeated acknowledgment,へいへい. Preserve the offhand or resigned compliance and its contrast with the earlier polite question;add no Captain,Mistress or relationship title.',
    35:'AE grandly repeats that the age of bananas is coming and gives an elaborate self-satisfied laugh. Preserve the comic confidence and distinctive vocal manner without declaring her royalty or inventing another punchline.',
    38:'The impersonal FE notice says bananas seem likely to become fashionable in セビリア. Preserve the explicit city,the commodity and prospective しそう likelihood rather than an already active boom,earned flag or completed event.',
}

if __name__=='__main__':
    assert not ROOT.exists()
    lead=deepcopy(next(b for b in read(INVENTORY)['blocks'] if b['block']==176))
    clean=Path('work/clean.nds');im=NdsImage.open(clean);block=IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[176]
    assert sha(clean.read_bytes())=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    assert sha(block)==lead['clean_block_sha256']=='04a6366f1e88a5d33d02031bbce7a7952ae789f47280f58fa9b53048d817dfe5'
    assert len(block)==392 and lead['speeches']==len(lead['records'])==10
    assert lead['source_selectors']==[174,175,254] and lead['source_macro_counts']=={'FI':0,'FA':0,'FO':0}
    assert lead['FE_panels']==1 and lead['relative_sites']==lead['typed_menu_2100_commands']==lead['typed_actor_style_4100_commands']==0
    commands=lead['complete_native_commands'];assert len(commands)==13
    assert [(c['offset'],c['whole_command_hex']) for c in commands if c['word']!=0x4000]==[(8,'00a0ffff010a0da1'),(384,'00c2'),(386,'00000000')]
    assert not any(c['word'] in [0x100,0x200,0x300,0x400,0x8000,0x8100,0x2000] for c in commands)
    for c in commands:at=c['offset'];assert block[at:at+c['native_extent']].hex()==c['whole_command_hex']
    assert {r['source_record_index'] for r in lead['records']}==set(MEANINGS)
    for r in lead['records']:
        at=r['source_reference']['offset'];raw=bytes.fromhex(r['source_hex'])
        assert block[at:at+len(raw)]==raw and block[at+len(raw)]==0 and block[at-5:at+1].hex()==r['source_complete_preamble_hex']
        assert raw[1:].decode('cp932')==r['source_Japanese']
        r.update(fresh_source_gloss=MEANINGS[r['source_record_index']],whole_exchange_context=CONTEXT,
            clean_source_complete_exchange_read_before_predecessor_English=True)
    ROOT.mkdir(parents=True);transcript=ROOT/'SC2_B176_complete_clean_exchange_and_glosses.txt';lines=[CONTEXT]
    for r in lead['records']:lines.extend(['\n'+r['id']+' selector'+format(r['source_selector'],'02X'),r['source_Japanese'],r['fresh_source_gloss']])
    transcript.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    save(ROOT/'all10_complete_B176_exchange_and_fresh_glosses.json',dict(format='dk4-editorial-clean-source-context-v1',source_ROM=str(clean),
        source_ROM_sha256=sha(clean.read_bytes()),source_SC2_sha256=sha(im.read_file('/data/SC2.DK4')),block=lead,total_editorial_objects=10,
        whole_exchange_context=CONTEXT,source_transcript=str(transcript),source_transcript_sha256=sha(transcript.read_bytes()),
        all10_clean_source_read_and_individually_glossed_before_predecessor_English=True,source_progressive_speeches=9,source_FE_speeches=1,
        source_relative_site_count=0,source_predicate_count=0,source_A000_count=1,source_C200_count=1,source_declared_end_offsets=[386],
        source_static_actor_selectors=[174,175],source_FE_notice_is_impersonal_prospective_city_commodity_fashion=True,
        AE_AF_names_voices_city_commodity_and_complete_native_controls_to_bind=True,
        current_names_voices_terms_entry_conditions_native_layout_actual_and_release_still_pending=True,no_predecessor_English_exposed=True,
        no_new_ROM_registry_ledger_orreview_credit=True,source_prose_or_completion_credit_added=0,new_emulator_runs=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [INVENTORY,transcript,Path(__file__)]}))
    print(dict(clean_objects=10,progressive=9,FE=1,commands=13,selectors=[174,175,254],FI=0,FA=0,FO=0,A000=1,C200=1,end=386,current_English_unexposed=True,credit=0))
