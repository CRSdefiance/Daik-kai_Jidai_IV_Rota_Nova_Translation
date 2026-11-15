"""Record24 new source/prose reviews without native-format or completion credit."""

from pathlib import Path
from shutil import copy2

from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_work_comments_v842 import ROOT,ROM,MANUSCRIPT,IDS
from scripts.verify_village_wrap_v608 import read,save


def main():
    path=Path('translations/editorial_review_current_v1.json');ledger=read(path)
    assert ledger['records_editorially_completed']==671 and ledger['records_with_source_and_prose_pass']==674
    doc=read(MANUSCRIPT);proof=read(ROOT/'native_context.json')
    assert len(doc['records'])==24 and all(not r['review']['formatting'] for r in doc['records'])
    assert len(proof['all42_NPC_voice_selections_cover_all_eight_classes'])==42
    assert len(proof['all8_real_protagonist_group_selections'])==8
    assert doc['current_ROM_sha256']==sha(ROM.read_bytes())==ledger['current_integrated_candidate']['sha256']
    save(ROOT/'editorial_ledger_before_checkpoint.json',ledger)
    ledger['records_with_source_and_prose_pass']=ledger['records_with_source_prose_drafts']=698
    ledger['source_prose_reviewed_counts_by_file']['/COMMON/MESFILE.DK4']=697
    ledger['reviewed_but_incomplete_COMMON_IDs']=[750,751,752,*IDS]
    ledger['active_source_prose_drafts']={'native_message_IDs':[750,751,752,*IDS],
        'manuscripts':['work/analysis/market_contract_v758/unmapped_750_752_prose_DRAFT.json',str(MANUSCRIPT)],
        'status':'three-older-context-unmapped-and24-work-comments-source-prose-reviewed-native-and-release-pending',
        'note':'27 reviewed pending entries are not the full remaining scope. Native fonts,generated layout,registered integration,actual samples and completion remain for the24 new comments.'}
    details=Path('docs/work_comments_v842_source_review.md')
    ledger['work_comments_v842']={'status':'source-prose-reviewed-native-format-release-and-actual-pending',
        'manuscript':str(MANUSCRIPT),'source_context':str(ROOT/'native_context.json'),
        'documentation':str(details),'proposed_revisions':21,'retentions':3,'completed_entries_added':0}
    checkpoint=('V842 source/prose-reviews24 independent Shipwright/Doctor comments1386-1409:21 proposed revisions and3 retentions. '
        'Original role13 and14 tables each select8 NPC voices plus4 actual protagonists.42 NPC helper calls cover all8 classes;8 original current-protagonist helper calls use real Rafael,Hodram,Lil,Maria captures without changing captains. '
        'The drafts restore preparation,ongoing work,production results,uncertainty,herbal knowledge and the reference to guys like Claudio. Native actor10 proves established Xien spelling,repairing old Xian in1409. '
        'These are work-flavor comments,not new item creation or medical/inventory commands. All formatting gates remain unapproved pending complete native-font/layout,registered release and actual samples. '
        'V838 stays current;671 complete and698 source/prose reviewed,with27 reviewed pending entries rather than the full unreviewed scope. Graphics/all18 plaques,raw-source revisit and older record re-audit remain open;full goal active.')
    ledger['latest_checkpoint']=checkpoint
    ledger['research_checkpoints'].append({'id':'V842-Shipwright-Doctor-source-review','native_message_IDs':list(IDS),
        'documentation':str(details),'proof':str(ROOT/'native_context.json'),'completed_entries_added':0,
        'previous_goal_turn_classification':'progress:25 Deck comments completed with native and actual evidence',
        'this_goal_turn_classification':'progress:24 source/prose reviews and50 original native voice/protagonist helper cases',
        'whole_goal_complete':False})
    before=read(ROOT/'editorial_ledger_before_checkpoint.json')
    assert ledger['current_integrated_candidate']==before['current_integrated_candidate']
    assert ledger['unresolved_graphics_work']==before['unresolved_graphics_work']
    assert sum(ledger['source_prose_reviewed_counts_by_file'].values())==698
    save(path,ledger)
    details.write_text('# V842: Shipwright and Doctor source/prose review\n\n'+checkpoint+'\n\n'
        'Source Japanese,current English,canonical/current byte references,individual glosses and reasons are in `'+str(MANUSCRIPT)+'`. '
        'The native context proof binds both8-entry NPC tables,both4-entry protagonist tables and the real captain identities. '
        'Shipwright is native role13 and Doctor role14;room slots and room types are separate values. '
        'Adjacent records are alternatives for other voices,not a consecutive conversation. The current approved combined ROM and every earlier translation remain unchanged.\n',encoding='utf-8')
    paragraph='\n\n## V842: work-comment source review\n\n'+checkpoint+' See [V842 source review](work_comments_v842_source_review.md).\n'
    docs=list(map(Path,('docs/translation_progress.md','docs/editorial_review_goal.md','docs/todo.md','docs/known_issues.md')))
    for p in docs:
        with p.open('a',encoding='utf-8') as f:f.write(paragraph)
    archive=Path('E:/Rota Nova translations/Editorial review/V842 Shipwright and Doctor source review')
    assert not archive.exists()
    sources=[MANUSCRIPT,path,details,Path(__file__),Path('scripts/prepare_work_comments_v842.py'),*docs]
    sources.extend(p for p in ROOT.rglob('*') if p.is_file())
    archived=[]
    for source in sorted(set(sources)):
        target=archive/source.absolute().relative_to(Path.cwd());target.parent.mkdir(parents=True,exist_ok=True)
        copy2(source,target);assert sha(source.read_bytes())==sha(target.read_bytes())
        archived.append({'source':str(source),'archive':str(target),'sha256':sha(target.read_bytes())})
    save(ROOT/'archive_manifest.json',{'archive':str(archive),'files':archived,'all_copies_hash_verified':True,'whole_goal_complete':False})
    print('V842 source checkpoint saved:671 complete,698 source/prose reviewed;24 new comments still require native formatting,integration and actual samples.',flush=True)


if __name__=='__main__':main()
