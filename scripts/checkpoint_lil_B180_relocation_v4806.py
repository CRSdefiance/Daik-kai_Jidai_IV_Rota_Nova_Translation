"""Stage the lossless B180 relocation/research checkpoint, zero credit."""
from pathlib import Path
from copy import deepcopy
import gzip
import json
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/lil_B180_relocation_checkpoint_v4806')
KEY='lil_B180_contextual_relocation_v4806'
MANUSCRIPT=Path('translations/lil_B180_editorial_manuscript_v3.json')
APPROVAL=Path('work/analysis/lil_B180_native_approval_v4795/all11_source_prose_current_native_approval.json')

NEXT='B180 relocation,stored native planes,whole-block loaders,external entry census,guarded ends and relocated control checks now pass. Do not repeat them without a concrete risk. Continue with paired disclosed Japanese/English B180 content cold boots retaining all28 source commands plus original B22 initialization. There are ten relative sites,two original500 predicates,three alternative A000 leaves,one C200 and one end;do not flatten the conditional paths or require every alternative to execute in one run. Observe all11 speeches,actual selected effect,predicate order and original RNG seed transitions,C200 context and normal parent return. Never force emulator RNG or import CPU-only seeds. Native FE geometry/current-font offline evidence does not replace actual current-font FE gameplay. Research ROM4801 is not a registered release or new build parent. After necessary actual checks,register the atomic compiler following the complete V4766 stack,verify the clean-input patch and current startup,then credit the11 objects once. Five revisions/six justified retentions remain uncredited. Keep all other storylines, shared town/shop dialogue,random scenes,Help and player prose in the full objective. Revisit earlier commodity forecast wording and premature wrapping by complete context and consumer;remaining comparison leads682/764/774/775 are not automatic rewrites. Preserve COMMON750-752,canonical Maria32 SC3B97,SourceItems/LocalProduct,five named-target leads,exact-record Proof consistency,Samwell full-catalog middle-field lead,B157 provenance and untranslated Sao Jorge alias15E5D4/pointer122504. Keep graphics/all18 plaques and later older-record technical re-audit/queued0D gap separate. Preserve every ROM, translation,draft,executed producer,proof and failure;the full goal remains active.'

SUMMARY='V4806 completes the B180 offline relocation and research gates. All28 commands,11 complete preambles and ten relative span fields map reversibly from576 source bytes to548 stored/546 logical bytes;inverse restoration recovers every original logical byte and all335 other SC2 blocks remain exact. All11 final stored native text planes equal the reviewed current-font planes across44 alignment cases:20 fresh and24 exact-proof reuses. Both predicates remain four-byte aligned. No prose,manual break, font,metric,shared guard or executable change is added.\n\nA pinned one-block research ROM4801 differs from complete V4766 only in SC2 block180; every other file and component remains exact. Fresh current/research checks pass672 whole-block loads/cache hits and1344 parent modes. Three shipped entry censuses,all28 mapped commands and50 target native branch cases pass. Original tail decodes at572 and542 return type0/extent4 with poisoned unread post-payload guards. Eleven relocated dispatches,seven exact leaves,two unforced snapshot RNG predicate pairs,three opaque A000 structural pairs,the source fleet-derived C200 request and25 mapped hypothetical paths pass. Every path preserves all11 speeches,one alternative effect,C200 and the single end. These CPU checks do not execute opaque effect bodies or prove actual scene outcomes,parent return or earned eligibility. Preserve stopped4800 and corrected 4800b/4800c preparation provenance.\n\nThere is one new research ROM and zero new emulator runs or editorial credit. Completed contextual5912,source/prose5915,integrated revisions3748,retentions2164 and route4313/4313 remain unchanged. B180 retains11 approved uncredited objects,5 revisions and6 justified retentions. Registered V4766 remains561 entries/114 accepted layers with its exact clean-input patch;promoted main V4701 remains unchanged. Premature wrapping review includes earlier retained translations across every storyline,shared town/shop exchange,random scene,Help and player prose. COMMON657 is fixed;other comparison leads are pending contextual and consumer review. Preserve every ROM, translation,draft,producer,proof,failure and nested ledger history. Graphics and the later older-record technical re-audit remain separate and open. Full goal active.\n\nB180 relocation,stored native planes,whole-block loaders,external entry census,guarded ends and relocated control checks now pass. Do not repeat them without a concrete risk. Continue with paired disclosed Japanese/English B180 content cold boots retaining all28 source commands plus original B22 initialization. There are ten relative sites,two original500 predicates,three alternative A000 leaves,one C200 and one end;do not flatten the conditional paths or require every alternative to execute in one run. Observe all11 speeches,actual selected effect,predicate order and original RNG seed transitions,C200 context and normal parent return. Never force emulator RNG or import CPU-only seeds. Native FE geometry/current-font offline evidence does not replace actual current-font FE gameplay. Research ROM4801 is not a registered release or new build parent. After necessary actual checks,register the atomic compiler following the complete V4766 stack,verify the clean-input patch and current startup,then credit the11 objects once. Five revisions/six justified retentions remain uncredited. Keep all other storylines, shared town/shop dialogue,random scenes,Help and player prose in the full objective. Revisit earlier commodity forecast wording and premature wrapping by complete context and consumer;remaining comparison leads682/764/774/775 are not automatic rewrites. Preserve COMMON750-752,canonical Maria32 SC3B97,SourceItems/LocalProduct,five named-target leads,exact-record Proof consistency,Samwell full-catalog middle-field lead,B157 provenance and untranslated Sao Jorge alias15E5D4/pointer122504. Keep graphics/all18 plaques and later older-record technical re-audit/queued0D gap separate. Preserve every ROM, translation,draft,executed producer,proof and failure;the full goal remains active.'

