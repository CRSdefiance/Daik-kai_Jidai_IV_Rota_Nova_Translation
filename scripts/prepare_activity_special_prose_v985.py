"""Review17 independent activity,Chapel-refusal and special-character comments."""
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.mood_comments_editorial_v981b import current_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/activity_special_v985')
ROM=Path('out/all_routes_combined_v981_candidate.nds')
MANUSCRIPT=Path('translations/activity_special_editorial_manuscript_v1.json')
IDS=tuple(range(1872,1889))
RETAINED={1872,1883,1886}
DATA='''1872|Angelo cajoles the listener not to be so angry and repeats a soft appeal.|Hey, don't get so angry. Come on.|Retain the natural informal calming appeal. Come on conveys the repeated na without inventing a relationship or apology absent from this line.
1873|Emilio says he got hungry,then promises not to do it again.|I got hungry... I won't do it again.|Restore the personal subject and explicit future promise. Never again by itself loses the clear promise and can sound like a refusal to repeat a bad experience.
1874|Samwell placates the listener and says it was a change of pace.|Now, now... It was just a change of pace.|Preserve the placating delivery and intended refreshment excuse. A change of pace is faithful to kibun tenkan without inventing a particular leisure activity.
1875|Jam says Sorry in English,then warns that getting angry is bad for the listener's health.|Sorry! Getting angry is bad for your health.|Restore health explicitly. Keep the breezy apology and deflection without caricaturing the source English word or importing a medical diagnosis.
1876|Fernando says work should not be rushed and should be done slowly,taking his time.|Now, now, there's no rush. Let's take our time with the work...|Restore the omitted leisurely approach to work as a natural deflection. Do not turn it into a specific work order or a measured productivity rule.
1877|Julio says he only had one drink to lift his spirits.|It was just one drink to lift my spirits.|Preserve the single-drink minimization and mood-lifting purpose. The source does not specifically say courage,rum or intoxication;do not add those.
1878|Al refuses Chapel assignment because it concerns his pride as an Arab,and asks to be excused.|It's a matter of pride for me as an Arab. Please excuse me.|Restore a complete natural request after the personal Arab-pride explanation. Do not generalize Arab identity into a universal religious rule or invent a named faith.
1879|Yifa says she cannot take the assignment because she is currently training in Taoist arts.|I can't do that. I'm training in Taoist arts.|Restore the personal ongoing training and refusal. The Japanese does not state that Taoist training categorically forbids Chapel duty;remove that invented doctrinal claim.
1880|Yukihisa formally explains that he is not a Christian and asks to be pardoned.|I am not a Christian. Please pardon me...|Restore complete polite sentences and deliberate formality from sessha and gozaran rather than subjectless telegraphic English. No conversion or universal employment rule is added.
1881|Yifa uses any free moment for repeated training,with two exertion cries.|Whenever I have a free moment, I train! Hah! Hyah!|Restore the personal habitual training and both exertion sounds as idiomatic English. Training is her current activity,not a completed task or a demand that someone else train.
1882|Julian suddenly thinks of a good romantic pickup line.|Oh! I just thought of a great pickup line!|Restore the act of thinking of the line now. Great reflects the favorable source ii without the old stronger perfect claim or an invented listener.
1883|Aziza defiantly says men will not beat her,with a short emphatic pause.|Men won't beat me!|Retain the natural confident challenge. The brief Japanese pause does not require an artificial English break or hesitation;do not turn the statement into an objective stat comparison.
1884|Aziza tells the addressed companion not to get into mischief and to come to her.|Don't get into mischief. Come here.|Restore the gentle complete admonition and invitation. Do not identify the addressee as a child,son,daughter or relative from an uninterpreted source state bit.
1885|Yifa eagerly says it is time to test the results of her training.|Time to put my training to the test!|Use the natural English idiom for applying her training in a real fight. Preserve readiness without inventing a victory or declaring the training complete.
1886|Julian remarks on the realism,then is startled that this is a real war.|So realistic... Wait, a real war?!|Retain the fluent comic realization and alarm. The elliptical exclamation is natural spoken English,with no invented simulation or claim that war is merely a performance.
1887|Aziza asks where the enemy is and demands to be allowed to fight.|Where's the enemy? Let me fight!|Restore the omitted request for permission to fight. My turn in the old English invents a turn-taking context and weakens her demand.
1888|Aziza reacts to an enemy and tells the addressed companion to stay hidden.|An enemy?! You stay hidden!|Restore the explicit you-focused instruction as natural urgent speech. Do not invent the companion's identity,gender,kinship or the source state bit's narrative meaning.'''
PROSE={}
for line in DATA.splitlines():
    n,meaning,english,note=line.split('|');n=int(n)
    PROSE[n]=(meaning,english,note,'retain' if n in RETAINED else 'revise')

