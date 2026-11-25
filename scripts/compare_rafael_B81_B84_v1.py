"""Compare330 source-drafted prose objects as complete exchanges;retain good dialogue and flag one action ambiguity."""
import re
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Rafael_B81_B100_clean_20261105')
CURRENT=Path('work/analysis/Rafael_B81_B84_current_20261105/current_effective.json')
CHOICES=CURRENT.with_name('current_choice_objects_v1.json')
RETAIN={
81:{20,37,43,51,70,82,86,98,102,110,114,118,130,134,138,142,150,154,159,163,168,171,176,185,189,194,202,213,220,231},
82:{14,24,37,69,72,96,113,117,121,130,143,147,154,161,164,168,172,175,178,187,191,194,197,205,208,220,228},
83:{16,27,41,52,59,71,75,84,92,104,114,117,120,123,133,185,188,206,213,221,234,238,248,251,255,260,264,291,303},
84:{5,10,17,27,37,44,48,53,57,60,71,76,93,97,100,106,110,114,117,121,125,130,134,143,147,151,164,171,182,193,197,201,210,215,218,248,253,262,272,281,290,294,306,314,332,340,353,366,376,385,394,402,407,446,449,454,461,487,491,507,511,515,518,523,530,556,560,566,577},
}
OVERRIDES={
(82,28):'...Is that who you meant?',(82,33):"That's right.",
(82,110):"Hmph. Just the sort of thing Herald would think of. Perhaps I went wrong raising him...",
(83,88):"Hold on! I'll save him!",(83,137):'Cristina... But the sea... the water...',
(83,156):'Mivor to the rescue!',(83,160):"Cristina! I'm coming!",
(83,177):"Yes, he's safe. His mother was grateful.",
(83,299):"I didn't thank you properly before. Thank you, Mivor. You were... pretty impressive...",
(83,307):"Really?! You thought I was impressive?! I'm so, so happy!",
(83,311):"You're getting the wrong idea!",
(83,326):'For all their bickering, they really do make a good pair.',
(84,389):'Teach us how you fight! Please!',
}
FINDINGS={
(81,5):'Keep the explicit bullfight promise and Spain destination in a natural granddaughter-to-grandfather reminder;B82 independently establishes their kinship.',
(81,16):'Restore the invitation to everyone and the something-to-talk-about rationale;the old That makes a good story is stiff and changes the prospective invitation.',
(81,47):'Keep Claudio\'s blunt dig at Julio\'s borrowed national pride,not a flat statement that he is unimportant.',
(81,54):'Use the source\'s popular bullfighter description without prematurely identifying the performer as the matador;the next exchange distinguishes picador from matador.',
(81,94):'Explain picador as the matador\'s assistant,retaining the Spanish cultural terms and the following division of roles.',
(81,106):'The Japanese transitive throw clause leaves its object unstated. The fresh reading treats Emilio as throwing the bull;the old English says the bull threw him. Context favors strength-based recruitment,but a concrete original visual/action binding is still required. Do not mark localization passed or ship either interpretation merely from the old translation.',
(81,198):'Preserve Claudio\'s physical double take and the delayed realization that Rafael meant Emilio rather than the matador;Whoa conveys the written stumble without inventing an injury.',
(81,209):'Retain the ship/tasty misunderstanding and Rafael\'s quick food-based persuasion;replace seek with natural spoken wording.',
(81,216):'Restore Rafael\'s optimistic uncertainty,expressed by surely in the Japanese,instead of converting it into unqualified knowledge of the whole world.',
(81,228):'Restore the explicitly spoken Ferog surname;the old line reduces the introduction to Emilio alone. Match the current source-bound name metadata.',
(82,8):'Use native Cristina,not the inconsistent Christina dialogue spelling,while retaining Mivor\'s theatrical affection as his claim,not an established romance.',
(82,18):'Restore complete natural sentences and Cristina\'s lack of consent to the parent-arranged engagement;do not imply an actual marriage.',
(82,28):'Use gender-neutral Is that who you meant? The Japanese says that person;the old That man adds a gender that this line does not state.',
(82,33):'Confirm the person neutrally,rather than preserving the old Yes,him gender inference.',
(82,49):'Repair the missing did you in the London arrival question;Grandpa is supported by the explicit granddaughter exchange.',
(82,56):'Preserve the warning that her parents will try to stop Julio,without asserting that they actually succeed.',
(82,75):'Restore that Mivor is the son of her father\'s friend,not merely an unspecified friend\'s son;keep her inability to remember his name.',
(82,82):'Keep the foppish full-name introduction and match native Mivor Genz rather than the old body\'s Gentz. This is an individual source/current consistency decision,not a global nationality claim.',
(82,103):'Preserve his insistence on sincere feelings and a respectful Miss Cristina;Lady Christina adds a title unsupported by this form of address.',
(82,110):'Retain the established spoken name Herald for sourceヘラルド,without claiming independent Latin attestation. Restore Julio\'s first-person self-mockery about raising him;the old passive raised wrong loses his responsibility.',
(82,125):'Say her grandfather told Rafael about her. The Japanese does not say that he praised her skill,as the old English does.',
(82,133):'Keep Julio\'s private one-thing-after-another aside and the admiral introduction. Correct the mixed full-width I and F in ordinary English without changing speaker controls.',
(82,140):'Restore the explicitly stated difficulty of finding sword opponents as a woman and the worldwide-training suggestion;the old wording replaces the former with an unsupported desire for matches abroad.',
(82,150):'Keep the repeated ignored objection as a comic continuation of Mivor\'s formal protest,not a new effective veto.',
(82,158):'Use the natural American idiom No time like the present for the source proverb while preserving her appeal to Grandpa.',
(82,213):'Preserve the wish to see her father\'s and grandfather\'s homeland once;do not turn homeland into a precise claim that both were born there.',
(83,101):'Localize the reassuring older-girl self-reference as I\'m here now. The rescued boy is not established as Cristina\'s brother.',
(83,111):'Make the breathless plea natural and retain the neck-grip/breathing problem without presenting Cristina as the boy\'s actual sister.',
(83,140):'Correct the reversed emotional progression:source fear>affection still prevents action here;the old Christina matters more belongs to the later turning point.',
(83,146):'Preserve the later fear<affection resolution and native Cristina spelling;the earlier hesitation and this resolve are distinct turns.',
(83,156):'Use a natural theatrical self-announcement,Mivor to the rescue,to preserve the comic named declaration as he finally jumps.',
(83,166):'Restore Cristina\'s confused location/what-happened questions after coughing awake;the old line omits the former.',
(83,177):'Confirm the boy is safe and that his mother expressed gratitude;avoid inventing us as the explicit recipient of her reported thanks.',
(83,192):'Restore Mivor\'s hesitant first-person I saved you;the Japanese uses I,not the old third-person Mivor self-reference at this sincere moment.',
(83,199):'Preserve his faltering account that the need to save Cristina overwhelmed his thoughts;do not turn the unfinished source into a definite clinical claim that his mind went blank.',
(83,203):'Use first-person I for his astonishment at swimming;this body swam is an unnatural third-person addition absent from the source.',
(83,226):'Render the child\'s friendly recognition without inventing a big-sister relationship.',
(83,245):'The mother reports a strange shout,not odd crying that could imply weeping during the plunge.',
(83,267):'Use the child\'s friendly goodbye without presenting Cristina as his sibling.',
(83,277):'Restore Rafael\'s surprise that Mivor actually swam. The old question about being afraid of water misstates the point of this response.',
(83,285):'Restore the source\'s speak-of-the-devil coincidence joke when Mivor appears during their conversation.',
(83,299):'Preserve her halting,embarrassed admiration and thanks without turning it into a romantic commitment;pretty impressive suits her everyday voice.',
(83,307):'Keep his exaggerated delighted echo of her praise,in first person rather than the old Mivor looked brave.',
(83,311):'Use her natural colloquial protest against his misunderstanding;the source does not mean she has consented to marry him.',
(83,326):'Restore the despite-their-bickering qualification in Rafael\'s good-pair joke,without making his opinion an objective relationship fact.',
(84,24):'Use Mr.Adernkatz for the generic respectful address;Master unnecessarily suggests a rank or profession.',
(84,30):'Keep Janus\'s uneasy reaction and hesitant name recollection without imposing an exact age from genericおじさん.',
(84,60):'Retain Claudio\'s fluent recognition,thanks and urgent request;replace only the full-width I artifact before fresh formatting.',
(84,93):'Retain the natural full introductions and exact FI/FA/FO substitution contract;replace only the full-width I artifact before fresh formatting.',
(84,137):'Explain Gerhard\'s admiral identity and strongest private pirate-hunting fleet in natural spoken sentences;do not invent a national navy or a new Grand Admiral rank.',
(84,140):'Keep the suppression of piracy across the named seas without claiming that every pirate literally vanished.',
(84,155):'Match source/current Manaus,not the old Manous body spelling;restore Gerhard checking the name and inviting the admiral and companions inside.',
(84,160):'Use Gerhard\'s source first person:he took in and trained Vels. The old this old man adds a self-reference absent here.',
(84,167):'Restore that Gerhard personally gave Vels the ship and subsequently resigned;replace the old passive/third-person account.',
(84,175):'Preserve the long-serving subordinates who deserted him for freedom and money,not just an ambiguous group of old comrades.',
(84,179):'Keep his uncertainty about his own strict,frugal leadership and his loss of confidence,not an assertion that discipline and thrift are intrinsically wrong virtues.',
(84,186):'Restore the first-person declaration that Gerhard abandoned the sea;the old passive The sea was abandoned before obscures who acted.',
(84,190):'Preserve first-person comfort,being left in peace and the emptiness of uneventful days;remove the non-source third-person this old man.',
(84,206):'Retain the explicit old-man self-deprecation where the source actually uses it,and the personal loss;preserve doubtful usefulness rather than an objective uselessness claim.',
(84,244):'Preserve Gerhard\'s judgment that he cannot imagine Rafael matching Vels,not a narrator\'s categorical assertion of inability.',
(84,277):'Express Rafael\'s personal conviction that Gerhard\'s methods were not wrong,not an impersonal proof that no method could have been wrong.',
(84,285):'Keep Rafael\'s own refusal to forgive Vels\'s greedy betrayal;the old passive wording weakens the personal conviction.',
(84,297):'Keep the proposal conditional and explain overconfidence as the reason a rumor may draw Vels out,rather than ordering Gerhard to spread news.',
(84,302):'Use Gerhard\'s own survival in first person;the source does not call him this old man here.',
(84,311):'Preserve personal responsibility and resolve to settle what he started;remove the third-person old-man phrasing.',
(84,319):'Preserve I am strict as Gerhard\'s warning,I won\'t go easy on you,not the fragment Harsh training.',
(84,327):'Make Rafael\'s appeal personal and positive:he wants Gerhard for more than defeating Vels,not the passive Your help is not wanted.',
(84,336):'Preserve Rafael\'s belief that they could achieve memorable deeds together without asserting an objectively guaranteed historic achievement.',
(84,358):'Restore Gerhard\'s first-person retirement and request to leave for today;the old passive sea sentence is unnatural.',
(84,381):'Retain the second physical persuasion branch and the same personal-conviction repair as277;do not merge alternative speeches.',
(84,389):'Keep Rafael\'s earnest plea,Teach us how you fight! Please!,without making I\'m asking you sound like an impatient demand.',
(84,398):'Restore Gerhard\'s strictness warning;Be ready alone loses that characterization.',
(84,458):'Use bow/stern and broadside naturally to explain the T tactic;Move before the ship is spatially awkward.',
(84,466):'Use the actual Aim skill and Gun Battery term and retain automatic gunnery during maneuvering;accuracy/gun deck obscure the referenced UI.',
(84,470):'Clearly contrast battle controls with ordinary sailing;Naval movement works as at sea is not a readable distinction.',
(84,473):'Use the reviewed Quarters caption instead of Marine Quarters and preserve refitting a hold at a town shipyard;formatter will remove the isolated hold line.',
(84,476):'Restore the explicit Swords skill and Boarding Leader assignment to Quarters,alongside extra crew.',
(84,480):'Tell the player to assign an officer with high Swords to Quarters,not merely a generic skilled fighter to an outdated room name.',
(84,483):'Retain automatic boarding on contact and the expected usefulness of the Boarding Leader,without turning a useful role into a guaranteed outcome.',
(84,527):'Apply the same bow/stern clarity in this second physical tutorial branch;retain both occurrences.',
(84,535):'Apply the same current Aim/Gun Battery terminology and automatic-fire explanation in the second branch.',
(84,539):'Keep the second system tutorial\'s ordinary sailing controls and automatic fire in range in readable complete prose.',
(84,542):'Apply reviewed Quarters terminology and continuous hold-refit wording in the second tutorial branch.',
(84,545):'Restore the second branch\'s explicit Swords/Boarding Leader/Quarters instruction and extra crew.',
(84,549):'Use the same exact Swords/Quarters assignment instruction in this repeated physical tutorial record.',
(84,552):'Retain the second physical boarding-contact explanation and the expected Boarding Leader benefit.',
(84,571):'Explain learning aboard ship in the player\'s own way,not the unintended personification that the ship itself must teach them.',
}

