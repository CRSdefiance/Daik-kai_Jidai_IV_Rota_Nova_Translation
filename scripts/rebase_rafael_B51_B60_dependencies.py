"""Qualify exact reuse on the verified seven-stage successor and rebase Fernan's field."""
import struct
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE
from dk4tool.patch.owned_name_fields_v2 import plan_arm9_name_fields
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load,save
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.generic_name_macro_owned_v5886b import expand as original_expand

ROOT=Path('work/analysis/Rafael_B51_B60_current_runtime_20261104')
SOURCE=Path('work/analysis/Rafael_early_story_B36_B41_B51_B60_clean_20261104')
DISPLAY=Path('work/analysis/Rafael_B51_B60_formatting_20261104')
OLD_RELEASE=Path('work/analysis/Rafael_B36_B41_release_verified_20261104/registered_release_verification.json')
RELEASE=Path('work/analysis/Shared_tutorial_name_data_release_verified_20261104/registered_release_verification.json')
FIELD=Path('work/analysis/Rafael_Fernan_name_field_20261104/owned_fields_proposal.json')
NATIVE=Path('work/analysis/Rafael_Fernan_name_native_20261104/native_name_fields_verification.json')
MACROS=Path('work/analysis/Rafael_early_tutorial_B42_B43_source_display_20261104/40_native_selectors_macros_andcomplete_preamble_bindings.json')


def cstring(raw,pointer):
    if not pointer:return b''
    start=pointer-BASE;assert 0<=start<len(raw)
    return raw[start:raw.index(0,start)]


