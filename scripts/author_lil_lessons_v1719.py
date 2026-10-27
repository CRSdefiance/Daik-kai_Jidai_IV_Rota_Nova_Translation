"""Source/context/prose review of60 tutorial speeches and four choice labels."""
from copy import deepcopy
from pathlib import Path
import re
import unicodedata

from dk4tool.dialogue.encoder import encode_fixed_dialogue
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_lessons_editorial_v1719')
PACKET=Path('work/analysis/lil_lessons_source_v1717/complete_lesson_source_context.json')
CHOICES=Path('work/analysis/lil_lesson_choices_v1718/native_two_choice_labels.json')
OUT=Path('translations/lil_lessons_editorial_manuscript_v1.json')
MENU=Path('translations/lil_lesson_choices_editorial_draft_v1.json')

# Chronological source objects include mutually exclusive nested branches.
# Each gloss precedes the proposed English and is based on the clean Japanese.
PROSE={
120:[
 (5,'Lil celebrates finally being at sea,enjoys the sea breeze and gull calls,and urges Camille to give everyone orders.',
  "We're finally at sea! I love the sound of the sea breeze and the gulls. Camille, hurry and give everyone their orders!",
  'Retain the existing reviewed-name catalog wording;use ordinary ASCII I under the proven guard,not a full-width workaround.'),
 (9,'Before giving orders,Camille says he will teach Lil how to handle the ship too.',
  'Before that, {MACRO:FI}, I need to teach you how to sail, too.',
  'Restore Camille as the teacher and Lil as the learner;keep the exact FI name substitution.'),
 (12,'Lil declines the lesson because she is not good at handling a ship.',
  "No thanks. I'm no good at that.",'Restore her stated lack of skill rather than a general dislike.'),
 (15,'Camille insists she learn despite her weakness because the future is uncertain and she must be prepared for emergencies.',
  "You still need to learn. We don't know what's ahead, so you have to be ready for an emergency.",
  'Keep the reason for learning and preparation for unforeseen trouble in natural spoken English.'),
 (19,'Lil reluctantly gives in to the lesson.', 'Ugh... All right!',
  'Retain the natural reluctant response.'),
 (23,'Camille begins by telling Lil to check which way the ship is pointing.',
  "Let's begin! Start by checking your ship's heading.",
  'Retain the clear existing heading instruction;source-native wrapping remains to verify.'),
 (27,'Lil is responsible for telling everyone the course the fleet should follow.',
  "{MACRO:FI}, you're the one who tells everyone which course the fleet should follow.",
  'Restore her responsibility and the fleet,rather than reduce the explanation to an immediate command.'),
 (31,'A ship must be pointed in the desired direction before it can travel that way.',
  "A ship won't go where you want unless you point it in that direction.",
  'Natural explanation of heading without adding a wind or sail mechanic.'),
 (36,'The ships travel direction can be set with the directional pad or stylus.',
  'Use the D-pad or stylus to steer.',
  'Retain the concise complete instruction;FE is a system-panel selector and needs its own native display review.'),
 (39,'Press the desired direction on the directional pad or touch the screen in that direction.',
  'Press the D-pad in the direction you want to go, or tap that direction on the screen.',
  'Make the screen direction explicit;preserve the two alternative controls.'),
 (42,'Camille asks whether Lil thinks she can manage the task.', 'Think you can do it?',
  'Retain the natural question.'),
 (62,'Camille privately worries whether Lil will be all right,then tells her Bruges is southwest of Amsterdam and encourages her.',
  '(Will she be all right?) Bruges is southwest of Amsterdam. Good luck!',
  'Retain the clear existing thought and spoken destination guidance;this is one conditional alternative,not a repeated consecutive speech.'),
 (80,'Camille privately worries whether Lil will be all right,then tells her Bruges is southwest of Amsterdam and encourages her.',
  '(Will she be all right?) Bruges is southwest of Amsterdam. Good luck!',
  'Retain matching wording for the identical source in this separate conditional branch.'),
 (109,'Camille privately worries whether Lil will be all right,then tells her Bruges is southwest of Amsterdam and encourages her.',
  '(Will she be all right?) Bruges is southwest of Amsterdam. Good luck!',
  'Retain matching wording for the identical source in this separate conditional branch.'),
 (134,'Camille praises Lil and says he is counting on her as admiral.',
  "Nice work! I'm counting on you, Admiral!",
  'Restore the spoken subject for smooth American English;retain the admiral address.'),
 (137,'Lil asks not to be distracted while she works out how to adjust the sails to the wind direction.',
  "D-don't distract me! Let's see... The wind's coming from over there, so I need to adjust the sails to match...",
  'Restore her hesitation and effort to reason through the wind direction;do not state an unsupported sail angle.'),
 (142,'Lil understands choosing a heading but wants to catch the wind and go much faster.',
  "Hmm... I get how to steer now, but I want to catch the wind and really pick up speed!",
  'Keep her personal wish and excited acceleration rather than turn it into a command to everyone.'),
 (146,'Camille says speed requires the sails to catch the wind properly and the next task is setting their angle.',
  'To do that, the sails need to catch the wind properly. Next, you need to tell everyone which way to turn them.',
  'Preserve her responsibility to give sail-angle orders as well as the reason for those orders.'),
 (150,'Lil stammers that this is a hassle.', 'Wh-what a hassle...',
  'Retain her reluctant voice and restore the source stammer.'),
 (155,'The L and R buttons control the sail angle,and adjusting the sails increases the ships speed.',
  'Turn the sails with L and R. Adjust them to increase your speed.',
  'Retain the existing complete button and speed explanation;FE display verification remains separate.'),
 (159,'Press L to rotate the sails left and R to rotate them right.',
  'Use L to turn the sails left, and R to turn them right.',
  'Retain both correctly paired directions and buttons.'),
 (163,'Stylus control automatically sets the optimal sail angle;touching the flagship stops it.',
  'When you use the stylus, the sails automatically turn to the best angle. Tap your flagship to stop.',
  'Restore the explicit automatic adjustment;retain the flagship stop instruction.'),
 (167,'Camille tells Lil to watch the wind direction and catch wind on the back of the sails relative to the ships heading.',
  "Watch the wind direction. With the ship's heading in mind, turn the sails so the wind hits them from behind.",
  'Keep the heading-relative explanation;do not invent a universal exact angle or reverse the wind-facing side.'),
 (171,'Lil is confused and is not sure she understands.', "Huh? I'm not sure I get it...",
  'Restore the hesitant uncertainty rather than the clipped Dont get it.'),
 (174,'Camille reassures her that practice will make it familiar and urges her to practice.',
  "You'll be fine once you get used to it. Come on, let's practice!",
  'Keep reassurance and friendly encouragement rather than an abrupt bare command.'),
 (177,'The onscreen speedometer shows speed;adjust the sails to maximize the bar to increase speed.',
  'Check your speed on the onscreen speedometer. To go faster, adjust the sails until the bar is as long as possible.',
  'Keep the speed indicator and maximum-bar instruction explicit.'),
 (186,'Camille privately worries whether Lil will be all right,then tells her Bruges is southwest of Amsterdam and encourages her.',
  '(Will she be all right?) Bruges is southwest of Amsterdam. Good luck!',
  'Retain matching wording for the identical destination guidance;no arrival at Bruges is asserted.'),
],
23:[
 (5,'Camille moves on to the next lesson.', 'Next up...',
  'Retain the natural conversational transition.'),
 (9,'Lil is surprised because she thought the lessons had already finished.',
  'What? I thought we were done!',
  'Correct the direction of her surprise;Were done already incorrectly sounds surprised that the lesson ended.'),
 (13,'Camille explains that the previous lesson covered ship handling and the next covers crew assignments.',
  'That was how to handle the ship. Next, we need to cover crew assignments.',
  'Use complete conversational sentences and distinguish the two lessons.'),
 (30,'If Lil already knows the material,Camille says he can safely leave it to her.',
  'Oh? Then I can leave it to you, right?',
  'Natural teasing confirmation for the skip-lesson branch,not an unconditional order.'),
 (40,'Lil complains that the lesson is a nuisance.', 'Ugh... What a pain.',
  'Natural reluctant complaint instead of the clipped A pain.'),
 (44,'Camille says being admiral is demanding and asks whether she would rather make him admiral.',
  'An admiral has a lot to do. Or would you rather put me in charge?',
  'Correct the role direction:Camille offers to become admiral;Want my job incorrectly treats him as the current admiral.'),
 (47,'Lil rejects the suggestion of making Camille admiral.', 'No way.',
  'Retain her firm natural refusal in the corrected exchange.'),
 (51,'Camille concludes that she must take the lessons seriously if she wants to stay in charge.',
  "Then you'll have to pay attention and learn.",
  'Use natural instruction rather than the overly literal Study properly.'),
 (54,'Lil gives a drawn-out reluctant assent.', 'Okaaay.',
  'Retain the deliberately drawn-out response as character voice.'),
 (58,'Camille will explain assigning officers to posts and their roles;each needs a duty for smooth voyages.',
  "I'll explain the different posts and what each one does. Assign each officer a job to keep our voyages running smoothly.",
  'Use officers consistently with current crew-role help;do not confuse all officers with the specific navigator function.'),
 (62,'Lil is the captain;a ship needs a captain to run smoothly,and she should stay in the captains cabin except during emergencies.',
  "You're the captain, of course, {MACRO:FI}. A ship needs its captain to run smoothly, so stay in the captain's cabin unless there's an emergency.",
  'Restore the direct address and complete emergency exception while preserving FI and the specific cabin.'),
 (65,'Sail Handlers adjust the sails relative to the wind;this is important and each mast needs one assigned officer.',
  'Next are the Sail Handlers. Their job is to adjust the sails to the wind. This is important work, and each mast needs one.',
  'Use the established Sail Handler role rather than sail master;retain the importance and one-per-mast requirement.'),
 (69,'When sails are set to Half Open,the Sail Handlers adjust them automatically.',
  'Set the sails to Half Open, and the Sail Handlers will adjust them automatically.',
  'Use the exact current HELP83 setting Half Open and the established crew role.'),
 (72,'Lil realizes Half Open means she need not issue sail-angle orders and wishes Camille had told her earlier.',
  "Oh! So if I set them to Half Open, I don't have to give any orders? You should have told me sooner!",
  'Keep her personal realization and mild complaint;use the full established setting name.'),
 (76,'Camille says Full Open will sometimes be necessary and she should practice now to avoid panicking then.',
  "Sometimes you'll need to sail at Full Open. Practice now so you won't panic when the time comes.",
  'Use the current full-setting label and retain preparation for a later need.'),
 (79,'Lil responds with a subdued noncommittal acknowledgment.', 'Hmm...',
  'Retain the natural muted response.'),
 (91,'The L and R buttons control sail angle;adjusting sails increases the ships speed.',
  'Turn the sails with L and R. Adjust them to increase your speed.',
  'Match the identical clean source in B120 R155,using clear button names and the same complete instruction.'),
 (95,'Stylus control automatically sets the optimal sail angle;touching the flagship stops it.',
  'When you use the stylus, the sails automatically turn to the best angle. Tap your flagship to stop.',
  'Match the identical source in B120 R163 and restore the automatic adjustment.'),
 (104,'A Helmsman turns the ship,an important task;a skilled one is needed to turn quickly.',
  'The Helmsman turns the ship, which is another important job. Choose someone skilled if you want the ship to turn quickly.',
  'Keep the importance of the role and the specific skill-to-turning-speed relationship.'),
 (107,'A skilled Helmsman can quickly move the ship into an advantageous position in naval combat.',
  'In battle, a skilled Helmsman can quickly maneuver the ship into a better position.',
  'Restore the speed of maneuvering rather than imply the officer personally seizes territory.'),
 (110,'A Surveyor enables Auto Move and provides fleet latitude and longitude;it is another important job.',
  "A Surveyor lets us use Auto Move and tells us the fleet's latitude and longitude. That's another important job.",
  'Preserve the exact Auto Move feature and explicitly identify the two coordinates.'),
 (120,'Fernando enthusiastically asks to be assigned as Lookout.',
  'Oh, right! Leave Lookout duty to me!',
  'Natural confident volunteering;do not imply he has already been assigned.'),
 (123,'Camille says Fernando is well suited to Lookout duty because of his Observation ability.',
  "Good idea. With your Observation, Fernando, you'd make a perfect Lookout.",
  'Restore the named addressee and ability-based suitability;Observation is the full ability term,not a new skill.'),
 (127,'Lil asks what a Lookout is.', 'A Lookout? What does that mean?',
  'Restore the explicit question that prompts Fernandos disbelief.'),
 (131,'Fernando incredulously asks how she can go to sea without even knowing what a Lookout does.',
  "Oh, come on! You're going to sea without even knowing what a Lookout does?",
  'Keep his exasperation and incredulous question as a complete spoken sentence.'),
 (135,'Lil tells him to be quiet and insists she only forgot briefly.',
  'Oh, be quiet! I only forgot for a moment!',
  'Restore her defensive subject and only;do not make the narrator endorse her excuse.'),
 (138,'Camille gently tries to calm both of them.', 'Easy, both of you...',
  'Retain his natural calming intervention.'),
 (142,'A Lookout checks and reports other ships affiliations and the state of cities while at sea.',
  'A Lookout checks which fleets other ships belong to and reports on cities while we are at sea.',
  'Restore affiliation identification missing from the generic nearby-ships draft;do not promise information about every enemy.'),
 (146,'Higher Observation allows discovery of cities and rare items over a wider area.',
  'The higher their Observation, the farther away they can spot cities and rare items!',
  'Preserve the wider detection range as a comparative mechanic rather than guarantee a specific discovery.'),
 (153,'Despite their suggestions,Lil has the final say over everyones assigned duties.',
  "But you're still the one who decides everyone's duties, {MACRO:FI}.",
  'Keep the contrast with their suggestions and use natural direct address with the genuine FI macro.'),
 (157,'This is enough for ordinary sailing;Camille wonders whether he explained too much at once.',
  'That covers an ordinary voyage. Hmm... Was that too much at once?',
  'Retain the natural wrap-up and self-conscious question.'),
 (161,'Lil says she will try it anyway.', "Well... I'll give it a try.",
  'Restore her own intention to try;Learn by doing incorrectly makes it a general maxim.'),
 (166,'Press X and select the Deck screen from the menu to change officers duties there.',
  "Press X and choose Deck from the menu. On the Deck screen, you can change each officer's post.",
  'Keep the X/menu/Deck sequence explicit and use the established role vocabulary.'),
]}


