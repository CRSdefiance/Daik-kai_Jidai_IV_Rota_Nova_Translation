"""Source/context review of28 independent bridge-duty comments."""

from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/bridge_duties_v868')
ROM=Path('out/all_routes_combined_v863_candidate.nds')
MANUSCRIPT=Path('translations/bridge_duties_editorial_manuscript_v1.json')
IDS=tuple(range(1471,1499))
PROSE={
1471:('Rafael reminds himself he is the captain and resolves to do his best.',"I'm the captain... I'll give it my all!",'Restore the self-reminder and enthusiastic resolve in a full natural thought.','revise'),
1472:('Joakim confidently resolves to build the strongest fleet.',"I'll build the strongest fleet...",'Restore strongest and the intent to build;the source does not merely claim ownership of this fleet.','revise'),
1473:('Lil laughs playfully that she is the captain.',"Hee hee! I'm the captain!",'Restore first-person delight without inventing a new appointment.','revise'),
1474:('Maria reflects that the organization rests on her shoulders.',"The whole company rests on my shoulders...",'Company names the established organization in this merchant-fleet setting;preserve the burden/responsibility metaphor.','revise'),
1475:('Politely offers to handle preparation of documents.',"Leave paperwork to me.",'Retain the natural concise offer;paperwork expresses the document-writing duty.','retain'),
1476:('Says the duty is to support the admiral from behind the scenes.',"My duty is to support the admiral behind the scenes.",'Restore the duty and supporting role instead of a disconnected aide label.','revise'),
1477:('Casually offers to handle diplomatic negotiations;IC is a character-dependent first-person pronoun.',"I'll handle the diplomatic talks!",'Preserve the fluent wording while replacing the earlier full-width I guard with ordinary ASCII under the source-proven current literal parser. Native IC is a pronoun,not a name.','revise'),
1478:('Asks the admiral whether they are writing something.',"Admiral, are you writing something?",'Restore a complete natural question;the context is document preparation,without inventing a specific letter.','revise'),
1479:('Confidently asks that the first-mate duty be left to the speaker.',"Leave the first mate's job to me!",'Use the established First Mate role and an assurance;do not turn it into a request for promotion.','revise'),
1480:('Politely offers to handle external diplomatic negotiations.',"Leave diplomacy to me.",'Retain the natural assurance;diplomacy preserves the external-negotiation context.','retain'),
1481:('Chuckles with pleasure at being the first mate.',"Heh heh... I'm the first mate!",'Restore the specific role and first-person boast;remove the unsupported new appointment.','revise'),
1482:('Politely offers to handle matters of negotiation.',"Leave the negotiations to me.",'Name negotiations explicitly rather than making the duty sound like ordinary conversation.','revise'),
1483:('Rafael accepts being first mate confidently,then notices something odd.',"So I'm the first mate. Leave it to me! ...Huh?",'Preserve the confident offer followed by puzzled realization;the neighboring protagonist alternatives explain the captain/first-mate joke.','revise'),
1484:('Joakim asks who is captain if he is serving as first mate.',"If I'm the first mate, who's the captain?",'Restore the conditional role conflict rather than an isolated question.','revise'),
1485:('Lil agrees to be first mate,but asks who is captain.',"First mate? Sure, but... who's the captain?",'Restore the role,concession and puzzled question in her casual voice.','revise'),
1486:('Maria acknowledges being first mate and offers to handle negotiations.',"I'm the first mate, then. Leave the negotiations to me.",'Restore both acknowledging the role and offering negotiation skill,using the established role term.','revise'),
1487:('Politely offers to handle the helm.',"Leave the helm to me.",'Retain the idiomatic assurance.','retain'),
1488:('Resolves to take care to sail safely.',"I'll do my best to keep us sailing safely...",'Express the effort and intention naturally without promising guaranteed safety.','revise'),
1489:('Accepts the helm and enthusiastically calls for hard starboard.',"The helm? Leave it to me! Hard starboard!",'Restore the omitted acceptance while preserving the nautical order and energetic voice.','revise'),
1490:('Casually says steering the ship is easy.',"Steering? Easy, easy.",'Retain the relaxed repetition and full steering context.','retain'),
1491:('Playfully comments on turning round and asks about another turn.',"Round and round! How about another turn?",'Keep the playful motion and another-turn question;do not assert a particular maneuver or change of course occurred.','revise'),
1492:('Confidently says the ship can be steered clear even of enemy shells.',"I'll steer us clear of enemy cannon fire!",'Preserve the confident resolve to evade fire without claiming that cannons categorically cannot hit.','revise'),
1493:('Says the speaker has wanted to steer a ship.',"I've always wanted to steer a ship.",'Restore a complete first-person thought and the ship;always is the natural English wish construction here.','revise'),
1494:('Invites the viewer to observe the speakers skill with the wheel.',"Just watch how I handle this wheel!",'Restore the invitation to see skill in action instead of an unrelated offer to take over.','revise'),
1495:('Rafael laughs that it turns well.',"Ha ha... It turns so easily.",'Preserve the amused ease of turning without identifying a new object or maneuver.','revise'),
1496:('Joakim says coordination between steering and the sail handler is important.',"The helmsman and sail handler need to work together.",'Express the importance of coordination as a complete natural statement;retain the established job terms.','revise'),
1497:('Lil reacts excitedly to moving the ship and confidently offers to handle it.',"I'm steering the ship?! Just leave it to me!",'Restore her excited realization as well as the emphatic assurance.','revise'),
1498:('Maria says Xien taught her steering.',"Xien taught me how to steer.",'Use the source-proven native actor10 spelling Xien in place of the older inconsistent Shen;preserve the teacher and learned skill.','revise'),
}


