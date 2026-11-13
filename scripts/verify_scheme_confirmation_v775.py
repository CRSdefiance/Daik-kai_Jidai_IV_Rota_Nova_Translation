"""Verify the default confirmation's final English against its same-table peer."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_machine_scoped_v764 import machine
from scripts.probe_tavern_continuation_layout_v768 import format_case
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/tavern_schemes_layout_v775_v3')
MANUSCRIPT=Path('translations/tavern_schemes_editorial_manuscript_v3.json')


def main():
    ROOT.mkdir(parents=True,exist_ok=True)
    previous=Path('translations/tavern_schemes_editorial_manuscript_v2.json')
    doc=read(previous)
    peer=next(r for r in doc['records'] if r['message_id']==947)
    row=next(r for r in doc['records'] if r['message_id']==940)
    row['english']="We'll lure a fleet from %s to %s. Is that correct?{PAD}"
    row['localization_note']+=' Final English pass: use a complete statement of the proposed action followed by a direct confirmation question. This suits both the neutral polite voice and the formal older voice947;source meaning does not require an invented difference between them.'
    assert row['english']==peer['english']
    assert row['source_native_arguments']==peer['source_native_arguments']==['faction','town']
    assert row['source_voice_table']==peer['source_voice_table']==0x021182A0
    doc['previous_draft']={'path':str(previous),'sha256':sha(previous.read_bytes())}
    doc['editorial_revision']='V775 complete default confirmation;identical wording for same-table polite947 is deliberate.'
    doc['producer_sha256']=sha(Path(__file__).read_bytes())
    save(MANUSCRIPT,doc)
    arm=NdsImage.open('out/all_routes_combined_v773_candidate.nds').read_file('/__arm9__.bin')
    old=read('work/analysis/tavern_schemes_layout_v775_v2/native_layout_matrix.json')
    expected=[r for r in old['cases'] if r['id']==947]
    updated=[]
    assert len(expected)==2394
    for i,case in enumerate(expected):
        if i%64==0:u=machine(arm)
        args=tuple(bytes.fromhex(s) for s in case['source_values_hex'])
        actual=format_case(u,row,args)
        actual['synthetic_23_byte_faction_boundary']=case['synthetic_23_byte_faction_boundary']
        assert actual=={**case,'id':940}
        updated.append(actual)
    # Retain the already executed V2 results for every unchanged record.
    cases=[r for r in old['cases'] if r['id']!=940]+updated
    cases.sort(key=lambda r:r['id'])
    findings=[r for r in cases if r['findings']]
    assert not any(not r['synthetic_23_byte_faction_boundary'] for r in findings)
    save(ROOT/'native_layout_matrix.json',{**old,'cases':cases,'findings_count':len(findings),
        'changed940_complete_native_reexecution_count':2394,
        'unchanged55_source_results':'work/analysis/tavern_schemes_layout_v775_v2/native_layout_matrix.json',
        'unchanged55_matrix_sha256':sha(Path('work/analysis/tavern_schemes_layout_v775_v2/native_layout_matrix.json').read_bytes())})
    save(ROOT/'layout_findings.json',findings)
    save(ROOT/'verification.json',{'manuscript':str(MANUSCRIPT),'manuscript_sha256':sha(MANUSCRIPT.read_bytes()),
        'complete_native_layouts':len(cases),'changed940_reexecuted_cases':2394,
        'real_catalog_cases':sum(not r['synthetic_23_byte_faction_boundary'] for r in cases),
        'real_catalog_findings':0,'remaining_synthetic23_byte_findings':len(findings),
        'all940_full_font_planes_identical_to_same_table947_planes_already_reviewed':True,
        'source_947_font_proof':'work/analysis/tavern_schemes_layout_v775_v2/verification.json',
        'formatting_approval_pending_until_name_input_bounds_resolved':True,
        'no_new_ROM_or_integration_or_gameplay_claim':True,'full_goal_complete':False,
        'producer_sha256':sha(Path(__file__).read_bytes())})
    print(f'{len(cases)} layouts;real catalog warnings0;{len(findings)} synthetic23-byte warnings remain. No integration approval.',flush=True)


if __name__=='__main__':main()
