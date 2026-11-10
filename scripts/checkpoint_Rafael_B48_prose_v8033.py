"""Checkpoint91 contextual B48 decisions and364 logical native cases; no release/completion credit."""
import argparse,gzip,json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.complete_B210_Ferid_v6547 import parent_at
from scripts.complete_Rafael_B47_v8018 import COUNTERS,AFTER
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B48_prose_checkpoint_v8033')
VERIFY=Path('work/analysis/editorial_handoff_verification_v8034')
PRIOR=Path('work/analysis/editorial_handoff_verification_v8019/verified_handoff.json')
LEDGER=Path('translations/editorial_review_current_v1.json')
DOC=Path('translations/rafael_B48_editorial_manuscript_v2.json')
NAMES=Path('translations/rafael_B48_speaker_name_review_v1.json')
KEY='Rafael_SC0B48_source_context_prose_logical_pending_layout_release_v8033'
SCOPE='unfinished_editorial_scope_v8033'
PROOFS={
    'source':'work/analysis/Rafael_next_clean_v8020/complete_clean_SC0_B48_EV0_andcoverage_before_current_English.json',
    'clean_names':'work/analysis/Rafael_B48_clean_names_v8021/nine_clean_static_identity_fields_before_current_English.json',
    'first_gloss':'work/analysis/Rafael_B48_clean_gloss_v8022/91_fresh_clean_glosses_nine_source_identities_before_current_English.json',
    'native_names':'work/analysis/Rafael_B48_names_v8023/nine_static_speakers18_getters_clean_fields36_synthetic_macro_alignments.json',
    'source_controls':'work/analysis/Rafael_B48_source_controls_v8024/source_EV0_28_relative_sites140_cases5_raw_predicates2_queries25_seeded_ends.json',
    'source_paths':'work/analysis/Rafael_B48_source_paths_v8025/500_source_result_compositions32_text_paths_two_exclusive_pairs.json',
    'B128_context':'work/analysis/Rafael_B48_clean_context_v8026/complete_clean_SC0_B128_EV0_andcoverage_before_current_English.json',
    'branch_gloss':'work/analysis/Rafael_B48_branch_gloss_v8027/91_fresh_glosses32_paths_B128_B37_context_before_current_English.json',
    'current':'work/analysis/Rafael_B48_current_v8028/all91_complete_source_current_refs_before_new_English_manuscript.json',
    'effective':'work/analysis/Rafael_B48_effective_v8029/all91_effective_English_templates182_original_dispatches4_FE.json',
    'prose':'work/analysis/Rafael_B48_prose_v8030/91_contextual_decisions32_path_reviews42_revisions49_retentions.json',
    'readback':'work/analysis/Rafael_B48_prose_refinement_v8031/R331_source_question_tone_refined_no_count_orcontrol_change.json',
    'logical':'work/analysis/Rafael_B48_logical_v8032/91_logical_paragraphs364_original_native_alignments4_FE.json',
}
SUMMARY="""Current registered cumulative ROM remains V8013;mainV4701 is unchanged. B47 is complete andcredited once. Counts remain6,991completed/6,994source-prose records anddrafts/4,369integrated revisions/2,622retentions;SC0 188 androute subset5,391. All636manifest batches/114accepted layers/18release checks/110regressions,whole-reference equality,exact clean-input patch andown-current Rafael startup remain verified. No B48 completion orsource/prose credit is added.

B48 now has translations/rafael_B48_editorial_manuscript_v2.json:91 complete contextual speech decisions,42 revisions and49 individually justified retentions across32 complete source text paths. All source/context/localization/naturalness gates pass;all91formatting gates remain false. Complete clean Japanese andnine clean identities were read/glossed before current English. Original source is5252stored/logical/tail0,163commands/91speeches. The clean optional B128sailing lesson/45speeches was read forcontext only;prior clean B37/72speeches is reused byexact clean ROM/archive identity. Neither context earns new dialogue credit.

Original event48/category5/action49 hasno explicit dependency list;outer scheduler/city conditions andnatural activation are not established. Native source entry,28relative sites/140structural cases,five8000raw predicates,two8100completion queries and25seeded normal-end value-carry cases pass. Original event128completion selects R71/R75 spontaneous research versusR81/R86 callback toJulio's earlier Athens errand;event37selects R379simple determination versusR385/R389/R393/R396Hayreddin ambition andresponses. Janus hasfive conditional speeches,Cesareone,Cristinaone. Three independent raw operand domains0/1/2/3/FFFFFFFF plus twoBoolean query domains produce500compositions/32distinct paths of78-88speeches;all163commands/91speeches areinthe structural union. The unforced opening composition has78speeches;this is not actual B48gameplay. No condition,party,role,roster,funds,RNG orresult is forced.

Nine original identities/getters are bound in own-current captain0 context:18progressive/full name getters,voices and36synthetic default macro alignments. Current names are Rafael Castor,Janus Pasar,Claudio Manaus,Julio Erneco,Cristina Erneco,Arcadius Eudoxios,Cesare Tony,Hans Letzel andPort Worker. Arcadius's full getter is Arcadius Eirene Eudoxios,matching the source middle field;do not insert Eirene into the spoken introduction or explain concealed characterization. Presented young-man wording andhesitant delivery remain;no extra biological reveal,romance orhealth diagnosis is authored. Shared Erneco surnames do not alone establish kinship. Port Worker naturally localizes 出港所の兄貴 inthis departure-office exchange;no brotherhood,rank ormanagement is inferred. Other seven counterpart consumers remain wider leads.

Hans's current native getters bothsayHans Letzel,while the stored introduction saysRetzel andthe joining panel saysLetze. This scoped review retains source-compatible Letzel andnormalizes these two literal batch references toits complete identity,without a name-asset change or a claim oforiginal Latin authority. Historical workflowRetzel remains preserved as a consistency lead. CesareTony andCristinaErneco retentions preserve source sound/current identity without invented national biographies;wider Cristina/Christina consumers andfull207review remain open. Allnine name formatting gates arefalse pendingcomplete nameplanes/bounds/actual headers/relevant catalogue UI.

First current exposure atv8028 preserves all163command words andcomplete six-byte preambles. All182source/current original dispatches pass:87progressive speeches/fourFEpanels. R370 alone selects a registered catalogue English template differing fromraw storage. Its English words work incontext andremain;the stray full-widthI is normalized andthe exact FI substitution is kept. Do not compare R370only against rawstorage. All91draft paragraphs pass364fresh original native logical alignments:348progressive and16null-actorFE. This proves complete literal/macro bytes andownership guards,not wrapping,fontpages,bounds,pagination,stored padding oractual gameplay. DefaultFI6/FA6/FO10 lengths aremeasured;onlyFIoccurs onceinsource. No custom player-name coverage isclaimed.

Whole-exchange revisions restore Julio's optional callback,consistent Proof ofConquest terminology,a puzzled question rather than disinterest,seven regional treasures andthe ancient SevenSages/maps withreported-legend attribution,conditional future ambition,uncertain recent African rumor andpossible information rather than guaranteed discovery. Hans's role remains naturalist/non-navigator;the Deck assignment restriction andX-at-item-information instruction arepreserved. Working banter,warm welcomes,polite assistant speech,Claudio's sincere reversal,Julio/Hans acquaintance andother lines remain with49specific retention reasons. SourceR38's provisional Cesare addressee was corrected:the complaint iscommon whileCesare's preceding remark isoptional;retain unnamedsecond person rather than invent a fixed addressee orchange branches. Readbackv8031refinesR331into a puzzled direct question andupdatesall32path reviews;v1andall earlier evidence remain.

No B48 ROM,layout plan,native font page,stored reconstruction,actual scene,frozen policy,atomic stage orregistered release existsyet. No new emulator run occurs thisturn;all offline native jobs areterminal. CurrentV8013,ledger completion counts,registry,pins andmain remain unchanged. Preserve every ROM,draft,translation,executed/failing producer andproof."""
NEXT="""Continue from verifiedV8034/current registeredV8013. B48source/context/identity/branch/current/effective/prose/logical checks arecomplete;reuse them without needless repetition. Current English isnowread forall91records,not an unread source batch. Use translations/rafael_B48_editorial_manuscript_v2.json,translations/rafael_B48_speaker_name_review_v1.json andthe exact proof paths inthis checkpoint. The v8030prose packet binds v1;the v8031readback binds v2andchanges onlyR331wording/path reviews. Counts stay6991/6994/4369/2622until finalintegration.

Next plan ordinary full-width wrapping from logical paragraphs without shortening meaning orcopying legacybreaks. Private source-bound selectors include00/04/05/06/07/08/0D/4B/71/FE;4Band71are native speaker state incomplete six-byte preambles,not literal leadingLatin. Preserve the unchanged bodyNULguard andoneFIwithmeasureddefault lengths. KeepfourFEconsumers distinct:validated216pxusable text inside228pxFEbitmap/logical-vsphysical geometry isnot the progressive216x64view. Bind actual current font metrics,complete leading/trailing/internal glyphs,bounds,pagination andconsumption. Long explanatory paragraphs such asR347 andcatalogue-selectedR370 mayneedoriginal pagination;justify specific per-record capacities andpage boundaries after native proof. Avoid artificially short rows merely toescape soft word-boundary warnings;any exception must stay exact-source/text/compiled/line bound withthe original diagnostic retained. Checkallnine full nameplanes/consumer distinctions.

Then complete source-bound relocation/all28spans/all163commands,source/current/archive inverses,finalstored native alignments,fullreference/loaders/callers andrepresentative actual scene tests. B48hasmore scene/effect transitions andjoining/UI behavior thanB47;keep all original setups,predicates,queries,effects,FEpanels andends inanydisclosed fixture. Use representative paths/focused distinct behavior risks,not an exhaustive natural playthrough orforced party/results. Measure normal carry,timing,RNG,components/calendar/laterRGB withhonest limits. Integrate once necessarychecks pass throughtheregistered cumulative/clean-input patch/startup workflow;credit91objects/42revisions/49retentions once only after finalvalidated integration. Expectedthen7082completed/7085source-prose anddrafts/4411revisions/2671retentions,SC0 279,route subset5482;these arenot current totals.

Keep the full objective across allfourstorylines,earlier dialogue,sharedshop/town/random/Help/remaining prose,all207names/roles/aliases andretrospective prematurewrapping. Preserve allprior unfinished inventories,twelvecontraction/question-tag leads,unscannedrecords beyond558plans,inherited weak-before-row lead andeveryolder item/counterpart/display lead. JanusPasar isdistinct fromPasha;no global replacement. Retain Sailor151-159 versusRetainer consumers,COMMON750-752,preLF6435,ArmadilloHide/SteelHide,HerophilusMedicine,AksumGoldSeal,AlShin/AlFeridShin,イギリス,Trader/PortWorker/Guildmaster,Cristina/Christina,HansRetzel/Letzel historicalconsistency andother recorded leads. Graphics/all18plaques andthelater older-record technical re-audit remainseparate,including normal-endvaluecarry,B35R65'ssource-only nineteenthcell andallmeasured timing/highlight/RNG/component/calendar/RGB limits. Preserve everyROM,translation,draft,failure,executedproducer andproof. MainV4701 unchanged;fullgoalactive,no separate unifiedpackage,promotion,pruning,commit orpush."""

