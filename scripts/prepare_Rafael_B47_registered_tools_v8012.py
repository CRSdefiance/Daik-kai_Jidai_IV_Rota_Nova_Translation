"""Prepare source-locked registration/build/regression/release-verification successors."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Rafael_B47_registered_tools_v8012')
if __name__=='__main__':
    assert not ROOT.exists()
    source=Path('scripts/register_Rafael_B46_v7963.py').read_text(encoding='utf8')
    old_update=source[source.index("    profile.update("):source.index("    updated=deepcopy(registry)")]
    new_update='''    profile.update(status='experimental',rafael_B47_editorial=owned.CONFIG,
        description="Complete V7964 plus Rafael B47:15 speeches;eight source-grounded revisions andseven contextual retentions.",
        note="Clean Japanese/B37 prerequisite,whole conditional exchange andsource-bound glosses before current English. Rafael Castor,Janus Pasar,Claudio Manaus,Julio Erneco retained;Pasar is distinct from Pasha. Valdes/Pasha/Hayreddin component-only retentions;full207 review remains open. Preserve guarded Mediterranean passage,eastern-half Ottoman territory,conditional enemy initiative,qualified recruitment,cautious trading,ship/personal preparation andrenewed resolve. Automatic216px/four-row geometry;15 paragraphs/16 pages,R53 alone two pages withordinary A4720 transition andfollowing R70. Six original infos/two exact source/text/compiled/line-bound warning exceptions;R5/R63 fuller three-row wrapping without word loss. All48 commands/24 relatives/six raw predicates/61FF/A000/fullend andcomplete preambles/source00/zero macros/inverses preserved.343 loads/686parent modes. Two disclosed original-entry fixture runs32002frames,11actual speeches each language/88complete holds;eight viewed sheets.Four conditional speeches/Janus header native-only. Normal[0,0] at6416/6655. Preserve24command/four duration differences,English+58LCGsteps at exit,later-7833,157/157laterRGBdifferences,models/persistent objects/actors/calendar differences andallrawmeasurements. No natural activation,fullroute,hardware,future-state/fullsimulation/completecausal claim.15policy positives/302guard rejections;whole-ROM atomic positive/202independent precommit rejections. One manifest batch includes15objects once. Fullgoal/allfour stories/earlier dialogue/shared shops/towns/random/Help/wraps/names remain active;graphics/later older-record re-audit separate. MainV4701 unchanged;no separate unified package,promotion,pruning,commit orpush.")
'''
    results=[derive('scripts/register_Rafael_B46_v7963.py','scripts/register_Rafael_B47_v8012.py',{
        old_update:new_update,
        '"""Register all26 B46 decisions after the complete V7911 stack, retaining both manifests."""':
            '"""Register fifteen B47 decisions after the complete V7964 stack."""',
        'rafael_B46_editorial_v2':'rafael_B47_editorial_v1',
        'Rafael_B46_release_paths_v7958':'Rafael_B47_release_paths_v8006',
        "profile_config.get('rafael_B45_editorial')":"profile_config.get('rafael_B46_editorial')",
        'B46':'B47','v7963':'v8012','v7964':'v8013','v7911':'v7964','V7911':'V7964',
        'v7962':'v8011','v7955':'v8008','==26':'==15','==187':'==202','==633':'==635',
    })]
    results.append(derive('scripts/build_Rafael_B46_v7964.py','scripts/build_Rafael_B47_v8013.py',{
        'B46':'B47','v7964':'v8013','v7963':'v8012',
    }))
    results.append(derive('scripts/run_Rafael_B46_regressions_v7964.py','scripts/run_Rafael_B47_regressions_v8013.py',{
        'B46':'B47','v7964':'v8013',
    }))
    results.append(derive('scripts/verify_Rafael_B46_release_v7965.py','scripts/verify_Rafael_B47_release_v8014.py',{
        'rafael_B46_editorial_v2':'rafael_B47_editorial_v1',
        "profile_config.get('rafael_B45_editorial')":"profile_config.get('rafael_B46_editorial')",
        'B46':'B47','v7965':'v8014','v7964':'v8013','v7963':'v8012','v7911':'v7964',
        'v7961':'v8010','==635':'==636','manifest_batches=635':'manifest_batches=636',
        'all635':'all636','==26':'==15','==[46]':'==[47]',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivations.json',dict(derivations=results,
        no_registry_builder_ROM_orcredit_change=True,new_credit=0,full_goal_complete=False))
    print('Four source-locked B47 registration/build/regression/release tools prepared. Execute registration only after all202 atomic guards pass.')
