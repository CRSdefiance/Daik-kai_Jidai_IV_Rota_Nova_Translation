"""Hydrate exact already-verified native/reference inputs; do not replay producers."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.hodram_B31_B53_profile_v1 import contract,validate_approved_batch,validate_runtime
from dk4tool.dialogue.hodram_B31_B53_names_v1 import validate_scoped_names
from scripts.review_Hodram_B31_B53_actual_v8744 import PROOFS
from scripts.verify_village_wrap_v608 import read

DOC=Path('translations/hodram_B31_B53_editorial_manuscript_v5.json')
NAMES=Path('translations/hodram_B31_B53_speaker_name_review_v3.json')
NATIVE=Path('work/analysis/Hodram_B31_B53_native_validation_v8754/independent_native_validation.json')
REFERENCES=Path('work/analysis/Hodram_B31_B53_reference_validation_v8756/independent_reference_validation.json')
ACTUAL=Path('work/analysis/Hodram_B31_B53_actual_review_v8744/qualified_actual_review.json')

def verified_inputs():
    doc,names=map(read,[DOC,NAMES]);frozen=contract();validate_approved_batch(doc);validate_scoped_names(names)
    data={k:read(p) for k,p in PROOFS.items()};data.update(manuscript=doc,names=names,actual_review=read(ACTUAL))
    for path in [NATIVE,REFERENCES]:
        proof=read(path);assert proof['manuscript_sha256']==sha(DOC.read_bytes())
        for p,h in proof['evidence'].items():assert sha(Path(p).read_bytes())==h,p
    assert read(NATIVE)['six_complete_source_andstored_native_pages_two_current_progressive_names_andall_independent_pixels_exact']
    assert read(REFERENCES)['positive_entire_archive_whole_reference_ROM_all323_unownedblocks_files_components_andallinverses']
    parent,clean,reference=[NdsImage.open(p) for p in [doc['current_ROM'],'work/clean.nds',doc['reference_ROM']]];validate_runtime(parent)
    native=dict(bodies={},names={})
    for version,models in data['models']['native_models'].items():
        native['bodies'][version]={}
        for m in models:
            binding=frozen['record_bindings'][m['id']];key='compiler_source_hex' if version=='clean_Japanese' else 'stored_hex'
            assert m['input_hex']==binding[key] and m['expanded_native_hex']==m['input_hex'][2:]
            pages=[]
            for p in m['pages']:
                plane=Path(p['native_plane']).read_bytes();assert sha(plane)==p['native_plane_sha256'] and len(plane)==216*64
                pages.append(dict(deepcopy(p),native_plane_bytes=plane))
            native['bodies'][version][m['id']]=dict(expanded_body=bytes.fromhex(m['expanded_native_hex']),source_selector=m['source_selector'],complete_consumed_bytes=m['complete_consumed_bytes'],pages=pages)
    for n in data['models']['name_planes']:
        plane=Path(n['native_plane']).read_bytes();assert sha(plane)==n['native_plane_sha256'] and len(plane)==216*64
        native['names'][n['actor_ID']]=dict(actor_ID=n['actor_ID'],text=n['text'],plane=plane,events=deepcopy(n['native_glyph_events']),width=n['original_pair_flush_width'])
    assert set(native['names'])=={34,113}
    bank=IlnkContainer.parse(reference.read_file('/data/SC1.DK4')).blocks
    groups=[dict(g,target_block=Path(g['target_block']).read_bytes()) for g in data['relocation']['groups']]
    for g in groups:assert g['target_block']==bank[g['block']] and sha(g['target_block'])==g['target_block_sha256']
    rebuilt=dict(target_archive=reference.read_file('/data/SC1.DK4'),target_blocks={g['block']:g['target_block'] for g in groups},groups=groups)
    protected={Path(p) for p in frozen['dependencies']}|{DOC,NAMES,NATIVE,REFERENCES,ACTUAL,Path(__file__),Path('translations/release_stack.json'),Path('translations/editorial_review_current_v1.json'),Path('translations/rom_retention_pins.json'),Path(doc['current_ROM']),Path(doc['reference_ROM']),Path('work/clean.nds')}
    return doc,data,frozen,parent,clean,reference,rebuilt,native,protected
