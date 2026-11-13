"""Source-led English review of24 independent Survey/Lookout battle comments."""
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.battle_bridge_editorial import current_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.prepare_work_comments_v842 import reference
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/battle_survey_lookout_v934')
ROM=Path('out/all_routes_combined_v928_candidate.nds')
MANUSCRIPT=Path('translations/battle_survey_lookout_editorial_manuscript_v1.json')
IDS=tuple(range(1709,1733))
DATA='''1709|Surveying on deck during battle requires courage.|Surveying on deck during a battle takes nerve...|Restore the explicit exposed deck location and battle context.
1710|A time like this especially calls for calmly determining the current position.|We need to stay calm and work out our position, especially at a time like this.|Restore the particular urgency and determining position rather than merely marking a known location.
1711|The speaker struggles to measure the position amid flying shots.|Our position? With all these shots flying, I can't take a reading...|Restore the interrupted difficulty;do not assert that shots damage or falsify readings.
1712|Taking measurements remains the speakers job even in this emergency.|Even in an emergency like this, taking measurements is my job...|Restore personal duty despite the emergency rather than an impersonal forecast.
1713|Roughly expresses disbelief at surveying during battle.|Surveying in the middle of a battle? Are you serious?!|Restore the rough incredulous spoken question.
1714|Surveying is constant even in battle;it is unglamorous but difficult work.|Surveying never stops, even in battle. It's unglamorous, but it's hard work.|Restore the continuing duty and unglamorous versus demanding observation without inventing gratitude or boredom.
1715|Would rather fight on deck than take measurements.|I'd rather be fighting on deck than taking measurements!|Restore the personal wish and deck location.
1716|Surveying at a time like this is no joke.|Surveying now... This is no joke.|Retain the natural contextual complaint and idiomatic no-joke wording.
1717|Rafael says a time like this particularly requires calm measurement.|This is when I need to stay calm and take my measurements.|Restore personal self-reminder and taking readings rather than an abstract instruction.
1718|Hodram says taking measurements like this is also important even though he is not fighting.|Even if I'm not fighting, taking these measurements matters, too...|Preserve the value of this work alongside fighting;do not falsely claim fighting is unimportant.
1719|Lil complains that the admiral is surveying during battle.|Why is the admiral stuck surveying in the middle of a battle?!|Retain her self-directed admiral complaint and explicit combat setting;stuck conveys frustration without inventing forced reassignment.
1720|Maria marvels at calmly taking measurements at such a time,with the person unstated.|Taking measurements so calmly, even at a time like this...|Preserve the trailing amazed observation. Japanese leaves the agent unstated;do not invent a you-versus-I relationship or a claim about anothers ability.
1721|Reports sighting an enemy ship and currently identifying its type.|Enemy ship sighted. I'm checking its type now.|Restore the personal current identification task and ship reference.
1722|Politely proposes trying to snipe the enemy admiral during hand-to-hand combat.|Let's try to snipe their admiral during the boarding action.|Restore the attempted targeted shot and naval melee timing. Established Lookout help124 explains sniping;no successful capture is promised.
1723|A successful sniping shot could reverse the battle in an instant.|A successful shot could turn the whole battle around!|Preserve success as a condition and the dramatic turnaround;no automatic victory is asserted.
1724|The speaker screams because shots are coming toward them.|Aah! Cannonballs are coming this way!|Restore panic and incoming movement rather than generic flying shots.
1725|Warns of incoming enemy cannon fire and relies on the helmsman.|Incoming cannon fire! Helmsman, I'm counting on you!|Restore reliance on the helmsman rather than an order to take command.
1726|The elderly speaker is impressed by the powerful spectacle.|What an impressive sight!|Retain the natural exclamation and source awe without inventing family address.
1727|The speaker cries out that shots keep flying toward them.|Whoa! The shots keep coming!|Retain the natural alarm and repeated incoming shots.
1728|Looks around to see whether any reinforcements might come.|I'm keeping an eye out for any reinforcements.|Restore personal watchfulness and uncertain possible arrival;no reinforcements are guaranteed.
1729|Rafael warns that the enemy is coming and asks whether everyone is ready.|The enemy's coming! Is everyone ready?|Restore complete natural warning and readiness question.
1730|Hodram warns of incoming enemy shots and orders the helmsman to follow his directions.|Incoming enemy fire! Helmsman, follow my orders!|Restore the explicitly personal my directions rather than unspecified orders.
1731|Lil says it is no time to enjoy the view.|This is no time to admire the view.|Retain the natural situational remark.
1732|Maria demands a gun and intends to aim at the enemy admiral.|Give me a gun! I'll take aim at their admiral!|Restore the direct demand and aiming intention without claiming the enemy admiral is already captured or defeated.'''
PROSE={}
for line in DATA.splitlines():
    n,meaning,english,note=line.split('|');n=int(n)
    PROSE[n]=(meaning,english,note,'retain' if n in (1716,1726,1727,1731) else 'revise')

