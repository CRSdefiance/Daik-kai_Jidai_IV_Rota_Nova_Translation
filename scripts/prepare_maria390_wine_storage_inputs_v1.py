"""Project the changed block for fresh checks; leave the other23 exact stored groups intact."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Maria_B152_B175_clean_20261109')


def main():
    out=ROOT/'stored_wine_inputs_v1';assert not out.exists()
    rebuiltpath=ROOT/'reconstruction_v3/reconstruction.json';rebuilt=load(rebuiltpath)
    nativepath=Path(rebuilt['native']);native=load(nativepath)
    oldpath=ROOT/'reconstruction_v2/reconstruction.json';old=load(oldpath)
    assert rebuilt['previous_wine_reconstruction_sha256']==digest(oldpath)
    assert all(a==b for a,b in zip(old['groups'],rebuilt['groups'],strict=True) if a['block']!=152)
    group=next(g for g in rebuilt['groups'] if g['block']==152)
    rows=[r for r in native['records'] if r['block']==152]
    assert len(rows)==len(group['text_records'])==14 and not group['native_objects']
    selected=deepcopy(native)
    selected.update(records=rows,pages=14,selected_alignment_cases=56,
        full_native_proof=str(nativepath),full_native_proof_sha256=digest(nativepath),
        subset_only_changed_storage_block_not_full_batch=True,new_credit=0)
    out.mkdir();partialnative=out/'native.json';save(partialnative,selected)
    partial=deepcopy(rebuilt)
    partial.update(groups=[group],reviewed_blocks=[152],changed_blocks=[152],source_editorial_objects=14,source_speeches=14,
        speech_count=14,total_rendered_speech_count=14,typed_choice_count=0,compound_objects=0,style_physical_speech_count=0,
        relative_sites=len(group['relative_fixups']),command_count=len(group['all_target_commands']),
        native=str(partialnative),native_sha256=digest(partialnative),
        full_reconstruction=str(rebuiltpath),full_reconstruction_sha256=digest(rebuiltpath),
        subset_only_changed_storage_block_not_full_batch=True,new_credit=0)
    save(out/'reconstruction.json',partial)
    print('Projected14 B152 bodies andtheir branch sites for fresh stored checks;other23 exact groups excluded from replay.')


if __name__=='__main__':main()