def main():
    assert not MANUSCRIPT.exists();ROOT.mkdir(parents=True,exist_ok=True)
    path=Path('work/analysis/bridge_duties_v866/source_context_packet.json');packet=read(path)
    terms=Path('work/analysis/bridge_duties_v867/source_pronoun_and_terms.json');proof=read(terms)
    ledger=read('translations/editorial_review_current_v1.json')
    assert sha(ROM.read_bytes())==packet['candidate_sha256']==proof['candidate_sha256']==ledger['current_integrated_candidate']['sha256']
    assert ledger['records_editorially_completed']==756 and ledger['records_with_source_and_prose_pass']==759
    assert len(packet['all54_original_role_helper_selections'])==54 and len(proof['all25_current_and_clean_parser_control_cases'])==25
    sources={r['message_id']:r for r in packet['records_with_immediate_storage_neighbors']};rows=[]
    for n,(meaning,english,note,decision) in PROSE.items():
        source=sources[n];assert english==' '.join(english.split()) and english.isascii() and not any(c in english for c in '%{}\n')
        if decision=='retain':assert english==source['current_English'].strip()
        if n<1475:role,first,label,index,hero=5,1471,'Captain',n-1471,n-1471
        elif n<1487:
            role,first,label=6,1475,'First Mate';index=n-first;hero=index-8 if index>=8 else None
        else:
            role,first,label=4,1487,'Helm';index=n-first;hero=index-8 if index>=8 else None
        speaker=f'Native NPC voice class{index}' if hero is None else ['Rafael','Joakim (native captain1)','Lil','Maria'][hero]
        rows.append({'id':f'COMMON_MESSAGE_{n}','message_id':n,'role_ID':role,'voice_class':index if hero is None else None,
            'protagonist_ID':hero,'speaker':speaker,'context':f'Independent {label} room{role} work-flavor comment. Source1471-1474 has four captain alternatives only;other duties have eight NPC voices and four actual captain alternatives. Storage neighbors are alternatives,not consecutive speech. The remark performs no assignment,promotion,steering action or fleet creation.',
            'source_Japanese':source['source_Japanese'],'source_hex':source['source_hex'],'source_reference':source['source_reference'],
            'canonical_source_hex':source['canonical_text_hex'],'current_reference':source['current_reference'],
            'current_text_hex':source['current_text_hex'],'current_English':source['current_English'],
            'source_meaning':meaning,'english':english,'localization_note':note,'editorial_decision':decision,
            'native_argument_count':0,'review':{'source':True,'context':True,'localization':True,'naturalness':True,'formatting':False}})
    assert tuple(r['message_id'] for r in rows)==IDS
    assert sum(r['editorial_decision']=='revise' for r in rows)==24
    save(MANUSCRIPT,{'format':'dk4-natural-dialogue-source-manuscript-v2','translation_policy':'natural-dialogue-v2','target_locale':'en-US',
        'encoder':'dialogue-relocatable-v1','consumer_layout_profile':'deck-bridge-duties-visible-v1',
        'review_gates':['source','context','localization','naturalness'],'formatting_review_pending':True,
        'status':'28-source-prose-reviewed-native-format-integration-and-actual-pending','file_path':'/COMMON/MESFILE.DK4',
        'source_clean_ROM_sha256':packet['source_clean_ROM_sha256'],'current_ROM':str(ROM),'current_ROM_sha256':sha(ROM.read_bytes()),
        'current_COMMON_sha256':packet['COMMON_sha256'],'current_ARM9_sha256':packet['ARM9_sha256'],
        'native_context_proof':str(path),'native_context_proof_sha256':sha(path.read_bytes()),
        'native_pronoun_terms_proof':str(terms),'native_pronoun_terms_proof_sha256':sha(terms.read_bytes()),'records':rows,'full_goal_complete':False})
    save(ROOT/'editorial_ledger_before_source_review.json',ledger)
    ledger['records_with_source_and_prose_pass']=ledger['records_with_source_prose_drafts']=787
    ledger['source_prose_reviewed_counts_by_file']['/COMMON/MESFILE.DK4']=786
    ledger['reviewed_but_incomplete_COMMON_IDs']=[750,751,752,*IDS]
    ledger['active_source_prose_drafts']={'native_message_IDs':[750,751,752,*IDS],
        'manuscripts':['work/analysis/market_contract_v758/unmapped_750_752_prose_DRAFT.json',str(MANUSCRIPT)],
        'status':'three-older-context-unmapped-and28-bridge-duty-source-prose-reviewed-format-release-pending',
        'note':'These31 reviewed pending entries are not the full remaining shared/route/player prose or raw-source scope.'}
    checkpoint=('V868 source/prose-reviews28 captain/first-mate/helm comments1471-1498:24 proposed revisions and4 retentions. '
        'All54 original role selections,50 current/clean IC pronoun expansions,and native First Mate/Xien terms pass. '
        'Drafts restore strongest-fleet resolve,support behind the scenes,the captain/first-mate jokes,full hard-starboard acceptance,safe-sailing effort,enemy-fire evasion and wheel-skill demonstration. '
        'Native font/layout,registered integration and actual scenes remain pending. V863 remains current;756 complete,787 source/prose reviewed. '
        'Older750-752 and all unreviewed shared/routes/player prose/raw coverage remain;separate graphics/all18 plaques and later older-record re-audit stay open;full goal active.')
    ledger['latest_checkpoint']=checkpoint
    ledger['bridge_duties_v868']={'status':'source-prose-reviewed-native-release-and-actual-pending','native_message_IDs':list(IDS),
        'manuscript':str(MANUSCRIPT),'source_context_proof':str(path),'native_pronoun_terms_proof':str(terms),
        'proposed_revisions':24,'justified_retentions':4,'completed_entries_added':0}
    ledger['research_checkpoints'].append({'id':'V868-Bridge-duties28-source-prose','proof':str(path),'manuscript':str(MANUSCRIPT),
        'new_source_prose_reviews':28,'completed_entries_added':0,'previous_goal_turn_classification':'progress:Planning/Finance24 complete inV863,next28 original contexts proved',
        'this_goal_turn_classification':'progress:50 source/current pronoun expansions,native terms and28 natural faithful source reviews','full_goal_complete':False})
    assert sum(ledger['source_prose_reviewed_counts_by_file'].values())==787
    save('translations/editorial_review_current_v1.json',ledger)
    doc=Path('docs/bridge_duties_v868_source_review.md');doc.write_text('# V868: bridge duties source review\n\n'+checkpoint+'\n',encoding='utf-8')
    for p in map(Path,('docs/translation_progress.md','docs/editorial_review_goal.md','docs/todo.md','docs/known_issues.md')):
        with p.open('a',encoding='utf-8') as f:f.write('\n\n## V868: bridge duties source review\n\n'+checkpoint+' See [V868 review](bridge_duties_v868_source_review.md).\n')
    archive=Path('E:/Rota Nova translations/Editorial review/V868 Bridge duties source review');assert not archive.exists();copied=[]
    for source in (MANUSCRIPT,path,terms,Path(__file__),doc,Path('translations/editorial_review_current_v1.json'),Path('scripts/probe_bridge_pronoun_v867.py')):
        target=archive/source.absolute().relative_to(Path.cwd());target.parent.mkdir(parents=True,exist_ok=True);copy2(source,target)
        assert sha(source.read_bytes())==sha(target.read_bytes());copied.append({'source':str(source),'archive':str(target),'sha256':sha(target.read_bytes())})
    save(ROOT/'archive_manifest.json',{'files':copied,'all_hashes_verified':True,'completed_entries_added':0})
    print('Bridge duties28 source/prose reviewed:24 revisions,4 retentions.756 complete,787 source/prose;native/release/actual pending.',flush=True)


if __name__=='__main__':main()
