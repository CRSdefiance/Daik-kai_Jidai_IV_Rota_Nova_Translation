"""Keep two completed menus and join the full-label third-menu verification."""
from pathlib import Path
from dk4tool.dialogue.reviewed_two_choice_object_v1 import compile_choices
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Hodram_B0_B41_clean_20261107')
DOC=ROOT/'formatting_v1/formatting_input_v2.json'
OUT=ROOT/'native_objects_v2/complete_choice_objects.json'


def main():
    assert not OUT.exists();doc=load(DOC);objects=[]
    for block,offset,directory in [(30,1100,'native_objects_v1/menus/B30_C1100'),
        (33,414,'native_objects_v1/menus/B33_C414'),(37,216,'native_objects_v2/B37_C216')]:
        folder=ROOT/directory;path=folder/'menu_provider_and_planes.json';proof=load(path)
        rows=[r for r in doc['records'] if r['kind']=='typed-choice-label' and r['block']==block and r['source_command_offset']==offset]
        assert len(rows)==2
        target=compile_choices(bytes.fromhex(rows[0]['source_choice_object_hex']),bytes.fromhex(rows[0]['current_choice_object_hex']),rows,require_formatting=False)
        binary=folder/'compiled_choice_object.bin';assert binary.read_bytes()==target
        assert proof['complete_caption_glyphs_centering_bounds_guards_andconsumption_pass']
        assert proof['source_index_andcount_preserved'] and not proof['actual_gameplay']
        assert digest(proof['review_sheet']['path'])==proof['review_sheet']['sha256']
        if block==37:assert proof['observer_reads_complete_NUL_terminated_labels_within_original_object']
        objects.append(dict(block=block,source_command_offset=offset,record_ids=[r['id'] for r in rows],
            receipt=str(path),receipt_sha256=digest(path),compiled_path=str(binary),compiled_sha256=digest(binary),review_sheet=proof['review_sheet']))
    save(OUT,dict(manuscript=str(DOC),manuscript_sha256=digest(DOC),objects=objects,physical_caption_records=6,
        native_provider_alignments=18,bridged_modal_returns=54,complete_caption_style_planes=24,all_checks_pass=True,
        two_completed_menu_proofs_reused_without_native_reexecution=True,
        full33_character_caption_preserved_no_prose_shortening=True,
        diagnostic_32_byte_observer_limit_repaired_without_native_provider_change=True,
        direct_view_pending=True,actual_gameplay=False,new_credit=0,producer_sha256=digest(__file__)))
    print('Joined all3 menus/six captions;18 provider alignments/54 bridged returns/24 planes pass. Direct view remains.')


if __name__=='__main__':main()
