"""Fresh complete-exchange source reading and63 glosses before old-English review."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
SOURCE=Path('work/analysis/lil_remaining_B131_B140_source_v3306b/next63_B131_B133_clean_current_context.json')
TRANSCRIPT=Path('work/analysis/lil_B131_B133_clean_transcripts_v3309/complete_clean_transcript_and_branch_tool_provenance.json')
ROOT=Path('work/analysis/lil_B131_B133_clean_context_v3312')
GLOSSES={
 (131,5):'Lil suspects that this Old Parchment is a map to the Proof of Supremacy.',
 (131,15):'Camille says it looks like ordinary paper, but surely there must be some hidden trick to it.',
 (131,20):'Fernando says nothing is written on it; there must be some hidden trick.',
 (131,26):'Lil wonders whether this red pigment might work.',
 (131,30):'She cannot think of anything else, so she is certain this must be what they use; she insists she cannot be wrong.',
 (131,42):'Fernando asks how she intends to use it.',
 (131,57):'Camille urgently asks FI to wait and asks what she is doing.',
 (131,64):'Lil says she will apply it over the paper, like this.',
 (131,76):'Fernando reacts in surprise: something is appearing on the paper.',
 (131,82):'Lil smugly says she was right and they now have the map to the North Sea Proof of Supremacy.',
 (131,92):'Camille praises FI and suggests going immediately to look for the Proof.',
 (131,98):'Fernando praises her for figuring it out and suggests going to look for the Proof.',
 (131,105):'Lil boasts that the North Sea is now hers.',
 (133,5):'Camille observes that this city is an important hub linking the North Sea and Mediterranean.',
 (133,8):'Lil complains that the Portuguese military and trading companies control it tightly and will not let her do business.',
 (133,12):'Rafael politely and hesitantly gets their attention.',
 (133,17):'Lil asks what he wants.',
 (133,21):'Rafael asks whether she is FI of FO.',
 (133,26):'Lil is pleased at how famous she has become, then asks who he is.',
 (133,29):'He introduces himself as Rafael Castor of the Castor Company.',
 (133,35):'Lil exclaims in surprise that he is the man from the Castor Company.',
 (133,38):'Rafael is puzzled.',
 (133,43):'Lil says she cannot believe it: he is still just a child.',
 (133,47):'Camille sharply calls FI by name to protest her rudeness.',
 (133,51):'Rafael repeats child, taken aback.',
 (133,56):'Claudio retorts that she is the last person they want to hear that from and appeals to Rafi.',
 (133,59):'Lil angrily asks what he said, calls him a rude muscular man and asks whether he is picking a fight.',
 (133,63):'Claudio protests that she was the one who said it first.',
 (133,66):'Camille tells FI that Claudio is right.',
 (133,70):'Rafael tries to calm Claudio down, using his familiar nickname Clau.',
 (133,75):'Claudio tells Rafael to get at least a little angry too.',
 (133,79):'Rafael says it is all right because he does not mind.',
 (133,83):'Claudio trails off in exasperation at him.',
 (133,87):'Lil asks whether this man really is an admiral.',
 (133,91):'Rafael confirms it, still puzzled by the question.',
 (133,96):'Lil says he is something of a letdown compared with what she expected.',
 (133,100):'Rafael remains puzzled.',
 (133,105):'Lil clears her throat, then asks whether he wants something from her.',
 (133,108):'Rafael asks whether she wants to make a contract in this city.',
 (133,113):'Lil says that is rather abrupt, but admits that she does.',
 (133,116):'Rafael politely proposes exchanging her market share in Nantes for his market share in Lisbon, if she is willing.',
 (133,120):'Lil is surprised by the suggestion of an exchange.',
 (133,124):'Rafael stresses that the proposal is only if she is willing.',
 (133,129):'Lil says it is not a bad proposition and asks whether they would exchange one percent for one percent.',
 (133,132):'Claudio refuses equal terms: Lisbon is a large city and a transportation hub, so two to one is about the best offer.',
 (133,136):'Lil confirms the direction: if she gives up two percent in Nantes, they give her one percent in Lisbon.',
 (133,140):'Rafael confirms yes.',
 (133,145):'Claudio says it is fine if she does not want the deal; they will ask someone else.',
 (133,148):'Rafael asks what she thinks.',
 (133,164):'Lil says that looking at his pampered young-man face has made her stop caring about the argument over terms.',
 (133,167):'She adds that they cannot avoid passing Lisbon on the way to the Mediterranean.',
 (133,170):'Rafael happily declares that they have a deal.',
 (133,175):'Claudio says they now have a foothold for expanding into the North Sea.',
 (133,178):'Rafael thanks FI and asks for their continued goodwill/cooperation.',
 (133,190):'An unlabeled system notice says the Nantes and Lisbon market shares have been exchanged.',
 (133,194):'Lil huffs that she will not fall for that smooth talk.',
 (133,197):'Rafael is disappointed that it did not work; he had thought the terms were good.',
 (133,201):'Claudio says they cannot help it and should ask someone else.',
 (133,205):'Rafael tells Claudio to leave it: expecting others to help was asking too much, and steady effort on their own is best.',
 (133,209):'Claudio grumbles that making money by a slow, unexciting grind does not suit his temperament.',
 (133,213):'Lil remarks that they are strange people.'}
CHOICES={(133,1530,0):'Hmm... all right; reluctant acceptance of the proposed terms.',(133,1530,1):'Are you stupid? A pointed, insulting refusal of the proposed terms.'}
if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE);transcript=read(TRANSCRIPT)
    assert {(r['block'],r['source_record_index']) for r in packet['records']}==set(GLOSSES) and len(GLOSSES)==61
    assert {(r['block'],r['command_offset'],r['option_index']) for r in packet['typed_choice_records']}==set(CHOICES) and len(CHOICES)==2
    for p in transcript['transcripts']:assert sha(Path(p['path']).read_bytes())==p['sha256']
    groups=[dict(block=131,scene='Lil reveals the North Sea Proof map by applying the red pigment to the Old Parchment.',progression='Suspected map and apparently blank paper;optional Camille/Fernando observations and questions;Lil has no other idea but grows adamantly confident;Camille objects as she acts;the image appears;Lil boasts,praises from either companion follow,andthey plan to seek the Proof. Companion alternatives are separate conditional turns,not one concatenated conversation.',voice='Lil is inventive,impulsive andsmug when her guess works;Camille is cautious then admiring;Fernando is practical andblunt.',facts='Preserve an initial guess,unwritten parchment,red pigment application andthe distinction between discovering its map andfinding the Proof itself. Final North Sea possession is Lil\'s boast,not an earned current territory claim. Use registered item names after exact item binding. No invented ink,water,fire,alchemy orrecipe.',native_context='Five native predicates and24 broader next-batch relative sites are bound separately. The physical source command order includes optional speakers. No new item use,reward,Proof discovery orscene activation is claimed.'),dict(block=133,scene='Lil meets Rafael Castor andClaudio at the Lisbon trade gateway andnegotiates unequal Nantes/Lisbon market-share terms.',progression='Camille notes the gateway;Lil complains about Portuguese control;Rafael politely introduces himself;Lil calls him a child;Claudio bristles,Camille corrects her andRafael diffuses the quarrel. Lil finds his mild manner underwhelming,thenRafael abruptly proposes a share exchange. Lil suggests one-to-one;Claudio demands two-to-one,with Lil explicitly confirming two percent Nantes for one percent Lisbon. Choice0 accepts reluctantly,followed by foothold/cooperation andFEexchange notice;choice1 rejects rudely,thenhumble Rafael favors steady self-reliance whileClaudio dislikes the grind andLil calls themstrange. Never merge the two endings.',voice='Lil is proud,prickly andskeptical,thenreluctantly pragmatic. Rafael is gentle,polite,hesitant and conciliatory,without hidden menace or romance. Claudio is brash,protective andbusinesslike. Camille is tactful but willing to call Lil out.',facts='Keep all percentages andtheir direction. Rafael is actually an admiral in this exchange;do not invent a new rank for Claudio or change captain/company context to Rafael\'s route. Child andpampered-face remarks are Lil\'s judgments,not numerical ages,kinship ornew noble rank. Familiar Rafi/Clau forms need approved-name reconciliation. The city/Portuguese military andcompanies/Lisbon travel claim remain character context,not a real-world navigation correction. The FE notice is unlabeled andonly on acceptance.',native_context='All18 source00 speeches contain real Japanese,with currentstatic actor0/Rafael Castor andFI/FO captain2 substitutions bound. There is one original2100 menu withordered indices0/1;two source/currentFE null-actor cases and122total dispatches are bound. Native original EV2 action selects SC2block133;the historical London snapshot is not a selected Lisbon eligibility or share-exchange claim.')]
    rows=[]
    for r in packet['records']+packet['typed_choice_records']:
        choice=r['kind']=='typed-choice-label';key=(r['block'],r['command_offset'],r['option_index']) if choice else (r['block'],r['source_record_index'])
        rows.append(dict(id=r['id'],block=r['block'],source_reference=r['source_reference'],source_hex=r['source_hex'],source_Japanese=r['source_Japanese'],source_meaning=CHOICES[key] if choice else GLOSSES[key],complete_exchange_context=next(g for g in groups if g['block']==r['block']),fresh_gloss_written_before_localized_English=True))
    assert len(rows)==63
    ROOT.mkdir(parents=True);save(ROOT/'all63_complete_clean_context_and_fresh_glosses.json',dict(source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),transcript_provenance=str(TRANSCRIPT),transcript_provenance_sha256=sha(TRANSCRIPT.read_bytes()),groups=groups,records=rows,all63_complete_clean_source_objects_read_before_older_English_comparison=True,all63_fresh_source_glosses_precede_localized_English=True,no_current_English_used_as_translation_source=True,older_English_comparison_still_pending=True,item_terminology_and_nickname_binding_still_pending=True,native_full_display_references_and_registered_release_pending=True,source_prose_or_completion_credit_added=0,new_emulator_runs=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Both complete clean exchanges andall63 source objects read;63fresh sourceglosses saved before older-English comparison orlocalizedprose. Zero review credit.')
