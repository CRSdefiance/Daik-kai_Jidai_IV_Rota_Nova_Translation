"""Source-led natural-English review of28 independent battle Bridge comments."""

from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.battle_finance_editorial import current_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.prepare_work_comments_v842 import reference
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/battle_bridge_v925')
ROM=Path('out/all_routes_combined_v922_candidate.nds')
MANUSCRIPT=Path('translations/battle_bridge_editorial_manuscript_v1.json')
IDS=tuple(range(1681,1709))
PROSE={1681: ('Rafael hesitates and tells himself to pull himself together.', "Um, um... I've got to pull myself together!", 'Restore hesitant repetition and personal resolve.', 'revise'), 1682: ('Hodram orders a barrage and prepares the deck crew for hand-to-hand combat.', 'Gunners, lay down a barrage! Deck crew, prepare for hand-to-hand combat!', 'Restore the barrage and addressed deck crew;no successful boarding or equipped ram is claimed.', 'revise'), 1683: ('Lil cannot keep relying on Camille forever.', "I can't keep relying on Camille forever...", 'Preserve Camille and natural wording;replace obsolete full-width initial I under native glyph verification.', 'revise'), 1684: ('Maria asks Xien for the battle situation.', 'Xien, report on the battle!', 'Restore established actor10 Xien,as in reviewed ordinary1498.', 'revise'), 1685: ('Politely offers to report the battle situation.', "I'll keep you informed about the battle.", 'Restore a personal offer rather than a detached prediction.', 'revise'), 1686: ('Will call for surrender when attacking a city.', "When we attack a city, I'll call on it to surrender!", 'Restore personal undertaking and city-attack condition;not an order to the admiral.', 'revise'), 1687: ('A captain and first mate are necessary if one wants a city to surrender.', "If you want a city to surrender, you'll need a captain and first mate.", 'Preserve required roles without guaranteeing surrender.', 'revise'), 1688: ('A first mates naval-battle work is mostly battle reports.', "In a sea battle, a first mate mostly just reports how it's going.", 'Restore limited naval-combat scope and casual qualification;not the entire sailing job.', 'revise'), 1689: ('Casually suggests going to the Guild to arrange a truce.', 'Should we go to the Guild and ask for a truce?', 'Restore going to the Guild and tentative suggestion;truce is the established offer term356.', 'revise'), 1690: ('The elderly speaker encourages the admiral to do their best.', 'Admiral, do your best!', 'Retain natural encouragement without inventing family relationships.', 'retain'), 1691: ('Says they are useful when attacking a city.', "I'm useful when we're attacking a city, you know!", 'Restore personal boast and conditional usefulness.', 'revise'), 1692: ('Politely says this is the admirals chance to show their skill.', "Now's your chance to show your skill, Admiral.", 'Localize the opportunity idiom as respectful encouragement;no victory claimed.', 'revise'), 1693: ('Rafael cannot negotiate now because they must go to a city.', "We can't negotiate now. We have to go to a city first.", 'Restore action and destination;no city-ownership requirement is invented.', 'revise'), 1694: ('Hodram cannot command from this location.', "I can't command from here...", 'Restore personal speaker and spatial limitation.', 'revise'), 1695: ('Lil says one cannot expect much of her in this location.', "You can't expect much from me here...", 'Restore Lil as the person with limited contribution in this room.', 'revise'), 1696: ('Maria says captain and first mate play an active part in city attacks.', 'The captain and first mate really shine when attacking a city.', 'Preserve role usefulness without adding exclusive leadership or surrender rules.', 'revise'), 1697: ('Politely asks which ship to approach.', 'Which ship should I approach?', 'Use a natural English verb and preserve the personal steering offer.', 'revise'), 1698: ('Promises to demonstrate dodging those shots.', "I'll show you I can dodge those shots!", 'Restore confident personal promise instead of passive automatic-evasion forecast.', 'revise'), 1699: ('Wonders whether the rain of shots can be dodged.', 'Can we dodge this rain of shot?', 'Retain nautical mass noun shot,metaphor and uncertain question.', 'retain'), 1700: ('Wants to charge and asks whether a ram is available.', "I want to charge! Don't we have a ram?", 'Preserve desire and equipment question;no ram ownership is asserted.', 'revise'), 1701: ('Roughly boasts those weak shots will not hit.', "Those weak shots won't hit us!", 'Retain the rough character boast,not a mechanical invulnerability claim.', 'retain'), 1702: ('Boasts that sea battles let veterans skills shine.', 'Sea battles let veterans shine!', 'Retain natural veteran boast and naval-battle scope.', 'retain'), 1703: ('Naval battle is the chance to show personal ship-handling skill.', 'A sea battle is my chance to show what I can do at the helm!', 'Restore personal skill and naval-battle context without inventing maneuvers.', 'revise'), 1704: ('Politely expresses eagerness to exercise skill in naval battle.', "A sea battle? I'm itching to put my skills to use!", 'Localize ude ga naru as eagerness to exercise skill;Blood boils mistranslates the idiom.', 'revise'), 1705: ('Rafael asks sail handlers to coordinate with his steering.', 'Sail handlers, coordinate with me at the helm!', 'Restore cooperation and Rafaels own steering using established role terminology.', 'revise'), 1706: ('Hodram charges toward the enemy ship and calls on Gerhard to prepare for hand-to-hand combat.', "I'm heading straight for the enemy ship! Gerhard, prepare to board!", 'Preserve enemy ship and Gerhard;boarding is the naval melee preparation;charging does not imply an equipped ram.', 'revise'), 1707: ('Lil says she would punch a huge hole in the enemy ship if a ram were available.', "If we had a ram, I'd punch a huge hole in them!", 'Restore explicit huge hole,personal threat and equipment condition without claiming damage.', 'revise'), 1708: ('Maria proposes closing on the flagship and finishing the enemy in one push.', 'Shall we close on their flagship and finish them off in one go?', 'Preserve enemy flagship,concentrated finish and proposal rather than a guaranteed outcome.', 'revise')}


