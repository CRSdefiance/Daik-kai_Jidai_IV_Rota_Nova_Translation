"""Keep complete live-menu checks and prove the exact adjacent Other -> Run away transition."""
from scripts import analyze_maria390_menu_actual_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous.source,{
    "        assert len(presses)==1,('A return not isolated between menu and next dialogue',final_menu_frame,right,presses)":
        """        consecutive=(declared['block'],declared['source_command_offset'])==(252,882)
        if consecutive:
            assert sha(args.fixture.read_bytes())=='389d6b91d94b2c370c466b9e79ff3b4d1097945f7a1ebd5d78896fa28ea6a210'
            assert len(presses)==2 and presses==[29680,29920] and final_menu_frame==29660 and right==29938
        else:
            assert len(presses)==1,('A return not isolated between menu and next dialogue',final_menu_frame,right,presses)""",
    "source_command_offset=declared['stored_command_offset'],count=count,":
        "source_command_offset=declared['stored_command_offset'],count=count,consecutive_menu_before_following_speech=consecutive,",
    '    args.out.mkdir();chosen=[]':
        """    assert [(m['block'],m['clean_source_command_offset']) for m in menus]==[(221,270),(252,882),(252,1876)]
    first,second=fixture['menus'][1:]
    assert first['fixture_offset']+len(bytes.fromhex(first['command_hex']))==second['fixture_offset']
    assert first['word']==0x2200 and second['word']==0x2100
    first_samples=[s for s in samples if s['source_command_offset']==first['stored_command_offset'] and s['visible_selected_option'] is not None]
    second_samples=[s for s in samples if s['source_command_offset']==second['stored_command_offset'] and s['visible_selected_option'] is not None]
    assert first_samples[-1]['visible_selected_option']==2 and second_samples[-1]['visible_selected_option']==1
    first_A,second_A=menus[1]['observed_default_return_A_input'],menus[2]['observed_default_return_A_input']
    assert first_samples[-1]['frame']<first_A<second_samples[0]['frame']<=second_samples[-1]['frame']<second_A<menus[2]['following_speech_frame']
    assert [r['start'] for r in inputs if r['buttons']==['A'] and first_samples[-1]['frame']<r['start']<=second_samples[0]['frame']]==[first_A]
    assert [r['start'] for r in inputs if r['buttons']==['A'] and second_samples[-1]['frame']<r['start']<=menus[2]['following_speech_frame']]==[second_A]
    consecutive_transition=dict(first_source_menu=[252,882],next_source_menu=[252,1876],
        complete_command_adjacency_exact=True,first_selected_index=2,second_selected_index=1,
        first_menu_last_selected_capture=first_samples[-1],second_menu_first_selected_capture=second_samples[0],
        second_menu_last_selected_capture=second_samples[-1],first_A=first_A,second_A=second_A,
        following_speech=menus[2]['following_speech'],following_speech_frame=menus[2]['following_speech_frame'],
        each_complete_caption_cursor_background_andone_normal_A_per_transition_pass=True)
    args.out.mkdir();chosen=[]""",
    'ordinary_A_return_to_next_fixture_speech_observed=True,':
        'ordinary_A_return_to_next_fixture_speech_observed=False,ordinary_A_returns_to_next_menu_or_fixture_speech_observed=True,consecutive_menu_transition=consecutive_transition,',
})
if __name__=='__main__':exec(compile(source,__file__+'::same-complete-native-planes-andtwo-exact-one-A-transition-intervals','exec'),globals())
