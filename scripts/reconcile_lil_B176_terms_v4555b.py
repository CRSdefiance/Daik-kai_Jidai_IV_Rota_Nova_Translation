"""Resolve Seville's current staged-pool pointer, preserving the failed direct-file probe."""
from pathlib import Path

if __name__=='__main__':
    source=Path(__file__).with_name('reconcile_lil_B176_terms_v4555.py');text=source.read_text(encoding='utf-8')
    text=text.replace('import struct\n','import struct\nfrom ndspy.code import MainCodeFile\nfrom dk4tool.patch.main_pool_cache_visibility import POOL,STAGE\n')
    a=text.index('    for label,path in ');b=text.index('    by={',a)
    text=text[:a]+'''    release=read('work/analysis/lil_B175_release_v4542/registered_release_verification.json')
    assert release['candidate_sha256']==source['current_ROM_sha256'] and release['all_source_shapes_BSS_and123040_staged_bytes_preserved']
    for label,path in [('clean','work/clean.nds'),('current',source['current_ROM'])]:
        arm=NdsImage.open(path).read_file('/__arm9__.bin');pointer=struct.unpack_from('<I',arm,at)[0]
        if label=='clean':
            offset=pointer-0x02000000;assert 0<=offset<len(arm)
            assert arm[at:at+4].hex().upper()==record['source_hex'].upper()
            storage=dict(mode='original-main-section',runtime_address=pointer)
        else:
            assert sha(arm)==release['ARM9_sha256']
            section=MainCodeFile(arm,0x02000000).sections[3];payload=bytes(section.data[:-48])
            assert section.ramAddress==STAGE and len(payload)==123040 and POOL<=pointer<POOL+len(payload)
            staged=bytes(section.data);assert arm.count(staged)==1
            offset=arm.index(staged)+pointer-POOL
            storage=dict(mode='validated-original-startup-staged-pool-copy',runtime_address=pointer,
                copy_destination=POOL,stage_address=STAGE,stage_file_offset=arm.index(staged),copied_bytes=len(payload),
                complete_copied_payload_sha256=sha(payload),historical_v2_replacement_pointer_not_current=record['replacement_hex'])
        end=arm.index(b'\\0',offset);value=arm[offset:end]
        assert value.decode('cp932')==('セビリア' if label=='clean' else 'Seville')
        bindings.append(dict(version=label,ROM=str(path),ARM9_sha256=sha(arm),pointer_field_offset=at,pointer=pointer,
            file_offset=offset,hex=value.hex(),text=value.decode('cp932'),storage=storage,whole_string_and_terminator_exact=True))
''' +text[b:]
    text=text.replace('[SOURCE,NAMES,CONTROL,CITY,Path(__file__)]',
        "[SOURCE,NAMES,CONTROL,CITY,Path(__file__),PRESERVED_PREDECESSOR,Path('work/analysis/lil_B175_release_v4542/registered_release_verification.json')]")
    exec(compile(text,str(source)+'::staged-pool-correction','exec'),
         {'__name__':'__main__','__file__':__file__,'PRESERVED_PREDECESSOR':source})
