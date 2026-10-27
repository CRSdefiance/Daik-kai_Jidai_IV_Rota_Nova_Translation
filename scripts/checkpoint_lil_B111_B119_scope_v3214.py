"""Preserve completed V3208 and document the next complete uncredited scope."""
from copy import deepcopy
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B111_B119_scope_checkpoint_v3214')
PRIOR=Path('work/analysis/editorial_handoff_verification_v3209/verified_handoff.json')
SOURCE=Path('work/analysis/lil_B111_B119_source_v3210b/complete182_clean_current_native_context.json')
BRANCH=Path('work/analysis/lil_B111_B119_branches_v3211/original_relative_skip_operand_proof.json')
CONTEXT=Path('work/analysis/lil_B111_B119_clean_context_v3213b/all182_complete_clean_exchange_context_notes.json')
TRANSCRIPTS=Path('work/analysis/lil_B111_B119_clean_transcripts_v3212/transcript_provenance.json')
SUMMARY="""V3214 preserves independently audited V3208 completion and registered experimental V3204:4425 contextual rereads/integrated/completed,3040 historically revised/1385 retained; source/prose4428 including2598 SC2, with all2826 reviewed route objects integrated. V3204 retains515 manifest batches/114 accepted layers, exact whole-ROM clean-input patch reconstruction,31 fresh opening/town framebuffer matches toV3144 and a viewed current six-frame sheet. V1492 remains promoted.

The next complete clean/current packet covers all182 unreviewed objects in nine SC2 B111-B119 exchanges:148 speeches(146 ordinary/two FE) and34 stored actor-style alternatives across six4100 objects/48slots. No player-choice objects occur. All305 clean/current commands match source shape and every raw speech header. All96 inline getters are freshly re-executed in clean/current code, preserving alias pointers, selectors, ABI, all4MiB and owner/input/boundary guards. All64 relative sites pass640 native clean/current skip cases. Fifteen predicate commands and one8100 event query remain to bind to current context.

All182 objects have been read in complete clean-only exchanges before older-English editorial comparison. Durable notes cover the monk's Buddhist rice-offering/courtesy lesson and politeness joke; grandfather-boy rescue/keepsake without inventing Lil kinship; jade valuation and building inference; reduced illegal slave/drug trade and cacao specialty; stone-tablet/mosque material inference; the separate stored Maria/bandit dialogue about colonial violence,slavery,revenge and great-power expansion; India building/map gift tip; mismatched statue/figurehead with distinct style6 meaning; tribal spiritual significance and exact24000-gold notice; and trend promotion,townspeople's smiles,profits,food/casino humor and alternative Guild-report speakers. SourceFI/FO and all conditional voices remain intact. No English revision,gloss/prose credit or completion credit is added by this source/context lead.

The initial3210 mapper rejected a stale all-D0 assumption. The six actual source actor-style objects useD0,D1,D6,D7 andDC;3210b binds every actual byte and retains the failed producer. Fresh dynamic-role/voice/consumer binding is required before target formatting; do not insert virtualD0 into other selectors' alternatives. B115 has WORD0000 at0x1B4 and another physical conversation region beginning with FE at0x1B8, including actor03/Maria and FO. Original VM/entry/route/macro semantics must be classified before relocation approval; do not assume a continuous cast,dead text,a new entry point,or company identity from a portrait. B114 query013F controls the address reaction. Both FE paragraphs and all NPC/item/site identities require native binding. These are new-source questions; the later older-record technical re-audit has not started.

Next: bind current actors/roles/styles,source control and mixed-region entry/macro semantics; compare older English only after that binding; write faithful glosses/natural prose or justified retentions; run all native/display/reference/representative/registered-release gates. B120 and235 B101-B110 objects remain completed and excluded. No new emulator run,selected next scene,nameplate,earned reward/progress,full route orhardware claim. COMMON750-752 callers and every wider untouched storyline/shared shop-town/random/help/player prose remain open,includingSourceItems/LocalProduct,five named-target leads and raw classificationB141/SC3B109. Keep graphics/all18 plaques separate and retain the later older-record technical re-audit/queued0D validation-gap lead without asserting an older runtime defect. Preserve every ROM,translation,executed producer/proof/failure and clean/canonical input. Full goal active; all jobs terminal."""

