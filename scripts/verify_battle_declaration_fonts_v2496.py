"""Current-ROM native expansion and full-canvas proof for22 confirmation/ready paragraphs."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
OLD=Path('scripts/probe_battle_declaration_fonts_v995b.py')
if __name__=='__main__':
 source=OLD.read_text();changes={
 "ROOT = Path('work/analysis/battle_declaration_v995b')":"ROOT = Path('work/analysis/battle_declaration_fonts_v2496')",
 "ROM = Path('out/all_routes_combined_v987_candidate.nds')":"ROM = Path('out/all_routes_combined_v2284_candidate.nds')",
 "MANUSCRIPT = Path('translations/battle_declaration_editorial_manuscript_v2.json')":"MANUSCRIPT = Path('translations/battle_declaration_contextual_editorial_manuscript_v1.json')\nfrom dk4tool.patch.refit_contextual_spritsail_v1 import current_entries\nfrom scripts.probe_common_single_cache_v862 import Loader\nfrom scripts.battle_declaration_layout_v996 import compiled as compile_paragraph",
 "arm = ARM.read_bytes()\n    assert sha(arm) == runtime['research_ARM9_sha256']":"rom=NdsImage.open(ROM);arm=rom.read_file('/__arm9__.bin');common=rom.read_file('/COMMON/MESFILE.DK4');entries=current_entries(common,arm)",
 "assert sha(ROM.read_bytes()) == doc['current_ROM_sha256'] == runtime['candidate_sha256']":"assert sha(ROM.read_bytes())==doc['current_ROM_sha256'];assert sha(arm)==doc['current_ARM9_sha256']",
 "compiled = b' '+row['english'].encode('ascii')":"compiled=compile_paragraph(row);assert compiled==entries[n].text==bytes.fromhex(row['current_hex'])",
 'for page in range(2):':'for page in range(8):',
 'selected = representative[page*11:(page+1)*11]':'selected = cases[page*24:(page+1)*24]',
 "(936, 912)":"(1404,1216)",
 'index % 2*468, index // 2*152':'index % 3*468, index // 3*152',
 "save(ROOT/'native_font_proof.json', {":"loader=Loader(arm,common);copies=[loader.copy(n,entries[n].text,mode)for mode in('cold','warm')for n in range(1889,1911)];assert len(copies)==44\n    save(ROOT/'native_font_proof.json', {'ARM9_sha256':sha(arm),'COMMON_sha256':sha(common),'all44_native_cold_warm_copies':copies,'native_file_IO_explicit_host_contract':True,'all22_complete_native_cases':[dict(message_ID=c['message_id'],**c)for c in representative],'complete_native_font_cases':176,'all22_source_numeric_selection_complete_ABI_words_and_visible_ink_pass':True,'current_modal_font_consumers_no_Deck_parent_projection_claim':True,'current_parent_projection_controls':0,'current_parent_projection_is_shared_ordinary_control_not_current_battle_GPU':False,",
 "'research_ARM9': str(ARM), 'research_ARM9_sha256': sha(arm)":"'current_ARM9_from_registered_ROM':True",
 "'runtime_proof': str(RUNTIME), 'runtime_proof_sha256': sha(RUNTIME.read_bytes())":"'historical_runtime_matrix_context_only':str(RUNTIME),'historical_runtime_matrix_sha256':sha(RUNTIME.read_bytes()),'current176_native_expansion_font_cases_executed_afresh':True",
 }
 for a,b in changes.items():assert a in source,a;source=source.replace(a,b)
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
 save('work/analysis/battle_declaration_fonts_v2496/producer_binding.json',dict(original=str(OLD),original_sha256=sha(OLD.read_bytes()),effective_source_sha256=sha(source.encode()),current_ARM9_used_no_research_patch_or_historical_matrix_rerun=True,full_goal_complete=False))
