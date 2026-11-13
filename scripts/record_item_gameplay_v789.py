"""Close the27 item entries,retain49 letter entries and all wider goal scope."""

import shutil
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/item_transactions_v789')
DOC=Path('docs/item_transactions_v789_checkpoint.md')
LEDGER=Path('translations/editorial_review_current_v1.json')
ARCHIVE=Path('E:/Rota Nova translations/Editorial review/V789 Item transactions and goodwill registration')
IDS=list(range(1070,1097))


def main():
    ordinary=read(ROOT/'ordinary_transactions_gameplay.json')
    qualified=read(ROOT/'qualified_transactions_gameplay.json')
    outcomes=read(ROOT/'qualified_outcomes.json')
    daily=read(ROOT/'daily_update_control.json')
    gate=read(ROOT/'Guild_menu_gate.json')
    doc=read('translations/item_diplomacy_editorial_manuscript_v2.json')
    rows={r['message_id']:r for r in doc['records']}
    rom=Path('out/all_routes_combined_v788_candidate.nds')
    assert ordinary['candidate_sha256']==qualified['candidate_sha256']==sha(rom.read_bytes())=='12a5d245dd0dee433f1c21bd97680805a54bfe4770df99d54380d39548283820'
    assert len(ordinary['holds'])==11 and len(qualified['holds'])==17
    assert len(ordinary['strict_whole_screen_controls'])==19 and len(qualified['strict_whole_screen_controls'])==26
    assert len(qualified['original_whole_screen_highlight_phase_controls'])==3
    assert len(ordinary['paired_native_state_model_object_task_frames'])==27
    assert len(qualified['ordinary_exact_native_state_model_object_task_frames'])==40
    assert len(daily['same_PRNG_input_controlled_frames'])==3
    assert len(gate['all8_original_predicate_cases'])==8
    assert outcomes['accepted_confirmation_one1000_coin_fee_and_one_document']
    assert outcomes['document_due_at3187_still_pending_at_town_return2659']
    for proof,script in ((ordinary,'scripts/verify_item_transactions_v789.py'),
                         (qualified,'scripts/verify_item_roles_gameplay_v789.py'),
                         (daily,'scripts/verify_item_roles_gameplay_v789.py'),
                         (gate,'scripts/verify_guild_gate_v789.py')):
        assert proof['producer_sha256']==sha(Path(script).read_bytes())
    config=read('translations/item_diplomacy_editorial_release_v1.json')
    for p,h in config['dependencies'].items(): assert sha(Path(p).read_bytes())==h,p
    production=read('work/analysis/item_diplomacy_integration_v788/production_layout/verification.json')
    subset=[r for r in production['cases'] if r['id'] in IDS]
    assert len(subset)==77 and all(not r['findings'] for r in subset)
    fonts=[r for r in production['all76_complete_native_font_planes_exact_to_visually_reviewed_images'] if r['ID'] in IDS]
    assert len(fonts)==27 and all(sha(Path(r['path']).read_bytes())==r['sha256'] for r in fonts)
    assert all(rows[n]['decision']=='revise' and all(rows[n]['review'].values()) for n in IDS)
    ordinary_ids={r['message_id'] for r in ordinary['holds']}
    qualified_ids={r['message_id'] for r in qualified['holds'] if r['message_id'] in IDS}
    assert len(ordinary_ids|qualified_ids)==10
    item_holds=[r for r in ordinary['holds']+qualified['holds'] if r['message_id'] in IDS]
    assert len(item_holds)==21
    save(ROOT/'item_family_completion.json',{'native_message_IDs':IDS,'all27_five_editorial_gates':True,
        'source_manuscript':'translations/item_diplomacy_editorial_manuscript_v2.json',
        'source_manuscript_sha256':sha(Path('translations/item_diplomacy_editorial_manuscript_v2.json').read_bytes()),
        'all77_production_layout_cases':subset,'all27_complete_native_font_planes':fonts,
        'actual21_complete_holds_across10_IDs':item_holds,'all_other17_rows_have_full_source_native_font_and_family_sampling':True,
        'economic_cancellation_acceptance_and_normal_return_samples':True,
        'all76_batch_or_full_goal_completion_claim':False})
    copies=[]
    for folder,frame,name in [('item_transactions_v789_live',8000,'Guild purchase offer'),
                              ('item_roles_v789_live',7200,'Purser bargaining'),
                              ('item_roles_v789_live',7600,'Reduced purchase price'),
                              ('item_roles_v789_live',16800,'Goodwill confirmation')]:
        source=Path('E:/Rota Nova translations/Generated/work/emulation_v193')/folder/f'frame_{frame:06d}_navigation.png'
        target=Path('E:/Rota Nova translations/Screenshots/Guide candidates')/f'V789 {name}.png'
        if target.exists():assert target.read_bytes()==source.read_bytes()
        else:shutil.copy2(source,target)
        assert sha(target.read_bytes())==sha(source.read_bytes())
        copies.append({'source':str(source),'copy':str(target),'sha256':sha(source.read_bytes()),'actual_verified_complete_hold':True,
                       'role_fixture_used':folder=='item_roles_v789_live','whole_diplomacy_batch_or_earned_progress_not_claimed':True})
    save(ROOT/'guide_candidates.json',copies)
    ledger=read(LEDGER)
    assert ledger['records_editorially_completed']==417 and ledger['records_revised_and_integrated']==293
    completed={r['message_id'] for f in ledger['completed_editorial_families'] for r in f['records']}
    assert not completed.intersection(IDS)
    save(ROOT/'editorial_ledger_before_v789.json',ledger)
    family={'id':'Guild-item-buy-sell-and-Purser-bargaining1070-1096','native_message_IDs':IDS,'records':[]}
    for n in IDS:
        family['records'].append({'message_id':n,'decision':'revised-and-integrated',
            'manuscript':'translations/item_diplomacy_editorial_manuscript_v2.json',
            'source_native_context_and_complete_font_verified':True,
            'ordinary_actual_display_verified':n in ordinary_ids,'actual_display_with_disclosed_fixture':n in qualified_ids,
            'actual_display_scope':'21 complete holds across ten IDs sample real buy/sell/cancel and Purser bargain consumers;the other17 have complete clean-source/context,original wrapper/provider,production layout/font and family sampling,not individual activation.',
            'source_native_arguments':rows[n]['source_native_arguments'],
            'English_argument_source_indices':rows[n]['English_argument_source_indices'],
            'gameplay_evidence':str(ROOT/'item_family_completion.json')})
    ledger['completed_editorial_families'].append(family)
    ledger['records_editorially_completed']=444
    ledger['records_revised_and_integrated']=320
    assert ledger['retained_wordings_editorially_completed']==124
    pending=ledger['active_source_prose_drafts']
    pending['native_message_IDs']=[n for n in pending['native_message_IDs'] if n not in IDS]
    assert len(pending['native_message_IDs'])==52
    pending.update({'status':'750-752-context-unmapped;1097-1145-diplomacy-native-reviewed-integrated-partial-gameplay',
        'note':'27 item entries completed separately.49 diplomatic entries retain full native coverage and seven actual holds across five IDs,but remaining type eligibility,actual CScheme SDK/GPU name menus and delivery lifecycle remain open. Three older unmapped contexts remain.'})
    summary=('V789 completes27 revised item-shop/Purser entries1070-1096:444 completed(320 revised/124 retained),496 source/prose and52 pending. '
        '21 complete item holds across ten IDs,77 production layouts/27 fonts,ordinary7700 purchase/6160 sale,qualified7546 purchase/6314 sale and declines/normal returns pass. '
        'Two runs provide28 total holds,45 strict full-screen controls,three complete original highlight-phase controls and67 exact pre-day state/model/object/task pairs. '
        'Seven goodwill holds across five IDs verify full nominal/recipient substitutions,cancel without charge,and one1000-coin registration with one courier record and48 calendar ticks. '
        'Three controlled same-PRNG daily-update pairs match all covered native objects;ordinary conversation streams diverge and their daily object outputs are not claimed identical. '
        'Only three role bytes and a separately declared PRNG word are fixture inputs;production ROM/logic and saves remain unchanged. '
        'V788 ROM/exact patch stays current;49 diplomatic entries,actual CScheme menus,delivery,750-752,wider shared/routes/prose and separate graphics audit remain open.')
    ledger['latest_checkpoint']=summary
    ledger['coverage_units'][0]['next']='Finish1097-1145 type eligibility,actual CScheme SDK/GPU name menus and delivery lifecycle;map conversation PRNG call-count divergence without changing native production logic. Then1146 onward,750-752,all routes and remaining prose. Separate graphics audit and older-record follow-up remain open.'
    ledger['current_integrated_candidate'].update({'details':str(DOC),'supplemental_verification':str(ROOT/'qualified_transactions_gameplay.json'),
        'remaining_in_this_registered_batch':'49 diplomatic entries:other type eligibility,actual CScheme SDK/GPU names and delivery lifecycle;conversation PRNG divergence callsite remains unmapped.',
        'latest_research_checkpoint':str(DOC)})
    checkpoint={'id':'V789-items-complete-goodwill-registration-partial','documentation':str(DOC),
        'new_editorially_completed':27,'revised':27,'retained':0,'actual_total_holds':28,
        'strict_whole_screen_controls':45,'original_whole_frame_phase_controls':3,'ordinary_exact_native_pairs':67,
        'controlled_same_PRNG_daily_pairs':3,'full_goal_complete':False}
    ledger['research_checkpoints'].append(checkpoint)
    save(LEDGER,ledger)
    save('out/editorial_review_latest.json',ledger['current_integrated_candidate'])
    DOC.write_text('''# V789: item-shop entries complete;goodwill registration verified

## Coverage

COMMON1070-1096 are editorially complete:27 revisions. Total444 completed(320
revised/124 retained),496 source/prose reviewed,52 pending(750-752 and1097-1145).
All27 retain clean-source/context review,the original voice/provider/argument
contracts,77 production layouts and27 complete independently decoded font planes.
Ten IDs have21 actual complete holds;other17 use full native/font evidence and
representative consumer-family sampling,not individual scene activation.

V788 remains the experimental integrated ROM with its exact clean-input patch.
SHA25612a5d245dd0dee433f1c21bd97680805a54bfe4770df99d54380d39548283820.
Its canonical baseline remainsout/raphael_natural_v2_accepted_base.nds,
SHA2563cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe.
No ROM,profile,production code,canonical,original save,commit or push changes here.
The full editorial goal and separate graphics audit remain active and unfinished.

## Actual item transactions and ordinary controls

The unmodified-save15600-frame run tests buying,declining,then selling and declining.
It pays7700 coins,receives6160,and returns to town with37276 from38816. Eleven full
holds,six IDs,nineteen strict whole-screen controls and27 complete native financial,
company/fleet/ship,actor/town/item/goods and task-span pairs match the earlierROM.
No role,inventory,currency,location,health or timing fixtures are used in that run.
The expected cash change correctly changes the company hash;the first verifier's
assumption of an unchanged company after a real transaction was rejected. Fleet,
ships and persistent actor/town/item/goods objects return to their initial state.

## Three-byte role fixture and qualified gameplay

A fresh disposable Maria Seoul save copy receives exactly three source-mapped bytes:
assign Xien to the existing First Mate room15,set empty room2's type to Purser,and
assign Jam there. The original room/actor/role getters prove both assignments;
all other4MiB bytes remain exact. No stats,XP,money,health,inventory,calendar,menu
flags or outcomes are edited. This is a testing prerequisite,not earned progress.

The original Guild menu requires at least1000 coins and an assigned First Mate.
Eight original CPU predicate cases test999/1000 with assigned/unassigned controls
in both ROMs. Only the cash getter is a declared scalar boundary in those CPU
cases;actual emulator runs use their real funds. Source menu logic stays unchanged.

The20000-frame qualified run includes Jam's actual buying/selling objections and
the merchant's complete7546/6314 counteroffers. Ten item holds plus seven goodwill
holds make17 complete holds. Margins,whole words,leading/trailing characters,
native substitutions and all blank paper pixels pass independent complete font
masks. Across both primary runs:28 holds,45 strict full-screen controls,and three
additional original whole-frame highlight-phase controls. Only frames8800,13600,
19600 need those phase controls;the complete candidate screen matches the original
frame sequence,with no rectangular exclusions. Original control runs are terminal.

An initial frame classification omitted the real1071 hold at12800. Its image,
template and full glyph plane were inspected and it now receives actual-hold
coverage. Cached text behind menus receives no hold credit.

## Goodwill recipient,confirmation and original registration

Xien's1120 drafting line,1100 recipient question and1115 confirmation display
complete natural English. Original type0 getterreturns親善;V788 returnsgoodwill
letter. Both actual confirmations correctly bind Kurushima then the nominal type.
The original names/order and complete English expansions are checked independently.

Declining at16800 leaves37584 coins and all courier slots unchanged. Acceptance
creates one source-initialized type0 courier record in slot4,owned by company3,
handled by Xien10,targeting company17(Kurushima). Its due tick3187 remains in the
future at town return2659. The charge is exactly1000 coins after acknowledgment,
and calendar registration advances48 ticks. No delivery completion is claimed.

Source91480 scans indices[4,14),ten eligible courier slots. Its third argument is
an exclusive end index,not a count of14 slots. This source reading supersedes any
earlier count-based interpretation without rewriting frozen historical evidence.

## Random input and daily update scope

The ordinary PRNG streams diverge during conversations before the day update.
All covered persistent objects match through18800. After the day advances,some
NPC/town values differ,while tested finances,company/fleet/ships and document
records match. The ordinary daily object outputs are not asserted identical.
The exact conversation PRNG callsite causing the count difference remains unmapped.

Two separately labeled runs replay the same inputs and use original srand at18800
to supply the actual V783 reference seed548127170. The only extra input is that
one PRNG word(0-4 changed bytes);its whole8MiB write contract is verified. All
available pre-seed4MiB snapshots3200-18800 exactly match their corresponding
uncontrolled run. No dialogue,menu,daily logic,world object,document,calendar or
cash is edited. At19200/19600/20000,the covered finances,company/fleet/ships,
actors/towns/items/goods and task spans match between ROMs under identical random
input. This supports preservation of the tested daily processing;it does not
claim identical ordinary random streams or a complete game-world audit.

The combined comparison has67 exact ordinary pre-day native state pairs plus
three controlled same-PRNG post-day pairs. Some early startup snapshots exist
only in the controls;no unavailable original early-RAM comparison is claimed.

## Evidence,storage and remaining work

work/analysis/item_transactions_v789 contains ordinary_transactions_gameplay.json,
qualified_transactions_gameplay.json,qualified_outcomes.json,daily_update_control.json,
Guild_menu_gate.json,item_family_completion.json and exact replay/control plans.
Original DeSmuME harness and all registered V788 dependencies remain unchanged.
These are targeted cold-boot emulator tests,not a route playthrough or hardware
verification. All process handles are terminal. Four complete actual screenshots
are saved under E:/Rota Nova translations/Screenshots/Guide candidates with receipts;
native CPU previews and diagnostic phase captures are not guide screenshots.

Next:finish other diplomatic type eligibility,actual shared CScheme SDK/GPU menus
and all complete names,and the delivery lifecycle. Keep the49-entry diplomatic
family open despite seven actual goodwill holds. Then continue1146 onward,the
unmapped750-752 contexts,all routes and other prose. Earlier676/677 formatting
remains exact by unchanged V788 ROM identity. Original18 plaques remain open;
preserve Online body exclusions,brown marks and Rafael/Joakim/Maria/Camille.
Revisit older record-based checks at whole-goal completion.
''',encoding='utf-8')
    heading='## V789: item transactions complete;goodwill registration and same-input daily control'
    for name in ('docs/known_issues.md','docs/todo.md','docs/translation_progress.md','docs/editorial_review_goal.md'):
        path=Path(name);text=path.read_text(encoding='utf-8');assert heading not in text
        path.write_text(text+'\n\n'+heading+'\n\n'+summary+' See [V789 checkpoint](item_transactions_v789_checkpoint.md).\n',encoding='utf-8')
    save(ROOT/'checkpoint.json',{**checkpoint,'summary':summary,'completed':444,'source_prose':496,'pending':52,
        'candidate':ledger['current_integrated_candidate'],'all_runs_terminal':True,
        'previous_goal_turn_classification':'progress:V788 registered integration,exact patch,native coverage and actual prompt/startup',
        'this_turn_classification':'progress:27 item entries completed and actual goodwill/conditional daily verification',
        'producer_sha256':sha(Path(__file__).read_bytes())})
    sources=[p for p in ROOT.glob('*.json') if p.name!='archive_receipt.json']
    sources += [ROOT/'effective_qualified_gameplay_verifier.py',DOC,LEDGER]
    sources += [Path('scripts')/name for name in ('native_item_roles_v789.py','native_item_rng_v789.py','run_item_roles_v789.py',
        'run_item_rng_v789.py','replay_item_v789.py','replay_item_rng_v789.py','verify_guild_gate_v789.py',
        'verify_item_transactions_v789.py','verify_item_roles_gameplay_v789.py','record_item_gameplay_v789.py')]
    archived=[]
    for source in sources:
        target=ARCHIVE/source;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,target)
        assert sha(source.read_bytes())==sha(target.read_bytes())
        archived.append({'source':str(source),'copy':str(target),'sha256':sha(source.read_bytes())})
    receipt={'archive':str(ARCHIVE),'copies':archived,'all_copies_SHA256_exact':True}
    save(ROOT/'archive_receipt.json',receipt);save(ARCHIVE/'archive_receipt.json',receipt)
    print(f'27 item entries completed;444 total,52 pending. V788 unchanged;{len(archived)} artifacts and four guide candidates saved. Goal active.',flush=True)


if __name__=='__main__':main()
