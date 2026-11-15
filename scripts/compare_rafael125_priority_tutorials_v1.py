"""Review complete early tutorials afterclean-first drafts;hold unresolved UI labels andall formatting."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save

ROOT = Path('work/analysis/Rafael_B121_B140_clean_20261105')
SEALED = ROOT/'sealed351_v1/all_source_meanings_andindependent_drafts.json'
CURRENT = Path('work/analysis/Rafael_B121_B140_current678_20261105/current_effective.json')
OBJECTS = Path('work/analysis/Rafael351_current_objects_v1_20261105/current_objects.json')
OUT = Path('translations/rafael_B121_B140_priority_tutorial_comparison_v1.json')
BLOCKS = {127,128,129,137,138,139,140}
# Retain exact logical current wording where it alreadyworks in its complete exchange.
RETAIN = {
127: {5:'A natural,calm suggestion ofthe correct first destination;the surrounding tutorial makes its priority clear.',
13:'The instruction clearlyidentifies the first practical step andpreserves current ship heading.',
20:'D-Pad is natural American hardware terminology,andboth source input methods arepresent.',
26:'Both automatic sail adjustment andflagship touch-to-stop arecomplete andclear.',
29:'The single natural question covers the source’s repeated comprehension check without losing either choice branch.',
44:'The concise encouragement preserves the explicit admiral address andmentor’s approval.',
58:'A natural brief expression ofRafael’s remaining doubt about the just-described sailing attempt.',
73:'Most preserves the source qualification;the antecedent is the preceding voyage-trouble list,andprompt port advice remains clear.',
80:'The direction andmap reference areclear;retain provisionally whilethe visible map-label binding ischecked.'},
128: {12:'The FI address andoffer toexplain remaining at-sea actions soundnatural inJulio’s mentoring voice.',
15:'A natural polite acceptance ofthe preceding explanation offer.',
36:'The brief acknowledgment naturallyfits Rafael learning fromJulio.',
63:'A natural surprised question about the unexpected manual-control requirement.',
72:'The stammer preserves Rafael’s nervous acceptance.',
81:'The instruction correctlynames L/R anduses natural nautical trim terminology,explained further inthe following line.',
85:'Both button directions areexplicit andcorrect;no wording change isneeded.',
89:'Automatic stylus trimming andflagship touch-to-stop areboth complete.',
107:'Rafael’s eager request totry the controls isclear andnatural.',
128:'The remembered errand andpolite FI-addressed request forAthens arealready idiomatic.',
152:'A natural,slightly noncommittal confirmation ofRafael’s suggested shared goal.',
168:'The short confirmation answers the preceding Athens question without unnecessary elaboration.',
174:'The Hayreddin promise isexplicit inthe source;the current sentence isclear andpreserves that necessary context.',
180:'The FI address andClaudio’s enthusiasm work naturally inthe exchange.',
200:'The concise question suits Janus’s measured curiosity about the destination.'},
129: {5:'A natural conversational check onwhether FI haslearned totrade profitably.',
20:'The existing wording preserves the small Portuguese island andsouthwest-of-Lisbon location morecompletely thanthe independent draft.',
30:'Both the three-town trade progression andnext two targets areclear;Cape Verde spelling remains held forapproved UI binding.',
33:'The transit-gateway explanation andlow-investment goods advantage areclear;retain subject toCape Verde label binding.',
36:'A coherent commercial progression fromtrading profits tolarger ships andgreater town shares;no battle action isadded.',
42:'The repeated farther gives natural momentum tothe advice toexpand trading range.',
58:'The self-aware worry aside fits Julio’s age andmentor role without inventing a family relationship.',
62:'A natural closing thatgives Rafael room tochoose his own approach.'},
137: {6:'Buy low,sell high is idiomatic American English andcaptures the complete trading principle.',
13:'The nearby-first advice andinitial limit onlong voyages areclear inthe beginner context.',
22:'The existing explanation clearlyconnects few initial ships/holds tothe quantity thatcanbe traded.',
30:'Both the market-share limit andthe benefit ofincreasing it arecomplete andnatural.',
44:'The natural question asks howtoincrease the company’s market share;the optional preceding choice supplies the definition prompt.'},
138: {6:'The complete needforordinary sailors isclear;her is anatural maritime reference tothe ship,notan invented character.',
10:'The source’s recruitment tactic andgenerosity areboth conveyed naturally without inventing a stat bonus.',
25:'The explanation ofextra sailors reducing supply endurance isclear andconsistent withthe source’s voyage-day warning.',
29:'A natural prompt topractice the just-described recruitment/allocation steps.'},
139: {19:'The neighboring-port agreement rule iscomplete andclear.',
27:'The FO substitution,neighbor relationship andLisbon/Ceuta route areall preserved.',
34:'The short echo question isappropriate;the visible Auto Travel label remains held ratherthan guessed.',
39:'The connected-route condition,destination choice andnavigators handling the ship areclear incontext.',
55:'The source’s standalone hesitation setsup the missing-surveyor joke;preserve its native speech boundary.',
64:'The missing-role obstacle isnatural andaccurate without assigning the role toan invented person.',
67:'The teasing big-talk remark matches Claudio’s familiar voice;old man doesnotcreate a family tie.',
74:'The explicit instruction toequip Julio himself iscorrect andmustremain;buying orcarrying the item alone isnot substituted.',
77:'The concise echo question naturallyshows Rafael’s uncertainty about equipment.',
82:'The item-inspection advice andreturn-to-Lisbon instruction arecomplete incontext.',
85:'The stammer preserves Rafael’s hesitant agreement.',
102:'Good luck is anatural English encouragement serving the same closing purpose.'},
}
FINDINGS = {
127: {9:'Replace the abrupt command withJulio naturallybeginning practical ship instruction.',
16:'Make itclear thatthe ship ispointed toward the desired heading,ratherthan leaving point withoutan object.',
23:'Specify touching the desired direction,notmerely touching anunspecified point onthe screen.',
49:'Replace the impersonal A heading isset withRafael’s own uncertainty andpreserve the wind-dependent question.',
54:'Retain headwind difficulty while restoring Julio’s explicit reassurance about this route’s tailwind.',
63:'Localize the proverb as reassuring spoken English;keep Lisbon asthe fallback ratherthan clipped commands.',
70:'Preserve the examples whilemaking the possibility ofvoyage trouble explicit,notan inevitable event.',
77:'A fleet recovers fromconditions;conditions themselves donot recover. Give the port-recovery instruction naturally.'},
128: {20:'Turn the disconnected fragment intoJulio’s explanation ofwhen full sail andanchoring areuseful.',
23:'Keep full speed andthe captain’s direct orders whilemaking the instruction soundspoken andreadable.',
26:'Keep the one-handler-per-mast requirement andautomatic trimming;replace clipped keep half phrasing.',
29:'Retain the qualified difficulty/battle advice inordinary English ratherthan terse label fragments.',
32:'A fleet spreads out;spread fleet isawkward. Preserve both regrouping andambush uses as examples.',
42:'Explain the speed adjustment naturally whilepreserving anchoring in place.',
46:'Give the A/B directions directly inordinary English;do notchange either button mapping.',
50:'Retain the exact B-driven Full-to-Half transition inclear mode wording,pending visible-label confirmation.',
53:'Retain the exact B-driven Half-to-Anchor stop inclear wording,pending label confirmation.',
56:'Spell out both A-driven transitions without the telegraphic for half/for full construction.',
60:'Address Rafael directly andpreserve the insufficient-handler exception even atHalf Sail.',
68:'Preserve the eventual full-speed need whileletting Julio encourage a captain tolearn sail handling.',
77:'Replace the abstract basis ofspeed witha clear explanation ofcatching wind behind the sails.',
93:'Set it behind the sails misleadinglymakes wind thething tocontrol. The player adjusts sails whilewatching wind direction.',
97:'Make itclear thata tailwind makes trimming easier;the headwind stillrequires skill.',
101:'Tell the player toadjust sails using the speed bar,notjust to maximize the bar as anabstract operation.',
104:'Study the rest yourself soundsdismissive. Preserve Julio’s expectation ofRafael learning throughexperimentation.',
111:'Replace the unnatural passive Something wasforgotten withJulio’s personal feeling thathe forgot something.',
114:'Retain the questioning reaction,butreplace the full-width Japanese question glyph withASCII punctuation.',
132:'Restore Rafael’s hesitant recognition ofGreece andeastern-Mediterranean location instead ofa flat formal statement.',
137:'Business awaits isstilted. Preserve Julio’s casual explanation thathe hasa little business there.',
140:'Give Claudio a natural skeptical question about choosing their destination aroundthe old man’s errand.',
143:'Restore the future-oriented investigation andJulio’s personal purpose,notmerely a generic shared search.',
147:'Keep the echoed future wording andRafael’s tentative interpretation asa shared goal.',
155:'Nothing mustbedone atonce isawkward andambiguous. Preserve the distinction between noimmediate action andlater necessity.',
164:'Athens willexplain it awkwardlypersonifies the city. Ask whether arriving there willmake the purpose clear.',
184:'Use a casual enthusiastic agreement thatfits Rafael speaking withClaudio.',
189:'Retain the working proverb,FI address andencouragement;correct the single full-width I toASCII.',
207:'Seek ourgoal isunnatural spoken English. Preserve Claudio’s playful announcement ofgoing tofind a goal.',
210:'Express Rafael’s puzzled response tothe odd announcement as anatural complete remark.'},
129: {24:'Restore sugar amongother local products,andthe expected future base role asFO expands,ratherthan omitting goods andstating certainty.',
27:'The condition isunclaimed market share being available,notmerely Madeira having market share.',
39:'Restore the increasing holds/goods relationship andprofit pertrading run;town goods andeach voyage areless precise.',
45:'Restore the distinction between anapparently unprofitable town andits possible new production throughcommercial investment.',
48:'Preserve the optional affordable New World trip;No needtoforce it isa calque ratherthan natural mentoring advice.',
52:'Give Rafael a natural personal commitment todo his best.'},
137: {9:'Preserve the opportunity once the crossing ispossible,ratherthan making quick profits soundautomatic.',
16:'Restore watching eachtown’s prices andgive natural advice ratherthan the clipped Seek bigger profits.',
19:'Make the suggested Lisbon-to-Ceuta starter sale clear whilepreserving saffron andalmonds as alternatives.',
26:'Explain the source’s one-full-hold transaction unit without adding anunverified open-hold rule.',
48:'Restore the unclaimed-share condition andinvestment action;trade-house label binding remains pending.',
52:'Keep the advice conditional onlater earnings/fleet growth,soit doesnotread as another immediate command beforefirst trading.',
60:'Restore checking the transaction,Confirm completing it,andthe invitation totry;do notleave onlya button name.'},
138: {14:'Restore whyoffering drinks helps andJulio’s qualified expectation thatinitial recruitment canwork without it.',
18:'The tutorial asks howmany ordinary sailors appear,notwhich named people. Preserve the recruitment command,pending label binding.',
21:'Replace the vague flagship option withthe source’s specific flagship-priority allocation choice,pending native-label confirmation.'},
139: {5:'Keep the already-natural question andFI substitution;correct both full-width I letters toASCII.',
23:'Restore the missing FO substitution andthe fact ofagreements withLisbon/Ceuta,notmerely current trading there.',
30:'Restore Captain/Surveyor assignment onthe Deck screen as acondition,notmerely possessing suitable people;Auto Travel label remains pending.',
42:'Restore the port command path anddestination selection onthe map,notan unspecified destination picker.',
59:'Retain the questioning reaction,butreplace the full-width Japanese question glyph withASCII punctuation.',
71:'Restore the request togo toLisbon,buythe sextant,andJulio’s offer tomanage withit,ratherthan animpersonal guaranteed solution.'},
140: {5:'Restore the reason forinvestment andthe specific town Arms statistic,subject toexisting native-label evidence.',
9:'Restore the towns alongthe route tothe Indian Ocean;generic eastern forts loses the geographic context.',
12:'Keep construction expertise,military investment andthe qualified expected saving;do notturn itintoan unconditional unspecified fortification bonus.',
16:'Give Rafael a natural personal acknowledgment ratherthan a formal collective response.'},
}
UI_HOLDS = {(127,80),(128,23),(128,26),(128,29),(128,32),(128,50),(128,53),(128,56),
    (129,30),(129,33),(137,48),(137,60),(138,18),(138,21),(139,30),(139,34),(139,42),(139,71),(140,5),(140,12)}
CHOICES = {
'SC0_B127_CHOICE_488_0': ('revision',"I've got it!",'Give the confident response a natural spoken form appropriate toRafael,ratherthan the formal adverb Perfectly.'),
'SC0_B127_CHOICE_488_1': ('revision','The wind might be against us...','Make the specific adverse-wind concern clear;the wind being wrong isawkward English.'),
'SC0_B129_CHOICE_80_0': ('retention',None,'Not yet naturallyanswers whether FI haslearned totrade profitably anddoesnotclaim prior mastery.'),
'SC0_B129_CHOICE_80_1': ('revision',"I've got the hang of it.",'Mastered isa status-like fragment andoverstates the source’s comfortable readiness.'),
'SC0_B137_CHOICE_704_0': ('revision','Market share?','Identify the commercial concept ratherthan anambiguous isolated Share.'),
'SC0_B137_CHOICE_704_1': ('retention',None,'Got it isanatural acknowledgment matching the understanding response.'),
'SC0_B139_CHOICE_112_0': ('retention',None,'The polite acceptance isalready a natural match forthe offered explanation.'),
'SC0_B139_CHOICE_112_1': ('retention',None,'The concise polite refusal explicitlystates understanding andfits the choice branch.'),
}
OVERRIDES = {
(127,70): 'Long voyages can bring all sorts of trouble: sickness, rats, leaks...',
(127,77): 'If your fleet develops an abnormal condition, put in at a town to recover.',
(128,97): 'A tailwind makes it fairly easy. A headwind takes some skill.',
(128,140): "Hey, are we really letting the old man's errand decide where we go?",
(128,184): 'Yeah!',
(128,210): "Huh? That's an odd way to put it...",
(139,30): 'With a Captain and Surveyor assigned on the Deck screen, you can use Auto Travel along an established route.',
(139,42): 'At the port, choose Auto Travel, then select your destination on the Map.',
(140,16): "I see. I'll keep that in mind.",
}

if __name__ == '__main__':
    assert not OUT.exists()
    sealed, current, objects = map(load,[SEALED,CURRENT,OBJECTS])
    assert sealed['source_objects'] == 351 and sealed['remaining_source_speech_style_orcaption_drafts'] == 0
    assert current['clean_meanings_sha256'] == sha((ROOT/'sealed351_v1/meanings_view.json').read_bytes())
    assert current['current_ROM_sha256'] == objects['current_ROM_sha256'] == 'cc71ec06ce5345dcc71f8b631232f4d8d501152f6989374741616260fa0ca448'
    bindings = {r['id']:r for g in current['groups'] for r in g['records']}
    bindings.update({r['id']:r for r in objects['choice_records']})
    records = []; glyphs = []; macros = []
    for source in sealed['records']:
        if source['block'] not in BLOCKS: continue
        row = deepcopy(source); old = bindings[row['id']]
        assert all(row[k] == old[k] for k in ['source_reference','source_hex','source_Japanese'])
        existing = old['current_comparison_paragraph']
        if row['id'] in CHOICES:
            decision, english, reason = CHOICES[row['id']]
            english = existing if english is None else english
            held = False
        else:
            number = row['source_reference']['record_index']; block = row['block']
            held = (block,number) in UI_HOLDS
            if number in RETAIN.get(block,{}):
                decision,english,reason = 'retention',existing,RETAIN[block][number]
            else:
                decision = 'revision'; reason = FINDINGS[block][number]
                english = OVERRIDES.get((block,number),row['independent_English_draft'])
                if (block,number) in [(128,189),(139,5)]: english = existing.replace('Ｉ','I')
        assert english.isascii() and not any(s in english for s in ['\n','\r','{LB','{PAD}','{ALIGN'])
        assert (english == existing) == (decision == 'retention'), row['id']
        current_macro_counts = {}
        for macro,count in row.get('source_macros',{}).items():
            assert english.count(macro) == count, (row['id'],macro)
            current_macro_counts[macro] = existing.count(macro)
            if existing.count(macro) != count:
                macros.append(dict(id=row['id'],macro=macro,source=count,current=existing.count(macro),reviewed=count))
        nonascii = [dict(index=i,character=c,codepoint=f'U+{ord(c):04X}') for i,c in enumerate(existing) if not c.isascii()]
        if nonascii: glyphs.append(dict(id=row['id'],current_characters=nonascii,reviewed_text_ASCII=True))
        row.update({k:old[k] for k in ['current_hex','current_reference','current_effective_hex','current_effective_text',
            'current_comparison_paragraph','current_stored_text','current_catalogue_selected','selected_native_pointer'] if k in old})
        row.update(english=english,current_English=existing,decision=decision,finding=reason,localization_note=reason,
            retention_reason=reason if decision == 'retention' else None,
            source_context_reviewed_as_complete_exchange=True,current_English_comparison_pending=False,
            earlier_English_unconsulted=False,current_ROM_English_unconsulted=False,
            review=dict(source=True,context=True,localization=not held,naturalness=True,formatting=False),
            UI_label_ornamed_item_binding_pending=held,fresh_display_stored_gameplay_andregistered_integration_pending=True,
            current_macro_counts=current_macro_counts,new_credit=0)
        records.append(row)
    assert len(records) == 125 and len({r['id'] for r in records}) == 125
    assert len(macros) == 1 and macros[0]['id'] == 'DK4_MES_B139_R0023' and macros[0]['macro'] == 'FO'
    assert sum(c['character'] == 'Ｉ' for r in glyphs for c in r['current_characters']) == 3
    assert sum(c['character'] == '？' for r in glyphs for c in r['current_characters']) == 2
    save(OUT,dict(format='dk4-natural-dialogue-v2-editorial-manuscript',translation_policy='natural-dialogue-v2',target_locale='en-US',
        encoder='dialogue-relocatable-v1',file_path=current['file_path'],blocks=sorted(BLOCKS),
        review_gates=['source','context','localization','naturalness','formatting'],records=records,
        current_ROM=current['current_ROM'],current_ROM_sha256=current['current_ROM_sha256'],current_archive_sha256=current['current_archive_sha256'],
        contextual_comparisons=125,proposed_revisions=sum(r['decision']=='revision' for r in records),
        justified_retentions=sum(r['decision']=='retention' for r in records),four_gate_passes=sum(all(r['review'][g] for g in ['source','context','localization','naturalness']) for r in records),
        pending_UI_name_term_IDs=[r['id'] for r in records if r['UI_label_ornamed_item_binding_pending']],
        glyph_findings=glyphs,substitution_findings=macros,remaining_source_comparisons=226,
        all_fifth_formatting_gates_pending=True,all_existing_source_drafts_preserved=True,
        actual_gameplay=False,new_credit=0,full_goal_complete=False,guide_photos=False,
        evidence={str(p):sha(p.read_bytes()) for p in [SEALED,CURRENT,OBJECTS,Path(__file__)]}))
    d=load(OUT)
    print(dict(comparisons=125,revisions=d['proposed_revisions'],retentions=d['justified_retentions'],four_gate_passes=d['four_gate_passes'],
        UI_name_term_holds=len(d['pending_UI_name_term_IDs']),full_width_I=3,full_width_questions=2,restored_company_substitutions=1,
        remaining_comparisons=226,fresh_display_pending=True,new_credit=0))
