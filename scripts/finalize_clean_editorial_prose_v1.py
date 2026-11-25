"""Seal individual prose/name gates from reviewed decisions and exact consumer bindings."""
import argparse
from collections import Counter
from copy import deepcopy
from pathlib import Path
import re
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

GATES=['source','context','localization','naturalness','formatting']


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--config',type=Path,required=True)
    args=ap.parse_args();cfg=load(args.config)
    paths=[Path(cfg[k]) for k in ['proposals','names','terms','roles','objects']]
    proposals,names,terms,roles,objects=map(load,paths);runtime=proposals['runtime']
    assert all(d['runtime']==runtime for d in [names,terms,roles,objects])
    assert proposals['records_count']==cfg['source_objects'] and proposals['all_five_gates_still_pending']
    assert (proposals['revised'],proposals['retained'])==tuple(cfg['proposal_counts'])
    assert len(terms['items'])==cfg['item_bindings']
    assert {r['actor_ID'] for r in names['records']}=={int(k) for k in cfg['name_reasons']}
    outputs=[Path(cfg[k]) for k in ['out','names_out','proof_out']];assert not any(p.exists() for p in outputs)
    scoped=[];forms={}
    for original in names['records']:
        row=deepcopy(original);actor=row['actor_ID'];reason=cfg['name_reasons'][str(actor)]
        approved={r['consumer']:r['text'] for r in row['current_consumers']}
        assert set(approved)=={'progressive-nameplate','full-catalogue'} and all(t.isascii() for t in approved.values())
        forms[actor]=approved['progressive-nameplate']
        row.update(id=f"{cfg['scope_id']}_ACTOR_{actor}_SCOPED_NAME",approved_forms=approved,english=forms[actor],speaker=forms[actor],
            context=cfg['name_context'],source_meaning=' / '.join(f['source']['text'] for f in row['source_andcurrent_fields'] if f['source']['text']),
            finding=reason,localization_note=reason,retention_reason=reason,decision='retention',review={g:g!='formatting' for g in GATES},
            name_localization_andfresh_display_approval_pending=False,fresh_native_display_orcompatible_proof_binding_pending=True,
            no_global207_name_approval=True,unused_metadata_not_globally_approved=True,new_credit=0)
        scoped.append(row)
    role_forms={r['source_selector']:r for r in roles['native_roles']['rows']}
    rows=deepcopy(proposals['records']);changes=[];amendments=cfg['amendments'];seen=set()
    for row in rows:
        assert not any(row['review'].values())
        text=row['proposed_English']
        if row['id'] in amendments:
            change=amendments[row['id']];assert text==change['before'];seen.add(row['id'])
            text=change['after'];assert text!=change['before'] and change['reason']
            changes.append(dict(id=row['id'],**change));row['finding']+=' '+change['reason'];row['localization_note']=row['finding']
            row.update(decision='revision',retention_reason='')
        assert text.isascii() and text==text.strip() and not any(t in text for t in ['\n','\r','\t','{LB','{ALIGN','{PAD'])
        assert re.findall(r'\bF[IAOU]\b',text)==re.findall(r'F[IAOU]',row['source_Japanese']),row['id']
        assert (text==row['current_comparison_paragraph'])==(row['decision']=='retention'),row['id']
        assert row['finding'] and row['source_meaning'] and row['whole_exchange_context']
        if row['decision']=='retention':assert row['retention_reason']
        sourcekind=row['kind'];selector=row.get('source_selector')
        if sourcekind=='typed-menu-caption':kind,speaker='typed-choice-label','Player response in '+row['whole_exchange_context']
        elif sourcekind=='physical-style-alternative':
            assert selector in role_forms
            kind,speaker='progressive',f'Dynamic selector{selector}; original voice slots{row["source_style_indices"]}; conditional assignment unvisited'
            obj=next(o for o in objects['style_objects'] if o['block']==row['block'] and o['source_command_offset']==row['source_command_offset'])
            row.update(native_object_kind='4100-style-alternative',source_object_hex=obj['source_object_hex'],
                source_choice_object_hex=obj['source_object_hex'],virtual_formatter_prefix_not_in_stored_body=True,
                current_record_index=row['current_reference']['physical_record_index'])
        else:
            assert sourcekind=='ordinary-speech'
            if selector==254:
                kind,speaker='system-FE',cfg['FE_contexts'][str(row['block'])]
                assert row['source_complete_preamble_hex']=='0040ffff00fe' and row['source_hex'].startswith('fe')
                row.update(source_presentation_kind='system-FE',source_FE_presentation_kind='system-FE',FE_is_not_an_ordinary_actor_nameplate=True)
            elif selector in role_forms:kind,speaker='progressive',f'Dynamic selector{selector}; conditional assignment unvisited'
            else:kind,speaker='progressive',forms[selector]
        row.update(independent_English_draft=row['english'],english=text,logical_English=text,proposed_English=text,
            original_source_kind=sourcekind,kind=kind,speaker=speaker,context=row['whole_exchange_context'],exchange_context=row['whole_exchange_context'],
            native_literal_token_counts=row['source_macros'],review={g:g!='formatting' for g in GATES},
            names_terms_consumers_andfresh_display_approval_pending=False,approved_names_terms_titles_andruntime_substitutions_pending=False,
            scoped_prose_name_term_references=[str(outputs[1]),str(paths[2]),str(paths[3])],
            final_whole_exchange_readaloud_review_complete=True,fresh_formatting_binding_pending=True,registered_release_and_completion_credit_pending=True)
    assert seen==set(amendments)
    counts=Counter(r['decision'] for r in rows);kinds=Counter(r['kind'] for r in rows)
    assert (counts['revision'],counts['retention'])==tuple(cfg['final_counts']) and dict(kinds)==cfg['kind_counts']
    doc=dict(format='dk4-contextual-dialogue-review-v2',translation_policy='natural-dialogue-v2',target_locale='en-US',
        encoder='dialogue-relocatable-v1',review_gates=GATES,file_path='/data/SC3.DK4',blocks=sorted({r['block'] for r in rows}),
        records=rows,source_objects=len(rows),complete_exchanges=proposals['complete_exchanges'],proposed_revisions=counts['revision'],justified_retentions=counts['retention'],
        runtime=runtime,current_ROM=runtime['candidate'],current_ROM_sha256=runtime['candidate_sha256'],scoped_name_term_andreadaloud_amendments=changes,
        all_individual_four_prose_gates_pass=True,all_fifth_formatting_gates_pending=True,
        native_macro_tokens_still_require_formatter_marking=True,no_new_formatted_pages_orbatch_gameplay_orintegration_claim=True,new_credit=0,full_goal_complete=False,
        evidence={str(p):digest(p) for p in [*paths,args.config,Path(__file__)]})
    structural=deepcopy(doc);structural['translation_policy']='natural-dialogue-v1';validate_natural_dialogue_batch(structural)
    try:validate_natural_dialogue_batch(doc)
    except ValueError as exc:
        assert 'v2 requires per-record' in str(exc);blocked=str(exc)
    else:raise AssertionError('Unformatted manuscript passed v2 release gate')
    save(outputs[1],dict(format='dk4-scoped-name-editorial-review-v2',translation_policy='natural-dialogue-v2',target_locale='en-US',records=scoped,
        runtime=runtime,scoped_actors=len(scoped),individual_name_retentions=len(scoped),first_four_gates_pass=True,formatting_gates_pending=True,
        no_new_name_table_bytes_or_global_metadata_approval=True,new_credit=0,evidence=doc['evidence']))
    doc['evidence'][str(outputs[1])]=digest(outputs[1]);save(outputs[0],doc)
    save(outputs[2],dict(manuscript=str(outputs[0]),manuscript_sha256=digest(outputs[0]),records=len(rows),complete_exchanges=proposals['complete_exchanges'],
        revisions=counts['revision'],retentions=counts['retention'],kinds=dict(kinds),scoped_name_retentions=len(scoped),first_four_individual_gates_pass=True,
        all_fifth_gates_false=True,structural_projection_pass=True,unformatted_manuscript_rejected_by_release_gate=blocked,amendments=changes,
        fresh_formatting_visual_storage_representative_gameplay_andregistration_pending=True,new_credit=0,full_goal_complete=False))
    print(dict(source_objects=len(rows),revisions=counts['revision'],retentions=counts['retention'],scoped_names=len(scoped),four_prose_gates_pass=True,formatting_pending=True,new_credit=0))


if __name__=='__main__':main()
