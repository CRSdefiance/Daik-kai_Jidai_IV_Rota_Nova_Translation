"""Recheck all52 source records and all126 actual holds against current code."""

import struct
from pathlib import Path

from PIL import Image

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.levelup_stat_format import current_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.verify_arrival_native_v792 import prepared
from scripts.verify_ceremony_consumers_v808 import production_functions
from scripts.verify_ceremony_heroes_v825 import cstring,identity
from scripts.verify_levelup_gameplay_v819 import glyphs
from scripts.verify_ceremony_and_cliff_v829 import zero_origin_glyphs
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/cliff_editorial_v829')
SPECS = [
    ('work/analysis/ceremony_access_v810/prayer_gameplay_verification_v814.json','complete_scene_holds'),
    ('work/analysis/ceremony_access_v810/site_chant_gameplay_verification_v815.json','complete_scene_holds'),
    ('work/analysis/ceremony_access_v810/temple_preparations_gameplay_verification_v815.json','complete_scene_holds'),
    ('work/analysis/ceremony_access_v810/church_prayer_gameplay_verification_v815.json','complete_scene_holds'),
    ('work/analysis/ceremony_Athens_v816/Athens_Temple_chant_gameplay_verification_v816.json','complete_scene_holds'),
    ('work/analysis/ceremony_rand_v822/V820_uncontrolled_ceremony_display_and_state_v824.json','complete_ceremony_holds'),
    ('work/analysis/ceremony_heroes_v825/actual_hero_fast_and_retained64_verification.json','complete_scene_holds'),
    ('work/analysis/ceremony_heroes_v825/actual_hero_fast_and_retained64_verification.json','retained_refusal_holds'),
    ('work/analysis/ceremony_lil_v826/actual_Lil_temple_and_dance_verification.json','complete_scene_holds'),
    ('work/analysis/ceremony_istanbul_v827/four_preparation_variants_actual_verification.json','complete_scene_holds'),
    ('work/analysis/cliff_editorial_v829/last_Lil_ceremony_variant_v828.json','complete_scene_holds'),
]


