"""Pin one-label research image, a complete source-exchange fixture, and exact target context."""
from pathlib import Path
from copy import deepcopy
import json,os
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/shady_man_research_tools_v6259')
if __name__=='__main__':
    assert not ROOT.exists();doc=read('translations/shady_man_label_manuscript_v1.json');ROOT.mkdir(parents=True)
    tools=[derive('scripts/research_generic_speaker_labels_v5881.py','scripts/research_shady_man_label_v6260.py',{
      'generic_speaker_labels_v5881':'shady_man_label_v6260','generic_speaker_labels_research_v5881':'shady_man_label_research_v6260',
      'translations/generic_speaker_labels_manuscript_v1.json':'translations/shady_man_label_manuscript_v1.json',
      'generic_speaker_label_data_v1':'shady_man_label_data_v1','three-label':'one-label','three_label':'one_label',
      'Man/Woman/Stranger':'Shady Man','V5872':'V6220','three-label data-only':'one-label data-only',
    })]
    tools.append(derive('scripts/current_build_native_context_v6097.py','scripts/current_build_native_context_v6261.py',{
      '03a905a9e4a4df117b8a4b5280ec3c669a4db00547972397413bc8bebc4afbbd':doc['target_ARM9_sha256'],
      'snapshot_is_current_opening_not_B180_activation':'snapshot_is_complete_B206_content_fixture_not_natural_event_activation',
    }))
    tools.append(derive('scripts/run_lil_B206_source_buy_v6243.py','scripts/run_shady_man_source_buy_v6262.py',{
      'work/analysis/lil_B206_source_fixture_v6242/complete_B206_source_B22_fixture.json':'work/analysis/shady_man_source_fixture_v6260/complete_B206_source_B22_fixture.json',
      'lil_B206_source_run_v6243_buy':'shady_man_source_run_v6262_buy','lil_B206_source_v6243_buy':'shady_man_source_v6262_buy',
      "\"'--capture-at',*map(str,range(2350,16001,60))\"":"\"'--capture-at','4000'\"",
      "\"'--dump-ram'\"":"\"'--dump-capture-ram','--dump-ram'\"",
      "    text=checked_text(source.read_text(encoding='utf-8'),changes)":"    changes[\"'--capture-every','999999'\"]=\"'--capture-every','60'\"\n    text=checked_text(source.read_text(encoding='utf-8'),changes)",
    }))
    save(ROOT/'source_locked_research_and_exact_context_tools.json',dict(tools=tools,target_ARM9_sha256=doc['target_ARM9_sha256'],native_addresses_and123264_payload_extent_preserved=True,no_old_RAM_overlay_or_runtime_fixture=True,full_goal_complete=False))
    print('Research-image,complete source-path run and exact target context tools prepared;no source checks weakened.')
