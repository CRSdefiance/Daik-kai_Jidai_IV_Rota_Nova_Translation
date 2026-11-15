"""Verify both live menus on the fixture carrying the independently tested surnames."""
from pathlib import Path

from scripts.analyze_rafael_B201_B220_menu_actual_v1 import PARENT, source as previous
from scripts.prepare_rafael_B261_B280_actual_v1 import NAME_PROOF, PROPOSAL
from scripts.qualify_rafael_plett_relocation_v1 import plan_surnames
from scripts.source_locked_derivation_v5118 import checked_text


source = checked_text(previous, {
    "        for resource in ['/__arm9__.bin','/COMMON/MESFILE.DK4','/GRP/KANJI.FNT']:assert image.read_file(resource)==original.read_file(resource)":
        """        for resource in ['/COMMON/MESFILE.DK4','/GRP/KANJI.FNT']:
            assert image.read_file(resource)==original.read_file(resource)
        assert fixture['proposed_surname_fields_applied'] and fixture['surname_proof_sha256']==sha(NAME_PROOF.read_bytes())
        name_proof=load(NAME_PROOF)
        assert name_proof['proposal_sha256']==sha(PROPOSAL.read_bytes())
        arm,_=plan_surnames(original.read_file('/__arm9__.bin'),load(PROPOSAL),NdsImage.open('work/clean.nds').read_file('/__arm9__.bin'))
        assert sha(arm)==name_proof['versions'][1]['ARM9_sha256'] and image.read_file('/__arm9__.bin')==arm""",
})

if __name__ == '__main__':
    exec(compile(source, __file__ + '::live-menus-with-verified-surname-fields', 'exec'), globals())
