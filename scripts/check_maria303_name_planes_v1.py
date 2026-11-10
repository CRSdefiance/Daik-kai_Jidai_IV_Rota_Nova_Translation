"""Reuse16 unchanged native name planes and freshly check eight strings on exact current dependencies."""
from copy import deepcopy
from pathlib import Path
import sys
from dk4tool.rom.nds import NdsImage
from PIL import Image
from scripts import check_scoped_name_planes_current_v1 as previous
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.source_locked_derivation_v5118 import checked_text
import inspect

ROOT=Path('work/Maria_B58_B70_clean_20261109')
PRIOR=Path('work/Maria_B51_B57_clean_20261109/name_planes_v1/native_name_planes.json')
PRIOR_APPROVAL=Path('work/Maria_B51_B57_clean_20261109/offline_display_approval_v1.json')

def main():
    review_path=ROOT/'name_inputs_v1/review.json';bindings_path=ROOT/'name_inputs_v1/bindings.json'
    assert not review_path.parent.exists() and not (ROOT/'name_planes_v1').exists()
    review_source=ROOT/'scoped20_names_editorial_review_v3.json'
    bound_source=ROOT/'scoped_names_macros_reference_v1.json';term_source=ROOT/'scoped_terms_reference_v1.json'
    review,bound,terms=map(load,[review_source,bound_source,term_source]);assert review['runtime']==bound['runtime']==terms['runtime']
    binding_rows=deepcopy(bound['records']);binding_rows.append(deepcopy(terms['spoken_Mihwa']))
    assert len(binding_rows)==20 and {r['actor_ID'] for r in binding_rows}=={r['actor_ID'] for r in review['records']}
    current=deepcopy(review)
    for row in current['records']:
        row['current_reference']=dict(candidate=review['runtime']['candidate'],candidate_sha256=review['runtime']['candidate_sha256'],
            file_path='/__arm9__.bin',source_native_bindings=str(bound_source if row['actor_ID']!=201 else term_source))
    review_path.parent.mkdir()
    save(review_path,current);save(bindings_path,dict(runtime=bound['runtime'],records=binding_rows,new_credit=0,
        evidence={str(p):digest(p) for p in [review_source,bound_source,term_source,Path(__file__)]}))
    prior=load(PRIOR);approval=load(PRIOR_APPROVAL)
    assert approval['all31_name_strings_directly_viewed'] and approval['names_sha256']==digest(PRIOR)
    image=NdsImage.open(bound['runtime']['candidate']);old=NdsImage.open(prior['runtime']['candidate'])
    assert image.read_file('/__arm9__.bin')==old.read_file('/__arm9__.bin')
    assert image.read_file('/GRP/KANJI.FNT')==old.read_file('/GRP/KANJI.FNT')
    cache={r['text']:r for r in prior['planes']}
    wanted={c['text'] for r in binding_rows for c in r['current_consumers']}
    assert (len(wanted),len(wanted&cache.keys()),len(wanted-cache.keys()))==(24,16,8)
    source=checked_text(inspect.getsource(previous.main),{
        "    for text in sorted({r['text'] for r in consumers}):":
        """    for text in sorted({r['text'] for r in consumers}):
        if text in CACHE:
            plane=deepcopy(CACHE[text])
            assert plane['complete_first_internal_final_codes_bounds_andindependent_font_pixels_pass']
            assert digest(plane['native_plane'])==plane['native_plane_sha256'] and digest(plane['preview'])==plane['preview_sha256']
            plane['exact_previous_native_plane_reuse']=dict(path=str(PRIOR),sha256=digest(PRIOR),
                previous_visual_approval=str(PRIOR_APPROVAL),previous_visual_approval_sha256=digest(PRIOR_APPROVAL),
                complete_ARM9_font_andtext_exact=True)
            planes.append(plane);pictures.append((text,Image.open(plane['preview']).convert('RGB')))
            continue""",
        "        direct_visual_review_pending=True,no_new_actual_headers_orconditional_role_assignment=True,":
        "        fresh_native_name_strings=8,reused_native_name_strings=16,previous_native_proof=str(PRIOR),previous_native_proof_sha256=digest(PRIOR),\n        direct_visual_review_pending=True,no_new_actual_headers_orconditional_role_assignment=True,",
    })
    env={**previous.main.__globals__,**globals(),'CACHE':cache}
    exec(compile(source,__file__+'::same-style11-complete-native-checks-with16-exact-plane-reuses','exec'),env)
    before=sys.argv[:]
    try:
        sys.argv=[__file__,'--name-review',str(review_path),'--bindings',str(bindings_path),'--out',str(ROOT/'name_planes_v1')]
        env['main']()
    finally:sys.argv=before
    proof=load(ROOT/'name_planes_v1/native_name_planes.json')
    assert (proof['actors'],proof['distinct_current_strings'],proof['fresh_native_name_strings'],proof['reused_native_name_strings'])==(20,24,8,16)
    print('Qualified20 actors/40 exact getter bindings;24 strings:16 compatible native planes reused,eight fresh. Direct visual review pending.')

if __name__=='__main__':main()
