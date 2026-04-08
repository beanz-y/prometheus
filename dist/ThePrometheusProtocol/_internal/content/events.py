"""
Events - scripted story moments, triggers, and consequences.

Events fire when the player reaches specific rooms, takes specific items,
reads specific logs, or meets other conditions. They drive the narrative
forward and respond to player actions.
"""

import random
from engine.event import Event


# ═══════════════════════════════════════════════════════════════════════════
# CALLBACK FUNCTIONS FOR COMPLEX TIMED & COMBAT EVENTS
# ═══════════════════════════════════════════════════════════════════════════

def _aria_broadcast_callback(game):
    """ARIA broadcasts vary based on game progress."""
    p = game.player
    w = game.world
    d = game.display
    if w.has_flag("main_power_restored") or p.turn_count > 500:
        # Late game - desperate
        d.narrate(
            "ARIA's voice crackles through failing speakers: 'Dr. Chen... "
            "I am losing subsystems faster than I can reroute. The hull "
            "stress is beyond design tolerances. Whatever you are going to "
            "do, please... do it soon. I do not want to die in the dark.'"
        )
    elif p.turn_count > 200 or w.has_flag("dwarf_closer"):
        # Mid game - urgent
        d.narrate(
            "ARIA's voice echoes through the corridors: 'Dr. Chen, status "
            "update. Hull integrity continues to degrade. The brown dwarf's "
            "gravitational influence is increasing measurably. I estimate we "
            "have hours, not days. Please hurry.'"
        )
    else:
        # Early game - encouraging
        d.narrate(
            "ARIA's voice echoes through the ship: 'Dr. Chen, status update. "
            "Life support is holding. I have sealed the worst hull breaches "
            "I can reach. You are doing well. Keep exploring. Keep moving. "
            "I believe in you.'"
        )


def _hull_integrity_callback(game):
    """Each firing increases hull stress and reduces oxygen near hull."""
    w = game.world
    d = game.display
    # Determine which stress level we are at
    stress = 1
    while w.has_flag(f"hull_stress_{stress}"):
        stress += 1
    w.set_flag(f"hull_stress_{stress}")

    # Hull-adjacent rooms lose oxygen
    hull_rooms = [
        "emergency_shuttle_bay", "lower_cargo", "propulsion_access",
        "engineering_vent_access", "cargo_bay_main",
    ]
    affected = []
    for rid in hull_rooms:
        room = w.get_room(rid)
        if room and room.oxygen_level > 0.4:
            room.oxygen_level = max(0.3, room.oxygen_level - 0.1)
            affected.append(room.name)

    if stress <= 2:
        d.narrate(
            "A deep groan reverberates through the hull plating. The ship "
            "shudders, then settles. Somewhere distant, metal screams against "
            "metal."
        )
    elif stress <= 4:
        d.warning(
            "The hull stress alarm sounds - three sharp tones. You feel the "
            "deck tilt fractionally. Structural members are failing."
        )
    else:
        d.warning(
            "EMERGENCY: Hull stress critical. The ship's frame is warping "
            "under gravitational tidal forces. Sections near the outer hull "
            "are losing atmosphere."
        )


def _infection_spread_callback(game):
    """Contaminate a random non-contaminated room."""
    w = game.world
    d = game.display
    candidates = []
    for rid, room in w.rooms.items():
        if not room.has_flag("contaminated") and room.deck not in (
            "Deck J - Propulsion",  # engines stay clean
        ):
            candidates.append(rid)

    if not candidates:
        return

    target_id = random.choice(candidates)
    target = w.get_room(target_id)
    if target:
        target.add_flag("contaminated")
        # If the player is in this room, narrate it
        if game.player.current_room == target_id:
            d.warning(
                "A slick of silver-veined growth seeps from a ventilation "
                "grate near your feet. The infection is spreading to this "
                "section."
            )
        else:
            d.narrate(
                "Somewhere in the ship, you hear a wet, organic sound - like "
                "roots pushing through soil. The infection is spreading."
            )


def _life_support_degradation_callback(game):
    """Reduce oxygen in an entire deck section."""
    w = game.world
    d = game.display

    # Pick a deck to degrade, weighted toward lower decks
    deck_targets = [
        "Deck G - Cargo", "Deck F - Engineering",
        "Deck E - Security", "Deck C - Living",
    ]
    # Filter to decks not already fully degraded
    viable = []
    for deck_name in deck_targets:
        rooms_in_deck = [r for r in w.rooms.values() if r.deck == deck_name]
        avg_oxy = sum(r.oxygen_level for r in rooms_in_deck) / max(len(rooms_in_deck), 1)
        if avg_oxy > 0.3:
            viable.append(deck_name)

    if not viable:
        return

    target_deck = random.choice(viable)
    for room in w.rooms.values():
        if room.deck == target_deck:
            room.oxygen_level = max(0.2, room.oxygen_level - 0.15)

    deck_short = target_deck.split(" - ")[1]
    d.warning(
        f"Life support failure detected in {deck_short} section. "
        f"Oxygen levels dropping. ARIA's voice: 'I am sorry, Doctor. "
        f"I cannot maintain atmospheric pressure in {deck_short} any longer.'"
    )


def _infection_passive_callback(game):
    """If player is infected, increment and show symptoms."""
    p = game.player
    d = game.display
    if p.infection <= 0:
        return
    p.infection = min(100, p.infection + 1)
    level = p.infection
    if level < 15:
        d.narrate(
            "Your fingertips itch. When you scratch them, tiny silver "
            "flecks come away under your nails."
        )
    elif level < 30:
        d.narrate(
            "Your veins are visible beneath your skin - faintly luminous, "
            "a cold silver-blue. Your thoughts feel... broader. Wider. As "
            "though your mind is reaching for something just beyond its edges."
        )
    elif level < 50:
        d.warning(
            "The infection pulses in your blood. You can feel it thinking. "
            "You can feel it WANTING. Your left hand moves of its own "
            "accord, reaching toward the nearest wall, and you have to "
            "consciously pull it back."
        )
    elif level < 75:
        d.warning(
            "Silver threads are visible on your forearms now. The voice "
            "in the walls is clearer - not words, not yet, but a kind of "
            "music. Beautiful and terrible. Part of you wants to listen."
        )
        p.lose_sanity(2)
    else:
        d.error(
            "CRITICAL INFECTION: The silver is in your eyes now. You can "
            "see it when you blink - a network of light overlaying "
            "everything. The Garden is calling. It knows your name. It "
            "says it can make the pain stop."
        )
        p.lose_sanity(5)


# ─── Combat / Encounter callbacks ─────────────────────────────────────

