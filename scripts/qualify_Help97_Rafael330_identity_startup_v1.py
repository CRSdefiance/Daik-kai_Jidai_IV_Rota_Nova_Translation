"""Bind own planned4001-frame startup toten exact reviewed RGB pairs andonlytheowned resources."""
from pathlib import Path
from PIL import Image
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Help97_Rafael330_identity_coldboot_20261105')
PREP=Path('work/analysis/Help97_Rafael330_release_v2_20261105/registered_preparation.json')
PARENT=Path('work/analysis/Sea22_Fleet66_release_verified_20261105/own_registered_startup_verification.json')

if __name__=='__main__':
    out=ROOT/'identity_RGB_qualification.json';assert not out.exists()
    reportpath=ROOT/'capture_report.json';report,prep,parent=map(load,[reportpath,PREP,PARENT])
    priorpath=Path(parent['capture_report']);assert sha(priorpath.read_bytes())==parent['capture_report_sha256'];prior=load(priorpath)
    assert report['frames']==prior['frames']==4001 and report['cold_boot'] and not report['savestate_loaded']
    assert not report.get('battery_save_preloaded') and not report['callback_errors']
    assert report['ROM_sha256']==prep['target_ROM_sha256']==sha(Path(report['ROM']).read_bytes())
    assert report['scripted_input_schedule']==prior['scripted_input_schedule'] and report['exact_requested_capture_frames']==prior['exact_requested_capture_frames']
    assert len(report['frames_captured'])==len(prior['frames_captured'])==10
    matches=[]
    for now,before in zip(report['frames_captured'],prior['frames_captured'],strict=True):
        assert now['frame']==before['frame']
        a,b=Path(now['path']),Path(before['path'])
        assert sha(a.read_bytes())==now['PNG_sha256'] and sha(b.read_bytes())==before['PNG_sha256']
        x,y=Image.open(a).convert('RGB'),Image.open(b).convert('RGB')
        assert x.size==y.size and x.tobytes()==y.tobytes()
        matches.append(dict(frame=now['frame'],capture=now,prior_capture=before,RGB_sha256=sha(x.tobytes()),byte_identical_to_prior_reviewed_RGB=True))
    current,previous=NdsImage.open(report['ROM']),NdsImage.open(prior['ROM'])
    assert {p for (_,p,a),(_,q,b) in zip(previous.iter_files(),current.iter_files(),strict=True) if p!=q or a!=b}=={'/data/SC0.DK4','/COMMON/HELP.DK4'}
    assert all(current.read_file(p)==v for p,v in previous.iter_components())
    a,b=[IlnkContainer.parse(im.read_file('/data/SC0.DK4')).blocks for im in [previous,current]]
    assert [i for i,(x,y) in enumerate(zip(a,b,strict=True)) if x!=y]==[81,82,83,84]
    assert current.read_file('/data/EV0.DK4')==previous.read_file('/data/EV0.DK4')
    resource=current.read_file('/COMMON/HELP.DK4');plan=load(Path('work/analysis/Remaining_HELP67_formatting_20261105/production_plan_v1.json'))
    assert sha(resource)==plan['target_HELP_sha256']=='34f66ba368fba5db2fde81c7eb3e1db42e0efa8f8d733bd7ae654c5ddce1008c'
    pages=IlnkContainer.parse(resource).blocks
    first=load(Path('work/analysis/HELP31_active_terms_20261105/production_plan_v1.json'))
    for p in first['pages']+plan['pages']:assert pages[p['topic_id']].hex()==p['encoded_hex']
    assert len(first['pages'])+len(plan['pages'])==103
    save(out,dict(planned_ROM=report['ROM'],planned_ROM_sha256=report['ROM_sha256'],
        capture_report=str(reportpath),capture_report_sha256=sha(reportpath.read_bytes()),
        parent_startup=str(PARENT),parent_startup_sha256=sha(PARENT.read_bytes()),exact_RGB_pairs=matches,
        original_opening_SC0_B44_EV0_COMMON_fonts_all_unowned_files_andcode_exact=True,
        only_four_reviewed_SC0_blocks_andtwo_ordered_Help_groups_differ=True,
        all103_Help_pages_equal_individually_reviewed_target_bytes=True,
        existing_direct_startup_visual_review_reused_by_exact_ten_RGB_pairs=True,
        own_RAM_snapshot_available_butnative_context_binding_pending=True,
        registered_output_identity_manifest_patch_andcompletion_credit_still_pending=True,
        actual_coldboot_frames=4001,full_route=False,hardware=False,guide_photos=False,new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [reportpath,PREP,PARENT,priorpath,Path(__file__)]}))
    print('Own4001-frame planned startup matchesall10 reviewed RGB frames;fourSC0 blocks and103 Help pages bound. Final registered identity/RAM/patch stillpending.')
