from __future__ import annotations

import json
from hashlib import sha256
from pathlib import Path

from dk4tool.rom.nds import NdsImage
from dk4tool.script.mesfile import iter_mesfile_records

ROOT = Path(__file__).resolve().parents[1]
INVENTORY_PATH = ROOT / "work/analysis/common_clean_inventory.json"
BASE_ROM = ROOT / "out/raphael_natural_v2_pre_common_accepted_rollback.nds"
SOURCE_HASH = "ecb0806b6f36f9bf4164ae46084fbbc12d4122af66b6a8920814197463f19491"


B25 = {
0:"That's the legendary white whale! Many ships have fallen prey to it. Admiral, let's take it down!",2:"There's the legendary white whale! Countless ships have fallen prey to it. Shall we destroy it?",4:"Admiral, what are you doing? Attack now!",5:"Admiral, what's wrong? We have to attack!",6:"Admiral, what's wrong? Please attack now!",7:"Admiral! What's the holdup? Let's attack!",8:"Admiral, stop dawdling and attack!",9:"Admiral, don't just sit there! Attack!",10:"Admiral, what's wrong? Attack now!",13:"The white whale got away... Huh? Something's shining where it dove!",14:"The white whale escaped... Wait! Something's shining where it dove!",15:"Aw, it got away... Huh? Something's glowing where it dove!",16:"Maybe it wants to befriend us. Perhaps it's gentle after all.",17:"Maybe the white whale is actually a gentle creature.",18:"Maybe it's gentle, and people just call it a monster.",19:"Maybe the white whale doesn't really want to fight humans.",20:"Maybe the white whale never wanted to fight humans at all.",21:"Perhaps the white whale is gentler than we thought.",22:"Maybe it just wants to play with us. Perhaps it's gentle.",23:"A pod of dolphins! May we record this in the ship's log?",25:"Admiral, look at that pod of dolphins! May we add it to the ship's log?",26:"Whoa, a pod of dolphins! Amazing! Can we put it in the ship's log?",27:"What a magnificent pod of dolphins! May we record it in the ship's log?",28:"Wow! So many dolphins! Can we put this in the ship's log, Admiral?",29:"Yes, record it.",31:"The dolphins have gone. That was soothing.",32:"The dolphins have gone. What a heartwarming sight.",33:"The dolphins left... That was nice.",34:"The dolphins are gone. A peaceful moment is nice now and then.",35:"The dolphins are gone. That was peaceful.",36:"The dolphins have left. What a peaceful feeling.",37:"Bye, dolphins... That was so relaxing.",38:"The dolphins have departed. A welcome moment of rest.",39:"My head... lt feels like I'm losing my mind!",40:"What is that sound? My head feels like it's splitting!",41:"Aah! My head... lt feels like I'm losing my mind!",42:"Help! My head... lt feels like I'm losing my mind!",43:"Aah! What a weird sound!",44:"Aah! My mind is slipping!",46:"The bubbles are swallowing the ship!",49:"Aah! Lightning!",50:"Damn! We got caught in it!",51:"This is bad! We're caught in the tornado!",52:"Aah! The ship's caught in the tornado!",53:"This is bad! The ship's being dragged in!",54:"Oh no! The tornado's swallowing us!",55:"Aah! We're caught in the whirlpool!",58:"We're hitting a reef!",59:"This is bad! A reef!",61:"Aah! A reef!",62:"No! We can't turn in time!",63:"It's no use! We can't turn in time!",64:"No! We can't turn in time!",65:"It's no use! We cannot turn in time!",66:"Oh no! We can't steer!",68:"Yes, that's right.",69:"Yes, exactly.",70:"Yes.",71:"Yes."
}
B25_PACKED = {
1:["That's the legendary white whale. Many ships have been attacked. Admiral, let's destroy it!","That's the legendary white whale! It's attacked countless ships. Shall we take it down?"],
3:["Wow, the famous white whale! It has attacked so many ships. Let's take it down!","That's the legendary white whale! Countless ships have fallen prey to it. Shall we destroy it ourselves?"],
11:["The white whale is escaping... Huh? Something's shining where it dove!","The whale's getting away... What's that? Something is shining where it dove!"],
12:["Aw, the whale got away... Wait! Something's shining over there!","It got away... Huh? Something's shining where it dove!"],
24:["Admiral, a pod of dolphins! May we record this in the ship's log?","Wow, a pod of dolphins! Can we add it to the ship's log?"],
30:["Yes, you may.","Yes. Record it.","Yes, please do."],
45:["The bubbles are swallowing the ship!","These bubbles are swallowing the ship!","The ship is being swallowed by bubbles!","The bubbles are swallowing the ship!","The bubbles are engulfing the ship!"],
47:["So cold... Brrr...","It's cold!"],48:["Aah, lightning!","Lightning!","L-lightning!","L-lightning!"],
56:["Oh no! We're caught in the whirlpool!","This is bad! The whirlpool has us!"],
57:["The whirlpool's eating the ship!","Damn, a reef!"],60:["Oh no! A reef!","This is bad! A reef!"],
67:["No! We can't turn in time!","That was a tough one..."]
}

