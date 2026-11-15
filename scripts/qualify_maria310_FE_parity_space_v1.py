"""Place one technical parity byte before a safe FE LF,with exact original native pixels."""
from pathlib import Path
from types import FunctionType
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.check_editorial_compiled_pages_v6 import check_FE_rows
from scripts import square_shopkeeper_font_oracles_v7020 as font
from scripts import Rafael_B45_FE_source_painter_v7894 as native
from scripts.meaning_maria_B51_B52_clean_v1 import ROOT

def main():
    out=ROOT/'FE_parity_space_qualification_v1.json';assert not out.exists()
    original_path=ROOT/'final_native_v1.json';doc_path=ROOT/'formatting_v1/formatting_input.json'
    old,doc=map(load,[original_path,doc_path]);runtime=doc['runtime']
    ctx=RegisteredRuntime(runtime['release_proof'],runtime['startup_proof'],captain=3);assert ctx.receipt()==runtime
    ident='DK4_MES_B54_R0507';row=next(r for r in old['records'] if r['id']==ident)
    source=next(r for r in doc['records'] if r['id']==ident);raw=bytes.fromhex(row['compiled_hex']);body=raw[1:]
    assert raw[0]==254 and '{MACRO:' not in source['english'] and len(body)==139
    plane=Path(row['complete_native_English_display']['native_plane']).read_bytes()
    af=FunctionType(font.make_painter.__code__,{**font.make_painter.__globals__,'CURRENT_ARM9':sha(ctx.arm)},argdefs=font.make_painter.__defaults__)
    factory=FunctionType(native.make_source_painter.__code__,{**native.make_source_painter.__globals__,'CURRENT_ARM9':sha(ctx.arm),'ASCII_painter':af},argdefs=native.make_source_painter.__defaults__)
    paint,calibration=factory(ctx.image);cases=[]
    for at in [i for i,value in enumerate(body) if value==10]:
        text=body[:at]+b' '+body[at:]
        case=dict(input_space_offset=at,compiled_hex=(raw[:1]+text).hex(),body_length=len(text),
            prose_unchanged=' '.join(text.decode('ascii').split())==source['editorial_logical_English'])
        try:
            rendered=paint(text);rows=check_FE_rows(text,rendered)
            assert rendered['physical']==plane and rendered['complete_consumed_bytes']==len(text)
        except AssertionError as exc:case.update(rejected=True,error=str(exc))
        else:case.update(rejected=False,all_original_native_assertions_pass=True,row_comparison=rows,
            complete_consumed_bytes=rendered['complete_consumed_bytes'],native_plane_sha256=sha(plane),
            exact_approved_physical_pixels=True,events=rendered['events'])
        assert case['prose_unchanged'];cases.append(case)
    good=[r for r in cases if not r['rejected']];assert good,'No qualified nontrailing parity-byte position'
    selected=good[0]
    save(out,dict(id=ident,runtime=runtime,source_reference=source['source_reference'],current_reference=source['current_reference'],
        source_hex=source['source_hex'],current_hex=source['current_hex'],logical_English=source['english'],
        original_compiled_hex=raw.hex(),target_compiled_hex=selected['compiled_hex'],
        selected_input_space_offset=selected['input_space_offset'],cases=cases,calibration=calibration,
        exactly_one_automatically_owned_ASCII_space_before_existing_LF=True,
        no_authored_breaks_no_prose_font_viewport_engine_orcontrol_changes=True,
        native_pixels_andfull_input_consumption_exact=True,needs_fresh_four_alignment_andstored_checks=True,new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [original_path,doc_path,Path(__file__)]}))
    print('Qualified FE parity byte before LF at',selected['input_space_offset'],'with full140-byte consumption andexact approved pixels;four alignments/storage remain.')
if __name__=='__main__':main()
