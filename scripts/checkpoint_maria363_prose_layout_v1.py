"""Publish363 contextual decisions and fresh layout plans without integration credit."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v10 import checkpoint

ROOT=Path('work/Maria_B216_B252_clean_20261110')


def main():
    releasepath=Path('work/maria321_B196_B215_release_v1/registered_release_verification.json');release=load(releasepath)
    manuscript=Path('translations/maria_B216_B252_contextual_review_v1.json');namepath=Path('translations/maria_B216_B252_scoped_names_v1.json')
    planpath=ROOT/'plan_v5/automatic_plans.json';doc,names,plan=map(load,[manuscript,namepath,planpath])
    initial={r['id']:r for r in load(ROOT/'plan_v1/automatic_plans.json')['records']}
    assert len(doc['records'])==363 and doc['complete_exchanges']==37
    assert (doc['proposed_revisions'],doc['justified_retentions'])==(203,160) and len(names['records'])==29
    gates=dict(source=True,context=True,localization=True,naturalness=True,formatting=False)
    assert all(r['review']==gates for r in doc['records']+names['records'])
    assert len(plan['records'])==351 and not plan['failures']
    assert not any(i['severity'] in ['error','warning'] for r in plan['records'] for i in r['base_QA']['issues'])
    pages=sum(r['expected_native_pages'] for r in plan['records']);assert pages==353
    changed=[r['id'] for r in plan['records'] if r['lines']!=initial[r['id']]['lines']];assert len(changed)==12
    native=load(ROOT/'native_inputs_v1/manuscript.json');assert len(native['records'])==351
    assert load(ROOT/'native_inputs_v1/separate_choice_scope.json')['choice_captions']==12
    paths=[releasepath,manuscript,namepath,planpath,ROOT/'plan_v5/diagnostics.json',Path(__file__)]
    paths += [ROOT/n for n in ['clean_draft_seal_v1.json','all363_clean_meanings_v1.json','all363_independent_drafts_v1.json',
        'contextual_comparisons_v1.json','current_v1/current_effective.json','current_objects_v1/current_objects.json',
        'scoped_names_macros_reference_v2.json','scoped_terms_reference_v1.json','dynamic_roles_current_v1.json','prose_gates_v1.json',
        'formatting_v1/formatting_input.json','formatting_v1/native_macro_measurements.json','formatting_v1/page_phrase_preferences_v4.json',
        'native_inputs_v1/manuscript.json','native_inputs_v1/plans.json','native_inputs_v1/separate_choice_scope.json']]
    evidence={str(p):digest(p) for p in paths}
    summary=('Maria B216–B252 now has363 contextual reviews across37 complete groups:203 proposed revisions,160 justified retentions and29 scoped name reviews. '
        'All four individual prose gates pass;all fifth gates remain pending. Fresh full-width plans cover351 bodies/353 pages plus12 captions,with no errors,warnings orfailures. '
        'Twelve layouts improve;native rendering,all-page visual review,storage,representative gameplay andregistered integration remain. '
        'No new ROM orcredit;22,707 integrated,registered5836b998,main andfull scope areunchanged. No worker islive.')
    document='docs/editorial_Maria363_B216_B252_prose_layout_20261110.md'
    text=f'''# Maria363 B216–B252 prose and layout checkpoint — November 10, 2026

{summary}

All363 clean meanings and independent drafts were saved and sealed before this batch's first current-story-English extraction. Four immutable authored parts cover B216–226(133),B227–243(100),B244–251(42),B252(88). The original first part and its outputs are preserved alongside a clean-only amendment clarifying the right-hand puzzle stone and replacing an unsupported friendship implication with companions. Exact source/current references,whole-exchange context,individual findings,proposals andretention reasons are in `{manuscript}` and `work/Maria_B216_B252_clean_20261110/contextual_comparisons_v1.json`. No completion credit is claimed.

The complete exchanges cover town ruins leads,two figurehead encounters,the water-and-floating-ice puzzle,eight guild requests/captures/handovers/reminders andthe branching forest/bear expedition. Meaning corrections restore Indonesia and India clues,reported uncertainty,Jean's circular denial joke,his French identity,the ship thief's fleet rather than a wholly stolen fleet,Maria's actual conditional replies andHernan's missing defeat objective. Remove the unsupported man-like-you reference to Maria,Lord title for Hernan andfinancial claim that Yuris is penniless. Correct the forest choice from Be brave to Fight bravely andthe intimidation choice to Scare it off. Keep the bear's possible man-eater status speculative,Emilio's sleep gag andsource injury qualifications. Preserve supernatural claims as character speech andconditional alternatives as alternatives. Working dialogue,reward amounts,share notices andclear captions have individual justified retentions.

Twenty-nine scoped names/roles pass four prose gates. Original native name getters bind58 cases,including the current156 fallback. Installed Jean Ramusio,Yuris Huygens,Gabriel Cardocci andHernan Berio are reconciled in dialogue;other supported names are retained with individual reasons. City/region metadata isnot a surname. Guildmaster andBarkeep remain roles;familiar addresses add no kinship. Source selectors207/208/211/215/216 are bound through original dispatch:207 resolves toMaria3;the others areunassigned atstartup andfall back to156/voice4. This isnot proof offuture conditional crew assignment oractual forest participation. All85 physical alternatives across12 style objects preserve their96 native slots/aliases. Twelve captions retain original two/three-choice order. Luck/Charm are bound toexact clean/current registered UI spans;translated notices do not prove executed stat effects. No global name-table approval ornew name bytes are claimed.

Fresh formatting preserves logical paragraphs,all13 FI/FA occurrences,complete original controls andvalidated216px progressive/228px FE geometry. Twenty exact compatible default-macro proofs are explicitly reused. Use `formatting_v1/formatting_input.json`, `formatting_v1/page_phrase_preferences_v4.json` and `plan_v5/automatic_plans.json`. All351 bodies/353 planned pages pass with zero errors,warnings orfailures. Twelve layouts change from the first plan. The gold-river opening grows from13 characters to28 anduses three rows instead offour;the Jean question loses a premature18-character first row andkeeps Jean Ramusio together. Puzzle conditions,escape phrases andshort questions stay coherent. Yuris's second page contains the whole final sentence rather than and fled. The pictorial-map report stays onone page within the same two-page body;first-page shorter trailing rows are the recorded cost ofkeeping that complete report together. No prose isshortened andno ordinary manual breaks areauthored.

One narrowly bound QA retention recognizes Where are you from? as a complete question rather than a stranded preposition. It applies only toB234R37's exact prose/line/index;no native guard iswaived. Failed orwarning-bearing plan_v2/v3/v4 andall earlier preferences arepreserved,not approved. Rejected single-page and36-character-opening proposals didnot relax geometry orchange prose. Plan_v5 is the sole selected plan atthis checkpoint.

**Next:** `native_inputs_v1/manuscript.json` and `plans.json` select all351 exact bodies fornative checks;12 captions remain separately bound. Run complete leading/internal/trailing glyph,pixel,consumption,alignment,canary,bounds/allocation/pagination checks anddirectly review every newly generated page onreadable contact sheets. Compile/check complete styles,captions andnames,then reconstruct stored text,validate branches/loaders andrun representative initialized gameplay fordistinct selectors,FE returns,pagination,menus andtransitions. Actual batch gameplay coverage iszero;all37 groups areunvisited inthis batch. Current native name/style/dispatch bindings areoffline execution against the registered own-startup context,not fresh gameplay. No native body-page images orvisual approval exist yet. All fifth gates remain false. Integrate once necessary checks pass;do not repeat completed compatible proofs.

[Registered Maria321](editorial_Maria321_B196_B215_registered_20261110.md) remains the current cumulative parent:721 manifest entries,114 accepted layers,56 release checks,exact clean-input patch,own startup and24 protected getters. Candidate:`{release['candidate']}`;SHA256:`{release['candidate_sha256']}`. Main remains all-routes-unified-v4701;no promotion without acceptance. Preserve Market's allocation/both pointers,six-section ARM9,ASCII right bounds,source25v2,inherited B164R99 correction andall earlier archives,names,fonts andgraphics. The user's old testing build is already bound by the [recorded Market fix](editorial_market_goods_info_fix_20261109.md);do not reinvestigate that closed overread.

Integrated22,707 =13,576 revisions+9,131 retentions;historical source/prose/draft22,710. Native story remainder3,191 =Maria1,386+Lil1,805 includes this uncredited363;shared/player-facing inventories remain separate. Keep every storyline,earlier unfinished contextual pass,town/shop/random/player prose,name,glyph andwrap review in scope,with early Rafael/tutorial priority. No guide photos. Deferred graphics artwork andlater older-record technical re-audit remain separate. All ROMs/translations/drafts/evidence arepreserved. No cleanup,build,promotion,commit orpush occurred;no worker islive. Full goal remains active.
'''
    checkpoint(mutation=ROOT/'prose_layout_checkpoint_v1',batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0,current_batch='Maria363:363 contextual reviews/four prose gates;351 bodies/353 planned pages;native/visual/storage/gameplay/release pending.',
            current_batch_not_yet_integrated=True,current_batch_registered_andcredited_once=False,
            proposed_revisions=203,justified_retentions=160,all_current_batch_fifth_gates_pending=True,
            native_job_live=False,native_sessions=[],stored_job_live=False,stored_sessions=[],registered_build_live=False,
            registered_cumulative_build_live=False,current_batch_evidence=evidence,guide_photos=False,
            next_action='Use prepared351-body inputs/final plan_v5 forfresh native andall-page visual checks;then mixed objects/storage/representative gameplay/registered integration.'),
        additional_updates={'Maria_SC3_B216_B252_clean_20261110':dict(new_credit=0,
            clean_meanings_andindependent_drafts_pending=False,clean_meanings=363,independent_drafts=363,
            clean_meanings_path=str(ROOT/'all363_clean_meanings_v1.json'),independent_drafts_path=str(ROOT/'all363_independent_drafts_v1.json'),
            clean_source_draft_seal=str(ROOT/'clean_draft_seal_v1.json'),current_English_not_read=False,contextual_comparison_pending=False,
            individual_contextual_comparisons=363,names_terms_consumers_pending=False,scoped_name_reviews=29,native_name_getter_bindings=58,
            proposed_revisions=203,justified_retentions=160,first_four_individual_prose_gates_pass=True,
            all_five_review_gates_pending=False,all_fifth_gates_pending=True,planned_body_pages=353,planned_body_records=351,
            planned_layout_changes=changed,planned_pages_reclaimed=0,native_pages_visually_reviewed=0,actual_batch_gameplay_records=0,
            registered_integration_pending=True,no_batch_worker_live=True,evidence=evidence,full_goal_complete=False)},
        summary=summary,document=document,document_text=text,completed=22707,
        protected={'translations/release_stack.json':release['registry_sha256'],release['candidate']:release['candidate_sha256'],
            release['manifest']:release['manifest_sha256'],release['patch']:release['patch_sha256'],release['canonical_base']:release['canonical_sha256']})
    save(ROOT/'current_checkpoint.json',dict(document=document,source_objects=363,revisions=203,retentions=160,
        scoped_name_reviews=29,planned_body_records=351,planned_pages=353,changed_layouts=changed,
        first_four_gates_pass=True,all_fifth_gates_pending=True,no_batch_worker_live=True,
        no_new_ROM_orcompletion_credit=True,full_goal_complete=False,evidence=evidence))
    print('Published Maria363:203 revisions/160 retentions,29 scoped names,353 planned pages;22707 integrated unchanged.')


if __name__=='__main__':main()