def main():
    rom = NdsImage.open('out/all_routes_combined_v829_candidate.nds')
    arm,common,font = [rom.read_file(p) for p in ('/__arm9__.bin','/COMMON/MESFILE.DK4','/GRP/KANJI.FNT')]
    entries = current_entries(common,arm)
    clean = NdsImage.open('work/clean.nds')
    original = common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/__arm9__.bin'))
    source_rows = read('translations/ceremony_editorial_manuscript_v2.json')['records']
    production = {r['message_id']:r for r in read('translations/ceremony_editorial_manuscript_v3.json')['records']}
    blocks = IlnkContainer.parse(common).blocks
    ordinary,modal,_,_ = production_functions()
    wrapped,owner = [struct.unpack_from('<I',arm,n)[0] for n in (0x54450,0x552A0)]
    proofs, reports, samples = {}, {}, {}
    native_context = read('work/analysis/ceremony_context_v806/native_context.json')
    assert native_context['every52_source_ID_bound_to_original_caller']
    source_hashes = read('translations/levelup_stat_format_release_v1.json')
    supported_arm = {source_hashes['source_arm9_sha256'],source_hashes['target_arm9_sha256']}
    for proof_path,field in SPECS:
        proof = read(proof_path)
        proofs[proof_path] = sha(Path(proof_path).read_bytes())
        for index,hold in enumerate(proof[field]):
            number,frame,capture = hold['message_id'],hold['frame'],hold['capture']
            folder = Path(capture['path']).parent
            if str(folder) not in reports:
                report = read(folder/'capture_report.json')
                assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
                source_rom = NdsImage.open(report['ROM'])
                assert report['ROM_sha256'] == sha(source_rom.source.read_bytes())
                assert source_rom.read_file('/COMMON/MESFILE.DK4') == common
                assert source_rom.read_file('/GRP/KANJI.FNT') == font
                assert sha(source_rom.read_file('/__arm9__.bin')) in supported_arm
                snapshots = {r['frame']:r for r in report.get('read_only_capture_RAM_snapshots',[])}
                snapshots.update({r['frame']:r for r in report.get('read_only_pause_RAM_snapshots',[])})
                reports[str(folder)] = report,snapshots
            report,snapshots = reports[str(folder)]
            snap = snapshots[frame]
            raw = Path(snap['path']).read_bytes()
            assert sha(raw) == snap['sha256'] and len(raw) == 0x400000 and snap['read_only_export']
            assert sha(Path(capture['path']).read_bytes()) == capture['PNG_sha256']
            who = identity(arm,raw)
            assert who['captain'] in range(4) and who['town'] in (19,22)
            values = ((b'Parthenon' if who['town'] == 19 else b'Cappadocia'),) if number == 1219 else (
                (who['notice_name'].encode(),) if number in (290,291,293,294,295) else ())
            picture = Image.open(capture['path']).convert('RGB')
            if number == 64:
                encoded = entries[64].text
                lines = [encoded.decode()]
                zero_origin_glyphs(arm,font,picture,encoded,lines)
            else:
                case = (modal if number in (289,290,291,293,294,295) else ordinary)(prepared(arm),production[number],values)
                assert not case['findings']
                encoded,lines = bytes.fromhex(case['formatted_hex']),case['lines']
                glyphs(arm,font,picture,encoded,lines)
            assert cstring(raw,wrapped) == encoded and cstring(raw,owner+0x2030) == entries[number].text
            assert raw.count(blocks[entries[number].block]) == 1
            samples.setdefault(number,[]).append(dict(proof=proof_path,field=field,index=index,frame=frame,
                capture=capture,source_sample_ROM_sha256=report['ROM_sha256'],actual_captain=who['captain'],
                actual_notice_name=who['notice_name'],lines=lines,
                freshly_rechecked_current_native_independent_actual_font_blank_plane_and_resident_copy=True))
    assert sum(map(len,samples.values())) == 126 and len(samples) == 52
    records = []
    for row in source_rows:
        number = row['message_id']
        assert original[number].text == bytes.fromhex(row['source_hex'])
        assert original[number].text.decode('cp932') == row['japanese']
        assert entries[number].text.strip().decode('cp932') == row['english'].removesuffix('{PAD}')
        records.append(dict(message_id=number,decision=row['decision'],english=row['english'],
            Japanese=row['japanese'],source_meaning=row['source_meaning'],speaker=row['speaker'],context=row['context'],
            localization_note=row['localization_note'],source_hex=row['source_hex'],source_reference=row['source_reference'],
            completed_candidate_reference=dict(ROM_sha256=sha(rom.source.read_bytes()),block=entries[number].block,
                table_offset=entries[number].table_offset,block_offset=entries[number].block_offset,
                copy_end=entries[number].copy_end,current_text_hex=entries[number].text.hex()),
            actual_samples=samples[number],individual_message_has_complete_actual_sample=True,
            review={g:True for g in ('source','context','localization','naturalness','formatting')},
            final_review='Retain reviewed production wording after clean-source,voice,actual-context and complete-display recheck.'))
    assert sum(r['decision'] == 'revise' for r in records) == 30
    assert sum(r['decision'] == 'retain' for r in records) == 22
    for row in source_rows:
        old = ' '.join(row['current_English'].split())
        final = ' '.join(row['english'].removesuffix('{PAD}').split())
        assert (old == final) == (row['decision'] == 'retain'), row['message_id']
    save('translations/ceremony_editorial_final_review_v1.json',dict(format='dk4-ceremony-final-editorial-review-v1',
        candidate='out/all_routes_combined_v829_candidate.nds',candidate_sha256=sha(rom.source.read_bytes()),
        clean_source_sha256=sha(clean.source.read_bytes()),native_source_context_proof='work/analysis/ceremony_context_v806/native_context.json',
        native_source_context_sha256=sha(Path('work/analysis/ceremony_context_v806/native_context.json').read_bytes()),
        all52_source_prose_and_actual_unique_message_samples_complete=True,complete_actual_hold_rechecks=126,
        prose_revisions=30,retained_wordings=22,production_records_reencoded=51,
        source_proof_sha256=proofs,records=records,
        original_random_yield_semantics_retained=True,
        original_strict_trace_failures_not_relabelled_as_passes='docs/ceremony_random_cause_v824_checkpoint.md',
        no_every_frame_observer_transparency_hardware_or_full_route_claim=True,
        source335_336_only_additional_formatting_samples_not_editorially_completed=True,
        ceremony_family_editorial_complete=True,full_goal_complete=False,
        producer_sha256=sha(Path(__file__).read_bytes())))
    print('PASS:all52 clean-source meanings/wordings retained;all126 actual holds freshly match current native+independent fonts and full text pixels.',flush=True)


if __name__ == '__main__':
    main()
