"""Source-led English review of39 independently selected mood and panic comments."""
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.illness_critical_editorial import current_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/mood_comments_v978')
ROM=Path('out/all_routes_combined_v975_candidate.nds')
MANUSCRIPT=Path('translations/mood_comments_editorial_manuscript_v1.json')
IDS=tuple(range(1833,1872))
RETAINED={1836,1837,1839,1847,1850,1854,1859,1861,1862,1863,1864,1865,1867,1871}
DATA='''1833|Politely reports being in an especially upbeat mood right now.|I'm in high spirits right now!|Restore the personal present mood. High spirits expresses norinori naturally without implying a lucky winning streak or measured task success.
1834|Reports feeling refreshed and ready for any command.|I feel refreshed and ready for any order!|Restore the omitted refreshed feeling and preserve the open willingness to receive orders,without inventing a specific assignment.
1835|Enthusiastically says the speaker is in top form and feels able to do anything.|I'm in top form! I feel like I can do anything!|Restore the personal subject and subjective feeling of possibility;do not turn it into a guaranteed ability to perform every task.
1836|Cheerfully reports a happy mood,with a musical delivery cue.|So happy!|Retain the natural joyful exclamation. The Japanese music note signals cheerful delivery rather than additional lexical content or song lyrics.
1837|Roughly expresses feeling ready to take on anything.|Bring it on!|Retain the natural idiomatic equivalent of don to koi;no new opponent,order or action is invented.
1838|The older speaker laughs heartily and says they feel good.|Ha ha! I feel great!|Restore the hearty laugh and personal good feeling in natural English,without imposing an exaggerated dialect or family relationship.
1839|The informal speaker says they are full of motivation.|Ready and raring to go!|Retain the fluent enthusiastic expression of motivation;the portrait and native response provide the personal context.
1840|Politely reports an excellent mood and says the speaker's work is progressing well.|I'm in a great mood! My work's going smoothly.|Restore the personal present assessment rather than a generic rule that work always goes faster. This is dialogue,not an independent measurement of a productivity modifier.
1841|Rafael says he feels good and is becoming motivated.|I feel great! I'm ready to get to work!|Restore the positive personal feeling and motivated readiness;What a mood can suggest a bad mood in English.
1842|Hodram feels strength welling up from deep within his body.|I feel strength welling up from deep within.|Restore the subjective personal sensation and deep origin of the strength,rather than declaring an objective power increase.
1843|Lil gives a pleased vocalization and an emphatic best-ever-feeling exclamation.|Mmm, I feel fantastic!|Restore a complete independent pleased exclamation. The old So refr is an unrelated cross-message fragment,not part of this source.
1844|Maria says she feels refreshed and clear.|I feel refreshed.|Restore the complete independent personal statement;the old eshing is a suffix incorrectly shared with1843.
1845|Sera cheerfully says she feels fantastic right now.|I feel fantastic right now!|Retain the natural wording and cheerful exclamation,while replacing the obsolete full-width I guard with complete ASCII subject to native-font and actual-scene proof.
1846|Hesitantly says the speaker cannot find motivation.|I just can't get motivated...|Retain the natural wording while replacing the obsolete full-width I guard with ASCII. Do not invent a cause or a request to change assignments.
1847|Says the speaker is not feeling in the mood.|Not feeling it...|Retain the natural understated colloquial expression of missing enthusiasm,with no invented object or reason.
1848|Casually wishes for a change of mood or pace.|I could use a change of pace.|Restore the personal soft suggestion,rather than a subjectless statement of a compulsory need.
1849|Sighs and says the speaker feels vaguely gloomy.|Sigh... I'm feeling kind of down...|Preserve the sigh and vague personal low mood. Kind of down is natural American English and avoids imposing a clinical diagnosis.
1850|Roughly expresses listless reluctance.|What a drag...|Retain the idiomatic weary complaint in this mental-state context;do not turn it into a particular accusation or physical injury.
1851|The older speaker hesitantly says they cannot find motivation.|I can't seem to get motivated...|Restore a natural personal statement and the uncertain lack of drive,without inventing age-related incapacity or a family relationship.
1852|The informal speaker emphatically says they are hungry.|I'm starving!|Restore the explicit oira first-person subject as natural English hunger hyperbole;do not interpret it as a verified fatal starvation state.
1853|Mumbles,then explains that the speaker was only talking to themself.|"Mutter, mutter..." Oh, I was just talking to myself...|Preserve the quoted mumble and natural corrective explanation. Just talking alone omits the source self-talk meaning.
1854|Rafael sighs without additional speech.|Sigh...|Retain the natural English representation of the sigh;do not add a reason or conclusion.
1855|Hodram is silent,represented only by a Japanese ellipsis.|...|Restore a normal English ellipsis as the complete independent nonverbal response. The old Ug letters belong to neither this source nor a shared continuation and must be removed.
1856|Lil whines and protests that she has had enough.|Ugh, I've had enough!|Restore the full independent complaint,including the leading vocalization. Do not borrow the missing Ug from1855 or leave the old leading h fragment.
1857|Maria pauses,says she cannot concentrate,and tentatively considers a change of pace.|... I can't concentrate... Maybe a change of pace...|Preserve the initial hesitation,personal lack of concentration and tentative refreshment idea. A change of pace is not necessarily a rest break or reassignment.
1858|Sera pauses and says she does not want to talk right now.|... I don't want to talk right now.|Retain the natural refusal and opening pause while replacing the full-width I and adding the ordinary word separator. No leading blank line or alignment space is authored.
1859|Politely and with a stammer asks what has happened.|W-what happened???|Retain the natural stammer and emphatic question marks,without inventing an event or an explanation.
1860|Repeatedly asks what is happening in alarm.|What? What? What's going on?!|Restore the repeated alarmed questions in natural English without imposing an old-fashioned dialect or a specific cause.
1861|Asks what is going on and says the speaker has no idea.|What's going on? No clue!|Retain the natural casual questions and explicit bewilderment;No clue conveys the source emphatic lack of understanding.
1862|Screams twice in panic.|Aah! Aah!|Retain both natural English screams without adding words,an attacker or an outcome.
1863|Gives a loud nonverbal bellow.|Raaagh!|Retain the English bellow as an alarmed nonverbal vocalization. Do not expand it into a spoken threat or order.
1864|The older speaker repeatedly asks what has happened in alarm.|What? What? What's happened?!|Retain the fluent repeated questions and alarm;do not invent an explanation or a caricatured dialect.
1865|Stammers and asks what has happened.|W-what happened?!|Retain the natural English stammer and alarmed question as an equivalent of the source repeated hesitation.
1866|Shows puzzled alarm and asks what is going on.|What...? What's going on?!|Express the source question-mark puzzlement as natural hesitant English before the alarmed question,instead of an isolated leading question-mark glyph.
1867|Rafael repeatedly asks what everything is in alarm.|What?! What is all this?!|Retain the natural emphatic bewilderment;English punctuation conveys the source repeated questions without requiring literal duplication of every word.
1868|Hodram reacts in alarm,then admonishes himself to remain calm at a time like this.|No! I have to stay calm at a time like this!|Restore his personal self-command and this-time emphasis,rather than a detached maxim about when calm matters.
1869|Lil screams twice and demands to know what is going on.|Aah! Aah! What's going on?!|Restore the repeated screams and her emphatic question,without inventing a cause or an accusation.
1870|Maria reacts in alarm and realizes that she must calm herself.|No! I have to calm down...|Restore the personal necessity to calm herself. The old Calm down can be read as an order to someone else.
1871|Sera's panic is represented by deliberately unintelligible comic symbols rather than readable words.|@#$*!!|Retain the established English comic-symbol equivalent as nonverbal garbled panic. Do not invent lexical content or expand it into explicit profanity. The string contains no percent formatter directive or translator control.'''
PROSE={}
for line in DATA.splitlines():
    n,meaning,english,note=line.split('|');n=int(n)
    PROSE[n]=(meaning,english,note,'retain' if n in RETAINED else 'revise')


