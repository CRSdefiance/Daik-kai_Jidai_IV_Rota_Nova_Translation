"""Source-first review of25 battle hobby comments;no formatting/completion credit."""

from pathlib import Path
from shutil import copy2

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.gunnery_deck_editorial import current_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.prepare_work_comments_v842 import reference
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/battle_personal_v891')
ROM=Path('out/all_routes_combined_v888_candidate.nds')
MANUSCRIPT=Path('translations/battle_personal_editorial_manuscript_v1.json')
IDS=tuple(range(1571,1596))
PROSE={
1571:('Rafael asks the listener to take courage from the music he plays.',
      'Let my music give you courage!',
      'Retain the fluent encouragement. This flavor comment does not promise a morale or statistic effect.','retain'),
1572:('Joakim judges that this battle will hardly require him to take part.',
      'This battle hardly needs me...',
      'Retain the natural confident dismissal and trailing reflection;do not invent a battle result.','retain'),
1573:('Lil snores,then complains that it is noisy.',
      'Zzz... Hey, keep it down!',
      'Retain the natural sleepy complaint and snoring. No extra dream or relationship is invented.','retain'),
1574:('Maria refuses to be flustered just because a battle is happening and takes a break.',
      "A battle's no reason to rush. Time for a break...",
      'Restore the explicit combat contrast. Ippuku means a break or refreshment and does not by itself prove smoking;remove the invented smoke. Her ordinary personal line1364 refers to tea,but this line does not specify a beverage.','revise'),
1575:('Janus reacts to a battle by considering consulting the book titled Naval Warfare Encyclopedia.',
      "A battle? Perhaps I'll consult the Naval Warfare Encyclopedia...",
      'Translate the explicit book title Kaizen Jiten as Naval Warfare Encyclopedia and retain hesitation. No matching established item-title translation was found in the searched glossary/item/equipment files;the exact Japanese title occurs once in clean COMMON. Do not invent a book effect.','revise'),
1576:('Claudio asks to be called when his turn to participate comes.',
      'Call me when you need me.',
      'Retain the natural request;when needed expresses the source occasion for his participation.','retain'),
1577:('Julio exhales with pleasure and says he cannot put down his alcohol even during battle.',
      "Ahhh! I'm not putting down my drink, even in battle!",
      'Preserve the stubborn drinking joke and pleased exhalation. Sake here is alcohol in general;the old rum invents a specific drink.','revise'),
1578:('Cristina calls for attention and identifies her dance as a battle dance.',
      'Look! This is my war dance!',
      'Retain the lively natural invitation and named dance;no combat effect is implied.','retain'),
1579:('Arcadius is startled by a naval battle and asks the listener to wait one more page.',
      'A sea battle?! Let me finish this page!',
      'Restore the request to wait while he reads another page. Finishing this page naturally conveys that immediate short delay.','revise'),
1580:('Camille suggests leisurely watching the sky together.',
      "Let's just watch the sky.",
      'Retain the calm natural shared suggestion;just carries the relaxed disregard for battle.','retain'),
1581:('Xien maintains composure and warns that becoming flustered means defeat.',
      'Stay calm... Panic means defeat.',
      'Retain the natural concise warning and pause without promising an actual combat calculation.','retain'),
1582:('Jam scoffs at the battle and values his fishing rod.',
      'A battle? Hmph! My fishing rod comes first.',
      'Use the established fishing hobby from ordinary1372 to identify the rod and make his dismissive priority sound natural. No fishing result is invented.','revise'),
1583:('Yukihisa politely asks for a moment because he is tending to his sword.',
      "Please wait a moment. I'm taking care of my sword...",
      'Restore the personal ongoing maintenance and polite delay. Do not specify sharpening or polishing when the source only says care.','revise'),
1584:('Cesare says he must put his valued model away.',
      "I'd better put my precious model away...",
      'Restore the personal intention and importance of the model,without inventing its type.','revise'),
1585:('Emilio munches and decides he needs to eat something in preparation for battle.',
      "Munch, munch... A battle? I'd better eat something first.",
      'Restore the personal thought and something-to-eat wording while preserving the chewing gag. No food or combat effect is invented.','revise'),
1586:('Angelo attends to his appearance before battle.',
      'Before battle, I have to look my best...',
      'Render midashinami as a natural personal grooming concern. His ordinary1376 concerns sea air spoiling his hair;do not add a specific grooming action here.','revise'),
1587:('Gerhard politely wonders whether his turn to participate has come yet.',
      'Is it my turn yet...?',
      'Restore a complete natural question and the source yet sense;avoid a clipped My turn fragment.','revise'),
1588:('Al makes two sharp training breaths and wonders whether any strong opponents are present.',
      'Hah! Hah! Any tough opponents around...?',
      'Interpret shi,shi as sharp exertion sounds in the proven fist-training hobby context1378,not the dismissive English Shoo. This contextual inference does not specify a particular punch or invent a challenger.','revise'),
1589:('Charles explains that he cannot leave his work until the experiment is finished.',
      "I can't stop until this experiment is finished...",
      'Restore a full personal explanation and the specific experiment. No ingredients or scientific result is invented.','revise'),
1590:('Carlo snores,half wakes at mention of battle,nods off,and snores again.',
      'Zzz... A battle...? (Nods off.) Zzz...',
      'Restore the explicit nodding-off stage direction as in his ordinary1380,keeping the sleepy interruption.','revise'),
1591:('Fernando offers to use cards to divine the outcome of this battle.',
      'Shall I read the cards for this battle?',
      'Restore the offer to tell the fortune;the old question asks whether cards can predict instead. Do not guarantee a correct prediction.','revise'),
1592:('Ian has a special technique in reserve for a duel.',
      "I've got a special move for a duel...",
      'Restore a complete colloquial personal statement while keeping the duel-specific special technique. Do not name the move or claim an unlock.','revise'),
1593:('Samwell sleepily reacts to battle,but cannot manage it because he is too full.',
      'Zzz... A battle...? Can\'t... Too full...',
      'Restore dame as the sleepy inability or refusal. Deliberate sleep-talk fragments are natural here;no extra meal or medical state is invented. The separate unresolved native header name is not cleared.','revise'),
1594:('Manuel is indignant that a battle interrupts him while he is making a model.',
      "A battle?! While I'm working on my model?!",
      'Restore the personal ongoing activity and incredulous interruption rather than an unnatural model-making label.','revise'),
1595:('Sera says fighting is bad and that the flowers are sad.',
      'Fighting is bad... The flowers are sad...',
      'Keep her gentle simple voice and personification;remove the stronger invented action of flowers weeping. Do not caricature her limited Japanese.','revise')}


