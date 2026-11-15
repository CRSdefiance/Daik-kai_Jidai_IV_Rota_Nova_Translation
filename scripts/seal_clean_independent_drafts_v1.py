"""Seal complete clean-source exchanges without granting current-comparison or display approval."""
from copy import deepcopy
from pathlib import Path
import re
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha


def seal(root,filename,data,contexts,choice_drafts,producer,expected):
    root=Path(root);out=root/filename;assert not out.exists()
    packet_path,choices_path=[root/p for p in ['clean_source_packet.json','clean_choice_objects.json']]
    packet,choices=map(load,[packet_path,choices_path]);rows=[]
    groups=[g for g in packet['groups'] if g['block'] in data]
    assert {g['block'] for g in groups}==set(data)==set(contexts)
    for group in groups:
        b=group['block'];assert {int(r['id'].split('_R')[-1]) for r in group['records']}==set(data[b])
        for source in group['records']:
            assert source['source_decode_error'] is None
            meaning,draft=data[b][int(source['id'].split('_R')[-1])]
            row=deepcopy(source)
            row.update(source_meaning=meaning,independent_English=draft,context=contexts[b],
                speaker='Native source selector '+str(source['source_selector'])+'; final name/role binding pending',
                review=dict(source=False,context=False,localization=False,naturalness=False,formatting=False),
                current_English_comparison_pending=True,approved_names_terms_titles_andruntime_substitutions_pending=True,new_credit=0)
            rows.append(row)
    labels=[r for r in choices['records'] if r['block'] in data]
    assert {(r['block'],r['source_index']) for r in labels}==set(choice_drafts)
    for source in labels:
        meaning,draft=choice_drafts[(source['block'],source['source_index'])];row=deepcopy(source)
        row.update(source_meaning=meaning,independent_English=draft,context=contexts[source['block']],speaker='Player choice',
            review=dict(source=False,context=False,localization=False,naturalness=False,formatting=False),
            current_English_comparison_pending=True,complete_native_menu_binding_andformatting_pending=True,new_credit=0)
        rows.append(row)
    for row in rows:
        draft=row['independent_English'];assert draft and '\n' not in draft and not any(t in draft for t in ['{LB','{ALIGN','{PAD}'])
        raw=bytes.fromhex(row['source_hex']);body=raw[1:] if 'source_selector' in row else raw
        row['native_literal_token_counts']={t.decode():body.count(t) for t in sorted(set(re.findall(rb'F[A-Z]',body)))}
        assert all(draft.count(token)==n for token,n in row['native_literal_token_counts'].items()),row['id']
    assert len(rows)==len({r['id'] for r in rows})==expected
    save(out,dict(records=rows,records_count=len(rows),ordinary_speeches=len(rows)-len(labels),typed_captions=len(labels),
        complete_blocks=list(data),source_contexts=contexts,all_five_gates_pending=True,
        no_current_English_extracted_for_this_intake_before_drafts=True,no_blanket_claim_of_historical_unexposure=True,
        all_source_literal_F_tokens_preserved_not_an_approval_of_their_native_consumers=True,
        no_ROM_or_registry_changes=True,new_credit=0,guide_photos=False,
        evidence={str(p):sha(p.read_bytes()) for p in [packet_path,choices_path,Path(producer),Path(__file__)]}))
    print(f'Sealed{len(rows)} clean meanings/independent drafts across{len(data)} completeblocks;literal native tokens exact. All current comparisons/bindings/five gates pending;no credit.')
