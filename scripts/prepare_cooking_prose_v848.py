"""Clean-source Cook15 prose review,including Sera's independent special line."""

from pathlib import Path
from shutil import copy2

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/cooking_comments_v848')
ROM=Path('out/all_routes_combined_v845_candidate.nds')
MANUSCRIPT=Path('translations/cooking_comments_editorial_manuscript_v1.json')
IDS=tuple(range(1410,1423))
# Faithful gloss precedes the independently authored natural English.
PROSE={
1410:('Plans to prepare nutritious food.',"Let's make a nourishing meal.",'The existing invitation is natural self-directed cooking dialogue and preserves nutritious food;meal is supported by the Cook duty.','retain'),
1411:('Adds salt,then considers this next ingredient.',"Add some salt... Now for this.",'Restore the self-directed sequence naturally;do not name an ingredient that Japanese leaves unspecified.','revise'),
1412:('Says cooking is a strength and wonders what to make.',"I'm good at cooking. What should I make?",'Keep both confidence and the question about a prospective dish;the older What next could imply an already-started recipe.','revise'),
1413:('Hums or chuckles cheerfully and boasts of being good at cooking.',"Hmm-hmm! I'm quite the cook!",'Use a playful hummed interjection for the source musical marks and a natural modest boast;no rank or special dish is invented.','revise'),
1414:('Looks for salt,then realizes this is sugar.',"Salt, salt... Wait, that's sugar!",'Restore the mistaken identification as a full comic reaction,rather than reducing the realization to the isolated word sugar.','revise'),
1415:('The older masculine speaker considers trying some male-style cooking.',"Let's see what a man can cook.",'Express the male-cooking joke as a light self-challenge in natural English;do not invent a hearty dish or an audience being served.','revise'),
1416:('Decides to taste the food,then wonders whether it is already gone.',"Time for a taste... Huh? All gone already?",'Keep the taste-testing intention and the comic already-gone question;do not state who ate the food.','revise'),
1417:('Approvingly notes that the seasoning is good.',"Hmm. Seasoned just right.",'Retain the natural tasting observation;the source repeated acknowledgment does not require a mechanical duplicate in English.','retain'),
1418:('The first protagonist notices the food is a little salty.',"Hmm, it's a little too salty...",'Retain the natural mild criticism and hesitation;no cooking failure or consequence is added.','retain'),
1419:('The second protagonist recalls often making this during his apprenticeship.',"Heh, I used to make this a lot as an apprentice...",'Restore the nostalgic past habit and apprenticeship. Do not turn it into an object called apprentice handiwork or invent which profession he apprenticed in.','revise'),
1420:('Lil complains about why she must do the cooking.',"Why do I have to do the cooking?!",'Make the exasperated personal obligation explicit;do not add all the cooking or a new assigned chore.','revise'),
1421:('Maria wonders whether fried rice would be good today.',"Maybe I'll make fried rice today.",'Use a natural tentative plan that retains the specific dish and today.','revise'),
1422:('Sera says that delicious food makes everyone happy.',"Good food makes everyone happy.",'Keep Sera simple and direct while giving her natural English. The source does not claim ownership of the food;remove the older my and its stronger assertion that everyone loves it.','revise'),
}