if __name__=='__main__':
    assert not ROOT.exists()
    doc,approval=map(read,[MANUSCRIPT,APPROVAL]);assert approval['manuscript_sha256']==sha(MANUSCRIPT.read_bytes())
    assert len(doc['records'])==11 and doc['revised']==5 and doc['retained']==6
    assert doc['all11_current_native_previews_viewed_on_two_sheets'] and doc['source_prose_or_completion_credit_added']==0
    assert all(all(r['review'].values()) for r in doc['records'])
    lp=Path('translations/editorial_review_current_v1.json');before=lp.read_bytes();old=json.loads(before)
    assert KEY not in old and old['goal_status']=='active' and not old['full_goal_complete']
    assert tuple(old[k] for k in ['records_editorially_completed','records_with_source_and_prose_pass','records_revised_and_integrated','retained_wordings_editorially_completed'])==(5912,5915,3748,2164)
    candidate=old['current_integrated_candidate'];assert sha(Path(candidate['path']).read_bytes())==candidate['sha256']==doc['current_ROM_sha256']
    evidence={str(p):sha(p.read_bytes()) for p in [MANUSCRIPT,APPROVAL,Path('work/analysis/current_native_context_controls_v4787/positive_and7_meaningful_rejections.json'),Path(__file__),*map(Path,['work/analysis/lil_B180_relocation_v4798/nested_source_relocation_research.json', 'work/analysis/lil_B180_stored_v4799/all11_final_stored_targets44_macro_cases_and_complete_planes.json', 'work/analysis/lil_B180_research_tools_v4800b/exact_key_correction.json', 'work/analysis/lil_B180_research_tools_v4800/prepared_tools.json', 'work/analysis/lil_B180_research_v4801/research_image_receipt.json', 'work/analysis/lil_B180_loader_v4802/whole_SC2_and_B180_initial_entry_proof.json', 'work/analysis/lil_B180_reference_census_v4803/all28_commands_ten_relative_sites_and_shipped_entry_census.json', 'work/analysis/lil_B180_ends_v4804/two_declared_tail_end_decodes_ten_relative_sites.json', 'work/analysis/lil_B180_relocated_controls_v4805/all11_dispatches_two_RNG_predicates_three_effects_C200_and25_mapped_paths.json'])]}
    for key in ['source_context','control_contract','actor_voice_contract','branch_proof','source_entry_proof',
        'source_effect_and_predicate_contract','predicate_RNG_ownership_proof','current_C200_source_ownership_proof',
        'source_nameplate_consumer_proof','actor_terminology_reconciliation','effective_current_comparison','native_font_proof']:
        p=Path(doc[key]);assert sha(p.read_bytes())==doc[key+'_sha256'];evidence[str(p)]=sha(p.read_bytes())
    new=deepcopy(old);new[KEY]=dict(summary=SUMMARY,manuscript=str(MANUSCRIPT),manuscript_sha256=sha(MANUSCRIPT.read_bytes()),
        records=doc['records'],revised=5,retained=6,approved_uncredited_objects=11,
        source_prose_or_completion_credit_added=0,native_source_pass_complete=True,
        relocation_and_stored_offline_checks_complete=True,actual_and_registered_release_pending=True,new_emulator_runs=0,new_ROMs=1,
        evidence=evidence,next=NEXT,full_goal_complete=False)
    new['previous_latest_checkpoint_before_B180_relocation_v4806']=old['latest_checkpoint'];new['latest_checkpoint']=SUMMARY
    inverse=deepcopy(new);inverse['latest_checkpoint']=inverse.pop('previous_latest_checkpoint_before_B180_relocation_v4806');inverse.pop(KEY)
    assert inverse==old
    ROOT.mkdir(parents=True);(ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0))
    targets={lp:encode_ledger(new)};assert len(targets[lp])<100*1024*1024
    section='## V4806: B180 stored relocation and research gates\n\n'+SUMMARY+'\n\n'
    for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
        p=Path('docs')/name;text=p.read_text(encoding='utf-8')
        if name=='editorial_handoff_current.md':after='# Current editorial handoff - V4806\n\n'+section+text
        else:
            first,rest=text.split('\n',1);after=first+'\n\n'+section+rest.lstrip('\n')
        targets[p]=after.replace('\n','\r\n').encode('utf-8')
    plan=[]
    for i,(target,after) in enumerate(targets.items()):
        raw=target.read_bytes();a=ROOT/f'{i:02d}.before';b=ROOT/f'{i:02d}.after'
        if target!=lp:a.write_bytes(raw)
        b.write_bytes(after)
        plan.append(dict(target=str(target.resolve()),before=str(a.resolve()) if target!=lp else None,
            before_sha256=sha(raw),staged=str(b.resolve()),after_sha256=sha(after)))
    save(ROOT/'mutation_plan.json',dict(files=plan,ledger_key=KEY,evidence=evidence,
        all_existing_root_and_nested_history_preserved=True,all_coverage_counters_unchanged=True,
        candidate=deepcopy(candidate),no_ROM_registry_builder_or_pin_change=True,
        all11_native_previews_viewed=True,full_goal_complete=False))
    print(dict(staged_files=6,ledger_bytes=len(targets[lp]),approved_uncredited_objects=11,revised=5,retained=6,shared_files_changed=False),flush=True)
