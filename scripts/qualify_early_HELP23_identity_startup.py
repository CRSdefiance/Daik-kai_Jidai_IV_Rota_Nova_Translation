"""Compare fresh own Rafael opening toreviewed parent;qualify only planned Help image identity."""
from pathlib import Path
from PIL import Image
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Early_HELP23_identity_coldboot_20261104')
PARENT=Path('work/analysis/Rafael_B61_B80_release_verified_20261104/own_registered_startup_verification.json')
PREP=Path('work/analysis/Early_HELP23_release_20261104/registered_preparation.json')
if __name__=='__main__':
    out=ROOT/'identity_RGB_qualification.json';assert not out.exists()
    report_path=ROOT/'capture_report.json';report,parent,prep=map(load,[report_path,PARENT,PREP])
    prior_path=Path(parent['capture_report']);assert sha(prior_path.read_bytes())==parent['capture_report_sha256'];prior=load(prior_path)
    assert report['frames']==prior['frames']==4001 and report['cold_boot'] and not report['savestate_loaded']
    assert not report.get('battery_save_preloaded') and not report['callback_errors']
    assert report['ROM_sha256']==prep['target_ROM_sha256']==sha(Path(report['ROM']).read_bytes())
    assert report['scripted_input_schedule']==prior['scripted_input_schedule'] and report['exact_requested_capture_frames']==prior['exact_requested_capture_frames']
    assert len(report['frames_captured'])==len(prior['frames_captured'])==10;matches=[]
    for a,b in zip(report['frames_captured'],prior['frames_captured'],strict=True):
        assert a['frame']==b['frame'] and sha(Path(a['path']).read_bytes())==a['PNG_sha256'] and sha(Path(b['path']).read_bytes())==b['PNG_sha256']
        aa,bb=[Image.open(r['path']).convert('RGB') for r in [a,b]];assert aa.size==bb.size and aa.tobytes()==bb.tobytes()
        matches.append(dict(frame=a['frame'],capture=a,prior_capture=b,byte_identical_to_prior_reviewed_RGB=True))
    current,previous=[NdsImage.open(r['ROM']) for r in [report,prior]]
    assert [p for _,p,v in previous.iter_files() if current.read_file(p)!=v]==['/COMMON/HELP.DK4']
    assert all(current.read_file(p)==v for p,v in previous.iter_components())
    save(out,dict(planned_ROM=report['ROM'],planned_ROM_sha256=report['ROM_sha256'],capture_report=str(report_path),capture_report_sha256=sha(report_path.read_bytes()),
        parent_startup=str(PARENT),parent_startup_sha256=sha(PARENT.read_bytes()),exact_RGB_pairs=matches,
        only_HELP_resource_differs_all_SC0_names_runtime_fonts_COMMON_graphics_andother_files_exact=True,
        existing_direct_startup_visual_review_reused_by_exact_ten_RGB_pairs=True,
        own_RAM_snapshot_available_butnative_context_binding_pending=True,registered_output_identity_manifest_patch_andcompletion_credit_still_pending=True,
        actual_coldboot_frames=4001,full_route=False,hardware=False,guide_photos=False,new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [report_path,PARENT,prior_path,PREP,Path(__file__)]}))
    print('Own4001-frame planned Help image matches all10 reviewed Rafael RGB frames;only Help changed. Final registered identity/patch/native RAM binding remain.')
