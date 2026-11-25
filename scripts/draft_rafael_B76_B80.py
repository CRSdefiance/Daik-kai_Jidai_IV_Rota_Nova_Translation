"""Source-first Mediterranean alternatives with the actual loss and Estado meaning."""
from pathlib import Path
from scripts.seal_source_drafts_v1 import seal

ROOT = Path('work/analysis/Rafael_B61_B80_clean_20261104')
DRAFTS = {
76: [
"Oh! Admiral Hayreddin!",
"...You've grown, {MACRO:FI}. The Ottoman Pasha's forces are extraordinarily strong, but you might...",
"Y-yes! (...No, wait!) Of course we can!",
"If you manage to defeat Pasha's forces, go to Alexandria and see the priest.",
"The priest in Alexandria...? All right. I'll remember that.",
"Whatever you do, don't let your guard down.",
"You bet! And thanks, Hayreddin!",
"Heh... Farewell, then.",
"Goodbye... Admiral Hayreddin!",
],
77: [
"All right! We've finally made {MACRO:FO} the greatest power in the Mediterranean!",
"We did take a nasty beating when we fought Valdes head-on... But a win's a win! Hold your head high!",
"You're right. Winning naval battles isn't everything! Now, let's take control of the overseas trading network!",
],
78: [
"Now we're the strongest power in the Mediterranean! Even Spain can't ignore {MACRO:FO} and our support for restoring the Portuguese royal house!",
"Y-yes. I hope you're right...",
"You've proved you're the master of the seas, in name and deed! Show some pride!",
"Y-yes. You're right. Thank you, Clau!",
"You're our admiral, after all! Come on, we're almost there! Give it your all!",
"All right! Let's go conquer the world's seas!",
"Yeeeaah!",
],
79: [
"Mr. {MACRO:FA}, you've done it! You've truly won supremacy in the Mediterranean. Please, accept this.",
"Whew... That took a long time.",
"This must be another map to a Proof of Conquest. If I remember correctly, the Mediterranean treasure is some kind of crown...",
"All right, that's what we've got to find. Let's go!",
"...? But this pattern on the cloth doesn't look anything like a map...",
],
80: [
"Whew! Finally found you! You're Mr. {MACRO:FA}, right? The king of Portugal's calling for you!",
"Hey! Mr. {MACRO:FA}'s back! The king wants to see you!",
],
}
NOTES = {
(76,12): 'Preserve source Ottoman-Pasha identification and extraordinary strength; keep the assessment of Rafael group unfinished, not a guaranteed victory.',
(76,15): 'Keep the nervous agreement, internal self-correction and more assured reply without inventing a rank or stated reason for the change.',
(76,20): 'The Alexandria priest contact remains conditional on defeating Pasha forces; do not imply that it has already happened.',
(76,31): 'Use Hayreddin as the familiar address instead of translating older-man address into Grandpa or invented kinship.',
(77,10): 'Preserve the painful direct defeat by Valdes despite overall Mediterranean supremacy. Do not turn the losing battle into a win.',
(77,13): 'The exact source-term checkpoint defines エシュタード as Portuguese overseas trading sphere/network, including B152R50 explicit 交易圏 and B164/B166 usages. Overseas trading network conveys the objective without inventing a city, country, sea route mechanic or royal rank.',
(78,5): 'Preserve explicit support for restoration of the Portuguese royal house, not a new personal kingship for Rafael.',
(78,13): 'Master of the seas is Claudio enthusiastic praise and established dominance, not a formal coronation.',
(79,22): 'Keep both the confident map inference and uncertain recollection of an unnamed crown; do not supply the item identity.',
(80,13): 'Keep the worker identification question and king of Portugal summons without inventing a messenger rank.',
(80,19): 'Keep the separate homecoming alternative; respectful Mr. is not a noble title.',
}

if __name__ == '__main__':
    seal(ROOT/'source_identity_event_andterm_checkpoint_v1.json',
         ROOT/'B76_B80_26_logical_English_drafts_v1.json', DRAFTS, NOTES, Path(__file__))
