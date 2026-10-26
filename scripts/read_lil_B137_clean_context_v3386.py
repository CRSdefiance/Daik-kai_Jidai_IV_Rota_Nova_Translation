"""Record the complete clean exchange and48 fresh glosses before older English."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
SOURCE=Path('work/analysis/lil_remaining_B137_B140_source_v3380b/next48_B137_clean_current_context.json')
TRANSCRIPT=Path('work/analysis/lil_B137_clean_transcripts_v3385/complete_clean_transcript_and_branch_tool_provenance.json')
ROOT=Path('work/analysis/lil_B137_clean_context_v3386')
GLOSSES={
6:'Lil casually asks the barkeep to make something to eat because she is very hungry. おじさん is familiar address,not evidence that the barkeep is her uncle.',
17:'If Emilio is present,Lil\'s hunger draws his complaint that he too is starving,with the hyperbole that his stomach andback will stick together.',
28:'Samwell adds that he is hungry too. This reply is nested inside the Emilio-present branch as well as its own Samwell predicate;do not flatten it into anunconditional crew chorus.',
38:'The barkeep apologetically says he is short ofingredients just now andcan only offer drinking snacks ifthose will do.',
41:'Lil protests andasks why he has run out ofingredients atthis time. Do not invent a particular clock time or meal.',
52:'Conditional Emilio protests dramatically that he will die;inthis hungry exchange it is comic exaggeration,not anactual death ormedical event.',
64:'Conditional Samwell says he does not want tostarve todeath,inside the same nested Emilio/Samwell structure.',
74:'The barkeep explains that the man indicated has bought almost everything. Do not invent that allother patrons were legally barred fromeating.',
77:'Lil incredulously repeats Almost everything? tolead into the reveal.',
81:'Nagarpur laughs affectedly,demands more lavish food andsays he has plenty ofmoney.',
85:'Benazir politely announces that the food/order is ready orapologizes forthe wait. No new family orjob rank is inferred.',
89:'Nagarpur chuckles about the pretty young woman andhis impulse totouch her. Preserve the leering intrusion;do not invent a body part,explicit sexual act,romance ormutual attraction.',
92:'Benazir gives asudden yelp andaddresses Nagarpur respectfully by name. The source does not establish that the yelp expresses pleasure.',
96:'Nagarpur offers atip withcondescending laughter andtells her totake it.',
99:'Nagarpur boasts that withmoney anything ispossible,this is awonderful world,a paradise,andlaughs. His claim is not narration endorsing universal purchasing power.',
111:'Optional Fernando mocks the exaggerated paradise boast,saying the paradise exists only inside Nagarpur\'s head. Keep the direct echo ofthe preceding boast as one joke.',
126:'Optional Al expresses blunt contempt forNagarpur. This is aseparate predicate fromFernando\'s aside;both must retain their original conditional control structure.',
133:'Lil sharply interrupts Nagarpur toget his attention.',
137:'Nagarpur mistakes Lil for anew tavern girl andjudges her asdisappointing compared withthe other women. Preserve his presumptuous demeaning assessment without inventing Lil\'s age,body measurements,actual employment orromance.',
141:'Nagarpur decides she will do anyway andsummons her closer,continuing his mistaken assumption.',
145:'Lil angrily repeats his low-rating insult,says he isrude andhas noright tospeak toher thatway.',
156:'Optional Fernando pretends todefend Lil:calling her low isgoing toofar;he suggests lower-middle instead. Preserve the backhanded compliment andcomic undercut,not asincere unequivocal defense.',
168:'Camille\'s optional enthusiastic agreement sits inside Fernando\'s presence branch andits own Camille predicate. It agrees withthe backhanded defense,setting upLil\'s next retort.',
175:'Within the Fernando branch,Lil asks whether they arepraising her orinsulting her. Do not move this response outside its source conditional context.',
181:'Nagarpur finds Lil\'s angry face charming,offers agenerous tip andasks her name. His continued leering patronage does not establish affection fromLil.',
192:'Optional Gerhard isoutraged that their admiral isbeing mocked. Admiral isexplicit here;do not invent another rank forGerhard.',
198:'Lil says Nagarpur has misunderstood,introduces herself withthe exact FI runtime name andsays anymerchant should recognize that name. She does not name a newcompany orrank here.',
201:'Nagarpur says he does not know the name anddoes notcare,since his only interest ishis ownmoney.',
205:'Lil questions how he canfunction as amerchant whileknowing so little about theworld. Preserve her exasperated challenge.',
208:'Nagarpur addresses her as FI orwhatever hername isandchecks that she said she isamerchant. Preserve the second FI substitution anddismissive tone.',
211:'After a brief pause,Lil sharply confirms that she isamerchant.',
215:'Nagarpur tells her that as amerchant she should appreciate money\'s worth,because withit onecan doanything. This remains his argument.',
219:'Lil calls him foolish andinsists that there arethings money cannot buy. Do not replace this witha claim that allher crew arealready proven loyal.',
231:'Optional Camille\'s parenthesized private thought addresses FI andmarvels that she hasmatured. Preserve the third FI andthe distinction between thought andspoken praise;do not invent physical growth.',
245:'Optional Manuel praises the admiral\'s words asanexcellent saying andsays he will record it inhis poetry notes. Admiral isexplicit;the notebook isnot anewgift,item acquisition ordiary ofromance.',
252:'Nagarpur calls her the fool andargues that money canbuy power,possessions andeverything:the world runs onmoney. Keep this ashis boast andlaughter.',
255:'Lil repeats that she hasjust said there arethings money cannot buy,withrising frustration.',
258:'Nagarpur proposes a hypothetical test:what ifhe offered her navigators andsailors five times thewages she pays? What would they do? Preserve the exact fivefold ratio andthe conditional proposal,not anactual offer accepted orcrew defection.',
270:'Optional Al condemns him asrotten through andbeyond hope. Preserve the blunt contempt without inventing aviolent response.',
276:'Lil\'s bare exclamation mark isawordless shocked reaction tothe wage argument. It isareviewed source emote,not a placeholder ornewspoken factual claim.',
280:'Nagarpur says many people would surely be tempted bythe proposal andlaughs. Do not report that any specific crew member actuallyaccepted.',
283:'Lil hesitates,then insists there mustalso bepeople who willnot be lured bymoney;money alone cannot buy everything. Preserve her recovered conviction andthe limited claim,not absolute certainty about every crew member.',
287:'Nagarpur calls her stubborn andthreatens orconsiders bringing her whole company underhis control. This isfuture domination,not anaccomplished takeover orneworganizational rank.',
291:'Lil declares she willnot allow that.',
295:'Nagarpur questions whether she should speak soboldly andsays she willlearn soonenough. No specific violent punishment isdescribed.',
298:'Lil throws his warning back athim:he isthe one who willlearn.',
302:'Nagarpur says that onceher company isunderhis control,he willmake her aservant inhis household,withplenty ofwork. Preserve the demeaning future threat without inventing enslavement,sexual work oranalreadyheld position.',
306:'Lil says he hasgone farenough withhis nonsense andwarns him nottocome crying later. Preserve her defiant indignation andidiomatic warning.',
}
CONTEXT='Lil andconditional hungry companions ask forfood;the barkeep points toNagarpur,whohas bought almosteverything. His lavish dining,leering treatment ofBenazir,tips andmoney-equals-paradise boast provoke crew contempt. He mistakes Lil foratavern worker anddemeans her;Fernando\'s conditional lower-middle defense andCamille\'s nested agreement backfire comically. Gerhard may object forthe admiral. Lil asserts her FI identity,Nagarpur caresonly abouthismoney,andtheir confrontation becomes anargument aboutwhat moneycan buy. Optional Camille thinks shehas matured;Manuel wants the maxim forhispoetry notes. Nagarpur\'s hypothetical fivefold wages shock Lil,butshe regains conviction that somepeople cannotbebought. He threatenscompany domination andservant work;she refuses andanswers hiswarnings. Review the leering/mistaken-role material,the backhanded-praise joke andthe moral debate ascomplete progressions. Twelve original predicates andall48 relative sites retain optional andnested reactions;do not present everyconditional asoneuninterrupted chorus. Noearnedmeal,tip,job,crewdefection,takeover,rankchange,victory orprogress isclaimed.'
if __name__=='__main__':
    assert not ROOT.exists();packet,transcript=map(read,[SOURCE,TRANSCRIPT]);assert len(GLOSSES)==48 and set(GLOSSES)=={r['source_record_index'] for r in packet['records']}
    for item in transcript['transcripts']:assert sha(Path(item['path']).read_bytes())==item['sha256']
    rows=[]
    for r in packet['records']:
        rows.append({k:r[k] for k in ['id','file_path','block','source_reference','source_hex','source_Japanese','source_complete_preamble_hex','source_selector']}|dict(fresh_source_gloss=GLOSSES[r['source_record_index']],whole_exchange_context=CONTEXT,localized_English_not_authored=True,older_dialogue_English_not_editorially_compared=True,source_prose_orcompletion_credit_added=0))
    ROOT.mkdir(parents=True);save(ROOT/'all48_complete_clean_context_and_fresh_glosses.json',dict(source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),clean_transcripts=str(TRANSCRIPT),clean_transcripts_sha256=sha(TRANSCRIPT.read_bytes()),complete_exchanges={'137':CONTEXT},records=rows,all48_complete_clean_source_objects_read_before_older_English_comparison=True,all48_fresh_source_glosses_precede_localized_English=True,all117_original_commands_and12_optional_nested_predicates_considered=True,nested_Emilio_Samwell_and_Fernando_Camille_Lil_reactions_preserved=True,parenthesized_Camille_thought_distinct_from_spoken_praise=True,fivefold_wages_are_hypothetical_not_actual_defection=True,leering_without_invented_body_parts_or_mutual_romance=True,source_bare_exclamation_is_wordless_shock=True,no_new_selected_gameplay_or_earned_progress=True,new_source_prose_reviews=0,new_completed_records=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Complete cleanB137 exchange and48freshglosses recorded beforeolderEnglish comparison;conditional joke/thought/leering/fivefold-wage progression bound. No newreviewcredit.')
