"""Resume only exact durable completed blocks; preserve all remaining stored/native checks."""
from scripts import check_qualified_rafael_mixed_stored_v2 as previous
from scripts.source_locked_derivation_v5118 import checked_text

compound_storage=previous.compound_storage
check_FE_rows=previous.check_FE_rows
progressive_expand=previous.progressive_expand
FE_expand=previous.FE_expand
source=checked_text(previous.source,{
    '    args=parser.parse_args();assert not args.out.exists()':
        "    parser.add_argument('--resume-blocks',type=Path)\n    args=parser.parse_args();assert not args.out.exists()",
    'typed=[];style_records=[]': 'typed=[];style_records=[];resumed=[]',
    "        block=blocks[group['block']];assert sha(block)==group['target_sha256']":
        """        block=blocks[group['block']];assert sha(block)==group['target_sha256']
        cached_path=args.resume_blocks/f'B{group["block"]}_checked.json' if args.resume_blocks else None
        if cached_path is not None and cached_path.exists():
            cached=load(cached_path)
            assert cached['block']==group['block'] and cached['target_block_sha256']==sha(block)
            assert cached['reconstruction_sha256']==sha(args.reconstruction.read_bytes()) and cached['native_sha256']==sha(args.native.read_bytes())
            assert cached['runtime']==runtime and cached['all_checks_for_this_block_complete']
            assert {r['id'] for r in cached['records']}=={r['id'] for r in group['text_records']}
            expected_styles={r['id'] for item in group.get('native_objects',[]) if item['word']==0x4100 for r in item['records']}
            assert {r['id'] for r in cached['style_records']}==expected_styles
            assert len(cached['relative_cases'])==len(group['relative_fixups'])
            for item in cached['records']:
                planned=plans[item['id']];old=compiled[item['id']]['complete_native_English_display']
                old_pages=[old] if compiled[item['id']]['kind']=='system-FE' else old['pages']
                assert len(old_pages)==planned['expected_native_pages']
                for page in old_pages:assert sha(Path(page['native_plane']).read_bytes())==page['native_plane_sha256']
                if item['parity_space_added']:fresh_pages+=len(old_pages)
                else:reused_pages+=len(old_pages)
            reused_pages+=sum(len(item['directly_viewed_planes']) for item in cached['style_records'])
            rows.extend(cached['records']);style_records.extend(cached['style_records']);typed.extend(cached['typed_objects']);relatives.extend(cached['relative_cases'])
            resumed.append(dict(path=str(cached_path),sha256=sha(cached_path.read_bytes()),block=group['block'],whole_complete_block_checks_reused=True))
            save(args.out/cached_path.name,{**cached,'exact_previous_block_receipt':resumed[-1]})
            print('Stored block',group['block'],'exact complete receipt reused',flush=True)
            continue""",
    '        records=rows,style_records=style_records,':
        '        prior_completed_block_receipts_reused=resumed,records=rows,style_records=style_records,',
})
exec(compile(source,__file__+'::same-native-checks-exact-durable-block-resumption', 'exec'),globals())
