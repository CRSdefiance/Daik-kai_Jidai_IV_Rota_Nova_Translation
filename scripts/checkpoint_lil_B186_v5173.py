"""Stage a compact lossless source/native/actual checkpoint with zero premature credit."""
from copy import deepcopy
from pathlib import Path
import gzip,json
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B186_checkpoint_v5173')
KEY='lil_B186_contextual_reference_v5173'
PREVIOUS='previous_latest_checkpoint_before_B186_v5173'
DOC=Path('translations/lil_B186_editorial_manuscript_v6.json')
APPROVAL=Path('work/analysis/lil_B186_reference_approval_v5172/approval_receipt.json')
VISUAL=Path('work/analysis/lil_B186_actual_review_v5170/all12_panels_20_fullscreens_conditional_return_and_measured_differences.json')
PRIOR=Path('work/analysis/editorial_handoff_verification_v5128/verified_handoff.json')
WIDER=(
    'Continue the full clean-Japanese whole-exchange editorial goal across all four storylines,earlier translations,shared town/shop exchanges,random scenes,Help and all other player prose. '
    'Revisit premature wrapping retrospectively,using each consumer’s validated space and complete exchanges;preserve meaningful pacing and justified good wording. No blanket reflow,maximum-fill rule,frozen compiler edit or duplicate review credit. '
    'COMMON657 and682/764/774/775 are already resolved;do not repeat or recount. Keep COMMON750-752 callers,SourceItems/LocalProduct,five named-target leads,exact-record Proof terminology consistency,Samwell full-catalog middle field,B157 provenance,untranslated Sao Jorge alias15E5D4/pointer122504 and new untranslated Alexandria alias15E4D0/pointer1223E4 caller/display lead open. '
    'The incidental COMMON405 rats scene remains a practical capture lead with no live global-ID/caller binding or editorial credit. '
    'Keep graphics/all18 plaques and the later older-record technical re-audit/queued0D separate and open. Preserve every ROM,translation,draft,executed producer,proof,failure and all historical ledger values. Full goal active.')
NEXT=(
    'Integrate the12 approved uncredited Lil SC2B186 objects after the complete registered V5122 stack. Start from manuscriptv6 and sealed relocation map/approval5172. '
    'Source/whole-exchange prose,current-native formatting,relocation,stored padding,loaders,censuses,guarded ends,conditional controls and representative actual review are sealed;do not repeat without a concrete risk. '
    'Create a source-locked atomic conditional compiler using actual dk4tool/patch/lil_B182_editorial_v1.py (there is no B182_editorial_v4),while carrying forward B185 complete source/current reference,length,record identity and both-command-map guards. '
    'Use B186 layoutv4;require exact R13 source/prose and both reviewed ordinary-boundary reasons after be and this. Preserve all12 words/controls,seven revisions/five justified retentions,Owner174/Cook175 voice0 and one null-actor FE. '
    'Preserve all24 commands,one raw700 predicate540,six relative operands548/552/556/568/580/592,three alternative opaque A000s560/572/584,C200644 and four-byte end646. '
    'Source652 stored/650 logical becomes584 stored/582 logical,with2 trailing zeros on both sides;predicate540 maps478,effects560/572/584 map498/510/522,C200644 maps576,end646 maps578. Inverse plus original tailzeros recovers the entire predecessor. '
    'Target predicate478 is halfword aligned:ownership5159 proves12 clean/current/relocated cases,three result classes around699/700/701,original optional scratch02279600=700 at0202A5D8 and RNG02168EB8 at020D984C,with all other4MiB exact. Do not inherit two500 predicates or strictly-one-write assumptions. '
    'Bind96 initial native alignments,48 stored cases (36 fresh/12 exact-byte reuse),18 consumer/28 formatter negatives,336 fresh target loads/672 modes and exact whole-ROM parent reuse,three entry censuses,30 skip cases and5 mapped structural paths. '
    'Paired9001-frame B22 content cold boots retain all24 source+9 original initializer commands;each actual path executes27 commands,all12 speeches,one selected source effect560,C200,end and normal return. '
    'All47 complete holds and115 nontext pairs pass;both actual sheets and20 full screens were viewed after image return. Rolls297/592 both return0/select560;returns5735/5737. '
    'Retain10 timing differences (4 speech/6 control/end),4 later original A-indicator differences6490/6670 lower shadow and7450/7630 full indicator,and unequal final PRNG1803218166/2467799992. FinalRGB,five native state groups and whole1A04 actor/captain2 agree within measured scope;no causal RNG,future-world or full-RAM equality claim. '
    'No further focus run is required by current display findings. No natural event186 eligibility,earned fashion,earlier Alexandria location,full route or hardware claim. '
    'After compiler rejection controls,register cumulatively,build only through build_integrated_release.py,verify the exact clean-input patch and fresh current cumulative startup,then credit12 once. '
    'Main V4701 remains promoted;V5122 remains current registered candidate. No promotion or pruning. '+WIDER)
