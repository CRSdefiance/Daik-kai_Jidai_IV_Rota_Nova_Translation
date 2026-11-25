"""Select bounded Lil exchanges and schedule menu input after the opening A pulse."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

prior = Path('scripts/select_lil382_display_v1.py').read_text(encoding='utf-8')
start = prior.index("    cases = [")
end = prior.index('    specs, union', start)
purpose_start = prior.index("            purpose=")
purpose_end = prior.index("'))", purpose_start) + 3
source = checked_text(prior, {
    'Lil382_residual_A_clean_20261110': 'Lil269_B243_B282_clean_20261110',
    'reconstruction_v2/reconstruction.json': 'reconstruction_v1/reconstruction.json',
    "stored['complete_stored_pages'] == 386": "stored['complete_stored_pages'] == 264",
    prior[start:end]: """    cases = [('Lil269_expedition_figurehead', list(range(243,251)), 0),
             ('Lil269_ruins_riddle', [251], 2),
             ('Lil269_spy_capture_rewards', [263,264,265,267,268,270,271], 0)]
""",
    "                frame = 3900 + (units-1)*240":
        "                menu_index = {(251,270):2, (251,1752):1}.get((obj['block'],obj['source_command_offset']),0)\n                assert 0 <= menu_index < obj['caption_count']\n                frame = 4000 + (units-1)*240",
    "captures += [frame-40, frame+20, frame+80, frame+120]":
        "captures += [frame-40, frame+20, frame+80, frame+140, frame+200]",
    'for step in range(choice)': 'for step in range(1,menu_index+1)',
    'expected_index=choice, caption_count=': 'expected_index=menu_index, caption_count=',
    prior[purpose_start:purpose_end]: """            purpose='Representative initialized Lil269 SC2 command QA: expedition directions and figurehead branches, '
                    'the complete repaired FE riddle and three/two-choice captions, both effective personality objects, '
                    'spy/deception/capture exchanges, reward notices, two-page paragraphs, names and host returns. '
                    'Conditional alternatives are concatenated without copying their outcomes. '
                    'No natural activation, original reward/branch result, geography, chronology, full route or hardware claim.'))""",
    'len(seen_menus) == 2': 'len(seen_menus) == 3',
    'unvisited_source_bodies=378-len(union)': 'unvisited_source_bodies=262-len(union)',
})

if __name__ == '__main__':
    exec(compile(source, __file__ + '::same-source-commands-complete-scope-and-buffer-guards', 'exec'),
         {'__file__': __file__, '__name__': '__main__'})
