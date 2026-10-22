"""Record six-type native/gameplay closure,without clearing delivery/name-menu gates."""

import shutil
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/letter_eligibility_v790')
DOC=Path('docs/letter_eligibility_v790_checkpoint.md')
LEDGER=Path('translations/editorial_review_current_v1.json')
ARCHIVE=Path('E:/Rota Nova translations/Editorial review/V790 Six diplomatic types and complete phrases')


def main():
    native=read(ROOT/'native_eligibility_verification.json')
    actual=read(ROOT/'actual_letter_dialogs.json')
    outcome=read(ROOT/'cancellation_outcomes.json')
    assert len(native['all22_original_menu_predicate_cases'])==22
    assert len(actual['holds'])==15 and len(actual['strict_whole_screen_controls'])==37
    assert len(actual['original_whole_frame_faction_highlight_controls'])==4
    assert len(actual['paired_native_state_model_object_task_frames'])==53
    assert len(actual['all_six_actual_command_labels_complete_native_ink_and_blank_cells'])==6
    assert outcome['cash8371_preserved_all53_native_snapshots'] and outcome['no_courier_registration_or1000_coin_charge_on_cancellation']
    assert sha(Path('out/all_routes_combined_v788_candidate.nds').read_bytes())==actual['candidate_sha256']=='12a5d245dd0dee433f1c21bd97680805a54bfe4770df99d54380d39548283820'
    assert native['producer_sha256']==sha(Path('scripts/verify_letter_eligibility_v790.py').read_bytes())
    assert actual['producer_sha256']==sha(Path('scripts/verify_letter_gameplay_v790.py').read_bytes())
    config=read('translations/item_diplomacy_editorial_release_v1.json')
    for p,h in config['dependencies'].items():assert sha(Path(p).read_bytes())==h,p
    for report_path in actual['source_reports']:
        report=read(report_path)
        donor=Path(report['battery_save_preloaded']['source'])
        assert sha(donor.read_bytes())=='d991cb3bcdf74eed7aeb58c9a75957766b7c820d002423fd2b55cc8493cf8132'
    captures=Path('E:/Rota Nova translations/Generated/work/emulation_v193/letter_eligibility_v790_live')
    photos=[]
    for frame,label in ((6800,'All six diplomatic commands'),(8800,'Pact termination confirmation'),
                        (11600,'Pact partner and opponent'),(21200,'Submission warning')):
        source=captures/f'frame_{frame:06d}_navigation.png'
        target=Path('E:/Rota Nova translations/Screenshots/Guide candidates')/f'V790 {label}.png'
        if target.exists():assert target.read_bytes()==source.read_bytes()
        else:shutil.copy2(source,target)
        assert sha(source.read_bytes())==sha(target.read_bytes())
        photos.append({'source':str(source),'copy':str(target),'sha256':sha(source.read_bytes()),
            'eight_disclosed_qualification_bytes':True,'actual_complete_glyphs_verified':True,'earned_progress_not_claimed':True})
    save(ROOT/'guide_candidates.json',photos)
    summary=('V790 closes native eligibility and actual cancellation/formatting samples for all six diplomatic types. '
        '22 original predicate cases and both complete six-mode target lists pass. An eight-byte source-defined Istanbul fixture supplies Gerhard First Mate/Speech215,regional proof acquired flag and two relation states;no menu flags or logic are overridden. '
        'All six command labels and all six complete nominal phrases appear in actual playback,including23-character pact termination notice. Fifteen complete holds across seven IDs,37 strict full-screen controls,four complete original faction-highlight controls and53 native state/model/object/task pairs pass. '
        'Pact partner/opponent order,submission warning,8371-coin balance,calendar,courier cancellation and normal town return are verified. '
        'These faction menus are not CScheme virtual-name menus;dynamic subject-selector and delivery lifecycle remain open. '
        'V788 ROM/exact patch unchanged;444 complete,496 source/prose,52 pending;full editorial and separate graphics goals unfinished.')
    DOC.write_text('''# V790: six diplomatic types and complete phrases in actual playback

## Status

V788 remains the experimental combined ROM with its registered exact clean-input
patch. ROM SHA25612a5d245dd0dee433f1c21bd97680805a54bfe4770df99d54380d39548283820.
No ROM,profile,canonical,original save,commit or push changes here. Editorial
coverage stays444 completed(320 revised/124 retained),496 source/prose and52
pending(750-752 and1097-1145). The49-entry letter family remains open for actual
CScheme name-menu scope and delivery lifecycle. All wider shared text,routes,
other prose and the separate graphics audit remain unfinished.

## Original eligibility and source-defined fixture

The existing Istanbul cartridge save has five living foreign factions in its
region. Source5BB4C selects targets by region,alive/active leader and relation
state. The original6-type constructor5B324 runs completely through its predicates
and stops before rendering;no menu flag is edited. Twenty-two native cases on
V783/V788 exercise real native qualification plus79/80,99/100,119/120,199/200 Speech
boundaries,missing proof,and an unassigned First Mate. Only the Speech getter is
a declared scalar input in boundary cases;the actual positive cases use the
unmodified getter and real fixture fields.

| Type | Original requirements exercised |
| --- | --- |
| Goodwill | Eligible regional foreign faction. |
| Sign Pact | Speech80 and at least two nonwar targets;opponent selection excludes player and partner. |
| Break Pact | Speech100 and an allied target. |
| Truce | Speech120 and a faction at war. |
| Declare War | Original extra availability predicate and a nonwar target. |
| Threaten | Speech200,acquired regional proof flag and independent target. |

The disposable live fixture changes eight bytes within nine source-defined
possible bytes:move actual companion Gerhard16 from room21 to the existing First
Mate room15,set his XP word300000(native Speech215),use the original one-byte
acquired-flag setter for item149 Cambyses' Crown,and set the two symmetric relation
fields for player faction2 with Castor Co.0(state1) and Albuquerque6(state2).
Both getter directions prove those relation values. All other4MiB bytes are exact.
The real native target counts for types0-5 become5,4,1,1,4,5. Money,location,
calendar,ship layout,code,menu flags and outcomes are untouched. This tests
disclosed prerequisites;it does not claim earned XP,proof acquisition or alliances.

The first preflight incorrectly equated faction2 with captain index2. The native
getter shows captain1;the failed check occurred before live fixture use and was
corrected. The formal cases and actual live receipt use that observed mapping.

## Actual menus,nominal phrases and confirmations

A24000-frame cold boot from an isolated byte-exact DSV copy reaches Istanbul's
Guild. All six localized commands are visible together. Their complete ink and
blank cells match independent native font masks. All six complete noun phrases
are used by actual question providers:goodwill letter,pact proposal,pact
termination notice,truce proposal,declaration of war,demand for submission.

The23-character pact termination notice is complete in the recipient question
and confirmation. The pact asks Castor Co. to oppose Albuquerque in the correct
source argument order. Truce correctly targets Albuquerque;war/goodwill and the
submission warning use Castor Co. The actual warning is1139 and its source
meaning is coming under the player's command,not the older unrelated choice
question. No translator-authored wrapping or padding is added.

Fifteen complete holds cover1097,1117,1098,1113,1103,1108,1139. Every hold binds
its exact resident block,owner template,printf arguments,wrapped bytes and full
independent native font plane. Complete leading/trailing letters,all words,
substitutions,margins,bounds and blank paper pixels pass. Old Japanese type
arguments and new complete English type arguments are bound separately to each
original getter;their expected translation is not treated as an argument mismatch.

## Controls and outcomes

The exact same controller/stylus journal replays on V783 with the same fixture.
Thirty-seven unselected full screens match exactly. Faction-highlight frames
11200/14000/17200/20800 require four original full-frame phase controls. A separate
observer adds only four100-frame read-only image windows,without altering inputs
or game logic. Each complete candidate frame matches an original frame in its
declared interval;no rectangular pixel exclusion is used. Original dialogue and
town reference frames remain exact across those original control runs.

All53 captured native financial/model/object/task pairs match between builds.
The real wallet getter shows8371 coins at every point. An initial visually guessed
83371 assertion was rejected and corrected to the native value;no charge or
gameplay defect was found. All confirmations and the submission warning are
cancelled. No1000-coin fee,no new courier and no calendar advancement occurs.
Postfixture company/fleet/ships,actors/towns/items/goods and task spans return
exactly to their starting state. The final town return is frame24000.

All emulator/process handles are terminal. Original saves and the frozen original
capture harness remain exact. These are targeted automated-emulator tests,not a
route playthrough,earned qualifications or physical-device verification.

## Actual class-menu distinction and remaining work

The actual faction selector9AEF4 encodes class4 objects. It is not the CScheme
class13 selector. Complete phrases in dialogue prove the real nominal providers
and paragraph crops;they do not approve a virtual CScheme name list. The earlier
native24-cell width/row proof remains valid,but its actual SDK/GPU name-menu scope
still needs closure. Other ordinary sources select actor class3 or fleet objects.
The remaining dynamic subject selector96704 has a direct source caller966B8;
its subject virtual method24 must be traced. This is a concrete next lead,not a
claim that document lists are unreachable or already tested.

Delivery also remains open. The V789 goodwill record is scheduled in the future;
acknowledgment and registration are not delivery completion. Next verify a
source-bound delivery cycle and any resulting messages/subject-name selectors.
The next unrevised shared range1146 onward is Palace contracts,defense and loaned
treasures;only its clean/current text was inspected here,no new prose-review
credit is awarded. Unmapped750-752 and every route/remaining prose remain open.

The six command-caption gameplay masks are supplemental graphics evidence only.
The original18 plaques stay open;Online screenshot-body exclusions,brown comic
marks and Rafael/Joakim/Maria/Camille remain unchanged. Revisit older record-based
checks after the entire editorial goal completes.

## Reproduction and storage

See work/analysis/letter_eligibility_v790/native_eligibility_verification.json,
actual_letter_dialogs.json,cancellation_outcomes.json and exact replay/observer
plans. Producers are native_letter_eligibility_v790.py,verify_letter_eligibility_v790.py,
run_letter_eligibility_v790.py,replay_letter_eligibility_v790.py,
run_letter_phase_v790.py and verify_letter_gameplay_v790.py. Capture folders must
be fresh. Four actual verified screenshots are saved on E under Screenshots/Guide
candidates with hashes and fixture provenance. Research observer images are not
promoted as guide material. Current evidence/producers are archived with receipts.
''',encoding='utf-8')
    ledger=read(LEDGER)
    assert ledger['records_editorially_completed']==444 and ledger['records_with_source_and_prose_pass']==496
    assert len(ledger['active_source_prose_drafts']['native_message_IDs'])==52
    save(ROOT/'editorial_ledger_before_v790.json',ledger)
    ledger['latest_checkpoint']=summary
    ledger['coverage_units'][0]['next']='Trace dynamic subject selector96704/caller966B8 and complete actual CScheme name-menu scope;verify a source-bound delivery cycle. Then1146 onward Palace contracts/treasure loans,750-752,all routes and remaining prose. Separate graphics audit/older-record follow-up remain open.'
    checkpoint={'id':'V790-six-letter-types-eligibility-and-actual-cancellations','documentation':str(DOC),
        'new_editorially_completed':0,'original_predicate_cases':22,'actual_complete_holds':15,'actual_IDs':[1097,1117,1098,1113,1103,1108,1139],
        'strict_whole_screen_controls':37,'original_whole_frame_phase_controls':4,'native_state_pairs':53,
        'all_six_actual_command_labels_and_complete_nominal_phrases':True,
        'remaining':['CScheme virtual name-menu scope','delivery lifecycle','wider shared/routes/prose'],
        'full_goal_complete':False}
    ledger['research_checkpoints'].append(checkpoint)
    ledger['active_source_prose_drafts']['note']='27 item entries complete.49 diplomatic entries have full native/source review and actual six-type eligibility,complete noun phrases/confirmations and cancellation evidence. Actual CScheme name-menu scope and delivery lifecycle remain open;three older unmapped contexts remain.'
    ledger['current_integrated_candidate'].update({'details':str(DOC),'supplemental_verification':str(ROOT/'actual_letter_dialogs.json'),
        'remaining_in_this_registered_batch':'Actual CScheme virtual name-menu scope and delivery lifecycle;conversation PRNG call-count source remains an investigation lead.',
        'latest_research_checkpoint':str(DOC)})
    save(LEDGER,ledger);save('out/editorial_review_latest.json',ledger['current_integrated_candidate'])
    heading='## V790: all six diplomatic types and complete phrases in actual playback'
    for name in ('docs/known_issues.md','docs/todo.md','docs/translation_progress.md','docs/editorial_review_goal.md'):
        path=Path(name);text=path.read_text(encoding='utf-8');assert heading not in text
        path.write_text(text+'\n\n'+heading+'\n\n'+summary+' See [V790 checkpoint](letter_eligibility_v790_checkpoint.md).\n',encoding='utf-8')
    save(ROOT/'checkpoint.json',{**checkpoint,'summary':summary,'completed':444,'source_prose':496,'pending':52,
        'candidate':ledger['current_integrated_candidate'],'all_capture_processes_terminal':True,
        'previous_goal_turn_classification':'progress:27 item entries complete and goodwill/controlled daily verification',
        'this_turn_classification':'progress:all six original eligibility predicates,actual command/phrase/confirmation masks and cancellations',
        'producer_sha256':sha(Path(__file__).read_bytes())})
    paths=[p for p in ROOT.glob('*.json') if p.name!='archive_receipt.json']
    paths += [ROOT/'effective_actual_letter_verifier.py',DOC,LEDGER]
    paths += [Path('scripts')/name for name in ('native_letter_eligibility_v790.py','run_letter_eligibility_v790.py',
        'verify_letter_eligibility_v790.py','replay_letter_eligibility_v790.py','run_letter_phase_v790.py',
        'verify_letter_gameplay_v790.py','record_letter_eligibility_v790.py')]
    copied=[]
    for source in paths:
        target=ARCHIVE/source;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,target)
        assert sha(source.read_bytes())==sha(target.read_bytes())
        copied.append({'source':str(source),'copy':str(target),'sha256':sha(source.read_bytes())})
    receipt={'archive':str(ARCHIVE),'copies':copied,'all_copies_SHA256_exact':True}
    save(ROOT/'archive_receipt.json',receipt);save(ARCHIVE/'archive_receipt.json',receipt)
    print(f'All six diplomatic types recorded;{len(copied)} artifacts and four guide candidates saved.444 complete,52 pending;goal active.',flush=True)


if __name__=='__main__':main()
