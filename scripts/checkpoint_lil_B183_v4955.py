"""Preserve B183 whole-exchange/native/reference progress without premature credit."""
from pathlib import Path
from copy import deepcopy
import gzip,json
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.verify_village_wrap_v608 import read,save
from scripts.checkpoint_lil_B182_references_v4910 import WIDER

ROOT=Path('work/analysis/lil_B183_checkpoint_v4955')
KEY='lil_B183_contextual_native_reference_v4955'
PREVIOUS='previous_latest_checkpoint_before_B183_v4955'
DOC=Path('translations/lil_B183_editorial_manuscript_v7.json')
NATIVE=Path('work/analysis/lil_B183_native_approval_v4946/all25_source_prose_current_native_approval.json')
RELOCATION=Path('work/analysis/lil_B183_relocation_v4947/nested_source_relocation_research.json')
STORED=Path('work/analysis/lil_B183_stored_v4948/all25_final_stored_targets100_macro_cases_and_complete_planes.json')
WRAP=Path('work/analysis/lil_B183_locative_wrap_v4939/before_after_all25_semantic_and_layout_comparison.json')
NEXT=(
    'Continue B183 from approved manuscriptv7,formatterv3,native proof4945/approval4946,wrap comparison4939,relocation4947,stored4948 and reference4950 gates4951-4954. '
    'Do not repeat completed source/native/reference gates without a concrete risk. All25 words/paragraphs remain reviewed as one exchange:16 revisions/9 individual retentions. '
    'Preserve five progressive roles:Square Shopkeeper85,Shipwright110,Priest132,Guildmaster148,Sailor153;the separate full-catalogue Retainer153 and native voice4 remain distinct. '
    'Observe both impersonal FE objects:sourceR53 Slam! between service thanks and private complaint,andR95 prospective Artwork/Basra notice. '
    'Retain all28 linear commands plus9 original B22 initialization commands in paired Japanese/English content fixtures:37 stored commands,25 speeches,23 progressive/2 FE,five total A000s,C200 and one four-byte end. '
    'A0008 raw00a0ffff013926a1 remains8;C200950 maps1048,end952 maps1050,source956 maps1056 stored/1054 logical with two trailing alignment zeros. '
    'No predicates,relative operands,typed objects,resources,presentations,pauses or substitutions exist;do not inherit B182 RNG/branch assumptions. '
    'Use original inputs and read-only observation. Extend the A-button schedule far enough to advance all25 panels:the old range ending8501 actually stops at8360,so include the later8600/8840 presses and confirm normal return. '
    'Measure actual timing,RGB,RNG and state without forcing equality;observe the five portraits/nameplates,Sailor voice4,the midscene FE-to-shopkeeper restoration,closing FE,C200,end and parent return. '
    'Confirm R35 displays its fitting question intact,then That one over there / is obviously better!,with all leading/final glyphs and guards preserved. '
    'The new source-bound planner recognizes complete over there and prioritizes an intact fitting first sentence before slack;no global helper or word list is changed. '
    'Keep v1/v2 planners,all drafts,initial native proofs and the partial-question finding4943. Review analogous earlier premature wrapping contextually without changing frozen compilers or adding duplicate credit. '
    'After representative checks,seal references,build a source-locked atomic compiler and rejection controls,register after the complete V4914 stack,build only through the registered builder,verify the exact clean-input patch and current startup,then credit25 once. '
    'They remain uncredited now. '+WIDER)
