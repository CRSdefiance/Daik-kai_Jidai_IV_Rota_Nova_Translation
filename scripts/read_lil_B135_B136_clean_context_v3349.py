"""Record whole clean exchanges and35 source glosses before older English."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
SOURCE=Path('work/analysis/lil_remaining_B135_B140_source_v3345b/next35_B135_B136_clean_current_context.json')
TRANSCRIPT=Path('work/analysis/lil_B135_B136_clean_transcripts_v3348/complete_clean_transcript_and_branch_tool_provenance.json')
ROOT=Path('work/analysis/lil_B135_B136_clean_context_v3349')
GLOSSES={
'DK4_MES_B135_R0006':'The distressed customer begs Espinosa to let him have the drug,stammering and struggling to speak.',
'DK4_MES_B135_R0009':'Espinosa first asks about money and whether the customer has brought it,using a cool transactional tone.',
'DK4_MES_B135_R0013':'The customer stammers as he offers what money he has.',
'DK4_MES_B135_R0017':'Espinosa counts the money,then says it is insufficient to obtain the named drug 女神の誘惑;the customer must raise more money andcome back.',
'DK4_MES_B135_R0021':'The customer protests in distress that this amount was enough before.',
'DK4_MES_B135_R0024':'Espinosa dismisses the prior price andsays market prices always fluctuate,using a respectable-business pretext.',
'DK4_MES_B135_R0027':'The customer says he has already sold his land andeverything else;the unfinished speech conveys desperation.',
'DK4_MES_B135_R0030':'Espinosa says that is none of his concern:without money there is no sale,andthe customer must leave.',
'DK4_MES_B135_R0034':'The customer makes one more broken plea,addressing Espinosa by name.',
'DK4_MES_B135_R0038':'Gilberto rudely orders the customer out,saying Espinosa considers him an eyesore. Do not invent anofficial subordinate rank.',
'DK4_MES_B135_R0041':'The customer sobs ormoans in distress;the sound is not a comic laugh.',
'DK4_MES_B135_R0045':'Espinosa chuckles andsavors how profitable the named drug is,saying he cannot stop laughing.',
'DK4_MES_B135_R0049':'Lil sharply calls out to Espinosa to get his attention.',
'DK4_MES_B135_R0053':'Espinosa affects polite charm toward Lil as a pretty young lady andasks whether she too wants the named drug. This does not establish noble status,romance orprecise age.',
'DK4_MES_B135_R0057':'Lil identifies him as the Espinosa who is spreading narcotics andmaking everyone suffer. Narcotics are explicit;do not soften this into ordinary goods ormedicine.',
'DK4_MES_B135_R0061':'Espinosa denies causing suffering,insists Lil is mistaken andclaims his customers are all pleased. This is his self-serving assertion,not narrator-confirmed happiness.',
'DK4_MES_B135_R0065':'Lil is outraged by his brazen denial andasks how he can carry on such a corrupt business without shame.',
'DK4_MES_B135_R0069':'Espinosa becomes sharper,tells her to stop making accusations andsays she has no right to interfere in what he calls legitimate transactions.',
'DK4_MES_B135_R0073':'Lil refuses to accept his feigned innocence,says she knows the whole situation andwarns she will respond if he persists.',
'DK4_MES_B135_R0077':'Espinosa asks mockingly what she intends to do.',
'DK4_MES_B135_R0081':'Lil vows that if he will not stop the drug trade,her FO company will defeat his trading company. Preserve the source FO substitution;this is a threat,not a completed victory.',
'DK4_MES_B135_R0085':'Espinosa addresses the listeners,inviting them to laugh at what he considers an amusing declaration.',
'DK4_MES_B135_R0088':'Gilberto cackles andmocks Lil,calling her threat a hilarious joke in coarse colloquial speech. No invented kinship orrank.',
'DK4_MES_B135_R0092':'Lil snorts andwarns that it will be too late when they regret underestimating her.',
'DK4_MES_B135_R0095':'Espinosa dismissively wishes her luck andchuckles.',
'DK4_MES_B135_R0106':'In the source-conditional Camille coda,Lil insists she will defeat Espinosa Company regardless of what happens andtells Camille that trying to stop her will be useless.',
'DK4_MES_B135_R0110':'Camille agrees that this time he will not stop her;he too finds Espinosa contemptible andunforgivable. Preserve the shift from Lil expecting restraint to shared resolve.',
'DK4_MES_B136_R0005':'Emilio asks why the object is in separate pieces,with casual childlike curiosity.',
'DK4_MES_B136_R0009':'Lil realizes he means the upper andlower halves of the mysterious stone tablet andnames both source items.',
'DK4_MES_B136_R0012':'Lil observes that although separate,they appear to be pieces of one tablet. This is her reasoning,not a newly invented legend.',
'DK4_MES_B136_R0015':'Emilio excitedly demonstrates that the two pieces fit together this way.',
'DK4_MES_B136_R0018':'Lil exclaims that they fit perfectly.',
'DK4_MES_B136_R0022':'Lil sees that the combined object is a map andtentatively asks whether it is the map to Africa\'s 覇者の証. Preserve uncertainty andthe distinction between a map andthe Proof itself.',
'DK4_MES_B136_R0025':'Emilio mishears Japanese chizu,map,as chiizu,cheese;he asks where it is andsays he wants to eat some. The joke is a food-driven phonetic misunderstanding,not knowledge of a separate cheese item.',
'DK4_MES_B136_R0029':'After a brief deadpan pause,Lil corrects Emilio:map,not cheese;then briskly announces they are going to search for the Proof. Preserve the correction/payoff together withthe preceding mishearing.',
}
if __name__=='__main__':
    assert not ROOT.exists();packet,transcript=map(read,[SOURCE,TRANSCRIPT]);assert len(GLOSSES)==35 and set(GLOSSES)=={r['id'] for r in packet['records']}
    for item in transcript['transcripts']:assert sha(Path(item['path']).read_bytes())==item['sha256']
    contexts={135:'A desperate drug customer has sold everything,Espinosa raises the price anddismisses him,Gilberto drives him away,andEspinosa gloats. Lil confronts him;his veneer of courtesy turns defensive while she escalates from moral outrage to a company-level threat. Espinosa andGilberto mock her. A conditional Lil/Camille coda establishes shared resolve. This complete exchange condemns exploitation without making the customer the butt of the joke. No narrator-endorsed customer happiness,medical claim,rank,kinship,noble status,earned victory ornew drug use is invented.',136:'Emilio notices two tablet pieces,Lil recognizes the source upper/lower items,andhe fits them together. Lil tentatively identifies a map to Africa\'s Proof. Emilio\'s map/cheese mishearing punctures the discovery with food-focused humor;Lil gives the deadpan correction andmoves the search forward. Review the mishearing andcorrection as one joke. An English phonetic food adaptation may be needed;the exact clean Japanese cheese meaning remains here. No earned Proof ornew geography is inferred.'}
    rows=[]
    for r in packet['records']:
        rows.append({k:r[k] for k in ['id','file_path','block','source_reference','source_hex','source_Japanese','source_complete_preamble_hex','source_selector']}|dict(fresh_source_gloss=GLOSSES[r['id']],whole_exchange_context=contexts[r['block']],localized_English_not_authored=True,older_dialogue_English_not_editorially_compared=True,source_prose_orcompletion_credit_added=0))
    ROOT.mkdir(parents=True);save(ROOT/'all35_complete_clean_context_and_fresh_glosses.json',dict(source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),clean_transcripts=str(TRANSCRIPT),clean_transcripts_sha256=sha(TRANSCRIPT.read_bytes()),complete_exchanges=contexts,records=rows,all35_complete_clean_source_objects_read_before_older_English_comparison=True,all35_fresh_source_glosses_precede_localized_English=True,all61_original_commands_and_conditional_Camille_coda_considered=True,terms_still_require_clean_current_item_and_narcotic_name_binding=True,English_map_cheese_joke_requires_contextual_localization=True,no_new_selected_gameplay_or_earned_progress=True,new_source_prose_reviews=0,new_completed_records=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Complete cleanB135/B136 exchanges and35freshglosses recorded beforeoldEnglish comparison;drug-exploitation tone andmap/cheese joke bound. No newreviewcredit.')
