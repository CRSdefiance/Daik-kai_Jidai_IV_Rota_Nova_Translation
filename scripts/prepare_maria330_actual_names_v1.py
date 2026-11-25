"""Bind the already-reviewed startup fallback156 for actual style-header comparisons."""
from copy import deepcopy
from pathlib import Path
import inspect
from dk4tool.rom.nds import NdsImage
from scripts.meaning_maria330_clean_v1 import ROOT
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.write_rafael_B169_contextual_v1 import fields,getter
from scripts.source_locked_derivation_v5118 import checked_text

def main():
    out=ROOT/'actual_name_inputs_v1';assert not out.exists()
    boundpath=ROOT/'name_inputs_v2/bindings.json';planespath=ROOT/'name_planes_v2/native_name_planes.json'
    priorbound=Path('work/Maria_B73_B95_clean_20261109/scoped_names_macros_reference_v1.json')
    priorreview=Path('translations/maria_B73_B95_scoped_names_final_v1.json')
    priorplanes=Path('work/Maria_B73_B95_clean_20261109/name_planes_v1/native_name_planes.json')
    approvalpath=Path('work/Maria_B73_B95_clean_20261109/offline_display_approval_v1.json')
    bound,planes,old,review,oldplanes,approval=map(load,[boundpath,planespath,priorbound,priorreview,priorplanes,approvalpath])
    runtime=bound['runtime'];ctx=RegisteredRuntime(runtime['release_proof'],runtime['startup_proof'],captain=3);assert ctx.receipt()==runtime
    original=next(r for r in old['records'] if r['actor_ID']==156);approved=next(r for r in review['records'] if r['actor_ID']==156)
    assert all(approved['review'].values()) and approval['all_names_and15_captions_directly_viewed']
    assert approval['evidence'][str(priorplanes)]==digest(priorplanes)
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin');assert fields(156,clean,ctx)==original['source_andcurrent_fields']
    previous=NdsImage.open(oldplanes['runtime']['candidate'])
    assert previous.read_file('/__arm9__.bin')==ctx.arm and previous.read_file('/GRP/KANJI.FNT')==ctx.image.read_file('/GRP/KANJI.FNT')
    adapter=checked_text(inspect.getsource(getter),{'for ident in [2,4,13,23,109]:':'for ident in [156]:'})
    scope={**getter.__globals__};exec(compile(adapter,__file__+'::same-original-two-name-getters-fallback156','exec'),scope)
    fresh=ctx.execute(scope['names']);assert len(fresh['rows'])==2
    assert fresh['rows']==original['current_consumers']
    assert {r['consumer']:r['text'] for r in fresh['rows']}==approved['approved_forms']=={'progressive-nameplate':'Sailor','full-catalogue':'Retainer'}
    row=deepcopy(original);row.update(current_consumers=fresh['rows'],previous_five_gate_review=str(priorreview),previous_five_gate_review_sha256=digest(priorreview),
        current_startup_fallback_only_not_a_conditional_story_assignment=True,no_new_name_localization_orcompletion_credit=True)
    extended=deepcopy(bound);extended['records'].append(row)
    assert len(extended['records'])==27 and len({r['actor_ID'] for r in extended['records']})==27
    extended['additional_current_fallback_reference_only']=156
    extended['evidence'].update({str(p):digest(p) for p in [boundpath,priorbound,priorreview,priorplanes,approvalpath,Path(__file__)]})
    out.mkdir();bindings=out/'header_bindings.json';save(bindings,extended)
    extendedplanes=deepcopy(planes)
    for text in ['Sailor','Retainer']:
        assert not any(r['text']==text for r in planes['planes'])
        p=deepcopy(next(r for r in oldplanes['planes'] if r['text']==text))
        assert p['complete_first_internal_final_codes_bounds_andindependent_font_pixels_pass']
        assert digest(p['native_plane'])==p['native_plane_sha256'] and digest(p['preview'])==p['preview_sha256']
        p['exact_prior_fallback_plane_reuse']=dict(path=str(priorplanes),sha256=digest(priorplanes),visual_approval=str(approvalpath),visual_approval_sha256=digest(approvalpath),
            complete_ARM9_font_text_andcurrent_name_fields_exact=True)
        extendedplanes['planes'].append(p)
    extendedplanes['consumer_bindings'].extend(dict(actor_ID=156,consumer=r['consumer'],text=r['text'],text_hex=r['text_hex']) for r in fresh['rows'])
    extendedplanes.update(actors=27,distinct_current_strings=31,additional_fallback156_strings_reused=2,
        no_additional_source_name_editorial_credit=True,actual_header_bindings=str(bindings),actual_header_bindings_sha256=digest(bindings))
    extendedplanes['evidence'].update({str(p):digest(p) for p in [bindings,priorplanes,approvalpath,Path(__file__)]})
    save(out/'native_name_planes.json',extendedplanes)
    print('Bound actual startup fallback156 through two original getters and two exact prior name planes;26 new scoped name retentions unchanged.')

if __name__=='__main__':main()
