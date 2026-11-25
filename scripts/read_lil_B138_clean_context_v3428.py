"""Record all44 clean glosses before any older-English dialogue comparison."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
SOURCE=Path('work/analysis/lil_remaining_B138_B140_source_v3422/next44_B138_clean_current_context.json')
TRANSCRIPT=Path('work/analysis/lil_B138_clean_transcripts_v3427/complete_clean_transcript_and_branch_tool_provenance.json')
ROOT=Path('work/analysis/lil_B138_clean_context_v3428')
GLOSSES={
11:'Lil asks the barkeep what is wrong. The familiar older-man address is not evidence of kinship.',
23:'In one company-status alternative, the barkeep is alarmed that Nagarpur Company has been absorbed by the company supplied by the exact FO runtime macro. Preserve that substitution and the source statement of absorption, without inventing the absorbing company identity.',
27:'The barkeep says Nagarpur Company apparently ended up as good as ruined. This follows the absorption report, not an independent claim that every form of company absorption is legal dissolution.',
40:'In the other company-status alternative, the barkeep says Nagarpur Company has collapsed and that this has left him in serious trouble. Do not speak both alternative reports as consecutive unconditional statements.',
49:'Lil is puzzled and asks why the company failure is such a problem for the barkeep.',
52:'The barkeep explains that his establishment had effectively depended on the company people eating and drinking there, so sales have plunged. No new patron relationship or ownership is asserted.',
55:'Lil awkwardly acknowledges that this must be hard for him, rather than responding with triumphant delight.',
58:'The barkeep adds that people from Nagarpur Company have left unpaid tabs. These are outstanding customer debts, not evidence that the barkeep owes Nagarpur money.',
69:'Optional Fernando sympathizes with the barkeep having such a run of bad luck. The familiar address does not make the barkeep his father.',
75:'The barkeep says they gave him this object because they had no money, but he cannot make sense of it and does not think it can cover a drinking bill. Keep the object unidentified until the next display and explanation.',
78:'Lil gives a wordless questioning reaction. The source question mark is meaningful, not a placeholder.',
82:'The barkeep points out the displayed object and reports that it is supposed to be a treasure map. He is openly skeptical and finds the situation troublesome. Do not turn the report into confirmed treasure or earned discovery.',
86:'The barkeep asks whether Lil is interested and would buy it from him. His familiar young-woman address does not establish a family tie or romantic interest.',
89:'Lil asks the price.',
93:'After considering it, the barkeep offers a price of exactly 100 gold coins. Preserve the quantity and currency without inferring a different runtime fund unit.',
104:'On the insufficient-funds dialogue path, Lil apologizes that she does not have that much money. This is conditional story dialogue, not a claim about the current test snapshot balance.',
108:'On that path, the barkeep decides to give it to her as thanks for listening to his complaints. Do not also charge her on this free-gift branch.',
111:'Lil apologizes and thanks him for the gift.',
117:'On the purchase alternative, Lil agrees to the offer. Preserve the distinction from the preceding free-gift path.',
121:'The barkeep confirms that they have a deal on the purchase path. Do not claim both the purchase and free gift occur in one exchange.',
130:'On the alternative after the earlier money confrontation, Lil recalls Nagarpur as the outrageous man who thought money could buy anything and says he brought his fate on himself. Preserve her initial harsh judgment before the following reflection.',
134:'Lil then reflects that Nagarpur was a lonely man who could trust only money and is glad she did not become like him. Preserve this softening and self-reflection, not a claim that she was formerly identical to him.',
145:'Optional Ian agrees in his restrained, polite manner that a person is finished once blinded by money. Do not invent a rank, religious office or new backstory.',
151:'Lil asks whether the barkeep has run out of ingredients again today and says she is hungry. The again/today callback belongs to the earlier food shortage.',
163:'Optional Emilio says he is hungry in his plain, casual voice.',
175:'Samwell says the same. His optional reply is nested inside the Emilio-present branch and his own presence check, not a separate unconditional chorus.',
185:'The barkeep laughs and assures Lil that there are ingredients today. He promises to cook with special effort, partly to make up for the earlier disappointment, and asks her to look forward to it. Food is promised, not shown as already eaten.',
188:'Lil hesitates and worries that she may have done the barkeep a disservice. Keep her uncertainty and concern.',
191:'The barkeep asks why she thinks so.',
195:'Lil explains that Nagarpur must have been a good customer for this establishment because he spent so much money. She is reconsidering the impact on the barkeep, not endorsing all Nagarpur behavior.',
207:'Optional Fernando admits that this is one way to look at it. His qualified agreement supports Lil\'s concern without reversing his established opinion of Nagarpur.',
214:'The barkeep acknowledges that Nagarpur paid well but says he himself had lost his human dignity then. His self-reference is the barkeep, not a new person named Uncle.',
217:'He explains that he fawned over Nagarpur for his money and obeyed whatever he said, and now feels ashamed of how he acted. Preserve the self-criticism without invented criminal acts.',
221:'Lil addresses the barkeep with a sympathetic pause. Do not invent a family relationship or a new factual statement.',
225:'The barkeep recalls Lil saying that some things cannot be bought with money and credits those words with opening his eyes. Keep the explicit callback to the earlier confrontation and its moral effect.',
236:'Optional Manuel warmly agrees that those words were a fine saying. Preserve his dignified approval without inventing poetry-note actions absent from this record.',
243:'The barkeep resolves to become a person with dignity like Lil. This is a personal resolve, not a change in employment, status or rank.',
246:'Lil is embarrassed by the praise, then encourages both of them to keep doing their best. Preserve the modest warmth and mutual encouragement without implying romance.',
249:'The barkeep thanks her and changes the subject, asking whether she knows what this object is. Keep the object question after the emotional resolution.',
253:'Lil gives another wordless questioning reaction before the display. It is a meaningful source question mark, not a placeholder.',
257:'The barkeep says a customer left the displayed object in place of payment for drinks, but he has no idea what it is. The customer is not named here; do not invent a new donor identity.',
261:'Lil observes that it is a leaf and wonders what it could be. Preserve her uncertainty rather than supplying a confirmed item identity, medicinal use or treasure location.',
265:'The barkeep offers it to Lil because he has no use for it. Do not invent a purchase price on this alternative.',
268:'Lil thanks him enthusiastically for the offer.',
}
CONTEXT='B138 contains alternatives rather than one unconditional conversation. The native event137 query selects the earlier-company-collapse/map transaction path versus the later reflection on the money confrontation. In the first path, alternative company-status reports describe Nagarpur Company being absorbed by FO Company or collapsing; the barkeep has lost regular trade and is owed tabs. Fernando may sympathize. A skeptical treasure-map report leads to an offer for 100 gold coins, then separate insufficient-funds/free-gift or purchase outcomes. In the other path, Lil initially calls Nagarpur\'s fate deserved, then sees the loneliness of trusting only money; Ian may agree. She asks about food again, with optional Emilio and nested Samwell. The barkeep promises a special meal. Lil worries about depriving him of a wealthy customer; Fernando may qualify her point. The barkeep confesses the loss of his dignity through fawning over money and credits Lil\'s earlier words with changing his outlook; Manuel may praise the saying. Lil is embarrassed, then encourages him warmly. The conversation ends with an unnamed customer\'s object, a leaf that neither fully identifies, offered to Lil. Preserve the movement from judgment to compassion, worry to confession, and gratitude to modest encouragement. The same original item operand appears in two display forms; do not invent two distinct items or erase the source map/leaf descriptions before exact item binding. All 45 relative sites, ten predicates and one query remain structurally significant. No selected B138 gameplay, earned company failure, meal, purchase, free gift, item acquisition or other progression is claimed by these offline readings.'
if __name__=='__main__':
    assert not ROOT.exists();packet,transcript=map(read,[SOURCE,TRANSCRIPT]);assert len(GLOSSES)==44 and set(GLOSSES)=={r['source_record_index'] for r in packet['records']}
    for r in transcript['transcripts']:assert sha(Path(r['path']).read_bytes())==r['sha256']
    rows=[{k:r[k] for k in ['id','file_path','block','source_reference','source_hex','source_Japanese','source_complete_preamble_hex','source_selector']}|dict(fresh_source_gloss=GLOSSES[r['source_record_index']],whole_exchange_context=CONTEXT,localized_English_not_authored=True,older_dialogue_English_not_editorially_compared=True,source_prose_orcompletion_credit_added=0) for r in packet['records']]
    ROOT.mkdir(parents=True);save(ROOT/'all44_complete_clean_context_and_fresh_glosses.json',dict(source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),clean_transcripts=str(TRANSCRIPT),clean_transcripts_sha256=sha(TRANSCRIPT.read_bytes()),complete_exchanges={'138':CONTEXT},records=rows,all44_complete_clean_source_objects_read_before_older_English_comparison=True,all44_fresh_source_glosses_precede_localized_English=True,all111_original_commands45_relative_sites10_predicates_and1_query_considered=True,alternative_map_transaction_and_post_confrontation_reflection_kept_distinct=True,insufficient_funds_gift_and_purchase_paths_kept_distinct=True,source_price_exactly100_gold_coins=True,nested_Emilio_Samwell_replies_preserved=True,wordless_question_marks_are_meaningful_source_reactions=True,map_leaf_and_shared_item_operand_require_exact_term_binding=True,no_new_selected_gameplay_or_earned_progress=True,new_source_prose_reviews=0,new_completed_records=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Complete clean B138 alternatives and44 fresh glosses recorded before older-English comparison. Transaction/reflection,price100,nested reactions and dignity callback preserved;zero review credit.')
