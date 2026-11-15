"""Bind three Lady labels, Amsterdam's inline names and pointer-selected Wheat."""
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.script.arm9_profiles import WORLD_CITY_ENTRIES
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B178_terms_v4669')
SOURCE=Path('work/analysis/lil_B178_source_v4662/all13_clean_current_complete_context.json')
NAMES=Path('work/analysis/lil_B178_names_v4667b/six_original_Lady166_167_168_name_consumers_readonly_paths.json')
CONTROL=Path('work/analysis/lil_B178_controls_v4668/one_A000_C200_single_end_and3_source_leaves.json')
CITY_PROFILE=Path('dk4tool/script/arm9_profiles.py')
COMMODITY=Path('translations/commodity_name_manuscript_v343.json')
REPACK=Path('dk4tool/patch/commodity_source_repack.py')
RELEASE=Path('work/analysis/lil_B177_release_v4656/registered_release_verification.json')

if __name__=='__main__':
    assert not ROOT.exists()
    source,names,control,release=map(read,[SOURCE,NAMES,CONTROL,RELEASE])
    assert names['source_context_sha256']==control['source_context_sha256']==sha(SOURCE.read_bytes())
    assert names['approved_prose_names']=={'166':'Lady','167':'Lady','168':'Lady'} and len(names['native_six_consumer_cases']['rows'])==6
    assert release['candidate_sha256']==source['current_ROM_sha256'] and release['all_source_shapes_BSS_and123040_staged_bytes_preserved']
    entries=[e for e in WORLD_CITY_ENTRIES if e.row_id in ['DK4_CITY_AMSTERDAM_A','DK4_CITY_AMSTERDAM_B']]
    assert [(e.row_id,e.offset,e.japanese,e.suggested_english,e.slot_size) for e in entries]==[
        ('DK4_CITY_AMSTERDAM_A',0x15DE84,'アムステルダム','Amsterdam',16),
        ('DK4_CITY_AMSTERDAM_B',0x15DF94,'アムステルダム','Amsterdam',16)]
    pointers={0x15DE84:0x122324,0x15DF94:0x122648}
    commodity=read(COMMODITY)['records'][0]
    assert (commodity['index'],commodity['pointer_field'],commodity['Japanese'],commodity['English'])==(0,0x15EF18,'小麦','Wheat')
    bindings=[];goods=[]
    for label,path in [('clean','work/clean.nds'),('current',source['current_ROM'])]:
        arm=NdsImage.open(path).read_file('/__arm9__.bin')
        if label=='current':assert sha(arm)==release['ARM9_sha256']
        for entry in entries:
            at,field=entry.offset,pointers[entry.offset];pointer=struct.unpack_from('<I',arm,field)[0]
            assert pointer==0x02000000+at
            value=arm[at:at+entry.source_length]
            assert value==(entry.expected_bytes if label=='clean' else b'Amsterdam'+bytes(7))
            bindings.append(dict(version=label,ROM=str(path),ARM9_sha256=sha(arm),source_profile_ID=entry.row_id,
                pointer_field_offset=field,pointer=pointer,file_offset=at,complete_span_bytes=16,complete_span_hex=value.hex(),
                unchanged_source_pointer_and_whole_inline_span_terminator_exact=True,no_new_city_widget_test_claimed=True))
        field=commodity['pointer_field'];at=struct.unpack_from('<I',arm,field)[0]-0x02000000;end=arm.index(0,at)
        expected='小麦' if label=='clean' else 'Wheat'
        assert at==(0x15B938 if label=='clean' else 0x15BC56)
        assert arm[at:end].decode('cp932')==expected and arm[field+4:field+12].hex()==commodity['metadata_hex']
        goods.append(dict(version=label,pointer_field_offset=field,pointer=0x02000000+at,file_offset=at,
            complete_terminated_hex=arm[at:end+1].hex(),text=expected,metadata_hex=arm[field+4:field+12].hex(),
            actual_pointer_selected_source_or_repacked_current_span=True,no_runtime_pool_growth_or_new_commodity_widget_test_claimed=True))
    assert len(bindings)==4 and len(goods)==2
    by={r['source_record_index']:r for r in source['records']}
    phrases={7:['パン','自分で焼く','最高'],10:['主人','大喜び'],13:['自分で焼く','おいしい'],17:['最高','ねえ'],
        21:['角のパン屋','目じゃない'],24:['私も','作ってみよう'],28:['そうしなさい'],32:['教えてあげる'],
        36:['本当','うれしい'],40:['さっそく','材料を買い'],43:['何が必要'],47:['まず','小麦'],51:['アムステルダム','小麦','流行しそう']}
    for index,parts in phrases.items():assert all(p in by[index]['source_Japanese'] for p in parts),index
    assert by[10]['source_selector']==by[32]['source_selector']==by[43]['source_selector']==167
    assert by[51]['kind']=='system-FE' and all('アムステルダム' not in r['source_Japanese'] for i,r in by.items() if i!=51)
    assert source['source_macro_counts']=={'FI':0,'FA':0,'FO':0}
    ROOT.mkdir(parents=True)
    save(ROOT/'three_Ladies_Amsterdam_Wheat_and_prospective_home_baking_fashion_reconciliation.json',dict(
        candidate=source['current_ROM'],candidate_sha256=source['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),
        approved_B178_prose_names=names['approved_prose_names'],chosen_city='Amsterdam',chosen_commodity_word='wheat',
        exact_city_source_current_inline_span_and_pointer_bindings=bindings,exact_wheat_source_current_pointer_selected_name_and_metadata_bindings=goods,
        Lady_native_labels_add_no_noble_rank_names_kinship_or_formal_relationship_address=True,
        husband_explicit_for167_only_no_named_husband_or_other_marriages_invented=True,
        home_baking_enthusiasm_corner_bakery_boast_curiosity_help_and_pleased_response_preserved=True,
        exact167_teaching_offer_then_ingredient_question_and168_wheat_suggestion_not_reassigned=True,
        wheat_not_flour_no_recipe_quantities_prices_completed_lesson_or_purchase_added=True,
        closing_FE_retains_prospective_likelihood_city_does_not_prove_earlier_location_or_B177_chronology=True,
        no_predecessor_story_English_exposed_by_this_binding=True,
        commodity_manuscript_historical_unfinished_formatting_actual_context_and_fidelity_notes_not_closed_by_pointer_binding=True,
        broad_SourceItems_LocalProduct_graphics_and_later_older_record_reaudit_stay_open=True,
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,NAMES,CONTROL,CITY_PROFILE,COMMODITY,REPACK,RELEASE,Path(__file__)]},
        new_emulator_runs=0,source_prose_or_completion_credit_added=0,no_ROM_registry_ledger_change=True,full_goal_complete=False))
    print('Bound three Lady labels,two Amsterdam inline spans and clean/current pointer-selected Wheat;metadata exact. Husband only for167;no source speaker reassignment. No credit.')
