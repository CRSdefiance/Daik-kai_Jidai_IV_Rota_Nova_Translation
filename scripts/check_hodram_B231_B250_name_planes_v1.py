"""Reuse exact literal name planes on the unchanged runtime and paint newly scoped strings."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from scripts import check_rafael_B61_B80_scoped_name_planes as previous
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.review_hodram_B231_B250_names_terms_v1 import NATIVE,REVIEW,ROOT
from scripts.source_locked_derivation_v5118 import checked_text

OUT=ROOT/'name_planes_v1'
PRIOR=Path('work/Hodram_B211_B230_resume_20261106/name_planes_v1/native_name_planes.json')
INPUT=ROOT/'name_plane_inputs_v1'
RELEASE=Path('work/hodram_B211_B230_release_v1/registered_release_verification.json')
STARTUP=ROOT/'own_parent_startup_v1/own_route_context.json'

def main():
    assert not OUT.exists() and not INPUT.exists()
    review,native,cache=map(load,(REVIEW,NATIVE,PRIOR));release=load(RELEASE)
    current=NdsImage.open(release['candidate']);old=NdsImage.open(cache['runtime']['candidate'])
    assert digest(cache['runtime']['candidate'])==cache['runtime']['candidate_sha256']
    assert current.read_file('/__arm9__.bin')==old.read_file('/__arm9__.bin')
    assert current.read_file('/GRP/KANJI.FNT')==old.read_file('/GRP/KANJI.FNT')
    assert current.read_file('/COMMON/MESFILE.DK4')==old.read_file('/COMMON/MESFILE.DK4')
    INPUT.mkdir();identity=INPUT/'identity.json';names=INPUT/'names.json'
    save(names,review)
    save(identity,dict(runtime=native['runtime'],name_bindings=review['records'],
        complete_target_ARM9_font_COMMON_identical_to_cache=True,new_credit=0))
    source=Path(previous.__file__).read_text(encoding='utf-8');source=source[source.index("if __name__=='__main__':"):]
    source=checked_text(source,{
        "ctx=RegisteredRuntime(RELEASE,RELEASE.with_name('own_registered_startup_verification.json'),captain=0)":
            "ctx=RegisteredRuntime(RELEASE,STARTUP,captain=1)",
        "assert qual['runtime']==ctx.receipt() and qual['previous_runtime']==bound['runtime']":
            "assert qual['runtime']==ctx.receipt()==bound['runtime'] and qual['complete_target_ARM9_font_COMMON_identical_to_cache']",
        "assert prior['proposed_ARM9_sha256']==sha(ctx.arm)":"assert prior['runtime']['ARM9_sha256']==sha(ctx.arm)",
        "len(doc['records'])==len(bound['name_bindings'])==22":"len(doc['records'])==len(bound['name_bindings'])==19",
        'assert len(planes)==21 and fresh+reused==21':'assert len(planes)==19 and fresh+reused==19',
        'scoped_actors=22,distinct_strings=21':'scoped_actors=19,distinct_strings=19',
        "print(f'22actors/21strings:":"print(f'19actors/19strings:",
    })
    env={**vars(previous),'ROOT':OUT,'NAMES':names,'BINDINGS':identity,'QUAL':identity,'PRIOR':PRIOR,
        'RELEASE':RELEASE,'STARTUP':STARTUP,'__file__':__file__,'__name__':'__main__'}
    exec(compile(source,__file__+'::same-native-style11-literal-name-checks-exact-cache','exec'),env)

if __name__=='__main__':main()
