"""Source-led English review of26 independently selected illness and near-death comments."""
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.physical_wounds_editorial import current_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/illness_critical_v972')
ROM=Path('out/all_routes_combined_v969_candidate.nds')
MANUSCRIPT=Path('translations/illness_critical_editorial_manuscript_v1.json')
IDS=tuple(range(1807,1833))
DATA='''1807|Politely and tentatively concludes that the speaker has come down with some illness.|I seem to have come down with something.|Localize the tentative personal illness report naturally,rather than describing an unspecified illness as having taken hold.
1808|Complains that the speaker's body feels hot.|I feel so hot...|Restore the personal bodily heat sensation without adding a diagnosed fever or a measured temperature.
1809|Wonders whether the speaker has caught a cold.|Maybe it's a cold.|Retain the natural tentative wording;it refers to the current physical condition and does not claim a confirmed diagnosis. Japanese leaves the personal subject implicit here.
1810|Casually reports feeling feverish.|I'm feeling feverish...|Retain the fluent wording while replacing the obsolete full-width I guard with ASCII,subject to complete native glyph and actual-scene verification.
1811|Roughly wonders about a circulating illness and confidently assumes sleep will cure it.|Did I catch that bug going around...? Well, some sleep should clear it up!|That bug going around naturally conveys the suspected epidemic illness. Sleep is the character's confident supposition,not a measured recovery mechanic or a claim that an entire epidemic can be cured by sleeping.
1812|Coughs repeatedly and says the speaker does not feel well.|Cough, cough... I'm not feeling well...|Preserve the repeated cough sound and restore a natural personal report;do not replace the cough with an unrelated groan or a diagnosis.
1813|The informal speaker wonders if they are ill and says they have no appetite.|Am I sick...? I've lost my appetite.|Restore the personal uncertainty and lack of appetite as natural complete clauses,without inventing a refusal to eat or a different symptom.
1814|Politely remarks that the speaker feels physically wrong and wonders if they are ill.|I don't feel right... Could I be sick?|Restore the personal bodily unease and tentative question,rather than the old subjectless Maybe sick fragment.
1815|Rafael wonders if he is ill but reassures himself that he is all right.|Maybe I'm sick... But I'm all right...|Restore the personal subject and contrasting reassurance without inventing a completed recovery or medical certainty.
1816|Hodram feels that he cannot take a rest over a mere illness because he is the admiral.|I'm the admiral. I can't take a break because of a little illness...|Restore his personal responsibility and dismissive appraisal. The old generic rule that an admiral cannot rest while sick misstates his individual resolve.
1817|Lil feels bodily heaviness and wonders if she is ill.|I feel so sluggish... Am I sick...?|Sluggish conveys the heavy-body sensation naturally in English,without implying weight gain or inventing a symptom beyond the physical heaviness.
1818|Maria says not to worry and confidently predicts that an illness like this will soon pass.|Don't worry. This will pass quickly.|Retain the fluent confident reassurance. This refers to her illness in the native physical-state context;it is character speech,not independent proof of a recovery effect.
1819|Sera says not to worry,reassures that she is all right,and says she only feels a little unwell.|Don't worry. I'm all right. I just feel a little unwell...|Restore the omitted all-right reassurance and slight degree of discomfort,while keeping her speech simple and natural.
1820|Says the body will not move and wonders if the speaker is done for.|I can't move... Am I done for...?|Restore the first person and natural despairing question,without asserting that death has already happened.
1821|Laments being in a place like this,in an unfinished near-death fragment.|Here, of all places...|Keep the independent place-focused lament. Remove the unrelated dangling Can from the old English;this source is not the first half of message1822.
1822|Says the speaker cannot die yet.|I can't die yet...|Restore the complete independent first-person statement. The old English starts with t die yet because a contraction was incorrectly split across independently selected alternatives1821/1822.
1823|Wonderingly fears that the speaker may die.|Am I going to die...?|Restore the personal uncertain question and explicit death reference;the old already implication has no source counterpart.
1824|Roughly and defiantly insists the speaker cannot die yet.|I can't die yet...|Preserve the natural defiant statement without adding profanity or a guaranteed outcome. Replace the obsolete full-width I guard with ASCII and verify the entire line;two voices may naturally share these words.
1825|The older speaker wonders whether their time has finally come,using a death euphemism.|Has my time finally come...?|Retain the natural death euphemism and finally nuance. Do not invent a literal visitor,escort or family relationship from omukae.
1826|The food-loving speaker regrets not having eaten more before death.|If I'm going to die, I wish I'd eaten more first...|Express the food regret naturally while keeping death anticipated rather than already completed. The conditional makes the deathbed thought idiomatic and preserves the source regret without inventing an actual death event.
1827|Politely and doubtfully wonders whether the speaker will die in a place like this.|Am I really going to die in a place like this...?|Restore the personal future-facing question and location lament,rather than the old detached Dying here fragment.
1828|Rafael trails off about his still-unfulfilled dream and resolves to accomplish it.|My dream... I still have to make it come true...|Restore the personal determination and still-unfulfilled dream in natural English. Do not invent the dream's specific content in this independent line.
1829|Hodram insists he cannot die until he sees the strongest fleet.|I can't die until I see the strongest fleet...|Restore the omitted first-person refusal to die and the superlative strongest. Do not silently assign a new owner to the fleet or reduce the ambition to merely a mighty fleet.
1830|Lil wonders if she is going to die and calls out to Camille.|Am I going to die...? Camille...|Retain the natural wording and locked Camille spelling while replacing the obsolete mid-sentence full-width I with ASCII. Native complete-word proof must cover both I and all of Camille.
1831|Maria refuses to let things end in this place.|This can't be where it ends...|Retain the natural determined refusal in context. Do not invent a specific unfinished mission or claim that her life has already ended.
1832|Sera hesitantly says that she does not want to die.|... I... don't want to die...|Restore the omitted personal subject and opening hesitation as a single natural paragraph. Preserve her explicit wish not to die;do not invent a plea to a named person or an actual outcome.'''
PROSE={}
for line in DATA.splitlines():
    n,meaning,english,note=line.split('|');n=int(n)
    PROSE[n]=(meaning,english,note,'retain' if n in (1809,1818,1825,1831) else 'revise')


