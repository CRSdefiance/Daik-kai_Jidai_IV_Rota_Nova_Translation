"""Complete the four contextual comparisons using the existing exact-reference writer."""
import inspect
from scripts import compare_rafael_B36_B37 as first
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.audit_story_glyph_consistency import load

KEEP={
38:{5:'Admiral! Spanish fleet! is a natural urgent lookout report; the source identifies the fleet with certainty here.',
29:'Heh! Let them come! naturally conveys Claudio’s defiant bravado.',
46:'Another fleet sighted! is natural naval reporting and preserves the new sighting.',
60:'Ah?! is the source’s brief surprised recognition, without an invented explanation.',
66:'Janus’s identical Ah?! is an appropriate conditional recognition response.',
77:'Hayreddin!! is Rafael’s exact startled identification.',
82:'Grr! You... Barbarossa!! preserves the Spanish commander’s anger and source-explicit alias.',
85:'Bored? Then play with me. is a natural threatening combat metaphor in this exchange; it does not introduce an unrelated game.',
96:'The existing identity-does-not-matter/prey warning is natural forceful speech and preserves Hayreddin’s general threat to ships crossing his waters.',
106:'...Tch! conveys the commander’s frustrated reaction naturally.',
114:'The existing thanks and full-speed departure orders clearly address Rafael’s own crew and preserve leaving these waters.',},
39:{15:'Hmm. Can you tell? is a natural contextual question about the immediately preceding signal.',
24:'The current Dutch-merchant question and tentative signaling observation are natural Janus dialogue. Keep all words and FI; correct only the full-width Ｉ in It.',
27:'Janus, can you tell? naturally asks the named companion to interpret the signal.',
48:'Brute... is a natural disparaging aside answering Claudio’s eagerness to fight.',
52:'Hm? Say something? is natural casual Claudio speech in response to the muttered insult.',
56:'Oh, you heard? naturally preserves Arcadius’s dry acknowledgment.',
68:'Yeah, yeah, Admiral FI. Got it. preserves Claudio’s exaggerated deference and dismissal without adding a title.',
71:'Well? naturally returns attention to the decoded signal.',
82:'Put in at Amsterdam is clear nautical English and preserves the signal’s destination.',
93:'Hmm... Thoughts? naturally asks the companions for their assessment before the recommendation.',
108:'The current suspicion/ambush/compliance advice is clear and natural; would keeps the ambush hypothetical rather than asserting an actual trap.',
119:'The current small-fleet/breakthrough response naturally conveys Claudio’s confident proposal to force passage.',
123:'The current count-on-you qualification acknowledges Claudio’s fighting usefulness before Rafael chooses caution.',
127:'Let’s be cautious and enter port. is a natural clear final decision and preserves calling at port.',},
40:{5:'You have grown strong. is natural haughty recognition of Rafael’s development.',
13:'The current exceeded-expectations/ready-to-conquer question works as Hayreddin’s clipped, assessing speech.',
26:'...Sure. is natural confident agreement from Rafael; no additional fact or title is needed.',
34:'Huh? is a natural confused reaction to the unexpected dock direction.',
43:'Bring it on! is an idiomatic challenge matching 望むところだ and works better than a literal desire statement.',},
41:{26:'The current Hans/Africa/Proof question naturally conveys Claudio’s impatience while preserving the regional clue.',
29:'No use rushing. is natural concise counsel against impatience.',
33:'The current question directly and naturally asks how to search for a clue.',
40:'By power, you mean a huge fleet? naturally offers one interpretation; the revised preceding paragraph retains power as its shared cue.',
55:'Perhaps wealth. is a natural tentative contribution to the companions’ brainstorming.',
69:'A vast trade sphere? clearly proposes a large trading sphere as another interpretation, without claiming a new mechanical requirement.',
79:'Wow... That’s a daunting task. naturally expresses Rafael’s overwhelmed reaction.',
83:'But power alone isn’t enough. is natural guidance and maintains the shared power term.',
87:'What?! There’s more? is the natural surprised follow-up and already matches the draft.',
98:'Ruins? is a natural questioning echo of the new lead.',
103:'Yes. is a natural affirmative confirmation from Hans.',
107:'Where are the ruins? clearly and naturally asks for their location.',
119:'Locals may know. Earn their trust first. naturally conveys the potential local knowledge and required approach without promising that every resident knows.',
122:'Trust...? preserves Rafael’s puzzled echo naturally.',
134:'Sounds like charity. is natural Claudio commentary on the concrete examples.',
141:'Whew... Becoming a ruler is hard. naturally expresses Rafael’s response to the ambition already established as ruling the seas, without adding a formal title.',
146:'The current laugh and no-one-has-done-it statement naturally close Hans’s explanation and preserve the source’s claim.',},
}
REVISE={
38:{9:'Restore the reported-rumor question rather than presenting pirate cooperation as an established alliance.',
13:'Replace the isolated leading punctuation cluster with Rafael’s natural shocked question about the report’s source.',
17:'Replace Depending on it with a natural answer-dependent threat and preserve hundreds of cannon firing on their weak fleet.',
20:'Correct the reversed bluff: the source says they cannot bluff their way out, not that the enemy’s threat is a bluff they can talk away.',
24:'Replace Bad. At our strength with Rafael naturally worrying that they may not yet be strong enough to win.',
40:'Make Julio’s criticism relate naturally to the mismatch between their actual strength and Claudio’s bravado, rather than narrowing it to skill alone.',
49:'Replace ambiguous Are we done?! with Rafael fearing that they are finished.',
73:'Restore Hayreddin’s first-person challenge instead of the unnatural this pirate self-reference; retain Pedro and the young companions.',
93:'Use the source’s Algiers-based force and natural making-an-enemy wording rather than a modern nationality label.',
110:'Clarify You’re in the way. Go. so Hayreddin’s dismissal of Rafael is distinct from the later Spanish withdrawal.',
119:'Replace Now fight. with Hayreddin’s challenge to begin; the source is not an imperative order directing Rafael to attack.',
123:'Make the withdrawal a natural declaration for this occasion and retain the threat of later consequences.',},
39:{11:'Restore the ship’s possible merchant identity and tentative signaling in the sailor’s natural report.',
19:'Replace Decoding signal! with the sailor undertaking to decode the signal in ordinary speech.',
31:'Use a natural first-person attempt to decode rather than responding to Can you tell? with another awkward proposal question.',
37:'Localize 腕が鳴る by its excited effect; My arms are ready! is an unnatural literal idiom.',
63:'Replace pick fights worldwide with Rafael naturally addressing their own voyage and Claudio’s behavior.',
87:'Make Janus’s decoding result conversational while preserving the tentative reading, Amsterdam and request for a decision.',
103:'Replace the literal once with the tentative suggestion to call at Amsterdam and investigate.',
112:'Use good head for strategy for Rafael’s natural internal reaction; preserve Arcadius by name without adding a gender inference.',},
40:{9:'Keep the stammered recognition and remove the detached leading exclamation cluster from ordinary English prose.',
17:'Restore Rafael’s first-person uncertainty rather than the report-like Outcome uncertain fragment.',
22:'Keep the powerful Ottoman Pasha force but replace the filler-like You know? with Hayreddin’s serious check that Rafael understands.',
31:'Preserve a deliberative pause in natural word order while giving the exact Algiers dock direction; do not invent the offered assistance.',
39:'Replace the compressed Next battle, no mercy with Hayreddin’s natural first-person warning about their next battle.',
48:'Give Hayreddin’s approving reaction idiomatic English and retain the expression on Rafael’s face rather than the missing-article Good look in your eyes.',},
41:{37:'Restore a complete explanation of power worthy of the ambition and the Proof not revealing itself; no Proof is an unnatural checklist fragment.',
43:'Use accomplished seafarer for 航海者として一人前: avoid confusing general voyaging competence with the narrower sailor crew class or navigator duty.',
75:'Restore that people interpret power differently before Hans suggests that all interpretations may matter.',
92:'Make the explicit personal-theory hedge conversational; it qualifies the following ruins guidance rather than an omniscient instruction.',
95:'Preserve the likelihood of the Proofs’ secrets being sealed in worldwide ruins in natural speech, rather than the weaker abbreviated may lie formulation.',
112:'Restore in or near cities, not only near, and Hans’s conjectural tone. This changes a practical search instruction.',
116:'Make Claudio’s complaint about inadequate directions natural spoken English rather than a detached fragment.',
127:'Retain the sound faith/culture sentence, then make the outsiders/location explanation active and natural while preserving that the voyagers themselves are outsiders.',
131:'Restore actual help with requests and the condition that merchants or military people are making residents suffer; avoid a blanket instruction to punish them.',
137:'Express the need for character that earns many people’s trust naturally in the ruling-the-seas context, rather than a formal qualification checklist.',},
}


