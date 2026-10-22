"""Checkpoint actual loan/reclaim and the newly found menu-boundary defect."""

import shutil
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/palace_gameplay_v798')
DOC=Path('docs/palace_treasure_v798_checkpoint.md')
ARCHIVE=Path('E:/Rota Nova translations/Editorial review/V798 Palace treasure loan and reclaim')
GUIDE=Path('E:/Rota Nova translations/Strategy Guide/Screenshots/V798 Palace treasure')


def main():
    assert not DOC.exists() and not ARCHIVE.exists()
    proof=read(ROOT/'treasure_gameplay_verification.json')
    assert len(proof['five_repaired_holds'])==5 and len(proof['native_transfer_replays'])==2
    assert proof['item_reclaimed_all_persistent_objects_match_post_fixture_start']
    ledger_path=Path('translations/editorial_review_current_v1.json');ledger=read(ledger_path)
    assert ledger['records_editorially_completed']==496 and ledger['records_with_source_and_prose_pass']==530
    save(ROOT/'editorial_ledger_before_v798.json',ledger)
    ledger['palace_next_source_packet']['actual_treasure_sample']=str(ROOT/'treasure_gameplay_verification.json')
    ledger['palace_next_source_packet']['next']='Repair the confirmed Palace Contract label terminator;finish actual Market-letter,defense and successful/refused-contract family samples. Keep31-entry completion gate open.'
    ledger['findings'].append({'id':'Palace-Contract-Cstring-no-NUL','status':'actual-defect-source-confirmed;bounded-V799-research-repair-native-verified;registered-ROM-and-actual-menu-pending',
        'source_label_address':0x02143DF4,'actual_capture':'E:/Rota Nova translations/Generated/work/emulation_v193/palace_v798_treasure/frame_007200_navigation.png',
        'source_proof':'work/analysis/palace_label_boundaries_v799/source_ownership.json',
        'detail':'Eight ASCII bytes Contract fill the original eight-byte source allocation without a NUL. The original Palace menu row reads onward into adjacent RTTI and Mil Invest. The adjacent leading vtable zero word is not spare text. All six source-label reference edges are mapped;repack source-owned text fields and rebind menu pointers.'})
    ledger['observed_item_prose_leads_during_V798']={'native_COMMON_message_IDs':[2828],
        'capture':'E:/Rota Nova translations/Generated/work/emulation_v193/palace_v798_treasure/frame_005600_navigation.png',
        'detail':'Alchemy Book description has awkward English. Inventory/context lead only;clean Japanese and full item-description family review remain required. Rocco sailing-guide description was also observed,not yet mapped/reviewed.',
        'no_review_or_completion_credit':True}
    ledger['current_integrated_candidate']['status']='experimental-inherited-Palace-menu-boundary-defect-confirmed'
    ledger['current_integrated_candidate']['additional_actual_verification']=str(ROOT/'treasure_gameplay_verification.json')
    ledger['current_integrated_candidate']['remaining_in_this_registered_batch']='Treasure loan/reclaim and contract-cancel samples verified. Palace menu terminator repair,Market letters,defense and successful/refused contracts remain pending.'
    summary=('V798 verifies actual Palace loan1164/monthly offer1166/acceptance1167/reclaim1169/return1171 in V797. '
        'A disclosed two-byte temporary-headquarters/Alchemy Book input enables the original menu;no menu flags or outcomes are forced. '
        'All five holds match complete independent native fonts,including250 coins per month. Original4A610/49F30 loan and reclaim replays '
        'match all covered actor/item/town/goods/model/financial/task objects. The book returns to owned state,cash stays8371,and the donor save is unchanged. '
        'No calendar month or actual monthly payment is claimed. A separate inherited Palace menu defect is now confirmed:Contract lacks its NUL and reads neighboring RTTI/label data. '
        'V799 source-bounded label repair passes native reads/copies/fonts but still needs registration and actual menu playback. '
        '496 complete/530 source-prose reviewed/34 pending unchanged;full goal active and separate graphics audit unfinished.')
    ledger['latest_checkpoint']=summary
    ledger['research_checkpoints'].append({'id':'V798-actual-Palace-treasure-and-menu-boundary-finding',
        'documentation':str(DOC),'new_editorially_completed':0,'new_ROM':False,'full_goal_complete':False})
    save(ledger_path,ledger);save('out/editorial_review_latest.json',ledger['current_integrated_candidate'])
    DOC.write_text('# V798: actual Palace treasure loan and reclaim\n\n'+summary+'\n\n'
        'The actual10200-frame DeSmuME run cold-boots an isolated copy of the unchanged Istanbul donor. '
        'The two input bytes temporarily make Istanbul headquarters (original headquarters getter3CD24) '
        'and grant Alchemy Book13 through original acquired setter4A204. Original loan menu filtering, '
        'item selection,yes/no response and transfer code still execute. This is not naturally earned '
        'headquarters travel,treasure discovery or letter eligibility.\n\n'
        'Actual holds:5200=1164,6000=1166 with250,6400=1167,8200=1169,9000=1171. '
        'Loan transfer completes by6800;reclaim by9400;normal town at10200. '
        'Alchemy Book has native price12500;the original unsigned multiplier/shift yields250 monthly. '
        'The original loan/reclaim method replays independently reproduce all covered persistent state. '
        'Price-sensitive rare-item alternate comments remain native/source-covered rather than separately '
        'activated;remaining Palace families are still open.\n\n'
        'The expanded Palace menu exposes an inherited nonterminated Contract string. Its source slot '
        'is eight bytes;the English label itself is eight bytes. Source-owned repacking is required. '
        'The leading zero at143E4C belongs to the following vtable and must remain untouched. '
        'A historical Guild-tail lead was rejected because V797 now uses it for an India label. '
        'The cannon-name tail was not reused because ownership of its last zero was not established. '
        'These findings reinforce the requirement to verify current ownership before using old records.\n\n'
        'Alchemy Book COMMON2828 and the displayed Rocco sailing-guide description are wider prose '
        'review leads,not approved translations. No new COMMON completion credit or canonical promotion. '
        'The independent graphics audit/18 plaques,Online-body exclusion,brown marks and approved names remain unchanged.\n',encoding='utf-8')
    for name in ('known_issues','todo','translation_progress','editorial_review_goal'):
        p=Path('docs')/(name+'.md');p.write_text(p.read_text(encoding='utf-8')+'\n\n## V798: Palace treasure and menu-boundary defect\n\n'+summary+
            ' See [V798 checkpoint](palace_treasure_v798_checkpoint.md).\n',encoding='utf-8')
    GUIDE.mkdir(parents=True,exist_ok=True);guide=[]
    for row in proof['five_repaired_holds']:
        source=Path(row['capture']['path']);dest=GUIDE/f"COMMON{row['id']}_verified.png"
        assert not dest.exists();shutil.copy2(source,dest);assert sha(source.read_bytes())==sha(dest.read_bytes())
        guide.append({'id':row['id'],'path':str(dest),'sha256':sha(dest.read_bytes()),'source_capture':str(source)})
    save(GUIDE/'provenance.json',{'screenshots':guide,'ROM_sha256':proof['candidate_sha256'],
        'disclosed_temporary_headquarters_and_owned_item_fixture':True,'menu_boundary_defect_not_included_in_these_dialogue_crops':True,
        'candidate_still_experimental':True,'full_goal_complete':False})
    files=[DOC,ledger_path]+list(ROOT.glob('*.json'))+[Path('scripts')/p for p in ('native_palace_fixture_v798.py',
        'run_palace_capture_v798.py','verify_palace_fixtures_v798.py','verify_palace_treasure_v798.py','record_palace_treasure_v798.py')]
    copies=[]
    for source in sorted(set(files)):
        assert not source.is_absolute();dest=ARCHIVE/source;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,dest)
        assert sha(source.read_bytes())==sha(dest.read_bytes());copies.append({'source':str(source),'copy':str(dest),'sha256':sha(dest.read_bytes())})
    receipt={'copies':copies,'all_copies_SHA256_exact':True,'guide_candidates':guide,'full_goal_complete':False}
    save(ROOT/'archive_receipt.json',receipt);save(ARCHIVE/'archive_receipt.json',receipt)
    print(f'V798 proof/progress saved;{len(copies)} exact archive copies and5 guide candidates;496 complete unchanged;goal active.',flush=True)


if __name__=='__main__':main()
