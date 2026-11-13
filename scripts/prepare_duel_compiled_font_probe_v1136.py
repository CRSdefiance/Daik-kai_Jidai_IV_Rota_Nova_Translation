"""Replace the Python layout boundary with actual compiled code in CPU research."""
from pathlib import Path


def main():
    source = Path('scripts/probe_duel_full_name_fonts_v1119.py').read_text(encoding='utf-8').split('\ndef main():', 1)[0]
    target = Path('scripts/probe_duel_compiled_fonts_v1136.py')
    assert not target.exists()
    changes = {
        'from scripts.verify_personal_gameplay_v841 import get_machine':
            'from scripts.verify_personal_gameplay_v841 import get_machine as base_machine',
        'from scripts.duel_postmacro_layout_v1119 import layout,trailing_ascii_phase':
            'from scripts.duel_postmacro_layout_v1134 import layout,trailing_ascii_phase',
        "ROOT=Path('work/analysis/duel_full_name_fonts_v1119')":
            "ROOT=Path('work/analysis/duel_compiled_fonts_v1136')",
    }
    for before, after in changes.items():
        assert source.count(before) == 1, before
        source = source.replace(before, after)
    begin = source.index('        assert value==text\n        output,lines=layout(value)')
    end = source.index('        draw.update(context=context', begin)
    source = source[:begin] + '''        output,lines=layout(text)
        assert value==output,'Compiled code output differs at original font entry'
        assert context-pointer==0x400 and len(output)<0x400
        assert struct.unpack('<i',u.mem_read(context+40,4))[0]==(12 if len(lines)==1 else 0)
        # Read-only reference check. Native compiled code already produced all
        # text bytes and the private Y value;Python changes neither.
''' + source[end:]
    before = '    def returned(u,pc,size,data):'
    assert source.count(before) == 1
    source = source.replace(before, '''    macro=[]
    def before_compiled(u,pc,size,data):
        pointer=u.reg_read(UC_ARM_REG_R1)
        value=bytes(u.mem_read(pointer,128)).split(b'\\0')[0]
        assert value==text
        macro.append(value.hex())
    def returned(u,pc,size,data):''')
    before = '    hooks=[cpu.hook_add(UC_HOOK_CODE,glyph_event,begin=0x01FF83AC,end=0x01FF83AC),'
    assert source.count(before) == 1
    source = source.replace(before, '''    hooks=[cpu.hook_add(UC_HOOK_CODE,before_compiled,begin=THUNK,end=THUNK),
        cpu.hook_add(UC_HOOK_CODE,glyph_event,begin=0x01FF83AC,end=0x01FF83AC),''')
    source = source.replace('    assert len(clears)==1 and len(registration)==1',
                            '    assert len(clears)==1 and len(registration)==1 and macro==[text.hex()]')
    source = source.replace("'original_macro_output_exact':True,", "'original_macro_output_exact':True,'compiled_native_formatter_executed_before_original_painter':True,")
    source = source.replace("'CPU_prototype_has_complete_correct_visible_layout':True,", "'compiled_native_formatter_has_complete_correct_visible_layout':True,")
    source += '''

THUNK=0x0247A000
COMPILER_PATH=Path('work/analysis/duel_layout_native_v1133/compiler_provenance.json')


def get_machine(arm,raw):
    from keystone import Ks,KS_ARCH_ARM,KS_MODE_ARM
    compiler=read(COMPILER_PATH);binary=Path(compiler['binary']).read_bytes()
    assert sha(binary)==compiler['binary_sha256']
    cpu,get=base_machine(arm,raw)
    cpu.mem_write(0x02470000,binary)
    assembly=f"""push {{r4-r6,lr}}
mov r4,r0
mov r5,r1
mov r0,r1
ldr r3,formatter
blx r3
cmp r0,#1
mov r1,#0
moveq r1,#12
str r1,[r4,#40]
mov r0,r4
mov r1,r5
bl 0x020d5404
pop {{r4-r6,pc}}
formatter: .word {compiler['entry']}
"""
    ka=Ks(KS_ARCH_ARM,KS_MODE_ARM)
    thunk=bytes(ka.asm(assembly,THUNK)[0])
    cpu.mem_write(THUNK,thunk)
    branch=bytes(ka.asm(f'bl {THUNK}',BASE+0xDAC0)[0])
    cpu.mem_write(BASE+0xDAC0,branch)
    return cpu,get


def main():
    assert not ROOT.exists()
    compiler=read(COMPILER_PATH)
    matrix_path=Path('work/analysis/duel_native_layout_v1134/compiled_native_DP_matrix.json')
    matrix=read(matrix_path)
    assert matrix['all4700_native_outputs_match_independent_physical_phase_DP']
    assert sha(Path(compiler['binary']).read_bytes())==compiler['binary_sha256']
    catalog_path=Path('work/analysis/duel_scope_names_v1117b/source_name_layout_catalogue.json')
    catalog=read(catalog_path)
    rom=NdsImage.open(ROM);arm=rom.read_file('/__arm9__.bin');kanji=rom.read_file('/GRP/KANJI.FNT')
    assert sha(ROM.read_bytes())==catalog['candidate_sha256']
    raw=Path(catalog['snapshot']).read_bytes();assert sha(raw)==catalog['snapshot_sha256']
    font_base=struct.unpack_from('<I',arm,0xD19B8)[0]-BASE
    assert raw[font_base:font_base+len(kanji)]==kanji
    assert kanji==NdsImage.open('work/clean.nds').read_file('/GRP/KANJI.FNT')
    selected=[];seen=set()
    for row in matrix['cases']:
        key=(row['message_ID'],row['input_hex'])
        if key in seen:continue
        seen.add(key);selected.append(row)
    assert len(selected)>=2820
    font=GameAsciiFont.from_arm9(arm);results=[];previews=[]
    ROOT.mkdir(parents=True)
    for row in selected:
        text=bytes.fromhex(row['input_hex'])
        case,native,visible=execute(arm,raw,text,font,kanji)
        assert case['native_draw_context']['generated_postmacro_hex']==row['generated_hex']
        assert case['compiled_native_formatter_has_complete_correct_visible_layout']
        assert case['native_font_consumes_complete_generated_string']
        assert case['glyph_ink_absent_from_final_crop']==0
        assert not case['first_glyph_damaged_by_later_stride_spill']
        case.update(message_ID=row['message_ID'],source_kind=row['kind'],
            source_208x36_4bit_SHA256=sha(native),visible_144x36_4bit_SHA256=sha(visible))
        case.pop('SDK_full_plane_clear_boundary_modeled')
        case.pop('original_renderer_three_final_crop_submissions')
        results.append(case)
        if row['message_ID'] in (1931,1933,1938,1944) and len(previews)<12 and (
                row['kind']=='legal-name-stress' and not text.isascii() or
                row['kind']=='source' and (b'Clifford' in text or b'\\x82\\x65ernando' in text or row['message_ID']==1944)):
            path=ROOT/f'native_compiled_{len(previews):02d}_ID{row["message_ID"]}.png'
            canvas=Image.new('RGB',(864,198),'#263238');draw=ImageDraw.Draw(canvas)
            draw.text((4,4),f'Compiled native formatter + original font/crops; CPU research; ID{row["message_ID"]}',fill='white')
            im=Image.frombytes('L',(144,36),bytes(255-v*17 for v in visible))
            canvas.paste(im.resize((864,144),Image.Resampling.NEAREST),(0,30));canvas.save(path)
            previews.append({'path':str(path),'sha256':sha(path.read_bytes()),'message_ID':row['message_ID']})
        if len(results)%400==0:print(f'Compiled native formatter + complete font/crops:{len(results)}/{len(selected)}',flush=True)
    assert len(results)==len(selected)
    proof=ROOT/'compiled_native_complete_fonts.json'
    save(proof,{'candidate':str(ROM),'candidate_sha256':catalog['candidate_sha256'],
        'compiler_provenance':str(COMPILER_PATH),'native_layout_matrix':str(matrix_path),
        'unique_complete_font_cases':len(results),'all_source_names_and_legal_name_stress_included':True,
        'cases':results,'research_previews':previews,'KANJI_font_sha256':sha(kanji),
        'original_macro_constructor_ASCII_CP932_fonts_and_three_crop_submissions_execute':True,
        'native_compiled_layout_and_private_Y_execute_without_Python_replacement':True,
        'Python_oracle_only_reads_and_compares_output_and_font_pixels':True,
        'CPU_only_trampoline_is_unconditionally_inserted_into_DA28_for_declared_case_inputs':THUNK,
        'production_caller_scope_and_owned_code_placement_not_yet_implemented':True,
        'boundary_models':['SDK clear','UI registration','GPU submission capture'],
        'not_actual_emulator_playback_or_a_playable_ROM_change':True,
        'all33_formatting_gates_still_false':True,'no_completion_credit':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    path=Path('translations/editorial_review_current_v1.json');ledger=read(path)
    assert ledger['records_editorially_completed']==1196 and ledger['records_with_source_and_prose_pass']==1267
    ledger['duel_prose_v1103'].update(compiled_native_complete_fonts=str(proof),
        formatting_status='compiled-native-layout-and-complete-fonts-pass;production-scope-owned-placement-integration-actual-open')
    save(path,ledger)
    print(f'{len(results)} complete compiled-native font/crop cases pass;production-scope/owned-placement/integration/actual still open.',flush=True)


if __name__=='__main__':main()
'''
    target.write_text(source, encoding='utf-8')
    print('Created native compiled formatter/font successor;Python boundary now read-only.')


if __name__ == '__main__':
    main()
