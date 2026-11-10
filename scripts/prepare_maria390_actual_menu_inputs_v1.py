"""Expose existing exact menu receipts to the qualified actual-interval checker."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Maria_B152_B175_clean_20261109')


def main():
    parent=ROOT/'menu_native_approved_v2.json';source=load(parent)
    output=ROOT/'actual_menu_inputs_v1';assert not output.exists()
    assert source['offline_visual_approved'] and not source['direct_view_pending']
    projected=deepcopy(source)
    for row in projected['menus']:
        assert digest(row['proof'])==row['proof_sha256']
        proof=load(row['proof']);assert proof['runtime']==source['runtime']
        assert proof['complete_caption_glyphs_centering_bounds_guards_andconsumption_pass']
        row.update(native_receipt=row['proof'],native_receipt_sha256=row['proof_sha256'])
    projected.update(complete_native_parent_receipt=str(parent),complete_native_parent_receipt_sha256=digest(parent),
        exact_metadata_alias_only_no_provider_pixels_orobject_bytes_replayed=True,
        actual_menu_pixels_still_pending=True,new_credit=0)
    output.mkdir();save(output/'native_menus.json',projected)
    print('Prepared exact8-menu receipt aliases;native checks reused,actual selections unapproved.')


if __name__=='__main__':main()
