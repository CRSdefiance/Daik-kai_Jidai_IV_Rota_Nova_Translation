"""Bind inherited M26/FE rules to actual wedding pixels; no new gameplay run."""
from pathlib import Path
import struct
from PIL import Image
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.xdelta import apply_xdelta
from dk4tool.patch.grand_race_menu_release import sha
from scripts.lil_kuhn_china_FE_painter_v2909 import make_painter
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Homecoming_Ian_wedding_contract_v3006')
SOURCE=Path('work/analysis/lil_Homecoming_Ian_source_v3002/complete172_clean_current_native_context.json')
HISTORY=Path('work/analysis/wedding_playback_v677/proof.json')
if __name__=='__main__':
    assert not ROOT.exists();source,history=map(read,[SOURCE,HISTORY])
    patch=Path('out/all_routes_combined_v666_candidate.xdelta');manifest=Path('out/all_routes_combined_v666_candidate.manifest.json')
    old_manifest=read(manifest);assert old_manifest['candidate_sha256']==history['candidate_sha256']
    ROOT.mkdir(parents=True);recovered=ROOT/'historical_V666_exact_patch_reconstruction_RESEARCH_ONLY.nds'
    # Historical ROM was already absent before this work. Reconstruct its exact
    # verified bytes from the retained clean-input patch; keep the recovered ROM.
    clean=Path('work/clean.nds');clean_sha=sha(clean.read_bytes())
    apply_xdelta(clean,patch,recovered)
    assert sha(recovered.read_bytes())==history['candidate_sha256'] and sha(clean.read_bytes())==clean_sha
    old,current,original=[NdsImage.open(p) for p in [recovered,source['current_ROM'],clean]]
    arm=current.read_file('/__arm9__.bin');old_arm=old.read_file('/__arm9__.bin')
    rp=Path(history['four_successful_runs']['fixture_baseline']['path']);assert sha(rp.read_bytes())==history['four_successful_runs']['fixture_baseline']['sha256']
    report=read(rp);snap=report['read_only_RAM_snapshot'];raw=Path(snap['path']).read_bytes();assert sha(raw)==snap['sha256'] and len(raw)==0x400000
    spans=[(0x5473C,0x54798),(0x5479C,0x54804),(0x2A0F8,0x2A148),(0x28A28,0x28A90),(0xD5088,0xD508C),(0xD19B8,0xD19BC)]
    for lo,hi in spans:assert old_arm[lo:hi]==raw[lo:hi]==arm[lo:hi]
    font=current.read_file('/GRP/KANJI.FNT');assert old.read_file('/GRP/KANJI.FNT')==font
    fontbase=struct.unpack_from('<I',arm,0xD19B8)[0]
    assert raw[fontbase-0x02000000:fontbase-0x02000000+len(font)]==font
    assets=[]
    for _,path,data in old.iter_files():
        if not path.upper().rsplit('/',1)[-1].startswith('M26.'):continue
        assert data==current.read_file(path)==original.read_file(path)
        assets.append(dict(path=path,bytes=len(data),sha256=sha(data)))
    assert assets
    old_block=IlnkContainer.parse(old.read_file('/data/SC2.DK4')).blocks[70]
    now_block=IlnkContainer.parse(current.read_file('/data/SC2.DK4')).blocks[70]
    assert len(old_block)==len(now_block)==6764
    assert struct.unpack_from('<H',old_block,4324)[0]==struct.unpack_from('<H',now_block,4324)[0]==0x4906
    before,after=old_block.split(b'\0'),now_block.split(b'\0')
    assert [i for i,(a,b) in enumerate(zip(before,after,strict=True)) if a!=b]==[397,615]
    text=before[626];assert text[:1]==b'\xfe' and text[1:].isascii() and not text[1:].startswith((b'\n',b' '))
    paint,calibration=make_painter(current);native=paint(text[1:])
    capture=report['frames_captured'][-1];cp=Path(capture['path']);assert capture['frame']==16000 and sha(cp.read_bytes())==capture['PNG_sha256']
    rgb=Image.open(cp).convert('RGB')
    wanted={(16+i%228,296+i//228) for i,v in enumerate(native['physical']) if v}
    actual={(x,y) for y in range(296,360) for x in range(16,244) if rgb.getpixel((x,y))==(0,8,0)}
    assert wanted==actual and native['complete_return_input_object_canaries_and_native_independent_plane_equal']
    rows=[r for r in source['records'] if r['kind']=='system-FE'];assert len(rows)==14
    staged=[r for r in rows if r['source_Japanese'].startswith('\n')];assert len(staged)==5
    movie=next(c for c in source['blocks'][0]['all_clean_native_commands'] if c['word']==0x4906);assert movie['offset']==4324
    save(ROOT/'historical_actual_wedding_FE_and_M26_source_contract.json',dict(current_ROM=source['current_ROM'],current_ROM_sha256=source['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),
        historical_proof=str(HISTORY),historical_proof_sha256=sha(HISTORY.read_bytes()),historical_ROM_recovered=str(recovered),historical_ROM_sha256=sha(recovered.read_bytes()),historical_clean_input_patch=str(patch),historical_patch_sha256=sha(patch.read_bytes()),historical_manifest=str(manifest),historical_manifest_sha256=sha(manifest.read_bytes()),
        actual_report=str(rp),actual_report_sha256=sha(rp.read_bytes()),actual_readonly_RAM=snap,actual_first_wedding_FE_capture=capture,historical_capture_viewed=True,historical_fixture_R1_22_to70_unearned_not_new_current_gameplay=True,
        current_owned_FE_callee_chapter_handler_and_font_literal_spans_equal_historical_ROM_and_actual_RAM=[dict(start=lo,end=hi,sha256=sha(arm[lo:hi])) for lo,hi in spans],current_complete_font_equals_historical_ROM_and_actual_resident_RAM=True,
        historical_body_hex=text.hex(),current_native_paint_of_historical_first_wedding_body_complete_ink_and_blank_mask_equals_actual=True,current_native_complete_physical_plane_sha256=sha(native['physical']),
        independent_current_typed_paper_calibration=calibration,logical_geometry=[228,48],physical_geometry=[228,64],actual_first_text_origin=[16,296],
        original_M26_assets_every_byte_equal_clean_historical_and_current=assets,original_chapter_movie_word=0x4906,source_movie_offset=4324,original_chapter6_requests_M26=[26,0,1,0],historical_all152_complete_original_M26_compositions_bound=True,
        current_B70_only_differs_from_historical_in_two_previously_validated_V678_records=[397,615],all14_FE_panels_source_mapped=True,five_Japanese_vertically_staged_FE_IDs=[r['id'] for r in staged],
        formatting_policy='Existing actual wedding English already begins at the normal first lower-screen row with M26 exclusively above. Do not recreate Japanese leading LF/fullwidth-space alignment in authored English. Keep14distinct source panels,including the conditional departure fragment,one FI macro andunlabeled wedding exchanges. Use calibrated source-bound automatic ordinary/FE formatting. Fresh complete current target-font/pagination proof remains required for all172 speeches. The source movie command andits mapped cursor/argument contract must remain exact after relocation.',
        later_relocated_M26_cursor_and_argument_verification_required=True,no_new_ROM_release_registry_ledger_or_editorial_credit=True,no_new_RGB_gameplay_capture_or_hardware_claim=True,new_emulator_runs=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    (ROOT/'RESEARCH_ONLY.txt').write_text('Historical V666 exact clean-input patch reconstruction, retained for source-bound wedding evidence. Not a construction parent or current release. Keep this ROM.\n',encoding='utf-8')
    print('HistoricalV666 recovered exactly. Current FE native plane matches whole actual first-wedding ink/blank mask;M26 assets/font/owned consumer bytes unchanged. No new gameplay;target prose/fonts/relocated movie contract pending.')