B26 = {
1:"This shark is so small. Killing it would be cruel.",2:"Even if it is a shark, l can't bear to take such a tiny life.",5:"Fine, but don't blame me for what happens later...",6:"Considering the future, this is best. Mercy has no place here.",8:"Call it intuition, but sharks might be edible. This could become a new trade good.",9:"Why don't we keep this one and find out?",10:"What are you saying? You have no idea how dangerous sharks are!",11:"Captured sharks should be killed! Admiral, forget this and kill it now!",13:"Aw, there goes the makings of a feast. What a waste.",14:"The wind has begun to blow.",15:"The wind, at last...",19:"Maybe it only fights because humans branded it a monster. l almost feel sorry for it.",21:"Maybe it only fights because we call it a monster. l almost feel sorry for it.",22:"Humans may have branded it a monster and forced it to fight. Poor creature.",24:"Admiral, look over there! Something is shining!",25:"Admiral, look! Something's shining over there!",26:"Admiral, look over there! Something's shining!",27:"Admiral, look! Something's glittering over there!",28:"Admiral! Something is shining over there!",29:"Look over there... Something's sparkling!",30:"Admiral, the extra armor protected us from the reef!",31:"Admiral, the extra armor prevented any damage.",32:"Admiral, the extra armor kept the ship unscathed!",33:"Admiral, the extra armor protected us from the reef!",34:"The extra armor protected us from the reef!",35:"The extra armor kept the ship safe! Always be prepared!",36:"With the extra armor, that reef was nothing!",37:"Admiral, the extra armor prevented any reef damage!",38:"Admiral, the ram shattered the ice. No damage!",39:"Admiral, the ram smashed the ice. No damage!",40:"Lucky! The ram smashed right through the ice!",41:"Admiral, the ram shattered the ice! What a relief.",44:"Admiral, that map was telling the truth!",45:"Admiral, what the map said was true!",46:"We're lucky to have found something this amazing!",47:"This looks valuable. Was it worth the price of the map?",48:"This is incredible! Buy me a good meal later!",49:"So this is the hidden treasure. What a time to be alive!",51:"Admiral, if you take that, l cannot do my job.",53:"Admiral, if you take that, l can't do my job.",54:"If you take that, l cannot do my job.",55:"Admiral, if you take that, l can't work!",57:"We don't need it now, but we gave %s to the sailors.",60:"God, please calm your anger!",61:"God, please be calm!",62:"God, please quell your anger!",63:"God, please don't be angry!",64:"The cat got rid of the rats."
}
B26_PACKED = {
0:["Admiral, what should we do with it?","Even if sharks are monsters, killing one this small feels wrong.","Even a shark this small is hard to kill."],
3:["You want to release it? Are you mad? Think what happens when it grows!","What? Are you serious?","Yes. l want to see what happens."],
4:["Yes, I'm serious.","Yes, though we don't know what will happen..."],7:["Hey, got a minute?","What is it?","What?","What is it?"],
12:["That's more like it!","This will be fun. l can't wait!"],16:["The wind's picking up!","The wind's rising. What a relief."],
17:["The wind's picking up!","The wind has begun to blow!","Wind! We did it! It's picking up!"],
18:["The wind has begun to blow.","Perhaps foolish humans branded it a monster and forced it to fight."],
20:["Maybe it's a creature deserving pity.","Maybe humans branded it a monster and forced it to fight. Poor thing."],
23:["Maybe it only fights because people call it a monster. Poor thing.","Admiral, look! Something is shining over there!"],
42:["The ram smashed the ice!","The ram destroyed the ice. The ship is safe!"],43:["The ram smashed the ice!","Admiral, the ram broke the ice, so we took no damage!"],
50:["Hooray! A feast tonight!","Such treasure... This is all thanks to you, Admiral."],
56:["We don't seem to need it now.","We don't need to use it now, do we?","We probably don't need it now."],
58:["We gave %s to the sailors.","We gave %s to the sailors.","Nobody knows how to use it.","How do we use it? Nobody seems to know."],
59:["What is that? Nobody knows how to use it.","How do we use it? Nobody seems to know."],
65:["The cat got rid of the rats.","We had the cat kill the rats."]
}
B26_CONTROL={52:["Admiral, if you take that, {MACRO:I}C can't do my job."]}