def visible(text):
    return re.sub(r'\s+',' ',unicodedata.normalize('NFKC',text)).strip()


if __name__=='__main__':
    assert not ROOT.exists() and not OUT.exists() and not MENU.exists()
    packet=read(PACKET);choice_proof=read(CHOICES);profile=get_dialogue_profile('lil-opening-editorial-native-v1')
    rows=[];layouts=[];menu_rows=[]
    for block in packet['blocks']:
        number=block['block'];proposals=PROSE[number]
        assert [r['record_index'] for r in block['records']]==[r[0] for r in proposals]
        for source,(index,meaning,english,note) in zip(block['records'],proposals,strict=True):
            row=deepcopy(source);prefix=row['source_presentation_prefix_hex']
            assert ('FI' in row['source_Japanese'])==('{MACRO:FI}' in english)
            expanded=english.replace('{MACRO:FI}','Lil')
            decision='retain-wording' if visible(expanded)==visible(row['current_native_macro_English']) else 'revise'
            row.update(source_meaning=meaning,english='{SPEAKER:'+prefix.upper()+'}'+english+'{PAD}',
                editorial_decision=decision,localization_note=note,
                context=f'Lil sailing tutorial,SC2 B{number},native speech at{row["source_reference"]["header_offset"]}. '
                    'B120 covers heading,wind and sail controls;B23 covers officer roles. Nested0100 ancestors identify conditional alternatives,not consecutive speeches. '
                    'Both whole source blocks and all surrounding speeches/choices were reviewed;native branch reachability and revised display remain pending.',
                review={'source':True,'context':True,'localization':True,'naturalness':True,'formatting':False})
            rows.append(row)
            try:
                value=encode_fixed_dialogue(bytes.fromhex(row['source_hex']),row['english'],profile)
                layouts.append({'id':row['id'],'historical_source_allocation_encodes':True,
                    'formatted_markup':value.formatted_markup,'padding_bytes':value.padding_bytes,
                    'diagnostics':[{'severity':d.severity,'code':d.code,'message':d.message} for d in value.diagnostics],
                    'native_glyph_bounds_pages_and_scene_review_pending':True})
            except ValueError as error:
                layouts.append({'id':row['id'],'historical_source_allocation_encodes':False,'error':str(error),
                    'faithful_prose_kept_intact_no_guard_relaxed':True,
                    'FE_requires_separate_native_panel_profile':prefix=='fe'})
        old,new=[next(r for r in choice_proof['cases'] if r['block']==number and r['version']==version) for version in ('clean','current')]
        proposals_menu=(['Count on me!','What about the wind?'] if number==120 else ["That's new to me...",'I already know that.'])
        glosses=(['Lil confidently volunteers that she can handle it.','Lil asks whether the wind needs to be considered.'] if number==120 else
            ['Lil says this is the first she has heard about crew assignment.','Lil says she already understands without needing an explanation.'])
        for jp,en,text,gloss in zip(old['labels'],new['labels'],proposals_menu,glosses,strict=True):
            assert jp['index']==en['index']
            menu_rows.append({'id':f'DK4_SC2_B{number:03d}_CHOICE_{old["command_offset"]:04X}_OPTION{jp["index"]}',
                'file_path':'/data/SC2.DK4','block':number,'command_offset':old['command_offset'],'option_index':jp['index'],
                'source_reference':{'offset':old['command_offset']+jp['relative_offset'],'bytes':len(bytes.fromhex(jp['hex']))},
                'current_reference':{'offset':new['command_offset']+en['relative_offset'],'bytes':len(bytes.fromhex(en['hex']))},
                'source_hex':jp['hex'],'source_Japanese':jp['text'],'current_text_hex':en['hex'],'current_English':en['text'],
                'english':text,'source_meaning':gloss,'speaker':'Lil (player choice)',
                'context':'Two-option response to Camille within the sailing/crew lesson. Original2100 choice count and both label pointers independently executed;original render/bounds/selected branch remain pending.',
                'localization_note':'Keep the short natural response and its original branch meaning;do not infer a selected branch from the label alone.',
                'editorial_decision':'retain-wording' if visible(text)==visible(en['text']) else 'revise',
                'review':{'source':True,'context':True,'localization':True,'naturalness':True,'formatting':False}})
    assert len(rows)==60 and len(menu_rows)==4
    ROOT.mkdir(parents=True)
    doc={'format':'dk4-natural-dialogue-source-manuscript-v2','translation_policy':'natural-dialogue-v2','target_locale':'en-US',
        'encoder':'dialogue-fixed-v1','dialogue_profile':profile.name,'file_path':'/data/SC2.DK4',
        'review_gates':['source','context','localization','naturalness','formatting'],'formatting_review_pending':True,
        'status':'60-source-context-prose-reviewed;FE-choices-branch-map-native-integration-and-actual-pending',
        'source_context':str(PACKET),'source_context_sha256':sha(PACKET.read_bytes()),
        'source_clean_ROM_sha256':packet['source_ROM_sha256'],'current_ROM':packet['current_ROM'],'current_ROM_sha256':packet['current_ROM_sha256'],
        'approved_names':['Rafael','Joakim','Maria','Camille'],'records':rows,
        'scope':'All27 B120 and33 B23 speech/system objects,including nested branches. Draft only;the B22 profile is an allocation probe,not FE or branch-release approval.'}
    try:validate_natural_dialogue_batch(doc)
    except ValueError as error:
        assert 'formatting' in str(error).lower()
        doc['release_validation_rejects_unapproved_formatting']=True
    else:raise AssertionError('Unreviewed formatting draft passed')
    save(OUT,doc)
    save(MENU,{'format':'dk4-editorial-typed-choice-source-draft-v1','translation_policy':'natural-dialogue-v2','target_locale':'en-US',
        'status':'four-label-source-prose-reviewed;native-render-branch-relocation-and-integration-pending',
        'records':menu_rows,'source_context':str(PACKET),'source_context_sha256':sha(PACKET.read_bytes()),
        'native_label_pointer_proof':str(CHOICES),'native_label_pointer_proof_sha256':sha(CHOICES.read_bytes()),
        'not_a_playable_or_generic_speech_batch':True,'full_goal_complete':False})
    save(ROOT/'allocation_probe_NOT_visual_approval.json',{'cases':layouts,
        'fixed_encodes':sum(r['historical_source_allocation_encodes'] for r in layouts),
        'fixed_failures':sum(not r['historical_source_allocation_encodes'] for r in layouts),
        'all9_FE_system_panels_require_independent_native_consumer_review':True,
        'nested0100_lengths_choice_offsets_branch_selection_and_external_references_unapproved':True,
        'no_ROM_registry_or_completion_change':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print({'speech_records':len(rows),'choice_labels':len(menu_rows),
        'proposed_revisions':sum(r['editorial_decision']=='revise' for r in rows+menu_rows),
        'retained_wordings':sum(r['editorial_decision']=='retain-wording' for r in rows+menu_rows),
        'fixed_encodes':sum(r['historical_source_allocation_encodes'] for r in layouts),
        'completed_entries_added':0},flush=True)
