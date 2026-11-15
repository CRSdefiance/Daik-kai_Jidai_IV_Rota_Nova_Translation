"""Add all clean B137 prerequisite speakers to the invitation/meeting identity packet."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Hodram_six_clean_names_tools_v8182')
if __name__=='__main__':
    assert not ROOT.exists()
    receipt=derive('scripts/read_Hodram_B45_B46_clean_names_v8180.py','scripts/read_Hodram_B137_B45_B46_clean_names_v8182.py',{
        'Hodram_B45_B46_clean_names_v8180':'Hodram_B137_B45_B46_clean_names_v8182',
        "g=dict(records=other['groups'][0]['records']+source['groups'][0]['records'])":"prerequisite=Path('work/analysis/Hodram_B137_clean_context_v8180/complete_clean_SC1_B137_EV1_andcoverage_before_current_English.json');extra=read(prerequisite);assert extra['source_ROM_sha256']==source['source_ROM_sha256'];g=dict(records=extra['groups'][0]['records']+other['groups'][0]['records']+source['groups'][0]['records'])",
        'chosen==[1,2,113]':'chosen==[1,2,9,16,18,113]',
        'three_clean_static_identity_fields_before_current_English.json':'six_clean_static_identity_fields_before_current_English.json',
        'source_invitation_packet_sha256=sha(invitation.read_bytes()),':'source_invitation_packet_sha256=sha(invitation.read_bytes()),source_prerequisite_packet=str(prerequisite),source_prerequisite_packet_sha256=sha(prerequisite.read_bytes()),',
        'Hodram B45/B46 actors':'Hodram B137/B45/B46 actors',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivation.json',receipt)
    print('Prepared six clean B137/B45/B46 speaker identities before currentEnglish.')
