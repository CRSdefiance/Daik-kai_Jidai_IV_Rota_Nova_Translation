"""Test the actual guarded35-cell continuation with unchanged codec/native font rules."""
from pathlib import Path
from types import FunctionType
from PIL import Image
from dk4tool.dialogue.codec import parse_markup,tokens_to_bytes
from dk4tool.dialogue.layout import lint_dialogue
from dk4tool.dialogue.lil_B208_profile_v1 import profile_for
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_build_native_context_v6261b import CurrentContext
from scripts.verify_lil_B174_fonts_v4470 import expand
from scripts.verify_name_catalog_glyphs_v278 import raster as inherited_raster
from scripts.shady_man_font_oracles_v6263 import expected_pixels
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B208_phase_capacity_v6411')
DOC=Path('translations/lil_B208_editorial_manuscript_v2.json')
if __name__=='__main__':
    assert not ROOT.exists();doc=read(DOC);ROOT.mkdir(parents=True);ctx=CurrentContext(doc['current_strict_native_input'],'unused-no-historical-ROM',ROOT/'current_context');block=IlnkContainer.parse(ctx.rom.read_file('/data/SC2.DK4')).blocks[208];profile=profile_for(ctx.arm,block)
    class FontROM:
        @staticmethod
        def open(p):assert str(p)=='work/clean.nds';return ctx.rom
    raster=FunctionType(inherited_raster.__code__,{**inherited_raster.__globals__,'NdsImage':FontROM},argdefs=inherited_raster.__defaults__);raster.__kwdefaults__=inherited_raster.__kwdefaults__
    row=next(r for r in doc['records'] if r['source_record_index']==36);real=['Oh, you want to get stronger?',"Then why not look for that pirate's",'prized sword?'];assert ' '.join(real)==row['english'].split('}',1)[1] and list(map(len,real))==[29,35,13]
    inputs=[('unchanged_B208_R36',real,bytes.fromhex(row['source_hex'])),('even34_then_odd35',['A'*34,'B'*35,'End.'],b'\xaaJapanese'),('odd35_then_odd35',['A'*35,'B'*35,'End.'],b'\xaaJapanese')];cases=[]
    for name,lines,raw in inputs:
        # Research-only prescribed breaks probe capacity;production manuscripts
        # remain one paragraph and must use an automatic source-bound planner.
        markup='{SPEAKER:AA}'+'{LB}'.join(lines);issues=lint_dialogue(raw,markup,profile);assert not [i for i in issues if i.severity=='error'];encoded=tokens_to_bytes(parse_markup(markup),guard_linebreaks=True,pair_phase_safe_breaks=True,macro_ascii_lengths=profile.macro_ascii_lengths);body=encoded[1:]
        native=ctx.execute(expand,body,170);ctx.machines.pop();assert all(c['output_hex']==body.hex() for c in native['cases'])
        pixels,events,font=raster(ctx.arm,body);assert pixels==expected_pixels(ctx.arm,font,events);visible=[e for e in events if e['code']!=32]
        assert [e['code'] for e in visible]==[b for b in body if b not in [10,32]] and len(visible)==len({(e['x'],e['y']) for e in visible}) and all(0<=e['x']<=210 and 0<=e['y']<=48 and e['y']%16==0 for e in visible)
        origins={y:min(e['x'] for e in visible if e['y']==y) for y in sorted({e['y'] for e in visible})};assert list(origins)==[0,16,32] and all(x==0 for x in origins.values())
        p=ROOT/(name+'.png');im=Image.new('RGB',(216,64));colors={0:(239,232,201),1:(0,8,0),15:(98,97,98)};im.putdata([colors[v] for v in pixels]);im.save(p)
        segments=body.split(b'\n');assert segments[1]==b' '+lines[1].encode('ascii') and len(segments[1])==36
        assert segments[0]==lines[0].encode('ascii')+(b' ' if len(lines[0])%2==0 else b'')
        cases.append(dict(case=name,research_markup=markup,logical_rows=lines,compiled_hex=encoded.hex(),compiled_row_hex=[s.hex() for s in segments],native_macro_cases=native,all_complete_independent_glyphs_canaries_bounds_origins_and_three_rows_equal=True,native_events=events,whole_native_plane_sha256=sha(pixels),preview=str(p),preview_sha256=sha(p.read_bytes()),prescribed_breaks_are_offline_capacity_probes_not_authored_manuscript_layout=True))
    bad='{SPEAKER:AA}'+'A'*36+'{LB}End.';diagnostics=lint_dialogue(b'\xaaJapanese',bad,profile);assert any(i.code=='pair-phase-auto-wrap' and i.severity=='error' for i in diagnostics)
    assert not ctx.machines
    save(ROOT/'three_complete_native_planes12_alignment_cases_and_36_cell_rejection.json',dict(candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],cases=cases,fresh_original_compiled_alignment_cases=12,unchanged216px_sixpx_font_four_rows_guards_and_pair_phase=True,thirty_five_visible_continuation_characters_with_original_guard_fit_and_complete=True,odd35_row_emits_no_preLF_phase_space_even34_does=True,unchanged_codec_source='dk4tool/dialogue/codec.py',unchanged_codec_sha256=sha(Path('dk4tool/dialogue/codec.py').read_bytes()),first36_cell_preLF_auto_wrap_rejected=True,no_changed_words_or_production_authored_breaks=True,all_complete_native_planes_independently_equal=True,actual_B208_English_gameplay_not_claimed=True,current_native_context_plan=str(ctx.proof_path),current_native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),evidence={str(p):sha(p.read_bytes()) for p in [DOC,Path(__file__),Path('dk4tool/dialogue/codec.py'),Path('scripts/shady_man_font_oracles_v6263.py')]},new_ROMs=0,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False));print('Original native35-cell continuation passes three complete planes/12 alignment cases;even34 keeps preLF space,odd35 needs none,first36 remains rejected. No words or native rules changed.')
