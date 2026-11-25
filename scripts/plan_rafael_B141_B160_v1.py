"""Reuse native paragraph geometry for549 newly reviewed source-bound speeches, including FU."""
import linecache
from pathlib import Path
from types import SimpleNamespace
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load
from scripts.source_locked_derivation_v5118 import checked_text
from scripts import plan_rafael_B121_B140_withstyles_v1 as previous

CURRENT=Path('work/analysis/Rafael_B141_B160_current867_20261105/current_effective.json')
PROOF=Path('work/analysis/Rafael557_macros_inputs_v1_20261105/qualified_identity_andmacros.json')

def qualify_source(doc):
    current,proof=map(load,[CURRENT,PROOF])
    assert current['runtime']==proof['runtime'] and doc['blocks']==list(range(141,161))
    assert doc['file_path']=='/data/SC0.DK4' and doc['all557_individual_four_prose_gates_pass'] and not doc['pending_name_term_IDs']
    assert doc['scoped_identity_proof_sha256']==sha(PROOF.read_bytes())
    assert proof['complete_ARM9_COMMON_font_andactor0_macro_dependencies_qualified']
    assert proof['macro_ascii_lengths']==dict(FI=6,FA=6,FO=10,FU=13)
    assert current['all_source_preambles_andcommand_kinds_preserved']
    cleanpath=Path('work/clean.nds')
    assert sha(cleanpath.read_bytes())=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    image=NdsImage.open(doc['current_ROM'])
    assert sha(Path(doc['current_ROM']).read_bytes())==doc['current_ROM_sha256']==proof['runtime']['candidate_sha256']
    assert sha(image.read_file('/__arm9__.bin'))==proof['runtime']['ARM9_sha256']
    assert sha(image.read_file(doc['file_path']))==doc['current_archive_sha256']
    clean=IlnkContainer.parse(NdsImage.open(cleanpath).read_file(doc['file_path'])).blocks
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
            macro_lengths=proof['macro_ascii_lengths'],no_new_dispatch_orconditional_activation_claim=True))
    assert len(bindings)==549 and {r['id'] for r in bindings}==set(originals)
    return zeros,bindings

parameters={**vars(previous.env['previous'])}
parameters['ADAPTER']=checked_text(parameters['ADAPTER'],{
    "profile.macro_ascii_lengths=={'FI':6,'FA':6,'FO':10}":"profile.macro_ascii_lengths=={'FI':6,'FA':6,'FO':10,'FU':13}",
})
def display(text):
    return text.replace('{MACRO:FI}','Rafael').replace('{MACRO:FA}','Castor').replace('{MACRO:FO}','Castor Co.').replace('{MACRO:FU}','Rafael Castor')
parameters['ENV']={**parameters['ENV'],'display':display}
parameters['PAIRS']|={('first','mate'),('sao','jorge'),('red','dye'),('old','parchment'),('stone','tablet'),
    ('kushan','platter'),('evergreen','lotus'),('lotus','leaf'),('ancient','kingdom'),('kingdom','coin'),
    ('lotion','jar'),('ceremonial','knife'),('sun-crest','sheath'),('tang','bamboo'),('bamboo','craft'),
    ('bamboo','assembly'),('assembly','plan'),('antony','kuhn'),('abraham','ibn'),('ibn','uddin'),
    ('market','share'),('naval','battle'),('nonaggression','pact'),('ottoman','empire'),('new','world'),
    ("doesn't",'he'),('all','right'),('go','ahead')}
source=checked_text(previous.source,{
    "macro_widths={'FI':36,'FA':36,'FO':60,'I':12},macro_ascii_lengths={'FI':6,'FA':6,'FO':10}":
        "macro_widths={'FI':36,'FA':36,'FO':60,'FU':78,'I':12},macro_ascii_lengths={'FI':6,'FA':6,'FO':10,'FU':13}",
})
env={**previous.env,'previous':SimpleNamespace(**parameters),'qualify_source':qualify_source,'__file__':__file__}
filename=__file__+'::same-native-geometry-current-full-name-length-and549-exact-preambles'
linecache.cache[filename]=(len(source),None,source.splitlines(keepends=True),filename)
exec(compile(source,filename,'exec'),env)
main=env['main']
if __name__=='__main__':main()
