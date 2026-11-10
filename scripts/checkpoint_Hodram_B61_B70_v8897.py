"""Persist full224 prose/native-page progress without completion credit."""
import sys
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B61_B70_checkpoint_v8897')
LEDGER=Path('translations/editorial_review_current_v1.json')
PRIOR=Path('work/analysis/editorial_handoff_verification_v8889/verified_handoff.json')
KEY='Hodram_SC1B61_B70_224_prose229_native_English_pages_pending_storage_actual_release_v8897'
SCOPE='unfinished_editorial_scope_v8897'
DOC=Path('translations/hodram_B61_B70_editorial_manuscript_v1.json')
VIEW=Path('work/analysis/Hodram_B61_B70_native_view_v8896/all224_English_native229_pages_direct_view_andboundary_review.json')
EVIDENCE=[str(DOC),str(VIEW),str(PRIOR),'translations/hodram_B61_B70_editorial_manuscript_partial_v1.json',
 'translations/hodram_B61_B70_speaker_name_review_v1.json',
 'work/analysis/Hodram_B61_B70_prose_v8890/224_contextual_decisions_formatting_still_pending.json',
 'work/analysis/Hodram_B61_B70_logical_v8891/logical_paragraphs.json',
 'work/analysis/Hodram_B61_B70_layout_v8892/automatic_plans.json',
 'work/analysis/Hodram_B61_B70_layout_v8893/automatic_plans.json',
 'work/analysis/Hodram_B61_B70_pages_v8894/compiled_native_pages.json',
 'work/analysis/Hodram_B61_B70_boundary_review_v8895/actual_boundary_findings_andprose_preserving_corrections.json',
 'work/analysis/Hodram_B61_B70_source_review_v8884/source_context_names_display_review_before_current_English.json',
 'work/analysis/Hodram_B61_B70_current_v8885/current_effective.json',
 *[f'scripts/{p}' for p in ['review_Hodram_B61_B70_prose_v8890.py','prepare_Hodram_B61_B70_logical_v8891.py',
 'prove_Hodram_B61_B70_logical_v8891.py','prepare_Hodram_B61_B70_layout_v8892.py','plan_Hodram_B61_B70_v8892.py',
 'prepare_Hodram_B61_B70_layout_v8893.py','plan_Hodram_B61_B70_v8893.py','prepare_Hodram_B61_B70_pages_v8894.py',
 'prove_Hodram_B61_B70_pages_v8894.py','review_Hodram_B61_B70_plan_deltas_v8895.py','record_Hodram_B61_B70_native_view_v8896.py']]]

