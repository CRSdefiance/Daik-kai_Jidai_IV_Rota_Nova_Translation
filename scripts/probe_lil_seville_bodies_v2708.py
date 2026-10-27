"""Conservative18-body layout/17native font probe;not full consumer approval."""
from dataclasses import replace
from pathlib import Path
from types import FunctionType
from PIL import Image,ImageDraw
from dk4tool.dialogue.encoder import encode_relocatable_dialogue
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_name_catalog_glyphs_v278 import raster as original_raster,expected_pixels
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Seville_body_probe_v2708')
DOC=Path('translations/lil_seville_encounter_editorial_manuscript_v1.json')
if __name__=='__main__':
    assert not ROOT.exists();doc=read(DOC);rom=NdsImage.open(doc['current_ROM']);arm=rom.read_file('/__arm9__.bin');assert sha(arm)==doc['required_runtime_ARM9_sha256']
    clean=NdsImage.open('work/clean.nds');assert clean.read_file('/GRP/KANJI.FNT')==rom.read_file('/GRP/KANJI.FNT')
    base=get_dialogue_profile('lil-opening-editorial-native-v1');profile=replace(base,name='Seville-body-research-only-not-registered',leading_speaker_bytes=frozenset({2,4,16,20,31,254}))
    class FontROM:
        @staticmethod
        def open(path):assert str(path)=='work/clean.nds';return rom
    raster=FunctionType(original_raster.__code__,{**original_raster.__globals__,'NdsImage':FontROM},argdefs=original_raster.__defaults__);raster.__kwdefaults__=original_raster.__kwdefaults__
    ROOT.mkdir(parents=True);rows=[];pictures=[];failures=[]
    for row in doc['records']:
        try:
            result=encode_relocatable_dialogue(bytes.fromhex(row['source_hex']),row['english'],profile)
            assert result.encoded[0]==int(row['source_presentation_prefix_hex'],16) and not any(d.severity in ['warning','error'] for d in result.diagnostics)
            case=dict(id=row['id'],kind=row['kind'],encoded_hex=result.encoded.hex(),formatted_markup=result.formatted_markup,diagnostics=[dict(severity=d.severity,code=d.code,message=d.message) for d in result.diagnostics],
                conservative216px_four_row_body_layout_pass=True,source_native_macro_alignment_and_UI_consumer_approval_pending=True)
            if row['kind']=='progressive':
                body=result.encoded[1:].replace(b'FI',b'Lil').replace(b'FA',b'Argot').replace(b'FO',b'Argot Co.')
                pixels,events,font=raster(arm,body);assert pixels==expected_pixels(arm,font,events)
                visible=[e for e in events if e['code']!=32]
                assert [e['code'] for e in visible]==[ord(c) for c in body.decode('ascii') if c not in ' \n']
                assert all(0<=e['x']<=210 and 0<=e['y']<=48 and e['y']%16==0 for e in visible)
                assert len(visible)==len({(e['x'],e['y']) for e in visible})
                origins={y:min(e['x'] for e in visible if e['y']==y) for y in sorted({e['y'] for e in visible})};assert all(x==0 for x in origins.values())
                path=ROOT/(row['id']+'_controlled_body.png');im=Image.new('RGB',(216,64));colors={0:(239,232,201),1:(0,8,0),15:(98,97,98)};im.putdata([colors[p] for p in pixels]);im.save(path);pictures.append((row['id'],row['speaker'],im))
                case.update(host_default_macro_expansion_used_before_paint=True,not_native_macro_context_execution=True,expanded_hex=body.hex(),complete_native_independent_plane_equal=True,whole_native_font_plane_sha256=sha(pixels),complete_glyph_events=events,visible_origins_by_row=origins,preview=str(path),preview_sha256=sha(path.read_bytes()))
            else:case.update(FE_full228x48_mode1_paper_and_pagination_still_pending=True,not_a_progressive_font_claim=True)
            rows.append(case)
        except (ValueError,AssertionError) as error:failures.append(dict(id=row['id'],type=type(error).__name__,error=str(error)))
    sheets=[]
    for start in range(0,len(pictures),8):
        sheet=Image.new('RGB',(920,640),'#263238');draw=ImageDraw.Draw(sheet)
        for i,(ident,speaker,im) in enumerate(pictures[start:start+8]):
            x,y=i%2*460,i//2*160;draw.text((x+5,y+3),ident+' / '+speaker,fill='white');sheet.paste(im.resize((432,128),Image.Resampling.NEAREST),(x+5,y+24))
        path=ROOT/f'body_only_sheet{start//8+1}.png';sheet.save(path);sheets.append(dict(path=str(path),sha256=sha(path.read_bytes())))
    save(ROOT/'body_only_layout_and_native_fonts.json',dict(candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],ARM9_sha256=sha(arm),manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),records=rows,failures=failures,review_sheets=sheets,visual_review_pending=True,
        expected_body_records=18,expected_progressive_planes=17,actual_progressive_planes=len(pictures),host_default_macro_substitution_not_native_macro_execution=True,scoped_profile_is_research_only_not_global_or_registered=True,
        FE_paper_typed_choices_current_native_macro_contexts_reference_maps_and_release_still_pending=True,source_prose_credit_added=0,completion_credit_added=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Body-only probe:',len(rows),'layout cases,',len(pictures),'native progressive planes;failures:',failures)
