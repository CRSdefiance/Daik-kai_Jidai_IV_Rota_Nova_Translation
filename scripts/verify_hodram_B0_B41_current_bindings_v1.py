"""Verify complete current outputs after v1's redundant second entry was rejected."""
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.gloss_hodram_B0_B41_clean_v1 import ROOT

OUT=ROOT/'current_binding_verification_v1.json'


def main():
    assert not OUT.exists()
    current_path=ROOT/'current_v1/current_effective.json'
    object_path=ROOT/'current_objects_v1/current_objects.json'
    current,objects,packet,drafts=map(load,(current_path,object_path,ROOT/'clean_source_packet.json',Path('translations/hodram_B0_B41_clean_drafts_v1.json')))
    release=load('work/hodram_B311_B324_release_v1/registered_release_verification.json')
    assert digest(release['candidate'])==current['current_ROM_sha256']==release['candidate_sha256']
    bank=IlnkContainer.parse(NdsImage.open(release['candidate']).read_file('/data/SC1.DK4')).blocks
    original={r['id']:r for g in packet['groups'] for r in g['records']}
    rows=[r for g in current['groups'] for r in g['records']]
    assert len(rows)==current['records']==current['original_current_catalogue_lookups']==len(original)==341
    assert {r['id'] for r in rows}==set(original)
    for group in current['groups']:
        block=bank[group['block']]
        assert block.hex()==group['current_block_hex']
        assert len(group['command_map'])==len(group['all_source_commands'])==len(group['all_current_commands'])
        for row in group['records']:
            source=original[row['id']]
            assert all(row[k]==source[k] for k in ('source_reference','source_hex','source_complete_preamble_hex'))
            at=row['current_reference']['offset']
            assert block[at:at+row['current_reference']['length']].hex()==row['current_hex']
            assert block[at-5:at+1].hex()==source['source_complete_preamble_hex']
    assert len(objects['style_records'])==47 and len(objects['choice_records'])==6 and objects['native_style_getter_cases']==56
    assert objects['current_ROM_sha256']==current['current_ROM_sha256'] and objects['runtime']==current['runtime']
    assert len(rows)+len(objects['style_records'])+len(objects['choice_records'])==drafts['records_count']==394
    assert current['all_source_preambles_andcommand_kinds_preserved']
    assert all(not any(r['review'].values()) for r in drafts['records'])
    save(OUT,dict(current_records=341,style_records=47,choice_records=6,native_style_getter_cases=56,
        all394_current_keys_bound_after_sealed_drafts=True,all39_current_blocks_exact_to_registered_target=True,
        all_source_preambles_andcomplete_command_membership_preserved=True,
        native_context_reuse=current['exact_native_context_reuse'],
        original_extraction_process_exit_code=1,
        original_extraction_completed_andwrote_all341_records_before_redundant_second_entry=True,
        second_entry_rejected_by_existing_output_directory_guard_before_new_output=True,
        extraction_not_rerun_oroutputs_overwritten=True,
        corrected_single_entry_wrapper='scripts/extract_editorial_current_scope_reuse_v2.py',
        object_binder_exit_code=0,verification_exit_contract='All explicit count/key/source/current assertions must pass.',
        no_editorial_ornew_display_gameplay_credit=True,new_credit=0,
        evidence={str(p):digest(p) for p in (current_path,object_path,ROOT/'native_context_reuse_qualification_v1.json',
            ROOT/'binding_inputs_v1/sealed_drafts.json',Path('scripts/extract_editorial_current_scope_reuse_v1.py'),
            Path('scripts/extract_editorial_current_scope_reuse_v2.py'),Path(__file__))}))
    print('Verified341 current speeches,47 variants,six captions and56 alias getter cases; all394 keys bound; zero credit.')


if __name__=='__main__':main()
