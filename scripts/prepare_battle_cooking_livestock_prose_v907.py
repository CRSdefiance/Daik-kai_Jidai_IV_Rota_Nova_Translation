"""Source-led review of25 independent battle Galley/Livestock comments."""

from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.battle_repair_medical_editorial import current_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.prepare_work_comments_v842 import reference
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/battle_cooking_livestock_v907')
ROM=Path('out/all_routes_combined_v904_candidate.nds')
MANUSCRIPT=Path('translations/battle_cooking_livestock_editorial_manuscript_v1.json')
IDS=tuple(range(1620,1645))
PROSE={
1620:('Says eating the speakers cooking will give the listener courage.',
      'My cooking will give you courage!',
      'Retain the natural personal encouragement. This is a cooking boast,not proof of a courage stat effect.','retain'),
1621:('Hesitantly suggests having a meal before battle.',
      'Perhaps a meal before battle...',
      'Restore the tentative suggestion. The deliberate trailing fragment conveys the source hesitation.','revise'),
1622:('Confidently says they can win if the listener eats this food.',
      'Eat this and victory is ours!',
      'Retain the natural confident food-and-victory boast,without asserting an actual buff or battle result.','retain'),
1623:('Reflects that people still get hungry even during battle.',
      'We still get hungry, even in battle...',
      'Preserve even-during battle and the reflective pause. The old wording incorrectly makes battle cause hunger.','revise'),
1624:('Roughly says one cannot fight on an empty stomach.',
      'No fighting on an empty belly!',
      'Retain the familiar blunt empty-belly idiom and informal voice.','retain'),
1625:('Hears there is a battle and decides to cook plenty.',
      "A battle, eh? I'd better cook plenty!",
      'Restore the personal intention and quantity. The source does not specify a lavish feast.','revise'),
1626:('Cheerfully urges hearty eating and vigorous action.',
      'Eat hearty and fight hard!',
      'Retain the natural casual American slogan. The battle context supplies fight for active effort.','retain'),
1627:('Considers making something special in preparation for a victory feast.',
      "Perhaps I'll make something special for the victory feast...",
      'Restore preparation and tentative personal intention. The feast is anticipated;victory has not already happened.','revise'),
1628:('Rafael wonders what he should cook to prepare for battle.',
      'What should I cook to get us ready for battle?',
      'Restore the personal planning question and preparation rather than a detached menu label.','revise'),
1629:('Hodram questions whether he should really be cooking in this situation.',
      'Should I really be cooking at a time like this...?',
      'Restore first-person ore and the uneasy question. The original does not refer to a separate generic cook.','revise'),
1630:('Lil complains about finding herself cooking during a battle.',
      'Why am I cooking in the middle of a battle?',
      'Restore her personal complaint instead of a general question about cooking tactics.','revise'),
1631:('Maria wonders whether delicious food might raise morale.',
      'I wonder if good food will boost morale...',
      'Keep the tentative thought and morale term. Remove inherited manual breaks and padding through the formatter;no guaranteed effect is asserted.','revise'),
1632:('Sera tells everyone to eat this before fighting.',
      'Everyone, eat this before battle.',
      'Preserve this food and an imminent battle,not a whole war. Use simple natural English without caricature. This is actor24s Galley-specific override.','revise'),
1633:('Says the pig is frightened by the sound of cannon fire.',
      'Cannon fire scares the pig.',
      'Retain the natural causal observation in the pig-care context.','retain'),
1634:('Says the speaker is lovingly cleaning or grooming the animal even during battle.',
      'Even in battle, I groom it with loving care.',
      'Restore the speakers ongoing personal care,not an instruction. Groom interprets migaku in pig-care context: ordinary1424 wipes it clean and battle1636 explicitly brushes it.','revise'),
1635:('Soothes the animal,says it will soon be over,and asks it not to get excited.',
      "Easy now. It'll be over soon. Don't get worked up.",
      'Restore the calm-down request and natural reassuring future. This comforts the pig rather than predicting the whole campaign.','revise'),
1636:('Insistently asks the animal to be still because the speaker will brush it.',
      'Hold still for the brush!',
      'Retain the natural impatient grooming command and implied imminent brushing.','retain'),
1637:('Roughly threatens to eat the animal if it keeps making such a racket.',
      "Keep making that racket and I'll eat you!",
      'Restore the personal comic threat. The source is not a passive rule that noisy pigs get eaten.','revise'),
1638:('Gently admonishes the animal not to make a fuss.',
      'Now, now. Settle down.',
      'Retain the natural gentle admonition and repeated soothing address.','retain'),
1639:('Emphatically insists that the speaker is not a pig.',
      "I'm telling you, I'm not a pig!",
      'Restore first-person oira;the old this one changes the referent. Ordinary1429 similarly protests I am not one of you. Do not invent a preceding spoken accusation.','revise'),
1640:('Observes that the pig still needs care even during battle.',
      'Even in battle, the pig still needs care.',
      'Restore the explicit even-in-battle contrast in a natural complete observation.','revise'),
1641:('Rafael says that in battle he could use even a pigs help.',
      "In battle, I could use even a pig's help.",
      'Adapt the cats-paw-help idiom to the sources pig joke. Preserve personal need and even;do not translate a literal animal hand.','revise'),
1642:('Hodram reflects that being with a pig makes it hard to feel tense.',
      "It's hard to feel tense with a pig around...",
      'Preserve the understated reflection. Ruins adds a negative judgment absent from the source.','revise'),
1643:('Lil exclaims about a panic caused by the loud noise and says she has had enough.',
      "All that noise has the pig in a panic! I've had enough!",
      'Restore her exasperation. The Japanese omits the panic subject;the assigned pig-care setting and neighboring cannon-fright lines support the pig as a contextual inference,not a claim that Lil herself panics.','revise'),
1644:('Maria tells the animal not to be scared,reassures it,and says the battle will soon end.',
      "Don't be scared. It's all right. The battle will be over soon.",
      'Restore the reassurance and natural future tense. This is comforting flavor dialogue,not a promised game outcome.','revise')}


