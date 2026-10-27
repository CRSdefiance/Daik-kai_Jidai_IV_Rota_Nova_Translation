"""Audit each independently timed menu's original blink states and actual returned choice."""
from pathlib import Path
if __name__ == '__main__':
    draft = Path('scripts/audit_lil_B166_actual_v4104.py')
    previous = Path('scripts/audit_lil_B166_actual_v4104b.py')
    text = draft.read_text(encoding='utf-8')
    changes = {
        "[p['word'] for p in selected if p['word'] & 0xFF00 == 0x6300] == [0x632B,0x632C]":
            "[p['word'] for p in selected if p.get('original_source_block') == 166 and p['word'] & 0xFF00 == 0x6300] == [0x632B,0x632C]",
        '    actualmenus = []': '''    def caption_style(picture,index):
        colors={picture.getpixel((101+x,272+20*index+y)) for y in range(12) for x in range(54)} & {(0,165,172),(205,198,180)}
        assert len(colors)==1
        return colors.pop()
    actualmenus = []''',
        "                color = picture.getpixel((x0,y0))\n                assert color == sourcepicture.getpixel((x0,y0))\n                assert color in ([(0,165,172),(205,198,180)] if index == option else [(205,198,180)])":
            "                color,sourcecolor=caption_style(picture,index),caption_style(sourcepicture,index)\n                allowed=[(0,165,172),(205,198,180)] if index==option else [(205,198,180)]\n                assert color in allowed and sourcecolor in allowed",
        "correct_selected_highlight_visible=picture.getpixel((101,272+20*option)) == (0,165,172),\n                transient_style_matches_paired_Japanese=True":
            "correct_selected_highlight_visible=caption_style(picture,option)==(0,165,172),\n                source_correct_selected_highlight_visible=caption_style(sourcepicture,option)==(0,165,172),\n                English_caption_styles=[caption_style(picture,i) for i in [0,1]],\n                Japanese_caption_styles=[caption_style(sourcepicture,i) for i in [0,1]],\n                menu_relative_ages=[frame-interval['start'],frame-byversion[option,'clean_Japanese']['actual_choice_command_pair']['start']],\n                original_permitted_blink_states_and_unselected_plain_style_pass=True)",
        "        assert holds and any(h['correct_selected_highlight_visible'] for h in holds)":
            "        assert holds and any(h['correct_selected_highlight_visible'] for h in holds) and any(h['source_correct_selected_highlight_visible'] for h in holds)",
        "evidence=evidence, producer_sha256=sha(Path(__file__).read_bytes()), full_goal_complete=False":
            "source_English_highlight_blink_phases_at_global_frames_are_recorded_without_false_RGB_equivalence=True, both_versions_visible_highlight_matches_returned_option_and_unselected_never_highlighted=True, preserved_failed_audits={str(p):sha(p.read_bytes()) for p in DRAFTS}, evidence=evidence, producer_sha256=sha(Path(__file__).read_bytes()), full_goal_complete=False",
    }
    # The replacement occupies a constructor argument tail; keep its closing parens once.
    changes["original_permitted_blink_states_and_unselected_plain_style_pass=True)"] = "original_permitted_blink_states_and_unselected_plain_style_pass=True"
    for old,new in changes.items():
        assert text.count(old) == 1, old
        text = text.replace(old,new)
    exec(compile(text,__file__,'exec'),dict(__name__='__main__',__file__=__file__,DRAFTS=[draft,previous]))
