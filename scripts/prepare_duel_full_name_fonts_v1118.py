"""Create an explicit successor of the ASCII prototype for all native names."""
from pathlib import Path


def main():
    source = Path('scripts/probe_duel_postmacro_v1115.py').read_text(encoding='utf-8').split('\ndef main():', 1)[0]
    target = Path('scripts/probe_duel_full_name_fonts_v1118.py')
    assert not target.exists()
    changes = {
        "ROOT=Path('work/analysis/duel_postmacro_v1115')": "ROOT=Path('work/analysis/duel_full_name_fonts_v1118')",
        'def execute(arm,raw,text,font):': 'def execute(arm,raw,text,font,kanji):',
        "events.append({'code':code,'style':style,'x':u.reg_read(UC_ARM_REG_R2),'y':u.reg_read(UC_ARM_REG_R3)})":
            "events.append({'kind':'cp932' if pc==0x01FF83AC else 'ascii','code':code,'style':style,'x':u.reg_read(UC_ARM_REG_R2),'y':u.reg_read(UC_ARM_REG_R3)})\n"
            "        if pc==0x01FF83AC:\n"
            "            assert struct.unpack('<I',u.mem_read(u.reg_read(UC_ARM_REG_R0)+12,4))[0]==0",
        "hooks=[cpu.hook_add(UC_HOOK_CODE,glyph_event,begin=BASE+0xD16B4,end=BASE+0xD16B4),":
            "hooks=[cpu.hook_add(UC_HOOK_CODE,glyph_event,begin=0x01FF83AC,end=0x01FF83AC),\n"
            "        cpu.hook_add(UC_HOOK_CODE,glyph_event,begin=BASE+0xD16B4,end=BASE+0xD16B4),",
        "native=bytes(1 if (b>>shift)&15 else 0 for b in packed for shift in (0,4))":
            "native=bytes((b>>shift)&15 for b in packed for shift in (0,4))",
        "    source_ink=sum(native);": "    source_ink=sum(bool(value) for value in native);",
        "    outside_source=[e for e in events if e['x']+6>208 or e['y']+12>36]":
            "    outside_source=[e for e in events if e['x']+(12 if e['kind']=='cp932' else 6)>208 or e['y']+12>36]",
        "    outside_crop=[e for e in events if e['x']+6>144 or e['y']+12>36]":
            "    outside_crop=[e for e in events if e['x']+(12 if e['kind']=='cp932' else 6)>144 or e['y']+12>36]",
        "native[(draw['initial_y']+y)*208+x]!=int(y<11 and bool(first.getpixel((x,y))))":
            "native[(draw['initial_y']+y)*208+x]!=15*int(y<11 and bool(first.getpixel((x,y))))",
        "return {'text':text.decode('ascii')": "return {'text':text.decode('cp932')",
        "'actual_final_crop_ink':sum(visible)": "'actual_final_crop_ink':sum(bool(value) for value in visible)",
        "'glyph_ink_absent_from_final_crop':full_ink-sum(visible)":
            "'glyph_ink_absent_from_final_crop':full_ink-sum(bool(value) for value in visible)",
    }
    for before, after in changes.items():
        assert source.count(before) == 1, before
        source = source.replace(before, after)
    begin = source.index('    expected=bytearray(208*36);full_ink=0;expected_letters=[]')
    end = source.index('    assert native==bytes(expected)', begin)
    source = source[:begin] + '''    expected,expected_letters=expected_plane(arm,kanji,font,draw['generated_lines'])
    full_ink=sum(bool(value) for value in expected)
    assert [(e['kind'],e['code'],e['x'],e['y']) for e in events if e['code']!=32]==expected_letters
    assert all(e['style']==15 and 0<=e['x'] and e['x']+(12 if e['kind']=='cp932' else 6)<=144 and 0<=e['y'] and e['y']+12<=36 for e in events)
''' + source[end:]
    source += '''

def expected_plane(arm,kanji,font,lines):
    mapping=struct.unpack_from('<3340H',arm,0x125EC4)
    plane=bytearray(208*36);letters=[]
    for row,line in enumerate(lines):
        ybase=12 if len(lines)==1 else row*12
        xbase=0
        for character in line:
            raw=character.encode('cp932');width=len(raw)*6
            code=int.from_bytes(raw,'big');kind='ascii' if len(raw)==1 else 'cp932'
            if character!=' ':letters.append((kind,code,xbase,ybase))
            if kind=='ascii':
                glyph=font.decode(character)
                for y in range(12):
                    for x in range(6):
                        plane[(ybase+y)*208+xbase+x]=15*int(y<11 and bool(glyph.getpixel((x,y))))
            else:
                assert code in mapping
                index=mapping.index(code);cell=kanji[index*22:(index+1)*22]
                for y in range(12):
                    for x in range(12):plane[(ybase+y)*208+xbase+x]=0
                for y in range(11):
                    for x in range(11):
                        if cell[y*2+x//8]&(0x80>>(x%8)):
                            plane[(ybase+y)*208+xbase+x]=15
                # Independent original D1898 bottom-to-top lower-right shadow.
                for y in range(11,0,-1):
                    for x in range(11):
                        if plane[(ybase+y-1)*208+xbase+x] and not plane[(ybase+y)*208+xbase+x+1]:
                            plane[(ybase+y)*208+xbase+x+1]=14
            xbase+=width
    return plane,letters


def main():
    assert not ROOT.exists()
    names_path=Path('work/analysis/duel_scope_names_v1117b/source_name_layout_catalogue.json')
    catalog=read(names_path)
    rom=NdsImage.open(ROM);arm=rom.read_file('/__arm9__.bin');kanji=rom.read_file('/GRP/KANJI.FNT')
    assert sha(ROM.read_bytes())==catalog['candidate_sha256']
    raw=Path(catalog['snapshot']).read_bytes();assert sha(raw)==catalog['snapshot_sha256']
    font_base=struct.unpack_from('<I',arm,0xD19B8)[0]-BASE
    assert raw[font_base:font_base+len(kanji)]==kanji
    assert kanji==NdsImage.open('work/clean.nds').read_file('/GRP/KANJI.FNT')
    names={row['name_hex']:row for row in catalog['names']}
    records=read('translations/duel_editorial_manuscript_v3.json')['records']
    assert len(names)==141
    font=GameAsciiFont.from_arm9(arm);results=[];samples=[]
    ROOT.mkdir(parents=True)
    for index,(name_hex,name) in enumerate(sorted(names.items())):
        argument=bytes.fromhex(name_hex)
        for record in records:
            number=record['message_id']
            if number>=1951:continue
            text=record['english'].encode('ascii').replace(b'%s',argument)
            case,native,visible=execute(arm,raw,text,font,kanji)
            assert case['CPU_prototype_has_complete_correct_visible_layout'] and case['native_font_consumes_complete_generated_string']
            assert case['glyph_ink_absent_from_final_crop']==0 and not case['first_glyph_damaged_by_later_stride_spill']
            case.update(actor_slot=name['actor_slot'],native_actor_ID=name['actor_ID'],name_hex=name_hex,message_ID=number,
                entire_208x36_4bit_plane_SHA256=sha(native),entire_144x36_visible_4bit_plane_SHA256=sha(visible))
            # Compact sufficient evidence retains all glyph requests and line output.
            case.pop('SDK_full_plane_clear_boundary_modeled')
            case.pop('original_renderer_three_final_crop_submissions')
            results.append(case)
            if not argument.isascii() and number in (1931,1938):
                path=ROOT/f'name{ name["actor_slot"] }_message{number}_CPU_research.png'
                canvas=Image.new('RGB',(864,198),'#263238');draw=ImageDraw.Draw(canvas)
                draw.text((4,4),f'CPU research only: native name slot{name["actor_slot"]}, message{number}',fill='white')
                im=Image.frombytes('L',(144,36),bytes(255-v*17 for v in visible))
                canvas.paste(im.resize((864,144),Image.Resampling.NEAREST),(0,30));canvas.save(path)
                samples.append({'path':str(path),'sha256':sha(path.read_bytes())})
        if (index+1)%20==0:print(f'Complete native names:{index+1}/141;full planes:{len(results)}',flush=True)
    assert len(results)==2820 and all(not row['glyphs_crossing_source_rows'] and not row['glyphs_outside_final_visible_crop'] for row in results)
    proof=ROOT/'native_all_source_names_font_proof.json'
    save(proof,{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),
        'native_name_catalogue':str(names_path),'native_name_catalogue_sha256':sha(names_path.read_bytes()),
        'source_slots208_unique_actual_IDs207_unique_name_strings141':True,
        'all2820_full_native_ASCII_CP932_planes_match_independent_complete_font_masks_and_shadows':True,
        'all20_duel_drafts_all_source_names_fit_without_truncated_letters_or_authored_indents':True,
        'original_KANJI_font_sha256':sha(kanji),'current_snapshot_contains_exact_original_KANJI_font':True,
        'cases':results,'research_previews':samples,
        'explicit_boundary_models':['SDK clear','widget registration','Python post-macro24x3 layout'],
        'original_constructor_measurement_macro_ASCII_CP932_painters_and_crop_submissions_execute':True,
        'not_assembled_runtime_or_actual_gameplay':True,'all33_formatting_gates_still_pending':True,
        'no_ROM_registry_runtime_or_completion_credit_change':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    path=Path('translations/editorial_review_current_v1.json');ledger=read(path)
    assert ledger['records_editorially_completed']==1196 and ledger['records_with_source_and_prose_pass']==1267
    ledger['duel_prose_v1103'].update(native_all_source_name_fonts=str(proof),
        all2820_CPU_native_font_planes_include_preserved_fullwidth_names=True,
        formatting_status='all-source-name-CPU-prototype-fonts-pass;assembled-runtime-owned-storage-integration-and-actual-still-pending')
    save(path,ledger)
    print('2820 complete native name/font cases pass;runtime/storage/integration/actual gates remain open.',flush=True)


if __name__=='__main__':main()
'''
    target.write_text(source, encoding='utf-8')
    print('Created full native-name ASCII/CP932 font successor;no ROM changes.')


if __name__ == '__main__':
    main()