SUMMARY=(
    'V5173 seals the complete B186 source/prose,current-native,reference and targeted actual review as12 uncredited objects:7 revisions/5 individually justified retentions. '
    'The Owner’s missing-sweetness realization and emphatic stretched sweet,the Cook’s doubt,the Owner’s circular self-authority,the practical question/job retort,two perfunctory yeah-yeah responses,confident fashion prediction and stylized laugh form one comic exchange. '
    'Retain the natural realization,Sweetness?,practical sweeter question,confident sweet-things prediction and tentative Sweets/Alexandria notice with individual reasons. '
    'No dish,recipe,ingredient,amount,kinship,rank,nobility,price,profit,completed boom or prior scene location is invented. Clean Owner/Cook fields and four current native name consumers support customers. '
    'Both Alexandria identities bind,but field1223E4/storage15E4D0 remains Japanese in current RAM;the separate1230B4 alias is complete English. Record the untranslated alias as an unresolved caller/display lead. '
    'Sweets is source sweet things,not a single commodity or all goods in UI Treats4. Twelve clean/current category calls distinguish them. All12 clean glosses preceded predecessor exposure;an incidental terminology search exposed the old closing FE before formal comparison,and that narrow caveat is recorded honestly.\n\n'
    'Visual review found premature four-row R13 wrapping. Exact source/prose-bound layoutv4 permits two ordinary complete-word soft wraps after be and this,producing three flowing rows without changing a word,font,width,guard,phase or pagination. '
    'Both exact warning reasons are recorded on R13;six mutation controls prevent transfer. All11 other compiled targets/native planes remain exact. Initial one-boundary attempt left all targets unchanged because a proposed35-character interior row exceeded the unchanged guard/phase reserve;retain its corrected diagnosis and all producers. '
    'All12 final native panels on2 sheets were viewed;96 initial alignments,18 consumer/28 formatter negatives and complete leading/internal/trailing glyph,bounds and single-page checks pass. Seven narrow Japanese/English row-count notes are accepted;no global weak-word waiver or manual break.\n\n'
    'All24 commands,six relative operands,one700 predicate,three alternative opaque effects,C200 and end map reversibly from652/650 stored/logical to584/582,with2 exact alignment zeros on each side. '
    'Thirty native skip cases and5 source/target structural paths agree;335 other SC2 blocks and every other file/component remain exact. Forty-eight stored alignments pass:36 fresh parity cases/12 exact-byte reuses. '
    'The target predicate is halfword aligned. Twelve ownership cases bind original scratch02279600 and RNG02168EB8 writers;all unowned4MiB and ABI remain exact,no emulator seed/outcome is forced. '
    'Fresh336 target loads/672 parent modes,exact whole-ROM V5122 parent reuse,three entry censuses,guarded ends and12 relocated dispatches pass. The frozen census console retained10/50;separate5163b receipt verifies actual asserted data6/30 without rerunning or altering the proof.\n\n'
    'Two disclosed Japanese/English B22 content cold boots9001 frames each execute27 conditional commands from33 stored commands,all12 speeches,selected effect560,C200,end and normal return. '
    'All47 complete native holds and115 paired upper/portrait/name samples match. Both actual sheets and20 full screens were viewed after image return;Owner/Cook portraits,the three-row R13 and null-actor FE remain intact. '
    'Unforced rolls297/592 both select560;returns5735/5737. Ten timings differ (4 speech/6 control/end). Four later original A-indicator differences remain unmasked:6490/6670 lower shadow,7450/7630 full indicator. '
    'Final9001 RGB,five native state groups and whole1A04 actor/captain2 agree;PRNG1803218166/2467799992 differs. No causal PRNG,future-world/full-RAM equivalence,natural event186 eligibility,earned state,earlier scene location,full-route or hardware claim. Following dialogue adds no credit. Both sessions17715/18367 are terminal/reaped.\n\n'
    'Atomic compiler/rejection controls,registered cumulative integration,clean-input patch and fresh current startup remain pending. Coverage stays6015 completed contextual rereads,6018 source/prose,3811 integrated revisions/2204 retentions,SC24130/SC396 and routes4416/4416,zero pending credited route drafts. '
    'These12 are approved uncredited objects. Current registered V5122 remains569 manifest batches/114 accepted layers/18 passing checks with exact patch;promoted main V4701 and every earlier ROM,translation and historical ledger value remain preserved. Three new research ROMs are pinned. Full goal active.\n\n'+NEXT)

