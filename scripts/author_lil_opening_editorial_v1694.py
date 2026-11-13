"""Full clean/current Lil opening review; prose draft is not release approval."""
import json
import re
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.encoder import encode_fixed_dialogue
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts.research_wedding_command_v676 import walk
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_opening_editorial_v1694')
ROM=Path('out/all_routes_combined_v1676_candidate.nds')
OUT=Path('translations/lil_opening_editorial_manuscript_v1.json')
SPEAKERS={2:'Lil Argot',9:'Camille',14:'Emilio',20:'Fernando'}
# Each gloss is checked against the complete original conversation, not the old English.
PROSE=[
 (19,"Hee hee! I finally got my trade permit! Just you watch--I'm going to make a fortune!",'Lil celebrates finally obtaining a trade permit and boasts that she will make a great deal of money.','Restore finally;keep her playful boast and exuberance.'),
 (23,'{MACRO:FI}! Wait! Wait for me!','Camille calls Lil by the original runtime name and urgently repeats his request to wait.','Keep the repeated plea and exact FI substitution.'),
 (26,"Come on, Camille! Hurry up and get the ship ready. We're setting sail right now!",'Lil impatiently tells Camille to hurry,prepare for departure,and leave immediately.','Use approved Camille;keep preparation and immediate departure as separate commands.'),
 (30,'Phew... Do we really have to leave today?','Panting,Camille objects that they need not depart this very day.','Natural rhetorical objection;do not invent a reason to delay.'),
 (33,"I didn't think they'd issue the permit so soon. We haven't even finished getting ready...",'Camille did not expect the permit to be issued so quickly,so preparations are still incomplete.','Restore his explanation and causal sequence;do not force a shortened fragment.'),
 (36,'Quit grumbling. Anyway...','Lil cuts off his grumbling and changes the subject.','Retain the existing natural wording;formatting remains unapproved.'),
 (40,"The permit's in my name, so that makes me captain of this ship, right?",'Lil reasons that because the permit is in her name,she should be the ships captain.','Keep her self-serving question,not a statement of a government rule.'),
 (44,'Huh? Oh... really?','Camille hesitantly questions her assertion.','Preserve his uncertainty rather than turn it into confident agreement.'),
 (48,"All hands to your stations! We're setting sail!",'Lil tells everyone to take their stations because they will depart immediately.','Use ordinary nautical commands without adding a new station assignment.'),
 (51,'Sail crew, set full sail! Weigh anchor!','Lil addresses the sail handlers,orders full sail,and orders the anchor raised.','Restore full sail and the addressed crew;preserve the original order of commands.'),
 (54,'...How did {MACRO:FI} of all people get a permit so easily?','Camille skeptically wonders how someone like Lil obtained the permit so readily.','Keep his skepticism and runtime name;do not add an accusation of bribery.'),
 (58,"Isn't it obvious? My enthusiasm won the officials over. Or maybe they were dazzled by my beauty!",'Lil claims her enthusiasm moved the officials,then playfully suggests her dazzling beauty may have swayed them.','Keep the officials and both alternative explanations;convey the musical teasing tone in the line.'),
 (61,'Yeah, yeah... But what are you going to do with a trade permit?','Camille dismisses her boasting and asks what she intends to do with the permit.','Keep the dismissive lead-in and practical question.'),
 (65,"What do you mean? With this, we can sign a contract with any city! The whole world's our market now!",'Lil says the permit lets them make contracts with any city,so the world can be their customers.','Restore the explicit city-contract mechanic missing from the old trade-with-any-city paraphrase.'),
 (69,"The whole world, huh? Why not keep trading around Amsterdam like we always have? What's wrong with that?",'Camille questions expanding worldwide and asks what is unsatisfactory about their familiar trade near Amsterdam.','Keep Amsterdam,continuity with their previous business,and his conservative skepticism.'),
 (72,'We barely make anything doing that! Across the sea, we could make a fortune!','Lil says their old way earns little,and overseas trade could bring a windfall.','Keep possibility rather than promise guaranteed riches.'),
 (76,"I don't know... I doubt getting rich is that easy.",'Camille doubts that striking it rich will be easy.','Natural hesitant skepticism,without adding a financial forecast.'),
 (79,"You just don't know when to give up, Camille.",'Fernando tells Camille he is still resisting the inevitable.','Restore the named addressee and render the idiom naturally.'),
 (83,"Fernando? You're coming too? I thought you said you'd never sail with us!",'Camille is surprised Fernando will come after emphatically refusing to travel with them.','Restore Fernando as the named addressee;retain the contradiction with his earlier refusal.'),
 (87,"Well... things happen. Anyway, let's get going.",'Fernando vaguely says there are reasons for his change of heart and urges departure.','Keep his evasiveness;do not invent those reasons.'),
 (90,"Hey, when are you going to give me something good to eat? I'm tired of waiting...",'Emilio asks when he will receive the promised delicious food and says he is tired of waiting.','Restore good food,rather than reduce the request to whether anyone eats.'),
 (94,'Emilio too?','Camille is surprised Emilio is also joining them.','Retain the natural short question;surrounding dialogue establishes its meaning.'),
 (98,"Yeah. He's strong, so I figured he'd come in handy. I lured him aboard with food.",'Fernando thought Emilios strength would be useful and enticed him with food.','Keep Fernando as the person who recruited him and the humorous food inducement.'),
 (102,'Quite a crew... Are we really going to be all right at sea?','Camille expresses misgivings about taking this remarkable collection of people out to sea.','Keep the ironic observation and apprehension without declaring them incompetent.'),
 (105,"Enough talk! Let's get going! Come on, Camille. Get to work!",'Lil cuts off discussion,insists on leaving,and playfully orders Camille to do his work.','Use approved Camille and preserve her brisk teasing authority.'),
 (109,"Sails are set and the anchor's up! Give us our orders!",'Fernando reports full sail and raised anchor and asks for instructions.','Use complete spoken nautical reporting,not the isolated Orders fragment.'),
 (112,'Oh, all right... Prepare the Arnhem to sail! Everyone to your stations!','Camille reluctantly gives the order to prepare the Arnhem for departure and take stations.','Preserve preparation as an order;the old Arnhem is ready changed the action into a status report.'),
 (116,"Now that's more like it! I'm counting on you!",'Lil praises his commanding appearance and says she is relying on him.','Natural encouraging praise;do not add a rank or relationship.'),
 (119,"Sigh... I'm worried about what we're in for.",'Camille sighs and worries about the future voyage.','Keep apprehension rather than assert a specific coming disaster.'),
 (123,'Heh. You say that, but who came along without much of a fight?','Fernando teases Camille that despite his complaints he readily came along.','Retain the teasing rhetorical question and his mild hypocrisy.'),
 (126,"I did promise to go if she got the permit...",'Camille explains that he had already promised to accompany Lil if she obtained the permit.','Restore the conditional promise;the preceding scene identifies Lil as the permit holder.'),
 (129,'The Netherlands is a new country. The government favors merchants to help strengthen the nation.','Fernando explains that the newly founded Netherlands encourages merchants to build national strength.','Restore the named country;do not add historical dates or outside explanations.'),
 (133,'Anyone can get a trade permit without much trouble.','Fernando says trade permits are easy for anyone to obtain.','Keep the broad claim as Fernandos explanation,not extra narrator commentary.'),
 (136,"S-so that's how it works...",'Camille stammers as he realizes the reason the permit was issued so readily.','Keep the realization and stammer.'),
 (140,'And apparently, that permit exempts profits at trading posts from taxes.','Fernando says it seems having the permit means profits at trading posts are not taxed.','Retain the apparent/hearsay qualification and profits,not all property or income.'),
 (144,'What? Really?!','Camille reacts with surprise and asks whether this is true.','Retain the existing natural exclamation.'),
 (148,"It's all part of the policy to encourage trade. So it's a tax-exemption permit, too.",'Fernando links the tax benefit to the trade-promotion policy and calls the document a tax-exemption permit as well.','Restore the explanation and dual function of the permit rather than a vague tax break.'),
 (152,'Oh, I see... No wonder {MACRO:FI} wanted it.','Camille understands why Lil wanted the permit.','Preserve the runtime FI macro and the conversational realization.'),
 (156,"You might as well give up. You've always been like this, haven't you?",'Fernando tells Camille to accept it and asks whether this has always been his pattern.','Keep the setup for the following joke about Lil,without inventing their shared history.'),
 (159,'Huh?','Camille asks what Fernando means.','Retain the natural short reaction.'),
 (163,"You're just destined to let her boss you around.",'Fernando jokes that Camille is fated never to be able to stand up to that woman,Lil.','Restore the teasing power dynamic;do not invent romance or kinship.'),
 (166,'N-no...','Camille protests with a stammer.','Retain the original hesitant protest and existing natural wording.'),
 (170,"Wait, where's {MACRO:FI}?",'Camille suddenly realizes Lil is missing and asks where she is.','Preserve the runtime name and transition into her private reflection.'),
 (175,'This is the city I grew up in... So much has happened here... But...','Lil reflects privately on her hometown and all that happened there,then trails off.','Restore a complete thought without inventing the unspecified events;do not copy the source-leading blank line.'),
 (179,"{MACRO:FI}! What's wrong?",'Camille calls to Lil and asks what is wrong.','Retain the natural question and exact runtime name.'),
 (182,"Oh... Camille. Sorry, sorry! It's nothing.",'Lil notices Camille,apologizes,and tells him nothing is wrong.','Use approved Camille and retain the repeated light apology.'),
 (186,"Really? Well... all right, then. We're ready to go.",'Camille accepts her reassurance and reports that their preparations are complete.','Keep his concern before the departure-readiness report.'),
 (190,'Come on! Give us the order!','Fernando urges her to give instructions quickly.','Use natural impatience rather than an abrupt new command role.'),
 (195,"All right, then... Arnhem, set sail! We're heading for the neighboring port of Bruges!",'Lil orders the Arnhem to depart for nearby Bruges.','Preserve the ship,destination,and neighboring-port detail;flag capacity issues rather than omit facts.'),
]


