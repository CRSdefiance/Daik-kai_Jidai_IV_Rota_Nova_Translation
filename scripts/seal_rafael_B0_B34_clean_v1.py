"""Seal 35 complete residual SC0 exchanges before current-English extraction."""
import re
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest


ROOT = Path('work/Rafael_B0_B34_clean_20261106')
AUDIT = Path('work/analysis/Rafael_source_coverage_20261106_v2/coverage.json')
RESIDUAL = AUDIT.with_name('residual_clean_source_packet.json')
PACKET = ROOT / 'clean_source_packet.json'
STYLES = ROOT / 'clean_style_objects.json'
MENUS = ROOT / 'clean_choice_objects.json'
SEALED = ROOT / 'sealed_clean_first_v1'
DRAFTS = [Path(f'translations/rafael_{label}_clean_drafts_v1.txt')
          for label in ('B0_B13', 'B14_B25', 'B26_B34')]


def main():
    assert not ROOT.exists()
    audit, residual = map(load, (AUDIT, RESIDUAL))
    assert not audit['inventory_failures'] and not audit['legacy_source_bindings_not_exact']
    assert len(audit['missing']) == 283 and all(r['kind'] == 'ordinary-speech' for r in audit['missing'])
    assert digest('translations/editorial_review_current_v1.json') == audit['ledger_sha256']
    assert digest('work/clean.nds') == audit['source_ROM_sha256']
    image = NdsImage.open('work/clean.nds')
    blocks = IlnkContainer.parse(image.read_file('/data/SC0.DK4')).blocks
    groups, source = [], {}
    for group in residual['groups']:
        n, commands = group['block'], group['all_source_commands']
        block = blocks[n]
        assert block.hex() == group['clean_block_hex']
        command_map = {r['offset']: r for r in commands}
        assert not any(r['word'] in (0x2100, 0x2200, 0x4100) for r in commands)
        rows = []
        for original in group['records']:
            assert not original['covered']
            raw = bytes.fromhex(original['source_hex'])
            at = original['source_reference']['offset']
            command = command_map[at-5]
            assert command['word'] == 0x4000 and block[at:at+len(raw)] == raw
            row = dict(id=original['id'], file_path='/data/SC0.DK4', block=n,
                source_selector=raw[0], source_hex=raw.hex(),
                source_complete_preamble_hex=block[at-5:at+1].hex(),
                source_reference=dict(file_path='/data/SC0.DK4', block=n, offset=at,
                    header_offset=at-5, record_index=block[:at].count(b'\0'), length=len(raw)),
                source_Japanese=raw[1:].decode('cp932'), source_decode_error=None,
                source_0100_ancestors=command['ancestor_0100_offsets'], native_extent=command['native_extent'],
                source_macros={m:raw[1:].count(m.encode()) for m in ('FI','FA','FO')},
                earlier_English_unconsulted=True, source_context_localization_formatting_gates_pending=True)
            source[row['id']] = row; rows.append(row)
        groups.append({**group, 'records': rows})
    assert [g['block'] for g in groups] == list(range(35)) and len(source) == 283
    contexts, records = {}, []
    for path in DRAFTS:
        active = None
        for line in path.read_text(encoding='utf-8').splitlines():
            if not line or line.startswith('#'):
                continue
            ident, meaning, english = line.split('|', 2)
            if ident.startswith('@'):
                active = int(ident[1:])
                assert active not in contexts and meaning and not english
                contexts[active] = meaning
                continue
            row = source.pop(ident)
            assert row['block'] == active and meaning and english and english.isascii(), ident
            assert not any(t in english for t in ('{LB', '{ALIGN', '{PAD}', '\t')), ident
            tokens = [t.decode() for t in re.findall(rb'F[AOIU]', bytes.fromhex(row['source_hex'])[1:])]
            assert re.findall(r'\bF[AOIU]\b', english) == tokens, ident
            records.append({**row, 'source_meaning': meaning, 'independent_English': english,
                'context': contexts[active], 'native_literal_tokens': tokens,
                'review': dict.fromkeys(('source','context','localization','naturalness','formatting'), False),
                'current_English_comparison_pending': True, 'new_credit': 0})
    assert not source and list(contexts) == list(range(35)) and len(records) == 283
    ROOT.mkdir(parents=True); SEALED.mkdir()
    save(PACKET, {**residual, 'groups': groups, 'records': 283,
        'clean_only_no_prior_English_ornew_editorial_credit': True,
        'coverage_audit': str(AUDIT), 'coverage_audit_sha256': digest(AUDIT)})
    shared = dict(source_packet=str(PACKET), source_packet_sha256=digest(PACKET), records=[], objects=[], new_credit=0)
    save(STYLES, {**shared, 'object_count':0, 'physical_alternatives':0, 'style_alias_slots':0})
    save(MENUS, {**shared, 'object_count':0, 'caption_count':0, 'label_free2000_controls':[]})
    sealed = SEALED / 'sealed_drafts.json'
    save(sealed, dict(records=records, records_count=283, ordinary_speeches=283, physical_style_alternatives=0,
        typed_captions=0, complete_blocks=list(range(35)), source_contexts=contexts,
        source_meanings_andlogical_drafts_sealed_before_current_ROM_English_extraction_in_this_intake=True,
        all_individual_review_gates_pending=True, no_already_credited_record_keys=True,
        terminology_qualification_pending=['Proof of Conquest','Muramasa','Bloodstained Shamshir','Xien','iron-armored ships'],
        scoped_name_localization_andglyph_consistency_pending=True, new_credit=0,
        evidence={str(p):digest(p) for p in (AUDIT, RESIDUAL, PACKET, STYLES, MENUS, *DRAFTS, Path(__file__))}))
    save(SEALED/'current_binding_meanings.json',dict(records=records, meanings=283, source_packet=str(PACKET),
        source_packet_sha256=digest(PACKET), all_drafts_sealed=str(sealed), all_drafts_sha256=digest(sealed), new_credit=0))
    print('Sealed 283 clean-first drafts across all 35 residual SC0 exchanges. Comparison and five gates remain.')


if __name__ == '__main__':
    main()
