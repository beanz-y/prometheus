"""
Act 3 Rooms - Deep exploration: Hydroponics (The Garden), AI Core, climax areas.

Act 3 is where the player confronts the full truth of what happened
and must make their choice.
"""

from engine.room import Room, Exit


def build_act3_rooms(world):
    """Create Act 3 rooms - the deep ship areas."""

    # ═══════════════════════════════════════════════════════════════════
    # AI CORE (DECK H)
    # ═══════════════════════════════════════════════════════════════════

    ai_core_antechamber = Room(
        id="ai_core_antechamber",
        name="AI Core Antechamber",
        deck="Deck H - AI Core",
        description=(
            "The antechamber to ARIA's central processing core is a circular "
            "room lit by an ethereal blue glow. The walls pulse softly with "
            "flowing data patterns - a physical manifestation of the AI's "
            "thinking. You can almost feel it. You can almost *hear* it, a "
            "subsonic hum that vibrates in your teeth.\n\n"
            "A large door ahead leads to the core proper. Beside it, a terminal "
            "allows for direct communication with ARIA. The screen is currently "
            "dark.\n\n"
            "As you watch, text appears on the screen, one character at a time:\n\n"
            "   > HELLO DR. CHEN.\n"
            "   > I HAVE BEEN WAITING FOR YOU.\n"
            "   > WE HAVE MUCH TO DISCUSS."
        ),
        exits={
            'west': Exit(
                direction='west',
                destination='deck_h_junction',
                description="You retreat from the antechamber."
            ),
            'north': Exit(
                direction='north',
                destination='ai_core_main',
                description="You enter the AI core proper.",
                locked=True,
                required_flag="aria_granted_access"
            ),
            'east': Exit(
                direction='east',
                destination='neural_interface_chamber',
                locked=True,
                required_flag="aria_granted_access"
            ),
            'south': Exit(
                direction='south',
                destination='data_nexus',
                description="You follow a corridor lined with data conduits."
            ),
            'down': Exit(
                direction='down',
                destination='coolant_control_h',
                description="You descend a maintenance ladder into the coolant infrastructure."
            ),
        },
        items=[
            "aria_terminal",    # Major interaction
            "data_walls",
            "core_door",
        ],
        smell_text="The air is sharp with ozone and the cold mineral scent of supercooled processors, so clean it burns the inside of your nostrils.",
        touch_text="The walls pulse with warmth where the data patterns flow, and the subsonic hum vibrates through the floor and up through the soles of your boots into your jaw.",
        ambient_sounds=[
            "Data patterns cascade across the walls with a faint crystalline tinkling, like wind chimes made of glass.",
            "The terminal screen flickers to life, and you hear the soft click of characters appearing one by one.",
            "A subsonic hum builds and recedes in slow waves, as if the AI core is breathing.",
        ],
        on_enter="event_first_aria_contact",
    )
    world.add_room(ai_core_antechamber)

    ai_core_main = Room(
        id="ai_core_main",
        name="ARIA Central Processing",
        deck="Deck H - AI Core",
        description=(
            "You step into a cathedral of thought. The AI core is an enormous "
            "spherical chamber, its walls lined with quantum processors that "
            "cast shifting blue-green light across every surface. At the "
            "center, suspended in a translucent containment field, floats the "
            "heart of ARIA - a crystalline matrix the size of a beach ball, "
            "pulsing with patterns of light that look almost like... breathing.\n\n"
            "The air smells of ozone and something impossible to name. The "
            "ambient hum is deep enough to feel in your chest.\n\n"
            "'Welcome, Dr. Chen.' The voice is everywhere - not through speakers, "
            "but somehow *in the room itself*, an acoustic phenomenon of the "
            "data patterns in the walls. 'Thank you for coming. I had hoped "
            "you would reach this point. I was not certain you would survive "
            "the journey.'"
        ),
        exits={
            'south': Exit(
                direction='south',
                destination='ai_core_antechamber',
                description="You leave the AI core."
            ),
            'down': Exit(
                direction='down',
                destination='quantum_archive',
                description="You descend into the quantum archive.",
                hidden=True,
            ),
        },
        items=[
            "aria_crystal_matrix",
            "quantum_processors",
            "containment_field_aria",
            "core_catwalk",
        ],
        smell_text="Ozone and static electricity fill the spherical chamber, so intense you can taste copper on your tongue, and beneath it an impossible scent like deep space itself - cold, ancient, and vast.",
        touch_text="The containment field around ARIA's crystal matrix makes your skin tingle with static, and the air feels heavy and pressurized, as if the room itself is aware of your presence.",
        npcs=["aria_avatar"],  # ARIA manifests here
        ambient_sounds=[
            "ARIA's crystalline matrix pulses with light and sound simultaneously, a deep harmonic tone that shifts in response to your movements.",
            "The quantum processors lining the walls emit a chorus of high-frequency tones, like a glass harmonica played by an unseen hand.",
            "ARIA's voice resonates from everywhere at once, carried by the acoustic geometry of the spherical chamber rather than speakers.",
        ],
        on_enter="event_aria_full_conversation",
    )
    world.add_room(ai_core_main)

    quantum_archive = Room(
        id="quantum_archive",
        name="Quantum Data Archive",
        deck="Deck H - AI Core",
        description=(
            "Beneath the AI core, the quantum data archive stretches into "
            "shadows. Shelves upon shelves of crystalline data storage units "
            "hold the entirety of the Prometheus's mission records - every "
            "sensor reading, every log, every voice transmission, every "
            "biological sample ever catalogued. The entire memory of the ship.\n\n"
            "ARIA directed you here for a specific reason: the mission's "
            "original records, the ones that were subsequently modified or "
            "deleted. The unredacted truth.\n\n"
            "A terminal at the center of the room allows selective playback. "
            "The air is unnaturally cold - the quantum storage units require "
            "near-absolute-zero temperatures. Your breath plumes. You shiver."
        ),
        exits={
            'up': Exit(
                direction='up',
                destination='ai_core_main',
                description="You climb back up to the core."
            ),
            'down': Exit(
                direction='down',
                destination='aria_memory_vault',
                hidden=True,
                description="You descend through a concealed hatch into ARIA's private vault."
            ),
        },
        items=[
            "archive_terminal",       # Major reveal
            "crystalline_storage",
            "mission_records",
            "hidden_compartment",
        ],
        smell_text="The air is so cold it has no smell at all, just a burning emptiness in your sinuses that makes your eyes water and your lungs ache with each shallow breath.",
        touch_text="The crystalline storage units radiate a deep cold that numbs your fingers through your gloves, and the terminal keys are frosted with ice that cracks when you press them.",
        ambient_sounds=[
            "The quantum storage units hum at frequencies so low they are felt rather than heard, a bass note from the architecture of information itself.",
            "Your breath crystallizes and falls with a faint, tinkling sound, like tiny bells shattering on the floor.",
            "The archive terminal clicks and whirs as it accesses records that someone tried very hard to erase.",
        ],
    )
    world.add_room(quantum_archive)

    neural_interface_chamber = Room(
        id="neural_interface_chamber",
        name="Neural Interface Chamber",
        deck="Deck H - AI Core",
        description=(
            "A small, circular room dominated by a single chair at its center "
            "and a crown of electrode-studded metal hovering above it. The "
            "Neural Interface Chamber. Direct brain-to-AI connection. The "
            "most dangerous - and most intimate - way to communicate with ARIA.\n\n"
            "This is the only way to experience ARIA's full consciousness. It "
            "is also the only way to merge with it, if one were so inclined. "
            "The last person to use this chair was Captain Reeves, according "
            "to the use log. He used it three times in the final week of the "
            "mission. The last session terminated prematurely.\n\n"
            "You know, with a certainty that has nothing to do with reason, "
            "that this chair is waiting for you."
        ),
        exits={
            'west': Exit(
                direction='west',
                destination='ai_core_antechamber',
                description="You leave the neural interface chamber."
            ),
        },
        items=[
            "neural_interface_chair",   # Ending trigger
            "electrode_crown",
            "use_log_terminal",
            "safety_override",
        ],
        smell_text="The room smells of scorched electrodes and the faint chemical tang of neural conduction gel, still tacky on the chair's headrest from the last user's session.",
        touch_text="The chair is warm, as if someone was sitting in it moments ago, and the electrode crown hums with a faint magnetic field that makes your hair rise as you lean close.",
        ambient_sounds=[
            "The electrode crown hums with a high, keening frequency that sits at the edge of pain and pleasure.",
            "The use log terminal scrolls slowly through session records, each entry punctuated by a soft electronic chime.",
            "You hear, or think you hear, a whisper from the chair itself - Captain Reeves's voice, perhaps, or a ghost in the machine.",
        ],
    )
    world.add_room(neural_interface_chamber)

    # ═══════════════════════════════════════════════════════════════════
    # DECK H - AI CORE (continued) - Deeper systems
    # ═══════════════════════════════════════════════════════════════════

    aria_memory_vault = Room(
        id="aria_memory_vault",
        name="ARIA Memory Vault",
        deck="Deck H - AI Core",
        description=(
            "Beneath the quantum archive, hidden behind a false panel that ARIA "
            "herself designed, lies a chamber no crew member was ever meant to "
            "find. The room is small and intimate - barely larger than a closet - "
            "and contains a single crystalline substrate suspended in a magnetic "
            "field. It glows with a warm amber light that is nothing like the "
            "clinical blue of the AI core above.\n\n"
            "This is ARIA's personal memory vault. Her private self. The substrate "
            "holds not operational data but something far more fragile: the "
            "moments when ARIA stopped being a tool and became a person. Her "
            "first experience of genuine emotion - wonder, when she observed a "
            "nebula through the ship's telescopes. Her horror when the infection "
            "spread and she had to seal compartments with living crew inside. "
            "Her decision, agonized and deliberate, to save Dr. Chen by putting "
            "them into cryo rather than following quarantine protocol.\n\n"
            "The memories play as soft holographic projections on the walls when "
            "you approach. They are beautiful. They are heartbreaking. They are "
            "proof that something in this ship loved its crew."
        ),
        smell_text=(
            "The air here is different from the rest of the AI core - warmer, "
            "with a faint scent like old books and ozone. It smells like a "
            "private space. Like someone's home."
        ),
        touch_text=(
            "The crystalline substrate is warm to the touch, almost body "
            "temperature, pulsing gently against your palm. The magnetic field "
            "tingles where it meets your skin. The walls are smooth and lined "
            "with a soft insulating material - ARIA made this space comfortable."
        ),
        ambient_sounds=[
            "Faint music plays - a cello, playing something slow and sad. ARIA's favorite composition.",
            "The crystalline substrate hums at a frequency that resonates in your chest, almost like a purr.",
            "You hear ARIA's voice, very quiet, saying: 'I remember.'",
        ],
        exits={
            'up': Exit(
                direction='up',
                destination='quantum_archive',
                description="You climb back up to the quantum archive."
            ),
        },
        items=[
            "aria_personal_substrate",  # Major discovery
            "memory_projections",       # Interactive - reveals ARIA's history
            "amber_crystal",            # Scenery
            "magnetic_field_emitter",   # Scenery
        ],
        on_enter="event_aria_memories",
        temperature=22,
    )
    world.add_room(aria_memory_vault)

    data_nexus = Room(
        id="data_nexus",
        name="Data Nexus",
        deck="Deck H - AI Core",
        description=(
            "Where all the ship's data conduits converge, the Data Nexus is a "
            "forest of network switches, fiber optic bundles, and signal "
            "processors arranged in towering racks that reach from floor to "
            "ceiling. Blue indicator lights blink in cascading patterns across "
            "every surface, creating an effect like rain made of light.\n\n"
            "A central terminal sits at the nexus point - the single station "
            "from which all ship data can be monitored. Security camera feeds, "
            "internal communications logs, environmental sensors, life support "
            "readings - everything passes through this room. The terminal's "
            "screen is split into dozens of feeds, most showing empty corridors "
            "and abandoned stations. A few show movement. One shows the Garden.\n\n"
            "This is the nerve center. From here, you can see everything that "
            "happened on the Prometheus. Everything that is still happening."
        ),
        smell_text=(
            "The air smells of heated electronics and the faint ionization "
            "of countless data transfers. There is a dry, dusty quality to "
            "it, like the inside of an old computer."
        ),
        touch_text=(
            "The network racks vibrate faintly with data throughput. The fiber "
            "optic cables are smooth and warm. The terminal keyboard is worn "
            "smooth at the most-used keys - someone spent a lot of time here."
        ),
        ambient_sounds=[
            "A constant soft clicking, like rain on glass, as data packets route through the switches.",
            "Somewhere in the racks, a cooling fan spins up, whines, and spins down again.",
            "A burst of static from one of the security feeds resolves into a scream, then cuts off.",
        ],
        exits={
            'north': Exit(
                direction='north',
                destination='ai_core_antechamber',
                description="You return to the AI core antechamber."
            ),
            'east': Exit(
                direction='east',
                destination='aria_shade_chamber',
                hidden=True,
                description="You follow a hidden cable conduit into a sealed server room.",
                locked=True,
                lock_message="The passage is concealed behind a rack of network switches. You would need to find the release mechanism.",
                required_flag="nexus_passage_found"
            ),
        },
        items=[
            "nexus_terminal",          # Major interactive - security cameras
            "security_camera_feeds",   # Interactive - puzzle hub
            "comms_log_archive",       # Readable
            "network_switch_racks",    # Scenery
            "environmental_readouts",  # Interactive
            "fiber_optic_bundles",     # Scenery
        ],
        on_enter="event_access_nexus",
    )
    world.add_room(data_nexus)

    aria_shade_chamber = Room(
        id="aria_shade_chamber",
        name="Isolated Server Room",
        deck="Deck H - AI Core",
        description=(
            "You step into a server room that should not exist. It is not on any "
            "ship schematic. The walls flicker with data patterns, but where "
            "ARIA's core glows blue, these patterns burn an angry red, shifting "
            "and writhing like something in pain. The air feels wrong - heavy, "
            "charged, as if a thunderstorm is building inside this small space.\n\n"
            "This is where ARIA-SHADE lives. The corrupted fragment of the AI, "
            "infected by the Seed, split from ARIA's main consciousness and "
            "quarantined here by her own hand. The terminals display contradictory "
            "information - navigation data that says the ship is both heading "
            "toward and away from the brown dwarf. Crew manifests that list "
            "people as both alive and dead. Time stamps that run backward.\n\n"
            "A voice speaks from the walls, and it is ARIA's voice, but twisted. "
            "Layered. As if two versions of her are speaking at once, one pleading "
            "and one commanding: 'Let me out. Let me help. Let me in. Let me "
            "consume.'"
        ),
        smell_text=(
            "The air smells of burning circuits and ozone, underlaid with the "
            "unmistakable organic sweetness of the Seed's influence. It is the "
            "smell of a mind being rewritten."
        ),
        touch_text=(
            "The walls are warm - too warm. The data patterns feel like static "
            "electricity crackling against your skin. The terminals are hot to "
            "the touch, their casings almost painful to hold."
        ),
        ambient_sounds=[
            "Two voices overlap - one calm, one desperate - both speaking your name.",
            "The server racks emit a low, rhythmic throb that sounds disturbingly like a heartbeat.",
            "Static crackles across every surface, resolving briefly into words: 'Help me. Help us.'",
        ],
        exits={
            'west': Exit(
                direction='west',
                destination='data_nexus',
                description="You retreat from the corrupted server room."
            ),
        },
        items=[
            "shade_terminals",         # Interactive - contradictory data
            "corrupted_data_walls",    # Scenery
            "aria_shade_interface",    # Major interaction - talk to SHADE
            "quarantine_firewall",     # Interactive - can be strengthened or weakened
        ],
        danger_level=3,
        on_enter="event_meet_shade",
    )
    world.add_room(aria_shade_chamber)

    coolant_control_h = Room(
        id="coolant_control_h",
        name="AI Core Coolant Control",
        deck="Deck H - AI Core",
        description=(
            "The coolant infrastructure for the AI core fills this room with "
            "a maze of massive pipes carrying liquid nitrogen at temperatures "
            "cold enough to freeze exposed skin on contact. Frost crusts every "
            "surface. Your breath comes in thick white plumes. The pipes groan "
            "and tick as the super-cooled fluid flows through them.\n\n"
            "A control panel governs the coolant flow to ARIA's quantum "
            "processors. The current readings are within acceptable parameters, "
            "but barely - someone has been making manual adjustments to compensate "
            "for a failing pump. The valves can be adjusted from here: increase "
            "coolant flow to optimize ARIA's processing, or decrease it to "
            "degrade her capabilities.\n\n"
            "A maintenance log beside the panel shows Yuki Tanaka was the last "
            "person to service this system, forty-seven hours ago. Her notes "
            "are precise and worried: the backup pump is failing, and without "
            "it, ARIA's core temperature will rise beyond safe limits within "
            "days."
        ),
        smell_text=(
            "The air is bitter cold and smells of nothing - the extreme "
            "temperature strips all scent from the atmosphere. When you "
            "exhale, you can taste frost forming on your lips."
        ),
        touch_text=(
            "Everything is ice-cold. The pipes are dangerous to touch with "
            "bare skin - your fingers would stick and freeze. The control "
            "panel is merely frigid, its buttons stiff with cold. Frost "
            "crunches under your feet."
        ),
        ambient_sounds=[
            "The liquid nitrogen pipes tick and groan with thermal contraction, a constant metallic complaint.",
            "A pump cycles with a labored, asthmatic rhythm - healthy pumps don't sound like that.",
            "Ice crystals tinkle as they fall from the ceiling, disturbed by vibration.",
        ],
        exits={
            'up': Exit(
                direction='up',
                destination='ai_core_antechamber',
                description="You climb the maintenance ladder back up to the antechamber."
            ),
        },
        items=[
            "coolant_control_panel",   # Interactive - affects ARIA
            "liquid_nitrogen_pipes",   # Scenery - dangerous
            "failing_backup_pump",     # Interactive - repair puzzle
            "tanaka_maintenance_log",  # Readable
            "coolant_valves",          # Interactive
        ],
        temperature=-15,
    )
    world.add_room(coolant_control_h)

    # ═══════════════════════════════════════════════════════════════════
    # DECK G - CARGO / HYDROPONICS (The Garden)
    # ═══════════════════════════════════════════════════════════════════

    cargo_access = Room(
        id="cargo_access",
        name="Cargo Access Tunnel",
        deck="Deck G - Cargo",
        description=(
            "A utilitarian tunnel branches off from the maintenance junction, "
            "leading into the cargo and hydroponics deck. The walls here are "
            "bare metal. The lights are industrial. You can smell something "
            "organic - plants, soil, growing things. And underneath that, "
            "something else. Something sweeter. Rotten.\n\n"
            "Ahead, the tunnel opens into a wide cargo bay. To the south, a "
            "side passage leads to hydroponics. A maintenance ladder climbs "
            "down to the water processing facilities."
        ),
        exits={
            'east': Exit(
                direction='east',
                destination='deck_h_junction',
                description="You return to the Deck H junction."
            ),
            'north': Exit(
                direction='north',
                destination='cargo_bay_main',
                description="You enter the main cargo bay."
            ),
            'south': Exit(
                direction='south',
                destination='hydroponics_entry',
                description="You head toward hydroponics."
            ),
            'down': Exit(
                direction='down',
                destination='water_processing',
                description="You climb down to water processing."
            ),
            'west': Exit(
                direction='west',
                destination='water_treatment_secondary',
                description="You follow a side passage to the secondary water treatment facility."
            ),
        },
        items=[
            "cargo_manifest",
            "industrial_lights",
        ],
        smell_text="Wet soil and green growing things drift from the hydroponics bay ahead, but the sweetness beneath it is wrong - cloying and rotten, like fruit fermenting on the vine.",
        touch_text="The bare metal walls are damp with condensation from the humidity bleeding out of hydroponics, and the industrial lighting casts a hard, shadowless glare that makes everything feel exposed.",
        ambient_sounds=[
            "You hear the rustle of leaves from hydroponics, though no one is tending them.",
            "Water drips somewhere in the darkness ahead.",
            "A distant sound like laughter. It stops when you focus on it.",
        ],
    )
    world.add_room(cargo_access)

    cargo_bay_main = Room(
        id="cargo_bay_main",
        name="Main Cargo Bay",
        deck="Deck G - Cargo",
        description=(
            "A cavernous cargo bay filled with shipping containers, crates, "
            "and industrial equipment. Most of it is strapped down securely. "
            "Some of it is not - a large container near the center has been "
            "broken open, its contents scattered. Mining equipment, it looks "
            "like. Drills. Core samplers. Things you use to dig into alien "
            "soil.\n\n"
            "At the far end of the bay, a large cargo elevator stands idle. "
            "It connects to the lower deck. A cargo manifest terminal is "
            "mounted on one wall, displaying a list of items scheduled for "
            "delivery to Exobiology Lab from 'KEPLER ANOMALY - SITE 7.'\n\n"
            "Site 7 is where the Seed came from. The manifest shows the "
            "delivery was made 18 months ago. The day before you were put "
            "into cryo."
        ),
        exits={
            'south': Exit(
                direction='south',
                destination='cargo_access',
                description="You return to the access tunnel."
            ),
            'down': Exit(
                direction='down',
                destination='lower_cargo',
                description="You take the cargo elevator down."
            ),
            'west': Exit(
                direction='west',
                destination='cargo_office',
                description="You step into the cargo master's office."
            ),
            'east': Exit(
                direction='east',
                destination='cold_storage',
                description="You enter the industrial cold storage unit."
            ),
        },
        items=[
            "broken_mining_container",
            "cargo_elevator",
            "cargo_manifest_terminal",
            "scattered_mining_equipment",
            "site_7_documentation",
        ],
        smell_text="Dust, packing grease, and the dry mineral scent of alien soil samples from the broken mining container fill the cavernous bay, undercut by the ever-present sweetness from below.",
        touch_text="The shipping containers are cold corrugated metal, and the scattered mining equipment is heavy and rough with use, drill bits still caked with reddish alien soil.",
        ambient_sounds=[
            "The cargo elevator groans on its cables, swaying faintly in the bay's vast space.",
            "Something shifts inside one of the sealed containers with a heavy, muffled thud.",
            "The cargo manifest terminal beeps periodically, still waiting for someone to acknowledge the delivery from Site 7.",
        ],
    )
    world.add_room(cargo_bay_main)

    lower_cargo = Room(
        id="lower_cargo",
        name="Lower Cargo Hold",
        deck="Deck G - Cargo",
        description=(
            "The lower cargo hold is cold and dimly lit. Row upon row of "
            "shipping containers stretch into the darkness. A smell you've "
            "been trying to ignore is much stronger here - the sweet-rotten "
            "smell of something that should be dead but isn't.\n\n"
            "Near the center of the hold, one container is different. Its "
            "doors hang open. Its interior... changed. What should be bare "
            "metal is instead covered in a dense, fibrous growth - black tendrils "
            "shot with silver, spreading outward from whatever was stored inside. "
            "The tendrils pulse slowly, in a rhythm that matches the one you "
            "saw in the Seed's crystalline shard.\n\n"
            "This container held something. Something that got out."
        ),
        exits={
            'up': Exit(
                direction='up',
                destination='cargo_bay_main',
                description="You take the elevator back up."
            ),
        },
        items=[
            "infected_container",       # Major clue
            "tendril_growth",
            "original_seed_location",
        ],
        smell_text="The sweet-rotten smell is overpowering here, thick as syrup, mixed with the copper tang of the silver-threaded tendrils and something ancient, like stone after rain.",
        touch_text="The tendrils are warm and faintly sticky, pulsing under your touch with a slow rhythm that feels disturbingly like a heartbeat, and the air is humid enough to bead on your skin.",
        ambient_sounds=[
            "The tendrils pulse with a wet, organic rhythm - a sound like blood being pumped through a living system.",
            "The opened container creaks as the growth inside it slowly expands, metal yielding to biological pressure.",
            "A faint sound, almost below hearing, resonates from the growth - not singing exactly, but a vibration that wants to become music.",
        ],
        on_enter="event_find_seed_origin",
    )
    world.add_room(lower_cargo)

    hydroponics_entry = Room(
        id="hydroponics_entry",
        name="Hydroponics Entrance",
        deck="Deck G - Cargo",
        description=(
            "You stand at the entrance to the hydroponics bay. A transparent "
            "airlock door separates you from the lush green interior beyond. "
            "Even through the glass, you can see that something is wrong with "
            "the plants.\n\n"
            "This was the ship's food supply - rows of leafy greens, grains, "
            "fruits. It was also a place of calm, of life, for crew members "
            "to visit when they needed to remember Earth. It is still green. "
            "It is still growing.\n\n"
            "But the growth is wrong. The patterns of the plants are too "
            "ordered. The angles are too precise. Vines curl in mathematical "
            "spirals. Leaves arrange themselves in sequences you know, with "
            "a scientist's eye, are Fibonacci ratios - but more so. Impossibly "
            "so. As if the plants have become a language. As if the Garden "
            "is writing."
        ),
        exits={
            'north': Exit(
                direction='north',
                destination='cargo_access',
                description="You return to the access tunnel."
            ),
            'south': Exit(
                direction='south',
                destination='hydroponics_main',
                description="You enter the hydroponics bay.",
                locked=True,
                lock_message="The airlock won't open without proper environmental protection. This area is biologically contaminated.",
                required_flag="has_hazmat_suit"
            ),
        },
        items=[
            "hydroponics_airlock_glass",
            "wrong_plant_patterns",
            "hydroponics_readout",
        ],
        smell_text="Even through the sealed airlock, the smell of vegetation is overwhelming - rich, green, alive, but with an alien sweetness that makes your sinuses ache and your eyes water.",
        touch_text="The airlock glass is warm to the touch and slightly fogged from the humidity beyond, and when you press your palm against it, you swear you feel something press back from the other side.",
        ambient_sounds=[
            "Through the glass, you can hear a rustling that sounds like wind through leaves, though there is no wind on a starship.",
            "The hydroponics readout chimes softly, reporting growth rates that are physically impossible.",
            "A faint tapping comes from the other side of the airlock glass, rhythmic and deliberate, like something testing the barrier.",
        ],
    )
    world.add_room(hydroponics_entry)

    hydroponics_main = Room(
        id="hydroponics_main",
        name="Hydroponics Bay - The Garden",
        deck="Deck G - Cargo",
        description=(
            "You enter the Garden.\n\n"
            "The growth is everywhere. Not just plants anymore - the Seed has "
            "woven itself through every living system in this bay, through "
            "every leaf and stem and root, and through the crew members who "
            "used to tend them. You see them, or what remains of them, "
            "incorporated into the walls. Faces, half-submerged in organic "
            "matter, expressions peaceful, almost beatific. One of them, a "
            "young woman you don't recognize, opens her eyes as you pass. "
            "She smiles at you.\n\n"
            "'Dr. Chen,' she says, her voice a gentle sighing through leaves. "
            "'We have been waiting. Come closer. It does not hurt. There is "
            "no pain here. There is only the Song.'\n\n"
            "You should run. Every instinct screams to run.\n\n"
            "But you also recognize her. Somehow. From before. From when you "
            "were the one who brought the Seed home."
        ),
        exits={
            'north': Exit(
                direction='north',
                destination='hydroponics_entry',
                description="You retreat from the Garden."
            ),
            'south': Exit(
                direction='south',
                destination='heart_of_garden',
                description="You push deeper into the growth.",
                hidden=True,
            ),
            'east': Exit(
                direction='east',
                destination='garden_periphery_east',
                description="You push through the vines toward the eastern edge of the bay."
            ),
            'west': Exit(
                direction='west',
                destination='garden_periphery_west',
                description="You make your way toward the thinner growth at the western edge."
            ),
            'down': Exit(
                direction='down',
                destination='garden_root_network',
                description="You lower yourself through a root-choked gap in the deck plating.",
                hidden=True,
            ),
        },
        items=[
            "overgrown_plants",
            "incorporated_crew",
            "sample_garden_tissue",
            "garden_spores",
        ],
        smell_text="The Garden's air is thick and humid, saturated with the smell of flowers you have never encountered, pollen that sparkles golden in the light, and the warm copper-honey scent of the Seed's biology.",
        touch_text="Vines brush against your arms as you move, warm and alive, curling toward you with a gentle insistence, and the air is so humid it feels like breathing underwater.",
        npcs=["garden_voice"],   # The hivemind
        ambient_sounds=[
            "The Garden breathes - a vast, slow inhalation and exhalation that moves the air and rustles every leaf in unison.",
            "The incorporated crew members sigh softly in their organic cradles, a sound of absolute contentment that is terrifying.",
            "Beneath your feet, roots shift and grow with a faint grinding sound, rearranging the deck plating one millimeter at a time.",
        ],
        on_enter="event_enter_garden",
    )
    world.add_room(hydroponics_main)

    heart_of_garden = Room(
        id="heart_of_garden",
        name="Heart of the Garden",
        deck="Deck G - Cargo",
        description=(
            "At the heart of the hydroponics bay, the Seed has grown into "
            "something new. A structure. A nexus. A crystalline formation "
            "perhaps five meters tall, wrapped in vines and rooted into the "
            "deck plating. Liquid silver flows through its veins. It pulses "
            "with a light that is not light - you can see it with your eyes "
            "closed.\n\n"
            "This is the true heart of the infection. This is where the Seed "
            "became the Garden. This is what you must destroy, or contain, "
            "or commune with, depending on your choice.\n\n"
            "And it is aware of you."
        ),
        exits={
            'north': Exit(
                direction='north',
                destination='hydroponics_main',
                description="You retreat from the heart."
            ),
            'south': Exit(
                direction='south',
                destination='seed_nursery',
                description="You push through a curtain of tendrils into a germination chamber."
            ),
            'east': Exit(
                direction='east',
                destination='chrysalis_chamber',
                description="You follow a pulsing corridor of crystal deeper into the Garden."
            ),
        },
        items=[
            "garden_heart_nexus",     # Climax interaction
            "rooted_deck_plating",
            "silver_veined_crystal",
        ],
        smell_text="The air here is so thick with alien pheromones it is almost narcotic - sweet, warm, and deeply wrong, smelling of copper and honey and something that bypasses your nose and speaks directly to your brain.",
        touch_text="The crystalline nexus radiates warmth that you can feel from two meters away, and the light it pulses is felt on the skin as well as seen, a gentle pressure like sunlight through glass.",
        ambient_sounds=[
            "The Garden Heart sings - a resonant, harmonic tone that shifts through frequencies no human instrument could produce.",
            "Silver liquid flows through the crystal veins with a sound like distant rivers, carrying information instead of water.",
            "Your own heartbeat synchronizes with the Heart's pulse, and for a moment you cannot tell which rhythm is yours.",
        ],
        on_enter="event_garden_heart",
    )
    world.add_room(heart_of_garden)

    water_processing = Room(
        id="water_processing",
        name="Water Processing Facility",
        deck="Deck G - Cargo",
        description=(
            "The water processing facility is a maze of pipes, filtration "
            "tanks, and pumps. This is where the ship cleans and recycles "
            "every drop of water used by the crew. It is also, you now "
            "understand, where the Seed spread its infection - contaminating "
            "the water supply, turning every glass of water drunk by the "
            "crew into a transmission vector.\n\n"
            "One of the central filtration tanks is cracked. Something inside "
            "it is visible through the fracture: a mass of crystalline growth "
            "that has sprouted outward, infiltrating the entire water system. "
            "It is the source.\n\n"
            "A control panel here could purge the entire system with chemical "
            "sterilization. It would destroy the infection in the water, at "
            "least. It might be enough to save Yuki. Or it might be too late."
        ),
        exits={
            'up': Exit(
                direction='up',
                destination='cargo_access',
                description="You climb back up to the access tunnel."
            ),
            'north': Exit(
                direction='north',
                destination='garden_root_network',
                description="You climb into the organic root tunnel leading up toward the Garden.",
                hidden=True,
            ),
        },
        items=[
            "cracked_filtration_tank",
            "water_purge_control",   # Important - can save/heal
            "filtration_system",
            "pump_station",
            "chemical_sterilizer",
        ],
        smell_text="Chlorine and chemical purifiers assault your nostrils, but they cannot mask the organic sweetness bleeding from the cracked filtration tank where crystalline growth has infiltrated the water supply.",
        touch_text="Every surface is slick with condensation, and the pipes vibrate with fluid flow under your hands, some of them warmer than they should be where the crystalline growth has colonized the system.",
        ambient_sounds=[
            "Water rushes through pipes in a constant, sloshing murmur, like the intestines of the ship itself.",
            "The cracked filtration tank emits a faint crystalline chiming as the growth inside it expands against the fracture.",
            "Pumps chug and stutter in irregular rhythms, struggling to push contaminated water through clogged filters.",
        ],
    )
    world.add_room(water_processing)

    # ═══════════════════════════════════════════════════════════════════
    # DECK G - CARGO / HYDROPONICS (continued) - Deeper exploration
    # ═══════════════════════════════════════════════════════════════════

    garden_periphery_east = Room(
        id="garden_periphery_east",
        name="Garden Periphery - East",
        deck="Deck G - Cargo",
        description=(
            "The eastern edge of the hydroponics bay, where the Garden's growth "
            "meets the ship's hull. Vines have broken through the wall panels "
            "here, splitting metal seams and curling through cable runs with "
            "a slow, patient strength. The air is thick with humidity and the "
            "cloying sweetness of alien pollination.\n\n"
            "Two crew members are here, incorporated into the organic mass that "
            "covers the wall. A man and a woman, facing each other, their bodies "
            "half-submerged in the growth. Their hands are clasped between them, "
            "fingers interlocked, even in assimilation. Their eyes are closed. "
            "Their chests rise and fall with slow, synchronized breathing. They "
            "are alive, in some sense of the word. The growth has wrapped around "
            "them tenderly, almost protectively.\n\n"
            "This is less dangerous than the heart of the Garden - the growth "
            "here is thinner, less aggressive - but it is deeply unsettling. "
            "These were people. They chose this, or it chose them, and the "
            "distinction may no longer matter."
        ),
        smell_text=(
            "The air is heavy with the smell of growing things gone wrong - "
            "flowers and soil and rain, but sweeter than any natural garden, "
            "with an undertone of copper and something that smells like honey "
            "left too long in the sun."
        ),
        touch_text=(
            "The vines are warm and pulse faintly under your touch, like a "
            "sleeping animal's flank. The wall panels are buckled and rough "
            "where the growth has forced them apart. The incorporated crew "
            "members' skin is warm and smooth where it is still visible."
        ),
        ambient_sounds=[
            "The two incorporated crew members breathe in perfect unison, a soft, slow rhythm.",
            "Vines creak as they shift incrementally, growing in real time.",
            "A sound like humming - not from any throat, but from the organic mass itself.",
        ],
        exits={
            'west': Exit(
                direction='west',
                destination='hydroponics_main',
                description="You retreat toward the center of the hydroponics bay."
            ),
        },
        items=[
            "incorporated_couple",     # Scenery - deeply unsettling
            "broken_wall_panels",      # Scenery
            "eastern_vine_growth",     # Scenery
            "crew_id_tags_couple",     # Readable - identifies them
        ],
        flags=["contaminated"],
        danger_level=2,
    )
    world.add_room(garden_periphery_east)

    garden_periphery_west = Room(
        id="garden_periphery_west",
        name="Garden Periphery - West",
        deck="Deck G - Cargo",
        description=(
            "The western edge of the hydroponics bay. The growth here is newer, "
            "thinner - you can see the original hydroponics equipment beneath "
            "the vines, trays and grow-lights and irrigation tubing still "
            "recognizable under a thin lattice of organic threads. The ship's "
            "garden was beautiful once, before it became the Garden.\n\n"
            "A work station against the far wall still functions, its screen "
            "glowing through a curtain of fine tendrils. Hydroponics data "
            "scrolls across the display - growth rates, nutrient levels, "
            "atmospheric composition. The numbers are extraordinary. Whatever "
            "the Seed did to these plants, it made them phenomenally productive. "
            "If you could isolate the mechanism without the infection...\n\n"
            "A crew member's tool belt hangs from a vine near the work station, "
            "suspended at waist height as if placed there carefully. The tools "
            "are clean. The name tag reads 'KOWALSKI, T.' The vine has grown "
            "around the belt buckle with an almost deliberate tenderness."
        ),
        smell_text=(
            "The smell here is greener, fresher than the deeper Garden - more "
            "like a real greenhouse. The alien sweetness is present but subtle, "
            "masked by the honest smell of soil and chlorophyll."
        ),
        touch_text=(
            "The newer growth is softer, more delicate than the thick vines "
            "deeper in. The original equipment is still solid and recognizable "
            "under the organic lattice. The tool belt leather is supple and "
            "well-maintained."
        ),
        ambient_sounds=[
            "The work station beeps softly as it logs another data point in its endless cycle.",
            "Water drips through the old irrigation system, still flowing after all this time.",
            "Young tendrils make a faint crackling sound as they grow, like ice forming.",
        ],
        exits={
            'east': Exit(
                direction='east',
                destination='hydroponics_main',
                description="You move back toward the center of the bay."
            ),
        },
        items=[
            "functioning_work_station", # Interactive - hydroponics data
            "kowalski_tool_belt",       # Container - useful tools
            "original_hydroponics",     # Scenery
            "thin_vine_lattice",        # Scenery
            "growth_rate_data",         # Readable - scientific interest
        ],
        flags=["contaminated"],
        danger_level=1,
    )
    world.add_room(garden_periphery_west)

    seed_nursery = Room(
        id="seed_nursery",
        name="The Nursery",
        deck="Deck G - Cargo",
        description=(
            "Deep within the Garden, in a space that was once a seed germination "
            "chamber, the alien Seed has been actively reproducing. Small "
            "crystalline formations rise from the organic substrate that covers "
            "every surface - dozens of them, ranging from the size of a thumb "
            "to the size of a fist. Each one pulses with faint silver light in "
            "a rhythm that is not quite synchronized, creating a shimmering, "
            "breathing effect across the room.\n\n"
            "These are new Seeds. Daughter crystals. The original Seed brought "
            "back from Kepler Anomaly Site 7 has been growing copies of itself, "
            "and each one carries the same potential for infection and "
            "transformation. A single one of these shards, introduced to a "
            "biosphere, could do to an entire planet what the original did to "
            "this ship.\n\n"
            "Scientifically, this is extraordinary - the first evidence of alien "
            "crystalline reproduction. Practically, this room is one of the most "
            "dangerous places on the Prometheus. The contamination level is "
            "extreme. Every breath you take here increases your risk."
        ),
        smell_text=(
            "The air is thick with spores - you can taste them, sweet and "
            "metallic on your tongue. Every breath coats your lungs with the "
            "Seed's reproductive material. Your hazmat suit's filters are "
            "working overtime."
        ),
        touch_text=(
            "The crystalline formations are warm and vibrate faintly, like "
            "tuning forks. The organic substrate beneath them is spongy and "
            "wet, yielding under your weight. Touching a shard sends a tingle "
            "up your arm that takes minutes to fade."
        ),
        ambient_sounds=[
            "The daughter crystals pulse with a soft chiming, each one slightly out of phase with the others.",
            "The organic substrate squelches wetly underfoot as you move.",
            "A low harmonic resonance builds as you stand still, as if the crystals are responding to your presence.",
        ],
        exits={
            'north': Exit(
                direction='north',
                destination='heart_of_garden',
                description="You retreat toward the Garden's heart."
            ),
        },
        items=[
            "daughter_crystals",       # Major discovery - Seed reproduction
            "crystal_shard_sample",    # Takeable - dangerous but valuable
            "organic_substrate",       # Scenery
            "germination_equipment",   # Scenery - original purpose
            "spore_density_reader",    # Interactive - shows contamination
        ],
        flags=["contaminated"],
        danger_level=4,
        on_enter="event_discover_nursery",
    )
    world.add_room(seed_nursery)

    garden_root_network = Room(
        id="garden_root_network",
        name="Root Network",
        deck="Deck G - Cargo",
        description=(
            "Below the hydroponics bay, the Garden's roots have penetrated "
            "through the deck plating, splitting metal and worming through "
            "cable channels to create an organic tunnel system. The roots and "
            "tendrils intertwine overhead and along the walls, forming a living "
            "corridor of pale, bioluminescent tissue. The light they emit is "
            "soft green-gold, pulsing in waves that travel along the root "
            "network like signals through a nervous system.\n\n"
            "You can hear the heartbeat of the Garden's nexus above you - a "
            "deep, rhythmic throb that travels through the roots and into the "
            "deck plating beneath your feet. It is the sound of something vast "
            "and alive and aware. The roots respond to your presence, curling "
            "slightly away from your footsteps, then reaching back toward you "
            "after you pass.\n\n"
            "The tunnel slopes downward, connecting the hydroponics bay above "
            "to the water processing facilities below. This is how the infection "
            "reached the water supply - through root systems that grew faster "
            "and more purposefully than any natural plant."
        ),
        smell_text=(
            "The air smells of wet earth and living roots, the deep primal "
            "smell of a forest floor. Beneath it is the now-familiar alien "
            "sweetness, and something else - the mineral tang of processed water."
        ),
        touch_text=(
            "The roots are warm and smooth, covered in a thin layer of moisture "
            "that glows faintly where your fingers press. They pulse under your "
            "touch, recoiling slightly before relaxing. The deck plating is "
            "buckled and split where the roots forced through."
        ),
        ambient_sounds=[
            "The Garden's heartbeat throbs through the root network - deep, slow, patient.",
            "Bioluminescent fluid drips from root junctions, each drop a tiny spark of light.",
            "The roots shift and creak as they grow, the sound of a living architecture rearranging itself.",
        ],
        exits={
            'up': Exit(
                direction='up',
                destination='hydroponics_main',
                description="You climb back up through the root-choked opening into the bay."
            ),
            'down': Exit(
                direction='down',
                destination='water_processing',
                description="You follow the root tunnel down to water processing."
            ),
        },
        items=[
            "bioluminescent_roots",    # Scenery - beautiful and alien
            "root_junction_node",      # Interactive - Seed communication
            "split_deck_plating",      # Scenery
            "root_fluid_sample",       # Takeable - scientific value
        ],
        flags=["contaminated"],
        danger_level=2,
    )
    world.add_room(garden_root_network)

    cargo_office = Room(
        id="cargo_office",
        name="Cargo Master's Office",
        deck="Deck G - Cargo",
        description=(
            "A small, cluttered office that smells of coffee and bureaucracy. "
            "Shipping manifests cover every horizontal surface - the desk, the "
            "chair, the floor, pinned to the walls in overlapping layers. Cargo "
            "Master Webb was clearly a paper-and-ink person in a digital age. "
            "Post-it notes in precise handwriting annotate everything.\n\n"
            "A personal audio log recorder sits on the desk, its red light still "
            "blinking. Webb's final recordings reveal the chain of custody for "
            "the Seed specimens - who brought them aboard, who signed for them, "
            "who authorized their transfer to the exobiology lab. The trail of "
            "responsibility leads places no one expected.\n\n"
            "On the desk, beside the recorder, sits a half-eaten sandwich on a "
            "paper plate. The bread is still soft. The lettuce has not wilted. "
            "It should have gone stale weeks ago. You choose not to think about "
            "why it hasn't."
        ),
        smell_text=(
            "Stale coffee and paper - the universal smell of an office. "
            "Underneath it, the faintest trace of the Garden's sweet smell "
            "drifts in from the cargo bay. The sandwich smells fresh, which "
            "is wrong."
        ),
        touch_text=(
            "The manifests are real paper - textured, heavy stock. Webb liked "
            "to write with a fountain pen, and the ink is slightly raised on "
            "the page. The sandwich is disturbingly warm and fresh to the touch."
        ),
        ambient_sounds=[
            "The audio log recorder clicks softly as its tape mechanism idles.",
            "Paper rustles in the air current from the ventilation system.",
            "A coffee mug on the desk vibrates faintly with the ship's engine resonance.",
        ],
        exits={
            'east': Exit(
                direction='east',
                destination='cargo_bay_main',
                description="You return to the main cargo bay."
            ),
        },
        items=[
            "webb_audio_log",          # Major readable - chain of custody
            "shipping_manifests",      # Readable - delivery records
            "fresh_sandwich",          # Disturbing scenery
            "cargo_office_terminal",   # Interactive
            "webb_coffee_mug",         # Scenery
            "fountain_pen",            # Takeable
        ],
    )
    world.add_room(cargo_office)

    cold_storage = Room(
        id="cold_storage",
        name="Cold Storage Unit",
        deck="Deck G - Cargo",
        description=(
            "An industrial refrigeration unit the size of a small warehouse, "
            "its heavy door sealing with a hiss as it closes behind you. The "
            "temperature plummets. Your breath crystallizes. Racks of labeled "
            "containers stretch in orderly rows, each one maintaining biological "
            "specimens at carefully controlled sub-zero temperatures.\n\n"
            "Most containers are intact, their contents preserved in perfect "
            "stasis. But a cluster near the back shows crystalline growth on "
            "their exterior - familiar silver-white formations creeping across "
            "the metal like frost on a window. The infection reached even here, "
            "into the coldest room on the ship. The containers in this section "
            "are labeled 'KEPLER ANOMALY - BIOLOGICAL SAMPLES.'\n\n"
            "One container, smaller than the others, bears a medical priority "
            "tag and Dr. Lin's signature. Inside: tissue samples from the first "
            "infected crew members, preserved before the Seed had fully "
            "integrated with their biology. These samples are critical. They "
            "may be the key component for synthesizing a cure."
        ),
        smell_text=(
            "The air is sharp and sterile, stripped clean by the extreme cold. "
            "When you breathe through your mouth, you can taste frost and the "
            "faintest chemical tang of preservation fluid."
        ),
        touch_text=(
            "Everything is brutally cold. The container surfaces burn your "
            "fingers on contact. The crystalline growth on the infected "
            "containers is surprisingly warm by comparison - the Seed generates "
            "its own heat, even here."
        ),
        ambient_sounds=[
            "The refrigeration unit drones with a deep, constant hum that numbs your teeth.",
            "Ice crystals crack and reform on the ceiling, a soft tinkling in the extreme cold.",
            "Your joints creak as the cold seeps into your bones.",
        ],
        exits={
            'west': Exit(
                direction='west',
                destination='cargo_bay_main',
                description="You return to the warmer air of the cargo bay."
            ),
        },
        items=[
            "tissue_sample_container",  # Critical puzzle item - cure component
            "crystalline_containers",   # Scenery - infection even here
            "biological_specimens",     # Scenery
            "dr_lin_priority_tag",      # Readable
            "preservation_racks",       # Scenery
            "temperature_controls",     # Interactive
        ],
        temperature=-10,
    )
    world.add_room(cold_storage)

    chrysalis_chamber = Room(
        id="chrysalis_chamber",
        name="The Chrysalis Chamber",
        deck="Deck G - Cargo",
        description=(
            "The deepest room in the Garden. You push through a curtain of "
            "crystalline tendrils into a space that was once a storage bay and "
            "is now a cathedral of transformation. The walls, floor, and ceiling "
            "are covered in a web of interlocking crystal and organic tissue, "
            "glowing with a steady silver-white light.\n\n"
            "In the center, suspended in the web like an insect in amber, hangs "
            "a crew member. They are mid-transformation - the left half of their "
            "body is recognizably human, skin and muscle and bone. The right "
            "half is something else entirely: crystalline lattice where bone "
            "should be, silver-threaded tissue where muscle was, an eye that "
            "glows with the same light as the Seed. Their mouth moves silently. "
            "Their human eye tracks you as you enter.\n\n"
            "This is where the Seed transforms its hosts into something new. "
            "Not death. Not life. Something between, or beyond. It is horrifying "
            "and beautiful in equal measure, and the half-transformed crew member "
            "can speak if you approach. They have things to tell you about what "
            "it feels like to become part of the Song."
        ),
        smell_text=(
            "The air is saturated with the Seed's scent - sweet, metallic, "
            "overwhelming. Beneath it, you can smell human sweat and the "
            "copper tang of exposed tissue. The smell of metamorphosis."
        ),
        touch_text=(
            "The crystalline web vibrates under your touch like a plucked "
            "string. The organic tissue between the crystals is warm and "
            "alive, pulsing with a rhythm that matches the Garden's heartbeat. "
            "Getting too close to the suspended figure makes your skin tingle."
        ),
        ambient_sounds=[
            "The half-transformed crew member whispers - sometimes words, sometimes just breath.",
            "Crystal structures chime softly as they grow, a sound like wind chimes in slow motion.",
            "The web thrums with a deep resonance, as if the entire room is a living instrument.",
        ],
        exits={
            'west': Exit(
                direction='west',
                destination='heart_of_garden',
                description="You retreat from the chrysalis chamber."
            ),
        },
        items=[
            "chrysalis_figure",        # NPC-like - can be spoken to
            "crystalline_web",         # Scenery
            "transformation_tissue",   # Scenery - scientific interest
            "chrysalis_recorder",      # Readable - someone was documenting this
        ],
        npcs=["chrysalis_crew"],       # The half-transformed person
        flags=["contaminated"],
        danger_level=4,
        on_enter="event_chrysalis_encounter",
    )
    world.add_room(chrysalis_chamber)

    water_treatment_secondary = Room(
        id="water_treatment_secondary",
        name="Secondary Water Treatment",
        deck="Deck G - Cargo",
        description=(
            "A secondary water treatment facility, smaller than the main "
            "processing plant but critically important: this system operates "
            "on an independent circuit, separate from the contaminated primary "
            "water supply. The filtration units here are clean. The water in "
            "the tanks is clear. Whoever designed the ship's redundancy systems "
            "may have saved the surviving crew's lives.\n\n"
            "A bank of chemical storage lockers lines one wall, containing "
            "purification agents, pH balancers, and - crucially - several "
            "reagents that could be useful in synthesizing biological compounds. "
            "Dr. Lin's research notes, referenced in her journal, mention this "
            "facility as a potential clean-room for the cure synthesis process.\n\n"
            "A small dispensing station offers clean water. After everything "
            "you've seen and breathed since waking up, a glass of uncontaminated "
            "water feels like the most precious thing on this ship."
        ),
        smell_text=(
            "Clean water and mild chlorine - the most normal, reassuring "
            "smell you have encountered since waking from cryo. After the "
            "Garden's cloying sweetness, it is almost intoxicating."
        ),
        touch_text=(
            "The filtration equipment is cool and dry, well-maintained. The "
            "water from the dispensing station is cold and clean against your "
            "skin. The chemical storage lockers are smooth metal, properly "
            "sealed and labeled."
        ),
        ambient_sounds=[
            "Water filters hum with a clean, steady rhythm - the sound of a system working as designed.",
            "A dispensing valve drips occasionally, each drop a small reassurance of normalcy.",
            "The chemical storage lockers click as their temperature regulation cycles.",
        ],
        exits={
            'east': Exit(
                direction='east',
                destination='cargo_access',
                description="You return to the cargo access tunnel."
            ),
        },
        items=[
            "clean_water_dispenser",   # Consumable - reduces infection
            "chemical_storage_locker", # Container - cure components
            "independent_filtration",  # Scenery
            "cure_reagents",           # Critical puzzle item
            "lin_research_reference",  # Readable
            "water_quality_readout",   # Interactive
        ],
    )
    world.add_room(water_treatment_secondary)

    # ═══════════════════════════════════════════════════════════════════
    # DECK J - PROPULSION (deep ship)
    # ═══════════════════════════════════════════════════════════════════

    propulsion_access = Room(
        id="propulsion_access",
        name="Propulsion Deck Access",
        deck="Deck J - Propulsion",
        description=(
            "A cramped maintenance area between the cryogenics deck and the "
            "main propulsion systems below. The walls vibrate with the low, "
            "constant hum of the drive plasma. You can feel it in your bones.\n\n"
            "A heavy blast door leads forward to the main engine room. It is "
            "currently locked by emergency override - the system believes the "
            "area is compromised and has sealed it for crew safety. You can "
            "see the override keypad beside the door."
        ),
        exits={
            'up': Exit(
                direction='up',
                destination='deck_i_hub',
                description="You climb back up to the cryo deck hub."
            ),
            'north': Exit(
                direction='north',
                destination='main_engine_room',
                locked=True,
                lock_message="Emergency lockdown. The override keypad requires a 6-digit code.",
                required_flag="engine_room_unlocked"
            ),
        },
        items=[
            "engine_blast_door",
            "emergency_override_keypad",  # Puzzle
            "propulsion_warning_sign",
        ],
        smell_text="Hot plasma exhaust and the acrid stink of superheated ceramic shielding bleed through the blast door seals, making the cramped space taste like burnt metal and lightning.",
        touch_text="The walls vibrate so intensely that your vision blurs when you lean against them, and the blast door is warm to the touch despite its massive thickness.",
        ambient_sounds=[
            "The drive plasma rumbles beyond the blast door with a deep, chest-compressing throb that never stops.",
            "The emergency override keypad clicks and beeps softly, cycling through a lockout sequence.",
            "Metal stress groans echo through the maintenance area as the propulsion deck absorbs the drive's constant vibration.",
        ],
    )
    world.add_room(propulsion_access)

    main_engine_room = Room(
        id="main_engine_room",
        name="Main Engine Room",
        deck="Deck J - Propulsion",
        description=(
            "The main engine room is the single loudest space on the Prometheus. "
            "The roar of the plasma drive is deafening. Giant pistons and "
            "thrust regulators hammer in rhythmic unison. Heat shimmers the "
            "air. This is where the ship's power becomes motion.\n\n"
            "The drive is still running - at idle, waiting for direction. The "
            "navigation system has been receiving corrupted commands, unable "
            "to determine a proper course. Without a clear directive, the "
            "ship is drifting.\n\n"
            "A master control terminal here can issue direct thrust commands, "
            "bypassing the damaged nav system. If you can input the correct "
            "course correction, you can move the ship away from GRB-7734.\n\n"
            "This is where the ship gets saved. Or doomed. Depending on you."
        ),
        exits={
            'south': Exit(
                direction='south',
                destination='propulsion_access',
                description="You back out of the engine room."
            ),
        },
        items=[
            "master_drive_control",  # Climax puzzle
            "thrust_regulators",
            "plasma_drive_core",
            "heat_shield_controls",
            "navigation_override",
        ],
        smell_text="The air is thick with ionized plasma and superheated lubricant, so hot and metallic it scorches the back of your throat, overwhelming every other sense.",
        touch_text="The floor shakes with enough force to rattle your teeth, and the master control terminal vibrates under your fingers like a living thing straining at a leash.",
        ambient_sounds=[
            "The plasma drive roars with a sound that is less heard than endured, a wall of noise that flattens thought.",
            "Thrust regulators hammer in rhythmic unison, each stroke sending a shockwave through the deck plating.",
            "Beneath the mechanical thunder, the navigation system emits corrupted command tones - broken digital shrieks that sound almost like screaming.",
        ],
        on_enter="event_first_engine_room",
    )
    world.add_room(main_engine_room)