if __name__=='__main__':
    assert not ROOT.exists()
    old=RegisteredRuntime(OLD_RELEASE,OLD_RELEASE.with_name('own_registered_startup_verification.json'),captain=0)
    ctx=RegisteredRuntime(RELEASE,RELEASE.with_name('own_registered_startup_verification.json'),captain=0)
    release=load(RELEASE);assert release['parent_sha256']==old.release['candidate_sha256']
    assert all(ctx.image.read_file(p)==v for _,p,v in old.image.iter_files())
    assert [p for p,v in old.image.iter_components() if ctx.image.read_file(p)!=v]==['/__arm9__.bin']
    assert ctx.actor_root==old.actor_root and ctx.actor_bytes==old.actor_bytes and ctx.common==old.common
    assert ctx.image.read_file('/GRP/KANJI.FNT')==old.image.read_file('/GRP/KANJI.FNT')
    inverse=bytearray(ctx.arm);spans=release['owned_text_data_proof']['changed_records']
    assert len(spans)==6
    for r in spans:
        at,n=r['physical_offset'],r['owned_bytes'];assert ctx.arm[at:at+n].hex()==r['new_hex'] and old.arm[at:at+n].hex()==r['old_hex']
        inverse[at:at+n]=bytes.fromhex(r['old_hex'])
    assert bytes(inverse)==old.arm
    identity_path=SOURCE/'B51_B60_source_identity_checkpoint_v1.json';identity=load(identity_path)
    assert identity['runtime']==old.receipt() and not set(identity['actors'])&{31,34}
    table=struct.unpack_from('<I',ctx.arm,0xCDAC0)[0]-BASE
    fields=[]
    for actor in [*identity['actors'],40]:
        at=table+32*actor;assert ctx.arm[at:at+32]==old.arm[at:at+32]
        for col in [0,4,8]:
            ptr=struct.unpack_from('<I',ctx.arm,at+col)[0];value=cstring(ctx.raw,ptr)
            assert value==cstring(old.raw,ptr)
            fields.append(dict(actor_ID=actor,column=col,pointer=ptr,text_hex=value.hex()))
    macros=load(MACROS)
    assert macros['runtime']['ARM9_sha256']==sha(old.arm) and macros['runtime']['COMMON_sha256']==sha(ctx.common)
    env=dict(original_expand.__globals__)
    exec(compile(macros['source_owned_progressive_adapter'],__file__+'::same-captain0-macro-ABI-on-own-successor','exec'),env)
    default=ctx.execute(env['expand'],b'FI FA FO',0)
    assert len(default['cases'])==4 and all(r['output_hex']==b'Rafael Castor Castor Co.'.hex() for r in default['cases'])
    proposal,native=map(load,[FIELD,NATIVE]);assert proposal['runtime']==old.receipt() and native['proposal_sha256']==sha(FIELD.read_bytes())
    rebased=deepcopy(proposal);rebased['runtime']=ctx.receipt()
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    arm,plan=plan_arm9_name_fields(ctx.arm,rebased,clean)
    prior_plan=native['name_data_plan']
    assert {k:v for k,v in plan.items() if k not in ['parent_ARM9_sha256','target_ARM9_sha256']}=={
        k:v for k,v in prior_plan.items() if k not in ['parent_ARM9_sha256','target_ARM9_sha256']}
    composed=bytearray(Path(native['proposed_ARM9']).read_bytes())
    for r in spans:
        at,n=r['physical_offset'],r['owned_bytes']
        assert all(at+n<=f['physical_offset'] or at>=f['physical_offset']+f['owned_bytes'] for f in proposal['fields'])
        composed[at:at+n]=bytes.fromhex(r['new_hex'])
    assert bytes(composed)==arm
    ROOT.mkdir();qual=ROOT/'dependency_qualification.json'
    save(qual,dict(runtime=ctx.receipt(),previous_runtime=old.receipt(),source_owned_parent_inverse=release['owned_text_data_proof'],
        all_SC0_COMMON_font_unowned_components_andcomplete_actor_models_exact=True,
        all18_speakers_andreferenced_actor40_name_inputs_exact=fields,
        own_captain0_default_macro_alignments=default,complete_code_unchanged_except_six_typed_text_data_spans=True,
        previously_rendered253_body_pages_andfour_captions_qualify_for_exact_reuse=True,
        Fernan_fixed_field_commutes_with_all_six_registered_data_spans=True,
        Fernan_native_name_getters_planes_andnegative_cases_reused_not_reexecuted=True,
        no_new_story_orcatalogue_gameplay_claim=True,new_credit=0,
        dependencies={str(p):sha(p.read_bytes()) for p in [OLD_RELEASE,RELEASE,identity_path,FIELD,NATIVE,MACROS,Path(__file__)]}))
    rebased.update(previous_proposal=str(FIELD),previous_proposal_sha256=sha(FIELD.read_bytes()),
        latest_runtime_dependency_qualification=str(qual),latest_runtime_dependency_qualification_sha256=sha(qual.read_bytes()))
    save(ROOT/'Fernan_owned_fields_proposal.json',rebased);save(ROOT/'Fernan_owned_fields_plan.json',plan)
    (ROOT/'Fernan_proposed_ARM9_RESEARCH_ONLY.bin').write_bytes(arm)
    packet_path=Path('work/analysis/Rafael_B51_B60_current_20261104/current_effective.json');packet=deepcopy(load(packet_path))
    assert packet['runtime']==old.receipt() and packet['current_archive_sha256']==sha(ctx.image.read_file('/data/SC0.DK4'))
    packet.update(current_ROM=str(ctx.rompath),current_ROM_sha256=ctx.release['candidate_sha256'],runtime=ctx.receipt(),
        source_current_binding=str(packet_path),source_current_binding_sha256=sha(packet_path.read_bytes()),exact_dependency_reuse=str(qual))
    save(ROOT/'current_effective.json',packet)
    manuscript_path=DISPLAY/'formatting_input.json';doc=deepcopy(load(manuscript_path))
    doc.update(current_ROM=str(ctx.rompath),current_ROM_sha256=ctx.release['candidate_sha256'],
        source_full_manuscript=str(manuscript_path),source_full_manuscript_sha256=sha(manuscript_path.read_bytes()),
        current_dependency_qualification=str(qual),current_dependency_qualification_sha256=sha(qual.read_bytes()))
    rebased_doc=ROOT/'formatting_input.json';save(rebased_doc,doc)
    plan_path=DISPLAY/'automatic_v4/automatic_plans.json';native_path=DISPLAY/'combined_native_v4.json'
    plans,pages=map(load,[plan_path,native_path])
    assert pages['runtime']==old.receipt() and plans['manuscript_sha256']==pages['manuscript_sha256']==sha(manuscript_path.read_bytes())
    plans.update(manuscript=str(rebased_doc),manuscript_sha256=sha(rebased_doc.read_bytes()),
        previous_plan=str(plan_path),previous_plan_sha256=sha(plan_path.read_bytes()),exact_dependency_reuse=str(qual))
    plan_out=ROOT/'compatible_plans.json';save(plan_out,plans)
    pages.update(runtime=ctx.receipt(),manuscript=str(rebased_doc),manuscript_sha256=sha(rebased_doc.read_bytes()),
        plan=str(plan_out),plan_sha256=sha(plan_out.read_bytes()),previous_native=str(native_path),previous_native_sha256=sha(native_path.read_bytes()),
        exact_dependency_reuse=str(qual),exact_dependency_reuse_sha256=sha(qual.read_bytes()),no_new_page_rendering_claim=True)
    save(ROOT/'compatible_native_pages.json',pages)
    save(ROOT/'rebase_checkpoint.json',dict(runtime=ctx.receipt(),all249_record_rows_andEnglish_unchanged=True,
        body_pages_reused=253,caption_records_reused=4,own_default_macro_cases=4,source_qualified_Fernan_name_field_rebased=True,
        proposed_ARM9_sha256=sha(arm),stored_native_headers_representative_gameplay_andrelease_pending=True,new_credit=0))
    print('Qualified4b10fd67:253 pages/4 captions reused;4 own macro cases;Fernan field rebased by exact disjoint inverse.')
