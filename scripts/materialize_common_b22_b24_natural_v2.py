from __future__ import annotations

import json
from hashlib import sha256
from pathlib import Path

from dk4tool.rom.nds import NdsImage
from dk4tool.script.mesfile import iter_mesfile_records

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "work/analysis/common_clean_inventory.json"
BASE_ROM = ROOT / "out/raphael_natural_v2_pre_common_accepted_rollback.nds"
SOURCE_HASH = "ecb0806b6f36f9bf4164ae46084fbbc12d4122af66b6a8920814197463f19491"


ENGLISH = {
22: {
1:"We can't fight anymore. Admiral, we surrender.",2:"We can't win this. Admiral, we surrender.",3:"No more wasted lives... We surrender.",4:"No hope... They'll all die. We surrender.",5:"A wise retreat... Admiral, we surrender.",6:"Should they attack this city, we'll crush them!",7:"Attack this city? Not happening!",8:"You won't attack this city!",10:"So you're attacking this city? You'll regret it!",11:"You won't hurt this city!",13:"Enemy flagship fled! We won!",14:"Admiral, victory! Enemy flagship fled!",15:"Admiral, victory! Enemy flagship fled!",16:"Enemy admiral fled! We won!",17:"Admiral, victory! Enemy flagship fled!",18:"Gun-platform powder ignited! A fire!",19:"Gun-platform powder ignited! A fire!",20:"Gun-platform powder caught fire!",21:"Gun-platform powder caught fire!",22:"Gunpowder ignited! A fire!",23:"Gun-platform powder ignited! A fire!",24:"Admiral, %s has sunk!",25:"Admiral, %s is sinking...",26:"Admiral, %s has sunk!",27:"Admiral, %s was sunk!",28:"Admiral, %s was sunk!",29:"Admiral, %s was sunk!",30:"Admiral, %s sank!",31:"Admiral, %s has sunk!",32:"Enemy ship %s sunk!",35:"Enemy ship %s sunk!",36:"Enemy ship %s sunk!",37:"Admiral, %s was captured!",38:"Admiral, enemy took %s!",39:"Admiral, %s was captured!",40:"Admiral, %s was captured!",41:"Admiral, they took %s!",42:"Admiral, %s was captured!",43:"Admiral, %s was captured!",44:"Admiral, %s was captured!",45:"Enemy ship %s captured!",46:"%s captured!",47:"Enemy ship %s captured!",48:"Enemy ship %s captured!",49:"Took enemy ship %s!",50:"Enemy ship %s captured!",51:"We took ship %s!",52:"Enemy ship %s captured!",53:"Admiral, %s surrendered!",54:"Admiral, %s surrendered!",55:"Admiral, %s surrendered!",56:"Admiral, %s surrendered!",57:"Admiral, %s surrendered!",58:"Admiral, %s surrendered!",59:"Admiral, %s surrendered!",60:"Admiral, %s surrendered!",61:"Enemy ship %s surrendered!",63:"Enemy ship %s surrendered!",64:"Enemy ship %s surrendered!",65:"Enemy ship %s surrendered!",66:"Enemy ship %s will surrender!",67:"Enemy ship %s surrendered!",68:"Ram hit the enemy ship!",69:"Ram hit!",73:"Admiral, withdrawing!",74:"Admiral, withdrawing!",75:"Admiral, withdrawing!",76:"Admiral, withdrawing!",77:"Shall we attack %s?",78:"Target %s. Confirm attack?",79:"Attack %s, okay?",80:"Attack %s. All right?",81:"Attack %s. Agreed?",82:"Attack %s. Agreed?",83:"Attack %s, okay?",84:"Shall we attack %s?",85:"Admiral, we won!",87:"Admiral, we won!",88:"Admiral, we won!",89:"Admiral, we won!",90:"We won! Admiral, victory is ours!",92:"Our flagship fell. We lost!",93:"Our flagship fell. We lost!",94:"Our flagship fell. We lost!",95:"Our flagship fell. We lost!",96:"Our flagship fell. We lost!",97:"Our flagship fell. We lost!",98:"Our flagship fell. We lost!"},
23: {
2:"This fight's easy!",3:"Shall we begin?",5:"Aaaah!",6:"Whoa! What's happening?!",7:"What in the world?!",13:"We lost when %s's flagship fell!",15:"%s down!",16:"%s down!",17:"%s down!",18:"We defeated %s!",19:"No choice... Raise the white flag.",21:"Where's your work? No time to play.",22:"Hey! What are you doing?!",23:"My, you look awfully idle. How fortunate.",24:"War declared?! Very well, we accept!",25:"War declared... Prepare all fleets!",26:"They declared war? We'll crush them!",27:"War?! Then we'll crush them!",28:"They declared war?! They'll lose!",30:"A foolish war. They'll regret it!",31:"W-we're at war?! Will we make it home alive?",32:"Amazing... Beyond measure!",33:"Whoa... Never seen that before!",34:"A-amazing... That lives in the sea?",35:"Wow... A monster!",36:"Whoa! Can we beat that thing?",37:"Aaaah! So scary!",38:"A true mystery of the sea...",39:"The expedition found nothing nearby.",40:"The expedition is back. Nothing worthwhile.",41:"The expedition found nothing nearby.",42:"The expedition is back. Nothing around here.",43:"The expedition found nothing nearby.",44:"Admiral! The expedition found this!",45:"A major discovery! The expedition found this.",46:"Amazing! The expedition found this!",47:"Admiral, a big find! Look!",48:"Admiral, a big find! Look at this!",49:"Amazing, a huge find! Admiral, look!",50:"Wonderful! Look what they found!",51:"Water %s barrels; food %s barrels.",52:"Water %s barrels; food %s barrels.",53:"Water %s barrels; food %s barrels.",54:"Water %s barrels; food %s barrels.",55:"Water %s barrels; food %s barrels.",58:"Kind natives invited us. Admiral, let's go!",59:"The natives shared food and water.",62:"Natives attacked the expedition!",63:"Natives attacked the expedition!",64:"Admiral! Natives attacked our team!",65:"How awful! Natives attacked our team!",66:"Natives attacked! At least no one was eaten!",68:"No discoveries. Prepare to leave... What?! Some sailors deserted!",69:"They found nothing... Wait! Sailors are missing. Desertion!",70:"They found nothing. Let's leave... Wait! Some sailors deserted!",72:"They found nothing. Let's go... Wait! Sailors deserted!"},
24: {
0:"They found nothing. Let's leave... What?! Some sailors deserted!",1:"Beasts attacked our team!",2:"Beasts attacked our team!",3:"Admiral! Beasts attacked our team!",4:"Beasts attacked our team!",5:"Admiral! Beasts attacked our team!",8:"Beast attack spread disease!",9:"Disease everywhere! Our attacked team spread it.",10:"Our team sank into quicksand!",11:"Our team seems trapped in quicksand!",12:"Admiral! Our team's in quicksand!",13:"Our team's in quicksand!",14:"Our team's in quicksand!",15:"Quicksand trapped our team!",17:"Admiral! They found a hot spring!",18:"The expedition found a hot spring!",19:"Wow! They found a hot spring!",20:"They found a hot spring!",22:"Admiral, hot springs cure fatigue.",23:"No more fatigue! Hot springs feel great.",24:"Hot springs feel wonderful. All fatigue is gone.",25:"Ahh, this feels good. Hot springs cure travel fatigue.",26:"Tastes bad, but feels great!",29:"They found an oasis! Hurry!",30:"They found an oasis! Let's hurry!",31:"An oasis here... A gift from heaven.",33:"An oasis here! We're lucky.",34:"An oasis here! Admiral, we're lucky!",36:"The oasis vanished... Admiral, it was a mirage.",37:"The oasis vanished... Just a mirage.",38:"The oasis vanished... Just a mirage.",39:"The oasis vanished... Just a mirage.",40:"The oasis vanished. Damn, a mirage!",41:"The oasis vanished. Admiral, it was a mirage.",42:"What a shame... The oasis vanished.",43:"Our team is trapped in a swamp!",44:"Our team seems trapped in a swamp!",45:"Our team got trapped in a swamp!",47:"The team found something!",48:"The team found something!",49:"The team found something!",50:"The team found something!",51:"The team found something!",52:"The team found something!",53:"The team found something!",54:"The team found something!",55:"Admiral! %s's proof: %s!",56:"Admiral! %s's proof is %s!",57:"Admiral! %s's proof is %s!",59:"Admiral! %s's proof is %s!",61:"A shark bit off %s!",62:"A shark bit %s off!",63:"A shark bit off %s!",65:"A shark bit off %s! What a glutton!",66:"The white whale has sunk countless ships. Let's kill it!",67:"The white whale has sunk countless ships. Let's kill it!"},
}

