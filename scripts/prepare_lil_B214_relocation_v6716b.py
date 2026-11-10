"""Derive the full ten-speech/seven-voice-body inverse, retaining all1316 original bytes."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B214_relocation_tools_v6716')
if __name__=='__main__':
    assert not ROOT.exists()
    proof=derive('scripts/research_lil_B209_relocation_v6466.py','scripts/research_lil_B214_relocation_v6716.py',{
        'B209':'B214','block209':'block214','block=209':'block=214','[209]':'[214]','newbank[209]':'newbank[214]',
        'relocation_research_v6466':'relocation_v6716','nested20_object':'all17_object',
        'source_v6450d/all20_clean_current_letter_and_voice_alternative_context':'source_v6697/all17_clean_current_letter_notices_reactions_full1316_inverse',
        'research_fonts_v6463/all20_bodies22_complete_native_pages_and160_alignments_RESEARCH':'native_pages_v6706/all17_complete_single_pages136_native_alignments',
        'controls_v6460/two_predicates40_relative_cases10_staging_structural_cases_and10_complete_ends':'controls_v6708/four_unforced_predicates_ten_structural_cases50_seeded_ends_four_route_models',
        'native_view_v6465/all22_native_pages_four_names_and_source_masks_viewed_actual_paging_pending':'view_v6711/seventeen_native_pages_eleven_names_nine_source_panels_and_scope_viewed',
        'len(old_commands)==18 and len(old_speeches)==5 and len(block)==1148 and block[1144:]==bytes(4)':'len(old_commands)==27 and len(old_speeches)==10 and len(block)==1316 and block[1310:]==bytes(6)',
        'len(patches)==7':'len(patches)==11','block[last:1148]':'block[last:1314]','mapped(1148)':'mapped(1314)',
        "for edge in control['four_relative_edges']:":"for original_edge in read(control['eight_relative_sites80_native_cases'])['operands_requiring_adjustment_when_resizing']:\n        edge=dict(offset=original_edge['offset'],word=original_edge['word'],span=original_edge['matched_skip_target']-original_edge['offset']-4,fallthrough=original_edge['unmatched_next_offset'],skip_target=original_edge['matched_skip_target'])",
        'len(commands)==18 and len(speeches)==5':'len(commands)==27 and len(speeches)==10',
        "struct.pack_into('<H',inverse,4,1140)":"struct.pack_into('<H',inverse,4,1306)",
        'assert inverse==block':'assert bytes(inverse)+block[1314:]==block','mapped(1144)':'mapped(1310)',
        'source_logical_end=1148':'source_logical_end=1314','source_tail_bytes=0':'source_tail_bytes=2',
        'all18_commands5_preambles15_bodies16_slots_and_aliases_preserved':'all27_commands10_preambles7_bodies8_slots_and_aliases_preserved',
        'inverse_recovers_every_original1148_byte':'inverse_recovers_every_original1316_byte',
        'source_offset=1144':'source_offset=1310','source=1148':'source=1316','speech_objects=5':'speech_objects=10','stored_style_bodies=15':'stored_style_bodies=7','inverse_all1148':'inverse_all1316'
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_full_inverse_relocation.json',dict(derivation=proof,all1316_bytes_including_tail2_inverse_required=True,all27_commands_ten_preambles_seven_bodies_eight_alias_slots_preserved=True,eight_relative_sites_two_predicates_letter_staging_A000_normal_end=True,all_native_numeric_constants_preserved=True,new_ROM_or_credit=False,full_goal_complete=False))
