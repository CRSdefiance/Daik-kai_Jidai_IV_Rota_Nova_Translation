"""Keep the new clean-source Rafael work and full editorial scope in a reversible checkpoint."""
import ast
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
SOURCE=Path('scripts/checkpoint_retrospective_B218_v7851.py')
TARGET=Path('scripts/checkpoint_Rafael_B45_source_v7865.py')
ROOT=Path('work/analysis/Rafael_B45_source_checkpoint_tools_v7865')
FINDING="""Current registered experimental V7857 and verified completionV7863 contain the integrated Lil B218 R27 wrap improvement. The complete632-batch/114-accepted-layer stack passes18 release checks and110 regressions,equals the reviewed reference,and reconstructs byte for byte from its clean-input patch. All6938 completed/6941 source-prose anddrafts/4347 integrated wording revisions/2591 retentions remain;the B218 retrospective update adds no duplicate credit. MainV4701 and every earlier artifact remain.

The next fresh main-story source review returns to Rafael's SC0 catalogue. Complete clean B45 has12 stored speeches,24 native commands,764 stored/762 logical bytes andtwo zero tail bytes. No source record overlaps the completed ledger. All12 Japanese speeches were read and freshly glossed before any current B45 English body was exposed. This is source-only progress,not a completed translation or new source/prose credit.

Source EV0 event45/category5/action46 selectsB45 and lists no explicit completion prerequisites or exclusions. The reviewed openingB44/event44 has no direct completion-dependency edge to45. Neither numeric adjacency nor those empty lists proves immediate chronology,natural eligibility/activation or original scene location. The dialogue itself refers to Lisbon andCeuta.

Rafael looks for the companion mentioned asフリオ,finds him at the trading facility,and learns about selling trade goods,obtaining local trading agreements by paying the ruler through a palace/governor's office,using the minimum fee early on,andhandling future agreements himself. The companion says he arranged Ceuta's agreement;one FE information panel states FO's Ceuta market share is20percent andthat trading depends onshare. The companion invites an optional sale andRafael agrees. Preserve the conditional cargo/sale/early-fee qualifications andthe difference between agreeing andhaving completed a profitable sale. Do not invent kinship,rank,fee amount,deadline,guaranteed mechanics orcompany ownership.

Original speakers/selectors are00 and06 plus one FE system panel. Native names/voices,Julio's exact approved forms,Rafael's current substitutions andboth progressive/FE consumers still require binding. Source macros areFI0/FA0/FO1. Preserve the complete leading00 selector andsix-byte preamble;FE is a display selector,not a character. The 20percent/company panel needs its own native percent/substitution/bounds check. The source also contains0100/0200/0300/0400 relative controls,61FF/6300/6328/632B/8000/C281 andcomplete ends;their original native behavior,conditions andbranches remain to be reviewed. Do not assume all12 stored speeches execute together.

The remaining12 retrospective wrap candidates remain open and are rebound offline toV7857. The original558-plan scan doesnot cover all6938 completed records. Retain the source-supported151-159 水夫/Sailor progressive nameplates while reviewing separate配下/Retainer full-name andother consumers. Continue all four storylines andearlier translations,broad practical shop/town/random scenes,Help andall remaining player prose,all207 names/roles/aliases andevery unfinished inventory/counterpart/item/display lead. Preserve all ROMs,translations,drafts,failed producers,proofs andmeasured limits. Graphics/all18 plaques andlater older-record technical re-audit stay separate. No canceled separate unified test package,promotion,pruning,commit orpush."""
NEXT="""Continue from verifiedV7866/currentV7857 andRafael's source-only B45 packet work/analysis/Rafael_next_clean_v7864/complete_clean_SC0_B45_EV0_andcoverage_before_current_English.json plus work/analysis/Rafael_B45_clean_gloss_v7864b/twelve_fresh_clean_exchange_glosses_before_current_English.json. All12 clean Japanese speeches areglossed;current B45 English remains unread. First bind the original event/branch/control scope andsource names/roles. Capture Rafael's own currentV7857 NewGame context when needed;verify actualcaptain0 andthe full current runtime/payload rather than using Lil's orMaria's RAM. Measure original0/6 getters andFO substitution,keep approvedRafael,andresolveJulio fromclean/source consumers without inventing relationship orrank.

Then compare all12 current effective English speeches asacomplete exchange against the clean glosses,binding catalogue routes and original controls before drafting natural-dialogue-v2 prose. Preserve the local trading-rights meaning ofagreement,conditional Lisbon cargo andoptional sale,early minimum-fee advice,Ceuta20percent market-share information andFO order. Treat the oneFE panel andpercent handling separately fromprogressive dialogue. Native branches/relative spans,complete first/final glyphs,bounds,pagination andrepresentative actual paths need their own source/current evidence;no generic wrap orall-lines-played assumption. Add credit only after necessary contextual/native/actual/registered integration checks.

B218's wrap isalready integrated andverified inV7857;do not replay unchanged checks. For future Lil native work use work/analysis/current_V7857_Lil_native_v7860/current_native_input.json. Other routes' earlier snapshots remain correctly labelled historical;obtain own current contexts when needed. Review the12 remaining contraction/question-tag candidates ascomplete exchanges,extend beyond the558 recorded markup plans,andretain ordinary wraps with reasons.

Keep the full four-storyline/earlier-dialogue/shared shop-town-random/Help/remaining-prose/207-name objective intact. Preserve all earlier unfinished inventories,role/item/counterpart/display leads,normal-end value-carry andsource-only nineteenth-cell findings for the later technical re-audit. Graphics/all18 plaques remain separate. Preserve every generated ROM andearlier translation. MainV4701 stays;no canceled separatepackage,automaticpromotion,pruning,commit orpush."""
GATES='''def gates():
    prior,proof=map(read,[PRIOR,PROOF])
    source=read(proof['source_packet'])
    assert proof['source_packet_sha256']==sha(Path(proof['source_packet']).read_bytes())
    assert len(proof['records'])==12 and proof['all12_complete_clean_Japanese_speeches_read_before_current_English']
    assert proof['no_current_English_comparison_localized_manuscript_orcomplete_prose_approval']
    assert all(r['current_English_body_unread'] and r['review']['source'] and not r['review']['formatting'] for r in proof['records'])
    assert source['live_ledger_sha256']==prior['ledger_sha256'] and source['source_only_no_current_English_exposed_orused']
    assert len(source['groups'])==1 and source['groups'][0]['block']==45 and source['groups'][0]['physical_speech_objects']==12
    assert source['groups'][0]['completed_coverage_overlap']==0 and not source['inventory_failures']
    assert sha(Path(source['source_ROM']).read_bytes())==source['source_ROM_sha256']
    assert not proof['new_credit'] and not proof['new_emulator_runs']
    assert sha(Path(prior['candidate']).read_bytes())==prior['candidate_sha256']
    assert sha(Path(prior['patch']).read_bytes())==prior['patch_sha256']
    return prior,proof'''
