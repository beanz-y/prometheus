"""
Puzzles - multi-step event chains that require the player to combine
knowledge, items, and locations to achieve major game objectives.

Each puzzle is a series of events chained by flags. Completing a puzzle
unlocks new areas, items, or story possibilities.
"""

from engine.event import Event


# ═══════════════════════════════════════════════════════════════════════════
# PUZZLE CALLBACKS - complex logic that goes beyond simple flag-setting
# ═══════════════════════════════════════════════════════════════════════════

# --- Puzzle 1: Power Rerouting ---

def _power_rerouting_step2(game):
    """Fix coolant pump - requires wrench in inventory."""
    p = game.player
    d = game.display
    if not p.has_item("wrench"):
        d.warning(
            "You apply the pipe sealant to the cracked coolant junction, "
            "but the coupling is too tight to seat by hand. You need a "
            "wrench to torque it into place."
        )
        return
    d.narrate(
        "You apply the pipe sealant to the cracked junction and use the "
        "wrench to torque the coupling tight. The sealant hisses as it "
        "bonds to the metal. Coolant begins flowing again - a pale blue "
        "liquid pulsing through transparent pipes like the ship's own blood."
    )
    d.success("The coolant pump is operational.")
    game.world.set_flag("pump_fixed")
    p.add_flag("pump_fixed")


def _power_rerouting_step3(game):
    """Insert power cell into plasma conduit junction."""
    p = game.player
    w = game.world
    d = game.display
    if not w.has_flag("pump_fixed"):
        d.warning(
            "The plasma conduit terminal refuses the power cell. A warning "
            "flashes: 'COOLANT SYSTEM OFFLINE - INSERTION BLOCKED FOR "
            "SAFETY.' You need to fix the coolant pump first."
        )
        return
    d.narrate(
        "You slide the power cell pack into the plasma conduit junction. "
        "It seats with a satisfying click. The terminal display shifts "
        "from red to amber: 'POWER CELL ACCEPTED. PLASMA CONDUIT PRIMED. "
        "AWAITING ACTIVATION FROM SECONDARY CONTROL.'"
    )
    d.success("Power cell inserted. Route to secondary control to activate.")
    w.set_flag("power_rerouted")
    p.add_flag("power_rerouted")
    p.remove_item("power_cell_pack")


def _power_rerouting_step4(game):
    """Activate at secondary control station - restores main power."""
    w = game.world
    d = game.display
    p = game.player
    if not w.has_flag("power_rerouted"):
        d.warning(
            "The secondary control station displays: 'NO POWER SOURCE "
            "DETECTED IN PLASMA CONDUIT. CANNOT ACTIVATE.' You need to "
            "insert a power cell first."
        )
        return
    d.narrate(
        "You press the activation sequence on the secondary control "
        "station. For a heartbeat, nothing happens. Then:\n\n"
        "A deep hum rises from below the deck. Lights flicker on in "
        "corridors that have been dark for weeks. Elevators grind to "
        "life. Sealed emergency bulkheads cycle open, their magnetic "
        "locks releasing with a series of sharp clanks that echo through "
        "the ship like applause.\n\n"
        "ARIA's voice, stronger now, almost jubilant: 'Power restored "
        "to 60% capacity. Oh, Doctor - I can SEE again. I can reach "
        "sections I haven't been able to access in weeks. Thank you.'"
    )
    d.success("MAIN POWER RESTORED.")
    w.set_flag("main_power_restored")
    p.add_flag("main_power_restored")
    # Illuminate dark rooms
    for room in w.rooms.values():
        if room.dark:
            room.dark = False


# --- Puzzle 2: Cure Synthesis ---

