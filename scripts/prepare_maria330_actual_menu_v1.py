"""Select the exact two captions for actual menu pixels without rerunning provider proofs."""
from copy import deepcopy
from scripts.meaning_maria330_clean_v1 import ROOT
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

def main():
    out=ROOT/'actual_menu_inputs_v1';assert not out.exists()
    path=ROOT/'menu_native_v1/menu_provider_and_planes.json';proof=load(path)
    parent=proof['manuscript'];doc=load(parent);assert digest(parent)==proof['manuscript_sha256']
    rows=[r for r in doc['records'] if r['kind']=='typed-choice-label'];assert len(rows)==2 and [r['source_index'] for r in rows]==[0,1]
    assert all(r['block']==102 and r['source_command_offset']==210 for r in rows)
    view=deepcopy(doc);view.update(records=rows,blocks=[102],physical_speech_objects=0,ordinary_speech_objects=0,style_physical_speech_objects=0,
        style_command_objects=0,typed_choice_objects=2,typed_choice_commands=1,metadata_only_exact_caption_subset=True,
        complete_parent_manuscript=parent,complete_parent_manuscript_sha256=digest(parent),new_credit=0)
    out.mkdir();manuscript=out/'captions.json';save(manuscript,view)
    projected=deepcopy(proof);projected.update(manuscript=str(manuscript),manuscript_sha256=digest(manuscript),
        complete_native_parent_receipt=str(path),complete_native_parent_receipt_sha256=digest(path),
        unchanged_native_proofs_selected_without_replay=True,actual_menu_pixels_still_pending=True)
    save(out/'native_menu_proof.json',projected);print('Selected both exact B102 captions and complete native proof for actual pixels; no provider checks repeated.')

if __name__=='__main__':main()
