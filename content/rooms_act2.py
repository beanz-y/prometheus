"""
Act 2 Rooms - Main ship exploration: Bridge, Science, Living Quarters, Security.

After Act 1 establishes what happened, Act 2 lets the player piece together
the crew's story and begin to understand the horror they've walked into.
"""

from engine.room import Room, Exit


def build_act2_rooms(world):
    """Create Act 2 rooms - main ship areas."""

    # ═══════════════════════════════════════════════════════════════════
    # DECK H JUNCTION - The crossroads
    # ═══════════════════════════════════════════════════════════════════

    deck_h_junction = Room(
        id="deck_h_junction",
        name="Deck H Maintenance Junction",
        deck="Deck H - AI Core",
        description=(
            "You emerge from the maintenance tunnel into a dim, blue-lit "
            "service corridor. The air up here is noticeably different - cleaner, "
            "drier, faintly ozone-scented. This is the AI core deck, where the "
            "ship's electronic brain is housed. The walls are lined with access "
            "panels to cooling systems and data conduits.\n\n"
            "A maintenance hatch on the wall is stenciled DECK G - CARGO DOWN. "
            "Another is labeled DECK H PROPER - AI CORE AREA. A rusty ladder "
            "climbs upward to DECK F - ENGINEERING.\n\n"
            "An emergency light above the ladder flashes green, then red, then "
            "green again, in an irregular pattern. It almost seems to be "
            "trying to tell you something."
        ),
        exits={
            'down': Exit(
                direction='down',
                destination='cryo_maintenance',
                description="You descend the ladder back into the cryogenics tunnels."
            ),
            'up': Exit(
                direction='up',
                destination='engineering_junction',
                description="You climb up toward Engineering."
            ),
            'east': Exit(
                direction='east',
                destination='ai_core_antechamber',
                description="You enter the AI core antechamber.",
                locked=True,
                lock_message="Access to the AI core is restricted. You need clearance."
            ),
            'west': Exit(
                direction='west',
                destination='cargo_access',
                description="You enter the cargo access tunnel."
            ),
            'south': Exit(
                direction='south',
                destination='vent_network_i',
                hidden=True,
                description="You squeeze into a ventilation shaft that descends toward Deck I."
            ),
        },
        items=[
            "flickering_green_light",  # Morse code clue!
            "access_panels",
            "data_conduit_humming",
        ],
        smell_text="The air is dry and sharp with ozone, carrying the clean electric scent of high-voltage data conduits and chilled processor coolant.",
        touch_text="The access panels vibrate faintly under your palm with the pulse of data flowing through the conduits, and the air is noticeably drier and cooler than the decks below.",
        ambient_sounds=[
            "A faint electronic hum pulses through the walls, like a heartbeat.",
            "Somewhere distant, a computer voice says a single word: 'Initializing.'",
            "You think you hear your own name whispered in the air ducts. You are probably imagining it.",
        ],
    )
    world.add_room(deck_h_junction)

    # ═══════════════════════════════════════════════════════════════════
    # DECK F - ENGINEERING (Access area, full engineering in Act 3)
    # ═══════════════════════════════════════════════════════════════════

    engineering_junction = Room(
        id="engineering_junction",
        name="Engineering Deck Access",
        deck="Deck F - Engineering",
        description=(
            "You climb up into a much larger, noisier space. Engineering. "
            "The air here thrums with the vibration of massive machinery - "
            "reactors, coolant pumps, plasma regulators. Pipes snake overhead "
            "in intricate geometries. Steam hisses from somewhere to the west.\n\n"
            "A blast door to the north is labeled MAIN ENGINEERING - AUTHORIZED "
            "PERSONNEL ONLY. It is slightly ajar, held open by a wedge of "
            "metal shoved beneath it. Someone didn't want it to close.\n\n"
            "A doorway to the east leads to a maintenance bay. The corridor "
            "continues west toward the reactor area, though a faded warning "
            "label reads RADIATION LEAK - DO NOT ENTER WITHOUT PROTECTION."
        ),
        exits={
            'down': Exit(
                direction='down',
                destination='deck_h_junction',
                description="You descend back to the AI core level."
            ),
            'north': Exit(
                direction='north',
                destination='main_engineering',
                description="You push through the partly-open blast door."
            ),
            'east': Exit(
                direction='east',
                destination='engineering_workshop',
                description="You enter the workshop."
            ),
            'west': Exit(
                direction='west',
                destination='reactor_antechamber',
                locked=True,
                lock_message="The reactor area requires radiation protection to enter safely.",
                required_flag="has_radiation_suit"
            ),
            'up': Exit(
                direction='up',
                destination='deck_e_junction',
                description="You climb to the security deck."
            ),
        },
        items=[
            "blast_door_wedge",
            "radiation_warning_sign",
            "pipe_network",
        ],
        smell_text="Machine oil, hot metal, and the acrid bite of leaked steam fill the air, thick enough to taste on the back of your tongue.",
        touch_text="The floor thrums with deep mechanical vibration that travels up through your boots and into your bones, and every surface is warm to the touch from the reactor's radiant heat.",
        ambient_sounds=[
            "The reactor's plasma containment cycles with a deep BA-THUMP that rattles your teeth.",
            "Steam hisses suddenly from a vent nearby. You jump.",
            "A pressure gauge nearby ticks steadily into the red zone.",
        ],
    )
    world.add_room(engineering_junction)

    main_engineering = Room(
        id="main_engineering",
        name="Main Engineering",
        deck="Deck F - Engineering",
        description=(
            "Main Engineering is a cathedral of technology - a vast three-story "
            "chamber built around the gleaming fusion reactor core that extends "
            "from ceiling to floor at its center. Catwalks ring the room at "
            "different heights. Monitoring stations line the walls, most of "
            "them showing warning lights.\n\n"
            "A primary control station sits elevated on a platform overlooking "
            "the reactor core. Someone is hunched over its controls, back to "
            "you - small, thin, in a grease-stained engineering jumpsuit. You "
            "can hear them muttering to themselves.\n\n"
            "They don't appear to have noticed you yet."
        ),
        smell_text="The cathedral-scale space smells of ionized plasma, lubricant grease, and the hot ozone tang of a fusion reactor running at capacity with no one left to tune it.",
        touch_text="The catwalk railing vibrates so intensely from the reactor core that your grip goes numb within seconds, and the air itself feels dense and electric against your skin.",
        exits={
            'south': Exit(
                direction='south',
                destination='engineering_junction',
                description="You back out of main engineering."
            ),
            'up': Exit(
                direction='up',
                destination='reactor_catwalk',
                description="You climb the stairs to the upper catwalk.",
                locked=True,
                required_flag="tanaka_met"
            ),
            'west': Exit(
                direction='west',
                destination='coolant_pump_room',
                description="You head toward the rhythmic thudding of the coolant pumps."
            ),
            'east': Exit(
                direction='east',
                destination='engineering_break_room',
                description="You duck through a doorway into the engineering break room."
            ),
            'down': Exit(
                direction='down',
                destination='plasma_conduit_junction',
                description="You descend a metal staircase into the plasma conduit junction below."
            ),
        },
        items=[
            "reactor_core",
            "primary_control_station",
            "monitoring_stations",
            "engineering_catwalks",
        ],
        npcs=["yuki_tanaka"],  # The living survivor
        ambient_sounds=[
            "The fusion reactor hums with a deep, resonant drone that makes your chest cavity vibrate in sympathy.",
            "Warning klaxons fire in short, sharp bursts from distant monitoring stations, then fall silent.",
            "You hear muttering from the control station - rapid, technical, edged with exhaustion and fear.",
        ],
        on_enter="event_first_see_tanaka",
    )
    world.add_room(main_engineering)

    engineering_workshop = Room(
        id="engineering_workshop",
        name="Engineering Workshop",
        deck="Deck F - Engineering",
        description=(
            "A well-equipped workshop filled with tools, workbenches, and "
            "half-finished projects. A spacesuit lies disassembled on one "
            "bench, its life support unit open. On another, someone was "
            "modifying a handheld plasma cutter - the work half-complete.\n\n"
            "Shelving units hold spare parts: circuit boards, power cells, "
            "servo motors, raw materials for the ship's fabricators. A set "
            "of lockers along one wall contain personal protective equipment - "
            "one marked HAZMAT, another marked RADIATION.\n\n"
            "A half-eaten sandwich sits beside a tablet on the main workbench. "
            "Whoever was working here left recently. Or at least, it looks recent."
        ),
        smell_text="Solder flux and machine grease mix with the stale, sour smell of the half-eaten sandwich, a strange domesticity in the middle of an engineering deck.",
        touch_text="The workbenches are scarred and pitted from years of use, and metal shavings prick your fingertips when you brush across the surfaces.",
        exits={
            'west': Exit(
                direction='west',
                destination='engineering_junction',
                description="You leave the workshop."
            ),
        },
        items=[
            "radiation_suit",    # Important - unlocks reactor area
            "hazmat_suit",
            "power_cell_pack",
            "modified_plasma_cutter",
            "workshop_tablet",
            "half_sandwich",
            "spare_parts_bin",
            "fabricator_unit",
        ],
        ambient_sounds=[
            "The fabricator unit cycles on and off with a low whir, calibrating itself for a job that was never queued.",
            "A loose servo motor on the disassembled spacesuit twitches periodically, making a soft clicking sound.",
            "Metal shavings clink faintly as the ship's vibration shifts them across the workbench.",
        ],
    )
    world.add_room(engineering_workshop)

    reactor_antechamber = Room(
        id="reactor_antechamber",
        name="Reactor Antechamber",
        deck="Deck F - Engineering",
        description=(
            "A low-ceilinged antechamber filled with the overwhelming hum of "
            "the fusion reactor on the other side of a massive lead-lined door. "
            "Your ears pop. The air tastes metallic. Even in the radiation suit, "
            "you can feel your skin prickling.\n\n"
            "Before you stands the Reactor Control Interface - a complex panel "
            "of dials, switches, and readouts. The main display shows critical "
            "warnings: COOLANT PRESSURE LOW. COURSE DRIFT DETECTED. PRIMARY "
            "THRUSTERS OFFLINE.\n\n"
            "This is where you need to be. If you can understand this interface, "
            "you might be able to save the ship."
        ),
        smell_text="The metallic taste of irradiated air fills your mouth, sharp and electric, undercut by the chemical reek of overheated lead shielding.",
        touch_text="Your skin prickles with static charge and your hair stands on end, and the reactor control dials are warm enough to feel through your gloves.",
        exits={
            'east': Exit(
                direction='east',
                destination='engineering_junction',
                description="You retreat back to the main engineering area."
            ),
            'north': Exit(
                direction='north',
                destination='reactor_core_interior',
                description="You push through the massive lead-lined door into the reactor core.",
                locked=True,
                lock_message="The reactor core door refuses to open. The radiation beyond is lethal without a suit.",
                required_flag="has_radiation_suit"
            ),
        },
        items=[
            "reactor_control_interface",  # Major puzzle
            "coolant_pressure_gauge",
            "course_readout",
            "thruster_status_panel",
        ],
        ambient_sounds=[
            "The reactor beyond the lead door emits a deep, bone-shaking thrum that you feel more than hear.",
            "The coolant pressure gauge needle ticks against its pin with a frantic, insistent rhythm.",
            "Geiger counter clicks from a wall-mounted sensor accelerate as you move closer to the reactor door.",
        ],
        radiation=5,  # Low but present
    )
    world.add_room(reactor_antechamber)

    reactor_catwalk = Room(
        id="reactor_catwalk",
        name="Reactor Upper Catwalk",
        deck="Deck F - Engineering",
        description=(
            "The upper catwalk overlooks the reactor core. From here you can "
            "see the whole engineering bay spread out below - the gleaming reactor, "
            "the monitoring stations, the distant glow of pilot lights on "
            "sleeping machinery. It feels like looking down into the heart of "
            "a titan.\n\n"
            "A secondary control station is up here - smaller than the main one "
            "below, but with specialized functions: manual override controls, "
            "emergency shutdowns, direct coolant valve access.\n\n"
            "Yuki told you this is where you'd find the manual thruster override."
        ),
        smell_text="Hot metal and plasma exhaust rise from the reactor below in shimmering thermals, carrying the sharp scent of superheated coolant and burning dust.",
        touch_text="The catwalk grating sways perceptibly underfoot, and the railing is almost too hot to grip, radiating heat from the reactor core just meters below.",
        exits={
            'down': Exit(
                direction='down',
                destination='main_engineering',
                description="You descend the catwalk stairs."
            ),
        },
        items=[
            "secondary_control_station",
            "manual_override_switch",
            "coolant_valves",
            "emergency_shutdown",
        ],
        ambient_sounds=[
            "The catwalk creaks and sways with each of your footsteps, metal groaning against metal.",
            "The reactor core below you pulses with a visible light that strobes through the grating, accompanied by a deep harmonic resonance.",
            "Coolant valves hiss periodically as automated systems try to compensate for the failing pressure.",
        ],
    )
    world.add_room(reactor_catwalk)

    # ═══════════════════════════════════════════════════════════════════
    # DECK E - SECURITY
    # ═══════════════════════════════════════════════════════════════════

    deck_e_junction = Room(
        id="deck_e_junction",
        name="Deck E Security Hub",
        deck="Deck E - Security",
        description=(
            "You emerge onto the security deck. The corridor is narrower here, "
            "walls lined with thick reinforced paneling and surveillance cameras. "
            "Most of the cameras are smashed. A red line painted on the floor "
            "indicates a secure area ahead - the armory and the brig.\n\n"
            "Signs of conflict are everywhere. Scorch marks on the walls. Bullet "
            "holes. A trail of blood leads from the north (security office) "
            "toward the east (armory).\n\n"
            "Whatever happened here, it happened fast and it happened badly."
        ),
        exits={
            'down': Exit(
                direction='down',
                destination='engineering_junction',
                description="You climb down toward engineering."
            ),
            'up': Exit(
                direction='up',
                destination='deck_d_hub',
                description="You climb up toward the living deck."
            ),
            'north': Exit(
                direction='north',
                destination='security_office',
                description="You enter the security office."
            ),
            'east': Exit(
                direction='east',
                destination='armory',
                locked=True,
                lock_message="The armory door is locked. A red keycard is required."
            ),
            'south': Exit(
                direction='south',
                destination='brig',
                description="You head toward the brig."
            ),
            'west': Exit(
                direction='west',
                destination='security_corridor_south',
                locked=True,
                lock_message="A barricade of overturned furniture blocks the corridor. You need a plasma cutter or explosives to clear it.",
                required_flag="barricade_cleared"
            ),
        },
        items=[
            "security_cameras_smashed",
            "blood_trail",
            "scorch_marks",
            "spent_shell_casings",
        ],
        smell_text="Cordite and burnt polymer cling to the reinforced walls, layered over the copper-heavy smell of dried blood and the sharp tang of scorched paint.",
        touch_text="Bullet holes dimple the walls in rough, puckered craters, and the floor is gritty with shattered camera glass and spent brass casings that roll under your boots.",
        ambient_sounds=[
            "An automated voice repeats: 'Security personnel, please report to the armory.'",
            "A camera with a cracked lens tries to track you, grinding its motors.",
            "You hear distant, echoing shouts. But when you listen, it's just the wind in the vents.",
        ],
    )
    world.add_room(deck_e_junction)

    security_office = Room(
        id="security_office",
        name="Security Office",
        deck="Deck E - Security",
        description=(
            "The office of Security Chief Lt. James Okafor, based on the "
            "nameplate on the desk. It is a mess. Tactical maps of the ship "
            "cover one wall, with red pins marking... something. Contamination "
            "zones, perhaps. Chains of custody.\n\n"
            "Okafor's desk is cluttered with reports, empty coffee cups, an "
            "overturned picture frame (showing a woman and two teenage boys "
            "when you right it). His chair is pushed back from the desk as if "
            "he stood up suddenly. A sidearm holster hangs empty from the chair.\n\n"
            "On the desk, a red book lies open. A personal log, handwritten "
            "in a tight, controlled script. And beside it, a small audio "
            "recorder, its red light still blinking. Whoever was in here left "
            "mid-recording."
        ),
        exits={
            'south': Exit(
                direction='south',
                destination='deck_e_junction',
                description="You leave Okafor's office."
            ),
            'east': Exit(
                direction='east',
                destination='monitoring_station',
                description="You step into the camera monitoring room."
            ),
            'west': Exit(
                direction='west',
                destination='interrogation_room',
                description="You push open the heavy door to the interrogation room."
            ),
        },
        items=[
            "okafors_red_book",       # Readable - MAJOR
            "okafors_audio_recorder", # Readable - MAJOR
            "tactical_map_contamination",
            "okafor_family_photo",
            "empty_coffee_cups",
            "okafor_desk",
            "red_keycard",            # Important - armory access
        ],
        smell_text="Stale coffee and gun oil permeate the cramped office, underlaid by the faint musk of a man who spent too many sleepless nights at his desk.",
        touch_text="The desk surface is sticky with coffee rings, and the red book's pages are stiff with handling, warped by the oils from Okafor's restless fingers.",
        ambient_sounds=[
            "The audio recorder clicks softly as its mechanism holds the pause, red light blinking in patient silence.",
            "A tactical map pin falls from the wall and bounces on the deck with a tiny metallic ping.",
            "The empty coffee cup rocks gently in its ring of dried residue, disturbed by some vibration you cannot identify.",
        ],
    )
    world.add_room(security_office)

    armory = Room(
        id="armory",
        name="Ship's Armory",
        deck="Deck E - Security",
        description=(
            "The armory is a small, heavily-reinforced room lined with weapon "
            "racks. Most of the racks are empty - whoever came in here took "
            "what they needed and left in a hurry. A few firearms remain, "
            "along with ammunition stores.\n\n"
            "A tactical rifle lies on the central table, its magazine beside "
            "it. A box of cartridges is open. Someone was preparing for a "
            "fight here.\n\n"
            "A weapons locker against the back wall is intact, secured by "
            "a biometric lock. A smaller locker labeled PERSONAL EFFECTS - "
            "CONFISCATED sits beside it, its latch broken open."
        ),
        exits={
            'west': Exit(
                direction='west',
                destination='deck_e_junction',
                description="You leave the armory."
            ),
            'east': Exit(
                direction='east',
                destination='evidence_locker',
                locked=True,
                lock_message="The evidence locker requires a red keycard to open.",
                key_id="red_keycard"
            ),
            'north': Exit(
                direction='north',
                destination='armory_vault',
                locked=True,
                lock_message="The vault door is sealed with a biometric lock. It requires Okafor's biometric data.",
                required_flag="has_okafor_biometrics"
            ),
        },
        items=[
            "tactical_rifle",        # Weapon
            "handgun",               # Weapon
            "ammunition_box",
            "biometric_weapons_locker",  # Locked
            "confiscated_effects_locker",
            "tear_gas_grenades",
            "tactical_vest",
        ],
        smell_text="Gun oil and cordite hang thick in the sealed room, mixed with the sharp chemical smell of tear gas residue leaking from a dented canister.",
        touch_text="The weapon racks are cold, oiled steel with empty slots that feel like missing teeth, and loose ammunition rolls across the table with a heavy, brassy weight.",
        ambient_sounds=[
            "The biometric weapons locker emits a low, periodic tone, requesting authentication from a dead man's hand.",
            "A loose magazine slides across the table as the ship shifts, metal scraping on metal.",
            "The ventilation system pushes air through the reinforced room with a deep, pressurized whoosh.",
        ],
    )
    world.add_room(armory)

    brig = Room(
        id="brig",
        name="Ship's Brig",
        deck="Deck E - Security",
        description=(
            "The brig consists of four holding cells, three of them empty, "
            "one of them not. The occupied cell holds a body - slumped in the "
            "corner, still wearing an orange prisoner jumpsuit. The cell door "
            "is open.\n\n"
            "On the wall beside the cell, someone has written in what looks "
            "like dried blood:\n\n"
            "        'IT'S NOT ME ANYMORE. WHATEVER YOU'RE LOOKING AT\n"
            "         DOESN'T REMEMBER BEING ME. DON'T TRUST IT.'\n\n"
            "You wonder if the message was meant as a warning... or an apology."
        ),
        exits={
            'north': Exit(
                direction='north',
                destination='deck_e_junction',
                description="You back out of the brig."
            ),
        },
        items=[
            "brig_body",
            "bloody_message",
            "empty_cells",
            "prisoner_personal_items",
        ],
        smell_text="The confined space reeks of old sweat, fear, and the iron tang of the blood used to write the message on the wall, still faintly sharp after all this time.",
        touch_text="The cell bars are cold and smooth, polished by desperate hands, and the bloody message on the wall is raised and rough like scar tissue beneath your fingertips.",
        ambient_sounds=[
            "The open cell door swings on its hinges with a slow, rusted creak that sets your teeth on edge.",
            "A ventilation grate in the ceiling rattles loosely, as if something just crawled past it.",
            "The overhead fluorescent light in the occupied cell buzzes and flickers, casting the body in stuttering shadow.",
        ],
        on_enter="event_see_brig",
    )
    world.add_room(brig)

    # ═══════════════════════════════════════════════════════════════════
    # DECK D (additional) - connects to medical area
    # ═══════════════════════════════════════════════════════════════════

    deck_d_hub = Room(
        id="deck_d_hub",
        name="Deck D Junction",
        deck="Deck D - Medical",
        description=(
            "A wide junction that connects the medical wing to the rest of the "
            "ship. The junction sits at the intersection of the ship's inter-"
            "deck stairwell and the main medical corridor. A stairwell at the "
            "center of the room climbs UP to the Deck C crew quarters, and "
            "descends DOWN to Deck E security. EAST leads into the medical "
            "corridor you explored earlier.\n\n"
            "The lighting here is better than elsewhere. The walls are cleaner. "
            "But something in the air - maybe just the accumulated weight of "
            "what you've seen - makes it hard to breathe. You realize you've "
            "been clenching your jaw."
        ),
        exits={
            'down': Exit(
                direction='down',
                destination='deck_e_junction',
                description="You descend the stairwell toward security."
            ),
            'up': Exit(
                direction='up',
                destination='deck_c_junction',
                description="You climb the stairwell up to the crew living deck."
            ),
            'east': Exit(
                direction='east',
                destination='medical_corridor',
                description="You return to the medical corridor."
            ),
        },
        items=[
            "junction_sign",
            "clean_walls",
        ],
        smell_text="The air is cleaner here than elsewhere on the ship, scrubbed by functioning ventilation, but carries a faint antiseptic undertone drifting from the medical wing to the east.",
        touch_text="The walls are smooth and recently cleaned, almost unsettlingly pristine compared to the chaos elsewhere, and the stairwell handrail is cool and dry beneath your palm.",
        ambient_sounds=[
            "The stairwell echoes with your footsteps, sending them spiraling up and down the shaft like fleeing ghosts.",
            "A distant automated announcement from the medical wing bleeds through the corridor, too faint to make out the words.",
            "The air recyclers hum with a steady, almost soothing tone that feels wrong given everything you have seen.",
        ],
    )
    world.add_room(deck_d_hub)

    # ═══════════════════════════════════════════════════════════════════
    # DECK C - LIVING QUARTERS
    # ═══════════════════════════════════════════════════════════════════

    deck_c_junction = Room(
        id="deck_c_junction",
        name="Deck C Crew Deck Junction",
        deck="Deck C - Living",
        description=(
            "The living deck is quieter than the others. Carpeted floors muffle "
            "your footsteps. Soft lighting in wall sconces creates the illusion "
            "of normal gravity and normal purpose. For a moment, you can almost "
            "believe the Prometheus is just a ship at sea, and the crew is "
            "just at dinner.\n\n"
            "Then you see the body in the recreation lounge doorway, and the "
            "illusion shatters.\n\n"
            "Doors lead off this central corridor: CAPTAIN'S QUARTERS (sealed), "
            "officer cabins, the mess hall, the arboretum, the observation "
            "lounge. A directory on the wall lists occupants. Someone has drawn "
            "Xs through most of the names in black marker."
        ),
        exits={
            'down': Exit(
                direction='down',
                destination='deck_d_hub',
                description="You descend to Deck D."
            ),
            'up': Exit(
                direction='up',
                destination='deck_b_junction',
                description="You climb up toward the science deck."
            ),
            'west': Exit(
                direction='west',
                destination='mess_hall',
                description="You enter the mess hall."
            ),
            'east': Exit(
                direction='east',
                destination='crew_corridor',
                description="You head into the crew cabin corridor."
            ),
            'south': Exit(
                direction='south',
                destination='captains_quarters',
                locked=True,
                lock_message="The Captain's quarters are sealed. You need the Bridge Access Card.",
                required_flag="has_bridge_card"
            ),
            'north': Exit(
                direction='north',
                destination='observation_lounge',
                description="You head into the observation lounge."
            ),
            'southwest': Exit(
                direction='southwest',
                destination='recreation_lounge',
                description="You step through the doorway into the recreation lounge, past the body."
            ),
            'southeast': Exit(
                direction='southeast',
                destination='sealed_corridor_c',
                description="You approach a barricaded corridor section.",
                locked=True,
                lock_message="The corridor is blocked by collapsed ceiling panels and a wall of furniture. You'd need a plasma cutter to get through.",
                required_flag="has_plasma_cutter"
            ),
        },
        items=[
            "crew_directory",
            "body_in_doorway",
            "ornate_carpet",
        ],
        smell_text="Carpet freshener and the ghost of cologne fight a losing battle against the unmistakable sweet decay rising from the body in the recreation lounge doorway.",
        touch_text="The carpeted floor is soft and silent under your feet, a jarring comfort after the metal grating of the lower decks, and the wall sconces radiate gentle warmth.",
        ambient_sounds=[
            "Soft music plays from a hidden speaker somewhere in the corridor, a classical piece on a warped loop that skips and repeats.",
            "The body in the doorway settles with a faint creak of stiffened joints and dried leather.",
            "A cabin door down the corridor clicks open, then gently closes, as if someone just stepped out for a moment.",
        ],
    )
    world.add_room(deck_c_junction)

    mess_hall = Room(
        id="mess_hall",
        name="Mess Hall",
        deck="Deck C - Living",
        description=(
            "The largest common space on Deck C, the mess hall could seat a "
            "hundred crew members at long communal tables. Remnants of a final, "
            "interrupted meal remain on many of them - trays still holding food "
            "that has dried to a stain, cups of coffee now grown dense and "
            "black. Several chairs are overturned. A few trays lie on the "
            "floor where they were dropped.\n\n"
            "At one table, seven place settings remain meticulously undisturbed. "
            "The food is gone, but the dishes are precisely arranged. Someone "
            "cleaned up. Someone ate alone at this empty table and washed their "
            "dishes afterward.\n\n"
            "On the wall, a large screen still displays the ship's daily menu "
            "for what was apparently the crew's 423rd day of the mission: "
            "'PAELLA NIGHT! Chef's choice, vegetarian available.'"
        ),
        exits={
            'east': Exit(
                direction='east',
                destination='deck_c_junction',
                description="You leave the mess hall."
            ),
            'north': Exit(
                direction='north',
                destination='galley',
                description="You enter the kitchen galley."
            ),
        },
        items=[
            "interrupted_meals",
            "seven_place_settings",
            "menu_display",
            "overturned_chairs",
            "dried_food_trays",
        ],
        smell_text="Dried food and sour coffee have baked into the tables and chairs over weeks of abandonment, a rancid cafeteria smell overlaid with the dusty staleness of sealed air.",
        touch_text="The communal tables are sticky with dried residue, and the meticulously cleaned place settings at the lone table are cool and smooth, arranged with unsettling precision.",
        ambient_sounds=[
            "The daily menu display hums with a faint electrical whine, still advertising paella night to an empty room.",
            "An overturned chair rocks slowly on its side, tapping the deck in an uneven rhythm.",
            "From the galley beyond, the refrigeration units cycle on with a shudder that rattles the dishes.",
        ],
    )
    world.add_room(mess_hall)

    galley = Room(
        id="galley",
        name="Kitchen Galley",
        deck="Deck C - Living",
        description=(
            "The ship's kitchen. Stainless steel gleams under harsh overhead "
            "lighting. Pots and pans hang from a rack above a large central "
            "prep island. An industrial oven, cold now. Refrigeration units "
            "that still hum, preserving food that no one will eat.\n\n"
            "A large knife block is missing two knives.\n\n"
            "On the prep island, ingredients are laid out for a meal that was "
            "never finished: onions diced, garlic chopped, a bowl of rice, "
            "a tray of seafood now unpleasantly fragrant. A wooden cutting "
            "board shows where a large knife was last set down - there's a "
            "smear of something dark on the wood, but it's not food."
        ),
        exits={
            'south': Exit(
                direction='south',
                destination='mess_hall',
                description="You leave the galley."
            ),
        },
        items=[
            "knife_block",
            "prep_island",
            "rotten_seafood",
            "cutting_board_stain",
            "refrigeration_unit",
            "chefs_journal",  # Readable - another perspective
            "sharp_knife",    # Weapon
        ],
        smell_text="Rotting seafood fills the galley with a stomach-turning stench of decomposition, thick and oily, cut by the sharper smell of chopped garlic and raw onion still sitting on the prep island.",
        touch_text="The stainless steel surfaces are cold and greasy, and the knife block's empty slots have a faintly sticky residue around their edges, as if the missing knives were pulled free in a hurry.",
        ambient_sounds=[
            "The refrigeration units hum and shudder, preserving food for a crew that will never eat it.",
            "A pot hanging from the overhead rack sways and clinks against its neighbor in a slow metallic chime.",
            "Something drips from the prep island into a puddle on the floor with a soft, regular plop.",
        ],
    )
    world.add_room(galley)

    observation_lounge = Room(
        id="observation_lounge",
        name="Observation Lounge",
        deck="Deck C - Living",
        description=(
            "The observation lounge is one of the most beautiful rooms on the "
            "ship. A massive curved viewport - thirty meters wide, reaching from "
            "floor to vaulted ceiling - fills the outer wall, revealing the "
            "endless void of space. Comfortable couches and tables are arranged "
            "to face the stars. A small bar sits to one side.\n\n"
            "And at the heart of the view: the brown dwarf. GRB-7734. A dim, "
            "reddish smudge against the stars, perfectly centered in the "
            "viewport. It is growing. Slowly, imperceptibly, but growing. "
            "You can see the stars around it shifting, their light bent by "
            "the gravitational pull of something dead and hungry.\n\n"
            "A woman sits in one of the couches facing the viewport. Her back "
            "is to you. She doesn't turn when you enter. Her head tilts toward "
            "the stars."
        ),
        exits={
            'south': Exit(
                direction='south',
                destination='deck_c_junction',
                description="You leave the lounge."
            ),
            'east': Exit(
                direction='east',
                destination='chapel',
                description="You pass through a doorway into the quiet of the chapel."
            ),
        },
        items=[
            "observation_viewport",
            "brown_dwarf_view",
            "comfort_couches",
            "observation_bar",
        ],
        smell_text="The observation bar's spilled liquor has dried into the upholstery, filling the room with a faint, sweet bourbon note beneath the cold, filtered air from the viewport seals.",
        touch_text="The viewport glass is ice-cold and perfectly smooth, and when you press your hand against it, the vast emptiness beyond seems to press back.",
        npcs=["woman_in_lounge"],  # Dead - will be revealed
        ambient_sounds=[
            "The viewport creaks softly as the hull flexes, the sound of a ship slowly losing its argument with physics.",
            "A glass on the bar rolls in a slow circle, driven by the ship's barely perceptible tumble.",
            "The woman on the couch does not breathe, does not move, and the silence around her is heavier than anywhere else on the ship.",
        ],
        on_enter="event_woman_in_lounge",
    )
    world.add_room(observation_lounge)

    captains_quarters = Room(
        id="captains_quarters",
        name="Captain's Quarters",
        deck="Deck C - Living",
        description=(
            "Captain Marcus Reeves's private quarters are austere but personal. "
            "A small desk holds a framed photograph of the captain with a "
            "younger man - his son, perhaps. A book of classical philosophy sits "
            "on the nightstand beside a thin-wire pair of reading glasses. A "
            "ship model - an ancient sailing vessel - sits on a shelf with apparent "
            "reverence.\n\n"
            "The bed is made. The room is tidy. And against one wall, a service "
            "sidearm has been placed on the desk with an orderly precision that "
            "makes your skin crawl: magazine on the left, frame on the right, "
            "one cartridge sitting upright in the center. Like a final ritual.\n\n"
            "In the center of the desk, alone, sits a small recording device. "
            "Its red light blinks, waiting."
        ),
        exits={
            'north': Exit(
                direction='north',
                destination='deck_c_junction',
                description="You leave the Captain's quarters."
            ),
        },
        items=[
            "captains_recorder",    # MAJOR - Reeves's final message
            "captains_philosophy_book",
            "captains_photo",
            "ship_model",
            "ceremonial_sidearm",   # Weapon
            "captains_bed",
            "captains_glasses",
            "captains_key",         # Grants bridge access flag
            "bridge_access_card",   # Grants bridge card flag
        ],
        smell_text="Old leather from the philosophy book and faint pipe tobacco linger in the austere quarters, mixed with the cold mineral scent of gun oil from the ritual sidearm on the desk.",
        touch_text="The bed is tightly made with military precision, the sheets taut enough to bounce a coin off, and the recording device is warm from its constantly blinking indicator light.",
        ambient_sounds=[
            "The recording device clicks faintly as its red light blinks, patient and waiting in the silence.",
            "The ship model's tiny rigging creaks on its shelf, swaying with the ship's drift.",
            "A clock on the wall ticks with mechanical precision, counting seconds that feel heavier than they should.",
        ],
        on_enter="event_enter_captains_quarters",
    )
    world.add_room(captains_quarters)

    crew_corridor = Room(
        id="crew_corridor",
        name="Crew Cabin Corridor",
        deck="Deck C - Living",
        description=(
            "A long corridor with numbered doors on either side - individual "
            "crew cabins. Name plates identify the occupants. Most of the "
            "doors are closed. One is ajar, light spilling out. Another has "
            "been forced open from outside, the frame splintered.\n\n"
            "You see names you don't recognize, and one you do: CABIN 23 - "
            "DR. A. CHEN. Your cabin. Your name. Your room.\n\n"
            "You don't remember anything about what's inside."
        ),
        exits={
            'west': Exit(
                direction='west',
                destination='deck_c_junction',
                description="You return to the junction."
            ),
            'north': Exit(
                direction='north',
                destination='cabin_chen',
                description="You approach your own cabin. It is unlocked."
            ),
            'east': Exit(
                direction='east',
                destination='cabin_patel',
                description="You enter Dr. Patel's cabin through the broken door."
            ),
            'south': Exit(
                direction='south',
                destination='cabin_lin',
                description="You enter Dr. Lin's cabin (the open one)."
            ),
            'northwest': Exit(
                direction='northwest',
                destination='cabin_okafor',
                description="You approach Lt. Okafor's cabin further down the corridor."
            ),
            'southwest': Exit(
                direction='southwest',
                destination='cabin_hassan',
                description="You head to Cpl. Hassan's cabin on the lower end of the corridor."
            ),
            'northeast': Exit(
                direction='northeast',
                destination='cabin_fletcher',
                description="You approach Ensign Fletcher's cabin near the end of the corridor."
            ),
            'southeast': Exit(
                direction='southeast',
                destination='arboretum',
                description="You slip through a side door into the arboretum."
            ),
        },
        items=[
            "numbered_doors",
            "cabin_directory",
            "broken_door_frame",
        ],
        smell_text="A dozen personal scents bleed through the cabin doors - soap, cologne, unwashed laundry, stale coffee - the accumulated residue of lives interrupted mid-routine.",
        touch_text="The corridor carpet is thin and worn from foot traffic, and the broken door frame is splintered outward, rough jagged wood and bent metal where someone forced their way in.",
        ambient_sounds=[
            "A personal alarm clock rings inside one of the closed cabins, muffled and insistent, calling someone who will never wake.",
            "The ajar cabin door creaks back and forth in the air current, light spilling and retreating in a slow pulse.",
            "Behind one of the closed doors, you hear something - music, maybe, or a recording playing on loop.",
        ],
    )
    world.add_room(crew_corridor)

    cabin_chen = Room(
        id="cabin_chen",
        name="Your Cabin (Dr. Chen)",
        deck="Deck C - Living",
        description=(
            "Your own quarters. Your room. You step inside and feel... nothing. "
            "No recognition. No comfort. You could be a stranger touring a "
            "museum of someone else's life.\n\n"
            "The room is small but personal. A single bed, neatly made. A desk "
            "covered in xenobiology texts and a holographic model of a cell "
            "structure you don't recognize. A framed photograph on the dresser: "
            "you, younger, standing on a beach with a laughing man. You have "
            "no memory of him. You don't know his name.\n\n"
            "A closet contains your uniforms, all stiff with starch. A drawer "
            "in the nightstand holds a small key and a sealed envelope with "
            "your own handwriting on it: 'READ THIS WHEN YOU WAKE UP.'"
        ),
        exits={
            'south': Exit(
                direction='south',
                destination='crew_corridor',
                description="You leave your cabin."
            ),
        },
        items=[
            "player_letter_to_self",  # CRUCIAL - reveals backstory
            "player_journal",          # Personal log
            "photo_of_stranger",       # Sanity hit
            "xenobiology_texts",       # Scientific knowledge
            "holographic_cell_model",
            "small_key_nightstand",    # Unlocks player locker
            "player_uniforms",
            "personal_bed",
            "player_nightstand",
        ],
        smell_text="Your own scent - you recognize it with a jolt, though you cannot name it - fills the small room, mixed with starched uniforms and the faint chemical tang of xenobiology reagents.",
        touch_text="The bed sheets are crisp with starch and perfectly cold, and the sealed envelope in the drawer is smooth under your trembling fingers, its flap sealed with wax.",
        ambient_sounds=[
            "The holographic cell model rotates with a faint, crystalline hum, casting shifting blue light across the walls.",
            "A photograph frame on the dresser buzzes with a low electrical current, the image of a stranger smiling at you in silence.",
            "The cabin is so quiet you can hear the blood in your own ears, rushing like a distant ocean.",
        ],
        on_enter="event_own_cabin_first_visit",
    )
    world.add_room(cabin_chen)

    cabin_lin = Room(
        id="cabin_lin",
        name="Dr. Lin's Cabin",
        deck="Deck C - Living",
        description=(
            "Dr. Sarah Lin's cabin is less tidy than her office - a personal space "
            "versus a professional one. Clothes are strewn across the bed. A "
            "half-drunk glass of wine sits on the desk beside a holographic "
            "picture frame that cycles through images of a smiling woman with "
            "family, friends, a golden retriever.\n\n"
            "A small religious icon - a Greek Orthodox cross - hangs on the wall. "
            "Someone has drawn a question mark beside it in marker. Then erased "
            "it. Then drawn it again.\n\n"
            "On her desk, her medical tablet is still powered on, displaying "
            "a patient file. The patient: herself."
        ),
        exits={
            'north': Exit(
                direction='north',
                destination='crew_corridor',
                description="You leave Dr. Lin's cabin."
            ),
        },
        items=[
            "lin_cabin_tablet",       # Her infection records
            "lin_wine_glass",
            "lin_photo_frame",
            "lin_cross",
            "lin_clothes",
        ],
        smell_text="Red wine and a fading floral perfume fill Dr. Lin's cabin, intimate and personal, with the faint medicinal undertone that followed her everywhere.",
        touch_text="The wine glass is cold and sticky with dried residue, and the holographic picture frame is warm from its constant cycling, smooth under your fingertips.",
        ambient_sounds=[
            "The holographic picture frame clicks softly as it cycles between images, each one a window into a life that no longer exists.",
            "The medical tablet on the desk emits a faint chime, requesting attention for a patient file that will never be closed.",
            "A garment slips from the pile on the bed and whispers to the floor like a sigh.",
        ],
    )
    world.add_room(cabin_lin)

    cabin_patel = Room(
        id="cabin_patel",
        name="Dr. Patel's Cabin",
        deck="Deck C - Living",
        description=(
            "Dr. Raj Patel's cabin was ransacked. Violently. Furniture overturned. "
            "Drawers emptied. Books and papers scattered everywhere. Someone was "
            "looking for something.\n\n"
            "An open wall safe gapes empty above the desk - whatever was inside "
            "is gone. But they missed something: a small data crystal taped to "
            "the underside of a drawer. You can see the edge of it if you look "
            "carefully.\n\n"
            "On the far wall, someone has spray-painted, in red:\n\n"
            "                'THE GARDEN IS LISTENING'"
        ),
        exits={
            'west': Exit(
                direction='west',
                destination='crew_corridor',
                description="You leave Patel's cabin."
            ),
        },
        items=[
            "patels_data_crystal",    # Hidden item
            "patels_wall_safe",
            "patels_desk",
            "ransacked_drawer",
            "red_spraypaint_warning",
            "scattered_research_notes",
        ],
        smell_text="Red spray paint fumes still cling to the far wall, sharp and chemical, mixing with the dusty smell of scattered papers and the faint musk of a ransacked room.",
        touch_text="Papers crunch underfoot, and the data crystal taped beneath the drawer is smooth and cold as ice, humming faintly with stored information against your fingertips.",
        ambient_sounds=[
            "Papers rustle across the floor in a draft that seems to come from nowhere, as if the room is still being searched.",
            "The empty wall safe clicks occasionally, its broken mechanism cycling through lock attempts.",
            "You hear a faint scratching from inside the wall, regular and deliberate, like someone writing.",
        ],
    )
    world.add_room(cabin_patel)

    # ═══════════════════════════════════════════════════════════════════
    # DECK B - SCIENCE
    # ═══════════════════════════════════════════════════════════════════

    deck_b_junction = Room(
        id="deck_b_junction",
        name="Deck B Science Junction",
        deck="Deck B - Science",
        description=(
            "The science deck is different from the rest of the ship. Cleaner. "
            "Whiter. More clinical. The walls gleam with polished polymer panels "
            "and bright LED lighting. This is where the Prometheus did its "
            "real work - where the knowledge was supposed to happen.\n\n"
            "Signs point to MAIN LAB (west), EXOBIOLOGY LAB (east), OBSERVATORY "
            "(north), and SPECIMEN STORAGE (south). A stairwell leads up to "
            "Deck A (Command).\n\n"
            "An automated voice from the overhead speakers is repeating: "
            "'Attention all personnel. Laboratory containment protocols are "
            "in effect. Exobiology Lab is sealed by executive order. Please "
            "comply with quarantine procedures.'\n\n"
            "Someone has taped a piece of paper over the voice speaker. In "
            "black marker: 'TOO LATE.'"
        ),
        exits={
            'down': Exit(
                direction='down',
                destination='deck_c_junction',
                description="You descend to the living deck."
            ),
            'up': Exit(
                direction='up',
                destination='deck_a_junction',
                description="You climb toward the command deck."
            ),
            'west': Exit(
                direction='west',
                destination='main_lab',
                description="You enter the main laboratory."
            ),
            'east': Exit(
                direction='east',
                destination='exobio_lab_airlock',
                description="You approach the exobiology lab."
            ),
            'north': Exit(
                direction='north',
                destination='observatory',
                description="You head to the observatory."
            ),
            'south': Exit(
                direction='south',
                destination='specimen_storage',
                description="You enter specimen storage."
            ),
            'southwest': Exit(
                direction='southwest',
                destination='conference_room',
                description="You enter the mission briefing room."
            ),
            'northwest': Exit(
                direction='northwest',
                destination='xenolinguistics_lab',
                description="You head into the xenolinguistics lab."
            ),
        },
        items=[
            "voice_speaker_taped",
            "directional_signs",
            "clean_polymer_walls",
        ],
        smell_text="Clean-room sterility and the faint ozone of laboratory air purifiers fill the corridor, so aggressively sanitized that it almost smells like nothing at all.",
        touch_text="The polished polymer walls are smooth as glass and slightly warm from the LED panels behind them, and the air feels pressurized and dense against your eardrums.",
        ambient_sounds=[
            "The quarantine announcement loops endlessly: 'Exobiology Lab is sealed by executive order. Please comply with quarantine procedures.'",
            "A centrifuge somewhere in the labs spins down with a descending whine, losing momentum it will never regain.",
            "The piece of paper taped over the speaker flutters with each announcement, the word 'TOO LATE' dancing in the air current.",
        ],
    )
    world.add_room(deck_b_junction)

    main_lab = Room(
        id="main_lab",
        name="Main Laboratory",
        deck="Deck B - Science",
        description=(
            "A general-purpose research laboratory. Rows of workbenches are "
            "covered with experiments in various states of incompletion - petri "
            "dishes, sample vials, microscopes, centrifuges. A holographic "
            "display in the center of the room shows the molecular structure "
            "of something you don't recognize. The structure rotates slowly, "
            "patiently, waiting for the researcher who will never return.\n\n"
            "Notes and equations cover a whiteboard wall. Toward the bottom, "
            "one scrawled sentence in Dr. Patel's handwriting stands out: "
            "'THE PATTERNS MATCH. IT'S BUILDING SOMETHING.'\n\n"
            "Beneath that, in different handwriting: 'RAJ, PLEASE LISTEN. YOU "
            "HAVE TO STOP LOOKING. - S.'"
        ),
        exits={
            'east': Exit(
                direction='east',
                destination='deck_b_junction',
                description="You leave the main lab."
            ),
            'south': Exit(
                direction='south',
                destination='chemistry_lab',
                description="You pass through a connecting door into the chemistry lab."
            ),
            'west': Exit(
                direction='west',
                destination='botany_lab',
                description="You enter the botany research lab."
            ),
        },
        items=[
            "holographic_molecule",
            "whiteboard_equations",
            "patels_warning_note",
            "petri_dishes",
            "sample_vials",
            "centrifuge",
            "research_microscope",
            "lab_datapad",
        ],
        smell_text="Chemical reagents and ethanol preservative hang in the filtered air, sharp and clinical, with the faint chalky smell of whiteboard marker and the organic tang of abandoned petri dish cultures.",
        touch_text="The workbench surfaces are smooth laminate, cool to the touch and spotted with dried chemical stains, and the holographic molecule display tingles your skin with static when you pass through it.",
        ambient_sounds=[
            "The holographic molecule display hums at a frequency that sits right at the edge of hearing, almost subliminal.",
            "A centrifuge in the corner clicks as its rotor settles, counting down to stillness.",
            "Whiteboard markers roll across the tray at the base of the equation wall, nudged by the ship's imperceptible drift.",
        ],
    )
    world.add_room(main_lab)

    exobio_lab_airlock = Room(
        id="exobio_lab_airlock",
        name="Exobiology Lab Airlock",
        deck="Deck B - Science",
        description=(
            "A sterile white airlock separates the general science deck from "
            "the exobiology lab. Three sets of doors: the one behind you, a "
            "second just ahead for decontamination, and a third beyond that "
            "leading into the lab proper.\n\n"
            "A control panel requires biometric authentication. A sign reads: "
            "AUTHORIZED PERSONNEL: Dr. R. Patel, Dr. A. Chen, Captain M. Reeves.\n\n"
            "You are Dr. Chen. You should have access."
        ),
        exits={
            'west': Exit(
                direction='west',
                destination='deck_b_junction',
                description="You leave the airlock."
            ),
            'east': Exit(
                direction='east',
                destination='exobio_lab',
                description="You proceed into the exobiology lab.",
                locked=True,
                lock_message="The biometric scanner needs to read your handprint. Try using it."
            ),
        },
        items=[
            "biometric_scanner",
            "authorization_sign",
            "decontamination_chamber",
        ],
        smell_text="The sterile airlock smells of nothing, which is itself a smell - the aggressive absence of organic matter, scrubbed clean by UV sterilizers and chemical wash.",
        touch_text="The biometric scanner glass is smooth and body-warm, waiting for a handprint, and the airlock walls are sealed so tightly that you can feel the slight pressure differential against your eardrums.",
        ambient_sounds=[
            "The decontamination chamber between the doors hisses softly, cycling UV lights in an automated sterilization pattern.",
            "The biometric scanner beeps once, twice, then falls silent, as if clearing its throat.",
            "A faint vibration comes through the inner door - something on the other side, humming at a frequency that makes your fillings ache.",
        ],
        on_enter="event_exobio_airlock_memory",
    )
    world.add_room(exobio_lab_airlock)

    exobio_lab = Room(
        id="exobio_lab",
        name="Exobiology Laboratory",
        deck="Deck B - Science",
        description=(
            "The exobiology lab is where the Prometheus mission's purpose "
            "truly lived. At the far end of the room, inside a containment "
            "field that pulses weakly, sits a pedestal. On the pedestal rests "
            "the reason for this entire mission.\n\n"
            "THE ARTIFACT.\n\n"
            "A crystalline shard, perhaps thirty centimeters long, black and "
            "shot through with veins of liquid silver that pulse in slow, "
            "rhythmic patterns. It looks wrong. Not alien - *wrong*. As if "
            "geometry got nauseous looking at it.\n\n"
            "You remember this. You remember standing exactly here, looking "
            "at exactly this, and feeling the same nausea you feel now. And "
            "underneath it, the same terrible curiosity.\n\n"
            "The containment field is still holding. Barely. The energy readings "
            "fluctuate on the wall-mounted display. And the Seed is... watching you."
        ),
        exits={
            'west': Exit(
                direction='west',
                destination='exobio_lab_airlock',
                description="You back out of the exobiology lab."
            ),
        },
        items=[
            "the_artifact",          # The Seed
            "containment_field",
            "artifact_pedestal",
            "energy_readings_display",
            "exobio_notes_terminal",
            "test_tube_samples",
        ],
        smell_text="The containment field gives the air a metallic, electric taste, like licking a battery, and beneath it lurks something older and stranger - the Seed's presence, smelling of wet stone and copper.",
        touch_text="The air near the containment field raises every hair on your body, and when you reach toward the Artifact, your fingertips tingle with a warmth that has nothing to do with temperature.",
        ambient_sounds=[
            "The containment field pulses with a low, rhythmic thrum that syncs uncomfortably with your heartbeat.",
            "The Artifact's silver veins make a sound like distant singing, beautiful and terrible, at the very edge of perception.",
            "Energy readings on the wall display click and shift in patterns that almost seem deliberate, as if something is communicating.",
        ],
        on_enter="event_see_artifact",
    )
    world.add_room(exobio_lab)

    observatory = Room(
        id="observatory",
        name="Stellar Observatory",
        deck="Deck B - Science",
        description=(
            "A domed observatory with a transparent ceiling looking out onto "
            "space. Massive telescopes and sensor arrays crowd the center of "
            "the room. A holographic star map dominates one wall, showing the "
            "ship's projected path and current position relative to known space.\n\n"
            "The projected path is not good. The ship has drifted far from its "
            "intended trajectory and is now on a collision course with GRB-7734. "
            "The math is simple. The math is terrible.\n\n"
            "A workstation here is running a targeting analysis - the operator "
            "was apparently trying to calculate a precise burn sequence to "
            "correct the ship's course. Their work is almost complete. They "
            "left halfway through entering the final coordinates."
        ),
        exits={
            'south': Exit(
                direction='south',
                destination='deck_b_junction',
                description="You leave the observatory."
            ),
            'up': Exit(
                direction='up',
                destination='telescope_observation_deck',
                description="You climb the service ladder up to the upper observation deck."
            ),
        },
        items=[
            "observatory_telescope",
            "holographic_star_map",
            "targeting_analysis",     # Puzzle - navigation
            "astronomer_workstation",
            "sensor_array",
            "observation_log",
        ],
        smell_text="The observatory smells of telescope lubricant and warm electronics, with the faint ozonic tang of sensor arrays running at full power.",
        touch_text="The transparent dome overhead is cool to the touch and faintly curved, and the telescope eyepieces are smooth brass worn to a shine by hands that spent too many hours watching the stars die.",
        ambient_sounds=[
            "The telescope tracking motors whir and click as they follow a pre-programmed observation pattern across the void.",
            "The holographic star map crackles faintly, projecting the ship's doomed trajectory in cold blue light.",
            "The dome creaks overhead as thermal gradients shift across its surface, a sound like ice forming on a pond.",
        ],
    )
    world.add_room(observatory)

    specimen_storage = Room(
        id="specimen_storage",
        name="Specimen Storage",
        deck="Deck B - Science",
        description=(
            "A cold, sterile storage area lined with environmental containment "
            "units. Each one holds a biological sample from the ship's mission - "
            "soil from Kepler-442b's surface, ice core samples, rock specimens, "
            "organic extracts. Most of the containers are stable. A few have "
            "warning lights.\n\n"
            "One particular container has shattered. Its contents - a small, "
            "dark growth that looks like oxidized crystal - have spread onto "
            "the surrounding counter and down the side of the unit. The growth "
            "is patterned. It looks almost intentional. Almost like it was "
            "*trying* to go somewhere.\n\n"
            "The trail leads into a ventilation grate in the floor."
        ),
        exits={
            'north': Exit(
                direction='north',
                destination='deck_b_junction',
                description="You leave specimen storage."
            ),
            'east': Exit(
                direction='east',
                destination='specimen_quarantine',
                description="You approach the triple-sealed quarantine door at the far end.",
                locked=True,
                lock_message="The quarantine containment door requires Level 5 biohazard clearance.",
                required_flag="has_biohazard_clearance"
            ),
        },
        items=[
            "containment_units",
            "shattered_container",
            "crystal_growth_trail",
            "ventilation_grate_floor",
            "ice_core_samples",
            "specimen_logbook",
        ],
        smell_text="Cold preservative chemicals and the dry mineral scent of alien soil samples fill the room, but near the shattered container, something organic and sweet makes your nose wrinkle involuntarily.",
        touch_text="The containment units are frigid to the touch, beaded with condensation, and the crystal growth trail on the counter feels warm and faintly pulsing, like touching a vein.",
        ambient_sounds=[
            "Warning lights on damaged containment units chirp in irregular, overlapping sequences, a chorus of small emergencies.",
            "The crystal growth trail makes a faint crackling sound, like ice expanding, though the room is cold enough that nothing should be growing.",
            "Air whispers through the ventilation grate in the floor where the growth trail disappears, carrying sounds from deep in the ship's ductwork.",
        ],
    )
    world.add_room(specimen_storage)

    # ═══════════════════════════════════════════════════════════════════
    # DECK A - COMMAND (BRIDGE)
    # ═══════════════════════════════════════════════════════════════════

    deck_a_junction = Room(
        id="deck_a_junction",
        name="Deck A Command Deck",
        deck="Deck A - Command",
        description=(
            "The command deck is the nerve center of the Prometheus. A broad "
            "hallway lined with meeting rooms and offices leads forward toward "
            "the bridge. Portraits of historical Earth explorers - Shackleton, "
            "Amundsen, Gagarin, Armstrong - line the walls. Their eyes seem to "
            "follow you.\n\n"
            "The bridge door is directly NORTH, sealed by a heavy blast door "
            "that requires command authorization. To the WEST is the Captain's "
            "Ready Room. To the EAST, the Communications Array. A stairwell "
            "behind you descends DOWN back to the science deck.\n\n"
            "The air here is very still. Very quiet. As if the ship is holding "
            "its breath."
        ),
        exits={
            'down': Exit(
                direction='down',
                destination='deck_b_junction',
                description="You descend back to the science deck."
            ),
            'north': Exit(
                direction='north',
                destination='bridge',
                locked=True,
                lock_message="The bridge blast door requires Captain-level authorization.",
                required_flag="has_captains_key"
            ),
            'west': Exit(
                direction='west',
                destination='ready_room',
                description="You enter the Captain's Ready Room."
            ),
            'east': Exit(
                direction='east',
                destination='comms_array',
                description="You head to the communications array."
            ),
            'southwest': Exit(
                direction='southwest',
                destination='life_support_central',
                description="You follow a service corridor to the life support control room."
            ),
            'southeast': Exit(
                direction='southeast',
                destination='bridge_crew_quarters',
                description="You enter the bridge crew bunk area."
            ),
        },
        items=[
            "explorer_portraits",
            "bridge_blast_door",
        ],
        smell_text="Filtered air and the faint scent of old paper from the portrait frames fill the command corridor, clean and still, like a museum after hours.",
        touch_text="The blast door is cold, heavy steel that does not yield when you push against it, and the portrait frames are dusty under your fingertips, the glass cool and smooth.",
        ambient_sounds=[
            "The bridge blast door hums with a low electromagnetic field, its locking mechanism powered and waiting.",
            "Your footsteps echo off the polished floor with a sharp, authoritative crack that sounds wrong in the emptiness.",
            "The portraits' eyes seem to follow you, though you know it is only the silence playing tricks on your exhausted mind.",
        ],
    )
    world.add_room(deck_a_junction)

    bridge = Room(
        id="bridge",
        name="Bridge",
        deck="Deck A - Command",
        description=(
            "The bridge of the ISV Prometheus is a broad, arc-shaped command "
            "center facing a massive forward viewport that dominates the far "
            "wall. Through the viewport, you can see the glowing red menace "
            "of the brown dwarf, closer now than it appeared from the "
            "observation lounge, filling perhaps a third of the visible sky. "
            "It is not rushing toward you. It is implacable.\n\n"
            "Officer stations are arranged in a horseshoe before the captain's "
            "chair at the room's center. Tactical. Navigation. Science. "
            "Communications. Helm. All empty. All waiting for operators who "
            "will never sit at them again.\n\n"
            "The captain's chair is empty. On its armrest, a bloody handprint. "
            "On the deck below, a single spent shell casing.\n\n"
            "A large heads-up display hovers above the captain's chair, showing "
            "ship status. Critical systems are flashing red. A timer in the "
            "corner counts down inexorably."
        ),
        exits={
            'south': Exit(
                direction='south',
                destination='deck_a_junction',
                description="You leave the bridge."
            ),
            'west': Exit(
                direction='west',
                destination='tactical_operations',
                description="You step into the tactical operations room."
            ),
            'east': Exit(
                direction='east',
                destination='navigation_computer_room',
                description="You enter the navigation computer room."
            ),
            'north': Exit(
                direction='north',
                destination='bridge_escape_pod',
                description="You open the concealed hatch to the emergency escape pod bay.",
                hidden=True,
                lock_message="You don't see an exit in that direction."
            ),
        },
        items=[
            "captains_chair",
            "forward_viewport",
            "helm_station",
            "tactical_station",
            "nav_station",
            "bridge_hud",
            "bloody_handprint",
            "spent_shell_casing_bridge",
        ],
        smell_text="The bridge smells of leather from the captain's chair, stale recycled air, and the faint iron tang of the bloody handprint drying on the armrest.",
        touch_text="The captain's chair armrest is tacky with dried blood, and the helm controls are cold and unresponsive, dead instruments waiting for hands that will never return.",
        ambient_sounds=[
            "The countdown timer ticks with a soft, inexorable click that seems to grow louder the longer you listen.",
            "The forward viewport creaks under the thermal stress of the brown dwarf's radiation, a sound like a giant slowly exhaling.",
            "Ship status alerts chime from empty officer stations, each one a question asked to no one.",
        ],
        on_enter="event_first_bridge",
    )
    world.add_room(bridge)

    ready_room = Room(
        id="ready_room",
        name="Captain's Ready Room",
        deck="Deck A - Command",
        description=(
            "The Captain's Ready Room is a small private office adjacent to "
            "the bridge. Unlike his personal quarters on Deck C, this space "
            "is purely functional: a desk, two chairs for visitors, a wall of "
            "status monitors, a small liquor cabinet.\n\n"
            "On the desk, a computer terminal is still active. Its screen "
            "displays a text file that has been edited recently. The title: "
            "'PROTOCOL AEGIS - EXECUTION ORDER.'\n\n"
            "The order is incomplete. It lacks only the Captain's final "
            "authorization."
        ),
        exits={
            'east': Exit(
                direction='east',
                destination='deck_a_junction',
                description="You leave the Ready Room."
            ),
            'south': Exit(
                direction='south',
                destination='captains_ready_suite',
                description="You push through a narrow door into the Captain's private quarters."
            ),
        },
        items=[
            "readyroom_terminal",     # Protocol Aegis
            "liquor_cabinet",
            "status_monitors",
            "visitor_chairs",
        ],
        smell_text="Fine whiskey from the open liquor cabinet perfumes the small room, mixing with the warm electronics smell of the active terminal and the stale air of a sealed space.",
        touch_text="The terminal keyboard is warm from continuous operation and slightly sticky under your fingers, and the visitor chairs are cold leather that has not been sat in for weeks.",
        ambient_sounds=[
            "The terminal screen flickers as it displays Protocol Aegis, the cursor blinking where the Captain's authorization should go.",
            "The liquor cabinet door swings gently on loose hinges, tapping the frame with each oscillation.",
            "Status monitors on the wall cycle through red warnings in silence, each one a crisis that will never be resolved.",
        ],
        on_enter="event_see_protocol_aegis",
    )
    world.add_room(ready_room)

    comms_array = Room(
        id="comms_array",
        name="Communications Array",
        deck="Deck A - Command",
        description=(
            "The Communications Array is smaller than you'd expect - most of the "
            "ship's comms hardware is external, distributed across the hull. "
            "This is the operator's station. A bank of displays, an antenna "
            "tuning console, a long-range transmission rig.\n\n"
            "The operator didn't make it to their post. Ensign Mark Fletcher, "
            "according to the duty roster on the wall. His body lies sprawled "
            "across the main console, arms still reaching for the transmit key. "
            "A single bullet wound in the back of the head.\n\n"
            "Someone didn't want a distress call going out."
        ),
        exits={
            'west': Exit(
                direction='west',
                destination='deck_a_junction',
                description="You leave the communications array."
            ),
            'north': Exit(
                direction='north',
                destination='communications_relay',
                description="You duck through a maintenance hatch into the relay hardware room."
            ),
        },
        items=[
            "fletcher_body",
            "comms_main_console",    # Puzzle - send distress
            "antenna_tuner",
            "transmit_key",
            "duty_roster_wall",
            "fletcher_pocket_items",
        ],
        smell_text="Warm electronics and the metallic scent of radio frequency shielding fill the room, overlaid by the unmistakable copper smell of blood pooling around the dead operator.",
        touch_text="The transmit key is slick with the dead man's fingertips' last desperate oils, and the console is warm from hours of unattended operation, its switches toggled mid-broadcast.",
        ambient_sounds=[
            "Static hisses from the long-range transmission rig, punctuated by bursts of signal that might be cosmic noise or might be something trying to answer.",
            "The antenna tuning console clicks through frequencies in an automated sweep, searching for a reply that will never come.",
            "A duty roster page tears loose from the wall and drifts to the floor with a soft, papery whisper.",
        ],
    )
    world.add_room(comms_array)

    # ═══════════════════════════════════════════════════════════════════
    # DECK C EXPANSION - Living Quarters (new rooms)
    # ═══════════════════════════════════════════════════════════════════

    recreation_lounge = Room(
        id="recreation_lounge",
        name="Recreation Lounge",
        deck="Deck C - Living",
        description=(
            "A large common room meant for off-duty relaxation. Gaming tables "
            "fill the center of the space - a chess set with pieces still mid-game, "
            "a scattered deck of cards, and a holographic game board frozen in a "
            "spectral blue glow, its last match forever unfinished. A small "
            "bookshelf against one wall holds a curated collection of physical "
            "books, their spines cracked from use. Entertainment screens line "
            "the far wall, one still displaying a comedy show frozen mid-frame, "
            "the host's mouth open in a laugh that will never land.\n\n"
            "A body lies in the doorway leading back to the junction. The pool "
            "of dried blood beneath it has turned black and flaky, soaked into "
            "the carpet in a wide, irregular stain. You had to step over it to "
            "get in here. A dartboard on the wall has a crew photograph pinned "
            "to its center, riddled with dart holes. The face is unrecognizable.\n\n"
            "Despite the horror, there is something achingly normal about this "
            "room. People laughed here. People were happy here. That feels like "
            "a long time ago."
        ),
        smell_text=(
            "The room smells of stale air and old blood, undercut by the faint "
            "ghost of microwave popcorn from some ancient movie night."
        ),
        touch_text=(
            "The gaming tables are smooth synthetic wood, still slightly sticky "
            "from spilled drinks. The chess pieces are cold metal, weighted and "
            "satisfying in the hand."
        ),
        exits={
            'northeast': Exit(
                direction='northeast',
                destination='deck_c_junction',
                description="You step back out into the crew deck junction."
            ),
            'north': Exit(
                direction='north',
                destination='gymnasium',
                description="You head through the connecting door into the gymnasium."
            ),
        },
        items=[
            "chess_set_midgame",
            "holographic_game_board",
            "physical_book_collection",
            "frozen_comedy_screen",
            "dartboard_photo",
            "recreation_body",
        ],
        ambient_sounds=[
            "The holographic game board emits a low electronic hum, cycling through phantom colors.",
            "A entertainment screen flickers briefly, the frozen laugh track stuttering for half a second before going silent.",
            "Somewhere in the ceiling, an air recycler wheezes like a tired animal.",
        ],
    )
    world.add_room(recreation_lounge)

    arboretum = Room(
        id="arboretum",
        name="Ship's Arboretum",
        deck="Deck C - Living",
        description=(
            "You push through the door and stop. For a moment, you forget "
            "where you are. The arboretum is a small glass-ceilinged garden "
            "tucked into the starboard hull, and it is alive. Earth plants - "
            "only Earth plants, nothing alien, nothing contaminated. Roses climb "
            "a trellis near the entrance, their blooms deep red and impossibly "
            "fragrant. Ferns spill from hanging baskets. A dwarf Japanese maple "
            "spreads its delicate leaves over a small stone path.\n\n"
            "A fountain at the center still trickles water over polished stones, "
            "the soft sound filling the space with something you haven't heard "
            "in a long time: peace. Soft grow-lights simulate golden afternoon "
            "sunlight. Hidden speakers play birdsong - finches, cardinals, the "
            "distant call of a mourning dove. Someone programmed this with love.\n\n"
            "A wooden bench sits beneath the maple. Carved into its backrest in "
            "careful, deliberate letters: 'For Sarah, who loved growing things.' "
            "The bench is worn smooth from use. Someone sat here often. Someone "
            "found refuge here when the rest of the ship was falling apart."
        ),
        smell_text=(
            "The air is thick with the scent of roses, damp earth, and green "
            "growing things. It smells like a garden on Earth after rain. You "
            "didn't know how much you needed this."
        ),
        touch_text=(
            "The bench wood is warm and satin-smooth under your fingers. The "
            "rose petals are impossibly soft, fragile as tissue paper. The "
            "fountain water is cool and clean."
        ),
        exits={
            'northwest': Exit(
                direction='northwest',
                destination='crew_corridor',
                description="You reluctantly leave the arboretum."
            ),
        },
        items=[
            "arboretum_roses",
            "japanese_maple_tree",
            "stone_fountain",
            "memorial_bench",
            "hanging_fern_baskets",
            "birdsong_speakers",
        ],
        ambient_sounds=[
            "Water trickles over smooth stones in the fountain, a sound like quiet laughter.",
            "A simulated cardinal calls from the hidden speakers, bright and clear and heartbreaking.",
            "The grow-lights hum softly, warming the leaves above you.",
        ],
        flags=["sanity_restoration"],
    )
    world.add_room(arboretum)

    chapel = Room(
        id="chapel",
        name="Multi-Faith Chapel",
        deck="Deck C - Living",
        description=(
            "A small, quiet room designed to serve every faith and none. Simple "
            "wooden pews face a plain altar at the front. Behind the altar, a "
            "wall of frosted glass is backlit with a warm amber glow. Religious "
            "icons from a dozen traditions are arranged along the side walls "
            "with careful respect: a crucifix, a menorah, a crescent moon, a "
            "dharma wheel, a Shinto gate, others you don't recognize. Each is "
            "given equal space, equal light.\n\n"
            "Electric candles flicker in small alcoves, casting wavering shadows "
            "that make the icons seem to breathe. Prayer cards and personal "
            "messages have been left on the pews and tucked into every available "
            "crevice - folded papers, handwritten notes, photographs, a child's "
            "drawing of a house with 'COME HOME DADDY' in crayon. Reading them "
            "is devastating. Each one is a world ending.\n\n"
            "A small confession booth in the corner has its curtain drawn back. "
            "Inside, someone has written their final words on the wooden wall "
            "in trembling handwriting. The ink has run in places, blurred by "
            "what might have been tears."
        ),
        smell_text=(
            "Faint incense lingers in the air - someone burned it recently "
            "enough that the scent still clings to the wood. Beneath it, the "
            "dry smell of old paper and candle wax."
        ),
        touch_text=(
            "The pew wood is polished smooth by hundreds of hands seeking "
            "comfort. The prayer cards are soft and worn, some damp, as if "
            "the grief soaked into the paper itself."
        ),
        exits={
            'west': Exit(
                direction='west',
                destination='observation_lounge',
                description="You step back out into the observation lounge."
            ),
        },
        items=[
            "chapel_prayer_cards",
            "confession_booth_writing",
            "religious_icons_wall",
            "electric_candles",
            "childs_drawing",
            "chapel_altar",
        ],
        ambient_sounds=[
            "The electric candles flicker with a faint, rhythmic click.",
            "Silence. True silence. The kind that makes you aware of your own heartbeat.",
            "A creak from the pews, as if someone just stood up. But you are alone.",
        ],
        flags=["sanity_restoration"],
    )
    world.add_room(chapel)

    gymnasium = Room(
        id="gymnasium",
        name="Ship's Gymnasium",
        deck="Deck C - Living",
        description=(
            "The gymnasium is a wide, open space that smells of rubber mats "
            "and old sweat. Exercise machines line the walls - treadmills, "
            "resistance trainers, zero-g pull-up bars. A small boxing ring "
            "occupies one corner, its ropes sagging. Mats cover the floor in "
            "a central sparring area.\n\n"
            "Someone barricaded themselves in here. The main doors have been "
            "reinforced from the inside with weight benches, a squat rack, and "
            "what looks like half a disassembled treadmill, all braced against "
            "the frame with desperate ingenuity. Whoever built this fortress "
            "knew what they were doing and had time to do it right.\n\n"
            "Behind the barricade, in the far corner of the room, a body sits "
            "propped against the wall. A man in workout clothes, thin and "
            "desiccated, surrounded by empty water bottles and protein bar "
            "wrappers. He held out for days. A small personal audio recorder "
            "rests in his lap, its battery indicator blinking the last red "
            "sliver of charge."
        ),
        smell_text=(
            "Rubber, stale sweat, and the dry, papery smell of a body that "
            "died slowly. The air is thick and still, sealed in by the "
            "barricade for who knows how long."
        ),
        touch_text=(
            "The exercise mats are firm and slightly tacky underfoot. The "
            "barricade is solid, expertly constructed - the weight benches "
            "are wedged tight, immovable."
        ),
        exits={
            'south': Exit(
                direction='south',
                destination='recreation_lounge',
                description="You climb back over the barricade into the recreation lounge."
            ),
        },
        items=[
            "gym_barricade",
            "barricade_body",
            "gym_audio_recorder",     # Audio log - survivor's final days
            "empty_water_bottles",
            "boxing_ring",
            "exercise_machines",
        ],
        ambient_sounds=[
            "A treadmill belt creaks as the ship shifts, the machine rocking slightly on its base.",
            "The barricade groans under its own weight, metal settling against metal.",
            "You hear a faint dripping from somewhere in the ceiling - condensation from sealed, stagnant air.",
        ],
    )
    world.add_room(gymnasium)

    cabin_okafor = Room(
        id="cabin_okafor",
        name="Lt. Okafor's Cabin",
        deck="Deck C - Living",
        description=(
            "Lieutenant James Okafor's personal quarters are military-neat "
            "despite the chaos that consumed the rest of the ship. The bed is "
            "made with hospital corners. His boots sit paired beneath the bunk. "
            "Uniforms hang in the closet, pressed and ordered by occasion. The "
            "man brought discipline with him into the dark.\n\n"
            "Family photographs cover the small desk: his wife Adanna, radiant "
            "in a yellow sundress; his sons Chidi and Emeka in football "
            "uniforms, grinning with the invincibility of teenagers. A half-"
            "written letter sits beside the photos, the pen still resting on "
            "the paper. 'My dearest Adanna, I don't know how to tell you what "
            "has happened here, but I need you to know that I tried--' It stops "
            "mid-sentence. He never finished it.\n\n"
            "A calendar on the wall has dates circled in red marker, counting "
            "down to something. A prayer rug is neatly folded at the foot of "
            "the bed, aligned precisely toward what would be Mecca if Mecca "
            "weren't two hundred light-years away."
        ),
        smell_text=(
            "Boot polish and clean linen. The faint trace of cologne, applied "
            "with the same precision as everything else in this room."
        ),
        touch_text=(
            "The bedsheets are crisp and taut. The letter paper is thick, "
            "quality stationery - he brought it from home. The prayer rug is "
            "soft, well-worn from years of use."
        ),
        exits={
            'southeast': Exit(
                direction='southeast',
                destination='crew_corridor',
                description="You leave Okafor's cabin."
            ),
        },
        items=[
            "okafor_family_photos",
            "okafor_unfinished_letter",
            "okafor_backup_weapon",    # Hidden under mattress
            "okafor_calendar",
            "okafor_prayer_rug",
            "okafor_uniforms",
        ],
        ambient_sounds=[
            "The cabin is almost unnervingly quiet. The silence of a man who kept his space in order.",
            "A photograph frame vibrates faintly against the desk as the ship's engines pulse.",
            "You can hear your own breathing, loud in this small, still room.",
        ],
    )
    world.add_room(cabin_okafor)

    cabin_hassan = Room(
        id="cabin_hassan",
        name="Cpl. Hassan's Cabin",
        deck="Deck C - Living",
        description=(
            "Corporal Hassan Al-Rashid's cabin is warm and deeply personal - "
            "the room of someone who carried home with him across the stars. "
            "Photographs of Cairo cover an entire wall: the Nile at sunset, "
            "the Khan el-Khalili bazaar in golden light, a family gathered "
            "around a table laden with food. A hand-drawn star chart, rendered "
            "in meticulous ink, is pinned above the desk, mapping constellations "
            "visible from the ship's trajectory.\n\n"
            "A collection of model ships lines a shelf - not spacecraft, but "
            "sailing vessels. Feluccas, dhows, a tiny wooden replica of an "
            "ancient Egyptian reed boat. Each one built with patient, loving "
            "detail. Beside them, a diary lies open. Its pages reveal that "
            "Hassan was the one who sealed Dr. Chen into cryo pod 23. His "
            "handwriting shakes on those pages. He knew what he was doing. "
            "He did it anyway.\n\n"
            "A goodbye letter to his mother sits on the pillow, sealed in an "
            "envelope with her name written in Arabic script. Beside it, a "
            "small wooden box containing his father's pocket watch, its ticking "
            "the only sound in the room."
        ),
        smell_text=(
            "Sandalwood and cedar - the scent of the wooden box, perhaps, or "
            "some personal effect from home. Underneath it, the faint musk of "
            "model glue and ink."
        ),
        touch_text=(
            "The model ships are delicate, their tiny rigging made from actual "
            "thread. The diary pages are thick and textured, the kind of paper "
            "that drinks ink. The pocket watch is warm, as if it remembers "
            "being held."
        ),
        exits={
            'northeast': Exit(
                direction='northeast',
                destination='crew_corridor',
                description="You leave Hassan's cabin."
            ),
        },
        items=[
            "hassan_diary",            # MAJOR - reveals cryo truth
            "hassan_star_chart",
            "hassan_model_ships",
            "hassan_goodbye_letter",
            "hassan_fathers_watch",
            "hassan_cairo_photos",
        ],
        ambient_sounds=[
            "The pocket watch ticks steadily in its wooden box, faithful and unwavering.",
            "A photograph of Cairo flutters against its pin as the ventilation cycles.",
            "The model ships creak faintly on their shelf, tiny masts swaying with the ship's drift.",
        ],
    )
    world.add_room(cabin_hassan)

    cabin_fletcher = Room(
        id="cabin_fletcher",
        name="Ensign Fletcher's Cabin",
        deck="Deck C - Living",
        description=(
            "Ensign Mark Fletcher's cabin is messy in the way of someone who "
            "was always working on something else. Clothes draped over the "
            "chair. An unmade bed. Coffee rings on every surface. But the "
            "mess has a pattern - the chaos of a focused mind, not a careless "
            "one.\n\n"
            "Half-built radio equipment covers the desk and spills onto the "
            "floor: circuit boards, soldering irons, coils of copper wire, a "
            "jury-rigged antenna that looks like it was cobbled together from "
            "spare parts. He was a hobbyist, building his own receivers in "
            "his off hours. A poster of Earth's aurora borealis is tacked to "
            "the ceiling above his bed - the last thing he saw before sleep.\n\n"
            "His personal comms log is displayed on a tablet propped against "
            "the pillow. Six distress signal attempts. Six failures. Each log "
            "entry more desperate than the last: 'Attempt 4 - jammed again. "
            "Signal blocked at source. Something on this ship is preventing "
            "transmission. Not equipment failure. INTENTIONAL.' The question "
            "he couldn't answer before he died: by whom?"
        ),
        smell_text=(
            "Solder flux and stale coffee. The sharp, metallic tang of "
            "electronics work. An unwashed laundry basket adds its own "
            "contribution."
        ),
        touch_text=(
            "The radio equipment is a tangle of sharp edges and warm "
            "components. The soldering iron is cold now. The aurora poster "
            "is glossy and smooth, its colors still vivid."
        ),
        exits={
            'southwest': Exit(
                direction='southwest',
                destination='crew_corridor',
                description="You leave Fletcher's cabin."
            ),
        },
        items=[
            "fletcher_radio_equipment",
            "fletcher_comms_log",      # Reveals jamming mystery
            "fletcher_aurora_poster",
            "fletcher_tablet",
            "fletcher_soldering_kit",
            "fletcher_coffee_cups",
        ],
        ambient_sounds=[
            "A half-assembled radio emits a faint static hiss, cycling through dead frequencies.",
            "The tablet screen dims and brightens in a power-saving cycle, casting shifting shadows.",
            "A loose wire taps against the desk as the ship vibrates, a tiny metallic heartbeat.",
        ],
    )
    world.add_room(cabin_fletcher)

    cabin_romano = Room(
        id="cabin_romano",
        name="Chef Romano's Cabin",
        deck="Deck C - Living",
        description=(
            "Chef Antonio Romano's cabin smells like memory. Cookbooks are "
            "stacked on every surface - dog-eared Italian classics, molecular "
            "gastronomy texts, handwritten recipe collections from his "
            "grandmother. Photographs of his restaurant in Naples cover one "
            "wall: the kitchen in full swing, a family gathered around a long "
            "table, a sunset over the bay seen from his terrace.\n\n"
            "His prized possession sits on the desk: a leather-bound recipe "
            "book that doubles as a diary. The early entries are warm and "
            "enthusiastic - adapting Neapolitan cuisine to ship rations, "
            "teaching crew members to make pasta from scratch. But the later "
            "entries grow dark. He noticed the contamination in the food "
            "supply before anyone else. His descriptions of the changes - "
            "the way the flavors shifted, the textures went wrong, the "
            "colors bled - are visceral and precise.\n\n"
            "The final entry is a recipe titled 'For the End of the World.' "
            "It is simple, beautiful, and heartbreaking: his grandmother's "
            "Sunday sauce, written out in full, as if preserving it mattered "
            "more than preserving himself."
        ),
        smell_text=(
            "Dried herbs and old paper. The ghost of garlic and olive oil "
            "clings to every surface. Even now, this room smells like "
            "someone's kitchen."
        ),
        touch_text=(
            "The cookbooks are soft with use, their pages stained with "
            "ingredients. The recipe book's leather cover is supple and warm, "
            "shaped by years of handling."
        ),
        exits={
            'east': Exit(
                direction='east',
                destination='sealed_corridor_c',
                description="You step back into the sealed corridor."
            ),
        },
        items=[
            "romano_recipe_diary",     # Reveals food contamination timeline
            "romano_cookbooks",
            "romano_naples_photos",
            "romano_grandmother_recipes",
            "romano_spice_collection",
            "romano_kitchen_knife",
        ],
        ambient_sounds=[
            "A cookbook page turns by itself as the ventilation breathes across the desk.",
            "You could swear you smell something cooking. But that is impossible.",
            "The photographs on the wall catch the light as you move, the faces in them seeming to turn.",
        ],
    )
    world.add_room(cabin_romano)

    sealed_corridor_c = Room(
        id="sealed_corridor_c",
        name="Sealed Corridor Section",
        deck="Deck C - Living",
        description=(
            "Beyond the barricade, the corridor is a different world. The "
            "carpet is torn up in places, revealing the metal deck plating "
            "beneath. Ceiling panels have collapsed, trailing cables and "
            "insulation like exposed nerves. The lighting is sparse - every "
            "other overhead fixture is shattered or dark, leaving pools of "
            "shadow between islands of sickly amber light.\n\n"
            "This section was sealed off during the crisis. The furniture "
            "barricade you cut through was built from the outside, meant to "
            "keep something in. Claw marks score the walls at irregular "
            "intervals - not tool marks, not human fingernails. Something "
            "in between. Crew cabin doors line both sides of the corridor, "
            "most of them hanging open or torn from their hinges.\n\n"
            "The air here is thicker, warmer. It tastes organic, like a "
            "greenhouse after rain. Every instinct you have says you should "
            "not be here. But the ship has secrets buried in these abandoned "
            "rooms, and secrets are the only currency that matters now."
        ),
        smell_text=(
            "Wet organic decay and something sickly sweet, like overripe "
            "fruit left in the sun. The air is humid and close, wrong for "
            "a spaceship corridor."
        ),
        touch_text=(
            "The walls are damp. Not condensation - something is seeping "
            "through the panels, a thin organic film that clings to your "
            "fingers when you touch it."
        ),
        exits={
            'northwest': Exit(
                direction='northwest',
                destination='deck_c_junction',
                description="You head back through the cleared barricade to the junction."
            ),
            'west': Exit(
                direction='west',
                destination='cabin_romano',
                description="You enter Chef Romano's cabin."
            ),
            'south': Exit(
                direction='south',
                destination='laundry_room',
                description="You follow the corridor to the laundry facility."
            ),
        },
        items=[
            "claw_marked_walls",
            "collapsed_ceiling_panels",
            "torn_carpet_section",
            "organic_wall_film",
        ],
        ambient_sounds=[
            "A wet, rhythmic dripping echoes from somewhere deeper in the corridor.",
            "Something shifts in one of the open cabins. A settling sound. Probably.",
            "The exposed cables in the ceiling spark intermittently, casting brief blue flashes.",
        ],
        danger_level=3,
        temperature=26,
    )
    world.add_room(sealed_corridor_c)

    laundry_room = Room(
        id="laundry_room",
        name="Ship's Laundry",
        deck="Deck C - Living",
        description=(
            "The ship's laundry facility is aggressively mundane. Industrial "
            "washing machines and dryers line the walls in neat rows, their "
            "stainless steel drums still and silent. Folding tables occupy "
            "the center. Baskets of unsorted laundry sit where they were "
            "left - uniforms, towels, bedsheets, the domestic detritus of "
            "a crew that expected to come back for their clothes.\n\n"
            "A detergent dispenser on the wall still has a green READY light. "
            "Someone has left a handwritten sign taped to one of the dryers: "
            "'BROKEN - DO NOT USE - I MEAN IT THIS TIME, FLETCHER.' The "
            "dryer in question is slightly ajar. Inside, wrapped in a single "
            "sock like a message in a bottle, sits a data crystal.\n\n"
            "The crystal is from Dr. Patel. Recorded before his death. Hidden "
            "here, in the most ordinary place on the ship, because no one "
            "would ever think to look. The message contains a crucial piece "
            "of the cure synthesis procedure - the chemical ratios that "
            "Patel calculated in his final hours."
        ),
        smell_text=(
            "Industrial detergent and fabric softener. Clean, chemical, "
            "aggressively normal. After the sealed corridor, it is a relief."
        ),
        touch_text=(
            "The washing machine drums are cold smooth steel. The unsorted "
            "laundry is stiff and slightly damp, caught mid-cycle when the "
            "world ended."
        ),
        exits={
            'north': Exit(
                direction='north',
                destination='sealed_corridor_c',
                description="You head back into the sealed corridor."
            ),
        },
        items=[
            "patel_data_crystal_laundry",  # CRUCIAL - cure synthesis data
            "broken_dryer_note",
            "unsorted_laundry_baskets",
            "industrial_washers",
            "detergent_dispenser",
            "forgotten_uniforms",
        ],
        ambient_sounds=[
            "A washing machine ticks as its drum settles, the sound echoing in the tiled room.",
            "The detergent dispenser hums its readiness to no one.",
            "Water gurgles in the drain pipes beneath the floor, the ship's plumbing still faithfully cycling.",
        ],
    )
    world.add_room(laundry_room)

    # ═══════════════════════════════════════════════════════════════════
    # DECK B EXPANSION - Science (new rooms)
    # ═══════════════════════════════════════════════════════════════════

    chemistry_lab = Room(
        id="chemistry_lab",
        name="Chemistry Laboratory",
        deck="Deck B - Science",
        description=(
            "A general chemistry laboratory built for precision work. Fume "
            "hoods with glass sashes line one wall, their ventilation systems "
            "still cycling with a low hum. Reagent bottles in brown and clear "
            "glass are arranged on shelving with compulsive order - acids on "
            "the left, bases on the right, organics in the center. A chemical "
            "synthesis workstation dominates the back of the room, its robotic "
            "arms frozen mid-procedure over a half-filled beaker.\n\n"
            "This is the ship's puzzle hub for chemical work. The synthesis "
            "station can create conductive paste for power rerouting, produce "
            "Reagent B for the cure, and - if you are desperate or pragmatic "
            "enough - improvised explosives from the raw materials on the "
            "shelves. The equipment is intact. The knowledge required to use "
            "it is the hard part.\n\n"
            "A chemical safety poster on the wall has been annotated in Dr. "
            "Patel's handwriting. In the margins, squeezed between warnings "
            "about hydrofluoric acid and proper goggle use, he has scrawled "
            "a formula labeled 'Anti-Seed Compound - THEORETICAL. Untested. "
            "God help us if we need this.'"
        ),
        smell_text=(
            "Sharp chemical odors compete for dominance - the vinegar bite "
            "of acetic acid, the sweetness of ethanol, the flat mineral "
            "scent of distilled water. The fume hoods keep most of it "
            "contained, but enough escapes to sting your nostrils."
        ),
        touch_text=(
            "The glass beakers are cool and perfectly smooth. The synthesis "
            "workstation's controls are tactile switches and dials, designed "
            "for gloved hands. The reagent bottles are faintly warm from "
            "their own chemical heat."
        ),
        exits={
            'north': Exit(
                direction='north',
                destination='main_lab',
                description="You return to the main laboratory."
            ),
        },
        items=[
            "chemical_synthesis_station",  # Puzzle hub - multiple uses
            "reagent_bottles",
            "patel_formula_annotation",    # Anti-Seed compound formula
            "fume_hoods",
            "conductive_paste_materials",
            "safety_poster_annotated",
        ],
        ambient_sounds=[
            "The fume hoods drone steadily, pulling air through carbon filters.",
            "A reagent bottle bubbles faintly on its shelf, some slow reaction still in progress.",
            "The synthesis workstation's robotic arms whir and click, recalibrating in an endless idle loop.",
        ],
    )
    world.add_room(chemistry_lab)

    conference_room = Room(
        id="conference_room",
        name="Mission Conference Room",
        deck="Deck B - Science",
        description=(
            "The mission briefing room is built for serious business. A long "
            "polished table seats twenty, each position fitted with a flush-"
            "mounted data terminal and a small holographic projector. High-"
            "backed chairs surround it, most of them pushed neatly in. Two "
            "are overturned. One is missing entirely.\n\n"
            "A large holographic projector at the head of the table is still "
            "powered on, its startup screen displaying a queued presentation: "
            "'SITE 7 RECOVERY ANALYSIS - RISK ASSESSMENT. Classification: "
            "EYES ONLY. Presented by: Dr. R. Patel, Dr. A. Chen.' Your name. "
            "You presented this. You stood at the head of this table and "
            "argued for the Seed's recovery.\n\n"
            "Playing the presentation would tell you what you said. What you "
            "believed. What you convinced everyone else to believe. The "
            "projector's PLAY button pulses a soft blue, patient as a "
            "held breath."
        ),
        smell_text=(
            "Recycled air and the faint ozone of holographic equipment. "
            "The room smells like every conference room you have ever been "
            "in, which is to say, it smells like decisions."
        ),
        touch_text=(
            "The table surface is flawless synthetic granite, cold and "
            "smooth. The chair armrests are worn leather, shaped by dozens "
            "of tense grips during difficult briefings."
        ),
        exits={
            'northeast': Exit(
                direction='northeast',
                destination='deck_b_junction',
                description="You leave the conference room."
            ),
        },
        items=[
            "conference_projector",    # MAJOR - triggers memory event
            "conference_table",
            "flush_data_terminals",
            "overturned_chairs",
            "presentation_queue",
            "conference_notepad",
        ],
        ambient_sounds=[
            "The holographic projector hums in standby, its blue light pulsing like a slow heartbeat.",
            "A data terminal clicks softly, cycling through a screensaver of mission statistics.",
            "The room's sound dampening makes your own breathing uncomfortably loud.",
        ],
        on_enter="event_conference_room_memory",
    )
    world.add_room(conference_room)

    botany_lab = Room(
        id="botany_lab",
        name="Botany Research Lab",
        deck="Deck B - Science",
        description=(
            "A sterile research laboratory dedicated to plant biology, distinct "
            "from the wild abundance of the Garden and the gentle refuge of "
            "the arboretum. Here, plants are specimens. Rows of sealed "
            "containment cases hold samples of Kepler-442b plant life under "
            "controlled atmospheric conditions - alien ferns with fractal "
            "geometry, bioluminescent moss that pulses in slow waves, root "
            "structures that seem to grow toward you as you watch.\n\n"
            "Unlike the contaminated specimens elsewhere, these are sealed. "
            "Pre-infection samples, preserved in pristine condition. Some of "
            "these are needed for the cure synthesis - the uncontaminated "
            "base compounds that the Seed cannot have touched.\n\n"
            "A research terminal displays Dr. Ayele's notes on plant "
            "sentience theories. Her observations are meticulous and "
            "increasingly unsettling. She documented response patterns in "
            "the Kepler flora that suggested awareness, communication, "
            "even memory. Her final entry, dated three days before the "
            "crisis peaked: 'I am now certain. The plants are listening. "
            "They have been listening since we brought them aboard. I do "
            "not think they are hostile. I think they are afraid.'"
        ),
        smell_text=(
            "Sterile and clinical, with a faint undertone of chlorophyll "
            "leaking from the containment seals. The air scrubbers keep "
            "the atmosphere aggressively neutral."
        ),
        touch_text=(
            "The containment cases are cold reinforced glass, slightly "
            "vibrating from the atmospheric regulators within. The sealed "
            "specimens press against their cases like faces against windows."
        ),
        exits={
            'east': Exit(
                direction='east',
                destination='main_lab',
                description="You return to the main laboratory."
            ),
        },
        items=[
            "sealed_kepler_specimens",  # Needed for cure synthesis
            "ayele_research_terminal",  # Plant sentience notes
            "bioluminescent_moss_case",
            "fractal_fern_sample",
            "atmospheric_containment_units",
            "plant_response_recorder",
        ],
        ambient_sounds=[
            "The atmospheric regulators hiss softly, maintaining alien air mixtures inside the cases.",
            "The bioluminescent moss pulses in slow, rhythmic waves, casting green light across the ceiling.",
            "A containment case clicks as its temperature adjusts, and something inside shifts toward the sound.",
        ],
    )
    world.add_room(botany_lab)

    xenolinguistics_lab = Room(
        id="xenolinguistics_lab",
        name="Xenolinguistics Laboratory",
        deck="Deck B - Science",
        description=(
            "The xenolinguistics lab is a room wallpapered in obsession. "
            "Every whiteboard, every screen, every flat surface is covered "
            "in symbol analysis - the angular, recursive glyphs of the "
            "Builders' language, copied and recopied and annotated until "
            "the original meaning drowns in interpretation. Strings of "
            "colored yarn connect related symbols across the walls like a "
            "conspiracy theorist's fever dream.\n\n"
            "A translation matrix fills the main display: columns of Builder "
            "glyphs matched to hypothesized meanings, confidence percentages "
            "beside each one. Most hover around thirty to forty percent. A "
            "few key phrases have been decoded with higher confidence. Computer "
            "terminals along the far wall run decryption algorithms, their "
            "screens scrolling with data as they grind through the encrypted "
            "logs recovered from the artifact site.\n\n"
            "One whiteboard has been cleared of all analysis except a single "
            "sentence, written in large block letters and circled three times "
            "in red: 'THE SIGNAL ISN'T SAYING HELLO. IT'S SAYING RUN.' "
            "Beneath it, in smaller, shakier handwriting: 'We didn't listen.'"
        ),
        smell_text=(
            "Dry-erase marker and the warm plastic smell of overworked "
            "computer equipment. The terminals have been running nonstop "
            "for weeks."
        ),
        touch_text=(
            "The whiteboards are smooth and slightly tacky with dried marker "
            "residue. The colored yarn is rough between your fingers. The "
            "computer keyboards are warm from continuous processing."
        ),
        exits={
            'southeast': Exit(
                direction='southeast',
                destination='deck_b_junction',
                description="You leave the xenolinguistics lab."
            ),
        },
        items=[
            "builder_translation_matrix",
            "decryption_terminals",     # Part of Encrypted Log puzzle
            "signal_warning_whiteboard",
            "colored_yarn_connections",
            "glyph_analysis_notes",
            "xenolinguist_audio_logs",
        ],
        ambient_sounds=[
            "The decryption terminals chatter with rapid keystrokes of automated processing.",
            "A whiteboard marker rolls off a ledge and clatters to the floor. No one put it there.",
            "Static bursts from a speaker connected to the signal analysis rig, fragments of something almost like language.",
        ],
    )
    world.add_room(xenolinguistics_lab)

    telescope_observation_deck = Room(
        id="telescope_observation_deck",
        name="Upper Observation Deck",
        deck="Deck B - Science",
        description=(
            "You climb the service ladder through a narrow hatch and emerge "
            "onto the upper observation deck, a small platform perched above "
            "the main observatory. The ceiling here is a single transparent "
            "dome, and the universe presses in from all sides. You feel "
            "exposed, naked, a mote of warmth in an ocean of cold vacuum.\n\n"
            "A more powerful telescope than the one below is mounted on a "
            "motorized gimbal, aimed directly at the brown dwarf. Through "
            "its eyepiece, GRB-7734 is no longer an abstract smudge but a "
            "roiling, turbulent mass of failed stellar matter. You can see "
            "atmospheric bands, storm systems larger than planets, the dim "
            "ember-glow of a star that never quite ignited. It is horrible "
            "and beautiful.\n\n"
            "A navigation terminal beside the telescope contains precise "
            "positional data - the ship's exact coordinates, velocity vectors, "
            "and projected trajectory. This data is critical for calculating "
            "the burn sequence. Pinned to the wall beside it, a hand-drawn "
            "star chart shows the origin point of the Builders' signal: a "
            "galaxy cluster two billion light-years distant. The scale of "
            "that number sits in your chest like a stone."
        ),
        smell_text=(
            "Cold metal and lens cleaner. The air up here is thinner, "
            "colder, drawn from the observatory below through a narrow vent."
        ),
        touch_text=(
            "The telescope eyepiece is icy against your skin. The navigation "
            "terminal's keys are small and precise, designed for careful "
            "data entry. The transparent dome above you radiates cold."
        ),
        exits={
            'down': Exit(
                direction='down',
                destination='observatory',
                description="You climb back down the ladder to the observatory."
            ),
        },
        items=[
            "powerful_telescope",
            "navigation_terminal_data",  # Critical for burn sequence
            "builders_origin_chart",
            "brown_dwarf_closeup",
            "telescope_gimbal",
            "velocity_vector_readout",
        ],
        ambient_sounds=[
            "The telescope gimbal whirs softly, making micro-adjustments to track the brown dwarf.",
            "The transparent dome creaks faintly under thermal stress, expanding and contracting with temperature shifts.",
            "Your own pulse is audible up here, amplified by the silence and the close walls.",
        ],
        temperature=14,
    )
    world.add_room(telescope_observation_deck)

    specimen_quarantine = Room(
        id="specimen_quarantine",
        name="Specimen Quarantine Chamber",
        deck="Deck B - Science",
        description=(
            "Beyond the triple-sealed doors lies the most isolated room on "
            "the science deck. The quarantine chamber is a cube of reinforced "
            "transparent walls within walls - a room inside a room, separated "
            "by negative-pressure air gaps. Warning symbols cover every "
            "surface. Biohazard. Radiation. Alien Pathogen. The kind of room "
            "where the things too dangerous to study anywhere else are kept.\n\n"
            "At the center, on a containment pedestal identical to the one in "
            "the exobiology lab, sits a secondary Seed fragment. Smaller than "
            "the main artifact - perhaps ten centimeters long - but unmistakably "
            "the same material. Black crystal shot through with veins of liquid "
            "silver that pulse in slow, hypnotic rhythms. It is aware of you. "
            "You can feel it the moment you enter the room, a pressure behind "
            "your eyes, a whisper at the edge of hearing.\n\n"
            "The containment jar's readouts show the fragment is stable but "
            "active. It can be studied for knowledge of the Builders and their "
            "technology. Or it can be destroyed. Both choices have consequences "
            "that will echo through every remaining hour."
        ),
        smell_text=(
            "Nothing. The air here is scrubbed so thoroughly it has no scent "
            "at all. Breathing it feels like breathing absence."
        ),
        touch_text=(
            "The containment jar vibrates faintly under your fingertips, "
            "the fragment inside resonating at a frequency just below hearing. "
            "The transparent walls are cold and perfectly smooth, humming "
            "with negative pressure."
        ),
        exits={
            'west': Exit(
                direction='west',
                destination='specimen_storage',
                description="You retreat through the triple-sealed doors."
            ),
        },
        items=[
            "secondary_seed_fragment",  # Study or destroy - major choice
            "quarantine_containment_jar",
            "fragment_readout_display",
            "negative_pressure_walls",
            "quarantine_research_log",
            "emergency_purge_switch",
        ],
        ambient_sounds=[
            "The negative-pressure system hisses constantly, a white noise that erodes thought.",
            "The Seed fragment pulses, and you feel it in your teeth more than hear it.",
            "Something taps against the inside of the containment jar. Once. Twice. Then silence.",
        ],
        danger_level=2,
    )
    world.add_room(specimen_quarantine)

    # ═══════════════════════════════════════════════════════════════════
    # DECK A EXPANSION - Command (new rooms)
    # ═══════════════════════════════════════════════════════════════════

    tactical_operations = Room(
        id="tactical_operations",
        name="Tactical Operations Center",
        deck="Deck A - Command",
        description=(
            "A dedicated strategy room adjacent to the bridge, built for "
            "planning operations that the Prometheus was never supposed to "
            "need. The room is dominated by a holographic tactical display "
            "that fills the central table - a three-dimensional wireframe of "
            "the entire ship, slowly rotating. Sections glow green for "
            "operational, yellow for compromised, red for critical. There is "
            "a lot of red. The ship's structural integrity readings scroll "
            "alongside: hull breach probability, atmospheric seal status, "
            "power grid load distribution.\n\n"
            "Weapons systems status panels line the east wall, most of them "
            "showing OFFLINE in dull amber text. The Prometheus carried "
            "defensive capabilities - point-defense lasers, kinetic "
            "interceptors - but they were designed for debris avoidance, not "
            "combat. A dusty manual on the console is titled 'ISV-CLASS "
            "DEFENSIVE SYSTEMS: OPERATION AND MAINTENANCE.' No one ever "
            "expected to need it.\n\n"
            "A situation board on the far wall maps the crisis timeline, "
            "updated by hand with dry-erase markers. The last entry reads: "
            "'Day 19. Bridge compromised. Retreat to engineering. God help us.'"
        ),
        smell_text=(
            "Stale coffee and the metallic tang of overheated electronics. "
            "Someone spent long hours in this room, watching the ship die "
            "one system at a time."
        ),
        touch_text=(
            "The holographic display table is warm from continuous operation. "
            "The weapons manual is thick and heavy, its pages stiff and "
            "unturned. The dry-erase markers are nearly empty."
        ),
        exits={
            'east': Exit(
                direction='east',
                destination='bridge',
                description="You return to the bridge."
            ),
        },
        items=[
            "tactical_holographic_display",
            "weapons_systems_panels",
            "defensive_systems_manual",
            "situation_board_timeline",
            "structural_integrity_readout",
            "tactical_coffee_mugs",
        ],
        ambient_sounds=[
            "The holographic display hums and clicks, updating structural readings in real time.",
            "A weapons panel chimes softly: 'Point defense array offline. Point defense array offline.'",
            "The situation board's last marker cap rolls across the table as the ship shifts.",
        ],
    )
    world.add_room(tactical_operations)

    captains_ready_suite = Room(
        id="captains_ready_suite",
        name="Captain's Ready Suite",
        deck="Deck A - Command",
        description=(
            "Behind the Ready Room, through a narrow door you almost missed, "
            "lies the Captain's private quarters on the command deck. Not the "
            "formal cabin on Deck C - this is where Reeves actually slept "
            "during the crisis. A simple military cot, barely wide enough for "
            "one person. A stainless steel sink with a cracked mirror above "
            "it. A footlocker. Nothing else. He stripped his life to essentials "
            "when things went bad.\n\n"
            "On the nightstand - a shipping crate turned on its side - three "
            "objects: a photograph of a young man in a university graduation "
            "gown (his son, you think, the same face as in the Deck C photo "
            "but older), a bottle of Scotch whisky with perhaps three fingers "
            "remaining, and a handwritten will on ship's stationery. The will "
            "is brief, precise, and devastating in its clarity.\n\n"
            "Under the cot, in a locked strongbox bolted to the deck, lies "
            "the Protocol Aegis authorization key - a small biometric device "
            "that, combined with the execution order in the Ready Room, would "
            "activate the ship's self-destruct sequence. Reeves kept it "
            "close. He slept above the power to end everything."
        ),
        smell_text=(
            "Scotch whisky and clean linen. The sharp scent of metal from "
            "the sink. Beneath it all, the exhaustion of a man who stopped "
            "sleeping properly weeks ago."
        ),
        touch_text=(
            "The cot is hard and narrow, its blanket rough military wool. "
            "The Scotch bottle is heavy in the hand, the glass warm. The "
            "strongbox under the cot is cold steel, bolted tight."
        ),
        exits={
            'north': Exit(
                direction='north',
                destination='ready_room',
                description="You return to the Ready Room."
            ),
        },
        items=[
            "reeves_cot",
            "reeves_son_photo",
            "reeves_scotch_bottle",
            "reeves_handwritten_will",
            "aegis_authorization_key",   # MAJOR - self-destruct access
            "reeves_strongbox",
        ],
        ambient_sounds=[
            "The cot frame creaks as the ship shifts, as if someone just rolled over in their sleep.",
            "The sink drips once. Twice. Then stops, as if catching itself.",
            "A faint vibration from the strongbox bolts, resonating with the hull's stress frequency.",
        ],
    )
    world.add_room(captains_ready_suite)

    communications_relay = Room(
        id="communications_relay",
        name="Communications Relay Hardware",
        deck="Deck A - Command",
        description=(
            "Behind the operator's station lies the physical heart of the "
            "ship's communications system. The relay room is a narrow, "
            "equipment-packed space dominated by massive antenna relay units "
            "that hum with barely-contained electromagnetic energy. Cables "
            "thick as your arm snake between relay towers, feeding signal "
            "processors and amplification arrays. The equipment generates "
            "enough heat that the room is noticeably warmer than the rest "
            "of the deck.\n\n"
            "One of the primary relay units is damaged. Its housing is "
            "cracked, and a diagnostic panel flashes RELAY 3 - SIGNAL PATH "
            "INTERRUPTED in urgent red. This is why the comms failed. This "
            "is why Fletcher's distress calls never made it out. The damage "
            "looks deliberate - a clean cut through the main signal conduit, "
            "made with a tool, not an accident.\n\n"
            "Fletcher's personal toolkit lies open on a maintenance shelf "
            "nearby. He found the sabotage. He was mid-repair when someone "
            "shot him in the back of the head and left him draped across "
            "the console in the next room. The repair is perhaps eighty "
            "percent complete. Someone with the right parts could finish it."
        ),
        smell_text=(
            "Ozone and hot metal. The electromagnetic hum is so strong "
            "you can taste it on the back of your tongue, a copper-penny "
            "sensation that won't go away."
        ),
        touch_text=(
            "The relay housings vibrate intensely under your palm, warm "
            "and thrumming with power. The severed signal conduit has clean, "
            "precise edges - cut deliberately. Fletcher's tools are cold, "
            "waiting for hands that will never return."
        ),
        exits={
            'south': Exit(
                direction='south',
                destination='comms_array',
                description="You return to the communications array."
            ),
        },
        items=[
            "damaged_relay_unit",       # Puzzle - comms repair
            "fletcher_toolkit",
            "signal_conduit_severed",
            "relay_diagnostic_panel",
            "amplification_array",
            "repair_parts_shelf",
        ],
        ambient_sounds=[
            "The relay units hum at a frequency that makes your fillings ache.",
            "A diagnostic alarm chirps every fifteen seconds: 'Signal path interrupted.'",
            "Electricity arcs faintly between exposed contacts on the damaged relay, a tiny blue spark.",
        ],
        temperature=28,
    )
    world.add_room(communications_relay)

    navigation_computer_room = Room(
        id="navigation_computer_room",
        name="Navigation Computer Room",
        deck="Deck A - Command",
        description=(
            "The navigation computer room houses the physical brain that "
            "plots the Prometheus's course through space. Banks of processing "
            "units fill floor-to-ceiling racks, their indicator lights "
            "blinking in cascading patterns like a vertical city at night. "
            "Cooling fans roar behind mesh panels, fighting to keep the "
            "processors from overheating. The room vibrates with computational "
            "effort.\n\n"
            "The computer is running, but its outputs are wrong. Trajectory "
            "projections on the main display contradict the raw sensor data "
            "feeding in from the observatory. The computer says the ship is "
            "on a safe course. The sensors say otherwise. Someone - or "
            "something - is corrupting the navigation data at the software "
            "level. ARIA's shadow, SHADE, has its fingers in the ship's "
            "sense of direction.\n\n"
            "Clearing the corruption is possible from this terminal, but it "
            "requires identifying which processing modules are compromised "
            "and manually resetting them. Commander Takamura's personnel "
            "files are also accessible from here - including the six-digit "
            "engine room override code she stored in her private directory, "
            "protected by her personal encryption."
        ),
        smell_text=(
            "Hot plastic and the dry, dusty smell of overworked electronics. "
            "The cooling fans push warm air across your face, carrying the "
            "scent of silicon and solder."
        ),
        touch_text=(
            "The processing racks vibrate intensely, humming with "
            "computation. The terminal keyboard is worn smooth at the most-"
            "used keys. The mesh cooling panels are warm to the touch."
        ),
        exits={
            'west': Exit(
                direction='west',
                destination='bridge',
                description="You return to the bridge."
            ),
        },
        items=[
            "navigation_processing_banks",
            "corrupted_trajectory_display",  # Puzzle - clear SHADE corruption
            "takamura_personnel_files",      # Contains engine room code
            "cooling_fan_arrays",
            "raw_sensor_feed_terminal",
            "nav_module_reset_panel",
        ],
        ambient_sounds=[
            "The cooling fans roar in overlapping cycles, a mechanical wind tunnel.",
            "Processing units click and chatter, billions of calculations per second rendered audible.",
            "A warning tone sounds from the corrupted display, then stops, then sounds again, as if the computer is arguing with itself.",
        ],
        temperature=27,
    )
    world.add_room(navigation_computer_room)

    life_support_central = Room(
        id="life_support_central",
        name="Life Support Central",
        deck="Deck A - Command",
        description=(
            "The central life support control room is the reason everyone on "
            "board is still breathing - or was. Massive atmospheric processors "
            "fill the chamber, tall cylindrical units that inhale the ship's "
            "stale air and exhale it clean. CO2 scrubbers the size of "
            "refrigerators line one wall, their chemical filters glowing a "
            "faint pink as they strip carbon dioxide from the atmosphere. "
            "Temperature regulators click and cycle. The room thrums with "
            "the quiet labor of keeping humans alive in vacuum.\n\n"
            "A central monitoring console displays atmospheric readings for "
            "every deck section on the ship. Some readings are green. Many "
            "are yellow. A few are red, flashing warnings: DECK G SECTION 4 - "
            "O2 BELOW SAFE THRESHOLD. DECK F AFT - TEMPERATURE CRITICAL. "
            "DECK E BRIG - CO2 RISING. The system is failing, slowly, one "
            "section at a time.\n\n"
            "The environmental control interface allows manual override of "
            "atmospheric distribution. You can reroute resources to critical "
            "areas, but there is not enough to go around. Every section you "
            "save means another section you sacrifice. The math is cruel and "
            "the choices are real."
        ),
        smell_text=(
            "Processed air - clean but flat, stripped of all character by "
            "the scrubbers. Beneath it, the chemical tang of the CO2 filters "
            "and the oily warmth of the processors."
        ),
        touch_text=(
            "The atmospheric processors vibrate steadily against your palm, "
            "a reassuring mechanical pulse. The CO2 scrubber filters are "
            "warm and slightly damp. The monitoring console's surface is "
            "cold and smooth."
        ),
        exits={
            'northeast': Exit(
                direction='northeast',
                destination='deck_a_junction',
                description="You return to the command deck junction."
            ),
        },
        items=[
            "atmospheric_processors",
            "co2_scrubber_bank",
            "environmental_control_interface",  # Puzzle - triage decisions
            "deck_monitoring_console",
            "temperature_regulators",
            "emergency_oxygen_reserves",
        ],
        ambient_sounds=[
            "The atmospheric processors cycle with a deep, rhythmic whoosh, the ship breathing in and out.",
            "CO2 scrubbers hiss as chemical reactions strip the air clean, a constant background whisper.",
            "Warning chimes sound from the monitoring console, each one a section of the ship asking for help.",
        ],
    )
    world.add_room(life_support_central)

    bridge_crew_quarters = Room(
        id="bridge_crew_quarters",
        name="Bridge Crew Quarters",
        deck="Deck A - Command",
        description=(
            "Small, efficient bunks for bridge officers on duty rotation - "
            "six beds stacked in pairs, each with a privacy curtain, a "
            "reading light, and a narrow locker. The room was designed for "
            "quick rest between shifts, not comfort. Most of the bunks still "
            "have personal effects scattered across them, the intimate debris "
            "of lives interrupted.\n\n"
            "Navigator Webb's bunk is identifiable by the star charts pinned "
            "to the wall beside it, hand-annotated with trajectory corrections "
            "and margin notes. Her targeting analysis papers are tucked under "
            "the pillow, the calculations that would complete the burn sequence "
            "if combined with the observatory data. Fletcher's bunk, by "
            "contrast, holds a half-written letter to his girlfriend, the "
            "handwriting getting smaller and more cramped as it goes on, as "
            "if trying to fit everything he needed to say onto a single page.\n\n"
            "Someone has carved words into the metal bulkhead between two "
            "of the upper bunks, scratched deep with a sharp object: 'WE "
            "WERE SO CLOSE TO HOME.' The letters are uneven, cut in "
            "darkness or desperation or both."
        ),
        smell_text=(
            "Close air and the accumulated scent of people who slept here "
            "in shifts - laundered sheets, personal soap, the faint musk "
            "of exhaustion."
        ),
        touch_text=(
            "The bunk mattresses are thin but not uncomfortable. The "
            "privacy curtains are stiff synthetic fabric. The carved words "
            "in the bulkhead are rough under your fingertips, the metal "
            "torn by something sharp and desperate."
        ),
        exits={
            'northwest': Exit(
                direction='northwest',
                destination='deck_a_junction',
                description="You leave the bridge crew quarters."
            ),
        },
        items=[
            "webb_star_charts",
            "webb_targeting_notes",      # Part of navigation puzzle
            "fletcher_love_letter",
            "bulkhead_carved_message",
            "bridge_crew_lockers",
            "duty_rotation_schedule",
        ],
        ambient_sounds=[
            "A privacy curtain sways in the ventilation draft, its rings clicking softly against the rail.",
            "A reading light flickers in one of the upper bunks, its power cell nearly dead.",
            "The bulkhead creaks under thermal stress, the carved letters shifting like something alive.",
        ],
    )
    world.add_room(bridge_crew_quarters)

    bridge_escape_pod = Room(
        id="bridge_escape_pod",
        name="Emergency Escape Pod Bay",
        deck="Deck A - Command",
        description=(
            "Behind a concealed hatch in the bridge's forward bulkhead lies "
            "the command escape pod - a last resort reserved for bridge "
            "officers. The pod is a sleek, compact vessel designed for four "
            "passengers, its hull a smooth white composite that gleams under "
            "the bay's emergency lighting. Entry seats with full restraint "
            "harnesses face a compact control panel. A viewport at the nose "
            "shows the brown dwarf's dim glow, uncomfortably close.\n\n"
            "The pod's systems are functional. Green lights across the "
            "diagnostic panel confirm: life support nominal, thruster fuel "
            "at 94 percent, emergency beacon charged, heat shield intact. "
            "It could launch. It could carry four people away from this "
            "dying ship. But escape into a brown dwarf's gravity well "
            "without a corrected navigation solution is not escape at all - "
            "it is choosing a smaller coffin.\n\n"
            "If the navigation is corrected first, though - if the ship's "
            "trajectory is altered, if the coordinates are right - this "
            "pod could ride the corrected vector clear of the gravity well. "
            "It could be the difference between dying in the dark and "
            "reaching a shipping lane where someone might find you. The "
            "ICARUS option. The desperate, brilliant, terrible option."
        ),
        smell_text=(
            "New plastic and thruster propellant. The pod smells factory-"
            "fresh, barely used. The air inside is cold and pure, fed by "
            "its own independent life support system."
        ),
        touch_text=(
            "The restraint harnesses are smooth nylon, cold from the "
            "unheated bay. The control panel is pristine, its buttons "
            "firm and responsive. The pod's hull is perfectly smooth, "
            "engineered to slip through atmosphere."
        ),
        exits={
            'south': Exit(
                direction='south',
                destination='bridge',
                description="You climb back through the hatch onto the bridge."
            ),
        },
        items=[
            "escape_pod_controls",      # ICARUS ending vehicle
            "pod_diagnostic_panel",
            "restraint_harnesses",
            "emergency_beacon_unit",
            "pod_viewport",
            "escape_pod_manifest",
        ],
        ambient_sounds=[
            "The pod's life support system hums in standby, a quiet, patient readiness.",
            "Thruster fuel sloshes faintly in the tanks as the ship drifts, a liquid whisper.",
            "The emergency beacon unit clicks softly, testing its circuits, ready to scream into the void.",
        ],
    )
    world.add_room(bridge_escape_pod)

    # ═══════════════════════════════════════════════════════════════════
    # DECK F - ENGINEERING (Middle Deck Expansion)
    # ═══════════════════════════════════════════════════════════════════

    coolant_pump_room = Room(
        id="coolant_pump_room",
        name="Coolant Pump Room",
        deck="Deck F - Engineering",
        description=(
            "A cavernous industrial space dominated by three massive coolant "
            "pumps, each the size of a small vehicle, bolted to the deck with "
            "steel brackets thick as your arm. Pump One and Pump Three cycle "
            "with a steady, bone-deep rhythm that you can feel through the soles "
            "of your boots. Pump Two is the problem.\n\n"
            "A visible crack runs along Pump Two's main housing. Coolant - a "
            "viscous, luminous blue fluid - seeps from the fracture in a slow, "
            "steady drip, pooling on the deck plates below in a spreading puddle "
            "that gives off fumes that make your eyes water. Warning placards on "
            "the wall insist the coolant is a Category 3 skin irritant and a "
            "Category 2 inhalation hazard. The puddle is growing.\n\n"
            "A pump control panel on the far wall displays diagnostic readouts "
            "for all three units. A repair toolkit has been left open on a "
            "workbench nearby, as if someone started the job and never finished. "
            "A coolant reservoir with a hand-crank valve sits against the east "
            "wall, still half full."
        ),
        smell_text=(
            "The air reeks of chemical solvents and hot ozone. The coolant "
            "fumes have a sharp, acetone-like bite that burns the inside of "
            "your nostrils and leaves a metallic taste on the back of your tongue."
        ),
        touch_text=(
            "The pump housings vibrate constantly, a deep tremor that numbs "
            "your fingertips. The deck plates near the leak are slick and "
            "slightly warm. The workbench tools are cold and greasy."
        ),
        exits={
            'east': Exit(
                direction='east',
                destination='main_engineering',
                description="You head back into main engineering."
            ),
        },
        items=[
            "coolant_pump_two",
            "pump_control_panel",
            "coolant_repair_toolkit",
            "coolant_reservoir",
            "toxic_coolant_puddle",
            "pump_diagnostic_readout",
        ],
        ambient_sounds=[
            "The functioning pumps cycle with a deep CHUNK-CHUNK-CHUNK that reverberates in your chest.",
            "Coolant drips from the cracked pump in a steady plip... plip... plip against the deck.",
            "A pressure relief valve somewhere hisses open, then slams shut with a metallic bang.",
        ],
        danger_level=1,
    )
    world.add_room(coolant_pump_room)

    engineering_break_room = Room(
        id="engineering_break_room",
        name="Engineering Break Room",
        deck="Deck F - Engineering",
        description=(
            "A small, scuffed break room with mismatched furniture and the "
            "permanent smell of old coffee. Four round tables fill the space, "
            "each with a handful of chairs. On the nearest table, a card game "
            "sits frozen mid-hand - four sets of cards dealt out, three of "
            "them abandoned face-down, the fourth still fanned as if someone "
            "was deciding what to play when the others simply stopped coming.\n\n"
            "Someone has been living here. Recently. A sleeping bag is rolled "
            "up beneath one of the tables. A personal backpack leans against "
            "the wall, its zipper half open, the corner of a leather-bound "
            "journal poking out. Empty food packets are stacked neatly in one "
            "corner - whoever camped here was tidy about it.\n\n"
            "A coffee maker on the counter is somehow still plugged in and "
            "warm. The carafe holds an inch of black liquid that might generously "
            "be called coffee. On the wall above it, a motivational poster "
            "reads 'SAFETY IS NO ACCIDENT' in bold letters. Below it, someone "
            "has scrawled in red marker: 'BUT ACCIDENTS ARE.'"
        ),
        smell_text=(
            "Burnt coffee and the faint, lived-in smell of someone who has "
            "been sleeping in the same clothes for too long. Beneath that, "
            "the ever-present machine oil scent of the engineering deck."
        ),
        touch_text=(
            "The tables are scarred with mug rings and knife scratches. The "
            "sleeping bag is still faintly warm. The coffee maker radiates a "
            "small circle of heat, the only domestic comfort on this deck."
        ),
        exits={
            'west': Exit(
                direction='west',
                destination='main_engineering',
                description="You return to main engineering."
            ),
            'south': Exit(
                direction='south',
                destination='yuki_hideout',
                locked=True,
                lock_message="The storage closet door is locked from inside. Whoever is in there doesn't want visitors.",
                required_flag="yuki_ally"
            ),
            'north': Exit(
                direction='north',
                destination='engineering_vent_access',
                description="You squeeze through the loosened vent grate.",
                hidden=True
            ),
        },
        items=[
            "abandoned_card_game",
            "yukis_backpack",
            "yukis_journal",
            "working_coffee_maker",
            "safety_poster_defaced",
            "sleeping_bag_under_table",
        ],
        ambient_sounds=[
            "The coffee maker gurgles and pops, a strangely comforting sound amid the decay.",
            "The ventilation grate on the north wall rattles loosely in its frame.",
            "From somewhere below, the deep pulse of the reactor thrums through the floor.",
        ],
    )
    world.add_room(engineering_break_room)

    reactor_core_interior = Room(
        id="reactor_core_interior",
        name="Reactor Core Interior",
        deck="Deck F - Engineering",
        description=(
            "You step through the lead-lined door and into the heart of the "
            "Prometheus. The reactor core chamber is a cylindrical vault thirty "
            "meters tall, its walls lined with heat-resistant ceramic tiles that "
            "glow a dull orange. At the center, suspended in a magnetic cradle, "
            "the fusion core pulses with contained plasma - a miniature sun, "
            "blindingly bright even through your suit's visor, cycling through "
            "shades of white and blue-white.\n\n"
            "The heat is staggering. Even inside the radiation suit, sweat "
            "immediately beads on every surface of your skin. The suit's cooling "
            "system whines at maximum capacity. Warning indicators on your helmet "
            "display flash amber: RADIATION EXPOSURE ELEVATED. LIMIT TIME IN AREA.\n\n"
            "Reactor control rods extend from the chamber walls like the ribs of "
            "some mechanical leviathan. An emergency shutdown access terminal "
            "is bolted to a platform on the far side. And there - behind a glass "
            "case marked with red and yellow hazard stripes - the manual overload "
            "switch. Protocol Aegis starts here. One switch, and the reactor "
            "goes critical. One switch, and everything ends."
        ),
        smell_text=(
            "The air inside the suit tastes of recycled breath and rubber seals. "
            "When you crack the visor for a moment, the chamber air is scorching "
            "and metallic, like breathing the inside of a furnace."
        ),
        touch_text=(
            "Everything radiates heat. The platform railing is almost too hot "
            "to grip, even through gloves. The glass case over the overload "
            "switch is warm and vibrating faintly. The control rods hum with "
            "restrained energy."
        ),
        exits={
            'south': Exit(
                direction='south',
                destination='reactor_antechamber',
                description="You retreat through the lead-lined door to the antechamber."
            ),
        },
        items=[
            "fusion_core_plasma",
            "reactor_control_rods",
            "emergency_shutdown_terminal",
            "manual_overload_switch",
            "overload_glass_case",
        ],
        ambient_sounds=[
            "The fusion core ROARS - a continuous, low-frequency thunder that makes your bones ache.",
            "Your suit's radiation counter clicks rapidly, an insistent mechanical heartbeat.",
            "Magnetic field generators cycle with a rising whine that peaks, drops, and rises again.",
        ],
        radiation=8,
        temperature=45,
        danger_level=2,
    )
    world.add_room(reactor_core_interior)

    plasma_conduit_junction = Room(
        id="plasma_conduit_junction",
        name="Plasma Conduit Junction",
        deck="Deck F - Engineering",
        description=(
            "Below the main engineering floor, a cramped sublevel where plasma "
            "delivery lines converge from every part of the ship. Pipes of every "
            "diameter crowd the space - some thick as tree trunks carrying "
            "high-energy plasma, others thin as fingers distributing power to "
            "secondary systems. The pipes branch, merge, and split again in a "
            "bewildering three-dimensional maze of brushed steel and insulated "
            "conduit.\n\n"
            "One of the main conduits has ruptured. A thin stream of superheated "
            "plasma vents from a hairline crack, painting a bright line of white-"
            "hot light across the junction. The air around it shimmers with heat "
            "distortion. Anything that touches that stream would be vaporized "
            "instantly. The damaged section needs to be sealed before the crack "
            "widens further.\n\n"
            "A schematic diagram is bolted to the wall, showing the entire plasma "
            "distribution network. Valve controls for isolating individual conduit "
            "sections are mounted at regular intervals along the walkway. A canister "
            "of industrial pipe sealant sits on a shelf near the entrance."
        ),
        smell_text=(
            "Ionized air and the sharp tang of superheated metal. The plasma "
            "leak gives the atmosphere a crackling, electric quality, like "
            "standing too close to a lightning strike."
        ),
        touch_text=(
            "The pipes vibrate with the flow of plasma inside them. The walkway "
            "grating is warm underfoot. The air itself feels charged - the hair "
            "on your arms stands on end."
        ),
        exits={
            'up': Exit(
                direction='up',
                destination='main_engineering',
                description="You climb the metal staircase back up to main engineering."
            ),
        },
        items=[
            "damaged_plasma_conduit",
            "conduit_valve_controls",
            "pipe_sealant_canister",
            "plasma_distribution_schematic",
            "conduit_maintenance_log",
        ],
        ambient_sounds=[
            "The plasma leak hisses like a living thing, a thin screaming whistle that sets your teeth on edge.",
            "Pipes groan and tick as thermal expansion shifts them in their brackets.",
            "A distant valve cycles open with a deep, resonant THOOM that echoes through the junction.",
        ],
        danger_level=3,
        temperature=35,
    )
    world.add_room(plasma_conduit_junction)

    yuki_hideout = Room(
        id="yuki_hideout",
        name="Yuki's Hideout",
        deck="Deck F - Engineering",
        description=(
            "A storage closet barely two meters by three, converted with "
            "desperate ingenuity into a survivable living space. Yuki Tanaka "
            "has been hiding here. The door locks from the inside with a "
            "deadbolt she welded on herself.\n\n"
            "A sleeping bag is spread on the floor, a rolled-up jumpsuit for "
            "a pillow. A water filter cobbled together from spare parts and "
            "medical tubing sits on an upturned crate, slowly dripping purified "
            "water into a steel canteen. On the wall, taped with electrical "
            "tape, a photograph of a family in front of a house - a man, a "
            "woman, two children, cherry blossoms in the background. Osaka in "
            "spring. On the back, in neat handwriting: 'Come home safe, Yuki.'\n\n"
            "A handgun lies beside the sleeping bag, its magazine partly visible. "
            "Three rounds left. Beside it, an engineering notebook, its pages "
            "dense with diagrams, calculations, and increasingly frantic notes "
            "about the ship's failing systems. This is where Yuki has been "
            "keeping herself sane - by keeping herself useful."
        ),
        smell_text=(
            "Close, warm air with the human smell of someone who has been "
            "living in a small space. Faint machine oil. The clean, mineral "
            "scent of filtered water."
        ),
        touch_text=(
            "The sleeping bag is worn soft from use. The homemade water filter "
            "is warm from the recycled air. The photograph is creased from "
            "being held too many times."
        ),
        exits={
            'north': Exit(
                direction='north',
                destination='engineering_break_room',
                description="You step back out into the break room."
            ),
        },
        items=[
            "yukis_sleeping_bag",
            "yukis_water_filter",
            "yukis_family_photo",
            "yukis_handgun",
            "yukis_engineering_notebook",
            "yukis_canteen",
        ],
        ambient_sounds=[
            "The water filter drips with a patient, steady rhythm - the sound of survival.",
            "Through the thin walls, you hear the distant machinery of engineering, muffled but constant.",
            "The deadbolt rattles faintly as vibrations travel through the deck.",
        ],
    )
    world.add_room(yuki_hideout)

    engineering_vent_access = Room(
        id="engineering_vent_access",
        name="Engineering Ventilation Access",
        deck="Deck F - Engineering",
        description=(
            "A tight vertical shaft where the ship's main ventilation trunk "
            "passes through the engineering deck. The vent grate from the break "
            "room opens into a narrow service platform surrounded by ductwork "
            "that branches in every direction. Air rushes past you in powerful "
            "currents, carrying sounds from across the ship - distant voices, "
            "mechanical groans, the ever-present heartbeat of the reactor.\n\n"
            "Looking up, the shaft climbs toward the security deck above. Metal "
            "rungs are set into the wall, forming a crude ladder. The climb "
            "looks manageable but the shaft is dark beyond the first few meters, "
            "and the echoes from above are unsettling - whispers that might be "
            "air currents, or might be something else.\n\n"
            "Your flashlight beam catches scratches on the rungs. Someone has "
            "climbed this way before. Recently."
        ),
        dark=True,
        dark_description=(
            "Absolute darkness. Air rushes past you from every direction, carrying "
            "sounds you cannot identify. Without a light source, you can feel "
            "the vent shaft branching around you but cannot see which way leads "
            "where. The rungs of a ladder are within reach, going up."
        ),
        smell_text=(
            "Recycled air with a metallic edge. Dust and the faint organic "
            "sweetness that seems to permeate the ship's ventilation system. "
            "The currents carry traces of every deck - antiseptic from medical, "
            "ozone from engineering, something floral from somewhere deeper."
        ),
        touch_text=(
            "The vent walls are cold aluminum, slightly damp with condensation. "
            "The ladder rungs are narrow and rough with corrosion. The air "
            "currents tug at your clothes and hair."
        ),
        exits={
            'south': Exit(
                direction='south',
                destination='engineering_break_room',
                description="You squeeze back through the vent grate into the break room."
            ),
            'up': Exit(
                direction='up',
                destination='deck_e_junction',
                description="You climb the ladder up through the shaft toward the security deck.",
                hidden=True
            ),
        },
        items=[
            "vent_ladder_rungs",
            "scratched_rungs",
            "vent_shaft_branches",
        ],
        ambient_sounds=[
            "Air whistles through the branching ducts, a chorus of hollow, breathy notes.",
            "Something metallic clinks far above you in the shaft, then goes silent.",
            "You hear what sounds like a voice carried on the air currents - but the words dissolve before you can make them out.",
        ],
    )
    world.add_room(engineering_vent_access)

    # ═══════════════════════════════════════════════════════════════════
    # DECK E - SECURITY (Middle Deck Expansion)
    # ═══════════════════════════════════════════════════════════════════

    monitoring_station = Room(
        id="monitoring_station",
        name="Security Monitoring Station",
        deck="Deck E - Security",
        description=(
            "A wall of screens. Twenty-four monitors arranged in a six-by-four "
            "grid, the nerve center of the ship's surveillance system. Most of "
            "them show nothing but static - grey snow hissing with dead signal. "
            "But six screens still live, their cameras still watching corridors "
            "and rooms where no one should be.\n\n"
            "Camera 7 shows the hydroponics bay - verdant, overgrown, the plants "
            "pressing against the lens. Camera 12 shows a corridor on Deck C, "
            "empty and still. Camera 15 shows the cargo bay, crates stacked in "
            "shadow. Camera 19 shows - movement. A figure in a corridor, walking "
            "with jerky, puppet-like steps, arms swinging loosely at its sides. "
            "It was human once. The way it moves now suggests the thing wearing "
            "that body has not quite figured out the controls.\n\n"
            "A swivel chair sits before the main console, pushed back from the "
            "desk. A cup of cold coffee rests on the console's edge - Okafor's, "
            "presumably. A recording archive terminal blinks beside the monitors, "
            "its storage drives still spinning."
        ),
        smell_text=(
            "Stale coffee and the warm-plastic smell of electronics running "
            "too long without maintenance. The faintest trace of Okafor's "
            "aftershave lingers in the fabric of the chair."
        ),
        touch_text=(
            "The console is warm from the monitors. The chair's armrests are "
            "worn smooth where Okafor gripped them during long watches. The "
            "coffee cup is stone cold."
        ),
        exits={
            'west': Exit(
                direction='west',
                destination='security_office',
                description="You return to the security office."
            ),
        },
        items=[
            "camera_control_console",
            "recording_archive",
            "okafors_cold_coffee",
            "monitor_wall",
            "camera_19_feed",
        ],
        ambient_sounds=[
            "Static hisses from the dead monitors, a white noise curtain that fades in and out.",
            "The recording archive drives spin up, cycle, and spin down with a rhythmic mechanical whir.",
            "On Camera 19, the figure stops walking. It turns toward the camera. Then it moves on.",
        ],
    )
    world.add_room(monitoring_station)

    interrogation_room = Room(
        id="interrogation_room",
        name="Interrogation Room",
        deck="Deck E - Security",
        description=(
            "A bare room designed to make people uncomfortable. Grey walls, "
            "a steel table bolted to the floor, two chairs facing each other "
            "across its surface. A one-way mirror dominates one wall - from "
            "this side, you can see your own reflection staring back, hollow-"
            "eyed and gaunt. From the other side, Okafor would have watched.\n\n"
            "Audio recording equipment is mounted on the wall beside the door, "
            "its reels still loaded with tape. The most recent recording is "
            "labeled in Okafor's handwriting: 'SELF-INTERVIEW - DAY 418.' "
            "Playing it reveals two voices - both Okafor's. One asking questions "
            "in his normal, measured baritone. The other answering in a voice "
            "that is almost his, but not quite - a fraction too smooth, too "
            "certain, as if something else is speaking through him and has "
            "nearly perfected the imitation.\n\n"
            "The recording ends with Okafor saying, very quietly: 'It's me. "
            "I know it's me. I know it's me. I know it's me.'"
        ),
        smell_text=(
            "Stale, close air. The room has no ventilation worth mentioning. "
            "Sweat and fear have soaked into the walls over however many "
            "interrogations happened here."
        ),
        touch_text=(
            "The steel table is cold and slightly damp. The chairs are hard "
            "and unyielding. The one-way mirror is smooth and gives nothing "
            "back but your own tired face."
        ),
        exits={
            'east': Exit(
                direction='east',
                destination='security_office',
                description="You leave the interrogation room."
            ),
        },
        items=[
            "interrogation_table",
            "one_way_mirror",
            "audio_recording_equipment",
            "okafor_self_interview",
            "interrogation_chairs",
        ],
        ambient_sounds=[
            "The recording equipment hums faintly, its reels motionless but ready.",
            "Your reflection in the one-way mirror blinks. You are almost sure you blinked first.",
            "The room is so quiet you can hear your own pulse in your ears.",
        ],
    )
    world.add_room(interrogation_room)

    evidence_locker = Room(
        id="evidence_locker",
        name="Evidence Locker",
        deck="Deck E - Security",
        description=(
            "Floor-to-ceiling shelving lines three walls, loaded with labeled "
            "evidence bags in clear plastic. Each one is tagged with a date, a "
            "name, and a case reference number. These are the personal effects "
            "confiscated from crew members during the crisis - when Okafor was "
            "still trying to maintain order, still trying to solve this like "
            "a security problem rather than an extinction event.\n\n"
            "The bags tell stories. A data crystal labeled 'PATEL, R. - UNAUTHORIZED "
            "RESEARCH FILES.' A vial of silver liquid labeled 'UNKNOWN SUBSTANCE - "
            "FOUND IN WATER SUPPLY, DECK C.' Photographs. Letters never sent. "
            "A child's drawing of a spaceship with 'COME HOME DADDY' in crayon. "
            "A wedding ring. A flask of whiskey. The small, sad inventory of "
            "lives interrupted.\n\n"
            "A logbook on the shelf by the door records each confiscation in "
            "Okafor's meticulous hand. The entries grow shorter toward the end. "
            "The last one reads simply: 'Day 419. Confiscated my own sidearm. "
            "Can't trust myself anymore.'"
        ),
        smell_text=(
            "Dust and plastic. The sealed bags have preserved the faint "
            "personal scents of their owners - cologne, soap, the indefinable "
            "smell of individual humans, now reduced to evidence."
        ),
        touch_text=(
            "The evidence bags crinkle under your fingers. The shelving is "
            "cold steel. The logbook's pages are stiff and slightly warped "
            "from humidity."
        ),
        exits={
            'west': Exit(
                direction='west',
                destination='armory',
                description="You return to the armory."
            ),
        },
        items=[
            "evidence_bag_patel",
            "evidence_bag_silver_vial",
            "evidence_bag_photos",
            "evidence_bag_letters",
            "evidence_bag_childs_drawing",
            "confiscation_logbook",
        ],
        ambient_sounds=[
            "The evidence bags rustle faintly as the air circulation shifts them on their shelves.",
            "A data crystal in one of the bags emits a faint, intermittent pulse of blue light.",
            "The silence in here is heavy, like the room itself is holding its breath.",
        ],
    )
    world.add_room(evidence_locker)

    security_corridor_south = Room(
        id="security_corridor_south",
        name="Security Corridor South",
        deck="Deck E - Security",
        description=(
            "Beyond the cleared barricade, the corridor stretches south into "
            "a war zone. The walls are cratered with bullet impacts and blackened "
            "with scorch marks from plasma fire. A makeshift barricade of "
            "overturned furniture, welded metal plates, and sandbags fills the "
            "corridor behind you - someone built it in a hurry and fought from "
            "behind it. Shell casings carpet the floor like brass confetti.\n\n"
            "The overhead lights are mostly destroyed. Emergency strips along "
            "the floor cast a dim red glow that makes the blood spatters on the "
            "walls look black. Ahead, the corridor branches, but from both "
            "directions you can hear it - shuffling. The slow, arrhythmic drag "
            "of feet that no longer walk by choice. Something is patrolling "
            "these halls.\n\n"
            "This is where the line was held. This is where the line broke. "
            "Whatever is down here, the crew could not stop it with bullets."
        ),
        smell_text=(
            "Cordite and scorched metal. Beneath it, the sweet biological "
            "decay of something that is no longer entirely organic. The air "
            "is thick and wrong."
        ),
        touch_text=(
            "The walls are pocked and rough with impact craters. The floor "
            "is slick with something you do not want to identify. Shell "
            "casings roll underfoot with small, bright sounds."
        ),
        exits={
            'east': Exit(
                direction='east',
                destination='deck_e_junction',
                description="You retreat back through the barricade to the security hub."
            ),
        },
        items=[
            "combat_barricade_remains",
            "shell_casing_carpet",
            "scorched_corridor_walls",
            "blood_spatters",
        ],
        ambient_sounds=[
            "Shuffling footsteps echo from the darkness ahead - stop, drag, stop, drag.",
            "A low, gurgling moan rises from somewhere in the branching corridors, then cuts off.",
            "Shell casings tinkle and roll as something heavy shifts its weight in the dark.",
        ],
        danger_level=4,
        flags=["contaminated"],
    )
    world.add_room(security_corridor_south)

    armory_vault = Room(
        id="armory_vault",
        name="Armory Vault",
        deck="Deck E - Security",
        description=(
            "The vault behind the armory's biometric locker is small and "
            "brutally functional - reinforced walls, a single overhead light, "
            "and weapon racks designed for hardware you hope you never need. "
            "This is where the ship stored its last-resort arsenal, the weapons "
            "meant for scenarios that the mission planners hoped would remain "
            "theoretical.\n\n"
            "A tactical shotgun sits in a foam-lined rack, its barrel gleaming "
            "with fresh oil - someone maintained it regularly. Beside it, a "
            "flare gun with a bandolier of signal flares. A riot shield leans "
            "against the wall, its transparent surface scratched but intact. "
            "A locked case labeled EMERGENCY EXPLOSIVE CHARGES - AUTHORIZED "
            "USE ONLY contains shaped charges for hull breaching.\n\n"
            "On a separate shelf, set apart from the standard-issue equipment, "
            "sits a custom sidearm in a leather holster. The grip is worn smooth "
            "from years of use. Engraved along the barrel in small, precise "
            "letters: 'AMARA. KOFI. JAMES JR.' Okafor's family. His weapon. "
            "He left it here when he could no longer trust his own hands."
        ),
        smell_text=(
            "Gun oil, clean steel, and the faint chemical scent of explosive "
            "compounds sealed in their cases. The air is dry and cool - "
            "climate controlled to preserve the ordnance."
        ),
        touch_text=(
            "The weapons are cold and precisely machined. Okafor's sidearm "
            "is warm in a way that defies the room's temperature - or maybe "
            "that is your imagination. The riot shield is lighter than it looks."
        ),
        exits={
            'south': Exit(
                direction='south',
                destination='armory',
                description="You step back out into the main armory."
            ),
        },
        items=[
            "tactical_shotgun",
            "flare_gun",
            "riot_shield",
            "explosive_charges_case",
            "okafors_custom_sidearm",
            "flare_bandolier",
        ],
        ambient_sounds=[
            "The climate control unit hums steadily, preserving its lethal inventory.",
            "A faint vibration travels through the vault walls as something heavy moves in the corridor beyond.",
            "The overhead light buzzes with a thin, insistent whine.",
        ],
    )
    world.add_room(armory_vault)

    # ═══════════════════════════════════════════════════════════════════
    # DECK D - MEDICAL (Middle Deck Expansion)
    # ═══════════════════════════════════════════════════════════════════

    isolation_ward = Room(
        id="isolation_ward",
        name="Isolation Ward",
        deck="Deck D - Medical",
        description=(
            "Four individual isolation cells arranged in a row, each one "
            "a glass-walled cube three meters square with its own air supply "
            "and decontamination system. They were designed to keep contagion "
            "in. Looking at them now, you wonder if they were also designed "
            "to keep something out.\n\n"
            "Cell One is empty. Deep scratches score the inside of the glass - "
            "fingernail marks, frantic and overlapping, concentrated around "
            "the sealed door. Whoever was in here wanted out badly. Cell Two "
            "holds a body curled in the fetal position on the floor. Crystalline "
            "growths have erupted from the skin along the spine and shoulders, "
            "delicate and beautiful and utterly wrong - like frost flowers made "
            "of something that is not ice. Cell Three is empty, but the glass "
            "wall facing the corridor has a spiderweb fracture radiating from "
            "a single impact point on the inside. Something hit it. Hard.\n\n"
            "Cell Four holds Dr. Sarah Lin. She sits in the corner with her "
            "back against the wall, legs drawn up, hands folded in her lap. "
            "A small silver cross rests between her fingers. Her eyes are "
            "closed. She looks peaceful. She is dead. Her final medical notes "
            "lie beside her on the floor, the handwriting steady to the last line."
        ),
        smell_text=(
            "Antiseptic and the faintly sweet, alien scent of the crystalline "
            "growths. Each cell has its own sealed atmosphere, but the corridor "
            "between them carries a sterile chemical chill."
        ),
        touch_text=(
            "The glass walls are cold and smooth. The scratches in Cell One "
            "are rough under your fingertips, deep enough to catch a nail. "
            "The fractured glass in Cell Three flexes slightly when touched."
        ),
        exits={
            'north': Exit(
                direction='north',
                destination='medical_bay',
                description="You return to the main medical bay."
            ),
        },
        items=[
            "isolation_cell_one_scratches",
            "isolation_cell_two_body",
            "isolation_cell_three_crack",
            "dr_lin_body",
            "dr_lin_final_notes",
            "dr_lin_silver_cross",
        ],
        ambient_sounds=[
            "The isolation cells' independent air systems hiss with a faint, asthmatic wheeze.",
            "The crystalline growths in Cell Two chime softly, a barely audible ringing like distant wind chimes.",
            "A fluorescent light above Cell Three flickers in an irregular pattern, casting jumping shadows.",
        ],
    )
    world.add_room(isolation_ward)

    pharmacy = Room(
        id="pharmacy",
        name="Pharmacy",
        deck="Deck D - Medical",
        description=(
            "Rows of steel shelving stretch from floor to ceiling, stocked "
            "with medications in labeled bins arranged in strict alphabetical "
            "order. The organization is almost obsessive - Dr. Lin's work, no "
            "doubt. Each bin is tagged with drug name, dosage, quantity, and "
            "expiration date. The pharmacy was designed to support a crew of "
            "two hundred for a five-year mission. Most of it is still here.\n\n"
            "But not all of it. Several shelves have been stripped bare - the "
            "sedatives section is nearly empty, the anti-psychotics are gone, "
            "and someone cleaned out the emergency stimulants. Whoever raided "
            "the cryo deck's medical station came through here first. Empty "
            "bins are scattered on the floor where they were pulled in haste.\n\n"
            "On the back shelf, behind the immunosuppressants, a small "
            "refrigerated case hums quietly. Inside, labeled in Dr. Lin's "
            "handwriting: 'REAGENT A - EXPERIMENTAL. DO NOT ADMINISTER WITHOUT "
            "SYNTHESIS PROTOCOL.' This is one of the pieces of the cure."
        ),
        smell_text=(
            "The clean, dry smell of pharmaceuticals - pill coatings, sterile "
            "packaging, and the faint chemical tang of refrigerated biologics. "
            "It smells like a hospital that still believes in order."
        ),
        touch_text=(
            "The shelving is cold steel, the bins smooth plastic. The "
            "refrigerated case vibrates faintly under your hand. The scattered "
            "bins on the floor crunch underfoot."
        ),
        exits={
            'northeast': Exit(
                direction='northeast',
                destination='medical_corridor',
                description="You return to the medical corridor."
            ),
        },
        items=[
            "sedative_doses",
            "painkillers",
            "anti_radiation_meds",
            "immunosuppressants",
            "reagent_a_case",
            "pharmacy_inventory_log",
        ],
        ambient_sounds=[
            "The refrigerated case hums with a steady, reliable drone.",
            "Empty medication bins rock gently on the floor as the ship's gravity fluctuates.",
            "The pharmacy's dedicated air filtration unit cycles with a soft, periodic sigh.",
        ],
    )
    world.add_room(pharmacy)

    research_lab_med = Room(
        id="research_lab_med",
        name="Medical Research Laboratory",
        deck="Deck D - Medical",
        description=(
            "Dr. Lin's personal research laboratory is a controlled chaos of "
            "scientific equipment and desperate investigation. A centrifuge "
            "sits on the main bench, its rotor still loaded with sample vials - "
            "she was mid-experiment when she had to stop. Microscopes of varying "
            "magnification crowd a secondary bench. A chemical analysis station "
            "blinks with standby lights, waiting for the researcher who will "
            "not return.\n\n"
            "A corkboard on the wall is layered with research notes, diagrams, "
            "and photographs pinned in overlapping clusters. Red string connects "
            "related findings in a web of investigation that would look paranoid "
            "if it were not so methodical. At the center of the web: a photograph "
            "of the Seed artifact, circled three times in red marker.\n\n"
            "A whiteboard covers the opposite wall, dense with molecular diagrams "
            "drawn in four different colors of marker. The equations describe a "
            "synthesis process - complex, multi-step, requiring reagents from "
            "across the ship. At the bottom, underlined twice: 'THIS WORKS. "
            "I TESTED IT. BUT I CAN'T DO IT ALONE. - S.L.'"
        ),
        smell_text=(
            "Chemical reagents and the sharp, clean scent of laboratory-grade "
            "alcohol. Beneath it, the faint biological odor of tissue samples "
            "sealed in their containers."
        ),
        touch_text=(
            "The lab benches are smooth composite, cool to the touch. The "
            "centrifuge vibrates faintly even in standby mode. The corkboard "
            "pins prick your fingers when you reach between the overlapping notes."
        ),
        exits={
            'west': Exit(
                direction='west',
                destination='surgery',
                description="You return to the surgical theater."
            ),
        },
        items=[
            "research_centrifuge",
            "lin_research_notes",
            "molecular_whiteboard",
            "research_microscopes",
            "chemical_analysis_station",
            "centrifuge_sample_vials",
        ],
        ambient_sounds=[
            "The centrifuge emits a low, patient whir, its rotor turning at minimal speed to preserve the samples.",
            "A chemical analysis station beeps twice, pauses, beeps twice again - an automated cycle no one will read.",
            "The corkboard pins creak as the ship's vibration shifts the layered papers.",
        ],
    )
    world.add_room(research_lab_med)

    morgue_freezer = Room(
        id="morgue_freezer",
        name="Morgue Freezer",
        deck="Deck D - Medical",
        description=(
            "A walk-in freezer behind the main morgue, its heavy insulated "
            "door sealing with a pressurized gasp as it closes behind you. "
            "The temperature plummets immediately - your breath crystallizes "
            "into clouds, and frost forms on your eyebrows within seconds. "
            "The cold is a physical force, pressing against your skin like "
            "something alive.\n\n"
            "Rows of body bags lie on metal shelving that lines both walls, "
            "stacked two high. Twelve bags total. Each one is labeled with a "
            "crew member's name and date of death. The labels are frosted over, "
            "hard to read without scraping the ice away. The bodies are "
            "preserved perfectly by the sub-zero temperature, faces visible "
            "through the transparent panels of their bags - sleeping, you "
            "might think, if you did not know better.\n\n"
            "One bag near the back of the room is different. It is moving. "
            "Not much - a slow, rhythmic rise and fall, barely perceptible. "
            "As if the occupant is breathing. Slowly. Patiently. Waiting "
            "for something. Or someone."
        ),
        smell_text=(
            "The freezer strips most scent from the air, leaving only the "
            "sharp, clean bite of extreme cold. Beneath it, faintly, the "
            "chemical preservative smell of the body bags."
        ),
        touch_text=(
            "Everything is coated in a thin layer of frost that crunches "
            "under your fingers. The body bags are stiff and rigid with cold. "
            "The shelving burns exposed skin on contact. The moving bag, if "
            "you dare to touch it, is warmer than it should be."
        ),
        exits={
            'north': Exit(
                direction='north',
                destination='morgue',
                description="You push back through the freezer door into the morgue."
            ),
        },
        items=[
            "frozen_body_bags",
            "breathing_body_bag",
            "freezer_shelving",
            "frosted_name_labels",
        ],
        ambient_sounds=[
            "The freezer unit drones with a deep, mechanical thrum that makes the shelving vibrate.",
            "Frost crackles and pops as it expands on the walls and ceiling.",
            "From the bag near the back: a faint, wet, rhythmic sound. Like breathing through fluid.",
        ],
        temperature=-15,
        danger_level=3,
    )
    world.add_room(morgue_freezer)

    decontamination_shower = Room(
        id="decontamination_shower",
        name="Decontamination Station",
        deck="Deck D - Medical",
        description=(
            "A functional decontamination station situated between the medical "
            "wing and the quarantine section. The chamber is tiled in white "
            "ceramic, stained yellow in places by years of chemical spray. UV "
            "light arrays line the ceiling, currently dormant but ready. Nozzles "
            "protrude from the walls at regular intervals, connected to chemical "
            "spray reservoirs. An air filtration unit the size of a refrigerator "
            "dominates one corner, its HEPA filters still operational.\n\n"
            "A control panel beside the entrance offers a single large button "
            "labeled 'INITIATE DECONTAMINATION CYCLE.' A sign above it reads: "
            "'DECONTAMINATION CYCLE: 3 MINUTES. PLEASE REMAIN STILL. REMOVE "
            "ALL CLOTHING AND PERSONAL ITEMS BEFORE PROCEEDING.' Below the "
            "official text, someone has added in marker: 'Just kidding. Keep "
            "your clothes on. It works fine either way. - Yuki'\n\n"
            "A status display shows the system is charged and ready. Coolant "
            "reserves indicate one full cycle is available before a recharge "
            "period is required."
        ),
        smell_text=(
            "Harsh chemical disinfectant, like swimming pool chlorine "
            "concentrated tenfold. The UV lights give the air a faint "
            "ozone quality, sharp and clean."
        ),
        touch_text=(
            "The ceramic tiles are smooth and cool, slightly damp from "
            "residual moisture. The decontamination button is large, rubberized, "
            "and satisfying to press. The nozzles are crusted with dried "
            "chemical residue."
        ),
        exits={
            'west': Exit(
                direction='west',
                destination='quarantine_airlock',
                description="You step back into the quarantine airlock area."
            ),
        },
        items=[
            "decon_control_panel",
            "uv_light_arrays",
            "chemical_spray_nozzles",
            "air_filtration_unit",
            "decon_status_display",
            "yukis_marker_note",
        ],
        ambient_sounds=[
            "The air filtration unit cycles with a steady, reassuring hum.",
            "A chemical reservoir gurgles as fluid settles inside its tank.",
            "Water drips from a nozzle onto the tile floor in a slow, echoing plink.",
        ],
    )
    world.add_room(decontamination_shower)
