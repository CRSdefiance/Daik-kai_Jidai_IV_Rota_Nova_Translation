"""Twenty-four independent source-grounded Livestock17/Chapel18 prose reviews."""

from pathlib import Path
from shutil import copy2

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/livestock_prayer_v853')
ROM=Path('out/all_routes_combined_v850_candidate.nds')
MANUSCRIPT=Path('translations/livestock_prayer_editorial_manuscript_v1.json')
IDS=tuple(range(1423,1447))
PROSE={
1423:('Gently asks the animal to grow big soon.',"Grow big soon, won't you?",'Restore soon and the gentle request without adding strength or a promised feeding result.','revise'),
1424:('Intends to wipe the animal clean.',"I'll wipe you clean...",'Keep the wiping action and self-directed resolve,rather than a generic invitation to clean.','revise'),
1425:('Laughs and remarks that the animal is cute.',"Ha ha! You're cute.",'Make the affectionate observation natural and complete while retaining the laugh.','revise'),
1426:('Fondly asks the little pig to grow big soon.',"Grow big soon, little pig.",'Retain the friendly animal address and restore the source soon;no human kinship or new animal is added.','revise'),
1427:('Gruffly tells the restless animal to stop moving around.',"Hold still, will you?!",'Retain the natural impatient imperative;it conveys the source warning and complaint about movement.','retain'),
1428:('Reflects that wiping the animal brings growing affection.',"I'm getting attached to you as I wipe you down.",'Restore both attachment and the act that prompts it;do not reduce the remark to a detached expression of fondness.','revise'),
1429:('Reacts in alarm and protests that he is not one of the animals.',"Whoa! I'm not one of you!",'Restore the explicit first-person denial in a natural comic reaction,without inventing what the pig did.','revise'),
1430:('Thinks this looks likely to grow into an excellent pig.',"Looks like you'll grow into a splendid pig.",'Keep the prospective growth and tentative looks like;do not invent a prize or make the prediction certain.','revise'),
1431:('Kindly offers to clean the animal.',"Let me clean you up.",'Retain Rafael\'s natural,gentle offer;the source does not require a more technical washing term.','retain'),
1432:('On closer inspection,the second protagonist finds the animal cute.',"You're cute, now that I get a good look...",'Preserve the change in assessment after looking carefully,rather than asserting physical closeness alone.','revise'),
1433:('Lil squeals and asks the animal not to rub its body against her.',"Eek! Don't rub up against me!",'Restore the startled cry and physical rubbing-against action;the older rubbing me was ambiguous.','revise'),
1434:('Maria tells the animal to eat plenty and grow big.',"Eat plenty and grow big.",'Retain the natural instruction and both source actions.','retain'),
1435:('Begins the invocation in the name of the Father,the Son,and the Holy Spirit.',"In the name of the Father, and of the Son, and of the Holy Spirit...",'Restore the full familiar English invocation instead of compressing its three named persons into Holy Trinity. Author no line breaks;the compiler must fit the complete wording.','revise'),
1436:('Says Amen with a lingering pause.',"Amen...",'Retain the complete conventional response and source hesitation.','retain'),
1437:('Cues himself to pray.',"Time to pray...",'Retain the natural self-directed cue;mechanical repetition of prayer is unnecessary.','retain'),
1438:('Asks God to hear the speaker\'s prayer or wish.',"God, please hear my prayer.",'Make the personal request explicit in natural prayer language;do not invent the content of the wish.','revise'),
1439:('Casually considers praying for a change,as an occasional act.',"Maybe I'll pray for a change!",'Restore the occasional for-a-change nuance and offhand decision;do not imply a new conversion or regular observance.','revise'),
1440:('States that religious faith is everything.',"Faith is everything.",'Use faith for the religious source term in the Chapel context,rather than generic belief.','revise'),
1441:('Became sleepy while reading the Bible.',"I got sleepy reading the Bible.",'Restore the Bible and this past occurrence;do not claim that all reading habitually makes the speaker sleepy.','revise'),
1442:('Addresses God in an act of confession.',"Lord, I confess my sins...",'Render the explicit confession naturally;my sins supplies the ordinary implied object without inventing any particular offense.','revise'),
1443:('Rafael wishes for Portugal\'s speedy recovery or restoration.',"May Portugal recover soon.",'Keep national recovery and the source soon;do not add a conquest or named political settlement.','revise'),
1444:('The second protagonist asks God whether he can build the strongest fleet.',"God, will I be able to build the strongest fleet?",'Restore the first-person question about ability and the strongest fleet. The old grant us a fleet changed both intent and subject.','revise'),
1445:('Lil asks God to protect her group.',"God, keep us safe.",'Retain the natural brief request and inclusive us.','retain'),
1446:('Maria wishes that everyone can sail safely.',"May we all sail safely.",'Retain the natural inclusive wish for safe sailing;no new destination or outcome is introduced.','retain'),
}


