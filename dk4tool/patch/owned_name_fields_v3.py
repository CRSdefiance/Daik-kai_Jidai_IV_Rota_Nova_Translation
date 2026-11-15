"""Extend fixed-slot proofs to explicitly reviewed complete owner groups."""
import inspect

from dk4tool.patch import owned_name_fields_v2 as previous
from scripts.source_locked_derivation_v5118 import checked_text


def source_bound_owners(arm, clean, table, clean_table, row, owners):
    expected = [dict(actor=row['actor'], column=row['column'], pointer=row['pointer'],
                     field_offset=row['table_field_offset'])]
    aliases = row.get('reviewed_aliases', [])
    for alias in aliases:
        actor, column = alias['actor'], alias['column']
        if not (0 <= actor < 207 and column in [0, 4, 8]):
            raise ValueError('Ordinary reviewed alias field required')
        if not all(alias['review'][g] is True for g in ['source', 'context', 'localization', 'naturalness']) or not alias['reason'].strip():
            raise ValueError('Every shared owner needs its individual editorial review')
        field = table - previous.BASE + 32 * actor + column
        pointer = previous.struct.unpack_from('<I', arm, field)[0]
        if pointer != row['pointer'] or field != alias['table_field_offset']:
            raise ValueError('Exact whole-string shared owner required; interior aliases forbidden')
        source = alias['source_clean_component']
        clean_field = clean_table - previous.BASE + 32 * actor + column
        clean_pointer = previous.struct.unpack_from('<I', clean, clean_field)[0]
        raw = bytes.fromhex(source['hex'])
        if not (source['column'] == column and source['source_ARM9_field_offset'] == clean_field
                and source['pointer'] == clean_pointer and source['offset'] == clean_pointer - previous.BASE
                and clean[clean_pointer - previous.BASE:clean_pointer - previous.BASE + len(raw) + 1] == raw + b'\0'
                and raw.decode('cp932') == source['text'] == row['source_clean_component']['text']):
            raise ValueError('Exact individually matching clean alias component required')
        expected.append(dict(actor=actor, column=column, pointer=pointer, field_offset=field))
    if len({(o['actor'], o['column']) for o in expected}) != len(expected):
        raise ValueError('Duplicate shared-owner review')
    expected.sort(key=lambda o: (o['actor'], o['column']))
    return owners == row['owners'] == expected


source = checked_text(inspect.getsource(previous.plan_arm9_name_fields), {
    "proposal['format']=='dk4-owned-name-fields-proposal-v2'":
    "proposal['format']=='dk4-owned-name-fields-proposal-v3'",
    "owners==row['owners']==[dict(actor=actor,column=column,pointer=pointer,field_offset=field)]":
    "source_bound_owners(arm,clean,table,clean_table,row,owners)",
    "'Exclusive name ownership including all interior aliases required'":
    "'All shared owners must be individually source-bound and reviewed; interior aliases forbidden'",
    "references==row['aligned_ARM9_references']==[dict(offset=field,pointer=pointer)]":
    "references==row['aligned_ARM9_references']==sorted([dict(offset=o['field_offset'],pointer=o['pointer']) for o in owners],key=lambda o:o['offset'])",
    'exclusive_owners=owners,': 'source_bound_owners=owners,reviewed_aliases=row.get(\'reviewed_aliases\',[]),',
})
env = {**previous.plan_arm9_name_fields.__globals__, 'source_bound_owners': source_bound_owners}
exec(compile(source, __file__ + '::same-fixed-slot-proof-with-complete-owner-groups', 'exec'), env)
plan_arm9_name_fields = env['plan_arm9_name_fields']
