"""Bind the invitation/meeting source identities andcomplete explicit B137 prerequisite context."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Hodram_source_context_tools_v8180')
if __name__=='__main__':
    assert not ROOT.exists()
    context=derive('scripts/inventory_Hodram_B46_clean_v8179.py','scripts/inventory_Hodram_B137_clean_v8180.py',{
        'Hodram_B46_clean_context_v8179':'Hodram_B137_clean_context_v8180','for number in [46]':'for number in [137]',
        'complete_clean_SC1_B46_EV1_andcoverage_before_current_English.json':'complete_clean_SC1_B137_EV1_andcoverage_before_current_English.json',
        "g['block']==46":"g['block']==137",'Hodram B46':'Hodram B137',
    })
    names=derive('scripts/read_Rafael_B50_clean_names_v8130.py','scripts/read_Hodram_B45_B46_clean_names_v8180.py',{
        'Rafael_B50_clean_names_v8130':'Hodram_B45_B46_clean_names_v8180',
        'Rafael_next_clean_v8129/complete_clean_SC0_B50_EV0_andcoverage_before_current_English.json':'Hodram_B46_clean_context_v8179/complete_clean_SC1_B46_EV1_andcoverage_before_current_English.json',
        "source=read(SOURCE);g=source['groups'][0];image=NdsImage.open(source['source_ROM']);arm=image.read_file('/__arm9__.bin')":
        "source=read(SOURCE);invitation=Path('work/analysis/Hodram_next_clean_v8178/complete_clean_SC1_B45_EV1_andcoverage_before_current_English.json');other=read(invitation);assert source['source_ROM_sha256']==other['source_ROM_sha256'];g=dict(records=other['groups'][0]['records']+source['groups'][0]['records']);image=NdsImage.open(source['source_ROM']);arm=image.read_file('/__arm9__.bin')",
        'chosen==[0,2,9]':'chosen==[1,2,113]',
        'source_packet=str(SOURCE),source_packet_sha256=sha(SOURCE.read_bytes()),':'source_packet=str(SOURCE),source_packet_sha256=sha(SOURCE.read_bytes()),source_invitation_packet=str(invitation),source_invitation_packet_sha256=sha(invitation.read_bytes()),',
        'B50 actors':'Hodram B45/B46 actors',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivations.json',[context,names])
    print('Prepared complete B137 prerequisite source andthree combined clean identities;no currentEnglish orcredit.')
