"""Bind the two directly viewed offline sheets without changing initial proofs."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

if __name__=='__main__':
    entries=[
        ('work/analysis/Hodram_B87_menu_20261101/menu_provider_and_planes.json',
            'Both complete choices are legible. The refusal says the player lacks the requested sum, not all money. Wider native geometry is in bounds; leading I and final period survive. Actual highlight/controller still pending.'),
        ('work/analysis/Emilio_name_glyph_native_20261101/native_name_glyph_verification.json',
            'The initial wide F differs visibly; proposed Emilio Ferog uses consistent ASCII glyphs, complete E and final g, with no clipping or overlap. This is a native preview from ordinary constructor fixtures, not a gameplay header.'),
    ]
    for filename,note in entries:
        path=Path(filename);report=load(path);sheet=report['review_sheet']
        assert sha(Path(sheet['path']).read_bytes())==sheet['sha256'] and report['direct_view_pending']
        out=path.with_name(path.stem+'_reviewed.json');assert not out.exists()
        report.update(direct_view_pending=False,offline_visual_approved=True,direct_view_note=note,
            initial_proof=str(path),initial_proof_sha256=sha(path.read_bytes()),reviewed_source_producer_sha256=sha(Path(__file__).read_bytes()))
        save(out,report)
    print('Two offline native sheets reviewed. Initial proofs preserved; actual/stored/release gates remain open.')
