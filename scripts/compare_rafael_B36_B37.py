"""Retain working dialogue and document specific source, voice and glyph corrections."""
import inspect,re
from pathlib import Path
from scripts import save_hodram_B171_B190_comparisons as previous
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/Rafael_early_story_B36_B41_B51_B60_clean_20261104')
CURRENT=Path('work/analysis/Rafael_B36_B41_current_20261104/current_effective.json')
DRAFTS=ROOT/'B36_B41_all175_sealed_drafts_v1.json'
OBJECTS=ROOT/'no_compound_text_for_comparison_v1.json'

KEEP={
36:{
16:'What fleet is that? is a natural identifying question and preserves Janus’s uncertainty.',
23:'Pirates? is Claudio’s exact, natural speculative question.',
54:'The existing explanation clearly preserves both the North African base and raids near Algiers; Julio’s explanatory register works.',
66:'Pirates! naturally conveys Janus’s alarmed confirmation after the preceding identification.',
77:'And... yes! Barbarossa Hayreddin! preserves recognition and the complete source-explicit name.',
89:'Seriously?! is a natural startled Claudio response to the force’s reputation.',
101:'The current trade/Gibraltar sentence preserves the immediate strategic obstacle; here clearly refers to the Mediterranean in this exchange.',
113:'A hard road ahead. works as Janus’s dry assessment after the regional warning; a full paraphrase is unnecessary.',
120:'Right now, we must survive this encounter. naturally redirects attention from future trade to the immediate danger.',
123:'Survive how? directly echoes Julio’s wording and naturally asks for a practical plan.',
},
37:{
13:'The current question naturally asks Admiral FI for a decision and preserves the given-name substitution.',
33:'The familiar unfinished enemy-of-my-enemy idiom naturally conveys Rafael’s hopeful shared-enemy reasoning before Claudio objects.',
38:'You’re too trusting. They’re pirates! is natural Claudio skepticism and preserves the reason for his objection.',
50:'This is bad... is a natural uneasy Janus reaction in the complete encounter.',
74:'How do we escape? clearly expresses Janus’s practical concern after discovery.',
84:'Stand tall...? All right. Ahem. naturally echoes Julio’s advice; the preceding revision keeps stand tall as the shared cue.',
94:'The shouted company name FO! completes Rafael’s preceding grand introduction without unnecessary expansion.',
99:'And I’m Admiral FU! is natural, source-faithful declaration wording and preserves the full-name macro. Retain its words while correcting only the inherited full-width Ｉ to ASCII I.',
103:'Oh! Splendid. preserves Julio’s impressed approval in an appropriate older voice.',
107:'Hear, hear! (applause) naturally conveys the crew’s supportive cheers and the source-explicit clapping.',
115:'No good... We’re dead... naturally captures Rafael’s frightened belief that his attempt has failed.',
123:'The current defeat-Spain question is a natural sharp echo from Hayreddin and preserves his sudden interest.',
126:'Y-yes. conveys Rafael’s hesitant confirmation without extra explanation.',
135:'W-what’s funny?! naturally preserves Claudio’s shaky indignation.',
139:'...Watch your tongue. is an idiomatic threat matching Hayreddin’s warning.',
157:'Tch. All right. FI, good luck. naturally shows Claudio’s reluctant compliance and encouragement.',
160:'All or nothing... Let’s try. works as Rafael’s terse resolve to gamble on his bluff.',
167:'Exactly! preserves Rafael’s quick affirmative bluff before Hayreddin points out his weakness.',
175:'Right! Now is not the time! naturally conveys Rafael seizing on that warning as a way out.',
180:'What?! is Salid’s direct indignant reaction.',
184:'Hahaha. Then when? is a natural teasing challenge to Rafael’s not-now claim.',
187:'The current experience/training sentence preserves both preparation and the goal of facing Hayreddin as equals; its pause suits Rafael’s declaration.',
200:'What?! naturally conveys Salid’s anger at being called cowardly.',
212:'You... called yourself FI? naturally recalls Rafael’s given name and preserves the unsettling pause.',
216:'Amusing. Very amusing, boy! retains Hayreddin’s patronizing delight; boy is supported by the source’s youngster address.',
219:'Sir!! is natural subordinate protest to an admiral without adding a new title.',
233:'Huh? Uh... naturally captures Salid’s embarrassed hesitation.',
236:'No matter. Such games amuse me. is natural haughty dismissal and preserves Hayreddin’s entertainment motive.',
239:'Yes. Understood. is natural submission to the order.',
242:'The current passage/trade contrast clearly permits Mediterranean transit while requiring trade elsewhere; both conditions survive.',
246:'W-what? naturally captures Rafael’s dismayed surprise at the trading restriction.',
262:'W-what? works as the nervous response when Hayreddin adds another point.',
271:'Really?! is a natural astonished response to the offer of help.',
279:'T-thank you!! preserves Rafael’s grateful, flustered response.',
288:'O-of course! naturally conveys immediate, nervous agreement to the territorial warning.',
293:'Hmph. Perhaps you... preserves the unfinished thought without inventing what Hayreddin has in mind.',
297:'The current dismissal, demand for greater strength and reminder to keep the promise are natural and preserve all three beats.',
306:'Good. Everyone, withdraw. is a natural command for his own crew to leave.',
309:'Aye! naturally answers the pirate captain’s withdrawal order.',
314:'That bluff worked! Not bad, FI! naturally praises the effective bluff in Claudio’s casual voice.',
338:'The current strong-under-pressure observation is idiomatic and preserves Claudio’s affectionate assessment.',
341:'Splendid. is natural, succinct Julio praise; no added familiar address is needed.',
},
}
REVISE={
36:{
5:'Restore looks like enemy ships; Hostile ships! removes the lookout’s source-explicit uncertainty.',
27:'Replace become trouble with Rafael’s natural worried hope about what the sighting means.',
39:'Restore the conditional if they are pirates and make the unavoidable fight sound conversational.',
46:'Use the source’s Algiers-based force rather than the modern-nationality implication of Algerian pirates.',
49:'Replace the inconsistent Alger pirates label with Algiers pirates, matching Julio’s identification.',
73:'Replace a trial already, which sounds like a literal test or court proceeding, with Claudio’s natural complaint about immediate trouble.',
80:'Restore Rafael’s spoken question about Hayreddin instead of the unnatural isolated Strong? after a name.',
85:'Replace ambiguous family with Hayreddin’s men and restore their superiority over the other Algiers pirates; no biological relationship is invented.',
93:'Restore the explicit Mediterranean scope, current strength and hearsay qualification in a natural complete explanation.',
97:'Clarify Claudio’s entrance/far-end Mediterranean image rather than leaving deep inside without its geographical referent.',
},
37:{
19:'Restore the reported bad relationship with the Algiers pirates; hate is stronger than the source and Algerian adds an unnecessary nationality label.',
24:'Restore chiefly targeting Spanish ships and identify Valdes as royal-navy commander in Julio’s spoken explanation.',
28:'Restore the recent reports and Spanish pressure rather than asserting the compressed Spain makes trade hard as an unqualified fact.',
57:'Restore southern Mediterranean; my waters prematurely substitutes a possession claim for the source’s actual geographical challenge.',
62:'Replace the clipped Damn, spotted! with Claudio’s natural reaction to their discovery.',
81:'Restore Julio’s hearsay and conditional risk. Cowards become prey turns advice into a categorical claim; keep stand tall to support the retained echo.',
89:'Restore sailing the world and under the banner of; the current under slogan fragment is unnatural in the grand introduction.',
111:'Express Salid’s threat to kill them rather than introducing a distinct imperative order to the crew.',
119:'Correct spoken Salih to the native-bound Salid identity; the Japanese サリド and current nameplate refer to the same man.',
131:'Use the Spanish Armada reference consistently and preserve the mocking rhetorical challenge without adding grand as a substitute for the named force.',
151:'Make Janus’s intervention and encouragement conversational; render 総帥 as the group’s leader rather than adding a capitalized Commander title.',
164:'Restore the conditional taunt naturally; dare to face us is a compressed imperative rather than Salid’s rhetorical challenge.',
172:'Replace at your strength, that would be fatal with Hayreddin’s natural warning about attempting it in their present condition.',
192:'Restore the fool/softhearted implication and use Salid’s brash speech rather than the abstract calmly watch another rise above them.',
195:'Use Algiers pirates and restore the provocation that the pirates fear being unable to beat them once they grow stronger.',
204:'Keep the request for free travel through these waters and consistently name the Spanish Armada.',
209:'Restore the warning against pushing his luck rather than substituting the broader hierarchical Know your place.',
223:'Restore both exploration and trade and strength worthy of Rafael’s words; Explore and grow strong omits a named way of developing.',
226:'Replace invented Lord with source-explicit Admiral Hayreddin.',
230:'Replace literal this chick with fledglings; American chick can suggest a woman and misrepresent the source’s inexperienced youngsters.',
251:'Restore the rhetorical warning about angering two great powers and less leniency than Hayreddin, rather than the categorical show no mercy.',
254:'Turn the compressed checklist into Hayreddin’s natural warning about making their name elsewhere before seeking Mediterranean rule.',
258:'Restore a natural thinking transition and one more thing; Yes... One more. is awkward and sounds like a quantity request.',
267:'Preserve the conditional Spanish attack and explicit restriction to Hayreddin’s own waters rather than leaving the territorial limit merely implicit.',
276:'Remove invented pirate king and preserve only the source’s lack of guarantee and busy schedule.',
284:'Use the crew’s territory rather than a biological family implication; preserve a challenge answered without mercy instead of inventing a separate declaration of war.',
301:'Replace Understood. A promise. with Rafael’s natural commitment, You have my word.',
326:'Restore Janus’s conversational praise for securing the promise instead of the detached noun fragment An amazing promise.',
333:'Replace Now fear sets in with Rafael speaking naturally about his own delayed fear.',
345:'Use Rafael’s natural resolution to work hard after his bold claims; avoid the stiff after saying that, we must grow strong.',
},
}