TEXT="""V8897 continues from verified V8889/current registered experimental V8865. The prior goal turn made concrete progress through224 clean/source/native/current bindings and44 prose decisions. This continuation completes the other180 individual decisions andall224 logical/compiled native English page checks anddirect views. Full objective stays active. No completion/source-prose credit, ROM, registered build, emulator run, promotion, separate package, pruning, commit or push. Counts remain7,319 completed/7,322 credited source-prose anddrafts/4,538 integrated revisions/2,781 retentions. Preserve every prior artifact andall earlier limitations. Roughly20,000 remaining is a planning estimate,not an audited denominator.

Full manuscript translations/hodram_B61_B70_editorial_manuscript_v1.json has224 individual four-prose-gate decisions:132 revisions/92 justified retentions. The earlier44 complete record values are reused exactly from partialv1;all180 new decisions include exact source/current/effective references,meanings,findings,reasons andall mapped alternate-path neighbor pairs. All224 formatting gates remain false pending stored/actual/release validation. Revisions reconcile Nagarpur/Sirwood with reviewed names,remove invented Lord,restore the Nagarpur Company/local power/money-versus-ability exchange,Indian Ocean/leaf/legend/country andkingdom context,the captain's apology andpromise to search,Sera's intended return andconfident belief in sea kingship,andhis qualified resilience/trust warning. Maria's full identity,conditional hostility to exploitation,naval ambition,rivalry/huge spice profits/forced occupation/arbitrary arrests/violent repression,active strategy,unexplained current fleet constraint andcontinued plan remain. Camille's prospective trap warning,Batavia andown promise of explanation,Lil's almost-doubting-Maria rather than making her an enemy,neutral reconciliation/missed work,andall wealth forKuhn's victims/unnamed mixed-in object are preserved. No invented romance,kinship,rank,historical biography,death count,reinforcements orcompleted future outcomes. Allsix circle/cross utterances remain exact opaque source language. Retain existing wording individually where it works;132 revisions are not132 runtime bugs.

Logical8891 passes896 fresh original native default-name alignments for224 one-paragraph English bodies in own V8865/captain1 context. First automatic plans8892 pass structural QA butdirect boundary review finds real readability problems:an incomplete first row You truly,split don't/you? tag,andHe won't separated frombe across a page;the question afterTell me... also benefits from staying together. Qualified planner8893 changes16 plans without changing a word. Remove only this batch's newly overconstraining king/of pair;add source-prose compound/tag/auxiliary preferences;allow a short complete first clause ending in sentence/pause punctuation while retaining the incomplete-opening preference. Every216px viewport/font/macro/pair-phase/guard/native-page-height/base-QA rule remains. No authored linebreaks,padding,narrower rows,fit-driven shortening,warning removal orwaivers. All68 original QAinfos remain,withzero warnings/errors. Source-bound33 non-ASCII retained bodies are exact current/clean punctuation,opaque language orcurrent full-width I values,not arbitrary multibyte prose. The before/after plans andfinding reasons remain in8895.

Compiled native8894 freshly executes all224 paragraphs/896 macro alignments andrenders229 complete progressive pages,includingfive two-page speeches B67R66/R165/R168/R172/R238. All23 English sheets were directly viewed in8896. Complete leading/internal/final codes,independent pixels,bounds,consumption,pagination andoriginal continuation-guard behavior pass. Every opaque symbol andthe full-width I introductions/apology remain complete. The English record begins atoriginal x0;an original continued-page guard canoccupy x0 before the first visible glyph atx6. B64R63 iron/ship is a reviewed ordinary complete-word wrap withinfour original rows,not a split word orlost glyph. Automatic long strategic paragraphs continue onpage2 withallwords present;representative actual paging stillneeds testing. No blank,overlap orunexpected extra page appears offline. This is native CPU/render evidence,not actual gameplay,source eventactivation,portrait/header/transition orhardware coverage.

Report actual findings separately from passing validation:the editorial review finds factual/voice/naturalness issues;four first-plan readability findings are corrected;the new source controls,logical macros andcompiled native page checks findzero new runtime control/glyph/bounds failures. Passing checks protect invariants anddo not themselves count as bugs found. Further stored-script oractual gameplay checks may expose different defects. The user's clarification aboutthis distinction is retained here forfuture updates.

Reuse all completed8877-8885 clean meanings/source controls/names/32clean32current getters/24nameplanes/224sourcepages/23sourceviews/45linked context speeches/15,830 structural combinations/current224 predecessor bindings. Source controls remain392commands/224preambles/60relative sites300cases/15unforcedqueries/83opaque pairs/250seeded fullnormalends. FI15/FA3/FO0 anddefaultHodram6/Bergstrom9/Fleet15 remain;no new FO semantics/custom-name coverage. Preserve source8100event44's unforced result,all alternative dialogue membership andopaque-effect limitations. Sixteen scoped progressive name retentions remain,withall207/fullcatalogue/customnames,AlShin full-name contexts,Geronimo/Alonso sharedデ field ownership/deployment/consumers andall prior name leads open.

Next:use fullmanuscriptv1,logical8891,finalplans8893,nativepages8894,directview8896 to map complete resized stored blocks/relative operands/normalends/tails,independent source/current/final references andwhole block/archive/NDS inverses;validate actual stored native planes andloaders. Then representative initialized ornatural gameplay/focused risks forconditional branches,mixedwidth retained language/name glyphs,progressive/multipage behavior andtransitions,without forcing plot/roster/flags/RNG/results. Complete production/atomic guards andregistered cumulative integration/exactclean-input patch/ownstartup beforeonce-only224 credit. Exhaustive natural playthroughs andindividually visiting everyconditional line arenotrequired. The new jobs logical74493/native54986 terminated successfully;do notreplay completed native checks because earlier outputwasquiet.

Current experimental V8865/exactpatch/648manifestbatches/114acceptedlayers/18releasechecks/110regressions/own4001-framestartup remainunchanged. MainV4701/canonicalbaseline remainunchanged. Reuse allcompleted B54-B60 andolderproofs without unnecessary repetition. Preserve allprevious long/focused gameplay timing,decoded-length,RNG,RGB,following-command andB60actor differences andthe absence ofimmediate-returnmainRAM;nonewcausal orfuture-equivalence claim.

The fullfour-storyline/earlierstorydialogue/sharedtown-shop/random/Help/restprose/207proper-role-alias-customnames/retrospectivepremature-break objective andeveryprevious unfinished-scope value/lead remainactive. Allprior ledger/scope values anddocument bytes arepreserved byindependent inverseaudit. Graphics/all18plaques andlaterolder-recordtechnicalre-audit stayseparate. Preserve everyROM,translation,draft,producer,proof andfailure. The fullgoal remainsincomplete.
"""

