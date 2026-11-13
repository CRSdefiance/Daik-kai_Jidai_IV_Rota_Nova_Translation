"""Read the complete clean bargaining exchange before predecessor English prose."""
import struct
from copy import deepcopy
from collections import Counter
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B196_clean_context_v5589')
SOURCE=Path('work/analysis/lil_B196_clean_inventory_v5588/all_clean_B196_speeches_before_predecessor_comparison.json')
GLOSSES={
 5:('You look as though you have money. Hee hee hee!','AD/173 sizes up the prospective customer and laughs theatrically. This is the speaker assessment,not a narrator-certified wealth,funds or eligibility statement. Bind the actual original role,voice and relationship before choosing an English name or gender.'),
 8:('...','02/2 gives an ellipsis-only response. Preserve the silent beat and original actor;do not add an agreement,question,emotion or spoken line.'),
 12:('I will sell you something nice. How about200000 in money? Hee hee hee!','The initial asking price is explicitly200000. The item is unnamed and described as good by the seller. Bind the approved money/unit terminology and source transaction controls;do not infer a specific item,effect,quality guarantee or affordable funds.'),
 24:('Hey,now. You are not inflating the price,are you?','14/20 challenges possible overcharging in a rough familiar register. Preserve the skeptical question,not proven fraud or narrator-certified fair value. Conditional advice must retain its actual selection condition.'),
 42:('You are generous. Still,this is sure to be useful.','AD praises the buyer as a big spender after the initial buy path and claims future usefulness. Preserve the seller claim and conversational turn without inventing a named item,mechanic or objective benefit.'),
 45:('FI:Charm increased by1!','FE system notice contains one source FI macro and explicitly魅力 plus one. Bind the actual stat label,FI referent and native effect/dispatch. This notice is one branch,not a promised outcome for every discounted purchase.'),
 62:('All right. How about100000 in money? Hee hee hee!','The second asking price is100000,half the first. Preserve the explicit number and cackle without claiming that money was already paid or the purchase accepted.'),
 74:('(Admiral,if a single attempt brought the price down by half,that means the original price was greatly inflated. You can haggle at least two more times.)','13/19 gives aside-style bargaining advice with explicit提督 address. Preserve one attempt,half-price inference and at least two more rounds as the character reasoning/advice. No FI is embedded in this line. Parentheses mark an aside,not proof of telepathy or a new relationship.'),
 92:('Hee hee hee! Impressive. This will surely come in handy.','AD compliments the bargain and promises usefulness on this purchase branch. Do not turn speaker confidence into narrator-certified item power or invent item identity.'),
 107:('Then how about70000 in money? Hee hee hee!','The next asking price is70000. Keep the exact price step and seller laugh;do not flatten the six separately selectable buying points into one transaction.'),
 118:('(If it were me,I would try haggling one more time.)','14/20 offers a conditional first-person opinion in a casual register. Preserve one further attempt and the hypothetical,not an unconditional command or guaranteed discount.'),
 136:('Here,it is yours. It is sure to come in handy. Hee hee hee!','AD hands over the unnamed item on this purchase branch and repeats a personal usefulness claim. Do not add a name,stat effect,origin,rarity or specific utility.'),
 152:('You are surprisingly greedy. How about50000 in money? Hee hee!','AD gives a backhanded reaction to persistent bargaining and offers50000. Preserve the chiding tone and exact price without adding a new insult,kinship,rank or objective greed assessment.'),
 170:('(If it were me,I would hold out one more time.)','06/6 gives a personal hypothetical in the originalわし/ぞい register. Bind actual character/voice before rendering speech style;preserve one further attempt without inventing age,kinship or a guaranteed outcome.'),
 178:('(Let us get the price down some more!)','19/25 gives an energetic,informal inclusive suggestion to bargain further. Preserve the enthusiasm and aside,without inventing a financial partnership or a new relationship.'),
 197:('You really know how to do business. Here is the item. There you go.','AD compliments the buyer bargaining skill and hands over the unnamed item on this purchase branch. Do not translateやり手 as a new occupation,rank or professional credential.'),
 212:('40000 in money......... Heh.','AD offers40000 with a long hesitation and shortened laugh. Preserve the weakening bargaining performance and pacing;do not invent an illness,threat,secret or hidden payment.'),
 223:('(I suppose this is about the right point to buy.)','13/19 tentatively judges the current buying point. Preserveここら andかね uncertainty;do not turn the opinion into a narrator guarantee that40000 is the absolute minimum.'),
 242:('I thought you were never going to buy it. Here,it is yours.','AD reacts to acceptance with relief/exasperation and hands over the item. Preserve the connection to prolonged bargaining,not a new prior history or repeated completed purchase.'),
 257:('Please,buy it.30000 in money will do.','AD pleads for acceptance and offers30000. Preserve the marked reversal from confident initial salesmanship to pleading,with no invented debt,need,deadline or external danger.'),
 268:('(I doubt the price will go any lower.)','06/6 gives a tentative judgment of the floor withじゃろう. Retain the original voice and personal uncertainty;native pricing/purchase mechanics need independent control checks.'),
 287:('Tch,I sold it far too cheaply. Well,take good care of it.','AD complains after this discounted sale and asks the buyer to look after the item. This branch explicitly speaks of a completed sale. Keep the seller regret without asserting objective fair value or changing unnamed item identity.'),
 302:('Hmph! Apparently there was poor judgment.','AD makes an angry,elliptical見る目がなかった remark after the continued refusal path. Japanese omits whose judgment and its object;read the opening appraisal and final dismissal together before resolving the English. Do not assume the customer lacks funds or cannot recognize item quality,or assign seller/buyer fault as certain without contextual justification.'),
 306:('Never mind! I will sell it to someone else!','AD dismisses the current negotiation and intends to sell to another person. Preserve future intention and frustrated ending;no second customer is present and no other sale is completed in the dialogue.'),
}

