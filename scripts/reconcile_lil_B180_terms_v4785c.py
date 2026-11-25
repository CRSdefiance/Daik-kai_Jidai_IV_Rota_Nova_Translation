"""Bind Lisbon and the Scents category before predecessor-English comparison."""
from pathlib import Path
import struct
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_category_lookup_v754 import cpu_for,getter,UI_RETURNS
from scripts.native_machine_scoped_v764 import machine as clean_machine
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B180_terms_v4785c')
SOURCE=Path('work/analysis/lil_B180_source_v4773/all11_clean_current_complete_context.json')

if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE)
    names=read('work/analysis/lil_B180_names_v4779/four_original_Lady_name_consumers.json')
    controls=read('work/analysis/lil_B180_controls_v4780c/two_predicates_three_A000_C200_ten_relative_sites_and_single_end.json')
    assert names['source_context_sha256']==controls['source_context_sha256']==sha(SOURCE.read_bytes())
    assert names['approved_prose_names']=={'166':'Lady','167':'Lady'}
    category=[];cities=[];members=[]
    manuscript=read('translations/commodity_name_manuscript_v343.json')
    goods={r['index']:r for r in manuscript['records'] if r['index'] in [59,60,61]}
    fidelity={r['index']:r for r in read('translations/commodity_fidelity_v2.json')['records']}
    for i,r in goods.items():
        assert fidelity[i]['Japanese']==r['Japanese'];r['English']=fidelity[i]['English']
    assert {i:r['English'] for i,r in goods.items()}=={59:'Musk',60:'Frankincense',61:'Ambergris'}
    for label,path in [('clean','work/clean.nds'),('current',packet['current_ROM'])]:
        image=NdsImage.open(path);arm=image.read_file('/__arm9__.bin')
        for field,at in [(0x122344,0x15C068),(0x122A5C,0x15C11C)]:
            pointer=struct.unpack_from('<I',arm,field)[0];assert pointer==0x02000000+at
            span=arm[at:at+12];text=span.split(b'\0')[0].decode('cp932')
            assert text==('リスボン' if label=='clean' else 'Lisbon')
            cities.append(dict(version=label,pointer_field=field,pointer=pointer,owned_offset=at,
                complete12_byte_span_hex=span.hex(),text=text,source_pointer_and_owned_termination_preserved=True))
        cpu=clean_machine(arm) if label=='clean' else cpu_for(arm)
        for parent in [*UI_RETURNS,0x0205FC48]:
            ptr=getter(cpu,10,parent);value=bytes(cpu.mem_read(ptr,80)).split(b'\0')[0]
            text=value.decode('cp932');assert text==('香料' if label=='clean' else 'Scents')
            category.append(dict(version=label,category_lookup_index=10,native_return_PC=parent,
                pointer=ptr,terminated_hex=(value+b'\0').hex(),text=text,
                native_stack_saved_registers_and_return_ABI_checked=True))
        for i,r in goods.items():
            field=r['pointer_field'];ptr=struct.unpack_from('<I',arm,field)[0];at=ptr-0x02000000;end=arm.index(0,at)
            assert arm[field+4:field+12].hex()==r['metadata_hex'] and arm[field+6]==11
            text=arm[at:end].decode('cp932');assert text==(r['Japanese'] if label=='clean' else r['English'])
            members.append(dict(version=label,commodity_index=i,pointer_field=field,pointer=ptr,
                terminated_hex=arm[at:end+1].hex(),text=text,original_product_category_byte=11,
                metadata_hex=r['metadata_hex'],no_new_widget_or_whole_commodity_fidelity_completion=True))
    by={r['source_record_index']:r for r in packet['records']}
    assert all(p in by[73]['source_Japanese'] for p in ['リスボン','香料','流行しそう'])
    assert by[73]['kind']=='system-FE' and all('リスボン' not in r['source_Japanese'] for i,r in by.items() if i!=73)
    expected={5:['あの方','すごくいい匂い','思いませんこと'],9:['あなたもそう思った'],13:['何の香り'],
        17:['存じません','きっと流行ります'],20:['他の方よりも先に','手に入れなくては'],24:['そうですわね'],
        28:['次にお会いするとき','思い切って','聞いてみる'],31:['いい考え','ぜひ'],34:['ごきげんよう'],38:['ごきげんよう']}
    for i,parts in expected.items():assert all(s in by[i]['source_Japanese'] for s in parts),i
    ROOT.mkdir(parents=True)
    save(ROOT/'Lady_Lisbon_Scents_and_prospective_fashion_reconciliation.json',dict(candidate=packet['current_ROM'],
        candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),
        approved_dialogue_roles=names['approved_prose_names'],generic_Lady_roles_do_not_establish_nobility_or_marriage=True,
        city='Lisbon',exact_two_city_alias_source_current_bindings=cities,
        category='Scents',source_category='香料',all12_native_category_getter_bindings=category,
        category_membership_crosschecks=members,
        category_is_not_a_single_named_perfume_ingredient_or_brand=True,
        narrator_notice_remains_prospective_and_does_not_locate_the_earlier_conversation=True,
        natural_prose_guidance='The narrator forecasts popularity of the Scents category in Lisbon. Preserve likelihood,do not claim a current boom,shortage,price rise,sale or guaranteed profit. Use natural category language;do not transplant commodity demand phrasing without proving that mechanic.',
        fragrance_identity_gender_third_person_rank_relationship_and_supplier_unknown=True,
        source_unforced_random_conditions_and_three_effect_alternatives_preserved=True,
        source_dialogue_knowledge_limit_distinct_from_speaker_confident_fashion_prediction=True,
        prior_whole_exchange_Japanese_and_fresh_glosses_recorded_before_predecessor_English=True,
        no_predecessor_English_exposed_by_this_tool=True,no_new_ROM_emulator_or_review_credit=True,
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,Path('dk4tool/patch/category_dialogue_lookup.py'),Path('work/analysis/category_dialogue_v754/lookup_native_ABI.json'),Path('translations/commodity_name_manuscript_v343.json'),Path('translations/commodity_fidelity_v2.json'),Path('translations/commodity_fidelity_manuscript_v2.json')]},
        full_goal_complete=False))
    print('Approved Lady/Lisbon/Scents bound:12 original category lookups,two city aliases andthree category members. No guessed demand mechanics,brand or earlier location.')
