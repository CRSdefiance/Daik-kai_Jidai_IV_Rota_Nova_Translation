"""Seal source-first drafts of complete selected exchanges without consulting current English."""
import argparse
import ast
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ['packet','data','out']:
        parser.add_argument('--'+name,type=Path,required=True)
    parser.add_argument('--blocks',type=int,nargs='+',required=True)
    args = parser.parse_args()
    assert not args.out.exists()
    values = {}
    for node in ast.parse(args.data.read_text(encoding='utf-8')).body:
        if isinstance(node,ast.Assign) and len(node.targets)==1 and isinstance(node.targets[0],ast.Name):
            values[node.targets[0].id] = ast.literal_eval(node.value)
    assert set(values) == {'CONTEXTS','ROWS'}
    packet = load(args.packet)
    groups = [g for g in packet['groups'] if g['block'] in args.blocks]
    assert [g['block'] for g in groups] == args.blocks
    expected = {(g['block'],r['source_reference']['record_index']) for g in groups for r in g['records']}
    data = {}
    for line in values['ROWS'].strip().splitlines():
        block,index,meaning,english = line.split('|',3)
        key = int(block),int(index)
        assert key not in data and meaning.strip() == meaning and english.strip() == english
        assert english.isascii() and '\n' not in english and '  ' not in english
        data[key] = meaning,english
    assert set(data) == expected
    records = []
    approved_source_names = {0:'Rafael',4:'Janus',6:'Julio',12:'Yukihisa',14:'Emilio'}
    for group in groups:
        for original in group['records']:
            row = deepcopy(original)
            key = group['block'],row['source_reference']['record_index']
            meaning,english = data[key]
            assert row['source_Japanese'] is not None and not row['source_decode_error']
            assert all(english.count('{MACRO:'+m+'}') == count for m,count in row['source_macros'].items())
            selector = row['source_selector']
            row.update(source_meaning=meaning,english=english,independent_English_draft=english,
                context=values['CONTEXTS'][group['block']],
                speaker=approved_source_names.get(selector,'Source selector'+str(selector)+';identity binding pending'),
                kind='system-FE' if selector==254 else 'progressive',
                localization_note='Source-first logical draft. '+meaning+' Names,item terms andnative speaker consumers remain to be bound before approval.',
                review=dict(source=True,context=True,localization=False,naturalness=True,formatting=False),
                current_English_comparison_pending=True,source_name_term_control_andformatting_binding_pending=True,
                source_dynamic_speaker_binding_pending=207<=selector<224,
                no_fixed_identity_inferred_for_dynamic_selector=True,new_credit=0)
            records.append(row)
    assert len(records) == len(expected)
    save(args.out,dict(format='dk4-partial-source-first-whole-exchange-drafts-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        file_path=packet['file_path'],source_packet=str(args.packet),source_packet_sha256=sha(args.packet.read_bytes()),
        records=records,source_speech_drafts=len(records),selected_blocks=args.blocks,
        dialogue_exchange_blocks=[g['block'] for g in groups if g['records']],control_only_blocks=[g['block'] for g in groups if not g['records']],
        remaining_packet_speech_drafts=packet['records']-len(records),
        current_SC0_English_not_consulted_in_this_intake=True,no_blanket_historical_exposure_claim=True,
        source_glosses_andindependent_drafts_precede_current_English_comparison=True,
        item_titles_andunbound_speakers_provisional_not_approved_or_shippable=True,
        all_current_comparisons_native_checks_andregistered_integration_pending=True,
        new_credit=0,guide_photos=False,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [args.packet,args.data,Path(__file__)]}))
    print(dict(source_speech_drafts=len(records),complete_exchanges=sum(bool(g['records']) for g in groups),
        remaining_speech_drafts=packet['records']-len(records),current_English_unconsulted=True,new_credit=0))


if __name__ == '__main__':
    main()
