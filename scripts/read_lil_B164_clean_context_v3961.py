"""Record all49 clean-first meanings before exposing predecessor English."""
from copy import deepcopy
from pathlib import Path
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B164_clean_context_v3961')
SOURCE=Path('work/analysis/lil_B164_source_v3960/all49_clean_current_complete_context_with_typed_choice.json')
CONTEXT='''Lil and Camille are explicitly in Alexandria. Lil marvels at its size and the apparently endless African land. The newcomer pedantically takes her figurative end-of-the-world remark literally and announces that Earth is round. She knows this and objects to his interruption, not to that fact. Camille is impressed by his claimed world travel and knowledge and invites him despite Lil's protests. Camille explicitly introduces Lil as their admiral. His suggestion that world travel implies sailing experience and useful shipboard skills remains his inference. Lil reluctantly but explicitly hires the newcomer, who gives his full name. Bind source actor13 to the existing native name before authoring; do not invent a profession, credential, military rank, nationality or relationship. The newcomer's repetitive formal de arimasu gives him a fussy, pedantic comic voice, contrasting with Lil's exasperated informality and Camille's curious, welcoming mediation.
Recruitment precedes the optional advice. The two choices concern hearing the new recruit's opinion about choosing ships, not accepting or refusing his employment. Declining elicits exaggerated praise of the admiral's independent principles, then his departure preparations. Listening elicits practical ship-purchasing advice, followed by the same preparations. Preserve both complete outcomes and the original choice and branch controls. Source0D is an actor selector requiring current original-consumer proof, not a carriage return to strip. This scoped proof cannot close the older-record0D technical audit.
The advice moves from contract towns and small market shares to increased purchasing power, affordable cargo capacity, medium ships, refitting and sailing distance, combat preparation and eventual regional fleets. Preserve every numerical threshold and comparison, the distinction between cargo and supply storage, sail-handling crew and marines, and qualified combat advice. Literal percentages must use percent in English. No extra currency, ship class, cargo unit, map rule or economic fact is supplied. Actual branch selection, display geometry, nameplate, transitions, recruitment effects and natural eligibility need their own evidence; extraction and isolated native calls do not establish them. The wider editorial goal remains open.'''
MEANINGS={
5:'Lil identifies this as Alexandria and casually remarks that it is quite a large city.',
8:'Camille reasons that Africa is vast, so it probably has many large cities. Preserve his tentative inference.',
11:'Lil agrees and says it feels as if the land stretches to the end of the world. Preserve the figurative phrase that prompts the interruption.',
15:'The newcomer abruptly declares, in emphatic formal language, that she is wrong. Preserve the intrusive correction.',
18:'Camille startles and asks who has suddenly interrupted.',
22:'Lil angrily demands who the stranger is and whether he is picking a fight. This is a verbal challenge, not an actual assault.',
25:'The newcomer insists she is wrong because she is wrong, states that there is no end of the Earth because it is round, and calls this common knowledge by now. Preserve the pedantic circular insistence.',
28:'Lil agrees with the fact but asks whether he was actually listening to their conversation. She was speaking figuratively.',
31:'The newcomer defensively says he merely corrected an error. Preserve his self-justification as speech.',
34:'Lil exasperatedly says she cannot make sense of this person.',
38:'Camille wonders whether this means the newcomer has a great deal of knowledge.',
42:'The newcomer affirms that he has traveled the world and acquired varied knowledge. These are his claims, not independently certified facts.',
46:'Camille is impressed and calls him studious. Do not invent a formal scholarly profession or credential.',
50:'Lil asks why Camille is impressed when the stranger abruptly picked a fight with her.',
54:'Camille excuses the interruption as bad timing and asks whether knowledge gained from world travel would be useful.',
58:'Lil begins a suspicious, unfinished warning that Camille cannot possibly be about to do what she fears.',
62:'Camille invites the newcomer to come with them.',
66:'The newcomer reacts with startled surprise to the invitation.',
70:'Lil says she knew it and asks Camille to wait. Preserve her interrupted protest.',
74:'Camille explains that they sail aboard a ship and that Lil is its admiral. Preserve the explicit title without adding a new rank.',
77:'The newcomer excitedly praises the news, addresses the admiral and formally begs to sail aboard with them.',
80:'Lil complains to Camille about what she is supposed to do now. Keep her drawn-out exasperation without inventing a new threat.',
83:'Camille infers that world travel means sailing experience and tentatively suggests the man can probably do shipboard work. Preserve this as Camille\'s reasoning, not a proven resume.',
86:'The newcomer formally begs the admiral to agree.',
89:'Lil sighs that this sounds tiring but gives in and explicitly agrees to hire him. This precedes the advice choice.',
92:'The newcomer formally thanks her and gives his full name, Chezaare Tooni in source phonetics. Bind the existing actor13 full-name spelling before authoring.',
95:'Camille greets Cesare courteously and offers to show him around the ship. Use the approved source-owned name spelling after binding.',
98:'Lil sighs that another strange person has joined them. Preserve her personal complaint, not a narrator diagnosis.',
103:'The newcomer remembers something, addresses the admiral and asks her to hear his opinion about choosing ships. This introduces an optional advice choice after hiring.',
121:'On declining advice, he says he underestimated her, praises her own principles and calls that wonderful. This is exaggerated deference, not a reversal of recruitment or his earlier Earth claim.',
125:'He says he will now begin preparations to depart and bids farewell. This concludes the no-advice branch.',
136:'On accepting advice, he clears his throat and begins his explanation.',
140:'While merely increasing contracted towns and expanding routes, there is no need to buy ships: a one percent contract allows only one to five units of trade goods. Preserve all quantities and the limited stage of expansion.',
143:'Once market share increases enough to buy many trade goods, it is time to buy a ship.',
147:'The first considerations are the ship\'s size and price.',
150:'Choose a ship suited to market share and available funds; otherwise there will not be enough goods to fill it, while it will require more sailors. Preserve the paired economic and crew consequences.',
153:'Price indicates size: under5000 is small,10000 through20000 is medium, and over50000 is large. Preserve strict under/over and the stated medium range; do not fill unstated gaps.',
156:'Small ships are very cheap, so they can readily increase fleet cargo capacity even when funds are limited.',
159:'After trading for a while and building up funds, replace them with medium ships.',
163:'Medium ships have two or three masts. Three masts are faster but require more sail-handling crew. Preserve both quantities and the tradeoff.',
166:'Refitting can provide the maximum five cargo holds. If avoiding combat for the time being, marine quarters and gun batteries are unnecessary. Bind approved room terminology without losing the conditional advice.',
169:'Increasing supply storage permits long voyages to open routes to distant towns. Distinguish supplies from trade cargo.',
173:'If confronting another power, large ships will be needed. Preserve the change from trading to combat preparation.',
177:'At least the flagship needs marine quarters and armed gun batteries, or winning naval battles will be difficult. Preserve at least and the qualified difficulty; do not make victory impossible or require every ship to be equipped.',
180:'The remaining decision depends on available funds: two medium ships are cheaper and carry more trade goods than one large ship. Preserve both comparative benefits and counts.',
183:'Eventually they will upgrade to large ships, but if they plan to form regional fleets later, keeping the old medium ships instead of selling them is an option. Bind the approved fleet term.',
186:'He concludes his opinion, says he will now begin departure preparations, and bids farewell. This concludes the advice branch.'
}
if __name__=='__main__':
    assert not ROOT.exists();v=read(SOURCE);rows=deepcopy(v['records']);choices=deepcopy(v['typed_choice_records']);assert len(rows)==len(MEANINGS)==47 and {r['source_record_index'] for r in rows}==set(MEANINGS)
    for r in rows:r.update(fresh_source_gloss=MEANINGS[r['source_record_index']],whole_exchange_context=CONTEXT,clean_source_complete_exchange_read_before_older_English=True)
    for r in choices:r.update(fresh_source_gloss=('Listen to his advice about choosing ships.' if r['option_index']==0 else 'Do not listen to his advice about choosing ships.'),whole_exchange_context=CONTEXT,clean_source_complete_exchange_read_before_older_English=True)
    ROOT.mkdir(parents=True);save(ROOT/'all49_complete_B164_exchange_and_fresh_glosses.json',dict(source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),whole_exchange_context=CONTEXT,records=rows,typed_choice_records=choices,all49_clean_first_glosses_before_predecessor_English=True,source_macro_counts=v['source_macro_counts'],numerical_facts={'contract_percent':1,'goods_min':1,'goods_max':5,'small_price_strictly_under':5000,'medium_price_inclusive_range':[10000,20000],'large_price_strictly_over':50000,'medium_mast_counts':[2,3],'maximum_cargo_holds':5,'medium_vs_large_ship_counts':[2,1],'minimum_combat_preparation_scope':'at least flagship'},source_actor13_name_voice_presentation_binding_pending=True,choice_outcome_binding_and_menu_geometry_pending=True,source_controls_native_actual_and_registered_release_pending=True,source_prose_orcompletion_credit_added=0,new_emulator_runs=0,no_ROM_registry_ledger_change=True,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,Path(v['source_transcript']),Path(__file__)]},full_goal_complete=False));print('49 clean-first glosses recorded;predecessor English still unexposed;no credit.')
