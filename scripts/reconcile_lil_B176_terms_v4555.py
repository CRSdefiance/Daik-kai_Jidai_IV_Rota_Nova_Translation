"""Bind Owner/Cook, the live Seville pointer and prospective banana-fad wording."""
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B176_terms_v4555')
SOURCE=Path('work/analysis/lil_B176_source_v4548/all10_clean_current_complete_context.json')
NAMES=Path('work/analysis/lil_B176_names_v4553/four_original_Owner_Cook_name_consumers_readonly_paths.json')
CONTROL=Path('work/analysis/lil_B176_controls_v4554/one_A000_C200_single_end_and3_source_leaves.json')
CITY=Path('translations/entity_ship_names_arm9_v2.json')

if __name__=='__main__':
    assert not ROOT.exists()
    source,names,control,city=map(read,[SOURCE,NAMES,CONTROL,CITY])
    assert names['source_context_sha256']==control['source_context_sha256']==sha(SOURCE.read_bytes())
    assert names['approved_prose_names']=={'174':'Owner','175':'Cook'} and len(names['native_four_consumer_cases']['rows'])==4
    record=next(r for r in city['records'] if r['english']=='Seville');at=record['offset'];bindings=[]
    for label,path in [('clean','work/clean.nds'),('current',source['current_ROM'])]:
        arm=NdsImage.open(path).read_file('/__arm9__.bin');pointer=struct.unpack_from('<I',arm,at)[0];offset=pointer-0x02000000
        assert 0<=offset<len(arm);end=arm.index(b'\0',offset);value=arm[offset:end]
        assert value.decode('cp932')==('セビリア' if label=='clean' else 'Seville')
        assert arm[at:at+4].hex().upper()==record['source_hex' if label=='clean' else 'replacement_hex'].upper()
        bindings.append(dict(version=label,ROM=str(path),ARM9_sha256=sha(arm),pointer_field_offset=at,pointer=pointer,
            file_offset=offset,hex=value.hex(),text=value.decode('cp932'),whole_string_and_terminator_exact=True))
    by={r['source_record_index']:r for r in source['records']}
    for index,phrases in {6:['バナナ','時代'],13:['味','絶対','いける'],17:['そうですかね'],21:['私がいける'],
        24:['分かりました','どういたします'],27:['バナナ','買えるだけ'],31:['へいへい'],35:['時代','おっほほ'],38:['セビリア','バナナ','流行しそう']}.items():
        assert all(p in by[index]['source_Japanese'] for p in phrases),index
    assert by[38]['kind']=='system-FE' and source['source_macro_counts']=={'FI':0,'FA':0,'FO':0}
    ROOT.mkdir(parents=True)
    save(ROOT/'Owner_Cook_Seville_and_prospective_banana_fashion_reconciliation.json',dict(
        candidate=source['current_ROM'],candidate_sha256=source['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),
        approved_B176_prose_names=names['approved_prose_names'],chosen_city='Seville',exact_city_source_current_pointer_bindings=bindings,
        chosen_ordinary_commodity_word='bananas',banana_is_direct_clean_source_food_word_not_an_invented_named_item_title=True,
        Owner_Cook_native_role_labels_not_added_as_Captain_Queen_Mistress_or_kinship_addresses=True,
        initial_clean_glosses_precede_and_are_now_followed_by_Owner_Cook_native_binding=True,
        taste_will_catch_on_is_speaker_confidence_not_food_safety_or_already_earned_sales=True,
        buy_as_many_as_possible_adds_no_quantity_price_hold_capacity_or_completed_purchase=True,
        polite_doubt_offhand_acknowledgment_and_elaborate_confident_laugh_preserved_without_nobility_claim=True,
        FE_Seville_notice_preserves_prospective_likelihood_not_current_or_guaranteed_boom=True,
        city_appears_only_in_closing_notice_no_unproved_earlier_scene_location=True,
        A000_00a0ffff010a0da1_packed_semantics_and_actual_earned_market_state_not_inferred=True,
        broad_SourceItems_LocalProduct_graphics_and_later_older_record_reaudit_stay_open=True,
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,NAMES,CONTROL,CITY,Path(__file__)]},new_emulator_runs=0,
        source_prose_or_completion_credit_added=0,no_ROM_registry_ledger_change=True,full_goal_complete=False))
    print('Bound Owner/Cook and exact clean/current Seville name pointer;bananas and prospective fashion notice remain source-faithful. No credit.')
