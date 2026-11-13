"""Faithful natural-English review of24 battle repair/medical alternatives."""

from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/battle_repair_medical_v901')
ROM=Path('out/all_routes_combined_v893_candidate.nds')
MANUSCRIPT=Path('translations/battle_repair_medical_editorial_manuscript_v1.json')
IDS=tuple(range(1596,1620))
PROSE={
1596:('Offers to reinforce places hit by gunfire immediately.',
      "I'll reinforce any spots that get hit right away.",
      'Restore the personal offer and immediate reinforcement of the damaged location. The source does not report a completed repair.','revise'),
1597:('Reflects that this is the time for a shipwright to play an active part.',
      "Now it's a shipwright's turn to shine...",
      'Use the familiar turn-to-shine idiom for katsuyaku,keeping the reflective pause and explicit shipwright role.','revise'),
1598:('Promises to rush over immediately if the ship is hit.',
      "If we're hit, I'll be there right away.",
      'Restore the speakers offer to come;the old instruction to call changes the source intent. We is the ship and crew in this battle context.','revise'),
1599:('Offers to repair hull damage immediately.',
      "I'll repair any hull damage right away!",
      'Restore the personal offer and explicit hull damage,without an invented repair result or speed statistic.','revise'),
1600:('Roughly asks the listener not to damage the ship too much.',
      'Try not to damage the ship too much.',
      'Restore too much and use the natural ship verb damage,rather than harm.','revise'),
1601:('Orders reports of where the ship has been hit and says the speaker will rush there.',
      "Report where we're hit! I'll be right there.",
      'Restore the location request and immediate personal response in a firm natural voice. Do not replace the speaker with anonymous help.','revise'),
1602:('Casually promises to repair damage if the ship takes a hit.',
      "If we take a hit, I'll fix it right up!",
      'Restore oira as first-person I and keep the informal reassuring offer.','revise'),
1603:('Notes that naval combat keeps a shipwright very busy.',
      'A sea battle? A shipwright has plenty to do.',
      'Restore the complete natural observation and active workload without adding a particular repair or damage event.','revise'),
1604:('Rafael asks the listener to leave repairs to him and fight without worrying.',
      'Leave the repairs to me! Just focus on the fight.',
      'Restore the personal reassurance and the invitation to concentrate on combat. No automatic protection or morale effect is promised.','revise'),
1605:('Hodram orders immediate damage reports and says he will go perform emergency repairs.',
      "Report damage right away! I'll come make emergency repairs.",
      'Restore immediately as the reporting requirement,and emergency repairs as his intended response. Do not claim repairs have already begun.','revise'),
1606:('Lil confidently promises to repair cannon damage very quickly.',
      "I'll fix cannon damage in no time!",
      'Restore her personal quick-repair boast;the source does not merely state repairs are easy.','revise'),
1607:('Maria says she will repair the ship immediately if it is damaged.',
      "If the ship is damaged, I'll repair it right away.",
      'Restore the complete conditional personal offer,instead of a detached damage/repair rule.','revise'),
1608:('Politely offers to care for the wounded personally.',
      "I'll take care of the wounded.",
      'Restore the first-person offer and natural complete sentence.','revise'),
1609:('Asks to be called immediately if anyone is injured.',
      'Call me right away if anyone gets hurt.',
      'Restore the explicit urgency in a natural request;no injury is asserted to have happened.','revise'),
1610:('Reassures the listener not to worry because the speaker is present;IC is the original first-person pronoun.',
      "I'm here, so don't worry!",
      'Preserve the already natural wording while replacing the obsolete full-width I with ordinary ASCII. Fifty current/clean native expansions prove IC is first person,not a character name;complete initial-glyph proof remains required.','revise'),
1611:('Cheerfully says the listener has an angel in white looking after them.',
      'Your angel in white is here!',
      'Retain the natural playful medical-angel metaphor and white-uniform image without inventing a relationship.','retain'),
1612:('Dismissively says to put saliva on an injury.',
      'A scrape? Just spit on it!',
      'Retain the rough dismissive injury joke. Scrape naturally conveys the speakers minimization;this is fictional flavor dialogue,not an actual treatment instruction to the user.','retain'),
1613:('Boasts that the listener has an expert doctor,the speaker,looking after them.',
      "You've got an expert doctor looking after you!",
      'Restore the personal boast and reassuring support,using expert doctor rather than the unnatural title master doctor.','revise'),
1614:('Casually says the speaker will treat the listener if they get hurt.',
      "If you get hurt, I'll patch you up.",
      'Restore first-person oira and use the familiar patch-you-up idiom for the informal treatment offer.','revise'),
1615:('Tells injured people not to push themselves and to come to the speaker.',
      "If you're hurt, don't push yourself. Come see me.",
      'Restore a complete conditional and natural personal invitation;no diagnosis or recovery result is added.','revise'),
1616:('Rafael warns against being injured by reckless fighting.',
      "Don't get hurt being reckless.",
      'Retain the natural complete caution;the battle context supplies the fighting.','retain'),
1617:('Hodram quietly warns the listener not to treat their life carelessly.',
      "Don't throw your life away...",
      'Use the natural English warning and source trailing pause,rather than the more forceful disconnected Value your life exclamation. No motive or new risk is invented.','revise'),
1618:('Lil hesitantly admits she is uncomfortable with blood.',
      'Blood makes me uneasy...',
      'Retain the natural personal discomfort and hesitant pause;do not add fainting or an injury.','retain'),
1619:('Maria observes that a ships doctor stays busy when battle begins.',
      'Doctors stay busy in battle.',
      'Retain the natural observation. The assigned ships-doctor context supplies the nautical setting without an unnecessary rewrite.','retain')}


