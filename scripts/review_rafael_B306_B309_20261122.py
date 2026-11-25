"""Review Rafael's Istanbul remedy exchange and the route to the hidden village."""

from inspect import getsource

from scripts import pair_rafael_B301_B342_20261122 as paired
from scripts import review_rafael_B221_B224_20261122 as prior
from scripts.source_locked_derivation_v5118 import checked_text


base = paired.parent.base
ROOT, PAIRED = paired.paths(301)
OUTPUT = ROOT / "contextual_decisions_B306_B309_v2.json"
CARRY = ROOT / "earlier_contextual_decisions.json"
DECISIONS = {
    306: """
5|||The boy's cough opens the exchange and prompts the father's response.
9|That cough again... You need to stay in bed to get better.|stay in bed to get better.|The father recognizes the cough and insists on bed rest, with worry behind his firm delivery.
13|||The boy draws out his reluctant answer before coughing again. Keep his youth and the repeated cough.
17|||Rafael asks directly what's wrong instead of speculating about the boy.
22|It's nothing. Telling you won't do any good.|Telling you won't do any good.|The father is reluctant to share something he thinks Rafael cannot help with. Keep the attempt to brush aside the question.
26|||Rafael's wordless confusion gives the father room to tell him the boy is ill.
34|He's sick? What's wrong with him?|What's wrong with him?|Rafael reacts to the illness and asks what makes it serious.
38|||The father says even the doctor has given up and quotes the grim estimate of a few years at best. His anger is at the situation.
42|||Rafael is shocked and can barely answer before the father continues.
47|They say there's a cure-all across the sea, in the East. But what good's a rumor to me?|across the sea,;what good's a rumor to me?|The father repeats the claim about the medicine and says a rumor is no help by itself. Keep the promise of a cure as hearsay.
58|||Rafael volunteers at once to look for the medicine. His short answer contrasts with the father's hopelessness.
63|||The father is taken aback that Rafael would volunteer.
67|The East, right? It has to be in China or somewhere nearby! Wait here. I'll find it, I promise!|China or somewhere nearby!;Wait here.;I'll find it, I promise!|Rafael guesses China or its vicinity and confidently promises to return. Preserve the geography as his guess.
75|||In the path where Rafael already has the remedy, he wonders whether this is the medicine the father means.
79|||The surprised father stammers and asks for confirmation.
82|I don't know if it'll help, though...|if it'll help, though...|Rafael acknowledges that he cannot promise the remedy will work. Keep his caution before the father pleads.
87|||The father is desperate enough to try anything and begs Rafael to give it to his son. The repeated plea matters to his voice.
90|||Rafael agrees promptly after the father's plea.
96|||The father's silent pause marks the wait before they see a response.
100|||Rafael asks the boy how he feels. Keep the quiet opening before the boy replies.
105|||The boy notices a change in his cough before he can say more.
109|Look! His color's already better!|His color's already better!|The father sees the boy's color return immediately. This is his first sign of improvement.
116|No way! Th-that stuff's amazing!|Th-that stuff's amazing!|Claudio responds with blunt disbelief and a stammer. Use the same wording when Rafael returns with the medicine.
127|||Carlo calls the change a wonder of Eastern medicine in the period language of the scene. Keep it as his remark.
134|Th-thank you! You saved my son's life!|You saved my son's life!|The father's halting thanks follow his desperation. The word boy reflects the explicit relationship.
137|Please, you don't owe me anything. I couldn't let a sweet kid like him die.|you don't owe me anything.;a sweet kid like him die.|Rafael gently waves off the gratitude and explains why he had to help. The warmth toward the child remains.
146|||Rafael thanks the father for his offer and tells him to take care. The exchange ends on ordinary courtesy.
""",
    307: """
19|Where on earth can I find that medicine from the East?|medicine from the East?|Away from the guild, Rafael wonders where he can find the rumored medicine. Keep his uncertainty.
25|Hua Tuo's Tonic must be what he meant. I've got to get it to the Istanbul guild right away.|Hua Tuo's Tonic;the Istanbul guild|Rafael thinks the named tonic is the one the father meant and urgently plans to deliver it to the correct guild.
41|||The father is still waiting and asks whether Rafael has any news of the medicine from the East.
""",
    308: """
5|You found it?! Please give it to him right away!|Please give it to him right away!|The father is startled that Rafael found the remedy and urges him to give it to the boy immediately.
8|||Rafael agrees promptly, just as he does if he has the remedy on the first visit.
14|||Keep the pause while the father waits to see how the boy responds.
18|||Rafael asks the boy how he feels, with the same quiet concern as on the other path.
23|||The boy notices his cough. Keep the unfinished thought before the father sees his color returning.
27|Look! His color's already better!|His color's already better!|Match the father's reaction to the same immediate improvement in the other path.
34|No way! Th-that stuff's amazing!|Th-that stuff's amazing!|Claudio is just as stunned by the improvement on the return path. Match his voice and stammer.
45|||Carlo marvels at Eastern medicine as before. Keep this as his reaction in the scene.
52|Th-thank you! You saved my son's life!|You saved my son's life!|Match the father's gratitude and relief when Rafael returns with the medicine.
55|Please, you don't owe me anything. I couldn't let a sweet kid like him die.|you don't owe me anything.;a sweet kid like him die.|Rafael responds with the same humility and concern for the boy as on the immediate-treatment path.
64|||The guildmaster knows a site he thinks Rafael will want to see and personally offers to guide him. This follows his offer to help with local questions.
""",
    309: """
5|||Claudio calls Rafael's attention to the dead-end sign. Preserve the given-name substitution and the distinction between his voice and the sign.
8|Hey, it's you. I hear a rockslide closed the road to the ruins.|closed the road to the ruins.|The guildmaster recognizes the crew and reports that a recent rockslide has closed the road. He relays what he's heard.
11|So we can't get to the ruins?|get to the ruins?|Rafael asks what the closure means for the expedition, before learning there may be another route.
15|||The guildmaster says they probably cannot get there for a while. Keep his qualification.
18|||Rafael wonders how long the guildmaster means and prompts his more discouraging estimate.
23|||The man says nobody goes that far, so the wait could be ten or twenty years. The dates are guesses.
27|||Claudio asks Rafael what they should do and rules out waiting that long. Preserve the original name substitution.
34|||Rafael echoes the cliff proposal in surprise before deciding to try it.
39|||The guildmaster warns that even locals rarely attempt the climb. The warning gives Rafael a chance to reconsider.
42|||Rafael commits to climbing. Preserve the brief, determined answer after the warning.
47|You've made up your mind. I'll do it for you.|You've made up your mind.;I'll do it for you.|The guildmaster recognizes Rafael's determination and agrees as a personal favor. The next line explains the practical plan.
54|||Rafael repeats the unexpected requirement for a map. The next line explains why they need it.
""",
}

source = checked_text(getsource(prior.main), {
    'map(base.load, (paired.PAIRED, paired.parent.RELEASE))': 'map(base.load, (PAIRED, paired.parent.RELEASE))',
    'base.digest(paired.PAIRED)': 'base.digest(PAIRED)',
    'source_packet=str(paired.PAIRED)': 'source_packet=str(PAIRED)',
    '    records = []': '''    carry = base.load(CARRY)
    assert carry["candidate_sha256"] == packet["candidate_sha256"]
    pending = {row["id"] for row in carry["pending_records"]}
    records = []''',
    'zip(group["records"], decisions, strict=True)': 'zip((row for row in group["records"] if row["id"] in pending), decisions, strict=True)',
    'len(records) == 56 and len({row["id"] for row in records}) == 56':
        'len(records) == 53 and {row["id"] for row in records} == pending',
    'for row in records) == 15': 'for row in records) == 0',
    'for row in records) == 5': 'for row in records) == 0',
})
scope = vars(prior) | globals()
exec(compile(source, __file__ + "::contextual-review", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
