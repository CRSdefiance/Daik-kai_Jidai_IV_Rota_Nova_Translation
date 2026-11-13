"""Read the complete cheese-specialty exchange from clean Japanese before old English."""
import struct
from copy import deepcopy
from pathlib import Path
from scripts.verify_village_wrap_v608 import read, save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/lil_B195_clean_context_v5540')
SOURCE=Path('work/analysis/lil_B195_clean_inventory_v5539/all_clean_B195_speeches_before_predecessor_comparison.json')
GLOSSES={
    6:('Huh? Do you smell something good?','Selector77/119 notices an appealing smell and asks the companion. Bind actual role/voice;do not identify the dish,venue,origin or a relationship from the question.'),
    9:('Sniff,sniff... Yes,I do.','Selector67/103 sniffs and agrees. Preserve the sensory action and conversational acknowledgment without a smell-quality guarantee or invented intoxication.'),
    13:('Hey,old man,what is that smell?','119 addresses selector5C/92 familiarly with親父 and asks the source of the aroma. This is not proof of fatherhood,age,kinship,employment or an actual personal name. Bind speaker/relationship before choosing natural address.'),
    17:('This? It is our house specialty. It has plenty of cheese and tastes great!','92 identifies an establishment specialty and claims it is tasty with abundant cheese. Preserve house specialty and the cheese ingredient. No dish name,pizza,recipe,cuisine,origin,price or nutritional claim is supplied.'),
    20:('Is it really that good?','103 challenges the taste claim with a skeptical question. Preserve the teasing exchange and speaker progression,not an independent narrator certification.'),
    24:('Do not ask a question with such an obvious answer.','92 responds with confident humorous indignation. Preserve the retort rather than making it a factual taste test or a new insult/relationship.'),
    28:('Then bring us one too.','119 orders one for the pair/group with俺たちにも１つ. Preserve the explicit one and shared order without inventing two servings,a price,a payment or completed eating.'),
    32:('All right,all right. Just wait a moment. I will bring it right over.','92 acknowledges the order,requests a short wait and promises prompt service. Preserve the brisk friendly rhythm and future serving intention.'),
    35:('Here you are. Sorry to keep you waiting.','Conventionalはい、お待ちどう marks the dish arriving. Natural service phrasing need not invent a long delay or an apology implying a failure. Read with the following surprise at speed.'),
    39:('Oh,that really was fast.','119 reacts to the actual prompt arrival. Preserve the good-humored surprise;no exact elapsed time or speed mechanic is stated.'),
    43:('Well,just humor me and try it first.','92 usesだまされたと思って as a coaxing idiom:give it a try/take my word for it. Preserve the joke and encouragement without inventing actual deception,fraud,danger or a taste guarantee.'),
    46:('All right.','119 agrees to try the food. Keep this short acceptance as part of the complete sensory progression.'),
    50:('Munch,munch.','119 chewing sound. Preserve the playful eating beat with natural American game-dialogue onomatopoeia or a justified action form;do not add spoken taste judgment early.'),
    54:('Munch,munch.','103 also chews. Keep the separate speaker/action beat rather than dropping the repeated response or merging the two actors.'),
    58:('So delicious!','119 bursts into emphatic praise with stretchedうっめぇーーー. Preserve energy and comic payoff after the chewing,without a new superlative,recipe,health effect or narrator fact.'),
    62:('This is really good! Amazing!','103 joins the enthusiastic praise. The register is casual and emphatic;bind actual voice rather than assigning a new rank,age or identity.'),
    65:('See? I told you!','92 confidently seeks agreement after the enthusiastic reactions. Preserve the satisfied payoff and connection to the earlier skeptical question.'),
    69:('We have to tell everyone about this!','119 wants to spread the word. This is future social intention,not already completed advertising,actual demand,profit or an earned trade event.'),
    73:('Yeah! Old man,this dish is definitely going to become hugely popular!','103 predicts strong popularity for the dish,addressing92 with親父. The certainty belongs to this character. Do not infer actual fatherhood or convert it into a narrator guarantee of price,demand or reward.'),
    77:('Cheese may become popular in ヴェラクルス.','Separate prospective FE. Bind approvedチーズ andヴェラクルス commodity/city names. Do not invent the unnamed dish,earlier scene location,earned fashion,shortage,price rise or guaranteed profit.'),
}

