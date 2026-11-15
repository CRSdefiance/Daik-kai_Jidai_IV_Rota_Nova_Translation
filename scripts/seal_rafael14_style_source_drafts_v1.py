"""Seal newly inventoried style meanings before decoding current style-body English."""
import struct
from copy import deepcopy
from pathlib import Path
from translations.rafael_B113_B119_style_source_drafts_v1 import ROWS
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

SOURCE=Path('work/analysis/Rafael_B101_B120_clean_20261105/clean_style_objects_v1.json')
OUT=SOURCE.with_name('14_style_meanings_andindependent_drafts_v1.json')

if __name__=='__main__':
    assert not OUT.exists();d=deepcopy(load(SOURCE));main=load('translations/rafael_B101_B120_contextual_editorial_manuscript_v4.json')
    assert (d['object_count'],d['physical_alternatives'],d['style_alias_slots'])==(2,14,16)
    seen=set()
    for row in d['records']:
        offset=row['source_reference']['offset']-row['source_command_offset']-20
        key=row['block'],offset;assert key not in seen;seen.add(key)
        meaning,english=ROWS[key];assert english.isascii() and not any(c in english for c in '\r\n\t')
        assert row['source_selector']==208 and all(v==0 for v in row['source_macros'].values())
        raw=bytes.fromhex(row['source_choice_object_hex']);slots=struct.unpack_from('<8H',raw,2)
        assert [i for i,v in enumerate(slots) if v==offset]==row['source_style_indices']
        context=next(r['context'] for r in main['records'] if r['block']==row['block'])
        context=('A runtime-selected companion first calls the admiral to look at the temple object. ' if row['block']==113 else
            'A runtime-selected companion first reports the dead end, before the embedded jar-shaped tablet is described. ')+context
        row.update(source_meaning=meaning,english=english,independent_English_draft=english,context=context,
            speaker='Runtime-selected companion, role1; fixed identity not inferred',native_object_kind='4100-style-alternative',
            native_role_voice_alias_controls_andformatting_pending=True,current_style_English_not_decoded_in_this_extension_intake=True,
            prior_whole_command_hex_was_available_in_current_packet=True,no_blanket_historical_English_exposure_claim=True,
            review=dict(source=True,context=True,localization=False,naturalness=True,formatting=False),new_credit=0)
    assert seen==set(ROWS)
    d.update(source_meanings_andindependent_drafts_sealed_before_current_style_English_decoding=True,
        current_4000_speech_andmenu_English_already_reviewed=True,earlier_current_style_object_hex_exposure_disclosed=True,
        all14_style_current_comparisons_andnative_role_bindings_pending=True,full_scope_objects_now255=True,
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,Path('translations/rafael_B113_B119_style_source_drafts_v1.py'),Path(__file__)]},new_credit=0)
    save(OUT,d);print('Sealed14 clean-first style meanings/drafts and16 source alias slots; earlier command-hex exposure disclosed.')
