"""Derive the next reversible completion transaction without changing native guards."""
import ast,re
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

SOURCE=Path('scripts/complete_Maria_story_v7784b.py')
TARGET=Path('scripts/complete_Maria_B36_v7826.py')
ROOT=Path('work/analysis/maria_B36_completion_tools_v7826')
INTRO="""Maria's confrontation with Lil, SC3 B36, is integrated in registered cumulative V7821. The complete clean Japanese exchange was reviewed before current English: 16 disjoint records receive credit once, with nine revisions and seven individually justified retentions. Exact clean, previous effective English, compiled, stored, actual and integrated references are in translations/maria_B36_contextual_final_review_v1.json.

The ledger now has 6,938 completed records, 6,941 source/prose records and drafts, 4,347 integrated revisions and 2,591 retentions. Completed file counts are SC0 135, SC1 91, SC2 4,915, SC3 197 and COMMON 1,600; COMMON retains three source/prose drafts. Route 5,338/5,338 is a subset, not the whole-goal denominator. V7821 preserves 631 batches and 114 accepted layers, passes 18 registered release checks and 110 regressions, equals the approved reference ROM and reconstructs byte for byte from its clean-input patch. Main V4701 remains unchanged."""
DETAILS="""All 16 English speeches fit complete original 216px/four-row single pages. Complete first, internal and final characters, independent font planes, bounds, canaries, guards, consumption and pagination pass. Final logical, compiled and stored checks each cover 64 alignments; 11 storage parity spaces add zero ink. Nine row-count infos have individual reasons, with no warnings or waivers. A scoped automatic soft-wrap preference keeps He's a great merchant! together without authored line breaks, prose changes or wider geometry.

All 16 six-byte preambles, original selectors, FI2/FO1 substitution order, 22 native commands, six numeric leaves and complete ends remain. There are no relative or in-block predicate commands. Resource and structural boundary tests are scoped evidence, not complete mechanics. Clean and previous B36 blocks and the entire previous archive invert exactly. Only B36 changes; all 302 other SC3 blocks and all other files/components remain exact to V7779. The original native loaders pass 303 full loads/cache hits and 606 parent modes. Policy passes 16 positives and 81 actual-changing rejections. Production passes one complete positive and 120 actual-changing corruptions, all rejected before any files-list commit with dependency checks bypassed.

Two initialized source/English gameplay fixtures each play all 16 speeches and 29 original fixture commands. Together they provide 32 complete pages and 132 complete body/nameplate holds, with no partial sampled holds, unidentified traces or unplayed lines. All 32 exact panes and nine sheets were viewed. All 16 paired upper scenes, portraits and nameplates agree, as do command results and UI requests. These are targeted headless emulator tests using ordinary inputs and the existing exact system-only unlock, earned=false; natural optional activation, original location, complete mechanics, full routes and hardware coverage remain unproved.

Preserve exits 8213/8216, 18 command-comparison rows, six duration differences and 108/131 later RGB differences. State/tasks/calendar agree; models/persistent objects and whole actors differ. Final seeds are 164302531/4157282706. All raw timing, RNG, component, actor, calendar, following-command and RGB evidence remains, without broad simulation or causal-equivalence claims. Initialized Hangzhou return8300 and incidental later navigation/level-up text earn no source-prose credit.

The fresh own-V7821 Maria startup runs 4001 frames and matches all seven prior whole-frame pairs plus captain3 and whole-actor controls. Its strict own-ROM input is work/analysis/current_V7821_native_v7824/route3/current_native_input.json. Unaffected route startup evidence is retained without replay. All three selected B36 progressive nameplates were observed: Lil Argot, Maria Li and Xien Yan. Actor0A is Xien, not Camille09. No global name asset changes; full catalogue UI and the complete 207-name/role/alias review remain open.

All earlier drafts, translations, failed and corrected producers, ROMs and proofs remain. Preserve the source normal-end value-carry finding and B35 R65 source-only nineteenth-cell glyph for the later older-record technical re-audit. All four storylines, earlier dialogue, broad practical town/shop/random capture, Help, remaining prose and retrospective premature wrapping remain active. Graphics and all 18 plaques remain separate. The separate unified test package stays canceled; no promotion, pruning, commit or push occurs."""
NEXT="""Continue the full editorial objective from verified V7827 and current registered V7821. B36 is complete; retain its source/native/actual/policy/production/inverse/patch/startup proofs without unnecessary replay. Use the new own-V7821 captain3 context for further Maria native work; obtain another route's own current context when needed.

Continue all four storylines and earlier translated exchanges, broad practical shared shop/town/random captures, Help and remaining player prose. Continue all 207 names/roles/aliases, including actor151-159 Sailor/Retainer and the remaining indirect, typed, COMMON and UI consumers. The 147-block/484-use/3150-context-speech census and nine-exchange/129-speech sample are evidence, not full approval. Check the original Japanese progressive-name consumer before inferring a global label from internal fields.

Retain the retrospective contracted-predicate early-wrap lead and every earlier unfinished inventory, counterpart conversation, role/item/display lead and family. Compare exact current consumers and complete clean exchanges before revisions; heuristic candidates add no credit. Integrate reviewed batches once their necessary checks pass. Preserve all generated ROMs and earlier translations. Graphics/all18 plaques and the later older-record technical re-audit remain separate. Main V4701 remains unchanged; do not create the canceled separate unified test package, promote, prune, commit or push."""