# These three variants share a 39-byte allocation. Keep the wording short enough
# to avoid an automatic one-word final line in the progressive renderer.
ENGLISH[22].update({
    14: "We won! Enemy flagship fled!",
    15: "We won! Enemy flagship fled!",
    17: "We won! Enemy flagship fled!",
})
ENGLISH[23][65] = "Natives attacked! How awful!"
ENGLISH[24][23] = "Hot springs erased all fatigue!"


PACKED = {
22: {
0:["I cannot waste more lives. We have no choice... We surrender.","It's hopeless... Admiral, this ship surrenders."],
9:["You're trying to attack this city? I won't allow it!","You bastards mean to attack this city? Then expect no mercy!"],
12:["You dare attack this city? We'll crush you!","The enemy flagship fled. Victory is ours!"],
33:["Enemy ship %s sunk!","Admiral! We sank enemy ship %s!","Enemy ship %s sunk!"],
34:["Yes! Enemy ship %s sunk!","We sank enemy ship %s!"],
62:["Admiral, enemy ship %s raised a white flag! It seems to surrender!","Admiral, enemy ship %s surrendered!"],
70:["Our ram hit the enemy ship!","Our ram hit the enemy ship!","Our ram struck the enemy ship broadside!"],
71:["Our ram hit the enemy ship!","Our ram hit the enemy ship!","Our ram hit the enemy ship!","Admiral, I'm leaving the battle!","Admiral, I'm withdrawing!"],
72:["Admiral, I'm leaving the battle!","Admiral, I'm withdrawing!"],
86:["Admiral, victory is ours!","Admiral, we won!"],
91:["Admiral, victory is ours!","Our flagship is down. We lost!"],
99:["I'll show you the power of drink!","A battle!","Battle?"],
100:["A battle! I'll do my best!","A battle? My turn!","My turn!"],
101:["A battle!","My turn!","A battle! Count on me!"],
},
23: {
0:["Leave it to me!","I'll do my best!","How exciting!"],1:["My turn! I'll do it!","I'm raring to go!"],4:["Whoa! What's happening?","What happened?","Aaaah!"],8:["What, what, what?!","W-what is happening?","Damn, I'm wounded!","Ugh... I'm hurt."],9:["Ow, I'm bleeding...","Ouch... I messed up..."],10:["Ugh, I'm hurt...","Whoa, I'm bleeding!"],11:["...I've been wounded.","%s's flagship was destroyed. We lost!","%s's flagship was sunk. We lost!","%s's flagship fell. We lost!"],12:["%s's flagship fell. We lost!","%s's flagship fell. We lost!"],14:["%s's flagship fell. We lost!","%s's flagship fell. We lost!","We defeated %s!"],20:["...Hm?","What? Ah!","Hey! Stop slacking!"],29:["What?! You declare war on me? Reckless fools! Become sea foam!","W-what?! Stop! Did I do something wrong?"],56:["Friendly natives will welcome us. Admiral, let's visit!","Kind natives will welcome us. Let's go!"],57:["Friendly natives will welcome us. Admiral, let's go!","Friendly natives will welcome us. Admiral, let's go now!"],60:["The natives shared food and water.","The natives shared food and water."],61:["The natives shared food and water.","Disaster! Natives attacked the expedition!"],67:["Natives attacked the expedition!","The expedition found nothing.","Admiral! Some sailors deserted!"],71:["The expedition found nothing. Prepare to leave... Admiral! Some sailors fled!","The expedition found nothing. Prepare to leave... Admiral! Some sailors deserted!"],
},
24: {
6:["The expedition was attacked by beasts!","Admiral, disease is spreading through the ship! The attacked expedition carried it back!"],7:["Admiral, disease is everywhere! The attacked expedition carried it back!","Disease has spread through the ship! The attacked expedition carried it back!"],16:["The expedition found a hot spring!","Admiral, the expedition seems to have found a hot spring!"],21:["The expedition found a hot spring!","Admiral, it feels wonderful. Hot springs cure travel fatigue."],27:["The expedition found an oasis! Let's visit!","The expedition found an oasis! Let's hurry!"],28:["Admiral! The expedition found an oasis! Let's hurry!","The expedition found an oasis! Let's go!"],32:["An oasis here was unexpected. Thank goodness.","An oasis here! We must be lucky."],35:["I never expected an oasis here. I feel renewed.","An oasis here! I'm so moved!"],46:["Admiral, disaster! The expedition is trapped in a bottomless swamp!","Admiral, bad news! The expedition is trapped in a bottomless swamp!","Disaster! The expedition is trapped in a bottomless swamp!","Disaster! The expedition is stuck in a bottomless swamp!"],58:["Admiral, the expedition found this! It is %s's proof of supremacy: %s!","Admiral, they found %s's proof of supremacy: %s!"],60:["Admiral, they found %s's proof of supremacy: %s!","Admiral, the expedition found this. It seems to be %s's proof of supremacy: %s!"],64:["Admiral, disaster! A shark bit off %s!","A shark bit off %s!"],
},
}