if __name__=='__main__':
    assert not ROOT.exists();doc,approval,visual,prior=map(read,[DOC,APPROVAL,VISUAL,PRIOR])
    assert approval['manuscripts'][str(DOC)]==sha(DOC.read_bytes())
    assert len(doc['records'])==12 and (doc['revised'],doc['retained'])==(7,5)
    assert doc['source_prose_or_completion_credit_added']==0
    assert all(all(r['review'].values()) and r['actual_B22_display_fixture_observed'] for r in doc['records'])
    assert visual['representative_actual_coverage_sufficient_for_this_distinct_display_scope'] and not visual['visual_review_pending']
    paths=[DOC,APPROVAL,VISUAL,PRIOR,Path(__file__),
        Path('work/analysis/lil_B186_predicate700_v5159/all12_aligned_and_unaligned_original700_ownership_cases.json'),
        Path('work/analysis/lil_B186_reference_count_clarification_v5163b/exact_data_counters_not_inherited_console_literals.json'),
        Path('work/analysis/lil_B186_terms_v5139b/untranslated_Alexandria_alias_unreviewed_caller_lead.json')]
    evidence={str(p):sha(p.read_bytes()) for p in paths}
    for obj in [doc,approval,read(doc['reference_map'])]:
        for key,value in obj.items():
            if key.endswith('_sha256') and key[:-7] in obj and isinstance(obj[key[:-7]],str):
                path=Path(obj[key[:-7]])
                if path.is_file():assert sha(path.read_bytes())==value;evidence[str(path)]=value
        for path,digest in obj.get('evidence',{}).items():assert sha(Path(path).read_bytes())==digest;evidence[path]=digest
    lp=Path('translations/editorial_review_current_v1.json');before=lp.read_bytes();old=json.loads(before)
    assert sha(before)==prior['ledger_sha256'] and KEY not in old and PREVIOUS not in old
    assert tuple(old[k] for k in ['records_editorially_completed','records_with_source_and_prose_pass','records_revised_and_integrated','retained_wordings_editorially_completed'])==(6015,6018,3811,2204)
    assert old['goal_status']=='active' and not old['full_goal_complete']
    current=old['current_integrated_candidate'];assert sha(Path(current['path']).read_bytes())==current['sha256']==doc['current_ROM_sha256']==prior['candidate_sha256']
    mapping=read(doc['reference_map']);refs={r['id']:r for r in mapping['blocks'][0]['text_records']}
    compact=[]
    for row in doc['records']:
        selected={key:deepcopy(row[key]) for key in ['id','file_path','block','source_reference','current_reference','source_hex','current_hex','source_Japanese','english','source_selector','source_complete_preamble_hex','speaker','source_meaning','localization_note','editorial_decision','review']}
        if row['editorial_decision']=='retain-wording':selected['fresh_retained_wording_justification']=row['fresh_retained_wording_justification']
        if row.get('reviewed_ordinary_boundaries'):selected['reviewed_ordinary_boundaries']=row['reviewed_ordinary_boundaries']
        ref=refs[row['id']];selected['planned_stored_reference']=dict(offset=ref['new_offset'],record_index=ref['new_record_index'],bytes=ref['new_length'],target_hex=ref['target_hex'])
        selected.update(full_review=str(DOC),full_review_sha256=sha(DOC.read_bytes()),completion_credit_added=0)
        compact.append(selected)
    new=deepcopy(old);new[KEY]=dict(summary=SUMMARY,next=NEXT,manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),records=compact,
        revised=7,retained=5,approved_uncredited_objects=12,source_prose_or_completion_credit_added=0,
        source_native_references_and_representative_actual_complete=True,atomic_compiler_registered_patch_and_current_startup_pending=True,
        new_emulator_runs=2,total_frames=18002,new_research_ROMs=3,all_generated_ROMs_preserved=True,
        compact_records_reference_complete_immutable_reviews_without_dropping_historical_values=True,evidence=evidence,full_goal_complete=False)
    new[PREVIOUS]=old['latest_checkpoint'];new['latest_checkpoint']=SUMMARY
    inverse=deepcopy(new);inverse['latest_checkpoint']=inverse.pop(PREVIOUS);inverse.pop(KEY);assert inverse==old
    ROOT.mkdir(parents=True);(ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0))
    targets={lp:encode_ledger(new)};assert len(targets[lp])<100*1024*1024
    section='## V5173: B186 complete exchange, early-wrap correction and targeted actual review; integration pending\n\n'+SUMMARY+'\n\n'
    for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
        path=Path('docs')/name;text=path.read_text(encoding='utf-8')
        if name=='editorial_handoff_current.md':after='# Current editorial handoff - V5173\n\n'+section+text
        else:
            first,rest=text.split('\n',1);after=first+'\n\n'+section+rest.lstrip('\n')
        targets[path]=after.replace('\n','\r\n').encode('utf-8')
    files=[]
    for i,(target,after) in enumerate(targets.items()):
        raw=target.read_bytes();staged=ROOT/f'{i:02d}.after';staged.write_bytes(after)
        if target!=lp:(ROOT/f'{i:02d}.before').write_bytes(raw)
        files.append(dict(target=str(target.resolve()),before_sha256=sha(raw),staged=str(staged.resolve()),after_sha256=sha(after)))
    save(ROOT/'mutation_plan.json',dict(files=files,ledger_key=KEY,previous_key=PREVIOUS,evidence=evidence,candidate=current,
        all_original_root_and_nested_history_preserved=True,all_coverage_counters_unchanged=True,full_goal_complete=False))
    print(dict(staged_files=6,ledger_bytes=len(targets[lp]),approved_uncredited_B186=12,revised=7,retained=5,shared_files_changed=False))