def main():
    assert not MANUSCRIPT.exists() and not ROOT.exists();ROOT.mkdir(parents=True)
    context_path=Path('work/analysis/activity_special_v984/source_context_packet.json');packet=read(context_path)
    ledger_path=Path('translations/editorial_review_current_v1.json');ledger=read(ledger_path)
    assert ledger['records_editorially_completed']==1157 and ledger['records_with_source_and_prose_pass']==1160
    assert sha(ROM.read_bytes())==packet['candidate_sha256']==ledger['current_integrated_candidate']['sha256']
    assert len(packet['all52_activity2_direct_and_main_priority_cases'])==52
    assert len(packet['all16_special_ordinary_battle_direct_and_main_bit2_controls'])==16
    assert len(packet['all12_original_actor_role_legality_controls'])==12
    assert len(packet['all3_original_Chapel_assignment_refusal_owner_and_speaker_calls'])==3
    rom,clean=map(NdsImage.open,(ROM,'work/clean.nds'))
    jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/__arm9__.bin'))
    en=current_entries(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'))
    source={r['message_id']:r for r in packet['records_and_immediate_neighbors']};rows=[]
    for n,(meaning,english,note,decision) in PROSE.items():
        s=source[n];assert jp[n].text.hex()==s['source_hex'] and en[n].text.hex()==s['current_text_hex']
        assert english.isascii() and english==' '.join(english.split()) and not any(c in english for c in '%{}\n')
        assert b'IC' not in jp[n].text and b'%' not in jp[n].text
        if decision=='retain':assert english==s['current_English'].strip()
        context=(
            'Independent actor-specific activity2 response after the original personnel event. Helper122A4 selects this line before physical,mood and job getters. Original13C94 sets activity1 during139EC and activity2 afterward;this is not evidence of a new Scold menu command. '
            if n<1878 else
            'Original CDeckPersonnelView assignment refusal for destination role18 Chapel. Original15DE4 rejects this actor;13450 calls actor-bearing dispatcher53FE4 with the actor object and this numeric ID,and makes no assignment. This is a modal speech consumer distinct from the embedded Deck comment body. '
            if n<1881 else
            'Independent ordinary personal comment for special actor25/26/27. Original12838 and main12104 activity1 in ordinary mode select this line. Actor27 has two original shared-object byte0x11 bit2 outcomes;the state meaning is not inferred. '
            if n<1885 else
            'Independent battle personal comment for special actor25/26/27. Original126A8 and main12104 activity1 with original mode0/1 select this line. Actor27 has two original shared-object byte0x11 bit2 outcomes;the state meaning is not inferred. ')
        context+='Storage neighbors are independent alternatives rather than consecutive dialogue. Native speaker names come from original virtual getters. No character identity,unlock,recruitment,earned role,measured stat effect or story relationship is invented.'
        rows.append({'id':f'COMMON_MESSAGE_{n}','message_id':n,'actor_ID':s['actor_ID'],'speaker':s['speaker'],
            'consumer':s['consumer'],'source_family':s['source_family'],'activity_state':2 if n<1878 else None if n<1881 else 1,
            'original_mode_fields8_12':([0,1] if n>=1885 else [0,0]) if n>=1881 else None,
            'context':context,'source_Japanese':s['source_Japanese'],'source_hex':s['source_hex'],'source_reference':s['source_reference'],
            'canonical_source_hex':s['canonical_text_hex'],'current_reference':s['current_reference'],'current_text_hex':s['current_text_hex'],
            'current_English':s['current_English'],'source_meaning':meaning,'english':english,'localization_note':note,
            'editorial_decision':decision,'native_argument_count':0,'source_native_macros':[],
            'review':{'source':True,'context':True,'localization':True,'naturalness':True,'formatting':False}})
    assert tuple(r['message_id'] for r in rows)==IDS and sum(r['editorial_decision']=='revise' for r in rows)==14
    policy=Path('translations/character_name_localization_policy_v1.json');supplement=ROOT/'source_context_and_faithfulness_review.json'
    save(supplement,{'candidate_sha256':sha(ROM.read_bytes()),'established_term_documents':{str(policy):sha(policy.read_bytes())},
        'all17_independent_source_alternatives_not_consecutive_dialogue':True,'all17_source_IC_and_printf_counts_zero':True,
        'native_speakers_from_original_getters':packet['original_actor_name_getters'],
        'Chapel18_refusal_actor_mapping':{'1878':17,'1879':25,'1880':12},
        'Yifa1879_personal_training_not_universal_Taoist_ban':True,'Al1878_Arab_pride_without_invented_religion':True,
        'Yukihisa1880_explicit_Christian_refusal_with_formal_voice':True,
        'Julio1877_mood_lifting_single_drink_not_invented_courage_rum_or_intoxication':True,
        'Aziza1884_1888_addressee_identity_gender_kinship_and_bit2_meaning_not_invented':True,
        'Julian1882_newly_conceived_pickup_line_and1886_comic_real_war_retained':True,
        'activity2_after_original_event_no_invented_Scold_button':True,
        'mixed_modal_and_embedded_native_consumers_need_separate_layout_proofs':True,
        'neighbors1871_and1889_no_new_review_credit':True})
    save(MANUSCRIPT,{'format':'dk4-natural-dialogue-source-manuscript-v2','translation_policy':'natural-dialogue-v2','target_locale':'en-US',
        'encoder':'dialogue-relocatable-v1','consumer_layout_profile':'activity-special-mixed-consumers-v1',
        'review_gates':['source','context','localization','naturalness'],'formatting_review_pending':True,
        'status':'17-source-prose-reviewed-two-native-consumers-font-release-actual-pending','file_path':'/COMMON/MESFILE.DK4',
        'source_clean_ROM_sha256':packet['source_clean_ROM_sha256'],'current_ROM':str(ROM),'current_ROM_sha256':sha(ROM.read_bytes()),
        'current_COMMON_sha256':packet['COMMON_sha256'],'current_ARM9_sha256':packet['ARM9_sha256'],
        'native_context_proof':str(context_path),'native_context_proof_sha256':sha(context_path.read_bytes()),
        'source_context_supplement':str(supplement),'source_context_supplement_sha256':sha(supplement.read_bytes()),'records':rows,'full_goal_complete':False})
    save(ROOT/'editorial_ledger_before_source_review.json',ledger)
    ledger['records_with_source_and_prose_pass']=ledger['records_with_source_prose_drafts']=1177
    ledger['source_prose_reviewed_counts_by_file']['/COMMON/MESFILE.DK4']=1176
    ledger['reviewed_but_incomplete_COMMON_IDs']=[750,751,752,*IDS]
    ledger['active_source_prose_drafts']={'native_message_IDs':[750,751,752,*IDS],
        'manuscripts':['work/analysis/market_contract_v758/unmapped_750_752_prose_DRAFT.json',str(MANUSCRIPT)],
        'status':'three-older-context-unmapped-and17-source-prose-reviewed-native-release-actual-pending',
        'note':'These20 pending reviewed entries are not the full remaining shared/routes/player prose or raw-source scope.'}
    checkpoint='V985 source/prose-reviews17 activity,Chapel-refusal and special-character comments1872-1888:14 revisions and3 retentions.52 original activity2,16 special ordinary/battle,12 role-legality and3 full Chapel refusal controls pass. Drafts restore the hunger promise,change of pace,health warning,leisurely work,single mood-lifting drink,personal Arab pride,Taoist training,formal Christian refusal,training cries,new pickup line,training test and demand to fight. No invented doctrinal ban,rum,kinship or source-bit story meaning. Modal1878-1880 and embedded other14 require distinct native layout proofs. Native fonts,registered integration and representative actual scenes remain pending. V981 stays current;1157 complete,1177 source/prose reviewed. Older750-752,remaining shared/routes/player prose/raw inventory,separate graphics/all18 plaques,Samwell header and later older-record re-audit remain open;full goal active.'
    ledger['latest_checkpoint']=checkpoint
    ledger['activity_special_v985']={'status':'17-source-prose-reviewed-native-release-actual-pending','native_message_IDs':list(IDS),
        'manuscript':str(MANUSCRIPT),'source_context_proof':str(context_path),'proposed_revisions':14,'justified_retentions':3,'completed_entries_added':0}
    ledger['research_checkpoints'].append({'id':'V985-activity-special17-source-prose','proof':str(context_path),'manuscript':str(MANUSCRIPT),
        'new_source_prose_reviews':17,'completed_entries_added':0,
        'previous_goal_turn_classification':'progress:39 mood entries completed in registered V981 with exact patch,six actual samples and68 next-family selection controls',
        'this_goal_turn_classification':'progress:17 source contexts and English reviews,exact native names,role legality and original Chapel refusal dispatch mapped',
        'full_goal_complete':False})
    previous=read(ROOT/'editorial_ledger_before_source_review.json')
    assert ledger['records_editorially_completed']==1157 and sum(ledger['source_prose_reviewed_counts_by_file'].values())==1177
    for key in ('current_integrated_candidate','unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','raw_source_coverage_revisit','approved_name_roles'):
        assert ledger[key]==previous[key]
    save(ledger_path,ledger)
    doc=Path('docs/activity_special_v985_source_review.md');assert not doc.exists()
    with doc.open('x',encoding='utf-8') as f:
        f.write('# V985: activity,Chapel refusal and special-character English review\n\n'+checkpoint+'\n\n')
        for row in rows:f.write(f"## COMMON {row['message_id']}: {row['speaker']}\n\n"+row['source_Japanese'].replace('\n',' ')+'\n\n'+row['source_meaning']+'\n\n'+row['english']+'\n\n'+row['localization_note']+'\n\n')
    for p in map(Path,('docs/translation_progress.md','docs/editorial_review_goal.md','docs/todo.md','docs/known_issues.md')):
        with p.open('a',encoding='utf-8') as f:f.write('\n\n## V985: activity and special-character source review\n\n'+checkpoint+' See [V985 source review](activity_special_v985_source_review.md).\n')
    archive=Path('E:/Rota Nova translations/Editorial review/V985 Activity special source review');assert not archive.exists();copied=[]
    for source in (MANUSCRIPT,context_path,supplement,Path(__file__),doc,ledger_path):
        target=archive/source.absolute().relative_to(Path.cwd());target.parent.mkdir(parents=True,exist_ok=True);copy2(source,target)
        assert source.read_bytes()==target.read_bytes();copied.append({'source':str(source),'archive':str(target),'sha256':sha(target.read_bytes())})
    save(ROOT/'archive_manifest.json',{'files':copied,'all_hashes_verified':True,'completed_entries_added':0})
    print('17 source/prose reviews:14 revisions,3 retentions.1157 complete,1177 source/prose;separate native-consumer proofs,release and actual samples pending.')

if __name__=='__main__':main()
