"""Bind scoped village/city/stat spellings to clean and current native data."""
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.script.arm9_profiles import WORLD_CITY_ENTRIES
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.qualify_rafael351_item_and_UI_terms_v1 import string

ROOT=Path('work/Lil269_B243_B282_clean_20261110')


def main():
    out=ROOT/'scoped_terms_reference_v1.json';assert not out.exists()
    current=ROOT/'current_v1/current_effective.json';runtime=load(current)['runtime']
    ctx=RegisteredRuntime(runtime['release_proof'],runtime['startup_proof'],captain=2);assert ctx.receipt()==runtime
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    def pointer_term(at,jp,en):
        a,b=struct.unpack_from('<I',clean,at)[0],struct.unpack_from('<I',ctx.arm,at)[0]
        before,after=string(clean,a),string(ctx.raw,b)
        assert before['text']==jp and after['text']==en
        return dict(pointer_field_offset=at,source_field_hex=clean[at:at+4].hex(),current_field_hex=ctx.arm[at:at+4].hex(),source=before,current=after)
    vp=Path('translations/village_ui_manuscript_v1.json');v=next(r for r in load(vp)['records'] if r['id']=='VILLAGE_NAME_16')
    assert v['english']=='Leveque' and v['Japanese']=='レバキュー' and all(v['review'].values())
    village=pointer_term(v['pointer_field'],v['Japanese'],v['english'])
    cityproof=Path('work/analysis/maria_B97_terms_v5006/bound_Maria_Xien_Bandit_Li_Clan_Sao_Jorge_Proof_and_tablet_context.json')
    prior=load(cityproof);source=prior['source_current_city_item_and_HELP_versions'][0]['city']
    assert prior['approved_city']=='Sao Jorge'
    sao=pointer_term(source['pointer_field'],'サン＝ジョルジェ','Sao Jorge')
    wanted={'Hamburg','Copenhagen','Sofala','Basra','Seville','Calicut','Hangzhou','Genoa','Batavia','Brunei'}
    aliases=[]
    for entry in WORLD_CITY_ENTRIES:
        if entry.suggested_english not in wanted:continue
        assert clean[entry.offset:entry.offset+entry.source_length]==entry.expected_bytes
        raw=ctx.arm[entry.offset:entry.offset+entry.slot_size]
        assert raw==entry.suggested_english.encode()+bytes(entry.slot_size-len(entry.suggested_english))
        aliases.append(dict(id=entry.row_id,offset=entry.offset,source_Japanese=entry.japanese,source_hex=entry.expected_bytes.hex(),current_hex=raw.hex(),english=entry.suggested_english))
    assert len(aliases)==14 and {r['english'] for r in aliases}==wanted
    sp=Path('guide/research/player-terminology-reference.json')
    stats=[r for r in load(sp) if (r.get('japanese'),r.get('english')) in [('運勢','Luck'),('魅力','Charm')]]
    assert len(stats)==2
    notices=[r for g in load(current)['groups'] for r in g['records'] if g['block']==250 and r['source_selector']==254 and any(t in r['source_Japanese'] for t in ['運勢','魅力'])]
    assert len(notices)==4
    for r in notices:
        term='Luck' if '運勢' in r['source_Japanese'] else 'Charm'
        assert term in r['current_comparison_paragraph'] and '1' in r['current_comparison_paragraph']
    save(out,dict(runtime=runtime,items=[],village= village,Sao_Jorge=sao,inline_city_aliases=aliases,permanent_attributes=stats,
        exact_current_source_stat_notices=[dict(id=r['id'],source_reference=r['source_reference'],current_reference=r['current_reference'],source_hex=r['source_hex'],current_hex=r['current_hex']) for r in notices],
        source_lexical_forms={'イギリス人':'English','オランダ':'Dutch','イタリア':'Italy/Italian','ポルトガル':'Portugal/Portuguese','スペイン':'Spain/Spanish','サン＝チャゴ大聖堂':'Santiago Cathedral','紫禁城':'Forbidden City','インド洋':'Indian Ocean','北海':'North Sea','地中海':'Mediterranean','ブルネイ':'Brunei'},
        source_unnamed_figureheads_treasures_kings_andvoices_not_expanded_to_catalogue_titles=True,
        reported_locations_legends_andmissing_people_not_promoted_to_confirmed_facts=True,
        current_stat_andcity_string_binding_not_new_UI_layout_orfont_approval=True,
        no_new_ROM_orcompletion_credit=True,new_credit=0,
        evidence={str(p):digest(p) for p in [current,vp,cityproof,sp,Path('dk4tool/script/arm9_profiles.py'),Path(__file__)]}))
    print('PASS Leveque/Sao Jorge,14 city spans,Luck/Charm andfour exact notices;zero credit.')


if __name__=='__main__':main()
