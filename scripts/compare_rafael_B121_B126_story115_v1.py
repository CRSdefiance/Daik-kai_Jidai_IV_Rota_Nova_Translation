"""Contextual comparison ofsix complete rescue/artifact/recruitment exchanges,including34 variants."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save

ROOT = Path('work/analysis/Rafael_B121_B140_clean_20261105')
SEALED = ROOT/'sealed351_v1/all_source_meanings_andindependent_drafts.json'
CURRENT = Path('work/analysis/Rafael_B121_B140_current678_20261105/current_effective.json')
OBJECTS = Path('work/analysis/Rafael351_current_objects_v1_20261105/current_objects.json')
OUT = Path('translations/rafael_B121_B126_contextual_comparison_v1.json')
RETAIN = {
121: {40:'What happened naturallyasks the distressed stranger about the situation;no unnecessary backstory isadded.',
52:'The frightened child’s call forhis actual grandfather andimplicit plea forhelp work naturally inthe drowning scene.',
56:'The complete alarm clearlyidentifies a boy drowning.',
90:'The grandfather’s reassurance andrelief arecomplete andnatural.',
93:'The repeated heartfelt thanks match the source’s emotional repetition afterthe rescue.',
96:'The spoken fragment naturallyshares the grandfather’s relief without aninvented kinship.',
104:'The concise offer isalready a natural match.',
127:'Then... thank you naturallyaccepts afterthe grandfather insists;the surrounding offer makes acceptance clear.',
134:'A natural concise farewell wishing the travelers safety.',
138:'Mister isanatural American child’s address toanolder male stranger;it doesnotmake the rescuer hisbrother.'},
122: {27:'The enthusiastic admiration ofthe jade isclear andnatural,without unsupported superlatives.'},
123: {51:'The question follows Janus’s stone-scarcity explanation naturally andpreserves the proposed nonlocal origin.',
55:'Yes,probably correctlypreserves Janus’s uncertainty.',
66:'How so naturallyasks the companion toexplain the unexpected claim.',
109:'The concise question identifies the attack andtown correctly;approved town-label spelling remains pending.',
112:'The sharp questions alreadyconvey startled hostility;extra swearing isunnecessary.',
119:'The accusation about guarding the town andruining the bandits’ plans isclear andappropriately angry.',
126:'The rebuke andthe townspeople’s needforhelp areclear inthe surrounding exchange;no newrank isneeded.',
130:'The rough accusation accuratelypreserves the destroyed village andEuropean perpetrators.',
133:'The vow naturallypreserves defiant determination despite objections.',
136:'The slavers/plundering soldiers andcontrast withall Europeans remain explicit;the nextspeech develops the moral consequence.',
139:'The natural no-better-than-the-villains comparison conveys the source’s accusation ofequivalent cruelty incontext.',
181:'A natural startled reaction tothe offer.',
185:'The invitation tosea andconfidence inhis spirit arecomplete andappropriate forthe persuasive speaker.',
193:'A natural resigned conclusion thatremaining here achieves nothing.',
200:'The simple welcome fits the acceptance without adding a rank orrelationship.',
207:'The uncertainty about aconnection tothe Proof andthe hidden-in-ruins location areboth preserved;do notforce a personal finder claim.'},
125: {10:'The short questioning reaction naturallyresponds tothe companion calling attention tothe statue.'},
126: {20:'The standard system-notice fragment gives the exact24000-coin reward without extra claims.',
27:'The polite return suggestion andexpectation ofthe waiting fleet arecomplete andnatural.'},
}
FIND = {
121: {6:'Replace telegraphic fragments withRafael naturallycommenting onthe palace andsuggesting a return totown.',
12:'Retain the questioning reaction usingASCII punctuation ratherthan the full-width Japanese glyph.',
45:'Restore relief atthe travelers’ timely arrival beforethe urgent request tosave the grandson.',
48:'The companion questions grandson,notmerely boy;preserve the relationship established inthe immediately preceding plea.',
86:'Give the frightened child a natural past-tense expression ofhow scared he was,notSo scary.',
100:'Restore the man’s personal lack ofa gift,his remembered idea andrequest towait;the passive sounds likea prohibition.',
108:'Rafael asks whatthe offered object is,notan unspecific What reaction.',
113:'Restore the man’s own youthful deed andpersonal reward fromthe governor,notan agentless bandit defeat.',
116:'Restore his lack ofknowledge andhearsay about value;do notassert valuable asan independently established fact.',
120:'Preserve the modest,respectful refusal andrequest tokeep the reward as amemento ratherthan a blunt No command.',
124:'Keep gratitude andinsistence,butmake the object’s lack ofbenefit inhis own hands distinct fromworthlessness orsentimental indifference.'},
122: {40:'Restore the New World comparison andjade being prized amonggems;the source doesnotcall itthe most prized gem.',
43:'Preserve the inference fromthe offerings tothis building’s significance instead ofasserting the conclusion asknown fact.'},
123: {29:'Stone isthe essential material inthe following local-scarcity clue;restore itandRafael’s casual initial dismissal.',
48:'Restore the causal connection between lacking local stone andbuilding the mosque fromdried mud;retain the complete clue.',
63:'Give the polite companion a natural complete observation andrestore stone,notan isolated fragment.',
71:'Make the because relationship explicit;the mud construction follows fromstone scarcity.',
75:'Restore surprise andthe unfinished inference asRafael begins tounderstand.',
80:'Frame the imported-tablet statement asa conclusion fromthe evidence,notunqualified historical knowledge.',
83:'Show understanding ratherthan justan ambiguous exclamation.',
98:'Treat the FE text asambient whispering,notan English command towhisper.',
102:'Preserve the questioning intent withASCII punctuation.',
106:'手が出ない concerns being unable toattack ormake a move here,notliterally touching anobject.',
115:'FO alone loses the affiliation statement;restore I amwithFO whilepreserving the substitution.',
123:'The food expression means losing a livelihood. Do notinvent literal starvation ortranslate itasphysical hunger.',
142:'The source challenges the speaker’s pretended understanding,notmerely whether the advice iseasy tosay.',
146:'Make the firm argument against revenge natural inspoken English whilepreserving its pointlessness andinability torestore happiness.',
150:'Preserve thatmore ofhis ownpeople willbe harmed byanother cycle offighting.',
154:'Restore the faltering challenge afterhis earlier certainty;the emotional turn matters tothe subsequent invitation.',
157:'State the political purpose naturally andpreserve European-power rivalry causing conflicts across the seas.',
161:'Preserve the shocked reaction withASCII punctuation.',
165:'Restore the powers seeking Proofs as apretext forpartitioning the world andthe group collecting them tostop it;the old syntax obscures purpose.',
168:'Use a natural incredulous reaction withthe source hesitation instead ofthe clinical Are yousane.',
171:'Restore the equal-or-better confidence andall-the-way-to-Africa reach;do notinvent deep inland penetration.',
174:'Preserve the silent beat withthe reviewed ASCII ellipsis convention.',
178:'Make the offer a natural invitation,notan unnaturally formal imperative.',
189:'Preserve the second silent hesitation withthe reviewed ASCII ellipsis convention.',
196:'Preserve anindividual decision totake a chance,notan unsupported collective declaration oftrust.',
210:'Restore stone andthe tentative ellipsis inthe artifact question.'},
124: {6:'Restore the friendly attention-getter beforethe request towait.',
10:'Preserve the dynamic speaker’s question usingASCII punctuation.',
14:'Replace the impersonal maxim withthe woman’s natural desire toreciprocate the present withuseful information.',
18:'The clean source says India,notbythe Ganges,anddoesnotestablish thatthe party isnear the landmark. Remove both inventions.',
22:'Explain thata map isneeded toreach itandkeep the enthusiastic encouragement tovisit.',
25:'Restore Rafael’s conditional promise ifhefinds a map,ratherthan implying the map isalready available.'},
125: {6:'Restore the explicit Admiral address whilekeeping the statue observation unfinished.',
33:'Rafael questions whether the statue isoutofplace;Yes isnotthat response.',
55:'Use a natural realization thatthe companion isright,notAh,true.'},
126: {6:'Preserve excited recognition without adding the definitive This isit conclusion absent fromthe words.',
10:'Keep the discoverers’ right toretain the small knife inidiomatic English;dagger needs separate item evidence.',
16:'Localize the tribe’s emotional source ofstrength naturally;do notmake sacred anchor soundlike a literal nautical object.'},
}
STYLE_RETAIN = {
'SC0_B121_STYLE_342_0':'The polite volunteer’s Leave it tome naturallyresponds tothe rescue need;allthree aliases stay intact.',
'SC0_B121_STYLE_342_42':'Got it isanatural confident response taking onthe rescue inthis immediate context.',
'SC0_B121_STYLE_342_54':'The emphatic Leave this tome suits the older companion’s volunteering without inventing kinship.',
'SC0_B123_STYLE_16_0':'The polite look request works withthe onscreen object supplying the referent;retain allthree aliases.',
'SC0_B123_STYLE_16_28':'The casual look call isclear withthe nearby tablet andpreserves the shared two-slot alternative.',
'SC0_B123_STYLE_16_48':'The familiar look-at-this call alreadymatches the rougher source variant.',
'SC0_B123_STYLE_16_74':'Look here is anatural older companion’s deictic direction tothe nearby object.',
'SC0_B123_STYLE_16_100':'The short excited call suits the youthful source voice andpointing context.',
'SC0_B125_STYLE_54_0':'The tentative design judgment isclear;this place refers tothe current building inthe complete exchange.',
'SC0_B125_STYLE_54_46':'The measured looks-out-of-place observation isnatural andits local referent isclear.',
'SC0_B125_STYLE_54_268':'The short casual observation suits theyouthful variant andthe alreadyidentified statue/building.',
'SC0_B125_STYLE_440_0':'The resemblance followed bya question about original function preserves the polite tentative reasoning.',
'SC0_B125_STYLE_440_52':'Perhaps preserves uncertainty whilethe second thought revisits the original identity.',
'SC0_B125_STYLE_440_238':'The casual resemblance andtentative recognition arealready natural forthe rougher voice.',
'SC0_B125_STYLE_440_394':'The measured observation andperhaps-originally inference fit the older formal variant without turning itintocertainty.',
}
STYLE_FIND = {
'SC0_B121_STYLE_80_0':'Restore the actual person onthe sandbar;the fragment omits whoorwhat wasnoticed.',
'SC0_B121_STYLE_80_24':'Name the sandbar clearlyratherthan the ambiguous bar,andmake the observation natural.',
'SC0_B121_STYLE_80_46':'Preserve the older companion noticing someone,notan incomplete location fragment.',
'SC0_B121_STYLE_80_70':'Make the youthful noticing reaction natural whilepreserving the source’s lack ofan explicit sandbar reference.',
'SC0_B121_STYLE_342_18':'Mine sounds likepossession,notnaturally volunteering torescue someone. Restore Leave it tome.',
'SC0_B121_STYLE_342_28':'The companion volunteers togo;avoidmaking it soundlike a plea forpermission.',
'SC0_B121_STYLE_342_76':'Preserve the youthful speaker volunteering togo,notasking tobe allowed toleave.',
'SC0_B122_STYLE_16_0':'Restore the clear call tolook atthe object whilepreserving the admiral address andfive aliases.',
'SC0_B122_STYLE_16_16':'Admiral alone loses the source look instruction;restore the casual look call.',
'SC0_B122_STYLE_16_30':'Make the youthful pointing call natural andcomplete without adding a newidentity.',
'SC0_B125_STYLE_54_92':'Stand out canmean positive distinction. Preserve the source’s sense ofbeing outofplace.',
'SC0_B125_STYLE_54_132':'Give match its building referent andretain the conversational appeal foragreement.',
'SC0_B125_STYLE_54_170':'Use a natural familiar question insteadofthe overlyformal Does thisnotseemwrong.',
'SC0_B125_STYLE_54_214':'Restore the older voice’s tentative impression instead ofthe firmer hardly suits assertion.',
'SC0_B125_STYLE_54_300':'Preserve the polite agreement-seeking question,notan unqualified statement.',
'SC0_B125_STYLE_440_106':'Retain the two-step realization whileusing natural contractions forthe casual voice.',
'SC0_B125_STYLE_440_182':'Make the conversational reconsideration soundlike a speaker’s thought,notan abstract noun phrase.',
'SC0_B125_STYLE_440_304':'A shape isnota figurehead. Preserve the oldervoice’s actual conclusion thatthe object itself isa figurehead.',
'SC0_B125_STYLE_440_366':'The youthful variant proposes using itasa figurehead;it doesnotassert the original identity. Preserve thatdistinct fact.',
}
OVERRIDE = {
(121,124): "No, no. I can't send my grandson's saviors off empty-handed. Please, don't worry. It won't do me any good to keep it.",
(123,168): 'Stop the great powers?! Are... are you out of your minds?',
(123,171): "We're not bluffing. Our influence already reaches all the way to Africa. I'm confident we can meet them on equal terms. Or better.",
(124,22): "You'll need a map to get there, though. You should really go and see it.",
(126,16): "Thanks to you, we've finally found something our tribe can draw strength from. Please accept it.",
}
STYLE_OVERRIDE = {
'SC0_B125_STYLE_54_170': "Doesn't this look out of place here?",
'SC0_B125_STYLE_440_106': "Doesn't this look like a figurehead? Maybe that's exactly what it is.",
}

if __name__ == '__main__':
    assert not OUT.exists()
    sealed,current,objects = map(load,[SEALED,CURRENT,OBJECTS])
    prior = {r['id']:r for g in current['groups'] for r in g['records']}
    prior.update({r['id']:r for r in objects['style_records']})
    records = []; glyphs = []
    for source in sealed['records']:
        if not 121 <= source['block'] <= 126: continue
        row = deepcopy(source); old = prior[row['id']]; existing = old['current_comparison_paragraph']
        assert all(row[k] == old[k] for k in ['source_reference','source_hex','source_Japanese'])
        style = row.get('native_object_kind') == '4100-style-alternative'
        block = row['block']; number = row['source_reference'].get('record_index')
        if (style and row['id'] in STYLE_RETAIN) or (not style and number in RETAIN.get(block,{})):
            decision,english = 'retention',existing
            reason = STYLE_RETAIN[row['id']] if style else RETAIN[block][number]
        else:
            decision = 'revision'
            reason = STYLE_FIND[row['id']] if style else FIND[block][number]
            english = STYLE_OVERRIDE.get(row['id'],row['independent_English_draft']) if style else OVERRIDE.get((block,number),row['independent_English_draft'])
        assert english.isascii() and not any(s in english for s in ['\n','\r','{LB','{PAD}','{ALIGN'])
        assert (english == existing) == (decision == 'retention'), row['id']
        for macro,count in row.get('source_macros',{}).items(): assert english.count(macro) == count
        nonascii = [dict(index=i,character=c,codepoint=f'U+{ord(c):04X}') for i,c in enumerate(existing) if not c.isascii()]
        if nonascii: glyphs.append(dict(id=row['id'],current_characters=nonascii,reviewed_text_ASCII=True))
        selector = row['source_selector']
        held = selector not in [0,4,5,6,8,254] or (block,number) in [(123,165),(123,207),(124,18),(126,10)]
        row.update({k:v for k,v in old.items() if k.startswith('current_') or k in ['selected_native_pointer','native_style_getter_cases']})
        row.update(english=english,current_English=existing,decision=decision,finding=reason,localization_note=reason,
            retention_reason=reason if decision == 'retention' else None,
            source_context_reviewed_as_complete_exchange=True,current_English_comparison_pending=False,
            earlier_English_unconsulted=False,current_ROM_English_unconsulted=False,
            review=dict(source=True,context=True,localization=not held,naturalness=True,formatting=False),
            scoped_name_role_oritem_binding_pending=held,native_dynamic_identity_not_assumed=207<=selector<224,
            fresh_display_stored_gameplay_andregistered_integration_pending=True,new_credit=0)
        records.append(row)
    assert len(records) == len({r['id'] for r in records}) == 115
    assert sum(r.get('native_object_kind') == '4100-style-alternative' for r in records) == 34
    save(OUT,dict(format='dk4-natural-dialogue-v2-editorial-manuscript',translation_policy='natural-dialogue-v2',target_locale='en-US',
        encoder='dialogue-relocatable-v1',review_gates=['source','context','localization','naturalness','formatting'],
        file_path=current['file_path'],blocks=list(range(121,127)),records=records,
        current_ROM=current['current_ROM'],current_ROM_sha256=current['current_ROM_sha256'],current_archive_sha256=current['current_archive_sha256'],
        contextual_comparisons=115,proposed_revisions=sum(r['decision']=='revision' for r in records),
        justified_retentions=sum(r['decision']=='retention' for r in records),
        four_gate_passes=sum(all(r['review'][g] for g in ['source','context','localization','naturalness']) for r in records),
        pending_name_role_item_IDs=[r['id'] for r in records if r['scoped_name_role_oritem_binding_pending']],glyph_findings=glyphs,
        source_kinship_uncertainty_cultural_context_andvariant_specific_facts_reviewed=True,
        original_event_activation_not_inferred_from_record_order=True,all_fifth_formatting_gates_pending=True,
        actual_gameplay=False,new_credit=0,full_goal_complete=False,guide_photos=False,
        evidence={str(p):sha(p.read_bytes()) for p in [SEALED,CURRENT,OBJECTS,Path(__file__)]}))
    d=load(OUT);print(dict(compared=115,revisions=d['proposed_revisions'],retentions=d['justified_retentions'],
        four_gate_passes=d['four_gate_passes'],name_role_item_holds=len(d['pending_name_role_item_IDs']),new_credit=0))