def main():
    assert not MANUSCRIPT.exists();ROOT.mkdir(parents=True,exist_ok=True)
    packet_path=Path('work/analysis/battle_bridge_v924/source_context_packet.json');packet=read(packet_path)
    ledger=read('translations/editorial_review_current_v1.json')
    assert ledger['records_editorially_completed']==966 and ledger['records_with_source_and_prose_pass']==969
    assert sha(ROM.read_bytes())==packet['candidate_sha256']==ledger['current_integrated_candidate']['sha256']
    assert len(packet['all162_original_battle_helper_main_and_ordinary_control_selections'])==162
    current,clean=map(NdsImage.open,(ROM,'work/clean.nds'))
    jp=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/__arm9__.bin'))
    en=current_entries(current.read_file('/COMMON/MESFILE.DK4'),current.read_file('/__arm9__.bin'))
    ordinary=[]
    for n in range(1471,1499):
        ordinary.append({'message_id':n,'source_Japanese':jp[n].text.decode('cp932'),'source_hex':jp[n].text.hex(),
            'source_reference':reference(jp[n]),'current_English':en[n].text.decode('cp932'),
            'current_text_hex':en[n].text.hex(),'current_reference':reference(en[n]),
            'already_reviewed_ordinary_context_no_new_credit':True})
    supplement=ROOT/'ordinary_context_and_terms.json'
    save(supplement,{'candidate_sha256':sha(ROM.read_bytes()),'source_clean_ROM_sha256':packet['source_clean_ROM_sha256'],
        'records':ordinary,'independent_alternatives_not_consecutive_dialogue':True,
        'established_term_documents':{p:sha(Path(p).read_bytes()) for p in ('translations/crew_help_manuscript_v1.json','translations/skill_terms_help_manuscript_v1.json','translations/character_name_localization_policy_v1.json')},
        'established_terms':{'シエン':'Xien','ゲルハルト':'Gerhard','カミル':'Camille','副官':'First Mate','停戦':'truce'},
        'Xien_evidence':{'ordinary_message1498_source_and_current':ordinary[-1],'prior_review':'docs/bridge_duties_v871_completion.md'},
        'Gerhard_source_and_current_evidence_message1985':{'Japanese':jp[1985].text.decode('cp932'),'English':en[1985].text.decode('cp932')},
        'truce_source_and_current_evidence_message356':{'Japanese':jp[356].text.decode('cp932'),'English':en[356].text.decode('cp932')},
        'Captain5_has_no_NPC_alternatives':True})
    sources={r['message_id']:r for r in packet['records_with_immediate_storage_neighbors']};rows=[]
    for n,(meaning,english,note,decision) in PROSE.items():
        s=sources[n]
        role,first,ordinary_first,has_npc=next(g for g in ((5,1681,1471,False),(6,1685,1475,True),(4,1697,1487,True)) if g[1]<=n<g[1]+(12 if g[3] else 4))
        index=n-first;hero=index-8 if has_npc and index>=8 else index if not has_npc else None
        voice=index if hero is None else None
        speaker=f'Native NPC voice class{voice}' if hero is None else ['Rafael','Hodram Joakim Bergstrom (genuine captain1)','Lil','Maria'][hero]
        assert english==' '.join(english.split()) and english.isascii() and not any(c in english for c in '%{}\n')
        if decision=='retain':assert english==s['current_English'].strip()
        rows.append({'id':f'COMMON_MESSAGE_{n}','message_id':n,'role_ID':role,'voice_class':voice,'protagonist_ID':hero,'speaker':speaker,
            'context':f'Independent activity0 battle working comment for role{role}:Captain5,First Mate6 or Helm4. Original12600 handles eight NPC voice alternatives for roles6/4;Captain5 NPC pointers are null. Original12720 handles four genuine protagonists for all three roles. Main12104 uses native battle fields8/12=0/1. These are independent alternatives,not consecutive speech or activity1 helper126A8. Dialogue does not execute maneuvers,grant equipment or guarantee victory.',
            'source_Japanese':s['source_Japanese'],'source_hex':s['source_hex'],'source_reference':s['source_reference'],
            'canonical_source_hex':s['canonical_text_hex'],'current_reference':s['current_reference'],
            'current_text_hex':s['current_text_hex'],'current_English':s['current_English'],
            'source_meaning':meaning,'english':english,'localization_note':note,'editorial_decision':decision,
            'native_argument_count':0,'review':{'source':True,'context':True,'localization':True,'naturalness':True,'formatting':False}})
    assert tuple(r['message_id'] for r in rows)==IDS and sum(r['editorial_decision']=='revise' for r in rows)==24
    save(MANUSCRIPT,{'format':'dk4-natural-dialogue-source-manuscript-v2','translation_policy':'natural-dialogue-v2','target_locale':'en-US',
        'encoder':'dialogue-relocatable-v1','consumer_layout_profile':'deck-battle-bridge-visible-v1',
        'review_gates':['source','context','localization','naturalness'],'formatting_review_pending':True,
        'status':'28-source-prose-reviewed-native-format-integration-and-actual-pending','file_path':'/COMMON/MESFILE.DK4',
        'source_clean_ROM_sha256':packet['source_clean_ROM_sha256'],'current_ROM':str(ROM),'current_ROM_sha256':sha(ROM.read_bytes()),
        'current_COMMON_sha256':packet['COMMON_sha256'],'current_ARM9_sha256':packet['ARM9_sha256'],
        'native_context_proof':str(packet_path),'native_context_proof_sha256':sha(packet_path.read_bytes()),
        'ordinary_context_supplement':str(supplement),'ordinary_context_supplement_sha256':sha(supplement.read_bytes()),
        'records':rows,'full_goal_complete':False})
    save(ROOT/'editorial_ledger_before_source_review.json',ledger)
    ledger['records_with_source_and_prose_pass']=ledger['records_with_source_prose_drafts']=997
    ledger['source_prose_reviewed_counts_by_file']['/COMMON/MESFILE.DK4']=996
    ledger['reviewed_but_incomplete_COMMON_IDs']=[750,751,752,*IDS]
    ledger['active_source_prose_drafts']={'native_message_IDs':[750,751,752,*IDS],
        'manuscripts':['work/analysis/market_contract_v758/unmapped_750_752_prose_DRAFT.json',str(MANUSCRIPT)],
        'status':'three-older-context-unmapped-and28-battle-bridge-source-prose-reviewed-format-release-pending',
        'note':'These31 pending reviewed entries are not the full remaining shared/routes/player prose or raw-source scope.'}
    checkpoint=('V925 source/prose-reviews28 battle Captain5/First Mate6/Helm4 comments1681-1708:24 revisions and4 retentions. '
        'All162 original battle-helper/main/ordinary controls pass;unsupported NPC Captain5 tables remain null. Drafts restore personal offers and limitations,barrage and hand-to-hand preparation,conditional city-surrender roles,Guild/truce suggestion,Xien,Camille and Gerhard,helm coordination and the eagerness idiom. '
        'Native layout,registered integration and actual scenes remain pending. V922 stays current;966 complete,997 source/prose reviewed. '
        'Older750-752,mood1833,special actors1885-1888,raw abandon-caption0x134E54,remaining shared/routes/player prose/raw inventory,separate graphics/all18 plaques,Samwell header and later older-record re-audit remain open;full goal active.')
    ledger['latest_checkpoint']=checkpoint
    ledger['battle_bridge_v925']={'status':'source-prose-reviewed-native-release-and-actual-pending','native_message_IDs':list(IDS),
        'manuscript':str(MANUSCRIPT),'source_context_proof':str(packet_path),'proposed_revisions':24,'justified_retentions':4,'completed_entries_added':0}
    ledger['research_checkpoints'].append({'id':'V925-Battle-Bridge28-source-prose','proof':str(packet_path),'manuscript':str(MANUSCRIPT),
        'new_source_prose_reviews':28,'completed_entries_added':0,
        'previous_goal_turn_classification':'progress:V922 shop676/677 preservation and earlier corrected actual scene verified;next28 Bridge packet available',
        'this_goal_turn_classification':'progress:28 faithful glosses,natural English decisions,exact references and ordinary-context/terminology supplement',
        'full_goal_complete':False})
    assert sum(ledger['source_prose_reviewed_counts_by_file'].values())==997
    save('translations/editorial_review_current_v1.json',ledger)
    doc=Path('docs/battle_bridge_v925_source_review.md')
    with doc.open('x',encoding='utf-8') as f:f.write('# V925: battle Bridge source review\n\n'+checkpoint+'\n')
    for d in map(Path,('docs/translation_progress.md','docs/editorial_review_goal.md','docs/todo.md','docs/known_issues.md')):
        with d.open('a',encoding='utf-8') as f:f.write('\n\n## V925: battle Bridge source review\n\n'+checkpoint+' See [V925 source review](battle_bridge_v925_source_review.md).\n')
    archive=Path('E:/Rota Nova translations/Editorial review/V925 Battle Bridge source review');assert not archive.exists();copied=[]
    for source in (MANUSCRIPT,packet_path,supplement,Path(__file__),doc,Path('translations/editorial_review_current_v1.json')):
        target=archive/source.absolute().relative_to(Path.cwd());target.parent.mkdir(parents=True,exist_ok=True);copy2(source,target)
        assert sha(source.read_bytes())==sha(target.read_bytes());copied.append({'source':str(source),'archive':str(target),'sha256':sha(target.read_bytes())})
    save(ROOT/'archive_manifest.json',{'files':copied,'all_hashes_verified':True,'completed_entries_added':0})
    print('28 source/prose reviews:24 revisions,4 retentions.966 complete,997 source/prose;native/release/actual pending.',flush=True)


if __name__=='__main__':main()