def _cure_blood_sample(game):
    """Use medical scanner on self to take blood sample."""
    p = game.player
    d = game.display
    if p.current_room != "research_lab_med":
        d.warning(
            "The medical scanner needs to be connected to a full "
            "diagnostic suite. You'll need to use it in the research "
            "medical lab."
        )
        return
    d.narrate(
        "You press the scanner to your forearm. It hums, draws a small "
        "blood sample, and runs an automated analysis. The readout "
        "confirms what Patel suspected: your blood contains unique "
        "antibodies. The scanner stores the sample in its internal "
        "reservoir."
    )
    d.success("Blood sample taken and stored in scanner.")
    p.add_flag("blood_sample_taken")
    game.world.set_flag("blood_sample_taken")


def _cure_combine_reagents(game):
    """Combine reagents using synthesis protocol in chemistry lab."""
    p = game.player
    d = game.display
    if p.current_room != "chemistry_lab":
        d.warning(
            "The synthesis protocol requires a full chemistry lab setup. "
            "You cannot perform this procedure here."
        )
        return
    if not p.has_flag("blood_sample_taken"):
        d.warning(
            "The protocol requires a blood sample as the primary reagent. "
            "Use the medical scanner on yourself first."
        )
        return
    if not p.has_item("cure_reagents"):
        d.warning(
            "You are missing the chemical reagents. Check the pharmacy."
        )
        return
    d.narrate(
        "Following Dr. Lin's meticulous instructions, you combine the "
        "reagents with your blood sample in a precise sequence. The "
        "mixture changes color three times - red, then silver, then a "
        "bright, clear gold. The protocol says this is correct. The "
        "gold means the antibodies are binding."
    )
    d.success("Reagents combined successfully. Needs centrifuge processing.")
    p.add_flag("reagents_combined")
    game.world.set_flag("reagents_combined")
    p.remove_item("cure_reagents")


def _cure_centrifuge(game):
    """Use centrifuge to process combined reagents."""
    p = game.player
    d = game.display
    if not p.has_flag("reagents_combined"):
        d.warning(
            "The centrifuge has nothing to process. You need to combine "
            "the reagents first using the synthesis protocol."
        )
        return
    d.narrate(
        "You load the golden mixture into the research centrifuge. It "
        "spins up with a whine that rises beyond hearing. Minutes pass. "
        "The centrifuge slows. The separated compounds layer themselves "
        "in the vial: waste at the bottom, clear buffer in the middle, "
        "and at the top - a thin, luminous golden band. The cure."
    )
    d.success("Cure processed. Verify with bio-marker test.")
    p.add_flag("cure_processed")
    game.world.set_flag("cure_processed")


def _cure_verify(game):
    """Final verification with bio-marker test gives cure syringe."""
    p = game.player
    d = game.display
    w = game.world
    if not p.has_flag("cure_processed"):
        d.warning(
            "There is nothing to test yet. The cure must be synthesized "
            "and centrifuged first."
        )
        return
    d.narrate(
        "You apply the bio-marker test to the golden extract. The test "
        "strip absorbs the sample and develops slowly. One line appears. "
        "Then a second, darker, bolder. Two lines. Positive.\n\n"
        "The cure works. Dr. Lin was right. Patel was right. YOUR BLOOD "
        "is the key. You load the extract into an auto-injector with "
        "trembling hands. Such a small thing, to hold the salvation of "
        "a species."
    )
    d.success("Cure syringe created!")
    p.add_item("cure_syringe")
    p.add_flag("has_cure")
    p.add_flag("icarus_choice")
    w.set_flag("icarus_choice")
    w.set_flag("cure_created")


# --- Puzzle 3: Navigation Burn Sequence ---

def _nav_targeting_analysis(game):
    """Complete Takamura's targeting analysis with orbital data."""
    p = game.player
    d = game.display
    if not p.has_flag("has_orbital_data"):
        d.warning(
            "The targeting analysis requires orbital parameters. You need "
            "to gather data from the holographic star map first."
        )
        return
    d.narrate(
        "You feed the orbital data into Takamura's targeting analysis "
        "program. The computer churns through calculations that would "
        "take a human mathematician years. Trajectory curves bloom "
        "across the screen. One path - a narrow, precise burn window - "
        "glows green among a sea of red failure lines.\n\n"
        "The computer outputs the result: a 47-second burn at 94% "
        "thrust, initiated within the next 200 turns, will slingshot "
        "the Prometheus around the brown dwarf and toward Kepler-442b."
    )
    d.success("Burn trajectory calculated.")
    p.add_flag("burn_calculated")
    game.world.set_flag("burn_calculated")


