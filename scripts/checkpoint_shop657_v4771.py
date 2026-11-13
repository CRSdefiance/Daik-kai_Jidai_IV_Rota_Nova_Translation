"""Stage a lossless editorial checkpoint; do not mutate shared metadata yet."""
from pathlib import Path
from copy import deepcopy
import json

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.duel_editorial import owned_entries
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/shop657_checkpoint_v4771')
LEDGER=Path('translations/editorial_review_current_v1.json')
FINAL=Path('translations/shop657_layout_final_review_v1.json')
RELEASE=Path('work/analysis/shop657_release_v4767/registered_release_verification.json')
ACTUAL=Path('work/analysis/shop657_actual_verification_v4770/ordinary_actual_and_startup_verification.json')
STUDY=Path('work/analysis/early_shop_breaks_v4763e/source_current_findings_and_native_proposal.json')

SUMMARY=(
    'V4771 resumes the full editorial objective with the user\'s whole-exchange American-localization '
    'and readable-wrapping clarification. Grammar, dictionary accuracy and technical passes alone '
    'do not establish editorial quality; apply this to earlier retentions as well as new work. '
    'Preserve source-supported gameplay terminology and uncertainty without invented facts. '
    'The bread example remains bread preparation, not an unrelated trading tip. '
    'COMMON657 is source-reread, wording retained with reason and formatting corrected from three '
    'short rows to two full-width rows in registered experimental V4766. The tag question stays '
    'together. A reviewed complete-word soft wrap after For preserves every word; no global '
    'weak-ending waiver, authored break, prose shortening, native geometry, metric, executable, '
    'table, macro or font change. Three generated terminal spaces preserve the exact original NUL '
    'and native selection boundaries. Comparison689 retains its working historical explanation '
    'and independently scoped native wrapping. Six complete native planes across the earlier and '
    'current fonts,7336 fresh native copies,16 atomic negatives and94 regressions pass. '
    'V4766 inherits the complete current560-entry translation/font/Square-repair stack and adds '
    'one source-locked formatting batch:561 entries/114 accepted layers,all18 release checks, '
    'whole-ROM equality to the scoped parent reconstruction and an exactly reconstructable '
    'clean-input patch. Only COMMON657 bytes change relative to the current repaired playtest '
    'parent; all four stories,every other message,file,component,font,graphic and runtime byte '
    'remain exact. Main V4701 and canonical baseline are unchanged; no promotion. '
    'A9501-frame ordinary-input town cold boot with the unchanged genuine inherited battery '
    'shows656,658,717 and657;657 is selected by the original random branch at7910 and held at8000. '
    'All four complete text/blank-paper planes match independent native oracles. Three sampled '
    'company/fleet/ship and five-field financial projections agree through the town return. '
    'The earlier6501-frame replay did not select657 and is not657 coverage. Fresh4001-frame '
    'New Game passes confirmation/opening masks. All eight review-sheet screens and the standalone '
    '657 full screen were viewed. Total20003 new emulator frames; no savestate,script or state '
    'fixture,random-value write,earned-progress,full-RAM,future-world,full-route or hardware claim. '
    'No duplicate editorial credit:5912 completed contextual rereads,5915 source/prose,3748 '
    'historical revisions/2164 retentions and4313/4313 route reviews/completions remain. '
    'The58-record exact legacy-compiler inventory is a formatting lead set,not a project '
    'denominator. Four additional prototype differences682/764/774/775 require consumer and '
    'context judgment; no blanket rewrite is approved. B180 now has22 source/current dispatch '
    'checks,100 original branch cases/ten sites,and original event180/action181 native binding '
    'without an explicit dependency prefix. This does not prove natural eligibility. Its missing '
    'historical V1909 input was recovered byte-exact from the retained clean-input patch and '
    'pinned; stopped4760/4762 producers remain beside passing successors. B180 still has11 '
    'uncredited speeches; names/controls/terms,complete predecessor comparison,localization, '
    'native layout,actual and release gates remain. Every storyline,shared town/shop exchange, '
    'random scene,Help and other player prose stays in scope. Preserve all earlier ROMs, '
    'translations,drafts,executed producers,proofs,failures and ledger history. Graphics/all18 '
    'plaques and the later older-record technical re-audit/queued0D gap stay separate and open.')

NEXT=(
    'Continue B180 from its complete clean-Japanese exchange and fresh glosses,passing22 '
    'dispatches/100 branch cases/event180-action181 binding. Bind both static Lady166/167 '
    'names,voices,all28 commands,11 complete preambles,two8000 raw500 predicates,three A000 '
    'effects,C200570/end572 and approved Lisbon/commodity terms without guessing packed '
    'semantics or earned eligibility. Apply the professional American-localization standard '
    'to the full exchange and earlier retained commodity forecasts,including the wheat '
    'Amsterdam lead. Preserve uncertainty and actual supported mechanics. Then finish native '
    'layout,relocation,representative actual and cumulative registered release gates. '
    'Review broader legacy wrapping by specific consumer and complete context; leads682/764/774/775 '
    'are unapproved comparisons,not mandatory changes. Keep every remaining storyline,shared '
    'town/shop exchange,random scene,Help and player prose in the full goal. Preserve COMMON750-752, '
    'canonical Maria32 SC3B97,SourceItems/LocalProduct,five named-target leads,exact-record Proof '
    'consistency,Samwell full-catalog middle-field lead,B157 provenance and untranslated Sao '
    'Jorge alias15E5D4/pointer122504. Keep graphics/all18 plaques and later older-record '
    'technical re-audit/queued0D gap separate. Preserve every ROM and earlier translation; '
    'do not repeat sealed checks without a concrete new risk.')