if __name__=='__main__':
    assert not TARGET.exists() and not ROOT.exists()
    original=SOURCE.read_text(encoding='utf-8');text=original
    tree=ast.parse(original)
    changes={}
    for node in tree.body:
        if isinstance(node,ast.Assign) and len(node.targets)==1 and isinstance(node.targets[0],ast.Name) and node.targets[0].id in ['INTRO','DETAILS','NEXT']:
            changes[ast.get_source_segment(original,node.value)]=repr(globals()[node.targets[0].id])
    # Keep explanatory prose outside the count substitutions below.
    for literal in changes:text=text.replace(literal,"'__"+next(k for k in ['INTRO','DETAILS','NEXT'] if repr(globals()[k])==changes[literal])+"__'")
    replacements={
        'scripts.Maria_story_final_paths_v7771':'scripts.Maria_B36_final_paths_v7816b',
        'maria_story_completion_v7784b':'maria_B36_completion_v7826',
        'editorial_handoff_verification_v7785b':'editorial_handoff_verification_v7827',
        'editorial_handoff_verification_v7774':'editorial_handoff_verification_v7817d',
        'maria_story_release_v7780':'maria_B36_release_v7822',
        'maria_story_startup_verification_v7782':'maria_B36_startup_verification_v7824',
        'own_Maria_startup_exact_V7717_andstrict_current_input':'own_Maria_startup_exact_V7779_andstrict_current_input',
        'maria_story_startup_view_v7783':'maria_B36_startup_view_v7825',
        'maria_story_atomic_challenges_v7776':'maria_B36_atomic_challenges_v7819',
        'maria_B34_B108_B35_contextual_final_review_v1':'maria_B36_contextual_final_review_v1',
        'Maria_SC3B34_B108_B35_completion_v7784b':'Maria_SC3B36_completion_v7826',
        'Maria_SC3B34_B108_B35_contextual_linked_arc_v7784b':'Maria_SC3B36_contextual_confrontation_v7826',
        'unfinished_editorial_scope_v7784b':'unfinished_editorial_scope_v7826',
        "['Maria_SC3B34_B108_B35_contextual_pending_v7736b','Maria_SC3B34_B108_B35_sealed_pending_v7773']":"['Maria_SC3B36_sealed_pending_v7817c']",
        'unfinished_editorial_scope_v7773':'unfinished_editorial_scope_v7817c',
        'all-routes-unified-v7779':'all-routes-unified-v7821',
        'all_current_requested_andfinal_frames_equal_V7717':'all_current_requested_andfinal_frames_equal_V7779',
        'maria_story_atomic_v7775c':'maria_B36_atomic_v7818b',
        'maria_story_registration_v7778':'maria_B36_registration_v7820',
        'maria_story_production_tools_v7775c':'maria_B36_production_tools_v7818b',
        "offline_only_object_IDs=['DK4_MES_B108_R0020','DK4_MES_B108_R0125']":"offline_only_object_IDs=[]",
        'all116_commands20_relative_sites67_preambles12_substitutions_andcomplete_ends_preserved':'all22_commands_no_relative_sites16_preambles3_substitutions_andcomplete_ends_preserved',
        'all_three_clean_predecessor_blocks_andwhole_archive_inverse_exact':'clean_predecessor_block_andwhole_archive_inverse_exact',
        '[34,108,35]':'[36]',
        "new[key][file]==114":"new[key][file]==181",
        "],181)": "],197)",
        'offline_only_objects=2':'offline_only_objects=0',
        'Maria_SC3B34_B108_B35_v7784b':'Maria_SC3B36_v7826',
        'row_infos22_no_waivers':'row_infos9_no_waivers',
        'all_measured_limits_andold_two_page_proofs_preserved':'all_measured_limits_andearlier_proofs_preserved',
        'Maria_story67_uncredited=False,Maria_story67_completed_once=True':'Maria_B36_sealed_uncredited=False,Maria_B36_completed_once=True',
        '## V7784b: Maria linked arc integrated in cumulative V7779':'## V7826: Maria confrontation integrated in cumulative V7821',
        '# Current editorial handoff - V7784b; V7779 current':'# Current editorial handoff - V7826; V7821 current',
        'currentV7779':'currentV7821',
        'VerifiedV7784b/V7779':'VerifiedV7826/V7821',
        'SC3_completed=181':'SC3_completed=197',
    }
    for key in replacements:assert key in text,key
    text=re.sub('|'.join(map(re.escape,sorted(replacements,key=len,reverse=True))),lambda m:replacements[m[0]],text)
    counts={6855:6922,6858:6925,4290:4338,2565:2584,6922:6938,6925:6941,4338:4347,2584:2591,5255:5322,5322:5338,67:16,48:9,19:7,65:16,130:32,528:132,256:120,200:81,630:631}
    text=re.sub(r'\d+',lambda m:str(counts.get(int(m[0]),int(m[0]))),text)
    for name in ['INTRO','DETAILS','NEXT']:text=text.replace("'__"+name+"__'",repr(globals()[name]))
    # These are current-state aliases, not historical proof keys.
    key='Maria_B36_sealed_uncredited=False,Maria_B36_completed_once=True,'
    assert key in text
    text=text.replace(key,key+"\n                completed=6938,source_prose=6941,revised=4347,retained=2591,SC3=197,reviewed_routes=5338,completed_routes=5338,\n                Maria_B36_actual_pages=32,Maria_B36_complete_body_andheader_holds=132,")
    compile(text,str(TARGET),'exec')
    result=derive(str(SOURCE),str(TARGET),{original:text})
    ROOT.mkdir(parents=True)
    save(ROOT/'provenance.json',dict(derivation=result,exact_original_source_bound=True,
        all_original_native_high_constants_andtransaction_inverse_hash_guards_preserved=True,
        before=[6922,6925,6925,4338,2584],after=[6938,6941,6941,4347,2591],
        only16_disjoint_records_newcredit=True,full_goal_complete=False))
    print('B36 completion transaction prepared; stage, audit, apply and verify remain.')