def main():
    assert not MANUSCRIPT.exists();ROOT.mkdir(parents=True,exist_ok=True)
    packet_path=Path('work/analysis/battle_survey_lookout_v933/source_context_packet.json');packet=read(packet_path)
    ledger=read('translations/editorial_review_current_v1.json')
    assert ledger['records_editorially_completed']==994 and ledger['records_with_source_and_prose_pass']==997
    assert sha(ROM.read_bytes())==packet['candidate_sha256']==ledger['current_integrated_candidate']['sha256']
    assert len(packet['all150_original_battle_helper_main_and_ordinary_control_selections'])==150
    current,clean=map(NdsImage.open,(ROM,'work/clean.nds'))
    jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/__arm9__.bin'))
    en=current_entries(current.read_file('/COMMON/MESFILE.DK4'),current.read_file('/__arm9__.bin'))
    ordinary=[{'message_id':n,'source_Japanese':jp[n].text.decode('cp932'),'source_hex':jp[n].text.hex(),'source_reference':reference(jp[n]),'current_English':en[n].text.decode('cp932'),'current_text_hex':en[n].text.hex(),'current_reference':reference(en[n]),'already_reviewed_ordinary_context_no_new_credit':True} for n in range(1499,1523)]
    supplement=ROOT/'ordinary_context_and_terms.json'
    save(supplement,{'candidate_sha256':sha(ROM.read_bytes()),'source_clean_ROM_sha256':packet['source_clean_ROM_sha256'],'records':ordinary,
        'independent_alternatives_not_consecutive_dialogue':True,'established_term_documents':{p:sha(Path(p).read_bytes()) for p in ('translations/crew_help_manuscript_v1.json','translations/skill_terms_help_manuscript_v1.json','translations/character_name_localization_policy_v1.json')},
        'established_roles':{'Survey':3,'Lookout':1},'sniping_context_help124':'Lookout help states that a Lookout with high Aim may snipe an enemy admiral in battle;success allows capturing that ship. Dialogue1722 proposes trying;it does not claim success.',
        'source1720_agent_unstated_preserved':True,'source1718_measurement_also_matters_not_fighting_is_unimportant':True,'source1725_helmsman_relied_upon_not_promoted_to_command':True})
    sources={r['message_id']:r for r in packet['records_with_immediate_storage_neighbors']};rows=[]
    for n,(meaning,english,note,decision) in PROSE.items():
        s=sources[n];role,first=(3,1709) if n<1721 else (1,1721);index=n-first;hero=index-8 if index>=8 else None;voice=index if hero is None else None
        speaker=f'Native NPC voice class{voice}' if hero is None else ['Rafael','Hodram Joakim Bergstrom (genuine captain1)','Lil','Maria'][hero]
        assert english==' '.join(english.split()) and english.isascii() and not any(c in english for c in '%{}\n')
        if decision=='retain':assert english==s['current_English'].strip()
        rows.append({'id':f'COMMON_MESSAGE_{n}','message_id':n,'role_ID':role,'voice_class':voice,'protagonist_ID':hero,'speaker':speaker,
            'context':f'Independent activity0 battle working comment for Survey3 or Lookout1,selected role{role}. Original12600 selects eight NPC alternatives and12720 selects the four genuine protagonists. Main12104 uses original battle fields8/12=0/1. Storage neighbors are independently selected variants,not consecutive dialogue or the separate activity1 helper126A8. Flavor lines do not execute measurements,sniping,capture or helm orders.',
            'source_Japanese':s['source_Japanese'],'source_hex':s['source_hex'],'source_reference':s['source_reference'],'canonical_source_hex':s['canonical_text_hex'],'current_reference':s['current_reference'],'current_text_hex':s['current_text_hex'],'current_English':s['current_English'],
            'source_meaning':meaning,'english':english,'localization_note':note,'editorial_decision':decision,'native_argument_count':0,'review':{'source':True,'context':True,'localization':True,'naturalness':True,'formatting':False}})
    assert tuple(r['message_id'] for r in rows)==IDS and sum(r['editorial_decision']=='revise' for r in rows)==20
    save(MANUSCRIPT,{'format':'dk4-natural-dialogue-source-manuscript-v2','translation_policy':'natural-dialogue-v2','target_locale':'en-US','encoder':'dialogue-relocatable-v1','consumer_layout_profile':'deck-battle-survey-lookout-visible-v1','review_gates':['source','context','localization','naturalness'],'formatting_review_pending':True,'status':'24-source-prose-reviewed-native-format-integration-and-actual-pending','file_path':'/COMMON/MESFILE.DK4','source_clean_ROM_sha256':packet['source_clean_ROM_sha256'],'current_ROM':str(ROM),'current_ROM_sha256':sha(ROM.read_bytes()),'current_COMMON_sha256':packet['COMMON_sha256'],'current_ARM9_sha256':packet['ARM9_sha256'],'native_context_proof':str(packet_path),'native_context_proof_sha256':sha(packet_path.read_bytes()),'ordinary_context_supplement':str(supplement),'ordinary_context_supplement_sha256':sha(supplement.read_bytes()),'records':rows,'full_goal_complete':False})
    save(ROOT/'editorial_ledger_before_source_review.json',ledger)
    ledger['records_with_source_and_prose_pass']=ledger['records_with_source_prose_drafts']=1021
    ledger['source_prose_reviewed_counts_by_file']['/COMMON/MESFILE.DK4']=1020
    ledger['reviewed_but_incomplete_COMMON_IDs']=[750,751,752,*IDS]
    ledger['active_source_prose_drafts']={'native_message_IDs':[750,751,752,*IDS],'manuscripts':['work/analysis/market_contract_v758/unmapped_750_752_prose_DRAFT.json',str(MANUSCRIPT)],'status':'three-older-context-unmapped-and24-battle-survey-lookout-source-prose-reviewed-format-release-pending','note':'These27 pending reviewed entries are not the full remaining shared/routes/player prose or raw-source scope.'}
    checkpoint='V934 source/prose-reviews24 battle Survey3/Lookout1 comments1709-1732:20 revisions and4 retentions. All150 original battle/main/ordinary controls pass. Drafts restore deck exposure,calm position finding,personal measurement duties,unglamorous work,measurement also mattering during combat,subject-neutral Maria observation,attempted boarding-action sniping,conditional turnaround,incoming shots,reliance on the helmsman,watch for possible reinforcements,and personal orders. Native layout,registered integration and actual scenes remain pending. V928 stays current;994 complete,1021 source/prose reviewed. Remaining shared/routes/player prose/raw inventory,older750-752,mood1833,special1885-1888,abandon-caption0x134E54,separate graphics/all18 plaques,Samwell header and later older-record re-audit remain open;full goal active.'
    ledger['latest_checkpoint']=checkpoint
    ledger['battle_survey_lookout_v934']={'status':'source-prose-reviewed-native-release-and-actual-pending','native_message_IDs':list(IDS),'manuscript':str(MANUSCRIPT),'source_context_proof':str(packet_path),'proposed_revisions':20,'justified_retentions':4,'completed_entries_added':0}
    ledger['research_checkpoints'].append({'id':'V934-Battle-Survey-Lookout24-source-prose','proof':str(packet_path),'manuscript':str(MANUSCRIPT),'new_source_prose_reviews':24,'completed_entries_added':0,'previous_goal_turn_classification':'progress:28 Bridge entries completed in V928,exact patch,four actual cases and next24 source contexts verified','this_goal_turn_classification':'progress:24 faithful glosses,natural English decisions,exact references and ordinary-context supplement','full_goal_complete':False})
    assert sum(ledger['source_prose_reviewed_counts_by_file'].values())==1021
    save('translations/editorial_review_current_v1.json',ledger)
    doc=Path('docs/battle_survey_lookout_v934_source_review.md')
    with doc.open('x',encoding='utf-8') as f:f.write('# V934: battle Survey/Lookout source review\n\n'+checkpoint+'\n')
    for d in map(Path,('docs/translation_progress.md','docs/editorial_review_goal.md','docs/todo.md','docs/known_issues.md')):
        with d.open('a',encoding='utf-8') as f:f.write('\n\n## V934: battle Survey/Lookout source review\n\n'+checkpoint+' See [V934 source review](battle_survey_lookout_v934_source_review.md).\n')
    archive=Path('E:/Rota Nova translations/Editorial review/V934 Battle Survey Lookout source review');assert not archive.exists();copied=[]
    for source in (MANUSCRIPT,packet_path,supplement,Path(__file__),doc,Path('translations/editorial_review_current_v1.json')):
        target=archive/source.absolute().relative_to(Path.cwd());target.parent.mkdir(parents=True,exist_ok=True);copy2(source,target);assert sha(source.read_bytes())==sha(target.read_bytes());copied.append({'source':str(source),'archive':str(target),'sha256':sha(target.read_bytes())})
    save(ROOT/'archive_manifest.json',{'files':copied,'all_hashes_verified':True,'completed_entries_added':0})
    print('24 source/prose reviews:20 revisions,4 retentions.994 complete,1021 source/prose;native/release/actual pending.',flush=True)
if __name__=='__main__':main()
