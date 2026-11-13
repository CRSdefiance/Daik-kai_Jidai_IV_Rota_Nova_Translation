"""Preserve the next complete prose batch and its explicitly unfinished layout checks."""
import ast
import gzip
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v10 import checkpoint

ROOT=Path('work/Lil269_B243_B282_clean_20261110')
ARCHIVE=Path('translations/editorial_checkpoints/Lil269_prose_20261110_v1')


def main():
    assert not ARCHIVE.exists()
    manuscript=Path('translations/lil_B243_B282_contextual_review_v2.json')
    namespath=Path('translations/lil_B243_B282_scoped_names_v2.json')
    doc,names=map(load,[manuscript,namespath])
    assert (doc['source_objects'],doc['complete_exchanges'],doc['proposed_revisions'],doc['justified_retentions'])==(269,40,104,165)
    assert len(names['records'])==25 and names['first_four_gates_pass']
    assert all(r['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False) for r in doc['records']+names['records'])
    gates=load(ROOT/'prose_gates_v2.json');assert gates['structural_projection_pass'] and gates['all_fifth_gates_false']
    plan=load(ROOT/'plan_v1/automatic_plans.json');qa=load(ROOT/'plan_v1/diagnostics.json')
    warnings=[r for r in qa['issues'] if r['severity']=='warning'];errors=[r for r in qa['issues'] if r['severity']=='error']
    assert len(plan['records'])==262 and sum(r['expected_native_pages'] for r in plan['records'])==265
    assert not errors and not plan['failures'] and len(warnings)==2
    assert {r['id'] for r in warnings}=={'SC2_B251_STYLE_352_212','SC2_B251_STYLE_900_214'}
    assert all(r['code']=='weak-line-ending' and "in!" in r['message'] for r in warnings)
    pending=ROOT/'layout_findings_v1.json';assert not pending.exists()
    save(pending,dict(initial_plan_exit_code=1,body_objects=262,provisional_pages=265,typed_captions=7,errors=errors,warnings=warnings,
        warnings_are_complete_caving_in_sentence_endings_not_approved_or_waived=True,
        unresolved_ordinary_page_boundaries=[dict(id=r['id'],logical_English=r['logical_English'],lines=r['lines']) for r in plan['records'] if r['expected_native_pages']>1],
        source_FE_riddle_anddirections_provisionally_fit_one_page_each=True,
        all_final_native_pixels_direct_visual_storage_gameplay_andrelease_gates_pending=True,new_credit=0))
    visual=ROOT/'current_context_v1/direct_visual_review_v1.json';assert not visual.exists()
    capture=load(ROOT/'current_context_v1/capture/capture_report.json')
    selected=[r for r in capture['frames_captured'] if r['frame'] in [2000,4000]];assert len(selected)==2
    for r in selected:assert digest(r['path'])==r['PNG_sha256']
    save(visual,dict(selected_captures=selected,both_selected_frames_directly_viewed=True,
        scope='Current candidate Lil character confirmation and opening text only; not the new269 optional events, full opening or hardware.',
        all_other_captured_frames_not_new_visual_credit=True,new_credit=0))
    files=[p for p in ROOT.rglob('*') if p.is_file() and p.suffix in ['.json','.txt']]
    ARCHIVE.mkdir(parents=True);artifacts={}
    for p in sorted(files):
        dest=(ARCHIVE/p.relative_to(ROOT)).with_suffix(p.suffix+'.gz');dest.parent.mkdir(parents=True,exist_ok=True)
        raw=p.read_bytes();dest.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0));assert gzip.decompress(dest.read_bytes())==raw
        artifacts[str(p)]=dict(archive=str(dest),source_sha256=digest(p),archive_sha256=digest(dest))
    producers=sorted(set(Path('scripts').glob('*lil269*.py'))|{Path('scripts/seal_clean_editorial_parts_v2.py'),Path('scripts/extend_scoped_names_for_roles_v1.py'),Path('scripts/prepare_captain_clean_formatting_v2.py')})
    for p in producers:ast.parse(p.read_bytes(),filename=str(p))
    archive_manifest=ARCHIVE/'archive_manifest.json'
    save(archive_manifest,dict(artifacts=artifacts,producers={str(p):digest(p) for p in producers},all_selected_artifacts_lossless=True,
        raw_ROM_RAM_andcaptures_preserved_locally_not_in_git_archive=True,records=269,first_four_gates_pass=True,
        formatting_pending=True,new_credit=0,full_goal_complete=False))
    rp=Path('work/lil382_residual_A_release_v1/registered_release_verification.json');release=load(rp)
    assert digest('translations/release_stack.json')==release['registry_sha256']
    protected={'translations/release_stack.json':release['registry_sha256'],release['candidate']:release['candidate_sha256'],
        release['manifest']:release['manifest_sha256'],release['patch']:release['patch_sha256'],release['canonical_base']:release['canonical_sha256'],
        'translations/promoted_build.json':digest('translations/promoted_build.json'),str(manuscript):digest(manuscript),str(namespath):digest(namespath)}
    evidence={str(p):digest(p) for p in [manuscript,namespath,archive_manifest,pending,ROOT/'clean_draft_seal_v1.json',ROOT/'prose_gates_v2.json',
        ROOT/'formatting_v1/native_macro_measurements.json',ROOT/'plan_v1/automatic_plans.json',ROOT/'plan_v1/diagnostics.json',rp]}
    summary=('The next269 Lil B243–B282 records have complete contextual prose decisions:104 proposed revisions,165 justified retentions and25 scoped name reviews. '
        'All first four individual gates pass; fifth gates remain false. Exact current bindings,roles,terms and20 native macro preflights pass. '
        'The provisional262-body/265-page plan has two unresolved weak-ending warnings andthree multipage boundaries to inspect;seven captions are separate. '
        'Native/visual/storage/representative gameplay andintegration remain. No new ROM orcredit;24,475 integrated. '
        'The pushed Lil382 testing candidate andmain are unchanged;full goal active,no worker live.')
    document='docs/editorial_Lil269_prose_plan_20261110.md'
    text=f'''# Lil B243–B282 prose and provisional layout — November 10, 2026

{summary}

The previous goal turn was progress: Lil382 was registered, credited once, packaged and pushed as `be889f2bdfe29d3f8329d1839bb37287c347d795`. This turn is progress: a new disjoint269-object batch has source-first meanings, independent drafts, complete comparisons and all four prose gates. Keep the full editorial objective active. No completed Lil382 check was restarted, no new candidate was promoted and no pending proposal receives completion credit.

Use `translations/lil_B243_B282_contextual_review_v2.json` and `translations/lil_B243_B282_scoped_names_v2.json`. All269 exact source/current references, findings, proposed revisions and individual retention reasons are present. Forty complete SC2 groups B243–B282 contain246 ordinary bodies,16 physical personality alternatives in two eight-slot objects, andseven captions across three menus, including a three-choice riddle. Of262 body candidates,226 are progressive and36 use native FE presentation. The existing native census is reused; clean source positions and disjoint current credit keys are checked without replaying the decoder.

Clean meanings and independent drafts were sealed before the first current-English extraction in this intake. Two authored parts preserve all107 and162 entries. The sectioned sealer's v2 admits exact ordered meaning/draft triples, verifies every saved draft against those triples, and preserves all source-byte, macro, earlier-unconsulted and meanings-file-before-drafts-file timestamp guards. Every source field and unpassed gate is retained. Ordinary/style/menu projections preserve original complete commands. No source material under `sources/` is edited.

The contextual review proposes104 revisions andretains165 working lines. Important findings: B247R16 remains Japanese in the current ROM and needs the extra-sailors/tavern transport instructions translated; B247/B248 omit or paraphrase away the Indian Ocean; the golden-sand story is reported by a sailor who visited the New World, not necessarily a New World native; Yuris/Plett/Jacob/Gabriel body spellings disagree with bound names; Gabriel's explicit Italian identity and Italy's Roman ruins became unsupported peninsula descriptions; several missing-person or hiding-place reports lost uncertainty. Julian refuses to return, but locating him still earns payment. Plett is captured alive and his victim's daughter decides his fate. Peralonso's rude flirtation sets up a deception without inventing romance or kinship. Preserve every amount,advance/balance distinction,share increase,puzzle answer index,figurehead branch andLuck/Charm+1 notice. Good short reactions,reward notices,humor andclear clues are retained individually.

Speaker controls identify Fernando20 throughout the B251 ruin discovery,alarm,curse concern andbodily-heaviness replies; R161's independent source note incorrectly called the speaker Lil. Actor96 is a separate Patron for B256R20/R27,not actor92 Barkeep. Fourteen precise attribution/finding-note corrections reconcile these controls while preserving the original sealed drafts and comparison file. The actual proposed dialogue and104/165 decisions are unchanged. A subsequent name-note correction removes a mistyped phonetic transcription ofTitis;v1 manuscripts andconfig remain preserved. FE inscriptions,mysterious voices andsounds have no ordinary actor nameplate andreceive no invented deity title.

Exact current bindings pass246 catalogue lookups,16 physical alternatives/16 native slots andseven captions with both menu arities. Twenty-four actors initially bind48 native name getters. The generic role-name extender reuses those exact48 results andexecutes only the missing actor151's two getters, yielding25 actors/50 getter bindings in `scoped_names_macros_reference_v2.json`. This keeps the earlier v1 proof intact. Dynamic207 resolves to captainLil2/voice3;208 currently falls back toSailor151/voice4. Eighteen source bodies use those selectors. No future conditional assignment orroster is claimed. Names retain Jacks Bloom,Julian Vermeer,Peralonso Aguirre,Yuris Huygens,Plett Perrault,Jacob Portunto,Gabriel Cardocci,Zaganos Bey andthe scoped hostesses/roles. Unconsumed Islam/Arab metadata, Nelly's still-Japanese Alexandria metadata,full catalogue UI layouts andbroader207-name review remain separate unfinished scope.

Leveque andSao Jorge are bound to exact clean/current native pointer fields andtheir approved name decisions. Fourteen inline city spans,source-geography terms andLuck/Charm terminology are checked. The source's North Sea region,Indian Ocean,Italy andForbidden City are retained asgame text,without external historical claims. Unnamed figureheads,treasures andthe king honored at the mosque are not expanded to unspoken catalogue titles. A fresh ordinary4,001-frame Lil boot onthe exact registered parent supplies current captain/route2,payload andnative getter guards,without savestate,battery,RAM/roster/conditional overrides. Only confirmation frame2000 andopening frame4000 were directly viewed;this isnot new269-event gameplay.

`formatting_v1/formatting_input.json` holds logical paragraphs andmarked runtime macros. The20 original-ABI preflight cases pass FI3/FA5/FO9/FU9 ASCII lengths with complete canaries. All10 source macro occurrences remain. The generic formatter v2 takes the expanded25-name proof explicitly without overwriting the earlier24-name evidence. Fonts,runtime,speaker controls andfull available widths are unchanged.

The first plan is deliberately not approved: `plan_v1/automatic_plans.json` has262 bodies/265 pages,zero errors,zero allocation failures andtwo weak-line-ending warnings,so its process exits1. Both warnings are the older personality's complete phrase caving in! at a sentence-ending row in B251 styles352_212/900_214. They remain unresolved andunwaived. Consider the equally faithful complete verb collapsing while preserving the older voice's We'd best retreat phrasing,or a qualified layout solution;any text change needs explicit contextual amendment andfresh formatting. Do not weaken the guard. Three two-page paragraphs also need full-width/page-density review: B247R9's expedition directions,B250R52's figurehead blessing/permission concern,andB267R12's plot/escape report. Do not shorten good prose merely to fit. The FE riddle andits directions provisionally fit one page each;native glyphs andactual FE behavior still require fresh checks.

Next resolve these layout findings,then run every changed-record native/display check anddirectly review all newly generated pages andcaptions/names using readable contact sheets. Reuse compatible earlier native characterization;do not retrace unchanged code. Follow with complete stored/reconstruction checks andrepresentative initialized tests covering the three-choice riddle,style dispatch,FE messages,page turns andnative host transitions. Keep offline versusactual/unvisited coverage explicit. No exhaustive natural playthrough orguide photos. Integrate the complete269 batch through a registered cumulative successor once its gates pass,with exact clean-input patch andown startup. No worker islive.

The registered testing ROM remains `{release['candidate_sha256']}`,726 entries/114 accepted layers/61 checks. Main stays V4701 andcanonical baseline remains unchanged. Integrated credit is24,475;all269 proposals are still within the1,423 remaining native Lil positions. The wider shared/shop/town/random/player-facing andname scope remains intact,asdo earlier unfinished contextual passes,early Rafael/tutorial priority,deferred artwork andthe later older-record technical re-audit. [Durable lossless checkpoint](../{archive_manifest.as_posix()}) preserves every current JSON/TXT part,comparison,failed/superseded record,plan andreceipt;raw ROM/RAM/captures remain local. Preserve all earlier translations,retentions,ROMs andevidence.
'''
    checkpoint(mutation=ROOT/'prose_plan_checkpoint_v1',batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0,current_batch='Lil269 B243-B282 all four prose gates pass; two layout warnings/native/visual/storage/gameplay/release pending.',
            current_batch_not_yet_integrated=True,current_batch_registered_andcredited_once=False,all_current_batch_fifth_gates_pending=True,
            proposed_revisions=104,justified_retentions=165,current_batch_evidence=evidence,no_batch_worker_live=True,guide_photos=False,
            previous_goal_turn_classification='progress',current_goal_turn_classification='progress',
            next_action='Resolve the two older-voice caving-in weak-ending diagnostics andreview three multipage paragraphs; thenfresh native/display checks for262 bodies,seven captions and25 scoped names.'),
        new_entries={'Lil_SC2_B243_B282_clean_20261110':dict(new_credit=0,source_objects=269,complete_exchanges=40,blocks=list(range(243,283)),
            source_meanings_sealed_before_current_intake=True,independent_drafts_sealed_before_current_intake=True,
            current_ordinary_bodies_bound=246,current_styles_bound=16,current_captions_bound=7,current_scoped_actors_bound=25,current_name_getters_bound=50,
            contextual_comparison_pending=False,names_terms_consumers_pending=False,first_four_individual_gates_pass=True,
            proposed_revisions=104,justified_retentions=165,all_fifth_gates_pending=True,provisional_bodies=262,provisional_pages=265,
            unresolved_plan_warnings=2,native_rendering_pending=True,direct_visual_review_pending=True,stored_checks_pending=True,
            gameplay_pending=True,registered_integration_pending=True,no_batch_worker_live=True,evidence=evidence,full_goal_complete=False)},
        summary=summary,document=document,document_text=text,completed=24475,protected=protected)
    for p,v in artifacts.items():assert digest(p)==v['source_sha256']
    print('PASS durable269 prose/provisional-plan checkpoint;zero new credit;registered candidate andfull goal preserved.')


if __name__=='__main__':main()
