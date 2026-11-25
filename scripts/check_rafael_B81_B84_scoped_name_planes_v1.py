"""Reuse nine identical current-runtime name planes and render the seven newly scoped names."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/check_rafael_B61_B80_scoped_name_planes.py').read_text(encoding='utf-8'),{
    'Rafael_B61_B80_progressive_name_planes_20261104':'Rafael_B81_B84_progressive_name_planes_20261105',
    'translations/rafael_B61_B80_scoped_names_andterms_v1.json':'translations/rafael_B81_B84_scoped_names_androles_v1.json',
    'work/analysis/Rafael_B51_B60_release_verified_20261104/registered_release_verification.json':
        'work/analysis/Shipyard_HELP37_release_verified_20261104/registered_release_verification.json',
    'work/analysis/Rafael_B61_B80_clean_20261104/source_identity_event_andterm_checkpoint_v1.json':
        'work/analysis/Rafael_B81_B84_formatting_20261105/scoped_names_macro_andconsumer_dependency_qualification_v1.json',
    'work/analysis/Rafael_B61_B80_latest_runtime_20261104/dependency_qualification.json':
        'work/analysis/Rafael_B81_B84_formatting_20261105/scoped_names_macro_andconsumer_dependency_qualification_v1.json',
    "    assert qual['runtime']==ctx.receipt() and qual['previous_runtime']==bound['runtime']":
        "    assert qual['runtime']==ctx.receipt()==bound['runtime'] and bound['complete_ARM9_COMMON_font_andactor_array_exact_to_qualified_runtime']",
    "len(doc['records'])==len(bound['name_bindings'])==22":"len(doc['records'])==len(bound['name_bindings'])==16",
    "    cache={r['text']:deepcopy(r) for r in prior['planes']}":
        """    cache={r['text']:deepcopy(r) for r in prior['planes']}
    cacheorigins={r['text']:PRIOR for r in prior['planes']}
    from dk4tool.rom.nds import NdsImage
    priorimage=NdsImage.open(prior['runtime']['candidate'])
    assert priorimage.read_file('/GRP/KANJI.FNT')==ctx.image.read_file('/GRP/KANJI.FNT')
    earlier=Path('work/analysis/Rafael_B61_B80_progressive_name_planes_20261104/native_name_planes.json')
    earlierproof=load(earlier);assert earlierproof['runtime']['ARM9_sha256']==sha(ctx.arm)
    earlierimage=NdsImage.open(earlierproof['runtime']['candidate'])
    assert earlierimage.read_file('/GRP/KANJI.FNT')==ctx.image.read_file('/GRP/KANJI.FNT')
    for plane in earlierproof['planes']:
        cache.setdefault(plane['text'],deepcopy(plane));cacheorigins.setdefault(plane['text'],earlier)""",
    'dict(path=str(PRIOR),sha256=sha(PRIOR.read_bytes()),':
        'dict(path=str(cacheorigins[text]),sha256=sha(cacheorigins[text].read_bytes()),',
    "assert len(planes)==21 and fresh+reused==21":"assert len(planes)==16 and (fresh,reused)==(7,9)",
    'scoped_actors=22,distinct_strings=21':'scoped_actors=16,distinct_strings=16',
    '[NAMES,BINDINGS,QUAL,PRIOR,RELEASE,Path(__file__)]':'[NAMES,BINDINGS,QUAL,PRIOR,earlier,RELEASE,Path(__file__)]',
    "print(f'22actors/21strings:":"print(f'16actors/16strings:",
})
exec(compile(source,__file__+'::same-full-native-style11-and-exact-nine-plane-reuse','exec'),globals())
