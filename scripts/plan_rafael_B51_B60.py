"""Use the calibrated Rafael formatter with exact per-record source/current controls."""
import linecache
from pathlib import Path
from types import SimpleNamespace
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load
from scripts import plan_rafael_early_tutorial_B42_B43 as previous

ROOT=Path('work/analysis/Rafael_early_story_B36_B41_B51_B60_clean_20261104')
PROOF=ROOT/'B51_B60_source_identity_checkpoint_v1.json'
CURRENT=Path('work/analysis/Rafael_B51_B60_current_20261104/current_effective.json')
MACROS=Path('work/analysis/Rafael_early_tutorial_B42_B43_source_display_20261104/40_native_selectors_macros_andcomplete_preamble_bindings.json')


def qualify_source(doc):
    assert doc['file_path']=='/data/SC0.DK4' and doc['blocks']==list(range(51,61))
    proof,current,macros=map(load,[PROOF,CURRENT,MACROS])
    assert proof['runtime']==current['runtime'] and proof['current_captain0_context_exact']
    assert current['all_source_preambles_andcommand_kinds_preserved']
    assert macros['macro_ascii_lengths']==dict(FI=6,FA=6,FO=10) and macros['selector00_native_actor_is_current_Rafael_captain']
    assert all(macros['runtime'][key]==current['runtime'][key] for key in ['ARM9_sha256','COMMON_sha256'])
    clean_path=Path('work/clean.nds');assert sha(clean_path.read_bytes())=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    clean=IlnkContainer.parse(NdsImage.open(clean_path).read_file(doc['file_path'])).blocks
    image=NdsImage.open(doc['current_ROM'])
    assert sha(Path(doc['current_ROM']).read_bytes())==doc['current_ROM_sha256']==current['runtime']['candidate_sha256']
    assert sha(image.read_file('/__arm9__.bin'))==current['runtime']['ARM9_sha256']
    bank=IlnkContainer.parse(image.read_file(doc['file_path'])).blocks
    assert sha(image.read_file(doc['file_path']))==doc['current_archive_sha256']
    originals={r['id']:r for g in current['groups'] for r in g['records']}
    actors=set(proof['actors']);zeros=set();bindings=[]
    for row in doc['records']:
        if row['kind']=='typed-choice-label':continue
        old=originals[row['id']]
        assert all(row[k]==old[k] for k in ['source_reference','current_reference','source_hex','current_hex','source_complete_preamble_hex'])
        source_ref,current_ref=row['source_reference'],row['current_reference']
        raw,stored,head=map(bytes.fromhex,[row['source_hex'],row['current_hex'],row['source_complete_preamble_hex']])
        assert len(head)==6 and head[:5]==bytes.fromhex('0040ffff00') and head[-1]==raw[0]==stored[0]==row['source_selector']
        assert raw[0] in actors|{254} and b'\0' not in raw[1:] and b'\0' not in stored[1:]
        assert clean[row['block']][source_ref['header_offset']:source_ref['offset']+len(raw)+1]==head[:5]+raw+b'\0'
        assert bank[row['block']][current_ref['header_offset']:current_ref['offset']+len(stored)+1]==head[:5]+stored+b'\0'
        if row['source_selector']==0:zeros.add(raw)
        bindings.append(dict(id=row['id'],source_reference=source_ref,current_reference=current_ref,complete_source_preamble_hex=head.hex(),
            source_body_sha256=sha(raw),selector00_owned_by_complete_preamble=row['source_selector']==0,
            scoped_identity_binding=str(PROOF),scoped_identity_binding_sha256=sha(PROOF.read_bytes()),
            same_Rafael_macro_contract=str(MACROS),same_Rafael_macro_contract_sha256=sha(MACROS.read_bytes()),
            no_new_per_record_dispatch_execution_claim=True))
    assert len(bindings)==245 and {r['id'] for r in bindings}==set(originals)
    return zeros,bindings


parameters={**previous.parameters,'PAIRS':previous.parameters['PAIRS']|{
    ('spice','islands'),('portuguese','military'),('royal','family'),('his','excellency'),('admiral','albuquerque'),
    ('governor','of'),('of','indochina'),('southeast','asia'),('east','asia'),('antony','kuhn'),
    ('evergreen','lotus'),('lotus','leaf'),('uddin','company'),('silveira','company'),('spanish','armada')}}
env={**previous.env,'previous':SimpleNamespace(**parameters),'qualify_source':qualify_source,'__file__':__file__}
source=previous.source
filename=__file__+'::same-Rafael-paragraph-planner-scoped249-record-source-contract'
linecache.cache[filename]=(len(source),None,source.splitlines(keepends=True),filename)
exec(compile(source,filename,'exec'),env);main=env['main']
if __name__=='__main__':main()