B27 = {
0:"The cat got rid of the rats.",1:"The ship won't move after dismissing every sailor!",2:"Admiral! We can't sail after dismissing every sailor!",4:"Who will sail the ship if you dismiss everyone? l can't do it alone!",5:"Wait... l can't work without this.",7:"l can't work without this.",8:"We found %s's fleet! Moving to attack!",10:"%s's fleet is attacking us!",11:"%s's fleet is attacking us!",12:"%s's fleet is attacking!",13:"We defeated %s %s's fleet! Victory is ours!",14:"We defeated %s %s's fleet. Victory is ours!",16:"We defeated %s %s's fleet! We won!",18:"%s %s's fleet has fled.",19:"%s %s's fleet ran away!",20:"%s %s's fleet has fled!",21:"%s %s's fleet ran away!",22:"We were defeated by %s %s's fleet...",25:"%s %s's fleet was stronger than expected, so we retreated...",27:"%s %s's fleet was very strong, so we retreated...",28:"%s %s's fleet was tougher than expected, so we retreated...",29:"%s %s's fleet was stronger than expected, so we retreated...",31:"Sorry. We suffered a loss of %s gold.",34:"We earned %s gold.",35:"We earned %s gold.",37:"We don't have enough gold to cover the loss. We'll add it to next month's expenses.",38:"We lack the gold to cover the loss, so we'll carry it into next month's expenses.",39:"We can't cover the loss. We'll add it to next month's expenses.",40:"%s has surrendered!",41:"We forced %s to surrender!",42:"%s has surrendered.",43:"%s surrendered!",44:"%s has surrendered!",45:"%s opened fire on us!",46:"%s opened fire on us!",47:"%s opened fire on us!",48:"%s is firing cannons at us!",49:"Enemy %s sunk!",50:"Enemy %s sunk.",51:"We sank the enemy %s!",52:"%s was sunk...",53:"%s sank...",54:"Enemy %s captured!",55:"Enemy %s captured.",56:"We captured the enemy %s!",57:"%s was captured...",58:"%s got captured...",59:"We seized %s gold in spoils!",60:"We acquired %s gold in spoils.",61:"We seized %s gold in spoils!",62:"We seized %s gold in spoils!",63:"We took %s gold in spoils!",64:"We took %s gold in spoils!",65:"We took %s gold in spoils!",66:"We seized %s gold in spoils!",67:"Beginning the attack on %s!",68:"Beginning the attack on %s.",69:"We're attacking %s!",70:"We will attack %s.",71:"We're launching an attack on %s!",72:"We'll attack %s!",73:"We're attacking %s now!",76:"We obtained information on pirate %s.",77:"We obtained information on pirate %s.",78:"We obtained information on pirate %s.",79:"We obtained information on pirate %s.",81:"There! Pirate %s is at %s! They're attacking!",82:"Aha! Pirate %s is at %s! They're attacking!"
}
B27_PACKED={
3:["Admiral! We can't sail after dismissing every sailor!","Hold on! The ship won't move if you dismiss every sailor!"],
6:["We can't work without this...","Wait! We can't work without this."],
9:["We found %s's fleet! Moving to attack!","We found %s's fleet! Attack!","We found %s's fleet! Let's attack!","%s's fleet is attacking us!"],
17:["We defeated %s %s's fleet! We won!","We defeated %s %s's fleet! Victory!","We beat %s %s's fleet! We won!","%s %s's fleet has fled!"],
24:["We were defeated by %s %s's fleet...","%s %s's fleet defeated us...","We lost to %s %s's fleet...","%s %s's fleet beat us..."],
30:["%s %s's fleet was tougher than expected, so we fled...","We apologize. We lost %s gold.","Sorry. We lost %s gold."],
32:["Sorry. We lost %s gold.","Forgive us. We lost %s gold."],33:["Sorry. We lost %s gold.","We earned %s gold."],
36:["We made %s gold!","We lack the gold to cover the loss, so we'll add it to next month's expenses.","We can't cover the loss, so we'll add it to next month's expenses."],
74:["Beginning the attack on %s.","At %s, we found pirate %s!","At %s, we found pirate %s!","At %s, we found pirate %s!"],
75:["At %s, we found pirate %s!","At %s, pirate %s!","At %s, we found pirate %s!"],
80:["Ho ho ho! We obtained information on pirate %s.","We obtained information on pirate %s!"]
}
B27_CONTROL={15:["We defeated %s %s's fleet! {MACRO:I}C won!"],23:["{MACRO:I}C was defeated by %s %s's fleet..."],26:["%s %s's fleet was tougher than expected, so {MACRO:I}C's fleet retreated..."]}

