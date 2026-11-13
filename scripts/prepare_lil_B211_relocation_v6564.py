"""Prepare a twelve-speech research relocation with normalized command aliases and full640-byte inverse."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B211_relocation_tools_v6564')
if __name__=='__main__':
    assert not ROOT.exists();proof=derive('scripts/research_lil_B210_relocation_v6513.py','scripts/research_lil_B211_relocation_v6564.py',{
        'lil_B210_source_v6498/ten_clean_current_complete_exchange_source_references.json':'lil_B211_source_v6550c/twelve_clean_current_complete_exchange_source_references.json',
        'lil_B210_research_fonts_v6508/all10_bodies10_complete_native_pages_and80_alignments_RESEARCH.json':'lil_B211_research_fonts_v6560/all12_bodies12_complete_native_pages_and96_alignments_RESEARCH.json',
        'lil_B210_source_native_view_v6512/ten_source_objects39_body_name_holds_ten_English_native_pages_and_name_literals_viewed.json':'lil_B211_source_native_view_v6563/twelve_source_objects_twelve_English_native_pages_names_and_scope_viewed.json',
        'B210':'B211','relocation_research_v6513':'relocation_research_v6564','relocation_v6513':'relocation_v6564','blocks[210]':'blocks[211]','block=210':'block=211','newbank[210]':'newbank[211]','==[210]':'==[211]','SC2_block210':'SC2_block211',
        '688':'640','686':'640','682':'636','678':'632','block[640:]==bytes(2)':'block[640:]==bytes(0)',
        'len(commands)==12 and len(speeches)==10':'len(commands)==14 and len(speeches)==12','len(patches)==10':'len(patches)==12','len(newcommands)==12 and len(newspoken)==10':'len(newcommands)==14 and len(newspoken)==12',
        'ten_speech_relocation':'twelve_speech_relocation','source_tail_bytes=2':'source_tail_bytes=0','all12_commands10_preambles':'all14_commands12_preambles','all10_manuscript':'all12_manuscript','commands=12,preambles=10':'commands=14,preambles=12',
        'name_asset_unchanged_and_full_catalogue_typography_correction_separate':'name_assets_unchanged_full207_name_queue_open',
        'mapped_native_commands=maps':'mapped_native_commands=maps,command_map=[dict(word=c[\'word\'],old_offset=c[\'old_offset\'],new_offset=c[\'new_offset\'],old_extent=c[\'old_native_extent\'],new_extent=c[\'new_native_extent\']) for c in maps],target_native_skip_cases=[]',
    });ROOT.mkdir(parents=True);save(ROOT/'source_locked_relocation_tool.json',dict(proof=proof,no_native_constants_or_preambles_changed=True,full_goal_complete=False))
