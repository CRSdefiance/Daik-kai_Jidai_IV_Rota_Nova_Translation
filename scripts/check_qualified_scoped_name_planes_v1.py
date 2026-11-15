"""Render scoped public names with the proven native style; reuse exact cached planes."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

BASE = Path('scripts/check_rafael_B61_B80_scoped_name_planes.py')
source = checked_text(BASE.read_text(encoding='utf-8'), {
    "if __name__=='__main__':\n    assert not ROOT.exists()":
        """if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ['names','identity','release','startup','out']:
        parser.add_argument('--'+name,type=Path,required=True)
    parser.add_argument('--prior',type=Path,nargs='+',required=True)
    args=parser.parse_args()
    ROOT,NAMES,BINDINGS,QUAL,PRIOR,RELEASE=args.out,args.names,args.identity,args.identity,args.prior[0],args.release
    assert not ROOT.exists()""",
    "ctx=RegisteredRuntime(RELEASE,RELEASE.with_name('own_registered_startup_verification.json'),captain=0)":
        "ctx=RegisteredRuntime(RELEASE,args.startup,captain=0)",
    "assert qual['runtime']==ctx.receipt() and qual['previous_runtime']==bound['runtime']":
        "assert qual['runtime']==ctx.receipt()==bound['runtime'] and bound['complete_ARM9_COMMON_font_andactor0_macro_dependencies_qualified']",
    "assert prior['proposed_ARM9_sha256']==sha(ctx.arm)":
        "assert prior['runtime']['ARM9_sha256']==sha(ctx.arm)",
    "len(doc['records'])==len(bound['name_bindings'])==22":
        "len(doc['records'])==len(bound['name_bindings']) and {r['actor_ID'] for r in doc['records']}==set(bound['actors'])",
    "    cache={r['text']:deepcopy(r) for r in prior['planes']}":
        """    cache={};cacheorigins={}
    from dk4tool.rom.nds import NdsImage
    for cachepath in args.prior:
        cacheproof=load(cachepath)
        assert cacheproof['runtime']['ARM9_sha256']==sha(ctx.arm)
        cacheimage=NdsImage.open(cacheproof['runtime']['candidate'])
        assert cacheimage.read_file('/GRP/KANJI.FNT')==ctx.image.read_file('/GRP/KANJI.FNT')
        for plane in cacheproof['planes']:
            cache.setdefault(plane['text'],deepcopy(plane))
            cacheorigins.setdefault(plane['text'],cachepath)""",
    'dict(path=str(PRIOR),sha256=sha(PRIOR.read_bytes()),':
        'dict(path=str(cacheorigins[text]),sha256=sha(cacheorigins[text].read_bytes()),',
    'assert len(planes)==21 and fresh+reused==21':
        "assert len(planes)==len({r['english'] for r in doc['records']}) and fresh+reused==len(planes)",
    'scoped_actors=22,distinct_strings=21': "scoped_actors=len(doc['records']),distinct_strings=len(planes)",
    '[NAMES,BINDINGS,QUAL,PRIOR,RELEASE,Path(__file__)]': '[NAMES,BINDINGS,QUAL,*args.prior,RELEASE,args.startup,BASE,Path(__file__)]',
    "print(f'22actors/21strings:": "print(f'{len(actors)}actors/{len(planes)}strings:",
})
if __name__ == '__main__':
    exec(compile(source, __file__+'::same-complete-native-style11-and-exact-string-dependency-cache', 'exec'), globals())
