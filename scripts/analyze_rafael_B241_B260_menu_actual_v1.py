"""Match live choices while allowing only the proven Francisca field change."""
from dk4tool.patch.owned_name_fields_v2 import plan_arm9_name_fields
from scripts.analyze_rafael_B201_B220_menu_actual_v1 import PARENT, source as previous
from scripts.prepare_rafael_B241_B260_actual_v1 import FRANCISCA, PROPOSAL
from scripts.source_locked_derivation_v5118 import checked_text


source = checked_text(previous, {
    "        for resource in ['/__arm9__.bin','/COMMON/MESFILE.DK4','/GRP/KANJI.FNT']:assert image.read_file(resource)==original.read_file(resource)":
        """        for resource in ['/COMMON/MESFILE.DK4','/GRP/KANJI.FNT']:
            assert image.read_file(resource)==original.read_file(resource)
        arm=original.read_file('/__arm9__.bin')
        if fixture.get('verified_Francisca_field_applied'):
            name_proof=load(FRANCISCA)
            assert sha(FRANCISCA.read_bytes())==fixture['Francisca_name_proof_sha256']
            assert sha(PROPOSAL.read_bytes())==name_proof['proposal_sha256']
            clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
            arm, owned=plan_arm9_name_fields(arm,load(PROPOSAL),clean)
            assert owned==name_proof['name_data_plan']
        assert image.read_file('/__arm9__.bin')==arm""",
})

if __name__ == '__main__':
    exec(compile(source, __file__+'::complete-live-menu-and-exclusive-field-proof', 'exec'), globals())
