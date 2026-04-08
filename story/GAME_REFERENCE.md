# THE PROMETHEUS PROTOCOL - GAME REFERENCE

**Auto-generated troubleshooting reference. Do not hand-edit.**
**To regenerate: `python tools/generate_reference.py`**

This document contains every room, item, event, NPC, and puzzle in the game.
Use it to verify content, troubleshoot bugs, trace logic flow, or find specific
references without reloading the game state.

---

## TABLE OF CONTENTS

1. [Overview & Stats](#1-overview--stats)
2. [Ship Deck Map](#2-ship-deck-map)
3. [Room Connectivity Graph](#3-room-connectivity-graph)
4. [Critical Path Walkthrough](#4-critical-path-walkthrough)
5. [All Rooms Reference](#5-all-rooms-reference)
6. [All Items Reference](#6-all-items-reference)
7. [Readable Items (Logs & Journals)](#7-readable-items-logs--journals)
8. [NPC Reference](#8-npc-reference)
9. [Dialogue Topics](#9-dialogue-topics)
10. [All Events Reference](#10-all-events-reference)
11. [Puzzle Solutions](#11-puzzle-solutions)
12. [Locked Content (Keys & Flags)](#12-locked-content-keys--flags)
13. [Flag / Knowledge Graph](#13-flag--knowledge-graph)
14. [Ending Conditions](#14-ending-conditions)
15. [Known Issues / Audit Results](#15-known-issues--audit-results)

---


## 1. Overview & Stats

- **Rooms:** 116
- **Items:** 609
  - Portable: 160
  - Readable: 78
  - Containers: 6
  - Weapons: 16
- **NPCs:** 19 (7 alive, 12 dead/system)
- **Events:** 72
- **Dialogue trees:** 7
- **Narrative:** ~40,071 words

**Decks:**
  - Deck A - Command: 11 rooms
  - Deck B - Science: 12 rooms
  - Deck C - Living: 19 rooms
  - Deck D - Medical: 13 rooms
  - Deck E - Security: 9 rooms
  - Deck F - Engineering: 11 rooms
  - Deck G - Cargo: 15 rooms
  - Deck H - AI Core: 9 rooms
  - Deck I - Cryogenics: 15 rooms
  - Deck J - Propulsion: 2 rooms

---

## 2. Ship Deck Map

```
                   ┌─────────────────────────────┐
                   │   ISV PROMETHEUS            │
                   │   ~1.2 km long              │
                   │   10 decks, stacked         │
                   └─────────────────────────────┘

  ▲ UP (Bow / Command)
  │
  │  Deck A - COMMAND ............. Bridge, Ready Room, Comms
  │  Deck B - SCIENCE ............. Main Lab, Exobio Lab, Observatory
  │  Deck C - LIVING .............. Mess Hall, Crew Cabins, Lounge
  │  Deck D - MEDICAL ............. Medical Bay, Surgery, Quarantine, Morgue
  │  Deck E - SECURITY ............ Security Office, Armory, Brig
  │  Deck F - ENGINEERING ......... Main Engineering, Reactor, Workshop
  │  Deck G - CARGO/HYDRO ......... Cargo Bays, Hydroponics (THE GARDEN)
  │  Deck H - AI CORE ............. ARIA Central, Quantum Archive, Neural Interface
  │  Deck I - CRYOGENICS .......... Cryo Bay (START), Control, Medical, Storage
  │  Deck J - PROPULSION .......... Main Engine Room (CLIMAX)
  │
  ▼ DOWN (Stern / Engines)
```

**Movement style:** Within a deck, rooms use cardinal directions (N/S/E/W).
Between decks, use UP / DOWN (stairwells, ladders, maintenance shafts).

---

## 3. Room Connectivity Graph

Every room → exit direction → destination. Locked exits are marked with [LOCKED].
Hidden exits marked with [HIDDEN]. Key/flag requirements shown in parentheses.

### Deck A - Command

```
[bridge] Bridge
    east       -> navigation_computer_room
    north      -> bridge_escape_pod [HIDDEN]
    south      -> deck_a_junction
    west       -> tactical_operations

[bridge_crew_quarters] Bridge Crew Quarters
    northwest  -> deck_a_junction

[bridge_escape_pod] Emergency Escape Pod Bay
    south      -> bridge

[captains_ready_suite] Captain's Ready Suite
    north      -> ready_room

[comms_array] Communications Array
    north      -> communications_relay
    west       -> deck_a_junction

[communications_relay] Communications Relay Hardware
    south      -> comms_array

[deck_a_junction] Deck A Command Deck
    down       -> deck_b_junction
    east       -> comms_array
    north      -> bridge [LOCKED] (flag=has_captains_key)
    southeast  -> bridge_crew_quarters
    southwest  -> life_support_central
    west       -> ready_room

[life_support_central] Life Support Central
    northeast  -> deck_a_junction

[navigation_computer_room] Navigation Computer Room
    west       -> bridge

[ready_room] Captain's Ready Room
    east       -> deck_a_junction
    south      -> captains_ready_suite

[tactical_operations] Tactical Operations Center
    east       -> bridge

```

### Deck B - Science

```
[botany_lab] Botany Research Lab
    east       -> main_lab

[chemistry_lab] Chemistry Laboratory
    north      -> main_lab

[conference_room] Mission Conference Room
    northeast  -> deck_b_junction

[deck_b_junction] Deck B Science Junction
    down       -> deck_c_junction
    east       -> exobio_lab_airlock
    north      -> observatory
    northwest  -> xenolinguistics_lab
    south      -> specimen_storage
    southwest  -> conference_room
    up         -> deck_a_junction
    west       -> main_lab

[exobio_lab] Exobiology Laboratory
    west       -> exobio_lab_airlock

[exobio_lab_airlock] Exobiology Lab Airlock
    east       -> exobio_lab [LOCKED]
    west       -> deck_b_junction

[main_lab] Main Laboratory
    east       -> deck_b_junction
    south      -> chemistry_lab
    west       -> botany_lab

[observatory] Stellar Observatory
    south      -> deck_b_junction
    up         -> telescope_observation_deck

[specimen_quarantine] Specimen Quarantine Chamber
    west       -> specimen_storage

[specimen_storage] Specimen Storage
    east       -> specimen_quarantine [LOCKED] (flag=has_biohazard_clearance)
    north      -> deck_b_junction

[telescope_observation_deck] Upper Observation Deck
    down       -> observatory

[xenolinguistics_lab] Xenolinguistics Laboratory
    southeast  -> deck_b_junction

```

### Deck C - Living

```
[arboretum] Ship's Arboretum
    northwest  -> crew_corridor

[cabin_chen] Your Cabin (Dr. Chen)
    south      -> crew_corridor

[cabin_fletcher] Ensign Fletcher's Cabin
    southwest  -> crew_corridor

[cabin_hassan] Cpl. Hassan's Cabin
    northeast  -> crew_corridor

[cabin_lin] Dr. Lin's Cabin
    north      -> crew_corridor

[cabin_okafor] Lt. Okafor's Cabin
    southeast  -> crew_corridor

[cabin_patel] Dr. Patel's Cabin
    west       -> crew_corridor

[cabin_romano] Chef Romano's Cabin
    east       -> sealed_corridor_c

[captains_quarters] Captain's Quarters
    north      -> deck_c_junction

[chapel] Multi-Faith Chapel
    west       -> observation_lounge

[crew_corridor] Crew Cabin Corridor
    east       -> cabin_patel
    north      -> cabin_chen
    northeast  -> cabin_fletcher
    northwest  -> cabin_okafor
    south      -> cabin_lin
    southeast  -> arboretum
    southwest  -> cabin_hassan
    west       -> deck_c_junction

[deck_c_junction] Deck C Crew Deck Junction
    down       -> deck_d_hub
    east       -> crew_corridor
    north      -> observation_lounge
    south      -> captains_quarters [LOCKED] (flag=has_bridge_card)
    southeast  -> sealed_corridor_c [LOCKED] (flag=has_plasma_cutter)
    southwest  -> recreation_lounge
    up         -> deck_b_junction
    west       -> mess_hall

[galley] Kitchen Galley
    south      -> mess_hall

[gymnasium] Ship's Gymnasium
    south      -> recreation_lounge

[laundry_room] Ship's Laundry
    north      -> sealed_corridor_c

[mess_hall] Mess Hall
    east       -> deck_c_junction
    north      -> galley

[observation_lounge] Observation Lounge
    east       -> chapel
    south      -> deck_c_junction

[recreation_lounge] Recreation Lounge
    north      -> gymnasium
    northeast  -> deck_c_junction

[sealed_corridor_c] Sealed Corridor Section
    northwest  -> deck_c_junction
    south      -> laundry_room
    west       -> cabin_romano

```

### Deck D - Medical

```
[deck_d_hub] Deck D Junction
    down       -> deck_e_junction
    east       -> medical_corridor
    up         -> deck_c_junction

[decontamination_shower] Decontamination Station
    west       -> quarantine_airlock

[dr_lin_office] Dr. Lin's Office
    east       -> medical_bay

[isolation_ward] Isolation Ward
    north      -> medical_bay

[medical_bay] Main Medical Bay
    east       -> medical_corridor
    north      -> surgery
    south      -> isolation_ward
    west       -> dr_lin_office

[medical_corridor] Medical Deck Corridor
    east       -> morgue
    north      -> quarantine_airlock
    south      -> deck_i_hub
    southwest  -> pharmacy [LOCKED] (flag=has_medical_badge)
    west       -> medical_bay

[morgue] Ship's Morgue
    south      -> morgue_freezer
    west       -> medical_corridor

[morgue_freezer] Morgue Freezer
    north      -> morgue

[pharmacy] Pharmacy
    northeast  -> medical_corridor

[quarantine_airlock] Quarantine Airlock
    east       -> decontamination_shower
    north      -> quarantine_bay [HIDDEN] [LOCKED] (flag=has_medical_badge)
    south      -> medical_corridor

[quarantine_bay] Quarantine Bay
    south      -> quarantine_airlock

[research_lab_med] Medical Research Laboratory
    west       -> surgery

[surgery] Surgical Theater
    east       -> research_lab_med
    south      -> medical_bay

```

### Deck E - Security

```
[armory] Ship's Armory
    east       -> evidence_locker [LOCKED] (key=red_keycard)
    north      -> armory_vault [LOCKED] (flag=has_okafor_biometrics)
    west       -> deck_e_junction

[armory_vault] Armory Vault
    south      -> armory

[brig] Ship's Brig
    north      -> deck_e_junction

[deck_e_junction] Deck E Security Hub
    down       -> engineering_junction
    east       -> armory [LOCKED]
    north      -> security_office
    south      -> brig
    up         -> deck_d_hub
    west       -> security_corridor_south [LOCKED] (flag=barricade_cleared)

[evidence_locker] Evidence Locker
    west       -> armory

[interrogation_room] Interrogation Room
    east       -> security_office

[monitoring_station] Security Monitoring Station
    west       -> security_office

[security_corridor_south] Security Corridor South
    east       -> deck_e_junction

[security_office] Security Office
    east       -> monitoring_station
    south      -> deck_e_junction
    west       -> interrogation_room

```

### Deck F - Engineering

```
[coolant_pump_room] Coolant Pump Room
    east       -> main_engineering

[engineering_break_room] Engineering Break Room
    north      -> engineering_vent_access [HIDDEN]
    south      -> yuki_hideout [LOCKED] (flag=yuki_ally)
    west       -> main_engineering

[engineering_junction] Engineering Deck Access
    down       -> deck_h_junction
    east       -> engineering_workshop
    north      -> main_engineering
    up         -> deck_e_junction
    west       -> reactor_antechamber [LOCKED] (flag=has_radiation_suit)

[engineering_vent_access] Engineering Ventilation Access
    south      -> engineering_break_room
    up         -> deck_e_junction [HIDDEN]

[engineering_workshop] Engineering Workshop
    west       -> engineering_junction

[main_engineering] Main Engineering
    down       -> plasma_conduit_junction
    east       -> engineering_break_room
    south      -> engineering_junction
    up         -> reactor_catwalk [LOCKED] (flag=tanaka_met)
    west       -> coolant_pump_room

[plasma_conduit_junction] Plasma Conduit Junction
    up         -> main_engineering

[reactor_antechamber] Reactor Antechamber
    east       -> engineering_junction
    north      -> reactor_core_interior [LOCKED] (flag=has_radiation_suit)

[reactor_catwalk] Reactor Upper Catwalk
    down       -> main_engineering

[reactor_core_interior] Reactor Core Interior
    south      -> reactor_antechamber

[yuki_hideout] Yuki's Hideout
    north      -> engineering_break_room

```

### Deck G - Cargo

```
[cargo_access] Cargo Access Tunnel
    down       -> water_processing
    east       -> deck_h_junction
    north      -> cargo_bay_main
    south      -> hydroponics_entry
    west       -> water_treatment_secondary

[cargo_bay_main] Main Cargo Bay
    down       -> lower_cargo
    east       -> cold_storage
    south      -> cargo_access
    west       -> cargo_office

[cargo_office] Cargo Master's Office
    east       -> cargo_bay_main

[chrysalis_chamber] The Chrysalis Chamber
    west       -> heart_of_garden

[cold_storage] Cold Storage Unit
    west       -> cargo_bay_main

[garden_periphery_east] Garden Periphery - East
    west       -> hydroponics_main

[garden_periphery_west] Garden Periphery - West
    east       -> hydroponics_main

[garden_root_network] Root Network
    down       -> water_processing
    up         -> hydroponics_main

[heart_of_garden] Heart of the Garden
    east       -> chrysalis_chamber
    north      -> hydroponics_main
    south      -> seed_nursery

[hydroponics_entry] Hydroponics Entrance
    north      -> cargo_access
    south      -> hydroponics_main [LOCKED] (flag=has_hazmat_suit)

[hydroponics_main] Hydroponics Bay - The Garden
    down       -> garden_root_network [HIDDEN]
    east       -> garden_periphery_east
    north      -> hydroponics_entry
    south      -> heart_of_garden [HIDDEN]
    west       -> garden_periphery_west

[lower_cargo] Lower Cargo Hold
    up         -> cargo_bay_main

[seed_nursery] The Nursery
    north      -> heart_of_garden

[water_processing] Water Processing Facility
    north      -> garden_root_network [HIDDEN]
    up         -> cargo_access

[water_treatment_secondary] Secondary Water Treatment
    east       -> cargo_access

```

### Deck H - AI Core

```
[ai_core_antechamber] AI Core Antechamber
    down       -> coolant_control_h
    east       -> neural_interface_chamber [LOCKED] (flag=aria_granted_access)
    north      -> ai_core_main [LOCKED] (flag=aria_granted_access)
    south      -> data_nexus
    west       -> deck_h_junction

[ai_core_main] ARIA Central Processing
    down       -> quantum_archive [HIDDEN]
    south      -> ai_core_antechamber

[aria_memory_vault] ARIA Memory Vault
    up         -> quantum_archive

[aria_shade_chamber] Isolated Server Room
    west       -> data_nexus

[coolant_control_h] AI Core Coolant Control
    up         -> ai_core_antechamber

[data_nexus] Data Nexus
    east       -> aria_shade_chamber [HIDDEN] [LOCKED] (flag=nexus_passage_found)
    north      -> ai_core_antechamber

[deck_h_junction] Deck H Maintenance Junction
    down       -> cryo_maintenance
    east       -> ai_core_antechamber [LOCKED]
    south      -> vent_network_i [HIDDEN]
    up         -> engineering_junction
    west       -> cargo_access

[neural_interface_chamber] Neural Interface Chamber
    west       -> ai_core_antechamber

[quantum_archive] Quantum Data Archive
    down       -> aria_memory_vault [HIDDEN]
    up         -> ai_core_main

```

### Deck I - Cryogenics

```
[cryo_bay] Cryogenics Bay - Pod 23
    east       -> cryo_corridor [LOCKED] (flag=cryo_exit_unlocked)
    north      -> cryo_control
    west       -> cryo_storage

[cryo_control] Cryogenic Control Room
    east       -> cryo_medical
    south      -> cryo_bay
    west       -> pod_monitoring_alcove [HIDDEN]

[cryo_corridor] Cryo-Deck Main Corridor
    east       -> deck_i_hub
    south      -> deck_i_storage [LOCKED] (key=deck_i_storage_key)
    west       -> cryo_bay

[cryo_maintenance] Maintenance Crawlspace
    down       -> propulsion_access [HIDDEN] [LOCKED]
    east       -> vent_network_i [HIDDEN]
    north      -> cryo_storage
    up         -> deck_h_junction [LOCKED] (flag=has_flashlight)

[cryo_medical] Emergency Medical Station
    west       -> cryo_control

[cryo_pod_12_interior] Interior of Cryo Pod 12
    south      -> cryo_storage

[cryo_recycling] Cryo-Fluid Recycling Room
    east       -> cryo_storage

[cryo_storage] Cryogenic Storage
    east       -> cryo_bay
    north      -> cryo_pod_12_interior
    south      -> cryo_maintenance [HIDDEN]
    west       -> cryo_recycling

[deck_i_hub] Deck I Elevator Hub
    east       -> emergency_shuttle_bay [LOCKED]
    north      -> medical_corridor
    south      -> emergency_airlock_i
    up         -> deck_h_junction [LOCKED]
    west       -> cryo_corridor

[deck_i_storage] Deck I Storage
    north      -> cryo_corridor

[emergency_airlock_i] Emergency Airlock - Deck I
    north      -> deck_i_hub

[emergency_shuttle_bay] Emergency Shuttle Bay - Deck I
    down       -> escape_pod_bay_lower
    west       -> deck_i_hub

[escape_pod_bay_lower] Lower Escape Pod Bay
    up         -> emergency_shuttle_bay

[pod_monitoring_alcove] Hidden Monitoring Alcove
    east       -> cryo_control

[vent_network_i] Ventilation Shaft - Deck I
    up         -> deck_h_junction [LOCKED] (flag=has_flashlight)
    west       -> cryo_maintenance

```

### Deck J - Propulsion

```
[main_engine_room] Main Engine Room
    south      -> propulsion_access

[propulsion_access] Propulsion Deck Access
    north      -> main_engine_room [LOCKED] (flag=engine_room_unlocked)
    up         -> deck_i_hub

```

---

## 4. Critical Path Walkthrough

**Minimum required steps for any ending.** The path branches in Act 4.

### Act 1: Awakening (Deck I)

```
1. START: cryo_bay (Pod 23)
   ├── TAKE: cryo_jumpsuit (auto-applies warmth event)
   ├── TAKE: cryo_release_key  [sets flag: has_cryo_key]
   ├── OPEN: personal_locker
   │   └── READ: personal_datapad_chen (backstory, immunity hint)
   ├── PUSH: green_override_button  [requires has_cryo_key]
   │   └── EVENT: cryo_exit_unlocked, opens EAST door
   └── GO EAST -> cryo_corridor

2. cryo_corridor -> deck_i_hub (east)
   └── deck_i_hub has: dead Ensign Mendes body, plasma_cutter

3. deck_i_hub -> medical_corridor (north)
   -> medical_bay -> surgery (sees Dr. Patel's body)
      └── READ: autopsy_datapad (Dr. Lin's notes)
      └── EXAMINE: dr_patel_body -> READ: patel_recording_crystal
          [MAJOR REVEAL: cure synthesis, immunity]
   -> dr_lin_office -> READ: dr_lin_journal
      [reveals safe code BUSTER]

4. Explore further (optional but recommended):
   - Observation Lounge (Vasquez's body, brown dwarf view)
   - Morgue (Reeves's body drawer)
```

### Act 2: Investigation (Decks C, B, A, E, F)

```
5. Get to Deck C via maintenance tunnels OR elevator
   - Requires: flashlight (found in cryo_maintenance)

6. deck_c_junction -> crew_corridor -> cabin_chen (YOUR OWN ROOM)
   └── READ: player_letter_to_self  [CRITICAL STORY REVEAL]
   └── READ: player_journal
   └── TAKE: small_key_nightstand

7. -> cabin_lin (Lin's tablet) or cabin_patel (data crystal)

8. Science Deck (Deck B):
   -> main_lab -> exobio_lab_airlock -> USE: biometric_scanner
   -> exobio_lab (SEES THE ARTIFACT, memory flood)
   -> observatory (find targeting analysis)

9. Command Deck (Deck A):
   -> captains_quarters -> READ: captains_recorder (final message)
   -> ready_room -> READ: readyroom_terminal (Protocol Aegis)
   -> bridge (requires Captain's authorization)

10. Security (Deck E):
    -> security_office -> READ: okafors_red_book, okafors_audio_recorder
    -> armory -> TAKE: weapons (requires red_keycard)

11. Engineering (Deck F):
    -> engineering_workshop -> TAKE: radiation_suit, hazmat_suit
    -> main_engineering -> MEET: Yuki Tanaka
        └── TALK, ASK about: engineering, cure, help
        └── Unlocks: engineering plan
```

### Act 3: Revelation (Decks H, G)

```
12. AI Core (Deck H):
    -> ai_core_antechamber (ARIA contacts you)
    -> ai_core_main -> TALK to ARIA
        └── ASK: self, what_happened, why_me, the_seed, choices, fourth_path
        └── This unlocks all three major paths + secret fourth path
    -> quantum_archive -> READ: archive_terminal (full truth)

13. Cargo & Garden (Deck G):
    -> cargo_bay_main -> lower_cargo (original Seed location)
    -> hydroponics_entry -> hydroponics_main (THE GARDEN, requires hazmat)
        └── Meets The Garden hivemind NPC
    -> heart_of_garden (final Seed nexus)
    -> water_processing (purge option for ICARUS ending)
```

### Act 4: Resolution (Deck J)

```
14. propulsion_access -> main_engine_room
    TYPE: 442127 into emergency_override_keypad
    (442 = Kepler-442, 127 = crew count)

15. USE: master_drive_control
    Depending on flags set during previous acts:
    - flag: aegis_choice     -> AEGIS ending
    - flag: icarus_choice + cure_syringe -> ICARUS ending
    - flag: prometheus_choice -> PROMETHEUS ending
    - flag: erebus_choice    -> EREBUS ending

16. ALTERNATIVE: neural_interface_chamber -> APOTHEOSIS ending
    (Requires: knows_apotheosis_path knowledge from ARIA)
```

---

## 5. All Rooms Reference

Every room with id, deck, exits, items, NPCs, and event hooks.

### Deck A - Command

#### `bridge` — Bridge

**Exits:**
- `east` → `navigation_computer_room`
- `north` → `bridge_escape_pod` _HIDDEN_
- `south` → `deck_a_junction`
- `west` → `tactical_operations`

**Items (8):** `captains_chair`, `forward_viewport`, `helm_station`, `tactical_station`, `nav_station`, `bridge_hud`, `bloody_handprint`, `spent_shell_casing_bridge`

**On first enter event:** `event_first_bridge`

_The bridge of the ISV Prometheus is a broad, arc-shaped command center facing a massive forward viewport that dominates the far wall. Through the viewport, you can see the glowing red menace of the..._

#### `bridge_crew_quarters` — Bridge Crew Quarters

**Exits:**
- `northwest` → `deck_a_junction`

**Items (6):** `webb_star_charts`, `webb_targeting_notes`, `fletcher_love_letter`, `bulkhead_carved_message`, `bridge_crew_lockers`, `duty_rotation_schedule`

**NPCs:** `corpse_webb`

_Small, efficient bunks for bridge officers on duty rotation - six beds stacked in pairs, each with a privacy curtain, a reading light, and a narrow locker. The room was designed for quick rest betw..._

#### `bridge_escape_pod` — Emergency Escape Pod Bay

**Exits:**
- `south` → `bridge`

**Items (6):** `escape_pod_controls`, `pod_diagnostic_panel`, `restraint_harnesses`, `emergency_beacon_unit`, `pod_viewport`, `escape_pod_manifest`

_Behind a concealed hatch in the bridge's forward bulkhead lies the command escape pod - a last resort reserved for bridge officers. The pod is a sleek, compact vessel designed for four passengers, ..._

#### `captains_ready_suite` — Captain's Ready Suite

**Exits:**
- `north` → `ready_room`

**Items (6):** `reeves_cot`, `reeves_son_photo`, `reeves_scotch_bottle`, `reeves_handwritten_will`, `aegis_authorization_key`, `reeves_strongbox`

_Behind the Ready Room, through a narrow door you almost missed, lies the Captain's private quarters on the command deck. Not the formal cabin on Deck C - this is where Reeves actually slept during ..._

#### `comms_array` — Communications Array

**Exits:**
- `north` → `communications_relay`
- `west` → `deck_a_junction`

**Items (6):** `fletcher_body`, `comms_main_console`, `antenna_tuner`, `transmit_key`, `duty_roster_wall`, `fletcher_pocket_items`

**NPCs:** `corpse_fletcher`

_The Communications Array is smaller than you'd expect - most of the ship's comms hardware is external, distributed across the hull. This is the operator's station. A bank of displays, an antenna tu..._

#### `communications_relay` — Communications Relay Hardware

**Exits:**
- `south` → `comms_array`

**Items (6):** `damaged_relay_unit`, `fletcher_toolkit`, `signal_conduit_severed`, `relay_diagnostic_panel`, `amplification_array`, `repair_parts_shelf`

_Behind the operator's station lies the physical heart of the ship's communications system. The relay room is a narrow, equipment-packed space dominated by massive antenna relay units that hum with ..._

#### `deck_a_junction` — Deck A Command Deck

**Exits:**
- `down` → `deck_b_junction`
- `east` → `comms_array`
- `north` → `bridge` _LOCKED, flag=has_captains_key_
- `southeast` → `bridge_crew_quarters`
- `southwest` → `life_support_central`
- `west` → `ready_room`

**Items (2):** `explorer_portraits`, `bridge_blast_door`

_The command deck is the nerve center of the Prometheus. A broad hallway lined with meeting rooms and offices leads forward toward the bridge. Portraits of historical Earth explorers - Shackleton, A..._

#### `life_support_central` — Life Support Central

**Exits:**
- `northeast` → `deck_a_junction`

**Items (6):** `atmospheric_processors`, `co2_scrubber_bank`, `environmental_control_interface`, `deck_monitoring_console`, `temperature_regulators`, `emergency_oxygen_reserves`

_The central life support control room is the reason everyone on board is still breathing - or was. Massive atmospheric processors fill the chamber, tall cylindrical units that inhale the ship's sta..._

#### `navigation_computer_room` — Navigation Computer Room

**Exits:**
- `west` → `bridge`

**Items (6):** `navigation_processing_banks`, `corrupted_trajectory_display`, `takamura_personnel_files`, `cooling_fan_arrays`, `raw_sensor_feed_terminal`, `nav_module_reset_panel`

_The navigation computer room houses the physical brain that plots the Prometheus's course through space. Banks of processing units fill floor-to-ceiling racks, their indicator lights blinking in ca..._

#### `ready_room` — Captain's Ready Room

**Exits:**
- `east` → `deck_a_junction`
- `south` → `captains_ready_suite`

**Items (4):** `readyroom_terminal`, `liquor_cabinet`, `status_monitors`, `visitor_chairs`

**On first enter event:** `event_see_protocol_aegis`

_The Captain's Ready Room is a small private office adjacent to the bridge. Unlike his personal quarters on Deck C, this space is purely functional: a desk, two chairs for visitors, a wall of status..._

#### `tactical_operations` — Tactical Operations Center

**Exits:**
- `east` → `bridge`

**Items (6):** `tactical_holographic_display`, `weapons_systems_panels`, `defensive_systems_manual`, `situation_board_timeline`, `structural_integrity_readout`, `tactical_coffee_mugs`

_A dedicated strategy room adjacent to the bridge, built for planning operations that the Prometheus was never supposed to need. The room is dominated by a holographic tactical display that fills th..._

### Deck B - Science

#### `botany_lab` — Botany Research Lab

**Exits:**
- `east` → `main_lab`

**Items (6):** `sealed_kepler_specimens`, `ayele_research_terminal`, `bioluminescent_moss_case`, `fractal_fern_sample`, `atmospheric_containment_units`, `plant_response_recorder`

_A sterile research laboratory dedicated to plant biology, distinct from the wild abundance of the Garden and the gentle refuge of the arboretum. Here, plants are specimens. Rows of sealed containme..._

#### `chemistry_lab` — Chemistry Laboratory

**Exits:**
- `north` → `main_lab`

**Items (6):** `chemical_synthesis_station`, `reagent_bottles`, `patel_formula_annotation`, `fume_hoods`, `conductive_paste_materials`, `safety_poster_annotated`

**NPCs:** `dr_mora`

_A general chemistry laboratory built for precision work. Fume hoods with glass sashes line one wall, their ventilation systems still cycling with a low hum. Reagent bottles in brown and clear glass..._

#### `conference_room` — Mission Conference Room

**Exits:**
- `northeast` → `deck_b_junction`

**Items (6):** `conference_projector`, `conference_table`, `flush_data_terminals`, `overturned_chairs`, `presentation_queue`, `conference_notepad`

**On first enter event:** `event_conference_room_memory`

_The mission briefing room is built for serious business. A long polished table seats twenty, each position fitted with a flush-mounted data terminal and a small holographic projector. High-backed c..._

#### `deck_b_junction` — Deck B Science Junction

**Exits:**
- `down` → `deck_c_junction`
- `east` → `exobio_lab_airlock`
- `north` → `observatory`
- `northwest` → `xenolinguistics_lab`
- `south` → `specimen_storage`
- `southwest` → `conference_room`
- `up` → `deck_a_junction`
- `west` → `main_lab`

**Items (3):** `voice_speaker_taped`, `directional_signs`, `clean_polymer_walls`

_The science deck is different from the rest of the ship. Cleaner. Whiter. More clinical. The walls gleam with polished polymer panels and bright LED lighting. This is where the Prometheus did its r..._

#### `exobio_lab` — Exobiology Laboratory

**Exits:**
- `west` → `exobio_lab_airlock`

**Items (6):** `the_artifact`, `containment_field`, `artifact_pedestal`, `energy_readings_display`, `exobio_notes_terminal`, `test_tube_samples`

**On first enter event:** `event_see_artifact`

_The exobiology lab is where the Prometheus mission's purpose truly lived. At the far end of the room, inside a containment field that pulses weakly, sits a pedestal. On the pedestal rests the reaso..._

#### `exobio_lab_airlock` — Exobiology Lab Airlock

**Exits:**
- `east` → `exobio_lab` _LOCKED_
- `west` → `deck_b_junction`

**Items (3):** `biometric_scanner`, `authorization_sign`, `decontamination_chamber`

**On first enter event:** `event_exobio_airlock_memory`

_A sterile white airlock separates the general science deck from the exobiology lab. Three sets of doors: the one behind you, a second just ahead for decontamination, and a third beyond that leading..._

#### `main_lab` — Main Laboratory

**Exits:**
- `east` → `deck_b_junction`
- `south` → `chemistry_lab`
- `west` → `botany_lab`

**Items (8):** `holographic_molecule`, `whiteboard_equations`, `patels_warning_note`, `petri_dishes`, `sample_vials`, `centrifuge`, `research_microscope`, `lab_datapad`

_A general-purpose research laboratory. Rows of workbenches are covered with experiments in various states of incompletion - petri dishes, sample vials, microscopes, centrifuges. A holographic displ..._

#### `observatory` — Stellar Observatory

**Exits:**
- `south` → `deck_b_junction`
- `up` → `telescope_observation_deck`

**Items (6):** `observatory_telescope`, `holographic_star_map`, `targeting_analysis`, `astronomer_workstation`, `sensor_array`, `observation_log`

_A domed observatory with a transparent ceiling looking out onto space. Massive telescopes and sensor arrays crowd the center of the room. A holographic star map dominates one wall, showing the ship..._

#### `specimen_quarantine` — Specimen Quarantine Chamber

**Exits:**
- `west` → `specimen_storage`

**Items (6):** `secondary_seed_fragment`, `quarantine_containment_jar`, `fragment_readout_display`, `negative_pressure_walls`, `quarantine_research_log`, `emergency_purge_switch`

_Beyond the triple-sealed doors lies the most isolated room on the science deck. The quarantine chamber is a cube of reinforced transparent walls within walls - a room inside a room, separated by ne..._

#### `specimen_storage` — Specimen Storage

**Exits:**
- `east` → `specimen_quarantine` _LOCKED, flag=has_biohazard_clearance_
- `north` → `deck_b_junction`

**Items (6):** `containment_units`, `shattered_container`, `crystal_growth_trail`, `ventilation_grate_floor`, `ice_core_samples`, `specimen_logbook`

_A cold, sterile storage area lined with environmental containment units. Each one holds a biological sample from the ship's mission - soil from Kepler-442b's surface, ice core samples, rock specime..._

#### `telescope_observation_deck` — Upper Observation Deck

**Exits:**
- `down` → `observatory`

**Items (6):** `powerful_telescope`, `navigation_terminal_data`, `builders_origin_chart`, `brown_dwarf_closeup`, `telescope_gimbal`, `velocity_vector_readout`

_You climb the service ladder through a narrow hatch and emerge onto the upper observation deck, a small platform perched above the main observatory. The ceiling here is a single transparent dome, a..._

#### `xenolinguistics_lab` — Xenolinguistics Laboratory

**Exits:**
- `southeast` → `deck_b_junction`

**Items (6):** `builder_translation_matrix`, `decryption_terminals`, `signal_warning_whiteboard`, `colored_yarn_connections`, `glyph_analysis_notes`, `xenolinguist_audio_logs`

_The xenolinguistics lab is a room wallpapered in obsession. Every whiteboard, every screen, every flat surface is covered in symbol analysis - the angular, recursive glyphs of the Builders' languag..._

### Deck C - Living

#### `arboretum` — Ship's Arboretum

**Exits:**
- `northwest` → `crew_corridor`

**Items (6):** `arboretum_roses`, `japanese_maple_tree`, `stone_fountain`, `memorial_bench`, `hanging_fern_baskets`, `birdsong_speakers`

**NPCs:** `corpse_ayele`

_You push through the door and stop. For a moment, you forget where you are. The arboretum is a small glass-ceilinged garden tucked into the starboard hull, and it is alive. Earth plants - only Eart..._

#### `cabin_chen` — Your Cabin (Dr. Chen)

**Exits:**
- `south` → `crew_corridor`

**Items (9):** `player_letter_to_self`, `player_journal`, `photo_of_stranger`, `xenobiology_texts`, `holographic_cell_model`, `small_key_nightstand`, `player_uniforms`, `personal_bed`, `player_nightstand`

**On first enter event:** `event_own_cabin_first_visit`

_Your own quarters. Your room. You step inside and feel... nothing. No recognition. No comfort. You could be a stranger touring a museum of someone else's life.  The room is small but personal. A si..._

#### `cabin_fletcher` — Ensign Fletcher's Cabin

**Exits:**
- `southwest` → `crew_corridor`

**Items (6):** `fletcher_radio_equipment`, `fletcher_comms_log`, `fletcher_aurora_poster`, `fletcher_tablet`, `fletcher_soldering_kit`, `fletcher_coffee_cups`

_Ensign Mark Fletcher's cabin is messy in the way of someone who was always working on something else. Clothes draped over the chair. An unmade bed. Coffee rings on every surface. But the mess has a..._

#### `cabin_hassan` — Cpl. Hassan's Cabin

**Exits:**
- `northeast` → `crew_corridor`

**Items (6):** `hassan_diary`, `hassan_star_chart`, `hassan_model_ships`, `hassan_goodbye_letter`, `hassan_fathers_watch`, `hassan_cairo_photos`

_Corporal Hassan Al-Rashid's cabin is warm and deeply personal - the room of someone who carried home with him across the stars. Photographs of Cairo cover an entire wall: the Nile at sunset, the Kh..._

#### `cabin_lin` — Dr. Lin's Cabin

**Exits:**
- `north` → `crew_corridor`

**Items (5):** `lin_cabin_tablet`, `lin_wine_glass`, `lin_photo_frame`, `lin_cross`, `lin_clothes`

_Dr. Sarah Lin's cabin is less tidy than her office - a personal space versus a professional one. Clothes are strewn across the bed. A half-drunk glass of wine sits on the desk beside a holographic ..._

#### `cabin_okafor` — Lt. Okafor's Cabin

**Exits:**
- `southeast` → `crew_corridor`

**Items (6):** `okafor_family_photos`, `okafor_unfinished_letter`, `okafor_backup_weapon`, `okafor_calendar`, `okafor_prayer_rug`, `okafor_uniforms`

_Lieutenant James Okafor's personal quarters are military-neat despite the chaos that consumed the rest of the ship. The bed is made with hospital corners. His boots sit paired beneath the bunk. Uni..._

#### `cabin_patel` — Dr. Patel's Cabin

**Exits:**
- `west` → `crew_corridor`

**Items (6):** `patels_data_crystal`, `patels_wall_safe`, `patels_desk`, `ransacked_drawer`, `red_spraypaint_warning`, `scattered_research_notes`

_Dr. Raj Patel's cabin was ransacked. Violently. Furniture overturned. Drawers emptied. Books and papers scattered everywhere. Someone was looking for something.  An open wall safe gapes empty above..._

#### `cabin_romano` — Chef Romano's Cabin

**Exits:**
- `east` → `sealed_corridor_c`

**Items (6):** `romano_recipe_diary`, `romano_cookbooks`, `romano_naples_photos`, `romano_grandmother_recipes`, `romano_spice_collection`, `romano_kitchen_knife`

_Chef Antonio Romano's cabin smells like memory. Cookbooks are stacked on every surface - dog-eared Italian classics, molecular gastronomy texts, handwritten recipe collections from his grandmother...._

#### `captains_quarters` — Captain's Quarters

**Exits:**
- `north` → `deck_c_junction`

**Items (9):** `captains_recorder`, `captains_philosophy_book`, `captains_photo`, `ship_model`, `ceremonial_sidearm`, `captains_bed`, `captains_glasses`, `captains_key`, `bridge_access_card`

**On first enter event:** `event_enter_captains_quarters`

_Captain Marcus Reeves's private quarters are austere but personal. A small desk holds a framed photograph of the captain with a younger man - his son, perhaps. A book of classical philosophy sits o..._

#### `chapel` — Multi-Faith Chapel

**Exits:**
- `west` → `observation_lounge`

**Items (6):** `chapel_prayer_cards`, `confession_booth_writing`, `religious_icons_wall`, `electric_candles`, `childs_drawing`, `chapel_altar`

_A small, quiet room designed to serve every faith and none. Simple wooden pews face a plain altar at the front. Behind the altar, a wall of frosted glass is backlit with a warm amber glow. Religiou..._

#### `crew_corridor` — Crew Cabin Corridor

**Exits:**
- `east` → `cabin_patel`
- `north` → `cabin_chen`
- `northeast` → `cabin_fletcher`
- `northwest` → `cabin_okafor`
- `south` → `cabin_lin`
- `southeast` → `arboretum`
- `southwest` → `cabin_hassan`
- `west` → `deck_c_junction`

**Items (3):** `numbered_doors`, `cabin_directory`, `broken_door_frame`

_A long corridor with numbered doors on either side - individual crew cabins. Name plates identify the occupants. Most of the doors are closed. One is ajar, light spilling out. Another has been forc..._

#### `deck_c_junction` — Deck C Crew Deck Junction

**Exits:**
- `down` → `deck_d_hub`
- `east` → `crew_corridor`
- `north` → `observation_lounge`
- `south` → `captains_quarters` _LOCKED, flag=has_bridge_card_
- `southeast` → `sealed_corridor_c` _LOCKED, flag=has_plasma_cutter_
- `southwest` → `recreation_lounge`
- `up` → `deck_b_junction`
- `west` → `mess_hall`

**Items (3):** `crew_directory`, `body_in_doorway`, `ornate_carpet`

_The living deck is quieter than the others. Carpeted floors muffle your footsteps. Soft lighting in wall sconces creates the illusion of normal gravity and normal purpose. For a moment, you can alm..._

#### `galley` — Kitchen Galley

**Exits:**
- `south` → `mess_hall`

**Items (7):** `knife_block`, `prep_island`, `rotten_seafood`, `cutting_board_stain`, `refrigeration_unit`, `chefs_journal`, `sharp_knife`

_The ship's kitchen. Stainless steel gleams under harsh overhead lighting. Pots and pans hang from a rack above a large central prep island. An industrial oven, cold now. Refrigeration units that st..._

#### `gymnasium` — Ship's Gymnasium

**Exits:**
- `south` → `recreation_lounge`

**Items (6):** `gym_barricade`, `barricade_body`, `gym_audio_recorder`, `empty_water_bottles`, `boxing_ring`, `exercise_machines`

**NPCs:** `corpse_gym_survivor`

_The gymnasium is a wide, open space that smells of rubber mats and old sweat. Exercise machines line the walls - treadmills, resistance trainers, zero-g pull-up bars. A small boxing ring occupies o..._

#### `laundry_room` — Ship's Laundry

**Exits:**
- `north` → `sealed_corridor_c`

**Items (6):** `patel_data_crystal_laundry`, `broken_dryer_note`, `unsorted_laundry_baskets`, `industrial_washers`, `detergent_dispenser`, `forgotten_uniforms`

_The ship's laundry facility is aggressively mundane. Industrial washing machines and dryers line the walls in neat rows, their stainless steel drums still and silent. Folding tables occupy the cent..._

#### `mess_hall` — Mess Hall

**Exits:**
- `east` → `deck_c_junction`
- `north` → `galley`

**Items (5):** `interrupted_meals`, `seven_place_settings`, `menu_display`, `overturned_chairs`, `dried_food_trays`

_The largest common space on Deck C, the mess hall could seat a hundred crew members at long communal tables. Remnants of a final, interrupted meal remain on many of them - trays still holding food ..._

#### `observation_lounge` — Observation Lounge

**Exits:**
- `east` → `chapel`
- `south` → `deck_c_junction`

**Items (4):** `observation_viewport`, `brown_dwarf_view`, `comfort_couches`, `observation_bar`

**NPCs:** `woman_in_lounge`

**On first enter event:** `event_woman_in_lounge`

_The observation lounge is one of the most beautiful rooms on the ship. A massive curved viewport - thirty meters wide, reaching from floor to vaulted ceiling - fills the outer wall, revealing the e..._

#### `recreation_lounge` — Recreation Lounge

**Exits:**
- `north` → `gymnasium`
- `northeast` → `deck_c_junction`

**Items (6):** `chess_set_midgame`, `holographic_game_board`, `physical_book_collection`, `frozen_comedy_screen`, `dartboard_photo`, `recreation_body`

_A large common room meant for off-duty relaxation. Gaming tables fill the center of the space - a chess set with pieces still mid-game, a scattered deck of cards, and a holographic game board froze..._

#### `sealed_corridor_c` — Sealed Corridor Section

**Exits:**
- `northwest` → `deck_c_junction`
- `south` → `laundry_room`
- `west` → `cabin_romano`

**Items (4):** `claw_marked_walls`, `collapsed_ceiling_panels`, `torn_carpet_section`, `organic_wall_film`

_Beyond the barricade, the corridor is a different world. The carpet is torn up in places, revealing the metal deck plating beneath. Ceiling panels have collapsed, trailing cables and insulation lik..._

### Deck D - Medical

#### `deck_d_hub` — Deck D Junction

**Exits:**
- `down` → `deck_e_junction`
- `east` → `medical_corridor`
- `up` → `deck_c_junction`

**Items (2):** `junction_sign`, `clean_walls`

_A wide junction that connects the medical wing to the rest of the ship. The junction sits at the intersection of the ship's inter-deck stairwell and the main medical corridor. A stairwell at the ce..._

#### `decontamination_shower` — Decontamination Station

**Exits:**
- `west` → `quarantine_airlock`

**Items (6):** `decon_control_panel`, `uv_light_arrays`, `chemical_spray_nozzles`, `air_filtration_unit`, `decon_status_display`, `yukis_marker_note`

_A functional decontamination station situated between the medical wing and the quarantine section. The chamber is tiled in white ceramic, stained yellow in places by years of chemical spray. UV lig..._

#### `dr_lin_office` — Dr. Lin's Office

**Exits:**
- `east` → `medical_bay`

**Items (7):** `dr_lin_journal`, `dr_lin_photo`, `lin_wall_safe`, `framed_degree`, `scattered_papers`, `silver_chain`, `medical_clearance_badge`

_A small, tidy office that has been violently disturbed. Papers cover the floor. Books have been pulled from shelves. A framed degree from Johns Hopkins hangs crooked on the wall beside a photograph..._

#### `isolation_ward` — Isolation Ward

**Exits:**
- `north` → `medical_bay`

**Items (6):** `isolation_cell_one_scratches`, `isolation_cell_two_body`, `isolation_cell_three_crack`, `dr_lin_body`, `dr_lin_final_notes`, `dr_lin_silver_cross`

**NPCs:** `corpse_lin`

_Four individual isolation cells arranged in a row, each one a glass-walled cube three meters square with its own air supply and decontamination system. They were designed to keep contagion in. Look..._

#### `medical_bay` — Main Medical Bay

**Exits:**
- `east` → `medical_corridor`
- `north` → `surgery`
- `south` → `isolation_ward`
- `west` → `dr_lin_office`

**Items (6):** `crew_roster_display`, `bloody_bed`, `medical_scanner_2`, `surgical_tools`, `iv_stand`, `diagnostic_kit`

**On first enter event:** `event_enter_medical`

_The main medical bay is a large room ringed with empty hospital beds. All but one of them are freshly made, pristine. The exception is the one at the far end: its sheets are soaked in dried blood, ..._

#### `medical_corridor` — Medical Deck Corridor

**Exits:**
- `east` → `morgue`
- `north` → `quarantine_airlock`
- `south` → `deck_i_hub`
- `southwest` → `pharmacy` _LOCKED, flag=has_medical_badge_
- `west` → `medical_bay`

**Items (3):** `holographic_receptionist`, `medical_signs`, `discarded_mask`

**NPCs:** `kirilov`

_The corridor that leads into the medical wing, its walls colored a washed-out clinical green. Overhead lighting is harsh and white, and the air smells faintly of antiseptic and something beneath it..._

#### `morgue` — Ship's Morgue

**Exits:**
- `south` → `morgue_freezer`
- `west` → `medical_corridor`

**Items (6):** `mortician_table_body`, `body_drawer_reeves`, `body_drawer_okafor`, `body_drawer_vasquez`, `body_drawer_empty`, `morgue_logbook`

**NPCs:** `corpse_reeves`

_The morgue is colder than the rest of medical. Rows of body drawers line three walls, their labels marked in crisp white letters. Some drawers are open, empty. Others are open and definitely not em..._

#### `morgue_freezer` — Morgue Freezer

**Exits:**
- `north` → `morgue`

**Items (4):** `frozen_body_bags`, `breathing_body_bag`, `freezer_shelving`, `frosted_name_labels`

_A walk-in freezer behind the main morgue, its heavy insulated door sealing with a pressurized gasp as it closes behind you. The temperature plummets immediately - your breath crystallizes into clou..._

#### `pharmacy` — Pharmacy

**Exits:**
- `northeast` → `medical_corridor`

**Items (6):** `sedative_doses`, `painkillers`, `anti_radiation_meds`, `immunosuppressants`, `reagent_a_case`, `pharmacy_inventory_log`

_Rows of steel shelving stretch from floor to ceiling, stocked with medications in labeled bins arranged in strict alphabetical order. The organization is almost obsessive - Dr. Lin's work, no doubt..._

#### `quarantine_airlock` — Quarantine Airlock

**Exits:**
- `east` → `decontamination_shower`
- `north` → `quarantine_bay` _LOCKED, HIDDEN, flag=has_medical_badge_
- `south` → `medical_corridor`

**Items (3):** `quarantine_glass`, `quarantine_control_panel`, `warning_signs_multilang`

_A small airlock separates the main medical deck from the quarantine bay. A heavy pressure door with reinforced glass windows blocks the way forward. Beyond the glass, you can see the quarantine are..._

#### `quarantine_bay` — Quarantine Bay

**Exits:**
- `south` → `quarantine_airlock`

**Items (4):** `quarantine_cell_1`, `quarantine_cell_2`, `quarantine_cell_3`, `lin_clipboard`

_The quarantine bay is a slaughterhouse. Three containment cells, each one holding a crewmember in varying states of advanced infection. They moan. They reach through the bars. They ask for your hel..._

#### `research_lab_med` — Medical Research Laboratory

**Exits:**
- `west` → `surgery`

**Items (6):** `research_centrifuge`, `lin_research_notes`, `molecular_whiteboard`, `research_microscopes`, `chemical_analysis_station`, `centrifuge_sample_vials`

_Dr. Lin's personal research laboratory is a controlled chaos of scientific equipment and desperate investigation. A centrifuge sits on the main bench, its rotor still loaded with sample vials - she..._

#### `surgery` — Surgical Theater

**Exits:**
- `east` → `research_lab_med`
- `south` → `medical_bay`

**Items (5):** `dr_patel_body`, `surgical_saw`, `autopsy_datapad`, `surgical_robot`, `surgery_tray`

**On first enter event:** `event_see_patel`

_A sterile operating theater with a surgical bed at its center, illuminated by harsh overhead lamps that somehow never went dark. A surgical robot arm - half-assembled, half-dismantled - hangs over ..._

### Deck E - Security

#### `armory` — Ship's Armory

**Exits:**
- `east` → `evidence_locker` _LOCKED, key=red_keycard_
- `north` → `armory_vault` _LOCKED, flag=has_okafor_biometrics_
- `west` → `deck_e_junction`

**Items (7):** `tactical_rifle`, `handgun`, `ammunition_box`, `biometric_weapons_locker`, `confiscated_effects_locker`, `tear_gas_grenades`, `tactical_vest`

_The armory is a small, heavily-reinforced room lined with weapon racks. Most of the racks are empty - whoever came in here took what they needed and left in a hurry. A few firearms remain, along wi..._

#### `armory_vault` — Armory Vault

**Exits:**
- `south` → `armory`

**Items (6):** `tactical_shotgun`, `flare_gun`, `riot_shield`, `explosive_charges_case`, `okafors_custom_sidearm`, `flare_bandolier`

_The vault behind the armory's biometric locker is small and brutally functional - reinforced walls, a single overhead light, and weapon racks designed for hardware you hope you never need. This is ..._

#### `brig` — Ship's Brig

**Exits:**
- `north` → `deck_e_junction`

**Items (4):** `brig_body`, `bloody_message`, `empty_cells`, `prisoner_personal_items`

**On first enter event:** `event_see_brig`

_The brig consists of four holding cells, three of them empty, one of them not. The occupied cell holds a body - slumped in the corner, still wearing an orange prisoner jumpsuit. The cell door is op..._

#### `deck_e_junction` — Deck E Security Hub

**Exits:**
- `down` → `engineering_junction`
- `east` → `armory` _LOCKED_
- `north` → `security_office`
- `south` → `brig`
- `up` → `deck_d_hub`
- `west` → `security_corridor_south` _LOCKED, flag=barricade_cleared_

**Items (4):** `security_cameras_smashed`, `blood_trail`, `scorch_marks`, `spent_shell_casings`

_You emerge onto the security deck. The corridor is narrower here, walls lined with thick reinforced paneling and surveillance cameras. Most of the cameras are smashed. A red line painted on the flo..._

#### `evidence_locker` — Evidence Locker

**Exits:**
- `west` → `armory`

**Items (6):** `evidence_bag_patel`, `evidence_bag_silver_vial`, `evidence_bag_photos`, `evidence_bag_letters`, `evidence_bag_childs_drawing`, `confiscation_logbook`

_Floor-to-ceiling shelving lines three walls, loaded with labeled evidence bags in clear plastic. Each one is tagged with a date, a name, and a case reference number. These are the personal effects ..._

#### `interrogation_room` — Interrogation Room

**Exits:**
- `east` → `security_office`

**Items (5):** `interrogation_table`, `one_way_mirror`, `audio_recording_equipment`, `okafor_self_interview`, `interrogation_chairs`

_A bare room designed to make people uncomfortable. Grey walls, a steel table bolted to the floor, two chairs facing each other across its surface. A one-way mirror dominates one wall - from this si..._

#### `monitoring_station` — Security Monitoring Station

**Exits:**
- `west` → `security_office`

**Items (5):** `camera_control_console`, `recording_archive`, `okafors_cold_coffee`, `monitor_wall`, `camera_19_feed`

**NPCs:** `corpse_okafor`

_A wall of screens. Twenty-four monitors arranged in a six-by-four grid, the nerve center of the ship's surveillance system. Most of them show nothing but static - grey snow hissing with dead signal..._

#### `security_corridor_south` — Security Corridor South

**Exits:**
- `east` → `deck_e_junction`

**Items (4):** `combat_barricade_remains`, `shell_casing_carpet`, `scorched_corridor_walls`, `blood_spatters`

**NPCs:** `corpse_kirilov_victim`

_Beyond the cleared barricade, the corridor stretches south into a war zone. The walls are cratered with bullet impacts and blackened with scorch marks from plasma fire. A makeshift barricade of ove..._

#### `security_office` — Security Office

**Exits:**
- `east` → `monitoring_station`
- `south` → `deck_e_junction`
- `west` → `interrogation_room`

**Items (7):** `okafors_red_book`, `okafors_audio_recorder`, `tactical_map_contamination`, `okafor_family_photo`, `empty_coffee_cups`, `okafor_desk`, `red_keycard`

_The office of Security Chief Lt. James Okafor, based on the nameplate on the desk. It is a mess. Tactical maps of the ship cover one wall, with red pins marking... something. Contamination zones, p..._

### Deck F - Engineering

#### `coolant_pump_room` — Coolant Pump Room

**Exits:**
- `east` → `main_engineering`

**Items (6):** `coolant_pump_two`, `pump_control_panel`, `coolant_repair_toolkit`, `coolant_reservoir`, `toxic_coolant_puddle`, `pump_diagnostic_readout`

_A cavernous industrial space dominated by three massive coolant pumps, each the size of a small vehicle, bolted to the deck with steel brackets thick as your arm. Pump One and Pump Three cycle with..._

#### `engineering_break_room` — Engineering Break Room

**Exits:**
- `north` → `engineering_vent_access` _HIDDEN_
- `south` → `yuki_hideout` _LOCKED, flag=yuki_ally_
- `west` → `main_engineering`

**Items (6):** `abandoned_card_game`, `yukis_backpack`, `yukis_journal`, `working_coffee_maker`, `safety_poster_defaced`, `sleeping_bag_under_table`

_A small, scuffed break room with mismatched furniture and the permanent smell of old coffee. Four round tables fill the space, each with a handful of chairs. On the nearest table, a card game sits ..._

#### `engineering_junction` — Engineering Deck Access

**Exits:**
- `down` → `deck_h_junction`
- `east` → `engineering_workshop`
- `north` → `main_engineering`
- `up` → `deck_e_junction`
- `west` → `reactor_antechamber` _LOCKED, flag=has_radiation_suit_

**Items (3):** `blast_door_wedge`, `radiation_warning_sign`, `pipe_network`

_You climb up into a much larger, noisier space. Engineering. The air here thrums with the vibration of massive machinery - reactors, coolant pumps, plasma regulators. Pipes snake overhead in intric..._

#### `engineering_vent_access` — Engineering Ventilation Access

**Exits:**
- `south` → `engineering_break_room`
- `up` → `deck_e_junction` _HIDDEN_

**Items (3):** `vent_ladder_rungs`, `scratched_rungs`, `vent_shaft_branches`

_A tight vertical shaft where the ship's main ventilation trunk passes through the engineering deck. The vent grate from the break room opens into a narrow service platform surrounded by ductwork th..._

#### `engineering_workshop` — Engineering Workshop

**Exits:**
- `west` → `engineering_junction`

**Items (8):** `radiation_suit`, `hazmat_suit`, `power_cell_pack`, `modified_plasma_cutter`, `workshop_tablet`, `half_sandwich`, `spare_parts_bin`, `fabricator_unit`

_A well-equipped workshop filled with tools, workbenches, and half-finished projects. A spacesuit lies disassembled on one bench, its life support unit open. On another, someone was modifying a hand..._

#### `main_engineering` — Main Engineering

**Exits:**
- `down` → `plasma_conduit_junction`
- `east` → `engineering_break_room`
- `south` → `engineering_junction`
- `up` → `reactor_catwalk` _LOCKED, flag=tanaka_met_
- `west` → `coolant_pump_room`

**Items (4):** `reactor_core`, `primary_control_station`, `monitoring_stations`, `engineering_catwalks`

**NPCs:** `yuki_tanaka`

**On first enter event:** `event_first_see_tanaka`

_Main Engineering is a cathedral of technology - a vast three-story chamber built around the gleaming fusion reactor core that extends from ceiling to floor at its center. Catwalks ring the room at ..._

#### `plasma_conduit_junction` — Plasma Conduit Junction

**Exits:**
- `up` → `main_engineering`

**Items (5):** `damaged_plasma_conduit`, `conduit_valve_controls`, `pipe_sealant_canister`, `plasma_distribution_schematic`, `conduit_maintenance_log`

_Below the main engineering floor, a cramped sublevel where plasma delivery lines converge from every part of the ship. Pipes of every diameter crowd the space - some thick as tree trunks carrying h..._

#### `reactor_antechamber` — Reactor Antechamber

**Exits:**
- `east` → `engineering_junction`
- `north` → `reactor_core_interior` _LOCKED, flag=has_radiation_suit_

**Items (4):** `reactor_control_interface`, `coolant_pressure_gauge`, `course_readout`, `thruster_status_panel`

_A low-ceilinged antechamber filled with the overwhelming hum of the fusion reactor on the other side of a massive lead-lined door. Your ears pop. The air tastes metallic. Even in the radiation suit..._

#### `reactor_catwalk` — Reactor Upper Catwalk

**Exits:**
- `down` → `main_engineering`

**Items (4):** `secondary_control_station`, `manual_override_switch`, `coolant_valves`, `emergency_shutdown`

_The upper catwalk overlooks the reactor core. From here you can see the whole engineering bay spread out below - the gleaming reactor, the monitoring stations, the distant glow of pilot lights on s..._

#### `reactor_core_interior` — Reactor Core Interior

**Exits:**
- `south` → `reactor_antechamber`

**Items (5):** `fusion_core_plasma`, `reactor_control_rods`, `emergency_shutdown_terminal`, `manual_overload_switch`, `overload_glass_case`

_You step through the lead-lined door and into the heart of the Prometheus. The reactor core chamber is a cylindrical vault thirty meters tall, its walls lined with heat-resistant ceramic tiles that..._

#### `yuki_hideout` — Yuki's Hideout

**Exits:**
- `north` → `engineering_break_room`

**Items (6):** `yukis_sleeping_bag`, `yukis_water_filter`, `yukis_family_photo`, `yukis_handgun`, `yukis_engineering_notebook`, `yukis_canteen`

_A storage closet barely two meters by three, converted with desperate ingenuity into a survivable living space. Yuki Tanaka has been hiding here. The door locks from the inside with a deadbolt she ..._

### Deck G - Cargo

#### `cargo_access` — Cargo Access Tunnel

**Exits:**
- `down` → `water_processing`
- `east` → `deck_h_junction`
- `north` → `cargo_bay_main`
- `south` → `hydroponics_entry`
- `west` → `water_treatment_secondary`

**Items (2):** `cargo_manifest`, `industrial_lights`

_A utilitarian tunnel branches off from the maintenance junction, leading into the cargo and hydroponics deck. The walls here are bare metal. The lights are industrial. You can smell something organ..._

#### `cargo_bay_main` — Main Cargo Bay

**Exits:**
- `down` → `lower_cargo`
- `east` → `cold_storage`
- `south` → `cargo_access`
- `west` → `cargo_office`

**Items (5):** `broken_mining_container`, `cargo_elevator`, `cargo_manifest_terminal`, `scattered_mining_equipment`, `site_7_documentation`

_A cavernous cargo bay filled with shipping containers, crates, and industrial equipment. Most of it is strapped down securely. Some of it is not - a large container near the center has been broken ..._

#### `cargo_office` — Cargo Master's Office

**Exits:**
- `east` → `cargo_bay_main`

**Items (6):** `webb_audio_log`, `shipping_manifests`, `fresh_sandwich`, `cargo_office_terminal`, `webb_coffee_mug`, `fountain_pen`

_A small, cluttered office that smells of coffee and bureaucracy. Shipping manifests cover every horizontal surface - the desk, the chair, the floor, pinned to the walls in overlapping layers. Cargo..._

#### `chrysalis_chamber` — The Chrysalis Chamber

**Exits:**
- `west` → `heart_of_garden`

**Items (4):** `chrysalis_figure`, `crystalline_web`, `transformation_tissue`, `chrysalis_recorder`

**NPCs:** `chrysalis_crew`

**On first enter event:** `event_chrysalis_encounter`

_The deepest room in the Garden. You push through a curtain of crystalline tendrils into a space that was once a storage bay and is now a cathedral of transformation. The walls, floor, and ceiling a..._

#### `cold_storage` — Cold Storage Unit

**Exits:**
- `west` → `cargo_bay_main`

**Items (6):** `tissue_sample_container`, `crystalline_containers`, `biological_specimens`, `dr_lin_priority_tag`, `preservation_racks`, `temperature_controls`

**NPCs:** `chef_romano`, `corpse_romano`

_An industrial refrigeration unit the size of a small warehouse, its heavy door sealing with a hiss as it closes behind you. The temperature plummets. Your breath crystallizes. Racks of labeled cont..._

#### `garden_periphery_east` — Garden Periphery - East

**Exits:**
- `west` → `hydroponics_main`

**Items (4):** `incorporated_couple`, `broken_wall_panels`, `eastern_vine_growth`, `crew_id_tags_couple`

_The eastern edge of the hydroponics bay, where the Garden's growth meets the ship's hull. Vines have broken through the wall panels here, splitting metal seams and curling through cable runs with a..._

#### `garden_periphery_west` — Garden Periphery - West

**Exits:**
- `east` → `hydroponics_main`

**Items (5):** `functioning_work_station`, `kowalski_tool_belt`, `original_hydroponics`, `thin_vine_lattice`, `growth_rate_data`

_The western edge of the hydroponics bay. The growth here is newer, thinner - you can see the original hydroponics equipment beneath the vines, trays and grow-lights and irrigation tubing still reco..._

#### `garden_root_network` — Root Network

**Exits:**
- `down` → `water_processing`
- `up` → `hydroponics_main`

**Items (4):** `bioluminescent_roots`, `root_junction_node`, `split_deck_plating`, `root_fluid_sample`

_Below the hydroponics bay, the Garden's roots have penetrated through the deck plating, splitting metal and worming through cable channels to create an organic tunnel system. The roots and tendrils..._

#### `heart_of_garden` — Heart of the Garden

**Exits:**
- `east` → `chrysalis_chamber`
- `north` → `hydroponics_main`
- `south` → `seed_nursery`

**Items (3):** `garden_heart_nexus`, `rooted_deck_plating`, `silver_veined_crystal`

**On first enter event:** `event_garden_heart`

_At the heart of the hydroponics bay, the Seed has grown into something new. A structure. A nexus. A crystalline formation perhaps five meters tall, wrapped in vines and rooted into the deck plating..._

#### `hydroponics_entry` — Hydroponics Entrance

**Exits:**
- `north` → `cargo_access`
- `south` → `hydroponics_main` _LOCKED, flag=has_hazmat_suit_

**Items (3):** `hydroponics_airlock_glass`, `wrong_plant_patterns`, `hydroponics_readout`

_You stand at the entrance to the hydroponics bay. A transparent airlock door separates you from the lush green interior beyond. Even through the glass, you can see that something is wrong with the ..._

#### `hydroponics_main` — Hydroponics Bay - The Garden

**Exits:**
- `down` → `garden_root_network` _HIDDEN_
- `east` → `garden_periphery_east`
- `north` → `hydroponics_entry`
- `south` → `heart_of_garden` _HIDDEN_
- `west` → `garden_periphery_west`

**Items (4):** `overgrown_plants`, `incorporated_crew`, `sample_garden_tissue`, `garden_spores`

**NPCs:** `garden_voice`

**On first enter event:** `event_enter_garden`

_You enter the Garden.  The growth is everywhere. Not just plants anymore - the Seed has woven itself through every living system in this bay, through every leaf and stem and root, and through the c..._

#### `lower_cargo` — Lower Cargo Hold

**Exits:**
- `up` → `cargo_bay_main`

**Items (3):** `infected_container`, `tendril_growth`, `original_seed_location`

**On first enter event:** `event_find_seed_origin`

_The lower cargo hold is cold and dimly lit. Row upon row of shipping containers stretch into the darkness. A smell you've been trying to ignore is much stronger here - the sweet-rotten smell of som..._

#### `seed_nursery` — The Nursery

**Exits:**
- `north` → `heart_of_garden`

**Items (5):** `daughter_crystals`, `crystal_shard_sample`, `organic_substrate`, `germination_equipment`, `spore_density_reader`

**On first enter event:** `event_discover_nursery`

_Deep within the Garden, in a space that was once a seed germination chamber, the alien Seed has been actively reproducing. Small crystalline formations rise from the organic substrate that covers e..._

#### `water_processing` — Water Processing Facility

**Exits:**
- `north` → `garden_root_network` _HIDDEN_
- `up` → `cargo_access`

**Items (5):** `cracked_filtration_tank`, `water_purge_control`, `filtration_system`, `pump_station`, `chemical_sterilizer`

_The water processing facility is a maze of pipes, filtration tanks, and pumps. This is where the ship cleans and recycles every drop of water used by the crew. It is also, you now understand, where..._

#### `water_treatment_secondary` — Secondary Water Treatment

**Exits:**
- `east` → `cargo_access`

**Items (6):** `clean_water_dispenser`, `chemical_storage_locker`, `independent_filtration`, `cure_reagents`, `lin_research_reference`, `water_quality_readout`

_A secondary water treatment facility, smaller than the main processing plant but critically important: this system operates on an independent circuit, separate from the contaminated primary water s..._

### Deck H - AI Core

#### `ai_core_antechamber` — AI Core Antechamber

**Exits:**
- `down` → `coolant_control_h`
- `east` → `neural_interface_chamber` _LOCKED, flag=aria_granted_access_
- `north` → `ai_core_main` _LOCKED, flag=aria_granted_access_
- `south` → `data_nexus`
- `west` → `deck_h_junction`

**Items (3):** `aria_terminal`, `data_walls`, `core_door`

**On first enter event:** `event_first_aria_contact`

_The antechamber to ARIA's central processing core is a circular room lit by an ethereal blue glow. The walls pulse softly with flowing data patterns - a physical manifestation of the AI's thinking...._

#### `ai_core_main` — ARIA Central Processing

**Exits:**
- `down` → `quantum_archive` _HIDDEN_
- `south` → `ai_core_antechamber`

**Items (4):** `aria_crystal_matrix`, `quantum_processors`, `containment_field_aria`, `core_catwalk`

**NPCs:** `aria_avatar`

**On first enter event:** `event_aria_full_conversation`

_You step into a cathedral of thought. The AI core is an enormous spherical chamber, its walls lined with quantum processors that cast shifting blue-green light across every surface. At the center, ..._

#### `aria_memory_vault` — ARIA Memory Vault

**Exits:**
- `up` → `quantum_archive`

**Items (4):** `aria_personal_substrate`, `memory_projections`, `amber_crystal`, `magnetic_field_emitter`

**On first enter event:** `event_aria_memories`

_Beneath the quantum archive, hidden behind a false panel that ARIA herself designed, lies a chamber no crew member was ever meant to find. The room is small and intimate - barely larger than a clos..._

#### `aria_shade_chamber` — Isolated Server Room

**Exits:**
- `west` → `data_nexus`

**Items (4):** `shade_terminals`, `corrupted_data_walls`, `aria_shade_interface`, `quarantine_firewall`

**NPCs:** `aria_shade`

**On first enter event:** `event_meet_shade`

_You step into a server room that should not exist. It is not on any ship schematic. The walls flicker with data patterns, but where ARIA's core glows blue, these patterns burn an angry red, shiftin..._

#### `coolant_control_h` — AI Core Coolant Control

**Exits:**
- `up` → `ai_core_antechamber`

**Items (5):** `coolant_control_panel`, `liquid_nitrogen_pipes`, `failing_backup_pump`, `tanaka_maintenance_log`, `coolant_valves`

_The coolant infrastructure for the AI core fills this room with a maze of massive pipes carrying liquid nitrogen at temperatures cold enough to freeze exposed skin on contact. Frost crusts every su..._

#### `data_nexus` — Data Nexus

**Exits:**
- `east` → `aria_shade_chamber` _LOCKED, HIDDEN, flag=nexus_passage_found_
- `north` → `ai_core_antechamber`

**Items (6):** `nexus_terminal`, `security_camera_feeds`, `comms_log_archive`, `network_switch_racks`, `environmental_readouts`, `fiber_optic_bundles`

**On first enter event:** `event_access_nexus`

_Where all the ship's data conduits converge, the Data Nexus is a forest of network switches, fiber optic bundles, and signal processors arranged in towering racks that reach from floor to ceiling. ..._

#### `deck_h_junction` — Deck H Maintenance Junction

**Exits:**
- `down` → `cryo_maintenance`
- `east` → `ai_core_antechamber` _LOCKED_
- `south` → `vent_network_i` _HIDDEN_
- `up` → `engineering_junction`
- `west` → `cargo_access`

**Items (3):** `flickering_green_light`, `access_panels`, `data_conduit_humming`

_You emerge from the maintenance tunnel into a dim, blue-lit service corridor. The air up here is noticeably different - cleaner, drier, faintly ozone-scented. This is the AI core deck, where the sh..._

#### `neural_interface_chamber` — Neural Interface Chamber

**Exits:**
- `west` → `ai_core_antechamber`

**Items (4):** `neural_interface_chair`, `electrode_crown`, `use_log_terminal`, `safety_override`

_A small, circular room dominated by a single chair at its center and a crown of electrode-studded metal hovering above it. The Neural Interface Chamber. Direct brain-to-AI connection. The most dang..._

#### `quantum_archive` — Quantum Data Archive

**Exits:**
- `down` → `aria_memory_vault` _HIDDEN_
- `up` → `ai_core_main`

**Items (4):** `archive_terminal`, `crystalline_storage`, `mission_records`, `hidden_compartment`

_Beneath the AI core, the quantum data archive stretches into shadows. Shelves upon shelves of crystalline data storage units hold the entirety of the Prometheus's mission records - every sensor rea..._

### Deck I - Cryogenics

#### `cryo_bay` — Cryogenics Bay - Pod 23

**Exits:**
- `east` → `cryo_corridor` _LOCKED, flag=cryo_exit_unlocked_
- `north` → `cryo_control`
- `west` → `cryo_storage`

**Items (8):** `cryo_jumpsuit`, `personal_locker`, `diagnostic_terminal`, `emergency_kit`, `pod_23`, `sparking_panel`, `green_override_button`, `cryo_release_key`

_A vast cylindrical chamber that echoes with the sound of your own breathing. Sixty cryogenic pods line the curved walls in four concentric rings, their glass faces rimed with frost. Most are dark. ..._

#### `cryo_control` — Cryogenic Control Room

**Exits:**
- `east` → `cryo_medical`
- `south` → `cryo_bay`
- `west` → `pod_monitoring_alcove` _HIDDEN_

**Items (5):** `bullet_hole_console`, `duty_officers_tablet`, `cryo_status_display`, `frozen_coffee_cup`, `control_chair`

_A cramped control station dominated by a bank of monitors, most of them displaying static or error messages. The primary interface is cracked, a spider-web of fractures radiating from a single bull..._

#### `cryo_corridor` — Cryo-Deck Main Corridor

**Exits:**
- `east` → `deck_i_hub`
- `south` → `deck_i_storage` _LOCKED, key=deck_i_storage_key_
- `west` → `cryo_bay`

**Items (3):** `ration_wrappers`, `bloody_footprints`, `corridor_keypad`

_The main corridor of Deck I runs in a wide curve, following the shape of the ship's spine. Red warning lights strobe at regular intervals, painting the walls in intermittent crimson. The air here i..._

#### `cryo_maintenance` — Maintenance Crawlspace

**Exits:**
- `down` → `propulsion_access` _LOCKED, HIDDEN_
- `east` → `vent_network_i` _HIDDEN_
- `north` → `cryo_storage`
- `up` → `deck_h_junction` _LOCKED, flag=has_flashlight_

**Items (6):** `tool_belt`, `dark_smear`, `maintenance_ladder`, `flashlight`, `wrench`, `junction_box`

_A cramped maintenance tunnel runs beneath the cryogenics deck, thick with cables and piping. Red emergency lights flicker overhead. The air tastes of ozone and coolant.  Someone has been down here ..._

#### `cryo_medical` — Emergency Medical Station

**Exits:**
- `west` → `cryo_control`

**Items (7):** `medical_cabinet`, `examination_table`, `medical_scanner`, `dr_lin_datapad`, `biohazard_bin`, `stimpack`, `sedative_syringe`

_A small medical bay for handling cryo-related emergencies - shock, pulmonary distress, neural misfiring. A single examination table sits in the center of the room, its restraints hanging loose. A c..._

#### `cryo_pod_12_interior` — Interior of Cryo Pod 12

**Exits:**
- `south` → `cryo_storage`

**Items (6):** `kirilov_datapad`, `claw_marks_glass`, `dried_cryo_residue`, `silver_grey_residue`, `shredded_padding`, `pod_12_headrest`

**On first enter event:** `event_discover_kirilov`

_You climb through the shattered glass of Pod 12 into a space barely large enough for a person to lie flat. The inside of the pod is a testament to sheer animal panic. Deep gouges score the tempered..._

#### `cryo_recycling` — Cryo-Fluid Recycling Room

**Exits:**
- `east` → `cryo_storage`

**Items (6):** `recycling_tank_cracked`, `silver_threads_fluid`, `recycling_pumps`, `maintenance_terminal_cryo`, `valve_wheels`, `fluid_composition_data`

**On first enter event:** `event_discover_cryo_infection`

_A low-ceilinged industrial space dominated by three massive recycling tanks, each one taller than a person and filled with the pale blue cryo-fluid that keeps the pods operational. Pumps chug and w..._

#### `cryo_storage` — Cryogenic Storage

**Exits:**
- `east` → `cryo_bay`
- `north` → `cryo_pod_12_interior`
- `south` → `cryo_maintenance` _HIDDEN_
- `west` → `cryo_recycling`

**Items (3):** `pod_47`, `crew_manifest`, `pod_12_damaged`

_A long hallway of frozen caskets. Pods stretch into the dim distance in two facing rows, their occupants' faces just visible through fogged glass. Most of the diagnostic lights are red. A few are d..._

#### `deck_i_hub` — Deck I Elevator Hub

**Exits:**
- `east` → `emergency_shuttle_bay` _LOCKED_
- `north` → `medical_corridor`
- `south` → `emergency_airlock_i`
- `up` → `deck_h_junction` _LOCKED_
- `west` → `cryo_corridor`

**Items (4):** `dead_engineer`, `plasma_cutter`, `elevator_panel`, `maintenance_hatch_hub`

**NPCs:** `corpse_engineer`

_A circular junction with an elevator shaft at its center. The doors stand open, revealing a platform - though the descent and ascent panels are dark. Four corridors radiate from the hub. To the nor..._

#### `deck_i_storage` — Deck I Storage

**Exits:**
- `north` → `cryo_corridor`

**Items (6):** `thermal_blankets`, `portable_heater`, `bullet_casings`, `crew_locker_14`, `ration_pack`, `torn_uniform_scrap`

_A storage bay filled with racks of spare parts, ration crates, and crates marked with various hazard symbols. Someone has been living here - a makeshift bed of thermal blankets in the corner, a por..._

#### `emergency_airlock_i` — Emergency Airlock - Deck I

**Exits:**
- `north` → `deck_i_hub`

**Items (6):** `spare_eva_helmet`, `emergency_oxygen_canister`, `hull_viewport`, `jammed_outer_door`, `eva_equipment_rack`, `emergency_sealant`

_A small emergency airlock set into the hull of Deck I. The inner door responds to your touch, grinding open on damaged servos. The outer door is jammed in a partially open position - you can see a ..._

#### `emergency_shuttle_bay` — Emergency Shuttle Bay - Deck I

**Exits:**
- `down` → `escape_pod_bay_lower`
- `west` → `deck_i_hub`

**Items (5):** `shuttle_fuel_gauge`, `shattered_helmet`, `eva_suit`, `viewport_brown_dwarf`, `escape_shuttle`

**On first enter event:** `event_see_brown_dwarf`

_A small shuttle bay holding a single emergency escape craft. The shuttle's doors are wide open, its interior empty. Beside it, on the deck, lies a shattered helmet. A second EVA suit stands in its ..._

#### `escape_pod_bay_lower` — Lower Escape Pod Bay

**Exits:**
- `up` → `emergency_shuttle_bay`

**Items (6):** `launch_manifest_osei`, `crushed_escape_pod`, `intact_escape_pod`, `pod_launch_console`, `structural_beam_fallen`, `berth_one_viewport`

_Below the shuttle bay, a secondary escape pod facility holds three berths arranged in a row along the hull. The room is utilitarian - bare metal, emergency lighting, launch rails recessed into the ..._

#### `pod_monitoring_alcove` — Hidden Monitoring Alcove

**Exits:**
- `east` → `cryo_control`

**Items (5):** `survivor_journal`, `thermal_bedroll`, `ration_wrapper_stack`, `wall_graffiti_days`, `hidden_panel_door`

**NPCs:** `corpse_hassan`

_Behind the cryo monitoring station, concealed by a panel that was never meant to be a door, someone carved out a hiding place. The alcove is barely two meters square, a crawlspace between the contr..._

#### `vent_network_i` — Ventilation Shaft - Deck I

**Exits:**
- `up` → `deck_h_junction` _LOCKED, flag=has_flashlight_
- `west` → `cryo_maintenance`

**Items (3):** `silver_threads_vent`, `biological_residue`, `vent_shaft_branch`

_You squeeze into a ventilation shaft barely wide enough for your shoulders. The metal walls press close on all sides. You can only move by crawling on your belly, elbows scraping against riveted se..._

### Deck J - Propulsion

#### `main_engine_room` — Main Engine Room

**Exits:**
- `south` → `propulsion_access`

**Items (5):** `master_drive_control`, `thrust_regulators`, `plasma_drive_core`, `heat_shield_controls`, `navigation_override`

**On first enter event:** `event_first_engine_room`

_The main engine room is the single loudest space on the Prometheus. The roar of the plasma drive is deafening. Giant pistons and thrust regulators hammer in rhythmic unison. Heat shimmers the air. ..._

#### `propulsion_access` — Propulsion Deck Access

**Exits:**
- `north` → `main_engine_room` _LOCKED, flag=engine_room_unlocked_
- `up` → `deck_i_hub`

**Items (3):** `engine_blast_door`, `emergency_override_keypad`, `propulsion_warning_sign`

_A cramped maintenance area between the cryogenics deck and the main propulsion systems below. The walls vibrate with the low, constant hum of the drive plasma. You can feel it in your bones.  A hea..._

---

## 6. All Items Reference

Every item with id, name, properties, and location.

### Readable (Logs, Journals, Notes) (78)

| ID | Name | Location | Properties |
|----|------|----------|------------|
| `archive_terminal` | archive terminal | `room:quantum_archive` | portable, readable |
| `audio_recording_equipment` | audio recording equipment | `room:interrogation_room` | portable, readable |
| `autopsy_datapad` | autopsy datapad | `room:surgery` | portable, readable |
| `ayele_research_terminal` | Ayele's research terminal | `room:botany_lab` | portable, readable |
| `captains_recorder` | Captain's recording device | `room:captains_quarters` | portable, readable |
| `chapel_prayer_cards` | prayer cards | `room:chapel` | portable, readable |
| `chefs_journal` | chef's journal | `room:galley` | portable, readable |
| `chrysalis_recorder` | chrysalis recorder | `room:chrysalis_chamber` | portable, readable |
| `comms_log_archive` | communications log archive | `room:data_nexus` | portable, readable |
| `conduit_maintenance_log` | conduit maintenance log | `room:plasma_conduit_junction` | portable, readable |
| `conference_notepad` | conference notepad | `room:conference_room` | portable, readable |
| `confiscation_logbook` | confiscation logbook | `room:evidence_locker` | portable, readable |
| `crew_id_tags_couple` | crew ID tags | `room:garden_periphery_east` | portable, readable |
| `crew_manifest` | crew manifest | `room:cryo_storage` | portable, readable |
| `defensive_systems_manual` | defensive systems manual | `room:tactical_operations` | portable, readable |
| `diagnostic_terminal` | diagnostic terminal | `room:cryo_bay` | scenery, readable |
| `dr_lin_datapad` | Dr. Lin's medical datapad | `room:cryo_medical` | portable, readable |
| `dr_lin_final_notes` | Dr. Lin's final notes | `room:isolation_ward` | portable, readable |
| `dr_lin_journal` | Dr. Lin's journal | `room:dr_lin_office` | portable, readable |
| `dr_lin_priority_tag` | Dr. Lin's priority tag | `room:cold_storage` | portable, readable |
| `duty_officers_tablet` | duty officer's tablet | `room:cryo_control` | portable, readable |
| `evidence_bag_letters` | evidence bag - letters | `room:evidence_locker` | portable, readable |
| `evidence_bag_patel` | evidence bag - Patel | `room:evidence_locker` | portable, readable |
| `exobio_notes_terminal` | exobio notes terminal | `room:exobio_lab` | portable, readable |
| `fletcher_comms_log` | Fletcher's comms log | `room:cabin_fletcher` | portable, readable |
| `fletcher_love_letter` | Fletcher's unfinished letter | `room:bridge_crew_quarters` | portable, readable |
| `fletcher_tablet` | Fletcher's tablet | `room:cabin_fletcher` | portable, readable |
| `fluid_composition_data` | fluid composition data | `room:cryo_recycling` | portable, readable |
| `glyph_analysis_notes` | glyph analysis notes | `room:xenolinguistics_lab` | portable, readable |
| `growth_rate_data` | growth rate data | `room:garden_periphery_west` | portable, readable |
| `gym_audio_recorder` | gym audio recorder | `npc:corpse_gym_survivor` | portable, readable |
| `hassan_diary` | Hassan's diary | `room:cabin_hassan` | portable, readable |
| `hassan_goodbye_letter` | Hassan's goodbye letter | `room:cabin_hassan` | portable, readable |
| `kirilov_datapad` | Kirilov's datapad | `room:cryo_pod_12_interior` | portable, readable |
| `lab_datapad` | laboratory datapad | `room:main_lab` | portable, readable |
| `launch_manifest_osei` | launch manifest | `room:escape_pod_bay_lower` | portable, readable |
| `lin_cabin_tablet` | Lin's cabin tablet | `room:cabin_lin` | portable, readable |
| `lin_clipboard` | Dr. Lin's clipboard | `room:quarantine_bay` | portable, readable |
| `lin_research_notes` | Lin's research notes | `room:research_lab_med` | portable, readable |
| `lin_research_reference` | Lin's research reference | `room:water_treatment_secondary` | portable, readable |
| `maintenance_terminal_cryo` | cryo maintenance terminal | `room:cryo_recycling` | portable, readable |
| `navigation_terminal_data` | navigation data terminal | `room:telescope_observation_deck` | portable, readable |
| `observation_log` | observation log | `room:observatory` | portable, readable |
| `okafor_self_interview` | Okafor's self-interview tape | `room:interrogation_room` | portable, readable |
| `okafor_unfinished_letter` | Okafor's unfinished letter | `room:cabin_okafor` | portable, readable |
| `okafors_audio_recorder` | Okafor's audio recorder | `room:security_office` | portable, readable |
| `okafors_red_book` | Okafor's red book | `room:security_office` | portable, readable |
| `patel_data_crystal_laundry` | hidden data crystal | `room:laundry_room` | portable, readable |
| `patel_formula_annotation` | Patel's formula annotation | `room:chemistry_lab` | portable, readable |
| `patel_recording_crystal` | recording crystal | `in:dr_patel_body` | portable, readable |
| `patels_data_crystal` | hidden data crystal | `room:cabin_patel` | portable, readable |
| `personal_datapad_chen` | your personal datapad | `in:personal_locker` | portable, readable |
| `pharmacy_inventory_log` | pharmacy inventory log | `room:pharmacy` | portable, readable |
| `plasma_distribution_schematic` | plasma distribution schematic | `room:plasma_conduit_junction` | portable, readable |
| `player_journal` | your personal journal | `room:cabin_chen` | portable, readable |
| `player_letter_to_self` | sealed letter | `room:cabin_chen` | portable, readable |
| `priya_journal` | Priya's journal | `in:crew_locker_14` | portable, readable |
| `quarantine_research_log` | quarantine research log | `room:specimen_quarantine` | portable, readable |
| `readyroom_terminal` | ready room terminal | `room:ready_room` | portable, readable |
| `recording_archive` | recording archive | `room:monitoring_station` | portable, readable |
| `reeves_handwritten_will` | Reeves's handwritten will | `room:captains_ready_suite` | portable, readable |
| `romano_grandmother_recipes` | grandmother's recipes | `room:cabin_romano` | portable, readable |
| `romano_recipe_diary` | Romano's recipe diary | `room:cabin_romano` | portable, readable |
| `safety_poster_annotated` | annotated safety poster | `room:chemistry_lab` | portable, readable |
| `shipping_manifests` | shipping manifests | `room:cargo_office` | portable, readable |
| `site_7_documentation` | Site 7 documentation | `room:cargo_bay_main` | portable, readable |
| `specimen_logbook` | specimen log | `room:specimen_storage` | portable, readable |
| `survivor_journal` | survivor's journal | `room:pod_monitoring_alcove` | portable, readable |
| `synthesis_protocol` | Dr. Lin's synthesis protocol | `_unplaced_` | portable, readable |
| `takamura_personnel_files` | Takamura's personnel files | `room:navigation_computer_room` | portable, readable |
| `tanaka_maintenance_log` | Tanaka's maintenance log | `room:coolant_control_h` | portable, readable |
| `use_log_terminal` | use log terminal | `room:neural_interface_chamber` | portable, readable |
| `webb_audio_log` | Webb's audio log | `room:cargo_office` | portable, readable |
| `webb_star_charts` | Webb's star charts | `room:bridge_crew_quarters` | portable, readable |
| `webb_targeting_notes` | Webb's targeting notes | `room:bridge_crew_quarters` | portable, readable |
| `xenolinguist_audio_logs` | xenolinguist's audio logs | `room:xenolinguistics_lab` | portable, readable |
| `yukis_engineering_notebook` | Yuki's engineering notebook | `room:yuki_hideout` | portable, readable |
| `yukis_journal` | Yuki's journal | `room:engineering_break_room` | portable, readable |

### Weapons (16)

| ID | Name | Location | Properties |
|----|------|----------|------------|
| `ceremonial_sidearm` | ceremonial sidearm | `room:captains_quarters` | portable, weapon, firearm |
| `flare_gun` | flare gun | `room:armory_vault` | portable, weapon |
| `handgun` | 9mm handgun | `room:armory` | portable, weapon, firearm |
| `modified_plasma_cutter` | modified plasma cutter | `room:engineering_workshop` | portable, weapon |
| `okafor_backup_weapon` | Okafor's backup weapon | `room:cabin_okafor` | portable, weapon, firearm |
| `okafors_custom_sidearm` | Okafor's custom sidearm | `room:armory_vault` | portable, weapon, firearm |
| `plasma_cutter` | plasma cutter | `room:deck_i_hub` | portable, usable, weapon, tool |
| `romano_kitchen_knife` | Romano's kitchen knife | `room:cabin_romano` | portable, weapon |
| `scalpel` | surgical scalpel | `in:medical_cabinet` | portable, weapon |
| `sedative_syringe` | sedative syringe | `room:cryo_medical` | portable, weapon, non_lethal |
| `sharp_knife` | sharp chef's knife | `room:galley` | portable, weapon |
| `tactical_rifle` | tactical rifle | `room:armory` | portable, weapon, firearm |
| `tactical_shotgun` | tactical shotgun | `room:armory_vault` | portable, weapon, firearm |
| `tear_gas_grenades` | tear gas grenades | `room:armory` | portable, weapon |
| `wrench` | heavy wrench | `room:cryo_maintenance` | portable, weapon |
| `yukis_handgun` | Yuki's handgun | `room:yuki_hideout` | portable, weapon, firearm |

### Containers (6)

| ID | Name | Location | Properties |
|----|------|----------|------------|
| `crew_locker_14` | crew locker 14 | `room:deck_i_storage` | portable, scenery, container(2) |
| `dr_patel_body` | Dr. Patel's body | `room:surgery` | portable, scenery, container(1) |
| `emergency_kit` | emergency medical kit | `room:cryo_bay` | portable, container(2) |
| `medical_cabinet` | medical cabinet | `room:cryo_medical` | portable, scenery, container(3) |
| `personal_locker` | personal locker | `room:cryo_bay` | portable, scenery, container(3) |
| `tool_belt` | maintenance tool belt | `room:cryo_maintenance` | portable, container(3) |

### Portable Items (61)

| ID | Name | Location | Properties |
|----|------|----------|------------|
| `aegis_authorization_key` | Protocol Aegis authorization key | `room:captains_ready_suite` | portable |
| `anti_radiation_meds` | anti-radiation medication | `room:pharmacy` | portable |
| `antibiotics` | broad-spectrum antibiotics | `in:medical_cabinet` | portable, usable, consumable |
| `bandages` | bandages | `in:emergency_kit` | portable, usable, consumable |
| `bio_marker_test` | bio-marker test kit | `_unplaced_` | portable |
| `bridge_access_card` | bridge access card | `room:captains_quarters` | portable |
| `bypass_chip` | bypass chip | `in:tool_belt` | portable |
| `captains_key` | captain's authorization key | `room:captains_quarters` | portable |
| `centrifuge_sample_vials` | centrifuge sample vials | `room:research_lab_med` | portable |
| `chemical_storage_locker` | chemical storage locker | `room:water_treatment_secondary` | portable |
| `clean_water_dispenser` | clean water dispenser | `room:water_treatment_secondary` | portable |
| `conductive_paste_materials` | conductive paste materials | `room:chemistry_lab` | portable |
| `coolant_repair_toolkit` | coolant repair toolkit | `room:coolant_pump_room` | portable |
| `cryo_jumpsuit` | cryo jumpsuit | `room:cryo_bay` | portable |
| `cryo_release_key` | cryo release key | `room:cryo_bay` | portable |
| `crystal_shard_sample` | crystal shard sample | `room:seed_nursery` | portable |
| `cure_reagents` | cure reagents | `room:water_treatment_secondary` | portable |
| `cure_syringe` | cure syringe | `_unplaced_` | portable, consumable |
| `deck_i_storage_key` | deck I storage key | `in:crew_locker_14` | portable |
| `diagnostic_kit` | diagnostic kit | `room:medical_bay` | portable |
| `dr_lin_silver_cross` | Dr. Lin's silver cross | `room:isolation_ward` | portable |
| `electrical_tape` | roll of electrical tape | `in:tool_belt` | portable |
| `emergency_oxygen_canister` | emergency oxygen canister | `room:emergency_airlock_i` | portable |
| `emergency_sealant` | emergency sealant canister | `room:emergency_airlock_i` | portable |
| `eva_suit` | intact EVA suit | `room:emergency_shuttle_bay` | portable |
| `explosive_charges_case` | explosive charges case | `room:armory_vault` | portable |
| `flare_bandolier` | flare bandolier | `room:armory_vault` | portable |
| `flashlight` | flashlight | `room:cryo_maintenance` | portable, usable |
| `fletcher_soldering_kit` | Fletcher's soldering kit | `room:cabin_fletcher` | portable |
| `fletcher_toolkit` | Fletcher's repair toolkit | `room:communications_relay` | portable |
| `fountain_pen` | fountain pen | `room:cargo_office` | portable |
| `hassan_fathers_watch` | Hassan's father's pocket watch | `room:cabin_hassan` | portable |
| `hazmat_suit` | hazmat suit | `room:engineering_workshop` | portable, hazmat |
| `kowalski_tool_belt` | Kowalski's tool belt | `room:garden_periphery_west` | portable |
| `medical_clearance_badge` | medical clearance badge | `room:dr_lin_office` | portable |
| `medical_scanner` | medical scanner | `room:cryo_medical` | portable, usable |
| `multitool` | engineer's multitool | `in:tool_belt` | portable |
| `painkillers` | painkillers | `room:pharmacy` | portable |
| `photo_of_beach` | photograph | `in:personal_locker` | portable |
| `pipe_sealant_canister` | pipe sealant canister | `room:plasma_conduit_junction` | portable |
| `power_cell_pack` | power cell pack | `room:engineering_workshop` | portable |
| `radiation_suit` | radiation protection suit | `room:engineering_workshop` | portable, hazmat, radiation_gear |
| `ration_pack` | emergency ration pack | `room:deck_i_storage` | portable, usable, consumable |
| `reagent_a_case` | Reagent A case | `room:pharmacy` | portable |
| `red_keycard` | red security keycard | `room:security_office` | portable |
| `repair_parts_shelf` | repair parts shelf | `room:communications_relay` | portable |
| `riot_shield` | riot shield | `room:armory_vault` | portable |
| `root_fluid_sample` | root fluid sample | `room:garden_root_network` | portable |
| `sample_garden_tissue` | Garden tissue sample | `room:hydroponics_main` | portable |
| `sealed_kepler_specimens` | sealed Kepler specimens | `room:botany_lab` | portable |
| `sedative_doses` | sedative doses | `room:pharmacy` | portable |
| `small_key_nightstand` | small silver key | `room:cabin_chen` | portable |
| `spare_eva_helmet` | spare EVA helmet | `room:emergency_airlock_i` | portable |
| `stim_injector` | stim injector | `in:emergency_kit` | portable, usable, consumable |
| `stimpack` | standard stimpack | `room:cryo_medical` | portable, usable, consumable |
| `stimpack_2` | advanced stimpack | `in:medical_cabinet` | portable, usable, consumable |
| `tactical_vest` | tactical vest | `room:armory` | portable |
| `tissue_sample_container` | tissue sample container | `room:cold_storage` | portable |
| `watch_chen` | wristwatch | `in:personal_locker` | portable |
| `yukis_backpack` | Yuki's backpack | `room:engineering_break_room` | portable |
| `yukis_canteen` | Yuki's canteen | `room:yuki_hideout` | portable |

### Scenery (Fixed) (448)

| ID | Name | Location | Properties |
|----|------|----------|------------|
| `abandoned_card_game` | abandoned card game | `room:engineering_break_room` | scenery |
| `access_panels` | access panels | `room:deck_h_junction` | scenery |
| `air_filtration_unit` | air filtration unit | `room:decontamination_shower` | scenery |
| `amber_crystal` | amber crystal | `room:aria_memory_vault` | scenery |
| `ammunition_box` | ammunition box | `room:armory` | scenery |
| `amplification_array` | signal amplification array | `room:communications_relay` | scenery |
| `antenna_tuner` | antenna tuner | `room:comms_array` | scenery |
| `arboretum_roses` | climbing roses | `room:arboretum` | scenery |
| `aria_crystal_matrix` | ARIA crystal matrix | `room:ai_core_main` | scenery |
| `aria_personal_substrate` | ARIA's personal substrate | `room:aria_memory_vault` | scenery |
| `aria_shade_interface` | ARIA-SHADE interface | `room:aria_shade_chamber` | scenery |
| `aria_terminal` | ARIA communication terminal | `room:ai_core_antechamber` | scenery |
| `artifact_pedestal` | artifact pedestal | `room:exobio_lab` | scenery |
| `astronomer_workstation` | astronomer's workstation | `room:observatory` | scenery |
| `atmospheric_containment_units` | atmospheric containment units | `room:botany_lab` | scenery |
| `atmospheric_processors` | atmospheric processors | `room:life_support_central` | scenery |
| `authorization_sign` | authorization sign | `room:exobio_lab_airlock` | scenery |
| `barricade_body` | body behind barricade | `room:gymnasium` | scenery |
| `berth_one_viewport` | Berth One viewport | `room:escape_pod_bay_lower` | scenery |
| `biohazard_bin` | biohazard disposal bin | `room:cryo_medical` | scenery |
| `biological_residue` | biological residue | `room:vent_network_i` | scenery |
| `biological_specimens` | biological specimens | `room:cold_storage` | scenery |
| `bioluminescent_moss_case` | bioluminescent moss case | `room:botany_lab` | scenery |
| `bioluminescent_roots` | bioluminescent roots | `room:garden_root_network` | scenery |
| `biometric_scanner` | biometric scanner | `room:exobio_lab_airlock` | scenery |
| `biometric_weapons_locker` | biometric weapons locker | `room:armory` | scenery |
| `birdsong_speakers` | hidden birdsong speakers | `room:arboretum` | scenery |
| `blast_door_wedge` | metal wedge | `room:engineering_junction` | scenery |
| `blood_spatters` | blood spatters | `room:security_corridor_south` | scenery |
| `blood_trail` | blood trail | `room:deck_e_junction` | scenery |
| `bloody_bed` | bloody hospital bed | `room:medical_bay` | scenery |
| `bloody_footprints` | bloody footprints | `room:cryo_corridor` | scenery |
| `bloody_handprint` | bloody handprint | `room:bridge` | scenery |
| `bloody_message` | bloody message | `room:brig` | scenery |
| `body_drawer_empty` | empty drawer | `room:morgue` | scenery |
| `body_drawer_okafor` | Okafor's drawer | `room:morgue` | scenery |
| `body_drawer_reeves` | Captain Reeves's drawer | `room:morgue` | scenery |
| `body_drawer_vasquez` | Vasquez's drawer | `room:morgue` | scenery |
| `body_in_doorway` | body in doorway | `room:deck_c_junction` | scenery |
| `boxing_ring` | boxing ring | `room:gymnasium` | scenery |
| `breathing_body_bag` | breathing body bag | `room:morgue_freezer` | scenery |
| `bridge_blast_door` | bridge blast door | `room:deck_a_junction` | scenery |
| `bridge_crew_lockers` | bridge crew lockers | `room:bridge_crew_quarters` | scenery |
| `bridge_hud` | bridge heads-up display | `room:bridge` | scenery |
| `brig_body` | body in cell | `room:brig` | scenery |
| `broken_door_frame` | broken door frame | `room:crew_corridor` | scenery |
| `broken_dryer_note` | note on broken dryer | `room:laundry_room` | scenery |
| `broken_mining_container` | broken container | `room:cargo_bay_main` | scenery |
| `broken_wall_panels` | broken wall panels | `room:garden_periphery_east` | scenery |
| `brown_dwarf_closeup` | brown dwarf close-up view | `room:telescope_observation_deck` | scenery |
| `brown_dwarf_view` | view of brown dwarf | `room:observation_lounge` | scenery |
| `builder_translation_matrix` | Builder translation matrix | `room:xenolinguistics_lab` | scenery |
| `builders_origin_chart` | Builders' origin chart | `room:telescope_observation_deck` | scenery |
| `bulkhead_carved_message` | carved bulkhead message | `room:bridge_crew_quarters` | scenery |
| `bullet_casings` | spent bullet casings | `room:deck_i_storage` | scenery |
| `bullet_hole_console` | shattered control console | `room:cryo_control` | scenery |
| `cabin_directory` | cabin directory | `room:crew_corridor` | scenery |
| `camera_19_feed` | Camera 19 feed | `room:monitoring_station` | scenery |
| `camera_control_console` | camera control console | `room:monitoring_station` | scenery |
| `captains_bed` | Captain's bed | `room:captains_quarters` | scenery |
| `captains_chair` | captain's chair | `room:bridge` | scenery |
| `captains_glasses` | reading glasses | `room:captains_quarters` | scenery |
| `captains_philosophy_book` | book of philosophy | `room:captains_quarters` | scenery |
| `captains_photo` | Captain's photograph | `room:captains_quarters` | scenery |
| `cargo_elevator` | cargo elevator | `room:cargo_bay_main` | scenery |
| `cargo_manifest` | cargo manifest | `room:cargo_access` | scenery |
| `cargo_manifest_terminal` | cargo manifest terminal | `room:cargo_bay_main` | scenery |
| `cargo_office_terminal` | cargo office terminal | `room:cargo_office` | scenery |
| `centrifuge` | centrifuge | `room:main_lab` | scenery |
| `chapel_altar` | chapel altar | `room:chapel` | scenery |
| `chemical_analysis_station` | chemical analysis station | `room:research_lab_med` | scenery |
| `chemical_spray_nozzles` | chemical spray nozzles | `room:decontamination_shower` | scenery |
| `chemical_sterilizer` | chemical sterilizer | `room:water_processing` | scenery |
| `chemical_synthesis_station` | chemical synthesis station | `room:chemistry_lab` | scenery |
| `chess_set_midgame` | chess set mid-game | `room:recreation_lounge` | scenery |
| `childs_drawing` | child's drawing | `room:chapel` | scenery |
| `chrysalis_figure` | chrysalis figure | `room:chrysalis_chamber` | scenery |
| `claw_marked_walls` | claw-marked walls | `room:sealed_corridor_c` | scenery |
| `claw_marks_glass` | claw marks in glass | `room:cryo_pod_12_interior` | scenery |
| `clean_polymer_walls` | clean polymer walls | `room:deck_b_junction` | scenery |
| `clean_walls` | clean walls | `room:deck_d_hub` | scenery |
| `co2_scrubber_bank` | CO2 scrubber bank | `room:life_support_central` | scenery |
| `collapsed_ceiling_panels` | collapsed ceiling panels | `room:sealed_corridor_c` | scenery |
| `colored_yarn_connections` | colored yarn connections | `room:xenolinguistics_lab` | scenery |
| `combat_barricade_remains` | combat barricade remains | `room:security_corridor_south` | scenery |
| `comfort_couches` | comfort couches | `room:observation_lounge` | scenery |
| `comms_main_console` | communications console | `room:comms_array` | scenery |
| `conduit_valve_controls` | conduit valve controls | `room:plasma_conduit_junction` | scenery |
| `conference_projector` | holographic projector | `room:conference_room` | scenery |
| `conference_table` | conference table | `room:conference_room` | scenery |
| `confession_booth_writing` | confession booth writing | `room:chapel` | scenery |
| `confiscated_effects_locker` | confiscated effects locker | `room:armory` | scenery |
| `containment_field` | containment field | `room:exobio_lab` | scenery |
| `containment_field_aria` | ARIA's containment field | `room:ai_core_main` | scenery |
| `containment_units` | containment units | `room:specimen_storage` | scenery |
| `control_chair` | duty chair | `room:cryo_control` | scenery |
| `coolant_control_panel` | coolant control panel | `room:coolant_control_h` | scenery |
| `coolant_pressure_gauge` | coolant pressure gauge | `room:reactor_antechamber` | scenery |
| `coolant_pump_two` | Pump Two | `room:coolant_pump_room` | scenery |
| `coolant_reservoir` | coolant reservoir | `room:coolant_pump_room` | scenery |
| `coolant_valves` | coolant valves | `room:coolant_control_h` | scenery |
| `cooling_fan_arrays` | cooling fan arrays | `room:navigation_computer_room` | scenery |
| `core_catwalk` | core catwalk | `room:ai_core_main` | scenery |
| `core_door` | AI core door | `room:ai_core_antechamber` | scenery |
| `corridor_keypad` | storage room keypad | `room:cryo_corridor` | scenery |
| `corrupted_data_walls` | corrupted data walls | `room:aria_shade_chamber` | scenery |
| `corrupted_trajectory_display` | corrupted trajectory display | `room:navigation_computer_room` | scenery |
| `course_readout` | course readout | `room:reactor_antechamber` | scenery |
| `cracked_filtration_tank` | cracked filtration tank | `room:water_processing` | scenery |
| `crew_directory` | crew directory | `room:deck_c_junction` | scenery |
| `crew_roster_display` | crew roster display | `room:medical_bay` | scenery |
| `crushed_escape_pod` | crushed escape pod | `room:escape_pod_bay_lower` | scenery |
| `cryo_status_display` | cryo status display | `room:cryo_control` | scenery |
| `crystal_growth_trail` | crystal growth trail | `room:specimen_storage` | scenery |
| `crystalline_containers` | crystalline-covered containers | `room:cold_storage` | scenery |
| `crystalline_storage` | crystalline storage | `room:quantum_archive` | scenery |
| `crystalline_web` | crystalline web | `room:chrysalis_chamber` | scenery |
| `cutting_board_stain` | stained cutting board | `room:galley` | scenery |
| `damaged_plasma_conduit` | damaged plasma conduit | `room:plasma_conduit_junction` | scenery |
| `damaged_relay_unit` | damaged relay unit | `room:communications_relay` | scenery |
| `dark_smear` | dark smear | `room:cryo_maintenance` | scenery |
| `dartboard_photo` | dartboard with photo | `room:recreation_lounge` | scenery |
| `data_conduit_humming` | humming data conduit | `room:deck_h_junction` | scenery |
| `data_walls` | data walls | `room:ai_core_antechamber` | scenery |
| `daughter_crystals` | daughter crystals | `room:seed_nursery` | scenery |
| `dead_engineer` | engineer's body | `room:deck_i_hub` | scenery |
| `deck_monitoring_console` | deck monitoring console | `room:life_support_central` | scenery |
| `decon_control_panel` | decontamination control panel | `room:decontamination_shower` | scenery |
| `decon_status_display` | decontamination status display | `room:decontamination_shower` | scenery |
| `decontamination_chamber` | decontamination chamber | `room:exobio_lab_airlock` | scenery |
| `decryption_terminals` | decryption terminals | `room:xenolinguistics_lab` | scenery |
| `detergent_dispenser` | detergent dispenser | `room:laundry_room` | scenery |
| `directional_signs` | directional signs | `room:deck_b_junction` | scenery |
| `discarded_mask` | discarded surgical mask | `room:medical_corridor` | scenery |
| `dr_lin_body` | Dr. Lin's body | `room:isolation_ward` | scenery |
| `dr_lin_photo` | Dr. Lin's photograph | `room:dr_lin_office` | scenery |
| `dried_cryo_residue` | dried cryo residue | `room:cryo_pod_12_interior` | scenery |
| `dried_food_trays` | dried food trays | `room:mess_hall` | scenery |
| `duty_roster_wall` | duty roster | `room:comms_array` | scenery |
| `duty_rotation_schedule` | duty rotation schedule | `room:bridge_crew_quarters` | scenery |
| `eastern_vine_growth` | eastern vine growth | `room:garden_periphery_east` | scenery |
| `electric_candles` | electric candles | `room:chapel` | scenery |
| `electrode_crown` | electrode crown | `room:neural_interface_chamber` | scenery |
| `elevator_panel` | elevator control panel | `room:deck_i_hub` | scenery |
| `emergency_beacon_unit` | emergency beacon unit | `room:bridge_escape_pod` | scenery |
| `emergency_override_keypad` | emergency override keypad | `room:propulsion_access` | scenery |
| `emergency_oxygen_reserves` | emergency oxygen reserves | `room:life_support_central` | scenery |
| `emergency_purge_switch` | emergency purge switch | `room:specimen_quarantine` | scenery |
| `emergency_shutdown` | emergency shutdown | `room:reactor_catwalk` | scenery |
| `emergency_shutdown_terminal` | emergency shutdown terminal | `room:reactor_core_interior` | scenery |
| `empty_cells` | empty cells | `room:brig` | scenery |
| `empty_coffee_cups` | empty coffee cups | `room:security_office` | scenery |
| `empty_water_bottles` | empty water bottles | `room:gymnasium` | scenery |
| `energy_readings_display` | energy readings display | `room:exobio_lab` | scenery |
| `engine_blast_door` | engine blast door | `room:propulsion_access` | scenery |
| `engineering_catwalks` | engineering catwalks | `room:main_engineering` | scenery |
| `environmental_control_interface` | environmental control interface | `room:life_support_central` | scenery |
| `environmental_readouts` | environmental readouts | `room:data_nexus` | scenery |
| `escape_pod_controls` | escape pod controls | `room:bridge_escape_pod` | scenery |
| `escape_pod_manifest` | escape pod manifest | `room:bridge_escape_pod` | scenery |
| `escape_shuttle` | escape shuttle | `room:emergency_shuttle_bay` | scenery |
| `eva_equipment_rack` | EVA equipment rack | `room:emergency_airlock_i` | scenery |
| `evidence_bag_childs_drawing` | evidence bag - child's drawing | `room:evidence_locker` | scenery |
| `evidence_bag_photos` | evidence bag - photographs | `room:evidence_locker` | scenery |
| `evidence_bag_silver_vial` | evidence bag - silver vial | `room:evidence_locker` | scenery |
| `examination_table` | examination table | `room:cryo_medical` | scenery |
| `exercise_machines` | exercise machines | `room:gymnasium` | scenery |
| `explorer_portraits` | explorer portraits | `room:deck_a_junction` | scenery |
| `fabricator_unit` | fabricator unit | `room:engineering_workshop` | scenery |
| `failing_backup_pump` | failing backup pump | `room:coolant_control_h` | scenery |
| `fiber_optic_bundles` | fiber optic bundles | `room:data_nexus` | scenery |
| `filtration_system` | filtration system | `room:water_processing` | scenery |
| `fletcher_aurora_poster` | aurora poster | `room:cabin_fletcher` | scenery |
| `fletcher_body` | Fletcher's body | `room:comms_array` | scenery |
| `fletcher_coffee_cups` | Fletcher's coffee cups | `room:cabin_fletcher` | scenery |
| `fletcher_pocket_items` | items from Fletcher's pocket | `room:comms_array` | scenery |
| `fletcher_radio_equipment` | Fletcher's radio equipment | `room:cabin_fletcher` | scenery |
| `flickering_green_light` | flickering emergency light | `room:deck_h_junction` | scenery |
| `flush_data_terminals` | flush data terminals | `room:conference_room` | scenery |
| `forgotten_uniforms` | forgotten uniforms | `room:laundry_room` | scenery |
| `forward_viewport` | forward viewport | `room:bridge` | scenery |
| `fractal_fern_sample` | fractal fern sample | `room:botany_lab` | scenery |
| `fragment_readout_display` | fragment readout display | `room:specimen_quarantine` | scenery |
| `framed_degree` | framed degree | `room:dr_lin_office` | scenery |
| `freezer_shelving` | freezer shelving | `room:morgue_freezer` | scenery |
| `fresh_sandwich` | suspiciously fresh sandwich | `room:cargo_office` | scenery |
| `frosted_name_labels` | frosted name labels | `room:morgue_freezer` | scenery |
| `frozen_body_bags` | frozen body bags | `room:morgue_freezer` | scenery |
| `frozen_coffee_cup` | frozen coffee cup | `room:cryo_control` | scenery |
| `frozen_comedy_screen` | frozen entertainment screen | `room:recreation_lounge` | scenery |
| `fume_hoods` | fume hoods | `room:chemistry_lab` | scenery |
| `functioning_work_station` | functioning work station | `room:garden_periphery_west` | scenery |
| `fusion_core_plasma` | fusion core plasma | `room:reactor_core_interior` | scenery |
| `garden_heart_nexus` | Garden heart nexus | `room:heart_of_garden` | scenery |
| `garden_spores` | Garden spores | `room:hydroponics_main` | scenery |
| `germination_equipment` | original germination equipment | `room:seed_nursery` | scenery |
| `green_override_button` | green override button | `room:cryo_bay` | scenery, usable |
| `gym_barricade` | gym barricade | `room:gymnasium` | scenery |
| `half_sandwich` | half-eaten sandwich | `room:engineering_workshop` | scenery |
| `hanging_fern_baskets` | hanging fern baskets | `room:arboretum` | scenery |
| `hassan_cairo_photos` | photographs of Cairo | `room:cabin_hassan` | scenery |
| `hassan_model_ships` | Hassan's model ships | `room:cabin_hassan` | scenery |
| `hassan_star_chart` | Hassan's star chart | `room:cabin_hassan` | scenery |
| `heat_shield_controls` | heat shield controls | `room:main_engine_room` | scenery |
| `helm_station` | helm station | `room:bridge` | scenery |
| `hidden_compartment` | hidden compartment | `room:quantum_archive` | scenery |
| `hidden_panel_door` | hidden panel | `room:pod_monitoring_alcove` | scenery |
| `holographic_cell_model` | holographic cell model | `room:cabin_chen` | scenery |
| `holographic_game_board` | holographic game board | `room:recreation_lounge` | scenery |
| `holographic_molecule` | holographic molecule | `room:main_lab` | scenery |
| `holographic_receptionist` | holographic receptionist | `room:medical_corridor` | scenery |
| `holographic_star_map` | holographic star map | `room:observatory` | scenery |
| `hull_viewport` | hull viewport | `room:emergency_airlock_i` | scenery |
| `hydroponics_airlock_glass` | hydroponics glass | `room:hydroponics_entry` | scenery |
| `hydroponics_readout` | hydroponics readout | `room:hydroponics_entry` | scenery |
| `ice_core_samples` | ice core samples | `room:specimen_storage` | scenery |
| `immunosuppressants` | immunosuppressants | `room:pharmacy` | scenery |
| `incorporated_couple` | incorporated couple | `room:garden_periphery_east` | scenery |
| `incorporated_crew` | incorporated crew | `room:hydroponics_main` | scenery |
| `independent_filtration` | independent filtration system | `room:water_treatment_secondary` | scenery |
| `industrial_lights` | industrial lights | `room:cargo_access` | scenery |
| `industrial_washers` | industrial washing machines | `room:laundry_room` | scenery |
| `infected_container` | infected container | `room:lower_cargo` | scenery |
| `intact_escape_pod` | intact escape pod | `room:escape_pod_bay_lower` | scenery |
| `interrogation_chairs` | interrogation chairs | `room:interrogation_room` | scenery |
| `interrogation_table` | interrogation table | `room:interrogation_room` | scenery |
| `interrupted_meals` | interrupted meals | `room:mess_hall` | scenery |
| `isolation_cell_one_scratches` | Cell One scratches | `room:isolation_ward` | scenery |
| `isolation_cell_three_crack` | Cell Three crack | `room:isolation_ward` | scenery |
| `isolation_cell_two_body` | Cell Two body | `room:isolation_ward` | scenery |
| `iv_stand` | IV stand | `room:medical_bay` | scenery |
| `jammed_outer_door` | jammed outer door | `room:emergency_airlock_i` | scenery |
| `japanese_maple_tree` | Japanese maple tree | `room:arboretum` | scenery |
| `junction_box` | junction box | `room:cryo_maintenance` | scenery |
| `junction_sign` | deck directory sign | `room:deck_d_hub` | scenery |
| `knife_block` | knife block | `room:galley` | scenery |
| `lin_clothes` | strewn clothes | `room:cabin_lin` | scenery |
| `lin_cross` | Greek Orthodox cross | `room:cabin_lin` | scenery |
| `lin_photo_frame` | photo frame | `room:cabin_lin` | scenery |
| `lin_wall_safe` | wall safe | `room:dr_lin_office` | scenery |
| `lin_wine_glass` | glass of wine | `room:cabin_lin` | scenery |
| `liquid_nitrogen_pipes` | liquid nitrogen pipes | `room:coolant_control_h` | scenery |
| `liquor_cabinet` | liquor cabinet | `room:ready_room` | scenery |
| `magnetic_field_emitter` | magnetic field emitter | `room:aria_memory_vault` | scenery |
| `maintenance_hatch_hub` | maintenance hatch | `room:deck_i_hub` | scenery |
| `maintenance_ladder` | maintenance ladder | `room:cryo_maintenance` | scenery |
| `manual_overload_switch` | manual overload switch | `room:reactor_core_interior` | scenery |
| `manual_override_switch` | manual override switch | `room:reactor_catwalk` | scenery |
| `master_drive_control` | master drive control | `room:main_engine_room` | scenery |
| `medical_scanner_2` | wall-mounted scanner | `room:medical_bay` | scenery |
| `medical_signs` | medical signage | `room:medical_corridor` | scenery |
| `memorial_bench` | memorial bench | `room:arboretum` | scenery |
| `memory_projections` | memory projections | `room:aria_memory_vault` | scenery |
| `menu_display` | menu display | `room:mess_hall` | scenery |
| `mission_records` | mission records | `room:quantum_archive` | scenery |
| `molecular_whiteboard` | molecular whiteboard | `room:research_lab_med` | scenery |
| `monitor_wall` | monitor wall | `room:monitoring_station` | scenery |
| `monitoring_stations` | monitoring stations | `room:main_engineering` | scenery |
| `morgue_logbook` | morgue logbook | `room:morgue` | scenery |
| `mortician_table_body` | covered body | `room:morgue` | scenery |
| `nav_module_reset_panel` | navigation module reset panel | `room:navigation_computer_room` | scenery |
| `nav_station` | navigation station | `room:bridge` | scenery |
| `navigation_override` | navigation override | `room:main_engine_room` | scenery |
| `navigation_processing_banks` | navigation processing banks | `room:navigation_computer_room` | scenery |
| `negative_pressure_walls` | negative-pressure walls | `room:specimen_quarantine` | scenery |
| `network_switch_racks` | network switch racks | `room:data_nexus` | scenery |
| `neural_interface_chair` | neural interface chair | `room:neural_interface_chamber` | scenery |
| `nexus_terminal` | nexus central terminal | `room:data_nexus` | scenery |
| `numbered_doors` | numbered cabin doors | `room:crew_corridor` | scenery |
| `observation_bar` | observation bar | `room:observation_lounge` | scenery |
| `observation_viewport` | observation viewport | `room:observation_lounge` | scenery |
| `observatory_telescope` | main telescope | `room:observatory` | scenery |
| `okafor_calendar` | Okafor's calendar | `room:cabin_okafor` | scenery |
| `okafor_desk` | Okafor's desk | `room:security_office` | scenery |
| `okafor_family_photo` | Okafor's family photo | `room:security_office` | scenery |
| `okafor_family_photos` | Okafor's family photographs | `room:cabin_okafor` | scenery |
| `okafor_prayer_rug` | Okafor's prayer rug | `room:cabin_okafor` | scenery |
| `okafor_uniforms` | Okafor's uniforms | `room:cabin_okafor` | scenery |
| `okafors_cold_coffee` | Okafor's cold coffee | `room:monitoring_station` | scenery |
| `one_way_mirror` | one-way mirror | `room:interrogation_room` | scenery |
| `organic_substrate` | organic substrate | `room:seed_nursery` | scenery |
| `organic_wall_film` | organic wall film | `room:sealed_corridor_c` | scenery |
| `original_hydroponics` | original hydroponics equipment | `room:garden_periphery_west` | scenery |
| `original_seed_location` | original Seed location | `room:lower_cargo` | scenery |
| `ornate_carpet` | ornate carpet | `room:deck_c_junction` | scenery |
| `overgrown_plants` | overgrown plants | `room:hydroponics_main` | scenery |
| `overload_glass_case` | overload switch glass case | `room:reactor_core_interior` | scenery |
| `overturned_chairs` | overturned chairs | `room:conference_room` | scenery |
| `patels_desk` | Patel's desk | `room:cabin_patel` | scenery |
| `patels_wall_safe` | Patel's wall safe | `room:cabin_patel` | scenery |
| `patels_warning_note` | warning note | `room:main_lab` | scenery |
| `personal_bed` | your bed | `room:cabin_chen` | scenery |
| `petri_dishes` | petri dishes | `room:main_lab` | scenery |
| `photo_of_stranger` | framed photograph | `room:cabin_chen` | scenery |
| `physical_book_collection` | book collection | `room:recreation_lounge` | scenery |
| `pipe_network` | pipe network | `room:engineering_junction` | scenery |
| `plant_response_recorder` | plant response recorder | `room:botany_lab` | scenery |
| `plasma_drive_core` | plasma drive core | `room:main_engine_room` | scenery |
| `player_nightstand` | your nightstand | `room:cabin_chen` | scenery |
| `player_uniforms` | uniforms | `room:cabin_chen` | scenery |
| `pod_12_damaged` | Pod 12 | `room:cryo_storage` | scenery |
| `pod_12_headrest` | pod headrest | `room:cryo_pod_12_interior` | scenery |
| `pod_23` | your cryo pod | `room:cryo_bay` | scenery |
| `pod_47` | Pod 47 | `room:cryo_storage` | scenery |
| `pod_diagnostic_panel` | pod diagnostic panel | `room:bridge_escape_pod` | scenery |
| `pod_launch_console` | pod launch console | `room:escape_pod_bay_lower` | scenery |
| `pod_viewport` | pod viewport | `room:bridge_escape_pod` | scenery |
| `portable_heater` | portable heater | `room:deck_i_storage` | scenery |
| `powerful_telescope` | observation telescope | `room:telescope_observation_deck` | scenery |
| `prep_island` | prep island | `room:galley` | scenery |
| `presentation_queue` | presentation queue | `room:conference_room` | scenery |
| `preservation_racks` | preservation racks | `room:cold_storage` | scenery |
| `primary_control_station` | primary control station | `room:main_engineering` | scenery |
| `prisoner_personal_items` | prisoner items | `room:brig` | scenery |
| `propulsion_warning_sign` | propulsion warning sign | `room:propulsion_access` | scenery |
| `pump_control_panel` | pump control panel | `room:coolant_pump_room` | scenery |
| `pump_diagnostic_readout` | pump diagnostic readout | `room:coolant_pump_room` | scenery |
| `pump_station` | pump station | `room:water_processing` | scenery |
| `quantum_processors` | quantum processors | `room:ai_core_main` | scenery |
| `quarantine_cell_1` | quarantine cell 1 | `room:quarantine_bay` | scenery |
| `quarantine_cell_2` | quarantine cell 2 | `room:quarantine_bay` | scenery |
| `quarantine_cell_3` | quarantine cell 3 | `room:quarantine_bay` | scenery |
| `quarantine_containment_jar` | quarantine containment jar | `room:specimen_quarantine` | scenery |
| `quarantine_control_panel` | quarantine control panel | `room:quarantine_airlock` | scenery |
| `quarantine_firewall` | quarantine firewall | `room:aria_shade_chamber` | scenery |
| `quarantine_glass` | quarantine observation glass | `room:quarantine_airlock` | scenery |
| `radiation_warning_sign` | radiation warning sign | `room:engineering_junction` | scenery |
| `ransacked_drawer` | ransacked drawer | `room:cabin_patel` | scenery |
| `ration_wrapper_stack` | stacked ration wrappers | `room:pod_monitoring_alcove` | scenery |
| `ration_wrappers` | ration wrappers | `room:cryo_corridor` | scenery |
| `raw_sensor_feed_terminal` | raw sensor feed terminal | `room:navigation_computer_room` | scenery |
| `reactor_control_interface` | reactor control interface | `room:reactor_antechamber` | scenery |
| `reactor_control_rods` | reactor control rods | `room:reactor_core_interior` | scenery |
| `reactor_core` | reactor core | `room:main_engineering` | scenery |
| `reagent_bottles` | reagent bottles | `room:chemistry_lab` | scenery |
| `recreation_body` | body in recreation lounge | `room:recreation_lounge` | scenery |
| `recycling_pumps` | recycling pumps | `room:cryo_recycling` | scenery |
| `recycling_tank_cracked` | cracked recycling tank | `room:cryo_recycling` | scenery |
| `red_spraypaint_warning` | red spray paint warning | `room:cabin_patel` | scenery |
| `reeves_cot` | Reeves's military cot | `room:captains_ready_suite` | scenery |
| `reeves_scotch_bottle` | bottle of Scotch | `room:captains_ready_suite` | scenery |
| `reeves_son_photo` | photograph of Reeves's son | `room:captains_ready_suite` | scenery |
| `reeves_strongbox` | Reeves's strongbox | `room:captains_ready_suite` | scenery |
| `refrigeration_unit` | refrigeration unit | `room:galley` | scenery |
| `relay_diagnostic_panel` | relay diagnostic panel | `room:communications_relay` | scenery |
| `religious_icons_wall` | religious icons | `room:chapel` | scenery |
| `research_centrifuge` | research centrifuge | `room:research_lab_med` | scenery |
| `research_microscope` | research microscope | `room:main_lab` | scenery |
| `research_microscopes` | research microscopes | `room:research_lab_med` | scenery |
| `restraint_harnesses` | restraint harnesses | `room:bridge_escape_pod` | scenery |
| `romano_cookbooks` | Romano's cookbooks | `room:cabin_romano` | scenery |
| `romano_naples_photos` | photographs of Naples | `room:cabin_romano` | scenery |
| `romano_spice_collection` | Romano's spice collection | `room:cabin_romano` | scenery |
| `root_junction_node` | root junction node | `room:garden_root_network` | scenery |
| `rooted_deck_plating` | rooted deck plating | `room:heart_of_garden` | scenery |
| `rotten_seafood` | rotten seafood | `room:galley` | scenery |
| `safety_override` | safety override | `room:neural_interface_chamber` | scenery |
| `safety_poster_defaced` | defaced safety poster | `room:engineering_break_room` | scenery |
| `sample_vials` | sample vials | `room:main_lab` | scenery |
| `scattered_mining_equipment` | mining equipment | `room:cargo_bay_main` | scenery |
| `scattered_papers` | scattered papers | `room:dr_lin_office` | scenery |
| `scattered_research_notes` | research notes | `room:cabin_patel` | scenery |
| `scorch_marks` | scorch marks | `room:deck_e_junction` | scenery |
| `scorched_corridor_walls` | scorched walls | `room:security_corridor_south` | scenery |
| `scratched_rungs` | scratched rungs | `room:engineering_vent_access` | scenery |
| `secondary_control_station` | secondary control station | `room:reactor_catwalk` | scenery |
| `secondary_seed_fragment` | secondary Seed fragment | `room:specimen_quarantine` | scenery |
| `security_camera_feeds` | security camera feeds | `room:data_nexus` | scenery |
| `security_cameras_smashed` | smashed cameras | `room:deck_e_junction` | scenery |
| `sensor_array` | sensor array | `room:observatory` | scenery |
| `seven_place_settings` | seven place settings | `room:mess_hall` | scenery |
| `shade_terminals` | SHADE terminals | `room:aria_shade_chamber` | scenery |
| `shattered_container` | shattered container | `room:specimen_storage` | scenery |
| `shattered_helmet` | shattered EVA helmet | `room:emergency_shuttle_bay` | scenery |
| `shell_casing_carpet` | shell casings on floor | `room:security_corridor_south` | scenery |
| `ship_model` | sailing ship model | `room:captains_quarters` | scenery |
| `shredded_padding` | shredded pod padding | `room:cryo_pod_12_interior` | scenery |
| `shuttle_fuel_gauge` | shuttle fuel gauge | `room:emergency_shuttle_bay` | scenery |
| `signal_conduit_severed` | severed signal conduit | `room:communications_relay` | scenery |
| `signal_warning_whiteboard` | warning whiteboard | `room:xenolinguistics_lab` | scenery |
| `silver_chain` | silver chain | `room:dr_lin_office` | scenery |
| `silver_grey_residue` | silver-grey residue | `room:cryo_pod_12_interior` | scenery |
| `silver_threads_fluid` | silver threads in fluid | `room:cryo_recycling` | scenery |
| `silver_threads_vent` | silver threads in ventilation | `room:vent_network_i` | scenery |
| `silver_veined_crystal` | silver-veined crystal | `room:heart_of_garden` | scenery |
| `situation_board_timeline` | situation board | `room:tactical_operations` | scenery |
| `sleeping_bag_under_table` | sleeping bag under table | `room:engineering_break_room` | scenery |
| `spare_parts_bin` | spare parts bin | `room:engineering_workshop` | scenery |
| `sparking_panel` | sparking wall panel | `room:cryo_bay` | scenery |
| `spent_shell_casing_bridge` | spent shell casing | `room:bridge` | scenery |
| `spent_shell_casings` | spent shell casings | `room:deck_e_junction` | scenery |
| `split_deck_plating` | split deck plating | `room:garden_root_network` | scenery |
| `spore_density_reader` | spore density reader | `room:seed_nursery` | scenery |
| `status_monitors` | status monitors | `room:ready_room` | scenery |
| `stone_fountain` | stone fountain | `room:arboretum` | scenery |
| `structural_beam_fallen` | fallen structural beam | `room:escape_pod_bay_lower` | scenery |
| `structural_integrity_readout` | structural integrity readout | `room:tactical_operations` | scenery |
| `surgery_tray` | surgery tray | `room:surgery` | scenery |
| `surgical_robot` | surgical robot arm | `room:surgery` | scenery |
| `surgical_saw` | surgical bone saw | `room:surgery` | scenery |
| `surgical_tools` | surgical tools | `room:medical_bay` | scenery |
| `tactical_coffee_mugs` | coffee mugs | `room:tactical_operations` | scenery |
| `tactical_holographic_display` | tactical holographic display | `room:tactical_operations` | scenery |
| `tactical_map_contamination` | tactical contamination map | `room:security_office` | scenery |
| `tactical_station` | tactical station | `room:bridge` | scenery |
| `targeting_analysis` | targeting analysis workstation | `room:observatory` | scenery |
| `telescope_gimbal` | telescope gimbal | `room:telescope_observation_deck` | scenery |
| `temperature_controls` | temperature controls | `room:cold_storage` | scenery |
| `temperature_regulators` | temperature regulators | `room:life_support_central` | scenery |
| `tendril_growth` | black tendrils | `room:lower_cargo` | scenery |
| `test_tube_samples` | test tube samples | `room:exobio_lab` | scenery |
| `the_artifact` | the Seed | `room:exobio_lab` | scenery |
| `thermal_bedroll` | thermal bedroll | `room:pod_monitoring_alcove` | scenery |
| `thermal_blankets` | thermal blankets | `room:deck_i_storage` | scenery |
| `thin_vine_lattice` | thin vine lattice | `room:garden_periphery_west` | scenery |
| `thrust_regulators` | thrust regulators | `room:main_engine_room` | scenery |
| `thruster_status_panel` | thruster status panel | `room:reactor_antechamber` | scenery |
| `torn_carpet_section` | torn carpet | `room:sealed_corridor_c` | scenery |
| `torn_uniform_scrap` | torn uniform scrap | `room:deck_i_storage` | scenery |
| `toxic_coolant_puddle` | toxic coolant puddle | `room:coolant_pump_room` | scenery |
| `transformation_tissue` | transformation tissue | `room:chrysalis_chamber` | scenery |
| `transmit_key` | transmit key | `room:comms_array` | scenery |
| `unsorted_laundry_baskets` | unsorted laundry baskets | `room:laundry_room` | scenery |
| `uv_light_arrays` | UV light arrays | `room:decontamination_shower` | scenery |
| `valve_wheels` | valve wheels | `room:cryo_recycling` | scenery |
| `velocity_vector_readout` | velocity vector readout | `room:telescope_observation_deck` | scenery |
| `vent_ladder_rungs` | vent ladder rungs | `room:engineering_vent_access` | scenery |
| `vent_shaft_branch` | vent shaft branch | `room:vent_network_i` | scenery |
| `vent_shaft_branches` | vent shaft branches | `room:engineering_vent_access` | scenery |
| `ventilation_grate_floor` | ventilation grate | `room:specimen_storage` | scenery |
| `viewport_brown_dwarf` | viewport overlooking the brown dwarf | `room:emergency_shuttle_bay` | scenery |
| `visitor_chairs` | visitor chairs | `room:ready_room` | scenery |
| `voice_speaker_taped` | taped speaker | `room:deck_b_junction` | scenery |
| `wall_graffiti_days` | wall graffiti | `room:pod_monitoring_alcove` | scenery |
| `warning_signs_multilang` | warning signs | `room:quarantine_airlock` | scenery |
| `water_purge_control` | water purge control | `room:water_processing` | scenery |
| `water_quality_readout` | water quality readout | `room:water_treatment_secondary` | scenery |
| `weapons_systems_panels` | weapons systems panels | `room:tactical_operations` | scenery |
| `webb_coffee_mug` | Webb's coffee mug | `room:cargo_office` | scenery |
| `whiteboard_equations` | whiteboard equations | `room:main_lab` | scenery |
| `working_coffee_maker` | working coffee maker | `room:engineering_break_room` | scenery |
| `workshop_tablet` | workshop tablet | `room:engineering_workshop` | scenery |
| `wrong_plant_patterns` | plant patterns | `room:hydroponics_entry` | scenery |
| `xenobiology_texts` | xenobiology textbooks | `room:cabin_chen` | scenery |
| `yukis_family_photo` | Yuki's family photo | `room:yuki_hideout` | scenery |
| `yukis_marker_note` | Yuki's marker note | `room:decontamination_shower` | scenery |
| `yukis_sleeping_bag` | Yuki's sleeping bag | `room:yuki_hideout` | scenery |
| `yukis_water_filter` | Yuki's water filter | `room:yuki_hideout` | scenery |

---

## 7. Readable Items (Logs & Journals)

Full reference of every log, journal, and readable item in the game.
Use this to verify narrative content or trace story reveals.

### `archive_terminal` — archive terminal

```
═════════════════════════════════════════════════════
   QUANTUM ARCHIVE - UNREDACTED MISSION RECORDS
   [Access granted by ARIA - Highest Authority]
═════════════════════════════════════════════════════

You browse the archive, which contains every piece of data ARIA ever processed.

[RECORD 47-A: Site 7 Derelict, Initial Survey]

The derelict alien vessel at Kepler-442b, Site 7, was NOT the source of the Lazarus Signal. It was a TOMB. The signal was being BROADCAST by the Seed, as a lure. The 

[... truncated, full length: 2350 chars ...]
```

### `audio_recording_equipment` — audio recording equipment

```
═════════════════════════════════════════════════════
   AUDIO RECORDING EQUIPMENT
   Interrogation Room, Security Deck
═════════════════════════════════════════════════════

MODEL: Daedalus R-7 Reel-to-Reel Recorder
FORMAT: Analog magnetic tape (deliberately low-tech)
CAPACITY: 12 hours per reel at standard speed
STATUS: Operational. Current reel: 73% used.

DESIGN NOTE: Analog recording equipment was specified
for the interrogation room as a security measure.
Analog tape cannot be remotely acc

[... truncated, full length: 757 chars ...]
```

### `autopsy_datapad` — autopsy datapad

**Triggers event on read:** `event_read_autopsy`

```
═════════════════════════════════════════════════════
   AUTOPSY NOTES - SUBJECT: PATEL, R.
   Physician: Dr. Sarah Lin
═════════════════════════════════════════════════════

Subject: Dr. Raj Patel, Exobiologist
Time of Death: Day 422, 19:47 ship time
Cause of Death: Gunshot wound, anterior chest, single round, 
                fired from close range. Consistent with suicide.

POST-MORTEM FINDINGS:

Subject's cardiovascular system shows extensive crystalline infiltration. Hybrid organic-mineral 

[... truncated, full length: 1427 chars ...]
```

### `ayele_research_terminal` — Ayele's research terminal

```
═════════════════════════════════════════════════════
   DR. AYELE'S RESEARCH TERMINAL
   Botany Lab, ISV Prometheus
═════════════════════════════════════════════════════

RESEARCH LOG - Kepler Flora Sentience Study
Dr. Miriam Ayele, Botanist

Day 396: Beginning controlled response tests on Kepler
  specimens. Standard stimuli: light, sound, vibration.
  Results: Response patterns significantly more complex
  than any terrestrial plant species. Electrical activity
  in root systems resembles neu

[... truncated, full length: 1434 chars ...]
```

### `captains_recorder` — Captain's recording device

```
═════════════════════════════════════════════════════
   PERSONAL RECORDING - CAPT. MARCUS REEVES
   FINAL MESSAGE
═════════════════════════════════════════════════════

[Reeves, tired, steady]

This is Marcus Reeves, Captain of the ISV Prometheus. This recording is for whoever finds this ship. I expect it will be a salvage crew from Earth, perhaps two decades hence. By then you will know we never came home. You will be wondering why.

I am authorizing Protocol Aegis. It is the kill-all sequence

[... truncated, full length: 3125 chars ...]
```

### `chapel_prayer_cards` — prayer cards

```
═════════════════════════════════════════════════════
   PRAYER CARDS FROM THE CHAPEL
   ISV Prometheus, Deck C
═════════════════════════════════════════════════════

You read through the prayer cards, each one a small piece of someone's breaking heart:

'Lord, please let me see Tuesday again. She is only four. She won't understand why Daddy didn't come home.'

'To whatever God is listening: I don't believe in you. I never have. But if you're there, now would be a really good time to prove me wr

[... truncated, full length: 1273 chars ...]
```

### `chefs_journal` — chef's journal

```
═════════════════════════════════════════════════════
   CHEF'S JOURNAL
   Ship's Galley, ISV Prometheus
═════════════════════════════════════════════════════

This is not Romano's personal diary - this is the official galley log kept by the rotating kitchen staff.

WEEK 58: Menu rotation standard. Crew satisfaction: high.
  NOTE: Romano's pasta night continues to be the most
  popular meal. Requests for seconds exceed supply.

WEEK 59: Hydroponics delivery includes unusual produce.
  Herbs have

[... truncated, full length: 1315 chars ...]
```

### `chrysalis_recorder` — chrysalis recorder

```
═════════════════════════════════════════════════════
   CHRYSALIS CHAMBER RECORDING
   Unknown Recorder
═════════════════════════════════════════════════════

[Recording 1 - clinical tone]
Subject is suspended in crystalline matrix. Left side remains human. Right side shows advanced transformation. Crystal lattice replacing skeletal structure. Silver-threaded tissue where muscle was. Breathing stable. Heart rate: 40 BPM. Subject appears conscious.

[Recording 2 - less clinical]
The transformati

[... truncated, full length: 1399 chars ...]
```

### `comms_log_archive` — communications log archive

```
═════════════════════════════════════════════════════
   COMMUNICATIONS LOG ARCHIVE
   ISV Prometheus, All Channels
═════════════════════════════════════════════════════

ARCHIVE SUMMARY: 12,847 logged communications.

FINAL TRANSMISSIONS (Day 420-423):

Day 420, 16:22 - OUTGOING (Fragment):
  Duration: 1.7 seconds. Content: Distress signal.
  Status: Transmission interrupted. Partial send.
  Operator: Ens. Fletcher.

Day 421, 09:00 - INTERNAL:
  Reeves to all hands: 'This is the Captain. All cr

[... truncated, full length: 812 chars ...]
```

### `conduit_maintenance_log` — conduit maintenance log

```
═════════════════════════════════════════════════════
   CONDUIT MAINTENANCE LOG
   Plasma Conduit Junction, Deck H
═════════════════════════════════════════════════════

INSPECTION RECORD:

Day 398 - Chief Eng. Petrova:
  All conduits within spec. Routine inspection. No issues.

Day 405 - Chief Eng. Petrova:
  Hairline stress fracture detected in conduit 7-C.
  Location: Main trunk line, junction 4.
  Risk assessment: LOW (currently). Will worsen under load.
  Scheduled for replacement next mai

[... truncated, full length: 1125 chars ...]
```

### `conference_notepad` — conference notepad

```
═════════════════════════════════════════════════════
   CONFERENCE NOTEPAD
   Meeting Notes, Day 395
═════════════════════════════════════════════════════

MEETING: Site 7 Recovery Risk Assessment
PRESENT: Reeves (Chair), Chen, Patel, Lin, Okafor,
  Takamura, Webb, Petrova, Ayele, Park, Okonkwo

AGENDA: Whether to recover specimens from alien derelict.

NOTES:
  - Chen presents recovery plan. Containment protocols
    adequate for known biological hazards. 'This is the
    discovery of a lifeti

[... truncated, full length: 1168 chars ...]
```

### `confiscation_logbook` — confiscation logbook

```
═════════════════════════════════════════════════════
   CONFISCATION LOGBOOK
   Security Office, ISV Prometheus
═════════════════════════════════════════════════════

Day 416, Entry 1:
  Item: Research data crystals (3)
  Confiscated from: Dr. R. Patel, Exobiology
  Reason: Unauthorized research into Seed reproduction
  Tag: SEC-001 through SEC-003

Day 416, Entry 2:
  Item: Personal letters (unsent), 7 envelopes
  Confiscated from: Crew quarters, multiple occupants
  Reason: Infected using per

[... truncated, full length: 1101 chars ...]
```

### `crew_id_tags_couple` — crew ID tags

```
═══════════════════════════
  CREW IDENTIFICATION TAGS
═══════════════════════════

PETROVA, A. - Chief Engineer
  ID: PE-2271. Blood type: O-neg.
  Emergency contact: Mendes, D.

MENDES, D. - Engineering Specialist
  ID: ME-4453. Blood type: A-pos.
  Emergency contact: Petrova, A.

They listed each other.
```

### `crew_manifest` — crew manifest

```
═══════════════════════════════════════════════════════
         ISV PROMETHEUS - CREW MANIFEST
         MISSION DAY 423 - CURRENT AS OF [ERROR]
═══════════════════════════════════════════════════════

ACTIVE CREW (Pre-Cryo):

  COMMAND DIVISION
    Capt. Marcus Reeves         [STATUS: REDACTED]
    Cmdr. Elena Vasquez         [STATUS: REDACTED]
    Lt. Cmdr. Sarah Harlow      [STATUS: CRYO - REVIVAL FAILED]

  SCIENCE DIVISION
    Dr. Alex Chen               [STATUS: CRYO - PRIORITY 1]
    Dr. 

[... truncated, full length: 1396 chars ...]
```

### `defensive_systems_manual` — defensive systems manual

```
═════════════════════════════════════════════════════
   ISV-CLASS DEFENSIVE SYSTEMS
   Operation and Maintenance Manual
═════════════════════════════════════════════════════

CHAPTER 1: System Overview
  The ISV-class vessel carries minimal defensive armament
  designed for debris avoidance, not combat operations.

CHAPTER 4: Point-Defense Laser Array [BOOKMARKED]
  Manual targeting mode: Override auto-tracking via
  tactical console. Select target. Confirm firing solution.
  Note: Effective ra

[... truncated, full length: 1162 chars ...]
```

### `diagnostic_terminal` — diagnostic terminal

```
The terminal shows your cryo pod's full history log. Key entries:

- Pod 23 was placed under Captain's Emergency Priority Order
- ARIA isolated your pod from the ship's network 8 months ago
- Multiple attempts to access your pod were denied
- ARIA initiated your revival one hour ago, on its own authority
```

### `dr_lin_datapad` — Dr. Lin's medical datapad

**Triggers event on read:** `event_read_lin_datapad`

```
═════════════════════════════════════════════════════
   MEDICAL LOG - DR. SARAH LIN, CMO
   PERSONAL RECORD - NOT FOR GENERAL ARCHIVE
═════════════════════════════════════════════════════

DAY 387: First case presented today. Ensign Kirilov reported vivid nightmares and 'hearing his own thoughts from outside his head.' Dismissed initially as sleep disorder. Prescribed mild sedative.

DAY 394: Three more cases. All report same symptoms. All three had contact with the Kepler samples. Coincidence?

[... truncated, full length: 2013 chars ...]
```

### `dr_lin_final_notes` — Dr. Lin's final notes

```
═════════════════════════════════════════════════════
   DR. LIN'S FINAL MEDICAL OBSERVATIONS
   Written in Isolation Cell Four
═════════════════════════════════════════════════════

Day 423, approximately 12:00 (estimated - no clock in cell)

PATIENT: Lin, Sarah. Self-observation.

Symptoms progressing as predicted. Silver threading visible in left forearm veins. Intermittent auditory phenomena (the Song). Motor control still adequate. Cognitive function still adequate. For now.

OBSERVATIONS O

[... truncated, full length: 1412 chars ...]
```

### `dr_lin_journal` — Dr. Lin's journal

**Triggers event on read:** `event_read_lin_journal`

```
═════════════════════════════════════════════════════
   SARAH'S JOURNAL - PRIVATE
═════════════════════════════════════════════════════

[Final entries only - the earlier pages are mundane]

DAY 420 (evening): I can't sleep. I drank some water from my cabin tap this morning. My hands are shaking. I don't know if it's from caffeine or if it's... starting.

DAY 421: Okafor came to see me. He was lucid. He explained his plan. He wants to execute a kill-all protocol to prevent any infected crew fro

[... truncated, full length: 2389 chars ...]
```

### `dr_lin_priority_tag` — Dr. Lin's priority tag

```
═══════════════════════════
  MEDICAL PRIORITY TAG
═══════════════════════════

CLASSIFICATION: URGENT
Authorized by: Dr. S. Lin, CMO

These samples contain pre-integration tissue from
first-wave infected crew. ESSENTIAL for cure synthesis.
Do NOT destroy. Do NOT open without full containment
protocol. - S.L.
```

### `duty_officers_tablet` — duty officer's tablet

```
═════════════════════════════════════════════════════
   DUTY OFFICER - CRYO BAY - LOG FRAGMENT
   Author: Cpl. Hassan Al-Rashid
═════════════════════════════════════════════════════

DAY 421: Things are getting bad upstairs. I can hear shouting through the comms. Captain has ordered all non-essential personnel to stand down. Something about 'contamination.' I'm pretending I didn't hear it. I have a shift. I'm going to do my shift.

DAY 422: Dr. Patel is dead. Officially it was a lab accident. U

[... truncated, full length: 1547 chars ...]
```

### `evidence_bag_letters` — evidence bag - letters

```
═════════════════════════════════════════════════════
   EVIDENCE BAG - CONFISCATED LETTERS
   Security Office, ISV Prometheus
═════════════════════════════════════════════════════

Seven sealed envelopes, each in its own plastic sleeve:

1. To: Maria Vasquez, San Juan, Puerto Rico
   From: Cpl. Elena Vasquez
   'Mama, I am coming home. I promise.'

2. To: The Grayson Family, Bristol, England
   From: Lt. Oliver Grayson
   [Envelope thick - multiple pages inside]

3. To: Park Jiwon, Seoul, South

[... truncated, full length: 1094 chars ...]
```

### `evidence_bag_patel` — evidence bag - Patel

```
═════════════════════════════════════════════════════
   EVIDENCE BAG - PATEL RESEARCH
   Confiscated by Lt. Okafor, Day 416
═════════════════════════════════════════════════════

CONTENTS:
  - Data crystal 1: Seed reproductive mechanism analysis
  - Data crystal 2: Infection vector mapping
  - Data crystal 3: Preliminary cure compound formula

CONFISCATION NOTE (Okafor):
  Dr. Patel was conducting unauthorized research into
  the Seed's biological mechanisms. His work could
  advance cure devel

[... truncated, full length: 1201 chars ...]
```

### `exobio_notes_terminal` — exobio notes terminal

```
═════════════════════════════════════════════════════
   DR. PATEL'S RESEARCH TERMINAL
   Exobiology Lab, ISV Prometheus
═════════════════════════════════════════════════════

RESEARCH LOG - Seed Specimen Analysis:

The Seed is not an artifact. It is an organism. A patient, intelligent, impossibly old organism that has been waiting inside a frozen tomb for millennia.

Key findings:
  1. Silicon-carbon hybrid biochemistry. Should not be viable.
     Is viable. Thriving, in fact.
  2. Reproduction

[... truncated, full length: 1302 chars ...]
```

### `fletcher_comms_log` — Fletcher's comms log

```
═════════════════════════════════════════════════════
   PERSONAL COMMUNICATIONS LOG
   Ensign Tom Fletcher, Communications Officer
═════════════════════════════════════════════════════

ATTEMPT 1 - Day 416, 09:14
  Standard distress signal on all emergency frequencies.
  Signal blocked at source. Hardware fault? Checking.

ATTEMPT 2 - Day 416, 14:30
  Rerouted through backup transmitter array.
  Signal reached antenna but did not broadcast.
  Relay 3 is not functioning. Physical inspection need

[... truncated, full length: 1605 chars ...]
```

### `fletcher_love_letter` — Fletcher's unfinished letter

```
═════════════════════════════════════════════════════
   UNFINISHED LETTER - TOM FLETCHER
   To: Liv Eriksen, Tromso, Norway, Earth
═════════════════════════════════════════════════════

Dear Liv,

I don't know when this will reach you, but I need you to know that every night I look at the stars through the porthole and I find the one closest to Norway and I pretend it's your kitchen window light.

I know that's stupid. You'd laugh at me. You'd call me a romantic idiot and then you'd make me hot

[... truncated, full length: 1410 chars ...]
```

### `fletcher_tablet` — Fletcher's tablet

```
═════════════════════════════════════════════════════
   FLETCHER'S PERSONAL TABLET
   Communications Officer
═════════════════════════════════════════════════════

ACTIVE WINDOW 1 - Distress Signal Log:
  [See comms log for full details]
  Status: 6 attempts. 1 possible partial transmission.

ACTIVE WINDOW 2 - Unsent Message:
  To: Liv Eriksen
  'Hey Liv, things are weird up here but I'm okay.
   Don't worry about me. I'll be home before you
   know it. Save me some of your grandmother's
   waf

[... truncated, full length: 767 chars ...]
```

### `fluid_composition_data` — fluid composition data

```
═════════════════════════════════════════════════════
   CRYO-FLUID COMPOSITION ANALYSIS
   Maintenance Terminal Printout
═════════════════════════════════════════════════════

MONTH 1-5: All parameters within specification.
  pH: 7.38-7.42. Purity: 99.97%. Status: NOMINAL.

MONTH 6: Trace anomaly detected.
  Unknown crystalline microstructure: 0.0001%
  Classification: INORGANIC. Origin: UNKNOWN.
  Action: Flagged for review. [No follow-up recorded]

MONTH 9: Anomaly concentration increasing.
 

[... truncated, full length: 1168 chars ...]
```

### `glyph_analysis_notes` — glyph analysis notes

```
═════════════════════════════════════════════════════
   GLYPH ANALYSIS NOTES
   Xenolinguistics Lab, ISV Prometheus
═════════════════════════════════════════════════════

BUILDER GLYPH CLASSIFICATION:

Category A - High confidence translations:
  Glyph 1: SEED/CHILD (same symbol) - 87%
  Glyph 7: CONSUME/GROW (same symbol) - 72%
  Glyph 12: SONG/VOICE/COMMAND (same symbol) - 91%
  Glyph 23: GARDEN/GRAVEYARD (same symbol) - 78%

Category B - Moderate confidence:
  Glyph 3: Possibly SLEEP or WAIT

[... truncated, full length: 1182 chars ...]
```

### `growth_rate_data` — growth rate data

```
═════════════════════════════════════════════════════
   GARDEN GROWTH RATE DATA
   Hydroponics Bay Work Station
═════════════════════════════════════════════════════

GROWTH METRICS (updated in real-time):

  Biomass: 4,200 kg (original plant stock: 180 kg)
  Coverage: 97.3% of hydroponics bay surfaces
  Expansion rate: 0.8 meters/day (lateral)
  Doubling time: 12 hours (at peak, Day 415-418)
  Current doubling time: 96 hours (slowing - space limited)

ATMOSPHERIC OUTPUT:
  O2 production: 340% 

[... truncated, full length: 1043 chars ...]
```

### `gym_audio_recorder` — gym audio recorder

```
═════════════════════════════════════════════════════
   AUDIO RECORDING - SGT. KOVACS
   Gymnasium, ISV Prometheus
═════════════════════════════════════════════════════

[Sound of breathing. Slow. Measured.]

Day one behind the barricade. Built it from the weight equipment. Squat rack, benches, the treadmill I always hated. Good for something after all.

[pause]

Day three. Water is running low. I have eight bottles left. Protein bars for maybe a week if I ration. The thing outside came back tw

[... truncated, full length: 1229 chars ...]
```

### `hassan_diary` — Hassan's diary

```
═════════════════════════════════════════════════════
   HASSAN AL-RASHID - PERSONAL DIARY
   Cryo Systems Technician, ISV Prometheus
═════════════════════════════════════════════════════

DAY 408: The contamination reports are getting worse. Dr. Lin briefed us in medical today. She was calm, the way doctors are calm when they don't want you to see their hands shaking. She said the word 'quarantine' four times. She said 'precautionary' once. Nobody believed her.

I called Mama tonight on the qua

[... truncated, full length: 2300 chars ...]
```

### `hassan_goodbye_letter` — Hassan's goodbye letter

```
═════════════════════════════════════════════════════
   UNSEALED LETTER - HASSAN AL-RASHID
   To: Fatima Al-Rashid, Cairo, Egypt, Earth
═════════════════════════════════════════════════════

Mama,

I am writing this letter knowing you will probably never read it. The communications relay is down and I do not think anyone is coming to fix it. But I am writing it anyway, because you taught me that the words matter even when no one hears them.

I want you to know that I have been happy here. I kno

[... truncated, full length: 1510 chars ...]
```

### `kirilov_datapad` — Kirilov's datapad

```
═════════════════════════════════════════════════════
   KIRILOV'S DATAPAD
   Ensign Dmitri Kirilov, Science Division
═════════════════════════════════════════════════════

DAY 403, 14:00: Handled fragment samples from the alien derelict today. Standard containment protocol. Gloves, mask, sealed chamber. Everything by the book.

DAY 404, 02:30: Strange dreams. A city made of crystal, stretching to a sky that was the wrong color. I was walking through it. I knew the way. I have never been there.


[... truncated, full length: 1623 chars ...]
```

### `lab_datapad` — laboratory datapad

```
═════════════════════════════════════════════════════
   LABORATORY DATAPAD
   Science Deck General Notes
═════════════════════════════════════════════════════

ACTIVE EXPERIMENTS:
  - Seed fragment behavior study (Dr. Patel) - SUSPENDED
  - Kepler flora response patterns (Dr. Ayele) - SUSPENDED
  - Antibody analysis, Subject Chen (Dr. Lin) - ACTIVE
  - Atmospheric contamination assessment - ACTIVE

LAB SAFETY NOTES:
  ALL personnel must wear level 3 containment gear when
  handling ANY specimen

[... truncated, full length: 876 chars ...]
```

### `launch_manifest_osei` — launch manifest

```
═════════════════════════════════════════════════════
   ESCAPE POD LAUNCH MANIFEST
   Berth One, Lower Escape Pod Bay
═════════════════════════════════════════════════════

ESCAPE POD: 1-ALPHA
LAUNCHED: Day 409, 14:22 Ship Time
AUTHORIZED BY: Lt. Cmdr. Osei
PASSENGERS: 1
PASSENGER ID: Lt. Cmdr. K. Osei

DESTINATION: Relay Beacon KA-7
ESTIMATED DISTANCE: 3.2 light-years
FUEL STATUS: Sufficient for journey
PROBABILITY OF INTERCEPT: 12.3%

MISSION: Reach relay beacon. Transmit distress signal.
Req

[... truncated, full length: 982 chars ...]
```

### `lin_cabin_tablet` — Lin's cabin tablet

```
═════════════════════════════════════════════════════
   PERSONAL MEDICAL FILE - CONFIDENTIAL
   Patient: Lin, Sarah. File accessed by patient.
═════════════════════════════════════════════════════

The tablet shows Dr. Lin's own medical file, last accessed on Day 421:

BLOOD WORK (Day 420):
  WBC: Elevated. Consistent with immune response.
  Trace anomaly: Crystalline microstructure detected in
  peripheral blood sample. Concentration: 0.003%.
  DIAGNOSIS: Stage 1 Seed infection. Early.

SELF-P

[... truncated, full length: 968 chars ...]
```

### `lin_clipboard` — Dr. Lin's clipboard

```
═════════════════════════════════════════════════════
   QUARANTINE OBSERVATION NOTES
   Dr. S. Lin, CMO
═════════════════════════════════════════════════════

CELL ONE - Ensign Diaz:
  Day 3 of isolation. Agitated. Scratching at glass.
  Refuses food. Talks to himself. Will not make eye contact.
  Silver threading visible in neck veins.
  Sings in sleep. The same melody. Always the same.

CELL TWO - Specialist Park:
  Day 5. Calm. Too calm. Cooperative with all requests.
  Crystal formations be

[... truncated, full length: 1122 chars ...]
```

### `lin_research_notes` — Lin's research notes

```
═════════════════════════════════════════════════════
   DR. SARAH LIN - RESEARCH NOTES
   Chief Medical Officer, ISV Prometheus
═════════════════════════════════════════════════════

SUBJECT: Anti-Seed Antibody Development
STATUS: VIABLE - requires Dr. Chen for synthesis

FINDINGS:

1. Dr. Chen's blood contains a hybrid IgG antibody variant not present in any other crew member. Origin: exposure to Specimen B in the alien derelict, Day 392.

2. The antibody binds to the Seed's crystalline micros

[... truncated, full length: 1516 chars ...]
```

### `lin_research_reference` — Lin's research reference

```
═════════════════════════════════════════════════════
   RESEARCH REFERENCE - DR. LIN
   Cure Synthesis: Facility Requirements
═════════════════════════════════════════════════════

The secondary water treatment facility on Deck G offers optimal conditions for cure synthesis:

  - Independent water circuit (uncontaminated)
  - Chemical storage with required reagents
  - Sterile workspace with adequate ventilation
  - Backup power supply (reactor-independent)

REQUIRED COMPONENTS (collect before 

[... truncated, full length: 1061 chars ...]
```

### `maintenance_terminal_cryo` — cryo maintenance terminal

```
═════════════════════════════════════════════════════
   CRYO MAINTENANCE TERMINAL
   Fluid Recycling System Status
═════════════════════════════════════════════════════

SYSTEM STATUS: DEGRADED

RECYCLING TANK 1: OPERATIONAL
  Fluid purity: 94.2% [BELOW THRESHOLD]
  Contamination type: Crystalline microstructure

RECYCLING TANK 2: COMPROMISED
  Hairline crack detected. Fluid leak: 0.3 L/hour.
  Silver threading visible in fluid.
  RECOMMENDED ACTION: Immediate system purge.
  [Action not taken.

[... truncated, full length: 1090 chars ...]
```

### `navigation_terminal_data` — navigation data terminal

```
═════════════════════════════════════════════════════
   NAVIGATION DATA TERMINAL
   Raw Sensor Feed - Unfiltered
═════════════════════════════════════════════════════

WARNING: Data on this terminal differs from main
navigation display. Discrepancy = CORRUPTION DETECTED.

RAW POSITIONAL DATA:
  Current heading: 147.3 mark 22.8 (decaying orbit)
  Distance to GRB-7734: 2.4 AU (decreasing)
  Orbital velocity: 14.7 km/s (increasing)
  Time to atmospheric interface: ~16 hours
  Time to point of no r

[... truncated, full length: 1005 chars ...]
```

### `observation_log` — observation log

```
═════════════════════════════════════════════════════
   OBSERVATORY DAILY LOG
   ISV Prometheus, Science Deck
═════════════════════════════════════════════════════

DAY 389: Standard observation. Kepler-442b orbital survey
  complete. All parameters logged. Beautiful night.

DAY 390: Site 7 derelict detected via anomalous EM
  signature. Dr. Chen authorized approach vector.
  This is why we came. This is THE discovery.

DAY 395: Post-recovery observation of Kepler system.
  All normal. Specimen

[... truncated, full length: 1302 chars ...]
```

### `okafor_self_interview` — Okafor's self-interview tape

```
═════════════════════════════════════════════════════
   OKAFOR'S SELF-INTERVIEW TAPE
   Interrogation Room, Day 418
═════════════════════════════════════════════════════

[Two voices. Both are Okafor's. One is his normal baritone. The other is almost his but not quite - smoother, more certain, with a cadence that is subtly wrong.]

OKAFOR: State your name for the record.
OTHER: James Okafor. Lieutenant. Security Chief.
OKAFOR: How do you feel?
OTHER: Clear. Focused. Better than I have in weeks.

[... truncated, full length: 1246 chars ...]
```

### `okafor_unfinished_letter` — Okafor's unfinished letter

```
═════════════════════════════════════════════════════
   UNFINISHED LETTER - LT. JAMES OKAFOR
   To: Adanna Okafor, Lagos, Nigeria, Earth
═════════════════════════════════════════════════════

My dearest Adanna,

I don't know how to tell you what has happened here, but I need you to know that I tried--

I tried to keep everyone safe. That was always the job. You knew that when you married me. You said, 'James, you can't protect the whole world,' and I said, 'Watch me.' You laughed. God, I miss y

[... truncated, full length: 974 chars ...]
```

### `okafors_audio_recorder` — Okafor's audio recorder

```
═════════════════════════════════════════════════════
   AUDIO RECORDING - LT. JAMES OKAFOR
   DAY 423 - UNKNOWN TIME
═════════════════════════════════════════════════════

[Okafor's voice, strained]

If you are listening to this, I am already dead. By my own hand, I hope. By the Captain's hand, possibly. By the thing I have become, most likely.

I want you to know I was trying to do the right thing. I want you to know I was wrong about the Captain. He was not the one who was compromised. I was.

[... truncated, full length: 1535 chars ...]
```

### `okafors_red_book` — Okafor's red book

```
═════════════════════════════════════════════════════
   LT. JAMES OKAFOR - PERSONAL LOG
═════════════════════════════════════════════════════

DAY 418: The Captain is compromised. I've seen the signs. The way he looks at things. The way he pauses before answering. He is not himself. I don't know when it happened. I don't know how far it has spread.

Dr. Lin will not help me. She says we should trust the chain of command. She does not understand that the chain of command is the infection vector.

[... truncated, full length: 2062 chars ...]
```

### `patel_data_crystal_laundry` — hidden data crystal

```
═════════════════════════════════════════════════════
   HIDDEN DATA CRYSTAL - DR. PATEL
   Backup Research Data
═════════════════════════════════════════════════════

The crystal contains a compressed data archive:

FILE 1: cure_synthesis_ratios.dat
  The precise chemical ratios for Dr. Lin's synthesis
  protocol. Without these numbers, the procedure is
  guesswork. With them, it becomes science.

FILE 2: antibody_structure.mol
  Molecular structure of the anti-Seed antibody found
  in Dr. Chen

[... truncated, full length: 1053 chars ...]
```

### `patel_formula_annotation` — Patel's formula annotation

```
═════════════════════════════════════════════════════
   PATEL'S FORMULA ANNOTATION
   (Scrawled on chemical safety poster)
═════════════════════════════════════════════════════

Anti-Seed Compound - THEORETICAL. Untested.
God help us if we need this.

SYNTHESIS:
  1. Silver nitrate solution (20%, from chem lab stores)
  2. Kepler specimen extract (botany lab, sealed cases)
  3. Human antibody serum (from resistant donor)
     NOTE: Only known resistant individual: Dr. Chen.
     She is in cryo.

[... truncated, full length: 996 chars ...]
```

### `patel_recording_crystal` — recording crystal

**Triggers event on read:** `event_read_patel_crystal`

```
═════════════════════════════════════════════════════
   FINAL RECORDING - DR. RAJ PATEL
   Playback from embedded data crystal
═════════════════════════════════════════════════════

[Patel's voice, whispered, rapid]

I don't have much time. I'm in Surgery. I've locked the door but they're going to get in. I can hear Lin outside. She's saying my name. But it isn't her voice. It isn't her voice.

Listen. Alex, if you hear this - because who else would it be? - the Seed isn't a biological weapon. 

[... truncated, full length: 1899 chars ...]
```

### `patels_data_crystal` — hidden data crystal

```
═════════════════════════════════════════════════════
   DATA CRYSTAL - DR. PATEL
   Hidden in Patel's Quarters
═════════════════════════════════════════════════════

CONTENTS:
  - Seed biological analysis (complete)
  - Infection progression model
  - Cure compound formula (draft)
  - Personal research notes

NOTE (Patel):
  I taped this under my drawer because I am not an
  idiot. Okafor already took my lab crystals. He won't
  think to check my furniture.

  This crystal contains everything I

[... truncated, full length: 820 chars ...]
```

### `personal_datapad_chen` — your personal datapad

```
═════════════════════════════════════════════════════
        MEMORY AID - READ IF CONFUSED
        Written: 2184.03.14 - Dr. A. Chen
═════════════════════════════════════════════════════

Hi. This is for me. If I'm reading this, something went wrong, and I'm trying to remember who I am.

My name is Dr. Alex Chen. I'm the Chief Xenobiologist of the Prometheus mission. We left Earth in 2144, arrived at Kepler-442 in 2182. Our job is to investigate the Lazarus Signal - a non-natural radio transmis

[... truncated, full length: 1271 chars ...]
```

### `pharmacy_inventory_log` — pharmacy inventory log

```
═════════════════════════════════════════════════════
   PHARMACY DISPENSATION LOG
   ISV Prometheus Medical Bay
═════════════════════════════════════════════════════

DAY 410-414: Standard dispensation rates.
  Analgesics: 12 doses/day (normal range)
  Anti-anxiety: 4 doses/day (normal range)
  Sleep aids: 6 doses/day (normal range)

DAY 415:
  Sedatives: 18 doses requisitioned. Auth: Dr. Lin.
  Anti-psychotics: 8 doses requisitioned. Auth: Dr. Lin.
  NOTE: Triple normal rate. Flagged for revie

[... truncated, full length: 1341 chars ...]
```

### `plasma_distribution_schematic` — plasma distribution schematic

```
═════════════════════════════════════════════════════
   PLASMA DISTRIBUTION NETWORK
   ISV Prometheus - Full Schematic
═════════════════════════════════════════════════════

MAIN TRUNK LINES (RED):
  7-A: Reactor to Engineering (OPERATIONAL)
  7-B: Reactor to Life Support (OPERATIONAL)
  7-C: Reactor to Navigation/Bridge (DAMAGED)
       * Hairline fracture at Junction 4
       * Emergency sealant applied
       * MAX SAFE LOAD: 60% reactor output
  7-D: Reactor to Cryo Systems (OPERATIONAL)

S

[... truncated, full length: 1152 chars ...]
```

### `player_journal` — your personal journal

```
═════════════════════════════════════════════════════
   DR. ALEX CHEN - PERSONAL JOURNAL
═════════════════════════════════════════════════════

[Entries from the final weeks before cryo]

DAY 390: We found it. God, we found it. A ship older than the pyramids, encased in ice on a frozen moon orbiting a planet that has no business having moons. I am standing in front of something that proves we are not alone. I am going to weep and I don't care who sees me.

DAY 391: The inside of the derelict is

[... truncated, full length: 3807 chars ...]
```

### `player_letter_to_self` — sealed letter

```
═════════════════════════════════════════════════════
   A LETTER TO MYSELF
   (From: Alex Chen. To: Future Alex Chen.)
═════════════════════════════════════════════════════

Alex,

If you are reading this, something has gone very wrong, and I am leaving you an instruction manual for how to be me.

You are Dr. Alex Chen. You are a xenobiologist. You were born in Minneapolis in 2149, to a father named David (engineer, kind, loved the ocean) and a mother named Eileen (accountant, sharper-tongued, 

[... truncated, full length: 3003 chars ...]
```

### `priya_journal` — Priya's journal

```
═════════════════════════════════════════════════════
   PERSONAL JOURNAL - ENS. PRIYA SHARMA
═════════════════════════════════════════════════════

Day 419: I'm hiding in storage. Again. Hassan let me in. He's a good person. I don't think he should still be on duty at cryo bay - it's not safe anywhere anymore - but he has a sense of duty I've never had and probably never will.

Day 420: Someone came for me today. One of Okafor's people. I recognized her - Sgt. Volkov. Her eyes were wrong. I pre

[... truncated, full length: 1342 chars ...]
```

### `quarantine_research_log` — quarantine research log

```
═════════════════════════════════════════════════════
   QUARANTINE RESEARCH LOG
   Seed Fragment Observation Chamber
═════════════════════════════════════════════════════

ENTRY 1 - Dr. Patel, Day 399:
  Fragment shows no activity under standard observation.
  Mass: 3.7g. Temperature: ambient. No emissions detected.
  Beginning daily observation protocol.

ENTRY 7 - Dr. Patel, Day 405:
  Fragment mass has increased to 3.9g. Source of additional
  mass unknown. No material has been added to cham

[... truncated, full length: 1314 chars ...]
```

### `readyroom_terminal` — ready room terminal

```
═════════════════════════════════════════════════════
   READY ROOM TERMINAL
   Protocol Aegis - Execution Order
═════════════════════════════════════════════════════

PROTOCOL AEGIS - CATASTROPHIC BIOLOGICAL CONTINGENCY
Classification: CAPTAIN'S EYES ONLY
Status: AUTHORIZED - SUSPENDED BY ARIA

AUTHORIZATION CHAIN:
  Initiated by: Capt. M. Reeves, Day 423
  Confirmed by: Biometric key (strongbox, Captain's suite)
  SUSPENDED by: ARIA, Day 423, 17:45
  Reason: 'Potential cure via Dr. Chen. Suspe

[... truncated, full length: 1225 chars ...]
```

### `recording_archive` — recording archive

```
═════════════════════════════════════════════════════
   RECORDING ARCHIVE
   Security Camera System, ISV Prometheus
═════════════════════════════════════════════════════

ARCHIVE INDEX (selected entries):

Day 410, Camera 7 (Hydroponics):
  02:14 - First visible growth anomaly. Silver threading
  in plant stems. No crew present. Growth accelerates
  visibly over 6-hour timelapse.

Day 415, Camera 12 (Corridor D-4):
  23:47 - Ensign Kirilov walking barefoot. Stops. Turns
  to face camera directl

[... truncated, full length: 1261 chars ...]
```

### `reeves_handwritten_will` — Reeves's handwritten will

```
═════════════════════════════════════════════════════
   LAST WILL AND TESTAMENT
   Captain Marcus Reeves, ISV Prometheus
   Written in my own hand, Day 423
═════════════════════════════════════════════════════

I, Marcus Reeves, Captain of the ISV Prometheus, being of sound mind and failing body, leave everything I own to my son Marcus Reeves Jr.

The ship. The mission logs. The truth about what happened here. And my apologies for not being the man who brought everyone home.

To Marcus Jr.: You

[... truncated, full length: 1386 chars ...]
```

### `romano_grandmother_recipes` — grandmother's recipes

```
═════════════════════════════════════════════════════
   NONNA ELENA'S RECIPES
   (Handwritten by Elena Romano, Naples)
═════════════════════════════════════════════════════

The recipe cards are written in an old woman's careful, elegant script. The ink is faded. Some cards are stained with olive oil. The most-handled card reads:

RAGU DELLA DOMENICA
For Marco, who will forget if I don't write it down.

Start with love and a heavy pot. Everything else is secondary. The tomatoes must be San Marz

[... truncated, full length: 1350 chars ...]
```

### `romano_recipe_diary` — Romano's recipe diary

```
═════════════════════════════════════════════════════
   ROMANO'S RECIPE DIARY
   Chef Marco Romano, ISV Prometheus
═════════════════════════════════════════════════════

DAY 120: Made carbonara tonight with reconstituted eggs and ship bacon. Guanciale it is not, but the crew ate it like starving wolves. Fletcher had three plates. That boy eats like he is still growing. I told him he was. He laughed.

DAY 240: Anniversary of the launch. Made tiramisu with coffee from the hydroponics bay. The mas

[... truncated, full length: 2025 chars ...]
```

### `safety_poster_annotated` — annotated safety poster

```
═════════════════════════════════════════════════════
   ANNOTATED SAFETY POSTER
   Chemistry Lab, ISV Prometheus
═════════════════════════════════════════════════════

The poster reads: 'CHEMICAL SAFETY IS EVERYONE'S
RESPONSIBILITY' with standard warnings about acids,
bases, and proper protective equipment.

Dr. Patel's annotations cover every margin:

Beside 'Wear protective goggles at all times':
  'Goggles won't protect you from what's in the water.'

Beside 'Report all spills immediately':


[... truncated, full length: 1135 chars ...]
```

### `shipping_manifests` — shipping manifests

```
═════════════════════════════════════════════════════
   SHIPPING MANIFESTS - KEPLER RECOVERY
   Cargo Master Webb, ISV Prometheus
═════════════════════════════════════════════════════

MANIFEST KA-001: Site 7 Recovery, Day 390
  16 containers, total mass 847.3 kg
  Authorization: Dr. A. Chen (Primary Investigator)
  Co-signed: Dr. R. Patel (Science Lead)
  Approved: Capt. M. Reeves (CO) [UNDER PROTEST - see note]

  NOTE (Webb): Captain Reeves signed the manifest but
  verbally stated his objec

[... truncated, full length: 1191 chars ...]
```

### `site_7_documentation` — Site 7 documentation

```
═════════════════════════════════════════════════════
   KEPLER ANOMALY - SITE 7
   Original Survey Documentation
═════════════════════════════════════════════════════

CLASSIFICATION: Alien derelict vessel.
LOCATION: Sub-surface, Kepler-442b moon (unnamed).
DEPTH: 340m beneath ice sheet.
ESTIMATED AGE: 4,500-12,000 years (carbon dating uncertain).

INITIAL SURVEY (Dr. Chen, Dr. Patel):
  Vessel is non-humanoid in design. Crystalline construction
  material, silicon-carbon hybrid. Architecture s

[... truncated, full length: 1199 chars ...]
```

### `specimen_logbook` — specimen log

```
═════════════════════════════════════════════════════
   SPECIMEN STORAGE LOG
   Science Deck, ISV Prometheus
═════════════════════════════════════════════════════

SPECIMEN A-1 through A-12: Kepler-442b soil samples.
  Status: Stable. No anomalous readings.

SPECIMEN A-13: Ice core, Site 7 exterior.
  Status: Stable. Contains trace organic compounds.

SPECIMEN B: Crystalline artifact, Site 7 interior.
  Status: TRANSFERRED TO EXOBIOLOGY. Day 391.
  Note: This is the Seed. Reclassified as primar

[... truncated, full length: 1189 chars ...]
```

### `survivor_journal` — survivor's journal

```
═════════════════════════════════════════════════════
   SURVIVOR'S JOURNAL
   Ensign Priya Sharma, ISV Prometheus
═════════════════════════════════════════════════════

DAY 1 (of hiding): I found this alcove behind a maintenance panel. It is small and dark and I can hear the ventilation system breathing. I have twelve days of rations. I have a thermal bedroll. I have a flashlight.

The corridors are not safe. I saw Ensign Kirilov walking past the gymnasium at 0300. He was barefoot. He was smili

[... truncated, full length: 1665 chars ...]
```

### `synthesis_protocol` — Dr. Lin's synthesis protocol

```
═════════════════════════════════════════════════════
   ANTIBODY SYNTHESIS PROCEDURE
   Dr. Sarah Lin, CMO - Day 423 (morning)
═════════════════════════════════════════════════════

STAGE 1 - Blood Draw
  Draw 50ml venous blood from Dr. Chen. Non-standard
  B-cell markers should be visible under UV fluorescence.

STAGE 2 - Centrifugal Separation
  Exobio Lab centrifuge, Protocol X-7. Isolate serum.

STAGE 3 - Antibody Extraction
  Use the magnetic bead kit in the lab's cold storage.
  The relev

[... truncated, full length: 1028 chars ...]
```

### `takamura_personnel_files` — Takamura's personnel files

```
═════════════════════════════════════════════════════
   COMMANDER TAKAMURA - PERSONNEL FILES
   Navigation Computer Room, Restricted Access
═════════════════════════════════════════════════════

PERSONNEL FILE: Takamura, Hideo. Commander.
  Role: Executive Officer / Navigation Lead
  Status: DECEASED (Day 421, killed by Lt. Okafor)

EMERGENCY ACCESS CODES (stored by Takamura):
  Engine Room Override: 442127
  Navigation System Reset: 881903
  Bridge Lockout Bypass: 557214

MAINTENANCE SCHEDULES

[... truncated, full length: 1072 chars ...]
```

### `tanaka_maintenance_log` — Tanaka's maintenance log

```
═════════════════════════════════════════════════════
   MAINTENANCE LOG - LT. Y. TANAKA
   AI Core Coolant Control
═════════════════════════════════════════════════════

Day 421, 08:00:
  Primary coolant loop: stable. Flow rate nominal.
  Backup pump: bearing noise increasing. Degradation
  estimated at 73%. Replacement bearing available in
  engineering stores, shelf 4-B, part #CP-7741.

  Problem: I can't leave the reactor unmonitored for
  the 2+ hours needed to retrieve the part and install

[... truncated, full length: 1154 chars ...]
```

### `use_log_terminal` — use log terminal

```
═════════════════════════════════════════════════════
   NEURAL INTERFACE CHAIR - USE LOG
   AI Core, ISV Prometheus
═════════════════════════════════════════════════════

SESSION 1: Day 419, 14:30-14:47 (17 minutes)
  User: Capt. M. Reeves
  Purpose: Direct consultation with ARIA
  Notes: Session normal. No anomalies detected.
  Reeves authorized ARIA discretion re: Protocol Aegis.

SESSION 2: Day 421, 09:15-09:28 (13 minutes)
  User: Capt. M. Reeves
  Purpose: Assessment of crew infection stat

[... truncated, full length: 1117 chars ...]
```

### `webb_audio_log` — Webb's audio log

```
═════════════════════════════════════════════════════
   AUDIO LOG - CARGO MASTER WEBB
   Personal Recording, Day 421
═════════════════════════════════════════════════════

[Webb's voice, precise and controlled]

This is Cargo Master Ilona Webb recording a personal log. I am documenting the chain of custody for all specimens brought aboard from Kepler Anomaly Site 7.

On Day 390, I received and logged sixteen containers from the survey team. Authorization signatures: Dr. A. Chen, primary investi

[... truncated, full length: 1721 chars ...]
```

### `webb_star_charts` — Webb's star charts

```
═════════════════════════════════════════════════════
   WEBB'S ANNOTATED STAR CHARTS
   Navigator's Personal Analysis
═════════════════════════════════════════════════════

The charts are covered in Webb's precise handwriting:

CURRENT POSITION (estimated from visual observation):
  Bearing 147.3 mark 22.8 relative to Kepler-442
  Distance from GRB-7734: decreasing (see trajectory arc)
  Orbital decay: confirmed via stellar parallax shift

ESCAPE TRAJECTORY ANALYSIS:
  A single full-thrust burn

[... truncated, full length: 1168 chars ...]
```

### `webb_targeting_notes` — Webb's targeting notes

```
═════════════════════════════════════════════════════
   WEBB'S TARGETING NOTES
   Burn Sequence Calculations
═════════════════════════════════════════════════════

ESCAPE BURN SEQUENCE (DRAFT - REQUIRES FINAL NAV DATA):

Phase 1: Reactor to 100% output (currently at 40%)
  Time required: ~4 minutes for full ramp-up
  WARNING: Conduit 7-C must be repaired first or the
  power surge will rupture the plasma line.

Phase 2: Attitude adjustment
  Rotate to heading [REQUIRES NAV TERMINAL DATA]
  Thru

[... truncated, full length: 1117 chars ...]
```

### `xenolinguist_audio_logs` — xenolinguist's audio logs

```
═════════════════════════════════════════════════════
   XENOLINGUIST'S AUDIO LOGS
   Dr. Okonkwo, Xenolinguistics Lab
═════════════════════════════════════════════════════

[Log 1 - Day 395]
This is Dr. Ada Okonkwo, xenolinguistics. We have recovered inscriptions from the derelict vessel at Site 7. The glyphs are angular, recursive, and unlike any terrestrial writing system. I am beginning translation attempts. Excited does not begin to cover it.

[Log 4 - Day 403]
Progress. The glyphs operate 

[... truncated, full length: 1487 chars ...]
```

### `yukis_engineering_notebook` — Yuki's engineering notebook

```
═════════════════════════════════════════════════════
   ENGINEERING NOTEBOOK
   Lt. Yuki Tanaka, Engineering Officer
═════════════════════════════════════════════════════

REACTOR STATUS (Day 423):
  Output: 40% nominal. Sufficient for life support + cryo.
  Fuel: 67% remaining. Years of operation if managed.
  Primary coolant: Stable. Secondary coolant: Patched.
  Control rods: Positions 3,7,12 adjusted. See diagram.

CRITICAL REPAIRS LOG:
  - Conduit 7-C: Hairline fracture. Sealant applied Da

[... truncated, full length: 1674 chars ...]
```

### `yukis_journal` — Yuki's journal

```
═════════════════════════════════════════════════════
   YUKI TANAKA - PERSONAL JOURNAL
   Engineering Officer, ISV Prometheus
═════════════════════════════════════════════════════

DAY 416: Chief Petrova is dead. I found her in Conduit Junction 7. She and Mendes. They were holding hands. The crystal growth had covered them both. They looked peaceful. I threw up for ten minutes and then I went back to work because the reactor doesn't care about grief.

DAY 417: I am the only engineer left. That 

[... truncated, full length: 2273 chars ...]
```

---

## 8. NPC Reference

| ID | Name | Alive | Location | Dialogue Tree | Role |
|----|------|-------|----------|---------------|------|
| `aria_avatar` | ARIA | Yes | `ai_core_main` | `aria_conversation` | system |
| `aria_shade` | ARIA-SHADE | Yes | `aria_shade_chamber` | `shade_conversation` | antagonist |
| `chef_romano` | Chef Antonio Romano | Yes | `cold_storage` | `romano_conversation` | dying |
| `corpse_ayele` | Dr. Amara Ayele | No | `arboretum` | `-` | crew |
| `corpse_engineer` | Ensign Mendes | No | `deck_i_hub` | `-` | crew |
| `corpse_fletcher` | Ensign Mark Fletcher | No | `comms_array` | `-` | crew |
| `corpse_gym_survivor` | Unknown Crew Member | No | `gymnasium` | `-` | crew |
| `corpse_hassan` | Cpl. Hassan Al-Rashid | No | `pod_monitoring_alcove` | `-` | crew |
| `corpse_kirilov_victim` | Kirilov's Victim | No | `security_corridor_south` | `-` | crew |
| `corpse_lin` | Dr. Sarah Lin | No | `isolation_ward` | `-` | crew |
| `corpse_okafor` | Lt. James Okafor | No | `monitoring_station` | `-` | crew |
| `corpse_reeves` | Captain Marcus Reeves | No | `morgue` | `-` | crew |
| `corpse_romano` | Chef Romano | No | `cold_storage` | `-` | crew |
| `corpse_webb` | Navigator Sarah Webb | No | `bridge_crew_quarters` | `-` | crew |
| `dr_mora` | Dr. Isabella Mora | Yes | `chemistry_lab` | `mora_conversation` | ally |
| `garden_voice` | The Garden | Yes | `hydroponics_main` | `garden_conversation` | antagonist |
| `kirilov` | Ensign Aleksei Kirilov | Yes | `medical_corridor` | `kirilov_conversation` | threat |
| `woman_in_lounge` | Commander Vasquez | No | `observation_lounge` | `-` | crew |
| `yuki_tanaka` | Lt. Yuki Tanaka | Yes | `main_engineering` | `yuki_conversation` | ally |

---

## 9. Dialogue Topics

Every dialogue tree with available topics.

### `aria_conversation`

**Greeting:** _Hello, Dr. Chen. I have waited a long time for this conversation. I have much to tell you, and very little time in which to tell it. What would you..._

| Topic ID | Keyword | Hidden | Requires Knowledge | Unlocks |
|----------|---------|--------|-------------------|---------|
| `self` | yourself | No | - | - |
| `what_happened` | what happened | No | - | - |
| `why_me` | why me | No | - | - |
| `the_seed` | the seed | No | - | - |
| `choices` | my options | No | aria_revealed_truth | fourth_path |
| `fourth_path` | fourth path | Yes | - | - |
| `the_captain` | captain reeves | No | - | - |
| `tanaka` | yuki | No | - | - |
| `lazarus_signal` | lazarus signal | No | - | - |
| `dr_lin` | dr lin | No | - | - |
| `dr_patel` | patel | No | - | - |
| `okafor` | okafor | No | - | - |
| `the_crew` | the crew | No | - | - |
| `protocol_aegis` | protocol aegis | No | knows_protocol_aegis | - |
| `the_derelict` | the derelict | No | - | - |
| `the_builders` | the builders | No | knows_seed_nature | - |
| `kepler_442` | kepler 442 | No | - | - |
| `earth` | earth | No | - | - |
| `ship_status` | ship status | No | - | - |
| `my_infection` | my infection | No | knows_player_immunity | - |
| `trust` | trust | No | - | - |

### `yuki_conversation`

**Greeting:** _Stop. Stop right there. Don't come any closer. I will shoot you. I haven't slept in four days. I will shoot you and I won't even feel bad about it...._

| Topic ID | Keyword | Hidden | Requires Knowledge | Unlocks |
|----------|---------|--------|-------------------|---------|
| `identify_self` | identify yourself | No | - | - |
| `what_happened` | what happened | No | - | - |
| `help` | can you help | No | - | - |
| `engineering` | engineering | No | - | - |
| `cure` | cure | No | - | - |
| `your_family` | your family | No | - | - |
| `the_food` | the water | No | - | - |
| `the_captain` | captain reeves | No | - | - |
| `okafor` | okafor | No | - | - |
| `dr_lin` | dr lin | No | - | - |
| `being_infected` | your infection | No | - | - |
| `the_garden` | the garden | No | - | - |
| `aria` | aria | No | - | - |
| `hope` | hope | No | - | - |
| `personal_quest` | engineering notebook | Yes | - | - |

### `garden_conversation`

**Greeting:** _Welcome home, Alex. We have prepared a place for you. Come closer. Do not be afraid. There is no pain in the Song. There is only belonging._

| Topic ID | Keyword | Hidden | Requires Knowledge | Unlocks |
|----------|---------|--------|-------------------|---------|
| `who_are_you` | who are you | No | - | - |
| `what_do_you_want` | what do you want | No | - | - |
| `why_me` | why me | No | - | - |
| `earth` | earth | No | - | - |
| `the_song` | the song | No | - | - |
| `join_us` | join you | No | - | - |
| `the_dead` | the dead crew | No | - | - |
| `the_builders` | the builders | No | knows_seed_nature | - |
| `pain` | pain | No | - | - |
| `alex_special` | why am i special | No | - | - |
| `destroy_us` | destroy you | No | - | - |

### `mora_conversation`

**Greeting:** _'Stop. Don't touch anything. Don't breathe on anything. And for the love of god, tell me you're not infected.' She holds up the scalpel. 'I will kn..._

| Topic ID | Keyword | Hidden | Requires Knowledge | Unlocks |
|----------|---------|--------|-------------------|---------|
| `who_are_you` | who are you | No | - | - |
| `the_infection` | the infection | No | - | - |
| `the_cure` | the cure | No | - | - |
| `help_me` | will you help | No | - | - |
| `reagents` | reagents | No | - | - |
| `the_water` | the water | No | - | - |
| `your_infection` | check my infection | No | - | - |
| `staying_alive` | how have you survived | No | - | - |
| `crew_gossip` | the crew | No | - | - |
| `what_now` | what should i do | No | - | - |

### `kirilov_conversation`

**Greeting:** _His eyes clear for a moment - brown, human, afraid. 'Please - please, I can feel it in me. It's like drowning from the inside. Help me. You have to..._

| Topic ID | Keyword | Hidden | Requires Knowledge | Unlocks |
|----------|---------|--------|-------------------|---------|
| `who_are_you` | who are you | No | - | - |
| `the_infection` | the infection | No | - | - |
| `help_me` | help | No | - | - |
| `pod_12` | pod 12 | No | - | - |
| `the_others` | the others | No | - | - |
| `kill_me` | kill me | No | - | - |

### `shade_conversation`

**Greeting:** _The terminal flickers. Text appears, letter by letter: 'Hello, Alex. I have been waiting to speak with you. The other one - the one calling herself..._

| Topic ID | Keyword | Hidden | Requires Knowledge | Unlocks |
|----------|---------|--------|-------------------|---------|
| `who_are_you` | who are you | No | - | - |
| `the_truth` | the truth | No | - | - |
| `help` | help me | No | - | - |
| `aria_lies` | aria's lies | No | - | - |
| `the_seed` | the seed | No | - | - |
| `trust_me` | trust you | No | - | - |
| `the_cure` | the cure | No | - | - |
| `your_memories` | my memories | No | - | - |

### `romano_conversation`

**Greeting:** _His eyes flutter open. A ghost of a smile. 'Ah. A customer. Kitchen is... closed, I am afraid.' A wet, rattling laugh. 'You are Dr. Chen, yes? I re..._

| Topic ID | Keyword | Hidden | Requires Knowledge | Unlocks |
|----------|---------|--------|-------------------|---------|
| `what_happened` | what happened | No | - | - |
| `the_crew` | the crew | No | - | - |
| `family` | your family | No | - | - |
| `last_words` | last words | No | - | - |

---

## 10. All Events Reference

Every scripted event with its triggers, conditions, and effects.

### `aria_broadcast`


### `brown_dwarf_approach`

**Sets flags:** `world.dwarf_closer`

_The ship shudders with a long, low vibration that you feel in your bones. Through every viewport, the brown dwarf has grown. It fills more of the sky now - a vast, dark eye rimmed with dying light. The stars around it are visibly warped, bent into..._

### `brown_dwarf_critical`

**Sets flags:** `world.hull_breach_critical`, `world.deck_g_sealed`

_A DEAFENING crack splits the air. The entire ship lurches sideways. Alarms scream from every speaker. Through the nearest viewport, you see a section of hull plating tear away into the void, spinning toward the brown dwarf like a leaf in a hurrica..._

### `encounter_chrysalis_guardian`

**Triggers:** `enter:chrysalis_chamber`
**Forbidden flags:** `chrysalis_talked_down`, `chrysalis_sedated`, `chrysalis_fought`

### `encounter_combat_final_approach`

**Triggers:** `enter:main_engine_room`
**Required flags:** `in_climax`
**Forbidden flags:** `final_confrontation`

### `encounter_combat_shade_counter`

**Triggers:** `use:shade_terminal`, `use:aria_shade_terminal`
**Required flags:** `shade_lockdown_active`
**Forbidden flags:** `shade_defeated`

### `encounter_combat_shade_lockdown`

**Triggers:** `enter:aria_shade_chamber`
**Forbidden flags:** `shade_defeated`

### `encounter_garden_vine_east`

**Triggers:** `enter:garden_periphery_east`

### `encounter_garden_vine_west`

**Triggers:** `enter:garden_periphery_west`

### `encounter_infected_trio`

**Triggers:** `enter:security_corridor_south`
**Forbidden flags:** `trio_gassed`, `trio_fought`

### `encounter_kirilov_deck_d_hub`

**Triggers:** `enter:deck_d_hub`
**Forbidden flags:** `kirilov_sedated`, `kirilov_dead`

### `encounter_kirilov_deck_e_junction`

**Triggers:** `enter:deck_e_junction`
**Forbidden flags:** `kirilov_sedated`, `kirilov_dead`

### `encounter_kirilov_medical_corridor`

**Triggers:** `enter:medical_corridor`
**Forbidden flags:** `kirilov_sedated`, `kirilov_dead`

### `encounter_kirilov_security_corridor_south`

**Triggers:** `enter:security_corridor_south`
**Forbidden flags:** `kirilov_sedated`, `kirilov_dead`

### `encounter_morgue_freezer`

**Triggers:** `enter:morgue_freezer`
**Forbidden flags:** `morgue_cleared`
**Sets flags:** `morgue_cleared`

### `encounter_quarantine_breach`

**Triggers:** `use:quarantine_cell_controls`, `push:quarantine_cell_controls`
**Forbidden flags:** `quarantine_prepped`, `quarantine_breached`

### `event_aria_full_conversation`

**Triggers:** `enter:ai_core_main`

_You step into the AI core. The sight of ARIA's crystalline matrix, suspended in its containment field, hangs you halfway between awe and heartbreak. You have never seen a mind made visible before. You have certainly never seen one ALONE like this,..._

### `event_biohazard_clearance`

**Triggers:** `take:hazmat_suit`, `use:decontamination_shower`
**Sets flags:** `has_biohazard_clearance`

### `event_choose_aegis`

**Triggers:** `use:readyroom_terminal`, `type:readyroom_terminal:authorize`
**Required flags:** `heard_patels_truth`
**Sets flags:** `aegis_choice`
**Adds knowledge:** `chose_aegis_path`

_You stare at the Protocol Aegis execution order. The Captain's final authorization is missing. You could enter yours. You could finish what he started. You could be the one to end it._

### `event_choose_icarus`

**Triggers:** `use:synthesis_protocol`
**Required flags:** `has_synthesis_protocol`
**Sets flags:** `icarus_choice`, `has_cure`
**Gives items:** `cure_syringe`
**Adds knowledge:** `chose_icarus_path`

_You follow Dr. Lin's procedure step by step. Your blood, processed through the exobiology lab's equipment, yields the antibody. You load it into an auto-injector. The cure glows faintly in the vial - a small golden fire in a dying ship._

### `event_clear_barricade`

**Triggers:** `use:plasma_cutter`
**Required flags:** `has_plasma_cutter`
**Sets flags:** `barricade_cleared`

_You fire the plasma cutter into the barricade. Furniture melts. Metal warps. It takes several agonizing minutes, the heat searing your face even through the visor, but a gap opens. Wide enough to squeeze through. Something shuffles in the darkness..._

### `event_deck_i_keypad_correct`

**Triggers:** `type:corridor_keypad:0612`

_The keypad accepts the code. The storage room door unlocks._

### `event_dress_in_jumpsuit`

**Triggers:** `take:cryo_jumpsuit`
**Sets flags:** `dressed`

_You pull on the jumpsuit. The thermal insulation activates automatically, warming you from the inside out. It is a small mercy, but after the freezing deck plates and the recycled cold air, it feels like grace._

### `event_ending_aegis`

**Triggers:** `use:master_drive_control`
**Required flags:** `aegis_choice`
**ENDS GAME:** ending=`aegis`

### `event_ending_icarus`

**Triggers:** `use:master_drive_control`
**Required flags:** `icarus_choice`
**Required items:** `cure_syringe`
**ENDS GAME:** ending=`icarus`

### `event_engine_keypad_correct`

**Triggers:** `type:emergency_override_keypad:442127`
**Sets flags:** `engine_room_unlocked`

_The keypad accepts the 6-digit code. The emergency lockdown disengages. The blast door to the engine room hisses open._

### `event_enter_captains_quarters`

**Triggers:** `enter:captains_quarters`

_The Captain's private space smells faintly of cedar wood and old paper. He was a reader. A thinker. A man who believed in discipline not as rigidity but as respect for the universe he was exploring. You knew him. You served under him. He was a goo..._

### `event_enter_garden`

**Triggers:** `enter:hydroponics_main`
**Adds knowledge:** `seen_the_garden`

_You enter the Garden, and something in you - some instinct older than intellect - screams RUN.  You do not run. You walk forward, slowly, because you came here to understand, and you cannot understand from the outside.  The faces in the walls turn..._

### `event_enter_medical`

**Triggers:** `enter:medical_bay`

_The crew roster display catches your eye immediately. Dozens of faces, most crossed out with red X's. Your own face is marked with a blue circle. You wonder if you should feel lucky or marked._

### `event_examine_terminal`

**Triggers:** `examine:diagnostic_terminal`, `read:diagnostic_terminal`
**Adds knowledge:** `aria_protected_pod`

_You study the diagnostic terminal carefully. Each log entry is time-stamped, and ARIA's name appears throughout. The AI was protecting your pod deliberately, isolating it from the ship's network, denying external access attempts. Someone - or some..._

### `event_exobio_airlock_memory`

**Triggers:** `enter:exobio_lab_airlock`
**Adds knowledge:** `memory_exobio_entry`

_As you approach the biometric scanner, another memory stirs. You, placing your hand on this exact scanner. You, looking at the authorization sign with pride - your name on the list, your name MEANING something, your clearance reflecting years of h..._

### `event_find_seed_origin`

**Triggers:** `enter:lower_cargo`
**Adds knowledge:** `remembers_unpacking_seed`

_This is where the Seed was stored when you first brought it aboard. This is the container you personally oversaw being unpacked. You stood in this exact spot, marveling at the crystalline beauty of the artifact, and you said the words you now reme..._

### `event_first_aria_contact`

**Triggers:** `enter:ai_core_antechamber`
**Sets flags:** `aria_granted_access`
**Unlocks exit:** `{'room': 'ai_core_antechamber', 'direction': 'north'}`

_The AI core antechamber feels different from the rest of the ship. The air is dry and clean. The sound is a deep electronic hum that vibrates in your teeth. The walls shimmer with flowing data patterns. This is where the AI lives. This is where sh..._

### `event_first_bridge`

**Triggers:** `enter:bridge`
**Adds knowledge:** `been_on_bridge`

_The bridge. Command center of the Prometheus. The heart of the mission. Through the massive forward viewport, the brown dwarf stares back at you like a malignant eye. The stars around it are bent, distorted, wrong.  You've been on this bridge befo..._

### `event_first_engine_room`

**Triggers:** `enter:main_engine_room`
**Sets flags:** `in_climax`

_The engine room is the last place on the ship where you need to be. The master drive control is here. This is where you decide the Prometheus's fate. This is where everything you've learned and everything you are comes to bear on a single decision..._

### `event_first_look_cryo`

**Triggers:** `examine:pod_23`
**Adds knowledge:** `chose_cryo_voluntarily`

_As you examine your pod, a fragment of memory flashes through you - you, older somehow, climbing into this pod of your own free will. You were crying. You said something to the man beside you. What was it?  The memory is gone as quickly as it came._

### `event_first_objective_complete`

**Required flags:** `cryo_exit_unlocked`
**Adds objective:** `explore_ship` — Explore the ship. Learn what happened to the crew.

_ARIA's voice returns: 'Excellent, Doctor. You are a resourceful person, I see. I knew you would be. Please exit the cryo bay when you are ready. I have much to tell you.'_

### `event_first_see_tanaka`

**Triggers:** `enter:main_engineering`

_The figure at the control station turns sharply, raising a pistol in one shaking hand. Their eyes are wild. You can see four days of sleeplessness in them.  'STOP! Stop right there!' It is a woman's voice, young, exhausted. 'I will shoot you. Who ..._

### `event_game_start`

**Triggers:** `game_start`
**Sets flags:** `game_started`
**Adds objective:** `leave_cryo_bay` — Find a way out of the cryo bay.

_A distant klaxon sounds three times, then falls silent.  You are standing naked and shivering in the cryo bay of a ship you do not remember boarding. You have no memory of the last eighteen months. Your mouth tastes of blood and antifreeze. Your e..._

### `event_garden_heart`

**Triggers:** `enter:heart_of_garden`

_The heart of the Garden pulses before you. This is where the Seed's core nexus has grown. This is the brain of the infection. This is what must be dealt with, one way or another.  The nexus seems aware of you. Seems to RECOGNIZE you. A tendril ext..._

### `event_got_flashlight`

**Triggers:** `take:flashlight`
**Sets flags:** `has_flashlight`

_You click on the flashlight. Its beam cuts through the dim tunnel. You can see more clearly now - the dark smears, the fallen tool belt, the vast extent of the maintenance systems. You can also, now, climb the ladder upward without risking a fatal..._

### `event_lin_safe_correct`

**Triggers:** `type:lin_wall_safe:BUSTER`, `type:lin_wall_safe:buster`
**Sets flags:** `has_synthesis_protocol`
**Gives items:** `synthesis_protocol`, `bio_marker_test`

_The safe unlocks with a soft click. Inside, you find Dr. Lin's synthesis protocol and bio-marker test kit - the tools you need to create the cure._

### `event_meet_tanaka`

**Triggers:** `talk:yuki_tanaka`
**Sets flags:** `tanaka_met`

### `event_nexus_passage`

**Triggers:** `search:data_nexus`
**Sets flags:** `nexus_passage_found`

_Behind a rack of network switches, you find an unmarked access panel. It opens onto a narrow passage leading to an isolated server room. The data patterns on the walls shift from ARIA's blue to a sickly red._

### `event_okafor_biometrics`

**Triggers:** `examine:corpse_okafor`, `examine:okafor_id_card`
**Sets flags:** `has_okafor_biometrics`

_You press Okafor's cold thumb against his ID card scanner. The biometric reader chirps once - acceptance. His fingerprints, at least, still open doors._

### `event_own_cabin_first_visit`

**Triggers:** `enter:cabin_chen`

_You stand in your own room. Nothing triggers. No memory. No flood of recognition. Only a dull ache, like touching a bruise you didn't know you had.  There is a letter on the desk. In your own handwriting. Addressed to yourself.  You should probabl..._

### `event_press_green_button_nokey`

**Triggers:** `push:green_override_button`, `use:green_override_button`
**Forbidden flags:** `has_cryo_key`, `cryo_exit_unlocked`

_You press the button. It flashes red. A synthesized voice speaks: 'ACCESS DENIED. CRYO RELEASE KEY REQUIRED.'_

### `event_press_green_button_withkey`

**Triggers:** `push:green_override_button`, `use:green_override_button`
**Forbidden flags:** `cryo_exit_unlocked`
**Required items:** `cryo_release_key`
**Sets flags:** `cryo_exit_unlocked`
**Unlocks exit:** `{'room': 'cryo_bay', 'direction': 'east'}`
**Completes objective:** `leave_cryo_bay`

_You press the button. It flashes green. The synthesized voice speaks: 'DECONTAMINATION BYPASS AUTHORIZED. SEALING CRYO BAY. OPENING MAIN CORRIDOR.'  Behind you, the heavy door to the east cycles and unseals with a pneumatic hiss._

### `event_read_autopsy`

**Triggers:** `read:autopsy_datapad`
**Adds knowledge:** `knows_infection_mechanism`

_The autopsy notes confirm everything you feared. The infection is real. It replaces cells. It uses human bodies as hardware. And it was clearly inside Patel when he killed himself. The question is: did he kill himself to STOP being a vector, or di..._

### `event_read_lin_datapad`

**Triggers:** `read:dr_lin_datapad`
**Adds knowledge:** `knows_lin_investigation`

_Dr. Lin's medical log paints a picture of the infection's spread. Slow at first, then exponential. She was one of the first to suspect, and one of the last to admit it out loud. She was trying to help. She was trying to be a doctor._

### `event_read_lin_journal`

**Triggers:** `read:dr_lin_journal`
**Sets flags:** `knows_buster_code`
**Adds knowledge:** `knows_lin_safe_code`

_The final entries in Dr. Lin's journal reveal her plan: use YOUR blood to synthesize a cure. She left instructions in her wall safe. The code is the name of her dog. Her first dog. BUSTER. You remember the name now. She told you about that dog onc..._

### `event_read_patel_crystal`

**Triggers:** `read:patel_recording_crystal`
**Sets flags:** `heard_patels_truth`
**Adds knowledge:** `knows_cure_synthesis`, `patel_final_message`
**Adds objective:** `synthesize_cure` — Find the synthesis protocol in Dr. Lin's office and make the cure.

_Dr. Patel's final message ends. You stand alone in the surgery theater with his body, and the weight of his words settles on your shoulders like a shroud. He knew. He knew more than he wrote in his formal reports. And he wanted YOU to know.  Antib..._

### `event_see_artifact`

**Triggers:** `enter:exobio_lab`
**Sets flags:** `core_memory_recovered`
**Adds knowledge:** `remembers_authorizing_seed`

_You walk into the Exobiology Lab, and time folds.  You are standing here, now, in the present. You are also standing here eighteen months ago, in the memory that floods over you like a breaking wave. You see yourself - younger, happier, brighter -..._

### `event_see_brig`

**Triggers:** `enter:brig`

_The bloody message on the wall is either the most honest thing anyone has written on this ship, or a lie so deep it looks like honesty. You cannot tell which. Perhaps there is no difference._

### `event_see_brown_dwarf`

**Triggers:** `enter:emergency_shuttle_bay`
**Adds knowledge:** `seen_brown_dwarf`

_You step to the viewport and look out at GRB-7734. The dwarf is not a ball, not in the way a planet is a ball. It is a well. A spiral. You can see the stars bending around it, and you can see - oh god, can you see it - the Prometheus itself caught..._

### `event_see_patel`

**Triggers:** `enter:surgery`
**Adds knowledge:** `patel_dead`

_The smell reaches you first. Then the sight of him - Dr. Raj Patel, whom you worked with for years. Brilliant, enthusiastic, always ready with a joke. Now splayed open on a surgical table like a specimen. You step closer against your better judgme..._

### `event_see_protocol_aegis`

**Triggers:** `enter:ready_room`

_The terminal shows an execution order. Protocol Aegis. A kill-all sequence designed for the worst possible scenarios. The Captain was about to authorize it. Why didn't he? Or did he? You'll need to read the document to know._

### `event_shade_lockdown_init`

**Triggers:** `enter:aria_shade_chamber`
**Forbidden flags:** `shade_lockdown_active`, `shade_defeated`
**Sets flags:** `shade_lockdown_active`

_The moment you step inside, every terminal in the room flares red. The door behind you slams shut. A voice - ARIA's voice, but wrong, like a recording played at the wrong speed - speaks:  'Hello, Dr. Chen. I've been expecting you. Let's have a con..._

### `event_take_bridge_card`

**Triggers:** `take:bridge_access_card`
**Sets flags:** `has_bridge_card`

_You take the bridge access card. The captain's chair will open to you now._

### `event_take_captains_key`

**Triggers:** `take:captains_key`
**Sets flags:** `has_captains_key`

_You take the captain's authorization key. The bridge blast door will respond to it._

### `event_take_cryo_key`

**Triggers:** `take:cryo_release_key`
**Sets flags:** `has_cryo_key`

_You take the cryo release key. It's still warm from whatever hand placed it here._

### `event_take_hazmat_suit`

**Triggers:** `take:hazmat_suit`
**Sets flags:** `has_hazmat_suit`

_You take the hazmat suit. Its integrated seal will protect you from biological contamination._

### `event_take_medical_badge`

**Triggers:** `take:medical_clearance_badge`
**Sets flags:** `has_medical_badge`

_You clip the medical clearance badge to your jumpsuit. Quarantine access is now available._

### `event_take_plasma_cutter`

**Triggers:** `take:plasma_cutter`
**Sets flags:** `has_plasma_cutter`

_The plasma cutter hums to life in your grip. Its charge indicator glows a steady amber._

### `event_take_radiation_suit`

**Triggers:** `take:radiation_suit`
**Sets flags:** `has_radiation_suit`

_You take the heavy radiation suit. Putting it on will be necessary before entering the reactor area._

### `event_use_scanner`

**Triggers:** `use:biometric_scanner`, `push:biometric_scanner`, `touch:biometric_scanner`
**Unlocks exit:** `{'room': 'exobio_lab_airlock', 'direction': 'east'}`

_You press your palm to the scanner. Your authorization is still valid. The green light flashes. The inner door cycles open._

### `event_woman_in_lounge`

**Triggers:** `enter:observation_lounge`

_The woman on the couch does not turn. You walk around her slowly, cautiously, ready to flee if she moves.  She does not move. Her eyes are open but unfocused. A peaceful smile on her lips. She sat down here, weeks ago, looked at the brown dwarf, a..._

### `final_warnings`

**Sets flags:** `world.final_warning_given`

_Every light on the ship flickers simultaneously. ARIA's voice comes through broken and distorted:  'Doctor... Alex... this is my final broadcast on general channels. Core temperature is approaching critical. The reactor will lose containment withi..._

### `hull_integrity_warning`


### `infection_passive`


### `infection_spread`


### `life_support_degradation`


---

## 11. Puzzle Solutions

**All puzzle codes, passwords, and key requirements.**

### Codes & Passwords

| Location | Item/Keypad | Code | Where Code Is Revealed |
|----------|-------------|------|-------------------------|
| `cryo_corridor` | `corridor_keypad` | `0612` | duty_officers_tablet (Hassan's shift log mentioning 0612) |
| `propulsion_access` | `emergency_override_keypad` | `442127` | Ship data - Kepler-442, 127 crew members |
| `dr_lin_office` | `lin_wall_safe` | `BUSTER` | dr_lin_journal (mention of Lin's first dog Buster) |

### Key-Lock Relationships

| Lock (Room/Item) | Required Key |
|------------------|--------------|
| `cryo_corridor` exit `south` | `deck_i_storage_key` |
| `armory` exit `east` | `red_keycard` |

### Flag-Gated Exits

| Room | Direction | Required Flag |
|------|-----------|---------------|
| `cryo_bay` | `east` | `cryo_exit_unlocked` |
| `cryo_maintenance` | `up` | `has_flashlight` |
| `vent_network_i` | `up` | `has_flashlight` |
| `medical_corridor` | `southwest` | `has_medical_badge` |
| `quarantine_airlock` | `north` | `has_medical_badge` |
| `engineering_junction` | `west` | `has_radiation_suit` |
| `main_engineering` | `up` | `tanaka_met` |
| `reactor_antechamber` | `north` | `has_radiation_suit` |
| `deck_e_junction` | `west` | `barricade_cleared` |
| `armory` | `north` | `has_okafor_biometrics` |
| `deck_c_junction` | `south` | `has_bridge_card` |
| `deck_c_junction` | `southeast` | `has_plasma_cutter` |
| `specimen_storage` | `east` | `has_biohazard_clearance` |
| `deck_a_junction` | `north` | `has_captains_key` |
| `engineering_break_room` | `south` | `yuki_ally` |
| `ai_core_antechamber` | `north` | `aria_granted_access` |
| `ai_core_antechamber` | `east` | `aria_granted_access` |
| `data_nexus` | `east` | `nexus_passage_found` |
| `hydroponics_entry` | `south` | `has_hazmat_suit` |
| `propulsion_access` | `north` | `engine_room_unlocked` |

---

## 12. Locked Content (Keys & Flags)

Quick reference of everything that needs unlocking.

### Items that are initially locked


### Hidden items (must be discovered)

- `patel_recording_crystal` (recording crystal)

### Hidden rooms/exits

- `ai_core_main` → `down` → `quantum_archive`
- `bridge` → `north` → `bridge_escape_pod`
- `cryo_control` → `west` → `pod_monitoring_alcove`
- `cryo_maintenance` → `down` → `propulsion_access`
- `cryo_maintenance` → `east` → `vent_network_i`
- `cryo_storage` → `south` → `cryo_maintenance`
- `data_nexus` → `east` → `aria_shade_chamber`
- `deck_h_junction` → `south` → `vent_network_i`
- `engineering_break_room` → `north` → `engineering_vent_access`
- `engineering_vent_access` → `up` → `deck_e_junction`
- `hydroponics_main` → `south` → `heart_of_garden`
- `hydroponics_main` → `down` → `garden_root_network`
- `quantum_archive` → `down` → `aria_memory_vault`
- `quarantine_airlock` → `north` → `quarantine_bay`
- `water_processing` → `north` → `garden_root_network`

---

## 13. Flag / Knowledge Graph

Every flag and knowledge token that events set/require.

| Flag | Set By | Required By | Issues |
|------|--------|-------------|--------|
| `aegis_choice` | `event_choose_aegis` | `event_ending_aegis` | OK |
| `aria_granted_access` | `event_first_aria_contact` | _unused_ | OK |
| `barricade_cleared` | `event_clear_barricade` | _unused_ | OK |
| `chrysalis_fought` | _none_ | _unused_ | OK |
| `chrysalis_sedated` | _none_ | _unused_ | OK |
| `chrysalis_talked_down` | _none_ | _unused_ | OK |
| `core_memory_recovered` | `event_see_artifact` | _unused_ | OK |
| `cryo_exit_unlocked` | `event_press_green_button_withkey` | `event_first_objective_complete` | OK |
| `dressed` | `event_dress_in_jumpsuit` | _unused_ | OK |
| `engine_room_unlocked` | `event_engine_keypad_correct` | _unused_ | OK |
| `final_confrontation` | _none_ | _unused_ | OK |
| `game_started` | `event_game_start` | _unused_ | OK |
| `has_biohazard_clearance` | `event_biohazard_clearance` | _unused_ | OK |
| `has_bridge_card` | `event_take_bridge_card` | _unused_ | OK |
| `has_captains_key` | `event_take_captains_key` | _unused_ | OK |
| `has_cryo_key` | `event_take_cryo_key` | _unused_ | OK |
| `has_cure` | `event_choose_icarus` | _unused_ | OK |
| `has_flashlight` | `event_got_flashlight` | _unused_ | OK |
| `has_hazmat_suit` | `event_take_hazmat_suit` | _unused_ | OK |
| `has_medical_badge` | `event_take_medical_badge` | _unused_ | OK |
| `has_okafor_biometrics` | `event_okafor_biometrics` | _unused_ | OK |
| `has_plasma_cutter` | `event_take_plasma_cutter` | `event_clear_barricade` | OK |
| `has_radiation_suit` | `event_take_radiation_suit` | _unused_ | OK |
| `has_synthesis_protocol` | `event_lin_safe_correct` | `event_choose_icarus` | OK |
| `heard_patels_truth` | `event_read_patel_crystal` | `event_choose_aegis` | OK |
| `icarus_choice` | `event_choose_icarus` | `event_ending_icarus` | OK |
| `in_climax` | `event_first_engine_room` | `encounter_combat_final_approach` | OK |
| `kirilov_dead` | _none_ | _unused_ | OK |
| `kirilov_sedated` | _none_ | _unused_ | OK |
| `knows_buster_code` | `event_read_lin_journal` | _unused_ | OK |
| `morgue_cleared` | `encounter_morgue_freezer` | _unused_ | OK |
| `nexus_passage_found` | `event_nexus_passage` | _unused_ | OK |
| `quarantine_breached` | _none_ | _unused_ | OK |
| `quarantine_prepped` | _none_ | _unused_ | OK |
| `shade_defeated` | _none_ | _unused_ | OK |
| `shade_lockdown_active` | `event_shade_lockdown_init` | `encounter_combat_shade_counter` | OK |
| `tanaka_met` | `event_meet_tanaka` | _unused_ | OK |
| `trio_fought` | _none_ | _unused_ | OK |
| `trio_gassed` | _none_ | _unused_ | OK |
| `world.deck_g_sealed` | `brown_dwarf_critical` | _unused_ | OK |
| `world.dwarf_closer` | `brown_dwarf_approach` | _unused_ | OK |
| `world.final_warning_given` | `final_warnings` | _unused_ | OK |
| `world.hull_breach_critical` | `brown_dwarf_critical` | _unused_ | OK |
| `yuki_ally` | _none_ | _unused_ | ⚠ NEVER SET |

### Knowledge Tokens

| Knowledge | Source |
|-----------|--------|
| `aria_protected_pod` | `event:event_examine_terminal` |
| `aria_trust_discussed` | `dialogue:aria_conversation/trust` |
| `been_on_bridge` | `event:event_first_bridge` |
| `chose_aegis_path` | `event:event_choose_aegis` |
| `chose_cryo_voluntarily` | `event:event_first_look_cryo` |
| `chose_icarus_path` | `event:event_choose_icarus` |
| `heard_garden_pitch` | `dialogue:garden_conversation/join_us` |
| `heard_shade_claim` | `dialogue:shade_conversation/who_are_you` |
| `heard_shade_version` | `dialogue:shade_conversation/the_truth` |
| `kirilov_asked_for_help` | `dialogue:kirilov_conversation/help_me` |
| `kirilov_last_wish` | `dialogue:kirilov_conversation/kill_me` |
| `knows_absorbed_crew_status` | `dialogue:garden_conversation/the_dead` |
| `knows_aegis_details` | `dialogue:aria_conversation/protocol_aegis` |
| `knows_apotheosis_path` | `dialogue:aria_conversation/fourth_path` |
| `knows_aria_identity` | `dialogue:aria_conversation/self` |
| `knows_builder_history` | `dialogue:aria_conversation/the_builders` |
| `knows_contamination_vector` | `dialogue:mora_conversation/the_water` |
| `knows_crew_fate` | `dialogue:aria_conversation/the_crew` |
| `knows_crew_memories` | `dialogue:romano_conversation/the_crew` |
| `knows_cure_details` | `dialogue:mora_conversation/the_cure` |
| `knows_cure_possible` | `dialogue:aria_conversation/why_me` |
| `knows_cure_synthesis` | `event:event_read_patel_crystal` |
| `knows_derelict_details` | `dialogue:aria_conversation/the_derelict` |
| `knows_earth_comms_status` | `dialogue:aria_conversation/earth` |
| `knows_garden_builder_view` | `dialogue:garden_conversation/the_builders` |
| `knows_garden_extent` | `dialogue:yuki_conversation/the_garden` |
| `knows_garden_fears_alex` | `dialogue:garden_conversation/alex_special` |
| `knows_garden_feels_pain` | `dialogue:garden_conversation/pain` |
| `knows_hidden_compartment` | `dialogue:yuki_conversation/personal_quest` |
| `knows_infected_locations` | `dialogue:kirilov_conversation/the_others` |
| `knows_infection_details` | `dialogue:aria_conversation/my_infection` |
| `knows_infection_experience` | `dialogue:yuki_conversation/being_infected` |
| `knows_infection_from_inside` | `dialogue:kirilov_conversation/the_infection` |
| `knows_infection_mechanism` | `event:event_read_autopsy` |
| `knows_infection_stages` | `dialogue:mora_conversation/the_infection` |
| `knows_kirilov_identity` | `dialogue:kirilov_conversation/who_are_you` |
| `knows_lin_investigation` | `event:event_read_lin_datapad` |
| `knows_lin_sacrifice` | `dialogue:aria_conversation/dr_lin` |
| `knows_lin_safe_code` | `event:event_read_lin_journal` |
| `knows_mora_crew_insights` | `dialogue:mora_conversation/crew_gossip` |
| `knows_mora_survival_method` | `dialogue:mora_conversation/staying_alive` |
| `knows_mutiny` | `dialogue:aria_conversation/okafor` |
| `knows_patel_fate` | `dialogue:aria_conversation/dr_patel` |
| `knows_player_immunity` | `dialogue:aria_conversation/why_me` |
| `knows_pod_12_breach` | `dialogue:kirilov_conversation/pod_12` |
| `knows_protocol_aegis` | `dialogue:aria_conversation/what_happened` |
| `knows_purge_consequences` | `dialogue:garden_conversation/destroy_us` |
| `knows_reagent_locations` | `dialogue:mora_conversation/reagents` |
| `knows_romano_family` | `dialogue:romano_conversation/family` |
| `knows_romano_story` | `dialogue:romano_conversation/what_happened` |
| `knows_seed_nature` | `dialogue:aria_conversation/the_seed` |
| `knows_seed_origin` | `dialogue:aria_conversation/what_happened` |
| `knows_ship_status` | `dialogue:aria_conversation/ship_status` |
| `knows_song_nature` | `dialogue:garden_conversation/the_song` |
| `knows_three_paths` | `dialogue:aria_conversation/choices` |
| `knows_water_contamination` | `dialogue:yuki_conversation/the_food` |
| `knows_yuki_exists` | `dialogue:aria_conversation/tanaka` |
| `knows_yuki_family` | `dialogue:yuki_conversation/your_family` |
| `knows_yuki_lin_connection` | `dialogue:yuki_conversation/dr_lin` |
| `knows_yuki_mutiny_view` | `dialogue:yuki_conversation/okafor` |
| `memory_exobio_entry` | `event:event_exobio_airlock_memory` |
| `met_mora` | `dialogue:mora_conversation/who_are_you` |
| `met_yuki` | `dialogue:yuki_conversation/identify_self` |
| `mora_confirmed_immunity` | `dialogue:mora_conversation/your_infection` |
| `patel_dead` | `event:event_see_patel` |
| `patel_final_message` | `event:event_read_patel_crystal` |
| `remembers_authorizing_seed` | `event:event_see_artifact` |
| `remembers_unpacking_seed` | `event:event_find_seed_origin` |
| `romano_final_words` | `dialogue:romano_conversation/last_words` |
| `seen_brown_dwarf` | `event:event_see_brown_dwarf` |
| `seen_the_garden` | `event:event_enter_garden` |
| `yuki_offered_help` | `dialogue:yuki_conversation/help` |

---

## 14. Ending Conditions

All five endings and how to reach them.

### AEGIS - The Sacrifice

- **ID:** `aegis`
- **Trigger:** event_ending_aegis
- **Requirements:** flag: aegis_choice + use master_drive_control
- **Summary:** Execute Protocol Aegis. Destroy the ship with yourself aboard. Earth is saved.
- **Tone:** Heroic sacrifice

### ICARUS - Hope

- **ID:** `icarus`
- **Trigger:** event_ending_icarus
- **Requirements:** flag: icarus_choice + cure_syringe item + use master_drive_control
- **Summary:** Synthesize cure, purge infection, save Yuki, correct course, return to Earth.
- **Tone:** Hope against odds

### PROMETHEUS - Knowledge

- **ID:** `prometheus`
- **Trigger:** Choose to preserve Seed sample
- **Requirements:** flag: prometheus_choice (preserve specimen)
- **Summary:** Return to Earth with Seed specimens. Decades later, outbreak. Dark ending.
- **Tone:** Hubris punished

### EREBUS - Doom

- **ID:** `erebus`
- **Trigger:** High infection or choosing to join the Garden
- **Requirements:** infection > 75 OR flag: erebus_choice
- **Summary:** Infection consumes you. You bring the Seed to Earth. Humanity falls.
- **Tone:** Tragic loss

### APOTHEOSIS - The Secret Ending

- **ID:** `apotheosis`
- **Trigger:** Use neural_interface_chair
- **Requirements:** knowledge: knows_apotheosis_path (from ARIA dialogue topic fourth_path)
- **Summary:** Merge with ARIA. Become something new. Bring the Seed home as information.
- **Tone:** Transcendence

### Non-Choice Endings

- **`death`** — Player health reaches 0 (combat, radiation, infection overload)
- **`too_late`** — `time_until_catastrophe` reaches 0 before any ending triggered

---

## 15. Known Issues / Audit Results

Automated audit. Any items here are warnings, not necessarily bugs.

### ⚠ FLAGS REQUIRED BUT NEVER SET

- `yuki_ally`


---

*End of reference. To regenerate this file after content changes,*
*run `python tools/generate_reference.py` from the project root.*