SUMMARY=(
    'V4955 completes B183 clean-first whole-exchange prose,current-native display,reversible relocation and offline reference review as25 uncredited objects:16 revisions/9 individually justified retentions. '
    'Keep the collectors\' competing tastes,lasting-fame prediction,recommendation to acquire work,purchase intentions,polite service,midscene Slam!,private shopkeeper complaint,rich-person pastime echo,art-judgment qualification,hearty response to candor and secrecy request as one exchange. '
    'Correct lost posterity,scarcity implication,ownership assertions,unsupported everyone/know nothing claims,missed candor response and untranslated-sounding lofty hobby. '
    'Retain praise,skeptical Really?/Oh.,blunt preference,service thanks,Slam!,commotion question,Rich folks at play and Of course with individual reasons. The approved Artwork/Basra forecast stays prospective. '
    'No artist name,title,unshown pointing direction,price,currency,profit,guaranteed fame,objective art verdict,player identity,kinship or earlier shop location is invented.\n\n'
    'Exact V4914 opening RAM binds207 names/eight voices,five source selectors,50 clean/current dispatches,ten read-only name paths and event183/action184. '
    'The progressive roles are Square Shopkeeper85,Shipwright110,Priest132,Guildmaster148,Sailor153;the separate catalogue name Retainer153 remains preserved. Source voice153 is4;the other four are0. '
    'Two live Basra aliases and Artwork57 bind through actual current pointers and unchanged commodity metadata. All28 commands,25 complete preambles,leading A0008 raw00a0ffff013926a1,C200950 and end952 are exact. '
    'No predicates,relative sites,typed objects,pauses,resources,presentations or FI/FA/FO exist. Offline A000 bodies and actual C200 resource bodies remain unexecuted.\n\n'
    'Visual review caught premature wrapping in R35:the fitting question What are you two talking about? had been split. Broad weak-there classification and then slack priority were responsible. '
    'The frozen v3 source-bound successor recognizes the complete locative over there and prioritizes an intact fitting first sentence after weak-boundary,orphan and row-count rules. '
    'It produces What are you two talking about? / That one over there / is obviously better! without changing any word,width,font,metric,guard or authored break. '
    'All24 other compiled targets and native planes remain exact. Shared helpers,original STRONG_ENDINGS/PROTECTED_BOUNDARIES lists and historical compilers stay unchanged;v1/v2 and the partial-question finding are retained. '
    'All25 final native panels on4 sheets were viewed:23 progressive216x64 and2 FE228x48 logical/228x64 physical. All200 initial alignments,24 source-consumer/28 formatter negatives and complete first/internal/final glyph,bounds and one-page checks pass. '
    'Only2 narrow Japanese/English row-count notes are accepted;no other safety waiver.\n\n'
    'All28 commands map reversibly from956 to1056 stored/1054 logical bytes,C200950 to1048,end952 to1050,two trailing alignment zeros. '
    'Inverse reconstruction restores every predecessor logical byte and335 other SC2 blocks stay exact. All100 stored alignments pass:64 fresh parity cases/36 exact-byte reuses. '
    'A pinned one-block research reference preserves every other file,font,graphic,story and executable component from V4914. Fresh336 target loads/672 modes,exact whole-ROM parent reuse,three entry censuses,poisoned post-logical-end guards,25 relocated dispatches and paired A000/C200 structural contracts pass. '
    'No new emulator run,natural event183 eligibility,earned state,full route or hardware claim. Actual content capture,reference sealing,atomic compiler,registered integration,clean-input patch and current startup remain pending.\n\n'
    'Coverage remains5941 completed contextual rereads,5944 source/prose,3764 integrated revisions/2177 retentions,SC24088 and route4342/4342,zero pending credited route drafts. '
    'These25 B183 objects have zero credit until the remaining checks pass. Registered V4914 remains564 manifest batches/114 accepted layers with its exact patch;promoted main V4701 and all earlier ROMs,translations and complete history are preserved. Full goal active.\n\n'+NEXT)

