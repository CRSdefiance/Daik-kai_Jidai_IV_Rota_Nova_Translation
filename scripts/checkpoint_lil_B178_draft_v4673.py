"""Checkpoint the uncredited B178 contextual draft after verified B177 integration."""
from collections import Counter
from copy import deepcopy
import gzip
import os
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B178_draft_checkpoint_v4673')
DOC=Path('translations/lil_B178_editorial_manuscript_v1.json')
PRIOR=Path('work/analysis/editorial_handoff_verification_v4660/verified_handoff.json')
NEXT=(
    'Continue B178 from thirteen complete clean-first glosses,source/current binding,three '
    'native Lady labels,26 dispatches,event178/action179,six read-only names,three control '
    'leaves,Amsterdam/Wheat reconciliation and manuscript v1 (two proposed revisions/eleven '
    'justified retentions). Formatting is pending;no B178 review credit or integration yet. '
    'Prepare the exact frozen B178 scoped profile and natural-dialogue-v2 layout,then audit '
    'all twelve progressive/one impersonal FE native planes,all alignments,leading/internal/ '
    'trailing characters,bounds and pagination. Preserve16 commands,opaque A0008 '
    'raw00a0ffff010002a1,C200488,single end490,logical494/stored496,zero FI/FA/FO. Then '
    'source/native approval,additive ledger credit,reversible relocation/stored proofs, '
    'representative actual coverage and registered cumulative integration. Do not repeat '
    'sealed B177 checks without a concrete new risk. Continue B178-B180 (38 physical speeches, '
    'not a project denominator),every storyline,shared shop/town dialogue,random scene,Help '
    'and other player-facing prose. Preserve COMMON750-752,canonical Maria32 SC3B97, '
    'SourceItems/LocalProduct,five named-target leads,exact-record Proof consistency,Samwell '
    'full-catalogue middle-field lead and B157 provenance amendment. Graphics/all18 plaques '
    'stay separate;retain the later older-record technical re-audit/queued0D gap. Preserve '
    'every ROM,translation,draft,executed producer,proof and failure. Full goal active.')
SUMMARY=(
    'V4673 preserves B178 manuscript v1 after a clean-first whole-exchange contextual pass: '
    'two proposed revisions/eleven individually justified retentions,without new review '
    'credit. All thirteen clean speeches were individually glossed before predecessor '
    'English. Preserve home-baking enthusiasm,the second Lady\'s explicit husband,curiosity, '
    'the corner-bakery boast,encouragement,offered help,pleased surprise,the immediate shopping '
    'proposal,ingredient question,first wheat suggestion and prospective impersonal Amsterdam '
    'notice. Retain eleven working lines. Replace clipped collective We\'ll teach with I\'ll '
    'show you how;restore first in Wheat first,of course. Preserve the original second '
    'speaker\'s teaching offer followed by her ingredient question;do not reassign speakers '
    'or invent an explanation. Native labels are Lady for166/167/168;they imply no noble '
    'rank,kinship or new names. Husband is explicit only for167. Add no recipe,flour,quantity, '
    'price,completed purchase/lesson,earned boom or earlier scene location.\n\n'
    'All16 source/current commands and thirteen complete preambles bind. Twenty-six native '
    'source/current speech dispatches preserve twelve progressive/one null-actor FE notice '
    'and zero FI/FA/FO. Six read-only native name consumers have zero scratch/getter writes '
    'and preserve all4MiB. All207 catalogue/eight voice groups remain exact. Event178/action179 '
    'has no explicit dependency prefix;one getter does not prove natural eligibility. Three '
    'nontext leaves preserve A0008 raw00a0ffff010002a1,C200488 and end490,logical494/stored496. '
    'C200 ownership matches;the isolated A000 structural walk bridges a nondecode callee and '
    'does not execute its effect body. No relative site,predicate,2000 pause,resource, '
    'presentation word or typed object. Amsterdam binds through two complete16-byte inline '
    'spans and unchanged source pointers. Wheat binds through original pointer-field15EF18 '
    'to clean15B938/current repacked15BC56,with exact terminators/eight metadata bytes. Do not '
    'read the obsolete current source allocation as the active Wheat label. This adds no '
    'commodity-widget test or broad commodity/SourceItems/LocalProduct completion.\n\n'
    'B177 remains fully integrated and independently audited in experimental V4655:five '
    'revisions/five retentions,95 atomic negatives,78 regressions,553 batches/114 accepted '
    'layers,byte-exact clean-input patch and whole-ROM equality to reviewed V4630. Fresh '
    'New Game/town startup passes31 whole frames/five actor controls and six viewed screens. '
    'Existing actual B177 evidence retains11 timing differences,14 following A-indicator '
    'RGB differences and unequal PRNG seeds;no full-RAM,future-world,new causal trace or '
    'hardware claim. Promoted main V4595 and pushed eff4adb/tag promoted-v4595 remain '
    'unchanged. Later work is local. Coverage stays5885 integrated/completed contextual '
    'rereads,zero pending credited route drafts,source/prose5888,SC24032/SC364,historical '
    '3738 revisions/2147 retentions androute4286/4286. The B178 thirteen decisions are '
    'uncredited drafts. Registry,builder,immutable inputs,accepted layers,all earlier '
    'packages,ROMs,translations,executed producers/proofs/failures and full ledger history '
    'remain preserved. One-space CRLF ledger encoding stays in use. Preserve the corrected '
    'completion-audit identifiers and six-name row-count successor. This checkpoint adds '
    'no ROM,emulator run,source/prose or completion credit.\n\n'+NEXT)