if __name__=='__main__':
    assert not ROOT.exists() and not FINAL.exists()
    release,actual,study=map(read,[RELEASE,ACTUAL,STUDY])
    assert release['exact_clean_input_reconstruction'] and actual['total_new_emulator_frames']==20003
    assert sha(Path(actual['sheet']).read_bytes())==actual['sheet_sha256']
    assert actual['all_four_holds_full_native_and_independent_ink_blank_pixels_equal']
    assert len(actual['actual_holds'])==4 and len(actual['startup_complete_masks'])==4
    ROOT.mkdir(parents=True)
    final=deepcopy(read('translations/shop657_full_width_reflow_manuscript_v1.json'))
    image=NdsImage.open(release['candidate']);conf=read('translations/shop657_full_width_reflow_release_v1.json')
    entry=owned_entries(image.read_file('/COMMON/MESFILE.DK4'),image.read_file('/__arm9__.bin'),conf['directory_sha256'])[657]
    row=final['records'][0];assert row['proposed_compiled_hex']==entry.text.hex()
    row.update(status='integrated-formatting-revisit-wording-retained-no-new-editorial-credit',
        integrated_reference=deepcopy(row['current_reference']),integrated_hex=entry.text.hex(),
        actual_evidence=next(r for r in actual['actual_holds'] if r['message_ID']==657))
    final.update(actual_new_gameplay_pending=False,candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],
        patch=release['patch'],patch_sha256=release['patch_sha256'],actual_proof=str(ACTUAL),
        native_proof=str(STUDY),release_proof=str(RELEASE),actual_review_sheet_viewed=True,
        actual_changed_fullscreen_viewed=True,all6_native_preview_tiles_viewed=True,
        source_wording_unchanged=True,added_editorial_credit=0,full_goal_complete=False)
    final_bytes=(json.dumps(final,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
    (ROOT/'final_review.staged.json').write_bytes(final_bytes)
    raw=LEDGER.read_bytes();ledger=json.loads(raw);before=json.loads(raw)
    assert [ledger[k] for k in ['records_editorially_completed','records_with_source_and_prose_pass','records_revised_and_integrated','retained_wordings_editorially_completed']]==[5912,5915,3748,2164]
    key='shop657_full_width_reflow_v4771';assert key not in ledger
    ledger[key]=dict(summary=SUMMARY,records=final['records'],comparison689=study['records'][1],
        source_study=str(STUDY),source_study_sha256=sha(STUDY.read_bytes()),
        final_review=str(FINAL),final_review_sha256=sha(final_bytes),native_cases=6,native_copies=7336,
        actual_proof=str(ACTUAL),actual_proof_sha256=sha(ACTUAL.read_bytes()),
        release_proof=str(RELEASE),release_proof_sha256=sha(RELEASE.read_bytes()),
        all8_actual_screens_and6_native_tiles_viewed=True,added_editorial_credit=0,
        remaining_unapproved_layout_leads=[682,764,774,775],prototype_unregistered=True,
        B180_passing_proofs=[
            'work/analysis/lil_B180_dispatches_v4760b/all11_source_current_dispatches_no_macros_and7_control_leaves.json',
            'work/analysis/lil_B180_branches_v4761/original_relative_branch_targets.json',
            'work/analysis/lil_B180_entry_v4762b/source_EV2_B180_action_dependency_and_native_getter_binding.json'],
        next=NEXT,full_goal_complete=False)
    # The branch proof's exact basename is discovered, never invented in a reference.
    branch_files=list(Path('work/analysis/lil_B180_branches_v4761').glob('*.json'))
    assert len(branch_files)==1
    ledger[key]['B180_passing_proofs'][1]=str(branch_files[0])
    for p in ledger[key]['B180_passing_proofs']:assert Path(p).exists()
    ledger['editorial_localization_and_layout_standard_v4771']=dict(
        path='docs/editorial_localization_and_layout_standard.md',
        sha256=sha(Path('docs/editorial_localization_and_layout_standard.md').read_bytes()),
        applies_to_new_and_previously_retained_wording=True,complete_original_goal_preserved=True)
    ledger['previous_current_integrated_candidate_before_shop657_v4771']=ledger['current_integrated_candidate']
    ledger['previous_latest_checkpoint_before_shop657_v4771']=ledger['latest_checkpoint']
    ledger['current_integrated_candidate']=dict(path=release['candidate'],sha256=release['candidate_sha256'],
        profile=release['profile'],MESFILE_sha256=sha(image.read_file('/COMMON/MESFILE.DK4')),
        ARM9_sha256=sha(image.read_file('/__arm9__.bin')),patch_sha256=release['patch_sha256'],
        manifest=release['manifest'],status='experimental-verified-editorial-checkpoint-not-promoted',
        manuscript_batches=561,accepted_layers=114,complete_current_font_and_Square_repairs_inherited=True)
    ledger['latest_checkpoint']=SUMMARY
    inverse=deepcopy(ledger)
    inverse['current_integrated_candidate']=inverse.pop('previous_current_integrated_candidate_before_shop657_v4771')
    inverse['latest_checkpoint']=inverse.pop('previous_latest_checkpoint_before_shop657_v4771')
    inverse.pop(key);inverse.pop('editorial_localization_and_layout_standard_v4771')
    assert inverse==before
    targets={LEDGER:encode_ledger(ledger)}
    assert len(targets[LEDGER])<100*1024*1024
    section='## V4771: full-width shop reply and localization clarification\n\n'+SUMMARY+'\n\nNext: '+NEXT+'\n\n'
    for name in ['editorial_review_goal.md','known_issues.md','todo.md','translation_progress.md']:
        path=Path('docs')/name;text=path.read_text(encoding='utf-8');first,rest=text.split('\n',1)
        targets[path]=(first+'\n\n'+section+rest.lstrip('\n')).replace('\n','\r\n').encode('utf-8')
    path=Path('docs/editorial_handoff_current.md');old=path.read_text(encoding='utf-8')
    targets[path]=('# Current editorial handoff - V4771\n\n'+section+old).replace('\n','\r\n').encode('utf-8')
    playtest=(f'# Current combined playtest build — V4766\n\nUse `{release["candidate"]}` '
        f'(SHA-256 `{release["candidate_sha256"]}`). It contains the complete repaired font/Square '
        'stack and latest integrated translation, plus the two-line shopkeeper correction. '
        'All561 registered entries/114 accepted layers and18 release checks pass. The clean-input '
        f'patch is `{release["patch"]}` (SHA-256 `{release["patch_sha256"]}`). '
        'Only one COMMON message changes from the previous repaired playtest build; every word '
        'is retained. The changed reply was viewed during ordinary shop gameplay; startup, '
        'town return and complete-pixel checks pass. Status remains experimental; promoted '
        'main and canonical baseline are unchanged. The earlier tutorial/crowd/Lisbon gameplay '
        'acceptance request remains open; this formatting test does not certify that sequence.\n\n'
        'Details: [V4771 checkpoint](shop657_full_width_reflow_v4771.md). '
        'The previous handoff follows as historical evidence.\n\n')
    path=Path('docs/current_playtest_build_20261027.md')
    targets[path]=(playtest+path.read_text(encoding='utf-8')).replace('\n','\r\n').encode('utf-8')
    details=('# V4771: two-line shopkeeper reply\n\n'+SUMMARY+'\n\n'
        f'Candidate: `{release["candidate"]}`\n\nROM SHA-256: `{release["candidate_sha256"]}`\n\n'
        f'Clean-input patch SHA-256: `{release["patch_sha256"]}`\n\n'
        f'Exact source/current/integrated ledger: `{FINAL}`.\n\n'
        f'Native study: `{STUDY}`. Actual proof: `{ACTUAL}`. Release proof: `{RELEASE}`.\n\n'
        'The prototype planner and earlier study producers remain research evidence; the '
        'registered fix uses the scoped657 full-width compiler. Failed study4763c showed '
        'that simply removing stored breaks would leave657 outside the native dynamic '
        'wrapper; that attempt was not registered or handed off. No executable workaround '
        'was installed. All earlier drafts/producers/failures remain preserved.\n\nNext: '+NEXT+'\n')
    targets[Path('docs/shop657_full_width_reflow_v4771.md')]=details.encode('utf-8')
    targets[FINAL]=final_bytes
    plan=[]
    for i,(path,after) in enumerate(targets.items()):
        old=path.read_bytes() if path.exists() else None
        before_path=ROOT/f'{i:02d}.before';after_path=ROOT/f'{i:02d}.after'
        if old is not None:before_path.write_bytes(old)
        after_path.write_bytes(after)
        plan.append(dict(target=str(path),existed=old is not None,before=str(before_path) if old is not None else None,
            before_sha256=sha(old) if old is not None else None,staged=str(after_path),after_sha256=sha(after)))
    save(ROOT/'metadata_plan.json',dict(files=plan,ledger_key=key,all_original_root_and_nested_history_preserved=True,
        original_coverage_counts_unchanged=True,no_registration_or_ROM_change=True,
        actual6_native_tiles_and8_full_screens_viewed=True,full_goal_complete=False))
    print(dict(staged_metadata_files=len(plan),ledger_bytes=len(targets[LEDGER]),added_editorial_credit=0,shared_metadata_changed=False),flush=True)
