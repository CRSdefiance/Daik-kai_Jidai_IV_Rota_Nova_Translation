"""Expose raw storage andactual current runtime wording forwhole-exchange review."""
import unicodedata
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_Shrines_Temples_comparison_v3169')
SOURCE=Path('work/analysis/lil_Shrines_Temples_source_v3163/complete235_clean_current_native_context.json')
CONTROL=Path('work/analysis/lil_Shrines_Temples_controls_v3168c/all235_source_current_dispatch_dynamic_styles_and_predicates.json')
CONTEXT=Path('work/analysis/lil_Shrines_Temples_context_v3164b/complete_clean_exchange_context_notes.json')
if __name__=='__main__':
    assert not ROOT.exists();source,control,context=map(read,[SOURCE,CONTROL,CONTEXT]);assert context['all164speech_56stored_actor_alternatives_and15choice_labels_read_in_complete_clean_exchanges'] and context['older_English_not_yet_editorially_compared']
    binding=read(control['registered_catalog_binding']);catalog={bytes.fromhex(r['key_hex']):r for r in binding['records']if r['route_mask']&4};cases={(r['id'],r['version']):r for r in control['speech_and_stored_alternative_dispatch_cases']}
    rows=[]
    for r in source['records']+source['typed_actor_style_records']+source['typed_choice_records']:
        stored=bytes.fromhex(r['current_hex']);is_speech=r['kind'] not in ['typed-4100-actor-style-alternative','typed-choice-label'];body=stored[1:]if is_speech else stored;entry=None if r['kind']=='typed-choice-label'else catalog.get(body);template=bytes.fromhex(entry['target_hex'])if entry else body
        effective=template.replace(b'FI',b'Lil').replace(b'FA',b'Argot').replace(b'FO',b'Argot Co.')
        if r['kind']!='typed-choice-label':assert cases[r['id'],'current-English']['boundaries'][1]['text_hex']==effective.hex()
        paragraph=' '.join(unicodedata.normalize('NFKC',template.decode('cp932')).split())
        rows.append(dict(**r,current_raw_storage_English=body.decode('cp932'),current_effective_runtime_English=effective.decode('cp932'),current_effective_macro_template_hex=template.hex(),current_effective_macro_template_English=template.decode('cp932'),current_effective_paragraph=paragraph,
            registered_runtime_catalog_entry=None if entry is None else dict(table_index=binding['records'].index(entry),route_mask=entry['route_mask'],requests=entry['requests']),
            editorial_older_English_comparison_pending=True,full_clean_context_precedes_comparison=True,source_prose_or_completion_credit_added=0))
    assert len(rows)==235 and sum(r['registered_runtime_catalog_entry']is not None for r in rows)==3
    ROOT.mkdir(parents=True);files=[]
    for b in source['blocks']:
        n=b['block'];lines=[f'B{n} SOURCE/CURRENT FULL EXCHANGE COMPARISON','Read after clean-only context3164b;no translation decision approved here.']
        for c in b['all_clean_native_commands']:
            at=c['offset'];owned=[r for r in rows if r['block']==n and (r.get('command_offset',r['source_reference'].get('header_offset'))==at)]
            if not owned:continue
            lines.append(f"\n@{at:04X} WORD{c['word']:04X}")
            for r in owned:
                lines.extend([r['id']+' '+('STYLES'+str(r['style_indices'])if 'style_indices'in r else 'OPTION'+str(r['option_index'])if 'option_index'in r else 'SELECTOR'+r['source_presentation_prefix_hex']),'JP: '+r['source_Japanese'],'CURRENT EFFECTIVE: '+r['current_effective_paragraph']])
                if r['registered_runtime_catalog_entry']:lines.append('REGISTERED RUNTIME REPLACEMENT;storedlegacykey: '+r['current_raw_storage_English'])
        p=ROOT/f'B{n}_source_and_current_effective.txt';p.write_text('\n'.join(lines)+'\n',encoding='utf8');files.append(dict(block=n,path=str(p),sha256=sha(p.read_bytes())))
    save(ROOT/'all235_current_effective_comparison_packet.json',dict(source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),control_proof=str(CONTROL),control_proof_sha256=sha(CONTROL.read_bytes()),clean_context_notes=str(CONTEXT),clean_context_notes_sha256=sha(CONTEXT.read_bytes()),records=rows,comparison_files=files,
        current_effective_wording_includes3_exact_registered_name_catalog_substitutions=True,raw_storage_is_preserved_separately=True,normalization_for_wording_comparison='NFKC presentation forms andcollapse legacy whitespace;runtime macros remain FI/FA/FO inunexpanded templates.',all235_current_English_editorial_reading_still_pending=True,source_prose_credit_added=0,completion_credit_added=0,new_emulator_runs=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('235source/current comparisons rendered;3registered runtime replacements distinguished fromstorage;no editorialdecisions orcredit yet.')
