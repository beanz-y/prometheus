"""
Act 1 Rooms - Deck I (Cryogenics) and initial exploration.

The player awakens in the cryo bay. Early rooms establish the tone,
introduce core mechanics, and set up the central mystery.
"""

from engine.room import Room, Exit


def build_act1_rooms(world):
    """Create all Act 1 rooms and add them to the world."""

    # ═══════════════════════════════════════════════════════════════════
    # DECK I - CRYOGENICS
    # ═══════════════════════════════════════════════════════════════════

    cryo_bay = Room(
        id="cryo_bay",
        name="Cryogenics Bay - Pod 23",
        deck="Deck I - Cryogenics",
        description=(
            "A vast cylindrical chamber that echoes with the sound of your own "
            "breathing. Sixty cryogenic pods line the curved walls in four "
            "concentric rings, their glass faces rimed with frost. Most are "
            "dark. Yours - Pod 23 - is the only one emitting its pale blue light.\n\n"
            "The air is freezing. Your lungs burn with each breath. Cryo-fluid "
            "drips from your hair and pools on the deck plate at your feet. "
            "Your legs tremble when you put weight on them. How long were you "
            "under? The chronometer on the pod reads eighteen months and change, "
            "but that can't be right.\n\n"
            "Emergency lighting strobes red in slow, sickening pulses. A panel "
            "across the room is sparking. The central monitoring station sits "
            "dark and abandoned. A diagnostic terminal blinks green beside your "
            "pod - the only living thing in here besides you.\n\n"
            "Set into the wall beside Pod 23, a small personal storage locker "
            "bears your name. Above the east door, a red light blinks: "
            "DECONTAMINATION IN PROGRESS."
        ),
        first_visit_text=(
            "You come awake in pieces.\n\n"
            "First the light. A searing blue that stabs at your eyes even through "
            "closed lids. Then sound - a hissing, rushing sound, and somewhere "
            "behind it, a rhythmic thump like a wounded heart.\n\n"
            "Then cold. God, the cold.\n\n"
            "Your lungs try to scream but there's fluid in them. You cough, "
            "retch, spit. The pod lid lifts. You fall forward onto your hands "
            "and knees on freezing deck plating, naked and shivering, your "
            "mind a white blank of terror and confusion."
        ),
        smell_text="The air reeks of ammonia and copper-tinged cryo-fluid, sharp enough to make your eyes water, underlaid by the sterile chill of recycled atmosphere.",
        touch_text="The deck plating is slick with condensation and freezing cold beneath your bare feet, each step sending needles of ice through your soles.",
        ambient_sounds=[
            "Somewhere in the distance, you hear a long, low groan of metal - the ship settling.",
            "A slow, rhythmic dripping echoes from the far wall.",
            "The atmospheric pumps whine and cycle, whine and cycle.",
            "Behind the hum of the cryo-pods, you think you hear... whispering? No. Just the air recyclers.",
        ],
        exits={
            'west': Exit(
                direction='west',
                destination='cryo_storage',
                description="You step past rows of frozen pods, your bare feet leaving prints in the ice."
            ),
            'north': Exit(
                direction='north',
                destination='cryo_control',
                description="You cross to the control station."
            ),
            'east': Exit(
                direction='east',
                destination='cryo_corridor',
                locked=True,
                lock_message="The door to the main corridor is sealed. A red light blinks above it: DECONTAMINATION IN PROGRESS. A green override button is set into the wall beside it.",
                required_flag="cryo_exit_unlocked"
            ),
        },
        items=[
            "cryo_jumpsuit",    # Clothing
            "personal_locker",  # Scenery container with items
            "diagnostic_terminal",  # Reveals backstory
            "emergency_kit",    # Health items
            "pod_23",          # Scenery
            "sparking_panel",  # Scenery hint
            "green_override_button",  # Puzzle component
            "cryo_release_key",  # Key item
        ],
        on_look="event_first_look_cryo",
    )
    world.add_room(cryo_bay)

    cryo_storage = Room(
        id="cryo_storage",
        name="Cryogenic Storage",
        deck="Deck I - Cryogenics",
        description=(
            "A long hallway of frozen caskets. Pods stretch into the dim distance "
            "in two facing rows, their occupants' faces just visible through "
            "fogged glass. Most of the diagnostic lights are red. A few are dark. "
            "None are green.\n\n"
            "Your breath plumes in the freezing air. You see a woman in Pod 47, "
            "peaceful in cryo-sleep - except her pod's vitals flat-line across "
            "the display. She died in her sleep. So did the man beside her. "
            "And the next. And the next.\n\n"
            "You realize, slowly, that you are walking past a cemetery. Sixty "
            "people who went to sleep expecting a quiet voyage, and never woke up.\n\n"
            "One pod stands out from the rest. Pod 12, halfway down the row, has "
            "its front glass smashed outward - spider-webbed cracks radiating from "
            "an impact point inside. The pod is empty. Whoever was in there didn't "
            "just die. They got OUT. A trail of dark smears leads north from the "
            "broken pod."
        ),
        smell_text="A faint, sickly-sweet odor of biological decay seeps from the failing pods, mixing with the sharp bite of leaking cryo-fluid and frost-rimed metal.",
        touch_text="The pod glass is fogged and ice-cold under your fingertips, and when you pull your hand away, the condensation clings to your skin like something reluctant to let go.",
        ambient_sounds=[
            "The hum of failing cryo systems creates a low, mournful drone.",
            "You hear a soft thump as something inside one of the pods settles.",
            "Somewhere down the corridor, an alarm beeps faintly, then falls silent.",
        ],
        exits={
            'east': Exit(
                direction='east',
                destination='cryo_bay',
                description="You return to the central bay."
            ),
            'south': Exit(
                direction='south',
                destination='cryo_maintenance',
                hidden=True,
                description="You squeeze through the maintenance access hatch."
            ),
            'north': Exit(
                direction='north',
                destination='cryo_pod_12_interior',
                description="You climb through the shattered glass of Pod 12."
            ),
            'west': Exit(
                direction='west',
                destination='cryo_recycling',
                description="You follow a service corridor to the cryo-fluid recycling room."
            ),
        },
        items=[
            "pod_47",           # Scenery - dead crew member
            "crew_manifest",    # Readable
            "pod_12_damaged",   # Important scenery
        ],
    )
    world.add_room(cryo_storage)

    cryo_control = Room(
        id="cryo_control",
        name="Cryogenic Control Room",
        deck="Deck I - Cryogenics",
        description=(
            "A cramped control station dominated by a bank of monitors, most "
            "of them displaying static or error messages. The primary interface "
            "is cracked, a spider-web of fractures radiating from a single bullet "
            "hole in the center of the screen.\n\n"
            "Whoever was on duty here is no longer at their post, but they left "
            "in a hurry. A coffee cup sits beside the keyboard, its contents "
            "frozen solid. A tablet lies face-down on the floor. A chair has "
            "been shoved backward hard enough to dent the wall.\n\n"
            "Above the main console, a holographic display flickers, showing "
            "the cryo-pod status grid. Of the sixty pods shown, fifty-eight "
            "are red. One is dark. One - yours - is green."
        ),
        smell_text="Frozen coffee and burnt electronics mingle in the frigid air, along with the faint metallic scent of the bullet that punched through the main screen.",
        touch_text="The cracked console screen is sharp-edged around the bullet hole, and the keyboard keys are stiff with frost, resisting your fingers.",
        exits={
            'south': Exit(
                direction='south',
                destination='cryo_bay',
                description="You return to the cryo bay proper."
            ),
            'east': Exit(
                direction='east',
                destination='cryo_medical',
                description="You enter the small emergency medical bay."
            ),
            'west': Exit(
                direction='west',
                destination='pod_monitoring_alcove',
                hidden=True,
                description="You pry open a loose wall panel and squeeze into a hidden alcove."
            ),
        },
        items=[
            "bullet_hole_console",   # Scenery with clue
            "duty_officers_tablet",  # Readable
            "cryo_status_display",   # Scenery
            "frozen_coffee_cup",     # Scenery - sanity detail
            "control_chair",         # Scenery
        ],
        ambient_sounds=[
            "The holographic status display emits a soft, irregular crackle as it flickers between data frames.",
            "Static hisses from the bullet-damaged console, punctuated by sharp pops of shorting circuits.",
            "The duty chair creaks faintly, rocking on its base as if someone just stood up.",
        ],
    )
    world.add_room(cryo_control)

    cryo_medical = Room(
        id="cryo_medical",
        name="Emergency Medical Station",
        deck="Deck I - Cryogenics",
        description=(
            "A small medical bay for handling cryo-related emergencies - shock, "
            "pulmonary distress, neural misfiring. A single examination table "
            "sits in the center of the room, its restraints hanging loose. A "
            "cabinet of medical supplies has been ransacked, drawers pulled out "
            "and contents scattered. Whoever raided this place was looking for "
            "something specific.\n\n"
            "A medical scanner in the corner still functions, blinking patiently. "
            "A biohazard waste bin sits beside it, full. A personal datapad lies "
            "forgotten on the counter, screen dark but battery indicator still "
            "green."
        ),
        smell_text="Rubbing alcohol and latex gloves dominate the air, but the overflowing biohazard bin adds a sour, biological note that turns your stomach.",
        touch_text="The examination table's restraints are cold leather, worn smooth by use, and the scattered medical supplies crunch like broken promises underfoot.",
        exits={
            'west': Exit(
                direction='west',
                destination='cryo_control',
                description="You return to the control room."
            ),
        },
        items=[
            "medical_cabinet",      # Container, ransacked
            "examination_table",    # Scenery
            "medical_scanner",      # Usable - checks infection
            "dr_lin_datapad",      # Important readable!
            "biohazard_bin",       # Scenery with contents
            "stimpack",            # Healing item
            "sedative_syringe",    # Puzzle item
        ],
        ambient_sounds=[
            "The medical scanner beeps in a slow, patient rhythm, waiting for a patient who will never come.",
            "Scattered pill bottles roll across the floor with each subtle shift of the ship's gravity.",
            "The biohazard bin's lid creaks open an inch, then settles closed, as if breathing.",
        ],
    )
    world.add_room(cryo_medical)

    cryo_maintenance = Room(
        id="cryo_maintenance",
        name="Maintenance Crawlspace",
        deck="Deck I - Cryogenics",
        description=(
            "A cramped maintenance tunnel runs beneath the cryogenics deck, "
            "thick with cables and piping. Red emergency lights flicker overhead. "
            "The air tastes of ozone and coolant.\n\n"
            "Someone has been down here recently. A worker's tool belt lies "
            "discarded on a junction box. A trail of dark smears leads deeper "
            "into the tunnel system. You don't want to look too closely at "
            "what those smears might be.\n\n"
            "The tunnel branches here - one route going down toward the propulsion "
            "deck, another climbing toward Deck H and the AI core. A rust-encrusted "
            "ladder bolted to the bulkhead leads up."
        ),
        dark=False,  # Has emergency lighting
        exits={
            'north': Exit(
                direction='north',
                destination='cryo_storage',
                description="You climb back through the access hatch."
            ),
            'up': Exit(
                direction='up',
                destination='deck_h_junction',
                description="You climb the maintenance ladder upward.",
                locked=True,
                lock_message="The ladder leads up into a darkness you have no means of navigating yet. You need a light source.",
                required_flag="has_flashlight"
            ),
            'down': Exit(
                direction='down',
                destination='propulsion_access',
                hidden=True,
                locked=True,
                lock_message="A security gate blocks the way down."
            ),
            'east': Exit(
                direction='east',
                destination='vent_network_i',
                hidden=True,
                description="You squeeze into a narrow ventilation shaft."
            ),
        },
        items=[
            "tool_belt",       # Container with tools
            "dark_smear",      # Scenery - disturbing clue
            "maintenance_ladder",  # Scenery
            "flashlight",      # Important - unlocks dark areas
            "wrench",          # Tool/weapon
            "junction_box",    # Scenery
        ],
        smell_text="Ozone and hot coolant dominate the cramped tunnel, mixed with the rusty tang of old blood from the dark smears along the floor.",
        touch_text="The cables and pipes press against you from all sides, some vibrating with fluid flow, others hot enough to flinch away from.",
        ambient_sounds=[
            "Pipes clank and gurgle somewhere in the darkness above you.",
            "You hear a distant thump, like something heavy being dropped.",
            "A faint electrical buzzing seems to come from everywhere and nowhere.",
        ],
    )
    world.add_room(cryo_maintenance)

    # ═══════════════════════════════════════════════════════════════════
    # DECK I - CRYOGENICS (continued) - Deeper exploration
    # ═══════════════════════════════════════════════════════════════════

    cryo_pod_12_interior = Room(
        id="cryo_pod_12_interior",
        name="Interior of Cryo Pod 12",
        deck="Deck I - Cryogenics",
        description=(
            "You climb through the shattered glass of Pod 12 into a space barely "
            "large enough for a person to lie flat. The inside of the pod is a "
            "testament to sheer animal panic. Deep gouges score the tempered glass "
            "of the lid - not cuts, but claw marks, ragged and frantic, torn by "
            "fingernails that must have split and bled. The padding is shredded. "
            "Cryo-fluid residue has dried into a tacky amber film.\n\n"
            "A personal datapad is wedged into the gap between the pod's headrest "
            "and the wall, as if hidden there deliberately. Its screen is cracked "
            "but functional. The last entry is timestamped six hours after the "
            "general alarm sounded - Ensign Kirilov's final rational thoughts "
            "before whatever was happening to them completed its work.\n\n"
            "Silver-grey residue lines the cracks in the glass, tracing the fracture "
            "patterns like veins. You have seen this residue before. It is the "
            "signature of the Seed."
        ),
        smell_text=(
            "The air inside the pod reeks of stale cryo-fluid and something "
            "metallic - copper, maybe, or old blood. Underneath it all is a "
            "faint sweetness that makes your stomach turn."
        ),
        touch_text=(
            "The claw marks in the glass are rough under your fingertips, jagged "
            "and sharp enough to cut. The dried residue is tacky and warm to the "
            "touch, as if the pod still remembers its occupant's body heat."
        ),
        ambient_sounds=[
            "The broken pod emits a faint, irregular clicking - a relay trying to restart.",
            "Cryo-fluid drips somewhere beneath the pod's base, slow and hollow.",
            "You hear your own breathing, amplified by the pod's curved interior.",
        ],
        exits={
            'south': Exit(
                direction='south',
                destination='cryo_storage',
                description="You carefully climb back out through the shattered glass."
            ),
        },
        items=[
            "kirilov_datapad",       # Major readable - last rational thoughts
            "claw_marks_glass",      # Scenery - disturbing
            "dried_cryo_residue",    # Scenery
            "silver_grey_residue",   # Clue - Seed signature
            "shredded_padding",      # Scenery
            "pod_12_headrest",       # Scenery
        ],
        on_enter="event_discover_kirilov",
    )
    world.add_room(cryo_pod_12_interior)

    cryo_recycling = Room(
        id="cryo_recycling",
        name="Cryo-Fluid Recycling Room",
        deck="Deck I - Cryogenics",
        description=(
            "A low-ceilinged industrial space dominated by three massive recycling "
            "tanks, each one taller than a person and filled with the pale blue "
            "cryo-fluid that keeps the pods operational. Pumps chug and wheeze "
            "along the far wall, pushing fluid through a web of pipes that "
            "disappear into the ceiling. Valve wheels and pressure gauges line "
            "every surface.\n\n"
            "The middle tank has a hairline crack running from its base to about "
            "waist height. Through the crack, you can see something that should "
            "not be there: silver threads, fine as spider silk, growing inside "
            "the fluid. They catch the emergency lighting and shimmer. The "
            "infection found its way into the cryo-fluid supply. Everyone who "
            "was in cryo was exposed.\n\n"
            "A maintenance terminal beside the cracked tank still functions. Its "
            "screen displays fluid composition data - and the anomalous readings "
            "that someone flagged but never acted upon."
        ),
        smell_text=(
            "The room smells powerfully of ammonia and copper, the sharp chemical "
            "tang of cryo-fluid cycling through its recycling process. Beneath "
            "it is a faint organic sweetness that does not belong here."
        ),
        touch_text=(
            "The tanks are cold to the touch, beaded with condensation. The valve "
            "wheels are slippery with moisture. The cracked tank vibrates faintly "
            "under your palm, as if something inside is moving."
        ),
        ambient_sounds=[
            "The pumps chug in a slow, asthmatic rhythm - ka-chunk, ka-chunk, ka-chunk.",
            "Fluid gurgles through pipes overhead, a sound like a living digestive system.",
            "The cracked tank emits a high, thin whine of pressure slowly escaping.",
        ],
        exits={
            'east': Exit(
                direction='east',
                destination='cryo_storage',
                description="You return to the cryo storage corridor."
            ),
        },
        items=[
            "recycling_tank_cracked",   # Major clue - infection vector
            "silver_threads_fluid",     # Scenery - Seed in fluid
            "recycling_pumps",          # Scenery
            "maintenance_terminal_cryo", # Readable - flagged anomalies
            "valve_wheels",             # Interactive
            "fluid_composition_data",   # Readable
        ],
        temperature=5,
        on_enter="event_discover_cryo_infection",
    )
    world.add_room(cryo_recycling)

    pod_monitoring_alcove = Room(
        id="pod_monitoring_alcove",
        name="Hidden Monitoring Alcove",
        deck="Deck I - Cryogenics",
        description=(
            "Behind the cryo monitoring station, concealed by a panel that was "
            "never meant to be a door, someone carved out a hiding place. The "
            "alcove is barely two meters square, a crawlspace between the control "
            "room's wall and the hull. It smells of sweat and desperation.\n\n"
            "A bedroll of thermal blankets has been flattened by weeks of use. "
            "Empty ration wrappers are stacked neatly in one corner - someone "
            "methodical, someone holding on to routine as the world ended around "
            "them. A personal journal lies open on the bedroll, its pages filled "
            "with increasingly erratic handwriting.\n\n"
            "On the wall, scratched into the bare metal with a sharp object, "
            "someone has written: 'DAY 5 - THEY STOPPED KNOCKING.' Below it, "
            "in smaller letters: 'DAY 8 - I CAN HEAR THEM SINGING.' And below "
            "that, barely legible: 'DAY 12 - THE SONG IS BEAUTIFUL.'"
        ),
        smell_text=(
            "The close air is thick with the smell of unwashed human - sweat, "
            "stale breath, the sour tang of fear metabolized into body chemistry. "
            "It is the smell of someone who lived in terror for weeks."
        ),
        touch_text=(
            "The thermal blankets are thin and worn smooth by use. The wall "
            "graffiti is rough under your fingers, carved deep into the metal "
            "by someone with trembling hands and absolute determination."
        ),
        ambient_sounds=[
            "The wall behind you conducts sound from the control room - faint electronic hums.",
            "Your own heartbeat seems loud in this tiny space.",
            "A faint scratching comes from somewhere inside the wall. Rats? There are no rats on a starship.",
        ],
        exits={
            'east': Exit(
                direction='east',
                destination='cryo_control',
                description="You squeeze back through the hidden panel into the control room."
            ),
        },
        items=[
            "survivor_journal",        # Major readable - descent into madness
            "thermal_bedroll",         # Scenery
            "ration_wrapper_stack",    # Scenery - methodical person
            "wall_graffiti_days",      # Scenery - chilling timeline
            "hidden_panel_door",       # Scenery
        ],
    )
    world.add_room(pod_monitoring_alcove)

    emergency_airlock_i = Room(
        id="emergency_airlock_i",
        name="Emergency Airlock - Deck I",
        deck="Deck I - Cryogenics",
        description=(
            "A small emergency airlock set into the hull of Deck I. The inner "
            "door responds to your touch, grinding open on damaged servos. The "
            "outer door is jammed in a partially open position - you can see a "
            "sliver of star-speckled void through the gap, and the air is thin "
            "here. Your ears pop. Each breath takes effort.\n\n"
            "Through the viewport beside the outer door, the hull of the Prometheus "
            "curves away in both directions, a vast grey expanse pockmarked with "
            "sensor arrays and maintenance hatches. Beyond the hull, the stars "
            "wheel slowly as the ship tumbles in its drift. You can see the brown "
            "dwarf from here too - a sullen dark ember eating the constellations.\n\n"
            "An EVA equipment rack is bolted to the wall. Most of the suits are "
            "missing, but a spare helmet sits in its cradle, visor scratched but "
            "intact. An emergency oxygen canister is mag-locked to the floor "
            "beside the outer door."
        ),
        smell_text=(
            "The air is thin and cold and tastes of metal - the tang of hard "
            "vacuum bleeding through the jammed outer door. There is a faint "
            "chemical smell from the emergency sealant that someone sprayed "
            "around the door frame."
        ),
        touch_text=(
            "Everything is cold. The walls, the floor, the equipment rack - all "
            "of it radiates the deep chill of space just centimeters away. The "
            "viewport glass is ice-cold under your palm."
        ),
        ambient_sounds=[
            "Air whistles thinly through the jammed outer door, a constant eerie keening.",
            "The hull groans and pops as thermal stresses shift across its surface.",
            "Your own breathing sounds labored and loud in the thin atmosphere.",
        ],
        exits={
            'north': Exit(
                direction='north',
                destination='deck_i_hub',
                description="You retreat from the airlock into the pressurized hub."
            ),
        },
        items=[
            "spare_eva_helmet",        # Equipment
            "emergency_oxygen_canister", # Consumable - restores oxygen
            "hull_viewport",           # Scenery - narrative moment
            "jammed_outer_door",       # Scenery
            "eva_equipment_rack",      # Scenery
            "emergency_sealant",       # Tool item
        ],
        oxygen_level=0.6,
        temperature=-5,
        danger_level=1,
    )
    world.add_room(emergency_airlock_i)

    escape_pod_bay_lower = Room(
        id="escape_pod_bay_lower",
        name="Lower Escape Pod Bay",
        deck="Deck I - Cryogenics",
        description=(
            "Below the shuttle bay, a secondary escape pod facility holds three "
            "berths arranged in a row along the hull. The room is utilitarian - "
            "bare metal, emergency lighting, launch rails recessed into the floor.\n\n"
            "Berth One is empty. The launch clamps are retracted, the pod gone, "
            "the launch tube open to a circular viewport of stars. Someone got "
            "out. A manifest on the wall shows the pod was launched fourteen days "
            "ago by Lieutenant Commander Osei - one passenger, destination: the "
            "nearest relay beacon, three light-years away.\n\n"
            "Berth Two is crushed. A structural beam has buckled and fallen across "
            "the pod, caving in its hull like a boot on an aluminum can. Cryo-fluid "
            "leaks from the wreckage in a slow blue trickle.\n\n"
            "Berth Three holds an intact pod, but its systems are dark. The launch "
            "console beside it displays a cascade of error messages. With the right "
            "knowledge, it might be repairable."
        ),
        smell_text=(
            "The air smells of hydraulic fluid and ozone, with the faint chemical "
            "sweetness of leaking cryo-fluid from the crushed pod. Cold metal "
            "and machine oil."
        ),
        touch_text=(
            "The launch rails are smooth and oiled. The crushed pod's hull is "
            "buckled and sharp-edged, dangerous to touch. The intact pod's "
            "exterior is smooth and cold, waiting."
        ),
        ambient_sounds=[
            "Wind whistles faintly through the open launch tube of Berth One, a ghostly moan.",
            "The crushed pod creaks as structural stress slowly deforms it further.",
            "Hydraulic fluid drips from the damaged beam in a steady, patient rhythm.",
        ],
        exits={
            'up': Exit(
                direction='up',
                destination='emergency_shuttle_bay',
                description="You climb back up to the shuttle bay."
            ),
        },
        items=[
            "launch_manifest_osei",    # Readable - who escaped
            "crushed_escape_pod",      # Scenery
            "intact_escape_pod",       # Interactive - possible repair puzzle
            "pod_launch_console",      # Interactive - error messages
            "structural_beam_fallen",  # Scenery
            "berth_one_viewport",      # Scenery
        ],
    )
    world.add_room(escape_pod_bay_lower)

    vent_network_i = Room(
        id="vent_network_i",
        name="Ventilation Shaft - Deck I",
        deck="Deck I - Cryogenics",
        description=(
            "You squeeze into a ventilation shaft barely wide enough for your "
            "shoulders. The metal walls press close on all sides. You can only "
            "move by crawling on your belly, elbows scraping against riveted "
            "seams, your breath bouncing back at you from the duct walls inches "
            "from your face.\n\n"
            "Air currents flow past you, carrying sounds from distant parts of "
            "the ship. You hear the hum of machinery. The whisper of atmospheric "
            "processors. And something else - something organic, like breathing "
            "that is not your own, or a pulse that is not your heartbeat. The "
            "sounds are directionless, impossible to locate.\n\n"
            "The shaft branches ahead. One route climbs upward through a vertical "
            "section toward Deck H. The other continues west, back toward the "
            "maintenance crawlspace. A thin coating of dust and biological residue "
            "lines the shaft walls. Your flashlight beam catches silver threads "
            "woven into the dust."
        ),
        dark=True,
        dark_description=(
            "You are in absolute darkness. The ventilation shaft presses against "
            "you on all sides. You can feel the air moving past your face, "
            "carrying sounds you cannot identify - whispers, pulses, the slow "
            "breathing of something vast. Without light, you cannot see which "
            "way the shaft branches. You need a flashlight to navigate."
        ),
        smell_text=(
            "The air in the shaft is stale and close, carrying the metallic "
            "taste of recycled atmosphere and a faint organic sweetness - spores, "
            "maybe, or the breath of the Garden carried through the ship's lungs."
        ),
        touch_text=(
            "The shaft walls are cold riveted metal, slick with condensation. "
            "The biological residue on the walls feels powdery and dry, like "
            "pollen. The silver threads are so fine they feel like cobwebs "
            "against your skin."
        ),
        ambient_sounds=[
            "Air currents carry distant whispers that almost resolve into words before dissolving.",
            "Something shifts in the ductwork ahead - a soft, wet sound, then silence.",
            "Your elbows scrape against metal, and the sound echoes endlessly through the shaft.",
        ],
        exits={
            'west': Exit(
                direction='west',
                destination='cryo_maintenance',
                description="You crawl back toward the maintenance area."
            ),
            'up': Exit(
                direction='up',
                destination='deck_h_junction',
                description="You haul yourself up the vertical section toward Deck H.",
                locked=True,
                lock_message="The vertical section is pitch black. You cannot navigate it without a light source.",
                required_flag="has_flashlight"
            ),
        },
        items=[
            "silver_threads_vent",     # Clue - Seed in ventilation
            "biological_residue",      # Scenery
            "vent_shaft_branch",       # Scenery
        ],
        danger_level=1,
    )
    world.add_room(vent_network_i)

    # ═══════════════════════════════════════════════════════════════════
    # DECK I TO DECK D (ascending) - The Medical Corridor
    # ═══════════════════════════════════════════════════════════════════

    cryo_corridor = Room(
        id="cryo_corridor",
        name="Cryo-Deck Main Corridor",
        deck="Deck I - Cryogenics",
        description=(
            "The main corridor of Deck I runs in a wide curve, following the "
            "shape of the ship's spine. Red warning lights strobe at regular "
            "intervals, painting the walls in intermittent crimson. The air "
            "here is warmer than the cryo bay - the life support has been "
            "working harder to keep this area habitable.\n\n"
            "Signs on the walls indicate the direction of various facilities: "
            "WEST leads back to the cryo bay where you woke up; EAST continues "
            "down the curve toward the Deck I elevator hub. A door to the "
            "SOUTH is labeled STORAGE - AUTHORIZED PERSONNEL ONLY.\n\n"
            "The floor is dry but dirty. Footprints. A few crumpled emergency "
            "ration wrappers. Signs that someone lived here, perhaps for days, "
            "before moving on."
        ),
        exits={
            'west': Exit(
                direction='west',
                destination='cryo_bay',
                description="You return to Cryo Bay."
            ),
            'east': Exit(
                direction='east',
                destination='deck_i_hub',
                description="You move down the corridor toward the elevator hub."
            ),
            'south': Exit(
                direction='south',
                destination='deck_i_storage',
                locked=True,
                lock_message="The storage room door is locked. A numeric keypad is mounted beside it.",
                key_id="deck_i_storage_key"
            ),
        },
        items=[
            "ration_wrappers",
            "bloody_footprints",
            "corridor_keypad",
        ],
        smell_text="Stale recycled air carries the ghost of burnt wiring and the faint chemical residue of emergency ration packaging.",
        touch_text="The corridor walls are warmer than the cryo bay but still cold enough to raise goosebumps, and the floor grits with dust and crumbled ration wrapper beneath your boots.",
        ambient_sounds=[
            "An automated voice repeats: 'Warning. Deck integrity compromised. Evacuation advised.'",
            "The lights above you buzz and flicker.",
            "You hear distant footsteps. When you listen closely, they stop.",
        ],
    )
    world.add_room(cryo_corridor)

    deck_i_hub = Room(
        id="deck_i_hub",
        name="Deck I Elevator Hub",
        deck="Deck I - Cryogenics",
        description=(
            "A circular junction with an elevator shaft at its center. The "
            "doors stand open, revealing a platform - though the descent and "
            "ascent panels are dark. Four corridors radiate from the hub. "
            "To the north, you see the medical corridor (marked with a green "
            "cross). South leads to propulsion access. West is the cryo deck "
            "you came from. East opens onto an emergency shuttle bay.\n\n"
            "A body lies in the elevator doorway, keeping the doors from closing."
        ),
        first_visit_text=(
            "As you approach the hub, the body registers first: a crew member "
            "in an engineering jumpsuit, sprawled half-inside the elevator. "
            "They're face down. Dried blood forms a dark halo around their head. "
            "A handheld tool - a plasma cutter - lies just beyond their reach.\n\n"
            "They were trying to escape. They didn't make it."
        ),
        smell_text="The iron-heavy stench of dried blood mingles with the ozone tang of the dead elevator shaft and the faint musk of a body left too long in recycled air.",
        touch_text="The elevator doors judder against the body whenever the mechanism tries to close, vibrating through the floor, and the air here moves in cold drafts from the open shaft above.",
        exits={
            'west': Exit(
                direction='west',
                destination='cryo_corridor',
                description="You return to the cryo deck corridor."
            ),
            'north': Exit(
                direction='north',
                destination='medical_corridor',
                description="You head into the medical corridor."
            ),
            'south': Exit(
                direction='south',
                destination='emergency_airlock_i',
                description="You head south toward the emergency airlock."
            ),
            'east': Exit(
                direction='east',
                destination='emergency_shuttle_bay',
                locked=True,
                lock_message="The shuttle bay doors are locked and will not respond to manual control."
            ),
            'up': Exit(
                direction='up',
                destination='deck_h_junction',
                locked=True,
                lock_message="The elevator is offline. You can see the shaft is intact, but without power to the platform, you can't use it."
            ),
        },
        items=[
            "dead_engineer",       # NPC body, actually
            "plasma_cutter",       # Weapon/tool
            "elevator_panel",      # Interactive
            "maintenance_hatch_hub",  # Hidden passage
        ],
        npcs=["corpse_engineer"],  # Body with log
        ambient_sounds=[
            "The elevator doors grind against the body with a mechanical shudder every thirty seconds, then retract.",
            "A cold wind sighs down the open elevator shaft from the decks above.",
            "The plasma cutter on the floor emits a faint, dying whine as its battery drains.",
        ],
    )
    world.add_room(deck_i_hub)

    emergency_shuttle_bay = Room(
        id="emergency_shuttle_bay",
        name="Emergency Shuttle Bay - Deck I",
        deck="Deck I - Cryogenics",
        description=(
            "A small shuttle bay holding a single emergency escape craft. The "
            "shuttle's doors are wide open, its interior empty. Beside it, "
            "on the deck, lies a shattered helmet. A second EVA suit stands "
            "in its charging alcove, dusty but intact.\n\n"
            "A large viewport overlooks open space. You can see the rust-red "
            "curve of the ship's hull outside, and beyond it... nothing but "
            "stars and a dim, malevolent spot where the rogue brown dwarf "
            "slowly swallows the constellations.\n\n"
            "You understand, looking at that spot, exactly how much time you "
            "have left."
        ),
        smell_text="The thin air carries the sharp chemical reek of EVA suit sealant and the cold, empty scent of vacuum bleeding through micro-fractures in the viewport seal.",
        touch_text="The viewport glass thrums with a deep subsonic vibration from the hull, and the shuttle's open door frame is ice-cold, radiating the chill of space beyond.",
        exits={
            'west': Exit(
                direction='west',
                destination='deck_i_hub',
                description="You return to the elevator hub."
            ),
            'down': Exit(
                direction='down',
                destination='escape_pod_bay_lower',
                description="You descend a metal staircase to the lower escape pod bay."
            ),
        },
        items=[
            "shuttle_fuel_gauge",
            "shattered_helmet",
            "eva_suit",
            "viewport_brown_dwarf",
            "escape_shuttle",
        ],
        ambient_sounds=[
            "The viewport seal whistles faintly as pressure differentials shift across the hull.",
            "The EVA suit charging alcove clicks and hums, maintaining a suit for a crew that will never wear it.",
            "Micrometeorite impacts tick against the outer hull like impatient fingernails on glass.",
        ],
        on_enter="event_see_brown_dwarf",
    )
    world.add_room(emergency_shuttle_bay)

    deck_i_storage = Room(
        id="deck_i_storage",
        name="Deck I Storage",
        deck="Deck I - Cryogenics",
        description=(
            "A storage bay filled with racks of spare parts, ration crates, "
            "and crates marked with various hazard symbols. Someone has been "
            "living here - a makeshift bed of thermal blankets in the corner, "
            "a portable heater, empty food containers.\n\n"
            "Bullet casings are scattered across the floor near the back wall. "
            "A few streak the bulkhead where shots went wide.\n\n"
            "A small locker in the corner is intact. Its number - 14 - matches "
            "the crew ID on a torn piece of uniform you notice snagged on "
            "the doorway."
        ),
        smell_text="Gunpowder residue and the dry, dusty scent of old ration packaging hang in the still air, undercut by the warmth of the portable heater baking stale sweat into the thermal blankets.",
        touch_text="Bullet casings roll under your boots with a brassy clink, and the portable heater radiates a circle of warmth that makes the surrounding cold feel even more hostile.",
        exits={
            'north': Exit(
                direction='north',
                destination='cryo_corridor',
                description="You exit the storage room."
            ),
        },
        items=[
            "thermal_blankets",
            "portable_heater",
            "bullet_casings",
            "crew_locker_14",     # Container with items
            "ration_pack",        # Food
            "torn_uniform_scrap", # Story clue
        ],
        ambient_sounds=[
            "The portable heater ticks and pings as its coils expand and contract.",
            "A loose ration crate lid flaps gently in the air circulation, a soft, irregular drumbeat.",
            "Somewhere behind the storage racks, something metallic shifts and settles with a muffled clang.",
        ],
    )
    world.add_room(deck_i_storage)

    # ═══════════════════════════════════════════════════════════════════
    # DECK D - MEDICAL (accessed via Deck I elevator/stairs)
    # ═══════════════════════════════════════════════════════════════════

    medical_corridor = Room(
        id="medical_corridor",
        name="Medical Deck Corridor",
        deck="Deck D - Medical",
        description=(
            "The corridor that leads into the medical wing, its walls colored "
            "a washed-out clinical green. Overhead lighting is harsh and white, "
            "and the air smells faintly of antiseptic and something beneath "
            "it - something sweet and wrong, like flowers left too long in water.\n\n"
            "A reception desk is to the east, manned only by a holographic "
            "receptionist that still loops through its welcome message on a "
            "broken half-second stutter: 'Welcome to - welcome to - welcome to - ' "
            "The cheerful voice is starting to put your teeth on edge.\n\n"
            "Signs point toward MEDICAL BAY (west), QUARANTINE (north, marked "
            "with a biohazard symbol), and MORGUE (east, past the broken receptionist)."
        ),
        exits={
            'south': Exit(
                direction='south',
                destination='deck_i_hub',
                description="You return to the Deck I elevator hub."
            ),
            'west': Exit(
                direction='west',
                destination='medical_bay',
                description="You enter the main medical bay."
            ),
            'north': Exit(
                direction='north',
                destination='quarantine_airlock',
                description="You approach the quarantine section."
            ),
            'east': Exit(
                direction='east',
                destination='morgue',
                description="You pass the stuttering hologram and head toward the morgue."
            ),
            'southwest': Exit(
                direction='southwest',
                destination='pharmacy',
                locked=True,
                lock_message="The pharmacy door requires a Medical Clearance Badge.",
                required_flag="has_medical_badge"
            ),
        },
        items=[
            "holographic_receptionist",
            "medical_signs",
            "discarded_mask",
        ],
        smell_text="Antiseptic and iodine hang heavy in the air, but beneath them lurks something sweet and organic, like wilting flowers in stagnant water.",
        touch_text="The walls are smooth polymer, faintly warm from the functioning overhead lights, and the floor has a tacky quality where spilled medical fluids have dried.",
        ambient_sounds=[
            "'Welcome to - welcome to - welcome to - welcome to - ' the hologram stutters.",
            "Somewhere deeper in medical, something metal hits the floor.",
            "A gurney rolls slowly past an open door, wheels squeaking.",
        ],
    )
    world.add_room(medical_corridor)

    medical_bay = Room(
        id="medical_bay",
        name="Main Medical Bay",
        deck="Deck D - Medical",
        description=(
            "The main medical bay is a large room ringed with empty hospital "
            "beds. All but one of them are freshly made, pristine. The exception "
            "is the one at the far end: its sheets are soaked in dried blood, "
            "the IV stand beside it fallen, tubes still dangling.\n\n"
            "Equipment is everywhere - scanners, surgical kits, diagnostic tools. "
            "A large holographic display in the center of the room shows the "
            "ship's crew roster, names and faces arranged in a grid. Most of "
            "the faces are crossed out with a red X. A few are marked with a "
            "yellow question mark. Only a handful remain unmarked.\n\n"
            "Your own face is there, marked with a blue circle. You don't know "
            "what that symbol means."
        ),
        smell_text="The sharp, clinical bite of antiseptic barely masks the darker smell of old blood soaked into the far bed's mattress, a coppery sweetness that clings to the back of your throat.",
        touch_text="The hospital bed rails are cold polished steel, and the holographic display warms your face with its pale light when you stand close enough to read the names of the dead.",
        exits={
            'east': Exit(
                direction='east',
                destination='medical_corridor',
                description="You return to the corridor."
            ),
            'north': Exit(
                direction='north',
                destination='surgery',
                description="You enter the surgical theater."
            ),
            'west': Exit(
                direction='west',
                destination='dr_lin_office',
                description="You enter what appears to be Dr. Lin's office."
            ),
            'south': Exit(
                direction='south',
                destination='isolation_ward',
                description="You walk down a short hallway into the isolation ward."
            ),
        },
        items=[
            "crew_roster_display",
            "bloody_bed",
            "medical_scanner_2",
            "surgical_tools",
            "iv_stand",
            "diagnostic_kit",
        ],
        ambient_sounds=[
            "Heart monitors flatline in a continuous, mournful tone from the bloody bed at the far end.",
            "The holographic crew roster hums and occasionally glitches, faces blurring into static.",
            "The fallen IV stand rocks gently, its tubes swaying like pendulums in the recycled air.",
        ],
        on_enter="event_enter_medical",
    )
    world.add_room(medical_bay)

    surgery = Room(
        id="surgery",
        name="Surgical Theater",
        deck="Deck D - Medical",
        description=(
            "A sterile operating theater with a surgical bed at its center, "
            "illuminated by harsh overhead lamps that somehow never went dark. "
            "A surgical robot arm - half-assembled, half-dismantled - hangs over "
            "the bed, its precision instruments glinting.\n\n"
            "The bed itself is occupied.\n\n"
            "A crew member lies strapped to it. Dr. Raj Patel, according to "
            "the ID badge clipped to his bloodied lab coat. His chest has been "
            "opened with clinical precision, ribs spread, heart removed. "
            "Someone was performing an autopsy on him. Someone who was "
            "interrupted mid-procedure - the surgical saw still lies in his "
            "open chest cavity.\n\n"
            "A datapad sits on a nearby tray, its screen still bright with "
            "notes."
        ),
        smell_text="Blood and exposed viscera fill the sterile air with a raw, metallic sweetness that the surgical ventilation cannot scrub away, no matter how hard it tries.",
        touch_text="The surgical bed's steel is slick with dried fluids, and the overhead lamps radiate a dry heat that makes the room feel like a furnace despite the cold horror on the table.",
        exits={
            'south': Exit(
                direction='south',
                destination='medical_bay',
                description="You back out of the surgical theater."
            ),
            'east': Exit(
                direction='east',
                destination='research_lab_med',
                description="You enter Dr. Lin's research laboratory."
            ),
        },
        items=[
            "dr_patel_body",      # Important discovery
            "surgical_saw",       # Weapon possibility
            "autopsy_datapad",    # MAJOR READABLE - reveals Seed infection
            "surgical_robot",     # Scenery
            "surgery_tray",       # Scenery
        ],
        ambient_sounds=[
            "The surgical robot arm twitches periodically, servos firing in abortive micro-movements as if trying to complete its interrupted procedure.",
            "Overhead lamps buzz with a harsh, fluorescent intensity that drills into your temples.",
            "A slow drip of something thick and dark falls from the surgical bed to the drain below.",
        ],
        on_enter="event_see_patel",
    )
    world.add_room(surgery)

    dr_lin_office = Room(
        id="dr_lin_office",
        name="Dr. Lin's Office",
        deck="Deck D - Medical",
        description=(
            "A small, tidy office that has been violently disturbed. Papers "
            "cover the floor. Books have been pulled from shelves. A framed "
            "degree from Johns Hopkins hangs crooked on the wall beside a "
            "photograph of a woman smiling with her arms around a golden "
            "retriever. Dr. Sarah Lin, presumably, in happier times.\n\n"
            "Her desk is empty except for a personal journal - leather-bound, "
            "old-fashioned - lying open to a page marked with a thin silver "
            "chain. A pen rests in the gutter, still uncapped, as if she "
            "stood up mid-word and walked out.\n\n"
            "A wall safe behind the desk is cracked but intact. Its electronic "
            "lock demands a code. A sticky note attached says, simply: "
            "'BUSTER - First dog.'"
        ),
        smell_text="Old paper and leather from the journal fill the small office with a warm, bookish scent, cut by the faint sweetness of the uncapped pen's ink drying in the sterile air.",
        touch_text="The leather journal is soft and well-worn under your fingers, its pages slightly warped from the humidity of someone's breath during late-night writing sessions.",
        exits={
            'east': Exit(
                direction='east',
                destination='medical_bay',
                description="You leave Dr. Lin's office."
            ),
        },
        items=[
            "dr_lin_journal",     # MAJOR READABLE
            "dr_lin_photo",
            "lin_wall_safe",      # Puzzle container
            "framed_degree",
            "scattered_papers",
            "silver_chain",
            "medical_clearance_badge",  # Grants medical badge flag
        ],
        ambient_sounds=[
            "Papers rustle across the floor in a draft from the ventilation, whispering like secrets.",
            "The wall safe's electronic lock emits a low, periodic beep, waiting patiently for a code that may never come.",
            "A book falls from the disturbed shelf, hitting the floor with a flat, startling slap.",
        ],
    )
    world.add_room(dr_lin_office)

    quarantine_airlock = Room(
        id="quarantine_airlock",
        name="Quarantine Airlock",
        deck="Deck D - Medical",
        description=(
            "A small airlock separates the main medical deck from the quarantine "
            "bay. A heavy pressure door with reinforced glass windows blocks "
            "the way forward. Beyond the glass, you can see the quarantine "
            "area - and movement. Something shuffles in the dim light. Something "
            "that might once have been human.\n\n"
            "A control panel beside the door requires a medical clearance "
            "badge to operate. Warnings in five languages urge anyone without "
            "proper authorization to turn back.\n\n"
            "Something strikes the glass from the other side. You flinch back.\n\n"
            "The shape retreats into shadow."
        ),
        exits={
            'south': Exit(
                direction='south',
                destination='medical_corridor',
                description="You back away from the quarantine door."
            ),
            'north': Exit(
                direction='north',
                destination='quarantine_bay',
                locked=True,
                hidden=True,
                lock_message="The quarantine door is sealed. You need a Medical Clearance Badge AND the courage to open it.",
                required_flag="has_medical_badge"
            ),
            'east': Exit(
                direction='east',
                destination='decontamination_shower',
                description="You step into the decontamination station."
            ),
        },
        items=[
            "quarantine_glass",
            "quarantine_control_panel",
            "warning_signs_multilang",
        ],
        smell_text="The air here is thick with the chemical tang of decontaminant spray, but it cannot quite mask the sweet, rotting undertone seeping through the door seals.",
        touch_text="The reinforced glass is cold and vibrates faintly when something moves on the other side, and the control panel's buttons are sticky with dried sanitizer gel.",
        ambient_sounds=[
            "Something strikes the quarantine glass wetly.",
            "A rasping moan comes from behind the door, then silence.",
            "You hear slow, dragging footsteps. Then nothing.",
        ],
    )
    world.add_room(quarantine_airlock)

    quarantine_bay = Room(
        id="quarantine_bay",
        name="Quarantine Bay",
        deck="Deck D - Medical",
        description=(
            "The quarantine bay is a slaughterhouse. Three containment cells, "
            "each one holding a crewmember in varying states of advanced "
            "infection. They moan. They reach through the bars. They ask for "
            "your help in voices that sound human until you listen too closely, "
            "at which point you hear the buzzing undertone beneath their words. "
            "This is where Dr. Lin's worst cases were kept. You should not "
            "open the cells. You should not let them out."
        ),
        smell_text="The stench hits you like a wall - rotting flesh, infection, and something alien and sweet that coats the inside of your mouth and refuses to leave.",
        touch_text="The air is humid and warm, thick with biological heat from the infected bodies, and the containment bars are slick with a glistening residue you do not want to identify.",
        exits={
            'south': Exit(
                direction='south',
                destination='quarantine_airlock',
                description="You flee the quarantine bay, closing the door behind you."
            ),
        },
        items=[
            "quarantine_cell_1",
            "quarantine_cell_2",
            "quarantine_cell_3",
            "lin_clipboard",
        ],
        ambient_sounds=[
            "The infected crew members moan in an eerie, almost-harmonic chorus that rises and falls like a diseased lullaby.",
            "Fingers scrape against the containment bars in slow, deliberate patterns, as if communicating in a language you almost understand.",
            "A wet, organic sound pulses from the darkest cell, rhythmic and alive, like a second heartbeat growing inside the walls.",
        ],
        danger_level=3,
    )
    world.add_room(quarantine_bay)

    morgue = Room(
        id="morgue",
        name="Ship's Morgue",
        deck="Deck D - Medical",
        description=(
            "The morgue is colder than the rest of medical. Rows of body "
            "drawers line three walls, their labels marked in crisp white "
            "letters. Some drawers are open, empty. Others are open and "
            "definitely not empty. A few are closed, occupied, their little "
            "red LEDs indicating active refrigeration.\n\n"
            "A mortician's table sits in the center of the room. On it, "
            "covered with a white sheet that isn't quite long enough, lies "
            "a body. One hand hangs off the edge, fingers curled.\n\n"
            "Along one wall, a bank of body-storage drawers has a number "
            "pad beside each. The one labeled 'REEVES, M. - CAPTAIN' has "
            "its status light blinking yellow. Something is wrong with that drawer."
        ),
        exits={
            'west': Exit(
                direction='west',
                destination='medical_corridor',
                description="You leave the morgue."
            ),
            'south': Exit(
                direction='south',
                destination='morgue_freezer',
                description="You push open the heavy freezer door and step into the cold."
            ),
        },
        items=[
            "mortician_table_body",
            "body_drawer_reeves",     # Important - Captain's body
            "body_drawer_okafor",     # Security chief
            "body_drawer_vasquez",    # First officer
            "body_drawer_empty",
            "morgue_logbook",         # Readable
        ],
        smell_text="Formaldehyde and cold preservation chemicals sting your nostrils, layered over the unmistakable sweet-rot smell of death that no amount of refrigeration can fully contain.",
        touch_text="Every surface radiates a deep, clinical cold that seeps through your gloves, and the drawer handles are frosted with a thin rime of ice.",
        ambient_sounds=[
            "The cooling units hum a tuneless dirge.",
            "A drawer slides open by itself. You realize it was just the ship's gravity fluctuation.",
            "The sheet on the mortician's table ripples faintly in the air current.",
        ],
    )
    world.add_room(morgue)
