# Fleet Info Missionary destination

Fleet Info now shows **To: Missionary** for the separate missionary destination object. The getter uses the existing resident English string. Its original Japanese source and the crew-role selector are recorded separately. [Exact source, current and installed references](../releases/all_routes_editorial_20261123_missionary_destination_candidate/verification/registered_review.json)

Offline native checks preserved all 114 town names, the no-target case and the original regional picker. A focused replay supplied slot 114 in Manuel Fleet's destination byte. The complete revised label fit the original detail and Report screens, and the list returned with the same pixels. This verifies the display with a supplied input. Ordinary reachability of slot 114 remains unverified. [Focused emulator evidence](../releases/all_routes_editorial_20261123_missionary_destination_candidate/verification/missionary_destination_1_20261123.png)

The cumulative release passed 450 checks, its own startup and 17 focused regressions. The clean-input patch reconstructs it byte for byte. [Testing build and patch](../releases/all_routes_editorial_20261123_missionary_destination_candidate/README.md)

The sole Drive ROM matched the registered build by streamed SHA-256. Cleanup removed the duplicate reconstruction and three disposable save copies after checking their hashes against the retained files. [Latest testing build](https://drive.google.com/file/d/1vM8IXRtSIMvFR4F-TR3oPLtcuhFobGwa/view?usp=drivesdk) · [Drive receipt](../translations/editorial_checkpoints/shared_display_20261123/missionary_destination_drive_20261123.json) · [Cleanup receipt](../translations/editorial_checkpoints/shared_display_20261123/missionary_destination_cleanup_20261123.json)
