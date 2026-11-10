"""Reuse exact name planes across the registered nine-byte metadata-only stage."""
from pathlib import Path
from copy import deepcopy
from dk4tool.patch.owned_name_fields_v2 import plan_arm9_name_fields
from dk4tool.rom.nds import NdsImage
from scripts import check_rafael_B61_B80_scoped_name_planes as previous
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.review_hodram_B211_B230_names_v1 import NATIVE,OUT as REVIEW
from scripts.review_hodram_B221_B230_contextual_v1 import ROOT as BATCH
from scripts.source_locked_derivation_v5118 import checked_text

ROOT=BATCH/'name_planes_v1'
INPUTS=BATCH/'name_plane_inputs_v1'
PRIOR=Path('work/Rafael_B0_B34_clean_20261106/retained_name_planes_v2/native_name_planes.json')
RELEASE=Path('work/rafael5186_release_v1/registered_release_verification.json')
STARTUP=BATCH/'own_parent_startup_v3/own_route_context.json'

def main():
    assert not INPUTS.exists() and not ROOT.exists()
    review,native,prior,release=map(load,(REVIEW,NATIVE,PRIOR,RELEASE))
    image=NdsImage.open(release['candidate']);old=NdsImage.open(prior['runtime']['candidate'])
    assert digest(prior['runtime']['candidate'])==prior['runtime']['candidate_sha256']
    assert prior['runtime']['ARM9_sha256']==release['middle_fields_proof']['parent_ARM9_sha256']
    proposal=load('work/Rafael_B0_B34_clean_20261106/owned_middle_fields_v1/proposal.json')
    target,proof=plan_arm9_name_fields(old.read_file('/__arm9__.bin'),proposal,NdsImage.open('work/clean.nds').read_file('/__arm9__.bin'))
    assert target==image.read_file('/__arm9__.bin') and proof['changed_bytes']==9 and proof['complete_parent_inverse_exact']
    assert proof['all_unowned_ARM9_bytes_sections_pointer_tables_andallocations_exact']
    assert old.read_file('/GRP/KANJI.FNT')==image.read_file('/GRP/KANJI.FNT')
    rows=[]
    for original in review['records']:
        row=deepcopy(original)
        row.update(english=row['approved_forms']['progressive-nameplate'],
            source_reference=dict(actor_ID=row['actor_ID'],fields=row['clean_fields']),
            current_reference=dict(actor_ID=row['actor_ID'],fields=row['current_fields']))
        rows.append(row)
    INPUTS.mkdir()
    names=INPUTS/'names.json';identity=INPUTS/'identity.json'
    save(names,{**review,'records':rows})
    save(identity,dict(runtime=native['runtime'],name_bindings=review['records'],actors=[r['actor_ID'] for r in rows],
        unrelated_middle_field_inverse=proof,renderer_font_andinput_strings_compatible=True,new_credit=0))
    source=Path(previous.__file__).read_text(encoding='utf-8')
    source=source[source.index("if __name__=='__main__':"):]
    source=checked_text(source,{
        "ctx=RegisteredRuntime(RELEASE,RELEASE.with_name('own_registered_startup_verification.json'),captain=0)":
            "ctx=RegisteredRuntime(RELEASE,STARTUP,captain=1)",
        "assert qual['runtime']==ctx.receipt() and qual['previous_runtime']==bound['runtime']":
            "assert qual['runtime']==ctx.receipt()==bound['runtime'] and qual['renderer_font_andinput_strings_compatible']",
        "assert prior['proposed_ARM9_sha256']==sha(ctx.arm)":
            "assert prior['runtime']['ARM9_sha256']==qual['unrelated_middle_field_inverse']['parent_ARM9_sha256'] and sha(ctx.arm)==qual['unrelated_middle_field_inverse']['target_ARM9_sha256']",
        "len(doc['records'])==len(bound['name_bindings'])==22":"len(doc['records'])==len(bound['name_bindings'])==23",
        'complete_target_ARM9_font_native_style_andinput_string_identical=True':
            'native_renderer_font_andinput_string_identical_only_unrelated_owned_middle_fields_differ=True',
        'assert len(planes)==21 and fresh+reused==21':'assert len(planes)==22 and fresh+reused==22',
        'scoped_actors=22,distinct_strings=21':'scoped_actors=23,distinct_strings=22',
        "print(f'22actors/21strings:":"print(f'23actors/22strings:",
    })
    env={**vars(previous),'ROOT':ROOT,'NAMES':names,'BINDINGS':identity,'QUAL':identity,'PRIOR':PRIOR,
        'RELEASE':RELEASE,'STARTUP':STARTUP,'__file__':__file__,'__name__':'__main__'}
    exec(compile(source,__file__+'::same-style11-inverse-qualified-name-cache','exec'),env)

if __name__=='__main__':main()
