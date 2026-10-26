"""Bind ten item names, stat terminology and four provisional actor annotations."""
from pathlib import Path
import struct
from ndspy.code import MainCodeFile
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.main_pool_cache_visibility import POOL
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_Crew_Items_terms_v3116')
SOURCE=Path('work/analysis/lil_Crew_Items_source_v3112/complete200_clean_current_native_context.json')
CATALOG=Path('translations/all_item_names_arm9_v1.json')
STATS=Path('translations/person_info_graphics_v3.json')
NATIVE=Path('translations/person_info_arm9_v1.json')
ITEMS={
1:('トマトの苗木','Tomato Seedling'),32:('掃滅のカッツバルゲル','Sweeping Katzbalger'),48:('妖刀村正','Muramasa'),
61:('孔雀かたびら','Peacock Mail'),63:('抜け忍の黒装束','Ninja Garb'),65:('ジャガー神の宿る胴着',"Jaguar God's Vest"),
73:('ミネルヴァの盾','Minerva Shield'),93:('奇跡の弾丸のペンダント','Miracle Bullet Charm'),
102:('ヘスティアの釜',"Hestia's Pot"),126:('アリスタルコスの望遠鏡','Aristarchus Telescope')}
if __name__=='__main__':
    assert not ROOT.exists();source,catalog,stats,native=map(read,[SOURCE,CATALOG,STATS,NATIVE]);versions=[]
    for label,path in [('clean','work/clean.nds'),('current',source['current_ROM'])]:
        image=NdsImage.open(path);arm=image.read_file('/__arm9__.bin');code=MainCodeFile(arm,0x02000000)
        views=[(s.ramAddress,bytes(s.data),'original-main-code-section') for s in code.sections]
        if label=='current':
            assert len(code.sections[3].data)-48==123040
            views.append((POOL,bytes(code.sections[3].data[:-48]),'registered123040-byte-runtime-pool-copy'))
        def string(pointer):
            hits=[v for v in views if v[0]<=pointer<v[0]+len(v[1])];assert len(hits)==1
            start,data,owner=hits[0];tail=data[pointer-start:];end=tail.index(b'\0')
            return dict(pointer=pointer,owner=owner,complete_C_string_hex=tail[:end+1].hex(),text=tail[:end].decode('cp932'))
        items=[]
        for index,(Japanese,English) in ITEMS.items():
            row=next(r for r in catalog['records'] if r['id']==f'DK4_ITEM_POINTER_{index:03d}');assert row['english']==English
            value=string(struct.unpack_from('<I',arm,row['offset'])[0]);assert value['text']==(Japanese if label=='clean' else English)
            items.append(dict(index=index,registered_record_ID=row['id'],pointer_file_offset=row['offset'],source_Japanese=Japanese,approved_English=English,**value))
        spirit=next(r for r in native['records'] if r['id']=='DK4_PERSON_STAT_SPIRIT');assert spirit['english']=='Spirit'
        off=spirit['offset'];value=arm[off:off+8].split(b'\0')[0].decode('cp932');assert value==('精神' if label=='clean' else 'Spirit')
        versions.append(dict(version=label,ROM=path,ROM_sha256=sha(Path(path).read_bytes()),ARM9_sha256=sha(arm),items=items,native_Spirit_stat=dict(offset=off,text=value,span_hex=arm[off:off+8].hex())))
    luck=next(r for r in stats['records'] if r['id']=='DK4_PERSON_STAT_PLAQUE_5_V2')
    spirit=next(r for r in stats['records'] if r['id']=='DK4_PERSON_STAT_PLAQUE_4_V2')
    mood=next(r for r in stats['records'] if r['id']=='DK4_PERSON_MOOD_PLAQUE')
    assert (luck['source_japanese'],luck['text'])==('運勢','Luck') and (spirit['source_japanese'],spirit['text'])==('精神','Spirit')
    assert mood['source_japanese']=='精神' and mood['text']=='Mood'
    names={k:r['historical_native_catalog_name'] for k,r in source['speaker_catalog'].items()}
    assert all(names[k]==v for k,v in {'108':'Trader','114':'Port Worker','152':'Retainer','188':'Margrete'}.items())
    text86=' '.join(r['source_Japanese'] for r in source['records'] if r['block']==86)
    assert 'カッツバルケル' in text86 and '掃滅' not in text86
    assert len([r for r in source['records'] if r['kind']=='system-FE' and 'FI' in r['source_Japanese']])==2
    ROOT.mkdir(parents=True);save(ROOT/'clean_current_ten_items_stat_UI_and_native_actor_terms.json',dict(source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),versions=versions,
        registered_item_catalog=str(CATALOG),registered_item_catalog_sha256=sha(CATALOG.read_bytes()),approved_item_names={str(k):v[1] for k,v in ITEMS.items()},all10_clean_current_pointer_strings_equal_registered_names=True,
        approved_stat_terms=dict(Luck=dict(record_ID=luck['id'],source='運勢',English='Luck'),Spirit=dict(record_ID=spirit['id'],source='精神',English='Spirit'),Mood=dict(record_ID=mood['id'],source='精神',English='Mood',not_the_plus1_stat_in_this_source=True)),
        stat_UI_config=str(STATS),stat_UI_config_sha256=sha(STATS.read_bytes()),native_stat_config=str(NATIVE),native_stat_config_sha256=sha(NATIVE.read_bytes()),
        no_new_graphics_render_or_plaque_completion_claim=True,source_plus1_notices_are_stat_changes_not_Mood_conditions=True,
        exact_native_actor_names=names,source_speaker_annotation_reconciliation={'108':'Trader;original actor108','114':'Port Worker;original actor114','152':'Former sailor;original native Retainer actor152,source role not noble rank','188':'Margrete;current registered actor188'},
        source86_generic_weapon_type='Katzbalger',source86_does_not_say_the_unique_item_prefix_Sweeping=True,
        source88_Ninja_Garb_requires_renegade_ninja_black_armored_outfit_context=True,
        source82_Miracle_Bullet_Charm_is_a_pendant_and_not_an_invented_cannon_upgrade=True,
        source99_Muramasa_retains_cursed_or_unnerving_blade_description_without_renaming_catalog=True,
        source_prose_or_completion_credit_added=0,no_ROM_registry_ledger_change=True,new_emulator_runs=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Ten clean/current item pointers,Spirit native label,Luck/Spirit/Mood UI distinction andTrader/PortWorker/Retainer/Margrete identities bound. Zero credit.')
