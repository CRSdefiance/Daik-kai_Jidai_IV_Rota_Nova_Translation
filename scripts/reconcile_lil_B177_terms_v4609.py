"""Bind Owner/Cook,Genoa's two inline city spans,and the tomato vignette's distinct meanings."""
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.script.arm9_profiles import WORLD_CITY_ENTRIES
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B177_terms_v4609')
SOURCE=Path('work/analysis/lil_B177_source_v4602/all10_clean_current_complete_context.json')
NAMES=Path('work/analysis/lil_B177_names_v4607/four_original_Owner_Cook_name_consumers_readonly_paths.json')
CONTROL=Path('work/analysis/lil_B177_controls_v4608/one_A000_C200_single_end_and3_source_leaves.json')
CITY_PROFILE=Path('dk4tool/script/arm9_profiles.py')
RELEASE=Path('work/analysis/lil_B176_release_v4596/registered_release_verification.json')

if __name__=='__main__':
    assert not ROOT.exists()
    source,names,control,release=map(read,[SOURCE,NAMES,CONTROL,RELEASE])
    assert names['source_context_sha256']==control['source_context_sha256']==sha(SOURCE.read_bytes())
    assert names['approved_prose_names']=={'174':'Owner','175':'Cook'} and len(names['native_four_consumer_cases']['rows'])==4
    assert release['candidate_sha256']==source['current_ROM_sha256'] and release['all_source_shapes_BSS_and123040_staged_bytes_preserved']
    entries=[e for e in WORLD_CITY_ENTRIES if e.row_id in ['DK4_CITY_GENOA_A','DK4_CITY_GENOA_B']]
    assert [(e.row_id,e.offset,e.japanese,e.suggested_english,e.slot_size) for e in entries]==[
        ('DK4_CITY_GENOA_A',0x15CA64,'ジェノヴァ','Genoa',12),('DK4_CITY_GENOA_B',0x15CC68,'ジェノヴァ','Genoa',12)]
    pointer_fields={0x15CA64:0x122384,0x15CC68:0x122C2C}
    bindings=[]
    for label,path in [('clean','work/clean.nds'),('current',source['current_ROM'])]:
        arm=NdsImage.open(path).read_file('/__arm9__.bin')
        if label=='current':assert sha(arm)==release['ARM9_sha256']
        for entry in entries:
            at=entry.offset;field=pointer_fields[at];pointer=struct.unpack_from('<I',arm,field)[0]
            assert pointer==0x02000000+at
            value=arm[at:at+entry.source_length]
            expected=entry.expected_bytes if label=='clean' else b'Genoa'+bytes(7)
            assert value==expected and value.split(b'\0')[0].decode('cp932')==('ジェノヴァ' if label=='clean' else 'Genoa')
            bindings.append(dict(version=label,ROM=str(path),ARM9_sha256=sha(arm),source_profile_ID=entry.row_id,
                pointer_field_offset=field,pointer=pointer,file_offset=at,complete_span_bytes=12,complete_span_hex=value.hex(),
                text=value.split(b'\0')[0].decode('cp932'),unchanged_source_pointer_and_whole_inline_span_terminator_exact=True,
                no_staged_pool_relocation_or_new_native_city_widget_test_claimed=True))
    assert len(bindings)==4
    by={r['source_record_index']:r for r in source['records']}
    for index,phrases in {6:['トマト','時代'],9:['真っ赤','食いもん'],12:['この赤','情熱','若い頃','身を焦がすような恋'],
        16:['そうですか','よかったですね'],20:['さっそく','トマト料理','売り出す'],23:['分かりました'],
        27:['トマトの流行','逃がさない'],30:['へいへい'],34:['がんばって','おっほほ'],37:['ジェノヴァ','トマト','流行しそう']}.items():
        assert all(p in by[index]['source_Japanese'] for p in phrases),index
    assert by[37]['kind']=='system-FE' and all('ジェノヴァ' not in r['source_Japanese'] for i,r in by.items() if i!=37)
    assert source['source_macro_counts']=={'FI':0,'FA':0,'FO':0}
    ROOT.mkdir(parents=True)
    save(ROOT/'Owner_Cook_Genoa_and_prospective_tomato_fashion_reconciliation.json',dict(
        candidate=source['current_ROM'],candidate_sha256=source['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),
        approved_B177_prose_names=names['approved_prose_names'],chosen_city='Genoa',exact_city_source_current_inline_span_and_pointer_bindings=bindings,
        chosen_ordinary_commodity_word='tomatoes',tomatoes_are_direct_clean_source_food_word_not_an_invented_named_item_title=True,
        approved_city_profile_source=str(CITY_PROFILE),approved_city_profile_source_sha256=sha(CITY_PROFILE.read_bytes()),
        Owner_Cook_native_role_labels_add_no_royal_military_kinship_or_formal_relationship_address=True,
        red_food_skepticism_does_not_add_poison_food_safety_or_historical_taboo=True,
        red_stirs_passion_and_recalls_her_youthful_romance_no_identified_lover_or_present_relationship=True,
        detached_polite_acknowledgment_not_shared_nostalgia_flirtation_or_extra_insult=True,
        immediate_cook_and_start_selling_order_adds_no_completed_sale_purchase_quantity_price_profit_or_hold_capacity=True,
        speaker_treats_tomato_fashion_as_opportunity_closing_FE_retains_prospective_likelihood=True,
        city_named_only_in_closing_notice_no_unproved_earlier_scene_location_or_B176_chronology=True,
        A000_00a0ffff01090fa1_packed_semantics_and_earned_fashion_state_not_inferred=True,
        incidental_predecessor_search_exposure_after_all_clean_glosses_recorded=dict(
            files=['scripts/materialize_lil_deep_route_v77.py','dk4tool/dialogue/profiles.py'],
            exposed='The retained closing Genoa forecast and historical location/role metadata appeared in repository name search. Full paragraph comparison remains separate after this binding.',
            no_clean_first_gloss_rewritten_from_predecessor=True),
        broad_SourceItems_LocalProduct_graphics_and_later_older_record_reaudit_stay_open=True,
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,NAMES,CONTROL,CITY_PROFILE,RELEASE,Path(__file__)]},
        new_emulator_runs=0,source_prose_or_completion_credit_added=0,no_ROM_registry_ledger_change=True,full_goal_complete=False))
    print('Bound Owner/Cook and both clean/current Genoa inline spans/pointers;red,passion,dry reply,cooking/selling order and prospective notice remain source-bound. No credit.')