def main():
    assert not MANUSCRIPT.exists();ROOT.mkdir(parents=True,exist_ok=True)
    context=Path('work/analysis/livestock_prayer_v852/source_context_packet.json');packet=read(context)
    ledger=read('translations/editorial_review_current_v1.json')
    assert sha(ROM.read_bytes())==packet['candidate_sha256']==ledger['current_integrated_candidate']['sha256']
    assert ledger['records_editorially_completed']==708 and ledger['records_with_source_and_prose_pass']==711
    assert len(packet['all50_original_role_helper_selections'])==50
    sources={r['message_id']:r for r in packet['records_with_immediate_storage_neighbors']};rows=[]
    for n,(meaning,english,note,decision) in PROSE.items():
        source=sources[n];assert english==' '.join(english.split()) and english.isascii() and not any(c in english for c in '%{}\n')
        if decision=='retain':assert english==source['current_English'].strip()
        role,first,label=(17,1423,'Livestock') if n<1435 else (18,1435,'Chapel');index=n-first
        speaker=f'Native NPC voice class{index}' if index<8 else ['Rafael','Joakim (native captain1)','Lil','Maria'][index-8]
        rows.append({'id':f'COMMON_MESSAGE_{n}','message_id':n,'role_ID':role,
            'voice_class':index if index<8 else None,'protagonist_ID':index-8 if index>=8 else None,'speaker':speaker,
            'context':f'Independent {label}{role} work-flavor comment. Original NPC helper1278C selects one of eight voices;original protagonist helper128B4 uses the actual captain. Storage neighbors are alternative speakers,not a consecutive conversation. No animal growth,religious conversion,inventory,stats or route outcome is caused by this comment.',
            'source_Japanese':source['source_Japanese'],'source_hex':source['source_hex'],'source_reference':source['source_reference'],
            'canonical_source_hex':source['canonical_text_hex'],'current_reference':source['current_reference'],
            'current_text_hex':source['current_text_hex'],'current_English':source['current_English'],
            'source_meaning':meaning,'english':english,'localization_note':note,'editorial_decision':decision,
            'native_argument_count':0,'review':{'source':True,'context':True,'localization':True,'naturalness':True,'formatting':False}})
    assert tuple(r['message_id'] for r in rows)==IDS
    save(MANUSCRIPT,{'format':'dk4-natural-dialogue-source-manuscript-v2','translation_policy':'natural-dialogue-v2',
        'target_locale':'en-US','encoder':'dialogue-relocatable-v1','consumer_layout_profile':'deck-livestock-prayer-visible-v1',
        'review_gates':['source','context','localization','naturalness'],'formatting_review_pending':True,
        'status':'24-source-prose-reviewed-native-format-integration-and-actual-pending','file_path':'/COMMON/MESFILE.DK4',
        'source_clean_ROM_sha256':packet['source_clean_ROM_sha256'],'current_ROM':str(ROM),'current_ROM_sha256':sha(ROM.read_bytes()),
        'current_COMMON_sha256':packet['COMMON_sha256'],'current_ARM9_sha256':packet['ARM9_sha256'],
        'native_context_proof':str(context),'native_context_proof_sha256':sha(context.read_bytes()),'records':rows,'full_goal_complete':False})
    save(ROOT/'editorial_ledger_before_source_review.json',ledger)
    ledger['records_with_source_and_prose_pass']=ledger['records_with_source_prose_drafts']=735
    ledger['source_prose_reviewed_counts_by_file']['/COMMON/MESFILE.DK4']=734
    ledger['reviewed_but_incomplete_COMMON_IDs']=[750,751,752,*IDS]
    ledger['active_source_prose_drafts']={'native_message_IDs':[750,751,752,*IDS],
        'manuscripts':['work/analysis/market_contract_v758/unmapped_750_752_prose_DRAFT.json',str(MANUSCRIPT)],
        'status':'three-older-context-unmapped-and24-livestock-prayer-source-prose-reviewed-format-and-release-pending',
        'note':'These27 reviewed pending entries are not the full unreviewed shared/route/player prose or raw-source scope.'}
    checkpoint=('V853 source/prose-reviews24 Livestock17/Chapel18 comments1423-1446:17 proposed revisions and7 retentions. '
        'Fifty original role-helper selections cover all eight NPC voices and four actual captains for each duty. '
        'Drafts restore cleaning-linked attachment,the explicit Father/Son/Holy Spirit invocation,the Bible,the act of confession,Portugal\'s speedy recovery and Joakim\'s question about building the strongest fleet. '
        'Formatting,integration and actual scenes remain pending. V850 remains current;708 complete and735 source/prose reviewed. '
        'Older750-752 and all unreviewed shared/routes/player prose/raw coverage remain;graphics/all18 plaques and later older-record re-audit remain open;full goal active.')
    ledger['latest_checkpoint']=checkpoint
    ledger['livestock_prayer_v853']={'status':'source-prose-reviewed-native-layout-release-and-actual-pending',
        'native_message_IDs':list(IDS),'manuscript':str(MANUSCRIPT),'source_context_proof':str(context),
        'proposed_revisions':17,'justified_retentions':7,'completed_entries_added':0}
    ledger['research_checkpoints'].append({'id':'V853-Livestock-Chapel24-source-prose','proof':str(context),
        'manuscript':str(MANUSCRIPT),'new_source_prose_reviews':24,'completed_entries_added':0,
        'previous_goal_turn_classification':'progress:Cooking13 completed in V850 and next24 source selectors mapped',
        'this_goal_turn_classification':'progress:24 faithful glosses,natural English reviews and exact source/current coverage references',
        'full_goal_complete':False})
    assert sum(ledger['source_prose_reviewed_counts_by_file'].values())==735
    save('translations/editorial_review_current_v1.json',ledger)
    doc=Path('docs/livestock_prayer_v853_source_review.md');doc.write_text('# V853: livestock and prayer source review\n\n'+checkpoint+'\n',encoding='utf-8')
    for path in map(Path,('docs/translation_progress.md','docs/editorial_review_goal.md','docs/todo.md','docs/known_issues.md')):
        with path.open('a',encoding='utf-8') as f:f.write('\n\n## V853: livestock and prayer source review\n\n'+checkpoint+' See [V853 source review](livestock_prayer_v853_source_review.md).\n')
    archive=Path('E:/Rota Nova translations/Editorial review/V853 Livestock and prayer source review');assert not archive.exists();copied=[]
    for src in (MANUSCRIPT,context,Path(__file__),doc,Path('translations/editorial_review_current_v1.json'),Path('scripts/prepare_livestock_prayer_context_v852.py')):
        dst=archive/src.absolute().relative_to(Path.cwd());dst.parent.mkdir(parents=True,exist_ok=True);copy2(src,dst)
        assert sha(src.read_bytes())==sha(dst.read_bytes());copied.append({'source':str(src),'archive':str(dst),'sha256':sha(dst.read_bytes())})
    save(ROOT/'archive_manifest.json',{'files':copied,'all_hashes_verified':True,'completed_entries_added':0})
    print('Livestock/Chapel24 source/prose reviewed:17 revisions,7 retentions.708 complete,735 source/prose reviewed;native/release/actual gates pending.',flush=True)


if __name__=='__main__':main()