if __name__=='__main__':
    assert not ROOT.exists();d=read(SOURCE);b=bytes.fromhex(d['clean_block_hex'])
    assert d['read_no_predecessor_English'] and len(d['records'])==20 and len(d['commands'])==23
    end=8+struct.unpack_from('<H',b,4)[0]
    assert len(b)==712 and end==710 and b[end:]==bytes(2)
    assert [(c['offset'],c['word'],c['whole_command_hex']) for c in d['commands'] if c['word']!=0x4000]==[
        (8,0xA000,'00a0ffff010841a1'),(704,0xC200,'00c2'),(706,0,'00000000')]
    assert not d['typed_choice_or_actor_style_commands']
    assert set(GLOSSES)=={r['source_record_index'] for r in d['records']}
    assert not any(m in bytes.fromhex(r['source_hex']) for r in d['records'] for m in [b'FI',b'FA',b'FO'])
    rows=[]
    for original in d['records']:
        row=deepcopy(original);row.update(zip(['fresh_source_gloss','whole_exchange_note'],GLOSSES[row['source_record_index']]));rows.append(row)
    ROOT.mkdir(parents=True)
    save(ROOT/'all20_clean_exchange_and_fresh_glosses.json',dict(source=str(SOURCE),source_sha256=sha(SOURCE.read_bytes()),
        file_path='/data/SC2.DK4',block=195,records=rows,physical_speech_objects=20,source_commands=23,
        source_stored_bytes=712,source_logical_end=710,source_alignment_tailzeros=2,
        source_selectors_hex=['77','67','5C','FE'],source_selectors_decimal=[119,103,92,254],
        source_FI_macros=0,source_FA_macros=0,source_FO_macros=0,
        complete_exchange_progression='119 notices an appealing smell;103 sniffs and agrees;119 asks92 about it;92 identifies a cheese-rich house specialty;103 is skeptical;92 retorts;119 orders one for them;92 promises prompt service and brings it;119 praises the speed;92 urges a try;119 agrees;both chew and then exclaim praise;92 responds with satisfaction;119 wants to tell everyone;103 predicts popularity for the dish;a separate prospective cheese/Veracruz notice follows.',
        source_fact_boundaries=[
            'Bind119/103/92 complete preambles,original names/voices and actual relationship before authoring.親父 is familiar address,not proof of fatherhood or kinship.',
            'The source identifies only a house specialty with plenty of cheese. Do not invent pizza,a dish name,recipe,cuisine,origin,price or health effect.',
            'Preserve the full teasing/skepticism/confident retort,one shared order,prompt service,coaxing idiom,two separate chewing beats and enthusiastic taste payoff.',
            'だまされたと思って invites a trial;it does not establish actual deception,fraud or dangerous food.',
            'Taste praise and dish-popularity certainty belong to the characters. Spreading the word remains intention;FE commodity fashion is prospective.',
            'Bind approvedチーズ andヴェラクルス names without claiming earlier scene location,earned fashion,shortage,price rise,profit or a reward.',
            'Keep23 linear commands/20 full speech preambles,A0008 raw00a0ffff010841a1,C200704,end706,source712 stored/710 logical with2 tailzeros. No macro,predicate,relative branch,pause or typed choice is present. Packed A000 semantics remain unbound.',
        ],read_no_predecessor_English=True,new_review_credit=0,new_emulator_runs=0,
        source_native_terms_predecessor_comparison_localization_formatting_actual_and_release_gates_pending=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('B195:20 clean-only whole-exchange glosses,23 linear commands,one shared order,two chewing beats,prospective cheese/Veracruz notice. No old English or credit.')
