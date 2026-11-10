"""Fifteen original progressive Japanese paragraphs andfour complete original-style11 names."""
import inspect
from pathlib import Path
from PIL import Image
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.papal_trade_route_native_context_v7626 import RouteCurrentContext
from scripts.generic_name_macro_owned_v5886b import expand
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.research_lil_B209_native_pages_v6461 import pages as old_pages
from scripts.square_shopkeeper_font_oracles_v7020 import expected_pixels
from scripts.prove_lil_B208_name_planes_v6405 import codes,original_name_events
from scripts import lil_B207_name_style_v6354d as name_source
from scripts.Rafael_B45_FE_source_painter_v7894 import make_source_painter
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B47_source_name_planes_v7986')
CURRENT=Path('work/analysis/Rafael_B47_current_v7980/all15_complete_source_current_refs_before_new_English_manuscript.json')
EFFECTIVE=Path('work/analysis/Rafael_B47_effective_v7981/all15_effective_English_templates30_original_progressive_dispatches.json')
NAMES=Path('work/analysis/Rafael_B47_names_v7976/four_static_speakers_eight_getters_clean_fields16_synthetic_macro_alignments.json')
NATIVE=Path('work/analysis/Rafael_B47_pages_v7985/15_complete_native_paragraphs16_pages60_compiled_alignments.json')
LOGICAL=Path('work/analysis/Rafael_B47_logical_v7983/15_logical_paragraphs60_original_native_progressive_alignments.json')
if __name__=='__main__':
    assert not ROOT.exists();current,effective,names,native,logical=map(read,[CURRENT,EFFECTIVE,NAMES,NATIVE,LOGICAL])
    image=NdsImage.open(current['current_ROM']);arm,font=image.read_file('/__arm9__.bin'),image.read_file('/GRP/KANJI.FNT')
    assert sha(arm)==current['current_ARM9_sha256']=='2b6aaaa499d634be9afc255d1c39b64ef0f578283c9768c525b31e34499abd0a'
    pe={**old_pages.__globals__,'expected_pixels':expected_pixels,'codes':codes}
    exec(compile(native['source_owned_progressive_page_adapter'],__file__+'::complete-original-progressive-CP932-pages','exec'),pe)
    ne=dict(expand.__globals__);exec(compile(logical['source_owned_progressive_adapter'],__file__+'::own-Rafael-name-literal-macros','exec'),ne)
    style_adapter=checked_text(inspect.getsource(name_source.style_source_proof),{'assert sha(arm)==ARM9;':'assert sha(arm)==CURRENT_ARM9;'})
    se={**name_source.__dict__,'CURRENT_ARM9':sha(arm)}
    exec(compile(style_adapter,__file__+'::current-original-style11','exec'),se)
    exec(compile(inspect.getsource(name_source.native_name_raster),__file__+'::original-current-name-raster','exec'),se)
    assert font==NdsImage.open('work/clean.nds').read_file('/GRP/KANJI.FNT')
    assert all(r['source_selector']!=254 for r in current['records'])
    FE_calibration=dict(unused='B47 has no FE source ornew FE coverage')
    ROOT.mkdir(parents=True);ctx=RouteCurrentContext(names['current_native_input'],'unused-no-historical-ROM',ROOT/'current_context')
    nameplanes=[];sourcepages=[]
    for getter in names['native_eight_progressive_andfull_getters']['rows']:
        if getter['consumer']!='progressive-nameplate':continue
        text=getter['text'];raw=text.encode('ascii');actor=getter['actor_ID']
        result=ctx.execute(ne['expand'],raw,actor);ctx.machines.pop()
        assert len(result['cases'])==4 and all(c['output_hex']==raw.hex() for c in result['cases'])
        pixels,events,usedfont=se['native_name_raster'](arm,raw)
        assert pixels==expected_pixels(arm,usedfont,events)
        visible,flushes=original_name_events(events,raw);assert visible==codes(raw)
        plane=ROOT/f'actor{actor}_complete_name.bin';plane.write_bytes(pixels)
        nameplanes.append(dict(actor_ID=actor,text=text,input_hex=raw.hex(),native_alignment=result,
            native_plane=str(plane),native_plane_sha256=sha(pixels),events=events,original_zero_ink_flushes=flushes,
            original_pair_flush_width=(len(raw)+1)//2*12,original_source_style=11))
    for row in current['records']:
        case=next(c for c in effective['source_current_dispatches'] if c['id']==row['id'] and c['version']=='clean-Japanese')
        kind='unexecuted-FE-modal-body' if row['source_selector']==254 else 'unexecuted-progressive-body'
        body=bytes.fromhex(next(b for b in case['boundaries'] if b['kind']==kind)['text_hex'])
        source=bytes.fromhex(row['source_hex'])[1:]
        assert body==source.replace(b'FI',b'Rafael').replace(b'FA',b'Castor').replace(b'FO',b'Castor Co.')
        if row['source_selector']==254:
            rendered=FE(body);plane=ROOT/(row['id']+'_source_FE228x48.bin');plane.write_bytes(rendered.pop('logical'))
            physical=ROOT/(row['id']+'_source_FE228x64.bin');physical.write_bytes(rendered.pop('physical'))
            events=rendered['events']
            pages=[dict(page=1,start=0,end=len(body),native_plane=str(plane),native_plane_sha256=sha(plane.read_bytes()),
                physical_plane=str(physical),physical_plane_sha256=sha(physical.read_bytes()),events=events)]
            rendered.update(pages=pages,distinct_original_null_actor_FE_paper=True)
        else:
            rendered=pe['pages'](arm,font,body)
            for page in rendered['pages']:
                pixels=bytes.fromhex(page.pop('native_plane_hex'));plane=ROOT/(row['id']+f'_source_page{page["page"]}.bin');plane.write_bytes(pixels)
                page.update(native_plane=str(plane),native_plane_sha256=sha(pixels))
        sourcepages.append(dict(id=row['id'],file_path=row['file_path'],block=47,source_selector=row['source_selector'],
            source_reference=row['source_reference'],kind=row['kind'],source_body_hex=source.hex(),
            original_current_expanded_source_hex=body.hex(),**rendered))
    assert len(nameplanes)==4 and len(sourcepages)==15 and not ctx.machines
    assert sum(len(r['pages']) for r in sourcepages)==15
    save(ROOT/'15_complete_source_pages4_names16_literal_alignments_all_progressive.json',dict(
        candidate=current['current_ROM'],candidate_sha256=current['current_ROM_sha256'],ARM9_sha256=sha(arm),font_sha256=sha(font),
        name_planes=nameplanes,source_records=sourcepages,source_complete_native_pages=15,
        current_name_literal_alignment_cases=16,original_style11_name_planes_fresh=True,
        original_current_name_style_source_proof=se['style_source_proof'](arm),source_owned_name_style_adapter=style_adapter,
        source_owned_header_raster=inspect.getsource(name_source.native_name_raster),source_owned_macro_adapter=logical['source_owned_progressive_adapter'],
        source_owned_page_adapter=native['source_owned_progressive_page_adapter'],FE_source_calibration=FE_calibration,
        all15_original_Japanese_paragraphs_andzero_macros_preserved=True,
        all_native_complete_codes_glyph_planes_bounds_input_canaries_andconsumption_exact=True,
        no_FE_source_orFE_palette_coverage_claim_B47_all_progressive=True,
        offline_source_andname_planes_not_actual_orfull207_name_approval=True,
        actual_source_English_body_header_andR53_two_page_transition_audit_pending=True,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        evidence={str(p):sha(p.read_bytes()) for p in [CURRENT,EFFECTIVE,NAMES,NATIVE,LOGICAL,Path(name_source.__file__),Path(__file__),
            Path('scripts/Rafael_B45_FE_source_painter_v7894.py')]},
        new_emulator_runs=0,new_credit=0,full_goal_complete=False))
    print('15 complete clean-source progressive pages,four original-style11 names/16 literal alignments pass.Allcurrent glyphs andbounds exact;actual comparisons pending.')
