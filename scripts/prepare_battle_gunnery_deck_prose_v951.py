"""Source-led English review of24 independent Gunnery/DeckCleaning battle comments."""
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.battle_sails_boarding_editorial import current_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.prepare_work_comments_v842 import reference
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/battle_gunnery_deck_v951')
ROM=Path('out/all_routes_combined_v947_candidate.nds')
MANUSCRIPT=Path('translations/battle_gunnery_deck_editorial_manuscript_v1.json')
IDS=tuple(range(1757,1781))
DATA='''1757|Orders careful aiming and firing.|Aim well and fire!|Retain the natural direct gunnery order.
1758|Reports target acquisition and warns not to miss.|Target acquired. Don't miss...|Restore target acquisition and the negative warning rather than a generic aim order.
1759|Says higher Aim allows more shots to be fired.|Better Aim lets you fire more shots.|Use the established Aim skill and preserve source more firing,not the old more hits substitution. Help129 separately says Gunners allow more shots;help173 discusses accuracy. This dialogue is not an independent measurement of the engine formula.
1760|Remarks that landing a hit is difficult.|It's not easy to land a hit, is it?|Restore a natural reflective spoken sentence rather than telegraphic wording.
1761|Roughly urges repeated firing because enough shots will land a hit.|Keep firing! One of them will hit!|Retain the natural volume-of-fire boast as character speech,not a measured hit-probability guarantee.
1762|Warns against hitting allies even by mistake.|Whatever happens, don't hit allies!|Retain the natural emphatic friendly-fire warning.
1763|Promises personally to demonstrate sinking the enemy flagship.|I'll show you I can sink their flagship!|Restore the personal boast and flagship target;do not turn it into a passive guaranteed outcome.
1764|Reflects that additional gun batteries would be effective.|More gun batteries would help.|Retain the natural conditional assessment and source-bound Gun Batteries term from help129.
1765|Rafael warns that the cannons cannot fire if they get too close.|If we get too close, the cannons won't be able to fire.|Restore the conditional crew perspective and these cannons rather than a detached generic statement about all guns.
1766|Hodram orders the gunners not to waste shots and to aim carefully.|Don't waste ammunition! Take careful aim!|Restore the firm negative order and careful aiming;the old save shots phrasing is unnatural.
1767|Lil reacts to a near miss and says just a little more is needed.|So close... Just a bit more...|Retain the natural disappointed near-hit reaction.
1768|Maria orders the next shot loaded and says they will fire again immediately.|Load the next shot! We'll fire again right away!|Restore the loading order and imminent firing intention;the ammunition is not reported already ready.
1769|Having deck personnel gives an advantage in hand-to-hand combat.|Having deckhands gives us an edge in boarding battles.|Use established Deckhands from help126 and restore advantage in naval melee,not merely help while moving aboard.
1770|Politely asks for orders if hand-to-hand combat begins.|If it comes to hand-to-hand combat, just give me the word.|Restore the conditional deferential offer;do not issue an unconditional order to start boarding.
1771|Is already cleaning because there is nothing else to do.|I've got nothing else to do, so I'm cleaning...|Restore personal ongoing action rather than proposing that everyone start cleaning.
1772|Ironically observes how leisurely cleaning at such a time is.|Cleaning at a time like this... Talk about taking it easy.|Localize the irony naturally without inventing who is being observed or a personal accusation.
1773|Casually suggests cleaning until hand-to-hand combat begins.|Might as well clean until the boarding starts!|Restore the casual suggestion and waiting period;not a formal order to the whole crew.
1774|The veteran says it is time to use strength built up by scrubbing the deck.|Time to use the strength I've built up scrubbing the deck!|Restore the source of the developed strength and the present opportunity to use it.
1775|Promises personally to be first into the boarding fight.|I'll be first aboard!|Restore first-person oira and first arrival. First aboard naturally conveys the boarding context without an invented appointment as party commander.
1776|Reflects that battle dirties the ship and makes cleaning difficult.|Battle makes such a mess to clean...|Retain the natural weary observation and cleanup burden.
1777|Rafael offers to handle the boarding fight.|Leave the boarding fight to me.|Retain the natural personal offer in the naval melee context.
1778|Hodram leaves this battle to everyone else and considers doing deck cleaning.|I'll leave this battle to the others and do some deck cleaning...|Restore his personal intention and this battle;not a direct you-fight order or claim that the deck objectively needs cleaning.
1779|Lil leaves the naval battle to others,scrubs,and reacts in surprise.|I'll leave the sea battle to everyone else. Scrub, scrub... Huh?|Restore her personal deferral,the naval-battle scope,scrubbing sound and puzzled recognition.
1780|Maria wonders why she is polishing the deck of all things.|Why am I polishing the deck, of all things?|Restore the ongoing personal self-question and source of-all-things nuance;do not add a new reason.'''
PROSE={}
for line in DATA.splitlines():
    n,meaning,english,note=line.split('|');n=int(n)
    PROSE[n]=(meaning,english,note,'retain' if n in (1757,1761,1762,1764,1767,1776,1777) else 'revise')

