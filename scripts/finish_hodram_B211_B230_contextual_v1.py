"""Complete the remaining 141 comparisons, preserving all 136 earlier decisions."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.consolidate_hodram_B211_B230_clean_drafts_v1 import OUT as DRAFTS
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.review_hodram_B221_B230_contextual_v1 import CURRENT,OBJECTS,OUT as PRIOR

OUT=Path('translations/hodram_B211_B230_contextual_complete_v1.json')
DECISIONS={
211:{
5:('R','Replace this man with I and preserve Emilio\'s drawn-out eagerness without baby talk.'),
8:('K','What is the natural surprised clarification before Emilio explains why he wants a weapon.'),
12:('R','Restore first-person desire, his wish to grow stronger too and a natural excited explanation.'),
15:('K','The concise food tease and weapon question naturally suit Hodram\'s dry familiarity.'),
18:('R','Use the bound Minotaur Axe catalogue name consistently, retaining Emilio\'s excited exclamation.'),
22:('K','The size inference and location question are complete, natural and do not assert a measured weapon statistic.'),
25:('R','Remove this man and restore the Minotaur report as hearsay and the limit of Emilio\'s knowledge.'),
29:('R','Make the offer to try looking someday conversational, without promising immediate action or ownership.'),
32:('K','Hooray is the natural unqualified celebration that sets up Hodram\'s correction.'),
36:('K','Someday, remember is a natural dry correction; the revised preceding offer retains someday for the comic echo.'),
40:('K','Still, hooray deliberately repeats Emilio\'s stubborn delight after the correction.'),
44:('R','Replace the stiff passive with Hodram explicitly withholding a decision to give Emilio the weapon.'),
47:('K','Aww is a natural disappointed protest; an added longer pause is unnecessary.'),
},
212:{
5:('K','The polite old man\'s request for a moment is natural and establishes no relationship.'),
9:('K','Me is a natural surprised question in response to the address.'),
13:('K','Yes, you naturally confirms whom the old man means.'),
17:('R','Make Cristina\'s question about what he wants clear rather than another ambiguous What.'),
21:('R','Replace the stiff Seeing you recalls construction with a personal recollection of the formidable female pirate.'),
25:('K','The paired look-alike and faces questions naturally ask whether Cristina resembles the woman just mentioned.'),
28:('R','Express bearing rather than the stiff your air phrase and preserve that Cristina looks strong too.'),
32:('R','Remove this woman and preserve her wish to grow stronger by the pirate\'s example.'),
36:('R','Use natural treasured sword wording and preserve the conditional invitation and the pirate\'s former ownership.'),
40:('K','Her sword is a natural short echo; the immediately preceding line establishes the pirate and treasured weapon.'),
44:('R','Remove this old man and restore reported use of the sword alongside his ignorance of its value.'),
48:('R','Give Cristina a conversational expression of interest and a direct location question.'),
51:('R','Use a natural complete answer naming the Caribbean Sea rather than an articleless geography label.'),
55:('R','Restore a natural reflective Caribbean echo with its article and pause.'),
59:('K','The great Caribbean battle, her participation and the supposedly lost sword are all clear and naturally expressed.'),
62:('K','And is Cristina\'s natural prompt for the further information she expects.'),
66:('K','That is all is a natural terse reply from the old man and sets up her frustration.'),
70:('R','Restore Cristina personally wondering how to search, instead of the impersonal how can it be found.'),
73:('R','Remove the invented prohibition Do not ask; he admits he cannot help while expressing an intuitive hope.'),
76:('R','Remove this woman and preserve a future intention to keep the lead in mind.'),
79:('K','The old man\'s confident encouragement and Good luck naturally preserve his optimistic farewell.'),
82:('K','Thank you is the complete natural response.'),
86:('R','Remove third-person self-reference, restore the treasured-sword thought and keep her interest as a wish rather than a necessity.'),
90:('R','Align Cristina with the source-bound native name and retain the exact Charm +1 result.'),
},
213:{
27:('R','Restore the legendary masterworks, their being Tokugawa\'s bane and Japan\'s ruler; do not invent plural rulers or a more specific office.'),
30:('R','Keep the apparent hiding of one blade and East Asia, but make the first-person letter report natural without an added urgency or physical discovery.'),
33:('R','Restore the long search and use the approved full Yukihisa Genjo Shiraki signature instead of an inconsistent kanji-based name.'),
65:('K','Jam\'s terse criticism naturally fits the rougher source 小難しい and recognizes Yukihisa\'s characteristic prose.'),
71:('R','Replace mechanical acknowledgments with Hodram\'s natural recognition that the lead is intriguing.'),
},
214:{
5:('R','Give Al a complete excited spoken report and restore that he picked up the information.'),
8:('K','The local lord, apparently acquired sword and remarkable edge are all present in a clear report.'),
11:('K','And is Hodram\'s natural concise invitation to continue.'),
15:('R','Restore reported faint red coloration instead of an unsupported glowing blade; retain the impression of absorbed human blood.'),
19:('K','Hm and Quite unusual naturally convey Hodram\'s measured interest.'),
23:('R','Preserve the unused sealed sword while making Al\'s coward judgment an inference and his voice conversational.'),
26:('K','What a waste is a complete natural reaction; extra connective words add no needed meaning here.'),
29:('R','Use a natural rough rebuke and preserve the question about what he intended to use a sword for.'),
33:('R','Replace impersonal His feeling is understandable with Hodram personally acknowledging the fear before asking about the weapon.'),
36:('R','Restore I did not find out the hiding place rather than asserting that it is unknown to everyone; keep the conditional search opportunity.'),
},
215:{
5:('R','Restore the little pond and tentative observation in a natural sequence of noticing and recognition.'),
9:('R','Render the FE swan call as recognizable English bird sound rather than an apparently human Aah.'),
13:('K','The pair, surprise at finding them here and direct question about their journey are all natural in her playful address.'),
17:('R','Preserve the complete sequence of bird calls and pauses, using honks rather than human exclamations.'),
21:('R','Give Cristina a natural personal expression of envy instead of the abstract Enviable.'),
24:('K','The repeated flap sound naturally conveys wingbeats; the source onomatopoeia is not a literal counted statistic.'),
28:('R','Use the observed progressive carrying action and natural surprised speech rather than They carry something.'),
32:('K','That way is a natural unfinished direction observation before the next speaker arrives.'),
36:('R','Correct Christina to Cristina while keeping Hodram\'s familiar discovery of her location.'),
40:('R','Preserve the exact FI substitution and restore Admiral in Cristina\'s address.'),
43:('R','Keep the surprise about swans this far into town rather than introduce a general biological claim about entering any city.'),
46:('R','Restore an inferred flight near Amsterdam rather than a confirmed destination and retain the invitation as a question.'),
},
216:{
5:('K','The greeting and knowledge question are natural and fit the retained Yes/No captions.'),
22:('R','Preserve a friendly reading recommendation rather than the clipped Read it command.'),
32:('R','Restore the man\'s personal delight and the specific commander question, retaining You do to fit the existing question.'),
51:('R','Remove this man and keep his excited shared preference and tentative expectation of getting along.'),
54:('R','Restore Changban Bridge and A Dou held in his arms, keeping the novel scene as the speaker recounts it rather than rewriting its history.'),
58:('R','Preserve a rumored spear on a peninsula around here rather than asserting this exact peninsula.'),
62:('R','Remove third-person self-reference and restore his personal wish for the spear before his unsuccessful search and hope for the party.'),
72:('R','Translate the wholly Japanese reply, preserving Guan Yu\'s Beautiful Beard epithet, different preference, wisdom and courage.'),
78:('R','Restore brilliant strategist, the pre-campaign memorial and probable second-favorite status; use the selected Zhuge Liang identity consistently for source Kongming.'),
},
217:{
5:('K','Excuse me, sir is a natural respectful address with no invented rank or relationship.'),
9:('K','Me naturally conveys Hodram\'s uncertain response to the stranger\'s address.'),
13:('R','Replace this old man with I in the polite request to inspect the still-unnamed object.'),
16:('K','That is the exact natural questioning echo of the object gesture; it need not become a different question.'),
20:('K','That item naturally clarifies the gesture without prematurely naming the object.'),
24:('K','The no-mistake recognition and foretold phrase fit the old man\'s ceremonial prophecy account.'),
27:('K','The source standalone question glyph is an intentional puzzled reaction, not a mixed-width English word; retain it pending fresh native checks.'),
31:('R','Restore more than three hundred years and the explicit emperor identity without expanding the mainland into an added conquest claim.'),
35:('R','Preserve the old man\'s elevated approach to the emperor\'s final hour rather than flattening the prophecy to eventually died.'),
38:('R','Restore the retainer as listener, the two-hundred-year prediction and the arrival in this land; preserve the continuing quotation.'),
42:('R','Keep the many foreigners and sword command, but restore one golden seal from a land the emperor could not rule.'),
45:('R','Restore the explicitly stated descent from that retainer; served him alone loses the family-tradition explanation.'),
48:('K','The ceremonial welcome and ruler-of-the-oceans address faithfully convey the old man\'s exalted belief.'),
52:('R','Remove this man and restore Hodram\'s modest refusal; old man is a familiar age address, not a kinship claim.'),
56:('K','The elevated These eyes do not err and Sea King declaration fit the explicit prophetic role and old man\'s voice.'),
59:('R','Restore the Shandong Peninsula, greatsword and expected discovery rather than assert an exact sword location as settled fact.'),
62:('R','Preserve entrusting the greatsword to Hodram, not an implication that an item has already been received.'),
},
218:{
34:('R','Make the signed letter\'s first-person opening complete and preserve a road leading to Rome.'),
38:('R','Restore hearing stories while walking, rather than inventing personal recollection triggered by the road.'),
41:('R','Restore the letter writer\'s personal lack of interest in religion and the one story that caught his attention.'),
44:('K','The sword, Judas, Jesus\'s twelve disciples, tentative continuing presence and associated place are all clear in natural formal correspondence.'),
48:('R','Keep unease about this sword simply because Judas owned it, rather than generalize fear to all his possessions.'),
51:('R','Restore hearsay and the writer\'s judgment while retaining the working keen-and-magnificent description and a blade bears no guilt.'),
62:('K','The qualifying aside naturally preserves Manuel\'s devotion and only a tentative suspected objection after the object-is-not-guilty argument.'),
68:('R','Correct the signature to Janus Pasar and preserve a conditional promise of further news in natural first person.'),
75:('R','Correct Gennas to Janus while keeping the natural pragmatic contrast between quality and origin.'),
87:('R','Remove third-person self-reference while retaining Manuel\'s measured concession, repentance and delegation.'),
},
219:{
5:('R','Make the woman\'s search for the king clear rather than leave an articleless King label.'),
9:('R','Give the vendor a direct angry rebuke instead of the abstract Stop hurting business, with no invented relationship.'),
13:('R','Restore the sword\'s heroic wielder; its hero after the king gives a misleading referent and omits the sword.'),
16:('K','Hodram\'s two direct questions naturally ask what is wrong and who the woman is.'),
19:('R','Remove this woman and align Vivienne and King Arthur with the source-bound literary names while preserving the maker identity.'),
22:('K','King Arthur is a natural surprised echo.'),
26:('K','The king\'s sleep and sacred sword still seeking a hero are naturally expressed in the woman\'s elevated register.'),
29:('K','The charge to seek Excalibur, Avalon and the sleeping king are all present; the prior two speeches already establish the sword\'s sacred nature.'),
32:('K','The natural spoken fragment Never heard of it preserves Hodram\'s unfamiliarity with Avalon.'),
36:('K','Gerhard\'s tentative tavern suggestion is natural and does not guarantee a knowledgeable informant.'),
},
220:{
5:('K','Barkeep naturally localizes the familiar source address without inventing fatherhood; the question about knowing a place is idiomatic.'),
8:('R','Restore the host\'s weary dismissal of the self-proclaimed witch\'s nonsense, not merely a neutral question about belief.'),
12:('K','Supposedly preserves the uncertain existence and the vague just-west location in this doubtful account.'),
16:('R','Preserve the host\'s never hearing of a discovery instead of asserting that no one has ever found Avalon.'),
}}

OVERRIDES={
'DK4_MES_B211_R0029':"I see. We'll try looking for it someday.",
'DK4_MES_B211_R0044':"And I haven't decided to give it to you, either.",
'DK4_MES_B213_R0030':'It appears that a clan bearing a grudge against Tokugawa has hidden one such blade somewhere in East Asia. I write to pass along this news.',
'DK4_MES_B214_R0015':"They say the blade has a faint red tinge, like it's drunk a lot of human blood.",
'DK4_MES_B215_R0005':"What a pretty square... Oh? It looks like there's something in that little pond. Is that...",
'DK4_MES_B216_R0032':"You do? Oh, that makes me happy! Who's your favorite commander?",
'DK4_MES_B216_R0078':"The brilliant strategist Zhuge Liang... Yes, that memorial of his before the campaign brings tears to my eyes. He's probably my second favorite.",
'DK4_MES_B217_R0059':"Search south of the Shandong Peninsula. You should find the emperor's greatsword there.",
'DK4_MES_B217_R0062':'I leave the greatsword in your care. Farewell...',
'DK4_MES_B218_R0051':'Yet I hear the sword is keen and magnificent. A blade bears no guilt, so I think a search would be worthwhile.',
'DK4_MES_B218_R0075':"A traitor's sword... Janus is practical enough to value quality over origin.",
'DK4_MES_B218_R0087':"...I'm not wholly opposed. Judas repented in the end. The decision is yours, Admiral.",
'SC1_B213_STYLE_702_188':'Difficult prose indeed. Very Yukihisa.',
}

def main():
    assert not OUT.exists()
    draft,prior,current,objects=map(load,(DRAFTS,PRIOR,CURRENT,OBJECTS))
    saved={r['id']:r for r in prior['records']};assert len(saved)==136
    by_id={r['id']:r for g in current['groups'] for r in g['records']}
    by_id.update({r['id']:r for r in objects['style_records']+objects['choice_records']})
    decisions={f'DK4_MES_B{b}_R{n:04d}':v for b,entries in DECISIONS.items() for n,v in entries.items()}
    local_overrides=dict(OVERRIDES)
    reaction={
0:('K','The brief prose comment and idiomatic Very Yukihisa naturally recognize the writer\'s characteristic complexity.'),
1:('R','Replace the awkward Hard prose collocation with a natural formal appraisal.'),
2:('K','The short complex-prose comment and familiar author comparison are natural spoken reactions.'),
3:('K','The gentle characteristic-author observation is natural; no invented feminine mannerism or relationship is needed.'),
4:('K','The terse Needlessly difficult criticism fits the rougher source 小難しい and is not a claim about illegible handwriting.'),
5:('R','Replace Hard prose with Difficult prose while retaining the older formal indeed and idiomatic author comparison.'),
6:('R','Use natural childlike first-person inability to understand the content rather than the robotic Cannot understand it.'),
7:('K','Truly, very Yukihisa preserves the source expansive emphasis and remains a natural characteristic-author comparison.'),
}
    arrival={
0:('K','The natural elliptical letter announcement conveys arrival in this delivery scene.'),
1:('K','The clipped correspondence report naturally preserves the formal source register.'),
2:('K','The natural shared announcement preserves both original personality aliases; an invented English distinction is unnecessary.'),
3:('R','Use a gentle natural report without the awkward American Mr. plus given-name rendering of さん.'),
4:('K','The direct simple report fits the familiar voice; the delivered-letter context supplies its arrival.'),
5:('K','The familiar letter announcement works for the older speaker without a forced archaic English caricature.'),
6:('K','The simple excited announcement already captures the childlike source naturally without baby talk.'),
}
    for r in objects['style_records']:
        if r['block']>=221:continue
        index=r['source_style_indices'][0]
        if r['block']==213 and r['source_command_offset']==702:decision=reaction[index]
        elif r['block']==213:decision=arrival[index]
        else:
            assert r['block']==218
            decision=('R','Correct Gennas to the bound Janus identity while preserving the appropriate letter-announcement register and source aliases.')
            if index!=3:
                assert r['current_comparison_paragraph'].count('Gennas')==1
                local_overrides[r['id']]=r['current_comparison_paragraph'].replace('Gennas','Janus')
        decisions[r['id']]=decision
    for r in objects['choice_records']:
        if r['block']!=216:continue
        if r['source_command_offset']==64:
            decisions[r['id']]=('K','The concise Yes/No answer naturally fits the retained question about knowing Romance of the Three Kingdoms.')
        else:
            decisions[r['id']]=('R','Restore the complete selected commander name, not a fit-driven surname abbreviation; preserve the original option and branch identity.')
    expected={r['id'] for r in draft['records']}-set(saved)
    assert len(expected)==141 and set(decisions)==expected
    rows=[]
    for original in draft['records']:
        ident=original['id']
        if ident in saved:
            rows.append(deepcopy(saved[ident]));continue
        cur=by_id[ident];code,finding=decisions[ident]
        assert all(original[k]==cur[k] for k in ['source_reference','source_hex','source_Japanese'])
        paragraph=cur['current_comparison_paragraph']
        english=paragraph if code=='K' else local_overrides.get(ident,original['english'])
        assert (english==paragraph)==(code=='K'),ident
        assert english==english.strip() and not any(t in english for t in ['\n','{LB','{ALIGN','{PAD}','  '])
        english.encode('cp932')
        raw=bytes.fromhex(original['source_hex'])
        assert all(english.count('{MACRO:'+m+'}')==raw.count(m.encode('ascii')) for m in ['FI','FA','FO'])
        row=deepcopy(original)
        row.update({k:v for k,v in cur.items() if k.startswith('current_') or k=='selected_native_pointer'})
        row.update(english=english,logical_English=english,decision='retention' if code=='K' else 'revision',finding=finding,
            retention_reason=finding if code=='K' else '',localization_note=finding+' '+original['localization_note'],
            source_current_conversation_comparison_complete=True,current_reference_pending=False,
            current_ROM_English_conversation_comparison_pending=False,source_context_localization_formatting_gates_pending=True,
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
            independent_clean_draft_reference=dict(path=str(DRAFTS),sha256=digest(DRAFTS),id=ident),new_credit=0)
        rows.append(row)
    assert len(rows)==277 and len({r['id'] for r in rows})==277
    assert all(next(r for r in rows if r['id']==ident)==row for ident,row in saved.items())
    counts={word:sum(r['decision']==word for r in rows) for word in ['revision','retention']}
    save(OUT,dict(format='dk4-editorial-prose-packet-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        encoder='dialogue-relocatable-v1',review_gates=['source','context','localization','naturalness','formatting'],
        file_path='/data/SC1.DK4',records=rows,records_count=277,counts=counts,remaining_contextual_comparisons=0,
        first136_decisions_exactly_preserved=True,all277_source_drafts_preserved=True,
        full_width_Latin_I_findings=prior['full_width_Latin_I_findings'],
        untranslated_current_Japanese_reply='DK4_MES_B216_R0072',
        fresh_formatting_andvisual_checks_pending=True,no_new_native_display_gameplay_orrelease_credit=True,
        new_credit=0,guide_photos=False,evidence={str(p):digest(p) for p in (DRAFTS,PRIOR,CURRENT,OBJECTS,Path(__file__))}))
    print('Completed all 277 contextual comparisons:',counts,'; first 136 exact. Scoped names and fresh display remain.')

if __name__=='__main__':main()