def normalized_current(row):
    text=previous.normalized_current(row)
    text=re.sub(r'(?<![A-Za-z])FU(?![A-Za-z])','{MACRO:FU}',text)
    if row['id']=='DK4_MES_B37_R0099':
        assert text=="And Ｉ'm Admiral {MACRO:FU}!"
        text=text.replace('Ｉ','I')
    return text


if __name__=='__main__':
    assert not OBJECTS.exists()
    source_packet=ROOT/'B36_B41_selected_source_packet_v1.json'
    packet=load(source_packet)
    assert not any(c['word'] in [0x2000,0x2100,0x2200,0x4100] for g in packet['groups'] for c in g['all_source_commands'])
    save(OBJECTS,dict(choice_records=[],source=str(source_packet),source_sha256=sha(source_packet.read_bytes()),no_compound_commands=True,new_credit=0))
    current=load(CURRENT)
    decisions={}
    for group in current['groups']:
        block=group['block']
        if block not in KEEP:continue
        assert set(KEEP[block]).isdisjoint(REVISE[block])
        assert set(KEEP[block])|set(REVISE[block])=={r['source_reference']['record_index'] for r in group['records']}
        decisions[block]=[('K | '+KEEP[block][r['source_reference']['record_index']]) if r['source_reference']['record_index'] in KEEP[block]
            else ('R | '+REVISE[block][r['source_reference']['record_index']]) for r in group['records']]
    source=checked_text(inspect.getsource(previous.save_comparison_part),{
        "['FI', 'FA', 'FO']":"['FI', 'FA', 'FO', 'FU']",
        'current_ROM_English_conversation_comparison_pending=False, current_reference_pending=False,':
            'current_ROM_English_conversation_comparison_pending=False, current_reference_pending=False,current_English_comparison_pending=False,earlier_English_unconsulted=False,current_English_now_exposed=True,',
        '            rows.append(row)':
            """            if row['id']=='DK4_MES_B37_R0099':
                assert code=='K' and row['english']=="And I'm Admiral {MACRO:FU}!"
                row['wording_retention_with_scoped_glyph_fix']=True
                row['glyph_finding']=dict(current='Ｉ',proposed='I',kind='unintended-fullwidth-Latin',complete_native_font_andpagination_checks_pending=True)
            rows.append(row)""",
    })
    env={**previous.save_comparison_part.__globals__,'ROOT':ROOT,'CURRENT':CURRENT,'DRAFTS':DRAFTS,'OBJECTS':OBJECTS,'normalized_current':normalized_current}
    exec(compile(source,__file__+'::same-exact-comparison-with-distinct-FU-and-one-bound-glyph-fix','exec'),env)
    env['save_comparison_part']('B36_B37_92',decisions,{
        'DK4_MES_B37_R0081':"I hear he's a proud man. Looking ready to run may only make us easier prey. Best to stand tall.",
    },__file__)
    saved=load(ROOT/'B36_B37_92_whole_exchange_comparison_v1.json')
    assert saved['compared']==92 and (saved['proposed_revisions'],saved['justified_retentions'])==(40,52)
    assert sum(bool(r.get('wording_retention_with_scoped_glyph_fix')) for r in saved['records'])==1
