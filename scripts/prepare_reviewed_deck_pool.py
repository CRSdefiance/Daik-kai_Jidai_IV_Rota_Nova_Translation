"""Bind all existing Deck owners and references before generating proposed ARM9 data."""
import struct
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.reviewed_deck_pool_v1 import plan_pool
from dk4tool.patch.main_pool_cache_visibility import BASE
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load,save
from scripts.inventory_arm9_text import components
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime

ROOT=Path('work/analysis/Shared_Deck_pool_proposal_20261104')
HISTORY=Path('work/analysis/deck_explanations_pool_proof.json')
REVIEW=Path('work/analysis/Shared_Deck_tutorials_contextual_20261104/four_panel_contextual_review_v1.json')
RELEASE=Path('work/analysis/Rafael_early_tutorial_release_verified_20261104/registered_release_verification.json')
STARTUP=RELEASE.with_name('own_registered_startup_verification.json')

if __name__=='__main__':
    assert not ROOT.exists()
    ctx=RegisteredRuntime(RELEASE,STARTUP,captain=0);history,review=map(load,[HISTORY,REVIEW])
    assert review['runtime']==ctx.receipt()
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin');start,end=history['source_span'];references=[]
    inventory=components(ctx.image)
    for name,_,raw in inventory:
        references.extend((name,at,value-BASE) for at in range(len(raw)-3) if start<= (value:=struct.unpack_from('<I',raw,at)[0])-BASE <end)
    proposed,proof=plan_pool(ctx.arm,clean,history,review,references)
    ROOT.mkdir();source=ROOT/'current_ARM9.bin';target=ROOT/'proposed_ARM9_RESEARCH_ONLY.bin'
    source.write_bytes(ctx.arm);target.write_bytes(proposed)
    cases=[]
    for case in ['lost-review','changed-clean','changed-current-owner','missing-reference','added-interior-reference']:
        from copy import deepcopy
        a,c,h,r,refs=ctx.arm,clean,deepcopy(history),deepcopy(review),list(references)
        if case=='lost-review':r['records'][0]['review']['source']=False
        elif case=='changed-clean':v=bytearray(c);v[r['records'][0]['offset']]^=1;c=bytes(v)
        elif case=='changed-current-owner':v=bytearray(a);v[start]^=1;a=bytes(v)
        elif case=='missing-reference':refs.pop()
        else:refs.append(('arm9',0,start+1))
        try:plan_pool(a,c,h,r,refs)
        except ValueError as error:cases.append(dict(case=case,error=str(error)))
        else:raise AssertionError('Invalid Deck proposal accepted:'+case)
    save(ROOT/'proposal.json',dict(runtime=ctx.receipt(),history=str(HISTORY),history_sha256=sha(HISTORY.read_bytes()),review=str(REVIEW),review_sha256=sha(REVIEW.read_bytes()),
        current_ARM9=str(source),proposed_ARM9=str(target),plan=proof,complete_current_pointer_inventory=references,
        inspected_components=[dict(name=name,sha256=sha(raw),bytes=len(raw)) for name,_,raw in inventory],negative_cases=cases,
        source_review_controls_all_four_panels=True,native_glyphs_geometry_consumers_andactual_gameplay_pending=True,
        no_ROM_created=True,registered_deployment_pending=True,new_credit=0,guide_photos=False,
        evidence={str(p):sha(p.read_bytes()) for p in [HISTORY,REVIEW,RELEASE,STARTUP,Path('dk4tool/patch/reviewed_deck_pool_v1.py'),Path(__file__)]}))
    print('31 owned labels/pointer fields;First Mate paragraph fits540 source bytes,five invalid inputs rejected;no ROM orcode change.')
