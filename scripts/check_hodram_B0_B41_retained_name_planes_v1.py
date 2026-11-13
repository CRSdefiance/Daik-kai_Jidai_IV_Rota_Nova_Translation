"""Reuse exact name planes, drawing only missing retained strings on the original consumer."""
from copy import deepcopy
from pathlib import Path

from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts import check_rafael_B61_B80_scoped_name_planes as previous
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.review_hodram_B0_B41_names_v1 import ROOT,OUT as REVIEW
from scripts.source_locked_derivation_v5118 import checked_text

NATIVE=ROOT/'scoped_names_current_v1.json'
INPUT=ROOT/'name_plane_inputs_v1'
OUT=ROOT/'retained_name_planes_v1'
PRIOR=ROOT/'retained_name_cache_v1.json'
RELEASE=Path('work/hodram_B301_B310_release_v1/registered_release_verification.json')
STARTUP=Path('work/Hodram_B311_B324_clean_20261107/own_parent_startup_v1/own_route_context.json')
CACHES=[Path(p)/'native_name_planes.json' for p in (
    'work/Hodram_B211_B230_resume_20261106/name_planes_v1',
    'work/Hodram_B231_B250_clean_20261107/name_planes_v1',
    'work/Hodram_B251_B280_clean_20261107/name_planes_v1',
    'work/Hodram_B281_B300_clean_20261107/name_planes_v2',
    'work/Hodram_B301_B310_clean_20261107/name_planes_v1',
    'work/Hodram_B311_B324_clean_20261107/name_planes_v1')]


def main():
    assert not INPUT.exists() and not OUT.exists() and not PRIOR.exists()
    native,review=map(load,(NATIVE,REVIEW));runtime=native['runtime']
    image=NdsImage.open(runtime['candidate']);arm=image.read_file('/__arm9__.bin')
    assert sha(arm)==runtime['ARM9_sha256']
    cache={};dependencies=[]
    for path in CACHES:
        if not path.exists():continue
        doc=load(path);old=NdsImage.open(doc['runtime']['candidate'])
        assert digest(doc['runtime']['candidate'])==doc['runtime']['candidate_sha256']
        assert old.read_file('/__arm9__.bin')==arm
        assert old.read_file('/GRP/KANJI.FNT')==image.read_file('/GRP/KANJI.FNT')
        assert old.read_file('/COMMON/MESFILE.DK4')==image.read_file('/COMMON/MESFILE.DK4')
        dependencies.append(dict(path=str(path),sha256=digest(path),complete_ARM9_font_COMMON_exact=True))
        for plane in doc['planes']:
            assert digest(plane['native_plane'])==plane['native_plane_sha256'] and digest(plane['preview'])==plane['preview_sha256']
            assert plane['complete_first_internal_final_codes_bounds_andindependent_font_pixels_pass']
            value=deepcopy(plane);value['original_cache_receipt']=str(path);value['original_cache_receipt_sha256']=digest(path)
            if value['text'] in cache:assert value['native_plane_sha256']==cache[value['text']]['native_plane_sha256']
            cache[value['text']]=value
    save(PRIOR,dict(runtime=runtime,planes=list(cache.values()),qualified_cache_inputs=dependencies,new_credit=0))
    rows=[]
    for row in review['records']:
        if row['decision']!='retention':continue
        record=deepcopy(row)
        record['english']=next(r['text'] for r in row['current_consumers'] if r['consumer']=='progressive-nameplate')
        assert record['english'].isascii()
        rows.append(record)
    assert len(rows)==39 and len({r['english'] for r in rows})==38
    INPUT.mkdir();names=INPUT/'names.json';identity=INPUT/'identity.json'
    save(names,{**review,'records':rows,'scoped_actors':39,'excludes_three_separately_verified_name_revisions':True})
    save(identity,dict(runtime=runtime,name_bindings=rows,complete_target_ARM9_font_COMMON_identical_to_cache=True,new_credit=0))
    source=Path(previous.__file__).read_text(encoding='utf-8');source=source[source.index("if __name__=='__main__':"):]
    source=checked_text(source,{
        "ctx=RegisteredRuntime(RELEASE,RELEASE.with_name('own_registered_startup_verification.json'),captain=0)":
            'ctx=RegisteredRuntime(RELEASE,STARTUP,captain=1)',
        "assert qual['runtime']==ctx.receipt() and qual['previous_runtime']==bound['runtime']":
            "assert qual['runtime']==ctx.receipt()==bound['runtime'] and qual['complete_target_ARM9_font_COMMON_identical_to_cache']",
        "assert prior['proposed_ARM9_sha256']==sha(ctx.arm)":"assert prior['runtime']['ARM9_sha256']==sha(ctx.arm)",
        "len(doc['records'])==len(bound['name_bindings'])==22":"len(doc['records'])==len(bound['name_bindings'])==39",
        'assert len(planes)==21 and fresh+reused==21':'assert len(planes)==38 and fresh+reused==38',
        'scoped_actors=22,distinct_strings=21':'scoped_actors=39,distinct_strings=38',
        "print(f'22actors/21strings:":"print(f'39actors/38strings:",
    })
    env={**vars(previous),'ROOT':OUT,'NAMES':names,'BINDINGS':identity,'QUAL':identity,'PRIOR':PRIOR,
        'RELEASE':RELEASE,'STARTUP':STARTUP,'__file__':__file__,'__name__':'__main__'}
    exec(compile(source,__file__+'::same-native-name-pixels-and-exact-qualified-cache','exec'),env)


if __name__=='__main__':main()