if __name__=='__main__':
    mode=sys.argv[1]
    if mode=='stage':
        assert not ROOT.exists();old=read(LEDGER);prior=read(PRIOR);doc=read(DOC);view=read(VIEW)
        assert prior['pass'] and sha(LEDGER.read_bytes())==prior['ledger_sha256'] and old['goal_status']=='active' and not old['full_goal_complete']
        assert old['records_editorially_completed']==7319 and doc['revised']==132 and doc['retained']==92 and len(doc['records'])==224
        assert view['all23_sheets229_English_native_pages_directly_viewed'] and view['complete_native_pages']==229
        assert KEY not in old and SCOPE not in old
        ROOT.mkdir(parents=True);(ROOT/'ledger_before.json').write_bytes(LEDGER.read_bytes())
        evidence={p:sha(Path(p).read_bytes()) for p in EVIDENCE+[__file__]}
        pending=dict(status='224-four-prose-gate-decisions-229-native-English-pages-viewed-stored-actual-production-atomic-registered-release-pending',
            total_uncredited_physical_speeches=224,individual_prose_decisions=224,draft_revisions=132,justified_draft_retentions=92,
            remaining_individual_prose_decisions=0,complete_native_English_pages=229,two_page_records=5,English_sheets_directly_viewed=23,
            all224_formatting_gates_still_false=True,original_QA_infos=68,warnings=0,errors=0,waivers=0,
            actual_first_plan_readability_findings=4,plans_refined=16,new_control_glyph_bounds_failures=0,
            manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),native_view=str(VIEW),native_view_sha256=sha(VIEW.read_bytes()),
            names='translations/hodram_B61_B70_speaker_name_review_v1.json',evidence=evidence,
            supersedes_pending_state_only='Hodram_SC1B61_B70_224_source_native_current_bound_first44_prose_180_pending_v8887',
            new_credit=0,new_emulator_runs=0,new_ROM=False,full_goal_complete=False)
        new=deepcopy(old);new['latest_checkpoint']=TEXT;new[KEY]=pending
        descriptor=old['unfinished_editorial_scope_v8887'];scopepath=Path(descriptor['path']);assert sha(scopepath.read_bytes())==descriptor['sha256']
        (ROOT/'scope_before.json').write_bytes(scopepath.read_bytes());scope=read(scopepath);assert KEY not in scope;scope[KEY]=deepcopy(pending)
        save(ROOT/'unfinished_editorial_scope_inventory.json',scope)
        new[SCOPE]=dict(path=str(ROOT/'unfinished_editorial_scope_inventory.json'),sha256=sha((ROOT/'unfinished_editorial_scope_inventory.json').read_bytes()),
            all_prior_leads_families_history_andfull_four_storyline_objective_preserved=True,new_completion_credit=0,new_uncredited_source_positions=224,full_goal_complete=False)
        new['research_checkpoints'].append(dict(id='V8897-Hodram-B61-B70-224-prose-229-native-English-pages',documentation='docs/editorial_Hodram_B61_B70_v8897.md',
            manuscript=str(DOC),native_view=str(VIEW),new_editorially_completed=0,new_registered_ROM=False,new_emulator_runs=0))
        save(ROOT/'ledger_staged.json',new);documents=[]
        for path,header in [('docs/editorial_handoff_current.md','# Current editorial handoff - V8897; V8865 current\n\n## B61-B70:224 prose decisions/229 native English pages;stored-actual-release pending\n\n'),
            ('docs/known_issues.md','## V8897 Hodram complete prose/native display checkpoint\n\n'),('docs/todo.md','## V8897 active full editorial continuation\n\n')]:
            p=Path(path);data=p.read_bytes();backup=ROOT/(p.name+'.before');backup.write_bytes(data);staged=ROOT/(p.name+'.staged');prefix=(header+TEXT+'\n').encode();staged.write_bytes(prefix+data)
            documents.append(dict(path=path,before=str(backup),before_sha256=sha(data),staged=str(staged),staged_sha256=sha(staged.read_bytes()),prefix_bytes=len(prefix)))
        cp=ROOT/'editorial_Hodram_B61_B70_v8897.md';cp.write_text('# Hodram B61-B70 checkpoint V8897\n\n'+TEXT,encoding='utf-8')
        c=old['current_integrated_candidate'];protected=[Path(p) for p in [c['path'],c['patch'],c['manifest'],'translations/release_stack.json',
            'scripts/build_integrated_release.py','out/raphael_natural_v2_accepted_base.nds','work/clean.nds']]
        save(ROOT/'stage_manifest.json',dict(previous_verified_handoff=str(PRIOR),previous_verified_handoff_sha256=sha(PRIOR.read_bytes()),
            ledger_before_sha256=sha(LEDGER.read_bytes()),ledger_staged_sha256=sha((ROOT/'ledger_staged.json').read_bytes()),
            scope_before_path=str(scopepath),scope_before_sha256=sha(scopepath.read_bytes()),documents=documents,
            checkpoint_doc=str(cp),checkpoint_doc_sha256=sha(cp.read_bytes()),protected_files={str(p):sha(p.read_bytes()) for p in protected},
            evidence=evidence,new_credit=0,new_emulator_runs=0,full_goal_complete=False))
        print('Staged full224-prose/229-native-page progress; independent audit required;zero credit.')
    elif mode=='apply':
        m=read(ROOT/'stage_manifest.json');audit=read(ROOT/'independent_staged_audit.json');assert audit['pass'] and audit['stage_manifest_sha256']==sha((ROOT/'stage_manifest.json').read_bytes())
        assert sha(LEDGER.read_bytes())==m['ledger_before_sha256']
        for p,h in {**m['evidence'],**m['protected_files']}.items():assert sha(Path(p).read_bytes())==h
        for d in m['documents']:assert sha(Path(d['path']).read_bytes())==d['before_sha256'] and sha(Path(d['staged']).read_bytes())==d['staged_sha256']
        target=Path('docs/editorial_Hodram_B61_B70_v8897.md');assert not target.exists()
        LEDGER.write_bytes((ROOT/'ledger_staged.json').read_bytes())
        for d in m['documents']:Path(d['path']).write_bytes(Path(d['staged']).read_bytes())
        target.write_bytes(Path(m['checkpoint_doc']).read_bytes())
        save(ROOT/'applied.json',dict(ledger_sha256=sha(LEDGER.read_bytes()),stage_manifest_sha256=sha((ROOT/'stage_manifest.json').read_bytes()),new_credit=0,full_goal_complete=False))
        print('Applied independently audited progress;live verification required.')
    else:raise ValueError(mode)
