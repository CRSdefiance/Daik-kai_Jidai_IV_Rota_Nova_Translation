"""Reuse the qualified full-width planner with exact Maria source/current bindings andmeasured macros."""
import inspect
import linecache
from pathlib import Path
from types import SimpleNamespace
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from scripts import plan_hodram_B211_B230_v2 as planner
from scripts.audit_story_glyph_consistency import load
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.source_locked_derivation_v5118 import checked_text

ROOT=Path('work/Maria_B0_B32_clean_20261109')
FORMATTING=ROOT/'formatting_v1'
MACROS=load(FORMATTING/'native_macro_measurements.json')
MACRO_LENGTHS=MACROS['macro_ascii_lengths']
DEFAULTS={k:v['text'] for k,v in MACROS['defaults'].items()}
assert MACRO_LENGTHS==dict(FI=5,FA=2,FO=7,FU=15)


def display(text):
    for token,value in DEFAULTS.items():
        text=text.replace('{MACRO:'+token+'}',value)
    return text


def qualify_source(doc):
    current=load(ROOT/'current_v1/current_effective.json')
    objects=load(ROOT/'current_objects_v1/current_objects.json')
    prose=load(doc['source_full_manuscript'])
    assert digest(doc['source_full_manuscript'])==doc['source_full_manuscript_sha256']
    assert doc['runtime']==current['runtime']==objects['runtime']==MACROS['runtime']
    assert doc['file_path']=='/data/SC3.DK4' and doc['physical_speech_objects']==299
    assert doc['blocks']==list(range(15))+list(range(16,33))
    assert current['all_source_preambles_andcommand_kinds_preserved']
    assert digest(doc['current_ROM'])==doc['current_ROM_sha256']==doc['runtime']['candidate_sha256']
    assert digest('work/clean.nds')=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    clean,bank=[IlnkContainer.parse(NdsImage.open(p).read_file(doc['file_path'])).blocks for p in ['work/clean.nds',doc['current_ROM']]]
    from dk4tool.patch.grand_race_menu_release import sha
    image=NdsImage.open(doc['current_ROM'])
    assert sha(image.read_file('/__arm9__.bin'))==doc['runtime']['ARM9_sha256']
    assert sha(image.read_file(doc['file_path']))==doc['current_archive_sha256']
    bound={r['id']:r for g in current['groups'] for r in g['records']}
    bound.update({r['id']:r for r in objects['style_records']+objects['choice_records']})
    original={r['id']:r for r in prose['records']}
    assert len(bound)==len(original)==len(doc['records'])==301
    bindings=[]
    for row in doc['records']:
        prior=bound[row['id']];source=original[row['id']]
        logical=row['english']
        for token in DEFAULTS:
            logical=logical.replace('{MACRO:'+token+'}',token)
        assert logical==source['english'] and row['review']==source['review']
        for key in ['source_reference','current_reference','source_hex','current_hex']:
            assert row[key]==prior[key]
        sr,cr=row['source_reference'],row['current_reference'];block=row['block']
        raw,stored=[bytes.fromhex(row[k]) for k in ['source_hex','current_hex']]
        assert clean[block][sr['offset']:sr['offset']+len(raw)+1]==raw+b'\0'
        assert bank[block][cr['offset']:cr['offset']+len(stored)+1]==stored+b'\0'
        if row['kind']=='typed-choice-label':
            before=bytes.fromhex(row['source_choice_object_hex']);now=bytes.fromhex(row['current_choice_object_hex'])
            assert before[:2]==now[:2]==b'\0!'
            assert clean[block][row['source_command_offset']:row['source_command_offset']+len(before)]==before
            assert bank[block][cr['command_offset']:cr['command_offset']+len(now)]==now
            continue
        if row.get('native_object_kind')=='4100-style-alternative':
            head=bytes.fromhex(row['source_header_hex']);before=bytes.fromhex(row['source_object_hex']);now=bytes.fromhex(row['current_style_object_hex'])
            assert head==before[:20] and head[:2]==b'\0A' and head[-2:]==bytes([0,row['source_selector']])
            assert clean[block][row['source_command_offset']:row['source_command_offset']+len(before)]==before
            assert bank[block][cr['command_offset']:cr['command_offset']+len(now)]==now
            assert row['source_style_indices']==prior['source_style_indices'] and row['current_style_indices']==prior['current_style_indices']
            assert row['virtual_formatter_prefix_is_not_part_of_stored_alternative_text']
        else:
            head=bytes.fromhex(row['source_complete_preamble_hex'])
            assert head[:5]==bytes.fromhex('0040ffff00') and head[-1]==raw[0]==stored[0]==row['source_selector']
            assert clean[block][sr['offset']-5:sr['offset']+1]==bank[block][cr['offset']-5:cr['offset']+1]==head
        bindings.append(dict(id=row['id'],source_reference=sr,current_reference=cr,complete_source_header_hex=head.hex(),source_body_sha256=sha(raw)))
    assert len(bindings)==299
    return set(),bindings


base=planner.main.__globals__['previous']
adapted=checked_text(base.ADAPTER,{
    "profile.macro_ascii_lengths=={'FI':6,'FA':9,'FO':15} and profile.macro_widths['FA']==54":
        "profile.macro_ascii_lengths==MACRO_LENGTHS and all(profile.macro_widths[k]==6*n for k,n in MACRO_LENGTHS.items())"})
previous=SimpleNamespace(**{**vars(base),'ADAPTER':adapted,
    'ENV':{**base.ENV,'display':display,'MACRO_LENGTHS':MACRO_LENGTHS}})
source=checked_text(inspect.getsource(planner.main),{
    "return replace(profile,window_width_px=228 if row['kind']=='system-FE' else 216,":
        "return replace(profile,macro_ascii_lengths=MACRO_LENGTHS,macro_widths={**profile.macro_widths,**{k:6*n for k,n in MACRO_LENGTHS.items()}},window_width_px=228 if row['kind']=='system-FE' else 216,",
    "'Hodram complete-exchange plan:'":"'Maria complete-exchange plan:'",
    "'Hodram-complete-exchange-RESEARCH-ONLY:'":"'Maria-complete-exchange-RESEARCH-ONLY:'",
    "    scoped=preferences['records']":
        "    page_phrases={k:v for k,v in page_phrases.items() if k in by_id}\n    scoped=preferences['records']",
})
env={**planner.main.__globals__,**globals(),'__file__':__file__}
filename=__file__+'::same-full-width-parity-pagination-planner-current-Maria-macro-calibration'
linecache.cache[filename]=(len(source),None,source.splitlines(keepends=True),filename)
exec(compile(source,filename,'exec'),env)
main=env['main']

if __name__=='__main__':main()
