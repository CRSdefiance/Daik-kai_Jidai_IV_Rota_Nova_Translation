"""Draft the opening audience in B166 from clean Japanese through the king's summons."""
from pathlib import Path
import inspect

from scripts import seal_clean_independent_drafts_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

CONTEXT={166:"Rafael returns to Portugal with the seven Proofs. Claudio asks to wait outside and jokes about a reward. At the audience the King praises Rafael, relays the reported diplomatic opportunity, appoints him viceroy over the overseas Estado and calls him out to the crowd. Optional companions respond in their own voices. The segment ends with Rafael's silence before the scene resumes outside. The appointment is offered here. Its later acceptance or refusal is not inferred from this audience alone."}
DATA={166:{
    6:("Janus announces they are back in Portugal and addresses Rafael.","Well, FI, we're back in Portugal!"),
    9:("The guard formally addresses Rafael by surname and says the King is waiting.","FA. His Majesty is expecting you."),
    20:("Cesare is stunned they will appear before the King and gets extremely nervous.","We're to appear before the King?! I-I'm getting terribly nervous!"),
    27:("Claudio quietly asks Rafael for a moment.","...FI. Can I talk to you for a second?"),
    30:("Rafael answers using Claudio's familiar nickname.","What is it, Clau?"),
    35:("Claudio dislikes the atmosphere of the court and asks if he can wait outside.","I've never been good in places like that... Mind if I wait outside?"),
    39:("Rafael would like Claudio beside him on this important occasion but accepts his reason.","This is a big moment. I'd like you there with me, Clau, but... Well, if that's how you feel, it's all right."),
    44:("Claudio agrees and asks Rafael to tell him what happened.","All right, then. Come tell me how it goes."),
    48:("Rafael agrees and promises to come back when the audience ends.","I will. I'll come back as soon as it's over."),
    52:("Claudio jokingly tells him to make sure he gets a reward.","And make sure you come back with a reward!"),
    55:("Rafael excuses himself to go in.","Well, here I go."),
    60:("Claudio casually says he will see him later.","Yeah. See you later."),
    64:("Janus prompts the party to proceed.","Shall we go in, then?"),
    69:("The King welcomes Rafael back as the pride of Portugal, using his surname.","Ah, FA, pride of Portugal! You've returned!"),
    72:("Rafael gives his full name and formally announces his return to his homeland.","I, FU, have returned to my homeland, Portugal."),
    85:("The King says he has heard that showing the Pope Rafael's seven collected Proofs will prompt him to press for renewed recognition of Portuguese royal authority.","I hear that if we show the Pope the seven Proofs of Conquest you've gathered, he'll press for the authority of the Portuguese Crown to be recognized again."),
    88:("Rafael responds with astonished confirmation.","Is that true?!"),
    96:("The King confirms it and calls Rafael a treasure of their seafaring country.","Indeed. You're a treasure to our seafaring nation!"),
    100:("In the name of the King of Portugal, the King appoints Rafael viceroy over all the overseas trading spheres Portugal holds, the Estado.","In the name of the King of Portugal, I appoint you viceroy over all our overseas trading spheres, the Estado!"),
    103:("Rafael is stunned and stammers the title in a respectful question.","What?! V-viceroy, Your Majesty?"),
    107:("Janus privately tells Rafael how impressive it is.","(Look at you, FI!)"),
    118:("Yifa is delighted and repeats her amazement at the viceroy title.","(Viceroy! That's amazing! Just amazing!)"),
    132:("Fernando privately claims a position like that is only to be expected.","(Heh. A position like that is only to be expected.)"),
    146:("Emilio doesn't understand what it means but thinks it sounds delicious.","(I don't get it, but it sounds delicious.)"),
    152:("The King says he will make a grand announcement now and urges Rafael to step outside the palace and show himself to the crowd in the square.","Now we'll announce it for all to hear. Step outside the palace and show yourself to the people in the square. Come, come!"),
    155:("Rafael responds with silence before the scene leaves the audience.","…"),
}}

source=checked_text(inspect.getsource(previous.seal),{
    "        b=group['block'];assert {int(r['id'].split('_R')[-1]) for r in group['records']}==set(data[b])":
        """        b=group['block']
        full=group['records']
        selected=[r for r in full if r['source_reference']['record_index'] in data[b]]
        assert len(full)==136 and len(selected)==26 and selected==full[:26]
        assert selected[-1]['source_reference']['record_index']==155
        assert full[26]['source_reference']['record_index']==170
        assert {r['source_reference']['record_index'] for r in selected}==set(data[b])""",
    "        for source in group['records']:":"        for source in selected:",
    "complete_blocks=list(data),source_contexts=contexts":"complete_blocks=[],source_contexts=contexts,complete_exchange_scope='B166 opening audience R0006–R0155',remaining_same_block_records=110",
    "across{len(data)} completeblocks":"for the complete opening B166 audience",
})
env={**previous.seal.__globals__}
exec(compile(source,__file__+'::exact-clean-exchange-prefix-through-audience-end','exec'),env)

if __name__=='__main__':
    env['seal']('work/analysis/Rafael_B161_B180_clean_20261105','B166_opening_audience_clean_drafts_v1.json',DATA,CONTEXT,{},__file__,26)
