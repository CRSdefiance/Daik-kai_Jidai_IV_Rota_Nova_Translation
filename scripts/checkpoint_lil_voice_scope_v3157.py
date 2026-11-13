"""Record the next native actor-style scope without editorial credit."""
from copy import deepcopy
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_voice_scope_checkpoint_v3157')
PRIOR = Path('work/analysis/editorial_handoff_verification_v3155/verified_handoff.json')
PROOF = Path('work/analysis/lil_4100_alternatives_v3156/all14_clean_current_eight_style_alternatives.json')
SUMMARY = (
    'V3157 classifies the next source0x4100 objects as actor-style dialogue alternatives, not player choices. '
    'Original code reads actor record byte1C through7E988, uses2A154 for the style pointer, then2425C for dispatch. '
    'All14 objects have eight inline slots:112 slots reference90 unique stored strings, including shared pointers. '
    'All224 clean/current getter cases preserve pointers, ABI, all4MiB, owner, input and boundary guards. '
    'The source has an18byte table plus2byte selector and textbase20;low-byte masks are zero. '
    'Do not apply the2100 player-choice decoder,VM or menu renderer to these objects. '
    'The unreviewed B101-B119 scope contains402 editorial objects:312 speeches(280ordinary/32FE) and90 stored alternatives. '
    'First ten complete B101-B110 exchanges contain220 objects:164 speeches(134ordinary/30FE) and56 alternatives across8objects/64slots. '
    'Remaining B111-B119 contains182 objects:148 speeches and34 alternatives across6objects/48slots. '
    'B120 is already completed and receives no duplicate credit. '
    'DynamicCF/D0 selectors, actor/style voice mapping, complete source/current context, runtime substitutions, native display, '
    'wrapping, leading/trailing glyphs, bounds, pagination, transitions, relocation and representative/release gates remain pending. '
    'Read whole clean exchanges before comparing old English. This classification adds zero prose/completion credit and no gameplay claims. '
    'The five0400sites and50clean/current cases establish that only result2 skips. The scoped explicitFFFFFFFF inventory input '
    'exposes all speech headers without changing runtime, global helpers or gameplay state;3150/3151failures and3151bdiagnostic remain preserved. '
    'This is next-source mapping;the later older-record technical re-audit has not started. '
    'Completed V3148 remains independently verified:4190 contextual rereads/integrated/completed,2923historically revised/1267retained; '
    'source/prose4193including2363SC2,and2591reviewedrouteobjects integrated. ExperimentalV3144 retains512manifestbatches/114acceptedlayers, '
    'exact whole clean-input patch reconstruction and31current opening/town framebuffer matches toV3103. '
    'No new emulator run, selected next scene, nameplate, earned progress, full route or hardware claim. '
    'COMMON750-752callers,all wider untouched storylines/sharedshop-town/random/help/playerprose,SourceItems/LocalProduct,five named-target leads, '
    'raw rejected classification includingB141,SC3B109,separate graphics/all18plaques andlater older-record technical re-audit remain open. '
    'Queued0Dvalidationgap remains for later without asserting anolder runtime defect. All completed families remain completed. '
    'Preserve every ROM,translation,executed producer/proof/failure and clean/canonical input. V1492remains promoted. Fullgoalactive;all jobs terminal.'
)

