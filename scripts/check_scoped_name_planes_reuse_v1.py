"""Reuse approved exact name planes while preserving all fresh style11 native guards."""
import argparse
from copy import deepcopy
import inspect
from pathlib import Path
import sys
from PIL import Image
from dk4tool.rom.nds import NdsImage
from scripts import check_scoped_name_planes_current_v1 as previous
from scripts.audit_story_glyph_consistency import load
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.source_locked_derivation_v5118 import checked_text


def main():
    ap=argparse.ArgumentParser(description=__doc__,add_help=False)
    ap.add_argument('--prior',type=Path,nargs='+',required=True)
    ap.add_argument('--prior-approval',type=Path,nargs='+',required=True)
    args,remaining=ap.parse_known_args();assert len(args.prior)==len(args.prior_approval)
    cache={};origins={}
    for path,approvalpath in zip(args.prior,args.prior_approval,strict=True):
        proof,approval=map(load,[path,approvalpath]);assert approval['names_sha256']==digest(path)
        assert any(v is True and 'name' in k and 'directly_viewed' in k for k,v in approval.items())
        assert digest(proof['runtime']['candidate'])==proof['runtime']['candidate_sha256']
        image=NdsImage.open(proof['runtime']['candidate'])
        for plane in proof['planes']:
            assert plane['complete_first_internal_final_codes_bounds_andindependent_font_pixels_pass']
            assert digest(plane['native_plane'])==plane['native_plane_sha256'] and digest(plane['preview'])==plane['preview_sha256']
            cache.setdefault(plane['text'],deepcopy(plane))
            origins.setdefault(plane['text'],dict(path=path,approval=approvalpath,runtime=proof['runtime'],image=image))
    source=checked_text(inspect.getsource(previous.main),{
        "    reviewed={r['actor_ID']:r for r in review['records']}":
            "    for row in review['records']:\n        if 'current_reference' not in row:row['current_reference']=dict(candidate_sha256=receipt['candidate_sha256'],file_path='/__arm9__.bin',exact_original_getter_binding=True)\n    reviewed={r['actor_ID']:r for r in review['records']}",
        "    for text in sorted({r['text'] for r in consumers}):":
            """    fresh=reused=0
    for text in sorted({r['text'] for r in consumers}):
        if text in CACHE:
            origin=ORIGINS[text];old=origin['image']
            assert old.read_file('/__arm9__.bin')==ctx.arm and old.read_file('/GRP/KANJI.FNT')==ctx.image.read_file('/GRP/KANJI.FNT')
            plane=deepcopy(CACHE[text]);plane['exact_previous_native_plane_reuse']=dict(path=str(origin['path']),sha256=digest(origin['path']),previous_visual_approval=str(origin['approval']),previous_visual_approval_sha256=digest(origin['approval']),complete_ARM9_font_andtext_exact=True)
            planes.append(plane);pictures.append((text,Image.open(plane['preview']).convert('RGB')));reused+=1
            continue
        fresh+=1""",
        '        direct_visual_review_pending=True,no_new_actual_headers_orconditional_role_assignment=True,':
            "        fresh_native_name_strings=fresh,reused_native_name_strings=reused,\n        direct_visual_review_pending=True,no_new_actual_headers_orconditional_role_assignment=True,",
        '[args.name_review,args.bindings,Path(__file__)]':'[args.name_review,args.bindings,*CACHE_PATHS,*APPROVAL_PATHS,Path(__file__)]',
        "len(planes),'fresh name strings;direct view pending.'":"fresh,'fresh/',reused,'reused name strings;direct view pending.'",
    })
    env={**previous.main.__globals__,**globals(),'CACHE':cache,'ORIGINS':origins,'CACHE_PATHS':args.prior,'APPROVAL_PATHS':args.prior_approval,'__file__':__file__}
    exec(compile(source,__file__+'::same-native-style11-instructions-codes-pixels-bounds-exact-plane-reuse','exec'),env)
    sys.argv=[sys.argv[0],*remaining];env['main']()


if __name__=='__main__':main()
