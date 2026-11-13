"""Make three clean-only refinements and record the authored gloss-before-draft schema."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT = Path('work/Lil382_residual_A_clean_20261110')


def main():
    changes = {
        'DK4_MES_B3_R0020': "Angel! Bring us around to the enemy's starboard quarter!",
        'DK4_MES_B238_R0023': 'It looks like one of my crewmates hurt his hand.',
        'DK4_MES_B115_R0099': 'Wait. Your anger should be directed at the corrupt merchants trading in slaves here in Africa and the ruthless soldiers who pillage.',
    }
    revised = []
    for part in ['B0_B21', 'B115_B235_B242']:
        before = ROOT/f'authored_{part}_v1.json'
        after = ROOT/f'authored_{part}_v2.json'
        assert not after.exists()
        original = load(before)
        result = deepcopy(original)
        assert original['whole_clean_exchanges_read_before_drafting'] and original['current_English_not_consulted']
        for row in result['records']:
            assert len(row) in [3, 4] and all(row[:3])
            if row[0] in changes:
                revised.append(dict(id=row[0], source_meaning=row[1], before=row[2], after=changes[row[0]]))
                row[2] = changes[row[0]]
        result.update(source_gloss_precedes_independent_draft_in_each_entry=True,
            source_meaning_column=1, independent_draft_column=2,
            previous_authored=str(before), previous_authored_sha256=digest(before),
            clean_only_refinement_before_current_English=True,
            refinement_reasons='Use precise nautical starboard-quarter direction;avoid inferring friendship from crewmate;avoid adding plural villages to the pillaging accusation.',
            all_original_authored_tables_andpart_outputs_preserved=True)
        save(after, result)
    assert {r['id'] for r in revised} == set(changes)
    save(ROOT/'clean_draft_amendments_v1.json', dict(records=revised, current_English_not_consulted=True,
        names_andnative_consumers_still_pending=True, new_credit=0,
        evidence={str(Path(__file__)): digest(__file__)}))
    print('Saved three clean-only refinements;source glosses precede drafts;all originals preserved.')


if __name__ == '__main__':
    main()
