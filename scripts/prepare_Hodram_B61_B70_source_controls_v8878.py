"""Prepare a source-locked successor for the ten complete clean exchanges.

The new gloss packet intentionally stores meanings rather than a second command
inventory. Bind every original record value to the complete source inventory,
then use that inventory for native controls. No English dialogue is inspected.
"""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/Hodram_B61_B70_controls_preparation_v8878')
BASE = Path('work/analysis/Hodram_next_clean_v8872/complete_clean_SC1_B61_B70_EV1_andcoverage_before_current_English.json')
GLOSS = Path('work/analysis/Hodram_B61_B70_clean_gloss_v8877/224_complete_clean_first_meanings_all_ten_exchanges_before_current_English.json')

if __name__ == '__main__':
    assert not ROOT.exists()
    base, gloss = map(read, [BASE, GLOSS])
    assert [g['block'] for g in base['groups']] == list(range(61, 71))
    assert [g['block'] for g in gloss['groups']] == list(range(61, 71))
    expected = {}
    event_ids = set()
    for source, meaning in zip(base['groups'], gloss['groups']):
        assert source['block'] == meaning['block']
        assert source['clean_block_sha256'] == meaning['source_block_sha256']
        assert source['source_event_records'] == meaning['source_event_records']
        assert len(source['records']) == len(meaning['records'])
        for raw, note in zip(source['records'], meaning['records']):
            assert all(note[k] == v for k, v in raw.items())
            assert note['current_English_dialogue_still_unconsulted']
            assert note['source_meaning_gloss'] and note['whole_exchange_fidelity_note']
        commands = source['commands']
        expected[source['block']] = (
            len(commands), len(source['records']),
            sum(c['word'] in [0x100, 0x200, 0x300, 0x400] for c in commands),
            sum(c['word'] in [0x8000, 0x8100] for c in commands),
            sum(c['word'] not in [0, 0x4000, 0x100, 0x200, 0x300, 0x400, 0x8000, 0x8100] for c in commands))
        event_ids.update(e['event_ID'] for e in source['source_event_anddependencies'])
    assert tuple(map(sum, zip(*expected.values()))) == (392, 224, 60, 15, 83)
    assert sorted(event_ids) == [0, 38, 44, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70]
    changes = {
        'Map complete clean B31/B53 controls in the own verified V8704 captain1 context.':
            'Map complete clean B61-B70 controls in the own verified V8865 captain1 context.',
        'scripts.Hodram_B31_B53_registered_route_context_v8781':
            'scripts.Hodram_B54_B60_registered_route_context_v8868',
        'work/analysis/Hodram_B54_B60_source_controls_v8791':
            'work/analysis/Hodram_B61_B70_source_controls_v8878',
        'work/analysis/Hodram_next_clean_gloss_v8787/82_qualified_clean_glosses_no_unbound_gender_orFA_type.json': str(GLOSS).replace('\\', '/'),
        'work/analysis/Hodram_next_clean_v8785/complete_clean_SC1_B54_B60_EV1_andcoverage_before_current_English.json': str(BASE).replace('\\', '/'),
        'work/analysis/current_V8778_Hodram_native_v8781/current_native_input.json':
            'work/analysis/current_V8865_Hodram_native_v8868/current_native_input.json',
        "assert gloss['all82_clean_utterances_andseven_complete_blocks_read_before_earlier_English'] and all(r['current_English_dialogue_still_unconsulted'] for g in gloss['groups'] for r in g['records'])":
            """assert gloss['all224_complete_clean_first_meanings_before_current_English'] and all(r['current_English_dialogue_still_unconsulted'] for g in gloss['groups'] for r in g['records'])
    assert len(base['groups'])==len(gloss['groups'])==10
    for original,meanings in zip(base['groups'],gloss['groups']):
        assert original['block']==meanings['block'] and original['clean_block_sha256']==meanings['source_block_sha256']
        assert original['source_event_records']==meanings['source_event_records'] and len(original['records'])==len(meanings['records'])
        for raw,note in zip(original['records'],meanings['records']):
            assert all(note[k]==v for k,v in raw.items()) and note['source_meaning_gloss'] and note['whole_exchange_fidelity_note']
            assert note['current_English_dialogue_still_unconsulted'] and note['meaning_read_in_complete_clean_exchange']""",
        'all-routes-unified-v8778': 'all-routes-unified-v8865',
        "for group in gloss['groups']:": "for group in base['groups']:",
        "[15,54,55,56,57,58,59,60,65,76,128,129,142]": repr(sorted(event_ids)),
        'not_current_eligibility_or_selected_Hodram_B54_B60_activation':
            'not_current_eligibility_or_selected_Hodram_B61_B70_activation',
        '::entry-ownV8778': '::entry-ownV8865',
        "for source in gloss['groups']:": "for source in base['groups']:",
        'number in [54,55,56,57,58,59,60]': 'number in '+repr(list(range(61,71))),
        "result=ctx.execute(probe,block,command);ctx.machines.pop();assert result['native_result'][0]==2 and result['no_predicate_or_event_flag_forced'];queries.append(result)":
            """result=ctx.execute(probe,block,command);ctx.machines.pop();assert result['native_result'][0]==2 and result['no_predicate_or_event_flag_forced']
                if word==0x8100:
                    event_ID=struct.unpack_from('<H',block,at+2)[0]
                    assert result['native_result'][1] in [0,1] and len(result['original_event_completion_calls'])==1
                    assert result['original_event_completion_calls'][0]['args'][1]==event_ID
                    result['source_event_operand_ID']=event_ID
                    result['original_event_getter_unforced_not_outer_activation_or_plot_semantics']=True
                else:assert result['original_event_completion_calls']==[]
                queries.append(result)""",
        '{54:(7,4,0,0,2),55:(3,1,0,0,1),56:(7,3,0,0,3),57:(11,8,0,0,2),58:(98,49,24,6,18),59:(14,7,0,0,6),60:(12,10,0,0,1)}': repr(expected),
        "len(groups)==7 and sum(len(g['complete_source_preambles']) for g in groups)==82":
            "len(groups)==10 and sum(len(g['complete_source_preambles']) for g in groups)==224",
        'complete_source_commands=152,complete_speech_preambles=82,relative_sites=24,native_relative_cases=120,raw_unforced_query_cases=6,opaque_structural_decode_pairs=33,normal_seeded_end_cases=175':
            'complete_source_commands=392,complete_speech_preambles=224,relative_sites=60,native_relative_cases=300,raw_unforced_query_cases=15,opaque_structural_decode_pairs=83,normal_seeded_end_cases=250',
        'all7_complete_normal_ends_preserve_existing_result_values_all6words_andguards':
            'all10_complete_normal_ends_preserve_existing_result_values_all6words_andguards',
        'all33_nonprose_resource_scene_andgameplay_bridges_are_structural_not_invented_effect_semantics':
            'all83_nonprose_resource_scene_andgameplay_bridges_are_structural_not_invented_effect_semantics',
        'current_B54_B60_English_dialogue_bodies_still_unconsulted':
            'current_B61_B70_English_dialogue_bodies_still_unconsulted',
        'B54-B60 source:152commands/82preambles/120branchcases/6unforcedqueries/33nonprose pairs/175whole normalends inownV8778.':
            'B61-B70 source:392commands/224preambles/300branchcases/15unforcedqueries/83nonprose pairs/250whole normalends inownV8865.'
    }
    result = derive('scripts/prove_Hodram_B54_B60_source_controls_v8791.py',
                    'scripts/prove_Hodram_B61_B70_source_controls_v8878.py', changes)
    ROOT.mkdir(parents=True)
    save(ROOT/'source_locked_derivation.json', dict(derivation=result,
        inventory_counts=expected, event_IDs=sorted(event_ids),
        all224_original_record_values_exact_in_first_meanings=True,
        original_probes_ownership_canaries_ABI_runtime_guards_preserved=True,
        event_completion_query_additionally_binds_its_original_operand=True,
        current_English_unread=True, new_credit=0, full_goal_complete=False))
    print('Prepared complete 224-speech/392-command native controls successor; no native tests executed yet.')