def main():
    assert not MANUSCRIPT.exists()
    ROOT.mkdir(parents=True,exist_ok=True)
    packet_path=Path('work/analysis/battle_cooking_livestock_v906/source_context_packet.json')
    packet=read(packet_path);ledger=read('translations/editorial_review_current_v1.json')
    assert ledger['records_editorially_completed']==905 and ledger['records_with_source_and_prose_pass']==908
    assert sha(ROM.read_bytes())==packet['candidate_sha256']==ledger['current_integrated_candidate']['sha256']
    assert len(packet['all150_original_battle_helper_main_and_ordinary_control_selections'])==150
    assert packet['Sera_role15_battle1632_and_ordinary1422_overrides_proved']
    current,clean=map(NdsImage.open,(ROM,'work/clean.nds'))
    jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/__arm9__.bin'))
    en=current_entries(current.read_file('/COMMON/MESFILE.DK4'),current.read_file('/__arm9__.bin'))
    context=[]
    for n in (1410,1419,1421,1422,*range(1423,1435)):
        context.append({'message_id':n,'source_Japanese':jp[n].text.decode('cp932'),'source_hex':jp[n].text.hex(),
            'source_reference':reference(jp[n]),'current_English':en[n].text.decode('cp932'),
            'current_text_hex':en[n].text.hex(),'current_reference':reference(en[n]),
            'already_reviewed_ordinary_context_no_new_credit':True})
    context_path=ROOT/'ordinary_context_supplement.json'
    save(context_path,{'candidate_sha256':sha(ROM.read_bytes()),'source_clean_ROM_sha256':packet['source_clean_ROM_sha256'],
        'records':context,'battle_variants_are_independently_selected_not_a_conversation':True,
        'pig_grooming_interpretation_supported_by1424_and1636':True,
        'first_person_pig_protest_supported_by1429_and_source_oira1639':True})
    sources={r['message_id']:r for r in packet['records_with_immediate_storage_neighbors']};rows=[]
    for n,(meaning,english,note,decision) in PROSE.items():
        s=sources[n];role,first,label=(15,1620,'Galley') if n<=1632 else (17,1633,'Livestock')
        special=n==1632;index=n-first;hero=index-8 if 8<=index<12 else None
        voice=index if index<8 else None
        speaker='Sera (actor24 Galley override)' if special else f'Native NPC voice class{voice}' if hero is None else ['Rafael','Hodram Joakim Bergstrom (genuine captain1)','Lil','Maria'][hero]
        assert english==' '.join(english.split()) and english.isascii() and not any(c in english for c in '%{}\n')
        if decision=='retain':assert english==s['current_English'].strip()
        rows.append({'id':f'COMMON_MESSAGE_{n}','message_id':n,'role_ID':role,'voice_class':voice,
            'protagonist_ID':hero,'special_actor_ID':24 if special else None,'speaker':speaker,
            'context':f'Independent battle {label}{role} working comment. Original12600 chooses NPC alternatives and Sera24s Galley override;12720 chooses the genuine captain. Main12104 state0 chooses battle mode8/12=0/1 for eligible work comments;other source moods can select a different response. Storage neighbors are independent alternatives,not consecutive speech. Food boasts and pig-care comments do not establish a stat change or battle outcome.',
            'source_Japanese':s['source_Japanese'],'source_hex':s['source_hex'],'source_reference':s['source_reference'],
            'canonical_source_hex':s['canonical_text_hex'],'current_reference':s['current_reference'],
            'current_text_hex':s['current_text_hex'],'current_English':s['current_English'],
            'source_meaning':meaning,'english':english,'localization_note':note,'editorial_decision':decision,
            'native_argument_count':0,'review':{'source':True,'context':True,'localization':True,'naturalness':True,'formatting':False}})
    assert tuple(r['message_id'] for r in rows)==IDS and sum(r['editorial_decision']=='revise' for r in rows)==18
    save(MANUSCRIPT,{'format':'dk4-natural-dialogue-source-manuscript-v2','translation_policy':'natural-dialogue-v2','target_locale':'en-US',
        'encoder':'dialogue-relocatable-v1','consumer_layout_profile':'deck-battle-cooking-livestock-visible-v1',
        'review_gates':['source','context','localization','naturalness'],'formatting_review_pending':True,
        'status':'25-source-prose-reviewed-native-format-integration-and-actual-pending','file_path':'/COMMON/MESFILE.DK4',
        'source_clean_ROM_sha256':packet['source_clean_ROM_sha256'],'current_ROM':str(ROM),'current_ROM_sha256':sha(ROM.read_bytes()),
        'current_COMMON_sha256':packet['COMMON_sha256'],'current_ARM9_sha256':packet['ARM9_sha256'],
        'native_context_proof':str(packet_path),'native_context_proof_sha256':sha(packet_path.read_bytes()),
        'ordinary_context_supplement':str(context_path),'ordinary_context_supplement_sha256':sha(context_path.read_bytes()),
        'records':rows,'full_goal_complete':False})
    save(ROOT/'editorial_ledger_before_source_review.json',ledger)
    ledger['records_with_source_and_prose_pass']=ledger['records_with_source_prose_drafts']=933
    ledger['source_prose_reviewed_counts_by_file']['/COMMON/MESFILE.DK4']=932
    ledger['reviewed_but_incomplete_COMMON_IDs']=[750,751,752,*IDS]
    ledger['active_source_prose_drafts']={'native_message_IDs':[750,751,752,*IDS],
        'manuscripts':['work/analysis/market_contract_v758/unmapped_750_752_prose_DRAFT.json',str(MANUSCRIPT)],
        'status':'three-older-context-unmapped-and25-battle-cooking-livestock-source-prose-reviewed-format-release-pending',
        'note':'These28 reviewed pending entries are not the full remaining shared/routes/player prose or raw-source scope.'}
    checkpoint=('V907 source/prose-reviews25 battle Galley15/Livestock17 comments1620-1644:18 revisions and7 retentions. '
        'Original150 battle-helper/main/ordinary controls include Sera24s special1632/1422 override;an additional genuine mood-response1833 lead remains unreviewed. '
        'Restored first-person cooking and pig protest,preparation for a future victory feast,Sera offering this food before battle,and personal grooming and reassurance. '
        'Native layout,registered integration and actual scenes remain pending. V904 remains current;905 complete,933 source/prose reviewed. '
        'Older750-752,other shared/routes/player prose,raw coverage,special actors1885-1888,separate graphics/all18 plaques,Samwell header and later older-record re-audit remain open;full goal active.')
    ledger['latest_checkpoint']=checkpoint
    ledger['battle_cooking_livestock_v907']={'status':'source-prose-reviewed-native-release-and-actual-pending','native_message_IDs':list(IDS),
        'manuscript':str(MANUSCRIPT),'source_context_proof':str(packet_path),'proposed_revisions':18,'justified_retentions':7,'completed_entries_added':0}
    ledger['research_checkpoints'].append({'id':'V907-Battle-cooking-livestock25-source-prose','proof':str(packet_path),'manuscript':str(MANUSCRIPT),
        'new_source_prose_reviews':25,'completed_entries_added':0,
        'previous_goal_turn_classification':'progress:current V904 exact repaired676/677 preservation verified against earlier actual corrected scene',
        'this_goal_turn_classification':'progress:25 faithful glosses,natural English decisions,exact references and ordinary pig-care context',
        'full_goal_complete':False})
    assert sum(ledger['source_prose_reviewed_counts_by_file'].values())==933
    save('translations/editorial_review_current_v1.json',ledger)
    doc=Path('docs/battle_cooking_livestock_v907_source_review.md')
    with doc.open('x',encoding='utf-8') as f:f.write('# V907: battle cooking and livestock source review\n\n'+checkpoint+'\n')
    for d in map(Path,('docs/translation_progress.md','docs/editorial_review_goal.md','docs/todo.md','docs/known_issues.md')):
        with d.open('a',encoding='utf-8') as f:f.write('\n\n## V907: battle cooking and livestock source review\n\n'+checkpoint+' See [V907 source review](battle_cooking_livestock_v907_source_review.md).\n')
    archive=Path('E:/Rota Nova translations/Editorial review/V907 Battle cooking livestock source review')
    assert not archive.exists();copied=[]
    for source in (MANUSCRIPT,packet_path,context_path,Path(__file__),doc,Path('translations/editorial_review_current_v1.json')):
        target=archive/source.absolute().relative_to(Path.cwd());target.parent.mkdir(parents=True,exist_ok=True);copy2(source,target)
        assert sha(source.read_bytes())==sha(target.read_bytes());copied.append({'source':str(source),'archive':str(target),'sha256':sha(target.read_bytes())})
    save(ROOT/'archive_manifest.json',{'files':copied,'all_hashes_verified':True,'completed_entries_added':0})
    print('25 source/prose reviews:18 revisions,7 retentions.905 complete,933 source/prose;format/release/actual pending.',flush=True)


if __name__=='__main__':main()