def logical_current(text):
    text=' '.join(text.split())
    for a,b in [('Ｉ','I'),('Ｆ','F'),('！','!'),('？','?'),('…','...')]:text=text.replace(a,b)
    if text and not text.strip('.'):text='...'
    return re.sub(r'\b(FI|FA|FO)\b',lambda m:'{MACRO:'+m[1]+'}',text)

if __name__=='__main__':
    target=ROOT/'B81_B84_325_whole_exchange_comparisons_v1.json';choice_target=ROOT/'B84_five_choice_comparisons_v1.json'
    assert not target.exists() and not choice_target.exists()
    draft_path=ROOT/'B81_B84_325_clean_meanings_andlogical_drafts_v1.json';draft,current=map(load,[draft_path,CURRENT])
    by={(g['block'],r['source_reference']['record_index']):r for g in current['groups'] for r in g['records']}
    assert len(by)==len(draft['records'])==325
    rows=[];glyphs=[]
    for original in draft['records']:
        row=deepcopy(original);key=row['block'],row['source_reference']['record_index'];old=by[key]
        assert row['source_hex']==old['source_hex'] and row['source_reference']==old['source_reference']
        keep=key[1] in RETAIN[key[0]];current_prose=logical_current(old['current_effective_text'])
        english=current_prose if keep else OVERRIDES.get(key,row['english'])
        assert english.isascii() and '  ' not in english and '\n' not in english
        assert all(english.count('{MACRO:'+m+'}')==count for m,count in row['source_macros'].items())
        if key not in FINDINGS:
            finding=(('Retain this clear,voice-appropriate response;it preserves ' if keep else
                'Recast the clipped or stiff current phrasing as natural complete-exchange dialogue,preserving ')+row['source_meaning'])
        else:finding=FINDINGS[key]
        assert not keep or english==current_prose
        pending=key==(81,106)
        row.update(english=english,independent_English_draft=original['english'],current_English=old['current_effective_text'],
            current_normalized_logical_English=current_prose,current_reference=old['current_reference'],current_hex=old['current_hex'],
            current_effective_hex=old['current_effective_hex'],current_catalogue_selected=old['current_catalogue_selected'],
            decision='retention' if keep else 'revision',finding=finding,retention_reason=finding if keep else None,localization_note=finding,
            review=dict(source=True,context=True,localization=not pending,naturalness=True,formatting=False),
            current_English_comparison_pending=False,current_English_now_exposed=True,earlier_English_unconsulted=False,
            native_name_controls_andterm_binding_pending=True,all_fresh_display_andintegration_pending=True,
            concrete_source_action_binding_pending=pending,retained_wording_exact_after_documented_glyph_normalization=keep,
            new_credit=0)
        chars={c:old['current_effective_text'].count(c) for c in set(old['current_effective_text']) if not c.isascii()}
        if chars:glyphs.append(dict(id=row['id'],block=key[0],source_record_index=key[1],current_reference=old['current_reference'],
            characters=chars,fullwidth_Latin_letters=sum(v for c,v in chars.items() if c in ['Ｉ','Ｆ']),
            ordinary_body_only_source_preamble_not_normalized=True,fresh_consumer_rendering_pending=True))
        rows.append(row)
    assert len(rows)==325 and sum(not r['review']['localization'] for r in rows)==1
    assert sum(r['fullwidth_Latin_letters'] for r in glyphs)==4
    save(target,dict(format='dk4-Rafael-four-whole-exchange-comparisons-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        source_drafts=str(draft_path),source_drafts_sha256=sha(draft_path.read_bytes()),current_binding=str(CURRENT),current_binding_sha256=sha(CURRENT.read_bytes()),
        current_ROM=current['current_ROM'],current_ROM_sha256=current['current_ROM_sha256'],current_archive_sha256=current['current_archive_sha256'],
        records=rows,records_count=325,proposed_revisions=sum(r['decision']=='revision' for r in rows),justified_retentions=sum(r['decision']=='retention' for r in rows),
        first_four_gates_passed=324,pending_source_action_record_IDs=[r['id'] for r in rows if not r['review']['localization']],
        glyph_findings=glyphs,fullwidth_Latin_letters_to_correct=4,fullwidth_Latin_records=3,
        source_ellipsis_andpunctuation_migration_consumer_verification_pending=True,
        name_consistency_decisions=['Cristina matches source/current name field7;replace body Christina in this scope.',
            'Mivor Genz matches source/current field79;replace body Gentz in full introduction.',
            'Claudio Manaus matches source/current field5;replace body Manous.',
            'Emilio Ferog full source introduction restored to match source/current field14.',
            'Sourceヘラルド retains existing body spelling Herald;no independent Latin attestation claimed.'],
        no_global_name_field_change_orapproval=True,all_fifth_gates_andregistered_integration_pending=True,
        new_credit=0,full_goal_complete=False,guide_photos=False,producer_sha256=sha(Path(__file__).read_bytes())))
    choice_current=load(CHOICES);choice_rows=[]
    for old in choice_current['records']:
        row=deepcopy(old);keep=(row['source_command_offset'],row['source_index']) in [(3114,1),(5298,2)]
        english=' '.join(row['current_stored_text'].split()) if keep else row['english']
        finding=('Retain the natural,contextually clear selectable intent: ' if keep else
            'Use a natural selectable answer that distinguishes this alternative: ')+row['source_meaning']
        if row['source_command_offset']==5298 and row['source_index']==1:finding+=' Preserve just/only;the old Hear him drops the distinction from undergoing training.'
        row.update(english=english,decision='retention' if keep else 'revision',finding=finding,
            retention_reason=finding if keep else None,localization_note=finding,
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
            current_English_andnative_caption_review_pending=False,native_caption_geometry_selection_anddisplay_pending=True)
        choice_rows.append(row)
    save(choice_target,dict(format='dk4-Rafael-five-choice-contextual-comparisons-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        current_binding=str(CHOICES),current_binding_sha256=sha(CHOICES.read_bytes()),records=choice_rows,records_count=5,
        proposed_revisions=3,justified_retentions=2,first_four_gates_passed=5,all_fifth_gates_andintegration_pending=True,
        new_credit=0,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
    print(dict(speeches=325,revisions=sum(r['decision']=='revision' for r in rows),retentions=sum(r['decision']=='retention' for r in rows),
        four_gate_passes=324,unresolved_bull_throw_action=1,typed_choices=5,choice_revisions=3,choice_retentions=2,
        fullwidth_Latin_letters=4,all_display_andintegration_pending=True))
