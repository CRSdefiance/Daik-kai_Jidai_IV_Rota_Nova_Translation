"""Faithful natural-English source review of24 survey/lookout alternatives."""

from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/survey_lookout_v873')
ROM=Path('out/all_routes_combined_v870_candidate.nds')
MANUSCRIPT=Path('translations/survey_lookout_editorial_manuscript_v1.json')
IDS=tuple(range(1499,1523))
PROSE={
1499:('A sextant helps surveying work progress.','A sextant makes surveying easier.','Express practical help naturally without inventing a measurement or result.','revise'),
1500:('The current position must always be known.','We must always know our current position.','Restore always,current position and the duty as a full formal thought.','revise'),
1501:('Is flustered about the current location and asks for a moment.','Huh? Where are we now? Hang on a second!','Keep the startled questions and brief request to wait;second is an idiomatic moment,not a timer.','revise'),
1502:('The current position can also be determined from stars.','You can work out our position from the stars, too.','Restore position and too;stars are a location reference,not destiny.','revise'),
1503:('Asks whether knowing the current location is all that is needed.','I just need to know where we are, right?','Restore the personal task confirmation,just and question.','revise'),
1504:('Surveying is a basic sailors skill.','Surveying is a basic skill for any sailor.','Express basic seamanship as a complete natural teaching statement.','revise'),
1505:('Acknowledges the surveyor role and promises to try hard.',"I'm the surveyor, right? I'll do my best.",'Restore personal effort instead of inventing impersonal competence.','revise'),
1506:('Acknowledges being the surveyor and dismisses the difficulty.',"I'm the surveyor, then. Easy enough.",'Restore personal role acknowledgment and the relaxed assurance.','revise'),
1507:('Rafael confirms that this tool is used for surveying.',"Surveying... I'm supposed to use this tool, right?",'Restore surveying and the self-confirming use of this tool;do not turn it into choosing which tool is right.','revise'),
1508:('Joakim explains determining current location from the suns position.',"Surveying uses the sun's position to tell us where we are.",'Restore surveying,the suns position as reference,and current location.','revise'),
1509:('Lil enthusiastically calls surveying basic seamanship.',"Surveying, right? That's basic seamanship!",'Restore the role acknowledgment and emphatic sailors basics.','revise'),
1510:('Maria explains determining current location from the sun and stars.','We use the sun and stars to work out where we are.','Restore calculating location instead of celestial bodies merely guiding us.','revise'),
1511:('Reassures the listener that the surroundings are being watched.',"I'm keeping watch. You can rest easy.",'Use a full natural personal reassurance;keeping watch conveys vigilance of the surroundings.','revise'),
1512:('Reports currently keeping watch on the surroundings.','Keeping watch now.','Retain the natural brief status report,including current timing.','retain'),
1513:('Will report immediately if anything abnormal happens.',"I'll let you know right away if anything's wrong.",'Restore the condition,immediate timing and personal offer.','revise'),
1514:('Sees far and reflects that the world is vast.','I can see so far... The world is huge!','Keep both the long view and amazed reflection on the worlds size.','revise'),
1515:('Enjoys being high up and the refreshing exhilarating feeling.','It feels great up here! What a rush!','Localize exhilaration naturally without inventing fear,illness or a fall.','revise'),
1516:('Will report immediately if something is discovered.',"I'll let you know right away if I spot anything.",'Restore the discovery condition and immediate report;a sighting need not be danger.','revise'),
1517:('Enjoys seeing far because of the height.','You can see so far from up here!','Restore the distant view and its connection with being up high.','revise'),
1518:('Repeats the watch duty and insists it is being done properly.',"On watch! I'm keeping a sharp lookout.",'Express repeated vigilance and confident proper performance idiomatically.','revise'),
1519:('Rafael will tell everyone if he spots anything.',"If I spot anything, I'll let everyone know.",'Restore finding something as the condition and everyone as recipients.','revise'),
1520:('Joakim urges vigilance for danger with the whole body.','Keep all your senses alert for danger.','Express whole-body vigilance through all senses;do not invent a supernatural danger detector.','revise'),
1521:('Lil reacts with delight at the good view.','Wow! What a view!','Retain the natural exclamation conveying her surprise and how well she can see.','retain'),
1522:('Maria expresses confidence in her eyesight and asks to be relied on.',"I've got sharp eyes. Leave it to me.",'Restore a full personal assurance while preserving confidence in her eyesight.','revise'),
}