# Fixed-allocation revisions found by exhaustive exact-font QA.  Keeping these as
# explicit overrides makes the first editorial draft above easy to compare with the
# final buildable wording without hiding any structural classification.
B25.update({
0:"The legendary white whale! Many ships lost. Admiral, let's kill it!",2:"The legendary white whale! Countless ships lost. Shall we kill it?",4:"Admiral, attack now!",5:"Admiral, what's wrong? Attack!",6:"Admiral, please attack!",7:"Admiral! Stop stalling! Attack!",9:"Admiral, hurry and attack!",17:"Maybe the white whale is gentle.",19:"Maybe the white whale wants peace.",21:"Perhaps the whale is gentle.",22:"Maybe it wants to play. Perhaps the whale is gentle.",23:"Dolphins! May we note them in the ship's log?",25:"Admiral, dolphins! May we add them to the log?",32:"The dolphins left. What a lovely sight.",34:"The dolphins left. A peaceful moment feels good.",36:"The dolphins left. That was peaceful.",38:"The dolphins left. A welcome rest.",39:"My head... Going mad!",40:"What is that sound? My head is splitting!",41:"Aah! My head... Going mad!",42:"Help! My head... Going mad!",43:"Aah! Strange sound!",46:"Bubbles engulf the ship!",51:"No! The tornado caught us!",52:"Aah! The tornado caught the ship!",53:"No! The ship's being dragged in!",55:"The whirlpool caught us!",63:"No! We can't turn in time!",65:"No! We cannot turn in time!",68:"Yes."
})
B26.update({
2:"Even for a shark, taking such a tiny life feels cruel.",5:"All right, but don't blame me later.",6:"This is best for the future. No mercy.",9:"Why don't we keep it and see?",10:"You fool! Sharks are dangerous!",11:"Admiral, kill the shark now!",13:"Our feast is gone. What a waste.",14:"The wind rises.",15:"Wind, at last.",19:"Maybe humans forced it to fight by calling it a monster. Poor thing.",21:"Maybe it fights because we call it a monster. Poor thing.",22:"Humans call it a monster and force it to fight. Poor thing.",24:"Admiral, look! Something's shining!",25:"Admiral, look! Something's shining!",26:"Admiral, look! Something's shining!",28:"Admiral! Something is shining!",29:"Look... Something's sparkling!",30:"Admiral, extra armor stopped reef damage!",31:"Admiral, extra armor stopped all damage.",32:"Admiral, extra armor kept us safe!",33:"Admiral, extra armor stopped reef damage!",34:"Extra armor stopped reef damage!",36:"Extra armor made that reef harmless!",39:"Admiral, the ram broke the ice. No damage!",40:"Lucky! The ram broke the ice!",41:"The ram broke the ice! We're safe.",44:"Admiral, the map was true!",46:"Lucky us, finding such treasure!",48:"Amazing! Buy me a feast later!",49:"The hidden treasure! What a sight!",51:"Admiral, take that and my work is done for.",53:"Admiral, take that and my work is done.",54:"Take that and my work is done for.",55:"Admiral, take that and my work is done!",57:"We gave the sailors %s."
})
B27.update({
0:"The cat killed the rats.",1:"No sailors means the ship can't move!",2:"Admiral! No sailors means no sailing!",4:"Who'll sail if all leave? Not me alone!",5:"Wait... Can't work without this.",7:"Can't work without this.",8:"We found %s's fleet! Attack!",13:"We beat %s %s's fleet! We won!",14:"We beat %s %s's fleet. We won!",25:"%s %s's fleet was too strong. We retreated.",27:"%s %s's fleet was too strong. We retreated.",31:"Sorry. We lost %s gold.",37:"Not enough gold. Add the loss to next month's costs.",38:"Not enough gold. Add the loss to next month's costs.",50:"%s sunk!",51:"Sank enemy %s!",54:"Captured %s!",55:"Captured %s",56:"We caught %s!",71:"Attack %s!",76:"News on pirate %s.",77:"News on pirate %s.",78:"News on pirate %s.",79:"News on pirate %s."
})
B25.update({2:"Legendary white whale! Countless ships lost. Shall we kill it?",22:"Maybe it wants to play. The whale may be gentle.",23:"Dolphins! Can we note this in our ship's log?",32:"What a lovely sight. The dolphins have gone.",34:"The dolphins left. Such a peaceful moment."})
B26.update({2:"Even a tiny shark's life is hard to take.",6:"This is best for the future. Show no mercy.",21:"Humans call it a monster. Maybe it fights back. Poor thing.",30:"Extra armor saved us from the reef, Admiral!",31:"Extra armor stopped all damage, Admiral.",33:"Extra armor saved us from the reef, Admiral!",39:"The ram broke the ice, Admiral. No damage!",53:"Without that, my work is impossible.",55:"Without that, my work is impossible, Admiral!"})
B27.update({1:"Dismiss all sailors and the ship stops!",2:"Admiral! Dismiss all sailors and we stop!",4:"Dismiss all sailors? Who sails? Not me!",37:"We lack enough gold. The loss goes on next month's bill.",38:"We lack enough gold. The loss goes on next month's bill."})
B25.update({34:"The dolphins left. That felt peaceful."})
B26.update({2:"Taking such a tiny shark's life feels cruel.",6:"The future demands this. Show no mercy.",30:"Admiral, extra armor saved the ship!",31:"Admiral, extra armor stopped damage.",33:"Extra armor saved the ship, Admiral!",39:"Admiral, rammed ice. No damage!",55:"Without that, my job is impossible!"})
B27.update({1:"No sailors, no sailing!",2:"Admiral! No sailors, no sailing!",4:"Who sails with no crew? Not me!"})
B27.update({81:"There! At %s, pirate %s! They're attacking!",82:"Aha! At %s, pirate %s! They're attacking!"})
B26.update({6:"Show no mercy. The future demands it."})
B26.update({6:"No mercy. The future demands it."})


