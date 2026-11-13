"""Record combined Inn integration with partial, accurately scoped gameplay."""

from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch import inn_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT=owned.ROOT
DOC=Path('docs/inn_integration_v803_checkpoint.md')
LEDGER=Path('translations/editorial_review_current_v1.json')
ARCHIVE=Path('E:/Rota Nova translations/Editorial review/V803 Inn prose integration and verified families')
GUIDE=Path('E:/Rota Nova translations/Strategy Guide/Screenshots/V803 Inn verified')


def copy_exact(source,destination):
    raw=source.read_bytes();destination.parent.mkdir(parents=True,exist_ok=True)
    if destination.exists():assert destination.read_bytes()==raw
    else:destination.write_bytes(raw)
    assert sha(destination.read_bytes())==sha(raw)
    return dict(source=str(source),destination=str(destination),sha256=sha(raw))


def main():
    assert not DOC.exists() and not ARCHIVE.exists() and not GUIDE.exists()
    release=read(ROOT/'registered_verification.json');stay=read(ROOT/'stay_gameplay_verification.json')
    other=read(ROOT/'news_report_refusal_gameplay.json');startup=read(ROOT/'newgame_regression.json')
    assert release['candidate_sha256']==stay['candidate_sha256']==other['candidate_sha256']==startup['candidate_sha256']
    assert len(stay['actual_holds'])==5 and len(other['actual_holds'])==6
    assert len(startup['whole_screen_frame_pairs'])==7
    assert release['clean_input_reconstruction_byte_exact'] and release['complete_warm_cold_copies']==5076
    rom=NdsImage.open(release['candidate']);common=rom.read_file('/COMMON/MESFILE.DK4');arm=rom.read_file('/__arm9__.bin')
    entries=owned.current_entries(common,arm);blocks=IlnkContainer.parse(common).blocks
    mapping=[]
    for e in entries:
        row={k:v for k,v in vars(e).items() if k!='text'}
        row['text']=dict(sha256=sha(e.text),bytes=len(e.text))
        row['complete_payload_sha256']=sha(blocks[e.block][e.block_offset:e.copy_end]);mapping.append(row)
    save(ROOT/'complete_current_message_map_v803.json',dict(candidate_sha256=release['candidate_sha256'],
        COMMON_sha256=sha(common),ARM9_sha256=sha(arm),current_exact3668_entry_selection_map=mapping))
    current=dict(path=release['candidate'],sha256=release['candidate_sha256'],profile=release['profile'],
        MESFILE_sha256=release['COMMON_sha256'],ARM9_sha256=release['ARM9_sha256'],patch_sha256=release['patch_sha256'],
        manifest=str(Path(release['candidate']).with_suffix('.manifest.json')),
        status='experimental-Inn23-integrated-stays-market-reports-refusal-gameplay-verified-battle-and-early-departure-open',
        details=str(DOC),supplemental_verification=str(ROOT/'news_report_refusal_gameplay.json'),
        remaining_in_this_registered_batch='Actual battle/raid rumors1195-1198 with full relative-month prose and multi-night early-departure1199 remain;no whole23 completion credit yet.',full_goal_complete=False)
    ledger=read(LEDGER)
    before_path=ROOT/'editorial_ledger_before_v803.json'
    if ledger['current_integrated_candidate']['sha256']==release['candidate_sha256']:
        # Recover only our interrupted checkpoint write from its exact snapshot.
        assert before_path.exists() and not DOC.exists() and not ARCHIVE.exists()
        ledger=read(before_path)
    assert ledger['records_editorially_completed']==527 and ledger['records_with_source_and_prose_pass']==553
    if before_path.exists():assert read(before_path)==ledger
    else:save(before_path,ledger)
    ledger['previous_whole_batch_verified_candidate_V799']=ledger['current_integrated_candidate']
    ledger['current_integrated_candidate']=current
    ledger['current_native_relocation_reference']=str(ROOT/'complete_current_message_map_v803.json')
    ledger['active_source_prose_drafts']['manuscripts'].append('translations/inn_editorial_manuscript_v3.json')
    ledger['active_source_prose_drafts']['status']='750-752-context-unmapped;Inn23-integrated-partial-actual-family-verification'
    ledger['active_source_prose_drafts']['note']='All23 Inn paragraphs registered/integrated,with full native source/layout/copy checks and actual stays,market pairs,one Strategist report/info window and refusal. Actual1195-1199 samples remain. No23-entry completion credit yet;three older contexts750-752 remain.'
    ledger['next_Inn_source_packet'].update(status='registered-integrated-stays-market-report-refusal-verified;battles-raids-and-early-departure-pending',
        production_manuscript='translations/inn_editorial_manuscript_v3.json',registered_verification=str(ROOT/'registered_verification.json'),
        actual_stays=str(ROOT/'stay_gameplay_verification.json'),actual_news_report_refusal=str(ROOT/'news_report_refusal_gameplay.json'),completion_credit=0)
    for f in ledger['findings']:
        if f['id']=='COMMON1185-buyout-rumor-wrong-faction-question':
            f.update(status='corrected-integrated-and-actual-full-font-follow-up-verified',proof=str(ROOT/'news_report_refusal_gameplay.json'),
                detail='Actual original buyout1184 town/goods then1185 affected-company shows faithful missed-purchase disappointment. Full glyphs,consumed event,one-coin/day stay and normal return pass. No full-Inn23 or full-game completion claim.')
        if f['id']=='Inn-relative-month-prose-abbreviations':
            f.update(status='full-phrases-integrated-native144-cases-and-fonts-pass;actual-battle-raid-display-pending',proof=str(ROOT/'registered_verification.json'))
    ledger['formatting_watchlist']['latest_reference_proof']=str(ROOT/'registered_verification.json')
    ledger['formatting_watchlist']['reference_case']+=' V803 preserves repaired676/677 exactly. Five actual stay and six market/report/refusal holds match complete native glyphs and blank paper,including aligned rows and one-line duration. No fresh676/677 activation;actual1195-1199 still pending.'
    summary=('V803 integrates23 Inn paragraphs(19 revised/4 retained) after the full V799 stack,with complete relative-month prose in owned storage. '
        '35320 selector/ABI cases,140 whole8MiB status cases,144 month cases,1169 production layouts,96 complete fonts and5076 full warm/cold copies pass. '
        'All3645 other COMMON texts,opaque payloads,470 batches,114 accepted layers,prior profiles/routes/graphics and staged123040 bytes are preserved;clean-input patch reconstructs exactly. '
        'Five actual stay holds verify1+3-night charges/calendar,complete fonts,13 exact screens and15 object/state pairs;seven New Game frames match. '
        'Six additional actual holds verify both market-news pairs,Gerhard voice1 report/company-info window and zero-funds refusal,with source-input fixtures,full fonts,market consumption and normal returns. '
        'Actual battle/raid1195-1198 and early-departure1199 remain.527 complete/553 source-prose and26 pending unchanged;no Inn23 completion credit. Full editorial and separate graphics audit stay unfinished.')
    ledger['latest_checkpoint']=summary
    ledger['coverage_units'][0]['next']='Complete original Inn battle/raid1195-1198 and early-departure1199 actual samples using source-bound inputs. Then close Inn23 if all gates pass;continue shared1200+,older750-752 contexts,all routes and other prose.'
    ledger['research_checkpoints'].append(dict(id='V803-Inn-integrated-partial-family-gameplay',documentation=str(DOC),new_source_prose_reviewed=0,new_editorially_completed=0,new_ROM=True,full_goal_complete=False))
    save(LEDGER,ledger);save('out/editorial_review_latest.json',current)
    post={**release,'actual_revised_gameplay_pending':True,
        'actual_stays_verified':str(ROOT/'stay_gameplay_verification.json'),'actual_news_report_refusal_verified':str(ROOT/'news_report_refusal_gameplay.json'),
        'startup_verified':str(ROOT/'newgame_regression.json'),'actual_remaining_IDs':[1195,1196,1197,1198,1199],
        'exact_complete_message_map':str(ROOT/'complete_current_message_map_v803.json'),'full_goal_complete':False}
    save(Path(release['candidate']).with_suffix('.verification.json'),post)
    DOC.write_text('# V803: combined Inn integration and verified families\n\n'+summary+'\n\n'
        '## Experimental candidate\n\n'
        f"ROM: `{Path(release['candidate']).resolve()}`\n\nSHA-256: `{release['candidate_sha256']}`\n\n"
        f"Patch SHA-256: `{release['patch_sha256']}`. The neighboring manifest and post-test verification identify the exact stack and open gameplay work.\n\n"
        'Profile `all-routes-unified-v803` retains470 batches/114 accepted layers and all preceding profile stages. '
        'Canonical base remains `out/raphael_natural_v2_accepted_base.nds`, SHA-256 '
        '`3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`;no promotion. '
        'Only `/COMMON/MESFILE.DK4` and ARM9 change from V799. Complete source pins,entry references and '
        'runtime/argument proofs are in the manuscripts,release config and complete_current_message_map_v803.json.\n\n'
        '## Actual tests and scope\n\n'
        'The ordinary stay run reproduces the completed V799 schedule from a fresh donor copy without new fixtures. '
        'One night costs1 coin/48 ticks;three nights cost3/144 ticks. Every letter and all blank-paper ink match '
        'independent source fonts in five holds. Every outside-body pixel,13 other full screens and15 source object/state pairs match. '
        'Seven cold-boot/New Game frames match the established control. These are targeted automated DeSmuME tests,not a route playthrough or hardware test.\n\n'
        'Four further fresh donor copies use disclosed bounded inputs:three original room/assignment bytes enable Gerhard as Strategist; '
        'market tests additionally seed a typed pending regional event,with the original vtable and validity method retained. '
        'The zero-funds fixture calls the original money method and changes only the two differing money bytes. '
        'Fixtures replace no text,code,selection,menu flags or outcomes. Their exact initial4MiB replay,all changes and donor hashes pass. '
        'Both market pairs are consumed normally,one coin/48 ticks is charged,and the refusal changes no calendar or covered persistent objects. '
        'The report uses original role2/voice1 and opens the original company-info screen;B closes that screen to the Inn menu,then B returns to town. '
        'The first short report run ended at the Inn menu and is preserved as partial evidence;the completed fresh run records the full return. '
        'Naturally earned assignment,market events or campaign progress are not claimed.\n\n'
        '## Formatting and remaining work\n\n'
        'Natural-dialogue-v2 production manuscripts have exact clean/current/canonical pins and all five per-record gates. '
        'The original unregistered time manuscript omitted encoder/review declarations;its failed attempt is preserved and its header was fixed '
        'before registration or ROM construction. Existing profiles/configs and frozen producers remain unchanged. '
        'The prior shop676/677 and arrival346-348 corrections remain exact;no new activation of those scenes is claimed.\n\n'
        'Actual battle/raid rumors1195-1198,including their full relative-month argument,and the multi-night interrupt1199 remain next. '
        'Do not mark all23 Inn entries or the full goal complete from this checkpoint. Continue shared1200+,old750-752 contexts,all routes and other prose. '
        'Keep the separate graphics/18-plaque audit open. Revisit old record-based checks after full editorial completion.\n',encoding='utf-8')
    for name in ('todo','translation_progress','editorial_review_goal','known_issues'):
        p=Path('docs')/(name+'.md');text=p.read_text(encoding='utf-8');heading='## V803: Inn integration and verified families'
        assert heading not in text;p.write_text(text+'\n\n'+heading+'\n\n'+summary+' See [V803 checkpoint](inn_integration_v803_checkpoint.md).\n',encoding='utf-8')
    archived=[]
    paths=[DOC,LEDGER,Path('translations/inn_editorial_release_v1.json'),Path('translations/inn_editorial_manuscript_v3.json'),Path('translations/inn_time_phrases_manuscript_v2.json')]
    paths += [ROOT/p for p in ('registered_verification.json','production_layout.json','prospective_common_repack.json','complete_current_message_map_v803.json',
        'stay_gameplay_verification.json','news_report_refusal_gameplay.json','newgame_regression.json','input_fixture_preflight.json')]
    paths += [ROOT/f'native_copies/native_copies_block_{b:02d}.json' for b in range(15,41)]
    for path in paths:archived.append(copy_exact(path,ARCHIVE/path.name))
    for scenario in other['scenarios']:
        path=Path(scenario['report']);archived.append(copy_exact(path,ARCHIVE/(path.parent.name+'_capture_report.json')))
    guide=[]
    for hold in stay['actual_holds']+other['actual_holds']:
        path=Path(hold['capture']['path']);destination=GUIDE/(f"COMMON{hold['message_id']}_"+path.name)
        receipt=copy_exact(path,destination);receipt.update(message_id=hold['message_id'],fixture_scope=hold.get('scenario','ordinary donor stay'))
        guide.append(receipt)
    for f,label in ((6000,'Original_company_information'),(6800,'Town_return_after_report')):
        p=Path(f'E:/Rota Nova translations/Generated/work/emulation_v193/inn_v803_report_complete/frame_{f:06d}_navigation.png')
        guide.append(copy_exact(p,GUIDE/(label+'.png')))
    save(ARCHIVE/'archive_manifest.json',dict(candidate=current,artifacts=archived,screenshots=guide,
        unearned_fixture_progress_not_claimed=True,remaining_actual_IDs=[1195,1196,1197,1198,1199],full_goal_complete=False))
    save(GUIDE/'screenshots_manifest.json',dict(candidate=current,screenshots=guide,
        label='Verified localized screens for later guide use;fixture scopes disclosed per sample,not earned campaign evidence.',full_goal_complete=False))
    print(f'V803 recorded with{len(archived)} exact archived artifacts/{len(guide)} guide screenshots;527 complete/553 reviewed,Inn23 completion still open.',flush=True)


if __name__=='__main__':main()
