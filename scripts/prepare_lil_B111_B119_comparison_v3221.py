"""Expose effective current English only after complete clean context and bindings."""
import unicodedata
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B111_B119_comparison_v3221')
SOURCE=Path('work/analysis/lil_B111_B119_source_v3217b/complete150_reachable_Lil_clean_current_context.json')
CONTROL=Path('work/analysis/lil_B111_B119_controls_v3219/all150_source_current_dispatch_variable_styles_predicates_and_query.json')
CONTEXT=Path('work/analysis/lil_B111_B119_clean_context_v3213b/all182_complete_clean_exchange_context_notes.json')
TERMS=Path('work/analysis/lil_B111_B119_terms_v3220/clean_current_items_and_native_actor_role_reconciliation.json')
if __name__=='__main__':
    assert not ROOT.exists()
    source,control,context,terms=map(read,[SOURCE,CONTROL,CONTEXT,TERMS])
    assert context['all148speech_and34_actor_style_alternatives_read_in_complete_clean_exchanges'] and context['older_English_not_yet_editorially_compared']
    assert control['source_context_sha256']==terms['source_context_sha256']==sha(SOURCE.read_bytes())
    binding=read(control['registered_catalog_binding'])
    catalog={bytes.fromhex(r['key_hex']):r for r in binding['records'] if r['route_mask']&4}
    cases={(r['id'],r['version']):r for r in control['speech_and_stored_alternative_dispatch_cases']}
    rows=[]
    for r in source['records']+source['typed_actor_style_records']:
        stored=bytes.fromhex(r['current_hex']);speech=r['kind']!='typed-4100-actor-style-alternative'
        body=stored[1:] if speech else stored;entry=catalog.get(body)
        template=bytes.fromhex(entry['target_hex']) if entry else body
        effective=template.replace(b'FI',b'Lil').replace(b'FA',b'Argot').replace(b'FO',b'Argot Co.')
        assert cases[r['id'],'current-English']['boundaries'][1]['text_hex']==effective.hex()
        paragraph=' '.join(unicodedata.normalize('NFKC',template.decode('cp932')).split())
        rows.append({**r,'current_raw_storage_English':body.decode('cp932'),
            'current_effective_runtime_English':effective.decode('cp932'),
            'current_effective_macro_template_hex':template.hex(),'current_effective_macro_template_English':template.decode('cp932'),
            'current_effective_paragraph':paragraph,
            'registered_runtime_catalog_entry':None if entry is None else dict(
                table_index=binding['records'].index(entry),route_mask=entry['route_mask'],requests=entry['requests']),
            'editorial_older_English_comparison_pending':True,'full_clean_context_precedes_comparison':True})
    assert len(rows)==150
    ROOT.mkdir(parents=True);files=[]
    for b in source['blocks']:
        n=b['block'];lines=[f'B{n} SOURCE/CURRENT FULL EXCHANGE COMPARISON',
            'Complete clean context read first;native variable-role/dispatch/query bindings andcurrent names reconciled. No translation decision approved here.']
        for c in b['all_clean_native_commands']:
            at=c['offset'];owned=[r for r in rows if r['block']==n and r.get('command_offset',r['source_reference'].get('header_offset'))==at]
            if not owned:continue
            lines.append(f"\n@{at:04X} WORD{c['word']:04X}")
            for r in owned:
                label='STYLES'+str(r['style_indices'])+' PREFIX'+format(r['source_selector'],'02X') if 'style_indices' in r else 'SELECTOR'+r['source_presentation_prefix_hex']
                lines.extend([r['id']+' '+label,'JP: '+r['source_Japanese'],'CURRENT EFFECTIVE: '+r['current_effective_paragraph']])
                if r['registered_runtime_catalog_entry']:lines.append('REGISTERED RUNTIME REPLACEMENT;storedlegacykey: '+r['current_raw_storage_English'])
        if n==115:lines.append('\nUNOWNED APPENDED32MARIA COPY NOT COMPARED ASLIL PROSE;canonicalSC3B97 queuedseparately.')
        path=ROOT/f'B{n}_source_and_current_effective.txt';path.write_text('\n'.join(lines)+'\n',encoding='utf-8')
        files.append(dict(block=n,path=str(path),sha256=sha(path.read_bytes())))
    replacements=sum(r['registered_runtime_catalog_entry'] is not None for r in rows)
    save(ROOT/'all150_current_effective_comparison_packet.json',dict(
        source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),
        control_proof=str(CONTROL),control_proof_sha256=sha(CONTROL.read_bytes()),
        clean_context_notes=str(CONTEXT),clean_context_notes_sha256=sha(CONTEXT.read_bytes()),
        actor_item_terms=str(TERMS),actor_item_terms_sha256=sha(TERMS.read_bytes()),
        records=rows,comparison_files=files,registered_runtime_catalog_replacement_count=replacements,
        raw_storage_is_preserved_separately=True,
        normalization_for_wording_comparison='NFKC presentation forms andcollapselegacywhitespace;runtime macros remainFI/FA/FO inunexpandedtemplates.',
        all150_current_English_editorial_reading_still_pending=True,
        canonical_Maria32_unreachable_copy_excluded_and_retained_in_full_goal=True,
        source_prose_credit_added=0,completion_credit_added=0,new_emulator_runs=0,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(f'150source/current comparisons rendered;{replacements}registered runtime catalog replacements distinguished. Full editorial comparison/decisions pending;zero credit.')
