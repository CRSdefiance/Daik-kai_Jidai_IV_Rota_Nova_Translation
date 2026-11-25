"""Read the complete clean funding exchange and record fresh glosses before comparison."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B141_clean_context_v3534')
SOURCE=Path('work/analysis/lil_B141_source_v3532b/all14_clean_current_complete_context.json')
GLOSSES={
15:"Lil apologizes: she still does not have enough money right now. This is the insufficient-funds path,not a refusal to help.",
26:"Camille sympathetically notes that the required amount is one million gold. He does not ask for an additional million or state the remaining balance.",
41:"Fernando says this is not an amount one can save easily;they have to work at earning it. His rough,practical encouragement does not promise instant success.",
47:"The research student understands Lil's willingness or intentions and thanks her. His acceptance leads directly to her insistence that she will do more than offer sympathy.",
50:"Lil says it will not stop at good intentions:she will certainly have the money ready soon. She asks him to trust her and wait. The line is an earnest promise,not already completed funding.",
54:"The student thanks her and says he will refine the plan so he can put it into action as soon as the means are available. Planning/preparation is distinct from completed construction.",
58:"Lil encourages him to do his best and says she will work hard too. Her warm response shares the effort without claiming that he will raise all the money himself.",
63:"On the funded path,Lil confidently tells him to leave it to her;she is not in business for nothing. Her boast reflects competence in trade,not an invented sum earned in a particular deal.",
66:"The student addresses FI politely in astonishment and struggles to find words. Preserve exactly one FI runtime substitution and his moved hesitation;san does not create a rank or family tie.",
69:"The student explains that he went to many places and borrowed money from various people,but raised only one tenth of the total. This is borrowing,not donations,and he has not raised the full million.",
73:"Lil calculates that he is still short900,000 gold and hands over money for him to use. The total million and this remaining900,000 must remain distinct. The native payment/effect contract is a separate verification obligation.",
77:"The student exclaims in surprise and hesitantly asks whether she really is sure she can give him this money. This is not a change to a loan agreement or a demand for more.",
80:"Lil affirms and urges him to work hard and build the polder soon. Keep the named land-reclamation concept from the preceding complete exchange;no completion date or existing completed polder is implied.",
84:"The student thanks her emphatically and asks her to leave it to him. His confident acceptance answers her encouragement;it does not certify a completed construction outcome."}
CONTEXT="The preceding B140 exchange explained the polder proposal,the poor farming village,Lil's personal connection to home and her wish to help struggling people worldwide. This B141 exchange follows that commitment. On the insufficient-money path,Lil apologizes,Camille notes the million-gold total,Fernando offers practical encouragement,the student thanks Lil for her willingness,and she insists she will bring the money soon. He will refine the plan and she encourages him while committing herself to work too. On the funded path,Lil is confidently ready to help. The student is astonished and explains that his borrowing raised only a tenth of the total. Lil supplies the missing900,000;he hesitates over accepting it,she urges him to build the polder,and he accepts responsibility with thanks. The student remains unnamed;do not invent a degree,nationality,rank,family relationship,interest terms or construction outcome. Native predicates,relative branches,effects630A/A000 and C200 still require exact contracts;their meanings must not be inferred solely from nearby prose. Source FI occurs once. The exact B142 copy of the student's surprised address is a navigation lead,not shared whole-event approval."
if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE);assert {r['source_record_index'] for r in packet['records']}==set(GLOSSES)
    ROOT.mkdir(parents=True);rows=[dict(id=r['id'],source_record_index=r['source_record_index'],source_reference=r['source_reference'],source_hex=r['source_hex'],source_Japanese=r['source_Japanese'],source_selector=r['source_selector'],fresh_source_gloss=GLOSSES[r['source_record_index']],whole_exchange_context=CONTEXT,source_read_before_older_English_comparison=True) for r in packet['records']]
    save(ROOT/'all14_complete_clean_context_and_fresh_glosses.json',dict(source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),records=rows,whole_exchange_context=CONTEXT,complete_clean_B141_read=True,preceding_complete_B140_clean_closing_revisited=True,older_English_not_translation_source=True,oldEnglish_comparison_not_yet_done=True,source_prose_review_or_completion_credit_added=0,no_ROM_registry_or_ledger_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('14 complete-exchange clean-source glosses saved before older-English comparison;no review credit.')
