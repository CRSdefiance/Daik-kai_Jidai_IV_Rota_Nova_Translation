"""Original clean-source body pages and eight exact progressive-name planes for actual audit."""
import inspect
from pathlib import Path
from PIL import Image
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.maria_unlocked_current_context_v7680 import MariaUnlockedCurrentContext
from scripts.generic_name_macro_owned_v5886b import expand
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.research_lil_B209_native_pages_v6461 import pages as old_pages
from scripts.square_shopkeeper_font_oracles_v7020 import expected_pixels
from scripts.prove_lil_B208_name_planes_v6405 import codes,original_name_events
from scripts import lil_B207_name_style_v6354d as name_source
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_confrontation_source_name_planes_v7810')
CURRENT=Path('work/analysis/maria_confrontation_current_v7789/all16_complete_source_current_refs_before_new_English_manuscript.json')
CONSUMERS=Path('work/analysis/maria_confrontation_effective_v7790/all16_effective_English_templates32_original_dispatches.json')
NAMES=Path('work/analysis/maria_confrontation_names_v7788/three_static_speakers_six_getters_clean_fields_source_macros.json')
PAGES=Path('work/analysis/maria_confrontation_row_reasons_v7801b/16_native_pages_exact_with_nine_individual_row_reasons.json')
INPUT=Path('work/analysis/current_V7779_native_v7782/route3/current_native_input.json')
if __name__=='__main__':
    assert not ROOT.exists();current,consumers,names,pages=map(read,[CURRENT,CONSUMERS,NAMES,PAGES])
    im=NdsImage.open(current['current_ROM']);arm,font=im.read_file('/__arm9__.bin'),im.read_file('/GRP/KANJI.FNT')
    assert sha(arm)==current['current_ARM9_sha256']=='2b6aaaa499d634be9afc255d1c39b64ef0f578283c9768c525b31e34499abd0a'
    pe={**old_pages.__globals__,'expected_pixels':expected_pixels,'codes':codes};exec(compile(pages['source_owned_native_page_adapter'],__file__+'::current-CP932-source-pages','exec'),pe)
    adapter=checked_text(inspect.getsource(expand),{'assert identity==prefix and captain==2':'assert identity==prefix and captain==3'})
    ne=dict(expand.__globals__);exec(compile(adapter,__file__+'::current-Maria-name-literal-ABI','exec'),ne)
    style_adapter=checked_text(inspect.getsource(name_source.style_source_proof),{'assert sha(arm)==ARM9;':'assert sha(arm)==CURRENT_ARM9;'})
    se={**name_source.__dict__,'CURRENT_ARM9':sha(arm)};exec(compile(style_adapter,__file__+'::exact-current-original-name-style11','exec'),se)
    exec(compile(inspect.getsource(name_source.native_name_raster),__file__+'::current-original-header-raster','exec'),se)
    ROOT.mkdir(parents=True);ctx=MariaUnlockedCurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context');nameplanes=[];sourcepages=[]
    getters=[r for r in names['native_six_progressive_and_full_name_consumers']['rows'] if r['consumer']=='progressive-nameplate']
    for getter in getters:
        text=getter['text'];raw=text.encode('ascii');actor=getter['actor_ID']
        native=ctx.execute(ne['expand'],raw,actor);ctx.machines.pop()
        assert all(c['output_hex']==raw.hex() for c in native['cases'])
        pixels,events,usedfont=se['native_name_raster'](arm,raw)
        assert pixels==expected_pixels(arm,usedfont,events)
        visible,flushes=original_name_events(events,raw);assert visible==codes(raw)
        plane=ROOT/f'actor{actor}_complete_name.bin';plane.write_bytes(pixels)
        picture=Image.new('RGB',(216,64));picture.putdata([(98,97,98) if b else (239,232,201) for b in pixels]);png=plane.with_suffix('.png');picture.save(png)
        nameplanes.append(dict(actor_ID=actor,text=text,input_hex=raw.hex(),native_alignment=native,native_plane=str(plane),native_plane_sha256=sha(pixels),
            preview=str(png),preview_sha256=sha(png.read_bytes()),events=events,original_zero_ink_flushes=flushes,
            original_pair_flush_width=(len(raw)+1)//2*12,original_source_style=11))
    for row in current['records']:
        case=next(r for r in consumers['source_current_dispatches'] if r['id']==row['id'] and r['version']=='clean-Japanese')
        body=bytes.fromhex(next(b for b in case['boundaries'] if b['kind']=='unexecuted-progressive-body')['text_hex'])
        source=bytes.fromhex(row['source_hex'])[1:];assert body==source.replace(b'FI',b'Maria').replace(b'FA',b'Li').replace(b'FO',b'Li Clan')
        rendered=pe['pages'](arm,font,body)
        for page in rendered['pages']:
            pixels=bytes.fromhex(page.pop('native_plane_hex'));plane=ROOT/(row['id']+f'_source_page{page["page"]}.bin');plane.write_bytes(pixels)
            picture=Image.new('RGB',(216,64));colors={0:(239,232,201),1:(0,8,0),15:(98,97,98)};picture.putdata([colors[b] for b in pixels])
            png=plane.with_suffix('.png');picture.save(png);page.update(native_plane=str(plane),native_plane_sha256=sha(pixels),preview=str(png),preview_sha256=sha(png.read_bytes()))
        sourcepages.append(dict(id=row['id'],file_path=row['file_path'],block=row['block'],source_selector=row['source_selector'],
            source_reference=row['source_reference'],source_body_hex=source.hex(),original_current_expanded_source_hex=body.hex(),**rendered))
        if len(sourcepages)%8==0:print('SOURCE_PAGES',len(sourcepages),flush=True)
    assert len(nameplanes)==3 and len(sourcepages)==16 and not ctx.machines
    save(ROOT/'16_clean_source_native_pages3_complete_name_planes12_literal_alignments.json',dict(
        candidate=current['current_ROM'],candidate_sha256=current['current_ROM_sha256'],ARM9_sha256=sha(arm),font_sha256=sha(font),
        name_planes=nameplanes,source_records=sourcepages,source_complete_native_pages=sum(len(r['pages']) for r in sourcepages),
        current_name_literal_alignment_cases=12,three_original_style11_progressive_name_planes_fresh=True,
        original_current_name_style_source_proof=se['style_source_proof'](arm),source_owned_name_style_adapter=style_adapter,
        source_owned_header_raster=inspect.getsource(name_source.native_name_raster),source_owned_macro_adapter=adapter,
        source_owned_page_adapter=pages['source_owned_native_page_adapter'],
        all16_original_Japanese_paragraphs_andmeasured_source_macros_preserved=True,
        all_native_codes_independent_glyph_planes_bounds_canaries_andconsumption_exact=True,
        offline_source_andname_font_checks_not_actual_scenes_orfull207_name_approval=True,
        source_andCP932_shadow_preview_colors_not_actual_palette_claim=True,actual_source_English_body_header_page_andtransition_audit_pending=True,
        existing_system_only_unlock_fixture=True,earned_unlock_verified=False,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        evidence={str(p):sha(p.read_bytes()) for p in [CURRENT,CONSUMERS,NAMES,PAGES,INPUT,Path(name_source.__file__),Path(__file__)]},
        new_emulator_runs=0,new_credit=0,full_goal_complete=False))
    print('PASS:16source paragraphs/pages',sum(len(r['pages']) for r in sourcepages),';3fresh complete original-style11 headers/12literal alignments.Actual audit pending.')