def restore(value):
    result=deepcopy(value);entry=result.pop(KEY)
    for op in reversed(entry['inverse_operations']):
        parent,key=parent_at(result,op['path'])
        if op['existed']:parent[key]=deepcopy(op['before'])
        else:parent.pop(key)
    return result
def gates():
    prior,doc,names=map(read,[PRIOR,DOC,NAMES]);data={k:read(p) for k,p in PROOFS.items()}
    assert prior['completed']==6991 and prior['manifest_batches']==636 and prior['Rafael_B47_completed_once']
    assert sha(Path(prior['candidate']).read_bytes())==prior['candidate_sha256']==doc['current_ROM_sha256']
    assert sha(Path(prior['patch']).read_bytes())==prior['patch_sha256']
    assert len(doc['records'])==91 and doc['revisions']==42 and doc['retentions']==49
    assert all(all(r['review'][g] for g in ['source','context','localization','naturalness']) and not r['review']['formatting'] for r in doc['records'])
    assert len(names['records'])==9 and all(not r['review']['formatting'] for r in names['records'])
    assert data['readback']['manuscript_sha256']==data['logical']['manuscript_sha256']==sha(DOC.read_bytes())
    assert data['logical']['total_bound_alignment_cases']==364 and data['logical']['FE_null_actor_alignment_cases']==16
    assert len(data['source']['groups'][0]['records'])==91 and data['source']['groups'][0]['completed_coverage_overlap']==0
    assert len(data['source_controls']['source_relative_cases'])==28 and len(data['source_controls']['normal_seeded_ends'])==25
    assert len(data['source_paths']['source_result_compositions'])==500 and len(data['source_paths']['representative_text_paths'])==32
    assert len(data['effective']['source_current_dispatches'])==182
    return prior,data
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('phase',choices=['stage','audit','apply','verify']);mode=ap.parse_args().phase
    prior,data=gates()
    if mode=='stage':
        assert not ROOT.exists();before=LEDGER.read_bytes();old=json.loads(before)
        assert sha(before)==prior['ledger_sha256'] and tuple(old[k] for k in COUNTERS)==AFTER
        assert old['goal_status']=='active' and not old['full_goal_complete'] and KEY not in old and SCOPE not in old
        new=deepcopy(old);ops=[]
        def put(path,value):
            parent,key=parent_at(new,path);exists=key in parent
            ops.append(dict(path=path,existed=exists,before=deepcopy(parent[key]) if exists else None));parent[key]=deepcopy(value)
        previous_scope=old[prior['unfinished_scope']]
        assert sha(Path(previous_scope['path']).read_bytes())==previous_scope['sha256']
        inventory=deepcopy(read(previous_scope['path']));inventory['next_focus']=NEXT
        evidence={str(p):sha(Path(p).read_bytes()) for p in [PRIOR,DOC,NAMES,Path(__file__),*map(Path,PROOFS.values())]}
        pending=dict(status='91-source-context-prose-logical-approved-pending-layout-native-stored-actual-policy-release',
            manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),names=str(NAMES),names_sha256=sha(NAMES.read_bytes()),
            file_path='/data/SC0.DK4',block=48,objects=91,revisions=42,retentions=49,current_English_unread=False,
            all91_first_four_gates_true_formatting_false=True,source_commands=163,source_relative_sites=28,source_relative_cases=140,
            raw8000_sites=5,completion8100_queries=2,native_source_compositions=500,distinct_source_text_paths=32,
            current_dispatches=182,logical_native_alignments=364,progressive_alignments=348,FE_alignments=16,
            current_ROM=prior['candidate'],current_ROM_sha256=prior['candidate_sha256'],all_proofs=PROOFS,
            native_font_layout_stored_actual_policy_atomic_registered_release_andstartup_pending=True,
            new_credit=0,new_emulator_runs=0,full_goal_complete=False)
        inventory[KEY]=deepcopy(pending)
        ROOT.mkdir(parents=True);scope=ROOT/'unfinished_editorial_scope_inventory.json';save(scope,inventory)
        put([SCOPE],dict(path=str(scope),sha256=sha(scope.read_bytes()),all_prior_leads_families_history_andfull_four_storyline_objective_preserved=True,
            incomplete_COMMON=3,incomplete_credited_route_drafts=0,graphics_andlater_older_record_technical_reaudit_separate=True,full_goal_complete=False))
        put(['latest_checkpoint'],SUMMARY+'\n\n'+NEXT)
        new[KEY]=dict(**pending,summary=SUMMARY,next=NEXT,evidence=evidence,inverse_operations=ops,goal_turn_classification='progress',all_sessions_terminal_andreaped=True)
        assert restore(new)==old and tuple(new[k] for k in COUNTERS)==AFTER and new['current_integrated_candidate']==old['current_integrated_candidate']
        (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0));targets={LEDGER:encode_ledger(new)}
        section='## V8033: B48 full contextual draft and logical-native checks; layout and integration pending\n\n'+SUMMARY+'\n\n'+NEXT+'\n\n'
        for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
            path=Path('docs')/name
            prefix=('# Current editorial handoff - V8033; V8013 current\n\n' if name=='editorial_handoff_current.md' else '')+section
            targets[path]=prefix.replace('\n','\r\n').encode()+path.read_bytes()
        files=[]
        for i,(path,value) in enumerate(targets.items()):
            planned=ROOT/f'{i:02d}.after';planned.write_bytes(value)
            if path!=LEDGER:(ROOT/f'{i:02d}.before.gz').write_bytes(gzip.compress(path.read_bytes(),mtime=0))
            files.append(dict(target=str(path.resolve()),before_sha256=sha(path.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(value)))
        save(ROOT/'staged_checkpoint.json',dict(files=files,evidence=evidence,unchanged_counters=list(AFTER),new_credit=0,full_goal_complete=False))
        print('B48 source/prose/logical checkpoint staged;six targets,zero credit.Deep inverse audit next.')
    else:
        plan=read(ROOT/'staged_checkpoint.json');old=json.loads(gzip.decompress((ROOT/'ledger.before.json.gz').read_bytes()));new=read(plan['files'][0]['planned'])
        assert restore(new)==old and tuple(new[k] for k in COUNTERS)==AFTER and new['goal_status']=='active' and not new['full_goal_complete']
        for entry in plan['files']:
            assert sha(Path(entry['planned']).read_bytes())==entry['planned_sha256']
            assert sha(Path(entry['target']).read_bytes())==entry['planned_sha256' if mode=='verify' else 'before_sha256']
        for path,digest in plan['evidence'].items():assert sha(Path(path).read_bytes())==digest
        if mode=='audit':
            assert not (ROOT/'preapplication_audit.json').exists()
            save(ROOT/'preapplication_audit.json',dict(staged_plan_sha256=sha((ROOT/'staged_checkpoint.json').read_bytes()),
                deep_inverse_recovers_every_prior_root_family_record_counter_andcandidate=True,
                full_goal_all_prior_leads_andB48_contextual_andnative_limits_preserved=True,new_credit=0,full_goal_complete=False))
            print('Deep inverse passes;every prior ledger value,candidate,count andunfinished lead recovers exactly.')
        elif mode=='apply':
            assert not (ROOT/'application_receipt.json').exists() and read(ROOT/'preapplication_audit.json')['staged_plan_sha256']==sha((ROOT/'staged_checkpoint.json').read_bytes())
            for entry in plan['files']:
                assert Path(entry['target']).is_relative_to(Path.cwd().resolve()) and Path(entry['planned']).is_relative_to(ROOT.resolve())
                with Path(entry['target']).open('r+b') as stream:stream.write(Path(entry['planned']).read_bytes());stream.truncate();stream.flush();os.fsync(stream.fileno())
                assert sha(Path(entry['target']).read_bytes())==entry['planned_sha256']
            save(ROOT/'application_receipt.json',dict(all_six_targets_hash_exact=True,all_prior_values_reversible=True,new_credit=0,full_goal_complete=False))
            print('B48 prose/logical checkpoint applied;currentV8013 andallcompletion counts unchanged.Full goal active.')
        else:
            assert read(ROOT/'application_receipt.json')['all_six_targets_hash_exact'] and not VERIFY.exists()
            verified=deepcopy(prior);verified.update(ledger_sha256=sha(LEDGER.read_bytes()),previous_verified_handoff=str(PRIOR),
                previous_verified_handoff_sha256=sha(PRIOR.read_bytes()),next_required=NEXT,unfinished_scope=SCOPE,pending_source_batch=KEY,
                B48_current_English_unread=False,B48_prose_records=91,B48_prose_revisions=42,B48_prose_retentions=49,
                B48_source_relative_cases=140,B48_source_text_paths=32,B48_current_dispatches=182,B48_logical_native_alignments=364,
                B48_native_font_layout_stored_actual_policy_atomic_registered_integration_pending=True,
                new_credit=0,new_emulator_runs=0,new_actual_frames=0,all_sessions_terminal_andreaped=True,
                all_prior_roots_families_records_andcounts_recover_exactly=True,full_goal_active=True,full_goal_complete=False,
                producer_sha256=sha(Path(__file__).read_bytes()))
            VERIFY.mkdir(parents=True);save(VERIFY/'verified_handoff.json',verified)
            print('VerifiedV8034/currentV8013:6991completed;B48 91decisions/42revisions49retentions/364logicalalignments pending layout/native/stored/actual/release.Full goal active.')