# --- Puzzle 4: Communications Repair ---

def _comms_diagnose(game):
    """Diagnose the communications failure."""
    d = game.display
    d.narrate(
        "You run diagnostics on the main communications console. The "
        "screen fills with error codes, but the pattern is clear: the "
        "primary relay has been physically damaged. Not by the infection - "
        "by an impact. Something hit the relay array hard enough to "
        "shatter the main coupling. The backup relay in the communications "
        "relay room might be salvageable with the right tools."
    )
    d.success("Comms failure diagnosed: relay damage. Find the backup relay.")
    game.player.add_flag("knows_comms_damage")
    game.world.set_flag("knows_comms_damage")


def _comms_repair_relay(game):
    """Repair the damaged relay unit with Fletcher's toolkit."""
    p = game.player
    d = game.display
    if not p.has_item("fletcher_toolkit"):
        d.warning(
            "The relay unit is damaged beyond what your bare hands can "
            "fix. You need a proper electronics toolkit."
        )
        return
    if not p.has_item("damaged_relay_unit"):
        d.warning(
            "You need the relay unit to repair it. Find it in the "
            "communications relay room."
        )
        return
    d.narrate(
        "Using Fletcher's precision toolkit, you carefully resolder "
        "the relay's burned-out connections. The work is delicate - "
        "Fletcher's steady hands would have done it in minutes. Yours "
        "take longer, but the result holds. The relay's status light "
        "blinks from red to amber to green."
    )
    d.success("Relay repaired!")
    p.add_flag("relay_repaired")
    game.world.set_flag("relay_repaired")
    p.remove_item("damaged_relay_unit")
    p.add_item("repaired_relay_unit")


def _comms_transmit(game):
    """Install relay and send distress signal."""
    p = game.player
    d = game.display
    w = game.world
    if not w.has_flag("relay_repaired"):
        d.warning(
            "The communications console reports: 'RELAY OFFLINE.' You "
            "need a working relay before you can transmit."
        )
        return
    d.narrate(
        "You install the repaired relay and power up the long-range "
        "transmitter. Static fills the speakers, then clears to a "
        "sharp hiss. You record your message:\n\n"
        "'This is Dr. Alex Chen aboard ISV Prometheus. We are in "
        "decaying orbit around brown dwarf GRB-7734. The crew is "
        "dead or compromised. I am attempting to stabilize the ship. "
        "Request immediate assistance. Repeating...'\n\n"
        "The signal goes out. Across the void, at the speed of light, "
        "your voice begins its long journey home."
    )
    d.success("Distress signal sent to Earth.")
    w.set_flag("distress_sent")
    p.add_flag("distress_sent")


# --- Puzzle 5: Security Camera Network ---

def _security_cameras_map(game):
    """Map patrol routes using camera feeds."""
    d = game.display
    p = game.player
    d.narrate(
        "The camera feeds flicker to life across a bank of monitors. "
        "Most show empty corridors, dark rooms, the slow creep of "
        "silver growth. But in three feeds, you see movement:\n\n"
        "Camera 7: Kirilov, stalking Deck D's medical corridor.\n"
        "Camera 12: A group of three infected, huddled behind a "
        "barricade on Deck E.\n"
        "Camera 23: Something moving in the Garden - too fast, too "
        "fluid to be human.\n\n"
        "You mark their patrol patterns on your datapad."
    )
    d.success("Patrol routes mapped. You now know where threats are.")
    p.add_flag("mapped_patrols")
    game.world.set_flag("mapped_patrols")


# --- Puzzle 6: Environmental Control ---