def main():
    assert not MANUSCRIPT.exists();ROOT.mkdir(parents=True,exist_ok=True)
    packet_path=Path('work/analysis/mood_comments_v977/source_context_packet.json');packet=read(packet_path)
    ledger=read('translations/editorial_review_current_v1.json')
    assert ledger['records_editorially_completed']==1118 and ledger['records_with_source_and_prose_pass']==1121
    assert sha(ROM.read_bytes())==packet['candidate_sha256']==ledger['current_integrated_candidate']['sha256']
    assert packet['source_mood_IDs']==[0,4,5] and packet['source_physical_condition0_required_for_mood_selection']
    assert len(packet['all225_original_direct_main_battle_and_ordinary_mood_selections'])==225
    assert len(packet['all75_physical_condition1_priority_controls'])==75 and len(packet['all72_direct_NPC_hero_normal_mood1_2_3_no_message_controls'])==72
    current,clean=map(NdsImage.open,(ROM,'work/clean.nds'))
    jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/__arm9__.bin'))
    en=current_entries(current.read_file('/COMMON/MESFILE.DK4'),current.read_file('/__arm9__.bin'))
    sources={r['message_id']:r for r in packet['records_with_immediate_storage_neighbors']}
    supplement=ROOT/'source_context_and_nonverbal_review.json'
    policy='translations/character_name_localization_policy_v1.json'
    save(supplement,{'candidate_sha256':sha(ROM.read_bytes()),'established_term_documents':{policy:sha(Path(policy).read_bytes())},
        'source_mood0_positive4_dejected5_panic':True,'physical_condition0_required_and_condition1_preempts_mood':True,'independent_alternatives_not_consecutive_dialogue':True,
        'all39_source_IC_macros':[{'message_id':n,'IC_count':jp[n].text.count(b'IC')} for n in IDS],'no_IC_native_macro_in_selected_Japanese':all(b'IC' not in jp[n].text for n in IDS),
        'literal_Japanese_first_person_preserved_as_natural_English':True,'independent1843_1844_and1855_1856_not_split_words':True,
        'obsolete_full_width_I_entries':[1845,1846,1858],'source1855_nonverbal_silence_only':jp[1855].text.decode('cp932'),
        'source1871_nonverbal_comic_symbols_only':jp[1871].text.decode('cp932'),'nonverbal_English_equivalents':{'1855':'...','1871':'@#$*!!'},
        'no_spoken_words_added_to_silence_or_comic_symbols':True,'source1868_and1870_are_personal_self_calming':True,
        'Sera_direct_normal_moods_not_used_outside_original_contract':True,'neighbors_no_new_review_credit':[1832,1872]})
    rows=[]
    for n,(meaning,english,note,decision) in PROSE.items():
        s=sources[n];first,mood=(1833,0) if n<1846 else (1846,4) if n<1859 else (1859,5);index=n-first
        voice=index if index<8 else None;hero=index-8 if 8<=index<12 else None;special=24 if index==12 else None
        speaker='Sera (native actor24 special response)' if special is not None else f'Native NPC voice class{voice}' if voice is not None else ['Rafael','Hodram Joakim Bergstrom (genuine captain1)','Lil','Maria'][hero]
        assert jp[n].text.hex()==s['source_hex'] and en[n].text.hex()==s['current_text_hex']
        assert english==' '.join(english.split()) and english.isascii() and not any(c in english for c in '%{}\n')
        if decision=='retain':assert english==s['current_English'].strip()
        rows.append({'id':f'COMMON_MESSAGE_{n}','message_id':n,'physical_condition_ID':0,'mood_ID':mood,'role_ID':2,'role_ID_is_CPU_layout_fixture_only_not_source_semantics':True,
            'voice_class':voice,'protagonist_ID':hero,'special_actor_ID':special,'speaker':speaker,'nonverbal_only':n in (1855,1871),
            'context':f'Independent activity0 mood{mood} response with original physical condition0. Main12104 checks physical status first,then mood0/4/5 before working roles. Original123C8 selects eight NPC voices,1242C the four genuine protagonists,and12380 Sera24 special1845/1858/1871. Storage neighbors are independent alternatives,not a conversation or shared word. Role2 is a CPU layout fixture only. Sera direct normal-mood1/2/3 calls are outside the original caller contract and are not used. Mood descriptions are character speech,not measured stat or productivity effects.',
            'source_Japanese':s['source_Japanese'],'source_hex':s['source_hex'],'source_reference':s['source_reference'],'canonical_source_hex':s['canonical_text_hex'],
            'current_reference':s['current_reference'],'current_text_hex':s['current_text_hex'],'current_English':s['current_English'],'source_meaning':meaning,'english':english,
            'localization_note':note,'editorial_decision':decision,'native_argument_count':0,'source_native_macros':[],
            'review':{'source':True,'context':True,'localization':True,'naturalness':True,'formatting':False}})
    assert tuple(r['message_id'] for r in rows)==IDS and sum(r['editorial_decision']=='revise' for r in rows)==25
    save(MANUSCRIPT,{'format':'dk4-natural-dialogue-source-manuscript-v2','translation_policy':'natural-dialogue-v2','target_locale':'en-US','encoder':'dialogue-relocatable-v1',
        'consumer_layout_profile':'deck-mood-comments-visible-v1','review_gates':['source','context','localization','naturalness'],'formatting_review_pending':True,
        'status':'39-source-prose-reviewed-native-format-integration-and-actual-pending','file_path':'/COMMON/MESFILE.DK4','source_clean_ROM_sha256':packet['source_clean_ROM_sha256'],
        'current_ROM':str(ROM),'current_ROM_sha256':sha(ROM.read_bytes()),'current_COMMON_sha256':packet['COMMON_sha256'],'current_ARM9_sha256':packet['ARM9_sha256'],
        'native_context_proof':str(packet_path),'native_context_proof_sha256':sha(packet_path.read_bytes()),'source_context_supplement':str(supplement),'source_context_supplement_sha256':sha(supplement.read_bytes()),
        'records':rows,'full_goal_complete':False})
    save(ROOT/'editorial_ledger_before_source_review.json',ledger)
    ledger['records_with_source_and_prose_pass']=ledger['records_with_source_prose_drafts']=1160
    ledger['source_prose_reviewed_counts_by_file']['/COMMON/MESFILE.DK4']=1159
    ledger['reviewed_but_incomplete_COMMON_IDs']=[750,751,752,*IDS]
    ledger['active_source_prose_drafts']={'native_message_IDs':[750,751,752,*IDS],'manuscripts':['work/analysis/market_contract_v758/unmapped_750_752_prose_DRAFT.json',str(MANUSCRIPT)],
        'status':'three-older-context-unmapped-and39-mood-source-prose-reviewed-format-release-pending','note':'These42 pending reviewed entries are not the full remaining shared/routes/player prose or raw-source scope.'}
    checkpoint='V978 source/prose-reviews39 mood0/4/5 comments1833-1871:25 revisions and14 retentions. All225 original direct/main battle/ordinary selections,75 physical-priority and72 defined normal-mood controls pass. Drafts restore personal mood,motivation,work assessment,independent1843/1844 and1855/1856,complete ASCII I,self-talk and personal self-calming. Silent1855 and comic1871 remain nonverbal. Native layout,registered integration and actual scenes remain pending. V975 stays current;1118 complete,1160 source/prose reviewed. Remaining shared/routes/player prose/raw coverage,older750-752,special1885-1888,raw abandon-caption0x134E54,separate graphics/all18 plaques,Samwell header and later older-record re-audit remain open;full goal active.'
    ledger['latest_checkpoint']=checkpoint
    ledger['mood_comments_v978']={'status':'source-prose-reviewed-native-release-and-actual-pending','native_message_IDs':list(IDS),'manuscript':str(MANUSCRIPT),
        'source_context_proof':str(packet_path),'proposed_revisions':25,'justified_retentions':14,'completed_entries_added':0}
    ledger['research_checkpoints'].append({'id':'V978-Mood39-source-prose','proof':str(packet_path),'manuscript':str(MANUSCRIPT),'new_source_prose_reviews':39,'completed_entries_added':0,
        'previous_goal_turn_classification':'progress:26 illness/near-death messages completed in V975 with52 native fonts,six actual scenes/returns,exact patch and next39 mood source contexts',
        'this_goal_turn_classification':'progress:39 source glosses,natural English decisions,372 defined source/control cases,independent split-word repairs and explicit nonverbal review','full_goal_complete':False})
    assert sum(ledger['source_prose_reviewed_counts_by_file'].values())==1160
    save('translations/editorial_review_current_v1.json',ledger)
    doc=Path('docs/mood_comments_v978_source_review.md')
    with doc.open('x',encoding='utf-8') as f:f.write('# V978: mood and panic source review\n\n'+checkpoint+'\n')
    for d in map(Path,('docs/translation_progress.md','docs/editorial_review_goal.md','docs/todo.md','docs/known_issues.md')):
        with d.open('a',encoding='utf-8') as f:f.write('\n\n## V978: mood and panic source review\n\n'+checkpoint+' See [V978 source review](mood_comments_v978_source_review.md).\n')
    archive=Path('E:/Rota Nova translations/Editorial review/V978 Mood comments source review');assert not archive.exists();copied=[]
    for source in (MANUSCRIPT,packet_path,supplement,Path(__file__),doc,Path('translations/editorial_review_current_v1.json')):
        target=archive/source.absolute().relative_to(Path.cwd());target.parent.mkdir(parents=True,exist_ok=True);copy2(source,target)
        assert sha(source.read_bytes())==sha(target.read_bytes());copied.append({'source':str(source),'archive':str(target),'sha256':sha(target.read_bytes())})
    save(ROOT/'archive_manifest.json',{'files':copied,'all_hashes_verified':True,'completed_entries_added':0})
    print('39 source/prose reviews:25 revisions,14 retentions.1118 complete,1160 source/prose;native/release/actual pending.',flush=True)


if __name__=='__main__':main()