def normalized_current(row):
    text=first.normalized_current(row)
    if row['id']=='DK4_MES_B39_R0024':
        assert text=="Admiral {MACRO:FI}, is that a Dutch merchant ship over there? Ｉt looks like they're trying to tell us something."
        text=text.replace('Ｉ','I')
    return text


if __name__=='__main__':
    current=load(first.CURRENT)
    decisions={}
    for group in current['groups']:
        b=group['block']
        if b not in KEEP:continue
        assert set(KEEP[b]).isdisjoint(REVISE[b])
        assert set(KEEP[b])|set(REVISE[b])=={r['source_reference']['record_index'] for r in group['records']}
        decisions[b]=[('K | '+KEEP[b][r['source_reference']['record_index']]) if r['source_reference']['record_index'] in KEEP[b]
            else ('R | '+REVISE[b][r['source_reference']['record_index']]) for r in group['records']]
    source=checked_text(inspect.getsource(first.previous.save_comparison_part),{
        "['FI', 'FA', 'FO']":"['FI', 'FA', 'FO', 'FU']",
        'current_ROM_English_conversation_comparison_pending=False, current_reference_pending=False,':
            'current_ROM_English_conversation_comparison_pending=False, current_reference_pending=False,current_English_comparison_pending=False,earlier_English_unconsulted=False,current_English_now_exposed=True,',
        '            rows.append(row)':
            """            if row['id']=='DK4_MES_B39_R0024':
                assert code=='K' and 'Ｉ' not in row['english']
                row['wording_retention_with_scoped_glyph_fix']=True
                row['glyph_finding']=dict(current='Ｉ',proposed='I',kind='unintended-fullwidth-Latin',complete_native_font_andpagination_checks_pending=True)
            rows.append(row)""",
    })
    env={**first.previous.save_comparison_part.__globals__,'ROOT':first.ROOT,'CURRENT':first.CURRENT,'DRAFTS':first.DRAFTS,
        'OBJECTS':first.OBJECTS,'normalized_current':normalized_current}
    exec(compile(source,__file__+'::same-complete-comparison-distinct-FU-and-bound-I-correction','exec'),env)
    env['save_comparison_part']('B38_B41_83',decisions,{
        'DK4_MES_B40_R0031':"I see... Then stop by the dock in Algiers.",
        'DK4_MES_B40_R0048':"Ha ha ha! I like that look on your face!",
        'DK4_MES_B41_R0037':"First and foremost, you need power worthy of someone who would rule the seas. Without it, the Proof will never reveal itself to you.",
        'DK4_MES_B41_R0043':"Or... becoming an accomplished seafarer?",
        'DK4_MES_B41_R0127':"Ruins and old churches embody their faith and culture. They won't readily share their locations with outsiders like us.",
        'DK4_MES_B41_R0131':"Do favors for the townspeople. Help them when they're in trouble. If corrupt merchants or soldiers are making them suffer, teach them a lesson...",
    },__file__)
    saved=load(first.ROOT/'B38_B41_83_whole_exchange_comparison_v1.json')
    assert (saved['compared'],saved['proposed_revisions'],saved['justified_retentions'])==(83,36,47)
