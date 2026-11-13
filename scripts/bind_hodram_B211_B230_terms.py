"""Bind named/hinted equipment andplaces without importing extra catalogue facts into dialogue."""
import struct
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from scripts.audit_native_given_name_table import string
from scripts.registered_editorial_runtime import RegisteredRuntime
from scripts.bind_hodram_B191_B210_identities import cstring
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.script.arm9_profiles import WORLD_CITY_ENTRIES

ROOT=Path('work/analysis/Hodram_B211_B230_clean_20261104')
RELEASE=Path('work/analysis/Hodram_B171_B190_release_verified_20261104/registered_release_verification.json')

if __name__=='__main__':
    output=ROOT/'source_current_term_checkpoint_v1.json';assert not output.exists()
    ctx=RegisteredRuntime(RELEASE,RELEASE.with_name('own_registered_startup_verification.json'))
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    item_asset=Path('translations/all_item_names_arm9_v1.json');items=[]
    indices=[36,37,38,40,41,45,46,47,48,55,60,67,68,69,70,71,72,73]
    hints={36:214,37:218,38:216,40:212,41:211,45:217,46:221,47:219,48:213,55:230,60:226,67:223,68:225,69:229,70:227,71:224,72:228,73:221}
    for index in indices:
        approved=next(r for r in load(item_asset)['records'] if r['id']==f'DK4_ITEM_POINTER_{index:03d}')
        field=approved['offset'];original=string(clean,struct.unpack_from('<I',clean,field)[0])
        pointer=struct.unpack_from('<I',ctx.arm,field)[0];raw=cstring(ctx.raw,pointer)
        assert original['status']=='printable-static-string' and raw and all(32<=b<127 for b in raw)
        assert clean[field+4:field+24]==ctx.arm[field+4:field+24]
        items.append(dict(index=index,source_Japanese=original['text'],source_hex=original['hex'],pointer_field=field,
            current_pointer=pointer,current_hex=raw.hex(),current_term=raw.decode('ascii'),source_hint_block=hints[index],
            all_nonname_item_metadata_exact=True,
            bound_catalogue_not_permission_to_add_omitted_adjectives_oritem_identity_to_dialogue=True))
    city_asset=Path('dk4tool/script/arm9_profiles.py');city_precedent=Path('scripts/reconcile_lil_B178_terms_v4669.py');cities=[]
    # These fields andboth complete16-byte inline owners are identified by the
    # source-qualified B178 city reconciliation,not inferred from a text search.
    pointers={0x15DE84:0x122324,0x15DF94:0x122648}
    for entry in WORLD_CITY_ENTRIES:
        if entry.row_id not in ['DK4_CITY_AMSTERDAM_A','DK4_CITY_AMSTERDAM_B']:continue
        at=entry.offset;field=pointers[at];size=entry.source_length
        assert size==entry.slot_size==16 and entry.japanese=='アムステルダム' and entry.suggested_english=='Amsterdam'
        assert clean[at:at+size]==entry.expected_bytes and ctx.arm[at:at+size]==b'Amsterdam'+bytes(7)
        assert struct.unpack_from('<I',clean,field)[0]==struct.unpack_from('<I',ctx.arm,field)[0]==0x02000000+at
        cities.append(dict(source_profile_ID=entry.row_id,source_Japanese=entry.japanese,source_span_hex=clean[at:at+size].hex(),
            current_term='Amsterdam',pointer_field=field,current_pointer=0x02000000+at,current_span_hex=ctx.arm[at:at+size].hex(),
            complete_inline_owner_andsource_pointer_unchanged=True))
    assert len(cities)==2
    terms_path=Path('guide/research/player-terminology-reference.json');terms=load(terms_path)
    charm=next(r for r in terms if r['japanese']=='魅力' and r['english']=='Charm')
    source=load(ROOT/'complete_clean_meanings_before_English.json')
    save(output,dict(runtime=ctx.receipt(),equipment_terms=items,city_aliases=cities,attribute=charm,
        literary_andgeographic_terms={
            '三國志演義':'Romance of the Three Kingdoms', '趙雲':'Zhao Yun', '関羽':'Guan Yu',
            '諸葛亮':'Zhuge Liang','諸葛孔明':'Zhuge Kongming; the source uses the courtesy-name form in the spoken response.',
            'カリブ海':'Caribbean Sea','東アジア':'East Asia','中央アジア':'Central Asia','西アジア':'Western Asia',
            '山東半島':'Shandong Peninsula','アヴァロン':'Avalon','タスマン海':'Tasman Sea',
            'トゥール':'Tours','ポワティエ':'Poitiers','北欧':'northern Europe; source inference stays tentative.',
            'フビライ・ハン':'Kublai Khan','ティムール':'Timur','アッティラ':'Attila','カール・マルテル':'Charles Martel',
            'サラディン':'Saladin','ノリツネ':'Noritsune','イエス':'Jesus','ユダ':'Judas','アーサー王':'King Arthur','ヴィヴィアン':'Vivienne','ローマ':'Rome',
            'トクガワ氏':'Tokugawa; do not add a first name or office beyond the source.',
        },
        source_terms_are_localization_bindings_not_external_historical_verification=True,
        item_names_not_spoken_in_source_must_not_be_added_asnew_facts=True,
        source_shortened_pirate_sword_label_does_not_add_catalogue_red_hair_description=True,
        no_full_catalogue_orindividual_item_city_widget_fidelity_claim=True,
        no_current_story_English_extraction=True,no_new_ROM_orcompletion_credit=True,new_credit=0,guide_photos=False,
        source_meanings=str(ROOT/'complete_clean_meanings_before_English.json'),source_meanings_sha256=sha((ROOT/'complete_clean_meanings_before_English.json').read_bytes()),
        evidence={str(p):sha(p.read_bytes()) for p in [item_asset,city_asset,city_precedent,terms_path,Path(__file__)]}))
    print('Bound18 equipment terms,',len(cities),'city aliases andCharm;source-shortened hints remain short;no current dialogue extraction.')
