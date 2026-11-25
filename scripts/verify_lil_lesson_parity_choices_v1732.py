"""Native parity-space preservation and complete four choice-label glyph planes."""
import struct
from pathlib import Path
from PIL import Image
from ndspy.code import MainCodeFile
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import execute_scene_caption_raster as modal
from scripts.verify_name_catalog_glyphs_v278 import raster,expected_pixels
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_lesson_parity_choices_v1732')


if __name__=='__main__':
    assert not ROOT.exists()
    research=read('work/analysis/lil_lesson_relocation_v1731/nested_source_relocation_research.json')
    font=read('work/analysis/lil_lesson_layout_v1725/all60_native_font_reconciliation.json')
    fonts={r['id']:r for r in font['cases']}
    source_proof=read('work/analysis/lil_lesson_fonts_v1724c/native_consumer_and_font_research.json')
    image=NdsImage.open(research['candidate']);arm=image.read_file('/__arm9__.bin')
    code=MainCodeFile(arm,0x02000000);itcm=code.sections[4]
    word=struct.unpack_from('<I',itcm.data,0xF24)[0];delta=word&0xFFFFFF
    if delta&(1<<23):delta-=1<<24
    alignment_entry=0x01FFCF24+8+4*delta;assert alignment_entry==0x0239B104
    env={**modal.__dict__,'MODAL_STAGED':bytes(code.sections[3].data[:-48]),
        'MODAL_CURSOR':source_proof['native_staged_cursor_helper'],
        'MODAL_CURSOR_BYTES':bytes.fromhex(source_proof['native_staged_cursor_helper_hex']),
        'MODAL_ITCM_START':itcm.ramAddress,'MODAL_ITCM':bytes(itcm.data),
        'MODAL_ALIGN_START':alignment_entry,'MODAL_ALIGN_BYTES':bytes.fromhex(source_proof['source_alignment_helper_hex'])}
    adapter=Path('work/analysis/lil_lesson_fonts_v1724c/scoped_modal_adapter_source.txt')
    exec(compile(adapter.read_text(encoding='utf-8'),str(adapter),'exec'),env)
    ROOT.mkdir(parents=True);parity=[];choices=[]
    for block in research['blocks']:
        for row in block['text_records']:
            if not row['parity_space_added']:continue
            case=fonts[row['id']];body=bytes.fromhex(row['target_hex'])[1:].replace(b'FI',b'Lil')
            assert body==bytes.fromhex(case['native_expanded_hex'])+b' '
            if case['consumer']=='original_FE_modal_548A8':
                pixels=env['execute'](arm,body.decode('ascii'),modal=True,modal_guarded=True,audit_modal_legacy_guards=True,mode=16)['pixels']
            else:
                pixels,events,kanji=raster(arm,body);assert pixels==expected_pixels(arm,kanji,events)
            assert sha(pixels)==case['native_font_plane_sha256']
            parity.append({'id':row['id'],'whole_native_font_plane_equal_before_after_added_parity_space':True,
                'native_plane_sha256':sha(pixels),'FE_actual_context_geometry_not_inferred':case['consumer']=='original_FE_modal_548A8'})
    menu=read('translations/lil_lesson_choices_editorial_draft_v1.json')
    for row in menu['records']:
        text=row['english'].encode('ascii');pixels,events,kanji=raster(arm,text)
        assert pixels==expected_pixels(arm,kanji,events)
        assert [e['code'] for e in events if e['code']!=32]==[c for c in text if c!=32]
        assert all(e['y']==0 and 0<=e['x']<=210 for e in events if e['code']!=32)
        expected=[(c,6*n,0) for n,c in enumerate(text) if c!=32]
        assert [(e['code'],e['x'],e['y']) for e in events if e['code']!=32]==expected
        im=Image.new('RGB',(216,64));colors={0:(239,232,201),1:(0,8,0),15:(98,97,98)}
        im.putdata([colors[v] for v in pixels]);path=ROOT/(row['id']+'.png');im.save(path)
        choices.append({'id':row['id'],'text':row['english'],'complete_first_last_and_all_internal_native_glyphs':True,
            'native_independent_font_plane_sha256':sha(pixels),'preview':str(path),'preview_sha256':sha(path.read_bytes()),
            'original_choice_UI_alignment_highlight_viewport_and_actual_selected_branch_pending':True})
    save(ROOT/'native_parity_and_choice_labels.json',{'candidate':research['candidate'],'candidate_sha256':research['candidate_sha256'],
        'all_selected_parity_spaces_repaint_identically':True,'parity_cases':parity,'choice_label_cases':choices,
        'native_choice_pointer_count_contract':'work/analysis/lil_lesson_choices_v1718/native_two_choice_labels.json',
        'FE_actual_metric_and_choice_UI_native_consumer_and_complete_revised_scene_pending':True,
        'no_ROM_registry_or_completion_change':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print({'parity_spaces_full_plane_exact':len(parity),'complete_native_choice_labels':len(choices)},flush=True)
