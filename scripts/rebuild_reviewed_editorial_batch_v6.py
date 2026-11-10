"""Keep complete mixed-object reconstruction guards for an explicit reviewed scope."""
import inspect
import os
from scripts import rebuild_reviewed_editorial_batch_v4 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(inspect.getsource(previous.main),{
    '    args=parser.parse_args();assert not args.out.exists()':
        """    for name in ['approval','release']:parser.add_argument('--'+name,type=Path,required=True)
    for name in ['expected-records','expected-speeches','expected-styles','expected-captions','expected-blocks']:parser.add_argument('--'+name,type=int,required=True)
    args=parser.parse_args();assert not args.out.exists()""",
    "    assert len(doc['records'])==323 and doc['physical_speech_objects']==len(layout['records'])==len(native['records'])==308 and not layout['failures']":
        """    assert len(doc['records'])==args.expected_records and doc['physical_speech_objects']==len(layout['records'])==len(native['records'])==args.expected_speeches+args.expected_styles and not layout['failures']
    approval,parent=map(load,[args.approval,args.release])
    assert approval['source_objects']==args.expected_records and approval['body_pages']==native['pages']
    assert approval['all_final_body_pages_directly_viewed'] and approval['all_names_andcaptions_directly_viewed'] and approval['all_fifth_formatting_gates_still_pending']
    assert approval['final_native_proof_sha256']==sha(args.native.read_bytes())
    assert all(r['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False) for r in doc['records'])
    assert not parent['own_registered_startup_pending'] and parent['clean_input_patch_byte_exact']
    assert sha(Path('translations/release_stack.json').read_bytes())==parent['registry_sha256']
    assert doc['current_ROM_sha256']==parent['candidate_sha256']
    assert sha(Path('work/clean.nds').read_bytes())=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    clean_image=NdsImage.open('work/clean.nds');clean_blocks=IlnkContainer.parse(clean_image.read_file(doc['file_path'])).blocks
    assert len(doc['blocks'])==args.expected_blocks and doc['blocks']==sorted(set(doc['blocks']))
    assert packet['runtime']==native['runtime']==doc['runtime']""",
    'assert (len(ordinary),len(alternatives),len(typed))==(260,48,15)':
        'assert (len(ordinary),len(alternatives),len(typed))==(args.expected_speeches,args.expected_styles,args.expected_captions)\n    assert args.expected_speeches+args.expected_styles+args.expected_captions==args.expected_records',
    "        assert current.hex()==group['current_block_hex']":
        "        assert clean==clean_blocks[block]\n        assert current.hex()==group['current_block_hex']",
    "word=0x2200,":"word=rows[0]['source_word'],",
    '        target,proof=rebuild_block(arm,clean,current,records,compiled,inventory,compound)':
        '        assert records or compound\n        target,proof=rebuild_block(arm,clean,current,records,compiled,inventory,compound)\n        assert len(target)<=9216',
    '        else:assert block==128 and not records and not compound and current==clean':
        '        else:assert target==current',
    "assert [g['block'] for g in groups]==doc['blocks'] and len(changed)==19":
        "assert [g['block'] for g in groups]==doc['blocks'] and len(groups)==args.expected_blocks and changed and set(changed)<=set(doc['blocks'])",
    "assert reopened.read_file(doc['file_path'])==result and reopened.read_file('/__arm9__.bin')==arm":
        "assert reopened.read_file(doc['file_path'])==result and reopened.read_file('/__arm9__.bin')==arm\n    reopened.replace_file(doc['file_path'],archive);assert bytes(reopened.rom.save())==Path(doc['current_ROM']).read_bytes()",
    "unchanged_control_only_blocks=[128],speech_count=260,":
        "unchanged_control_only_blocks=[],source_editorial_objects=args.expected_records,source_speeches=args.expected_speeches,speech_count=args.expected_speeches,",
    'style_physical_speech_count=48,total_rendered_speech_count=308,typed_choice_count=15,compound_objects=13,':
        'style_physical_speech_count=args.expected_styles,total_rendered_speech_count=args.expected_speeches+args.expected_styles,typed_choice_count=args.expected_captions,compound_objects=len(menu[\'menus\'])+len(styles[\'objects\']),',
    'producers={str(p):sha(p.read_bytes()) for p in [Path(__file__),':
        "approval=str(args.approval),approval_sha256=sha(args.approval.read_bytes()),registered_parent_proof=str(args.release),registered_parent_proof_sha256=sha(args.release.read_bytes()),FE_continuation_owners=0,FE_inserted_commands=0,source_manuscript=str(args.manuscript),source_manuscript_sha256=digest,producers={str(p):sha(p.read_bytes()) for p in [Path(__file__),",
    "    if not any(p['path']==absolute for p in saved):saved.append(dict(path=absolute,reason='B111-B130 complete source-bound reconstruction; keep for ongoing editorial/storage/gameplay and registered release proofs.'))\n    save(pins,saved)":
        """    assert not any(p['path']==absolute for p in saved)
    before=pins.read_bytes();saved.append(dict(path=absolute,reason='Complete source-bound mixed research reconstruction; preserve all original and generated ROMs. SHA256 '+sha(rom.read_bytes())))
    (args.out/'pins.before.json').write_bytes(before);pending=pins.with_name('rom_retention_pins.'+args.out.parent.name+'.pending.json');assert not pending.exists();save(pending,saved)
    assert pins.read_bytes()==before;os.replace(pending,pins)""",
    'ordinary_speeches=260,style_alternatives=48,menu_labels=15,changed_blocks=19,':
        'ordinary_speeches=args.expected_speeches,style_alternatives=args.expected_styles,menu_labels=args.expected_captions,changed_blocks=len(changed),',
})
env={**vars(previous),'os':os,'__file__':__file__}
exec(compile(source,__file__+'::same-complete-source-current-compound-allocation-archive-andserialized-ROM-inverses','exec'),env)
if __name__=='__main__':env['main']()