def main():
    assert not MANUSCRIPT.exists()
    ROOT.mkdir(parents=True,exist_ok=True)
    context=Path('work/analysis/battle_personal_v890/source_context_packet.json');packet=read(context)
    ledger=read('translations/editorial_review_current_v1.json')
    assert ledger['records_editorially_completed']==856 and ledger['records_with_source_and_prose_pass']==859
    assert sha(ROM.read_bytes())==packet['candidate_sha256']==ledger['current_integrated_candidate']['sha256']
    assert len(packet['all125_original_selector_and_discriminating_control_cases'])==125
    current,clean=map(NdsImage.open,(ROM,'work/clean.nds'))
    jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/__arm9__.bin'))
    en=current_entries(current.read_file('/COMMON/MESFILE.DK4'),current.read_file('/__arm9__.bin'))
    ordinary=read('translations/personal_chatter_editorial_manuscript_v3.json')
    previous={r['message_id']:r for r in ordinary['records']}
    assert len(previous)==25
    title='海戦事典'.encode('cp932')
    title_matches=[r.message_id for r in jp if title in r.text]
    assert title_matches==[1575],title_matches
    supplement=[]
    for n in (1364,1365,1367,1372,1376,1378,1380,1381,1385):
        supplement.append({'message_id':n,'source_Japanese':jp[n].text.decode('cp932'),'source_hex':jp[n].text.hex(),
            'source_reference':reference(jp[n]),'current_English':en[n].text.decode('cp932'),
            'current_reference':reference(en[n]),'previous_review_speaker':previous[n]['speaker']})
    evidence=ROOT/'hobby_and_term_context.json'
    save(evidence,{'candidate_sha256':sha(ROM.read_bytes()),'source_clean_ROM_sha256':packet['source_clean_ROM_sha256'],
        'ordinary_hobby_source_controls':supplement,'clean_COMMON_exact_book_title_matches':title_matches,
        'book_title_is_translated_from_clean_source_not_an_external_official_title_claim':True,
        'Al_training_sound_interpretation_is_contextual_inference_from1378':True,
        'Maria_ippuku_does_not_prove_smoking':True,'producer_sha256':sha(Path(__file__).read_bytes())})
    sources={r['message_id']:r for r in packet['records_with_immediate_storage_neighbors']};rows=[]
    for n,(meaning,english,note,decision) in PROSE.items():
        s=sources[n];actor=n-1571;speaker=previous[1361+actor]['speaker']
        if actor==1:speaker='Joakim (native captain1)'
        assert english==' '.join(english.split()) and english.isascii() and not any(c in english for c in '%{}\n')
        assert bytes.fromhex(s['source_hex'])==jp[n].text and bytes.fromhex(s['current_text_hex'])==en[n].text
        assert (english==s['current_English'].strip())==(decision=='retain')
        rows.append({'id':f'COMMON_MESSAGE_{n}','message_id':n,'actor_ID':actor,'role_ID':12,
            'protagonist_ID':actor if actor<4 else None,'speaker':speaker,
            'context':'Independent battle-time personal hobby reaction. Original12104 uses126A8 when the original mode object fields8/12 are0/1;role12 Cabin with activity0 and personal activity1 both select1571 plus actor. Storage neighbors are independent actor alternatives,not consecutive dialogue. This flavor text performs no action or combat effect.',
            'source_Japanese':s['source_Japanese'],'source_hex':s['source_hex'],'source_reference':s['source_reference'],
            'canonical_source_hex':s['canonical_text_hex'],'current_reference':s['current_reference'],
            'current_text_hex':s['current_text_hex'],'current_English':s['current_English'],
            'source_meaning':meaning,'english':english,'localization_note':note,'editorial_decision':decision,
            'native_argument_count':0,'review':{'source':True,'context':True,'localization':True,'naturalness':True,'formatting':False}})
    assert tuple(r['message_id'] for r in rows)==IDS
    revised=sum(r['editorial_decision']=='revise' for r in rows);assert revised==18
    save(MANUSCRIPT,{'format':'dk4-natural-dialogue-source-manuscript-v2','translation_policy':'natural-dialogue-v2','target_locale':'en-US',
        'encoder':'dialogue-relocatable-v1','consumer_layout_profile':'deck-battle-personal-visible-v1',
        'review_gates':['source','context','localization','naturalness'],'formatting_review_pending':True,
        'status':'25-source-prose-reviewed-native-format-integration-and-actual-pending','file_path':'/COMMON/MESFILE.DK4',
        'source_clean_ROM_sha256':packet['source_clean_ROM_sha256'],'current_ROM':str(ROM),'current_ROM_sha256':sha(ROM.read_bytes()),
        'current_COMMON_sha256':packet['COMMON_sha256'],'current_ARM9_sha256':packet['ARM9_sha256'],
        'native_context_proof':str(context),'native_context_proof_sha256':sha(context.read_bytes()),
        'hobby_and_term_proof':str(evidence),'hobby_and_term_proof_sha256':sha(evidence.read_bytes()),
        'records':rows,'full_goal_complete':False})
    save(ROOT/'editorial_ledger_before_source_review.json',ledger)
    ledger['records_with_source_and_prose_pass']=ledger['records_with_source_prose_drafts']=884
    ledger['source_prose_reviewed_counts_by_file']['/COMMON/MESFILE.DK4']=883
    ledger['reviewed_but_incomplete_COMMON_IDs']=[750,751,752,*IDS]
    ledger['active_source_prose_drafts']={'native_message_IDs':[750,751,752,*IDS],
        'manuscripts':['work/analysis/market_contract_v758/unmapped_750_752_prose_DRAFT.json',str(MANUSCRIPT)],
        'status':'three-older-context-unmapped-and25-battle-personal-source-prose-reviewed-format-release-pending',
        'note':'These28 reviewed pending entries are not the full remaining shared/route/player prose or raw-source scope.'}
    checkpoint=('V891 source/prose-reviews25 battle-personal comments1571-1595:18 revisions and7 justified retentions. '
        'Original125 selector/control cases distinguish battle from ordinary personal comments and preserve four genuine captains. '
        'Review removes invented smoke/rum,restores the book title,reading delay,fishing priority,sword/model care,food/grooming thoughts,training breaths,experiment,nodding-off gag,card-reading offer,duel move,sleepy refusal and sad flowers. '
        'Native layout,registered integration and actual battle display remain pending. V888 remains current;856 complete,884 source/prose reviewed. '
        'Older750-752,additional special actors1885-1888,and all unreviewed shared/routes/player prose/raw coverage remain;separate graphics/all18 plaques,Samwell header and later older-record re-audit stay open;full goal active.')
    ledger['latest_checkpoint']=checkpoint
    ledger['battle_personal_v891']={'status':'source-prose-reviewed-native-release-and-actual-pending','native_message_IDs':list(IDS),
        'manuscript':str(MANUSCRIPT),'source_context_proof':str(context),'proposed_revisions':18,'justified_retentions':7,'completed_entries_added':0}
    ledger['research_checkpoints'].append({'id':'V891-Battle-personal25-source-prose','proof':str(context),'manuscript':str(MANUSCRIPT),
        'new_source_prose_reviews':25,'completed_entries_added':0,
        'previous_goal_turn_classification':'progress:V889 completed24 andV890 mapped125 battle selector/control cases;intervening user screenshot answer was read-only confirmation',
        'this_goal_turn_classification':'progress:25 faithful source glosses,natural English reviews and exact source/current references',
        'full_goal_complete':False})
    assert sum(ledger['source_prose_reviewed_counts_by_file'].values())==884
    save('translations/editorial_review_current_v1.json',ledger)
    doc=Path('docs/battle_personal_v891_source_review.md')
    with doc.open('x',encoding='utf-8') as f:
        f.write('# V891: battle personal source review\n\n'+checkpoint+'\n\n'
            'Each record is an independent actor alternative. No NPC is substituted for a captain. The retained ordinary hobby lines provide context for Maria,Julio,Jam,Angelo,Al,Carlo,Fernando and Sera. '
            'The Al sound interpretation is a documented contextual inference from his original fist-training line,not an assertion that a specific punch animation was observed. '
            'The original Japanese book title is translated directly;no external official English title is claimed. '
            'Actual battle initialization,complete fonts,visible bounds,transitions and exact registered reconstruction remain required. No new ROM or completion credit.\n')
    for p in map(Path,('docs/translation_progress.md','docs/editorial_review_goal.md','docs/todo.md','docs/known_issues.md')):
        with p.open('a',encoding='utf-8') as f:f.write('\n\n## V891: battle personal source review\n\n'+checkpoint+' See [V891 review](battle_personal_v891_source_review.md).\n')
    archive=Path('E:/Rota Nova translations/Editorial review/V891 Battle personal source review');assert not archive.exists();copied=[]
    for source in (MANUSCRIPT,context,evidence,Path(__file__),doc,Path('translations/editorial_review_current_v1.json')):
        target=archive/source.absolute().relative_to(Path.cwd());target.parent.mkdir(parents=True,exist_ok=True);copy2(source,target)
        assert sha(source.read_bytes())==sha(target.read_bytes());copied.append({'source':str(source),'archive':str(target),'sha256':sha(target.read_bytes())})
    save(ROOT/'archive_manifest.json',{'files':copied,'all_hashes_verified':True,'completed_entries_added':0})
    print('Battle personal25 source/prose reviewed:18 revisions,7 retentions.856 complete,884 source/prose;format/release/actual pending.',flush=True)


if __name__=='__main__':main()
