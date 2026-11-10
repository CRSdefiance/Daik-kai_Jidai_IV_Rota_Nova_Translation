"""Reuse calibrated paragraph formatting, adding only measured FU and exact source scope."""
import linecache
from pathlib import Path
from types import SimpleNamespace
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load
from scripts import plan_rafael_early_tutorial_B42_B43 as previous
from scripts.source_locked_derivation_v5118 import checked_text

PROOF=Path('work/analysis/Rafael_early_story_B36_B41_B51_B60_clean_20261104/B36_B41_source_identity_andFU_checkpoint_v1.json')
CURRENT=Path('work/analysis/Rafael_B36_B41_current_20261104/current_effective.json')


def display(text):
    for key,value in [('FI','Rafael'),('FA','Castor'),('FO','Castor Co.'),('FU','Rafael Castor')]:
        text=text.replace('{MACRO:'+key+'}',value)
    return text


def qualify_source(doc):
    assert doc['file_path']=='/data/SC0.DK4' and doc['blocks']==list(range(36,42))
    proof,current=map(load,[PROOF,CURRENT])
    assert proof['runtime']==current['runtime'] and proof['default_macro_lengths']==dict(FI=6,FA=6,FO=10,FU=13)
    assert proof['FU_expands_complete_full_name_not_first_name'] and proof['FU_fresh_alignment_cases']==8
    assert current['all_source_preambles_andcommand_kinds_preserved']
    originals={r['id']:r for g in current['groups'] for r in g['records']}
    clean_path=Path('work/clean.nds')
    assert sha(clean_path.read_bytes())=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    clean=IlnkContainer.parse(NdsImage.open(clean_path).read_file(doc['file_path'])).blocks
    image=NdsImage.open(doc['current_ROM'])
    assert sha(Path(doc['current_ROM']).read_bytes())==doc['current_ROM_sha256']==current['runtime']['candidate_sha256']
    assert sha(image.read_file('/__arm9__.bin'))==current['runtime']['ARM9_sha256']
    bank=IlnkContainer.parse(image.read_file(doc['file_path'])).blocks
    assert sha(image.read_file(doc['file_path']))==doc['current_archive_sha256']
    actors=set(proof['actors']);zeros=set();bindings=[]
    for row in doc['records']:
        original=originals[row['id']]
        assert all(row[k]==original[k] for k in ['source_reference','current_reference','source_hex','current_hex','source_complete_preamble_hex'])
        source_ref,current_ref=row['source_reference'],row['current_reference']
        raw,stored=bytes.fromhex(row['source_hex']),bytes.fromhex(row['current_hex'])
        head=bytes.fromhex(row['source_complete_preamble_hex'])
        assert len(head)==6 and head[:5]==bytes.fromhex('0040ffff00') and head[-1]==raw[0]==stored[0]==row['source_selector']
        assert raw[0] in actors and b'\0' not in raw[1:] and b'\0' not in stored[1:]
        assert clean[row['block']][source_ref['header_offset']:source_ref['offset']+len(raw)+1]==head[:5]+raw+b'\0'
        assert bank[row['block']][current_ref['header_offset']:current_ref['offset']+len(stored)+1]==head[:5]+stored+b'\0'
        if row['source_selector']==0:zeros.add(raw)
        bindings.append(dict(id=row['id'],source_reference=source_ref,current_reference=current_ref,complete_source_preamble_hex=head.hex(),
            source_body_sha256=sha(raw),selector00_owned_by_complete_preamble=row['source_selector']==0,
            static_actor_name_andvoice_characterization_reused=str(PROOF),static_actor_name_andvoice_characterization_reused_sha256=sha(PROOF.read_bytes()),
            no_new_per_record_dispatch_execution_claim=True))
    assert len(bindings)==175 and {r['id'] for r in bindings}==set(originals)
    return zeros,bindings


adapter=checked_text(previous.adapter,{
    "profile.macro_ascii_lengths=={'FI':6,'FA':6,'FO':10}":"profile.macro_ascii_lengths=={'FI':6,'FA':6,'FO':10,'FU':13}",
})
parameters={**previous.parameters,'ADAPTER':adapter,'ENV':{**previous.parameters['ENV'],'display':display},
    'PAIRS':previous.parameters['PAIRS']|{('barbarossa','hayreddin'),('algiers','pirates'),('spanish','armada'),('southern','mediterranean'),('north','african'),('full','speed'),('good','luck')}}
source=checked_text(previous.source,{
    "name='rafael-early-tutorial-measured-native-v1'":"name='rafael-B36-B41-measured-FU-v1'",
    "macro_widths={'FI':36,'FA':36,'FO':60,'I':12}":"macro_widths={'FI':36,'FA':36,'FO':60,'FU':78,'I':12}",
    "macro_ascii_lengths={'FI':6,'FA':6,'FO':10}":"macro_ascii_lengths={'FI':6,'FA':6,'FO':10,'FU':13}",
})
env={**previous.env,'previous':SimpleNamespace(**parameters),'qualify_source':qualify_source,'__file__':__file__}
filename=__file__+'::same-scoped-paragraph-planner-measured-native-FU'
linecache.cache[filename]=(len(source),None,source.splitlines(keepends=True),filename)
exec(compile(source,filename,'exec'),env)
main=env['main']
if __name__=='__main__':main()
