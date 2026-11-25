# Sound Setup Play and Stop

Sound Setup now shows **Stop** while a BGM track is playing and retains **Play** for starting a track or previewing a sound effect. The four text bytes fit the original eight-byte slot. Ordinary title-menu replays checked both playback states, changing the track, the SFX preview action and the return to Options and title. The English label also removes three leftover Japanese glyph pixels that persisted after leaving Stop. [Exact review and captures](../releases/all_routes_editorial_20261123_sound_play_stop_candidate/verification/registered_review.json)

The candidate's startup, 24 protected name getter checks, 17 repository tests and exact clean-input patch reconstruction passed. Audio output and handheld display were outside this check. [Testing build and patch](../releases/all_routes_editorial_20261123_sound_play_stop_candidate/README.md)