PADDING = {22:{102},23:set(),24:{68}}


def context(block: int, index: int) -> str:
    if block == 22:
        return "A shared naval battle voice reports surrender, ship status, attack confirmation, victory, or defeat."
    if block == 23:
        return "A shared battle or expedition voice reacts to combat, discovery, natives, or desertion."
    return "A shared expedition voice reports hazards, springs, oases, discoveries, sharks, or the white whale."


def materialize(block: int, clean_rows: dict[int, dict], base_rows: dict[int, object]) -> None:
    singles, packed, padding = set(ENGLISH[block]), set(PACKED[block]), PADDING[block]
    expected = set(range(len(clean_rows)))
    if singles & packed or singles & padding or packed & padding or singles | packed | padding != expected:
        raise ValueError(f"block {block}: classification does not cover every record exactly once")
    audit, safe, blocked = [], [], []
    for i in range(len(clean_rows)):
        clean, base = clean_rows[i], base_rows[i]
        if len(base.raw_bytes) != int(clean["source_length"]):
            raise ValueError(f"block {block} record {i}: allocation mismatch")
        rid = f"DK4_MES_B{block:02d}_R{i:04d}"
        drafts = PACKED[block].get(i)
        english = ENGLISH[block].get(i)
        classification = "padding-only" if i in padding else "packed-multiple-entry" if drafts else "single-message"
        meaning = "Padding-only empty record." if i in padding else " / ".join(drafts) if drafts else english
        is_safe = i in singles
        audit.append({"id":rid,"block_index":block,"segment_index":i,"source_offset":clean["source_offset"],"source_length":clean["source_length"],"clean_source_hex":clean["source_hex"],"accepted_source_hex":base.raw_bytes.hex().upper(),"japanese_markup":clean["markup"],"accepted_markup_for_structure_only":base.text,"accepted_differs_from_clean":base.raw_bytes.hex().upper()!=clean["source_hex"],"classification":classification,"source_meaning":meaning,"safe_to_replace":is_safe,"safety_reason":"One independently addressable Japanese message selected for guarded fixed-dialogue QA." if is_safe else "Padding is not dialogue." if i in padding else "Multiple adjacent messages appear without NUL delimiters; their interior entry offsets are unproven."})
        rec={"id":rid,"speaker":"Multiple shared voices" if drafts else "Shared battle or expedition voice","context":context(block,i),"source_meaning":meaning}
        if is_safe:
            rec.update({"english":english+"{PAD}","localization_note":"Uses concise, idiomatic American English while preserving the source event, tone, facts, and runtime substitutions.","review":{g:True for g in ("source","context","localization","naturalness","formatting")}}); safe.append(rec)
        else:
            rec.update({"source_length":clean["source_length"],"japanese_markup":clean["markup"],"draft_messages":drafts or [],"blocker":"Padding-only record is intentionally preserved." if i in padding else "Multiple concatenated messages have unproven interior entry offsets.","review":{"source":True,"context":True,"localization":True,"naturalness":True,"formatting":False}}); blocked.append(rec)
    stem=f"common_natural_v2_b{block:02d}"
    (ROOT/f"work/analysis/common_b{block:02d}_entry_audit.json").write_text(json.dumps({"format":"dk4-common-entry-safety-audit-v1","file_path":"/COMMON/MESFILE.DK4","block_index":block,"source":"work/analysis/common_clean_inventory.json generated from work/clean.nds","accepted_source_file_sha256":SOURCE_HASH,"classification_counts":{"single-message":len(singles),"packed-multiple-entry":len(packed),"padding-only":len(padding),"likely-identifier":0},"replacement_counts":{"safe_to_replace":len(safe),"blocked":len(blocked)},"records":audit},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (ROOT/f"translations/{stem}_safe.json").write_text(json.dumps({"format":"dk4-ilnk-translation-batch-v1","file_path":"/COMMON/MESFILE.DK4","source_file_sha256":SOURCE_HASH,"encoder":"dialogue-fixed-v1","dialogue_profile":"shared-pair-live","translation_policy":"natural-dialogue-v2","target_locale":"en-US","review_gates":["source","context","localization","naturalness","formatting"],"scope":f"Independently addressable Japanese records in shared MESFILE block {block}","blocked_packed_records":[f"DK4_MES_B{block:02d}_R{i:04d}" for i in sorted(packed)],"blocked_records":[r["id"] for r in blocked],"records":safe},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (ROOT/f"translations/{stem}_blocked.json").write_text(json.dumps({"format":"dk4-blocked-editorial-inventory-v1","file_path":"/COMMON/MESFILE.DK4","source_file_sha256":SOURCE_HASH,"block_index":block,"buildable":False,"records":blocked},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"block {block}: audit={len(audit)} safe={len(safe)} blocked={len(blocked)}")


def main() -> None:
    inventory=json.loads(INVENTORY.read_text(encoding="utf-8"))
    mes=NdsImage.open(BASE_ROM).read_file("/COMMON/MESFILE.DK4")
    if sha256(mes).hexdigest()!=SOURCE_HASH: raise ValueError("accepted baseline MESFILE hash mismatch")
    all_base=list(iter_mesfile_records(mes,include_non_japanese=True))
    for block in (22,23,24):
        clean={int(r["segment_index"]):r for r in inventory["records"] if int(r["block_index"])==block}
        base={r.segment_index:r for r in all_base if r.block_index==block}
        if set(clean)!=set(base): raise ValueError(f"block {block}: clean and accepted indices differ")
        materialize(block,clean,base)


if __name__=="__main__": main()
