"""Reuse validated Rafael geometry for325 speeches;typed labels retain their own consumer."""
import linecache
from pathlib import Path
from types import SimpleNamespace
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load
from scripts import plan_rafael_B51_B60_v3 as previous

CURRENT=Path('work/analysis/Rafael_B81_B84_current_20261105/current_effective.json')
PROOF=Path('work/analysis/Rafael_B81_B84_formatting_20261105/scoped_names_macro_andconsumer_dependency_qualification_v1.json')

def qualify_source(doc):
    assert doc['file_path']=='/data/SC0.DK4' and doc['blocks']==[81,82,83,84]
    current,proof=map(load,[CURRENT,PROOF])
    assert current['runtime']==proof['runtime'] and proof['complete_ARM9_COMMON_font_andactor_array_exact_to_qualified_runtime']
    assert sha(PROOF.read_bytes())==doc['scoped_identity_proof_sha256']
    assert proof['macro_ascii_lengths']==dict(FI=6,FA=6,FO=10)
    assert current['all_source_preambles_andcommand_kinds_preserved']
    cleanpath=Path('work/clean.nds');assert sha(cleanpath.read_bytes())=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    clean=IlnkContainer.parse(NdsImage.open(cleanpath).read_file(doc['file_path'])).blocks
    image=NdsImage.open(doc['current_ROM'])
    assert sha(Path(doc['current_ROM']).read_bytes())==doc['current_ROM_sha256']==current['runtime']['candidate_sha256']
    assert sha(image.read_file('/__arm9__.bin'))==current['runtime']['ARM9_sha256']
    assert sha(image.read_file(doc['file_path']))==doc['current_archive_sha256']
    bank=IlnkContainer.parse(image.read_file(doc['file_path'])).blocks
    originals={r['id']:r for g in current['groups'] for r in g['records']}
    zeros=set();bindings=[]
    for row in doc['records']:
        if row['kind']=='typed-choice-label':continue
        old=originals[row['id']]
        assert all(row[k]==old[k] for k in ['source_reference','current_reference','source_hex','current_hex','source_complete_preamble_hex'])
        sr,cr=row['source_reference'],row['current_reference']
        raw,stored,head=map(bytes.fromhex,[row['source_hex'],row['current_hex'],row['source_complete_preamble_hex']])
        assert len(head)==6 and head[:5]==bytes.fromhex('0040ffff00') and head[-1]==raw[0]==stored[0]==row['source_selector']
        assert raw[0] in set(proof['actors'])|{254} and b'\0' not in raw[1:] and b'\0' not in stored[1:]
        assert clean[row['block']][sr['header_offset']:sr['offset']+len(raw)+1]==head[:5]+raw+b'\0'
        assert bank[row['block']][cr['header_offset']:cr['offset']+len(stored)+1]==head[:5]+stored+b'\0'
        if raw[0]==0:zeros.add(raw)
        if raw[0]==254:assert row['source_FE_presentation_kind'] and row['FE_is_not_an_ordinary_actor_nameplate']
        bindings.append(dict(id=row['id'],source_reference=sr,current_reference=cr,complete_source_preamble_hex=head.hex(),
            source_body_sha256=sha(raw),selector00_owned_by_complete_preamble=raw[0]==0,
            scoped_identity_binding=str(PROOF),scoped_identity_binding_sha256=sha(PROOF.read_bytes()),
            no_new_per_record_dispatch_execution_claim=True))
    assert len(bindings)==325 and {r['id'] for r in bindings}==set(originals)
    return zeros,bindings

parameters={**vars(previous.env['previous'])}
parameters['PAIRS']=parameters['PAIRS']|{
    ('gun','battery'),('boarding','leader'),('sword','fighting'),('bull','fighting'),('north','sea'),('private','fleet'),
    ('mivor','genz'),('gerhard','adernkatz'),('emilio','ferog'),('claudio','manaus'),('julio','erneco'),
    ('mr.','adernkatz'),('miss','cristina'),('tough','training'),('battle','begins'),
    ("aren't",'you'),("isn't",'it'),("didn't",'you'),("don't",'you'),('remember','me')}
env={**previous.env,'previous':SimpleNamespace(**parameters),'qualify_source':qualify_source,'__file__':__file__}
source=previous.source
filename=__file__+'::same-paragraph-native-geometry-and330-exact-source-controls'
linecache.cache[filename]=(len(source),None,source.splitlines(keepends=True),filename)
exec(compile(source,filename,'exec'),env);main=env['main']
if __name__=='__main__':main()
