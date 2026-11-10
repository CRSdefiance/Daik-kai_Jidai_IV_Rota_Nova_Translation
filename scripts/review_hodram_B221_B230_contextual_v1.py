"""Record individual whole-exchange comparisons for nine complete later exchanges."""
from copy import deepcopy
from pathlib import Path
import re
from scripts.audit_story_glyph_consistency import load,save
from scripts.consolidate_hodram_B211_B230_clean_drafts_v1 import OUT as DRAFTS
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Hodram_B211_B230_resume_20261106')
CURRENT=ROOT/'current_v1/current_effective.json'
OBJECTS=ROOT/'current_objects_v1/current_objects.json'
OUT=Path('translations/hodram_B211_B230_contextual_review_v1.json')

# K retains the effective paragraph exactly; R uses the sealed draft unless a
# complete-exchange refinement is stated explicitly below.
DECISIONS={
221:{
5:('R','Restore Ian hearing the lead in town and a complete conversational opening.'),
8:('K','The concise name question fits Hodram\'s restrained curiosity and naturally answers the report.'),
11:('R','Restore the twelve Olympian gods and align Holy Spear of Ares with the bound item name.'),
14:('R','Restore Ares as god of war while making the location question conversational.'),
18:('K','The reported nearby armor remains unnamed and uncertain; the prior line supplies the Olympian context.'),
21:('K','The complete, dry correction suits Hodram after Ian evades the location question.'),
24:('R','Replace this man with I and preserve the local inference and Ian\'s personal desire.'),
28:('R','Express surprised recognition of Ian\'s interest rather than the broader implication that he rarely cares.'),
32:('R','Replace this man with a natural personal question and keep Ian reacting to Hodram\'s expression.'),
36:('K','Yes is the candid, deliberately blunt answer to Ian\'s question.'),
40:('R','Restore Ian\'s personal feeling and his unexpectedly romantic voice across the paired speeches.'),
43:('R','Restore weapons the gods may have used rather than treating their ownership as certain.'),
46:('K','The quiet Ah is a natural acknowledgment that lets Ian\'s unusual enthusiasm stand.'),
},
223:{
5:('R','Remove third-person self-reference and restore a warm greeting before Julian\'s extravagant flattery.'),
8:('R','Make Lucia\'s recognition of his smooth talking sound like a familiar spoken reply.'),
12:('K','The short puzzled sound is natural and motivates Lucia\'s next question.'),
16:('K','Something on my face is a natural spoken ellipsis, with the full preceding question intact.'),
19:('K','The tentative resemblance to the legendary empress preserves Julian\'s fanciful comparison without claiming identity.'),
23:('K','The direct question naturally challenges the unexplained comparison.'),
27:('R','Restore the casual apology and hearing the lead; use the bound Empress Gown name.'),
31:('R','Align the echoed item title with Empress Gown rather than retain a conflicting catalogue spelling.'),
35:('R','Restore the beautiful empress and hearsay; remove the unsupported causal claim that tyranny brought her death.'),
39:('K','The expressive conjecture, glance imagery and pointed comparison already convey Julian\'s flirtation naturally.'),
42:('R','Replace this woman with I and preserve Lucia\'s objection to the insulting implication.'),
46:('R','Repair the awkward attachment of about as much as you have while keeping the teasing reassurance.'),
50:('R','Keep the protective-gown fantasy but replace the stiff Do you not agree with a natural short question.'),
53:('R','Make Lucia\'s practical counterproposal conversational while preserving rings and necklaces.'),
57:('R','Retain the price interpretation and practical-women joke but make Julian\'s sudden exit sound spoken.'),
61:('K','See you is a natural reply and lets Lucia\'s private complaint close the scene.'),
65:('R','Remove this woman and restore about to ask, rather than claiming that she already made the gift request.'),
},
224:{
5:('R','Replace the incomplete without hearing phrase with a forceful, natural shopkeeper\'s call.'),
8:('R','Make Hodram\'s question about what is special here idiomatic in this square encounter.'),
12:('K','Do you know of the Crusades is a natural knowledge question; Yes and No fit both original branches.'),
28:('R','Preserve soldiers valuing chivalry without implying an added noble rank or turning the whole army into knights.'),
34:('R','Preserve the dismissive opening and the European account as a report of soldiers valuing chivalry.'),
40:('K','The forceful convenient-lie accusation is clear, natural and remains the resident\'s claim.'),
43:('K','The truth is a natural questioning echo inviting the counteraccount.'),
47:('R','Restore Al\'s heard report and confirmation question instead of presenting his allegation as unqualified fact.'),
50:('R','Use a spoken angry protest and restore the resident\'s identification with our Saladin.'),
53:('K','The direct request for Saladin\'s identity correctly prompts Al\'s explanation.'),
57:('R','Restore the name enduring in Islamic history and make Al\'s respectful explanation natural.'),
61:('R','Keep every humane-conduct example and express the rejection of underhanded methods in natural speech.'),
64:('K','A true hero, then naturally states Hodram\'s conclusion from the preceding appraisal.'),
68:('R','Replace Word says and the stiff imperative with remembered hearsay and a conditional invitation.'),
},
225:{
5:('K','The native ellipsis is a deliberate source silence before the sunset conversation, not mixed-width Latin.'),
9:('R','Restore contemplation without narrowing it to being troubled; address Gerhard naturally.'),
12:('R','Remove this man and restore Gerhard\'s personal surprise at being moved by the story.'),
16:('K','Whose tale is a concise, appropriately formal question about the person in the story.'),
20:('K','The complete introduction preserves Noritsune, his warrior identity and the centuries-old period.'),
23:('K','The deed question is natural and preserves Hodram\'s curiosity about the distant past.'),
27:('K','The once-mighty clan, repeated defeats and threatened destruction form a clear spoken account.'),
30:('K','The formal kin diction suits Gerhard\'s martial story and preserves his disparaging comparison.'),
33:('R','Restore reported leaping toward the enemy commander\'s ship, not merely crossing toward a foe.'),
37:('R','Restore one enemy soldier under each arm and the complete strait-and-armor image without adding a capture event.'),
40:('R','Keep Gerhard\'s period viewpoint and reference to the East rather than replacing it with a claim about only Japan\'s people.'),
44:('K','The fearsome death and recognition of a true warrior already fit Hodram\'s restrained formal voice.'),
47:('K','Exactly is a natural emphatic agreement with the warrior appraisal.'),
51:('K','The direct acknowledgment of Gerhard\'s feeling follows the emotion he already disclosed.'),
54:('R','Restore the splendid armor in Hodram\'s echo of the submerged-treasure clue.'),
57:('R','Replace this man with I while keeping Gerhard\'s self-check and inclusive return-to-work question.'),
},
226:{
28:('R','Restore Ian personally finding an interesting book at an antique shop, not a book appearing at an unspecified shop.'),
31:('R','Restore the declining imperial line and make the complete book description natural, preserving period and extent.'),
34:('R','Attribute the claim to the book and preserve chipped sword and spear blades rather than a vague turned edge.'),
37:('K','The burial, decades-later theft and other grave goods are all present in a natural formal letter sentence.'),
40:('R','Retain the existing plural reading permitted by the unnumbered Japanese, while restoring exhaustion and the almost-visible sea.'),
44:('R','Restore the reported uncertainty about the long-unknown fate and use a complete natural account of the still-missing chainmail.'),
48:('R','Correct the mismatched full-width I in Ian and make the signed invitation natural without authored alignment.'),
56:('R','Correct the full-width I in Ian and preserve Hodram\'s surprise about his interest in Asian history.'),
67:('R','Restore the Russian people rather than a later state and preserve Cesare\'s probable explanation of Ian\'s interest.'),
70:('K','Hm is Hodram\'s brief interested acknowledgment after the explanation; it needs no expansion.'),
},
227:{
5:('R','Make the greeting and compliment sound like Julian speaking directly to Safia.'),
8:('K','The warm, simple welcome is already natural and complete.'),
11:('K','The deliberate native ellipsis is the source silent look prompting Safia\'s question.'),
15:('K','The spoken ellipsis Something on my face is natural and matches the surrounding exchange.'),
18:('R','Remove this man and the stiff petrification phrasing while retaining the eyes-and-stone simile.'),
22:('R','Restore a request to explain what he is talking about rather than an ambiguous What is this.'),
26:('R','Restore a natural personal recollection, keep the reported Tasman Sea location and align Medusa Shield.'),
29:('R','Preserve Safia\'s questioning identification and objection in direct, natural speech.'),
32:('R','Remove the invented instruction Hide your hair; the source says he would not even need her to uncover it.'),
35:('K','Always joking is a natural familiar rebuke after his extravagant reassurance.'),
39:('K','The deliberate dreamlike fragment preserves stone, eternal nearness and moonlight and suits Julian\'s romantic fantasy.'),
43:('R','Remove this woman and restore her conditional refusal to look after him rather than an assertion of ignoring him.'),
46:('R','Preserve the flattery through the rebuff and give Julian a natural spoken exit.'),
50:('K','The brief farewell is natural and leaves the private admission separate.'),
54:('R','Replace the unnatural this heart circumlocution and restore a little as the degree of her private excitement.'),
},
228:{
5:('K','The theatrical proclamation and religious epithet fit the boy\'s hero-play; naming his pretend identity is not the generic this man defect.'),
9:('R','Replace this man yields with a natural playful surrender and restore the retreat stammer.'),
12:('K','The simple observation question is natural and complete.'),
16:('K','Gerhard\'s formal champions phrasing naturally explains the children\'s admiration in this hero-play context.'),
20:('R','Repair the broken What name phrase and preserve the local hero and Hodram\'s incomplete recollection.'),
23:('R','Restore more than eight hundred years rather than flattening the period to exactly eight centuries.'),
26:('R','Restore between Tours and Poitiers and the Iberian Peninsula rather than narrowing the source geography to Spain.'),
29:('K','The concise objection to victory alone justifying hero status is natural in Hodram\'s reserved voice.'),
33:('R','Replace the incomplete Why fragment with Gerhard\'s statement about the victory\'s significance.'),
37:('R','Preserve Gerhard\'s emphatic historical counterfactual as his viewpoint; do not silently weaken or modernize it.'),
41:('K','The paired reflection clearly presents Hodram\'s inference about the children\'s game and Europe\'s defender.'),
45:('K','Gerhard\'s formal praise is natural and preserves the explicit comparison with Charles Martel.'),
49:('R','Remove this man and restore looking forward to Hodram\'s future reputation, not merely wondering about it.'),
},
229:{
5:('K','The concise respectful greeting is complete; the extra greeting in the independent draft is unnecessary.'),
8:('K','Manuel is Hodram\'s natural familiar recognition.'),
12:('R','Use the trading context\'s trends and restore a natural acknowledgment of Hodram\'s work.'),
15:('R','Replace the stilted respite fragment with a conversational explanation of taking a break.'),
18:('K','True works as a brief acknowledgment of Hodram\'s explanation in this exchange.'),
22:('K','The elliptical question is a natural direct inquiry from Gerhard to Manuel.'),
25:('R','Restore the Admiral as the comparison: Gerhard asked this question, so the same as you addresses the wrong participant.'),
28:('R','Ask whether Hodram has heard of the historical figure, preserving the explicit king title without implying personal acquaintance.'),
32:('K','The familiar-name reply is natural and preserves limited recognition.'),
36:('R','Restore the reported account and both Roman Empires, replacing the vague pressured Rome phrasing.'),
40:('K','Gerhard\'s compact inference about Attila\'s stature is natural and remains military admiration rather than moral endorsement.'),
44:('R','Complete the clipped maxim and make impermanence of political power unambiguous, retaining the empire-and-stronger-foe contrast.'),
47:('K','The terse Harsh and vigilance question suit Hodram\'s dry acknowledgment and preserve the application to their own position.'),
50:('R','Use a natural spoken formulation of effort determining outcomes.'),
53:('K','The concise question naturally returns to why Manuel raised Attila.'),
57:('R','Restore Manuel just hearing the lead nearby while retaining its explicit rumor limitation.'),
61:('R','Restore the questioning echo Armor; Mail invents a specific armor type and loses the question.'),
65:('K','The death, unknown bearer, northwest direction and reported status are all clear and natural.'),
69:('K','Gerhard\'s formal reflection preserves the northwest armor clue and fear inspired by a threat to Rome.'),
73:('R','Restore the tentative northern-Europe inference rather than declaring it a confirmed location.'),
},
230:{
5:('R','Keep nonverbal exertion calls instead of adding the spoken challenge Take this.'),
9:('R','Restore direct address to Yifa rather than switching to her, while retaining the marine comparison.'),
13:('R','Restore the sword specifically and Yifa\'s conversational voice instead of an abstract formal maxim.'),
16:('R','Make the condition and possible worse injury explicit, preserving the explanation rather than sounding like an instruction to fear a blade.'),
19:('R','Restore martial arts clothing rather than a specific robe and make the reported equipment lead conversational.'),
22:('R','Preserve the surprised question about the sword being chipped in natural English.'),
25:('R','Replace this woman with I and preserve the temptation to fight wholeheartedly.'),
28:('R','Restore the self-check and a natural reference to her teacher before the quoted lesson.'),
32:('R','Restore her energetic return to training and the two exertion calls.'),
}}

