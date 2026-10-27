"""Source-grounded planning19/finance20 prose;no formatting/completion credit yet."""

from pathlib import Path
from shutil import copy2

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/planning_finance_v858')
ROM=Path('out/all_routes_combined_v855_candidate.nds')
MANUSCRIPT=Path('translations/planning_finance_editorial_manuscript_v1.json')
IDS=tuple(range(1447,1471))
PROSE={
1447:('Decides to think up the next scheme.',"Time to think up my next scheme...",'Restore the thought of devising the next scheme as a natural self-directed resolve.','revise'),
1448:('Mulls over this particular plan.',"Now, about this plan...",'Preserve the purposeful unfinished thought without inventing the plan\'s details.','revise'),
1449:('Wonders whether there is a good move or idea.',"Any bright ideas?",'Retain the idiomatic rhetorical brainstorming question;another speaker is not required.','retain'),
1450:('Needs more study to devise a good plan.',"I need to study more and come up with a good plan.",'Restore the personal need,more study,and the purpose of devising a good plan.','revise'),
1451:('Plans to devise a scheme,dozes off,and corrects the neru/devising versus neru/sleeping confusion.',"I'll dream up a plan... Zzz... Wrong kind of dreaming!",'Adapt the Japanese homophone joke through dream up a plan versus actual dreaming,preserving the dozing and comic correction without adding a speaker.','revise'),
1452:('Says experience counts when scheming.',"Schemes take experience.",'Retain the natural proverb-like observation;no age claim or earned experience-point change.','retain'),
1453:('Is surprised at being asked to scheme,but resolves to try hard.',"Me, scheming? ...I'll give it my best shot.",'Keep surprise,hesitation and a natural resolve to make an effort.','revise'),
1454:('Politely expresses confidence and asks others to expect good things from the plan.',"Count on my plan.",'Retain the natural assurance implied by the source expectation;no specific successful outcome is promised.','retain'),
1455:('Rafael resolves to study scheming too.',"I'll learn about scheming, too!",'Restore first-person resolve and too,keeping his enthusiasm and the intrigue context.','revise'),
1456:('Joakim says direct methods alone are insufficient and schemes also matter.',"Direct tactics aren't enough. Schemes matter, too...",'Restore the qualification alone and the importance of schemes;do not assert that direct tactics categorically fail.','revise'),
1457:('Lil confidently offers to handle schemes.',"Leave schemes to me!",'Retain the natural,emphatic boast.','retain'),
1458:('Maria says strategy is a strength.',"Strategy's my strength.",'Retain her natural confident statement;the broader source word for plans supports strategy here.','retain'),
1459:('Plans to investigate market prices at each port.',"Let's check the market prices at each port.",'Restore each port and market prices,without claiming that the information has already been collected.','revise'),
1460:('Reaffirms that watching market prices is essential.',"You really have to keep an eye on market prices...",'Express the reaffirmed attention idiomatically;generic you states a principle without adding an addressed character.','revise'),
1461:('Wonders approximately how much profit is being made this month.',"I wonder how much profit we're making this month.",'Restore a full personal question about this month and profit,without an amount or completed result.','revise'),
1462:('Complains that making money is difficult.',"Making money is hard!",'Retain the natural emphatic complaint.','retain'),
1463:('Considers market prices and admits not really understanding them.',"Market prices... Hmm, I don't really get them.",'Restore the lack of understanding,rather than implying there is no current price information.','revise'),
1464:('Wonders what is selling well now.',"What's selling well now?",'Retain the natural question and present-time reference.','retain'),
1465:('Wonders where selling goods would make a profit.',"Where could we sell goods for a profit...?",'Restore selling as the means of profit;name no cargo,ownership,price or completed trade.','revise'),
1466:('Turns to calculating this month\'s profit.',"Now then... I'll calculate this month's profit.",'Restore the month and accounting intention;no amount or completed calculation is invented.','revise'),
1467:('Rafael decides to understand the company\'s finances.',"I should get a clear picture of our finances.",'Use a natural resolve to understand finances without inventing a crisis or an executed financial action.','revise'),
1468:('Joakim considers this month\'s profit and pauses thoughtfully.',"This month's profit... Hmm...",'Restore this month and the purposeful unfinished accounting thought.','revise'),
1469:('Lil complains that the many numbers are overwhelming her.',"Ugh, all these numbers are making my head spin!",'Use the natural English idiom for being overwhelmed by so many numbers,without a literal illness or generic habit.','revise'),
1470:('Maria wonders which goods appear likely to be profitable now.',"Which goods look profitable right now...?",'Keep current timing and tentative profitability;avoid suggesting that goods themselves will profit.','revise'),
}


