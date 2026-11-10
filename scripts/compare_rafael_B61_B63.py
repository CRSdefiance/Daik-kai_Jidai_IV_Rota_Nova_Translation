"""Review77 current speeches against clean complete exchanges andsealed independent drafts."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Rafael_B61_B80_clean_20261104')
RETAIN={
61:{12:'The lament anddisdain already work;urn is a defensible generic rendering of壺 here anddoes not assert ashes oran invented named item.',
27:'A natural hearty congratulation withthe correct admiral/surname substitution;an extra opening Oh is unnecessary.',
31:'We managed conveys Rafael modest relief,andthe thanks address the governor naturally without needing to repeat Pereira.',
42:'No trouble is a natural informal response to thanks in this conditional occurrence;do not inflate it solely to use the new draft.',
64:'The same brief friendly response works in this distinct source occurrence;retain its independent branch reference.',
78:'Sir is a natural respectful address to the governor here,not an invented knighthood. The pause conveys Rafael being moved.',
129:'My word suits Janus polite surprise atthe enormous gift andis already natural American English.',
154:'The short question captures disbelief atthe amount andasks permission naturally;no content needs restoring.',
161:'The spirited affirmative already matches the source andcloses the encouragement exchange.'},
62:{5:'The formal praise,continent/seas reference,surname substitution andoffered object areall accurate andnatural;no formal coronation is invented.',
15:'The thanks followed by Huh preserves gratitude turning to surprise without an unnecessary added Oh.',
19:'Gone already is a natural casual observation in Claudio voice;the preceding giver departure supplies its subject.'},
63:{5:'The request fora moment andthe inn invitation already sound natural andpreserve the private meeting setup.',
18:'What is a natural brief response to Claudio deliberately vague opener;the next line supplies the missing subject.',
25:'The short defensive Only a little precisely matches Rafael attempt to minimize the work.',
38:'So that excuses it is a sharp,natural rejection of Rafael justification andkeeps the argument escalating.',
41:'The protest already preserves Rafael hurt andfrustration in natural speech;an extra ellipsis is not required.',
46:'The angry Hmph anddismissal sound natural in Claudio voice andmotivate his exit.',
52:'The name/question naturally expresses Arcadius concern;the source substitution andquestion intent areintact.',
60:'Claudio seemed to be shouting is natural tactful reporting of what Arcadius heard,withthe source hesitation.',
71:'Can we talk is a natural tentative request in this worried exchange;no expansion is necessary.',
75:'Yes withthe trailing pause fits the tentative consent better than a more assured Of course.',
79:'The admission naturally identifies Eirene asthe subject of the quarrel;actually preserves the reluctant disclosure.',
84:'Me is a natural startled confirmation question after learning the argument concerned Eirene.',
100:'The silent ellipsis matches the source pause;retain the intended native punctuation rather than invent speech.',
104:'Just yelled at me andstormed out naturally conveys Rafael account of Claudio one-sided anger.',
113:'The apology already links the concealed female identity to Rafael trouble in a gentle voice. Retain wording;correct its two unintended full-width I letters.',
122:'Giving it your all asour admiral is natural,accurate praise in this reassurance. Retain wording;correct the single full-width I.',
126:'The concise reassurance accurately credits Rafael forbeing able to sail safely andfits the intimate exchange.',
134:'The gentle warning not to push himself too hard already works. Retain wording andthe name substitution;correct the single full-width I.',
138:'The quiet Eirene pause is exactly the intended emotional reaction andneeds no expansion.',
150:'Me is a natural brief response of surprise atthe sister comparison,leading to Rafael confirmation.',
154:'The straightforward acknowledgment andthanks convey feeling better andappreciating the listening without unnecessary expansion.',
179:'The hearty greeting andmeal question already sound natural in Claudio suddenly cheerful voice.',
182:'The stammer andClau address naturally show Rafael uncertainty after the quarrel.',
197:'The brief internal observation preserves Rafael amazement thatClaudio forgot the fight andsets up the next thought.',
202:'The final speculative scholar explanation already preserves the naive comic payoff without inventing romance.'}}
FINDINGS={
61:{15:'Replace Remember me,which sounds like a request to be remembered,witha natural angry vow not to forget the defeat.',
22:'Correct the erroneous Koon spelling to established Kuhn andkeep his wounded self-importance/near-success lament in spoken English.',
75:'Restore Pereira own promise to stop objecting over details andhis encouragement to use independent judgment;Enough/Trust your heart blurs that concession.',
83:'Make Claudio compliment directly address Pereira,which prompts the following self-boast;keep familiar warmth without kinship.',
94:'Restore the Governor of Indochina self-title,which is part of Pereira comic third-person boast.',
107:'Restore the same Governor of Indochina good-guy boast in the longer alternative,alongwiththe distinct gift handover.',
113:'Keep the correct500000 military amount butuse a neutral player-facing receipt voice andthe source explicit astonishment rather than an unidentified us speaker.',
122:'Preserve the clearly drawn-out comic astonishment atthe enormous gift,not only a brief What question.',
136:'Make Claudio excited praise sound like complete natural exclamations while retaining the generosity andgovernor address.',
147:'Preserve Jam deliberate long yahoo vocalization rather than changing it to a different yee-haw cheer.',
158:'Restore the hearty reassurance andpersonal I am counting on you;do not silently turn Pereira private encouragement into an unspecified collective pledge.'},
62:{10:'Restore the tentative,excited unfinished connection to the Proof rather than the clipped label A Proof clue.',
23:'Restore the looks-like qualification,the missing sword observation andRafael puzzled question asnatural speech.',
34:'Use deciphering the map,not unlocking a map,which can imply obtaining oractivating a map instead of interpreting it.',
40:'Preserve Arcadius confident inference andthe map-deciphering function withthe full Proof of Conquest term.',
46:'Replace Claudio overly formal Surely withhis casual agreement andkeep the treasure asan anticipated prize rather than a completed acquisition.'},
63:{9:'Restore the mild initial puzzlement before agreement;Rafael does not yet know why Claudio wants to talk.',
14:'Replace the unnatural Show her some care witha vague consideration request,asinthe source before Eirene is identified.',
22:'Preserve helping withthe work rather than alleging forced performance of all the work;integrate the named topic naturally without an early added gendered pronoun.',
30:'Make the physical concern andangry consideration demand natural in Claudio rough voice without inventing a diagnosed illness.',
34:'Replace the stiff special circumstances defense withRafael hesitant,ordinary explanation thatthere were reasons.',
55:'Replace the abrupt translated Something answer witha naturally evasive statement thatsomething is on his mind.',
63:'Ask whether Arcadius heard the argument content,not merely whether the shouting was audible,which the previous line already established.',
67:'Clarify thatArcadius heard the shouting butcould not make out its content,allowing Rafael to explain voluntarily.',
88:'Clarify thatClau is angry withRafael andrecall the earlier assistance naturally;the current line can sound asifhe is angry atEirene.',
92:'Preserve the circumstances,the publicly male persona andthe tentative question seeking agreement instead of a blunt summary.',
95:'Correct current We said to the source first-person I told him;Rafael is recounting his own attempted explanation.',
108:'Correct current collective We care to Rafael own effort to look out forEirene andhis feeling of unfair treatment.',
117:'Replace brusque Let it go withthe gentle source reassurance not to worry,retaining the working opening apology.',
130:'Restore the omitted blush/embarrassment andreplace the unidiomatic Sudden fragment witha natural question about the unexpected praise.',
143:'Restore the specific permission to share worries even just to complain;Talking helps alone loses the advice thatpays off in B73.',
146:'Preserve the older-sister simile andtentative pause;do not invent an actual sibling relationship.',
159:'Keep the reciprocal apology focus:it is Eirene whofeels she should apologize,not an added thank-you followed by an abbreviated apology.',
162:'Keep the personal unfamiliar quarrel withClau andRafael repeated uncertainty;What should we do misassigns the burden being discussed.',
166:'Keep the working reassurance butmake the meal/forgetting prediction idiomatic andappropriately qualified.',
170:'Replace Yes,which does not naturally ask whether the prediction is true,withYou think so.',
175:'Express fond simplicity asnot thatcomplicated,andkeep the invitation to eat without making Eirene unnecessarily insulting.',
186:'Make Claudio question about the odd expression idiomatic rather than the clipped Why thatface.',
189:'Answer the odd-expression question witha flustered Nothing andthe source observation about his good mood.',
193:'Replace the unidiomatic See you ahead withthe actual intention to go on ahead,retaining the casual puzzled dismissal.'}}
OVERRIDES={
(61,15):"Damn it! I won't forget this!",
(61,22):"Me, Kuhn, beaten by these whelps... when I was so close?!",
(61,75):"All right, no more nitpicking from me. Do things your way! Go beat Spain, or whoever else gets in your way!",
(61,136):"Whoa! Now that's generous! You're amazing, Governor!",
(62,23):"It looks like a sword sheath, but there's no sword inside... What could that mean?",
(63,22):"You had Eirene help with the heavy lifting the other day, didn't you?",
(63,55):"Oh, Arcadius... Just... something on my mind.",
(63,67):"No, I couldn't make out what you were saying.",
(63,95):"That's what I told him. We didn't have a choice. But he's furious.",
(63,117):"No, it's not your fault. Sorry for complaining. Don't worry about it.",
(63,166):"Oh, that? Claudio will be fine. He'll probably forget all about it once he's eaten.",
(63,175):"Yes. He's really not that complicated. Come on, let's eat.",
(63,186):"Huh? What's with the funny face?",
(63,189):"N-nothing. I just thought you seemed in a good mood...",
(63,193):"Huh? Whatever. I'll go on ahead.",
}

def current_paragraph(row):
    value=row['current_comparison_paragraph']
    for key,count in row['source_macros'].items():
        assert value.count(key)==count,(row['id'],key,value)
        value=value.replace(key,'{MACRO:'+key+'}')
    return value.replace('Ｉ','I')

if __name__=='__main__':
    output=ROOT/'B61_B63_77_whole_exchange_comparison_v1.json';assert not output.exists()
    draft_path=ROOT/'B61_B64_all197_sealed_drafts_v1.json';current_path=Path('work/analysis/Rafael_B61_B64_current_20261104/current_effective.json')
    draft,current=map(load,[draft_path,current_path]);byid={r['id']:r for g in current['groups'] for r in g['records']}
    records=[];glyphs=[]
    for original in [r for r in draft['records'] if r['block']<=63]:
        row=deepcopy(original);now=byid[row['id']];block=row['block'];index=row['source_reference']['record_index']
        assert (index in RETAIN[block])!=(index in FINDINGS[block])
        prior=current_paragraph(now);keep=index in RETAIN[block]
        english=prior if keep else OVERRIDES.get((block,index),row['english'])
        assert all(english.count('{MACRO:'+key+'}')==count for key,count in row['source_macros'].items())
        assert '\n' not in english and not any(t in english for t in ['{LB','{ALIGN','{PAD}']) and 'Ｉ' not in english
        finding=RETAIN[block][index] if keep else FINDINGS[block][index]
        for key in ['current_hex','current_reference','current_record_index','current_stored_text','current_effective_hex',
            'current_effective_text','current_comparison_paragraph','current_catalogue_selected','selected_native_pointer']:
            row[key]=now[key]
        changes=now['current_comparison_paragraph'].count('Ｉ')
        if changes:glyphs.append(dict(id=row['id'],fullwidth_I_replaced=changes,wording_retained=keep))
        row.update(english=english,logical_English=english,decision='retention' if keep else 'revision',finding=finding,
            retention_reason=finding if keep else None,source_first_draft_English=original['english'],
            source_first_draft_reference=dict(path=str(draft_path),sha256=sha(draft_path.read_bytes()),id=row['id']),
            source_first_draft=False,earlier_English_unconsulted=False,current_English_comparison_pending=False,
            current_ROM=current['current_ROM'],current_ROM_sha256=current['current_ROM_sha256'],
            complete_source_current_anddraft_considered_in_whole_exchange=True,
            four_prose_gates_pass_butformatting_pending=True,fullwidth_I_corrections=changes,
            glyph_only_correction_withwording_retention=bool(changes and keep))
        records.append(row)
    revised=sum(r['decision']=='revision' for r in records);retained=len(records)-revised
    assert len(records)==77 and (revised,retained)==(40,37) and sum(r['fullwidth_I_replaced'] for r in glyphs)==4
    save(output,dict(format='dk4-whole-exchange-editorial-comparison-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        records=records,proposed_revisions=revised,justified_retentions=retained,fullwidth_I_corrections=glyphs,
        source_first_drafts=str(draft_path),source_first_drafts_sha256=sha(draft_path.read_bytes()),
        current_binding=str(current_path),current_binding_sha256=sha(current_path.read_bytes()),
        all_three_complete_source_current_anddraft_exchanges_read=True,
        all_first_four_individual_gates_pass=True,all_individual_fifth_gates_still_false=True,
        remaining120_already_bound_butnot_compared_in_this_receipt=True,
        remaining342_older_English_not_selected_orconsulted=True,
        fresh_formatting_native_visual_stored_actual_andregistered_integration_pending=True,
        new_credit=0,guide_photos=False,producer_sha256=sha(Path(__file__).read_bytes())))
    print('77 contextual comparisons:40 revisions/37 justified retentions;four full-width I letters corrected inthree retained speeches. Formatting/credit pending.',flush=True)
