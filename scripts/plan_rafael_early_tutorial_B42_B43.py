"""Reuse the paragraph planner with source-bound actor0 andmeasured Rafael defaults."""
import inspect
import linecache
from pathlib import Path
from types import SimpleNamespace
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load
from scripts import plan_editorial_scene_prose_v18 as previous
from scripts.source_locked_derivation_v5118 import checked_text

PROOF=Path('work/analysis/Rafael_early_tutorial_B42_B43_source_display_20261104/40_native_selectors_macros_andcomplete_preamble_bindings.json')

def display(text):
    return text.replace('{MACRO:FI}','Rafael').replace('{MACRO:FA}','Castor').replace('{MACRO:FO}','Castor Co.')

def qualify_source(doc):
    assert doc['file_path']=='/data/SC0.DK4' and doc['blocks']==[42,43]
    proof=load(PROOF);assert proof['macro_ascii_lengths']==dict(FI=6,FA=6,FO=10)
    assert proof['all40_exact_source_current_sixbyte_preambles_andoriginal_dispatches_pass'] and proof['selector00_native_actor_is_current_Rafael_captain']
    originals={r['id']:r for r in proof['records']}
    clean=Path('work/clean.nds');assert sha(clean.read_bytes())=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    blocks=IlnkContainer.parse(NdsImage.open(clean).read_file(doc['file_path'])).blocks
    zeros,bindings=set(),[]
    for row in doc['records']:
        ref=row['source_reference'];block=blocks[row['block']];raw=bytes.fromhex(row['source_hex']);head=bytes.fromhex(row['source_complete_preamble_hex'])
        assert len(head)==6 and head[:5]==bytes.fromhex('0040ffff00') and head[-1]==row['source_selector']==raw[0]
        assert block[ref['header_offset']:ref['offset']+len(raw)+1]==head[:5]+raw+b'\0'
        original=originals[row['id']]
        assert original['source_reference']==ref and original['current_reference']==row['current_reference'] and original['logical_English']==row['english']
        assert original['complete_source_andcurrent_preamble_hex']==head.hex()
        if row['source_selector']==0:
            assert head.hex()=='0040ffff0000' and b'\0' not in raw[1:];zeros.add(raw)
        bindings.append(dict(id=row['id'],source_reference=ref,complete_source_preamble_hex=head.hex(),source_body_sha256=sha(raw),
            current_Rafael_native_dispatch_andmacro_proof=str(PROOF),current_Rafael_native_dispatch_andmacro_proof_sha256=sha(PROOF.read_bytes()),
            selector00_owned_by_complete_preamble=row['source_selector']==0))
    assert len(bindings)==40 and len(zeros)==5 and set(originals)=={r['id'] for r in doc['records']}
    return zeros,bindings

inherited=previous.main.__globals__['previous']
adapter=checked_text(inherited.ADAPTER,{
    "profile.macro_ascii_lengths=={'FI':6,'FA':9,'FO':15} and profile.macro_widths['FA']==54":
        "profile.macro_ascii_lengths=={'FI':6,'FA':6,'FO':10} and profile.macro_widths['FA']==36",
})
parameters={**vars(inherited),'ADAPTER':adapter,'ENV':{**inherited.ENV,'display':display},
    'PAIRS':inherited.PAIRS|{('first','mate'),('sail','handler'),('deck','view'),('north','sea'),('good','companions'),('old','man'),('on','its'),('its','own')}}
source=checked_text(inspect.getsource(previous.main),{
    "profile=get_dialogue_profile('hodram-story-live')":"profile=get_dialogue_profile('raphael-story-live')",
    'profile.macro_ascii_lengths==dict(FI=6,FA=9,FO=15)':'profile.macro_ascii_lengths==dict(FI=7,FA=6,FO=10)',
    "return replace(profile,window_width_px=228 if row['kind']=='system-FE' else 216,":
        "return replace(profile,name='rafael-early-tutorial-measured-native-v1',balanced_wrapping=True,literal_prefix_policy='native-guard-v255',macro_widths={'FI':36,'FA':36,'FO':60,'I':12},macro_ascii_lengths={'FI':6,'FA':6,'FO':10},window_width_px=228 if row['kind']=='system-FE' else 216,",
    'Hodram complete-exchange plan:':'Rafael early-tutorial plan:',
    'Hodram-complete-exchange-RESEARCH-ONLY:':'Rafael-early-tutorial-RESEARCH-ONLY:',
})
env={**previous.main.__globals__,'previous':SimpleNamespace(**parameters),'qualify_source':qualify_source,'__file__':__file__}
filename=__file__+'::same-automatic-paragraphs-source0-measured-Rafael-defaults'
linecache.cache[filename]=(len(source),None,source.splitlines(keepends=True),filename)
exec(compile(source,filename,'exec'),env);main=env['main']
if __name__=='__main__':main()
