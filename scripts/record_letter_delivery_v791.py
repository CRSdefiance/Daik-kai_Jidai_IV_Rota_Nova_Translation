"""Record actual courier progress and new unapproved arrival-text defects."""

import shutil
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT=Path('work/analysis/letter_delivery_v791')
LEDGER=Path('translations/editorial_review_current_v1.json')
DOC=Path('docs/letter_delivery_v791_checkpoint.md')
MANUSCRIPT=Path('translations/arrival_notices_editorial_manuscript_v1.json')
ARCHIVE=Path('E:/Rota Nova translations/Editorial review/V791 Courier delivery and arrival defects')


def main():
    assert not DOC.exists() and not ARCHIVE.exists()
    proof=read(ROOT/'delivery_verification.json');draft=read(MANUSCRIPT)
    assert len(proof['native_state_comparison'])==43 and len(proof['strict_whole_screen_controls'])==31
    assert len(draft['records'])==3 and all(not r['review']['formatting'] for r in draft['records'])
    assert not draft['whole_batch_completion_credit']
    ledger=read(LEDGER);assert ledger['records_editorially_completed']==444
    assert ledger['records_with_source_and_prose_pass']==496
    assert len(ledger['active_source_prose_drafts']['native_message_IDs'])==52
    protected={p:sha(Path(p).read_bytes()) for p in (
        'out/all_routes_combined_v788_candidate.nds','out/all_routes_combined_v788_candidate.xdelta',
        'out/raphael_natural_v2_accepted_base.nds','work/clean.nds','scripts/headless_desmume_v193.py',
        'translations/release_stack.json','E:/Rota Nova translations/Saves/Test fixtures/V751 disposable Istanbul donor.dsv')}
    assert protected['out/all_routes_combined_v788_candidate.nds']==proof['candidate_sha256']
    assert protected['out/raphael_natural_v2_accepted_base.nds']=='3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
    save(ROOT/'editorial_ledger_before_v791.json',ledger)
    summary=('V791 verifies normal registration and arrival of a pact termination notice and goodwill letter using '
        'disclosed qualification,random-input and deadline controls. Two1000-coin fees,two1-coin Inn stays,192 calendar ticks,'
        'original pact cancellation and inactive courier records are verified;43 exact paired cash/task snapshots and31 '
        'strict full-screen controls pass. Random gains and daily object outputs differ and are not approved as identical. '
        'Actual arrival347 ends with stray R while independent348 starts elations. Three notices346-348 now have source/prose '
        'drafts,two revised/one retained,with formatting/integration/corrected gameplay pending. '
        'V788 ROM/exact patch unchanged;444 complete,499 source/prose,55 pending. Full editorial and graphics goals remain unfinished.')
    DOC.write_text('''# V791: courier delivery and independent arrival-message defects

## Verified progress

Two completed20000-frame automated emulator cold boots use V788 and preceding
V783 with the same controller/stylus journal and isolated byte-exact Istanbul DSV.
The ordinary Guild menus register a pact termination notice and a goodwill letter
to Castor Co. The existing V790 qualification changes eight source-defined bytes;
the letters themselves are registered by original code. Each costs1000 coins and
advances48 calendar ticks. Only after both registrations do two existing deadline
words change to the next day. No record is fabricated or result forced.

Two normal Stay1Day Inn visits each cost1 coin. Couriers dispatch at midnight during
the second stay. The first stay ends later on the due date;the daily dispatcher
requires source clock field10==0 before calling91598. The original due comparison
is against the source day-update context+14. The termination handler changes the
alliance to neutral;the goodwill handler later improves relations. Both records
end with inactive kind11. Final cash6369 matches8371 minus2000 minus2;the full
calendar advance is192 ticks,including the two registration days and two Inn days.
Normal town return is frame20000. Original saves,ROMs,registry and harness stay exact.

The actual V788 termination draw raises friendship50->52 and goodwill adds5 to57.
The exact same input replay on V783 also finishes both deliveries and charges the
same fees,but random gains and some daily object outputs differ. Every compared
cash/state and courier-record snapshot matches(43);full model and actor/town/item/
goods comparisons are explicitly recorded as true or false rather than waived.
31 complete unmodified screens match,including all actual recipient dialogue
frames17200-18800 and the19600 Inn return.15 other frames remain unapproved pixel
comparisons;they include revised Guild prose,menu highlights,clock phases and the
random relationship-gain digit. This investigation does not claim full paired
presentation approval or identical uncontrolled RNG. The original courier engine
91598..93BAC and day dispatcherCB240..CB3C8 are exact to clean source in both ROMs.

## New source-proven formatting defect

Actual347 at17200 and18000 displays Castor Co. got a letter. followed by a stray R.
Actual348 at19200 starts elations rose5. These are independent native status
messages separated by recipient responses. Clean347 says the letter reached the
recipient;clean348 says the relationship score increased. Its leading R was
incorrectly placed in the earlier English message,matching the user's concern
about dropped letters and words borrowed across neighboring storage selections.

Three natural-dialogue-v2 drafts preserve the original recipient/amount argument:

| ID | Proposed standalone text | Decision |
| --- | --- | --- |
|346|%s refused to accept the letter.|Retain wording.|
|347|The letter has reached %s.|Revise delivery notice;remove stray R.|
|348|Relations improved by %s points.|Restore complete word and natural score report.|

The source gloss precedes localized English in the manuscript. Each record has
source/context/localization/naturalness approval and formatting=false. Native
paragraph dispatch,guard/pair behavior,long faction substitutions,complete font
planes/bounds,registered no-growth integration,exact clean-input patch and actual
corrected arrival playback remain required. No production fix is claimed yet.
Wider335-369 source/current inventory is evidence only;other entries receive no
review/completion credit from that inventory. Actual recipient responses2736/2738,
2711/2713 and2721 also remain in the broader eventual prose review.

## Still open

The49-entry diplomatic batch has actual six-type menus,cancellations,normal
registration and now a representative source-bound delivery lifecycle. The
CScheme virtual-name menu scope remains open;no such menu appeared during this
delivery. New source RTTI leads identify map-town/fleet/village/route classes,
but a broad word-reference scan includes secondary/construction tables and is
explicitly unapproved as a concrete dispatch proof. Do not claim those leads
close the selector or fabricate a CScheme list for an ordinary-gameplay claim.

444 completed(320 revised/124 retained),499 source/prose,55 pending(346-348,
750-752,1097-1145). Wider shared dialogue,all routes,help/other prose and the
separate graphics audit remain open.18 original plaques remain in audit;Online
low-resolution bodies stay excluded,brown comic marks stay preserved,and approved
Rafael/Joakim/Maria/Camille spellings remain. Revisit older record-based checks
after the full editorial goal completes.

## Evidence and reproduction

See work/analysis/letter_delivery_v791/delivery_verification.json,source_delivery_
and_subjects.json,arrival_source_packet.json and the exact baseline_replay_plan.json.
The adapter only replaces the condition-fixture import;its frozen original
harness/fixture/program hashes are saved with terminal reports. Failed assertions
about startup RAM sets,journal ROM identity and the prefixture relation were
corrected against actual metadata;none is counted as a passing result.

The initial process lost its interactive handle during context handoff at3200
before letter registration. Its exact live PID was verified and terminated;the
fresh recovered capture is authoritative and terminal. All later replay handles
are terminal. This is targeted emulator verification,not a full-route or hardware
playthrough. Defect screenshots are saved under E:/Rota Nova translations/
Screenshots/Test fixtures/V791 Courier delivery defects,not guide candidates.
''',encoding='utf-8')
    ledger['records_with_source_and_prose_pass']=499
    active=ledger['active_source_prose_drafts']
    active['native_message_IDs']=sorted(active['native_message_IDs']+[346,347,348])
    active['manuscripts'].append(str(MANUSCRIPT))
    active['status']='55-pending-including-unintegrated-arrival-notices-and-CScheme-name-menu-scope'
    active['note']='Three arrival notices are source/prose-reviewed drafts;347/348 have actual split-word defects.49 integrated diplomatic entries now have representative two-letter delivery evidence;CScheme virtual-name menu scope remains.750-752 context remains unmapped.'
    ledger['latest_checkpoint']=summary
    ledger['coverage_units'][0]['next']='Repair independent arrival notices346-348 via original paragraph consumer and registered no-growth release;verify corrected arrival scenes. Close actual CScheme virtual-name-menu scope. Then Palace1146 onward,750-752,all routes and remaining prose.'
    ledger['findings'].append({'id':'COMMON347-348-split-Relations-across-independent-notices','native_message_ids':[347,348],
        'status':'actual-defect-confirmed-source-prose-draft-not-integrated',
        'detail':'347 ends with stray R;348 begins elations.Independent original delivery and score notices have intervening recipient responses.',
        'proof':str(ROOT/'delivery_verification.json')})
    ledger['formatting_watchlist']['requirements'].append('Check independent system notices for letters or fragments mistakenly moved into adjacent storage selections;actual347/348 is a confirmed unfinished example.')
    checkpoint={'id':'V791-two-courier-delivery-and-arrival-defects','documentation':str(DOC),'new_editorially_completed':0,
        'new_source_prose_reviewed':3,'exact_cash_task_pairs':43,'strict_whole_screen_controls':31,
        'remaining':['Arrival347/348 production repair and revised playback','CScheme virtual name-menu scope','wider shared/routes/prose'],
        'full_goal_complete':False}
    ledger['research_checkpoints'].append(checkpoint)
    ledger['current_integrated_candidate'].update({'details':str(DOC),'supplemental_verification':str(ROOT/'delivery_verification.json'),
        'remaining_in_this_registered_batch':'CScheme virtual-name-menu scope. Independent old arrival347/348 have confirmed defects pending a new registered repair;random-stream daily-object equality remains unproven.',
        'latest_research_checkpoint':str(DOC)})
    save(LEDGER,ledger);save('out/editorial_review_latest.json',ledger['current_integrated_candidate'])
    heading='## V791: courier delivery and independent arrival-text defects'
    for name in ('docs/known_issues.md','docs/todo.md','docs/translation_progress.md','docs/editorial_review_goal.md'):
        path=Path(name);text=path.read_text(encoding='utf-8');assert heading not in text
        path.write_text(text+'\n\n'+heading+'\n\n'+summary+' See [V791 checkpoint](letter_delivery_v791_checkpoint.md).\n',encoding='utf-8')
    shots=[]
    for f,label in ((17200,'Stray R after letter arrival'),(19200,'Missing R in relationship notice')):
        source=Path('E:/Rota Nova translations/Generated/work/emulation_v193/letter_delivery_v791_recovered')/f'frame_{f:06d}_navigation.png'
        dest=Path('E:/Rota Nova translations/Screenshots/Test fixtures/V791 Courier delivery defects')/(label+'.png')
        dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,dest)
        assert sha(source.read_bytes())==sha(dest.read_bytes())
        shots.append({'source':str(source),'copy':str(dest),'sha256':sha(dest.read_bytes()),'defect_not_guide_material':True})
    assert all(sha(Path(p).read_bytes())==h for p,h in protected.items())
    save(ROOT/'checkpoint.json',{**checkpoint,'summary':summary,'completed':444,'source_prose':499,'pending':55,
        'previous_turn_classification':'progress:current repaired shop formatting identity and earlier actual framebuffer rechecked',
        'this_turn_classification':'progress:two actual courier lifecycles,paired state evidence,new source-proven defects and three drafts',
        'protected_files_exact':protected,'screenshots':shots,'producer_sha256':sha(Path(__file__).read_bytes()),
        'all_capture_processes_terminal':True})
    paths=list(ROOT.glob('*.json'))+[DOC,LEDGER,MANUSCRIPT]
    paths += [Path('scripts')/name for name in ('native_letter_delivery_v791.py','run_letter_delivery_v791.py',
        'replay_letter_delivery_v791.py','verify_letter_delivery_v791.py','review_arrival_notices_v791.py','record_letter_delivery_v791.py')]
    copied=[]
    for source in paths:
        dest=ARCHIVE/source;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,dest)
        assert sha(source.read_bytes())==sha(dest.read_bytes())
        copied.append({'source':str(source),'copy':str(dest),'sha256':sha(dest.read_bytes())})
    save(ROOT/'archive_receipt.json',{'copies':copied,'all_copies_SHA256_exact':True})
    shutil.copy2(ROOT/'archive_receipt.json',ARCHIVE/'archive_receipt.json')
    print(f'V791 recorded;{len(copied)} exact artifacts,two defect screenshots.444 complete,499 source/prose,55 pending.ROM unchanged;goal active.',flush=True)


if __name__=='__main__':main()
