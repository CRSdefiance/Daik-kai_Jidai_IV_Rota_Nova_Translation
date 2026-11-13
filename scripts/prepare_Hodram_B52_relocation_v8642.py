"""Source-lock sparse B52 speech/menu reconstruction while preserving both original end words."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B52_relocation_tools_v8642');assert not root.exists()
    result=derive('scripts/relocate_Hodram_B49_v8398.py','scripts/relocate_Hodram_B52_v8642.py',{
        'scripts.Hodram_outcomes_registered_route_context_v8380':'scripts.Hodram_B51_registered_route_context_v8612',
        'Hodram_B49_relocation_v8398':'Hodram_B52_relocation_v8642',
        'work/analysis/Hodram_B49_choice_binding_v8387b/current_with_choices.json':'work/analysis/Hodram_B52_current_v8631/current_effective.json',
        'hodram_B49_editorial_manuscript_v2':'hodram_B52_editorial_manuscript_v3',
        'work/analysis/Hodram_B49_native_review_v8397/native_body_review.json':'work/analysis/Hodram_B52_native_note_v8638/qualified_native_review.json',
        'Hodram_B49_source_controls_v8384':'Hodram_B52_source_controls_v8620','current_V8377_Hodram_native_v8380':'current_V8609_Hodram_native_v8612',
        "native['manuscript_sha256']==sha(DOC.read_bytes()) and native['reviewed_body_pages']==14":"native['manuscript_sha256']==sha(DOC.read_bytes()) and native['all_words_compiled_bytes_source_current_refs_individual_review_gates_native_planes_choice_geometry_andactual_scope_unchanged'] and sha(Path(native['prior_native_review']).read_bytes())==native['prior_native_review_sha256'] and read(native['prior_native_review'])['reviewed_body_pages']==3",
        "len(doc['records'])==14":"len(doc['records'])==3",
        "g['block']==49":"g['block']==52",'container.blocks[49]':'container.blocks[52]','oldend==cleanend==984':'oldend==cleanend==228',
        'len(before)==36 and len(speeches)==14':'len(before)==14 and len(speeches)==3',
        'value[0] in [1,2,254]':'value[0] in [113]','block=49':'block=52',
        "at==jamenu['offset']==574 and len(previous)==len(source)==26 and len(typed)==22":"at==jamenu['offset']==68 and len(previous)==len(source)==36 and len(typed)==32",
        'old[at:at+26]':'old[at:at+36]','clean[at:at+26]':'clean[at:at+36]','B49-complete-native-menu':'B52-complete-native-menu','end=at+26':'end=at+36',
        'len(patches)==15':'len(patches)==4',"edge['block']==49":"edge['block']==52",'len(fixups)==8':'len(fixups)==4',
        'len(after)==36 and len(finalspeeches)==14':'len(after)==14 and len(finalspeeches)==3',
        'old_length=26':'old_length=36','new_length=22':'new_length=32',
        'SC1_B49_RESEARCH_ONLY':'SC1_B52_RESEARCH_ONLY','blocks[49]=target':'blocks[52]=target','if a!=b]==[49]':'if a!=b]==[52]','inverse[49]=old':'inverse[52]=old',
        'source_relative_sites=8':'source_relative_sites=4','all36_commands14_six_byte_preambles8_relatives1_query2_choices4_picture_hide_boundaries7_opaque_effects_andfull_terminal_preserved':'all14_commands3_six_byte_preambles4_relatives_zeroqueries2_choices4_opaque_controls_andboth_distinct_terminals_preserved','source_FE_panels=1':'source_FE_panels=0',
        'Sparse research reconstruction of the complete B49 exchange':'Sparse research reconstruction of the complete B52 exchange',
        'B49 reconstructed:14 speeches+2 choices,36 commands,8 relocated branches/40 cases':'B52 reconstructed:3 speeches+2 choices,14 commands,4 relocated branches/20 cases',
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(tool=result,all_native_high_integer_constants_andmultiplicity_preserved=True,all_source_current_preambles_typedcount_order_relative_targets_opaque_controls_bothendwords_andfull_block_archive_inverses_required=True,manuscriptv3_qualified_native_note_andoriginal_review_bound=True,no_ROM_registry_orcredit_change=True,new_credit=0,full_goal_complete=False))
