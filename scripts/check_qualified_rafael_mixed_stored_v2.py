"""Restore integer selector keys fromJSON andretain completed block receipts for future reuse."""
from scripts import check_qualified_rafael_mixed_stored_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

compound_storage=previous.compound_storage
check_FE_rows=previous.check_FE_rows
progressive_expand=previous.progressive_expand
FE_expand=previous.FE_expand
source=checked_text(previous.source,{
    "'DYNAMIC_BINDINGS':native['dynamic_role_bindings']":"'DYNAMIC_BINDINGS':{int(k):v for k,v in native['dynamic_role_bindings'].items()}",
    "        print('Stored block',group['block'],'checked',flush=True)":
        """        save(args.out/f'B{group["block"]}_checked.json',dict(block=group['block'],target_block_sha256=group['target_sha256'],
            reconstruction_sha256=sha(args.reconstruction.read_bytes()),native_sha256=sha(args.native.read_bytes()),runtime=runtime,
            records=[r for r in rows if r['block']==group['block']],style_records=[r for r in style_records if r['block']==group['block']],
            typed_objects=[r for r in typed if r['block']==group['block']],relative_cases=[r for r in relatives if r['block']==group['block']],
            all_checks_for_this_block_complete=True,whole_batch_pass_not_inferred=True,new_credit=0))
        print('Stored block',group['block'],'checked',flush=True)""",
})
exec(compile(source,__file__+'::same-complete-checks-json-integer-selector-keys-anddurable-block-receipts', 'exec'),globals())