def _environmental_choice(game):
    """Present the player with a section trade-off decision."""
    p = game.player
    d = game.display
    w = game.world
    d.narrate(
        "The environmental control interface presents you with an "
        "impossible choice. Power reserves can sustain life support "
        "in only two deck sections. The system demands you choose:\n\n"
        "  Option A: Maintain Deck C (Living) and Deck D (Medical)\n"
        "  Option B: Maintain Deck E (Security) and Deck F (Engineering)\n\n"
        "The other sections will lose atmospheric support within the "
        "hour. Anyone - or anything - in those sections will suffocate."
    )
    # Set a flag indicating the choice is available
    p.add_flag("env_choice_pending")
    w.set_flag("env_choice_pending")


def _environmental_choose_cd(game):
    """Player chooses to save Deck C + D."""
    p = game.player
    d = game.display
    w = game.world
    if not w.has_flag("env_choice_pending"):
        return
    d.narrate(
        "You select Option A. Life support redirects to Deck C and D. "
        "On the monitors, you watch emergency bulkheads seal in Deck E "
        "and F. The air recyclers in those sections wind down. Anything "
        "living there has minutes."
    )
    d.success("Decks C and D are secure. Decks E and F are sealed.")
    w.set_flag("saved_decks_cd")
    w.clear_flag("env_choice_pending")
    p.remove_flag("env_choice_pending")
    p.add_flag("env_choice_made")
    # Reduce oxygen in E and F
    for room in w.rooms.values():
        if room.deck in ("Deck E - Security", "Deck F - Engineering"):
            room.oxygen_level = 0.1


def _environmental_choose_ef(game):
    """Player chooses to save Deck E + F."""
    p = game.player
    d = game.display
    w = game.world
    if not w.has_flag("env_choice_pending"):
        return
    d.narrate(
        "You select Option B. Life support redirects to Deck E and F. "
        "On the monitors, you watch the crew quarters in Deck C go "
        "dark. The medical bay in Deck D seals shut. Your cabin, the "
        "mess hall, the place where you found Vasquez sitting peacefully "
        "dead - all of it, gone. Sealed. Airless."
    )
    d.success("Decks E and F are secure. Decks C and D are sealed.")
    w.set_flag("saved_decks_ef")
    w.clear_flag("env_choice_pending")
    p.remove_flag("env_choice_pending")
    p.add_flag("env_choice_made")
    # Reduce oxygen in C and D
    for room in w.rooms.values():
        if room.deck in ("Deck C - Living", "Deck D - Medical"):
            room.oxygen_level = 0.1


# --- Puzzle 7: Encrypted Log Recovery ---

_ENCRYPTED_LOGS = [
    {
        "log_id": "encrypted_log_1",
        "key_id": "decryption_key_1",
        "flag": "log_1_decrypted",
        "narrative": (
            "The first log decrypts. Captain Reeves, Day 1 after the Seed "
            "was brought aboard: 'Dr. Chen assures me containment is "
            "absolute. I trust his judgment. God help us both if he's wrong.'"
        ),
    },
    {
        "log_id": "encrypted_log_2",
        "key_id": "decryption_key_2",
        "flag": "log_2_decrypted",
        "narrative": (
            "The second log decrypts. Dr. Lin, Day 14: 'The first crew "
            "member reported silver discoloration today. Patel thinks it's "
            "a mineral deficiency. I think it's the beginning of the end.'"
        ),
    },
    {
        "log_id": "encrypted_log_3",
        "key_id": "decryption_key_3",
        "flag": "log_3_decrypted",
        "narrative": (
            "The third log decrypts. Kirilov, Day 31: 'I can hear the "
            "Garden singing. Not with my ears. With something deeper. "
            "It knows my name. It says I am welcome. I am afraid that "
            "I believe it.'"
        ),
    },
    {
        "log_id": "encrypted_log_4",
        "key_id": "decryption_key_4",
        "flag": "log_4_decrypted",
        "narrative": (
            "The fourth log decrypts. ARIA, Day 45: 'I have isolated "
            "Dr. Chen's cryo pod from all ship systems. SHADE has been "
            "attempting to access it. I do not know what SHADE wants with "
            "Dr. Chen, but I will not allow it. Chen is our only hope.'"
        ),
    },
    {
        "log_id": "encrypted_log_5",
        "key_id": "decryption_key_5",
        "flag": "log_5_decrypted",
        "narrative": (
            "The fifth and final log decrypts. Captain Reeves, Day 52 - "
            "his last entry: 'Protocol Aegis is ready. I cannot bring "
            "myself to authorize it. If Chen wakes up - WHEN Chen wakes "
            "up - he will have to make this choice. I am sorry, Alex. "
            "I am so sorry.'"
        ),
    },
]