def main():
    assert not MANUSCRIPT.exists()
    ROOT.mkdir(parents=True,exist_ok=True)
    packet_path=Path('work/analysis/cooking_comments_v847/source_context_packet.json')
    packet=read(packet_path);ledger=read('translations/editorial_review_current_v1.json')
    assert sha(ROM.read_bytes())==packet['candidate_sha256']==ledger['current_integrated_candidate']['sha256']
    assert ledger['records_editorially_completed']==695 and ledger['records_with_source_and_prose_pass']==698
    assert len(packet['all25_original_role_helper_selections'])==25
    originals={r['message_id']:r for r in packet['records_with_immediate_storage_neighbors']}
    rows=[]
    for n,(meaning,english,note,decision) in PROSE.items():
        src=originals[n];assert english==' '.join(english.split()) and english.isascii() and not any(c in english for c in '%{}\n')
        if decision=='retain':assert english==src['current_English'].strip()
        index=n-1410
        speaker=(f'Native NPC voice class{index}' if index<8 else ['Rafael','Joakim (native captain1)','Lil','Maria'][index-8]) if n!=1422 else 'Sera (native actor24)'
        rows.append({'id':f'COMMON_MESSAGE_{n}','message_id':n,'role_ID':15,
            'voice_class':index if index<8 else None,'protagonist_ID':index-8 if 8<=index<12 else None,
            'fixed_actor_ID':24 if n==1422 else None,'speaker':speaker,
            'context':'Independent Cook15 work-flavor comment. Original NPC helper1278C uses eight voice variants;actor24 Sera has a special1422 branch. Original protagonist helper128B4 uses four real captain variants1418-1421. Storage neighbors are alternatives,not consecutive dialogue;no ingredients,inventory,stats or hunger are changed by these lines.',
            'source_Japanese':src['source_Japanese'],'source_hex':src['source_hex'],'source_reference':src['source_reference'],
            'canonical_source_hex':src['canonical_text_hex'],'current_reference':src['current_reference'],
            'current_text_hex':src['current_text_hex'],'current_English':src['current_English'],
            'source_meaning':meaning,'english':english,'localization_note':note,'editorial_decision':decision,
            'native_argument_count':0,'review':{'source':True,'context':True,'localization':True,'naturalness':True,'formatting':False}})
    assert tuple(r['message_id'] for r in rows)==IDS
    rom=NdsImage.open(ROM)
    save(MANUSCRIPT,{'format':'dk4-natural-dialogue-source-manuscript-v2','translation_policy':'natural-dialogue-v2',
        'target_locale':'en-US','encoder':'dialogue-relocatable-v1','consumer_layout_profile':'deck-cooking-comments-visible-v1',
        'review_gates':['source','context','localization','naturalness'],'formatting_review_pending':True,
        'status':'13-source-prose-reviewed-native-format-integration-and-actual-pending','file_path':'/COMMON/MESFILE.DK4',
        'source_clean_ROM_sha256':packet['source_clean_ROM_sha256'],'current_ROM':str(ROM),'current_ROM_sha256':sha(ROM.read_bytes()),
        'current_COMMON_sha256':sha(rom.read_file('/COMMON/MESFILE.DK4')),'current_ARM9_sha256':sha(rom.read_file('/__arm9__.bin')),
        'native_context_proof':str(packet_path),'native_context_proof_sha256':sha(packet_path.read_bytes()),
        'layout_producer':'scripts/work_comments_layout_v843.py','layout_producer_sha256':sha(Path('scripts/work_comments_layout_v843.py').read_bytes()),
        'records':rows,'full_goal_complete':False})
    save(ROOT/'editorial_ledger_before_source_review.json',ledger)
    ledger['records_with_source_and_prose_pass']=ledger['records_with_source_prose_drafts']=711
    ledger['source_prose_reviewed_counts_by_file']['/COMMON/MESFILE.DK4']=710
    ledger['reviewed_but_incomplete_COMMON_IDs']=[750,751,752,*IDS]
    ledger['active_source_prose_drafts']={'native_message_IDs':[750,751,752,*IDS],
        'manuscripts':['work/analysis/market_contract_v758/unmapped_750_752_prose_DRAFT.json',str(MANUSCRIPT)],
        'status':'three-older-context-unmapped-and13-cooking-source-prose-reviewed-format-and-release-pending',
        'note':'16 reviewed pending entries are not the full unreviewed shared/route/player prose or raw-source scope.'}
    checkpoint=('V848 source/prose-reviews13 Cook15 comments1410-1422:10 proposed revisions and3 justified retentions. '
        'All25 original role-helper selections prove eight NPC voice slots,four actual captain variants and the special Sera actor24 line1422. '
        'The draft restores cooking choices,salt/sugar reaction,tasting already gone,Joakim\'s frequent apprenticeship cooking,Lil\'s complaint,Maria\'s tentative fried rice and Sera\'s simple general observation. '
        'Formatting,integration and actual-display gates remain pending. V845 remains current;695 complete and711 source/prose reviewed. '
        'Older750-752 and all unreviewed shared/routes/player prose/raw coverage remain;graphics/all18 plaques and later older-record re-audit remain open;full goal active.')
    ledger['latest_checkpoint']=checkpoint
    ledger['cooking_comments_v848']={'status':'source-prose-reviewed-native-layout-release-and-actual-pending',
        'native_message_IDs':list(IDS),'manuscript':str(MANUSCRIPT),'source_context_proof':str(packet_path),
        'proposed_revisions':10,'justified_retentions':3,'completed_entries_added':0}
    ledger['research_checkpoints'].append({'id':'V848-Cooking13-source-prose','proof':str(packet_path),
        'manuscript':str(MANUSCRIPT),'new_source_prose_reviews':13,'completed_entries_added':0,
        'previous_goal_turn_classification':'progress:24 work comments completed in V845 and13 cooking source selectors mapped',
        'this_goal_turn_classification':'progress:13 faithful source glosses,natural English reviews and exact coverage references',
        'full_goal_complete':False})
    assert sum(ledger['source_prose_reviewed_counts_by_file'].values())==711
    save('translations/editorial_review_current_v1.json',ledger)
    doc=Path('docs/cooking_comments_v848_source_review.md');doc.write_text('# V848: cooking-comment source review\n\n'+checkpoint+'\n',encoding='utf-8')
    for p in map(Path,('docs/translation_progress.md','docs/editorial_review_goal.md','docs/todo.md','docs/known_issues.md')):
        with p.open('a',encoding='utf-8') as f:f.write('\n\n## V848: cooking-comment source review\n\n'+checkpoint+' See [V848 source review](cooking_comments_v848_source_review.md).\n')
    archive=Path('E:/Rota Nova translations/Editorial review/V848 Cooking source and prose review');assert not archive.exists()
    copied=[]
    for src in (MANUSCRIPT,packet_path,Path(__file__),doc,Path('translations/editorial_review_current_v1.json'),Path('scripts/prepare_cooking_context_v847.py')):
        dst=archive/src.absolute().relative_to(Path.cwd());dst.parent.mkdir(parents=True,exist_ok=True);copy2(src,dst)
        assert sha(src.read_bytes())==sha(dst.read_bytes());copied.append({'source':str(src),'archive':str(dst),'sha256':sha(dst.read_bytes())})
    save(ROOT/'archive_manifest.json',{'files':copied,'all_hashes_verified':True,'completed_entries_added':0})
    print('Cooking13 source/prose reviewed:10 revisions,3 retentions.695 complete,711 source/prose reviewed;format and actual gates remain.',flush=True)


if __name__=='__main__':main()
