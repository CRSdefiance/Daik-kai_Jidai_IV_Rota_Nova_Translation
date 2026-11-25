"""Prepare lossless B180 actual/reference checkpoint with truthful unequal outcomes."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save
from scripts.prepare_lil_B180_checkpoint_v4806 import NEXT as PRIOR_NEXT,EVIDENCE as PRIOR_EVIDENCE

ROOT=Path('work/analysis/lil_B180_checkpoint_tools_v4817')
NEXT=(
    'Continue B180 from sealed manuscriptv4,mapv1 and reference approval4816. Source/prose, '
    'current-font native planes,stored alignment,relocation,whole loaders,entry census, '
    'ends,relocated controls and representative actual checks pass;do not repeat them '
    'without a concrete new risk. Implement the source-locked atomic compiler for '
    '28 commands,11 speeches,seven exact leaves,ten adjusted relative sites,two original '
    'threshold500 RNG predicates,three A000 alternatives,C200 and one end. Preserve '
    'source576 to target548 stored/546 logical and end572 to542. Use current B180 '
    'formatter/profile and fresh source locks;do not inherit B179 linear/no-C200 or '
    'equal-random-outcome assertions. The actual runs select original effects504 and472 '
    'with different legitimate random results;four focus runs account for the final '
    'one-byte town difference. Keep all recorded timings,PRNG inequality and indicator '
    'differences disclosed. Add meaningful atomic negatives,register after the complete '
    'V4766 stack and build through the sole registered builder. Verify the exact '
    'clean-input patch and current startup,then credit11 objects once. B180 remains '
    'uncredited now;do not use a research fixture as a parent or natural activation claim. '+
    PRIOR_NEXT[PRIOR_NEXT.index('Keep all other storylines,'):])
SUMMARY=(
    'V4817 seals B180 representative actual and source-reference approval. Paired '
    'Japanese/English content cold boots retain every28 source commands plus the nine '
    'original B22 initializers:37 stored commands,ten relative sites,two500 predicates, '
    'three alternative A000s,C200 and one end. The fixture selects content through B22, '
    'not natural event180 eligibility. All11 English panels match independent current-font '
    'native planes,with complete leading/internal/final glyphs,bounds and single-page '
    'consumption. Both actual sheets and36 full screens on nine paired sheets were '
    'viewed. Lady166/Lady167 portraits and nameplates remain distinct;the impersonal '
    'Scents forecast clears them. No source-supported gender,rank,relationship or prior '
    'scene location is invented. Lisbon appears in the forecast;the initialized fixture '
    'background is Amsterdam. Five revisions/six justified retentions remain unchanged.\n\n'
    'The original random paths differ legitimately. Japanese reaches effect504 after '
    'two draws946/result2 and38/result0;English reaches effect472 after one draw38/result0. '
    'All actual predicate seed transitions match the original LCG and bounded1000 '
    'threshold500 logic. Type3 branch commands preserve the prior result value;the '
    'stopped initial zero-value assumption is corrected. Source/English actual C200 '
    'requests both reach[1,2,13,0,2,0,1],pending1,after source UI resource bodies advance '
    'fields4/5;the isolated CPU request before those bodies was[1,2,13,0,0,0,1]. '
    'The source and English conditional paths select31 and27 commands respectively, '
    'all11 speeches and the original end,returning normally at5495/5496. No alternative '
    'is omitted from stored source or forced in the emulator.\n\n'
    'All115 sampled upper/portrait/name regions agree. Twelve measured common-command '
    'timing differences comprise eight speeches and four controls/end. Twelve following '
    'full-RGB differences are confined to the viewed original A-indicator box;the final '
    '9001-frame RGB agrees. Four of five final component groups and the complete1A04 '
    'actor model/captain2 agree;PRNG seeds differ2467799992/790984746. A concrete unequal '
    'town-state finding prompted two focused6001-frame cold boots. Their common command '
    'boundaries reproduce the first runs exactly,including all WRAM hashes,with only '
    'local artifact paths normalized after byte-hash validation. Read-only effect exports '
    'show identical pre-effect actor/town/item/goods arrays. Original effect504 writes '
    'town11 field102 from125 to315;effect472 writes it to317. At9001 the sole difference '
    'within all four arrays is that exact low byte59/61 at town-array1294. Actor,item '
    'and goods arrays stay exact. The risk is source-effect bound;no market/plot semantics, '
    'full-WRAM write ownership,future-world equality or forced RNG is claimed.\n\n'
    'Four actual cold boots total30004 frames. Two new content research ROMs are pinned; '
    'all older ROMs and translations remain. Manuscriptv4 and the independently reversible '
    'mapv1 are sealed for registered integration. No editorial credit or playable release '
    'is added. Coverage remains5912 contextual,5915 source/prose,3748 integrated revisions, '
    '2164 retentions and route4313/4313;B180 has11 approved uncredited objects. V4766 '
    'remains561 entries/114 accepted layers with its exact clean-input patch;mainV4701 '
    'is unchanged. Every storyline,shared town/shop dialogue,random scene,Help,player '
    'prose and earlier premature-wrapping review remains in scope. Graphics and later '
    'older-record technical re-audit stay separate and open. Full goal active.\n\n'+NEXT)
EVIDENCE=PRIOR_EVIDENCE+[
    'work/analysis/lil_B180_display_fixture_v4808/complete_B180_B22_fixtures.json',
    'work/analysis/lil_B180_display_tools_v4809/runner_and_pin_receipt.json',
    'work/analysis/lil_B180_actual_v4811c/actual_all11_progressive_FE_RNG_effect_C200_and_single_end.json',
    'work/analysis/lil_B180_actual_review_v4812/all2_actual_sheets11_planes_fullscreens_and_resolved_effect_state.json',
    'work/analysis/lil_B180_effect_focus_v4814b/two_actual_original_effects_and_exact_one_byte_final_town_difference.json',
    'work/analysis/lil_B180_reference_approval_v4816/approval_receipt.json',
    'translations/lil_B180_editorial_relocation_map_v1.json']

if __name__=='__main__':
    assert not ROOT.exists()
    original=Path('scripts/checkpoint_lil_B180_native_v4796.py').read_text(encoding='utf-8')
    a=original.index('NEXT=(');b=original.index("if __name__=='__main__':",a)
    tools=[derive('scripts/checkpoint_lil_B180_native_v4796.py','scripts/checkpoint_lil_B180_references_v4817.py',{
        original[a:b]:'NEXT='+repr(NEXT)+'\n\nSUMMARY='+repr(SUMMARY)+'\n\n',
        'lil_B180_native_checkpoint_v4796':'lil_B180_reference_checkpoint_v4817',
        'lil_B180_contextual_native_v4796':'lil_B180_contextual_references_v4817',
        'previous_latest_checkpoint_before_B180_native_v4796':'previous_latest_checkpoint_before_B180_references_v4817',
        'lil_B180_editorial_manuscript_v3':'lil_B180_editorial_manuscript_v4',
        'work/analysis/lil_B180_native_approval_v4795/all11_source_prose_current_native_approval.json':
        'work/analysis/lil_B180_reference_approval_v4816/approval_receipt.json',
        "assert approval['manuscript_sha256']==sha(MANUSCRIPT.read_bytes())":"assert approval['manuscripts'][str(MANUSCRIPT)]==sha(MANUSCRIPT.read_bytes())",
        '## V4796: B180 contextual and current-font native pass':'## V4817: B180 actual scenes and sealed references',
        '# Current editorial handoff - V4796':'# Current editorial handoff - V4817',
        "Path(__file__)]}":"Path(__file__),*map(Path,"+repr(EVIDENCE)+")]}",
        'relocation_actual_and_registered_release_pending=True,new_emulator_runs=0,new_ROMs=0':
        'relocation_actual_and_references_approved=True,registered_release_pending=True,new_emulator_runs=4,new_ROMs=2',
        'Stage a lossless current-font B180 source/prose/native checkpoint, zero credit.':
        'Stage a lossless B180 actual/reference checkpoint, zero credit.'})]
    tools.append(derive('scripts/verify_editorial_handoff_v4797.py','scripts/verify_editorial_handoff_v4818.py',{
        'lil_B180_native_checkpoint_v4796':'lil_B180_reference_checkpoint_v4817',
        'editorial_handoff_verification_v4797':'editorial_handoff_verification_v4818',
        'previous_latest_checkpoint_before_B180_native_v4796':'previous_latest_checkpoint_before_B180_references_v4817',
        'no_new_ROM_or_emulator_or_completion_credit=True':'no_new_registered_ROM_or_completion_credit=True,new_research_ROMs=2,new_emulator_runs=4',
        '    ROOT.mkdir(parents=True)':'    from scripts.verify_lil_B180_checkpoint_v4818 import audit_actual\n    audit_actual(new[key])\n    ROOT.mkdir(parents=True)'}))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_checkpoint_tools.json',dict(tools=tools,evidence=EVIDENCE,full_goal_complete=False))
    print('Prepared lossless B180 actual/reference checkpoint and independent audit.')
