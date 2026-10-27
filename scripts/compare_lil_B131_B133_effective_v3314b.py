"""Expose effective current wording after complete clean context and native binding."""
import unicodedata
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B131_B133_comparison_v3314b')
SOURCE=Path('work/analysis/lil_remaining_B131_B140_source_v3306b/next63_B131_B133_clean_current_context.json')
CONTROL=Path('work/analysis/lil_B131_B133_controls_v3308b/all61_source_current_dispatch_selector00_FE_and5_predicates.json')
CONTEXT=Path('work/analysis/lil_B131_B133_clean_context_v3312/all63_complete_clean_context_and_fresh_glosses.json')
TERMS=Path('work/analysis/lil_B131_B133_terms_v3313/clean_current_items_names_and_share_ratio_reconciliation.json')
if __name__=='__main__':
    assert not ROOT.exists();source,control,context,terms=map(read,[SOURCE,CONTROL,CONTEXT,TERMS])
    assert context['all63_complete_clean_source_objects_read_before_older_English_comparison']
    assert control['source_context_sha256']==terms['source_context_sha256']==sha(SOURCE.read_bytes())
    assert context['all63_fresh_source_glosses_precede_localized_English']
    binding=read(control['registered_catalog_binding']);catalog={bytes.fromhex(r['key_hex']):r for r in binding['records'] if r['route_mask']&4}
    cases={(r['id'],r['version']):r for r in control['speech_dispatch_cases']};rows=[]
    for r in source['records']+source['typed_choice_records']:
        choice=r['kind']=='typed-choice-label';stored=bytes.fromhex(r['current_hex']);body=stored if choice else stored[1:];entry=None if choice else catalog.get(body)
        template=bytes.fromhex(entry['target_hex']) if entry else body;effective=template if choice else template.replace(b'FI',b'Lil').replace(b'FA',b'Argot').replace(b'FO',b'Argot Co.')
        if not choice:assert cases[r['id'],'current-English']['boundaries'][1]['text_hex']==effective.hex()
        paragraph=' '.join(unicodedata.normalize('NFKC',template.decode('cp932')).split())
        rows.append({**r,'current_raw_storage_English':body.decode('cp932'),'current_effective_runtime_English':effective.decode('cp932'),'current_effective_macro_template_hex':template.hex(),'current_effective_macro_template_English':template.decode('cp932'),'current_effective_paragraph':paragraph,'registered_runtime_catalog_entry':None if entry is None else dict(table_index=binding['records'].index(entry),route_mask=entry['route_mask'],requests=entry['requests']),'editorial_older_English_comparison_pending':True,'full_clean_context_precedes_comparison':True})
    assert len(rows)==63;ROOT.mkdir(parents=True);files=[]
    for b in source['blocks']:
        n=b['block'];lines=[f'B{n} SOURCE/CURRENT COMPLETE EXCHANGE COMPARISON','Clean complete exchange read first. Current names including static00 Rafael,FE null actor,FI/FO,five predicates,item names andtwo-to-one share terms bound. No editorial decision approved here.']
        for c in b['all_clean_native_commands']:
            at=c['offset'];owned=[r for r in rows if r['block']==n and r.get('command_offset',r['source_reference'].get('header_offset'))==at]
            if not owned:continue
            lines.append(f"\n@{at:04X} WORD{c['word']:04X}")
            for r in owned:
                label='OPTION'+str(r['option_index']) if r['kind']=='typed-choice-label' else 'SELECTOR'+r['source_presentation_prefix_hex']
                lines.extend([r['id']+' '+label,'JP: '+r['source_Japanese'],'CURRENT EFFECTIVE: '+r['current_effective_paragraph']])
                if r['registered_runtime_catalog_entry']:lines.append('REGISTERED RUNTIME REPLACEMENT;historical stored key: '+r['current_raw_storage_English'])
        p=ROOT/f'B{n}_source_and_current_effective.txt';p.write_text('\n'.join(lines)+'\n',encoding='utf-8');files.append(dict(block=n,path=str(p),sha256=sha(p.read_bytes())))
    replacements=sum(r['registered_runtime_catalog_entry'] is not None for r in rows)
    save(ROOT/'all63_current_effective_comparison_packet.json',dict(source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),control_proof=str(CONTROL),control_proof_sha256=sha(CONTROL.read_bytes()),clean_context_notes=str(CONTEXT),clean_context_notes_sha256=sha(CONTEXT.read_bytes()),actor_item_terms=str(TERMS),actor_item_terms_sha256=sha(TERMS.read_bytes()),fresh63_glosses_precede_current_English_comparison=True,records=rows,comparison_files=files,registered_runtime_catalog_replacement_count=replacements,raw_storage_is_preserved_separately=True,normalization_for_wording_comparison='NFKC presentation forms and collapsed legacy whitespace; runtime macros remain FI/FA/FO in unexpanded templates.',all63_current_English_editorial_reading_still_pending=True,source_prose_credit_added=0,completion_credit_added=0,new_emulator_runs=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(source_current_comparisons=63,registered_runtime_replacements=replacements,complete_editorial_reading_and_decisions_still_pending=True,credit=0))