if __name__ == '__main__':
    assert not ROOT.exists()
    lp = Path('translations/editorial_review_current_v1.json')
    ledger = read(lp)
    before = deepcopy(ledger)
    assert sha(lp.read_bytes()) == read(PRIOR)['ledger_sha256']
    proof = read(PROOF)
    assert proof['native_inline_getter_cases'] == 224
    assert len(proof['objects']) == 14 and len(proof['records']) == 90
    assert proof['player_choice_count_pointer_VM_and_choice_renderer_must_not_be_applied']
    assert all(o['not_a_player_menu'] and len(o['versions']) == 2 and all(len(v['style_slots']) == 8 for v in o['versions']) for o in proof['objects'])
    assert len([r for r in proof['records'] if r['block'] <= 110]) == 56
    docs = [Path('docs') / n for n in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']]
    assert docs[0].read_text(encoding='utf8').startswith('# Current editorial handoff - V3154')
    ROOT.mkdir(parents=True)
    for p in [lp, *docs]:
        copy2(p, ROOT / (p.name + '.before'))
    lead = deepcopy(ledger['lil_next_clean_scope_lead_v3154'])
    lead.update(status='clean-current4100-pointers-classified;context-prose-consumer-and-display-pending',
        alternative_proof=str(PROOF), alternative_proof_sha256=sha(PROOF.read_bytes()),
        source_4100_label_count_and_decoder_consumer_unbound=False, source_4100_not_player_choices=True,
        source_4100_style_slots=112, source_4100_unique_stored_alternatives=90, total_editorial_objects=402,
        next_source_4100_style_slots=64, next_source_4100_unique_stored_alternatives=56, next_editorial_objects=220,
        remaining_source_4100_unique_stored_alternatives=34, remaining_editorial_objects=182,
        all_current_macro_dynamic_actor_voice_native_display_reference_and_prose_gates_pending=True,
        source_alternative_references=[{k:r[k] for k in ['id','file_path','block','command_offset','style_indices','source_reference','current_reference','source_hex','current_hex','source_selector']} for r in proof['records']])
    inventory = deepcopy(read(ledger['unfinished_editorial_scope_v3154']['path']))
    inventory['next_clean_current_uncredited_exchange_scope_v3156'] = lead
    inventory['next_focus'] = 'Bind complete B101-B110 source/current context for220objects:164speech and56stored actor-style alternatives in8source4100objects. Preserve every style alias and dynamic selector. Then full clean context,old English comparison,faithful prose and distinct native/release gates. Later B111-B119 has182objects;B120 already completed.'
    inv = ROOT / 'unfinished_editorial_scope_inventory.json'
    save(inv, inventory)
    ledger['unfinished_editorial_scope_v3157'] = dict(path=str(inv),sha256=sha(inv.read_bytes()),incomplete_COMMON=3,incomplete_route_source_prose=0,next_editorial_objects=402,next_first_ten_editorial_objects=220,full_goal_complete=False)
    ledger['lil_next_voice_scope_lead_v3157'] = lead
    ledger['latest_checkpoint'] = SUMMARY
    restored = deepcopy(ledger)
    for key in ['unfinished_editorial_scope_v3157','lil_next_voice_scope_lead_v3157']:
        restored.pop(key)
    restored['latest_checkpoint'] = before['latest_checkpoint']
    assert restored == before and ledger['goal_status'] == 'active' and not ledger['full_goal_complete']
    save(lp, ledger)
    section = '## V3157:actor-style alternatives classified;next220objects uncredited\n\n' + SUMMARY + '\n\nAlternative classification: ' + PROOF.as_posix() + '. Unfinished scope: ' + inv.as_posix() + '. Completed V3144release/patch/currentstartup details remain inV3148below.\n\n'
    for i,p in enumerate(docs):
        firstline,rest = p.read_text(encoding='utf8').split('\n',1)
        p.write_text(('# Current editorial handoff - V3157' if i == 0 else firstline) + '\n\n' + section + rest,encoding='utf8',newline='\n')
    evidence = {str(p):sha(p.read_bytes()) for p in [PRIOR,PROOF,inv,Path(__file__),Path('scripts/classify_lil_4100_alternatives_v3156.py')]}
    save(ROOT/'checkpoint_receipt.json',dict(checkpoint='V3157',summary=SUMMARY,evidence=evidence,updated_files={str(p):sha(p.read_bytes()) for p in [lp,*docs]},prior_verified_handoff=str(PRIOR),new_source_prose_reviews=0,new_completed_records=0,source_prose=4193,completed=4190,fresh_reread=4190,fresh_integrated=4190,fresh_pending=0,historical_revised=2923,historical_retained=1267,next_editorial_objects=402,next_first_ten_editorial_objects=220,candidate=ledger['current_integrated_candidate'],new_emulator_runs=0,all_jobs_terminal=True,full_goal_complete=False))
    print('V3157:90stored actor-style alternatives classified;first56+164speech=220objects.402objects scoped withoutcredit;4190completed/V3144 preserved. Fullgoalactive.')
