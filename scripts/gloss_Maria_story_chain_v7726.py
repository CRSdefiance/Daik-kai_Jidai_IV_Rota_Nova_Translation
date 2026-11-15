"""Author67 clean-Japanese source glosses as three whole exchanges before any current English."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_story_chain_gloss_v7726')
SOURCE=Path('work/analysis/maria_story_chain_clean_v7725/complete_clean_34_108_35_67_refs_explicit_source_dependency_chain_before_current_English.json')
GLOSSES={
34:{
5:"Speaker74 asks whether the visitor is the famous person addressed by the FA name macro plus polite san. He advises withdrawing before becoming caught up in the dispute between クーン (Kuhn spelling-consistency lead) and ペレイラ (Pereira). It is a safety recommendation, not an order or a claim that the visitor is already involved.",
10:"The same speaker says either side's victory makes no difference to people like him; the whole affair is a nuisance. He ends with an exasperated sigh. The following explanation supplies the sense that neither result helps the locals, rather than proving that he feels no concern about harm.",
13:"Maria asks why. In context she is asking why either outcome makes no useful difference to the people he has just mentioned.",
17:"The local speaker explains that these distant newcomers are trying to expand their own countries. Whichever side wins, the locals will only be exploited; there is no benefit for the local area. Preserve both foreign national expansion and local exploitation without inventing a tax, slave trade, massacre, named current town or guaranteed game statistic.",
20:"Speaker0A draws the conclusion that neither side gives any thought to the local people. The Japanese voice uses the reflective janaa form; preserve the judgment without inferring a family relationship, title or new age label from that speech style.",
23:"Maria falls silent in thought. The source contains a single CP932 ellipsis, not three and not spoken assent or a new promise.",
34:"Speaker4A formally reports that Portugal and the Netherlands both have designs on expanding into East Asia. Keep the two countries and East Asia distinct from the earlier local remark; do not substitute Southeast Asia or assert the current scene location. This line's actual conditional/role selection still needs native binding.",
42:"Maria tentatively concludes that action will need to be taken before harm reaches her homeland. Preserve the prospective assessment and protective motivation; no particular war, attack plan, alliance or guaranteed outcome is specified.",
},
108:{
4:"The injured speaker9B groans weakly and collapses with the written batta falling sound. Preserve the gasp and sound cue; do not invent a wound type or cause at this point.",
14:"Speaker0A reacts with a startled stammer: what is happening? This is a source reaction variant whose actual selection must be preserved rather than assumed to play with all other reactions.",
20:"Speaker1A likewise gives a startled stammered reaction. Preserve its separate source speaker and possible alternative placement; no extra spoken explanation is given.",
34:"Speaker4A exclaims that someone has collapsed. Keep the formal voicing and discovery; the line itself supplies no diagnosis or account of an attacker.",
43:"Maria asks what is wrong or what has happened, responding to the collapse.",
47:"The injured man haltingly asks for help.",
51:"Speaker0A observes that the injury is severe and asks what on earth happened. The cause is still a question.",
54:"Maria says treatment must come first and asks him to bear with the pain. No particular medicine, operation, bandage or completed recovery is stated.",
57:"The injured man offers a weak apologetic/grateful sumanee response to the offered care. In this exchange it can convey thanks for the trouble without inventing a new confession.",
61:"Maria tentatively judges the wounds to be marks from a beating. She introduces herself with the FA name macro and politely asks whether he will tell her why this happened. Preserve the looks-like qualification and voluntary request.",
64:"The man recognizes the FA speaker as belonging to FO and appeals to her as someone who will believe his story. Preserve the recognition and hopeful personal appeal, not narrator confirmation that his whole account is verified.",
68:"He says he worked under Kuhn but felt pangs of conscience over Kuhn's dirty methods and ended up helping the residents. He gives no specific method of helping, job title or military rank.",
71:"He says he was then treated as a traitor and fled Kuhn's service. Preserve the causal connection to helping residents; do not invent a sworn allegiance to Maria or new crew recruitment.",
75:"Speaker0A asks how he received these injuries, skeptically noting that this hardly looks like a roadside robbery during his escape. A highway robbery is not established as fact.",
79:"Maria says the injuries clearly look like professional work and asks whether he knows a secret of Kuhn's. The secret is a question here; no named assassin, weapon or torture technique is supplied.",
82:"The man praises her perceptiveness, admits knowing Kuhn's plan, and says disclosure would put Kuhn in trouble. Do not invent a particular legal penalty or already public exposure.",
85:"Speaker0A reflects on Kuhn having a plan and expects it to be a serious piece of villainy. Preserve the suspicious appraisal as this speaker's judgment.",
88:"Maria invites him to explain the plan and explicitly guarantees his personal safety. Preserve the strength of her spoken promise; it is a character assurance, not verification of an invulnerability or protection mechanic.",
92:"The man thanks her, says he now has no other course than relying on her, and asks whether she knows the Argot company. Keep his predicament and question without inventing a prior friendship.",
96:"Speaker0A recalls a small concern of that name around the North Sea and tentatively recalls its admiral's name as Lil Argot. Preserve the small scale, region and uncertain recollection, not a claim that it is Swedish.",
100:"The man says Kuhn is using the Argot company to stop FO from moving into Southeast Asia. This is the man's report about the scheme; expansion into the region does not by itself mean a military invasion.",
103:"Maria asks what he means and invites the explanation.",
107:"He says Kuhn fed the Argot company false information claiming that FO engaged in dishonest trading. Preserve that the allegation is fabricated in his account; no particular illicit commodity or abuse is named.",
111:"He reports that the Argot company's young female head has a strong sense of justice and was angrily declaring that she would never forgive FO. Preserve the hearsay and reported reaction without inventing a precise age or verified first-hand quotation.",
114:"Speaker0A infers Kuhn's calculation: while FO has its hands full dealing with the Argot company, it cannot make a move into Southeast Asia. Keep this strategic inference; no trade-stat or battle-outcome guarantee is stated.",
125:"Speaker1A gives an angry exclamation condemning Kuhn's conduct. The exact final American phrasing must follow the bound character's voice, without inventing a new accusation.",
132:"Maria calls the plan very risky: if word of it got out, Kuhn could be caught in an attack from both sides. Preserve the conditional danger, not a completed alliance or assured victory.",
136:"The man explains that this is why Kuhn cannot allow those who know the secret to leave alive. If he is found, he expects certainly to be killed or permanently silenced. Preserve the deadly threat without adding graphic methods.",
140:"Maria recalls the Argot company and asks whether its leader has shown any sign of knowing about the plan.",
144:"The man says he cannot tell her that much. Preserve this limit to his information; he does not confirm whether the Argot head knows.",
147:"Speaker0A addresses Maria through FI and says this seems worth investigating. Preserve the familiar name address and prospective investigative conclusion, not immediate combat or a guaranteed reward.",
},
35:{
6:"Speaker01 politely interrupts or asks leave to enter, apologizing for the sudden approach. No rank or relationship is stated in this greeting.",
10:"Maria reacts with a questioning pause and asks who he is.",
15:"Speaker01 identifies himself by the surname Bergstrom and as a member of the Swedish navy, then asks whether she is the lately much-talked-about Admiral FA. Preserve the navy, surname, recent reputation and name macro; do not invent a specific naval rank or full name absent from the body.",
18:"Maria guardedly asks what if she says that she is. Preserve the conditional, challenging response rather than turning it into an enthusiastic introduction.",
22:"Bergstrom says he only wants to see for himself whether she is their enemy. This is a question of possible enmity, not a declaration of war.",
25:"Maria says whether she is his enemy depends entirely on him. Preserve her firm, conditional challenge without inventing an alliance, threat of killing or demand for payment.",
28:"Bergstrom pauses in silence. No acceptance or hostility is spoken.",
32:"Maria turns to a question of her own: he said he was with the Swedish forces, so does he know the Argot company from the same North Sea region? Preserve the source's regional frame without modern geographical correction or making the company Swedish.",
36:"Bergstrom repeats the Argot company's name and cautiously says he is not unfamiliar with it. Preserve the hedged acknowledgment, not a denial that he has ever heard of it.",
40:"Camille apologizes for interrupting and asks what has happened with the Argot company or why it has been mentioned. His interest is evident, but no new prior knowledge is stated yet.",
43:"Maria asks who this other man is.",
47:"Bergstrom introduces him as Camille. Camille is not a member of their fleet but is accompanying them for unspecified reasons. Do not make him a Swedish officer, subordinate or newly hired crewman.",
51:"Camille says he knows the Argot company well and asks whether she would tell him about the matter. Preserve the offered attention and invitation.",
54:"Maria reflects that explaining it may be worth trying. This remains a tentative judgment.",
58:"Maria explains that Kuhn and Pereira control Southeast Asia and that FO and the Argot company seem to have become caught up in their struggle. Preserve Southeast Asia, both powers and the seems-like qualification, not an already resolved war or confirmed current location beyond her statement.",
61:"Camille says it was as he suspected or feared. This reveals a prior suspicion, not proof that he already knew the entire scheme.",
65:"Maria stops him and asks who he really is if he knows about this. Preserve the question and sharpened interest without adding an accusation that he is a spy.",
68:"Bergstrom explains that Camille is a young man belonging to the Argot company and is closely associated with Admiral Argot. They simply happen to be acting separately for now. No romantic, familial, military-rank or permanent-separation claim is made.",
72:"Maria acknowledges this and asks whether Admiral Argot realizes that Kuhn is using her. Keep the question rather than assuming the admiral knowingly cooperates.",
76:"Camille says he thinks she still does not know, then reacts in frustration that his suspicion was right. Preserve thinks/still and the emotional realization.",
79:"Maria observes that Camille does not know the whole story either. Kuhn's plot has brought FO and the Argot company to the brink of a clash. Preserve near-conflict rather than a battle that has already occurred.",
83:"Bergstrom addresses Admiral FA, says he understands that the situation is quite complicated, and asks what she intends to do. Keep the respectful address and practical question without assigning him a new superior rank.",
87:"Maria wants to speak directly with the Argot company's head, without intermediaries. She addresses Camille by name with familiar kun and asks him to guide her. Do not turn kun into a familial or invented age/rank label.",
91:"Camille hesitates to agree to that request, but thinks Lil is staying somewhere around Batavia. Preserve his reluctance, tentative location and approximate area; no exact inn or guaranteed presence is supplied.",
95:"Maria repeats Batavia, decides to go there and thanks him. This is her intended next action, not proof of completed travel.",
98:"Bergstrom asks whether Camille does not want or need to go himself and says it seems a good opportunity. Preserve the gentle invitation without inventing a need to apologize or a reason for their separation.",
101:"Camille apologizes and says that, right now, he really cannot meet her, trailing off. Preserve the emotional reluctance and unstated reason; do not invent a breakup, betrayal or promise to meet later.",
104:"Bergstrom quietly accepts this and allows Camille to do as he wishes. Preserve the acknowledgment and freedom of choice without adding anger, punishment or dismissal from a fleet to which he does not belong.",
},
}
CONTEXT={
34:"A gruff local warns the famous FA visitor about Kuhn/Pereira; Maria asks why either outcome is bad for locals. Foreign national expansion and exploitation prompt a reflective response, silence, a formal country/region report and a tentative protective resolve. Source branch/role selection remains unbound; not every reaction or report is assumed to play in one route through the block.",
108:"After the source completion flag for event34, an injured former Kuhn worker collapses. Alternative startled reactions lead into Maria's treatment-first care, cautious questions and explicit promise of safety. The man's reported secret explains fabricated trading allegations to the justice-minded Argot head, the intended diversion from Southeast Asia, risk of a two-sided response and the lethal effort to suppress disclosure. His information has stated limits, and the exchange ends with investigation rather than confirmed combat or reward.",
35:"After the source completion flag for event108, Bergstrom of the Swedish navy cautiously approaches Maria. Their possible enmity depends on choices, and Maria asks about the Argot company. Camille interrupts, is explicitly an outsider accompanying the fleet, and is then identified as an Argot member close to its admiral. Rumor and partial knowledge lead Maria to seek a direct meeting, with a tentative Batavia lead. Camille's refusal to meet Lil remains personal and unexplained; Bergstrom respects it. No romance, kinship or invented rank is implied.",
}
if __name__=='__main__':
    assert not ROOT.exists();source=read(SOURCE);assert source['current_English_bodies_unread'] and source['all67_source_positions_uncredited'] and source['source_dependency_chain']==[34,108,35]
    groups=[];rows=[]
    for g in source['groups']:
        block=g['block'];assert set(GLOSSES[block])=={r['source_record_index'] for r in g['records']};records=[]
        for r in g['records']:
            row=deepcopy(r);row.update(source_gloss=GLOSSES[block][r['source_record_index']],full_clean_exchange_context=CONTEXT[block],source_gloss_mode='freshly authored from the complete clean Japanese andexplicit source event chain before current English',source_gloss_not_current_English_derived=True,review=dict(source=True,context=False,localization=False,naturalness=False,formatting=False),native_roles_names_macros_branches_andactual_gates_pending=True,new_source_prose_orcompletion_credit=0)
            records.append(row)
        groups.append(dict(block=block,file_path=g['file_path'],clean_block_sha256=g['clean_block_sha256'],source_header_hex=g['source_header_hex'],records=records,whole_exchange_context=CONTEXT[block]));rows.extend(records)
    assert len(rows)==67
    ROOT.mkdir(parents=True);save(ROOT/'all67_clean_whole_exchange_glosses_before_current_English.json',dict(source_ROM=source['source_ROM'],source_ROM_sha256=source['source_ROM_sha256'],clean_ARM9_sha256=source['clean_ARM9_sha256'],file_path=source['file_path'],source_packet=str(SOURCE),source_packet_sha256=sha(SOURCE.read_bytes()),groups=groups,records=rows,source_dependency_chain=[34,108,35],all67_glosses_precede_current_English_exposure=True,fresh_gloss_authoring_not_reused_other_route_English=True,whole_three_exchanges_andemotional_progression_read_before_glossing=True,branch_variants_andadditional_conditions_not_assumed_all_naturally_spoken=True,source_actor_labels_naming_native_getters_andmacro_expansions_unapproved=True,FA_FO_FI_preserved_as_source_macros_not_invented_default_expansions=True,explicit_safety_guarantee_is_Maria_spoken_promise_not_a_mechanic=True,reported_false_trade_allegation_not_asserted_actual_illicit_trade=True,Camille_not_in_Swedish_fleet_close_association_not_invented_romance_kinship=True,NorthSea_EastAsia_SoutheastAsia_Batavia_distinctions_preserved=True,no_specific_current_city_date_commodity_assassin_technique_ornew_game_result_added=True,new_English_manuscript_not_authored=True,current_English_bodies_unread=True,new_source_prose_reviews=0,new_completed_records=0,new_credit=0,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,Path(__file__)]},full_goal_complete=False))
    print('67 fresh source glosses saved before current English:three complete linked exchanges withbranch/name/macro/native/display gates pending.Zero new prose/completion credit.')