DATA={25:(73,B25,B25_PACKED,{},"A shared ocean-event voice reports wildlife, hazards, or a discovery."),26:(67,B26,B26_PACKED,B26_CONTROL,"A shared ocean-event voice discusses a shark, weather, equipment, treasure, or an item."),27:(83,B27,B27_PACKED,B27_CONTROL,"A shared naval report announces fleet, city, ship, loot, or pirate events.")}


def main():
    inv=json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))
    mes=NdsImage.open(BASE_ROM).read_file("/COMMON/MESFILE.DK4")
    if sha256(mes).hexdigest()!=SOURCE_HASH: raise ValueError("accepted baseline MESFILE hash mismatch")
    accepted={(r.block_index,r.segment_index):r for r in iter_mesfile_records(mes,include_non_japanese=True)}
    clean={(int(r["block_index"]),int(r["segment_index"])):r for r in inv["records"]}
    for block,(count,singles,packed,controls,context) in DATA.items():
        padding={count-1}
        if set(singles)|set(packed)|set(controls)|padding != set(range(count)): raise ValueError(f"block {block} classification incomplete")
        if any(a&b for a,b in ((set(singles),set(packed)),(set(singles),set(controls)),(set(packed),set(controls)))): raise ValueError("overlap")
        audit=[]; safe=[]; blocked=[]
        for i in range(count):
            c=clean[(block,i)]; a=accepted[(block,i)]; rid=f"DK4_MES_B{block:02d}_R{i:04d}"
            if len(a.raw_bytes)!=int(c["source_length"]): raise ValueError(f"{rid}: allocation mismatch")
            if i in singles: cls="single-message"; drafts=None; meaning=singles[i]; reason="One independently addressable Japanese message selected for guarded fixed-dialogue QA."
            elif i in packed: cls="packed-multiple-entry"; drafts=packed[i]; meaning=" / ".join(drafts); reason="Multiple adjacent messages appear without NUL delimiters; their interior entry offsets are unproven."
            elif i in controls: cls="accepted-source-command-ambiguous"; drafts=controls[i]; meaning=" / ".join(drafts); reason="The accepted allocation contains an ASCII command-like macro whose runtime semantics are not proven safe for replacement."
            else: cls="padding-only"; drafts=[]; meaning="Padding only."; reason="The clean allocation contains no spoken message."
            audit.append({"id":rid,"block_index":block,"segment_index":i,"source_offset":c["source_offset"],"source_length":c["source_length"],"clean_source_hex":c["source_hex"],"accepted_source_hex":a.raw_bytes.hex().upper(),"japanese_markup":c["markup"],"accepted_markup_for_structure_only":a.text,"accepted_differs_from_clean":a.raw_bytes.hex().upper()!=c["source_hex"],"classification":cls,"source_meaning":meaning,"safe_to_replace":i in singles,"safety_reason":reason})
            rec={"id":rid,"speaker":"Shared event or battle voice","context":context,"source_meaning":meaning}
            if i in singles:
                rec.update({"english":singles[i]+"{PAD}","localization_note":"Concise idiomatic American English preserving the event, intent, voice, and runtime substitutions.","review":{g:True for g in ("source","context","localization","naturalness","formatting")}}); safe.append(rec)
            else:
                rec.update({"source_length":c["source_length"],"japanese_markup":c["markup"],"draft_messages":drafts,"blocker":reason,"review":{"source":True,"context":True,"localization":True,"naturalness":True,"formatting":False}}); blocked.append(rec)
        stem=f"common_natural_v2_b{block}"
        (ROOT/f"work/analysis/common_b{block}_entry_audit.json").write_text(json.dumps({"format":"dk4-common-entry-safety-audit-v1","file_path":"/COMMON/MESFILE.DK4","block_index":block,"source":"work/analysis/common_clean_inventory.json generated from work/clean.nds","accepted_source_file_sha256":SOURCE_HASH,"classification_counts":{"single-message":len(singles),"packed-multiple-entry":len(packed),"padding-only":1,"likely-identifier":0,"accepted-source-command-ambiguous":len(controls)},"replacement_counts":{"safe_to_replace":len(singles),"blocked":len(blocked)},"records":audit},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        (ROOT/f"translations/{stem}_safe.json").write_text(json.dumps({"format":"dk4-ilnk-translation-batch-v1","file_path":"/COMMON/MESFILE.DK4","source_file_sha256":SOURCE_HASH,"encoder":"dialogue-fixed-v1","dialogue_profile":"shared-pair-live","translation_policy":"natural-dialogue-v2","target_locale":"en-US","review_gates":["source","context","localization","naturalness","formatting"],"scope":f"Independently addressable Japanese records in shared MESFILE block {block}","blocked_packed_records":[f"DK4_MES_B{block:02d}_R{i:04d}" for i in sorted(packed)],"blocked_records":[r["id"] for r in blocked],"records":safe},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        (ROOT/f"translations/{stem}_blocked.json").write_text(json.dumps({"format":"dk4-blocked-editorial-inventory-v1","file_path":"/COMMON/MESFILE.DK4","source_file_sha256":SOURCE_HASH,"block_index":block,"buildable":False,"records":blocked},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        print(f"block {block}: audit={len(audit)} safe={len(safe)} blocked={len(blocked)}")


if __name__=="__main__": main()
