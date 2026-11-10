"""Recover the saved visual receipt and refine only the concrete layout findings."""
from pathlib import Path
from copy import deepcopy
from scripts.audit_story_glyph_consistency import load,save
from scripts.source_locked_derivation_v5118 import checked_text
from scripts import refine_hodram_B281_B300_visual_v1 as previous

ROOT=previous.ROOT
OUT=ROOT/'formatting_v1/visual_preferences_v4.json'

def main():
    assert not OUT.exists()
    # v1 saved its preferences, then failed to write its receipt because Path was
    # not imported. Preserve that preference file and verify its exact contents.
    source=checked_text(Path(previous.__file__).read_text(encoding='utf-8'),{
        'assert not VIEW.exists() and not PREFERENCES.exists()':
            'assert not VIEW.exists() and PREFERENCES.exists()',
        'save(PREFERENCES,prefs)':'assert load(PREFERENCES)==prefs',
    })
    env={**vars(previous),'Path':Path,'__name__':'visual_receipt_recovery','__file__':previous.__file__}
    exec(compile(source,__file__+'::recover-original-receipt-without-overwriting-preferences','exec'),env)
    env['main']()
    p=deepcopy(load(previous.PREFERENCES))
    p['records']['DK4_MES_B282_R0019'].pop('one_page')
    p['records']['DK4_MES_B282_R0019']['page_clause']='I am counting on you.'
    p['records']['DK4_MES_B282_R0019']['reason']='One page is infeasible with complete names and intact prose. Keep the complete final sentence on the continuation page instead of splitting I am from counting on you.'
    p['records']['DK4_MES_B287_R0125']['required_pairs'].append(['the','ancient'])
    p['records']['SC1_B290_STYLE_1924_0']['required_pairs'].append(["won't",'run'])
    p['records']['SC1_B291_STYLE_24_156']['required_pairs'].append(["we'll",'get'])
    p['records']['DK4_MES_B286_R0075']['required_pairs'] += [['sooner','or'],['or','later']]
    save(OUT,p)
    save(ROOT/'visual_receipt_recovery_v2.json',dict(
        failure='The original producer saved preferences then raised NameError for missing Path while constructing its receipt.',
        preserved_preferences=str(previous.PREFERENCES),receipt=str(previous.VIEW),
        recovered_with_exact_preference_equality=True,no_native_orvisual_checks_repeated=True,
        next_preferences=str(OUT),new_credit=0))
    print('Recovered initial visual receipt; refined five concrete layout candidates.')

if __name__=='__main__':main()