def same_except(a,b,allowed):
    assert {k:v for k,v in a.items() if k not in allowed}=={k:v for k,v in b.items() if k not in allowed}


if __name__=='__main__':
    assert not ROOT.exists()
    lp=Path('translations/editorial_review_current_v1.json');oldbytes=lp.read_bytes();before=read(lp)
    assert sha(oldbytes)==read(PRIOR)['ledger_sha256']
    doc=read(DOC);rows=doc['records']
    assert len(rows)==13 and Counter(r['editorial_decision'] for r in rows)=={'revise':2,'retain-wording':11}
    assert doc['formatting_review_pending'] and doc['source_prose_or_completion_credit_added']==0
    assert all(r['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False) for r in rows)
    paths=[DOC,PRIOR,Path(__file__),Path('scripts/lil_B178_prose_v4671.py')]
    for k in ['source_context','control_contract','whole_exchange_context_notes','actor_voice_contract','branch_proof',
        'source_entry_proof','source_effect_and_predicate_contract','actor_terminology_reconciliation',
        'source_nameplate_consumer_proof','effective_current_comparison']:
        path=Path(doc[k]);assert sha(path.read_bytes())==doc[k+'_sha256'];paths.append(path)
    evidence={str(p):sha(p.read_bytes()) for p in paths}
    ledger=deepcopy(before)
    assert 'lil_B178_uncredited_draft_v4673' not in ledger
    ledger['lil_B178_uncredited_draft_v4673']=dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),
        uncredited_objects=13,proposed_revisions=2,justified_retentions=11,evidence=evidence,
        formatting_native_actual_references_and_registered_release_pending=True,
        source_prose_reviews_added=0,completion_credit_added=0,next=NEXT,full_goal_complete=False)
    ledger['latest_checkpoint']=SUMMARY
    for a,b in zip(before['coverage_units'],ledger['coverage_units'],strict=True):
        if a['id']=='all-route-scenes':b['next']=NEXT;same_except(a,b,{'next'})
        else:assert a==b
    same_except(before,ledger,{'latest_checkpoint','lil_B178_uncredited_draft_v4673','coverage_units'})
    assert tuple(ledger[k] for k in ['records_editorially_completed','records_with_source_and_prose_pass',
        'records_revised_and_integrated','retained_wordings_editorially_completed'])==(5885,5888,3738,2147)
    fresh=ledger['contextual_story_natural_dialogue_pass_v1871']
    assert tuple(fresh[k] for k in ['fresh_pass_records_explicitly_reread','fresh_pass_records_integrated',
        'fresh_pass_records_pending_native_actual_release'])==(5885,5885,0)
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete']
    planned={lp:encode_ledger(ledger)};assert len(planned[lp])<100*1024*1024
    ROOT.mkdir(parents=True)
    (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(oldbytes,mtime=0))
    section='## V4673: B177 integrated;13 uncredited B178 contextual decisions\n\n'+SUMMARY+'\n\nDraft: '+DOC.as_posix()+'. Verified B177: '+PRIOR.as_posix()+'.\n\nNext: '+NEXT+'\n\n'
    for i,name in enumerate(['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']):
        p=Path('docs')/name;(ROOT/(name+'.before')).write_bytes(p.read_bytes())
        first,rest=p.read_text(encoding='utf-8').split('\n',1)
        planned[p]=(('# Current editorial handoff - V4673' if i==0 else first)+'\n\n'+section+rest).encode('utf-8')
    staged=ROOT/'staged';staged.mkdir();plan=[]
    for i,(p,data) in enumerate(planned.items()):
        out=staged/f'{i}.planned';out.write_bytes(data)
        plan.append(dict(target=str(p.resolve()),before_sha256=sha(p.read_bytes()),planned=str(out.resolve()),planned_sha256=sha(data)))
    save(ROOT/'mutation_plan.json',plan)
    stable={p:sha(Path(p).read_bytes()) for p in ['translations/release_stack.json','translations/promoted_build.json',
        'translations/rom_retention_pins.json','scripts/build_integrated_release.py']}
    for r in plan:
        assert sha(Path(r['target']).read_bytes())==r['before_sha256'] and sha(Path(r['planned']).read_bytes())==r['planned_sha256']
    for r in plan:
        data=Path(r['planned']).read_bytes()
        with Path(r['target']).open('r+b') as stream:
            stream.write(data);stream.truncate(len(data));stream.flush();os.fsync(stream.fileno())
        assert sha(Path(r['target']).read_bytes())==r['planned_sha256']
    assert all(sha(Path(p).read_bytes())==h for p,h in stable.items())
    save(ROOT/'checkpoint_receipt.json',dict(checkpoint='V4673',ledger_sha256=sha(lp.read_bytes()),evidence=evidence,
        fresh_reread=5885,integrated=5885,pending_credited=0,uncredited_B178_draft=13,source_prose=5888,
        revised=3738,retained=2147,new_source_prose_reviews=0,new_completed_records=0,new_emulator_runs=0,
        stable_release_files=stable,updated_files={str(Path(r['target']).relative_to(Path.cwd())):r['planned_sha256'] for r in plan},
        all_jobs_terminal=True,ROMs_deleted=0,full_goal_complete=False))
    print('V4673:13 uncredited B178 decisions checkpointed;5885 completed,main V4595/latest experimental V4655 preserved;full goal active.')
