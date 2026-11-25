"""Stage a lossless current-font B180 source/prose/native checkpoint, zero credit."""
from pathlib import Path
from copy import deepcopy
import gzip
import json
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/lil_B180_native_checkpoint_v4796')
KEY='lil_B180_contextual_native_v4796'
MANUSCRIPT=Path('translations/lil_B180_editorial_manuscript_v3.json')
APPROVAL=Path('work/analysis/lil_B180_native_approval_v4795/all11_source_prose_current_native_approval.json')

NEXT=(
    'Continue B180 from approved manuscriptv3 and all11 viewed current-font native planes. '
    'Build a complete independently reversible relocation map for576-byte source/current B180, '
    'all28 commands/11 preambles,ten relative span fields,two original500/RNG predicates, '
    'three alternative A000 leaves472/504/516,C200570 and single end572. Preserve the original '
    'three-way threshold results and every packed effect byte;do not inherit B179 linear/no-C200 '
    'assumptions. Current source snapshot is exact V4766 Lil opening,not historical London or '
    'natural B180 eligibility. Source/current controls and native planes are now current-input '
    'bound;do not repeat them without a concrete risk. Complete stored native tests,loaders and '
    'mapped ends;then paired disclosed content cold boots or a practical ordinary activation '
    'for all11 speeches,the selected effect,predicate evaluation order/seed transitions,C200 '
    'and parent return. Do not force RNG in actual gameplay or import isolated CPU boundary '
    'fixture seeds. C200 descriptor field2 is current native fleet-derived value2,not old '
    'London value0;bind its actual context rather than assume either constant. Current FE '
    'painter uses source-calibrated typed geometry and current-font independent pixels; '
    'actual current B180 FE display remains to capture. Preserve the five revisions and '
    'six individually justified retentions unless a concrete new finding requires change. '
    'Register after the entire V4766 stack,verify clean-input patch and current startup,then '
    'credit these11 exactly once. They remain uncredited now. Keep all other storylines, '
    'shared town/shop dialogue,random scenes,Help and player prose in the full objective. '
    'Revisit earlier commodity forecast wording and premature wrapping by complete context '
    'and consumer;remaining comparison leads682/764/774/775 are not automatic rewrites. '
    'Preserve COMMON750-752,canonical Maria32 SC3B97,SourceItems/LocalProduct,five named-target '
    'leads,exact-record Proof consistency,Samwell full-catalog middle-field lead,B157 provenance '
    'and untranslated Sao Jorge alias15E5D4/pointer122504. Keep graphics/all18 plaques and '
    'later older-record technical re-audit/queued0D gap separate. Preserve every ROM, '
    'translation,draft,executed producer,proof and failure;the full goal remains active.')

