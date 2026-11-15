"""Use the original catalogue guard on the two changed bodies; reuse all exact matches."""
from scripts.check_qualified_rafael_stored_catalogue_v1 import source as previous,TEMPLATE
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    "['stored','current','qualification','out']":"['stored','current','qualification','previous-catalogue','out']",
    "    rows=ctx.execute(env['native_lookup'],stored['records'])":"""    prior=load(args.previous_catalogue);prior_stored=Path(prior['stored'])
    assert sha(prior_stored.read_bytes())==prior['stored_sha256'] and prior['runtime']==runtime
    assert prior['current_sha256']==sha(CURRENT.read_bytes()) and prior['all_new_effective_bodies_byte_exact_before_original_macro_expansion']
    old={r['id']:r for r in prior['records']};new={r['id']:r for r in stored['records']};assert set(old)==set(new)
    changed=[r for ident,r in new.items() if bytes.fromhex(r['stored_hex'])[1:].hex()!=old[ident]['stored_body_hex']]
    assert {r['id'] for r in changed}=={'DK4_MES_B154_R0084','DK4_MES_B154_R0114'}
    fresh=ctx.execute(env['native_lookup'],changed);assert {r['id'] for r in fresh}=={r['id'] for r in changed}
    fresh_by_id={r['id']:r for r in fresh};rows=[]
    for ident,r in new.items():
        exact=ident not in fresh_by_id;proof=old[ident] if exact else fresh_by_id[ident]
        assert proof['all_unowned4MiB_SP_andinput_canaries_exact'] and proof['complete_effective_body_equals_new_stored_body']
        assert proof['stored_body_hex']==proof['target_hex']==bytes.fromhex(r['stored_hex'])[1:].hex()
        rows.append({**proof,'exact_previous_lookup_proof_reused':exact})""",
    "records=rows,prior_catalogue_selected_IDs=previous_aliases,":"records=rows,prior_catalogue_selected_IDs=previous_aliases,fresh_native_lookups=len(fresh),exact_previous_lookups_reused=len(rows)-len(fresh),",
    '[STORED,CURRENT,args.qualification,TEMPLATE,Path(original.__file__),Path(__file__)]':
        '[STORED,CURRENT,args.qualification,args.previous_catalogue,prior_stored,TEMPLATE,Path(original.__file__),Path(__file__)]',
    "print('All newly stored bodies survive the original catalogue lookup byte forbyte;source-owned aliases cannot restore old glyphs orwrapping.')":
        "print(dict(fresh_native_lookups=len(fresh),exact_previous_lookups_reused=len(rows)-len(fresh),all_effective_bodies_byte_exact=True))",
})
if __name__=='__main__':exec(compile(source,__file__+'::same-complete-catalogue-guards-two-delta-records','exec'),globals())
