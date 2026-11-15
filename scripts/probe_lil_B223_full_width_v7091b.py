"""Test the exact216px continuation capacity with unchanged prose and protected native breaks."""
from dataclasses import replace
from types import FunctionType
from pathlib import Path
from dk4tool.dialogue import encoder
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
from scripts.research_lil_B209_native_pages_v6461 import pages as old_pages
from scripts.square_shopkeeper_font_oracles_v7020 import expected_pixels
from scripts.square_shopkeeper_exact_native_context_v7020 import CurrentContext
from scripts.verify_lil_B174_fonts_v4470 import expand
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B223_full_width_v7091b')
DOC=Path('translations/lil_B223_editorial_manuscript_v1.json')
INPUT=Path('work/analysis/current_V7067_native_v7077/current_native_input.json')
PRIOR=Path('work/analysis/lil_B222_native_pages_v7047/all16_paragraphs16_complete_native_pages128_alignments.json')
if __name__=='__main__':
    assert not ROOT.exists();row=next(r for r in read(DOC)['records'] if r['source_record_index']==28);prefix,body=row['english'].split('}',1);prefix+='}';words=body.split();lines=[' '.join(words[:6]),' '.join(words[6:])]
    assert ' '.join(lines)==body and list(map(len,lines))==[25,36];markup=prefix+'{LB}'.join(lines)
    profile=replace(get_dialogue_profile('lil-opening-editorial-native-v1'),name='B223-exact216px-capacity-RESEARCH-ONLY',max_lines=4,leading_speaker_bytes=frozenset([2,13,21,208]))
    def formatted(text,p):assert text==row['english'] and p==profile;return markup
    enc=FunctionType(encoder.encode_relocatable_dialogue.__code__,{**encoder.encode_relocatable_dialogue.__globals__,'format_markup':formatted},argdefs=encoder.encode_relocatable_dialogue.__defaults__);value=enc(bytes.fromhex(row['source_hex']),row['english'],profile).encoded;assert value[0]==21 and b'\n ' in value and value[1:].replace(b' \n ',b' ').replace(b'\n ',b' ')==body.encode('ascii')
    ROOT.mkdir(parents=True);ctx=CurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context');pipeline=ctx.execute(expand,value[1:],21);ctx.machines.pop();assert not ctx.machines and len(pipeline['cases'])==4 and all(c['output_hex']==value[1:].hex() for c in pipeline['cases'])
    adapter=read(PRIOR)['source_owned_2b6_page_adapter'];env={**old_pages.__globals__,'expected_pixels':expected_pixels};exec(compile(adapter,__file__+'::unchanged-original216px-pages','exec'),env);result=env['pages'](ctx.arm,ctx.rom.read_file('/GRP/KANJI.FNT'),value[1:]);assert len(result['pages'])==1
    page=result['pages'][0];glyphs=[e for e in page['events'] if e['code']!=32];first=next(e for e in glyphs if e['y']==16);last=glyphs[-1];assert first['code']==ord('i') and first['x']==0 and last['code']==ord('.') and (last['x'],last['y'])==(210,16)
    pixels=bytes.fromhex(page.pop('native_plane_hex'));plane=ROOT/'complete_two_rows25_and36_native.bin';plane.write_bytes(pixels);page.update(native_plane=str(plane),native_plane_sha256=sha(pixels))
    save(ROOT/'unchanged_R28_two_rows25_36_all_glyphs_protected_breaks_and_four_alignments.json',dict(id=row['id'],manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),source_reference=row['source_reference'],current_reference=row['current_reference'],English=row['english'],generated_research_lines=lines,compiled_hex=value.hex(),native_processor=pipeline,complete_native_pages=result,continuation_first_visible_x0_final_visible_period_x210=True,all216_pixels_six_px_ASCII_and16px_pitch_unchanged=True,all_native_guards_pairphase_protection_and_input_output_canaries_retained=True,no_global_profile_QA_rule_or_runtime_change=True,only_extra_planning_reservation_is_unnecessary_for_this_bound_consumer=True,original_three_row_plan_preserved=True,actual_English_R28_full_width_hold_still_required=True,no_prose_change_or_byte_budget_shortening=True,new_emulator_runs=0,new_credit=0,evidence={str(p):sha(p.read_bytes()) for p in [DOC,INPUT,PRIOR,Path(__file__)]},full_goal_complete=False))
    print('Unchanged R28 fits25/36 cells:protected guards,all4 input alignments,first continuation i at0,last period at210,full native page and canaries pass. Actual English still required.')