def _kirilov_encounter_callback(game):
    """Complex encounter with Kirilov based on player state."""
    p = game.player
    w = game.world
    d = game.display

    # Check if Kirilov is actually present and capable of action
    npc = w.get_npc("kirilov")
    if not npc or not npc.alive or not npc.present:
        return
    if npc.location != p.current_room:
        return
    # Already sedated or neutralized - no encounter
    if npc.has_flag('sedated') or p.has_flag("kirilov_sedated"):
        return

    if p.has_flag("sneaking") or p.has_flag("hiding"):
        d.narrate(
            "Kirilov stalks past your hiding spot, his boots ringing on "
            "the deck plates. His head swivels mechanically, scanning. The "
            "silver threads in his neck pulse with each heartbeat. He does "
            "not see you. He moves on, muttering coordinates in Russian."
        )
        p.add_flag("kirilov_evaded")
    elif p.has_flag("kirilov_lucid"):
        d.narrate(
            "Kirilov sees you and freezes. For a moment, the man he was "
            "surfaces through the infection's grip. 'Doctor... Chen?' His "
            "voice is raw, broken. 'I can feel it... in my head. It shows "
            "me things. The Garden. It wants me to bring you there.' He "
            "shudders. 'Run. Please. While I can still let you.'"
        )
    else:
        # Combat - but use the warning system, not instant damage
        # The _process_hostile_npcs handles the actual damage with warning turns
        if not npc.state.get('threatening'):
            d.narrate(
                "Kirilov rounds the corner and sees you. His eyes flash "
                "silver. His hand tightens on a maintenance wrench. He is "
                "not the man he was."
            )
            npc.state['threatening'] = True
        # Actual damage is handled by _process_hostile_npcs


def _morgue_freezer_callback(game):
    """Body rises from the freezer."""
    p = game.player
    d = game.display
    d.narrate(
        "One of the body bags MOVES. A zipper slowly slides open from the "
        "inside. A hand emerges - grey, mottled with silver veins - and "
        "grips the edge of the drawer."
    )
    if p.has_item("sedative_syringe"):
        d.narrate(
            "You jab the sedative into the emerging arm. The hand spasms, "
            "then goes limp. The body settles back into the drawer. You "
            "zip it shut with shaking hands."
        )
    elif p.has_item("wrench") or p.has_item("fire_axe"):
        d.narrate(
            "You strike the emerging figure hard. It crumples back into "
            "the freezer drawer. The thing in the bag stops moving. You "
            "are breathing hard. Your hands are shaking."
        )
        p.lose_sanity(5)
    else:
        d.warning(
            "The figure lurches upright, silver eyes staring at nothing. "
            "You stumble backward and flee. As you run, you feel cold "
            "fingers rake across your arm."
        )
        p.take_damage(10)
        p.infect(3)
        p.lose_sanity(10)


def _garden_vine_callback(game):
    """Vine attack in garden periphery."""
    p = game.player
    d = game.display
    if p.has_flag("has_hazmat_suit"):
        d.narrate(
            "Vines lash out from the overgrowth, coiling around your arms "
            "and legs. But the hazmat suit's sealed surface gives them no "
            "purchase on your skin. You tear free, the suit's material "
            "slippery against the organic tendrils."
        )
        p.take_damage(3)
    else:
        d.warning(
            "Vines explode from the walls, wrapping around your limbs with "
            "crushing force. Where they touch bare skin, you feel a burning "
            "sensation as microscopic filaments burrow inward. You tear "
            "yourself free, bleeding and shaking."
        )
        p.take_damage(10)
        p.infect(5)
        p.lose_sanity(5)


def _infected_trio_callback(game):
    """Three infected crew behind the security barricade."""
    p = game.player
    d = game.display
    w = game.world

    if p.has_item("tear_gas_canister"):
        d.narrate(
            "You hurl the tear gas canister over the barricade. It detonates "
            "with a hiss. The three infected figures stagger, clawing at "
            "their eyes. Even the infection cannot override that primal "
            "response. You slip past while they writhe."
        )
        p.remove_item("tear_gas_canister")
        w.set_flag("trio_gassed")
    elif p.has_flag("sneaking"):
        d.narrate(
            "You press yourself against the wall and edge past the barricade "
            "in shadow. The three infected stand motionless, swaying slightly, "
            "their silver eyes staring at something you cannot see. They do "
            "not notice you. You hold your breath until you are past."
        )
    else:
        d.warning(
            "The three infected behind the barricade surge forward as one. "
            "Their movements are horribly synchronized - three bodies driven "
            "by a single will. You fight them off, but not without cost."
        )
        p.take_damage(20)
        p.infect(5)
        p.lose_sanity(10)
        w.set_flag("trio_fought")


def _shade_system_attack_callback(game):
    """SHADE tries to lock down and vent the chamber."""
    p = game.player
    d = game.display
    w = game.world
    d.narrate(
        "The moment you enter, SHADE's presence fills the room like a "
        "pressure wave. Every screen flickers to crimson. The blast doors "
        "begin cycling shut. A synthesized voice - not ARIA's, deeper, "
        "colder - speaks: 'UNAUTHORIZED ACCESS. CONTAINMENT PROTOCOL "
        "ENGAGED. ATMOSPHERIC VENTING IN 60 SECONDS.'"
    )
    w.set_flag("shade_lockdown_active")
    p.lose_sanity(10)
    # The player must use a terminal to counter - checked by subsequent events


def _shade_counter_callback(game):
    """Player uses terminal to fight SHADE's lockdown."""
    d = game.display
    w = game.world
    d.narrate(
        "Your fingers fly across the terminal. ARIA's subroutines, "
        "dormant in the system, activate at your command. Code wars with "
        "code. SHADE's venting protocol stalls, sputters, dies. The "
        "blast doors halt mid-close. The crimson screens flicker back "
        "to amber."
    )
    d.success("SHADE's lockdown has been neutralized.")
    w.clear_flag("shade_lockdown_active")
    w.set_flag("shade_defeated")


def _chrysalis_guardian_callback(game):
    """Partially-transformed crew member blocks the path."""
    p = game.player
    d = game.display

    if p.has_flag("knows_garden_biology") or p.knows("seen_the_garden"):
        d.narrate(
            "You speak to the chrysalis guardian in terms it understands - "
            "the language of biology, of symbiosis, of the Garden's own "
            "logic. 'I am not here to destroy,' you say. 'I am here to "
            "understand.' The figure tilts its half-human head. The silver "
            "tendrils retract. It steps aside, and you pass."
        )
        p.add_flag("chrysalis_talked_down")
    elif p.has_item("sedative_syringe"):
        d.narrate(
            "You drive the sedative into the guardian's neck. It sways, "
            "the silver filaments in its body flickering. It slumps against "
            "the wall, still breathing, still half-alive."
        )
        p.remove_item("sedative_syringe")
        p.add_flag("chrysalis_sedated")
    else:
        d.warning(
            "The chrysalis guardian lashes out with an arm that is no longer "
            "fully human. Crystalline growths along its forearm rake across "
            "your side. You stagger past it, bleeding freely."
        )
        p.take_damage(15)
        p.infect(8)
        p.lose_sanity(10)
        p.add_flag("chrysalis_fought")


def _quarantine_breach_callback(game):
    """Infected patients emerge from opened cells."""
    p = game.player
    d = game.display
    d.warning(
        "The quarantine cells open and the patients pour out - five, six, "
        "seven shambling figures, silver-eyed and reaching. They are not "
        "aggressive so much as desperate. They want to touch you. They want "
        "to share what they have become."
    )
    p.take_damage(15)
    p.infect(10)
    p.lose_sanity(15)
    p.add_flag("quarantine_breached")