if __name__=='__main__':
    assert not ROOT.exists()
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);before=deepcopy(ledger)
    assert sha(lp.read_bytes())==read(PRIOR)['ledger_sha256']
    source,branch,context,transcripts=map(read,[SOURCE,BRANCH,CONTEXT,TRANSCRIPTS])
    assert source['current_ROM_sha256']==ledger['current_integrated_candidate']['sha256']
    assert source['total_editorial_objects']==182 and len(source['records'])==148 and len(source['typed_actor_style_records'])==34
    assert source['system_FE_panels']==2 and source['actor_style_objects']==6 and source['actor_style_slots']==48
    assert source['all_2000_group_text_commands_absent'] and source['typed_choice_records']==[]
    assert len(source['original_clean_current_inline_getter_cases'])==96
    assert source['distinct_actor_style_presentation_selectors']==[208,209,214,215,220]
    assert len(branch['cases'])==640 and len(branch['operands_requiring_adjustment_when_resizing'])==64
    assert context['all148speech_and34_actor_style_alternatives_read_in_complete_clean_exchanges']
    assert context['older_English_not_yet_editorially_compared'] and context['macro_company_identity_not_inferred_from_speaker_portrait']
    assert context['original_predicate_commands']==15 and context['original_event_queries']==1
    assert sum(len(b['all_clean_native_commands']) for b in source['blocks'])==305
    rows=source['records']+source['typed_actor_style_records']
    known={(r['file_path'],r['id']) for r in ledger['contextual_story_natural_dialogue_pass_v1871']['record_keys']}
    assert not known&{(r['file_path'],r['id']) for r in rows}
    documents=[Path('docs')/n for n in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']]
    assert documents[0].read_text(encoding='utf-8').startswith('# Current editorial handoff - V3208')
    ROOT.mkdir(parents=True)
    for p in [lp,*documents]:copy2(p,ROOT/(p.name+'.before'))
    lead=dict(status='182clean-current-objects-mapped;whole-clean-context-read;currentbindings-oldEnglish-prose-native-release-pending',
        blocks=list(range(111,120)),editorial_objects=182,speeches=148,ordinary=146,FE=2,
        actor_style_objects=6,actor_style_slots=48,unique_actor_style_alternatives=34,player_choices=0,commands=305,
        relative_sites=64,clean_current_skip_cases=640,clean_current_inline_getter_cases=96,predicates=15,event_queries=1,
        dynamic_actor_style_source_selectors=[208,209,214,215,220],
        source_packet=str(SOURCE),source_packet_sha256=sha(SOURCE.read_bytes()),
        branch_proof=str(BRANCH),branch_proof_sha256=sha(BRANCH.read_bytes()),
        clean_context_notes=str(CONTEXT),clean_context_notes_sha256=sha(CONTEXT.read_bytes()),
        clean_transcripts=str(TRANSCRIPTS),clean_transcripts_sha256=sha(TRANSCRIPTS.read_bytes()),
        whole_clean_context_read_before_older_English_comparison=True,older_English_editorial_comparison_pending=True,
        original_mixed_B115_entry_VM_route_and_FO_semantics_pending=True,
        source_prose_or_completion_credit_added=0,new_emulator_runs=0,
        concrete_source_risks=context['concrete_new_source_risks'],
        source_current_references=[{k:r[k] for k in ['id','file_path','block','source_reference','current_reference','source_hex','current_hex']} for r in rows])
    inventory=deepcopy(read(ledger['unfinished_editorial_scope_v3208']['path']))
    inventory['next_complete_B111_B119_source_scope_v3214']=lead
    inventory['next_focus']='Bind newsource D0/D1/D6/D7/DCroles/voices,current macros/consumers andB115second-region entry/VM/FO semantics;bindB114query013F. All182clean objects alreadyread inwhole exchanges;olderEnglishcomparison/gloss/prose/retentions andallnative/reference/representative/registeredrelease gates remainpending. Preserve allwider editorialscope,graphics separation andlatertechnical re-audit.'
    inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory)
    ledger['unfinished_editorial_scope_v3214']=dict(path=str(inv),sha256=sha(inv.read_bytes()),
        incomplete_COMMON=3,incomplete_route_source_prose=0,next_uncredited_editorial_objects=182,full_goal_complete=False)
    ledger['lil_B111_B119_next_source_lead_v3214']=lead;ledger['latest_checkpoint']=SUMMARY
    restored=deepcopy(ledger)
    for k in ['unfinished_editorial_scope_v3214','lil_B111_B119_next_source_lead_v3214']:restored.pop(k)
    restored['latest_checkpoint']=before['latest_checkpoint']
    assert restored==before and ledger['goal_status']=='active' and not ledger['full_goal_complete']
    save(lp,ledger)
    section='## V3214: Next182 clean-source objects and whole-exchange context; uncredited\n\n'+SUMMARY+'\n\nSource: '+SOURCE.as_posix()+'. Context: '+CONTEXT.as_posix()+'. Unfinished scope: '+inv.as_posix()+'. Registered V3204 release details remain inV3208 below.\n\n'
    for i,p in enumerate(documents):
        first,rest=p.read_text(encoding='utf-8').split('\n',1)
        p.write_text(('# Current editorial handoff - V3214' if i==0 else first)+'\n\n'+section+rest,encoding='utf-8',newline='\n')
    evidence={str(p):sha(p.read_bytes()) for p in [PRIOR,SOURCE,BRANCH,CONTEXT,TRANSCRIPTS,inv,Path(__file__),
        Path('scripts/map_lil_B111_B119_source_v3210.py'),Path('scripts/map_lil_B111_B119_source_v3210b.py'),
        Path('work/analysis/lil_B111_B119_source_tools_v3210a/source_selector_successor_receipt.json')]}
    save(ROOT/'checkpoint_receipt.json',dict(checkpoint='V3214',summary=SUMMARY,evidence=evidence,
        updated_files={str(p):sha(p.read_bytes()) for p in [lp,*documents]},prior_verified_handoff=str(PRIOR),
        new_source_prose_reviews=0,new_completed_records=0,source_prose=4428,completed=4425,
        fresh_reread=4425,fresh_integrated=4425,fresh_pending=0,historical_revised=3040,historical_retained=1385,
        next_uncredited_editorial_objects=182,candidate=ledger['current_integrated_candidate'],new_emulator_runs=0,
        goal_turn_classification='progress',all_jobs_terminal=True,full_goal_complete=False))
    print('V3214:next182objects/current refs/wholeclean context mapped;96getters/64spans/640skipcases.4425completed/V3204/exactpatch/currentstartup preserved;zero newcredit. Fullgoalactive.')