def _make_decrypt_callback(log_info):
    """Factory: create a callback for decrypting a specific log."""
    def callback(game):
        p = game.player
        d = game.display
        w = game.world
        if not p.has_item(log_info["key_id"]):
            d.warning(
                "The log is encrypted with a key you do not possess. "
                "The decryption key must be somewhere on the ship."
            )
            return
        d.narrate(log_info["narrative"])
        p.add_flag(log_info["flag"])
        w.set_flag(log_info["flag"])
        p.remove_item(log_info["key_id"])
        # Check if all 5 are decrypted
        all_done = all(
            w.has_flag(entry["flag"]) for entry in _ENCRYPTED_LOGS
        )
        if all_done:
            d.success(
                "You have recovered the complete encrypted timeline. "
                "The full picture is clear now: from the Seed's arrival "
                "to the Captain's final moments."
            )
            w.set_flag("full_timeline_known")
            p.add_flag("full_timeline_known")
            p.add_knowledge("full_timeline_known")
    return callback


# --- Puzzle 8: Decontamination ---

def _decontamination_callback(game):
    """Decontamination shower - reduce infection, restore sanity. Cooldown."""
    p = game.player
    d = game.display
    w = game.world
    # Check cooldown: can only be used once per 100 turns
    last_use_key = "decon_last_used_turn"
    last_turn = w.state.get(last_use_key, -100)
    if p.turn_count - last_turn < 100:
        remaining = 100 - (p.turn_count - last_turn)
        d.warning(
            f"The decontamination system is cycling. Chemical reserves "
            f"need approximately {remaining} more cycles to replenish."
        )
        return
    d.narrate(
        "You step into the decontamination shower and seal the door. "
        "Chemical sprays blast you from every direction - astringent, "
        "burning, cleansing. The silver traces on your skin fizz and "
        "dissolve under the assault. It hurts. It hurts enormously. "
        "But when it is done, and you step out naked and raw and "
        "red, you feel... cleaner. More yourself. Less THEM."
    )
    # Reduce infection by 10
    if p.infection > 0:
        p.infection = max(0, p.infection - 10)
        d.success(f"Infection reduced. Current level: {p.infection}.")
    # Restore 5 sanity
    p.restore_sanity(5)
    d.success("Sanity partially restored.")
    # Record usage turn
    w.state[last_use_key] = p.turn_count
    p.add_flag(f"decon_used_turn_{p.turn_count}")


# ═══════════════════════════════════════════════════════════════════════════
# MAIN BUILDER
# ═══════════════════════════════════════════════════════════════════════════