def main():
    assert not MANUSCRIPT.exists();ROOT.mkdir(parents=True,exist_ok=True)
    packet_path=Path('work/analysis/illness_critical_v971/source_context_packet.json');packet=read(packet_path)
    ledger=read('translations/editorial_review_current_v1.json')
    assert ledger['records_editorially_completed']==1092 and ledger['records_with_source_and_prose_pass']==1095
    assert sha(ROM.read_bytes())==packet['candidate_sha256']==ledger['current_integrated_candidate']['sha256']
    assert packet['source_condition_IDs']==[4,5]
    assert packet['condition4_selects_critical_sounding1820_1832_not_illness1807_1819'] and packet['condition5_selects_illness1807_1819']
    assert len(packet['all150_original_direct_main_battle_and_ordinary_condition4_5_selections'])==150 and len(packet['all100_prior_condition0_1_2_3_discriminating_controls'])==100
    current,clean=map(NdsImage.open,(ROM,'work/clean.nds'))
    jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/__arm9__.bin'))
    en=current_entries(current.read_file('/COMMON/MESFILE.DK4'),current.read_file('/__arm9__.bin'))
    sources={r['message_id']:r for r in packet['records_with_immediate_storage_neighbors']}
    policy_path=Path('translations/character_name_localization_policy_v1.json');policy=read(policy_path)
    camille=next(r for r in policy['confirmed_decisions'] if r['japanese']=='カミル');assert camille['localized_first_name']=='Camille'
    supplement=ROOT/'source_context_and_names.json'
    save(supplement,{'candidate_sha256':sha(ROM.read_bytes()),'established_term_documents':{str(policy_path):sha(policy_path.read_bytes())},'approved_Camille_decision':camille,
        'source_condition4_is_critical_dialogue_and5_is_illness':True,'physical_status_precedes_job_mood_and_battle_work':True,
        'independent_alternatives_not_consecutive_dialogue':True,'all26_source_IC_macros':[{'message_id':n,'IC_count':jp[n].text.count(b'IC')} for n in IDS],
        'no_IC_native_macro_in_selected_Japanese':all(b'IC' not in jp[n].text for n in IDS),'literal_Japanese_first_person_preserved_as_natural_English':True,
        'independent1821_and1822_no_cross_message_contraction':True,'obsolete_full_width_I_entries':[1810,1824,1830],
        'source1816_personal_admiral_responsibility_preserved':True,'source1828_dream1829_strongest_fleet1830_Camille1832_personal_wish_preserved':True,
        'cure_boasts_and_death_fears_are_character_speech_not_measured_game_outcomes':True,'neighbors_no_new_review_credit':[1806,1833]})
    rows=[]
    for n,(meaning,english,note,decision) in PROSE.items():
        s=sources[n];first=1807 if n<1820 else 1820;index=n-first;voice=index if index<8 else None;hero=index-8 if 8<=index<12 else None;special=24 if index==12 else None;condition=5 if n<1820 else 4
        speaker='Sera (native actor24 special response)' if special is not None else f'Native NPC voice class{voice}' if voice is not None else ['Rafael','Hodram Joakim Bergstrom (genuine captain1)','Lil','Maria'][hero]
        assert jp[n].text.hex()==s['source_hex'] and en[n].text.hex()==s['current_text_hex']
        assert english==' '.join(english.split()) and english.isascii() and not any(c in english for c in '%{}\n')
        if decision=='retain':assert english==s['current_English'].strip()
        rows.append({'id':f'COMMON_MESSAGE_{n}','message_id':n,'physical_condition_ID':condition,'role_ID':2,
            'role_ID_is_CPU_layout_fixture_only_not_source_semantics':True,'voice_class':voice,'protagonist_ID':hero,'special_actor_ID':special,'speaker':speaker,
            'context':f'Independent activity0 physical response for original condition{condition}. Condition5 selects illness1807-1819;condition4 selects critical-sounding1820-1832. Main12104 prioritizes physical state over job,mood and battle work. Original1250C selects eight NPC voices,12584 the four genuine protagonists,and12494 Sera24 special1819/1832. Neighbors are independent alternatives,not a conversation or shared contraction. Role2 is a CPU layout fixture only. Remarks and fears do not execute a cure,death or recovery.',
            'source_Japanese':s['source_Japanese'],'source_hex':s['source_hex'],'source_reference':s['source_reference'],'canonical_source_hex':s['canonical_text_hex'],
            'current_reference':s['current_reference'],'current_text_hex':s['current_text_hex'],'current_English':s['current_English'],'source_meaning':meaning,'english':english,
            'localization_note':note,'editorial_decision':decision,'native_argument_count':0,'source_native_macros':[],
            'review':{'source':True,'context':True,'localization':True,'naturalness':True,'formatting':False}})
    assert tuple(r['message_id'] for r in rows)==IDS and sum(r['editorial_decision']=='revise' for r in rows)==22
    save(MANUSCRIPT,{'format':'dk4-natural-dialogue-source-manuscript-v2','translation_policy':'natural-dialogue-v2','target_locale':'en-US','encoder':'dialogue-relocatable-v1',
        'consumer_layout_profile':'deck-illness-critical-visible-v1','review_gates':['source','context','localization','naturalness'],'formatting_review_pending':True,
        'status':'26-source-prose-reviewed-native-format-integration-and-actual-pending','file_path':'/COMMON/MESFILE.DK4',
        'source_clean_ROM_sha256':packet['source_clean_ROM_sha256'],'current_ROM':str(ROM),'current_ROM_sha256':sha(ROM.read_bytes()),
        'current_COMMON_sha256':packet['COMMON_sha256'],'current_ARM9_sha256':packet['ARM9_sha256'],'native_context_proof':str(packet_path),
        'native_context_proof_sha256':sha(packet_path.read_bytes()),'source_context_supplement':str(supplement),'source_context_supplement_sha256':sha(supplement.read_bytes()),'records':rows,'full_goal_complete':False})
    save(ROOT/'editorial_ledger_before_source_review.json',ledger)
    ledger['records_with_source_and_prose_pass']=ledger['records_with_source_prose_drafts']=1121
    ledger['source_prose_reviewed_counts_by_file']['/COMMON/MESFILE.DK4']=1120
    ledger['reviewed_but_incomplete_COMMON_IDs']=[750,751,752,*IDS]
    ledger['active_source_prose_drafts']={'native_message_IDs':[750,751,752,*IDS],'manuscripts':['work/analysis/market_contract_v758/unmapped_750_752_prose_DRAFT.json',str(MANUSCRIPT)],
        'status':'three-older-context-unmapped-and26-illness-critical-source-prose-reviewed-format-release-pending',
        'note':'These29 pending reviewed entries are not the full remaining shared/routes/player prose or raw-source scope.'}
    checkpoint='V972 source/prose-reviews26 illness/near-death comments1807-1832 for original conditions5/4:22 revisions and4 retentions. All150 original direct/main battle/ordinary selections and100 prior-status controls pass. Drafts restore personal symptoms,reassurance,admiral responsibility,independent complete1821/1822,death fears,food regret,dream,strongest fleet,locked Camille and Seras hesitant wish. Obsolete full-width I1810/1824/1830 becomes ASCII pending glyph proof. Native layout,registered integration and actual scenes remain pending. V969 stays current;1092 complete,1121 source/prose reviewed. Remaining shared/routes/player prose/raw coverage,older750-752,mood1833,special1885-1888,separate graphics/all18 plaques,Samwell header and later older-record re-audit remain open;full goal active.'
    ledger['latest_checkpoint']=checkpoint
    ledger['illness_critical_v972']={'status':'source-prose-reviewed-native-release-and-actual-pending','native_message_IDs':list(IDS),'manuscript':str(MANUSCRIPT),
        'source_context_proof':str(packet_path),'proposed_revisions':22,'justified_retentions':4,'completed_entries_added':0}
    ledger['research_checkpoints'].append({'id':'V972-Illness-Critical26-source-prose','proof':str(packet_path),'manuscript':str(MANUSCRIPT),'new_source_prose_reviews':26,'completed_entries_added':0,
        'previous_goal_turn_classification':'progress:13 wound messages completed in V969 with52 native fonts,four actual scenes/returns,exact patch and next26 physical-state source contexts',
        'this_goal_turn_classification':'progress:26 faithful source glosses,natural English decisions,250 selector/control cases,complete independent1821/1822 and source-bound naming review','full_goal_complete':False})
    assert sum(ledger['source_prose_reviewed_counts_by_file'].values())==1121
    save('translations/editorial_review_current_v1.json',ledger)
    doc=Path('docs/illness_critical_v972_source_review.md')
    with doc.open('x',encoding='utf-8') as f:f.write('# V972: illness and near-death source review\n\n'+checkpoint+'\n')
    for d in map(Path,('docs/translation_progress.md','docs/editorial_review_goal.md','docs/todo.md','docs/known_issues.md')):
        with d.open('a',encoding='utf-8') as f:f.write('\n\n## V972: illness and near-death source review\n\n'+checkpoint+' See [V972 source review](illness_critical_v972_source_review.md).\n')
    archive=Path('E:/Rota Nova translations/Editorial review/V972 Illness Critical source review');assert not archive.exists();copied=[]
    for source in (MANUSCRIPT,packet_path,supplement,Path(__file__),doc,Path('translations/editorial_review_current_v1.json')):
        target=archive/source.absolute().relative_to(Path.cwd());target.parent.mkdir(parents=True,exist_ok=True);copy2(source,target)
        assert sha(source.read_bytes())==sha(target.read_bytes());copied.append({'source':str(source),'archive':str(target),'sha256':sha(target.read_bytes())})
    save(ROOT/'archive_manifest.json',{'files':copied,'all_hashes_verified':True,'completed_entries_added':0})
    print('26 source/prose reviews:22 revisions,4 retentions.1092 complete,1121 source/prose;native/release/actual pending.',flush=True)


if __name__=='__main__':main()