def main():
    assert not MANUSCRIPT.exists();ROOT.mkdir(parents=True,exist_ok=True)
    packet_path=Path('work/analysis/battle_gunnery_deck_v950/source_context_packet.json');packet=read(packet_path)
    ledger=read('translations/editorial_review_current_v1.json')
    assert ledger['records_editorially_completed']==1042 and ledger['records_with_source_and_prose_pass']==1045
    assert sha(ROM.read_bytes())==packet['candidate_sha256']==ledger['current_integrated_candidate']['sha256']
    assert len(packet['all150_original_battle_helper_main_and_ordinary_control_selections'])==150
    current,clean=map(NdsImage.open,(ROM,'work/clean.nds'))
    jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/__arm9__.bin'))
    en=current_entries(current.read_file('/COMMON/MESFILE.DK4'),current.read_file('/__arm9__.bin'))
    ordinary=[{'message_id':n,'source_Japanese':jp[n].text.decode('cp932'),'source_hex':jp[n].text.hex(),'source_reference':reference(jp[n]),'current_English':en[n].text.decode('cp932'),'current_text_hex':en[n].text.hex(),'current_reference':reference(en[n]),'already_reviewed_ordinary_context_no_new_credit':True} for n in range(1547,1571)]
    supplement=ROOT/'ordinary_context_and_terms.json'
    save(supplement,{'candidate_sha256':sha(ROM.read_bytes()),'source_clean_ROM_sha256':packet['source_clean_ROM_sha256'],'records':ordinary,
        'independent_alternatives_not_consecutive_dialogue':True,'established_term_documents':{p:sha(Path(p).read_bytes()) for p in ('translations/crew_help_manuscript_v1.json','translations/skill_terms_help_manuscript_v1.json','translations/character_name_localization_policy_v1.json')},
        'established_roles':{'Gunnery':8,'DeckCleaning':2},
        'Aim_and_Gun_Batteries_terms_source_bound':True,
        'source1759_says_more_firing_not_independently_measured_shot_formula':True,
        'source1768_loading_order_not_already_loaded_state':True,
        'source1770_conditional_deference_not_boarding_order':True,
        'no_IC_native_macro_in_selected_Japanese':all(b'IC' not in jp[n].text for n in IDS),
        'reference_help':[ {k:r[k] for k in ('topic_id','heading','source_Japanese_with_link_IDs','english','clean_source_hex','source_meaning')} for file in ('translations/crew_help_manuscript_v1.json','translations/skill_terms_help_manuscript_v1.json') for r in read(file)['records'] if r.get('topic_id') in (126,129,173)]})
    sources={r['message_id']:r for r in packet['records_with_immediate_storage_neighbors']};rows=[]
    for n,(meaning,english,note,decision) in PROSE.items():
        s=sources[n];role,first=(8,1757) if n<1769 else (2,1769);index=n-first;hero=index-8 if index>=8 else None;voice=index if hero is None else None
        speaker=f'Native NPC voice class{voice}' if hero is None else ['Rafael','Hodram Joakim Bergstrom (genuine captain1)','Lil','Maria'][hero]
        assert english==' '.join(english.split()) and english.isascii() and not any(c in english for c in '%{}\n')
        if decision=='retain':assert english==s['current_English'].strip()
        rows.append({'id':f'COMMON_MESSAGE_{n}','message_id':n,'role_ID':role,'voice_class':voice,'protagonist_ID':hero,'speaker':speaker,
            'context':f'Independent activity0 battle working comment for Gunnery8 or DeckCleaning2,selected role{role}. Original12600 selects eight NPC alternatives and12720 selects the four genuine protagonists. Main12104 uses original battle fields8/12=0/1. Storage neighbors are independently selected variants,not consecutive dialogue or the separate activity1 helper126A8. Flavor lines do not execute firing or boarding,guarantee hits or victory,or assign the others to fight.',
            'source_Japanese':s['source_Japanese'],'source_hex':s['source_hex'],'source_reference':s['source_reference'],'canonical_source_hex':s['canonical_text_hex'],'current_reference':s['current_reference'],'current_text_hex':s['current_text_hex'],'current_English':s['current_English'],
            'source_meaning':meaning,'english':english,'localization_note':note,'editorial_decision':decision,'native_argument_count':0,'source_native_macros':[],'review':{'source':True,'context':True,'localization':True,'naturalness':True,'formatting':False}})
    assert tuple(r['message_id'] for r in rows)==IDS and sum(r['editorial_decision']=='revise' for r in rows)==17
    save(MANUSCRIPT,{'format':'dk4-natural-dialogue-source-manuscript-v2','translation_policy':'natural-dialogue-v2','target_locale':'en-US','encoder':'dialogue-relocatable-v1','consumer_layout_profile':'deck-battle-gunnery-deck-visible-v1','review_gates':['source','context','localization','naturalness'],'formatting_review_pending':True,'status':'24-source-prose-reviewed-native-format-integration-and-actual-pending','file_path':'/COMMON/MESFILE.DK4','source_clean_ROM_sha256':packet['source_clean_ROM_sha256'],'current_ROM':str(ROM),'current_ROM_sha256':sha(ROM.read_bytes()),'current_COMMON_sha256':packet['COMMON_sha256'],'current_ARM9_sha256':packet['ARM9_sha256'],'native_context_proof':str(packet_path),'native_context_proof_sha256':sha(packet_path.read_bytes()),'ordinary_context_supplement':str(supplement),'ordinary_context_supplement_sha256':sha(supplement.read_bytes()),'records':rows,'full_goal_complete':False})
    save(ROOT/'editorial_ledger_before_source_review.json',ledger)
    ledger['records_with_source_and_prose_pass']=ledger['records_with_source_prose_drafts']=1069
    ledger['source_prose_reviewed_counts_by_file']['/COMMON/MESFILE.DK4']=1068
    ledger['reviewed_but_incomplete_COMMON_IDs']=[750,751,752,*IDS]
    ledger['active_source_prose_drafts']={'native_message_IDs':[750,751,752,*IDS],'manuscripts':['work/analysis/market_contract_v758/unmapped_750_752_prose_DRAFT.json',str(MANUSCRIPT)],'status':'three-older-context-unmapped-and24-battle-gunnery-deck-source-prose-reviewed-format-release-pending','note':'These27 pending reviewed entries are not the full remaining shared/routes/player prose or raw-source scope.'}
    checkpoint='V951 source/prose-reviews24 battle Gunnery8/DeckCleaning2 comments1757-1780:17 revisions and7 retentions. All150 original battle/main/ordinary controls pass. Source-bound help129/173 distinguishes Aim,more firing and accuracy without an unmeasured engine-formula claim. Drafts restore target acquisition,personal flagship promise,conditional close-range firing,the next-shot loading order,deckhand melee advantage,conditional deference,ongoing cleaning,irony,strength from scrubbing,first aboard and personal captain cleaning remarks. Native layout,registered integration and actual scenes remain pending. V947 stays current;1042 complete,1069 source/prose reviewed. Remaining shared/routes/player prose/raw inventory,older750-752,mood1833,special1885-1888,abandon-caption0x134E54,separate graphics/all18 plaques,Samwell header and later older-record re-audit remain open;full goal active.'
    ledger['latest_checkpoint']=checkpoint
    ledger['battle_gunnery_deck_v951']={'status':'source-prose-reviewed-native-release-and-actual-pending','native_message_IDs':list(IDS),'manuscript':str(MANUSCRIPT),'source_context_proof':str(packet_path),'proposed_revisions':17,'justified_retentions':7,'completed_entries_added':0}
    ledger['research_checkpoints'].append({'id':'V951-Battle-Gunnery-Deck24-source-prose','proof':str(packet_path),'manuscript':str(MANUSCRIPT),'new_source_prose_reviews':24,'completed_entries_added':0,'previous_goal_turn_classification':'progress:24 SailHandling/Boarding entries completed in V947;50 pronoun controls,four actual cases,exact patch and next24 source contexts verified','this_goal_turn_classification':'progress:24 faithful glosses,natural English decisions,source-bound Aim/Gun Batteries help,exact references and ordinary-context supplement','full_goal_complete':False})
    assert sum(ledger['source_prose_reviewed_counts_by_file'].values())==1069
    save('translations/editorial_review_current_v1.json',ledger)
    doc=Path('docs/battle_gunnery_deck_v951_source_review.md')
    with doc.open('x',encoding='utf-8') as f:f.write('# V951: battle Gunnery/DeckCleaning source review\n\n'+checkpoint+'\n')
    for d in map(Path,('docs/translation_progress.md','docs/editorial_review_goal.md','docs/todo.md','docs/known_issues.md')):
        with d.open('a',encoding='utf-8') as f:f.write('\n\n## V951: battle Gunnery/DeckCleaning source review\n\n'+checkpoint+' See [V951 source review](battle_gunnery_deck_v951_source_review.md).\n')
    archive=Path('E:/Rota Nova translations/Editorial review/V951 Battle Gunnery Deck source review');assert not archive.exists();copied=[]
    for source in (MANUSCRIPT,packet_path,supplement,Path(__file__),doc,Path('translations/editorial_review_current_v1.json')):
        target=archive/source.absolute().relative_to(Path.cwd());target.parent.mkdir(parents=True,exist_ok=True);copy2(source,target);assert sha(source.read_bytes())==sha(target.read_bytes());copied.append({'source':str(source),'archive':str(target),'sha256':sha(target.read_bytes())})
    save(ROOT/'archive_manifest.json',{'files':copied,'all_hashes_verified':True,'completed_entries_added':0})
    print('24 source/prose reviews:17 revisions,7 retentions.1042 complete,1069 source/prose;native/release/actual pending.',flush=True)
if __name__=='__main__':main()