SUMMARY=(
    'V4796 completes the uncredited B180 whole-exchange source/prose/current-native pass: '
    '11 speeches,5 revisions/6 individually justified retentions. The complete clean Japanese '
    'and fresh glosses preceded all predecessor English. Remove unsupported third-person '
    'she/her,restore the shared-impression question,the explicit knowledge limit and confident '
    'fashion prediction,the surprised first-to-acquire urgency and future proposal to work '
    'up the nerve to ask. Correct the closing source category香料 from Spices to registered '
    'Scents in Lisbon. Preserve six working replies/questions/farewells with individual reasons. '
    'No brand,ingredient,supplier,rank,marriage,relationship,earlier scene location,completed '
    'purchase,shortage,price increase,earned boom or unsupported demand mechanic is invented. '
    'The two source roles remain generic Lady166/Lady167;the third person remains unspecified. '
    'Two exact Lisbon aliases,12 clean/current native category lookups and Musk/Frankincense/'
    'Ambergris membership bind the terminology;the old Incense label is superseded by the '
    'registered Frankincense fidelity decision. No new commodity-widget or broad item '
    'fidelity completion is claimed.\n\n'
    'All four story files and EV2 are byte-identical between V4749 and current V4766. Fresh '
    '207-name/eight-voice checks,22 dispatches,100 branch cases/ten sites,event180/action181 '
    'binding and four read-only Lady name consumers use the actual V4766 opening snapshot '
    'at4000. The exact123040-byte deployed pool and every executed instruction match current '
    'source;no historical initialized-RAM overlay is used. Seven stale/foreign-code,actor-write, '
    'alternate-RAM and wrong-hash controls reject. This reuses existing capture evidence and '
    'does not constitute a new B180 activation or earned event eligibility.\n\n'
    'A rejected read-only predicate assumption led to a strict original-RNG contract:raw500 '
    'uses an original bounded1000 draw,returning0 below500,1 at500 and2 above500. Each evaluation '
    'writes exactly the owned PRNG word02168EB8 via original020D984C;the LCG transition and all '
    'other4MiB are verified. Sixteen source/current cases include four unforced current-snapshot '
    'cases and12 explicitly disclosed CPU-only499/500/501 boundary fixtures. No emulator '
    'seed/outcome was forced. Cleanup restores only the owned field after validating its '
    'genuine transition. Current C200 field2 comes from the original fleet getter and constructor '
    '(value2 here);the older London value0 is not assumed. Both source/current C200 contracts '
    'preserve exact owned request writes and all other4MiB. All25 structural predicate-result '
    'paths preserve all11 speeches,one of the three original opaque A000 effects,C200570 and '
    'single end572. Effect bodies and actual outcomes remain unexecuted. Preserve stopped '
    '4780/4780b,diagnostics4781/4783 and passing4780c/4782/4784.\n\n'
    'All11 logical paragraphs pass QA with four narrow source/English row-count notes only. '
    'All11 complete current-font native planes and88 logical/compiled alignment cases pass: '
    'ten progressive216x64 and one FE228x48logical/228x64physical. Both sheets were viewed '
    'separately;all leading/internal/final glyphs,punctuation,bounds and one-page consumption '
    'are complete. Source-consumer18 and formatter28 negative cases reject. The current '
    'one-pixel font offset is modeled explicitly;historical FE evidence supplies unchanged '
    'typed geometry,not a claim of new current-font FE gameplay. No new phrase exception, '
    'prose shortening,authored break,shared metric or guard change. Manuscriptv3 has all five '
    'individual review gates approved offline;relocation,stored checks,actual scene and '
    'registered cumulative integration remain.\n\n'
    'No new ROM,emulator run,source/prose tally or completion credit is added. Coverage stays '
    '5912 completed contextual rereads,5915 source/prose,3748 historical revisions/2164 '
    'retentions,route4313/4313 and zero pending credited route drafts;B180 has11 explicitly '
    'uncredited approved draft objects. Current integrated V4766 remains561 entries/114 '
    'accepted layers with its exact clean-input patch and verified two-line COMMON657 fix. '
    'Main V4701/pushed4d63fd3/tag promoted-v4701,immutable baseline,registry,builder,pins, '
    'all earlier ROMs/translations/drafts/executed producers/proofs/failures and full nested '
    'ledger history remain preserved. Whole-exchange American-localization and readable '
    'wrapping standards apply to new and earlier retained work. Every storyline,shared '
    'town/shop exchange,random scene,Help and player prose stays in scope. Graphics/all18 '
    'plaques and later older-record technical re-audit/queued0D gap remain separate and open. '
    'Full goal active.\n\n'+NEXT)

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
    evidence={str(p):sha(p.read_bytes()) for p in [MANUSCRIPT,APPROVAL,Path('work/analysis/current_native_context_controls_v4787/positive_and7_meaningful_rejections.json'),Path(__file__)]}
    for key in ['source_context','control_contract','actor_voice_contract','branch_proof','source_entry_proof',
        'source_effect_and_predicate_contract','predicate_RNG_ownership_proof','current_C200_source_ownership_proof',
        'source_nameplate_consumer_proof','actor_terminology_reconciliation','effective_current_comparison','native_font_proof']:
        p=Path(doc[key]);assert sha(p.read_bytes())==doc[key+'_sha256'];evidence[str(p)]=sha(p.read_bytes())
    new=deepcopy(old);new[KEY]=dict(summary=SUMMARY,manuscript=str(MANUSCRIPT),manuscript_sha256=sha(MANUSCRIPT.read_bytes()),
        records=doc['records'],revised=5,retained=6,approved_uncredited_objects=11,
        source_prose_or_completion_credit_added=0,native_source_pass_complete=True,
        relocation_actual_and_registered_release_pending=True,new_emulator_runs=0,new_ROMs=0,
        evidence=evidence,next=NEXT,full_goal_complete=False)
    new['previous_latest_checkpoint_before_B180_native_v4796']=old['latest_checkpoint'];new['latest_checkpoint']=SUMMARY
    inverse=deepcopy(new);inverse['latest_checkpoint']=inverse.pop('previous_latest_checkpoint_before_B180_native_v4796');inverse.pop(KEY)
    assert inverse==old
    ROOT.mkdir(parents=True);(ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0))
    targets={lp:encode_ledger(new)};assert len(targets[lp])<100*1024*1024
    section='## V4796: B180 contextual and current-font native pass\n\n'+SUMMARY+'\n\n'
    for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
        p=Path('docs')/name;text=p.read_text(encoding='utf-8')
        if name=='editorial_handoff_current.md':after='# Current editorial handoff - V4796\n\n'+section+text
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
