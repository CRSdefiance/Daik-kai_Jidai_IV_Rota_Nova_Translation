"""Bind clean and registered dialogue around company-name punctuation."""

from inspect import getsource
from pathlib import Path

from scripts import prepare_london_guild_assignments_20261118 as precedent
from scripts import register_stock_encounter_names_20261121 as parent
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = Path("work/company_name_dialogue_20261121")
BLOCKS = ((37, 44, 70, 73, 143, 154, 162, 292),
          (38, 153, 168), (54, 55, 60, 138, 151, 282), (62, 113, 118, 135, 139))
CONTEXT = (
    "Rafael's company announcement, introductions, permission to pass and discussions of company leadership.",
    "Hodram's fleet is recognized by observers and officials during encounters and town visits.",
    "Lil's company's actions are discussed in private exchanges, news reports and public introductions.",
    "Maria's clan is identified in negotiations, recollections, guild business and crew conversations.",
)


def main():
    code = checked_text(getsource(precedent.main), {
        '    ROOT.mkdir()': '    ROOT.mkdir(parents=True)',
    })
    namespace = vars(precedent) | globals()
    exec(compile(code, __file__ + "::bind", "exec"), namespace)
    namespace["main"]()
    packet = ROOT / "paired_source.json"
    data = precedent.base.load(packet)
    data["additional_command_alignment_needed"] = [dict(route=0, block=84, source_count=217, installed_count=219),
                                                  dict(route=3, block=116, source_count=62, installed_count=64)]
    precedent.base.save(packet, data)


if __name__ == "__main__":
    main()