if __name__=='__main__':
    assert not ROOT.exists();doc=read(DOC);native=read(NATIVE);assert native['manuscript_sha256']==sha(DOC.read_bytes())
    assert len(doc['records'])==25 and (doc['revised'],doc['retained'])==(16,9) and doc['source_prose_or_completion_credit_added']==0
    assert all(all(r['review'].values()) for r in doc['records'])
    paths=[DOC,NATIVE,RELOCATION,STORED,WRAP,Path(__file__),
        Path('work/analysis/lil_B183_research_v4950/research_image_receipt.json'),
        Path('work/analysis/lil_B183_loader_v4951/whole_SC2_and_B183_initial_entry_proof.json'),
        Path('work/analysis/lil_B183_reference_census_v4952/all28_commands_no_relative_sites_and_shipped_entry_census.json'),
        Path('work/analysis/lil_B183_ends_v4953/two_declared_tail_end_decodes_no_relative_sites.json'),
        Path('work/analysis/lil_B183_relocated_controls_v4954/all25_progressive_FE_dispatches_A000_C200_pairs_and3_leaves.json')]
    evidence={str(p):sha(p.read_bytes()) for p in paths}
    for k,v in doc.items():
        if k.endswith('_sha256') and k[:-7] in doc and isinstance(doc[k[:-7]],str):
            p=Path(doc[k[:-7]])
            if p.is_file():assert sha(p.read_bytes())==v;evidence[str(p)]=v
    lp=Path('translations/editorial_review_current_v1.json');before=lp.read_bytes();old=json.loads(before)
    assert sha(before)==read('work/analysis/editorial_handoff_verification_v4921/verified_handoff.json')['ledger_sha256']
    assert KEY not in old and PREVIOUS not in old and old['goal_status']=='active' and not old['full_goal_complete']
    assert tuple(old[k] for k in ['records_editorially_completed','records_with_source_and_prose_pass','records_revised_and_integrated','retained_wordings_editorially_completed'])==(5941,5944,3764,2177)
    current=old['current_integrated_candidate'];assert sha(Path(current['path']).read_bytes())==current['sha256']==doc['current_ROM_sha256']
    new=deepcopy(old);new[KEY]=dict(summary=SUMMARY,next=NEXT,manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),records=doc['records'],
        revised=16,retained=9,approved_uncredited_objects=25,source_prose_or_completion_credit_added=0,
        source_native_relocation_and_offline_references_complete=True,actual_sealing_compiler_registered_patch_and_startup_pending=True,
        new_emulator_runs=0,new_research_ROMs=1,research_ROM_pinned=True,
        wrap_finding=dict(id='DK4_MES_B183_R0035',proof=str(WRAP),proof_sha256=sha(WRAP.read_bytes()),
            fitting_question_and_complete_locative_preserved=True,all_words_and_other24_planes_unchanged=True,
            analogous_earlier_wraps_remain_contextual_revisit_leads=True,no_duplicate_review_credit=True),
        evidence=evidence,full_goal_complete=False)
    new[PREVIOUS]=old['latest_checkpoint'];new['latest_checkpoint']=SUMMARY
    inverse=deepcopy(new);inverse['latest_checkpoint']=inverse.pop(PREVIOUS);inverse.pop(KEY);assert inverse==old
    ROOT.mkdir(parents=True);(ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0))
    targets={lp:encode_ledger(new)};assert len(targets[lp])<100*1024*1024
    section='## V4955: B183 whole-exchange/native/reference review and early-wrap correction; actual integration pending\n\n'+SUMMARY+'\n\n'
    for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
        p=Path('docs')/name;text=p.read_text(encoding='utf-8')
        if name=='editorial_handoff_current.md':after='# Current editorial handoff - V4955\n\n'+section+text
        else:
            first,rest=text.split('\n',1);after=first+'\n\n'+section+rest.lstrip('\n')
        targets[p]=after.replace('\n','\r\n').encode('utf-8')
    files=[]
    for i,(target,after) in enumerate(targets.items()):
        raw=target.read_bytes();staged=ROOT/f'{i:02d}.after';staged.write_bytes(after)
        if target!=lp:(ROOT/f'{i:02d}.before').write_bytes(raw)
        files.append(dict(target=str(target.resolve()),before_sha256=sha(raw),staged=str(staged.resolve()),after_sha256=sha(after)))
    save(ROOT/'mutation_plan.json',dict(files=files,ledger_key=KEY,previous_key=PREVIOUS,evidence=evidence,
        all_original_root_and_nested_history_preserved=True,all_coverage_counters_unchanged=True,candidate=current,full_goal_complete=False))
    print(dict(staged_files=6,ledger_bytes=len(targets[lp]),approved_uncredited_B183=25,revised=16,retained=9,shared_files_changed=False))
