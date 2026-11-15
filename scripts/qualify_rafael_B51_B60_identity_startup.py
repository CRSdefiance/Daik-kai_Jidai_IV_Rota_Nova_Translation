"""Reuse exact reviewed startup RGB on the planned identity; do not preapprove registration/RAM."""
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from PIL import Image
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Rafael_B51_B60_identity_coldboot_20261104')
PARENT=Path('work/analysis/Shared_tutorial_name_data_release_verified_20261104/own_registered_startup_verification.json')
COMPOSITION=Path('work/analysis/Rafael_B51_B60_focused_20261104/composition.json')

if __name__=='__main__':
    output=ROOT/'identity_RGB_qualification.json';assert not output.exists()
    report_path=ROOT/'capture_report.json';report,parent,composition=map(load,[report_path,PARENT,COMPOSITION])
    prior_path=Path(parent['capture_report']);assert sha(prior_path.read_bytes())==parent['capture_report_sha256']
    prior=load(prior_path)
    assert report['frames']==prior['frames']==4001 and report['cold_boot'] and not report['savestate_loaded']
    assert not report.get('battery_save_preloaded') and not report['callback_errors']
    assert report['ROM_sha256']==composition['research_ROM_sha256']==sha(Path(report['ROM']).read_bytes())
    assert report['scripted_input_schedule']==prior['scripted_input_schedule'] and report['exact_requested_capture_frames']==prior['exact_requested_capture_frames']
    assert len(report['frames_captured'])==len(prior['frames_captured'])==10
    matches=[]
    for current,previous in zip(report['frames_captured'],prior['frames_captured'],strict=True):
        assert current['frame']==previous['frame']
        a,b=Path(current['path']),Path(previous['path'])
        assert sha(a.read_bytes())==current['PNG_sha256'] and sha(b.read_bytes())==previous['PNG_sha256']
        aa,bb=Image.open(a).convert('RGB'),Image.open(b).convert('RGB')
        assert aa.size==bb.size and aa.tobytes()==bb.tobytes()
        matches.append(dict(frame=current['frame'],capture=current,prior_capture=previous,RGB_sha256=sha(aa.tobytes()),byte_identical_to_prior_reviewed_RGB=True))
    current,previous=NdsImage.open(report['ROM']),NdsImage.open(prior['ROM'])
    assert [p for _,p,v in previous.iter_files() if current.read_file(p)!=v]==['/data/SC0.DK4']
    assert [p for p,v in previous.iter_components() if current.read_file(p)!=v]==['/__arm9__.bin']
    before,after=[IlnkContainer.parse(im.read_file('/data/SC0.DK4')).blocks for im in [previous,current]]
    assert [i for i,(a,b) in enumerate(zip(before,after,strict=True)) if a!=b]==list(range(51,61))
    plan=composition['name_plan'];inverse=bytearray(current.read_file('/__arm9__.bin'))
    for field in plan['fields']:
        at,n=field['physical_offset'],field['owned_bytes']
        assert inverse[at:at+n].hex()==field['new_hex'];inverse[at:at+n]=bytes.fromhex(field['old_hex'])
    assert bytes(inverse)==previous.read_file('/__arm9__.bin')
    save(output,dict(planned_ROM=report['ROM'],planned_ROM_sha256=report['ROM_sha256'],capture_report=str(report_path),capture_report_sha256=sha(report_path.read_bytes()),
        parent_startup=str(PARENT),parent_startup_sha256=sha(PARENT.read_bytes()),exact_RGB_pairs=matches,
        original_opening_SC0_B44_EV0_COMMON_fonts_all_unowned_files_andcode_exact=True,
        only_ten_later_scene_blocks_andexclusive_Fernan_field_differ=True,
        existing_direct_startup_visual_review_reused_by_exact_ten_RGB_pairs=True,
        own_RAM_snapshot_available_butnative_context_binding_pending=True,
        registered_output_identity_manifest_patch_andcompletion_credit_still_pending=True,
        actual_coldboot_frames=4001,full_route=False,hardware=False,guide_photos=False,new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [report_path,PARENT,prior_path,COMPOSITION,Path(__file__)]}))
    print('4001-frame own planned-identity startup matches all10 reviewed RGB frames;only ten later scenes/Fernan field differ. Registered identity/RAM binding pending.',flush=True)
