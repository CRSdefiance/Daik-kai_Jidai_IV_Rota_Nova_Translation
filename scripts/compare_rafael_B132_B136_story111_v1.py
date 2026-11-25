"""Finish contextual comparisons ofbattle/recruitment/ambush/tavern/treasure exchanges."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save

ROOT = Path('work/analysis/Rafael_B121_B140_clean_20261105')
SEALED = ROOT/'sealed351_v1/all_source_meanings_andindependent_drafts.json'
CURRENT = Path('work/analysis/Rafael_B121_B140_current678_20261105/current_effective.json')
OBJECTS = Path('work/analysis/Rafael351_current_objects_v1_20261105/current_objects.json')
OUT = Path('translations/rafael_B132_B136_contextual_comparison_v1.json')
RETAIN = {
132: {25:'The concise readiness question is natural forthe composed companion.',
40:'The rough confidence andchallenge toattack preserve the source’s battle enthusiasm.',
46:'Claudio’s eager response alreadyfits his energetic voice.',
58:'On it naturallytakesup the captain’s call forsupport without adding a duty orrank.',
65:'The formal contempt,Portuguese identity,Spanish Empire andbelated defiance areclear;the sentence fragment works asan insult.',
83:'The concise battle cry preserves the enemy perspective onPortuguese rebels andthe charge order.'},
133: {5:'The recollective Ah andpause work withRafael’s question andJulio’s remembered proposal.',
17:'The natural question elicits Cristina’s identity inthe nextturn.',
22:'The grandfather relationship andsword skill areboth explicit andnaturallyconcise.',
35:'Rafael’s support rests onher sword skill,notan invented romance orrelationship.',
52:'The public cough andbrief agreement work afterthe private aside andsuit Arcadius’s measured voice.',
60:'The parenthesized concession preserves FI andClaudio’s surprise thatRafael alsoopposes him.',
64:'The reluctant concession naturallyfollows the group’s insistence.',
71:'The plain question ispolite English andpreserves the inquiry aboutwhere she lives.',
76:'London is acomplete natural answer tothe preceding location question.'},
134: {6:'The stammer andsharp question naturallyconvey shock atthe surprise attack.',
15:'The flag recognition,pirate warning andadmiral address areclear;retain Vels provisionally pending native-name binding.',
23:'The urgent FI-addressed warning alreadyworks.',
44:'Retain Claudio here:unlike the familiar Clau calls elsewhere,the source explicitlyuses hisfull given name inalarm.'},
135: {9:'The hesitant denial naturallydistinguishes casual acquaintance fromclose friendship.',
32:'The flirtatious maxim leads directlyintothe personal-preference explanation andpreserves the source’s proposed remedy.',
35:'Different preferences,findingout her interests andgiving a suitable gift areall clearlypresent.',
60:'The defensive stammer isthe punchline afterRafael’s innocent professional interpretation.',
69:'The laugh andidiomatic encouragement naturallyclose the exchange;English neednotrepeat the encouragement twice.'},
136: {5:'The familiar FI-addressed attention call isnatural andcomplete.',
9:'A natural question inviting Claudio’s news.',
18:'The brief interested question naturallyelicits the treasure’s name inthe following answer.',
26:'The concise question naturallyasks whythe treasure matters.',
34:'The deadpan question suits Rafael’s practical response toClaudio’s excitement.',
43:'The hesitant where question setsup Claudio’s circular answer naturally.',
48:'The overconfident circular answer alreadyworks ascomedy;the Staff ofGuidance label remains held.',
52:'The repeated practical question isthe necessary nextbeat inthe joke.',
57:'The abrupt admission is natural andpunctures Claudio’s confidence.',
60:'The practical question naturallyexposes the problem withsearching withouta location.',
65:'The short concession preserves hisdeflation.',
69:'The existing rebuke clearlyquestions the vague rumor’s truth withoutasserting the treasure isfalse.',
73:'The dejected concession andNo use then naturallyfollow Rafael’s practical objection.',
79:'The familiar Clau question shows Rafael noticing hisfriend’s dejection.',
84:'My boy is anidiomatic affectionate mentor address here,notliteral fatherhood;the nextturn explicitlyobjects toboy.',
88:'The polite request naturallyechoes the familiar boy address andpreserves Rafael’s irritation.',
92:'The courteous apology andold-habit explanation suit Julio’s older voice.',
98:'The concise question naturallyidentifies the treasure Claudio mentioned.',
120:'The earnest question preserves Rafael’s request forconfirmation,notan objective fact.',
125:'So legends say correctlylimits Julio’s evidence.',
129:'The tentative location question naturallyfollows the legend discussion.',
138:'Rafael deliberatelyoverinterprets the legend;his certainty isthe character’s misunderstanding andmustnotbe smoothed away.',
152:'The direct thanks arealready natural.',
157:'The call afterRafael works naturally ashe rushes away.',
161:'The brief observation preserves thathe hasalready left beforeJulio canstop him.',
179:'The plan toask Janus foradrink isclear anddoesnotassume anaccepted invitation.'},
}
FIND = {
132: {13:'Make the decisive battle anda personal appeal tothe crew natural;stand firm adds a tactical nuance notneeded bythe source.',
68:'Restore the speaker’s threat andthe explicit all-ships preparation order.',
71:'Preserve the subordinate acknowledgment andrelay the all-ships order,notjustan unspecified battle-stations call.',
75:'Preserve the silent beat withASCII ellipsis.',
79:'Restore the action offorming a battle line,notmerely naming one.'},
133: {9:'Preserve the question withASCII punctuation.',
14:'Retain the working proposal,butcorrect Christina tothe approved contextual spelling Cristina.',
25:'Restore natural rough speech andthe near-revelation ofanexisting woman;Against it isastilted fragment.',
28:'The source explicitlyuses Clau,notClaudio;preserve the familiar warning nickname.',
32:'Preserve the stammer andagreement-seeking question instead ofa categorical woman-is-trouble declaration.',
40:'Make the objection andpain reaction natural withoutinventing a pinch,blow orotherphysical action.',
43:'Restore the one-versus-two comparison andits rhetorical question;keep itas aprivate parenthesized aside.',
47:'Restore agreement andthe expected ease ofanotherwoman’s presence;retain the source’s third-person Arcadius reference.',
56:'Restore Clau asthe explicit addressee andmake the appeal natural.',
67:'Preserve Julio’s puzzled question withASCII punctuation.',
80:'Give Rafael a natural polite decision tohead forLondon ratherthan a formal Let usgo.'},
134: {11:'Preserve the sailor’s initial pirates-appearance qualification beforeClaudio recognizes the flag.',
19:'Make Janus’s remembered dangerous reputation andunlucky discovery natural inspoken English.',
27:'Preserve the shocked reaction usingASCII exclamation marks.',
32:'Use a natural English cry ofpain ratherthan a Japanese-like Gwaaah transcription.',
51:'The source hereuses Clau. Restore thatfamiliar call whilepreserving Rafael’s alarm aboutthe injury.',
56:'Make Claudio’s scratch claim a natural reassurance,notan order toignore the incident. Hisclaim doesnotprove actual injury severity.',
60:'Restore the explicit full-speed retreat order whilekeeping the existing frustrated exclamation.',
65:'Restore thatthey cannotcontinue intheir present condition andtherefore needa nearby port.',
70:'Give Claudio a natural urgent warning andalternative-port suggestion ratherthan clipped fragments.'},
135: {5:'Ask aboutthe admiral’s closeness tothe girls,notmerely whether thegirls themselves arefriendly.',
14:'Make the playful advice soundconversational andpreserve the information motive.',
18:'Restore enemy fleet movements andthe occasional location tip,notjust anabstract list ofrare ruins.',
21:'Keep the character’s exaggerated adventurer standard asplayful spoken English,notan impersonal fail condition.',
25:'Specify getting close tothem asthe difficult thing andgive Rafael a natural hesitant question.',
29:'Replace the abstract Mere customer talk withnatural advice whilepreserving dozens ofdaily conversations.',
43:'Restore hearsay anda North Sea town,notgoods soldinthe sea;keep Snowfall Robe provisional ratherthan silentlyrename it.',
52:'Make the undemanding-girl observation colloquial andnatural ratherthan the formal leastgreedy/what she desires phrasing.',
56:'Courting canimply aformality beyondthe source flirting. Preserve Rafael’s naive rationalization ofserial flirtation asprofessional necessity.',
64:'Rafael resolves tofollow the example;he doesnotexplicitlydemand Teach me.'},
136: {14:'Restore thata rumor washeard andgive Claudio a natural excited report,notanews headline.',
23:'Preserve the tentative something-called naming ratherthan a flat authoritative title statement.',
31:'Restore the highest price Claudio personallyhaseverseen andthe hearsay thatnobody hasfound ityet,notan absolute universal claim.',
39:'Keep the get-rich excitement inClaudio’s casual spoken voice ratherthan formal Let usgo.',
76:'Restore a grammatical first-person self-reproach andthe context ofgetting carriedaway so easily.',
95:'Make Julio’s hesitant subject change natural whileholding the item label fornative binding.',
102:'Give the offer a natural question form instead ofthe fragment Hear whatthis oldmanknows.',
116:'Preserve the reported moral guidance inidiomatic English,notan awkward toward-the-path construction.',
134:'Use the source’s India ratherthan anunexplained archaic regional label;keep they say uncertainty.',
143:'Limit Julio’s knowledge tolegend. Only inlegend canimply proven nonexistence,which thesource doesnotassert.',
147:'Restore Rafael’s personal remorse forhowhespoke toClau andhis decision toapologize.',
165:'Keep Claudio’s gloomy mood spoiling Julio’s enjoyment ofdrink;anextra tavern location isunnecessary andnotestablished bythe speech.',
168:'Retain the natural reflective wording andFI substitution;replace both full-width I letters withASCII.',
189:'Make the distrustful accusation natural andpreserve the question followedbyrefusal tofall forthe supposed trick.',
193:'Julio denies hisown intent;do notmake anunnecessary collective assertion aboutClaudio.',
196:'Localize 酒の肴 asthe butt ofjokes over drinks,notas awkward drinking gossip orliteral food.',
200:'Restore Julio’s repeated personal denial beforehe givesup arguing.',
203:'Use a natural first-person explanation ofapproaching Rafael tohelp the upset Claudio,notThis oldman asan artificial self-label.',
206:'Preserve Rafael’s embarrassed realization andapology aftermisjudging Julio’s intent.',
210:'Make the reassurance natural instead ofUnderstanding isenough,andkeep the instruction tocheer Clau up.',
214:'Preserve the sudden polite acknowledgment simply,matching his apology andturntoward helping Clau.',
219:'Make the exasperated aside natural whilekeeping the drinking-talk punchline.',
230:'Preserve the decision toinvite Janus,notan implication thatJanus hasalready agreed tojoin.',
236:'Keep the mischievous laugh andgeneric alcohol anticipation;ale isnot specified inthe Japanese.'},
}
OVERRIDE = {
(132,71): 'Aye! All ships, prepare for battle!',
(133,14): 'Yes, yes. Let us bring Cristina.',
(134,19): "I've heard the rumors. He's known as a dangerous man. Of all the people to spot us...",
(134,60): 'Damn! Retreat at full speed!',
(135,43): 'Take Sakura in Osaka. They say you can buy the Snowfall Robe she wants in a town somewhere on the North Sea.',
(136,23): 'Something called the Staff of Guidance, I think.',
(136,76): 'Why do I get carried away so easily...?',
(136,95): 'Well... About that Staff of Guidance.',
(136,116): 'The Staff of Guidance is said to lead people toward goodness.',
(136,134): 'They say it is in India.',
(136,143): "Remember, it's only a legend.",
(136,147): "Oh... I shouldn't have been so harsh with Clau. I owe him an apology.",
(136,165): "Well, that should cheer Claudio up. He's so gloomy when he's down that I can't even enjoy my drink.",
(136,219): 'What a handful they are. Now all this talk of drinking has made me thirsty.',
(136,236): 'Heh heh. Time for a drink.',
}
LABEL_HOLDS = {(132,13),(134,15),(135,43),(136,23),(136,48),(136,95),(136,116),(136,168)}

if __name__ == '__main__':
    assert not OUT.exists()
    sealed,current,objects = map(load,[SEALED,CURRENT,OBJECTS])
    prior = {r['id']:r for g in current['groups'] for r in g['records']}
    prior.update({r['id']:r for r in objects['choice_records']})
    records = []; glyphs = []; grammar = []
    for source in sealed['records']:
        if not 132 <= source['block'] <= 136: continue
        row = deepcopy(source); old = prior[row['id']]; existing = old['current_comparison_paragraph']
        assert all(row[k] == old[k] for k in ['source_reference','source_hex','source_Japanese'])
        block = row['block']; number = row['source_reference'].get('record_index')
        if row['kind'] == 'typed-choice-label':
            decision,english,reason = 'retention',existing,('The polite acceptance naturallyanswers Julio’s offer.' if row['source_index'] == 0
                else 'The dismissive response leads tothe distrust branch,anddoesnotfalselyclaim knowledge ofthe legend.')
        elif number in RETAIN.get(block,{}):
            decision,english,reason = 'retention',existing,RETAIN[block][number]
        else:
            decision,reason = 'revision',FIND[block][number]
            english = OVERRIDE.get((block,number),row['independent_English_draft'])
            if (block,number) == (136,168): english = existing.replace('Ｉ','I')
        assert english.isascii() and not any(s in english for s in ['\n','\r','{LB','{PAD}','{ALIGN'])
        assert (english == existing) == (decision == 'retention'), row['id']
        for macro,count in row.get('source_macros',{}).items(): assert english.count(macro) == count
        nonascii = [dict(index=i,character=c,codepoint=f'U+{ord(c):04X}') for i,c in enumerate(existing) if not c.isascii()]
        if nonascii: glyphs.append(dict(id=row['id'],current_characters=nonascii,reviewed_text_ASCII=True))
        selector = row.get('source_selector')
        held = selector is not None and selector not in [0,4,5,6,8,20,26,151,254]
        held = held or (block,number) in LABEL_HOLDS
        if (block,number) == (136,76): grammar.append(dict(id=row['id'],current=existing,reviewed=english,missing_first_person_subject_after_am=True))
        row.update({k:v for k,v in old.items() if k.startswith('current_') or k == 'selected_native_pointer'})
        row.update(english=english,current_English=existing,decision=decision,finding=reason,localization_note=reason,
            retention_reason=reason if decision == 'retention' else None,
            source_context_reviewed_as_complete_exchange=True,current_English_comparison_pending=False,
            earlier_English_unconsulted=False,current_ROM_English_unconsulted=False,
            review=dict(source=True,context=True,localization=not held,naturalness=True,formatting=False),
            scoped_name_role_oritem_binding_pending=held,fresh_display_stored_gameplay_andregistered_integration_pending=True,new_credit=0)
        records.append(row)
    assert len(records) == len({r['id'] for r in records}) == 111
    assert sum(r['kind'] == 'typed-choice-label' for r in records) == 2
    assert sum(c['character'] == 'Ｉ' for r in glyphs for c in r['current_characters']) == 2
    save(OUT,dict(format='dk4-natural-dialogue-v2-editorial-manuscript',translation_policy='natural-dialogue-v2',target_locale='en-US',
        encoder='dialogue-relocatable-v1',review_gates=['source','context','localization','naturalness','formatting'],
        file_path=current['file_path'],blocks=list(range(132,137)),records=records,
        current_ROM=current['current_ROM'],current_ROM_sha256=current['current_ROM_sha256'],current_archive_sha256=current['current_archive_sha256'],
        contextual_comparisons=111,proposed_revisions=sum(r['decision']=='revision' for r in records),
        justified_retentions=sum(r['decision']=='retention' for r in records),
        four_gate_passes=sum(all(r['review'][g] for g in ['source','context','localization','naturalness']) for r in records),
        pending_name_role_item_IDs=[r['id'] for r in records if r['scoped_name_role_oritem_binding_pending']],
        glyph_findings=glyphs,grammar_findings=grammar,
        source_revelation_asides_legend_uncertainty_andcomic_progression_reviewed=True,
        no_new_family_rank_location_drink_type_orinjury_severity_claim=True,
        all_fifth_formatting_gates_pending=True,actual_gameplay=False,new_credit=0,full_goal_complete=False,guide_photos=False,
        evidence={str(p):sha(p.read_bytes()) for p in [SEALED,CURRENT,OBJECTS,Path(__file__)]}))
    d=load(OUT);print(dict(compared=111,revisions=d['proposed_revisions'],retentions=d['justified_retentions'],
        four_gate_passes=d['four_gate_passes'],name_role_item_holds=len(d['pending_name_role_item_IDs']),new_credit=0))