def main():
    assert not MANUSCRIPT.exists();ROOT.mkdir(parents=True,exist_ok=True)
    path=Path('work/analysis/planning_finance_v857/source_context_packet.json');packet=read(path)
    ledger=read('translations/editorial_review_current_v1.json')
    assert sha(ROM.read_bytes())==packet['candidate_sha256']==ledger['current_integrated_candidate']['sha256']
    assert ledger['records_editorially_completed']==732 and ledger['records_with_source_and_prose_pass']==735
    assert len(packet['all50_original_role_helper_selections'])==50
    sources={r['message_id']:r for r in packet['records_with_immediate_storage_neighbors']};rows=[]
    for n,(meaning,english,note,decision) in PROSE.items():
        source=sources[n];assert english==' '.join(english.split()) and english.isascii() and not any(c in english for c in '%{}\n')
        if decision=='retain':assert english==source['current_English'].strip()
        role,first,label=(19,1447,'Planning') if n<1459 else (20,1459,'Finance');index=n-first
        speaker=f'Native NPC voice class{index}' if index<8 else ['Rafael','Joakim (native captain1)','Lil','Maria'][index-8]
        rows.append({'id':f'COMMON_MESSAGE_{n}','message_id':n,'role_ID':role,
            'voice_class':index if index<8 else None,'protagonist_ID':index-8 if index>=8 else None,'speaker':speaker,
            'context':f'Independent {label}{role} work-flavor comment. Original NPC helper1278C selects eight voice alternatives;protagonist helper128B4 uses the real captain. Storage neighbors are alternatives,not consecutive speech. No scheme is executed,goods sold,funds credited or stats changed by this comment.',
            'source_Japanese':source['source_Japanese'],'source_hex':source['source_hex'],'source_reference':source['source_reference'],
            'canonical_source_hex':source['canonical_text_hex'],'current_reference':source['current_reference'],
            'current_text_hex':source['current_text_hex'],'current_English':source['current_English'],
            'source_meaning':meaning,'english':english,'localization_note':note,'editorial_decision':decision,
            'native_argument_count':0,'review':{'source':True,'context':True,'localization':True,'naturalness':True,'formatting':False}})
    assert tuple(r['message_id'] for r in rows)==IDS
    save(MANUSCRIPT,{'format':'dk4-natural-dialogue-source-manuscript-v2','translation_policy':'natural-dialogue-v2',
        'target_locale':'en-US','encoder':'dialogue-relocatable-v1','consumer_layout_profile':'deck-planning-finance-visible-v1',
        'review_gates':['source','context','localization','naturalness'],'formatting_review_pending':True,
        'status':'24-source-prose-reviewed-native-format-integration-and-actual-pending','file_path':'/COMMON/MESFILE.DK4',
        'source_clean_ROM_sha256':packet['source_clean_ROM_sha256'],'current_ROM':str(ROM),'current_ROM_sha256':sha(ROM.read_bytes()),
        'current_COMMON_sha256':packet['COMMON_sha256'],'current_ARM9_sha256':packet['ARM9_sha256'],
        'native_context_proof':str(path),'native_context_proof_sha256':sha(path.read_bytes()),'records':rows,'full_goal_complete':False})
    save(ROOT/'editorial_ledger_before_source_review.json',ledger)
    ledger['records_with_source_and_prose_pass']=ledger['records_with_source_prose_drafts']=759
    ledger['source_prose_reviewed_counts_by_file']['/COMMON/MESFILE.DK4']=758
    ledger['reviewed_but_incomplete_COMMON_IDs']=[750,751,752,*IDS]
    ledger['active_source_prose_drafts']={'native_message_IDs':[750,751,752,*IDS],
        'manuscripts':['work/analysis/market_contract_v758/unmapped_750_752_prose_DRAFT.json',str(MANUSCRIPT)],
        'status':'three-older-context-unmapped-and24-planning-finance-source-prose-reviewed-format-release-pending',
        'note':'These27 reviewed pending entries are not the full remaining unreviewed shared/route/player prose or raw-source scope.'}
    checkpoint=('V858 source/prose-reviews24 planning19/finance20 comments1447-1470:17 proposed revisions and7 retentions. '
        'Fifty original role selections cover all eight NPC voices and four real captains per duty. Drafts restore the planning/sleeping pun through dream up versus dreaming,the need for more study,schemes alongside direct tactics,each port,monthly profit,selling goods and current tentative profitability. '
        'Native formatting,registered integration and actual scenes remain pending. V855 stays current;732 complete and759 source/prose reviewed. Older750-752 and all unreviewed shared/route/player prose/raw coverage remain;graphics/all18 plaques and later older-record re-audit stay open;full goal active.')
    ledger['latest_checkpoint']=checkpoint
    ledger['planning_finance_v858']={'status':'source-prose-reviewed-native-layout-release-and-actual-pending',
        'native_message_IDs':list(IDS),'manuscript':str(MANUSCRIPT),'source_context_proof':str(path),
        'proposed_revisions':17,'justified_retentions':7,'completed_entries_added':0}
    ledger['research_checkpoints'].append({'id':'V858-Planning-Finance24-source-prose','proof':str(path),
        'manuscript':str(MANUSCRIPT),'new_source_prose_reviews':24,'completed_entries_added':0,
        'previous_goal_turn_classification':'progress:Livestock/Chapel24 completed and next24 source selectors mapped',
        'this_goal_turn_classification':'progress:24 faithful glosses,natural English reviews and exact source/current coverage references',
        'full_goal_complete':False})
    assert sum(ledger['source_prose_reviewed_counts_by_file'].values())==759
    save('translations/editorial_review_current_v1.json',ledger)
    doc=Path('docs/planning_finance_v858_source_review.md');doc.write_text('# V858: planning and finance source review\n\n'+checkpoint+'\n',encoding='utf-8')
    for p in map(Path,('docs/translation_progress.md','docs/editorial_review_goal.md','docs/todo.md','docs/known_issues.md')):
        with p.open('a',encoding='utf-8') as f:f.write('\n\n## V858: planning and finance source review\n\n'+checkpoint+' See [V858 source review](planning_finance_v858_source_review.md).\n')
    archive=Path('E:/Rota Nova translations/Editorial review/V858 Planning and finance source review');assert not archive.exists();copied=[]
    for source in (MANUSCRIPT,path,Path(__file__),doc,Path('translations/editorial_review_current_v1.json'),Path('scripts/prepare_planning_finance_context_v857.py')):
        target=archive/source.absolute().relative_to(Path.cwd());target.parent.mkdir(parents=True,exist_ok=True);copy2(source,target)
        assert sha(source.read_bytes())==sha(target.read_bytes());copied.append({'source':str(source),'archive':str(target),'sha256':sha(target.read_bytes())})
    save(ROOT/'archive_manifest.json',{'files':copied,'all_hashes_verified':True,'completed_entries_added':0})
    print('Planning/Finance24 source/prose reviewed:17 revisions,7 retentions.732 complete,759 source/prose reviewed;native/release/actual gates pending.',flush=True)


if __name__=='__main__':main()
