"""Save authored clean meanings before independent drafts, with exact source bindings."""
import argparse
from collections import Counter
from copy import deepcopy
from pathlib import Path
import struct
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.qualify_rafael351_item_and_UI_terms_v1 import string


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ['packet','authored','out']:
        parser.add_argument('--'+name,type=Path,required=True)
    args = parser.parse_args()
    assert not args.out.exists()
    packet, authored = map(load,[args.packet,args.authored])
    assert packet['source_only_not_current_English']
    groups = [g for g in packet['groups'] if str(g['block']) in authored['contexts']]
    assert {str(g['block']) for g in groups} == set(authored['contexts'])
    expected = {r['id']:r for g in groups for r in g['records']}
    supplied = {r[0]:r for r in authored['records']}
    assert len(supplied) == len(authored['records']) == len(expected) and supplied.keys() == expected.keys()
    clean = NdsImage.open(packet['source_ROM'])
    assert digest(packet['source_ROM']) == packet['source_ROM_sha256']
    arm = clean.read_file('/__arm9__.bin')
    from dk4tool.patch.grand_race_menu_release import sha
    assert sha(arm) == packet['source_ARM9_sha256']
    base = struct.unpack_from('<I',arm,0xCDAC0)[0]-0x02000000
    meanings, drafts, actors = [], [], {}
    for group in groups:
        block = bytes.fromhex(group['clean_block_hex'])
        for original in group['records']:
            ident, meaning, english, *notes = supplied[original['id']]
            assert meaning.strip() and english.strip() == english and '\n' not in english
            assert english.encode('ascii') and not any(t in english for t in ['{LB','{PAD','{ALIGN'])
            row = deepcopy(original)
            at = row['source_reference']['offset']
            raw = bytes.fromhex(row['source_hex'])
            assert block[at:at+len(raw)] == raw and not row['covered']
            row.update(source_meaning=meaning,whole_exchange_context=authored['contexts'][str(group['block'])],
                source_meaning_reviewed_from_complete_clean_exchange=True,current_English_not_consulted=True,
                independent_draft_pending=True,contextual_comparison_pending=True,new_credit=0)
            if row['kind']=='ordinary-speech':
                selector = raw[0]
                row.update(source_selector=selector,source_complete_preamble_hex=block[at-5:at+1].hex())
                if selector<207:
                    fields=[]
                    for column,pointer in enumerate(struct.unpack_from('<3I',arm,base+32*selector)):
                        fields.append(dict(field_offset=base+32*selector+4*column,pointer=pointer,
                            value=string(arm,pointer) if pointer else None))
                    actors[selector]=fields
                    row['clean_static_actor_components']=[f['value']['text'] if f['value'] else '' for f in fields]
                else:
                    assert selector in [207,208,254]
                    row['dynamic_or_FE_identity_requires_native_consumer_binding']=True
            source_macros={token:row['source_Japanese'].count(token) for token in ['FI','FA','FO','FU']}
            assert source_macros == {token:english.count(token) for token in source_macros},ident
            row['source_macros']=source_macros
            meanings.append(row)
            draft=deepcopy(row)
            draft.update(independent_English_draft=english,english=english,independent_draft_pending=False,
                localized_independently_from_sealed_clean_meaning=True,logical_paragraph_without_authored_wraps=True,
                localization_note=notes[0] if notes else 'Natural independent wording of the clean exchange; names, item titles and native consumers still require scoped binding.',
                names_andUI_terms_provisional_until_consumer_binding=True,
                review=dict(source=False,context=False,localization=False,naturalness=False,formatting=False))
            drafts.append(draft)
    args.out.mkdir()
    common=dict(source_packet=str(args.packet),source_packet_sha256=digest(args.packet),
        authored=str(args.authored),authored_sha256=digest(args.authored),complete_exchanges=len(groups),
        blocks=[g['block'] for g in groups],current_English_not_consulted=True,new_credit=0,
        source_actor_fields_are_static_identity_evidence_not_native_dispatch_orname_UI_approval=True,
        clean_actor_fields=[dict(actor_ID=k,fields=v) for k,v in sorted(actors.items())],
        evidence={str(p):digest(p) for p in [args.packet,args.authored,Path(__file__)]})
    meanings_path=args.out/'clean_meanings.json'
    save(meanings_path,dict(common,records=meanings,source_meanings=len(meanings),independent_drafts_not_yet_saved=True))
    assert load(meanings_path)['records']==meanings
    save(args.out/'independent_drafts.json',dict(common,records=drafts,source_meanings=str(meanings_path),
        source_meanings_sha256=digest(meanings_path),independent_drafts=len(drafts),
        all_contextual_comparisons_names_terms_andfive_gates_pending=True,
        translation_policy='natural-dialogue-v2',target_locale='en-US'))
    print(dict(meanings=len(meanings),independent_drafts=len(drafts),complete_exchanges=len(groups),
        kinds=dict(Counter(r['kind'] for r in drafts)),current_English_not_read=True,new_credit=0))


if __name__=='__main__':main()
