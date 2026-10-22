"""Faithful natural-English source review of24 gunnery/deck-cleaning alternatives."""

from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/gunnery_deck_v886')
ROM=Path('out/all_routes_combined_v882_candidate.nds')
MANUSCRIPT=Path('translations/gunnery_deck_editorial_manuscript_v1.json')
IDS=tuple(range(1547,1571))
PROSE={1547: ('Reports currently test-firing the cannons.',
        "I'm test-firing the cannons now.",
        'Restore a full personal status report;the cannon context comes from the original Gunnery role.',
        'revise'),
 1548: ('Politely asks to talk later because test-firing is underway.',
        "I'm test-firing right now. Could we talk later?",
        'Restore the reason and polite deferral rather than a clipped command.',
        'revise'),
 1549: ('Is practicing in preparation for naval combat.',
        "I'm practicing for naval battles.",
        'Restore the personal ongoing preparation as natural speech.',
        'revise'),
 1550: ('Asks whether firing makes the listener feel nervous anticipation.',
        "Don't you get nervous firing a cannon?",
        'Express harahara as nervous anticipation without escalating it to outright fear.',
        'revise'),
 1551: ('Enthusiastically decides to try one more shot.',
        'All right, one more shot!',
        'Retain the natural enthusiastic continuation and one-more-shot intent.',
        'retain'),
 1552: ('Enthusiastically proposes firing away heartily.',
        "Let's fire away!",
        'Retain the idiomatic energetic offer;the source repeated firing sound need not be copied literally.',
        'retain'),
 1553: ('Says the loud boom reverberates in an empty stomach.',
        'That boom rattles my empty stomach!',
        'Restore the empty-stomach hunger joke in a natural physical reaction;do not invent an injury or damage.',
        'revise'),
 1554: ('Says accuracy is the key issue with cannons.',
        'Cannon accuracy matters.',
        'Retain the clear natural technical observation.',
        'retain'),
 1555: ('Rafael practices so he can fight whenever needed.',
        "I'm practicing so I'll always be ready to fight!",
        'Restore the personal ongoing practice and its purpose of readiness at any time.',
        'revise'),
 1556: ('Joakim reflects that hitting a target is difficult.',
        'Hitting the target is hard...',
        'Retain the natural reflective observation and pause.',
        'retain'),
 1557: ('Lil dislikes the sound whenever she hears it.',
        'That sound is always awful!',
        'Retain the natural emphatic dislike and repeated-time sense.',
        'retain'),
 1558: ('Maria says more study of gunnery is needed.',
        'I need to learn more about gunnery.',
        'Restore a complete personal learning intention without inventing a skill result.',
        'revise'),
 1559: ('Asks whether it now looks clean.',
        "How does it look? Nice and clean now, isn't it?",
        'Restore the request for approval and confirmation in a natural polite voice.',
        'revise'),
 1560: ('Says the ship is as good as home and must be polished.',
        'This ship is our home. We need to keep it polished.',
        'Restore the personal obligation and home comparison as full natural thoughts.',
        'revise'),
 1561: ('Says it is our ship,so it must be kept clean;IC plus plural ra refers to the speakers group.',
        "It's our ship, so we have to keep it clean!",
        'Retain the fluent wording while replacing the old full-width I guard with ordinary ASCII. Original IC is first person;the plural '
        'suffix makes our,not an actor name.',
        'revise'),
 1562: ('Complains that it becomes dirty again immediately even after cleaning.',
        'It gets dirty again as soon as I clean it!',
        'Restore a full personal complaint with the repeated cleaning/dirt relationship.',
        'revise'),
 1563: ('Confidently offers to handle deck cleaning.',
        'Deck cleaning? Leave it to me!',
        'Restore the offer;do not turn it into a claim that deck cleaning is merely the speakers assigned job.',
        'revise'),
 1564: ('Enjoys occasionally doing cleaning outdoors.',
        "It's nice to do some cleaning outside now and then.",
        'Restore the occasional timing and open-air cleaning naturally.',
        'revise'),
 1565: ('Scrubs and cheerfully reports that it is clean.',
        'Scrub, scrub... All clean!',
        'Retain the natural scrub sound and completed-cleaning reaction.',
        'retain'),
 1566: ('Feels motivated to make an effort because the ship is important to the group.',
        'This ship means a lot to us, so I give it my all.',
        'Preserve affection/value and effort without calling it a fine-quality or luxurious ship.',
        'revise'),
 1567: ('Rafael notes that it has become much cleaner.',
        "Now that's much cleaner.",
        'Retain the natural pleased observation and degree of improvement.',
        'retain'),
 1568: ('Joakim feels nostalgic for the days spent training under his mentor.',
        'I miss the days I spent training under my mentor...',
        'Restore both nostalgia and training under a mentor;do not invent a family relationship or name the mentor without scene evidence.',
        'revise'),
 1569: ('Lil notices leftovers and identifies Emilio as the likely culprit.',
        'These leftovers... Emilio!',
        'Retain the natural staccato recognition/accusation and the established Emilio spelling;do not add ownership or a new food detail.',
        'retain'),
 1570: ('Maria says keeping the ship clean feels pleasant.',
        'A clean ship feels wonderful.',
        'Retain the natural positive reaction;ship is supplied by the original deck-cleaning context.',
        'retain')}


