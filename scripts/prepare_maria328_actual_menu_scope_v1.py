"""Select exact native proofs for only the two menus requested by the actual fixture."""
from copy import deepcopy
from scripts.meaning_maria328_clean_v1 import ROOT
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

def main():
    out=ROOT/'actual_analysis_inputs_v1';assert not out.exists()
    fixturepath=ROOT/'display_fixture_v1/Maria328_FE_menus_styles_pagination_fixture.json'
    nativepath=ROOT/'menu_native_v1/menu_provider_and_planes.json'
    fixture,native=map(load,[fixturepath,nativepath])
    keys={(m['block'],m['source_command_offset']) for m in fixture['menus']};assert keys=={(87,816),(92,372)}
    docpath=native['manuscript'];doc=load(docpath);assert digest(docpath)==native['manuscript_sha256']
    captions=[r for r in doc['records'] if r['kind']=='typed-choice-label' and (r['block'],r['source_command_offset']) in keys]
    assert len(captions)==6
    scoped=deepcopy(doc);scoped.update(records=captions,blocks=[87,92],source_objects=6,complete_exchanges=0,
        physical_speech_objects=0,ordinary_speech_objects=0,style_physical_speech_objects=0,style_command_objects=0,
        typed_choice_objects=6,typed_choice_commands=2,metadata_only_exact_caption_subset=True,
        complete_parent_manuscript=docpath,complete_parent_manuscript_sha256=digest(docpath),new_credit=0)
    out.mkdir();manuscript=out/'menus_manuscript.json';save(manuscript,scoped)
    proof=deepcopy(native)
    proof.update(manuscript=str(manuscript),manuscript_sha256=digest(manuscript),
        menus=[m for m in native['menus'] if (m['block'],m['source_command_offset']) in keys],
        records=[r for r in native['records'] if (r['block'],r['command_offset']) in keys],
        compiler_negatives_rejected=[r for r in native['compiler_negatives_rejected'] if (r['block'],r['source_command_offset']) in keys],
        native_provider_alignments=12,bridged_modal_returns=48,complete_English_caption_style_planes=24,review_sheets=[],
        unchanged_native_proofs_selected_without_replay=True,complete_native_parent_receipt=str(nativepath),
        complete_native_parent_receipt_sha256=digest(nativepath),actual_menu_pixels_still_pending=True,new_credit=0,
        evidence={str(p):digest(p) for p in [fixturepath,nativepath,manuscript,__file__]})
    assert len(proof['records'])==24 and sum(len(r['rejected']) for r in proof['compiler_negatives_rejected'])==16
    save(out/'two_menu_proofs.json',proof)
    print('Prepared exact two-menu/six-caption native proof scope for actual pixels; no new native, visual or gameplay approval.')

if __name__=='__main__':main()
