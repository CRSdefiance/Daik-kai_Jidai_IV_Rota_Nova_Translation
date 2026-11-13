"""Check production B52 references, native command inventories and full ROM inverses."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.hodram_B52_profile_v1 import validate_approved_batch, validate_runtime
from dk4tool.patch.hodram_B52_references_v1 import reconstruct_and_bind
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/Hodram_B52_references_production_v8677')
DOC = Path('translations/hodram_B52_editorial_manuscript_v6.json')
PATHS = dict(relocation='work/analysis/Hodram_B52_references_v8647/source_current_final_map.json',
    current='work/analysis/Hodram_B52_current_v8631/current_effective.json',
    source_controls='work/analysis/Hodram_B52_source_controls_v8620/source_controls.json')

if __name__ == '__main__':
    assert not ROOT.exists()
    doc = read(DOC)
    data = {k: read(p) for k, p in PATHS.items()}
    parent, reference, clean = [NdsImage.open(p) for p in [doc['current_ROM'], doc['reference_ROM'], 'work/clean.nds']]
    validate_approved_batch(doc)
    validate_runtime(parent)
    before = bytes(parent.rom.save())

    def require(value, message):
        if not value:
            raise ValueError('B52 production references:' + message)

    result = reconstruct_and_bind(parent, clean, reference, doc, data, require)
    assert result['summary']['editorial_references'] == 5 and result['summary']['whole_reference_ROM_equal']
    negatives = []

    def reject(label, changed):
        assert changed != doc
        try:
            reconstruct_and_bind(parent, clean, reference, changed, data, require)
        except ValueError as error:
            assert 'Native dependency changed' not in str(error)
            negatives.append(dict(label=label, actual_changed_input=True, rejected=True, diagnostic=str(error)))
        else:
            raise AssertionError('Changed reference accepted:' + label)
        assert bytes(parent.rom.save()) == before

    for field in ['records', 'typed_choice_records']:
        for index, row in enumerate(doc[field]):
            for reference_field in ['source_reference', 'current_reference', 'final_reference']:
                changed = deepcopy(doc)
                changed[field][index][reference_field]['offset'] += 2
                reject(row['id'] + ':' + reference_field, changed)
            changed = deepcopy(doc)
            changed[field][index]['final_hex'] += '20'
            reject(row['id'] + ':final-byte', changed)
    assert len(negatives) == 20 and bytes(parent.rom.save()) == before
    ROOT.mkdir(parents=True)
    save(ROOT / 'references_production_validation.json', dict(summary=result['summary'], negative_cases=negatives, negative_count=20,
         every_input_change_semantically_rejected_before_ROM_commit=True,
         all_clean_current_final_speech_andtyped_references_native_inventories_andwhole_ROM_inverse_independent=True,
         no_native_CPU_producer_oractual_capture_replay=True, no_ROM_registry_orcredit_mutation=True,
         new_credit=0, full_goal_complete=False,
         evidence={str(p): sha(Path(p).read_bytes()) for p in [DOC, *PATHS.values(), __file__, 'dk4tool/patch/hodram_B52_references_v1.py']}))
    print('B52 production references:5 disjoint source/current/final references/all14 commands/whole archive andROM inverses;20 semantic reference defects reject. No commit/credit.')