def main():
    assert not MANUSCRIPT.exists();ROOT.mkdir(parents=True,exist_ok=True)
    path=Path('work/analysis/gunnery_deck_v884/source_context_packet.json');packet=read(path)
    ledger=read('translations/editorial_review_current_v1.json')
    assert sha(ROM.read_bytes())==packet['candidate_sha256']==ledger['current_integrated_candidate']['sha256']
    assert ledger['records_editorially_completed']==832 and ledger['records_with_source_and_prose_pass']==835
    assert len(packet['all50_original_role_helper_selections'])==50
    sources={r['message_id']:r for r in packet['records_with_immediate_storage_neighbors']};rows=[]
    for n,(meaning,english,note,decision) in PROSE.items():
        source=sources[n];assert english==' '.join(english.split()) and english.isascii() and not any(c in english for c in '%{}\n')
        if decision=='retain':assert english==source['current_English'].strip()
        role,first,label=(8,1547,'Gunnery') if n<1559 else (2,1559,'Deck Cleaning');index=n-first
        hero=index-8 if index>=8 else None
        speaker=f'Native NPC voice class{index}' if hero is None else ['Rafael','Joakim (native captain1)','Lil','Maria'][hero]
        rows.append({'id':f'COMMON_MESSAGE_{n}','message_id':n,'role_ID':role,'voice_class':index if hero is None else None,'protagonist_ID':hero,
            'speaker':speaker,'context':f'Independent {label}{role} work comment. Original1278C chooses eight NPC voices;128B4 uses the genuine captain. Storage neighbors are independent alternatives,not consecutive speech. No measurement,discovery,report or gameplay action is performed by this flavor text.',
            'source_Japanese':source['source_Japanese'],'source_hex':source['source_hex'],'source_reference':source['source_reference'],
            'canonical_source_hex':source['canonical_text_hex'],'current_reference':source['current_reference'],
            'current_text_hex':source['current_text_hex'],'current_English':source['current_English'],
            'source_meaning':meaning,'english':english,'localization_note':note,'editorial_decision':decision,
            'native_argument_count':0,'review':{'source':True,'context':True,'localization':True,'naturalness':True,'formatting':False}})
    assert tuple(r['message_id'] for r in rows)==IDS and sum(r['editorial_decision']=='revise' for r in rows)==15
    pronoun=Path('work/analysis/gunnery_deck_v885/source_pronoun_and_terms.json');assert read(pronoun)['candidate_sha256']==sha(ROM.read_bytes())
    save(MANUSCRIPT,{'format':'dk4-natural-dialogue-source-manuscript-v2','translation_policy':'natural-dialogue-v2','target_locale':'en-US',
        'encoder':'dialogue-relocatable-v1','consumer_layout_profile':'deck-gunnery-deck-visible-v1',
        'review_gates':['source','context','localization','naturalness'],'formatting_review_pending':True,
        'status':'24-source-prose-reviewed-native-format-integration-and-actual-pending','file_path':'/COMMON/MESFILE.DK4',
        'source_clean_ROM_sha256':packet['source_clean_ROM_sha256'],'current_ROM':str(ROM),'current_ROM_sha256':sha(ROM.read_bytes()),
        'current_COMMON_sha256':packet['COMMON_sha256'],'current_ARM9_sha256':packet['ARM9_sha256'],
        'native_context_proof':str(path),'native_context_proof_sha256':sha(path.read_bytes()),'native_pronoun_proof':str(pronoun),'native_pronoun_proof_sha256':sha(pronoun.read_bytes()),'records':rows,'full_goal_complete':False})
    save(ROOT/'editorial_ledger_before_source_review.json',ledger)
    ledger['records_with_source_and_prose_pass']=ledger['records_with_source_prose_drafts']=859
    ledger['source_prose_reviewed_counts_by_file']['/COMMON/MESFILE.DK4']=858
    ledger['reviewed_but_incomplete_COMMON_IDs']=[750,751,752,*IDS]
    ledger['active_source_prose_drafts']={'native_message_IDs':[750,751,752,*IDS],
        'manuscripts':['work/analysis/market_contract_v758/unmapped_750_752_prose_DRAFT.json',str(MANUSCRIPT)],
        'status':'three-older-context-unmapped-and24-gunnery-deck-source-prose-reviewed-format-release-pending',
        'note':'These27 reviewed pending entries are not the full remaining shared/route/player prose or raw-source scope.'}
    checkpoint=('V886 source/prose-reviews24 Gunnery8/DeckCleaning2 comments1547-1570:15 proposed revisions and9 retentions. '
        'All50 original selections cover eight NPC voices and four genuine captains per duty. Drafts restore polite test-firing deferral,nervous anticipation,the empty-stomach joke,personal preparation,deck-cleaning offers,our ship pronoun,occasional outdoor cleaning,ship value and mentor nostalgia. '
        'Native layout,registered integration and actual scenes remain pending. V882 remains current;832 complete,859 source/prose reviewed. Older750-752 and all unreviewed shared/routes/player prose/raw coverage remain;separate graphics/all18 plaques and later older-record re-audit stay open;full goal active.')
    ledger['latest_checkpoint']=checkpoint
    ledger['gunnery_deck_v886']={'status':'source-prose-reviewed-native-release-and-actual-pending','native_message_IDs':list(IDS),
        'manuscript':str(MANUSCRIPT),'source_context_proof':str(path),'proposed_revisions':15,'justified_retentions':9,'completed_entries_added':0}
    ledger['research_checkpoints'].append({'id':'V886-Gunnery-Deck24-source-prose','proof':str(path),'manuscript':str(MANUSCRIPT),
        'new_source_prose_reviews':24,'completed_entries_added':0,'previous_goal_turn_classification':'progress:Sails/Boarding24 completed inV882,next24 original contexts proved',
        'this_goal_turn_classification':'progress:24 faithful source glosses,natural English reviews and exact source/current references','full_goal_complete':False})
    assert sum(ledger['source_prose_reviewed_counts_by_file'].values())==859
    save('translations/editorial_review_current_v1.json',ledger)
    doc=Path('docs/gunnery_deck_v886_source_review.md');doc.write_text('# V886: gunnery and deck cleaning source review\n\n'+checkpoint+'\n',encoding='utf-8')
    for p in map(Path,('docs/translation_progress.md','docs/editorial_review_goal.md','docs/todo.md','docs/known_issues.md')):
        with p.open('a',encoding='utf-8') as f:f.write('\n\n## V886: gunnery and deck cleaning source review\n\n'+checkpoint+' See [V886 review](gunnery_deck_v886_source_review.md).\n')
    archive=Path('E:/Rota Nova translations/Editorial review/V886 Gunnery and deck cleaning source review');assert not archive.exists();copied=[]
    for source in (MANUSCRIPT,path,Path(__file__),doc,Path('translations/editorial_review_current_v1.json'),Path('scripts/prepare_gunnery_deck_context_v884.py')):
        target=archive/source.absolute().relative_to(Path.cwd());target.parent.mkdir(parents=True,exist_ok=True);copy2(source,target)
        assert sha(source.read_bytes())==sha(target.read_bytes());copied.append({'source':str(source),'archive':str(target),'sha256':sha(target.read_bytes())})
    save(ROOT/'archive_manifest.json',{'files':copied,'all_hashes_verified':True,'completed_entries_added':0})
    print('Gunnery/Deck24 source/prose reviewed:15 revisions,9 retentions.832 complete,859 source/prose;native/release/actual pending.',flush=True)


if __name__=='__main__':main()