if __name__=='__main__':
    assert not ROOT.exists();d=read(SOURCE);b=bytes.fromhex(d['clean_block_hex']);commands=d['commands']
    end=8+struct.unpack_from('<H',b,4)[0]
    assert d['read_no_predecessor_English'] and len(d['records'])==24 and len(commands)==119
    assert len(b)==1816 and end==1814 and b[end:]==bytes(2)
    assert set(GLOSSES)=={r['source_record_index'] for r in d['records']}
    choices=d['typed_choice_or_actor_style_commands']
    assert len(choices)==6 and {r['word'] for r in choices}=={0x2100}
    assert [r['offset'] for r in choices]==[218,582,832,1156,1370,1588]
    choices=deepcopy(choices)
    for r in choices:
        raw=bytes.fromhex(r['whole_command_hex']);labels=[v.decode('cp932') for v in raw[6:].split(b'\0') if v]
        assert labels==['買う','買わない']
        r.update(source_labels=labels,fresh_glosses=['Buy','Do not buy'],literal_labels_do_not_say_haggle=True,
            branch_results_funds_item_effects_and_fallbacks_not_yet_bound=True)
    assert sum(bytes.fromhex(r['source_hex']).count(b'FI') for r in d['records'])==1
    assert not any(m in bytes.fromhex(r['source_hex']) for r in d['records'] for m in [b'FA',b'FO'])
    rows=[]
    for original in d['records']:
        row=deepcopy(original);row.update(zip(['fresh_source_gloss','whole_exchange_note'],GLOSSES[row['source_record_index']]));rows.append(row)
    counts=Counter(format(c['word'],'04X') for c in commands)
    ROOT.mkdir(parents=True)
    save(ROOT/'all24_clean_exchange_six_choices_and_fresh_glosses.json',dict(source=str(SOURCE),source_sha256=sha(SOURCE.read_bytes()),
        file_path='/data/SC2.DK4',block=196,records=rows,choices=choices,physical_speech_objects=24,physical_choice_objects=6,choice_labels=12,
        source_commands=119,source_command_counts=dict(counts),source_stored_bytes=1816,source_logical_end=1814,source_alignment_tailzeros=2,
        source_selectors_hex=['AD','02','14','FE','13','06','19'],source_selectors_decimal=[173,2,20,254,19,6,25],
        source_FI_macros=1,source_FA_macros=0,source_FO_macros=0,
        source_asking_price_ladder=[200000,100000,70000,50000,40000,30000],
        complete_exchange_progression='AD appraises the buyer as wealthy and cackles;02 remains silent;AD offers an unnamed item for200000;conditional14 challenges the high asking price. Six successive Buy/Do-not-buy choices accompany offers200000/100000/70000/50000/40000/30000. Conditional13 explains the first halving and advises at least two more attempts;14 advises one more attempt;06 or19 can urge further bargaining;13 tentatively favors the40000 buying point;06 doubts the30000 price will drop further. Each buy path has its own seller reaction/handing-over text;the first has a separate FI Charm-plus-one notice. Continued refusal yields an angry elliptical judgment remark and future intention to sell elsewhere.',
        source_fact_boundaries=[
            'Bind all seven source selectors,original names/voices,complete preambles,one FE and one FI macro before authoring. The source explicitly addresses Admiral in13 advice;do not invent kinship,rank,age,gender,employment or relationships elsewhere.',
            'Preserve six literal Buy/Do-not-buy choices and six exact asking prices. Bargaining progression,affordability,debits,item ownership,effects,prior results and fallback paths require original control/predicate/caller binding;do not infer them from price prose.',
            'The item is unnamed in these speeches. Keep seller usefulness claims as character claims. Do not invent item identity,rarity,origin,a recipe,a commodity or an objective stat effect for every discounted purchase.',
            'Keep cackling salesmanship,skepticism,aside-style personal advice,backhanded praise/chiding,shortening laugh/hesitation,pleading,post-sale regret and final frustrated dismissal as a whole emotional progression.',
            'Preserve one-try halving,at-least-two-more advice,one-further-attempt opinions and tentative buying-floor assessments without narrator certification.',
            'R302 poor-judgment subject/object are elliptical;justify any chosen interpretation from the entire clean exchange rather than copied English. R306 is future intent to sell to another person,not a completed other sale.',
            'Source1816 stored/1814 logical bytes has two tailzeros and119 commands. Keep every nested conditional,relative operand,six typed choices,effect/UI leaf and every source end. Do not inherit B195 linear shape or claim a single tail end.'
        ],read_no_predecessor_English=True,new_review_credit=0,new_emulator_runs=0,
        source_native_terms_predecessor_comparison_localization_formatting_actual_and_release_gates_pending=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('B196:24 clean-only speech glosses,six choices/12 labels,six exact prices,119 commands. Native actors/control/effect mapping pending;no English comparison or credit.')