def main():
    assert not MANUSCRIPT.exists();ROOT.mkdir(parents=True,exist_ok=True)
    packet_path=Path('work/analysis/battle_repair_medical_v899/source_context_packet.json');packet=read(packet_path)
    pronoun=Path('work/analysis/battle_medical_v900/source_pronoun_proof.json');p=read(pronoun)
    ledger=read('translations/editorial_review_current_v1.json')
    assert ledger['records_editorially_completed']==881 and ledger['records_with_source_and_prose_pass']==884
    assert sha(ROM.read_bytes())==packet['candidate_sha256']==p['candidate_sha256']==ledger['current_integrated_candidate']['sha256']
    assert len(packet['all150_original_battle_helper_main_and_ordinary_control_selections'])==150
    assert p['IC_is_first_person_not_actor_name'] and len(p['all25_current_and_clean_parser_control_cases'])==25
    sources={r['message_id']:r for r in packet['records_with_immediate_storage_neighbors']};rows=[]
    for n,(meaning,english,note,decision) in PROSE.items():
        s=sources[n];role,first,label=(13,1596,'Shipwright') if n<1608 else (14,1608,'Medical care');index=n-first
        hero=index-8 if index>=8 else None
        speaker=f'Native NPC voice class{index}' if hero is None else ['Rafael','Hodram Joakim Bergstrom (genuine captain1)','Lil','Maria'][hero]
        assert english==' '.join(english.split()) and english.isascii() and not any(c in english for c in '%{}\n')
        if decision=='retain':assert english==s['current_English'].strip()
        rows.append({'id':f'COMMON_MESSAGE_{n}','message_id':n,'role_ID':role,'voice_class':index if hero is None else None,
            'protagonist_ID':hero,'speaker':speaker,
            'context':f'Independent battle {label}{role} working comment. Original12600 chooses eight NPC voice alternatives;12720 chooses the genuine captain. Main12104 state0 selects the battle table when native mode fields8/12 are0/1. Storage neighbors belong to independent alternatives,not consecutive speech. The flavor text performs no repair,treatment or stat change.',
            'source_Japanese':s['source_Japanese'],'source_hex':s['source_hex'],'source_reference':s['source_reference'],
            'canonical_source_hex':s['canonical_text_hex'],'current_reference':s['current_reference'],
            'current_text_hex':s['current_text_hex'],'current_English':s['current_English'],
            'source_meaning':meaning,'english':english,'localization_note':note,'editorial_decision':decision,
            'native_argument_count':0,'review':{'source':True,'context':True,'localization':True,'naturalness':True,'formatting':False}})
    assert tuple(r['message_id'] for r in rows)==IDS and sum(r['editorial_decision']=='revise' for r in rows)==19
    assert p['source1610_hex']==sources[1610]['source_hex']
    save(MANUSCRIPT,{'format':'dk4-natural-dialogue-source-manuscript-v2','translation_policy':'natural-dialogue-v2','target_locale':'en-US',
        'encoder':'dialogue-relocatable-v1','consumer_layout_profile':'deck-battle-repair-medical-visible-v1',
        'review_gates':['source','context','localization','naturalness'],'formatting_review_pending':True,
        'status':'24-source-prose-reviewed-native-format-integration-and-actual-pending','file_path':'/COMMON/MESFILE.DK4',
        'source_clean_ROM_sha256':packet['source_clean_ROM_sha256'],'current_ROM':str(ROM),'current_ROM_sha256':sha(ROM.read_bytes()),
        'current_COMMON_sha256':packet['COMMON_sha256'],'current_ARM9_sha256':packet['ARM9_sha256'],
        'native_context_proof':str(packet_path),'native_context_proof_sha256':sha(packet_path.read_bytes()),
        'native_pronoun_proof':str(pronoun),'native_pronoun_proof_sha256':sha(pronoun.read_bytes()),'records':rows,'full_goal_complete':False})
    save(ROOT/'editorial_ledger_before_source_review.json',ledger)
    ledger['records_with_source_and_prose_pass']=ledger['records_with_source_prose_drafts']=908
    ledger['source_prose_reviewed_counts_by_file']['/COMMON/MESFILE.DK4']=907
    ledger['reviewed_but_incomplete_COMMON_IDs']=[750,751,752,*IDS]
    ledger['active_source_prose_drafts']={'native_message_IDs':[750,751,752,*IDS],
        'manuscripts':['work/analysis/market_contract_v758/unmapped_750_752_prose_DRAFT.json',str(MANUSCRIPT)],
        'status':'three-older-context-unmapped-and24-battle-repair-medical-source-prose-reviewed-format-release-pending',
        'note':'These27 reviewed pending entries are not the full remaining shared/routes/player prose or raw-source scope.'}
    checkpoint=('V901 source/prose-reviews24 battle Shipwright13/Medical14 comments1596-1619:19 revisions and5 retentions. '
        'Original150 battle-helper/main-selector/ordinary controls and50 current/clean first-person expansions pass. '
        'Drafts restore immediate personal reinforcement/repair offers,damage reporting,emergency repairs,medical reassurance,personal treatment and understated life warning;the obsolete full-width I1610 becomes ASCII pending glyph proof. '
        'Native layout,registered integration and actual scenes remain pending. V893 remains current;881 complete,908 source/prose reviewed. '
        'Older750-752,other shared/routes/player prose,raw coverage,special actors1885-1888,separate graphics/all18 plaques,Samwell header and later older-record re-audit remain open;full goal active.')
    ledger['latest_checkpoint']=checkpoint
    ledger['battle_repair_medical_v901']={'status':'source-prose-reviewed-native-release-and-actual-pending','native_message_IDs':list(IDS),
        'manuscript':str(MANUSCRIPT),'source_context_proof':str(packet_path),'proposed_revisions':19,'justified_retentions':5,'completed_entries_added':0}
    ledger['research_checkpoints'].append({'id':'V901-Battle-repair-medical24-source-prose','proof':str(packet_path),'manuscript':str(MANUSCRIPT),
        'new_source_prose_reviews':24,'completed_entries_added':0,
        'previous_goal_turn_classification':'progress:25 battle-personal entries completed inV893;next24 original contexts mapped',
        'this_goal_turn_classification':'progress:24 faithful source glosses,natural English reviews,exact references and50 first-person parser controls',
        'full_goal_complete':False})
    assert sum(ledger['source_prose_reviewed_counts_by_file'].values())==908
    save('translations/editorial_review_current_v1.json',ledger)
    doc=Path('docs/battle_repair_medical_v901_source_review.md')
    with doc.open('x',encoding='utf-8') as f:f.write('# V901: battle repair and medical source review\n\n'+checkpoint+'\n')
    for d in map(Path,('docs/translation_progress.md','docs/editorial_review_goal.md','docs/todo.md','docs/known_issues.md')):
        with d.open('a',encoding='utf-8') as f:f.write('\n\n## V901: battle repair and medical source review\n\n'+checkpoint+' See [V901 source review](battle_repair_medical_v901_source_review.md).\n')
    archive=Path('E:/Rota Nova translations/Editorial review/V901 Battle repair medical source review');assert not archive.exists();copied=[]
    for source in (MANUSCRIPT,packet_path,pronoun,Path(__file__),Path('scripts/probe_battle_medical_pronoun_v900.py'),doc,Path('translations/editorial_review_current_v1.json')):
        target=archive/source.absolute().relative_to(Path.cwd());target.parent.mkdir(parents=True,exist_ok=True);copy2(source,target)
        assert sha(source.read_bytes())==sha(target.read_bytes());copied.append({'source':str(source),'archive':str(target),'sha256':sha(target.read_bytes())})
    save(ROOT/'archive_manifest.json',{'files':copied,'all_hashes_verified':True,'completed_entries_added':0})
    print('Battle repair/medical24 source/prose reviewed:19 revisions,5 retentions.881 complete,908 source/prose;native/release/actual pending.',flush=True)


if __name__=='__main__':main()
