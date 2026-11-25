"""Seal all 135 clean-first records before opening the registered English."""
import inspect
from pathlib import Path

from scripts import seal_rafael_B261_B264_clean_v1 as earlier
from scripts.audit_story_glyph_consistency import load, save
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = earlier.ROOT
OUTPUT = ROOT/'B265_B280_clean_drafts_v1.json'
DRAFT = Path('translations/rafael_B265_B280_clean_drafts_v1.txt')
SEALED = ROOT/'sealed_clean_first_v1'
BLOCKS = list(range(261,281))
digest = earlier.digest

source = checked_text(inspect.getsource(earlier.main), {
    "len(rows) == 57 and sum(row.get('kind') == 'actor-style-alternative' for row in rows) == 16":
        "len(rows) == 78 and not any(row.get('kind') == 'actor-style-alternative' for row in rows)",
    "sum(row.get('kind') == 'typed-choice-label' for row in rows) == 5":
        "not any(row.get('kind') == 'typed-choice-label' for row in rows)",
    'records_count=57, ordinary_speeches=36, style_alternatives=16':
        'records_count=78, ordinary_speeches=78, style_alternatives=0',
    'typed_captions=5': 'typed_captions=0',
    'Sealed 57 clean-source drafts across four complete Rafael exchanges.':
        'Sealed 78 clean-source drafts across B265–B280.',
})
env = {**vars(earlier), 'OUTPUT':OUTPUT, 'DRAFT':DRAFT, 'BLOCKS':BLOCKS[4:], '__file__':__file__}
exec(compile(source, __file__+'::whole-clean-exchanges', 'exec'), env)


def main():
    assert not SEALED.exists()
    env['main']()
    packet, style, menu, first, last = map(load, (earlier.PACKET, earlier.STYLES, earlier.MENUS, earlier.OUTPUT, OUTPUT))
    drafts = (first, last)
    assert [block for doc in drafts for block in doc['complete_blocks']] == BLOCKS
    assert all(doc['all_five_gates_pending'] and doc['no_current_English_extracted_for_this_intake_before_drafts'] for doc in drafts)
    assert all(digest(path) == expected for doc in drafts for path, expected in doc['evidence'].items())
    speech = [row for group in packet['groups'] for row in group['records']]
    records = [row for doc in drafts for row in doc['records']]
    ids = {row['id']:row for row in records}
    assert len(records) == len(ids) == 135
    for clean in speech + style['records'] + menu['records']:
        row = ids[clean['id']]
        assert all(row[key] == value for key, value in clean.items()) and not any(row['review'].values())
    ledger = load('translations/editorial_review_current_v1.json')['contextual_story_natural_dialogue_pass_v1871']
    key = lambda row: (row['file_path'],row['id'])
    assert set(map(key,records)).isdisjoint(map(key,ledger['integrated_record_keys']))
    SEALED.mkdir()
    sealed = SEALED/'sealed_drafts.json'
    save(sealed, dict(records=sorted(records,key=lambda row:(row['block'],row['source_reference']['offset'])),
        records_count=135, ordinary_speeches=114, physical_style_alternatives=16, style_objects=2,
        style_alias_slots=16, typed_captions=5, typed_choice_objects=2, control_only_blocks=[],
        complete_blocks=BLOCKS, source_contexts={k:v for doc in drafts for k,v in doc['source_contexts'].items()},
        source_meanings_andlogical_drafts_sealed_before_current_ROM_English_extraction_in_this_intake=True,
        all_individual_review_gates_pending=True, no_already_credited_record_keys=True, new_credit=0,
        evidence={str(path):digest(path) for path in (earlier.PACKET,earlier.STYLES,earlier.MENUS,earlier.OUTPUT,OUTPUT,Path(__file__))}))
    shared = dict(source_packet=str(earlier.PACKET),source_packet_sha256=digest(earlier.PACKET),
        all_drafts_sealed=str(sealed),all_drafts_sha256=digest(sealed),new_credit=0)
    save(SEALED/'current_binding_meanings.json',dict(records=[
        {**ids[row['id']],'current_ROM_English_unconsulted':True} for row in speech],meanings=114,**shared))
    for key, doc in (('style_meanings',style),('choice_meanings',menu)):
        save(SEALED/f'{key}.json',{**doc,**shared,'records':[ids[row['id']] for row in doc['records']]})
    print('All 135 clean-source drafts are sealed before registered English comparison.')


if __name__ == '__main__':
    main()