def main():
    assert not MANUSCRIPT.exists();ROOT.mkdir(parents=True,exist_ok=True)
    path=Path('work/analysis/survey_lookout_v872/source_context_packet.json');packet=read(path)
    ledger=read('translations/editorial_review_current_v1.json')
    assert sha(ROM.read_bytes())==packet['candidate_sha256']==ledger['current_integrated_candidate']['sha256']
    assert ledger['records_editorially_completed']==784 and ledger['records_with_source_and_prose_pass']==787
    assert len(packet['all50_original_role_helper_selections'])==50
    sources={r['message_id']:r for r in packet['records_with_immediate_storage_neighbors']};rows=[]
    for n,(meaning,english,note,decision) in PROSE.items():
        source=sources[n];assert english==' '.join(english.split()) and english.isascii() and not any(c in english for c in '%{}\n')
        if decision=='retain':assert english==source['current_English'].strip()
        role,first,label=(3,1499,'Survey') if n<1511 else (1,1511,'Lookout');index=n-first
        hero=index-8 if index>=8 else None
        speaker=f'Native NPC voice class{index}' if hero is None else ['Rafael','Joakim (native captain1)','Lil','Maria'][hero]
        rows.append({'id':f'COMMON_MESSAGE_{n}','message_id':n,'role_ID':role,'voice_class':index if hero is None else None,'protagonist_ID':hero,
            'speaker':speaker,'context':f'Independent {label}{role} work comment. Original1278C chooses eight NPC voices;128B4 uses the genuine captain. Storage neighbors are independent alternatives,not consecutive speech. No measurement,discovery,report or gameplay action is performed by this flavor text.',
            'source_Japanese':source['source_Japanese'],'source_hex':source['source_hex'],'source_reference':source['source_reference'],
            'canonical_source_hex':source['canonical_text_hex'],'current_reference':source['current_reference'],
            'current_text_hex':source['current_text_hex'],'current_English':source['current_English'],
            'source_meaning':meaning,'english':english,'localization_note':note,'editorial_decision':decision,
            'native_argument_count':0,'review':{'source':True,'context':True,'localization':True,'naturalness':True,'formatting':False}})
    assert tuple(r['message_id'] for r in rows)==IDS and sum(r['editorial_decision']=='revise' for r in rows)==22
    save(MANUSCRIPT,{'format':'dk4-natural-dialogue-source-manuscript-v2','translation_policy':'natural-dialogue-v2','target_locale':'en-US',
        'encoder':'dialogue-relocatable-v1','consumer_layout_profile':'deck-survey-lookout-visible-v1',
        'review_gates':['source','context','localization','naturalness'],'formatting_review_pending':True,
        'status':'24-source-prose-reviewed-native-format-integration-and-actual-pending','file_path':'/COMMON/MESFILE.DK4',
        'source_clean_ROM_sha256':packet['source_clean_ROM_sha256'],'current_ROM':str(ROM),'current_ROM_sha256':sha(ROM.read_bytes()),
        'current_COMMON_sha256':packet['COMMON_sha256'],'current_ARM9_sha256':packet['ARM9_sha256'],
        'native_context_proof':str(path),'native_context_proof_sha256':sha(path.read_bytes()),'records':rows,'full_goal_complete':False})
    save(ROOT/'editorial_ledger_before_source_review.json',ledger)
    ledger['records_with_source_and_prose_pass']=ledger['records_with_source_prose_drafts']=811
    ledger['source_prose_reviewed_counts_by_file']['/COMMON/MESFILE.DK4']=810
    ledger['reviewed_but_incomplete_COMMON_IDs']=[750,751,752,*IDS]
    ledger['active_source_prose_drafts']={'native_message_IDs':[750,751,752,*IDS],
        'manuscripts':['work/analysis/market_contract_v758/unmapped_750_752_prose_DRAFT.json',str(MANUSCRIPT)],
        'status':'three-older-context-unmapped-and24-survey-lookout-source-prose-reviewed-format-release-pending',
        'note':'These27 reviewed pending entries are not the full remaining shared/route/player prose or raw-source scope.'}
    checkpoint=('V873 source/prose-reviews24 Survey3/Lookout1 comments1499-1522:22 proposed revisions and2 retentions. '
        'All50 original selections cover eight NPC voices and four genuine captains per duty. Drafts restore always/current position,surveyor effort,sun/star location determination,distant views,conditional immediate reports and natural whole-body vigilance. '
        'Native layout,registered integration and actual scenes remain pending. V870 remains current;784 complete,811 source/prose reviewed. Older750-752 and all unreviewed shared/routes/player prose/raw coverage remain;separate graphics/all18 plaques and later older-record re-audit stay open;full goal active.')
    ledger['latest_checkpoint']=checkpoint
    ledger['survey_lookout_v873']={'status':'source-prose-reviewed-native-release-and-actual-pending','native_message_IDs':list(IDS),
        'manuscript':str(MANUSCRIPT),'source_context_proof':str(path),'proposed_revisions':22,'justified_retentions':2,'completed_entries_added':0}
    ledger['research_checkpoints'].append({'id':'V873-Survey-Lookout24-source-prose','proof':str(path),'manuscript':str(MANUSCRIPT),
        'new_source_prose_reviews':24,'completed_entries_added':0,'previous_goal_turn_classification':'progress:Bridge duties28 completed inV870,next24 original contexts proved',
        'this_goal_turn_classification':'progress:24 faithful source glosses,natural English reviews and exact source/current references','full_goal_complete':False})
    assert sum(ledger['source_prose_reviewed_counts_by_file'].values())==811
    save('translations/editorial_review_current_v1.json',ledger)
    doc=Path('docs/survey_lookout_v873_source_review.md');doc.write_text('# V873: surveying and lookout source review\n\n'+checkpoint+'\n',encoding='utf-8')
    for p in map(Path,('docs/translation_progress.md','docs/editorial_review_goal.md','docs/todo.md','docs/known_issues.md')):
        with p.open('a',encoding='utf-8') as f:f.write('\n\n## V873: surveying and lookout source review\n\n'+checkpoint+' See [V873 review](survey_lookout_v873_source_review.md).\n')
    archive=Path('E:/Rota Nova translations/Editorial review/V873 Survey and lookout source review');assert not archive.exists();copied=[]
    for source in (MANUSCRIPT,path,Path(__file__),doc,Path('translations/editorial_review_current_v1.json'),Path('scripts/prepare_survey_lookout_context_v872.py')):
        target=archive/source.absolute().relative_to(Path.cwd());target.parent.mkdir(parents=True,exist_ok=True);copy2(source,target)
        assert sha(source.read_bytes())==sha(target.read_bytes());copied.append({'source':str(source),'archive':str(target),'sha256':sha(target.read_bytes())})
    save(ROOT/'archive_manifest.json',{'files':copied,'all_hashes_verified':True,'completed_entries_added':0})
    print('Survey/Lookout24 source/prose reviewed:22 revisions,2 retentions.784 complete,811 source/prose;native/release/actual pending.',flush=True)


if __name__=='__main__':main()
