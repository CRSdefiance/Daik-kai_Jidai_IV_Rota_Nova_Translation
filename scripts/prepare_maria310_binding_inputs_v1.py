"""Project the sealed clean-first310 into the unchanged v7 native-current binder."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
import re
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.meaning_maria_B51_B52_clean_v1 import ROOT

def main():
    out=ROOT/'binding_inputs_v1';assert not out.exists()
    original=ROOT/'clean_source_packet.json';packet=load(original)
    parts=[ROOT/'B51_B52_independent_drafts_v1.json',ROOT/'B53_B57_independent_drafts_v1.json']
    docs=list(map(load,parts));rows=[deepcopy(r) for doc in docs for r in doc['records']]
    assert all(d['current_English_not_consulted'] for d in docs)
    source={(g['block'],r['id']):r for g in packet['groups'] for r in g['records']}
    groups={g['block']:g for g in packet['groups']}
    assert len(rows)==len(source)==310 and {(r['block'],r['id']) for r in rows}==source.keys()
    for row in rows:
        group=groups[row['block']];before=source[(row['block'],row['id'])]
        assert all(row[k]==v for k,v in before.items()) and not any(row['review'].values())
        command=next(c for c in group['all_source_commands'] if c['offset']==row['source_reference']['command_offset'])
        raw=bytes.fromhex(command['whole_command_hex']);body=bytes.fromhex(row['source_hex'])
        assert command['word']==0x4000 and raw[5:-1]==body and raw[-1:]==b'\0'
        selector=body[0];english=re.sub(r'\{MACRO:(F[A-Z])\}',lambda m:m[1],row['english'])
        counts=dict(Counter(re.findall(r'F[A-Z]',row['source_Japanese'])))
        assert dict(Counter(re.findall(r'F[A-Z]',english)))==counts,(row['id'],counts,english)
        assert english.isascii() and '\n' not in english and '{LB' not in english
        row.update(independent_English_draft=english,source_record_index=int(row['id'].split('_R')[1]),
            source_command_offset=command['offset'],source_word=command['word'],
            source_0100_ancestors=command['ancestor_0100_offsets'],source_native_extent=command['native_extent'],
            source_selector=selector,source_complete_preamble_hex=raw[:6].hex(),
            source_presentation_kind='source-FE-system-panel' if selector==254 else 'source-named-progressive',
            whole_exchange_context=row.get('whole_exchange_context',row['context']),
            source_macros=counts,source_meaning_pending=False,localized_draft_pending=False,
            source_first_independent_meaning_saved=True,
            source_read_with_all_previous_andfollowing_speeches_in_block=True,
            independent_draft_precedes_current_English_intake=True,current_English_comparison_pending=True,
            earlier_English_unconsulted=True,current_ROM_English_unconsulted=True,
            no_blanket_historical_English_unexposure_claim=True)
    out.mkdir()
    for group in packet['groups']:
        group['clean_block_sha256']=sha(bytes.fromhex(group['clean_block_hex']))
        group['records']=[r for r in rows if r['block']==group['block']]
    projected=out/'clean_source_packet.json';save(projected,packet)
    sealed=ROOT/'all310_clean_meanings_andindependent_drafts_v1.json'
    save(sealed,dict(records=rows,records_count=310,complete_exchanges=7,translation_policy='natural-dialogue-v2',target_locale='en-US',
        source_meanings_andlogical_drafts_sealed_before_current_ROM_English_extraction_in_this_intake=True,
        current_English_unconsulted=True,all_five_gates_pending=True,
        source_projection_adds_native_metadata_no_prose_changes=True,
        working_spoken_name_bindings_pending=['Mivor Gentz','Herald'],
        original_chunks_preserved=True,new_credit=0,full_goal_complete=False,
        evidence={str(p):digest(p) for p in [original,*parts,Path(__file__)]}))
    save(out/'meanings_view.json',dict(records=rows,meanings=310,
        source_packet=str(projected),source_packet_sha256=digest(projected),
        all_drafts_sealed=str(sealed),all_drafts_sha256=digest(sealed),
        no_blanket_prior_English_exposure_claim=True,new_credit=0))
    save(out/'projection_qualification.json',dict(source_objects=310,ordinary_speeches=310,physical_style_alternatives=0,
        captions=0,complete_blocks=7,source_native_preambles_andall_original_commands_bound=True,
        all310_meanings_anddrafts_sealed_before_current_intake=True,
        macros=dict(sum((Counter(r['source_macros']) for r in rows),Counter())),
        selector_counts=dict(Counter(r['source_selector'] for r in rows)),new_credit=0,
        evidence={str(p):digest(p) for p in [original,sealed,projected,Path(__file__)]}))
    print('Prepared310 sealed clean-first drafts for unchanged native binder;all5gates pending,zero credit.')
if __name__=='__main__':main()