if __name__=='__main__':
    assert not ROOT.exists() and not TARGET.exists()
    text=SOURCE.read_text(encoding='utf-8');tree=ast.parse(text)
    assigns={n.targets[0].id:ast.get_source_segment(text,n) for n in tree.body if isinstance(n,ast.Assign)
        and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}
    gates=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='gates')
    evidence=next(n for n in ast.walk(tree) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='evidence' for t in n.targets))
    newevidence="""evidence={str(p):sha(p.read_bytes()) for p in [PRIOR,PROOF,scope,Path(__file__),
            Path('work/analysis/Rafael_next_clean_v7864/complete_clean_SC0_B45_EV0_andcoverage_before_current_English.json'),
            Path('scripts/inventory_Rafael_next_clean_v7864.py'),Path('scripts/gloss_Rafael_B45_clean_v7864b.py')]}"""
    changes={
        assigns['FINDING']:'FINDING='+repr(FINDING),assigns['NEXT']:'NEXT='+repr(NEXT),
        assigns['SUMMARY']:'SUMMARY=FINDING',ast.get_source_segment(text,gates):GATES,
        ast.get_source_segment(text,evidence):newevidence,
        'work/analysis/retrospective_B218_checkpoint_v7851':'work/analysis/Rafael_B45_source_checkpoint_v7865',
        'editorial_handoff_verification_v7852':'editorial_handoff_verification_v7866',
        'editorial_handoff_verification_v7835':'editorial_handoff_verification_v7863',
        'translations/lil_B218_retrospective_layout_manuscript_v2.json':'work/analysis/Rafael_B45_clean_gloss_v7864b/twelve_fresh_clean_exchange_glosses_before_current_English.json',
        'retrospective_B218_native_actual_policy_pending_integration_v7851':'Rafael_SC0B45_clean_gloss_pending_v7865',
        'unfinished_editorial_scope_v7851':'unfinished_editorial_scope_v7865',
        "old['unfinished_editorial_scope_v7834']":"old['unfinished_editorial_scope_v7862']",
        'wordings_retained=13,pending_layout_revisions=1,other_exact_compiled_reuses=12':'clean_source_speeches=12,fresh_source_glosses=12,current_English_bodies_unread=True',
        'native_actual_policy_complete_atomic_registered_release_pending=True':'native_names_macros_branches_current_English_andall_display_gates_pending=True',
        'wording_retentions=13,pending_automatic_wrap_revisions=1,no_duplicate_dialogue_credit=True':'clean_source_speeches=12,fresh_source_glosses=12,no_source_prose_orcompletion_credit=True',
        'new_credit=0,new_emulator_runs=3,new_actual_frames=36003,new_native_getter_executions=0':'new_credit=0,new_emulator_runs=0,new_actual_frames=0,new_native_getter_executions=0',
        'only13_metadata_leads_andone_pending_changed_plan_not_broad_wrap_approval=True':'clean_Japanese_only_no_current_English_orlocalized_prose_exposed=True',
        'full_scope_all13_other_wrap_leads_andnames_remain_open=True':'full_scope_remaining12_wrap_leads_andnames_remain_open=True',
        '## V7851: B218 wrap native/actual/policy approved; atomic registered integration pending':'## V7865: Rafael B45 clean-source review begun; V7857 current',
        '# Current editorial handoff - V7851; V7821 current':'# Current editorial handoff - V7865; V7857 current',
        'Six retrospective-wrap checkpoint targets staged':'Six Rafael clean-source checkpoint targets staged',
        'Six audited retrospective-wrap checkpoint targets applied':'Six audited Rafael clean-source checkpoint targets applied',
        'V7821/6938completed unchanged':'V7857/6938completed unchanged',
        'retrospective_B218_R27_layout_pending=True,retrospective_B218_native_actual_policy_complete=True,retrospective_wrap_leads=13,':
        'Rafael_B45_clean_source_review_pending=True,Rafael_B45_fresh_clean_glosses=12,Rafael_B45_current_English_bodies_unread=True,',
        'pending_layout_manuscript=str(PROOF),pending_layout_manuscript_sha256=sha(PROOF.read_bytes()),':
        'pending_Rafael_source_gloss=str(PROOF),pending_Rafael_source_gloss_sha256=sha(PROOF.read_bytes()),',
        "strict_own_Lil_current_input='work/analysis/current_V7821_Lil_native_v7837/current_native_input.json',":
        'Rafael_B45_own_current_route0_context_pending=True,',
        'V7852 verified:B218 wrap native/actual/policy approved;atomic integration pending;V7821/6938complete remain.Fullobjective active.':
        'V7866 verified:Rafael B45 clean12 glosses/current English unread;V7857/6938complete remain.Fullobjective active.',
    }
    result=derive(str(SOURCE),str(TARGET),changes)
    ROOT.mkdir(parents=True);save(ROOT/'provenance.json',dict(derivation=result,
        all_original_inverse_hash_counter_family_currentROM_andscope_guards_preserved=True,
        source_only12_glosses_no_current_English_exposed_no_credit_orROMchange=True,full_goal_complete=False))