OVERRIDES={
    'DK4_MES_B224_R0028':'Hmph. As soldiers who valued chivalry and fought to reclaim the Holy Land, right?',
    'DK4_MES_B224_R0034':"Hmph. Apparently, in Europe they talk about soldiers who valued chivalry and fought to reclaim the Holy Land...",
    'DK4_MES_B226_R0040':'The thieves fled into the scorching desert to evade pursuit, but their strength finally gave out, and they died with the sea almost in sight.',
    'DK4_MES_B229_R0044':'However mighty an empire may be, a stronger foe will eventually appear. No power lasts forever, I suppose.',
    'SC1_B224_CHOICE_138_0':'Yes',
}

def main():
    assert not OUT.exists()
    draft=load(DRAFTS);drafts={r['id']:r for r in draft['records']}
    current,objects=map(load,(CURRENT,OBJECTS))
    assert current['current_ROM_sha256']==objects['current_ROM_sha256']
    by_id={r['id']:r for g in current['groups'] for r in g['records']}
    by_id.update({r['id']:r for r in objects['style_records']+objects['choice_records']})
    decisions={f'DK4_MES_B{b}_R{n:04d}':v for b,rows in DECISIONS.items() for n,v in rows.items()}
    for r in objects['style_records']:
        if r['block']==226:
            indices=r['source_style_indices']
            note='Correct full-width I in Ian and preserve '+{
                0:'the conversational arrival report.',1:'the formal correspondence register.',
                2:'the shared casual arrival report and both aliases.',3:'the gentle delivery without the awkward Mr. Ian address.',
                4:'the clipped familiar report.',5:'the older familiar report without forced archaism.',
                6:'the simple excited letter announcement.'}[indices[0]]
            decisions[r['id']]=('R',note)
    decisions['SC1_B224_CHOICE_138_0']=('R','Yes naturally answers the retained Do you know of the Crusades question; Know it can read as a command.')
    decisions['SC1_B224_CHOICE_138_1']=('K','No naturally answers the retained knowledge question; there is no need to replace it with a response to a different question.')
    expected={r['id'] for r in draft['records'] if 221<=r['block']<=230}
    assert len(expected)==136 and set(decisions)==expected
    rows=[]
    for original in draft['records']:
        if original['id'] not in decisions:continue
        cur=by_id[original['id']];code,finding=decisions[original['id']]
        assert all(original[k]==cur[k] for k in ['source_reference','source_hex','source_Japanese'])
        paragraph=cur['current_comparison_paragraph']
        english=paragraph if code=='K' else OVERRIDES.get(original['id'],original['english'])
        assert (english==paragraph)==(code=='K'),original['id']
        assert english==english.strip() and not any(t in english for t in ['\n','{LB','{ALIGN','{PAD}','  '])
        english.encode('cp932')
        row=deepcopy(original)
        row.update({k:v for k,v in cur.items() if k.startswith('current_') or k=='selected_native_pointer'})
        row.update(english=english,logical_English=english,decision='retention' if code=='K' else 'revision',
            finding=finding,retention_reason=finding if code=='K' else '',
            localization_note=finding+' '+original['localization_note'],
            source_current_conversation_comparison_complete=True,current_reference_pending=False,
            current_ROM_English_conversation_comparison_pending=False,
            source_context_localization_formatting_gates_pending=True,
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
            independent_clean_draft_reference=dict(path=str(DRAFTS),sha256=digest(DRAFTS),id=original['id']),
            new_credit=0)
        rows.append(row)
    counts={word:sum(r['decision']==word for r in rows) for word in ['revision','retention']}
    glyphs=[r['id'] for r in rows if re.search('[\uff21-\uff3a\uff41-\uff5a]',r['current_comparison_paragraph'])]
    assert len(glyphs)==9 and all(not re.search('[\uff21-\uff3a\uff41-\uff5a]',r['english']) for r in rows)
    save(OUT,dict(format='dk4-editorial-prose-packet-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        encoder='dialogue-relocatable-v1',review_gates=['source','context','localization','naturalness','formatting'],
        file_path='/data/SC1.DK4',records=rows,records_count=136,counts=counts,
        complete_exchange_blocks=[221,223,224,225,226,227,228,229,230],control_only_block222_not_prose=True,
        remaining_contextual_comparisons=141,all277_source_drafts_preserved=True,
        full_width_Latin_I_findings=glyphs,fresh_formatting_andvisual_checks_pending=True,
        no_new_native_display_gameplay_orrelease_credit=True,new_credit=0,guide_photos=False,
        evidence={str(p):digest(p) for p in (DRAFTS,CURRENT,OBJECTS,Path(__file__))}))
    print('Saved 136 contextual comparisons:',counts,'; nine mixed-font I defects identified. 141 comparisons and display remain.')

if __name__=='__main__':main()
