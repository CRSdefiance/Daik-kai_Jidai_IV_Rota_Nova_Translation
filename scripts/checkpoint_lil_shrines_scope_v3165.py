"""Record the next native actor-style scope without editorial credit."""
from copy import deepcopy
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_shrines_scope_checkpoint_v3165')
PRIOR = Path('work/analysis/editorial_handoff_verification_v3158/verified_handoff.json')
SOURCE = Path('work/analysis/lil_Shrines_Temples_source_v3163/complete235_clean_current_native_context.json')
CHOICE = Path('work/analysis/lil_three_option_source_v3162/all5_three_option_clean_current_native_pointer_proof.json')
CONTEXT = Path('work/analysis/lil_Shrines_Temples_context_v3164b/complete_clean_exchange_context_notes.json')
BRANCH = Path('work/analysis/lil_Shrines_Temples_branches_v3160/original_relative_skip_operand_proof.json')
PROOF = Path('work/analysis/lil_4100_alternatives_v3156/all14_clean_current_eight_style_alternatives.json')
SUMMARY = 'V3165 preserves completed V3148 andthe registered V3144 release:4190contextual rereads/integrated/completed,2923historically revised/1267retained;source/prose4193including2363SC2,and2591reviewedrouteobjects integrated. V3144 retains512manifestbatches/114acceptedlayers,exactwhole clean-inputpatch reconstruction and31current opening/town framebuffer matches toV3103. The next complete B101-B110 source/current packet nowhas235objects:164speech(134ordinary/30FE),56stored actor-style alternatives across8source4100objects/64slots,and15player-answer labels in5source2200three-option menus. The earlier220object packet andinitial transcripts omitted the15choice labels andremain preserved asnonexhaustive predecessors. The native2200count/pointer getter passes40clean/current calls;sourceindex0/1/2 and8bytetextbase arebound,while selection/cancel/VM,geometry andfullnative menu display remainpending. Source4100 iseight actor-style alternatives,not playerchoices;all14broader objects/112slots/90stored strings retain224clean/current getter cases andexact aliases. B101-B119 thereforecontains417unreviewed editorialobjects;remainingB111-B119 has182objects. B120alreadycompleted andexcluded. All421commands inthenexttenexchanges match source/currentshape;114relative sites pass1140clean/current cases,including5third-result0400sites. No runtime/globalhelper/registry/ROM edits ornewgameplay. All235objects have nowbeenread inwholeclean exchanges withdurable contextnotes beforeeditorialcomparison ofolderEnglish. Notes preserve priestblessings/twomapkeys,Christianprayer/oldcross humor,talkingtemplevoice,Sphinx questions and4/5/6babychoice,violent cult/villagerhelp alternatives,star-adornment uncertainty,communityfaith/lamp/Ottoman request,1/30/59secondbeanbranches andLil confidence/hunch humor,andtheleft-hand jug riddle whosecorrectactionisturnright. Preserve sourceethical/religious/culturalcontext,allstylealiases,optionalCamilleclauses,explicituncertainty andunearnedconditional gifts/injuries. Initial3164contextnotes misgroupedonecrossstyle alias;3164bcorrectlykeepsstyle0separate andaliases1/7and2/3. Both arepreserved. CurrentdynamicCF/D0binding,sourceNPCidentity/role andnativevoicegroup mapping,currentmacro/consumer/FE/fonts/leadingblankline/pagination proofs,completeolderEnglishcomparison,freshglosses/prose,justifiedretentions,relocation,representative/release gates remainpending. No newsource/prose orcompletioncredit. COMMON750-752callers,everywider untouchedstoryline/sharedshop-town/random/help/playerprose,SourceItems/LocalProduct,fivenamedtargetleads,rawrejectedclassification includingB141,SC3B109,separategraphics/all18plaques andlater older-record technical re-audit remainopen. Queued0Dvalidationgap staysforlater withoutassertinganolderruntimedefect. Preserve everyROM,translation,executedproducer/proof/failure andclean/canonicalinput;allpreviouscompletedfamilies remaincompleted. V1492remainspromoted. No selectednextscene,newnameplate,earnedprogress,fullroute orhardwareclaim. Fullgoalactive;alljobsterminal.'

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
    assert docs[0].read_text(encoding='utf8').startswith('# Current editorial handoff - V3157')
    ROOT.mkdir(parents=True)
    for p in [lp, *docs]:
        copy2(p, ROOT / (p.name + '.before'))
    lead = deepcopy(ledger['lil_next_voice_scope_lead_v3157'])
    lead.update(status='clean-current4100-pointers-classified;context-prose-consumer-and-display-pending',
        alternative_proof=str(PROOF), alternative_proof_sha256=sha(PROOF.read_bytes()),
        source_4100_label_count_and_decoder_consumer_unbound=False, source_4100_not_player_choices=True,
        source_4100_style_slots=112, source_4100_unique_stored_alternatives=90, total_editorial_objects=402,
        next_source_4100_style_slots=64, next_source_4100_unique_stored_alternatives=56, next_editorial_objects=220,
        remaining_source_4100_unique_stored_alternatives=34, remaining_editorial_objects=182,
        all_current_macro_dynamic_actor_voice_native_display_reference_and_prose_gates_pending=True,
        source_alternative_references=[{k:r[k] for k in ['id','file_path','block','command_offset','style_indices','source_reference','current_reference','source_hex','current_hex','source_selector']} for r in proof['records']])
    doc,choice,context,branch = map(read,[SOURCE,CHOICE,CONTEXT,BRANCH])
    assert doc['total_editorial_objects']==235 and len(doc['typed_choice_records'])==15 and choice['original_native_count_and_pointer_calls']==40
    assert context['all164speech_56stored_actor_alternatives_and15choice_labels_read_in_complete_clean_exchanges'] and context['older_English_not_yet_editorially_compared']
    assert context['source_context_sha256']==sha(SOURCE.read_bytes()) and len(branch['cases'])==1140 and len(branch['operands_requiring_adjustment_when_resizing'])==114
    lead.update(status='235source-current-objects-mapped;whole-clean-context-read;old-English-prose-native-gates-pending',
        total_editorial_objects=417,next_editorial_objects=235,next_three_option_menu_objects=5,next_three_option_choice_labels=15,
        next_source_packet=str(SOURCE),next_source_packet_sha256=sha(SOURCE.read_bytes()),next_choice_source_proof=str(CHOICE),next_choice_source_proof_sha256=sha(CHOICE.read_bytes()),
        next_branch_proof=str(BRANCH),next_branch_proof_sha256=sha(BRANCH.read_bytes()),whole_clean_context_notes=str(CONTEXT),whole_clean_context_notes_sha256=sha(CONTEXT.read_bytes()),
        first_line_source_orientation_only=False,whole_clean_context_read_before_older_English_comparison=True,older_English_editorial_comparison_pending=True,
        earlier220_scope_nonexhaustive_without15_three_option_choice_labels=True,gloss_prose_retentions_and_all_current_native_reference_representative_release_gates_pending=True)
    inventory = deepcopy(read(ledger['unfinished_editorial_scope_v3157']['path']))
    inventory['next_source_mapped_shrines_scope_v3163'] = lead
    inventory['next_focus'] = 'Continue source-bound current CF/D0 identity/voice/dispatch/macro/FE andthree-option menu proofs forB101-B110. Wholeclean235object contextnotes3164b exist;olderEnglishcomparison,freshgloss/prose,justifiedretentions andall native/reference/representative/registeredrelease gates pending. RemainingB111-B119 has182objects;B120completed;fullwidergoalpreserved.'
    inv = ROOT / 'unfinished_editorial_scope_inventory.json'
    save(inv, inventory)
    ledger['unfinished_editorial_scope_v3165'] = dict(path=str(inv),sha256=sha(inv.read_bytes()),incomplete_COMMON=3,incomplete_route_source_prose=0,next_editorial_objects=417,next_first_ten_editorial_objects=235,full_goal_complete=False)
    ledger['lil_next_shrines_scope_lead_v3165'] = lead
    ledger['latest_checkpoint'] = SUMMARY
    restored = deepcopy(ledger)
    for key in ['unfinished_editorial_scope_v3165','lil_next_shrines_scope_lead_v3165']:
        restored.pop(key)
    restored['latest_checkpoint'] = before['latest_checkpoint']
    assert restored == before and ledger['goal_status'] == 'active' and not ledger['full_goal_complete']
    save(lp, ledger)
    section = '## V3165:complete235source objects andclean-exchange context;uncredited\n\n' + SUMMARY + '\n\nAlternative classification: ' + PROOF.as_posix() + '. Unfinished scope: ' + inv.as_posix() + '. Completed V3144release/patch/currentstartup details remain inV3148below.\n\n'
    for i,p in enumerate(docs):
        firstline,rest = p.read_text(encoding='utf8').split('\n',1)
        p.write_text(('# Current editorial handoff - V3165' if i == 0 else firstline) + '\n\n' + section + rest,encoding='utf8',newline='\n')
    evidence = {str(p):sha(p.read_bytes()) for p in [PRIOR,PROOF,SOURCE,CHOICE,CONTEXT,BRANCH,inv,Path(__file__),Path('scripts/classify_lil_4100_alternatives_v3156.py')]}
    save(ROOT/'checkpoint_receipt.json',dict(checkpoint='V3165',summary=SUMMARY,evidence=evidence,updated_files={str(p):sha(p.read_bytes()) for p in [lp,*docs]},prior_verified_handoff=str(PRIOR),new_source_prose_reviews=0,new_completed_records=0,source_prose=4193,completed=4190,fresh_reread=4190,fresh_integrated=4190,fresh_pending=0,historical_revised=2923,historical_retained=1267,next_editorial_objects=417,next_first_ten_editorial_objects=235,candidate=ledger['current_integrated_candidate'],new_emulator_runs=0,all_jobs_terminal=True,full_goal_complete=False))
    print('V3165:235source/current objects andwholecleancontext mapped;15three-choice labels included.417unreviewed nextobjects;4190completed/V3144/exactpatch/currentstartup preserved. Fullgoalactive.')
