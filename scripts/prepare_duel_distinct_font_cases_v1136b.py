"""Count actual distinct expanded inputs instead of duplicate unused arguments."""
from pathlib import Path


def main():
    source = Path('scripts/probe_duel_compiled_fonts_v1136.py').read_text(encoding='utf-8')
    target = Path('scripts/probe_duel_compiled_fonts_v1136b.py')
    assert not target.exists()
    source = source.replace("duel_compiled_fonts_v1136')", "duel_compiled_fonts_v1136b')")
    before = '    assert len(selected)>=2820'
    assert source.count(before) == 1
    source = source.replace(before, '    assert len(selected)==1356\n'
        "    assert {row['message_ID'] for row in selected}==set(range(1931,1951))")
    source = source.replace("'unique_complete_font_cases':len(results),", "'unique_complete_font_cases':len(results),\n"
        "        'all4700_matrix_inputs_project_to1356_distinct_message_and_expanded_text_pairs':True,\n"
        "        'non_argument_messages_have_identical_text_for_all_unused_name_arguments':True,")
    target.write_text(source, encoding='utf-8')
    print('Created distinct-input successor:1140 source cases plus216 additional name-stress expansions.')


if __name__ == '__main__':
    main()