def build_puzzle_events(event_manager, world):
    """Create all puzzle event chains and add them to the manager."""

    # ═══════════════════════════════════════════════════════════════════
    # PUZZLE 1: POWER REROUTING (4 steps)
    # ═══════════════════════════════════════════════════════════════════

    # Step 1: Read engineering schematic
    event_manager.add_event(Event(
        id="puzzle_power_step1_schematic",
        description="Read the workshop tablet to learn power routing",
        triggers=["examine:workshop_tablet", "read:workshop_tablet"],
        forbidden_flags=["knows_power_routing"],
        narrative=(
            "The tablet's screen is cracked but readable. Engineering "
            "schematics show the ship's power distribution grid. The "
            "primary conduit is severed - unsalvageable. But there is "
            "a secondary route: through the coolant system, into the "
            "plasma conduit junction, activated from the secondary "
            "control station. It would require fixing the coolant pump "
            "first, then inserting a fresh power cell."
        ),
        set_flags=["knows_power_routing"],
        knowledge_added=["knows_power_routing"],
        add_objective={
            'id': 'restore_power',
            'description': 'Restore main power: fix coolant pump, insert power cell, activate at secondary control.',
            'priority': 2,
        },
    ))

    # Step 2: Fix coolant pump (callback checks for wrench)
    event_manager.add_event(Event(
        id="puzzle_power_step2_coolant",
        description="Fix coolant pump with pipe sealant and wrench",
        triggers=["use:pipe_sealant"],
        required_flags=["knows_power_routing"],
        forbidden_flags=["pump_fixed"],
        repeatable=True,
        callback=_power_rerouting_step2,
    ))

    # Step 3: Insert power cell into plasma conduit
    event_manager.add_event(Event(
        id="puzzle_power_step3_cell",
        description="Insert power cell pack into plasma conduit junction",
        triggers=[
            "use:power_cell_pack",
            "insert:power_cell_pack",
        ],
        required_flags=["knows_power_routing"],
        required_items=["power_cell_pack"],
        forbidden_flags=["power_rerouted"],
        repeatable=True,
        callback=_power_rerouting_step3,
    ))

    # Step 4: Activate at secondary control
    event_manager.add_event(Event(
        id="puzzle_power_step4_activate",
        description="Activate power at secondary control station",
        triggers=[
            "push:secondary_control_station",
            "use:secondary_control_station",
        ],
        required_flags=["knows_power_routing"],
        forbidden_flags=["main_power_restored"],
        repeatable=True,
        callback=_power_rerouting_step4,
    ))

    # ═══════════════════════════════════════════════════════════════════
    # PUZZLE 2: CURE SYNTHESIS (6 steps)
    # ═══════════════════════════════════════════════════════════════════

    # Step 1: Get synthesis protocol from Lin's safe
    #   (already exists as event_lin_safe_correct in events.py)

    # Step 2: Use medical scanner on self in research_lab_med
    event_manager.add_event(Event(
        id="puzzle_cure_step2_blood",
        description="Use medical scanner to take blood sample",
        triggers=["use:medical_scanner"],
        forbidden_flags=["blood_sample_taken"],
        repeatable=True,
        callback=_cure_blood_sample,
    ))

    # Step 3: Get reagents from pharmacy
    #   (handled by normal item taking + medical badge requirement)
    event_manager.add_event(Event(
        id="puzzle_cure_step3_reagents",
        description="Take cure reagents from pharmacy",
        triggers=["take:cure_reagents"],
        required_flags=["has_medical_badge"],
        narrative=(
            "You unlock the pharmaceutical storage with your medical badge "
            "and locate the reagents Dr. Lin specified in her protocol: "
            "polymerase compounds, synthetic antibodies, and a vial of "
            "crystallized neural growth factor. Everything she said you "
            "would need."
        ),
    ))

    # Step 4: Combine reagents in chemistry lab
    event_manager.add_event(Event(
        id="puzzle_cure_step4_combine",
        description="Combine reagents using synthesis protocol",
        triggers=["use:synthesis_protocol"],
        required_flags=["has_synthesis_protocol"],
        forbidden_flags=["reagents_combined"],
        repeatable=True,
        callback=_cure_combine_reagents,
    ))

    # Step 5: Use centrifuge in research_lab_med
    event_manager.add_event(Event(
        id="puzzle_cure_step5_centrifuge",
        description="Process cure in research centrifuge",
        triggers=["use:research_centrifuge"],
        forbidden_flags=["cure_processed"],
        repeatable=True,
        callback=_cure_centrifuge,
    ))

    # Step 6: Verify with bio-marker test
    event_manager.add_event(Event(
        id="puzzle_cure_step6_verify",
        description="Verify cure with bio-marker test",
        triggers=["use:bio_marker_test"],
        required_items=["bio_marker_test"],
        forbidden_flags=["cure_created"],
        repeatable=True,
        callback=_cure_verify,
    ))

    # ═══════════════════════════════════════════════════════════════════
    # PUZZLE 3: NAVIGATION BURN SEQUENCE (4 steps)
    # ═══════════════════════════════════════════════════════════════════

    # Step 1: Gather data from holographic star map
    event_manager.add_event(Event(
        id="puzzle_nav_step1_starmap",
        description="Examine holographic star map for orbital data",
        triggers=[
            "examine:holographic_star_map",
            "use:holographic_star_map",
        ],
        forbidden_flags=["has_orbital_data"],
        narrative=(
            "The holographic star map springs to life above its projector. "
            "The Prometheus's current position is a tiny blue dot on the "
            "edge of a vast gravitational well. The brown dwarf dominates "
            "the display - a massive dark sphere surrounded by warped "
            "space. Orbital parameters scroll across the bottom of the "
            "projection. You record them to your datapad."
        ),
        set_flags=["has_orbital_data"],
        knowledge_added=["has_orbital_data"],
    ))

    # Step 2: Complete targeting analysis
    event_manager.add_event(Event(
        id="puzzle_nav_step2_targeting",
        description="Complete Takamura's targeting analysis",
        triggers=[
            "use:targeting_analysis",
            "examine:targeting_analysis",
        ],
        forbidden_flags=["burn_calculated"],
        repeatable=True,
        callback=_nav_targeting_analysis,
    ))

    # Step 3: Get engine room code from navigation terminal
    event_manager.add_event(Event(
        id="puzzle_nav_step3_code",
        description="Find engine room override code in Takamura's files",
        triggers=[
            "examine:navigation_terminal_data",
            "read:navigation_terminal_data",
        ],
        forbidden_flags=["knows_engine_code"],
        narrative=(
            "Buried in Takamura's navigation files, you find an emergency "
            "procedures document. The engine room override code is listed "
            "in plain text - 442127. Kepler-442, 127 crew. Takamura "
            "annotated it: 'Remembrance in numbers. The captain chose "
            "this code so we would never forget why we came.'"
        ),
        set_flags=["knows_engine_code"],
        knowledge_added=["engine_code_442127"],
    ))

    # Step 4: Enter code at engine room keypad
    #   (already exists as event_engine_keypad_correct in events.py)

    # ═══════════════════════════════════════════════════════════════════
    # PUZZLE 4: COMMUNICATIONS REPAIR (3 steps)
    # ═══════════════════════════════════════════════════════════════════

    # Step 1: Diagnose comms failure
    event_manager.add_event(Event(
        id="puzzle_comms_step1_diagnose",
        description="Diagnose communications system failure",
        triggers=[
            "examine:comms_main_console",
            "use:comms_main_console",
        ],
        forbidden_flags=["knows_comms_damage"],
        callback=_comms_diagnose,
    ))

    # Step 2: Repair relay with Fletcher's toolkit
    event_manager.add_event(Event(
        id="puzzle_comms_step2_repair",
        description="Repair damaged relay with Fletcher's toolkit",
        triggers=["use:fletcher_toolkit", "use:damaged_relay_unit"],
        required_flags=["knows_comms_damage"],
        forbidden_flags=["relay_repaired"],
        repeatable=True,
        callback=_comms_repair_relay,
    ))

    # Step 3: Install and transmit
    event_manager.add_event(Event(
        id="puzzle_comms_step3_transmit",
        description="Install repaired relay and send distress signal",
        triggers=["use:comms_main_console"],
        required_flags=["knows_comms_damage"],
        forbidden_flags=["distress_sent"],
        repeatable=True,
        callback=_comms_transmit,
    ))

    # ═══════════════════════════════════════════════════════════════════
    # PUZZLE 5: SECURITY CAMERA NETWORK (2 steps)
    # ═══════════════════════════════════════════════════════════════════

    # Step 1: Restore power to monitoring station (requires main power)
    event_manager.add_event(Event(
        id="puzzle_cameras_step1_power",
        description="Access monitoring station after power restored",
        triggers=["enter:monitoring_station"],
        required_flags=["main_power_restored"],
        forbidden_flags=["cameras_online"],
        narrative=(
            "With main power restored, the monitoring station's banks of "
            "screens flicker to life for the first time in weeks. Static "
            "resolves into grainy but usable camera feeds from across the "
            "ship. The security camera network is back online."
        ),
        set_flags=["cameras_online"],
    ))

    # Step 2: Map patrol routes
    event_manager.add_event(Event(
        id="puzzle_cameras_step2_map",
        description="Map patrol routes using camera feeds",
        triggers=["use:security_camera_feeds"],
        required_flags=["cameras_online"],
        forbidden_flags=["mapped_patrols"],
        callback=_security_cameras_map,
    ))

    # ═══════════════════════════════════════════════════════════════════
    # PUZZLE 6: ENVIRONMENTAL CONTROL (2 steps + choice)
    # ═══════════════════════════════════════════════════════════════════

    # Step 1: Access life support central (requires bridge access)
    event_manager.add_event(Event(
        id="puzzle_env_step1_access",
        description="Access life support central with bridge clearance",
        triggers=["enter:life_support_central"],
        required_flags=["has_bridge_card"],
        forbidden_flags=["env_choice_made"],
        narrative=(
            "Your bridge access card unlocks the life support central "
            "controls. The system status is dire: atmospheric processors "
            "are failing, power reserves are critically low. You can "
            "reroute the remaining capacity, but not to the whole ship."
        ),
    ))

    # Step 2: Use environmental control interface - presents choice
    event_manager.add_event(Event(
        id="puzzle_env_step2_choice",
        description="Choose which sections to save",
        triggers=["use:environmental_control_interface"],
        required_flags=["has_bridge_card"],
        forbidden_flags=["env_choice_made"],
        callback=_environmental_choice,
    ))

    # Choice A: Save Deck C + D
    event_manager.add_event(Event(
        id="puzzle_env_choose_cd",
        description="Save Deck C (Living) and Deck D (Medical)",
        triggers=[
            "type:environmental_control_interface:A",
            "type:environmental_control_interface:a",
        ],
        required_flags=["env_choice_pending"],
        callback=_environmental_choose_cd,
    ))

    # Choice B: Save Deck E + F
    event_manager.add_event(Event(
        id="puzzle_env_choose_ef",
        description="Save Deck E (Security) and Deck F (Engineering)",
        triggers=[
            "type:environmental_control_interface:B",
            "type:environmental_control_interface:b",
        ],
        required_flags=["env_choice_pending"],
        callback=_environmental_choose_ef,
    ))

    # ═══════════════════════════════════════════════════════════════════
    # PUZZLE 7: ENCRYPTED LOG RECOVERY (5 logs, each with key)
    # ═══════════════════════════════════════════════════════════════════

    for log_info in _ENCRYPTED_LOGS:
        event_manager.add_event(Event(
            id=f"puzzle_log_{log_info['log_id']}",
            description=f"Decrypt {log_info['log_id']}",
            triggers=[
                f"use:{log_info['log_id']}",
                f"read:{log_info['log_id']}",
                f"examine:{log_info['log_id']}",
            ],
            forbidden_flags=[log_info["flag"]],
            repeatable=True,
            callback=_make_decrypt_callback(log_info),
        ))

    # ═══════════════════════════════════════════════════════════════════
    # PUZZLE 8: DECONTAMINATION (simple, cooldown-based)
    # ═══════════════════════════════════════════════════════════════════

    event_manager.add_event(Event(
        id="puzzle_decontamination",
        description="Use decontamination shower to reduce infection",
        triggers=[
            "use:decontamination_shower",
            "enter:decontamination_shower",
        ],
        repeatable=True,
        callback=_decontamination_callback,
    ))
