"""Prepare the lossless relocation checkpoint without changing editorial credit."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save
from scripts.checkpoint_lil_B180_native_v4796 import NEXT as PRIOR_NEXT

ROOT=Path('work/analysis/lil_B180_checkpoint_tools_v4806')
NEXT=(
    'B180 relocation,stored native planes,whole-block loaders,external entry census,guarded '
    'ends and relocated control checks now pass. Do not repeat them without a concrete risk. '
    'Continue with paired disclosed Japanese/English B180 content cold boots retaining all28 '
    'source commands plus original B22 initialization. There are ten relative sites,two '
    'original500 predicates,three alternative A000 leaves,one C200 and one end;do not flatten '
    'the conditional paths or require every alternative to execute in one run. Observe all11 '
    'speeches,actual selected effect,predicate order and original RNG seed transitions,C200 '
    'context and normal parent return. Never force emulator RNG or import CPU-only seeds. '
    'Native FE geometry/current-font offline evidence does not replace actual current-font '
    'FE gameplay. Research ROM4801 is not a registered release or new build parent. After '
    'necessary actual checks,register the atomic compiler following the complete V4766 '
    'stack,verify the clean-input patch and current startup,then credit the11 objects once. '
    'Five revisions/six justified retentions remain uncredited. '+
    PRIOR_NEXT[PRIOR_NEXT.index('Keep all other storylines,'):])
SUMMARY=(
    'V4806 completes the B180 offline relocation and research gates. All28 commands,11 '
    'complete preambles and ten relative span fields map reversibly from576 source bytes '
    'to548 stored/546 logical bytes;inverse restoration recovers every original logical '
    'byte and all335 other SC2 blocks remain exact. All11 final stored native text planes '
    'equal the reviewed current-font planes across44 alignment cases:20 fresh and24 '
    'exact-proof reuses. Both predicates remain four-byte aligned. No prose,manual break, '
    'font,metric,shared guard or executable change is added.\n\n'
    'A pinned one-block research ROM4801 differs from complete V4766 only in SC2 block180; '
    'every other file and component remains exact. Fresh current/research checks pass672 '
    'whole-block loads/cache hits and1344 parent modes. Three shipped entry censuses,all28 '
    'mapped commands and50 target native branch cases pass. Original tail decodes at572 '
    'and542 return type0/extent4 with poisoned unread post-payload guards. Eleven relocated '
    'dispatches,seven exact leaves,two unforced snapshot RNG predicate pairs,three opaque '
    'A000 structural pairs,the source fleet-derived C200 request and25 mapped hypothetical '
    'paths pass. Every path preserves all11 speeches,one alternative effect,C200 and the '
    'single end. These CPU checks do not execute opaque effect bodies or prove actual '
    'scene outcomes,parent return or earned eligibility. Preserve stopped4800 and corrected '
    '4800b/4800c preparation provenance.\n\n'
    'There is one new research ROM and zero new emulator runs or editorial credit. '
    'Completed contextual5912,source/prose5915,integrated revisions3748,retentions2164 and '
    'route4313/4313 remain unchanged. B180 retains11 approved uncredited objects,5 revisions '
    'and6 justified retentions. Registered V4766 remains561 entries/114 accepted layers '
    'with its exact clean-input patch;promoted main V4701 remains unchanged. Premature '
    'wrapping review includes earlier retained translations across every storyline,shared '
    'town/shop exchange,random scene,Help and player prose. COMMON657 is fixed;other '
    'comparison leads are pending contextual and consumer review. Preserve every ROM, '
    'translation,draft,producer,proof,failure and nested ledger history. Graphics and the '
    'later older-record technical re-audit remain separate and open. Full goal active.\n\n'+NEXT)

EVIDENCE=[
    'work/analysis/lil_B180_relocation_v4798/nested_source_relocation_research.json',
    'work/analysis/lil_B180_stored_v4799/all11_final_stored_targets44_macro_cases_and_complete_planes.json',
    'work/analysis/lil_B180_research_tools_v4800b/exact_key_correction.json',
    'work/analysis/lil_B180_research_tools_v4800/prepared_tools.json',
    'work/analysis/lil_B180_research_v4801/research_image_receipt.json',
    'work/analysis/lil_B180_loader_v4802/whole_SC2_and_B180_initial_entry_proof.json',
    'work/analysis/lil_B180_reference_census_v4803/all28_commands_ten_relative_sites_and_shipped_entry_census.json',
    'work/analysis/lil_B180_ends_v4804/two_declared_tail_end_decodes_ten_relative_sites.json',
    'work/analysis/lil_B180_relocated_controls_v4805/all11_dispatches_two_RNG_predicates_three_effects_C200_and25_mapped_paths.json']

if __name__=='__main__':
    assert not ROOT.exists()
    original=Path('scripts/checkpoint_lil_B180_native_v4796.py').read_text(encoding='utf-8')
    start=original.index('NEXT=(');end=original.index("if __name__=='__main__':",start)
    new_constants='NEXT='+repr(NEXT)+'\n\nSUMMARY='+repr(SUMMARY)+'\n\n'
    tools=[derive('scripts/checkpoint_lil_B180_native_v4796.py','scripts/checkpoint_lil_B180_relocation_v4806.py',{
        original[start:end]:new_constants,
        'lil_B180_native_checkpoint_v4796':'lil_B180_relocation_checkpoint_v4806',
        'lil_B180_contextual_native_v4796':'lil_B180_contextual_relocation_v4806',
        'previous_latest_checkpoint_before_B180_native_v4796':'previous_latest_checkpoint_before_B180_relocation_v4806',
        '## V4796: B180 contextual and current-font native pass':'## V4806: B180 stored relocation and research gates',
        '# Current editorial handoff - V4796':'# Current editorial handoff - V4806',
        "Path(__file__)]}":"Path(__file__),*map(Path,"+repr(EVIDENCE)+")]}",
        'relocation_actual_and_registered_release_pending=True,new_emulator_runs=0,new_ROMs=0':
        'relocation_and_stored_offline_checks_complete=True,actual_and_registered_release_pending=True,new_emulator_runs=0,new_ROMs=1',
        'Stage a lossless current-font B180 source/prose/native checkpoint, zero credit.':
        'Stage the lossless B180 relocation/research checkpoint, zero credit.'})]
    tools.append(derive('scripts/verify_editorial_handoff_v4797.py','scripts/verify_editorial_handoff_v4807.py',{
        'lil_B180_native_checkpoint_v4796':'lil_B180_relocation_checkpoint_v4806',
        'editorial_handoff_verification_v4797':'editorial_handoff_verification_v4807',
        'previous_latest_checkpoint_before_B180_native_v4796':'previous_latest_checkpoint_before_B180_relocation_v4806',
        'no_new_ROM_or_emulator_or_completion_credit=True':'no_new_registered_ROM_or_emulator_or_completion_credit=True,new_research_ROMs=1',
        '    ROOT.mkdir(parents=True)':'    from scripts.verify_lil_B180_checkpoint_v4807 import audit_relocation\n    audit_relocation(new[key])\n    ROOT.mkdir(parents=True)'}))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_checkpoint_tools.json',dict(tools=tools,evidence=EVIDENCE,full_goal_complete=False))
    print('Prepared lossless B180 relocation checkpoint and independent audit;shared metadata untouched.')
