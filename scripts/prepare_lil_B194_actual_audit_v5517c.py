"""Audit the observed default false branch without treating two skipped Julio lines as gameplay."""
from pathlib import Path
import re
from collections import Counter
from scripts.source_locked_derivation_v5118 import native_numbers
from scripts.prepare_lil_B156_layout_v3705 import derive as original_derive

def derive(a,b,changes):
    source=Path(a).read_text(encoding='utf-8')
    assert all(k in source for k in changes)
    target=re.sub('|'.join(re.escape(k) for k in sorted(changes,key=len,reverse=True)),lambda m:changes[m.group(0)],source)
    compile(target,b,'exec')
    before,after=native_numbers(source),native_numbers(target)
    assert before-after==Counter({4294967295:1,1103515245:1}) and not after-before
    result=original_derive(a,b,changes)
    assert Path(b).read_text(encoding='utf-8')==target
    return {**result,'only_removed_constants_are_B191_LCG_multiplier_and_modulus_mask':True,
        'all_native_addresses_and_other_high_constants_exact':True}

if __name__ == '__main__':
    print(derive('scripts/audit_lil_B191_actual_v5389.py', 'scripts/audit_lil_B194_actual_v5517.py', {
        'B191': 'B194', 'actual_v5389': 'actual_v5517', 'display_fixture_v5386': 'display_fixture_v5514',
        'fonts_v5374b/all13_progressive_FE_native_planes_and104_alignment_cases':
        'fonts_v5502/all11_progressive_FE_native_planes_and88_alignment_cases',
        'display_run_v5388': 'display_run_v5515', 'display_v5388': 'display_v5515',
        'source_event191_not_selected': 'source_event194_not_selected',
        'all_source38_commands_12_progressive1_FE_three_predicates16_branches_four_A000_or_no_effect_C200_end_retained':
        'all_source21_commands_10_progressive1_FE_one_availability4_branches_one_FI_resource42_two_C200_end_retained',
        "source['block']!=191": "source['block']!=194", 'original_source_block=191': 'original_source_block=194',
        "pair.get('original_source_block')==191": "pair.get('original_source_block')==194",
        "r.get('original_source_block')==191": "r.get('original_source_block')==194",
        'all47_stored_fixture_commands': 'all30_stored_fixture_commands',
        "len(fixture['all47_stored_fixture_commands'])==47": "len(fixture['all30_stored_fixture_commands'])==30",
        "                after_seed=(pair['before_seed']*0x41C64E6D+0x3039)&0xFFFFFFFF\n                roll=((after_seed>>16)&0x7FFF)%1000\n                threshold=int.from_bytes(block[cursor+4:cursor+8],'little');assert threshold in [500,700]\n                result=0 if roll<threshold else 1 if roll==threshold else 2\n                assert pair['after_seed']==after_seed and pair['result_words']==[2,result]\n                last=result;predicates.append(dict(source_offset=pair['original_source_offset'],\n                    fixture_offset=cursor,before_seed=pair['before_seed'],after_seed=after_seed,roll=roll,result=result,\n                    actual_unforced_original_LCG_transition=True,threshold=threshold))":
        "                assert block[cursor:cursor+8].hex()=='0080ffff06fe0030'\n                result=pair['result_words'][1];assert result==0 and pair['result_words']==[2,result]\n                assert pair['before_seed']==pair['after_seed']\n                last=result;predicates.append(dict(source_offset=pair['original_source_offset'],fixture_offset=cursor,\n                    before_seed=pair['before_seed'],after_seed=pair['after_seed'],result=result,\n                    actual_unforced_original_actor6_availability=True,no_RNG_advance_at_this_predicate=True))",
        "selected[-1]['original_source_offset']==730": "selected[-1]['original_source_offset']==536",
        '==13': '==9', '=13': '=9',
        "[r['id'] for r in fixture['original_text_records']]": "[r['id'] for r in fixture['original_text_records'] if r['source_selector']!=6]",
        "len(predicates)==2 and predicates[0]['source_offset']==8 and predicates[1]['source_offset'] in [28,76]":
        "len(predicates)==1 and predicates[0]['source_offset']==312 and predicates[0]['result']==0",
        'len(effect_offsets) in [0,1] and all(at in [48,60,96,108] for at in effect_offsets)':
        'effect_offsets==[8]',
        "ui[0]['original_source_offset']==728": "ui[0]['original_source_offset']==534",
        'single_source_end730': 'single_source_end536',
        'original_RNG_and_per_path_native_checks': 'original_availability_and_per_path_native_checks',
        'actual_all13_progressive_FE_RNG_effect_or_no_effect_C200_and_single_end':
        'actual_selected9_progressive_FE_availability0_A000_C200_and_single_end',
        'offline_only_display_IDs=[]': "offline_only_display_IDs=[r['id'] for r in font['cases'] if r['id'] not in {p['id'] for p in actual}]",
        'all38_source_commands': 'all21_source_commands',
        'all13_speeches12_progressive1_impersonal_FE_observed': 'all9_selected_speeches8_progressive1_impersonal_FE_observed',
        'observed_random_path_difference': 'observed_availability_path_comparison',
        'original_selected_effect_or_no_effect_C200': 'original_selected_A000_common_C200',
    }))
