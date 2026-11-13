"""Author32 faithful en-US paragraphs;native formatting/release gates stay open."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

CONTEXT=Path('work/analysis/battle_reactions_context_v1479/source_and_original_reaction_context.json')
OUT=Path('translations/battle_reactions_editorial_manuscript_v1.json')
# Faithful meaning is recorded before the localized wording.
REVIEW={
2147:('An upbeat acknowledgement that this is a battle.','A battle, then!','Retain the natural enthusiastic acknowledgement;then is an idiomatic response,not a new sequence of events.'),
2148:('A terse recognition of a battle,with the reflective question particle ka.','A battle, huh.','Use a brief reflective reaction rather than the stiff introductory comma in the current line;no uncertainty about the outcome is invented.'),
2149:('A cheerful battle reaction followed by a promise to do ones best.',"A battle! I'll give it my best!",'Retain the fluent wording;normalize the full-width Latin I to ordinary English in the unwrapped paragraph. Native macro/wrap safety still needs verification.'),
2150:('A speaker says a battle is their chance to take an active part.','A battle? This is my moment!','Retain the idiomatic confident claim;it does not promise victory or a particular combat skill.'),
2151:('An emphatic rough-voiced announcement that it is the speakers turn.',"It's my turn now!",'Retain the natural emphatic wording and normalize the full-width I;now conveys the immediate turn without adding a story event.'),
2152:('An older-sounding speaker emphatically recognizes a battle.','A battle, eh!','Retain the concise excited reaction and its conversational eh;no invented archaic grammar.'),
2153:('A buoyant informal announcement that it is the speakers turn.','My turn!','Use a lively English exclamation;remove the current huh,which can sound doubtful in this confident context.'),
2154:('A measured formal acknowledgement of a battle.','A battle, I see!','Retain the measured natural reaction;normalize the full-width I without changing the voice.'),
2155:('A confident request that others expect good work from the speaker.','You can count on me!','Retain the idiomatic assurance;no specific result or ability is added.'),
2156:('A concise offer to take care of the task.','Leave it to me.','Retain the fluent calm assurance and restrained punctuation.'),
2157:('An informal cheerful resolve to try ones best.',"I'll give it my best!",'Retain the natural resolve;normalize the full-width I and do not author a line break.'),
2158:('The speaker says the situation is exciting.','This is exciting!','Retain the natural delighted reaction without adding an attack or outcome.'),
2159:('An assertive announcement of ones turn and determination to do it.',"It's my turn! I'll get it done!",'Retain both emphatic ideas;normalize full-width I characters and leave wrapping to the native consumer.'),
2160:('An exuberant claim of being full of enthusiasm.',"I'm raring to go!",'Retain the idiomatic energetic boast and normalize the full-width I;do not invent a particular tactic.'),
2161:('A boast that a battle like this is as easy as breakfast.','A fight like this is a piece of cake!','Localize the asameshi-mae idiom with the equivalent English piece of cake;preserve like this and the boast without claiming a completed victory.'),
2162:('A mature conversational suggestion to get started.','Shall we begin?','Retain the natural measured suggestion;the inclusive we is idiomatic in a shared task.'),
2163:('A startled exclamation and question about what is happening.',"Whoa! What's going on?!",'Retain the fluent startled question;do not explain the cause that the speaker does not state.'),
2164:('An abrupt emphatic question about what has happened.',"What's happening?!",'Retain the terse alarm without inventing an attacker or specific injury.'),
2165:('A loud startled cry.','Whoa!!!','Retain the short cry and deliberate emphatic punctuation;it is a complete reaction rather than truncated prose.'),
2166:('A sudden frightened cry.','Aaaah!','Retain the natural English cry;no factual or gender claim is added.'),
2167:('A startled cry followed by repeated questioning of what is happening.',"Whoa! What's happening?!",'Retain the alarm and question;English intensity conveys the repeated nanda without awkward duplication.'),
2168:('An older-sounding repeated question expressing confusion.','What in the world?!','Retain the idiomatic confused exclamation without inventing archaic speech.'),
2169:('Three rapid repetitions of what,in alarm.','What? What? What?!','Retain the deliberate repetition and escalating punctuation,which are the source performance.'),
2170:('A stammering measured question about what is happening,ending hesitantly.',"W-what's going on here...?",'Retain the stammer and hesitant ending;here is a natural discourse word,not a new location fact.'),
2171:('A pained realization that the speaker has been injured.',"Ugh! I'm hurt!",'Use an immediate natural injury reaction rather than the stiff passive wording;do not specify a wound mechanism or severity.'),
2172:('A pained groan and realization of injury.',"Urgh... I'm hurt...",'Retain the subdued groan and hesitations;normalize full-width I to ordinary English.'),
2173:('A cry of pain followed by noticing bleeding.',"Ow! I'm bleeding...",'Retain both pain and the explicit bleeding,including the trailing hesitation;normalize the full-width I.'),
2174:('Repeated little cries of pain.','Ow, ow...','Retain the pained repetition without inventing an explicit diagnosis.'),
2175:('A rough frustrated exclamation after realizing something has gone badly,in the original injury branch.','Aw, damn it...','Render yacchimatta ka yo as frustrated injury-context speech. The current I messed up can imply tactical failure or personal blame;the source does not specify either. Mild damn it conveys the rough frustration without inventing a cause. Do not copy the source trailing LF.'),
2176:('A groan and realization that the speaker has been hurt.',"Ugh... I'm hurt...",'Use natural immediate speech instead of the clumsy passive Ive been hurt;retain the hesitation and injury meaning.'),
2177:('An alarmed drawn-out cry followed by noticing bleeding.',"Aah! I'm bleeding!",'Preserve the cry and explicit bleeding;use a natural panicked English exclamation and ordinary Latin I.'),
2178:('A hesitant formal admission that the speaker has suffered an injury.',"...I've been wounded.",'Retain the formal wording and initial hesitation;normalize the full-width I without adding blame or seriousness.')}

if __name__=='__main__':
    assert not OUT.exists()
    context=read(CONTEXT);canonical=NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    base=common_message_entries(canonical.read_file('/COMMON/MESFILE.DK4'),canonical.read_file('/__arm9__.bin'))
    assert context['all32_current_original_actor_selection_file_copy_printf_macro_entry_contracts_executed']
    by_id={n:f for f in context['families'] for n in f['native_message_IDs']};rows=[]
    for original in context['records']:
        if not original['selected']:continue
        row=deepcopy(original);n=row['message_ID'];family=by_id[n];meaning,english,note=REVIEW[n]
        assert english.isascii() and english==' '.join(english.split()) and not any(c in english for c in '{}%\n\r\t')
        row.update(id=f'COMMON_MESSAGE_{n}',message_id=n,source_family=family['family_lead'],
            speaker='Original actor object selected by its source eight-class voice table through53F0C',
            context=family['original_context'],consumer='original-actor-portrait-speech-after-selection-printf-and-macro-expansion',
            source_meaning=meaning,english=english,localization_note=note,
            editorial_decision='retain' if english==row['current_English'] else 'revise',
            canonical_source_hex=base[n].text.hex(),native_argument_count=0,source_native_macros=[],
            original_native_entry=family['original_entry'],original_native_parent=family['original_parent'],
            source_table=family['table'],source_voice=n-family['first_ID'],selector_stack_offset=family['selector_stack_offset'],
            authored_as_one_unwrapped_paragraph=True,
            review={'source':True,'context':True,'localization':True,'naturalness':True,'formatting':False},
            status='source-context-prose-reviewed;native-formatting-release-and-gameplay-pending')
        rows.append(row)
    assert [r['message_id'] for r in rows]==list(range(2147,2179))
    revised=sum(r['editorial_decision']=='revise' for r in rows)
    save(OUT,{'format':'dk4-native-common-editorial-v1','translation_policy':'natural-dialogue-v2','target_locale':'en-US',
        'encoder':'dialogue-relocatable-v1','consumer_layout_profile':'battle-reactions-actor-postmacro-v1',
        'file_path':'/COMMON/MESFILE.DK4','review_gates':['source','context','localization','naturalness','formatting'],
        'formatting_review_pending':True,'status':'32-source-context-prose-reviewed;native-release-gameplay-pending',
        'source_clean_ROM_sha256':context['source_ROM_sha256'],'current_ROM':context['candidate'],
        'current_ROM_sha256':context['candidate_sha256'],'current_COMMON_sha256':context['COMMON_sha256'],
        'current_ARM9_sha256':context['ARM9_sha256'],'source_context':str(CONTEXT),'source_context_sha256':sha(CONTEXT.read_bytes()),
        'source_original_actor_selections_preserved':True,'all32_original_source_has_no_printf_or_macro_arguments':True,
        'no_authored_line_breaks_or_alignment':True,'records':rows,'revised':revised,'retained':32-revised,
        'no_native_formatting_release_gameplay_or_completion_approval':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('32 source/context/prose reviews:',revised,'proposed revisions,',32-revised,'justified retentions. No integration or completion credit.')
