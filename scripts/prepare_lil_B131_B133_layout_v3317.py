"""Bind two blocks andsource00 without changing shared codec/encoder behavior."""
from pathlib import Path
import importlib
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
SOURCE=Path('work/analysis/lil_remaining_B131_B140_source_v3306b/next63_B131_B133_clean_current_context.json')
CONTROL=Path('work/analysis/lil_B131_B133_controls_v3308b/all61_source_current_dispatch_selector00_FE_and5_predicates.json')
VOICE=Path('work/analysis/lil_B131_B133_voices_v3307b/current_five_static_names_voices_selector00_and207_catalog_rebind.json')
TERMS=Path('work/analysis/lil_B131_B133_terms_v3313/clean_current_items_names_and_share_ratio_reconciliation.json')
BRANCH=Path('work/analysis/lil_B131_B133_branches_v3309b/original_relative_skip_operand_proof.json')
CATALOG=Path('work/analysis/lil_B131_B133_controls_v3308b/current_registered_name_catalog_binding.json')
PROFILE=Path('dk4tool/dialogue/lil_B131_B133_profile.py')
FORMATTER=Path('dk4tool/dialogue/lil_B131_B133_layout_v1.py')
OLD=Path('dk4tool/dialogue/lil_B122_B127_layout_v2.py')
PLANNER=Path('scripts/plan_lil_B131_B133_layout_v3317b.py')
ROOT=Path('work/analysis/lil_B131_B133_layout_tools_v3317')
if __name__=='__main__':
    assert not any(p.exists() for p in [PROFILE,FORMATTER,PLANNER,ROOT]);source=read(SOURCE);deps={str(p):sha(p.read_bytes()) for p in [SOURCE,CONTROL,VOICE,TERMS,BRANCH,CATALOG]};hashes=sorted({r[k] for r in source['blocks'] for k in ['clean_block_sha256','current_block_sha256']})
    t='''"""Exact B131/B133 static speakers andFE;source00 is actor0,not a terminator."""
from dataclasses import replace
from pathlib import Path
import json
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.patch.grand_race_menu_release import sha
ARM9_SHA=ARM_REPLACE
BLOCKS=frozenset(BLOCK_REPLACE)
SELECTORS=frozenset({0,2,5,9,20})
DEPENDENCIES=DEP_REPLACE
CONTROL=Path(CONTROL_REPLACE)
VOICE=Path(VOICE_REPLACE)
def profile_for(arm,source_block,consumer='progressive'):
    if sha(arm)!=ARM9_SHA or sha(source_block) not in BLOCKS:raise ValueError('B131/B133 requires exact clean/current blocks andruntime')
    for p,digest in DEPENDENCIES.items():
        if sha(Path(p).read_bytes())!=digest:raise ValueError('B131/B133 source contract changed:'+p)
    control=json.loads(CONTROL.read_text(encoding='utf-8'));voice=json.loads(VOICE.read_text(encoding='utf-8'))
    if (len(control['speech_dispatch_cases'])!=122 or sum(r['source_selector']==0 for r in control['speech_dispatch_cases'])!=36
        or len(control['current_original_predicate_cases'])!=5 or control['original_event_queries']
        or control['source_macro_counts']!={'FI':6,'FA':0,'FO':1}
        or not control['all2_FE_cases_dispatch5473C_and24310_null_actor_before_dynamic_fallback']
        or not control['source00_is_static_actor0_Rafael_Castor_without_role_assignment']
        or len(voice['fresh_five_actor_names']['rows'])!=5 or not voice['source00_is_static_actor0_not_empty_text_or_dynamic_role']):
        raise ValueError('Complete source00/static actor/FE/predicate/macro contracts required')
    base=get_dialogue_profile('lil-opening-editorial-native-v1')
    if consumer=='progressive':
        return replace(base,name='lil-B131-B133-progressive-runtime-bound-v1',leading_speaker_bytes=SELECTORS,
            metrics_source=base.metrics_source+';60progressive speeches,18source00 actor0/Rafael. Complete speaker00 precedes a nonempty C-string body;only this source-bound prefix may containzero. FI3/FA5/FO9 use Lil captain2 context,not Rafael route macros. No dynamic selector/4100/2000;one2100 menu separate.')
    if consumer=='FE-paper':
        return replace(base,name='lil-B131-B133-FE-runtime-bound-v1',leading_speaker_bytes=frozenset({254}),
            metrics_source=base.metrics_source+';one unlabeled share-exchange notice;original24310null actor before5473C/fallback208.228x48logical/228x64physical paper,conservative216px planning.No leading staging orinvented name/macro.')
    raise ValueError('Unknown B131/B133 consumer')
'''
    for a,b in [('ARM_REPLACE',repr(source['current_ARM9_sha256'])),('BLOCK_REPLACE',repr(hashes)),('DEP_REPLACE',repr(deps)),('CONTROL_REPLACE',repr(str(CONTROL))),('VOICE_REPLACE',repr(str(VOICE)))]:assert a in t;t=t.replace(a,b)
    compile(t,str(PROFILE),'exec');PROFILE.write_text(t,encoding='utf-8')
    t=OLD.read_text(encoding='utf-8').replace('B122-B127','B131-B133');a='frozenset({2,6,9,20,26,92,95,151})';assert a in t;t=t.replace(a,'frozenset({0,2,5,9,20})')
    a='PROTECTED_BOUNDARIES=frozenset({';assert a in t;t=t.replace(a,a+"('old','parchment'),('red','dye'),('castor','company'),('rafael','castor'),('north','sea'),")
    a="_encode=_clone(encoder.encode_relocatable_dialogue,{'format_markup':_format})";assert t.count(a)==1
    t=t.replace(a,'''# The shared relocated encoder rejects all NUL bytes. The current native
# speech handler independently consumes the proven source00 actor byte before
# its body C-string. Permit exactly that one prefix only in this exact profile;
# embedded,extra ortrailing NULs andall other consumers retain the hard rejection.
encoder_source=inspect.getsource(encoder.encode_relocatable_dialogue)
nul=chr(92)+'0'
needle='    if b"'+nul+'" in encoded:'
replacement='    if b"'+nul+'" in encoded and not (source_raw[:1]==b"'+nul+'" and encoded[:1]==b"'+nul+'" and b"'+nul+'" not in encoded[1:] and profile.name=="lil-B131-B133-progressive-runtime-bound-v1" and profile.leading_speaker_bytes==frozenset({0,2,5,9,20})):'
if encoder_source.count(needle)!=1:raise ValueError('Scoped source00 encoder guard source differs')
encoder_source=encoder_source.replace(needle,replacement)
SCOPED_ENCODER_SOURCE_SHA256=sha(encoder_source.encode('utf-8'))
encoder_env={**encoder.__dict__,'format_markup':_format}
exec(compile(encoder_source,__file__,'exec'),encoder_env)
_encode=encoder_env['encode_relocatable_dialogue']''')
    compile(t,str(FORMATTER),'exec');FORMATTER.write_text(t,encoding='utf-8')
    oldplan=Path('scripts/prepare_lil_B122_B127_layout_v3281.py');t=oldplan.read_text(encoding='utf-8')
    a=t.index('SOURCE=Path(');z=t.index('INPUTS=[',a)
    t=t[:a]+f'SOURCE=Path({str(SOURCE)!r})\nPROFILE=Path({str(PROFILE)!r})\nFORMATTER=Path({str(FORMATTER)!r})\nOLD=Path({str(OLD)!r})\n'+t[z:]
    changes={
      'lil_B122_B127_layout_v3281':'lil_B131_B133_layout_v3317b',
      'lil_B122_B127_editorial_manuscript_v2.json':'lil_B131_B133_editorial_manuscript_v1.json',
      'lil_B122_B127_choice_manuscript_v1.json':'lil_B131_B133_choice_manuscript_v1.json',
      'lil_B122_B127_editorial_manuscript_v4.json':'lil_B131_B133_editorial_manuscript_v2.json',
      'lil_B122_B127_choice_manuscript_v3.json':'lil_B131_B133_choice_manuscript_v2.json',
      'dk4tool.dialogue.lil_B122_B127_profile_v2':'dk4tool.dialogue.lil_B131_B133_profile',
      'dk4tool.dialogue.lil_B122_B127_layout_v2':'dk4tool.dialogue.lil_B131_B133_layout_v1',
      'all159_paragraph_and_label_layout_QA.json':'all63_paragraph_and_label_layout_QA.json',
      'len(reports)==159':'len(reports)==63','plans=159':'plans=63'}
    for a,b in changes.items():assert a in t,a;t=t.replace(a,b)
    compile(t,str(PLANNER),'exec');PLANNER.write_text(t,encoding='utf-8');ROOT.mkdir(parents=True)
    save(ROOT/'source00_scoped_formatter_and_planner_provenance.json',dict(source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),profile=str(PROFILE),profile_sha256=sha(PROFILE.read_bytes()),formatter=str(FORMATTER),formatter_sha256=sha(FORMATTER.read_bytes()),previous_formatter=str(OLD),previous_formatter_sha256=sha(OLD.read_bytes()),planner=str(PLANNER),planner_sha256=sha(PLANNER.read_bytes()),only_exact_proven_source00_actor_prefix_allowed_not_embedded_NUL=True,global_codec_encoder_QA_and_all_previous_profiles_unchanged=True,old_record_technical_reaudit_not_started_or_claimed=True,no_ROM_ledger_registry_credit=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