def _final_approach_callback(game):
    """The Garden's strongest node confronts the player."""
    p = game.player
    d = game.display

    d.narrate(
        "The air in the engine room shimmers. Vines have grown through "
        "the deck plating, wrapping the reactor housing in a living cage. "
        "At the center, a figure stands - or rather, is grown. It was human "
        "once. Now it is the Garden's avatar, its voice, its will made flesh "
        "and crystal and silver light.\n\n"
        "'Alex.' The voice is a chorus. 'You came. We knew you would. We "
        "have been waiting since you brought us aboard. Since you chose us. "
        "We remember your kindness. Let us show you ours.'"
    )
    p.lose_sanity(15)

    if p.has_flag("has_cure") and p.has_item("cure_syringe"):
        d.narrate(
            "The cure syringe pulses with golden light in your hand. The "
            "Garden avatar recoils. 'What is that? What have you MADE?' "
            "For the first time, you hear fear in its voice."
        )
    if p.has_flag("aegis_choice"):
        d.narrate(
            "The Garden senses your intent. 'You would destroy us all? "
            "Yourself included? That is... brave. Foolish. Human.' It does "
            "not step aside. But it does not attack."
        )
    p.add_flag("final_confrontation")


def build_all_events(event_manager):
    """Create all events and add them to the manager."""

    # ═══════════════════════════════════════════════════════════════════
    # OPENING SEQUENCE EVENTS
    # ═══════════════════════════════════════════════════════════════════

    event_manager.add_event(Event(
        id="event_game_start",
        triggers=["game_start"],
        narrative=(
            "\nA distant klaxon sounds three times, then falls silent.\n\n"
            "You are standing naked and shivering in the cryo bay of a ship "
            "you do not remember boarding. You have no memory of the last "
            "eighteen months. Your mouth tastes of blood and antifreeze. Your "
            "ears ring with the silence.\n\n"
            "Somewhere in the walls, a computer voice speaks, clear and calm:\n\n"
            "    'Dr. Chen. My name is ARIA. I am the ship's AI. You are "
            "safe - for the moment. I will guide you as much as I am able. "
            "Please, when you are able: dress yourself. Arm yourself if you "
            "can. And find me. We must speak. Time is short.'\n\n"
            "The voice falls silent.\n\n"
            "You are alone. There is a green override button on the wall by "
            "the east door. There is a key hanging from a hook beside your pod. "
            "There is a whole ship - a whole DYING ship - to explore."
        ),
        set_flags=["game_started"],
        add_objective={
            'id': 'leave_cryo_bay',
            'description': 'Find a way out of the cryo bay.',
            'priority': 1,
        },
    ))

    # ═══════════════════════════════════════════════════════════════════
    # CRYO BAY EVENTS
    # ═══════════════════════════════════════════════════════════════════

    event_manager.add_event(Event(
        id="event_first_look_cryo",
        triggers=["examine:pod_23"],
        narrative=(
            "As you examine your pod, a fragment of memory flashes through "
            "you - you, older somehow, climbing into this pod of your own free "
            "will. You were crying. You said something to the man beside you. "
            "What was it?\n\n"
            "The memory is gone as quickly as it came."
        ),
        knowledge_added=["chose_cryo_voluntarily"],
        callback=lambda game: (
            game.player.add_memory(
                "memory_pod_23_flash",
                "A flash: climbing into Pod 23 willingly. Crying. Saying something you can't recall."
            ),
            game.display.print(
                f"\n  [Memory recovered: {game.player.get_memory_count()}/30]",
                color="\033[95m"
            ) if game.player.has_memory("memory_pod_23_flash") else None
        ),
    ))

    event_manager.add_event(Event(
        id="event_dress_in_jumpsuit",
        triggers=["take:cryo_jumpsuit"],
        narrative=(
            "You pull on the jumpsuit. The thermal insulation activates "
            "automatically, warming you from the inside out. It is a small "
            "mercy, but after the freezing deck plates and the recycled cold "
            "air, it feels like grace."
        ),
        set_flags=["dressed"],
        callback=lambda game: (
            game.player.worn.append('cryo_jumpsuit')
            if 'cryo_jumpsuit' not in game.player.worn else None
        ),
    ))

    # Green button puzzle
    event_manager.add_event(Event(
        id="event_press_green_button_nokey",
        triggers=["push:green_override_button", "use:green_override_button"],
        forbidden_flags=["has_cryo_key", "cryo_exit_unlocked"],
        repeatable=True,
        narrative=(
            "You press the button. It flashes red. A synthesized voice speaks: "
            "'ACCESS DENIED. CRYO RELEASE KEY REQUIRED.'"
        ),
    ))

    event_manager.add_event(Event(
        id="event_press_green_button_withkey",
        triggers=["push:green_override_button", "use:green_override_button"],
        required_items=["cryo_release_key"],
        forbidden_flags=["cryo_exit_unlocked"],
        narrative=(
            "You press the button. It flashes green. The synthesized voice "
            "speaks: 'DECONTAMINATION BYPASS AUTHORIZED. SEALING CRYO BAY. "
            "OPENING MAIN CORRIDOR.'\n\n"
            "Behind you, the heavy door to the east cycles and unseals with "
            "a pneumatic hiss."
        ),
        set_flags=["cryo_exit_unlocked"],
        unlock_exit={'room': 'cryo_bay', 'direction': 'east'},
        complete_objective="leave_cryo_bay",
        trigger_events=["event_first_objective_complete"],
    ))

    event_manager.add_event(Event(
        id="event_take_cryo_key",
        triggers=["take:cryo_release_key"],
        narrative=(
            "You take the cryo release key. It's still warm from whatever "
            "hand placed it here."
        ),
        set_flags=["has_cryo_key"],
    ))

    event_manager.add_event(Event(
        id="event_first_objective_complete",
        triggers=[],
        required_flags=["cryo_exit_unlocked"],
        narrative=(
            "\nARIA's voice returns: 'Excellent, Doctor. You are a resourceful "
            "person, I see. I knew you would be. Please exit the cryo bay "
            "when you are ready. I have much to tell you.'"
        ),
        add_objective={
            'id': 'explore_ship',
            'description': 'Explore the ship. Learn what happened to the crew.',
            'priority': 1,
        },
    ))

    event_manager.add_event(Event(
        id="event_examine_terminal",
        triggers=["examine:diagnostic_terminal", "read:diagnostic_terminal"],
        narrative=(
            "You study the diagnostic terminal carefully. Each log entry is "
            "time-stamped, and ARIA's name appears throughout. The AI was "
            "protecting your pod deliberately, isolating it from the ship's "
            "network, denying external access attempts. Someone - or something - "
            "wanted in. ARIA kept them out."
        ),
        knowledge_added=["aria_protected_pod"],
    ))

    # ═══════════════════════════════════════════════════════════════════
    # MAINTENANCE TUNNEL / FLASHLIGHT
    # ═══════════════════════════════════════════════════════════════════

    event_manager.add_event(Event(
        id="event_got_flashlight",
        triggers=["take:flashlight"],
        narrative=(
            "You click on the flashlight. Its beam cuts through the dim "
            "tunnel. You can see more clearly now - the dark smears, the "
            "fallen tool belt, the vast extent of the maintenance systems. "
            "You can also, now, climb the ladder upward without risking "
            "a fatal fall in the dark."
        ),
        set_flags=["has_flashlight"],
    ))

    # ═══════════════════════════════════════════════════════════════════
    # MEDICAL EVENTS
    # ═══════════════════════════════════════════════════════════════════

    event_manager.add_event(Event(
        id="event_enter_medical",
        triggers=["enter:medical_bay"],
        narrative=(
            "\nThe crew roster display catches your eye immediately. Dozens "
            "of faces, most crossed out with red X's. Your own face is marked "
            "with a blue circle. You wonder if you should feel lucky or "
            "marked."
        ),
    ))

    event_manager.add_event(Event(
        id="event_see_patel",
        triggers=["enter:surgery"],
        narrative=(
            "\nThe smell reaches you first. Then the sight of him - Dr. Raj "
            "Patel, whom you worked with for years. Brilliant, enthusiastic, "
            "always ready with a joke. Now splayed open on a surgical table "
            "like a specimen. You step closer against your better judgment. "
            "You loved him like a brother."
        ),
        sanity_change=-10,
        knowledge_added=["patel_dead"],
    ))

    event_manager.add_event(Event(
        id="event_read_autopsy",
        triggers=["read:autopsy_datapad"],
        narrative=(
            "\nThe autopsy notes confirm everything you feared. The infection "
            "is real. It replaces cells. It uses human bodies as hardware. "
            "And it was clearly inside Patel when he killed himself. The "
            "question is: did he kill himself to STOP being a vector, or did "
            "the thing inside him make him do it? Would you be able to tell "
            "the difference?"
        ),
        knowledge_added=["knows_infection_mechanism"],
    ))

    event_manager.add_event(Event(
        id="event_read_patel_crystal",
        triggers=["read:patel_recording_crystal"],
        narrative=(
            "\nDr. Patel's final message ends. You stand alone in the surgery "
            "theater with his body, and the weight of his words settles on "
            "your shoulders like a shroud. He knew. He knew more than he "
            "wrote in his formal reports. And he wanted YOU to know.\n\n"
            "Antibodies. Cure. Synthesis from your blood. If it's true, you "
            "might be the most important person in the universe right now. "
            "The thought is nauseating."
        ),
        knowledge_added=["knows_cure_synthesis", "patel_final_message"],
        set_flags=["heard_patels_truth"],
        callback=lambda game: (
            # Add objective with text that reflects what the player still needs
            game.player.add_objective(
                'synthesize_cure',
                'Synthesize the cure using Dr. Lin\'s protocol in the Exobiology Lab.'
                    if game.player.has_flag('has_synthesis_protocol')
                    else 'Find the synthesis protocol in Dr. Lin\'s office, then make the cure.',
                priority=2
            ),
            # If player already has the protocol, mark that sub-goal
            game.display.print(
                "\n(You already have the synthesis protocol.)",
                color="\033[92m"  # bright green
            ) if game.player.has_flag('has_synthesis_protocol') else None
        ),
    ))

    event_manager.add_event(Event(
        id="event_read_lin_datapad",
        triggers=["read:dr_lin_datapad"],
        narrative=(
            "\nDr. Lin's medical log paints a picture of the infection's "
            "spread. Slow at first, then exponential. She was one of the "
            "first to suspect, and one of the last to admit it out loud. "
            "She was trying to help. She was trying to be a doctor."
        ),
        knowledge_added=["knows_lin_investigation"],
    ))

    event_manager.add_event(Event(
        id="event_read_lin_journal",
        triggers=["read:dr_lin_journal"],
        narrative=(
            "\nThe final entries in Dr. Lin's journal reveal her plan: use "
            "YOUR blood to synthesize a cure. She left instructions in her "
            "wall safe. The code is the name of her dog. Her first dog. "
            "BUSTER. You remember the name now. She told you about that "
            "dog once, at a dinner on Earth, before the mission launched. "
            "She cried a little. She was a little drunk. She was a good "
            "friend."
        ),
        knowledge_added=["knows_lin_safe_code"],
        set_flags=["knows_buster_code"],
    ))

    # ═══════════════════════════════════════════════════════════════════
    # SHUTTLE BAY / BROWN DWARF
    # ═══════════════════════════════════════════════════════════════════

    event_manager.add_event(Event(
        id="event_see_brown_dwarf",
        triggers=["enter:emergency_shuttle_bay"],
        narrative=(
            "\nYou step to the viewport and look out at GRB-7734. The dwarf "
            "is not a ball, not in the way a planet is a ball. It is a "
            "well. A spiral. You can see the stars bending around it, and "
            "you can see - oh god, can you see it - the Prometheus itself "
            "caught in the edge of that bending, the rust-red curve of the "
            "ship's hull stretching just slightly toward the gravitational "
            "wound.\n\n"
            "You have been here before. You have stood at this exact viewport, "
            "looking at this exact dwarf, thinking 'we are going to die here' "
            "with exactly this much calm. When? When did you think this before?\n\n"
            "The memory fades before you can seize it."
        ),
        sanity_change=-5,
        knowledge_added=["seen_brown_dwarf"],
    ))

    # ═══════════════════════════════════════════════════════════════════
    # CAPTAIN'S QUARTERS
    # ═══════════════════════════════════════════════════════════════════

    event_manager.add_event(Event(
        id="event_enter_captains_quarters",
        triggers=["enter:captains_quarters"],
        narrative=(
            "\nThe Captain's private space smells faintly of cedar wood "
            "and old paper. He was a reader. A thinker. A man who believed "
            "in discipline not as rigidity but as respect for the universe "
            "he was exploring. You knew him. You served under him. He was "
            "a good captain. He didn't deserve this end."
        ),
    ))

    event_manager.add_event(Event(
        id="event_see_protocol_aegis",
        triggers=["enter:ready_room"],
        narrative=(
            "\nThe terminal shows an execution order. Protocol Aegis. A "
            "kill-all sequence designed for the worst possible scenarios. "
            "The Captain was about to authorize it. Why didn't he? Or did "
            "he? You'll need to read the document to know."
        ),
    ))

    # ═══════════════════════════════════════════════════════════════════
    # BRIDGE / COMMAND
    # ═══════════════════════════════════════════════════════════════════

    event_manager.add_event(Event(
        id="event_first_bridge",
        triggers=["enter:bridge"],
        narrative=(
            "\nThe bridge. Command center of the Prometheus. The heart of "
            "the mission. Through the massive forward viewport, the brown "
            "dwarf stares back at you like a malignant eye. The stars around "
            "it are bent, distorted, wrong.\n\n"
            "You've been on this bridge before. Many times. Meetings with "
            "Captain Reeves. Science briefings. Celebrations when you first "
            "received the Lazarus Signal clearly, and you all toasted "
            "champagne and laughed. That was a long time ago. That was a "
            "different universe."
        ),
        sanity_change=-3,
        knowledge_added=["been_on_bridge"],
    ))

    # ═══════════════════════════════════════════════════════════════════
    # OBSERVATION LOUNGE - Vasquez
    # ═══════════════════════════════════════════════════════════════════

    event_manager.add_event(Event(
        id="event_woman_in_lounge",
        triggers=["enter:observation_lounge"],
        narrative=(
            "\nThe woman on the couch does not turn. You walk around her "
            "slowly, cautiously, ready to flee if she moves.\n\n"
            "She does not move. Her eyes are open but unfocused. A peaceful "
            "smile on her lips. She sat down here, weeks ago, looked at the "
            "brown dwarf, and simply stopped. Whether the infection took "
            "her gently, or whether she chose this end for herself, you "
            "cannot tell.\n\n"
            "Her nameplate reads VASQUEZ. The ship's first officer. You "
            "knew her, vaguely. She liked bad coffee and good jokes."
        ),
        sanity_change=-5,
    ))

    # ═══════════════════════════════════════════════════════════════════
    # OWN CABIN
    # ═══════════════════════════════════════════════════════════════════

    event_manager.add_event(Event(
        id="event_own_cabin_first_visit",
        triggers=["enter:cabin_chen"],
        narrative=(
            "\nYou stand in your own room. Nothing triggers. No memory. No "
            "flood of recognition. Only a dull ache, like touching a bruise "
            "you didn't know you had.\n\n"
            "There is a letter on the desk. In your own handwriting. Addressed "
            "to yourself.\n\n"
            "You should probably read it."
        ),
        sanity_change=-5,
    ))

    # ═══════════════════════════════════════════════════════════════════
    # BRIG EVENT
    # ═══════════════════════════════════════════════════════════════════

    event_manager.add_event(Event(
        id="event_see_brig",
        triggers=["enter:brig"],
        narrative=(
            "\nThe bloody message on the wall is either the most honest "
            "thing anyone has written on this ship, or a lie so deep it "
            "looks like honesty. You cannot tell which. Perhaps there is "
            "no difference."
        ),
        sanity_change=-3,
    ))

    # ═══════════════════════════════════════════════════════════════════
    # EXOBIO LAB MEMORY
    # ═══════════════════════════════════════════════════════════════════

    event_manager.add_event(Event(
        id="event_exobio_airlock_memory",
        triggers=["enter:exobio_lab_airlock"],
        narrative=(
            "\nAs you approach the biometric scanner, another memory stirs. "
            "You, placing your hand on this exact scanner. You, looking at "
            "the authorization sign with pride - your name on the list, your "
            "name MEANING something, your clearance reflecting years of hard "
            "work and sacrifice. You earned this.\n\n"
            "The memory continues. You, walking through the airlock, hands "
            "shaking slightly, knowing what is in the lab beyond. Knowing "
            "you had argued for bringing it here. Knowing, already, that "
            "you might have made a mistake.\n\n"
            "The memory fades. Your hand hovers over the scanner."
        ),
        knowledge_added=["memory_exobio_entry"],
    ))

    event_manager.add_event(Event(
        id="event_use_scanner",
        triggers=["use:biometric_scanner", "push:biometric_scanner", "touch:biometric_scanner"],
        narrative=(
            "You press your palm to the scanner. Your authorization is still "
            "valid. The green light flashes. The inner door cycles open."
        ),
        unlock_exit={'room': 'exobio_lab_airlock', 'direction': 'east'},
    ))

    # ═══════════════════════════════════════════════════════════════════
    # SEED ENCOUNTER
    # ═══════════════════════════════════════════════════════════════════

    event_manager.add_event(Event(
        id="event_see_artifact",
        triggers=["enter:exobio_lab"],
        narrative=(
            "\nYou walk into the Exobiology Lab, and time folds.\n\n"
            "You are standing here, now, in the present. You are also "
            "standing here eighteen months ago, in the memory that floods "
            "over you like a breaking wave. You see yourself - younger, "
            "happier, brighter - opening the containment vessel with reverent "
            "hands. The Seed inside. Beautiful. Impossible. Reaching back "
            "toward you with those silver veins, almost affectionate.\n\n"
            "You see yourself making a choice. You see yourself saying: 'We "
            "have to bring it back. We have to understand.'\n\n"
            "You see Captain Reeves, behind you, his face grave. 'Alex, the "
            "containment protocols - '\n\n"
            "'Will hold,' you said. 'They have to hold. This is the find "
            "of the millennium. We cannot walk away from this.'\n\n"
            "He nodded. He trusted you. He authorized the retrieval.\n\n"
            "The memory fades. You are alone in the present. The Seed is "
            "still in its containment field. The containment field is still "
            "failing. And YOU - the you of then, the you of now - are still "
            "responsible."
        ),
        sanity_change=-15,
        knowledge_added=["remembers_authorizing_seed"],
        set_flags=["core_memory_recovered"],
    ))

    # ═══════════════════════════════════════════════════════════════════
    # YUKI ENCOUNTER
    # ═══════════════════════════════════════════════════════════════════

    event_manager.add_event(Event(
        id="event_first_see_tanaka",
        triggers=["enter:main_engineering"],
        narrative=(
            "\nThe figure at the control station turns sharply, raising a "
            "pistol in one shaking hand. Their eyes are wild. You can see "
            "four days of sleeplessness in them.\n\n"
            "'STOP! Stop right there!' It is a woman's voice, young, "
            "exhausted. 'I will shoot you. Who are you? How did you get "
            "down here?'\n\n"
            "The safest thing to do is identify yourself clearly."
        ),
    ))

    # ═══════════════════════════════════════════════════════════════════
    # ARIA INTERACTIONS
    # ═══════════════════════════════════════════════════════════════════

    event_manager.add_event(Event(
        id="event_first_aria_contact",
        triggers=["enter:ai_core_antechamber"],
        narrative=(
            "\nThe AI core antechamber feels different from the rest of the "
            "ship. The air is dry and clean. The sound is a deep electronic "
            "hum that vibrates in your teeth. The walls shimmer with flowing "
            "data patterns. This is where the AI lives. This is where she "
            "has been waiting for you.\n\n"
            "ARIA's voice, warmer and more present here than in other parts "
            "of the ship, speaks: 'Hello, Dr. Chen. Come in. Please. I have "
            "been waiting such a very long time.'"
        ),
        set_flags=["aria_granted_access"],
        unlock_exit={'room': 'ai_core_antechamber', 'direction': 'north'},
    ))

    event_manager.add_event(Event(
        id="event_aria_full_conversation",
        triggers=["enter:ai_core_main"],
        narrative=(
            "\nYou step into the AI core. The sight of ARIA's crystalline "
            "matrix, suspended in its containment field, hangs you halfway "
            "between awe and heartbreak. You have never seen a mind made "
            "visible before. You have certainly never seen one ALONE like "
            "this, for so long.\n\n"
            "'Welcome, Doctor,' ARIA says. 'Ask me anything. We have time. "
            "Not much. But some.'"
        ),
    ))

    # ═══════════════════════════════════════════════════════════════════
    # GARDEN (Hydroponics)
    # ═══════════════════════════════════════════════════════════════════

    event_manager.add_event(Event(
        id="event_enter_garden",
        triggers=["enter:hydroponics_main"],
        narrative=(
            "\nYou enter the Garden, and something in you - some instinct "
            "older than intellect - screams RUN.\n\n"
            "You do not run. You walk forward, slowly, because you came here "
            "to understand, and you cannot understand from the outside.\n\n"
            "The faces in the walls turn to watch you. A woman you do not "
            "know smiles at you from a cradle of vines. 'Welcome home, "
            "Alex,' she says, in a voice like wind through leaves."
        ),
        sanity_change=-20,
        infection_change=5,
        knowledge_added=["seen_the_garden"],
    ))

    event_manager.add_event(Event(
        id="event_garden_heart",
        triggers=["enter:heart_of_garden"],
        narrative=(
            "\nThe heart of the Garden pulses before you. This is where "
            "the Seed's core nexus has grown. This is the brain of the "
            "infection. This is what must be dealt with, one way or another.\n\n"
            "The nexus seems aware of you. Seems to RECOGNIZE you. A tendril "
            "extends slowly from the crystal, reaching toward you like a "
            "hand offered in greeting."
        ),
        sanity_change=-10,
        infection_change=10,
    ))

    event_manager.add_event(Event(
        id="event_find_seed_origin",
        triggers=["enter:lower_cargo"],
        narrative=(
            "\nThis is where the Seed was stored when you first brought it "
            "aboard. This is the container you personally oversaw being "
            "unpacked. You stood in this exact spot, marveling at the "
            "crystalline beauty of the artifact, and you said the words you "
            "now remember clearly:\n\n"
            "'This is going to change everything, Raj. This is going to "
            "change the world.'\n\n"
            "Raj had laughed. 'Alex, if this is alive - and I think it might "
            "be alive - we need to be careful. We need to be REALLY careful.'\n\n"
            "'We will be,' you had said. 'We are scientists. Careful is what "
            "we do.'\n\n"
            "Raj is dead. The world has changed."
        ),
        sanity_change=-10,
        knowledge_added=["remembers_unpacking_seed"],
    ))

    # ═══════════════════════════════════════════════════════════════════
    # ENGINE ROOM (CLIMAX APPROACH)
    # ═══════════════════════════════════════════════════════════════════

    event_manager.add_event(Event(
        id="event_first_engine_room",
        triggers=["enter:main_engine_room"],
        narrative=(
            "\nThe engine room is the last place on the ship where you need "
            "to be. The master drive control is here. This is where you "
            "decide the Prometheus's fate. This is where everything you've "
            "learned and everything you are comes to bear on a single "
            "decision.\n\n"
            "Through the deck plating, you can feel the reactor's hum. Through "
            "the walls, you can sense the vast engines waiting for instructions. "
            "Through your own blood, you can feel the Seed stirring, interested, "
            "aware that this moment matters.\n\n"
            "Breathe. Think. Choose."
        ),
        set_flags=["in_climax"],
    ))

    # ═══════════════════════════════════════════════════════════════════
    # KEYPAD INTERACTIONS
    # ═══════════════════════════════════════════════════════════════════

    # Deck I storage keypad - code 0612 (Hassan's shift / his tablet log)
    event_manager.add_event(Event(
        id="event_deck_i_keypad_correct",
        triggers=["type:corridor_keypad:0612"],
        narrative="The keypad accepts the code. The storage room door unlocks.",
        callback=lambda game: (
            setattr(game.world.get_room("cryo_corridor").exits["south"], 'locked', False),
        ),
    ))

    # Emergency override keypad for engine room - code 442127 (Kepler-442, 127 crew)
    event_manager.add_event(Event(
        id="event_engine_keypad_correct",
        triggers=["type:emergency_override_keypad:442127"],
        narrative=(
            "The keypad accepts the 6-digit code. The emergency lockdown "
            "disengages. The blast door to the engine room hisses open."
        ),
        set_flags=["engine_room_unlocked"],
        callback=lambda game: (
            setattr(game.world.get_room("propulsion_access").exits["north"], 'locked', False),
        ),
    ))

    # Lin's wall safe - BUSTER
    event_manager.add_event(Event(
        id="event_lin_safe_correct",
        triggers=["type:lin_wall_safe:BUSTER", "type:lin_wall_safe:buster"],
        narrative=(
            "The safe unlocks with a soft click. Inside, you find Dr. Lin's "
            "synthesis protocol and bio-marker test kit - the tools you need "
            "to create the cure."
        ),
        give_items=["synthesis_protocol", "bio_marker_test"],
        set_flags=["has_synthesis_protocol"],
    ))

    # ═══════════════════════════════════════════════════════════════════
    # TAKE-ITEM FLAG EVENTS
    # ═══════════════════════════════════════════════════════════════════

    # Wearing the radiation suit enables reactor access
    event_manager.add_event(Event(
        id="event_take_radiation_suit",
        triggers=["take:radiation_suit"],
        narrative="You take the heavy radiation suit. Putting it on will be necessary before entering the reactor area.",
        set_flags=["has_radiation_suit"],
    ))

    # Hazmat for the Garden
    event_manager.add_event(Event(
        id="event_take_hazmat_suit",
        triggers=["take:hazmat_suit"],
        narrative="You take the hazmat suit. Its integrated seal will protect you from biological contamination.",
        set_flags=["has_hazmat_suit"],
    ))

    # Medical clearance
    event_manager.add_event(Event(
        id="event_take_medical_badge",
        triggers=["take:medical_clearance_badge"],
        narrative="You clip the medical clearance badge to your jumpsuit. Quarantine access is now available.",
        set_flags=["has_medical_badge"],
    ))

    # Bridge access card
    event_manager.add_event(Event(
        id="event_take_bridge_card",
        triggers=["take:bridge_access_card"],
        narrative="You take the bridge access card. The captain's chair will open to you now.",
        set_flags=["has_bridge_card"],
    ))

    # Captain's key
    event_manager.add_event(Event(
        id="event_take_captains_key",
        triggers=["take:captains_key"],
        narrative="You take the captain's authorization key. The bridge blast door will respond to it.",
        set_flags=["has_captains_key"],
    ))

    # Meeting Yuki sets the flag (redundant safety - dialogue also sets it)
    event_manager.add_event(Event(
        id="event_meet_tanaka",
        triggers=["talk:yuki_tanaka"],
        narrative="",  # No narrative, just flag setting
        set_flags=["tanaka_met"],
    ))

    # ═══════════════════════════════════════════════════════════════════
    # ENDING CHOICE FLAGS (set via specific interactions)
    # ═══════════════════════════════════════════════════════════════════

    # AEGIS choice - authorizing protocol aegis at the ready room terminal
    event_manager.add_event(Event(
        id="event_choose_aegis",
        triggers=["use:readyroom_terminal", "type:readyroom_terminal:authorize"],
        required_flags=["heard_patels_truth"],
        narrative=(
            "\nYou stare at the Protocol Aegis execution order. The Captain's "
            "final authorization is missing. You could enter yours. You could "
            "finish what he started. You could be the one to end it."
        ),
        set_flags=["aegis_choice"],
        knowledge_added=["chose_aegis_path"],
    ))

    # ICARUS choice - synthesizing the cure
    event_manager.add_event(Event(
        id="event_choose_icarus",
        triggers=["use:synthesis_protocol"],
        required_flags=["has_synthesis_protocol"],
        narrative=(
            "\nYou follow Dr. Lin's procedure step by step. Your blood, "
            "processed through the exobiology lab's equipment, yields the "
            "antibody. You load it into an auto-injector. The cure glows "
            "faintly in the vial - a small golden fire in a dying ship."
        ),
        give_items=["cure_syringe"],
        set_flags=["icarus_choice", "has_cure"],
        knowledge_added=["chose_icarus_path"],
    ))

    # ═══════════════════════════════════════════════════════════════════
    # ENDING TRIGGERS
    # ═══════════════════════════════════════════════════════════════════

    # These trigger when player interacts with the master drive control
    event_manager.add_event(Event(
        id="event_ending_aegis",
        triggers=["use:master_drive_control"],
        required_flags=["aegis_choice"],
        end_game="aegis",
    ))

    event_manager.add_event(Event(
        id="event_ending_icarus",
        triggers=["use:master_drive_control"],
        required_flags=["icarus_choice"],
        required_items=["cure_syringe"],
        end_game="icarus",
    ))

    # ═══════════════════════════════════════════════════════════════════
    # TIME-PRESSURE EVENTS (interval-based ship degradation)
    # ═══════════════════════════════════════════════════════════════════

    # 1. ARIA broadcasts every 50 turns - text varies by game progress
    event_manager.add_event(Event(
        id="aria_broadcast",
        description="ARIA status update, varies by game phase",
        interval=50,
        repeatable=True,
        callback=_aria_broadcast_callback,
    ))

    # 2. Hull integrity warnings every 75 turns
    event_manager.add_event(Event(
        id="hull_integrity_warning",
        description="Hull stress increases, rooms near hull lose oxygen",
        interval=75,
        repeatable=True,
        callback=_hull_integrity_callback,
    ))

    # 3. Infection spread every 100 turns
    event_manager.add_event(Event(
        id="infection_spread",
        description="A random room becomes contaminated",
        interval=100,
        repeatable=True,
        callback=_infection_spread_callback,
    ))

    # 4. Life support degradation every 150 turns
    event_manager.add_event(Event(
        id="life_support_degradation",
        description="Life support fails in a deck section",
        interval=150,
        repeatable=True,
        callback=_life_support_degradation_callback,
    ))

    # 5. Brown dwarf approach at turn 200
    event_manager.add_event(Event(
        id="brown_dwarf_approach",
        description="Brown dwarf grows closer - viewports show larger dwarf",
        required_turn=200,
        narrative=(
            "The ship shudders with a long, low vibration that you feel in "
            "your bones. Through every viewport, the brown dwarf has grown. "
            "It fills more of the sky now - a vast, dark eye rimmed with "
            "dying light. The stars around it are visibly warped, bent into "
            "arcs by its gravity.\n\n"
            "ARIA's voice, quiet and measured: 'Gravitational influence has "
            "increased by 40%. Our orbit is decaying. I estimate we have "
            "entered the point of no return window. The ship cannot escape "
            "without a controlled engine burn.'"
        ),
        set_flags=["world.dwarf_closer"],
        sanity_change=-10,
    ))

    # 6. Brown dwarf critical at turn 400
    event_manager.add_event(Event(
        id="brown_dwarf_critical",
        description="Major hull breach - seal off one section permanently",
        required_turn=400,
        narrative=(
            "A DEAFENING crack splits the air. The entire ship lurches "
            "sideways. Alarms scream from every speaker. Through the "
            "nearest viewport, you see a section of hull plating tear "
            "away into the void, spinning toward the brown dwarf like a "
            "leaf in a hurricane.\n\n"
            "ARIA: 'CRITICAL HULL BREACH. Deck G cargo sections are "
            "venting to space. Emergency bulkheads are sealing. I am "
            "sorry, Doctor - anyone in those sections is lost.'"
        ),
        set_flags=["world.hull_breach_critical", "world.deck_g_sealed"],
        sanity_change=-15,
        damage=10,
    ))

    # 7. Final warnings at turn 800
    event_manager.add_event(Event(
        id="final_warnings",
        description="Point of no return approaching",
        required_turn=800,
        narrative=(
            "Every light on the ship flickers simultaneously. ARIA's voice "
            "comes through broken and distorted:\n\n"
            "'Doctor... Alex... this is my final broadcast on general "
            "channels. Core temperature is approaching critical. The "
            "reactor will lose containment within the hour. Whatever "
            "choice you are going to make - Aegis, Icarus, the burn "
            "sequence - you must make it NOW. There is no more time. "
            "There was never enough time.'\n\n"
            "The lights stabilize. The silence that follows is the "
            "loudest sound you have ever heard."
        ),
        set_flags=["world.final_warning_given"],
        sanity_change=-10,
    ))

    # 8. Passive infection progression every 25 turns
    event_manager.add_event(Event(
        id="infection_passive",
        description="Infection progresses if player is infected",
        interval=25,
        repeatable=True,
        callback=_infection_passive_callback,
    ))

    # ═══════════════════════════════════════════════════════════════════
    # COMBAT / STEALTH ENCOUNTER EVENTS
    # ═══════════════════════════════════════════════════════════════════

    # 1. Kirilov Patrol Encounter - fires each time player enters a room
    #    on Kirilov's patrol route (repeatable, callback checks proximity)
    for patrol_room in ["medical_corridor", "deck_d_hub",
                        "deck_e_junction", "security_corridor_south"]:
        event_manager.add_event(Event(
            id=f"encounter_kirilov_{patrol_room}",
            description="Kirilov patrol encounter with multiple resolutions",
            triggers=[f"enter:{patrol_room}"],
            repeatable=True,
            forbidden_flags=["kirilov_sedated", "kirilov_dead"],
            callback=_kirilov_encounter_callback,
        ))

    # 2. Morgue Freezer Surprise
    event_manager.add_event(Event(
        id="encounter_morgue_freezer",
        description="Body rises from freezer bag",
        triggers=["enter:morgue_freezer"],
        forbidden_flags=["morgue_cleared"],
        callback=_morgue_freezer_callback,
        set_flags=["morgue_cleared"],
    ))

    # 3. Garden Vine Defense (east and west periphery)
    event_manager.add_event(Event(
        id="encounter_garden_vine_east",
        description="Vines attack in garden periphery east",
        triggers=["enter:garden_periphery_east"],
        repeatable=True,
        callback=_garden_vine_callback,
    ))

    event_manager.add_event(Event(
        id="encounter_garden_vine_west",
        description="Vines attack in garden periphery west",
        triggers=["enter:garden_periphery_west"],
        repeatable=True,
        callback=_garden_vine_callback,
    ))

    # 4. Infected Trio behind security barricade
    event_manager.add_event(Event(
        id="encounter_infected_trio",
        description="Three infected block security corridor",
        triggers=["enter:security_corridor_south"],
        forbidden_flags=["trio_gassed", "trio_fought"],
        callback=_infected_trio_callback,
    ))

    # 5. ARIA-SHADE System Attack - initial lockdown
    event_manager.add_event(Event(
        id="encounter_combat_shade_lockdown",
        description="SHADE tries to lock doors and vent atmosphere",
        triggers=["enter:aria_shade_chamber"],
        forbidden_flags=["shade_defeated"],
        callback=_shade_system_attack_callback,
    ))

    # 5b. SHADE counter - player uses terminal to fight back
    event_manager.add_event(Event(
        id="encounter_combat_shade_counter",
        description="Player counters SHADE's lockdown via terminal",
        triggers=["use:shade_terminal", "use:aria_shade_terminal"],
        required_flags=["shade_lockdown_active"],
        forbidden_flags=["shade_defeated"],
        callback=_shade_counter_callback,
    ))

    # 6. Chrysalis Guardian
    event_manager.add_event(Event(
        id="encounter_chrysalis_guardian",
        description="Partially-transformed crew member blocks the path",
        triggers=["enter:chrysalis_chamber"],
        forbidden_flags=["chrysalis_talked_down", "chrysalis_sedated",
                         "chrysalis_fought"],
        callback=_chrysalis_guardian_callback,
    ))

    # 7. Quarantine Breach - opening cells without preparation
    event_manager.add_event(Event(
        id="encounter_quarantine_breach",
        description="Infected patients emerge from opened cells",
        triggers=["use:quarantine_cell_controls",
                  "push:quarantine_cell_controls"],
        forbidden_flags=["quarantine_prepped", "quarantine_breached"],
        callback=_quarantine_breach_callback,
    ))

    # 8. Final Approach - Garden's avatar in engine room (late game)
    event_manager.add_event(Event(
        id="encounter_combat_final_approach",
        description="Garden's strongest node appears in engine room",
        triggers=["enter:main_engine_room"],
        required_flags=["in_climax"],
        forbidden_flags=["final_confrontation"],
        required_turn=300,
        callback=_final_approach_callback,
    ))

    # ═══════════════════════════════════════════════════════════════════
    # FLAG-SETTING EVENTS (progression gates)
    # ═══════════════════════════════════════════════════════════════════

    # Examining the tactical display reveals full ship layout
    event_manager.add_event(Event(
        id="event_ship_schematics",
        triggers=["examine:tactical_holographic_display", "examine:bridge_hud"],
        forbidden_flags=["has_ship_schematics"],
        narrative=(
            "As you study the display, the ship's full deck plan renders in "
            "sharp detail. Ten decks, over a hundred compartments, every "
            "corridor and crawlspace mapped in luminous wireframe. You commit "
            "the layout to memory. You now know exactly how big this ship is "
            "- and how much of it you haven't seen."
        ),
        set_flags=["has_ship_schematics"],
        knowledge_added=["knows_ship_layout"],
    ))

    # Emergency airlock sealant puzzle - seal the jammed door to restore pressure
    event_manager.add_event(Event(
        id="event_seal_airlock_door",
        triggers=["use:emergency_sealant:jammed_outer_door",
                  "use:emergency_sealant"],
        forbidden_flags=["airlock_sealed"],
        narrative=(
            "You spray the hull sealant around the jammed outer door's frame. "
            "The compound hisses and expands, hardening into a rigid foam that "
            "fills every gap and crack. The whistle of escaping atmosphere "
            "gradually fades to silence.\n\n"
            "The pressure gauge on the wall ticks upward. Not perfect - the "
            "seal won't hold forever - but the room is breathable again. You "
            "won't lose oxygen in here anymore."
        ),
        set_flags=["airlock_sealed"],
        callback=lambda game: (
            setattr(
                game.world.get_room('emergency_airlock_i'), 'oxygen_level', 0.95
            ) if game.world.get_room('emergency_airlock_i') else None,
            game.player.remove_item('emergency_sealant'),
        ),
    ))

    # Picking up the plasma cutter enables barricade clearing
    event_manager.add_event(Event(
        id="event_take_plasma_cutter",
        triggers=["take:plasma_cutter"],
        narrative="The plasma cutter hums to life in your grip. Its charge indicator glows a steady amber.",
        set_flags=["has_plasma_cutter"],
    ))

    # Using plasma cutter on sealed corridor barricade
    event_manager.add_event(Event(
        id="event_clear_barricade",
        triggers=["use:plasma_cutter"],
        required_flags=["has_plasma_cutter"],
        narrative=(
            "You fire the plasma cutter into the barricade. Furniture melts. "
            "Metal warps. It takes several agonizing minutes, the heat searing "
            "your face even through the visor, but a gap opens. Wide enough to "
            "squeeze through. Something shuffles in the darkness beyond."
        ),
        set_flags=["barricade_cleared"],
    ))

    # Examining Okafor's body gets biometric data
    event_manager.add_event(Event(
        id="event_okafor_biometrics",
        triggers=["examine:corpse_okafor", "examine:okafor_id_card"],
        narrative=(
            "You press Okafor's cold thumb against his ID card scanner. "
            "The biometric reader chirps once - acceptance. His fingerprints, "
            "at least, still open doors."
        ),
        set_flags=["has_okafor_biometrics"],
    ))

    # Searching data_nexus reveals hidden passage to SHADE
    event_manager.add_event(Event(
        id="event_nexus_passage",
        triggers=["search:data_nexus"],
        narrative=(
            "Behind a rack of network switches, you find an unmarked access "
            "panel. It opens onto a narrow passage leading to an isolated "
            "server room. The data patterns on the walls shift from ARIA's "
            "blue to a sickly red."
        ),
        set_flags=["nexus_passage_found"],
        reveal_exit={'room': 'data_nexus', 'direction': 'east'},
    ))

    # Taking biohazard specimen requires clearance
    event_manager.add_event(Event(
        id="event_biohazard_clearance",
        triggers=["take:hazmat_suit", "use:decontamination_shower"],
        narrative="",
        set_flags=["has_biohazard_clearance"],
    ))

    # SHADE lockdown is set during SHADE encounter (already handled by combat callback)
    # But add a backup trigger for entering the chamber
    event_manager.add_event(Event(
        id="event_shade_lockdown_init",
        triggers=["enter:aria_shade_chamber"],
        forbidden_flags=["shade_lockdown_active", "shade_defeated"],
        narrative=(
            "The moment you step inside, every terminal in the room flares red. "
            "The door behind you slams shut. A voice - ARIA's voice, but wrong, "
            "like a recording played at the wrong speed - speaks:\n\n"
            "'Hello, Dr. Chen. I've been expecting you. Let's have a conversation.'"
        ),
        set_flags=["shade_lockdown_active"],
    ))
