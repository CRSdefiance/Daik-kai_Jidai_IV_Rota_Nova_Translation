"""Derive source-qualified B50 stored-control checks using its own current Hodram context."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B50_controls_production_tools_v8529');assert not root.exists()
    path=Path('dk4tool/patch/hodram_B49_controls_v3.py');source=path.read_text(encoding='utf-8')
    a=source.index("    for key in ['source_owned_entry_adapter'");b=source.index("    trusted_adapter('dispatch'",a)
    c=source.index("    sk=dict(native_skip.__globals__)");d=source.index("    events=source['source_event_records']",c)
    tools=[derive(str(path),'dk4tool/patch/hodram_B50_controls_v1.py',{
        'hodram_B49_native_guards_v1':'hodram_B50_native_guards_v1',
        'scripts.Hodram_outcomes_registered_route_context_v8380':'scripts.Hodram_B49_registered_route_context_v8478',
        'Hodram_B49_controls_v8401d':'Hodram_B50_controls_v8497',
        'Hodram_B49_relocation_v8398':'Hodram_B50_relocation_v8495',
        'work/analysis/Hodram_B49_choice_binding_v8387b/current_with_choices.json':'work/analysis/Hodram_B50_current_v8488/current_effective.json',
        'Hodram_B49_source_controls_v8384':'Hodram_B50_source_controls_v8486',
        'Hodram_B49_source_display_v8386b':'Hodram_B50_source_display_v8487',
        'Hodram_B49_stored_v8399':'Hodram_B50_stored_v8496',
        'current_V8377_Hodram_native_v8380':'current_V8475_Hodram_native_v8478',
        source[a:b]:"    require(source['source_owned_EV1_entry_adapter']==trusted['source_owned_EV1_entry_adapter'],'exact trusted original EV1 entry adapter')\n",
        "source['source_owned_entry_adapter']":"source['source_owned_EV1_entry_adapter']",
        source[c:d]:'',
        '[(48,48,[]),(49,49,[48])]':'[(50,50,[49])]',
        'original EV1 getter fields for prerequisite48/event49':'original EV1 getter fields for event50/prerequisite49',
        "    branches=[];byoffset=":"    require(not g['relative_fixups'] and not g['relocated_skip_cases'] and not any(c['word'] in [0x100,0x200,0x300,0x400,0x2100,0x8000,0x8100] for c in g['all_target_commands']),'source B50 has no relative/query/menu sites')\n    branches=[];byoffset=",
        "source['paired_opaque_structural_decodes']":"source['groups'][0]['isolated_original_structural_pairs']",
        "len(opaque)==7,'all seven original opaque effects'":"len(opaque)==6,'all six original opaque effects'",
        'len(dispatches)==14':'len(dispatches)==3',
        'len(queries)==1 and len(pictures)==4 and len(controls)==13':'len(queries)==0 and len(pictures)==2 and len(controls)==9',
        '[0x4820,0x4700,0x4800,0x4700]':'[0x4800,0x4700]',
        "len(g['relative_fixups'])==8 and sum(len(r['cases']) for r in g['relocated_skip_cases'])==40":"not g['relative_fixups'] and not queries",
        'Hodram-B49-controls-':'Hodram-B50-controls-',
    })]
    tools.append(derive('scripts/validate_Hodram_B49_controls_v8441b.py','scripts/validate_Hodram_B50_controls_v8530.py',{
        'hodram_B49_controls_v3':'hodram_B50_controls_v1',
        'hodram_B49_reconstruction_v2':'hodram_B50_reconstruction_v1',
        'from dk4tool.dialogue.hodram_B49_choices_v2 import compile_choices\n':'',
        'hodram_B49_native_evidence_v1':'hodram_B50_native_evidence_v1',
        'validate_Hodram_B49_native_v8433':'validate_Hodram_B50_native_v8520',
        'Hodram_B49_independent_controls_v8441b':'Hodram_B50_independent_controls_v8530',
        'work/analysis/Hodram_B49_relocation_v8398/reconstruction.json':'work/analysis/Hodram_B50_references_v8503/source_current_final_map.json',
        'work/analysis/Hodram_B49_choice_binding_v8387b/current_with_choices.json':'work/analysis/Hodram_B50_current_v8488/current_effective.json',
        'Hodram_B49_source_controls_v8384':'Hodram_B50_source_controls_v8486',
        'Hodram_B49_controls_v8401d':'Hodram_B50_controls_v8497',
        'translations/hodram_B49_editorial_manuscript_v4.json':'translations/hodram_B50_editorial_manuscript_v5.json',
        '.blocks[49]':'.blocks[50]',
        "data['source_controls']['operands_requiring_adjustment_when_resizing'],doc['typed_choice_records'],compile_choices(doc['typed_choice_records'])":"[]",
        'Independent B49 controls:14dispatches/nullFE/8branches40cases/1rawquery/4picture-hide/25normalends/2EV1getters/7pairedopaque decodes;no emulator replay orcredit.':'Independent B50 controls:3dispatches/nullFE/no branch-query-menu/2picture-hide/25normalends/1EV1getter/6pairedopaque decodes;no emulator replay orcredit.',
        'freshly rebuilt B49':'freshly rebuilt B50',
    }))
    root.mkdir(parents=True);save(root/'derivations.json',dict(tools=tools,all_native_high_integer_constants_andmultiplicity_preserved=True,own_V8475_Hodram_captain1_context_only=True,all_original_dispatch_macro_actor_voice_FE_picture_descriptor_layout_hide_pointer_delta_25_end_carries_EV1_andopaque_decoder_guards_preserved=True,no_emulator_replay_ROM_orcredit_change=True,new_credit=0,full_goal_complete=False))
