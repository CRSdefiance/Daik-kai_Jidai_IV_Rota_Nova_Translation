"""Derive B51 reconstruction from the exact eight-relative B49 algorithm."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__ == '__main__':
    root = Path('work/analysis/Hodram_B51_relocation_tools_v8565')
    assert not root.exists()
    sourcepath = Path('scripts/relocate_Hodram_B49_v8398.py')
    source = sourcepath.read_text('utf-8')
    menu_build = source[source.index("    menu=packet['typed_choices'][0]"):source.index('    patches.sort')]
    menu_refs = source[source.index('    mc=dict('):source.index('    for source_version,original in')]
    menu_getters = source[source.index('    getters=choice_getters('):source.index('    assert not ctx.machines')]
    result = derive(str(sourcepath), 'scripts/relocate_Hodram_B51_v8565.py', {
        'Sparse research reconstruction of the complete B49 exchange, including its typed menu.': 'Sparse B51 research reconstruction: five speeches and eight exact native relatives; no menu.',
        'from scripts.prove_lil_B212_controls_v6603b import compile_menu\n': '',
        'from scripts.prove_lil_B212_consumers_v6595 import choice_getters\n': '',
        'scripts.Hodram_outcomes_registered_route_context_v8380': 'scripts.Hodram_B50_registered_route_context_v8546',
        'Hodram_B49_relocation_v8398': 'Hodram_B51_relocation_v8565',
        'work/analysis/Hodram_B49_choice_binding_v8387b/current_with_choices.json': 'work/analysis/Hodram_B51_current_v8559/current_effective.json',
        'translations/hodram_B49_editorial_manuscript_v2.json': 'translations/hodram_B51_editorial_manuscript_v2.json',
        'work/analysis/Hodram_B49_native_review_v8397/native_body_review.json': 'work/analysis/Hodram_B51_native_review_v8564/native_body_review.json',
        'work/analysis/Hodram_B49_source_controls_v8384/source_controls.json': 'work/analysis/Hodram_B51_source_controls_v8555/source_controls.json',
        'work/analysis/current_V8377_Hodram_native_v8380/current_native_input.json': 'work/analysis/current_V8543_Hodram_native_v8546/current_native_input.json',
        "native['reviewed_body_pages']==14": "native['reviewed_body_pages']==5",
        "len(doc['records'])==14 and len(doc['typed_choice_records'])==2": "len(doc['records'])==5 and not doc.get('typed_choice_records')",
        "doc['records']+doc['typed_choice_records']": "doc['records']+doc.get('typed_choice_records',[])",
        "g['block']==49": "g['block']==51",
        'container.blocks[49]': 'container.blocks[51]',
        'oldend==cleanend==984': 'oldend==cleanend==340',
        'len(before)==36 and len(speeches)==14': 'len(before)==20 and len(speeches)==5',
        'value[0] in [1,2,254]': 'value[0] in [1,16,18,113]',
        'block=49': 'block=51',
        menu_build: '',
        'len(patches)==15': 'len(patches)==5',
        "assert edge['block']==49": "assert edge['block']==51",
        'len(after)==36 and len(finalspeeches)==14': 'len(after)==20 and len(finalspeeches)==5',
        "        elif word==0x2100:assert br==bytes.fromhex(oldmenu['whole_command_hex']) and nr==typed\n": '',
        menu_refs: '',
        menu_getters: '',
        'SC1_B49_RESEARCH_ONLY': 'SC1_B51_RESEARCH_ONLY',
        'blocks[49]=target': 'blocks[51]=target',
        'a!=b]==[49]': 'a!=b]==[51]',
        'inverse[49]=old': 'inverse[51]=old',
        'choice_commands=[mc]': 'choice_commands=[]',
        'relocated_menu_getters=getters': 'source_query_sites=2',
        'all36_commands14_six_byte_preambles8_relatives1_query2_choices4_picture_hide_boundaries7_opaque_effects_andfull_terminal_preserved':
            'all20_commands5_six_byte_preambles8_relatives2_queries4_opaque_controls_andfull_terminal_preserved',
        'source_FE_panels=1': 'source_FE_panels=0',
        'stored_fonts_choice_UI_actual_policy_atomic_andregistered_release_pending': 'stored_fonts_actual_branch_context_policy_atomic_andregistered_release_pending',
        ',Path(compile_menu.__code__.co_filename),Path(choice_getters.__code__.co_filename)': '',
        "print('B49 reconstructed:14 speeches+2 choices,36 commands,8 relocated branches/40 cases;324 other blocks exact;both whole block inverses andparent archive exact. Parity tails:'":
            "print('B51 reconstructed:5 speeches,20 commands,8 relocated branches/40 cases;324 other blocks exact;both whole block inverses andparent archive exact. Parity tails:'",
    })
    root.mkdir(parents=True)
    save(root / 'derivation.json', dict(derivation=result, all_original_native_addresses_constants_andmultiplicity_preserved=True,
        same_exact_eight_relative_relocation_algorithm_all_command_preamble_scope_parity_end_tail_andinverse_guards_preserved=True,
        source_has_no_typed_menu_FE_picture_or_macros=True, all_five_approved_paragraphs_owned_no_other_record=True,
        no_ROM_write_registration_orcredit_by_preparer=True))
