"""Automatic full-width plans, with exact source-bound silent/question reactions."""
import inspect
from dataclasses import replace
from types import FunctionType
from pathlib import Path
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts import plan_Hodram_B31_B53_v8725 as previous
from scripts.Hodram_FE_font_oracles_v8315 import bind
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B54_B60_layout_v8802b')
DOC=Path('translations/hodram_B54_B60_editorial_manuscript_v1.json')
LOGICAL=Path('work/analysis/Hodram_B54_B60_logical_v8801/logical_paragraphs.json')
MEASUREMENT=previous.MEASUREMENT
document=read(DOC)
REACTIONS={r['id']:dict(source_hex=r['source_hex'],logical_English=r['english']) for r in document['records'] if r['english'] in ['…','？']}
assert len(REACTIONS)==6

def source_bound_reaction(row,body):
    binding=REACTIONS.get(row['id'])
    return binding==dict(source_hex=row['source_hex'],logical_English=body) and bytes.fromhex(row['source_hex'])[1:].decode('cp932')==body

def get_profile(row):
    assert (row['kind']=='progressive' and row['source_selector'] in [1,20,23,24,36,84,113,114,119,141]) or (row['kind']=='system-FE' and row['source_selector']==254)
    p=get_dialogue_profile('hodram-story-live')
    assert p.window_width_px==216 and p.max_lines==4 and p.default_ascii_width==6 and p.default_multibyte_width==12
    assert p.macro_ascii_lengths==dict(FI=6,FA=9,FO=15) and p.guard_linebreaks and p.pair_phase_safe_breaks
    return replace(p,leading_speaker_bytes=frozenset({row['source_selector']}))

def display(text):return text.replace('{MACRO:FI}','Hodram').replace('{MACRO:FA}','Bergstrom').replace('{MACRO:FO}','Bergstrom Fleet')

ADAPTER=checked_text(previous.ADAPTER,{
    "row['source_selector'] in [34,113]":"row['source_selector'] in [1,20,23,24,36,84,113,114,119,141]",
    'all(32<=ord(c)<127 for c in body)':"all(32<=ord(c)<127 or c in '…？' and source_bound_reaction(row,body) for c in body)",
    'length=len(display(text))':"length=len(display(text).encode('cp932'))",
    'line_lengths=[len(display(v)) for v in lines]':"line_lengths=[len(display(v).encode('cp932')) for v in lines]",
    'Hodram B31/B53 plan:':'Hodram B54-B60 plan:',
    'Hodram-B31-B53-RESEARCH-ONLY:':'Hodram-B54-B60-RESEARCH-ONLY:',
})
PAIRS=previous.PAIRS|{('ethnic','group'),('younger','brother'),('king','solomon'),('demon','king'),('portuguese','fleet'),('sao','jorge'),('proof','of'),('of','conquest'),('high','price'),('slave','trader'),('slave','raids'),('ship\'s','carpenter'),('second','home'),('peace','and'),('and','prosperity'),('thank','you'),("don't",'mention'),('mention','it')}
ENV={**previous.ENV,'get_profile':get_profile,'display':display,'PAIRS':PAIRS,'BOUND_ZERO_SOURCE_BODIES':frozenset(),'source_bound_reaction':source_bound_reaction}
exec(compile(ADAPTER,__file__+'::source-bound-reactions-full-width','exec'),ENV);plan=ENV['plan']
base_qa=FunctionType(previous.base_qa.__code__,{**previous.base_qa.__globals__,'get_profile':get_profile},argdefs=previous.base_qa.__defaults__)

if __name__=='__main__':
    assert not ROOT.exists();logical,measured=map(read,[LOGICAL,MEASUREMENT])
    assert logical['manuscript_sha256']==sha(DOC.read_bytes()) and logical['fresh_native_alignment_cases']==328 and len(document['records'])==82
    image=NdsImage.open(document['current_ROM']);assert sha(Path(document['current_ROM']).read_bytes())==document['current_ROM_sha256']
    _,_,oracle=bind(image);assert oracle['whole12byte_name_inverse_to_previous_font_oracle_ARM9'] and measured['ARM9_sha256']==previous.previous.bound['current_ARM9_sha256']
    rows=[];failures=[]
    for row in document['records']:
        try:
            assert not row['review']['formatting'];planning=dict(row);planning['english']=row['planned_English_markup']
            p=plan(planning);assert ' '.join(p['lines'])==row['english'];raw=bytes.fromhex(p['encoded_hex'])
            assert raw[0]==row['source_selector'] and b'\0' not in raw[1:]
            p.update(file_path=row['file_path'],block=row['block'],source_record_index=row['source_record_index'],source_selector=row['source_selector'],kind=row['kind'],logical_English=row['english'],planning_record=planning,
                base_QA=base_qa(planning,p),original_consumer_usable_text_width_px=216,original_consumer_bitmap_width_px=228 if row['kind']=='system-FE' else 216)
            rows.append(p)
        except (ValueError,AssertionError) as exc:failures.append(dict(id=row['id'],error_type=type(exc).__name__,error=str(exc)))
    ROOT.mkdir(parents=True)
    save(ROOT/'automatic_plans.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),logical=str(LOGICAL),logical_sha256=sha(LOGICAL.read_bytes()),records=rows,failures=failures,
        source_owned_planner=ADAPTER,source_owned_profile_function=inspect.getsource(get_profile),source_owned_display_function=inspect.getsource(display),
        source_owned_reaction_predicate=inspect.getsource(source_bound_reaction),source_bound_reaction_bindings=REACTIONS,coherent_pairs=sorted(PAIRS),
        all_words_punctuation_andFI3_FA4_FO0_preserved_without_shortening=True,prose_manual_breaks_authored=False,automatic_compiler_breaks_not_manual_prose=True,
        original_FE_usable216_bitmap228_stride288_metrics6x12_physical16_distinction_preserved=True,
        earlier_boundary_measurement=str(MEASUREMENT),earlier_boundary_measurement_sha256=sha(MEASUREMENT.read_bytes()),target_font_oracle_inverse_binding=oracle,
        original_QA_warnings_errors_infos_retained_without_waiver=True,formatting_gate_native_glyphs_stored_actual_andrelease_pending=True,
        new_credit=0,new_emulator_runs=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [DOC,LOGICAL,MEASUREMENT,Path(previous.__file__),Path(__file__)]}))
    for p in rows:
        issues=[(i['severity'],i['code']) for i in p['base_QA']['issues']]
        print(p['id'],p['expected_native_pages'],p['lines'],issues)
    print('PLANS',len(rows),'FAILURES',failures)
    assert not failures and len(rows)==82
