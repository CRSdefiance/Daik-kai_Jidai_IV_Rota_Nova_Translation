"""Natural English review of source-bound ceremony dialogue and result notices."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/ceremony_context_v806')
MANUSCRIPT=Path('translations/ceremony_editorial_manuscript_v1.json')
DOC=Path('docs/ceremony_editorial_v806_checkpoint.md')

# English,faithful source gloss,and the explicit localization decision.
TEXT={
64:('No business? Leave now.', 'Those with no business here must leave immediately.', 'Retain the natural terse refusal. Other shared consumers and exact presentation must be preserved before integration.'),
289:('A sense of peace fills you.', 'The player feels that their heart has become peaceful.', 'Retain the natural existing narration. This is the Church-role10 result,not an NPC speech.'),
290:('%s and the others had a remarkable experience: a journey into an unfamiliar spiritual world.', 'The named protagonist and companions have a valuable experience of being drawn into an unknown spiritual world.', 'Replace the unrelated trade-good instructions. Remarkable experience conveys the valued experience naturally;the journey is the source spiritual experience,not literal world-map travel.'),
291:('%s and the others gained valuable firsthand experience of a new culture.', 'The named protagonist and companions gain valuable direct experience of a new culture.', 'Use consistent party narration and preserve the firsthand cultural experience from helping with preparations.'),
293:('A gentle melody echoed deep within the hearts of %s and the others.', 'A peaceful melody resonates deep in the hearts of the protagonist and companions.', 'Restore the depth and echoing melody rather than merely saying it moves them. One original given-name argument remains.'),
294:('After enduring hunger, %s and the others glimpsed a new state of awareness.', 'After enduring hunger,the protagonist and companions glimpse a new state of mind or awareness.', 'Keep the hunger-to-awareness sequence and use the established party narration.'),
295:('%s and the others got a strenuous workout on land for the first time in a while.', 'The protagonist and companions exercise strenuously on land for the first time in some time.', 'Retain the accurate idiomatic existing wording;do not imply a real battle or add a specific injury.'),
1200:('A blessed day! Let us pray together.', 'Today is an auspicious or celebratory day;the priest invites the group to pray together.', 'Retain the natural religious invitation. Original53F9C makes this an offer with a real yes/no response.'),
1201:('Hmm? Have you come to take part in the ceremony?', 'The ritual officiant pauses and asks whether the group has come to participate in the rite.', 'Restore the opening hesitation and participation meaning in natural,slightly formal speech.'),
1202:('Come, let us sing a song of joy.', 'The priest invites everyone to sing a joyful song.', 'Retain the clear,faithful formal invitation.'),
1203:('Kneel there. Now... ahem.', 'The officiant orders the group to kneel,then clears their throat before beginning.', 'Retain the natural order and comic throat-clearing. It is reused by Temple chanting and a site rite.'),
1204:('Aaaah... Aaaah!', 'The officiant draws out repeated ah sounds.', 'Retain the extended vocalization;it is an intonation,not meaningful words or a pain/injury claim.'),
1205:('What?!', 'The protagonist reacts in surprise to the officiant vocalization.', 'This is a complete alternative reaction for hero indices0/1/3,not the first half of1206.'),
1206:('What was that?!', 'Lil exclaims in surprise and bewilderment at the sound.', 'The original table selects this entire reaction for Lil alone. Restore a complete utterance without joining neighboring selections.'),
1207:('(Unintelligible chanting...)', 'The officiant chants symbolic,unintelligible syllables.', 'The source supplies unreadable symbolic syllables and explicitly labels them incomprehensible. Preserve chanting and unintelligibility without inventing English lyrics or a real religious mantra.'),
1208:('???', 'The protagonist is confused by the unintelligible chant.', 'Retain the source comic punctuation as a self-contained reaction.'),
1209:('Huh???', 'Lil reacts with a bewildered huh to the unintelligible chant.', 'Retain the expressive existing reaction;it is the Lil alternative to1208.'),
1210:('Then help us with the preparations. Get started.', 'The officiant tells the group to begin helping with preparations immediately.', 'Keep the command to assist and the urgency,using natural English rather than implying the protagonist offered to help.'),
1211:('Help?', 'Rafael repeats the unexpected instruction to help.', 'Retain the straightforward surprised echo.'),
1212:('Help, you say?', 'Hodram incredulously repeats the demand to help.', 'Retain the gruff theatrical echo,which suits his reaction and adds no rank or relationship.'),
1213:('You mean help with the preparations?', 'Lil echoes the unexpected demand to help.', 'Replace You want to help?,which reverses the request. Preparations are supplied by the immediately preceding original1210 call.'),
1214:('Help out?', 'Maria repeats the instruction to help.', 'Retain the natural,brief echo.'),
1215:('Come on, keep working!', 'The officiant urges the group not to stop working.', 'Retain the natural impatient order.'),
1216:('...', 'The protagonist responds with silence or an ellipsis.', 'Retain the deliberate silent reaction. No empty page or authored blank line is intended.'),
1217:('(Ugh, what is this all about?)', 'Lil privately complains about the baffling situation.', 'Retain the idiomatic thought and annoyed tone.'),
1218:('God is always watching what you do.', 'The priest says God always observes the player actions.', 'Retain the accurate wording. This is the original Church-role10 priest response when the offer is unavailable or declined.'),
1219:('Are you here to take part in the %s ceremony?', 'The guard asks whether the group is participating in the ceremony associated with the supplied historic site.', 'Preserve the site-name modifier and the true yes/no choice. The source argument is a historic-site name,not a religion or a person.'),
1220:('All right. Go in.', 'The guard accepts the response and orders the party to enter.', 'Use the short authoritative gatekeeper instruction;the original next provider changes to the ritual officiant.'),
1221:('What business do you have at this site? If you have none, leave at once.', 'The guard asks the group business at the historic site and orders them away if they have none.', 'Restore the site reference and firm conditional warning in a complete natural paragraph.'),
1222:('Kaaaaaaah!', 'The officiant lets out a long,forceful kaah cry.', 'Preserve the prolonged phonetic cry without inventing meaningful words or a physical attack.'),
1223:('What?!', 'The protagonist reacts in shock to the forceful cry.', 'Use the same complete surprised reaction as the identical Japanese punctuation in1205.'),
1224:('Huh?', 'Lil gives a puzzled huh in response to the cry.', 'Replace the broken ! Ra fragment. The next chant1225 is a different NPC message,not a continuation of this hero reaction.'),
1225:('Haaaaah! (Unintelligible chanting.)', 'The officiant draws out a loud haaah and continues with forceful unintelligible syllables.', 'Retain the cry and explicit incomprehensibility. Do not invent a real prayer or combine this with1224.'),
1226:('Pilgrims, are you? Line up there and offer your prayers one at a time.', 'The officiant recognizes the group as pilgrims and directs them to line up and pray in turn.', 'Retain the accurate natural formal address and instructions.'),
1227:('Then join the circle of dancers.', 'The officiant tells the group to join the dancing circle.', 'Retain the idiomatic existing instruction.'),
1228:('Dancing?', 'The protagonist questions the instruction to dance.', 'Use the natural English activity echo instead of the ambiguous standalone Dance?.'),
1229:('What do you mean, dancing?', 'Lil indignantly questions what the officiant means by dancing.', 'Preserve the incredulous echo of the invitation,not a request to identify an unseen dance.'),
1230:('Clear your mind. Forget everything, and let this gentle music carry you away, body and soul.', 'The officiant asks the group to abandon distracting thoughts and surrender body and soul to a gentle swirl of music.', 'Use a natural musical metaphor while preserving the mental release,the gentle music,and body and soul.'),
1231:("Let the heat welling up deep inside you flow freely. Yes, that's it.", 'The officiant urges the group to release the hot flow rising from deep within their bodies and encourages them.', 'Keep the source spiritual/physical metaphor and encouragement without adding a doctrine or a new action.'),
1232:('Your fast begins now. Understood?', 'The officiant announces the beginning of fasting and demands acknowledgment.', 'Original53FE4 is ordinary speech,not a yes/no offer. Understood? preserves the rhetorical command without promising an actual player choice.'),
1233:('What?!', 'Rafael exclaims in surprise at the fasting or pilgrimage instruction.', 'Retain the natural existing startled reaction.'),
1234:('What did you say?!', 'Hodram reacts forcefully to the instruction.', 'Retain the accurate gruff reaction.'),
1235:('Whaaat?!', 'Lil gives a drawn-out exclamation of disbelief.', 'Retain the expressive existing wording.'),
1236:('... I suppose I have no choice.', 'Maria pauses,then resignedly accepts that it cannot be helped.', 'Use natural restrained resignation instead of the literal cannot-be-helped construction;normalize the old full-width first letter.'),
1237:('Now pray in silence.', 'The officiant directs the group to pray quietly.', 'Retain the natural existing instruction.'),
1238:('(Stomach rumbles...)', 'Rafael stomach rumbles during fasting.', 'Render the onomatopoeia as a clear parenthetical hunger sound caption,not a spoken grammatical sentence.'),
1239:('(Stomach rumbles...)', 'Hodram stomach rumbles during fasting.', 'Keep the same source sound as1238 while preserving its separate protagonist selection.'),
1240:("(I'm so hungry...)", 'Lil privately thinks that she is hungry.', 'Retain the natural English wording and normalize the old full-width I through the proper formatter.'),
1241:('...', 'Maria maintains a silent or restrained response during fasting.', 'Preserve the source ellipsis in the standard English font;no new words or blank pages.'),
1242:("We'll climb the sacred peak to collect holy water. Understood?", 'The officiant announces a climb to a sacred peak to collect holy water and seeks acknowledgment.', 'Keep the purpose and sacred water. This is ordinary53FE4 speech,so use a rhetorical acknowledgment rather than a new consent choice.'),
1243:("Follow me, then. Stay close so you don't get separated.", 'The officiant tells the party to follow and stay together.', 'Retain the accurate natural wording;replace the legacy full-width F with normal English through the approved native formatter.'),
1244:("Hurry! If we're not back before dark, the wild beasts will make a meal of us.", 'The officiant warns that failing to return before sunset will make the group prey to wild beasts and urges haste.', 'Restore the actual danger lost in beasts will find us. Make a meal of us is an idiomatic equivalent of becoming their prey,not a new event.'),
}


def main():
    assert not MANUSCRIPT.exists() and not DOC.exists()
    proof=ROOT/'native_context.json';context=read(proof)
    assert context['every52_source_ID_bound_to_original_caller'] and len(context['source_rows'])==52
    assert len(context['hero_table_selections'])==32 and len(context['complete_hero_wrapper_ABI_cases'])==32
    assert len(context['parent_dispatch_cases'])==270 and len(context['source_branch_cases'])==81
    assert set(TEXT)=={r['message_id'] for r in context['source_rows']}
    records=[];revisions=0
    for source in context['source_rows']:
        n=source['message_id'];english,meaning,note=TEXT[n]
        assert english==english.strip() and '\n' not in english and english.isascii()
        assert english.count('%s')==bytes.fromhex(source['source_hex']).count(b'%s')
        occurrences=[(i,event) for i,case in enumerate(context['source_branch_cases']) for event in case['events'] if event.get('message')==n]
        kinds={e['kind'] for i,e in occurrences};assert occurrences
        if kinds=={'protagonist_reaction'}:
            indices=sorted({e['hero_index'] for i,e in occurrences})
            speaker='Protagonist reaction: '+', '.join(context['hero_names'][i]['current_name'] for i in indices)
            scene='Original53BD8/53C6C four-protagonist table with first-valid fallback. This message is selected as a complete reaction;neighboring alternative IDs are not chronological halves of a sentence.'
        elif kinds=={'system_result_notice'}:
            speaker='System result narration,original546B8 modal consumer'
            scene='Original ceremony result notice after the indicated prayer,chant,preparation,dance,fast or climb sequence. A source%s argument is the current custom admiral given-name from virtual+0x20 and refers to the party via tachi. It is not a trade-good or faction description.'
        else:
            actor_ids=sorted({(e['speaker_actor']-(context['town_role_name_mappings'][0]['actor_pointer']-context['town_role_name_mappings'][0]['actor_ID']*32))//32 for i,e in occurrences})
            if n in (1200,1202,1218):speaker='Church-role10 priest,clean Japanese神父'
            elif n in (1219,1220,1221):speaker='Historic-site gatekeeper role11,clean Japanese衛兵'
            else:speaker='Ritual officiant role9,clean Japanese祭主'
            scene='Original source branches and NPC providers bind this line to '+speaker+'. Temple instructions alternate chanting/preparations;Church offers a prayer/song;accepted site entry changes from guard to officiant and selects one of five rites. Native day/offer selectors are verified,not inferred from neighboring storage.'
        args=['historic_site_name'] if n==1219 else ['current_admiral_given_name'] if n in (290,291,293,294,295) else []
        decision='retain' if english==' '.join(source['current_English'].split()) else 'revise'
        revisions+=decision=='revise'
        records.append(dict(id=f'COMMON_MESSAGE_{n}',message_id=n,interaction_group='Religious-ceremony-dialogue-and-original-result-notices',
            japanese=source['japanese'],source_hex=source['source_hex'],source_reference=source['source_reference'],
            current_text_hex=source['current_hex'],current_English=source['current_English'],current_reference=source['current_reference'],
            english=english+'{PAD}',source_meaning=meaning,speaker=speaker,context=scene,localization_note=note,
            source_context_case_indices=sorted({i for i,e in occurrences}),source_native_arguments=args,English_argument_source_indices=list(range(len(args))),
            decision=decision,review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
            status='source-context-and-prose-reviewed;native-formatting-production-integration-and-actual-scenes-pending'))
    save(MANUSCRIPT,dict(format='dk4-common-entry-manuscript-v1',translation_policy='natural-dialogue-v2',encoder='dialogue-fixed-v1',
        target_locale='en-US',file_path='/COMMON/MESFILE.DK4',review_gates=['source','context','localization','naturalness','formatting'],
        native_context_proof=str(proof),native_context_sha256=sha(proof.read_bytes()),
        source_current_pins={k:context[k] for k in ('candidate','candidate_sha256','source_ARM9_sha256','current_ARM9_sha256','source_RAM','source_RAM_sha256')},
        records=records,production_approval=False,whole_batch_completion_credit=False,ROM_changed=False,full_goal_complete=False,
        remaining=['Map and verify the distinct ordinary,protagonist and modal formatting contracts;preserve every argument and presentation control.',
            'Audit other shared64 consumers before changing its retained one-line presentation.',
            'Generate and inspect complete native layouts/fonts including all21 site names and all four protagonist cases.',
            'Integrate all changes through a registered combined release,full native copies and exact clean-input patch.',
            'Perform actual representative ceremony scenes,not merely source-branch interception;verify voices,notices,effects and returns.'],
        producer_sha256=sha(Path(__file__).read_bytes())))
    ledger_path=Path('translations/editorial_review_current_v1.json');ledger=read(ledger_path)
    assert ledger['records_editorially_completed']==550 and ledger['records_with_source_and_prose_pass']==553
    assert ledger['active_source_prose_drafts']['native_message_IDs']==[750,751,752]
    done={n for f in ledger['completed_editorial_families'] for n in f.get('native_message_IDs',[])};assert not set(TEXT)&done
    ledger['records_with_source_and_prose_pass']=605;ledger['records_with_source_prose_drafts']=605
    active=ledger['active_source_prose_drafts'];active['native_message_IDs']+=sorted(TEXT);active['manuscripts'].append(str(MANUSCRIPT))
    active['status']='750-752-context-unmapped;ceremony52-source-context-prose-reviewed-production-pending'
    active['note']='52 ceremony/refusal/result entries reviewed,with32 hero selections/32 wrapper ABI cases,270 NPC mappings and270 parent bindings. No formatting/integration/completion credit;three older750-752 contexts remain.'
    packet=ledger['next_ceremony_source_packet'];packet.update(native_IDs=sorted(TEXT),status='source-context-and-prose-reviewed;native-formatting-and-actual-scenes-pending',
        additional_scope=[64,289,290,291,293,294,295],excluded_unrelated_notice=292,manuscript=str(MANUSCRIPT),context_proof=str(proof),review_credit=52,completion_credit=0)
    for f in ledger['findings']:
        if f['id'] in ('COMMON1205-1206-possible-cross-selection-fragments','COMMON1224-1225-reaction-and-chant-boundary-lead','COMMON1213-help-request-subject-lead'):
            f.update(status='source-selector-and-sequence-proven;faithful-complete-English-drafted;integration-pending',proof=str(proof))
    ledger['findings'].append(dict(id='COMMON290-unrelated-trade-good-placeholder-in-ceremony-result',native_message_ids=[290],
        status='source-caller-and-given-name-argument-proven;faithful-result-drafted;integration-pending',proof=str(proof),
        detail='Original546B8 result290 describes a valuable unfamiliar spiritual experience after chanting/dance. Current trade-good instructions are unrelated;replace with source-based party narration and preserve the admiral given-name argument.'))
    summary=(f'V806 source/context/prose-reviews52 ceremony-related entries:45 spoken/reaction records plus shared refusal64 and six result notices289/290/291/293/294/295. '
        f'{revisions} proposed revisions/{52-revisions} retained wordings. Original32 hero selections/32 wrapper ABI cases,270 NPC role/name mappings,21 site names,81 source branches and270 parent date/site bindings pass. '
        '1205/1206 and1223/1224 are protagonist alternatives,not sentence halves;1213 is a response to a help order.290 unrelated trade-good placeholder is replaced in the draft. '
        'Original festival formula is modulo28,not30. Notice292 is an unrelated discovery message and is excluded. '
        '550 complete/605 source-prose/55 pending;no new ROM or completion credit. V803 remains current;actual ceremony/native production verification and wider goal remain unfinished.')
    ledger['latest_checkpoint']=summary;ledger['coverage_units'][0]['next']='Prototype all52 ceremony entries through distinct ordinary/hero/modal consumers,including site/admiral substitutions and shared64 preservation;then registered integration/copies/patch and actual ceremony samples. Continue remaining shared,old750-752 contexts,all routes and other prose.'
    ledger['research_checkpoints'].append(dict(id='V806-ceremony52-source-context-prose',documentation=str(DOC),new_source_prose_reviewed=52,new_editorially_completed=0,new_ROM=False,full_goal_complete=False))
    save(ledger_path,ledger)
    DOC.write_text('# V806: ceremony52 source,context and English review\n\n'+summary+'\n\n'
        '## Proven original context\n\n'
        'The45 original entries1200-1244 are supplemented by shared refusal64 and six notices actually called by these scenes. '
        '292 describes a trade discovery in a town and is not a ceremony result. The original53BD8 wrapper selects one of four protagonist messages,with first-valid fallback; '
        '1205 is for Rafael/Hodram/Maria and1206 for Lil.1223/1224 are likewise alternatives. '
        'The full wrapper binds the current admiral actor and original53C14 caller contract. These are complete utterances,not halves to join.\n\n'
        'Original61B44 derives the ceremony date as ((TownID+1) mod28)+1 and dispatches types9/10/11 to619A0/618E4/61570. '
        'The modulo30 assumption was rejected by native Town27 boundary evidence and the original92492493/divisor28 constants. '
        'Type9 alternates chanting and preparation work. Type10 offers prayer/song. Type11 asks the guard for site entry,then changes to the role9 officiant for one of five rites. '
        'Clean NPC descriptors identify role9祭主,role10神父 and role11衛兵;270 original town/role mappings preserve actual names. '
        '1219 receives a historic-site name from CB16C records,not a religion. Istanbul uses Cappadocia(index8). All21 supplied names are mapped;not every Town/type combination is claimed visitable.\n\n'
        'Result notices use546B8 and its distinct modal consumer. Most take the current admiral given-name from the original virtual+0x20 getter;289 has no argument. '
        '290 wrongly contains generic trade-good instructions in the current ROM. The new draft restores the spiritual-experience narrative. '
        '1232 and1242 use ordinary speech despite their rhetorical questions;the English introduces no new yes/no choice.\n\n'
        '## Evidence and limits\n\n'
        '`work/analysis/ceremony_context_v806/native_context.json` pins all52 clean/current records,code spans,32 selector cases,32 complete-wrapper ABI cases,270 NPC mappings,21 names,81 branch traces and270 parent bindings. '
        'Original choice/provider logic executes;UI/IO,action-animation,crew-effect and time calls are explicit interception boundaries. These are source-context tests,not emulator gameplay or verified stat outcomes. '
        '`translations/ceremony_editorial_manuscript_v1.json` has source/context/localization/naturalness approval;every formatting gate remains false. '
        'Ordinary paragraphs,protagonist reactions and modal result notices require their own original-consumer checks. Other64 consumers must retain their presentation contract.\n\n'
        'No playable ROM changed. Preserve frozen V803 and its exact patch until the new source-owned formatting,COMMON copies,registered release and actual ceremony checks pass. '
        'The whole editorial goal and separate graphics/18-plaque audit remain open.\n',encoding='utf-8')
    for name in ('todo','translation_progress','editorial_review_goal','known_issues'):
        p=Path('docs')/(name+'.md');text=p.read_text(encoding='utf-8');heading='## V806: ceremony52 source/context/prose review'
        assert heading not in text;p.write_text(text+'\n\n'+heading+'\n\n'+summary+' See [ceremony review](ceremony_editorial_v806_checkpoint.md).\n',encoding='utf-8')
    print(summary,flush=True)


if __name__=='__main__':main()