def visible(text):
    return re.sub(r'\s+',' ',text[1:].replace('FI','{MACRO:FI}')).strip()


if __name__=='__main__':
    assert not ROOT.exists() and not OUT.exists()
    clean,current=NdsImage.open('work/clean.nds'),NdsImage.open(ROM)
    assert sha(ROM.read_bytes())==read(ROM.with_suffix('.manifest.json'))['candidate_sha256']
    files=[r.read_file('/data/SC2.DK4') for r in (clean,current)]
    blocks=[IlnkContainer.parse(f).blocks[22] for f in files]
    parts=[b.split(b'\0') for b in blocks]
    assert len(parts[0])==len(parts[1])==207 and len(blocks[0])==len(blocks[1])==3000
    assert len(PROSE)==49 and len({r[0] for r in PROSE})==49
    walks=[walk(r.read_file('/__arm9__.bin'),b) for r,b in zip((clean,current),blocks,strict=True)]
    assert all(not w['error'] and w['stopped_offset']==w['logical_end']==3000 for w in walks)
    commands=[[r for r in w['rows'] if r['word']==0x4000] for w in walks]
    assert len(commands[0])==len(commands[1])==49
    assert [(r['offset'],r['word'],r['native_extent']) for r in walks[0]['rows']]==[(r['offset'],r['word'],r['native_extent']) for r in walks[1]['rows']]
    offsets=[{n:sum(len(p)+1 for p in pp[:n]) for n,_,_,_ in PROSE} for pp in parts]
    assert {c['offset']+5 for c in commands[0]}==set(offsets[0].values())
    profile=get_dialogue_profile('lil-story-b22-intro-probe')
    records=[];layout=[]
    for n,english,gloss,note in PROSE:
        source,before=parts[0][n],parts[1][n];at=offsets[0][n]
        assert offsets[1][n]==at and source[0]==before[0] and source[0] in SPEAKERS
        assert blocks[0][at-5:at]==blocks[1][at-5:at]==b'\0\x40\xff\xff\0'
        assert ('FI' in source.decode('cp932'))==('{MACRO:FI}' in english)
        markup='{SPEAKER:'+f'{source[0]:02X}'+'}'+english+'{PAD}'
        decision='retain-wording' if visible(before.decode('cp932'))==english else 'revise'
        records.append({'id':f'DK4_MES_B22_R{n:04d}','file_path':'/data/SC2.DK4','block':22,'record_index':n,
            'source_reference':{'offset':at,'bytes':len(source),'header_offset':at-5},
            'current_reference':{'offset':at,'bytes':len(before),'header_offset':at-5},
            'source_hex':source.hex(),'source_Japanese':source[1:].decode('cp932'),
            'current_text_hex':before.hex(),'current_English':before[1:].decode('cp932'),
            'source_presentation_prefix_hex':source[:1].hex(),'speaker':SPEAKERS[source[0]],
            'context':f'Complete Amsterdam opening,B22 chronological speech {len(records)+1} of49. Lil obtains her permit,Camille worries about departure,Fernando explains contracts and tax exemptions,and Lil leaves her hometown for Bruges. Original native speaker byte{source[0]:02X} and adjacent commands remain authoritative.',
            'source_meaning':gloss,'english':markup,'localization_note':note,'editorial_decision':decision,
            'review':{'source':True,'context':True,'localization':True,'naturalness':True,'formatting':False}})
        try:
            encoded=encode_fixed_dialogue(source,markup,profile)
            layout.append({'id':records[-1]['id'],'fixed_allocation_encodes':True,'formatted_markup':encoded.formatted_markup,
                'padding_bytes':encoded.padding_bytes,'diagnostics':[{'severity':d.severity,'code':d.code,'message':d.message} for d in encoded.diagnostics],
                'formatting_not_approved_without_complete_rendered_native_scene_review':True})
        except ValueError as error:
            layout.append({'id':records[-1]['id'],'fixed_allocation_encodes':False,'error':str(error),
                'faithful_prose_kept_intact_for_relocation_or_formatter_review':True})
    ROOT.mkdir(parents=True)
    packet={'format':'dk4-editorial-source-context-packet-v1','route':'Lil','file_path':'/data/SC2.DK4','block':22,
        'source_ROM':'work/clean.nds','source_ROM_sha256':sha(Path('work/clean.nds').read_bytes()),
        'current_ROM':str(ROM),'current_ROM_sha256':sha(ROM.read_bytes()),
        'source_file_sha256':sha(files[0]),'current_file_sha256':sha(files[1]),
        'source_block_sha256':sha(blocks[0]),'current_block_sha256':sha(blocks[1]),
        'original_and_current_native_walks':walks,'all49_native_speech_commands_exhaustively_accounted_for':True,
        'all90_native_command_offsets_words_and_extents_preserved':True,'records':records,
        'findings':['Literal Kamil remains in current R0026/R0182 despite approved Camille;other references omit the named addressee.',
            'R0065 loses the explicit city-contract mechanic;R0148 weakens the tax-exemption explanation.',
            'R0112 changes an order to prepare the ship into a claim that it is ready.',
            'Current manual line breaks,padding,small fragments,and omitted clauses need the full formatter/native/actual review.'],
        'linear_native_extent_walk_is_not_runtime_branch_reachability':True,'prose_draft_not_integrated_or_complete':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False}
    save(ROOT/'complete_opening_source_context.json',packet)
    doc={'format':'dk4-natural-dialogue-source-manuscript-v2','translation_policy':'natural-dialogue-v2','target_locale':'en-US',
        'encoder':'dialogue-fixed-v1','dialogue_profile':profile.name,'file_path':'/data/SC2.DK4',
        'review_gates':['source','context','localization','naturalness','formatting'],'formatting_review_pending':True,
        'status':'49-source-context-prose-reviewed;formatting-relocation-native-integration-and-actual-pending',
        'source_context':str(ROOT/'complete_opening_source_context.json'),'source_context_sha256':sha((ROOT/'complete_opening_source_context.json').read_bytes()),
        'source_clean_ROM_sha256':packet['source_ROM_sha256'],'current_ROM':str(ROM),'current_ROM_sha256':packet['current_ROM_sha256'],
        'scope':'Complete49-line Lil Amsterdam opening through departure for Bruges;retain original49 native speech commands and all control flow.',
        'approved_names':['Rafael','Joakim','Maria','Camille'],'records':records}
    try:validate_natural_dialogue_batch(doc)
    except ValueError as error:
        assert 'formatting' in str(error).lower(),str(error)
        doc['strict_build_validation_rejects_draft_until_formatting_review']=True
    else:raise AssertionError('Unapproved formatting draft passed release validation')
    save(OUT,doc)
    save(ROOT/'allocation_probe_NOT_visual_approval.json',{'cases':layout,'encodes':sum(r['fixed_allocation_encodes'] for r in layout),
        'pending':sum(not r['fixed_allocation_encodes'] for r in layout),'no_automatic_warning_waivers':True,'no_ROM_changed':True})
    print({'source_and_prose_reviewed':49,'revised_drafts':sum(r['editorial_decision']=='revise' for r in records),
        'retained_wording_drafts':sum(r['editorial_decision']=='retain-wording' for r in records),
        'native_commands_accounted':len(walks[0]['rows']),'fixed_encodes':sum(r['fixed_allocation_encodes'] for r in layout),
        'fixed_failures_kept_open':sum(not r['fixed_allocation_encodes'] for r in layout),'completed_entries_added':0})
