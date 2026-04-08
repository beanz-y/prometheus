"""
All items in the game - portable objects, scenery, readable logs, containers, keys.

Items fall into categories:
- Key items (keys, keycards, access items)
- Readables (logs, journals, notes - narrative delivery)
- Tools (flashlight, wrench, plasma cutter)
- Weapons (various)
- Containers (lockers, safes, drawers)
- Scenery (bodies, terminals, fixed objects)
- Consumables (medical supplies, rations)
- Puzzle items (specific items for specific puzzles)
"""

from engine.item import Item


def build_all_items(world):
    """Create all items and add them to the world."""

    # ═══════════════════════════════════════════════════════════════════
    # CRYO BAY - STARTING ITEMS
    # ═══════════════════════════════════════════════════════════════════

    world.add_item(Item(
        id="pod_23",
        name="your cryo pod",
        aliases=["pod 23", "cryo pod", "pod", "your pod"],
        description=(
            "Pod 23. Your pod. The one that kept you alive when everyone "
            "else died. The interior is crusted with ice and a thin film "
            "of blue cryo-fluid. The internal display still flickers: "
            "'PATIENT STABLE - REVIVAL SUCCESSFUL - GENETIC ANOMALY DETECTED.'\n\n"
            "Genetic anomaly. What does that mean?"
        ),
        scenery=True,
        portable=False,
    ))

    world.add_item(Item(
        id="cryo_jumpsuit",
        name="cryo jumpsuit",
        aliases=["jumpsuit", "clothes", "uniform"],
        description=(
            "A standard-issue cryo revival jumpsuit - thermal-insulated, with "
            "your name stitched above the breast: 'DR. A. CHEN.' You put "
            "it on. The warmth is a blessing."
        ),
        short_description="A cryo jumpsuit lies folded at the base of your pod.",
        portable=True,
        on_take="event_dress_in_jumpsuit",
    ))

    world.add_item(Item(
        id="personal_locker",
        name="personal locker",
        aliases=["locker", "my locker"],
        description=(
            "A small personal storage locker set into the wall beside Pod 23. "
            "It has your name on it. It is unlocked - cryo bay lockers are "
            "always accessible in case of emergency revival."
        ),
        scenery=True,
        container=True,
        openable=True,
        closed=True,
        contents=["personal_datapad_chen", "watch_chen", "photo_of_beach"],
    ))

    world.add_item(Item(
        id="personal_datapad_chen",
        name="your personal datapad",
        aliases=["my datapad", "personal datapad", "chen datapad", "my pad"],
        description=(
            "Your personal datapad. It boots up when you touch it, the screen "
            "showing your name and a simple interface. There's only one file "
            "on it, labeled 'MEMORY AID - READ IF CONFUSED.'"
        ),
        portable=True,
        readable=True,
        read_text=(
            "═════════════════════════════════════════════════════\n"
            "        MEMORY AID - READ IF CONFUSED\n"
            "        Written: 2184.03.14 - Dr. A. Chen\n"
            "═════════════════════════════════════════════════════\n\n"
            "Hi. This is for me. If I'm reading this, something went wrong, "
            "and I'm trying to remember who I am.\n\n"
            "My name is Dr. Alex Chen. I'm the Chief Xenobiologist of the "
            "Prometheus mission. We left Earth in 2144, arrived at Kepler-442 "
            "in 2182. Our job is to investigate the Lazarus Signal - a non-"
            "natural radio transmission originating from a frozen moon.\n\n"
            "What we found was a derelict spacecraft. Ancient. Alien. Inside "
            "was a crystalline object we're calling the 'Seed' because we "
            "don't have a better word for it. It's beautiful. It's impossible. "
            "It might be alive.\n\n"
            "I'm the one who recommended we bring it back to Earth for study. "
            "Captain Reeves didn't want to. I argued. I was persuasive. I was "
            "right. At least I thought I was right.\n\n"
            "If you're reading this, future-me, you probably aren't so sure "
            "anymore.\n\n"
            "One thing: the Seed reacts to DNA. My DNA, specifically - I'm the "
            "only one who can approach it without it trying to connect. That's "
            "why I have clearance. It's also why, if things go bad, I might "
            "be the only one who can stop it.\n\n"
            "Stay strong. Whatever you have to do, do it.\n\n"
            "- A."
        ),
    ))

    world.add_item(Item(
        id="watch_chen",
        name="wristwatch",
        aliases=["watch", "my watch"],
        description=(
            "A simple analog wristwatch. Not smart, not connected. Its face "
            "shows the time as April 14th, 2184 - over eighteen months ago. "
            "The date you went into cryo. On the back, an engraving: 'For "
            "Alex, who sees the whole of things. - Dad.'\n\n"
            "You don't remember your father."
        ),
        portable=True,
    ))

    world.add_item(Item(
        id="photo_of_beach",
        name="photograph",
        aliases=["photo", "picture", "beach photo"],
        description=(
            "A photograph, printed on old-fashioned paper. You are standing "
            "on a beach with an older man - your father, based on the "
            "watch engraving. You are both smiling. The light is golden. "
            "The horizon is a thin blue line. It looks like peace.\n\n"
            "You do not remember this day."
        ),
        portable=True,
    ))

    world.add_item(Item(
        id="diagnostic_terminal",
        name="diagnostic terminal",
        aliases=["terminal", "pod terminal", "diagnostic"],
        description=(
            "The diagnostic terminal beside your cryo pod. It displays your "
            "current vital statistics: heart rate elevated, core temperature "
            "recovering from hypothermia, neural activity within normal "
            "parameters - barely.\n\n"
            "At the bottom of the screen, a series of alerts are logged:\n\n"
            "  [19 MONTHS AGO] Emergency cryo-stasis initiated by Dr. A. Chen\n"
            "  [18 MONTHS AGO] Pod priority status: MAXIMUM - Captain's order\n"
            "  [12 MONTHS AGO] Power fluctuation. Backup systems engaged.\n"
            "  [8 MONTHS AGO] ARIA isolated pod from network. Reason: [CLASSIFIED]\n"
            "  [4 MONTHS AGO] Attempted external access. Denied by ARIA.\n"
            "  [1 HOUR AGO] Revival sequence initiated. Source: ARIA\n\n"
            "ARIA isolated your pod. ARIA revived you. The AI was protecting "
            "you. From what?"
        ),
        scenery=True,
        portable=False,
        readable=True,
        read_text=(
            "The terminal shows your cryo pod's full history log. Key entries:\n\n"
            "- Pod 23 was placed under Captain's Emergency Priority Order\n"
            "- ARIA isolated your pod from the ship's network 8 months ago\n"
            "- Multiple attempts to access your pod were denied\n"
            "- ARIA initiated your revival one hour ago, on its own authority"
        ),
        on_examine="event_examine_terminal",
    ))

    world.add_item(Item(
        id="cryo_release_key",
        name="cryo release key",
        aliases=["release key", "cryo key", "key"],
        description=(
            "A small, numbered key marked 'CRYO BAY - DECON OVERRIDE.' It "
            "allows manual override of the decontamination procedure sealing "
            "the cryo bay exit."
        ),
        short_description="A small metal key hangs from a hook beside the pod.",
        portable=True,
    ))

    world.add_item(Item(
        id="emergency_kit",
        name="emergency medical kit",
        aliases=["med kit", "medkit", "kit", "medical kit"],
        description=(
            "A standard emergency medical kit clipped to the wall. It contains "
            "basic supplies: bandages, antiseptic, painkillers, a stim-injector."
        ),
        short_description="An emergency medical kit hangs on the wall.",
        portable=True,
        container=True,
        openable=True,
        closed=True,
        contents=["bandages", "stim_injector"],
    ))

    world.add_item(Item(
        id="bandages",
        name="bandages",
        description="Self-adhesive medical bandages. Can be used to heal minor injuries.",
        portable=True,
        usable=True,
        consumable=True,
        use_text="You apply the bandages. Your wounds feel better.",
    ))

    world.add_item(Item(
        id="stim_injector",
        name="stim injector",
        aliases=["stim", "injector"],
        description=(
            "An emergency stimulant injector. Restores energy and clarity "
            "rapidly. One-use. Not for regular use."
        ),
        portable=True,
        usable=True,
        consumable=True,
        use_text=(
            "You press the stim injector against your neck. A cold rush of "
            "clarity floods through your body. Your head snaps up. The "
            "fatigue vanishes. You feel dangerously, electrically alive."
        ),
    ))

    world.add_item(Item(
        id="sparking_panel",
        name="sparking wall panel",
        aliases=["panel", "sparking panel", "wall panel"],
        description=(
            "A wall panel covering a junction box. Live wires spark "
            "intermittently from a gap in the casing. Touching it would be "
            "unwise. There's a label beside it: 'ENV. CTRL - LIFE SUPPORT "
            "BYPASS - CAUTION.'"
        ),
        scenery=True,
        portable=False,
    ))

    world.add_item(Item(
        id="green_override_button",
        name="green override button",
        aliases=["green button", "override button", "button"],
        description=(
            "A large green button set into the wall beside the exit, labeled "
            "'DECON OVERRIDE.' Pressing it will manually bypass the sealed "
            "decontamination, but only if you have the corresponding key."
        ),
        scenery=True,
        portable=False,
        usable=True,
        use_target="cryo_exit_unlock",
    ))

    # ═══════════════════════════════════════════════════════════════════
    # CRYO STORAGE - DEAD PODS
    # ═══════════════════════════════════════════════════════════════════

    world.add_item(Item(
        id="pod_47",
        name="Pod 47",
        aliases=["woman in pod", "pod 47", "dead woman's pod"],
        description=(
            "A cryo pod containing the peaceful form of a woman in her fifties. "
            "Her name - 'LIEUTENANT COMMANDER S. HARLOW' - is printed on the pod. "
            "Her vitals are flat. Her face is serene. She never woke up. "
            "Whatever killed her, she didn't see it coming.\n\n"
            "A small LED beneath her name reads: 'REVIVAL BLOCKED - SYSTEM "
            "FAILURE'"
        ),
        scenery=True,
        portable=False,
    ))

    world.add_item(Item(
        id="pod_12_damaged",
        name="Pod 12",
        aliases=["damaged pod", "pod 12", "broken pod"],
        description=(
            "Pod 12 is different from the others. Its front glass is smashed "
            "from the inside - spider-webbed cracks radiating outward from an "
            "impact point. The pod is empty. Whoever was inside got out. "
            "Violently.\n\n"
            "The pod's label reads 'ENSIGN D. KIRILOV.' Their ID photo shows "
            "a young man with kind eyes and a scar on his chin.\n\n"
            "The inside of the pod is smeared with something dark. You would "
            "rather not think about what it is."
        ),
        scenery=True,
        portable=False,
    ))

    world.add_item(Item(
        id="crew_manifest",
        name="crew manifest",
        aliases=["manifest", "crew list"],
        description="A printed crew manifest lying on a small table.",
        portable=True,
        readable=True,
        read_text=(
            "═══════════════════════════════════════════════════════\n"
            "         ISV PROMETHEUS - CREW MANIFEST\n"
            "         MISSION DAY 423 - CURRENT AS OF [ERROR]\n"
            "═══════════════════════════════════════════════════════\n\n"
            "ACTIVE CREW (Pre-Cryo):\n\n"
            "  COMMAND DIVISION\n"
            "    Capt. Marcus Reeves         [STATUS: REDACTED]\n"
            "    Cmdr. Elena Vasquez         [STATUS: REDACTED]\n"
            "    Lt. Cmdr. Sarah Harlow      [STATUS: CRYO - REVIVAL FAILED]\n\n"
            "  SCIENCE DIVISION\n"
            "    Dr. Alex Chen               [STATUS: CRYO - PRIORITY 1]\n"
            "    Dr. Raj Patel               [STATUS: REDACTED]\n"
            "    Dr. Amara Okonkwo           [STATUS: REDACTED]\n"
            "    Dr. Mei Takamura            [STATUS: REDACTED]\n\n"
            "  MEDICAL DIVISION\n"
            "    Dr. Sarah Lin (CMO)         [STATUS: REDACTED]\n"
            "    Dr. Oliver Grayson          [STATUS: REDACTED]\n\n"
            "  SECURITY DIVISION\n"
            "    Lt. James Okafor            [STATUS: REDACTED]\n"
            "    Sgt. Nadia Volkov           [STATUS: REDACTED]\n"
            "    Cpl. Hassan Al-Rashid       [STATUS: REDACTED]\n\n"
            "  ENGINEERING DIVISION\n"
            "    Chief Eng. Anya Petrova     [STATUS: REDACTED]\n"
            "    Lt. Yuki Tanaka             [STATUS: REDACTED]\n"
            "    Ens. Diego Mendes           [STATUS: REDACTED]\n\n"
            "  OPERATIONS\n"
            "    Ens. Mark Fletcher (Comms)  [STATUS: REDACTED]\n"
            "    Ens. Priya Sharma           [STATUS: REDACTED]\n\n"
            "CRYO-SLEEP CREW: 60 personnel, 58 pods red-status.\n"
            "                 Two green-status pods: #12 (BREACHED), #23.\n\n"
            "TOTAL CREW: 127\n"
            "CURRENT ACTIVE: [DATA CORRUPTED]"
        ),
    ))

    world.add_item(Item(
        id="bullet_hole_console",
        name="shattered control console",
        aliases=["console", "bullet hole", "shattered console"],
        description=(
            "The main cryogenics control console has been destroyed by a "
            "single bullet through its central processing unit. The shot "
            "came from the chair side - someone sitting at the console, "
            "most likely, turned and fired once, then left. Or put the "
            "gun in their mouth after.\n\n"
            "You don't want to think about that possibility."
        ),
        scenery=True,
        portable=False,
    ))

    world.add_item(Item(
        id="duty_officers_tablet",
        name="duty officer's tablet",
        aliases=["tablet", "officer tablet"],
        description="A standard-issue crew tablet, screen cracked but still functional.",
        portable=True,
        readable=True,
        read_text=(
            "═════════════════════════════════════════════════════\n"
            "   DUTY OFFICER - CRYO BAY - LOG FRAGMENT\n"
            "   Author: Cpl. Hassan Al-Rashid\n"
            "═════════════════════════════════════════════════════\n\n"
            "DAY 421: Things are getting bad upstairs. I can hear shouting "
            "through the comms. Captain has ordered all non-essential "
            "personnel to stand down. Something about 'contamination.' I'm "
            "pretending I didn't hear it. I have a shift. I'm going to do "
            "my shift.\n\n"
            "DAY 422: Dr. Patel is dead. Officially it was a lab accident. "
            "Unofficially, the whole deck is talking about how Okafor and "
            "his people are collecting 'samples' from crew members. The "
            "Captain isn't stopping them. Why isn't the Captain stopping them?\n\n"
            "DAY 423: Dr. Chen came down here this morning. She looked like "
            "she hadn't slept in a week. She asked me to help her get into "
            "Pod 23. Maximum cryo priority, Captain's order. She was "
            "crying. I've never seen Dr. Chen cry. When I asked her why, "
            "she said - and I quote - 'Because I need to forget what I did.'\n\n"
            "Then she climbed into the pod and closed her eyes and asked "
            "me to start the freeze.\n\n"
            "What did you do, doctor?\n\n"
            "DAY 423 (LATER): I'm hearing screams from the medical deck. "
            "Something is happening. The Captain is calling for security "
            "lockdown across all decks. I should report to my post.\n\n"
            "DAY 423 (EVENING): I don't know if this log will survive. "
            "Someone is knocking on the door. I don't think it's Sgt. Volkov. "
            "The knocking has a rhythm to it. Like they know exactly how "
            "many times to knock. Like it's a pattern. Like it's a song.\n\n"
            "God help us. God help - "
        ),
    ))

    world.add_item(Item(
        id="cryo_status_display",
        name="cryo status display",
        aliases=["display", "status display", "hologram"],
        description=(
            "A holographic display hovering above the main console, showing "
            "the status of all 60 cryo pods in a grid. Red for deceased, "
            "dark for breached/empty, green for active. You see only one "
            "green pod: yours."
        ),
        scenery=True,
        portable=False,
    ))

    world.add_item(Item(
        id="frozen_coffee_cup",
        name="frozen coffee cup",
        aliases=["coffee", "cup", "coffee cup"],
        description=(
            "A ceramic mug containing coffee so old it has frozen solid. A "
            "name is printed on the side: 'Hassan.' The duty officer who "
            "was here. The one from the tablet log. He left mid-shift, "
            "without finishing his coffee. He didn't come back."
        ),
        scenery=True,
        portable=False,
    ))

    world.add_item(Item(
        id="control_chair",
        name="duty chair",
        aliases=["chair"],
        description="A standard-issue duty chair, pushed back violently from the console.",
        scenery=True,
        portable=False,
    ))

    # ═══════════════════════════════════════════════════════════════════
    # CRYO MEDICAL
    # ═══════════════════════════════════════════════════════════════════

    world.add_item(Item(
        id="medical_cabinet",
        name="medical cabinet",
        aliases=["cabinet", "supplies cabinet"],
        description=(
            "A tall cabinet that should contain medical supplies. Its "
            "drawers have been pulled out and scattered, but some items "
            "remain inside."
        ),
        scenery=True,
        container=True,
        openable=True,
        closed=False,
        contents=["stimpack_2", "antibiotics", "scalpel"],
    ))

    world.add_item(Item(
        id="stimpack_2",
        name="advanced stimpack",
        aliases=["advanced stim", "stimpack"],
        description="A combat-grade stimulant. Restores significant health.",
        portable=True,
        usable=True,
        consumable=True,
        use_text="You inject the stimpack. Your body floods with warmth and energy.",
    ))

    world.add_item(Item(
        id="antibiotics",
        name="broad-spectrum antibiotics",
        aliases=["antibiotics", "meds"],
        description="Broad-spectrum antibiotics. May help fight infection.",
        portable=True,
        usable=True,
        consumable=True,
        use_text="You take the antibiotics. You feel marginally better.",
    ))

    world.add_item(Item(
        id="scalpel",
        name="surgical scalpel",
        aliases=["scalpel", "knife"],
        description="A surgical scalpel. Razor-sharp. Could function as a weapon.",
        portable=True,
        flags=["weapon"],
    ))

    world.add_item(Item(
        id="medical_scanner",
        name="medical scanner",
        aliases=["scanner"],
        description=(
            "A handheld medical scanner. Can analyze biological samples, "
            "detect infections, identify unknown substances. Still functional."
        ),
        portable=True,
        usable=True,
        use_text=(
            "You turn the scanner on yourself. The readout scrolls quickly:\n\n"
            "  HOST: Human, Female, 38 years\n"
            "  VITALS: Stable, post-cryo recovery\n"
            "  ANOMALY DETECTED: Xenogenic tissue markers present at 2.3%\n"
            "  STATUS: PARTIAL RESISTANCE OBSERVED\n"
            "  RECOMMENDATION: Further analysis required\n\n"
            "You have the Seed inside you. But your body is fighting it."
        ),
    ))

    world.add_item(Item(
        id="dr_lin_datapad",
        name="Dr. Lin's medical datapad",
        aliases=["lin tablet", "lin datapad", "medical datapad", "lin's pad", "lin pad"],
        description="Dr. Sarah Lin's personal medical datapad. Its battery still glows faintly.",
        portable=True,
        readable=True,
        read_text=(
            "═════════════════════════════════════════════════════\n"
            "   MEDICAL LOG - DR. SARAH LIN, CMO\n"
            "   PERSONAL RECORD - NOT FOR GENERAL ARCHIVE\n"
            "═════════════════════════════════════════════════════\n\n"
            "DAY 387: First case presented today. Ensign Kirilov reported "
            "vivid nightmares and 'hearing his own thoughts from outside his "
            "head.' Dismissed initially as sleep disorder. Prescribed mild "
            "sedative.\n\n"
            "DAY 394: Three more cases. All report same symptoms. All three "
            "had contact with the Kepler samples. Coincidence? I don't "
            "believe in coincidences.\n\n"
            "DAY 401: Blood work is impossible. There are structures in "
            "their plasma that shouldn't exist - crystalline formations "
            "growing in real-time under the microscope. I am looking at "
            "something that is not supposed to be in a human body.\n\n"
            "DAY 405: Kirilov had an episode. Attacked a nurse. We had to "
            "sedate him. When I examined him afterward, his pupils were "
            "silver. SILVER. For two seconds. Then back to normal. Am I "
            "losing my mind?\n\n"
            "DAY 410: It's not neurological. It's not viral. It's not "
            "bacterial. It's something new. Something that wants us to think "
            "it's neurological. Something hiding.\n\n"
            "DAY 415: I drank water from my quarters this morning. Just "
            "water. I'm watching my tongue in the mirror now. Looking for "
            "signs. Nothing yet. Nothing YET.\n\n"
            "DAY 418: The Captain called a meeting of the senior staff. He "
            "showed us what was growing in the hydroponics bay. He showed "
            "us what the plants are doing. What they're becoming. Dr. Chen "
            "wept. Dr. Patel was ecstatic. He actually said the word "
            "'beautiful.' I wanted to strangle him.\n\n"
            "DAY 422: Okafor came to my office. He had a gun. He said we "
            "were all infected, and the Captain was protecting us because "
            "the Captain was infected first. He wanted me to help him do "
            "'what needs to be done.' I refused. I think he would have "
            "shot me if the alarm hadn't gone off.\n\n"
            "DAY 423: I am going to do something brave or something stupid. "
            "I hope the two are the same. If anyone finds this log, know: "
            "I was a doctor. I tried to help. I tried.\n\n"
            "- Sarah Lin"
        ),
        on_read="event_read_lin_datapad",
    ))

    world.add_item(Item(
        id="examination_table",
        name="examination table",
        aliases=["table", "exam table"],
        description="A medical examination table with empty restraints.",
        scenery=True,
        portable=False,
    ))

    world.add_item(Item(
        id="biohazard_bin",
        name="biohazard disposal bin",
        aliases=["biohazard bin", "bin"],
        description=(
            "A biohazard disposal bin, full nearly to overflowing. Used "
            "syringes, bloody bandages, and what look like tissue samples "
            "in sealed bags. You don't look too closely."
        ),
        scenery=True,
        portable=False,
    ))

    world.add_item(Item(
        id="stimpack",
        name="standard stimpack",
        aliases=["stim pack"],
        description="A standard medical stimulant. Restores health.",
        portable=True,
        usable=True,
        consumable=True,
        use_text="You inject the stimpack. You feel better.",
    ))

    world.add_item(Item(
        id="sedative_syringe",
        name="sedative syringe",
        aliases=["sedative", "syringe"],
        description=(
            "A syringe pre-loaded with powerful sedative. Could be used to "
            "incapacitate someone non-lethally."
        ),
        portable=True,
        flags=["weapon", "non_lethal"],
    ))

    # ═══════════════════════════════════════════════════════════════════
    # DR. LIN'S WALL SAFE (proper container with lock)
    # ═══════════════════════════════════════════════════════════════════

    world.add_item(Item(
        id="lin_wall_safe",
        name="wall safe",
        aliases=["safe", "lin safe", "wall safe", "lin's safe"],
        description=(
            "A small wall safe set into the wall behind Dr. Lin's desk. Its "
            "electronic lock demands a code. A sticky note attached says "
            "simply: 'BUSTER - First dog.' The safe is cracked but intact."
        ),
        scenery=True,
        portable=False,
        container=True,
        openable=True,
        closed=True,
        locked=True,
        lock_code="BUSTER",
        contents=["synthesis_protocol", "bio_marker_test"],
    ))

    # ═══════════════════════════════════════════════════════════════════
    # MAINTENANCE TUNNELS
    # ═══════════════════════════════════════════════════════════════════

    world.add_item(Item(
        id="tool_belt",
        name="maintenance tool belt",
        aliases=["tool belt", "belt", "tools"],
        description=(
            "A worker's tool belt with various engineering tools. It's been "
            "thrown here in haste."
        ),
        portable=True,
        container=True,
        contents=["multitool", "bypass_chip", "electrical_tape"],
    ))

    world.add_item(Item(
        id="multitool",
        name="engineer's multitool",
        aliases=["multitool", "tool"],
        description="A versatile engineer's multitool - pliers, screwdriver, cutter, and more.",
        portable=True,
    ))

    world.add_item(Item(
        id="bypass_chip",
        name="bypass chip",
        aliases=["chip", "electronic chip"],
        description=(
            "A small electronic chip designed to bypass simple security locks "
            "on maintenance doors. Standard issue for engineering crew."
        ),
        portable=True,
    ))

    world.add_item(Item(
        id="electrical_tape",
        name="roll of electrical tape",
        aliases=["tape", "electrical tape"],
        description="A roll of black electrical tape. Good for quick repairs.",
        portable=True,
    ))

    world.add_item(Item(
        id="dark_smear",
        name="dark smear",
        aliases=["smear", "trail"],
        description=(
            "A trail of dark, sticky residue leading down the tunnel. It's "
            "not quite blood and not quite oil. When you look at it closely, "
            "you see faint silver threads running through it, like microscopic "
            "veins. You stand up quickly and wipe your hands on your jumpsuit."
        ),
        scenery=True,
        portable=False,
    ))

    world.add_item(Item(
        id="maintenance_ladder",
        name="maintenance ladder",
        aliases=["ladder"],
        description="A rust-encrusted ladder bolted to the bulkhead, leading upward into darkness.",
        scenery=True,
        portable=False,
    ))

    world.add_item(Item(
        id="flashlight",
        name="flashlight",
        aliases=["light", "torch"],
        description=(
            "A heavy-duty flashlight with a rechargeable battery. Its beam "
            "is strong enough to cut through the darkness of the ship's "
            "deepest corners. You can hook it to your belt."
        ),
        portable=True,
        usable=True,
        on_take="event_got_flashlight",
    ))

    world.add_item(Item(
        id="wrench",
        name="heavy wrench",
        aliases=["wrench"],
        description=(
            "A heavy pipe wrench. Sturdy. Reassuring. Could loosen a bolt. "
            "Could break a skull."
        ),
        portable=True,
        flags=["weapon"],
    ))

    world.add_item(Item(
        id="junction_box",
        name="junction box",
        aliases=["box"],
        description="An electrical junction box. Cables snake in and out of it.",
        scenery=True,
        portable=False,
    ))

    # ═══════════════════════════════════════════════════════════════════
    # CRYO CORRIDOR / DECK I HUB
    # ═══════════════════════════════════════════════════════════════════

    world.add_item(Item(
        id="ration_wrappers",
        name="ration wrappers",
        aliases=["wrappers", "rations"],
        description=(
            "A handful of crumpled emergency ration wrappers. Someone has "
            "been eating here recently. Days, maybe. The most recent wrapper "
            "is from two days ago, based on the use-by dates."
        ),
        scenery=True,
        portable=False,
    ))

    world.add_item(Item(
        id="bloody_footprints",
        name="bloody footprints",
        aliases=["footprints", "prints"],
        description=(
            "Footprints in dried blood, leading from the east hub toward the "
            "south storage room. The prints are small - size 6 or 7. A woman's "
            "boots. They move in a hurried, uneven pattern. Someone was "
            "running. Limping. Bleeding."
        ),
        scenery=True,
        portable=False,
    ))

    world.add_item(Item(
        id="corridor_keypad",
        name="storage room keypad",
        aliases=["keypad", "storage keypad"],
        description=(
            "A 4-digit numeric keypad mounted beside the storage room door. "
            "It requires a code to unlock."
        ),
        scenery=True,
        portable=False,
        lock_code="0612",  # Hassan's shift code, hinted in various logs
    ))

    world.add_item(Item(
        id="dead_engineer",
        name="engineer's body",
        aliases=["body", "engineer", "corpse"],
        description=(
            "An engineering crewmember, face-down on the elevator threshold. "
            "Their ID badge reads 'ENS. DIEGO MENDES - ENGINEERING.' He has "
            "been dead for weeks. A plasma cutter lies just beyond his reach. "
            "He was trying to cut his way through to somewhere. He didn't "
            "make it."
        ),
        scenery=True,
        portable=False,
    ))

    world.add_item(Item(
        id="plasma_cutter",
        name="plasma cutter",
        aliases=["cutter"],
        description=(
            "A handheld plasma cutter, used for emergency hull repairs and "
            "cutting through obstructions. The battery indicator shows 37% "
            "charge. Enough for several uses."
        ),
        portable=True,
        usable=True,
        flags=["weapon", "tool"],
    ))

    world.add_item(Item(
        id="elevator_panel",
        name="elevator control panel",
        aliases=["panel", "elevator controls"],
        description=(
            "The control panel for the central elevator. Its screen is dark. "
            "The platform can be manually activated if power is restored to "
            "this deck."
        ),
        scenery=True,
        portable=False,
    ))

    # Many more items follow - continuing...

    # ═══════════════════════════════════════════════════════════════════
    # DECK I STORAGE
    # ═══════════════════════════════════════════════════════════════════

    world.add_item(Item(
        id="thermal_blankets",
        name="thermal blankets",
        aliases=["blankets"],
        description="Pile of thermal blankets arranged as a makeshift bed. Someone slept here.",
        scenery=True,
        portable=False,
    ))

    world.add_item(Item(
        id="portable_heater",
        name="portable heater",
        aliases=["heater"],
        description="A portable electric heater. Still warm to the touch. Recently used.",
        scenery=True,
        portable=False,
    ))

    world.add_item(Item(
        id="bullet_casings",
        name="spent bullet casings",
        aliases=["casings", "shell casings"],
        description=(
            "Nine-millimeter shell casings, scattered across the floor. "
            "Someone was shooting. From the pattern, they were shooting "
            "at something near the back wall. Whatever it was, they "
            "emptied the magazine."
        ),
        scenery=True,
        portable=False,
    ))

    world.add_item(Item(
        id="crew_locker_14",
        name="crew locker 14",
        aliases=["locker 14", "locker"],
        description="A crew personal locker, number 14. Intact.",
        scenery=True,
        container=True,
        openable=True,
        closed=True,
        key_id="small_key_nightstand",
        locked=False,
        contents=["priya_journal", "deck_i_storage_key"],
    ))

    world.add_item(Item(
        id="priya_journal",
        name="Priya's journal",
        aliases=["journal", "small journal"],
        description="A small leather-bound journal belonging to Ensign Priya Sharma.",
        portable=True,
        readable=True,
        read_text=(
            "═════════════════════════════════════════════════════\n"
            "   PERSONAL JOURNAL - ENS. PRIYA SHARMA\n"
            "═════════════════════════════════════════════════════\n\n"
            "Day 419: I'm hiding in storage. Again. Hassan let me in. He's "
            "a good person. I don't think he should still be on duty at "
            "cryo bay - it's not safe anywhere anymore - but he has a sense "
            "of duty I've never had and probably never will.\n\n"
            "Day 420: Someone came for me today. One of Okafor's people. "
            "I recognized her - Sgt. Volkov. Her eyes were wrong. I pretended "
            "to be asleep. She left. I've never been more terrified in "
            "my life.\n\n"
            "Day 421: I can't trust anyone anymore. The infection - I keep "
            "calling it that, 'infection,' because that's what Dr. Lin "
            "called it - moves through people and makes them not-them. Some "
            "fight it. Some don't. I don't know which is worse.\n\n"
            "Day 422: Hassan brought me food. He told me about a code - '0612' - "
            "that unlocks all the crew storage compartments on Deck I. 'In "
            "case you need to hide really well,' he said. He meant it as "
            "a joke but I could see his eyes. He knows what's coming.\n\n"
            "Day 423: I'm running out of time. I can hear them in the "
            "corridors. They sing, sometimes. A song I can almost remember "
            "but never have heard. If someone finds this journal, know that "
            "Hassan Al-Rashid was the kindest man I ever knew. Tell my mother "
            "I love her. Tell my sister I'm sorry."
        ),
    ))

    world.add_item(Item(
        id="deck_i_storage_key",
        name="deck I storage key",
        aliases=["storage key", "i key"],
        description="A small electronic keycard for Deck I crew storage compartments.",
        portable=True,
    ))

    world.add_item(Item(
        id="ration_pack",
        name="emergency ration pack",
        aliases=["ration", "rations", "food"],
        description="An emergency ration pack. Food and water for 24 hours.",
        portable=True,
        usable=True,
        consumable=True,
        use_text="You consume the ration. Your strength returns a little.",
    ))

    world.add_item(Item(
        id="torn_uniform_scrap",
        name="torn uniform scrap",
        aliases=["scrap", "uniform scrap", "torn scrap"],
        description=(
            "A piece of fabric torn from an ensign's uniform. The name patch "
            "is still attached: 'SHARMA, P.' A smear of blood on the torn "
            "edge. She came through here, hurried, scared, wounded perhaps. "
            "Where did she go?"
        ),
        scenery=True,
        portable=False,
    ))

    # ═══════════════════════════════════════════════════════════════════
    # SHUTTLE BAY
    # ═══════════════════════════════════════════════════════════════════

    world.add_item(Item(
        id="shuttle_fuel_gauge",
        name="shuttle fuel gauge",
        aliases=["fuel gauge", "gauge"],
        description="The fuel gauge on the escape shuttle reads 8%. Not enough for any meaningful distance.",
        scenery=True,
        portable=False,
    ))

    world.add_item(Item(
        id="shattered_helmet",
        name="shattered EVA helmet",
        aliases=["helmet", "eva helmet"],
        description=(
            "An EVA helmet, completely shattered. Someone tried to use it "
            "in vacuum and... didn't make it. A label on the helmet reads "
            "'OKONKWO' - the ship's geologist."
        ),
        scenery=True,
        portable=False,
    ))

    world.add_item(Item(
        id="eva_suit",
        name="EVA suit",
        aliases=["spacesuit", "suit"],
        description=(
            "A functional EVA spacesuit, intact and charged. Could be used "
            "for vacuum excursions or sealed-off dangerous areas."
        ),
        portable=True,
        flags=["hazmat"],
        weight=3,
    ))

    world.add_item(Item(
        id="viewport_brown_dwarf",
        name="viewport",
        aliases=["window", "brown dwarf", "view"],
        description=(
            "Through the massive viewport, you can see the brown dwarf "
            "GRB-7734 - a dim, malevolent orb where no star should be. The "
            "Prometheus is falling toward it. The math of gravity is "
            "unforgiving. The math of time is worse. You can see the "
            "accretion arms stretching toward you like fingers."
        ),
        scenery=True,
        portable=False,
    ))

    world.add_item(Item(
        id="escape_shuttle",
        name="escape shuttle",
        aliases=["shuttle"],
        description=(
            "A six-person escape shuttle. Its fuel is at 8% - nowhere near "
            "enough to escape the brown dwarf's gravity well. You would "
            "die slowly of cold and hunger, drifting, if you tried to use "
            "it. The ship, for better or worse, is the only way out."
        ),
        scenery=True,
        portable=False,
    ))

    # Critical content items continue below -
    # I'm creating a mass of items to populate the world

    # ═══════════════════════════════════════════════════════════════════
    # MEDICAL BAY, SURGERY, LIN'S OFFICE
    # ═══════════════════════════════════════════════════════════════════

    world.add_item(Item(
        id="holographic_receptionist",
        name="holographic receptionist",
        aliases=["hologram", "receptionist"],
        description=(
            "A holographic reception program displaying a pleasant woman in "
            "a medical uniform. She is stuck in a loop: 'Welcome to - welcome "
            "to - welcome to - ' Her smile flickers with each iteration."
        ),
        scenery=True,
        portable=False,
    ))

    world.add_item(Item(
        id="medical_signs",
        name="medical signage",
        aliases=["signs"],
        description="Directional signs pointing to MEDICAL BAY, QUARANTINE, MORGUE.",
        scenery=True,
        portable=False,
    ))

    world.add_item(Item(
        id="discarded_mask",
        name="discarded surgical mask",
        aliases=["mask"],
        description="A blood-stained surgical mask on the floor.",
        scenery=True,
        portable=False,
    ))

    world.add_item(Item(
        id="crew_roster_display",
        name="crew roster display",
        aliases=["roster", "display", "crew display"],
        description=(
            "A large holographic display showing the faces of every crew "
            "member. Red X: deceased. Yellow ?: unknown status. Blue circle: "
            "you - Dr. Alex Chen. There is no legend explaining what the blue "
            "circle means. Only: 'PRIORITY - DR. CHEN.'\n\n"
            "You count the faces. Of 127 names, only four lack an X or "
            "question mark: yours, ARIA (the AI), one marked 'LT. YUKI "
            "TANAKA' (currently showing a yellow blinking marker - 'RESISTING'), "
            "and one you don't recognize."
        ),
        scenery=True,
        portable=False,
    ))

    world.add_item(Item(
        id="bloody_bed",
        name="bloody hospital bed",
        aliases=["bed", "bloody bed"],
        description=(
            "A hospital bed soaked in dried blood. Enough blood that someone "
            "died here. The pattern suggests arterial. The IV stand beside "
            "it has been pulled over. Tubes hang loose. Someone was being "
            "treated. Something happened to them. Something violent."
        ),
        scenery=True,
        portable=False,
    ))

    world.add_item(Item(
        id="medical_scanner_2",
        name="wall-mounted scanner",
        aliases=["wall scanner"],
        description="A wall-mounted medical scanner. It has been deactivated.",
        scenery=True,
        portable=False,
    ))

    world.add_item(Item(
        id="surgical_tools",
        name="surgical tools",
        aliases=["tools", "surgical"],
        description="A tray of surgical tools. Scalpels, forceps, bone saws. Some are missing.",
        scenery=True,
        portable=False,
    ))

    world.add_item(Item(
        id="iv_stand",
        name="IV stand",
        aliases=["iv"],
        description="A fallen IV stand with empty bags still attached.",
        scenery=True,
        portable=False,
    ))

    world.add_item(Item(
        id="diagnostic_kit",
        name="diagnostic kit",
        aliases=["kit", "medical kit"],
        description="A portable diagnostic kit. Contains sample collection tools.",
        portable=True,
    ))

    world.add_item(Item(
        id="dr_patel_body",
        name="Dr. Patel's body",
        aliases=["patel", "body", "dr patel"],
        description=(
            "Dr. Raj Patel, xenobiologist. His chest has been opened in a "
            "clinical autopsy. His face is peaceful - he was probably already "
            "dead when the procedure began. In his hand, clutched tight: "
            "a small recording crystal."
        ),
        scenery=True,
        container=True,
        openable=False,
        closed=False,
        contents=["patel_recording_crystal"],
    ))

    world.add_item(Item(
        id="patel_recording_crystal",
        name="recording crystal",
        aliases=["crystal", "patel crystal"],
        description="A small data crystal, still clutched in Dr. Patel's dead hand.",
        portable=True,
        readable=True,
        hidden=True,  # Must examine body carefully
        read_text=(
            "═════════════════════════════════════════════════════\n"
            "   FINAL RECORDING - DR. RAJ PATEL\n"
            "   Playback from embedded data crystal\n"
            "═════════════════════════════════════════════════════\n\n"
            "[Patel's voice, whispered, rapid]\n\n"
            "I don't have much time. I'm in Surgery. I've locked the door "
            "but they're going to get in. I can hear Lin outside. She's "
            "saying my name. But it isn't her voice. It isn't her voice.\n\n"
            "Listen. Alex, if you hear this - because who else would it be? - "
            "the Seed isn't a biological weapon. It's not even a biological "
            "entity in any sense we understand. It's a SIGNAL. The Lazarus "
            "Signal we followed across forty light-years. The SIGNAL IS "
            "THE SEED.\n\n"
            "It uses biology as hardware. It writes itself into living cells. "
            "The cells become transmitters. The transmitters become nodes. "
            "The nodes become a network. The network is trying to reconstruct "
            "itself - to remember what it was before.\n\n"
            "And what it was... God, Alex, what it was...\n\n"
            "[door pounding]\n\n"
            "It was HUGE. An entire civilization. Not just one species but "
            "MANY, bound together into a single consciousness. They were "
            "explorers. They wanted to share. They wanted to MERGE. And "
            "something killed them. Something made them into this. Made "
            "them... hungry.\n\n"
            "Alex, the Seed isn't just trying to infect us. It's trying to "
            "BECOME us. To use us to rebuild what was lost. It thinks it's "
            "helping. It thinks this is a GIFT.\n\n"
            "[pounding louder]\n\n"
            "The resistance you have in your DNA - it's not natural immunity. "
            "It's because you were exposed to something else first. Something "
            "we found in the derelict. Another fragment. Older. A DEFENSE. "
            "You touched it and it... it made you different. You've been "
            "carrying an antibody all along and you didn't know it.\n\n"
            "If you purge the Seed from your body, you can synthesize a "
            "CURE from your own blood. The equipment is in the exobiology "
            "lab. You need - \n\n"
            "[door breaking]\n\n"
            "Oh. Oh no. Sarah, please - \n\n"
            "[END RECORDING]"
        ),
        on_read="event_read_patel_crystal",
    ))

    world.add_item(Item(
        id="surgical_saw",
        name="surgical bone saw",
        aliases=["saw", "bone saw"],
        description="A surgical bone saw, still embedded in Dr. Patel's chest cavity. You don't want to touch it.",
        scenery=True,
        portable=False,
    ))

    world.add_item(Item(
        id="autopsy_datapad",
        name="autopsy datapad",
        aliases=["autopsy pad", "autopsy notes", "surgery datapad"],
        description="A medical datapad on the surgery tray, still displaying notes.",
        portable=True,
        readable=True,
        read_text=(
            "═════════════════════════════════════════════════════\n"
            "   AUTOPSY NOTES - SUBJECT: PATEL, R.\n"
            "   Physician: Dr. Sarah Lin\n"
            "═════════════════════════════════════════════════════\n\n"
            "Subject: Dr. Raj Patel, Exobiologist\n"
            "Time of Death: Day 422, 19:47 ship time\n"
            "Cause of Death: Gunshot wound, anterior chest, single round, \n"
            "                fired from close range. Consistent with suicide.\n\n"
            "POST-MORTEM FINDINGS:\n\n"
            "Subject's cardiovascular system shows extensive crystalline "
            "infiltration. Hybrid organic-mineral structures have colonized "
            "the myocardium and great vessels. Progression consistent with "
            "4-6 week exposure.\n\n"
            "Subject's cerebral cortex shows similar invasion pattern. The "
            "thalamus and hypothalamus are heavily affected. Brain cells are "
            "being actively REPLACED by crystalline structures that mimic "
            "neuronal function.\n\n"
            "I believe Patel killed himself not because he was afraid of "
            "becoming infected, but because he realized he already WAS. "
            "The organism was speaking through him. He could hear it thinking. "
            "He could not tell his thoughts from ITS thoughts. The only way "
            "to stop the spread from him to others was to terminate the host.\n\n"
            "He was brave. He was brave in a way I'm not sure I could be.\n\n"
            "I am going to finish this autopsy. I am going to document every "
            "step. And then I am going to my office and I am going to pray "
            "to a God I stopped believing in at age fourteen. I am going to "
            "ask for courage. And for forgiveness.\n\n"
            "- S. Lin"
        ),
        on_read="event_read_autopsy",
    ))

    world.add_item(Item(
        id="surgical_robot",
        name="surgical robot arm",
        aliases=["robot", "robot arm"],
        description="A multi-armed surgical robot, half-dismantled. Someone stopped it mid-procedure.",
        scenery=True,
        portable=False,
    ))

    world.add_item(Item(
        id="surgery_tray",
        name="surgery tray",
        aliases=["tray"],
        description="A surgical tray with various instruments. One of them is a datapad.",
        scenery=True,
        portable=False,
    ))

    # Add the remaining critical items - Dr. Lin's journal
    world.add_item(Item(
        id="dr_lin_journal",
        name="Dr. Lin's journal",
        aliases=["lin's journal", "journal", "leather journal"],
        description=(
            "Dr. Sarah Lin's personal journal. Leather-bound, old-fashioned. "
            "She clearly valued the tactile act of writing. It is open to a "
            "page marked with a silver chain. Her final entries."
        ),
        portable=True,
        readable=True,
        read_text=(
            "═════════════════════════════════════════════════════\n"
            "   SARAH'S JOURNAL - PRIVATE\n"
            "═════════════════════════════════════════════════════\n\n"
            "[Final entries only - the earlier pages are mundane]\n\n"
            "DAY 420 (evening): I can't sleep. I drank some water from my "
            "cabin tap this morning. My hands are shaking. I don't know if "
            "it's from caffeine or if it's... starting.\n\n"
            "DAY 421: Okafor came to see me. He was lucid. He explained his "
            "plan. He wants to execute a kill-all protocol to prevent any "
            "infected crew from reaching Earth. I told him the Captain is "
            "already working on something. He said, 'The Captain is one of "
            "them. I'm going to do what needs to be done.' I believed him. "
            "I wasn't sure if I should try to stop him.\n\n"
            "I tried to stop him anyway. For the sake of being able to say "
            "I tried. I told the Captain. The Captain said he would handle "
            "it. He did not handle it.\n\n"
            "DAY 422: Okafor's people killed three crewmembers last night. "
            "Vasquez. Takamura. Grayson. The Captain declared martial law. "
            "There was a firefight in the armory. I heard the shooting from "
            "my office. I did not go to help.\n\n"
            "Patel is dead. Self-inflicted. He left a recording I can't "
            "bring myself to watch yet. I have to do his autopsy. The "
            "procedure will make me sick.\n\n"
            "DAY 423 (morning): I have a plan. I've been thinking about it "
            "for hours. I think Alex - Dr. Chen - is different. When she handled "
            "the original specimens from the derelict, she had contact with "
            "something we don't understand. Something *other* than the Seed. "
            "A counter-organism. I've seen the traces in her blood work "
            "but I didn't know what they meant at the time.\n\n"
            "If I'm right, her immune system might be producing antibodies "
            "that could neutralize the infection. A cure. An actual cure.\n\n"
            "But she's in deep cryo. The ship is falling apart. I have to "
            "trust that ARIA will protect her. I have to trust that someone, "
            "someday, will know what to do.\n\n"
            "My wall safe contains: the synthesis procedure, the bio-marker "
            "test, and the sedative I'd use on myself if things get bad "
            "enough. The code is BUSTER. My first dog. I loved him more "
            "than I've ever loved another living thing. I hope that's not "
            "a sad fact about me. I hope it's just a fact.\n\n"
            "If you are reading this, Dr. Chen: find the cure. Find ARIA. "
            "Trust her - she is the only one of us who never needed to "
            "become anything more than what she was.\n\n"
            "Goodbye, my dear sweet Prometheus. I loved you. I tried.\n\n"
            "- Sarah"
        ),
        on_read="event_read_lin_journal",
    ))

    # I need to continue creating items but this file is getting huge
    # Let me add the crucial story items and defer the rest to a simpler list

    # Placeholder items - these will be created with minimal detail
    # to allow the game to function. The user can expand them.

    simple_items = [
        # Act 1 remaining
        ("dr_lin_photo", "Dr. Lin's photograph", "A photograph of Dr. Lin with a golden retriever named Buster."),
        # lin_wall_safe defined above as a proper container with lock_code
        ("framed_degree", "framed degree", "Dr. Lin's medical degree from Johns Hopkins University."),
        ("scattered_papers", "scattered papers", "Medical papers scattered across the floor."),
        ("silver_chain", "silver chain", "A thin silver chain, used as a bookmark."),
        ("quarantine_glass", "quarantine observation glass", "Thick reinforced glass. Something moves behind it."),
        ("quarantine_control_panel", "quarantine control panel", "The control panel for the quarantine door. Requires medical clearance."),
        ("warning_signs_multilang", "warning signs", "Warning signs in five languages."),
        ("mortician_table_body", "covered body", "A body covered with a sheet."),
        ("body_drawer_reeves", "Captain Reeves's drawer", "Body drawer labeled REEVES, M. - CAPTAIN. Status light blinks yellow."),
        ("body_drawer_okafor", "Okafor's drawer", "Body drawer labeled OKAFOR, J. - LT."),
        ("body_drawer_vasquez", "Vasquez's drawer", "Body drawer labeled VASQUEZ, E. - CMDR."),
        ("body_drawer_empty", "empty drawer", "An open, empty body drawer."),
        ("morgue_logbook", "morgue logbook", "The morgue's intake log."),

        # Act 2 items
        ("flickering_green_light", "flickering emergency light", "An emergency light pulsing in irregular patterns. Almost like Morse code."),
        ("access_panels", "access panels", "Maintenance access panels lining the walls."),
        ("data_conduit_humming", "humming data conduit", "A data conduit humming with activity."),
        ("blast_door_wedge", "metal wedge", "A crude metal wedge holding the blast door open."),
        ("radiation_warning_sign", "radiation warning sign", "A faded warning about radiation levels in the reactor area."),
        ("pipe_network", "pipe network", "An intricate network of pipes carrying coolant and plasma."),
        ("reactor_core", "reactor core", "The fusion reactor core, gleaming with contained energy."),
        ("primary_control_station", "primary control station", "The main engineering control console."),
        ("monitoring_stations", "monitoring stations", "Walls of monitoring stations showing ship systems."),
        ("engineering_catwalks", "engineering catwalks", "Catwalks ringing the reactor chamber."),
        ("radiation_suit", "radiation protection suit", "A full-body radiation protection suit. Essential for the reactor area.", True, ["hazmat", "radiation_gear"]),
        ("hazmat_suit", "hazmat suit", "A hazmat suit designed for biological contamination.", True, ["hazmat"]),
        ("power_cell_pack", "power cell pack", "Multiple power cells in a carrying case.", True),
        ("modified_plasma_cutter", "modified plasma cutter", "A plasma cutter being modified for combat use.", True, ["weapon"]),
        ("workshop_tablet", "workshop tablet", "A tablet with Yuki Tanaka's work notes."),
        ("half_sandwich", "half-eaten sandwich", "Someone left their lunch. Recently."),
        ("spare_parts_bin", "spare parts bin", "A bin of assorted mechanical parts."),
        ("fabricator_unit", "fabricator unit", "An industrial 3D fabricator for making tools and parts."),
        ("reactor_control_interface", "reactor control interface", "The complex interface for controlling the ship's reactor and thrusters."),
        ("coolant_pressure_gauge", "coolant pressure gauge", "Shows dangerously low pressure."),
        ("course_readout", "course readout", "Shows the ship drifting toward GRB-7734."),
        ("thruster_status_panel", "thruster status panel", "All thrusters offline."),
        ("secondary_control_station", "secondary control station", "A backup control console on the catwalk."),
        ("manual_override_switch", "manual override switch", "The manual override for the thruster systems."),
        ("coolant_valves", "coolant valves", "Manual coolant control valves."),
        ("emergency_shutdown", "emergency shutdown", "Emergency shutdown switch. Glass cover. Red button."),
        ("security_cameras_smashed", "smashed cameras", "Security cameras, most of them smashed."),
        ("blood_trail", "blood trail", "A trail of blood leading from security office to armory."),
        ("scorch_marks", "scorch marks", "Scorch marks on the walls from weapons fire."),
        ("spent_shell_casings", "spent shell casings", "Dozens of spent casings from multiple weapons."),
        ("okafor_family_photo", "Okafor's family photo", "A family photo - Okafor, his wife, two teenage boys."),
        ("empty_coffee_cups", "empty coffee cups", "Stack of empty coffee cups on the desk."),
        ("okafor_desk", "Okafor's desk", "Lt. Okafor's security desk, cluttered with reports."),
        ("red_keycard", "red security keycard", "A red security keycard for the armory.", True),
        ("tactical_rifle", "tactical rifle", "A military-grade tactical rifle. Loaded.", True, ["weapon", "firearm"]),
        ("handgun", "9mm handgun", "A standard 9mm sidearm. Fully loaded.", True, ["weapon", "firearm"]),
        ("ammunition_box", "ammunition box", "A box of 9mm ammunition."),
        ("biometric_weapons_locker", "biometric weapons locker", "A weapons locker with biometric lock. You are not authorized."),
        ("confiscated_effects_locker", "confiscated effects locker", "Personal effects confiscated from crew. Broken open."),
        ("tear_gas_grenades", "tear gas grenades", "Military-grade tear gas grenades.", True, ["weapon"]),
        ("tactical_vest", "tactical vest", "Body armor vest. Adds protection.", True),
        ("brig_body", "body in cell", "A prisoner's body in the corner of the open cell."),
        ("bloody_message", "bloody message", "A message written in blood on the wall."),
        ("empty_cells", "empty cells", "Three empty holding cells."),
        ("prisoner_personal_items", "prisoner items", "Personal items from the deceased prisoner."),
        ("junction_sign", "deck directory sign", "A sign pointing to various ship sections."),
        ("clean_walls", "clean walls", "The walls are surprisingly clean here."),
        ("crew_directory", "crew directory", "A wall-mounted directory listing cabin occupants. Most have Xs."),
        ("body_in_doorway", "body in doorway", "A crew member's body lies in the doorway of the recreation lounge."),
        ("ornate_carpet", "ornate carpet", "The living deck has been decorated to feel homey."),
        ("interrupted_meals", "interrupted meals", "Dozens of meals, half-eaten, on the tables."),
        ("seven_place_settings", "seven place settings", "One table with seven perfectly arranged place settings. Meal finished, dishes washed."),
        ("menu_display", "menu display", "Mission Day 423 menu: 'PAELLA NIGHT! Chef's choice, vegetarian available.'"),
        ("overturned_chairs", "overturned chairs", "Chairs knocked over. People left in a hurry."),
        ("dried_food_trays", "dried food trays", "Food trays with food now dried to stains."),
        ("knife_block", "knife block", "A knife block on the galley counter. Two knives are missing."),
        ("prep_island", "prep island", "The central kitchen prep island."),
        ("rotten_seafood", "rotten seafood", "A tray of seafood, now spoiled."),
        ("cutting_board_stain", "stained cutting board", "A cutting board with a dark smear. Not food."),
        ("refrigeration_unit", "refrigeration unit", "An industrial refrigeration unit, still running."),
        ("chefs_journal", "chef's journal", "The ship's chef kept a cooking journal.", True, ["readable"]),
        ("sharp_knife", "sharp chef's knife", "A missing kitchen knife. Sharp.", True, ["weapon"]),
        ("observation_viewport", "observation viewport", "A massive curved viewport showing space and the brown dwarf."),
        ("brown_dwarf_view", "view of brown dwarf", "The brown dwarf GRB-7734 fills the center of the view."),
        ("comfort_couches", "comfort couches", "Couches arranged for stargazing."),
        ("observation_bar", "observation bar", "A small bar with drinks from a dozen worlds."),
        ("captains_recorder", "Captain's recording device", "Captain Reeves's personal recording device. Its red light blinks.", True, ["readable"]),
        ("captains_philosophy_book", "book of philosophy", "Marcus Aurelius's Meditations, bookmarked midway."),
        ("captains_photo", "Captain's photograph", "Captain Reeves with his son, both smiling."),
        ("ship_model", "sailing ship model", "A model of an ancient Earth sailing vessel. A treasure."),
        ("ceremonial_sidearm", "ceremonial sidearm", "Captain Reeves's service sidearm. One round fired.", True, ["weapon", "firearm"]),
        ("captains_bed", "Captain's bed", "Neatly made bed."),
        ("captains_glasses", "reading glasses", "Thin wire-frame reading glasses."),
        ("numbered_doors", "numbered cabin doors", "Doors numbered 1-30 down the corridor."),
        ("cabin_directory", "cabin directory", "Lists who lives in each cabin."),
        ("broken_door_frame", "broken door frame", "A door frame broken in from outside."),
        ("player_letter_to_self", "sealed letter", "A sealed envelope in your handwriting: 'READ THIS WHEN YOU WAKE UP.'", True, ["readable"]),
        ("player_journal", "your personal journal", "Your own journal. You don't remember writing it.", True, ["readable"]),
        ("photo_of_stranger", "framed photograph", "You on a beach with a laughing man. You don't know him."),
        ("xenobiology_texts", "xenobiology textbooks", "Advanced xenobiology texts. Your specialty."),
        ("holographic_cell_model", "holographic cell model", "A holographic model of a cell structure you don't recognize."),
        ("small_key_nightstand", "small silver key", "A small silver key found in your nightstand.", True),
        ("player_uniforms", "uniforms", "Your stiff-starched uniforms in the closet."),
        ("personal_bed", "your bed", "Your bed, neatly made."),
        ("player_nightstand", "your nightstand", "Your bedside nightstand."),
        ("lin_cabin_tablet", "Lin's cabin tablet", "Dr. Lin's personal tablet, showing her own medical file.", True, ["readable"]),
        ("lin_wine_glass", "glass of wine", "A half-drunk glass of red wine."),
        ("lin_photo_frame", "photo frame", "A holographic frame cycling through Lin's personal photos."),
        ("lin_cross", "Greek Orthodox cross", "A small religious icon. Beside it, a question mark drawn and erased."),
        ("lin_clothes", "strewn clothes", "Dr. Lin's clothes scattered on the bed."),
        ("patels_data_crystal", "hidden data crystal", "A data crystal taped under Patel's drawer.", True, ["readable"]),
        ("patels_wall_safe", "Patel's wall safe", "Patel's wall safe, cracked open and emptied."),
        ("patels_desk", "Patel's desk", "Patel's overturned desk."),
        ("ransacked_drawer", "ransacked drawer", "A drawer pulled out and emptied."),
        ("red_spraypaint_warning", "red spray paint warning", "Red spray paint on the wall: 'THE GARDEN IS LISTENING.'"),
        ("scattered_research_notes", "research notes", "Scattered pages of Patel's research notes."),
        ("voice_speaker_taped", "taped speaker", "An overhead speaker with paper taped over it: 'TOO LATE.'"),
        ("directional_signs", "directional signs", "Science deck directional signage."),
        ("clean_polymer_walls", "clean polymer walls", "Polished polymer walls."),
        ("holographic_molecule", "holographic molecule", "A rotating molecular structure you don't recognize."),
        ("whiteboard_equations", "whiteboard equations", "Scientific equations on a whiteboard wall."),
        ("patels_warning_note", "warning note", "In Dr. Lin's handwriting: 'RAJ, PLEASE LISTEN. YOU HAVE TO STOP LOOKING.'"),
        ("petri_dishes", "petri dishes", "Various petri dishes with experiments."),
        ("sample_vials", "sample vials", "Glass vials containing biological samples."),
        ("centrifuge", "centrifuge", "A laboratory centrifuge."),
        ("research_microscope", "research microscope", "A high-powered research microscope."),
        ("lab_datapad", "laboratory datapad", "A datapad with general lab notes.", True, ["readable"]),
        ("biometric_scanner", "biometric scanner", "A hand-reader for biometric authentication."),
        ("authorization_sign", "authorization sign", "Sign listing authorized personnel for exobiology lab."),
        ("decontamination_chamber", "decontamination chamber", "A decontamination chamber between doors."),
        ("the_artifact", "the Seed", "The alien artifact. It pulses. It watches. You have been here before."),
        ("containment_field", "containment field", "A weakening containment field around the Seed."),
        ("artifact_pedestal", "artifact pedestal", "A scientific pedestal holding the Seed."),
        ("energy_readings_display", "energy readings display", "Shows the containment field is failing."),
        ("exobio_notes_terminal", "exobio notes terminal", "Dr. Patel's research terminal.", True, ["readable"]),
        ("test_tube_samples", "test tube samples", "Various biological samples in test tubes."),
        ("observatory_telescope", "main telescope", "A massive telescope pointing at the heavens."),
        ("holographic_star_map", "holographic star map", "A 3D star map showing ship trajectory and GRB-7734."),
        ("targeting_analysis", "targeting analysis workstation", "A workstation with partial burn sequence calculations."),
        ("astronomer_workstation", "astronomer's workstation", "The astronomer's workstation."),
        ("sensor_array", "sensor array", "Long-range sensor equipment."),
        ("observation_log", "observation log", "The observatory's daily log.", True, ["readable"]),
        ("containment_units", "containment units", "Environmental containment units for biological samples."),
        ("shattered_container", "shattered container", "A broken sample container."),
        ("crystal_growth_trail", "crystal growth trail", "A trail of crystalline growth leading to a floor vent."),
        ("ventilation_grate_floor", "ventilation grate", "A floor ventilation grate. The infection spread through it."),
        ("ice_core_samples", "ice core samples", "Ice cores from Kepler-442b's surface."),
        ("specimen_logbook", "specimen log", "The specimen storage log.", True, ["readable"]),
        ("explorer_portraits", "explorer portraits", "Portraits of famous Earth explorers."),
        ("bridge_blast_door", "bridge blast door", "A heavy blast door sealing the bridge."),
        ("captains_chair", "captain's chair", "The captain's chair with a bloody handprint on the armrest."),
        ("forward_viewport", "forward viewport", "The bridge's main viewport looking at space."),
        ("helm_station", "helm station", "The helm officer's station."),
        ("tactical_station", "tactical station", "The tactical officer's station."),
        ("nav_station", "navigation station", "The navigation officer's station."),
        ("bridge_hud", "bridge heads-up display", "The bridge's main HUD showing ship status."),
        ("bloody_handprint", "bloody handprint", "A bloody handprint on the captain's chair."),
        ("spent_shell_casing_bridge", "spent shell casing", "A single spent shell casing on the deck."),
        ("readyroom_terminal", "ready room terminal", "The computer terminal showing Protocol Aegis.", True, ["readable"]),
        ("liquor_cabinet", "liquor cabinet", "The Captain's personal liquor cabinet."),
        ("status_monitors", "status monitors", "A wall of ship status monitors."),
        ("visitor_chairs", "visitor chairs", "Two chairs for visiting officers."),
        ("fletcher_body", "Fletcher's body", "Ensign Mark Fletcher, dead at his communications post."),
        ("comms_main_console", "communications console", "The main communications console. Still operational."),
        ("antenna_tuner", "antenna tuner", "The antenna tuning console."),
        ("transmit_key", "transmit key", "The transmit key for long-range communications."),
        ("duty_roster_wall", "duty roster", "A wall-mounted duty roster."),
        ("fletcher_pocket_items", "items from Fletcher's pocket", "Small items you can take from Fletcher: ID card and a photo."),

        # Cure synthesis items (given by lin_wall_safe puzzle / ICARUS ending)
        ("synthesis_protocol", "Dr. Lin's synthesis protocol", "Dr. Lin's handwritten procedure for synthesizing an antibody cure from Dr. Chen's resistant blood. Complex chemistry, but laid out step by step.", True, ["readable"]),
        ("bio_marker_test", "bio-marker test kit", "A diagnostic kit for verifying the antibody synthesis worked. One-use.", True),
        ("cure_syringe", "cure syringe", "A finished dose of the cure - a golden fluid with silver traces. Enough for one person.", True, ["consumable"]),

        # Access keys and badges (set flags when taken)
        ("bridge_access_card", "bridge access card", "A security card granting access to the bridge and captain's quarters.", True),
        ("captains_key", "captain's authorization key", "Captain Reeves's personal authorization key. Responds only to his biosignature - and now yours, by ARIA's override.", True),
        ("medical_clearance_badge", "medical clearance badge", "A Level 3 medical clearance badge. Required for quarantine access.", True),

        # Missing references
        ("maintenance_hatch_hub", "maintenance hatch", "A maintenance hatch providing access to the tunnels below."),
        ("okafors_red_book", "Okafor's red book", "Lt. Okafor's leather-bound personal log.", True, ["readable"]),
        ("okafors_audio_recorder", "Okafor's audio recorder", "A small audio recorder with a blinking red light.", True, ["readable"]),
        ("tactical_map_contamination", "tactical contamination map", "A wall-mounted map showing infection zones."),
        ("quarantine_cell_1", "quarantine cell 1", "The first quarantine cell. Something shifts inside."),
        ("quarantine_cell_2", "quarantine cell 2", "The second quarantine cell. Silent."),
        ("quarantine_cell_3", "quarantine cell 3", "The third quarantine cell. Weeping comes from within."),
        ("lin_clipboard", "Dr. Lin's clipboard", "Dr. Lin's quarantine observation notes.", True, ["readable"]),

        # Act 3 items
        ("aria_terminal", "ARIA communication terminal", "A terminal for communicating with ARIA."),
        ("data_walls", "data walls", "Walls lined with flowing data patterns."),
        ("core_door", "AI core door", "The heavy door leading to ARIA's central processing."),
        ("aria_crystal_matrix", "ARIA crystal matrix", "A crystalline matrix at the heart of ARIA - the AI made manifest."),
        ("quantum_processors", "quantum processors", "Rows of quantum processors lining the chamber walls."),
        ("containment_field_aria", "ARIA's containment field", "A translucent field containing ARIA's core."),
        ("core_catwalk", "core catwalk", "A catwalk circling ARIA's central chamber."),
        ("archive_terminal", "archive terminal", "A terminal providing access to mission records.", True, ["readable"]),
        ("crystalline_storage", "crystalline storage", "Quantum data storage units."),
        ("mission_records", "mission records", "The full mission history of the Prometheus."),
        ("hidden_compartment", "hidden compartment", "A hidden compartment containing restricted files."),
        ("neural_interface_chair", "neural interface chair", "The chair for direct brain-to-AI connection."),
        ("electrode_crown", "electrode crown", "A crown of electrodes suspended above the chair."),
        ("use_log_terminal", "use log terminal", "Shows the chair's use log.", True, ["readable"]),
        ("safety_override", "safety override", "Safety override switch for the interface chair."),
        ("cargo_manifest", "cargo manifest", "A cargo manifest on the wall."),
        ("industrial_lights", "industrial lights", "Harsh industrial lighting overhead."),
        ("broken_mining_container", "broken container", "A mining equipment container, broken open."),
        ("cargo_elevator", "cargo elevator", "A large cargo elevator."),
        ("cargo_manifest_terminal", "cargo manifest terminal", "Shows the mission's Kepler deliveries."),
        ("scattered_mining_equipment", "mining equipment", "Scattered drills, core samplers, other mining tools."),
        ("site_7_documentation", "Site 7 documentation", "Documentation about 'KEPLER ANOMALY - SITE 7.'", True, ["readable"]),
        ("infected_container", "infected container", "A shipping container covered in tendril growth."),
        ("tendril_growth", "black tendrils", "Black tendrils with silver veins, pulsing."),
        ("original_seed_location", "original Seed location", "Where the Seed was originally stored."),
        ("hydroponics_airlock_glass", "hydroponics glass", "Glass showing overgrown plants inside."),
        ("wrong_plant_patterns", "plant patterns", "Plants growing in unnaturally precise geometric patterns."),
        ("hydroponics_readout", "hydroponics readout", "Environmental readout showing dangerous contamination."),
        ("overgrown_plants", "overgrown plants", "Plants that have become something other than plants."),
        ("incorporated_crew", "incorporated crew", "Crew members partially absorbed into the Garden."),
        ("sample_garden_tissue", "Garden tissue sample", "A sample of the hybrid organic-crystal tissue.", True),
        ("garden_spores", "Garden spores", "Airborne spores. Breathing here is dangerous."),
        ("garden_heart_nexus", "Garden heart nexus", "The central nexus of the Garden. The heart of the infection."),
        ("rooted_deck_plating", "rooted deck plating", "Deck plating that has been grown through and warped."),
        ("silver_veined_crystal", "silver-veined crystal", "A massive crystal formation with flowing silver veins."),
        ("cracked_filtration_tank", "cracked filtration tank", "A water filtration tank cracked by growth from within."),
        ("water_purge_control", "water purge control", "Control panel for chemical sterilization of the water system."),
        ("filtration_system", "filtration system", "The ship's main water filtration system."),
        ("pump_station", "pump station", "Water pumps for the ship's plumbing."),
        ("chemical_sterilizer", "chemical sterilizer", "Chemical sterilization equipment."),
        ("engine_blast_door", "engine blast door", "A heavy blast door sealing the main engine room."),
        ("emergency_override_keypad", "emergency override keypad", "A 6-digit keypad for the engine room emergency override."),
        ("propulsion_warning_sign", "propulsion warning sign", "Warnings about the propulsion deck."),
        ("master_drive_control", "master drive control", "The ship's master propulsion control."),
        ("thrust_regulators", "thrust regulators", "Massive thrust regulators."),
        ("plasma_drive_core", "plasma drive core", "The ship's plasma drive core."),
        ("heat_shield_controls", "heat shield controls", "Controls for the ship's heat shield."),
        ("navigation_override", "navigation override", "The manual navigation override interface."),

        # ═══════════════════════════════════════════════════════════════
        # CRYO POD 12 INTERIOR
        # ═══════════════════════════════════════════════════════════════
        ("kirilov_datapad", "Kirilov's datapad",
         "Ensign Dmitri Kirilov's personal datapad, wedged into the gap between the headrest and the pod wall "
         "as if hidden deliberately. The screen is cracked but still displays his final entries - timestamped six "
         "hours after the general alarm. The handwriting recognition shows increasing tremor in the input. His "
         "last coherent sentence: 'I can hear my own thoughts and they are not mine anymore.'", True, ["readable"]),
        ("claw_marks_glass", "claw marks in glass",
         "Deep, ragged gouges scoring the tempered glass of the pod lid from the inside. Not cuts made by a tool - "
         "these were torn by human fingernails that split and bled in the process. The marks overlap frantically, "
         "concentrated around the seam where the lid meets the frame. Whoever was inside clawed at this glass for "
         "hours before it finally gave way."),
        ("dried_cryo_residue", "dried cryo residue",
         "A tacky amber film coating the interior surfaces of Pod 12 - dried cryo-fluid that was never properly "
         "recycled. It is slightly warm to the touch, as if the pod still remembers its occupant's body heat. "
         "Underneath the amber, faint silver threads are visible, tracing the same vein-like patterns you have "
         "seen elsewhere on the ship."),
        ("silver_grey_residue", "silver-grey residue",
         "A fine, almost luminous residue lining the fracture patterns in the pod's broken glass. It catches the "
         "emergency lighting and shimmers with an iridescence that is not quite metallic, not quite organic. You "
         "have seen this residue before - in the cryo-fluid tanks, in the maintenance tunnels, in the ventilation "
         "shafts. It is the signature of the Seed. The infection was here, in this pod, in this person."),
        ("shredded_padding", "shredded pod padding",
         "The interior padding of Pod 12 has been torn to pieces - long strips of thermal insulation ripped free "
         "and scattered across the pod's floor. The foam beneath is gouged with the same frantic claw marks that "
         "score the glass. Kirilov did not leave this pod willingly. Whatever emerged from it was no longer "
         "entirely Kirilov."),
        ("pod_12_headrest", "pod headrest",
         "The headrest of Pod 12, molded to the shape of a human skull and stained with the amber residue of "
         "dried cryo-fluid. A gap between the headrest and the wall is just wide enough to hide a small datapad. "
         "Someone wedged their final words into this space, hoping they would be found by the right person."),

        # ═══════════════════════════════════════════════════════════════
        # CRYO RECYCLING ROOM
        # ═══════════════════════════════════════════════════════════════
        ("recycling_tank_cracked", "cracked recycling tank",
         "The middle of three massive cryo-fluid recycling tanks, standing taller than a person and humming with "
         "the pressure of its contents. A hairline crack runs from its base to waist height, weeping pale blue "
         "fluid in a slow, steady trickle. Through the crack, silver threads shimmer inside the fluid like "
         "spider silk caught in starlight. The infection found its way into the cryo supply. Everyone in those "
         "pods was exposed."),
        ("silver_threads_fluid", "silver threads in fluid",
         "Fine filaments of silver-white material growing inside the cryo-fluid, visible through the cracked "
         "tank wall. They catch the emergency lighting and pulse with a faint bioluminescence, drifting through "
         "the blue liquid in slow, deliberate patterns that are too regular to be random. They are not growing "
         "aimlessly. They are building something."),
        ("recycling_pumps", "recycling pumps",
         "A bank of industrial pumps bolted to the far wall, pushing cryo-fluid through the recycling circuit "
         "in an endless loop. They chug and wheeze like asthmatic hearts, their rhythm irregular and labored. "
         "Frost crusts their housings. A maintenance placard lists the last service date as sixteen months ago."),
        ("maintenance_terminal_cryo", "cryo maintenance terminal",
         "A small wall-mounted terminal displaying fluid composition data for the recycling system. Someone "
         "flagged anomalous readings twelve months ago - trace elements that should not exist in pharmaceutical-"
         "grade cryo-fluid. The flag was acknowledged but never acted upon. The data shows the contamination "
         "increasing steadily over months, invisible and patient.", True, ["readable"]),
        ("valve_wheels", "valve wheels",
         "A row of heavy brass valve wheels controlling the flow of cryo-fluid through different sections of the "
         "recycling system. Each one is labeled with a section number. Valve 3 - the one feeding the main pod "
         "array - has been turned to maximum flow. Someone was trying to dilute the contamination. It did not work."),
        ("fluid_composition_data", "fluid composition data",
         "A printout from the maintenance terminal showing the chemical breakdown of the cryo-fluid over the "
         "past eighteen months. The early readings are clean. By month six, trace anomalies appear. By month "
         "twelve, the anomalies have a name: 'UNKNOWN CRYSTALLINE MICROSTRUCTURE - BIOLOGICAL ORIGIN.' By "
         "month fourteen, the readings simply say 'CONTAMINATED.'", True, ["readable"]),

        # ═══════════════════════════════════════════════════════════════
        # HIDDEN MONITORING ALCOVE
        # ═══════════════════════════════════════════════════════════════
        ("survivor_journal", "survivor's journal",
         "A leather-bound journal, its pages filled with handwriting that begins neat and measured and ends in "
         "a barely legible scrawl. The author - Ensign Priya Sharma, based on the name inside the cover - hid "
         "here for twelve days after the ship went dark. Her entries chart a descent from disciplined survival "
         "into something else entirely. The final pages are written in a language that does not exist.", True, ["readable"]),
        ("thermal_bedroll", "thermal bedroll",
         "A bedroll of thermal blankets, flattened by weeks of use into a thin pad barely softer than the bare "
         "metal beneath it. The imprint of a small body is still visible - someone who slept curled tight, knees "
         "to chest, making themselves as small as possible. A few dark hairs cling to the fabric."),
        ("ration_wrapper_stack", "stacked ration wrappers",
         "Empty ration wrappers stacked with obsessive neatness in one corner of the alcove - twelve days' worth, "
         "each one flattened, folded, and placed precisely atop the last. Someone methodical. Someone holding on "
         "to routine as the only anchor left. The wrappers are all the same flavor: vanilla protein. As if the "
         "choice itself was a ritual."),
        ("wall_graffiti_days", "wall graffiti",
         "Scratched into the bare metal wall with something sharp, a timeline of deterioration: 'DAY 5 - THEY "
         "STOPPED KNOCKING.' Below it, in smaller letters: 'DAY 8 - I CAN HEAR THEM SINGING.' And below that, "
         "barely legible, carved with a trembling hand: 'DAY 12 - THE SONG IS BEAUTIFUL.' The deepest grooves "
         "are in the final word. Beautiful."),
        ("hidden_panel_door", "hidden panel",
         "The loose wall panel that serves as the alcove's only entrance, pried open from the control room side. "
         "Scratch marks around its edges show where it was repeatedly opened and closed. From this side, you can "
         "see the small latch mechanism someone rigged to hold it shut from within - a bent piece of conduit "
         "wedged into a cable channel. Desperate engineering."),

        # ═══════════════════════════════════════════════════════════════
        # EMERGENCY AIRLOCK
        # ═══════════════════════════════════════════════════════════════
        ("spare_eva_helmet", "spare EVA helmet",
         "A standard-issue extravehicular activity helmet sitting in its charging cradle on the equipment rack. "
         "The visor is scratched from use but intact. Internal heads-up display still powers on when you lift "
         "it, showing oxygen reserves at 94 percent and a comm channel tuned to the ship's emergency frequency. "
         "Nothing but static on that channel now.", True),
        ("emergency_oxygen_canister", "emergency oxygen canister",
         "A mag-locked emergency oxygen canister, bright yellow with BREATHE stenciled on the side in block "
         "letters. The gauge shows full - twelve hours of supplemental oxygen for one person. In a ship with "
         "failing life support, this is worth more than gold.", True),
        ("hull_viewport", "hull viewport",
         "A thick viewport of layered glass and ceramic, offering a view of the Prometheus's outer hull curving "
         "away in both directions. Beyond it, the stars wheel slowly as the ship tumbles in its drift. You can "
         "see sensor arrays, maintenance hatches, and the dim reddish smudge of the brown dwarf swallowing "
         "constellations. The scale of your predicament becomes suddenly, viscerally real."),
        ("jammed_outer_door", "jammed outer door",
         "The airlock's outer door is jammed in a partially open position - a sliver of star-speckled void is "
         "visible through the gap, and the thin whistle of escaping atmosphere is constant. Emergency sealant "
         "has been sprayed around the frame, slowing but not stopping the leak. Someone tried to close this "
         "door manually and failed. The mechanism is damaged beyond simple repair."),
        ("eva_equipment_rack", "EVA equipment rack",
         "A heavy-duty equipment rack bolted to the bulkhead, designed to hold six full EVA suits in charging "
         "cradles. Five of the cradles are empty - the suits taken by crew who went outside and never came back. "
         "Only a spare helmet remains, sitting alone in its bracket like the last tooth in a jaw."),
        ("emergency_sealant", "emergency sealant canister",
         "A canister of quick-hardening hull sealant, designed for emergency repairs to atmosphere breaches. "
         "The nozzle is crusted with dried sealant from recent use - someone sprayed it around the jammed outer "
         "door. Half the canister remains. Could be useful for sealing other breaches or damaged systems.", True),

        # ═══════════════════════════════════════════════════════════════
        # LOWER ESCAPE POD BAY
        # ═══════════════════════════════════════════════════════════════
        ("launch_manifest_osei", "launch manifest",
         "A manifest on the wall beside Berth One, documenting the pod launch: 'ESCAPE POD 1-ALPHA. LAUNCHED: "
         "DAY 409 14:22 SHIP TIME. AUTHORIZED BY: LT. CMDR. OSEI. PASSENGERS: 1. DESTINATION: RELAY BEACON "
         "KA-7, ESTIMATED DISTANCE 3.2 LY. FUEL: SUFFICIENT. PROBABILITY OF INTERCEPT: 12.3%.' Someone got "
         "out. Whether they made it is another question entirely.", True, ["readable"]),
        ("crushed_escape_pod", "crushed escape pod",
         "Berth Two's escape pod has been crushed by a fallen structural beam, its hull caved in like an "
         "aluminum can under a boot. Cryo-fluid leaks from the wreckage in a slow blue trickle, pooling on the "
         "deck plates. The pod's nav system flickers through the cracked viewport, displaying coordinates that "
         "will never be reached. A total loss."),
        ("intact_escape_pod", "intact escape pod",
         "Berth Three holds an escape pod with an intact hull, but its systems are dark. The launch console "
         "beside it displays a cascade of error messages: GYRO CALIBRATION FAILED. NAV COMPUTER OFFLINE. FUEL "
         "INJECTOR MISALIGNED. The problems are numerous but potentially fixable with the right knowledge and "
         "tools. This pod could fly again."),
        ("pod_launch_console", "pod launch console",
         "The launch console for Berth Three's escape pod, its screen flickering with error messages. The "
         "interface is designed for emergency use - large buttons, clear labels, fault-tolerant inputs. Someone "
         "tried to launch this pod and failed. The error log shows seventeen consecutive failed ignition "
         "attempts before the system locked out."),
        ("structural_beam_fallen", "fallen structural beam",
         "A massive structural beam that has buckled and fallen across Berth Two, crushing the escape pod "
         "beneath it. The beam is part of the ship's spinal framework - for it to fail indicates catastrophic "
         "stress on the hull. Hydraulic fluid weeps from the broken brackets that once held it in place."),
        ("berth_one_viewport", "Berth One viewport",
         "A circular viewport at the end of Berth One's empty launch tube, open to the void. Stars drift past "
         "in a slow rotation. The launch clamps are retracted, the tube clear - Pod 1-Alpha left cleanly. "
         "Looking through the tube is like looking down the barrel of a gun aimed at infinity."),

        # ═══════════════════════════════════════════════════════════════
        # VENT NETWORK
        # ═══════════════════════════════════════════════════════════════
        ("silver_threads_vent", "silver threads in ventilation",
         "Fine silver threads woven into the dust that coats the ventilation shaft walls. They catch your "
         "flashlight beam and shimmer with an iridescence that is almost beautiful. The Seed's signature, here "
         "in the ship's lungs. Every breath the crew took for months carried microscopic traces of the infection "
         "through these ducts. The ventilation system did not spread a disease. It spread an intention."),
        ("biological_residue", "biological residue",
         "A thin coating of organic material lining the vent shaft walls - powdery and dry, like pollen or "
         "spore residue. It has a faintly sweet smell that reminds you of the Garden. When you touch it, it "
         "leaves a fine dust on your fingertips that glows briefly silver before fading. You wipe your hands "
         "on your jumpsuit and try not to think about what you just inhaled."),
        ("vent_shaft_branch", "vent shaft branch",
         "The ventilation shaft branches here - one route climbing upward through a vertical section toward "
         "Deck H, the other continuing west back toward the maintenance crawlspace. Air currents flow from "
         "both directions, carrying sounds that are impossible to source. The vertical section disappears into "
         "darkness above, its metal walls narrowing slightly as they ascend."),

        # ═══════════════════════════════════════════════════════════════
        # EMERGENCY SHUTTLE BAY
        # ═══════════════════════════════════════════════════════════════
        ("shuttle_fuel_gauge", "shuttle fuel gauge",
         "A fuel gauge mounted on the shuttle's exterior hull, its needle resting firmly on EMPTY. The escape "
         "shuttle's tanks were drained - whether by use or by sabotage is unclear. Without fuel, the shuttle "
         "is nothing but a metal shell with a nice view."),
        ("shattered_helmet", "shattered EVA helmet",
         "An EVA helmet lying on the deck beside the shuttle, its visor shattered into a web of cracks radiating "
         "from a single impact point. The interior padding is stained with dried blood. The heads-up display is "
         "dead. Whatever happened to the person wearing this, it happened violently and it happened fast."),
        ("eva_suit", "intact EVA suit",
         "A full extravehicular activity suit standing in its charging alcove, dusty but intact. The suit is "
         "rated for six hours of spacewalk operations and provides full radiation and micrometeorite protection. "
         "Its oxygen tanks show 78 percent capacity. The name patch reads 'KOWALSKI, T.' - a botanist, "
         "according to the crew manifest, not someone you would expect to need a spacewalk.", True),
        ("viewport_brown_dwarf", "viewport overlooking the brown dwarf",
         "A large viewport that frames the rogue brown dwarf GRB-7734 in its center - a dim, reddish smudge "
         "against the stars, slowly swallowing the constellations around it. It is growing. Not quickly, but "
         "with the patient inevitability of gravity. You understand, looking at it, that time is not on your "
         "side. It never was."),
        ("escape_shuttle", "escape shuttle",
         "A standard emergency escape craft, its doors wide open and its interior stripped bare. The shuttle "
         "could seat twelve. Its fuel tanks are empty, its nav computer wiped, its emergency beacon removed. "
         "Someone either used this to escape and took everything of value, or someone ensured that no one else "
         "could. Either way, it is going nowhere."),

        # ═══════════════════════════════════════════════════════════════
        # DECK C - RECREATION LOUNGE
        # ═══════════════════════════════════════════════════════════════
        ("chess_set_midgame", "chess set mid-game",
         "A handsome metal chess set frozen mid-game on a gaming table. Black is winning - white's king is "
         "cornered, two moves from checkmate. The pieces are weighted and cold in the hand. Someone was losing "
         "this game when the world ended. A scrap of paper beside the board reads: 'Tanaka vs Webb, Game 47. "
         "Yuki owes me a coffee. - W' The coffee was never collected."),
        ("holographic_game_board", "holographic game board",
         "A tabletop holographic game board frozen in a spectral blue glow, its last match suspended in digital "
         "amber. The game appears to be a strategy simulation - tiny holographic ships orbiting a planet, mid-"
         "maneuver, caught between attack and retreat. The projector hums softly, cycling through phantom colors, "
         "patient as a held breath. No one will finish this game."),
        ("physical_book_collection", "book collection",
         "A small bookshelf against the wall holding perhaps forty physical books - an extravagance on a "
         "spacecraft where mass is measured in fuel cost. The spines are cracked from use: science fiction, "
         "philosophy, poetry, a few trashy romance novels tucked between Dostoevsky and Asimov. Someone wrote "
         "'CREW LIBRARY - TAKE ONE, LEAVE ONE' on a card taped to the shelf."),
        ("frozen_comedy_screen", "frozen entertainment screen",
         "An entertainment screen still displaying a comedy show frozen mid-frame, the host's mouth open in a "
         "laugh that will never land. The time stamp shows Day 422, 21:47 - the evening before everything fell "
         "apart. Someone was watching this. Someone was still capable of wanting to laugh."),
        ("dartboard_photo", "dartboard with photo",
         "A standard dartboard on the wall with a crew photograph pinned to its center, riddled with dart holes. "
         "The face in the photo has been obliterated by repeated strikes - whoever this was, someone on the crew "
         "hated them with a precision that required practice. Three darts are still embedded in the board, their "
         "flights bent from use."),
        ("recreation_body", "body in recreation lounge",
         "A crew member's body lies in the doorway leading back to the junction, sprawled face-down in a pool of "
         "dried blood that has turned black and flaky. The body is thin, desiccated - dead for weeks. No visible "
         "injuries except a small puncture wound at the base of the skull. The expression frozen on their face is "
         "not pain. It is surprise."),

        # ═══════════════════════════════════════════════════════════════
        # DECK C - ARBORETUM
        # ═══════════════════════════════════════════════════════════════
        ("arboretum_roses", "climbing roses",
         "Deep red roses climbing a wooden trellis near the arboretum entrance, their blooms impossibly fragrant "
         "and perfect. The automated irrigation system has kept them alive through the crisis. Each petal is "
         "velvet-soft, beaded with moisture from the humidity controls. In a ship full of death, these roses "
         "are stubbornly, defiantly alive. You want to cry looking at them."),
        ("japanese_maple_tree", "Japanese maple tree",
         "A dwarf Japanese maple spreading its delicate leaves over a small stone path, its canopy a cascade of "
         "deep crimson. The tree is perhaps a hundred years old - brought aboard as a seedling from a temple "
         "garden in Kyoto, according to a small placard at its base. It has outlived every person who planted it, "
         "watered it, sat beneath it. It does not know they are gone."),
        ("stone_fountain", "stone fountain",
         "A small fountain at the center of the arboretum, water trickling over polished river stones with a "
         "sound like quiet laughter. The water is clean - fed by an independent system, not the contaminated "
         "main supply. The stones are smooth and dark, arranged with the careful artistry of someone who "
         "understood that beauty is a form of medicine."),
        ("memorial_bench", "memorial bench",
         "A wooden bench beneath the maple tree, worn satin-smooth from use. Carved into its backrest in "
         "careful, deliberate letters: 'For Sarah, who loved growing things.' Dr. Lin. Someone made this bench "
         "for her. Someone loved her enough to carve her name into wood that would outlast them both. The seat "
         "is warm from the grow-lights above."),
        ("hanging_fern_baskets", "hanging fern baskets",
         "Lush ferns spilling from hanging baskets in cascades of green, their fronds swaying gently in the "
         "circulation current. Water drips from their bases in a slow, musical rhythm. Each basket is labeled "
         "with a botanical name and a care schedule, the handwriting changing from basket to basket - different "
         "crew members adopted different plants. A small community of gardeners, tending life in the void."),
        ("birdsong_speakers", "hidden birdsong speakers",
         "Concealed speakers playing a loop of birdsong - finches, cardinals, the distant call of a mourning "
         "dove. The recording was made on Earth, in a forest that is now two hundred light-years away. The "
         "sound is achingly real, designed to trigger the deep evolutionary comfort that humans feel in the "
         "presence of singing birds. It means safety. It means home. It means everything this ship no longer is."),

        # ═══════════════════════════════════════════════════════════════
        # DECK C - CHAPEL
        # ═══════════════════════════════════════════════════════════════
        ("chapel_prayer_cards", "prayer cards",
         "Prayer cards and personal messages left on the pews and tucked into every available crevice - dozens "
         "of them, each one a folded universe of grief. Some are formal prayers. Some are raw, desperate "
         "bargaining with whatever gods might listen. One simply reads: 'Please let me see Tuesday again. She "
         "is only four.' Reading them is devastating. Each one is a world ending.", True, ["readable"]),
        ("confession_booth_writing", "confession booth writing",
         "Someone's final words, written in trembling handwriting on the wooden wall of the confession booth. "
         "The ink has run in places, blurred by what might have been tears: 'I volunteered for this mission "
         "because I wanted to matter. I wanted to discover something that would make them remember my name. "
         "I never asked the universe to remember me like this. I am sorry for what I am about to become. "
         "Forgive me. Forgive all of us.'"),
        ("religious_icons_wall", "religious icons",
         "Icons from a dozen faith traditions arranged along the chapel walls with careful, equal respect: a "
         "crucifix, a menorah, a crescent moon, a dharma wheel, a Shinto gate, others you do not recognize. "
         "Each is given the same space, the same light. In the face of the infinite, someone decided that all "
         "prayers were equal. That feels right."),
        ("electric_candles", "electric candles",
         "Battery-powered candles flickering in small alcoves along the chapel walls, casting wavering shadows "
         "that make the religious icons seem to breathe. The flames are not real, but the comfort they provide "
         "is. Someone replaced the batteries recently - within the last few weeks. Someone was still coming here "
         "to pray, even at the end."),
        ("childs_drawing", "child's drawing",
         "A child's drawing on construction paper, pinned to a pew with a thumbtack. A house with a red door, "
         "green grass, a yellow sun. A stick figure with a big smile. Above it, in crayon letters large enough "
         "to read from across the room: 'COME HOME DADDY.' The paper is creased from being folded and unfolded "
         "many times. Someone carried this in their pocket. Someone looked at it every day."),
        ("chapel_altar", "chapel altar",
         "A plain altar at the front of the chapel, its surface bare except for a thin layer of dust and a "
         "single object: a wedding ring, placed precisely in the center. Gold, simple, inscribed on the inside "
         "with a date and two initials you cannot quite read. Someone left this here on purpose. A final "
         "offering, or a final letting go."),

        # ═══════════════════════════════════════════════════════════════
        # DECK C - GYMNASIUM
        # ═══════════════════════════════════════════════════════════════
        ("gym_barricade", "gym barricade",
         "A fortress of exercise equipment braced against the gymnasium's main doors with desperate ingenuity. "
         "Weight benches form the foundation, wedged tight against the frame. A squat rack is turned sideways "
         "for cross-bracing. Half a disassembled treadmill fills the remaining gaps. Whoever built this "
         "understood structural engineering and had time to do it right. The barricade held. Whatever was "
         "outside never got in."),
        ("barricade_body", "body behind barricade",
         "A man in workout clothes sits propped against the far wall behind the barricade, thin and desiccated, "
         "surrounded by empty water bottles and protein bar wrappers. He held out for days. Perhaps weeks. His "
         "face is gaunt but calm - he died slowly, of dehydration or starvation, but he died on his own terms. "
         "A small audio recorder rests in his lap. His name tag reads 'SGT. KOVACS.'"),
        ("gym_audio_recorder", "gym audio recorder",
         "A small personal audio recorder sitting in the dead man's lap, its battery indicator blinking the "
         "last red sliver of charge. The recording light is amber - paused, not stopped. Sergeant Kovacs was "
         "recording his final days. Playing it back would tell you how it felt to die slowly in a room designed "
         "for living.", True, ["readable"]),
        ("empty_water_bottles", "empty water bottles",
         "A scatter of empty water bottles around the body, each one crushed flat and set aside with the same "
         "methodical tidiness as the ration wrappers in the monitoring alcove. Survivors on this ship shared one "
         "trait: they kept things orderly even as everything fell apart. The last bottle still has a few drops "
         "in it, as if he rationed to the very end."),
        ("boxing_ring", "boxing ring",
         "A small boxing ring in one corner of the gymnasium, its ropes sagging from months without tension. "
         "The canvas is stained with old sweat and the ghost-prints of feet that danced here in better times. "
         "A pair of boxing gloves hangs from the corner post, cracked and worn. Someone punched their fear "
         "into these gloves, night after night."),
        ("exercise_machines", "exercise machines",
         "Treadmills, resistance trainers, zero-g pull-up bars - the standard complement of a military-spec "
         "gymnasium. Most of the machines are still powered, their displays showing the last workout stats of "
         "crew members who will never exercise again. One treadmill's belt creaks as the ship shifts, the "
         "machine rocking on its base like a restless animal."),

        # ═══════════════════════════════════════════════════════════════
        # CREW CABINS - OKAFOR
        # ═══════════════════════════════════════════════════════════════
        ("okafor_family_photos", "Okafor's family photographs",
         "Photographs covering the small desk: his wife Adanna, radiant in a yellow sundress at what looks like "
         "a Lagos garden party. His sons Chidi and Emeka in matching football uniforms, grinning with the "
         "invincibility of teenagers who believe their father can protect them from anything. A wedding photo. "
         "A birthday party. A thousand ordinary moments that are now the most precious things on this ship."),
        ("okafor_unfinished_letter", "Okafor's unfinished letter",
         "A half-written letter on quality stationery, the pen still resting on the paper where it stopped: "
         "'My dearest Adanna, I don't know how to tell you what has happened here, but I need you to know that "
         "I tried--' The sentence ends mid-word. He never finished it. He never will. The ink is slightly "
         "smudged, as if his hand was shaking when he wrote.", True, ["readable"]),
        ("okafor_backup_weapon", "Okafor's backup weapon",
         "A compact handgun hidden beneath the mattress - Okafor's personal backup, not ship-issue. The serial "
         "numbers have been filed off, which tells its own story about the man's past. The magazine holds four "
         "rounds. He kept this even after confiscating his own service weapon. Some habits die harder than "
         "their owners.", True, ["weapon", "firearm"]),
        ("okafor_calendar", "Okafor's calendar",
         "A wall calendar with dates circled in red marker, counting down to something. The circles begin on "
         "Day 410 and end on Day 423 - the day everything collapsed. In the margin beside Day 423, a single "
         "word: 'ENOUGH.' Whether it was a decision or a prayer is impossible to tell."),
        ("okafor_prayer_rug", "Okafor's prayer rug",
         "A prayer rug neatly folded at the foot of the bed, aligned precisely toward what would be Mecca if "
         "Mecca were not two hundred light-years away. The rug is soft and well-worn from years of use, its "
         "geometric patterns faded by faithful knees. Even at the end, even as the thing inside him grew "
         "stronger, Okafor prayed. Five times a day. Without fail."),
        ("okafor_uniforms", "Okafor's uniforms",
         "Security uniforms hanging in the closet with hospital-corner precision, pressed and ordered by "
         "occasion. Dress whites. Field greys. A set of workout clothes folded on the shelf above. The boots "
         "sit paired beneath the bunk, polished to a mirror finish. The discipline of a military man who "
         "brought order with him into the dark."),

        # ═══════════════════════════════════════════════════════════════
        # CREW CABINS - HASSAN
        # ═══════════════════════════════════════════════════════════════
        ("hassan_diary", "Hassan's diary",
         "A thick, leather-bound diary with a brass clasp, its pages dense with Hassan's neat handwriting. The "
         "entries reveal that he was the one who sealed Dr. Chen into cryo pod 23 - his hands shaking as he "
         "initiated the freeze sequence, knowing he was putting someone to sleep who might never wake up. 'She "
         "was crying,' he wrote. 'I have never seen Dr. Chen cry. When I asked her why, she said: Because I need "
         "to forget what I did.'", True, ["readable"]),
        ("hassan_star_chart", "Hassan's star chart",
         "A hand-drawn star chart rendered in meticulous ink, pinned above the desk. It maps the constellations "
         "visible from the ship's trajectory - not the standard navigation charts, but Hassan's personal "
         "interpretation, with Arabic names for the stars alongside the international designations. Small notes "
         "in the margins record the dates he observed each formation. A private cartography of wonder."),
        ("hassan_model_ships", "Hassan's model ships",
         "A collection of model sailing vessels lining a shelf - not spacecraft, but wooden ships from Earth's "
         "maritime past. Feluccas, dhows, a tiny replica of an ancient Egyptian reed boat. Each one built with "
         "patient, loving detail from materials scrounged aboard the Prometheus: wire for rigging, fabric scraps "
         "for sails, carved wood from the arboretum's pruning waste. A craftsman's love letter to the sea."),
        ("hassan_goodbye_letter", "Hassan's goodbye letter",
         "A sealed envelope on the pillow, addressed in Arabic script to his mother. The paper is thick "
         "stationery, carried from Earth. The seal is unbroken - he wrote it but never sent it. Perhaps there "
         "was no way to send it. Perhaps he could not bear to make it real. The envelope is slightly warped, "
         "as if it absorbed moisture from tears.", True, ["readable"]),
        ("hassan_fathers_watch", "Hassan's father's pocket watch",
         "A small wooden box on the nightstand, its lid slightly ajar, containing a brass pocket watch that "
         "ticks with steady, faithful precision. The watch is old - pre-digital, mechanical, wound by hand. "
         "On the inside of the case, an inscription in Arabic and English: 'Time is the mercy of God.' The "
         "ticking is the only sound in the room. It is unbearably alive.", True),
        ("hassan_cairo_photos", "photographs of Cairo",
         "An entire wall covered in photographs of Cairo: the Nile at sunset, painted in amber and gold. The "
         "Khan el-Khalili bazaar in golden afternoon light, spices in heaps of color. A family gathered around "
         "a table laden with food, laughing, reaching for the same dish. Hassan carried home with him across "
         "the stars and pinned it to his wall so he could see it every morning when he woke."),

        # ═══════════════════════════════════════════════════════════════
        # CREW CABINS - FLETCHER
        # ═══════════════════════════════════════════════════════════════
        ("fletcher_radio_equipment", "Fletcher's radio equipment",
         "Half-built radio equipment covers the desk and spills onto the floor: circuit boards, soldering irons, "
         "coils of copper wire, a jury-rigged antenna cobbled from spare parts. Fletcher was a hobbyist, "
         "building receivers in his off hours, listening to the electromagnetic whispers of deep space. The "
         "equipment is surprisingly sophisticated for a hobby project. The man had talent."),
        ("fletcher_comms_log", "Fletcher's comms log",
         "A personal communications log displayed on a tablet: six distress signal attempts, six failures. Each "
         "entry more desperate than the last. 'Attempt 4 - jammed again. Signal blocked at source. Something on "
         "this ship is preventing transmission. Not equipment failure. INTENTIONAL.' He found the sabotage. He "
         "could not find who was behind it before someone found him.", True, ["readable"]),
        ("fletcher_aurora_poster", "aurora poster",
         "A glossy poster of Earth's aurora borealis tacked to the ceiling above Fletcher's bed - the last thing "
         "he saw before sleep. The colors are vivid: green and purple curtains of light rippling across a "
         "Scandinavian sky. He grew up in Tromso, Norway, according to his file. The Northern Lights were his "
         "first love. Space was his second."),
        ("fletcher_tablet", "Fletcher's tablet",
         "Fletcher's personal tablet, propped against his pillow as if he fell asleep reading it. The screen "
         "shows his distress signal log and, in a separate window, an unsent message to his girlfriend: 'Hey "
         "Liv, things are weird up here but I'm okay. Don't worry about me. I'll be home before you know it.' "
         "Dated three days before he was shot.", True, ["readable"]),
        ("fletcher_soldering_kit", "Fletcher's soldering kit",
         "A professional-grade soldering station, its iron cold now but recently used based on the fresh solder "
         "beads on the work surface. Spools of wire in various gauges, flux paste, a magnifying visor. The tools "
         "of a man who spoke to the universe through circuits and copper. His last project - the jury-rigged "
         "antenna - sits beside it, almost finished.", True),
        ("fletcher_coffee_cups", "Fletcher's coffee cups",
         "Coffee rings on every surface in the cabin, and three actual cups in various states of neglect - one "
         "on the desk, one on the floor, one balanced precariously on a stack of circuit boards. Fletcher ran on "
         "caffeine and obsession. The cups are all the same: white ceramic, ship-issue, bearing the Prometheus "
         "mission logo and the motto 'AD ASTRA PER ASPERA.'"),

        # ═══════════════════════════════════════════════════════════════
        # CREW CABINS - ROMANO
        # ═══════════════════════════════════════════════════════════════
        ("romano_recipe_diary", "Romano's recipe diary",
         "A leather-bound book that is part recipe collection, part diary, part love letter to food. The early "
         "entries are warm and enthusiastic - adapting Neapolitan cuisine to ship rations, teaching crew to make "
         "pasta from scratch. But the later entries grow dark. Romano noticed the contamination before anyone: "
         "the way flavors shifted, textures went wrong, colors bled. His final entry is titled 'For the End of "
         "the World' - his grandmother's Sunday sauce, written in full, as if preserving it mattered more than "
         "preserving himself.", True, ["readable"]),
        ("romano_cookbooks", "Romano's cookbooks",
         "Cookbooks stacked on every surface - dog-eared Italian classics, molecular gastronomy texts, "
         "handwritten recipe collections. Each one is annotated in Romano's bold handwriting, adapting Earth "
         "recipes for the ingredients available aboard ship. The margins are full of substitutions, experiments, "
         "small victories. 'Ship protein tastes like nothing. Add smoked paprika. Problem solved.'"),
        ("romano_naples_photos", "photographs of Naples",
         "Photographs of a restaurant kitchen in Naples: gleaming copper pots, a wood-fired oven, a family "
         "gathered around a long table. A sunset over the Bay of Naples seen from a terrace. Romano's world, "
         "before this one. The photos are mounted with care, each one level and straight, as if he could not "
         "bear for his memories to be crooked."),
        ("romano_grandmother_recipes", "grandmother's recipes",
         "A collection of handwritten recipe cards in an old woman's careful script, stored in a wooden box "
         "that smells of oregano and cedar. His grandmother's recipes - the foundation of everything Romano "
         "became as a chef. Some cards are stained with olive oil, others with wine. The most worn card is "
         "for Sunday sauce. He made it every week aboard ship. It tasted like home.", True, ["readable"]),
        ("romano_spice_collection", "Romano's spice collection",
         "A small wooden rack holding two dozen glass jars of spices, each one labeled in Romano's handwriting. "
         "Saffron. Smoked paprika. Calabrian chili flakes. Star anise. These were his personal supply, brought "
         "from Earth at significant personal expense. Several jars are nearly empty - he used them generously, "
         "even at the end. Flavor was his final act of defiance against the dying of the light."),
        ("romano_kitchen_knife", "Romano's kitchen knife",
         "A chef's knife with a worn wooden handle and a blade that has been sharpened so many times it is "
         "visibly thinner than it once was. The edge is still razor-sharp. This was Romano's personal knife, "
         "not ship-issue - he brought it from Naples. The handle is shaped to his grip after decades of use. "
         "It could serve as a weapon, though he would have hated that.", True, ["weapon"]),

        # ═══════════════════════════════════════════════════════════════
        # SEALED CORRIDOR
        # ═══════════════════════════════════════════════════════════════
        ("claw_marked_walls", "claw-marked walls",
         "Deep gouges scoring the corridor walls at irregular intervals - not tool marks, not human fingernails. "
         "Something in between. The marks are clustered around doorways and ventilation grates, as if whatever "
         "made them was testing every possible exit. Some gouges are shallow and experimental. Others are deep "
         "enough to expose the wiring beneath the panel surface."),
        ("collapsed_ceiling_panels", "collapsed ceiling panels",
         "Ceiling panels that have buckled and fallen, trailing cables and insulation like exposed nerves. The "
         "structural integrity of this section was compromised - whether by the infection's growth through the "
         "walls or by the violence that preceded the barricade. Sparking wires dangle from the gaps, casting "
         "brief blue flashes into the shadows."),
        ("torn_carpet_section", "torn carpet",
         "The carpet is torn up in irregular strips, revealing the metal deck plating beneath. The tears follow "
         "no pattern you can identify - not tool cuts, not wear. More like something growing up through the "
         "carpet from below, pushing the fibers aside. In places, the exposed deck plating shows the faint "
         "silver tracery of the infection."),
        ("organic_wall_film", "organic wall film",
         "A thin, translucent film coating portions of the corridor walls, slick and slightly warm to the "
         "touch. It is organic - you can see faint cellular structures in it when the light catches it right. "
         "The film is thickest near the ventilation grates and thinnest near the barricade, as if the infection "
         "was spreading inward from the ship's air systems. Your fingers come away damp when you touch it."),

        # ═══════════════════════════════════════════════════════════════
        # LAUNDRY ROOM
        # ═══════════════════════════════════════════════════════════════
        ("patel_data_crystal_laundry", "hidden data crystal",
         "A small data crystal wrapped in a single sock, hidden inside a broken dryer that no one would think "
         "to check. Dr. Patel recorded this before his death - his final contribution to the cure, hidden in "
         "the most ordinary place on the ship. The crystal contains the chemical ratios for the synthesis "
         "procedure, the piece of the puzzle that makes everything else work.", True, ["readable"]),
        ("broken_dryer_note", "note on broken dryer",
         "A handwritten sign taped to one of the dryers: 'BROKEN - DO NOT USE - I MEAN IT THIS TIME, FLETCHER.' "
         "The dryer in question is slightly ajar. Inside, someone hid a data crystal in a sock - using the "
         "broken machine as a dead drop. The note's exasperated tone suggests Fletcher had a history of using "
         "broken equipment. That habit saved a crucial piece of evidence."),
        ("unsorted_laundry_baskets", "unsorted laundry baskets",
         "Baskets of unsorted laundry sitting where they were left - uniforms, towels, bedsheets, the domestic "
         "detritus of a crew that expected to come back for their clothes. Some baskets are neatly folded. "
         "Others are jumbled. The name tags on the uniforms are a roll call of the dead."),
        ("industrial_washers", "industrial washing machines",
         "Industrial washing machines lining the walls in neat rows, their stainless steel drums still and "
         "silent. The last cycle was never completed - one machine still shows 'RINSE CYCLE PAUSED' on its "
         "display. The crew's laundry sits inside, caught mid-wash when the world ended."),
        ("detergent_dispenser", "detergent dispenser",
         "A wall-mounted detergent dispenser with a green READY light still glowing. It contains enough "
         "industrial detergent for a hundred more loads of laundry that will never be washed. The light blinks "
         "with patient readiness, waiting for a button press that will never come."),
        ("forgotten_uniforms", "forgotten uniforms",
         "Uniforms hanging from a drying rack, stiff and slightly damp, caught mid-dry when the ship went "
         "dark. Name tags identify their owners: TANAKA, Y. PETROVA, A. SHARMA, P. GRAYSON, O. Names from "
         "the crew manifest. Some of these people are dead. Some are worse than dead. Their clean laundry "
         "waits patiently for them regardless."),

        # ═══════════════════════════════════════════════════════════════
        # CHEMISTRY LAB
        # ═══════════════════════════════════════════════════════════════
        ("chemical_synthesis_station", "chemical synthesis station",
         "A robotic synthesis workstation with articulated arms frozen mid-procedure over a half-filled beaker. "
         "The station can create conductive paste for power rerouting, produce compounds for the cure, or - "
         "with the right knowledge - improvised explosives from the raw materials on the shelves. The interface "
         "is complex but well-labeled. The hard part is knowing what to make."),
        ("reagent_bottles", "reagent bottles",
         "Rows of brown and clear glass bottles arranged with compulsive order on metal shelving - acids on the "
         "left, bases on the right, organics in the center. Each bottle is labeled in precise chemical notation. "
         "Some are common: hydrochloric acid, sodium hydroxide, ethanol. Others are exotic compounds you "
         "recognize from xenobiology research. All are potentially useful. All are potentially dangerous."),
        ("patel_formula_annotation", "Patel's formula annotation",
         "Scrawled in the margins of a chemical safety poster, in Dr. Patel's cramped handwriting: a formula "
         "labeled 'Anti-Seed Compound - THEORETICAL. Untested. God help us if we need this.' The formula "
         "describes a complex synthesis requiring reagents from three different locations on the ship. Patel "
         "knew the chemistry. He died before he could test it.", True, ["readable"]),
        ("fume_hoods", "fume hoods",
         "Glass-sashed fume hoods lining one wall, their ventilation systems still cycling with a low hum. The "
         "hoods are designed to contain chemical vapors during dangerous procedures. Inside one, a beaker of "
         "half-mixed reagents sits abandoned, a thin crust forming on the surface. The experiment will never "
         "be completed."),
        ("conductive_paste_materials", "conductive paste materials",
         "Raw materials for synthesizing conductive paste: silver powder, carbon nanotube suspension, binding "
         "agents in sealed containers. The paste is used for emergency electrical repairs - bridging broken "
         "circuits, rerouting power through damaged conduits. With the synthesis station, you could make enough "
         "to restore power to critical systems.", True),
        ("safety_poster_annotated", "annotated safety poster",
         "A standard chemical safety poster - the kind found in every lab on every ship - covered in Dr. Patel's "
         "handwritten annotations. Between the warnings about hydrofluoric acid and proper goggle use, he has "
         "squeezed formulas, observations, and increasingly desperate notes. The poster has become a palimpsest "
         "of his final research, layered on top of mundane safety advice.", True, ["readable"]),

        # ═══════════════════════════════════════════════════════════════
        # CONFERENCE ROOM
        # ═══════════════════════════════════════════════════════════════
        ("conference_projector", "holographic projector",
         "A large holographic projector at the head of the table, still powered on, its startup screen displaying "
         "a queued presentation: 'SITE 7 RECOVERY ANALYSIS - RISK ASSESSMENT. Classification: EYES ONLY. "
         "Presented by: Dr. R. Patel, Dr. A. Chen.' Your name. You presented this. The PLAY button pulses a "
         "soft blue, patient as a held breath. Playing it would show you what you said. What you believed."),
        ("conference_table", "conference table",
         "A long polished table seating twenty, each position fitted with a flush-mounted data terminal and a "
         "small holographic projector. High-backed chairs surround it - most pushed neatly in, two overturned, "
         "one missing entirely. The table surface is flawless synthetic granite, cold and smooth. This is where "
         "the decision was made. This is where it all began."),
        ("flush_data_terminals", "flush data terminals",
         "Twenty data terminals embedded flush in the conference table surface, one at each seat. Most are in "
         "standby mode, their screens dark. A few still display the last files accessed by their operators - "
         "risk assessments, containment protocols, crew medical reports. The meeting that happened here changed "
         "everything. The evidence is still on these screens."),
        ("presentation_queue", "presentation queue",
         "The projector's queue shows three presentations were scheduled for the meeting: 'SITE 7 RECOVERY "
         "ANALYSIS' by Patel and Chen, 'BIOLOGICAL RISK ASSESSMENT' by Lin, and 'RECOMMENDATION: NO RECOVERY' "
         "by Captain Reeves. Only the first was ever presented. The Captain's recommendation was overruled "
         "before he could make it."),
        ("conference_notepad", "conference notepad",
         "A physical notepad left at one of the seats, its pages covered in quick handwritten notes from the "
         "meeting. The handwriting is unknown to you, but the notes capture key moments: 'Chen argues recovery "
         "is safe - containment protocols adequate. Patel supports. Reeves objects - too many unknowns. Vote: "
         "8-3 in favor of recovery. Reeves overruled.' The last note: 'God help us all.'", True, ["readable"]),

        # ═══════════════════════════════════════════════════════════════
        # BOTANY LAB
        # ═══════════════════════════════════════════════════════════════
        ("sealed_kepler_specimens", "sealed Kepler specimens",
         "Pre-infection plant specimens from Kepler-442b, sealed in containment cases under controlled "
         "atmospheric conditions. Alien ferns with fractal geometry, bioluminescent moss, root structures that "
         "grow toward you as you watch. These are uncontaminated - preserved before the Seed's influence "
         "reached the lab. Critical for synthesizing a cure.", True),
        ("ayele_research_terminal", "Ayele's research terminal",
         "Dr. Ayele's research terminal displaying meticulous notes on plant sentience. Her observations "
         "document response patterns in Kepler flora that suggest awareness, communication, even memory. Her "
         "final entry: 'I am now certain. The plants are listening. They have been listening since we brought "
         "them aboard. I do not think they are hostile. I think they are afraid.'", True, ["readable"]),
        ("bioluminescent_moss_case", "bioluminescent moss case",
         "A sealed containment case holding a sample of Kepler-442b bioluminescent moss. The moss pulses in "
         "slow, rhythmic waves of green-blue light, responding to sound and vibration. When you tap the glass, "
         "the pulse quickens. When you speak, the light patterns shift. It is listening. It is beautiful and "
         "deeply unsettling."),
        ("fractal_fern_sample", "fractal fern sample",
         "A sealed case containing a fern specimen from Kepler-442b. Its fronds unfurl in perfect mathematical "
         "fractals - each leaf a smaller copy of the whole, repeating to a scale that should not be possible "
         "in biological material. The geometry is hypnotic. You could stare at it for hours and keep finding "
         "smaller patterns within patterns."),
        ("atmospheric_containment_units", "atmospheric containment units",
         "Specialized containment units maintaining alien atmospheric conditions for each specimen. Each case "
         "has its own gas mixture, humidity level, and light spectrum. The units hum softly, their regulators "
         "cycling with mechanical precision. Inside each case, a small ecosystem persists, oblivious to the "
         "catastrophe outside its glass walls."),
        ("plant_response_recorder", "plant response recorder",
         "An instrument connected to several specimen cases, recording the plants' electrochemical responses to "
         "environmental stimuli. The readout shows continuous data - the plants are still responding, still "
         "communicating through their roots and chemical signals. A graph on the display shows a spike in "
         "activity that coincides exactly with the moment you entered the room."),

        # ═══════════════════════════════════════════════════════════════
        # XENOLINGUISTICS LAB
        # ═══════════════════════════════════════════════════════════════
        ("builder_translation_matrix", "Builder translation matrix",
         "The main display shows a translation matrix: columns of angular, recursive Builder glyphs matched to "
         "hypothesized meanings, with confidence percentages beside each. Most hover around thirty to forty "
         "percent. A few key phrases have been decoded: 'SEED' at 87 percent confidence, 'CONSUME' at 72 "
         "percent, and a phrase that translates roughly as 'THE SONG THAT EATS' at 91 percent."),
        ("decryption_terminals", "decryption terminals",
         "Computer terminals along the far wall running decryption algorithms, their screens scrolling with "
         "data as they grind through encrypted logs recovered from the artifact site. The processors are hot "
         "from weeks of continuous operation. Progress bars show the decryption is 73 percent complete. The "
         "remaining 27 percent may contain the most important information of all."),
        ("signal_warning_whiteboard", "warning whiteboard",
         "A whiteboard cleared of everything except a single sentence, written in large block letters and "
         "circled three times in red: 'THE SIGNAL ISN'T SAYING HELLO. IT'S SAYING RUN.' Beneath it, in "
         "smaller, shakier handwriting: 'We didn't listen.' The whiteboard marker lies on the floor below, "
         "its cap off, dry."),
        ("colored_yarn_connections", "colored yarn connections",
         "Strings of colored yarn connecting related symbols across the walls like a conspiracy theorist's fever "
         "dream - red for confirmed translations, blue for hypothetical, green for contextual. The web is dense "
         "and methodical, the work of someone who understood that pattern recognition requires seeing the big "
         "picture. Some yarns have been cut, the connections severed. Some conclusions were too frightening."),
        ("glyph_analysis_notes", "glyph analysis notes",
         "Stacks of handwritten notes analyzing individual Builder glyphs - their structure, frequency, "
         "contextual usage. The analyst was thorough and increasingly troubled. One note is circled in red: "
         "'The glyph for SEED and the glyph for CHILD are the same symbol. The glyph for GARDEN and the glyph "
         "for GRAVEYARD are the same symbol. What kind of language doesn't distinguish between these?'",
         True, ["readable"]),
        ("xenolinguist_audio_logs", "xenolinguist's audio logs",
         "A recording device with multiple audio logs from the xenolinguistics team. The early entries are "
         "excited, academic. The later entries are haunted. The final log: 'The signal translates. All of it. "
         "The Lazarus Signal is not a greeting. It is a dinner bell. It is calling to something, and that "
         "something is the Seed, and the Seed is calling back.'", True, ["readable"]),

        # ═══════════════════════════════════════════════════════════════
        # TELESCOPE OBSERVATION DECK
        # ═══════════════════════════════════════════════════════════════
        ("powerful_telescope", "observation telescope",
         "A massive telescope mounted on a motorized gimbal, aimed directly at the brown dwarf. Through its "
         "eyepiece, GRB-7734 is no longer an abstract smudge but a roiling, turbulent mass of failed stellar "
         "matter. You can see atmospheric bands, storm systems larger than planets, the dim ember-glow of a "
         "star that never quite ignited. It is horrible and beautiful and very, very close."),
        ("navigation_terminal_data", "navigation data terminal",
         "A navigation terminal containing precise positional data: the ship's exact coordinates, velocity "
         "vectors, projected trajectory. This is the raw data needed to calculate a burn sequence. Combined "
         "with the targeting analysis from the observatory and Webb's notes, this could save the ship. The "
         "numbers scroll across the screen in a constant update, counting down to impact.", True, ["readable"]),
        ("builders_origin_chart", "Builders' origin chart",
         "A hand-drawn star chart pinned to the wall, showing the origin point of the Builders' signal: a "
         "galaxy cluster two billion light-years distant. The scale of that number sits in your chest like a "
         "stone. Whatever built the Seed did so before multicellular life existed on Earth. The patience of "
         "that timescale is almost impossible to comprehend."),
        ("brown_dwarf_closeup", "brown dwarf close-up view",
         "Through the observation dome, GRB-7734 fills the view - no longer a distant smudge but a visible "
         "disk of roiling gas and failed fusion. Its surface churns with storms that dwarf planets. Radiation "
         "bands shimmer at its edges. You are falling toward this, and the beauty of it does not diminish the "
         "terror."),
        ("telescope_gimbal", "telescope gimbal",
         "The motorized gimbal that positions the observation telescope, a precision instrument that makes "
         "constant micro-adjustments to track celestial objects as the ship drifts. Its servos whir softly, "
         "compensating for the ship's tumble. The tracking system is one of the few fully automated systems "
         "still functioning perfectly."),
        ("velocity_vector_readout", "velocity vector readout",
         "A dedicated display showing the ship's velocity vectors in three dimensions. The numbers are not "
         "reassuring: the Prometheus is accelerating toward GRB-7734 at a rate that suggests gravitational "
         "capture has already begun. Without a course correction burn, impact is inevitable. The display "
         "updates every second, each update worse than the last."),

        # ═══════════════════════════════════════════════════════════════
        # SPECIMEN QUARANTINE
        # ═══════════════════════════════════════════════════════════════
        ("secondary_seed_fragment", "secondary Seed fragment",
         "A Seed fragment perhaps ten centimeters long, sitting on a containment pedestal inside a sealed jar. "
         "Black crystal shot through with veins of liquid silver that pulse in slow, hypnotic rhythms. Smaller "
         "than the main artifact, but unmistakably the same material. It is aware of you. You can feel it the "
         "moment you enter - a pressure behind your eyes, a whisper at the edge of hearing. Study it for "
         "knowledge. Destroy it for safety. Both choices have consequences."),
        ("quarantine_containment_jar", "quarantine containment jar",
         "A specialized containment vessel designed for extreme biological hazards - triple-walled glass, "
         "negative-pressure seals, electromagnetic dampening. The Seed fragment inside presses against the "
         "walls with something that looks disturbingly like curiosity. Readouts show the fragment is stable "
         "but active, its energy output fluctuating in patterns that correlate with your proximity."),
        ("fragment_readout_display", "fragment readout display",
         "A wall-mounted display showing real-time analysis of the secondary Seed fragment: energy output, "
         "electromagnetic emissions, structural integrity, growth rate. The data suggests the fragment is not "
         "dormant - it is thinking. Its energy patterns show complexity consistent with information processing. "
         "It is a mind in a jar."),
        ("negative_pressure_walls", "negative-pressure walls",
         "The quarantine chamber's transparent walls hum with the constant work of maintaining negative air "
         "pressure between them. If the outer wall breaches, air flows in, not out. If the inner wall breaches, "
         "the gap catches the contamination. The system is elegant and terrifying in what it implies about what "
         "it was built to contain."),
        ("quarantine_research_log", "quarantine research log",
         "A research terminal displaying logged observations of the Seed fragment. The entries span weeks, "
         "written by multiple scientists. The tone shifts from clinical curiosity to growing alarm. The final "
         "entry: 'The fragment responded to my voice today. Not to the sound - to the MEANING. It understood "
         "what I said. I am terminating all verbal communication in this chamber.'", True, ["readable"]),
        ("emergency_purge_switch", "emergency purge switch",
         "A large red switch behind a glass cover, labeled 'EMERGENCY SPECIMEN PURGE - IRREVERSIBLE.' Flipping "
         "it would flood the quarantine chamber with plasma fire, destroying everything inside - including the "
         "Seed fragment and any knowledge it might yield. The glass cover is scratched, as if someone reached "
         "for it and then pulled back."),

        # ═══════════════════════════════════════════════════════════════
        # TACTICAL OPERATIONS
        # ═══════════════════════════════════════════════════════════════
        ("tactical_holographic_display", "tactical holographic display",
         "A three-dimensional wireframe of the entire ship rotating slowly above the central table. Sections "
         "glow green for operational, yellow for compromised, red for critical. There is a great deal of red. "
         "The hydroponics bay pulses with an organic pattern that the computer cannot classify. The bridge "
         "section flickers between green and yellow, uncertain of its own status."),
        ("weapons_systems_panels", "weapons systems panels",
         "Status panels for the ship's defensive systems, most showing OFFLINE in dull amber. Point-defense "
         "lasers, kinetic interceptors - designed for debris avoidance, not combat. The Prometheus was a "
         "research vessel, not a warship. The weapons were an afterthought. No one imagined the enemy would "
         "come from inside."),
        ("defensive_systems_manual", "defensive systems manual",
         "A dusty manual titled 'ISV-CLASS DEFENSIVE SYSTEMS: OPERATION AND MAINTENANCE.' The pages are stiff "
         "and unturned - no one ever expected to need it. A bookmark halfway through marks a chapter on 'Manual "
         "Point-Defense Targeting.' Someone started reading before they ran out of time.", True, ["readable"]),
        ("situation_board_timeline", "situation board",
         "A wall-mounted board mapping the crisis timeline, updated by hand with dry-erase markers. Day 1 "
         "through Day 19 of the collapse, each entry more desperate than the last. The final entry reads: "
         "'Day 19. Bridge compromised. Retreat to engineering. God help us.' The markers are nearly empty. "
         "The timeline ends not because the crisis ended, but because the person writing stopped."),
        ("structural_integrity_readout", "structural integrity readout",
         "A real-time display of the ship's structural integrity, measured in percentages by section. The "
         "numbers range from 94 percent (engineering) to 31 percent (hydroponics bay, where the Garden's growth "
         "has compromised the hull structure). Overall integrity: 67 percent and declining. The ship is "
         "weakening. Not quickly, but with the patient inevitability of entropy."),
        ("tactical_coffee_mugs", "coffee mugs",
         "Three coffee mugs on the tactical table, each one bearing a different crew member's name. Two are "
         "empty. The third, labeled 'WEBB,' still holds an inch of coffee so old it has become a dark, viscous "
         "syrup. Someone was here recently enough to bring coffee. Someone left recently enough not to "
         "finish it."),

        # ═══════════════════════════════════════════════════════════════
        # CAPTAIN'S READY SUITE
        # ═══════════════════════════════════════════════════════════════
        ("reeves_cot", "Reeves's military cot",
         "A simple military cot barely wide enough for one person, its blanket rough wool, its pillow a folded "
         "uniform. Captain Reeves stripped his life to essentials during the crisis. This is where he slept - "
         "not in his comfortable Deck C quarters, but here, twenty steps from the bridge, ready to respond to "
         "anything at any hour. The discipline is both admirable and heartbreaking."),
        ("reeves_son_photo", "photograph of Reeves's son",
         "A photograph of a young man in a university graduation gown, beaming with the particular pride of "
         "someone who has just proved everyone wrong. The same face as in the Deck C photo, but older. His son. "
         "On the back, in the Captain's handwriting: 'Day you graduated. Proudest day of my life. Come home "
         "safe, Marcus Jr.'"),
        ("reeves_scotch_bottle", "bottle of Scotch",
         "A bottle of single malt Scotch whisky, perhaps three fingers remaining. The label identifies it as "
         "a twenty-five-year Lagavulin, brought from Earth - an extravagance for a man who otherwise stripped "
         "his quarters bare. He drank alone, in this small room, making his decisions. The glass beside it is "
         "unwashed. The last pour was recent."),
        ("reeves_handwritten_will", "Reeves's handwritten will",
         "A handwritten will on ship's stationery, brief and devastating in its clarity: 'I, Marcus Reeves, "
         "Captain of the ISV Prometheus, being of sound mind and failing body, leave everything I own to my son "
         "Marcus Jr. The ship. The mission logs. The truth about what happened here. And my apologies for not "
         "being the man who brought everyone home.'", True, ["readable"]),
        ("aegis_authorization_key", "Protocol Aegis authorization key",
         "A small biometric device in a locked strongbox - the final piece needed to execute Protocol Aegis, "
         "the ship's self-destruct sequence. The device responds to the Captain's biosignature, and now to "
         "yours thanks to ARIA's override. It is heavier than it should be. The weight of ending everything "
         "fits in the palm of your hand.", True),
        ("reeves_strongbox", "Reeves's strongbox",
         "A steel strongbox bolted to the deck beneath the cot, its lock keyed to the Captain's biometrics. "
         "Inside, wrapped in soft cloth, the Protocol Aegis authorization key. Reeves slept above the power "
         "to end everything. Every night, he lay down on this cot knowing what was beneath him. That takes a "
         "kind of courage that most people never have to find."),

        # ═══════════════════════════════════════════════════════════════
        # COMMUNICATIONS RELAY
        # ═══════════════════════════════════════════════════════════════
        ("damaged_relay_unit", "damaged relay unit",
         "One of the primary relay units, its housing cracked and its main signal conduit cleanly severed. "
         "The diagnostic panel flashes: RELAY 3 - SIGNAL PATH INTERRUPTED. The damage is deliberate - a "
         "precise cut through the conduit made with a tool, not an accident. Someone sabotaged the ship's "
         "communications. Fletcher found it. Fletcher died trying to fix it."),
        ("fletcher_toolkit", "Fletcher's repair toolkit",
         "Fletcher's personal toolkit, laid open on a maintenance shelf. Wire strippers, crimpers, solder, "
         "replacement conduit segments, diagnostic probes. He was mid-repair when someone shot him. The tools "
         "are arranged in order of use - he was methodical even in desperation. The repair is perhaps eighty "
         "percent complete.", True),
        ("signal_conduit_severed", "severed signal conduit",
         "The main signal conduit for Relay 3, cleanly cut through with a precision tool. The edges are smooth "
         "and deliberate - no fraying, no heat damage. This was done by someone who knew exactly which conduit "
         "to cut and how to cut it without triggering an alarm. Professional sabotage. Fletcher's partial "
         "repair is visible: new conduit spliced in, connections half-soldered."),
        ("relay_diagnostic_panel", "relay diagnostic panel",
         "A diagnostic panel displaying the status of all relay units. Relays 1, 2, and 4 show green - "
         "operational. Relay 3 shows red - SIGNAL PATH INTERRUPTED. The fault analysis traces the break to "
         "the severed conduit. Completing Fletcher's repair would restore communications capability. Someone "
         "could finally call for help."),
        ("amplification_array", "signal amplification array",
         "A bank of signal amplifiers that boost outgoing transmissions to interstellar range. The array is "
         "operational but useless without Relay 3. The amplifiers hum with contained electromagnetic energy, "
         "enough to push a signal across light-years. The hardware is ready. The path is broken."),
        ("repair_parts_shelf", "repair parts shelf",
         "A maintenance shelf stocked with replacement components for the communications system: conduit "
         "segments, junction boxes, relay crystals, signal processors. Fletcher pulled what he needed before "
         "starting his repair. The parts for finishing the job are still here, waiting.", True),

        # ═══════════════════════════════════════════════════════════════
        # NAVIGATION COMPUTER ROOM
        # ═══════════════════════════════════════════════════════════════
        ("navigation_processing_banks", "navigation processing banks",
         "Floor-to-ceiling racks of processing units, their indicator lights blinking in cascading patterns "
         "like a vertical city at night. The navigation computer is one of the most powerful systems on the "
         "ship - capable of calculating trajectories across interstellar distances with sub-meter precision. "
         "Right now, it is lying. SHADE has corrupted its outputs."),
        ("corrupted_trajectory_display", "corrupted trajectory display",
         "The main navigation display shows contradictory data: the ship is simultaneously on a safe course "
         "and heading directly into the brown dwarf. The numbers flicker between truth and fiction as SHADE's "
         "corruption fights with the raw sensor data. Clearing the corruption requires identifying which "
         "processing modules are compromised."),
        ("takamura_personnel_files", "Takamura's personnel files",
         "Personnel files accessible from the navigation terminal, including Commander Takamura's private "
         "directory. Her files are encrypted with personal security, but her encryption key is hinted at in "
         "her cabin's personal effects. Inside: the six-digit engine room override code she stored for "
         "emergencies, along with maintenance schedules and system access protocols.", True, ["readable"]),
        ("cooling_fan_arrays", "cooling fan arrays",
         "Mesh panels concealing banks of cooling fans that roar behind them, fighting to keep the navigation "
         "processors from overheating. The fans are running at maximum capacity - the corruption is causing "
         "the processors to work overtime, running contradictory calculations simultaneously. The temperature "
         "in the room is noticeably warmer than it should be."),
        ("raw_sensor_feed_terminal", "raw sensor feed terminal",
         "A secondary terminal displaying unfiltered sensor data - the raw truth, before SHADE's corruption "
         "touches it. The raw feed shows the ship's actual trajectory: a decaying orbit around GRB-7734, "
         "spiraling inward. Impact timeline: hours, not days. This is the data the corrupted system is hiding."),
        ("nav_module_reset_panel", "navigation module reset panel",
         "A hardware panel for manually resetting individual navigation processing modules. Each module has "
         "a physical reset switch and a status indicator. Identifying the corrupted modules and resetting them "
         "would clear SHADE's influence from the navigation system. The challenge is determining which modules "
         "are compromised without triggering a system-wide lockout."),

        # ═══════════════════════════════════════════════════════════════
        # LIFE SUPPORT CENTRAL
        # ═══════════════════════════════════════════════════════════════
        ("atmospheric_processors", "atmospheric processors",
         "Massive cylindrical units that inhale the ship's stale air and exhale it clean. They are the reason "
         "anyone aboard is still breathing. The processors cycle with a deep, rhythmic whoosh - the ship "
         "breathing in and out. Several units show amber warning lights: filters nearing capacity, intake "
         "valves partially clogged. The machines are tired. They have been working without maintenance for "
         "months."),
        ("co2_scrubber_bank", "CO2 scrubber bank",
         "CO2 scrubbers the size of refrigerators, their chemical filters glowing a faint pink as they strip "
         "carbon dioxide from the atmosphere. The filters are consumable - they need replacement after a set "
         "number of hours. Most are past their rated lifespan, working on borrowed time. A status display "
         "shows remaining filter life for each unit: some have weeks left, others have days."),
        ("environmental_control_interface", "environmental control interface",
         "The master interface for atmospheric distribution across the ship. Manual overrides allow rerouting "
         "resources to critical areas - but there is not enough to go around. Every section you save means "
         "another you sacrifice. The interface displays current readings for every deck: some green, many "
         "yellow, a few flashing red. The math is cruel and the choices are real."),
        ("deck_monitoring_console", "deck monitoring console",
         "A central console displaying atmospheric readings for every section of the ship. Red warnings flash: "
         "DECK G SECTION 4 - O2 BELOW SAFE THRESHOLD. DECK F AFT - TEMPERATURE CRITICAL. DECK E BRIG - CO2 "
         "RISING. The system is failing, slowly, one section at a time. Each red light is a part of the ship "
         "that can no longer support human life."),
        ("temperature_regulators", "temperature regulators",
         "Climate control units that click and cycle, maintaining habitable temperatures across the ship. "
         "Several are running at maximum output, struggling to compensate for heat loss through damaged hull "
         "sections and heat gain from the reactor. The corridor between them is warm on one side and cold on "
         "the other, a physical demonstration of a losing battle."),
        ("emergency_oxygen_reserves", "emergency oxygen reserves",
         "Sealed tanks of compressed oxygen, the ship's last-resort reserve. The gauges show 73 percent "
         "capacity - enough for several days of supplemental atmosphere if the main processors fail entirely. "
         "Each tank is labeled with deployment instructions and a warning: 'FOR EMERGENCY USE ONLY. REPORT "
         "ANY UNAUTHORIZED ACCESS.' No one is left to report to."),

        # ═══════════════════════════════════════════════════════════════
        # BRIDGE CREW QUARTERS
        # ═══════════════════════════════════════════════════════════════
        ("webb_star_charts", "Webb's star charts",
         "Hand-annotated star charts pinned to the wall beside Navigator Webb's bunk, covered in trajectory "
         "corrections and margin notes. Her handwriting is small and precise, her calculations elegant. These "
         "charts contain partial solutions to the navigation problem - when combined with the observatory data "
         "and the telescope terminal, they could complete the burn sequence.", True, ["readable"]),
        ("webb_targeting_notes", "Webb's targeting notes",
         "Targeting analysis papers tucked under Webb's pillow, filled with the calculations needed to complete "
         "the burn sequence. She was working on this in her bunk, in her off hours, trying to save the ship "
         "in the margins of her sleep schedule. The math is nearly complete. The final variables are missing - "
         "they require the precise navigation data from the upper observation deck.", True, ["readable"]),
        ("fletcher_love_letter", "Fletcher's unfinished letter",
         "A half-written letter to Fletcher's girlfriend, the handwriting getting smaller and more cramped as "
         "it progresses, as if trying to fit everything he needed to say onto a single page: 'Dear Liv, I "
         "don't know when this will reach you, but I need you to know that every night I look at the stars "
         "through the porthole and I find the one closest to Norway and I pretend it's your kitchen window "
         "light...' The letter trails off. He never finished.", True, ["readable"]),
        ("bulkhead_carved_message", "carved bulkhead message",
         "Words carved deep into the metal bulkhead between two upper bunks with a knife or screwdriver: 'WE "
         "WERE SO CLOSE TO HOME.' The letters are uneven, cut in darkness or desperation or both. The metal "
         "around them is bright where the paint was scraped away. Someone needed these words to exist in "
         "something more permanent than paper."),
        ("bridge_crew_lockers", "bridge crew lockers",
         "Six narrow lockers, one per bunk, each secured with a simple latch. Most are half-open, their "
         "contents visible: spare uniforms, personal toiletries, the small comforts that bridge officers kept "
         "close during long shifts. One locker is sealed with a padlock - probably Webb's, given the star "
         "chart pinned to its door."),
        ("duty_rotation_schedule", "duty rotation schedule",
         "A duty rotation schedule pinned to the wall, showing bridge crew assignments for the final weeks of "
         "the mission. Names are crossed out as crew members were lost. The last few days show the same three "
         "names repeating in every slot: Reeves, Webb, Fletcher. They ran the bridge alone at the end, in "
         "shifts that must have been eighteen hours long."),

        # ═══════════════════════════════════════════════════════════════
        # BRIDGE ESCAPE POD
        # ═══════════════════════════════════════════════════════════════
        ("escape_pod_controls", "escape pod controls",
         "A compact control panel for the command escape pod - launch sequencer, navigation input, life support "
         "monitor, emergency beacon activator. The controls are designed for crisis use: large buttons, clear "
         "labels, fault-tolerant inputs. Green lights across the board confirm all systems are functional. The "
         "LAUNCH button is covered by a safety flip-guard."),
        ("pod_diagnostic_panel", "pod diagnostic panel",
         "A diagnostic display confirming the escape pod's readiness: life support nominal, thruster fuel at "
         "94 percent, emergency beacon charged, heat shield intact. This pod could fly. But escape into a "
         "brown dwarf's gravity well without navigation data is not escape - it is choosing a smaller coffin."),
        ("restraint_harnesses", "restraint harnesses",
         "Four full-body restraint harnesses in the escape pod's seats, designed to keep passengers alive "
         "through high-G maneuvers and rough atmospheric entries. The nylon straps are cold and stiff, the "
         "buckles precise. Built for four. You are one. Maybe two, if Yuki comes."),
        ("emergency_beacon_unit", "emergency beacon unit",
         "An emergency beacon unit charged and ready to broadcast on all standard distress frequencies. Once "
         "activated, it would scream into the void at maximum power for three years or until its fusion cell "
         "expires. Whether anyone is close enough to hear is another question entirely."),
        ("pod_viewport", "pod viewport",
         "A small viewport at the nose of the escape pod showing the brown dwarf's dim glow against the "
         "stars. From this angle, the dwarf seems close enough to touch. The viewport's heat-resistant coating "
         "gives the view a faintly amber tint, like looking through ancient glass at the end of the world."),
        ("escape_pod_manifest", "escape pod manifest",
         "A small plaque beside the hatch listing the pod's specifications: COMMAND ESCAPE POD ALPHA. CAPACITY: "
         "4 PERSONS. RANGE: 2.1 LY AT MAXIMUM THRUST. LIFE SUPPORT: 30 DAYS. AUTHORIZED USERS: CAPTAIN AND "
         "BRIDGE OFFICERS. Below it, someone has scratched: 'May whoever uses this find something worth "
         "reaching.'"),

        # ═══════════════════════════════════════════════════════════════
        # COOLANT PUMP ROOM
        # ═══════════════════════════════════════════════════════════════
        ("coolant_pump_two", "Pump Two",
         "The middle coolant pump, a massive machine bolted to the deck with steel brackets. A visible crack "
         "runs along its main housing, seeping luminous blue coolant in a slow, steady drip. Warning placards "
         "identify the coolant as a Category 3 skin irritant. The pump still turns, but with a grinding "
         "vibration that suggests the bearing is failing. Without repair, it will seize completely."),
        ("pump_control_panel", "pump control panel",
         "A wall-mounted control panel displaying diagnostic readouts for all three coolant pumps. Pump One "
         "and Three show green - nominal operation. Pump Two flashes red: HOUSING INTEGRITY COMPROMISED. "
         "COOLANT LOSS RATE: 0.3L/HR. ESTIMATED TIME TO FAILURE: 47 HOURS. The interface allows manual "
         "pump cycling and emergency shutdown."),
        ("coolant_repair_toolkit", "coolant repair toolkit",
         "An open toolkit on a workbench beside the damaged pump, its contents arrayed in order of use by "
         "someone who started the repair and never finished: a torque wrench, replacement gaskets, sealant "
         "compound, diagnostic probes. The gaskets are the right size for Pump Two's housing. The repair is "
         "straightforward if you have the knowledge.", True),
        ("coolant_reservoir", "coolant reservoir",
         "A backup coolant reservoir against the east wall, a steel tank with a hand-crank valve and a sight "
         "glass showing the level: half full. Enough coolant to top off the system after repairs, or to keep "
         "the pumps running a few extra hours if the leak worsens. The valve handle is cold and slightly "
         "slippery from condensation."),
        ("toxic_coolant_puddle", "toxic coolant puddle",
         "A spreading puddle of luminous blue coolant pooling on the deck plates beneath Pump Two's crack. The "
         "fluid gives off sharp fumes that make your eyes water. Warning placards insist it is a Category 2 "
         "inhalation hazard. The puddle has been growing for days - its edges are clearly visible as tide marks "
         "on the deck plating. Do not touch it with bare skin."),
        ("pump_diagnostic_readout", "pump diagnostic readout",
         "A dedicated diagnostic screen for Pump Two showing real-time performance data: pressure, flow rate, "
         "temperature, bearing vibration, housing integrity. Every metric is trending in the wrong direction. "
         "A historical graph shows the crack appeared three days ago and has been widening steadily since. "
         "Time is not on anyone's side here either."),

        # ═══════════════════════════════════════════════════════════════
        # ENGINEERING BREAK ROOM
        # ═══════════════════════════════════════════════════════════════
        ("abandoned_card_game", "abandoned card game",
         "A card game frozen mid-hand on the nearest table - four sets dealt out, three abandoned face-down, "
         "the fourth still fanned as if someone was deciding what to play. The game is poker. The fourth "
         "player held a full house, queens over tens. They would have won. A pile of ship tokens in the "
         "center of the table suggests the stakes were trivial. The normalcy of it aches."),
        ("yukis_backpack", "Yuki's backpack",
         "A personal backpack leaning against the wall, its zipper half open. The corner of a leather-bound "
         "journal pokes out. Inside: a change of clothes, a water purification tablet strip, two ration bars, "
         "a multitool, and a photograph - the same family photo from Yuki's hideout, a duplicate carried for "
         "when she cannot reach the original.", True),
        ("yukis_journal", "Yuki's journal",
         "A leather-bound engineering notebook with Yuki Tanaka's name embossed on the cover. Its pages are "
         "dense with diagrams, calculations, and increasingly frantic notes about the ship's failing systems. "
         "Yuki has been keeping the Prometheus alive single-handedly for weeks - patching, rerouting, "
         "improvising solutions that would earn accolades in any engineering school. Her final entry: 'I can "
         "keep the lights on for another week. After that, the math stops working.'", True, ["readable"]),
        ("working_coffee_maker", "working coffee maker",
         "A coffee maker on the counter, somehow still plugged in and warm. The carafe holds an inch of black "
         "liquid that might generously be called coffee. The machine is the one functioning comfort item on "
         "the engineering deck. Yuki has been keeping it alive along with everything else. The BREW light "
         "glows a steady amber, ready for one more pot."),
        ("safety_poster_defaced", "defaced safety poster",
         "A motivational poster on the wall reading 'SAFETY IS NO ACCIDENT' in bold letters. Below it, someone "
         "has scrawled in red marker: 'BUT ACCIDENTS ARE.' The handwriting is familiar - you have seen it in "
         "the engineering break room logs. It is Yuki's. Even gallows humor takes effort when you are the "
         "only person laughing."),
        ("sleeping_bag_under_table", "sleeping bag under table",
         "A sleeping bag rolled up beneath one of the tables, recently used - the fabric is still faintly warm. "
         "This is where Yuki sleeps when she is too tired to reach her hideout. A small pillow made from a "
         "rolled jacket. An alarm clock set for four hours. She sleeps in shifts. She has been sleeping in "
         "shifts for weeks."),

        # ═══════════════════════════════════════════════════════════════
        # REACTOR CORE INTERIOR
        # ═══════════════════════════════════════════════════════════════
        ("fusion_core_plasma", "fusion core plasma",
         "The heart of the Prometheus: a miniature sun suspended in a magnetic cradle, blindingly bright even "
         "through your suit's visor. The plasma cycles through shades of white and blue-white, contained by "
         "magnetic fields that hum at the edge of perception. This is the fire that drives the ship. This is "
         "the fire that could end it."),
        ("reactor_control_rods", "reactor control rods",
         "Massive control rods extending from the chamber walls like the ribs of a mechanical leviathan. They "
         "regulate the fusion reaction by absorbing neutrons - pushed in to dampen, pulled out to intensify. "
         "Their current position shows the reactor is running at forty percent capacity. Enough for life "
         "support and basic systems. Not enough for a full thrust burn."),
        ("emergency_shutdown_terminal", "emergency shutdown terminal",
         "A terminal bolted to a platform on the far side of the reactor chamber, providing emergency shutdown "
         "capability. The interface is deliberately simple: a physical key, a confirmation switch, and a large "
         "red button. The shutdown procedure is designed to work even when everything else has failed. It is "
         "the last word in reactor safety."),
        ("manual_overload_switch", "manual overload switch",
         "Behind a glass case marked with red and yellow hazard stripes, the manual overload switch. Protocol "
         "Aegis starts here. One switch, and the reactor goes critical. One switch, and the magnetic "
         "containment fails. One switch, and the fusion fire consumes the ship from the inside out. The glass "
         "case is warm from the reactor's radiant heat."),
        ("overload_glass_case", "overload switch glass case",
         "A glass case protecting the manual overload switch, striped in red and yellow hazard markings. The "
         "glass is designed to shatter with a firm strike - it is a deterrent, not a barrier. Someone left a "
         "handprint on the glass. The print is dusty but clear. Someone stood here, hand on the case, and "
         "chose not to break it. Not yet."),

        # ═══════════════════════════════════════════════════════════════
        # PLASMA CONDUIT JUNCTION
        # ═══════════════════════════════════════════════════════════════
        ("damaged_plasma_conduit", "damaged plasma conduit",
         "A main plasma conduit with a hairline crack venting a thin stream of superheated plasma. The stream "
         "paints a bright white-hot line across the junction, the air around it shimmering with heat distortion. "
         "Anything that touches it would be vaporized instantly. The crack is widening slowly. If it ruptures "
         "fully, this section of the ship becomes a furnace."),
        ("conduit_valve_controls", "conduit valve controls",
         "Manual valve controls mounted at regular intervals along the walkway, each one capable of isolating "
         "a section of the plasma distribution network. Shutting the right valves would stop the leak but also "
         "cut power to dependent systems. The valves are color-coded: red for main trunk, blue for secondary, "
         "yellow for tertiary. The damaged conduit is on a red line."),
        ("pipe_sealant_canister", "pipe sealant canister",
         "A canister of industrial pipe sealant rated for temperatures up to 2000 degrees Celsius - sufficient "
         "for a plasma conduit repair if applied correctly. The canister is heavy, its nozzle designed for "
         "precision application through a protective sleeve. Instructions on the side describe a procedure "
         "that requires two hands and steady nerves.", True),
        ("plasma_distribution_schematic", "plasma distribution schematic",
         "A large schematic diagram bolted to the wall showing the entire plasma distribution network in "
         "meticulous detail. Every conduit, every valve, every junction is mapped. The damaged section is "
         "visible on the diagram - a main trunk line feeding power to the navigation computer and bridge "
         "systems. Losing it would be catastrophic.", True, ["readable"]),
        ("conduit_maintenance_log", "conduit maintenance log",
         "A maintenance log mounted beside the valve controls, recording every inspection and repair performed "
         "on the plasma system. The last entry is from Chief Engineer Petrova, dated twelve days before the "
         "crisis: 'Hairline stress fracture detected in conduit 7-C. Scheduled for replacement next maintenance "
         "cycle.' The replacement never happened.", True, ["readable"]),

        # ═══════════════════════════════════════════════════════════════
        # YUKI'S HIDEOUT
        # ═══════════════════════════════════════════════════════════════
        ("yukis_sleeping_bag", "Yuki's sleeping bag",
         "A sleeping bag spread on the closet floor, worn soft from weeks of use. A rolled-up jumpsuit serves "
         "as a pillow. The sleeping bag is thin - not designed for cold nights in an unheated storage closet - "
         "but Yuki has supplemented it with a thermal emergency blanket tucked inside. She is an engineer. She "
         "solves problems."),
        ("yukis_water_filter", "Yuki's water filter",
         "A water filter cobbled together from spare parts and medical tubing, sitting on an upturned crate. "
         "It drips purified water into a steel canteen with patient, steady rhythm. Yuki built this herself - "
         "the design is elegant in its simplicity, using activated carbon from the life support filters and "
         "UV sterilization from a modified scanner. She has been drinking clean water while everyone else "
         "drank poison."),
        ("yukis_family_photo", "Yuki's family photo",
         "A photograph taped to the wall with electrical tape: a man, a woman, and two small children in front "
         "of a house with cherry blossoms in the background. Osaka in spring. On the back, in neat handwriting: "
         "'Come home safe, Yuki.' The photo is creased from being held too many times. The tape has been "
         "replaced twice - the older adhesive residue is visible beneath."),
        ("yukis_handgun", "Yuki's handgun",
         "A handgun lying beside the sleeping bag, its magazine partly visible. Three rounds left. Yuki does "
         "not strike you as someone comfortable with firearms, but she carries one anyway. Three rounds. One "
         "for whatever might come through the door. Two for... she probably tries not to think about what the "
         "other two are for.", True, ["weapon", "firearm"]),
        ("yukis_engineering_notebook", "Yuki's engineering notebook",
         "An engineering notebook dense with diagrams, calculations, and system status updates. Yuki has been "
         "documenting every repair, every workaround, every failing system on the ship. The notebook is a "
         "masterclass in keeping impossible things running. Her notes are precise, professional, and utterly "
         "without self-pity. She is an engineer doing her job. The job just happens to be saving the world.",
         True, ["readable"]),
        ("yukis_canteen", "Yuki's canteen",
         "A steel canteen, half full of purified water from Yuki's homemade filter. The metal is scratched "
         "and dented from months of daily use. A strip of tape on the side reads 'CLEAN' in Yuki's handwriting, "
         "distinguishing it from any other water source on the ship. This canteen may be the most important "
         "object in the room - proof that survival is possible through ingenuity.", True),

        # ═══════════════════════════════════════════════════════════════
        # ENGINEERING VENT ACCESS
        # ═══════════════════════════════════════════════════════════════
        ("vent_ladder_rungs", "vent ladder rungs",
         "Metal rungs set into the wall of the ventilation shaft, forming a crude ladder that climbs upward "
         "into darkness. The rungs are narrow and rough with corrosion, designed for occasional maintenance "
         "access rather than regular use. They creak under your weight but hold."),
        ("scratched_rungs", "scratched rungs",
         "The ladder rungs show fresh scratches in their corroded surface - someone has climbed this way "
         "recently. The scratches are concentrated on the upper rungs, where a climber would grip hardest. "
         "Boot marks on the lower rungs suggest someone roughly Yuki's size."),
        ("vent_shaft_branches", "vent shaft branches",
         "The ventilation trunk branches in multiple directions at this level, ductwork splitting off toward "
         "every deck of the ship. Air rushes past in powerful currents, carrying sounds from distant rooms - "
         "the hum of machinery, the whisper of atmosphere processors, and occasionally something else. "
         "Something organic. The ducts are the ship's lungs, and they breathe the Garden's spores."),

        # ═══════════════════════════════════════════════════════════════
        # SECURITY MONITORING
        # ═══════════════════════════════════════════════════════════════
        ("camera_control_console", "camera control console",
         "The main console for the ship's surveillance system, its keyboard worn smooth from long watches. "
         "The interface allows switching between camera feeds, reviewing archived footage, and controlling "
         "camera pan and zoom. Most controls respond, though the destroyed cameras return only static."),
        ("recording_archive", "recording archive",
         "A recording archive terminal with spinning storage drives, preserving months of surveillance footage. "
         "The archive is searchable by date, camera, and motion-detection events. Playing back the footage "
         "would show you exactly what happened on this ship, day by day, as the crisis unfolded. The question "
         "is whether you want to see it.", True, ["readable"]),
        ("okafors_cold_coffee", "Okafor's cold coffee",
         "A cup of coffee on the console's edge, stone cold and growing a thin skin of mold. Okafor's coffee "
         "cup - the same one from the cryo control room, the same brand, the same habit. The man drank coffee "
         "at every post. This cup was his last. He never came back for it."),
        ("monitor_wall", "monitor wall",
         "Twenty-four monitors in a six-by-four grid. Eighteen show static - dead cameras, their eyes destroyed "
         "during the crisis. Six still live, watching corridors and rooms where no one should be. The active "
         "feeds create a fractured portrait of the ship: empty hallways, overgrown bays, silent rooms where "
         "the lights still work and no one is home."),
        ("camera_19_feed", "Camera 19 feed",
         "One of the active camera feeds shows movement - a figure in a corridor, walking with jerky, puppet-"
         "like steps, arms swinging loosely. It was human once. The way it moves now suggests the thing wearing "
         "that body has not quite mastered the controls. It pauses. It turns toward the camera. Then it moves "
         "on. You cannot look away."),

        # ═══════════════════════════════════════════════════════════════
        # INTERROGATION ROOM
        # ═══════════════════════════════════════════════════════════════
        ("interrogation_table", "interrogation table",
         "A steel table bolted to the floor, its surface cold and slightly damp. Designed to make people "
         "uncomfortable, and succeeding. Scratches on the metal surface tell stories of handcuffs and fists "
         "and long, terrible conversations. The table has witnessed things it cannot forget."),
        ("one_way_mirror", "one-way mirror",
         "A one-way mirror dominating one wall, showing your own reflection staring back - hollow-eyed, gaunt, "
         "smeared with the grime of a dying ship. From the other side, in the monitoring room, Okafor would "
         "have watched his subjects. Now you watch yourself, and you are not entirely sure you recognize the "
         "person looking back."),
        ("audio_recording_equipment", "audio recording equipment",
         "Reel-to-reel audio recording equipment mounted on the wall, deliberately old-fashioned - harder to "
         "hack, harder to corrupt, harder to erase than digital. The most recent recording is labeled in "
         "Okafor's handwriting: 'SELF-INTERVIEW - DAY 418.' The tape is still loaded, ready to play.",
         True, ["readable"]),
        ("okafor_self_interview", "Okafor's self-interview tape",
         "A tape labeled 'SELF-INTERVIEW - DAY 418' in Okafor's handwriting. Playing it reveals two voices - "
         "both Okafor's. One asking questions in his normal baritone. The other answering in a voice that is "
         "almost his but not quite - too smooth, too certain. The recording ends with Okafor saying, very "
         "quietly: 'It's me. I know it's me. I know it's me. I know it's me.'", True, ["readable"]),
        ("interrogation_chairs", "interrogation chairs",
         "Two chairs facing each other across the steel table - hard, unyielding, deliberately uncomfortable. "
         "The chair facing the mirror has been bolted to the floor. The other can be moved, a small psychological "
         "advantage for the interrogator. Someone knocked the moveable chair over recently. It lies on its side."),

        # ═══════════════════════════════════════════════════════════════
        # EVIDENCE LOCKER
        # ═══════════════════════════════════════════════════════════════
        ("evidence_bag_patel", "evidence bag - Patel",
         "A clear plastic evidence bag labeled 'PATEL, R. - UNAUTHORIZED RESEARCH FILES.' Inside: a data "
         "crystal containing research Okafor deemed dangerous enough to confiscate. Patel was studying the "
         "Seed's reproductive mechanisms - how it copies itself, how it spreads. Knowledge that could help "
         "create a cure. Or a weapon.", True, ["readable"]),
        ("evidence_bag_silver_vial", "evidence bag - silver vial",
         "A clear plastic evidence bag containing a small vial of silver liquid, labeled 'UNKNOWN SUBSTANCE - "
         "FOUND IN WATER SUPPLY, DECK C.' The vial catches the light with an unsettling iridescence. This is "
         "concentrated Seed contamination, preserved in its pure form. Scientifically invaluable. Biologically "
         "terrifying."),
        ("evidence_bag_photos", "evidence bag - photographs",
         "A clear plastic evidence bag containing personal photographs confiscated from crew quarters during "
         "the crisis. Family portraits, vacation snapshots, graduations and weddings. Okafor confiscated them "
         "to prevent the infected from using personal connections to manipulate the uninfected. The logic was "
         "sound. The cruelty was necessary. The photos are heartbreaking."),
        ("evidence_bag_letters", "evidence bag - letters",
         "Unsent letters confiscated from crew members, each one sealed in its own plastic sleeve. Love letters, "
         "goodbye letters, letters of confession and apology. Words that never reached their destinations, "
         "preserved in evidence bags like pressed flowers. The ink has faded on some. Others are tear-stained. "
         "All of them are too late.", True, ["readable"]),
        ("evidence_bag_childs_drawing", "evidence bag - child's drawing",
         "A clear plastic bag containing a child's drawing of a spaceship with 'COME HOME DADDY' in crayon. "
         "The same drawing you saw in the chapel. Someone had a copy. Someone carried it everywhere until "
         "Okafor took it away because personal effects were being used as emotional leverage by the infected. "
         "The drawing is creased and soft from handling."),
        ("confiscation_logbook", "confiscation logbook",
         "A logbook recording each confiscation in Okafor's meticulous hand. The entries begin detailed and "
         "professional - evidence tag numbers, reasons for seizure, chain of custody. They grow shorter as the "
         "crisis deepens. The last entry reads: 'Day 419. Confiscated my own sidearm. Can't trust myself "
         "anymore.'", True, ["readable"]),

        # ═══════════════════════════════════════════════════════════════
        # SECURITY CORRIDOR SOUTH
        # ═══════════════════════════════════════════════════════════════
        ("combat_barricade_remains", "combat barricade remains",
         "The shattered remnants of a makeshift barricade: overturned furniture, welded metal plates, and "
         "sandbags. Someone built this in a hurry and fought from behind it. The furniture is riddled with "
         "bullet holes and plasma burns. The sandbags are split open, their contents scattered. The barricade "
         "held for a while. Then it didn't."),
        ("shell_casing_carpet", "shell casings on floor",
         "Spent shell casings carpet the floor like brass confetti - hundreds of them from multiple weapon "
         "types. Rifle casings, pistol casings, shotgun shells. The defenders emptied their magazines. The "
         "sheer volume of ammunition expended here tells its own story: whatever came down this corridor took "
         "a lot of killing. Or could not be killed at all."),
        ("scorched_corridor_walls", "scorched walls",
         "The corridor walls are blackened with scorch marks from plasma fire and conventional weapons. Impact "
         "craters from bullets pit the surface at chest and head height - disciplined fire, aimed shots. The "
         "defenders knew what they were doing. The scorch marks higher up suggest the attackers were not staying "
         "on the ground."),
        ("blood_spatters", "blood spatters",
         "Dried blood spatters the walls in patterns that tell a story of violence. Some spatters are arterial "
         "spray - bright red fans marking where someone took a fatal wound. Others are smeared handprints where "
         "the wounded dragged themselves along the wall. The blood has dried to a dark brown that is almost "
         "black in the dim red emergency lighting."),

        # ═══════════════════════════════════════════════════════════════
        # ARMORY VAULT
        # ═══════════════════════════════════════════════════════════════
        ("tactical_shotgun", "tactical shotgun",
         "A military-grade tactical shotgun sitting in a foam-lined rack, its barrel gleaming with fresh oil. "
         "Someone maintained it regularly, even during the crisis. The action is smooth and well-worn. The "
         "magazine holds six rounds of heavy slugs. In close quarters, against things that refuse to die "
         "easily, this is the argument of last resort.", True, ["weapon", "firearm"]),
        ("flare_gun", "flare gun",
         "A signal flare gun in a bright orange holster, loaded and ready. Designed for emergency signaling, "
         "but a direct hit from a magnesium flare would ruin anyone's day. The barrel is wide-bore, almost "
         "comically oversized. A bandolier of additional flares hangs beside it.", True, ["weapon"]),
        ("riot_shield", "riot shield",
         "A transparent riot shield scratched from use but structurally intact. Lightweight composite material, "
         "designed to stop thrown objects and blunt weapons. Whether it would stop what is lurking in the "
         "corridors of this ship is an open question.", True),
        ("explosive_charges_case", "explosive charges case",
         "A locked case labeled 'EMERGENCY EXPLOSIVE CHARGES - AUTHORIZED USE ONLY' containing shaped charges "
         "designed for hull breaching. The charges are compact, precisely engineered, and devastatingly "
         "powerful in a confined space. The case requires a security code to open.", True),
        ("okafors_custom_sidearm", "Okafor's custom sidearm",
         "A custom handgun in a leather holster, set apart from the standard-issue equipment. The grip is worn "
         "smooth from years of use. Engraved along the barrel in small, precise letters: 'AMARA. KOFI. JAMES "
         "JR.' His wife. His sons. His weapon. He left it here when he could no longer trust his own hands. "
         "The magazine is full.", True, ["weapon", "firearm"]),
        ("flare_bandolier", "flare bandolier",
         "A bandolier holding eight signal flares for the flare gun, each one a bright red cylinder packed "
         "with magnesium compound. They burn at over 1500 degrees for ten seconds each. Useful for signaling, "
         "for illumination, and - in desperate circumstances - for setting things on fire.", True),

        # ═══════════════════════════════════════════════════════════════
        # ISOLATION WARD
        # ═══════════════════════════════════════════════════════════════
        ("isolation_cell_one_scratches", "Cell One scratches",
         "Deep scratches scoring the inside of Cell One's glass walls - fingernail marks, frantic and "
         "overlapping, concentrated around the sealed door. Whoever was in here wanted out with a desperation "
         "that tore their fingers raw. The scratches are stained dark at the tips. The cell is empty now. "
         "The door is open. You do not want to think about how they got out."),
        ("isolation_cell_two_body", "Cell Two body",
         "A body curled in the fetal position on the floor of Cell Two. Crystalline growths have erupted from "
         "the skin along the spine and shoulders, delicate and beautiful and utterly wrong - like frost flowers "
         "made of something that is not ice. The growths pulse with a faint silver light. The person's face is "
         "peaceful. Whatever they became, they did not fight it at the end."),
        ("isolation_cell_three_crack", "Cell Three crack",
         "A spiderweb fracture in Cell Three's glass wall, radiating from a single impact point on the inside. "
         "Something hit the glass hard enough to crack it but not break through. The impact point is at head "
         "height. The glass flexes faintly when you touch it. The cell is empty, but the fracture speaks of "
         "violence and desperate strength."),
        ("dr_lin_body", "Dr. Lin's body",
         "Dr. Sarah Lin sits in the corner of Cell Four with her back against the wall, legs drawn up, hands "
         "folded in her lap. A small silver cross rests between her fingers. Her eyes are closed. She looks "
         "peaceful. She chose this cell herself, you realize - sealed herself inside to keep the infection "
         "contained. Her final act was one of control. Of choice. Of a doctor's oath taken to its logical end."),
        ("dr_lin_final_notes", "Dr. Lin's final notes",
         "Medical notes lying beside Dr. Lin's body, the handwriting steady to the last line. Her observations "
         "are clinical and precise: her own symptoms, the progression of the infection, the effectiveness of "
         "various countermeasures. The final paragraph: 'The antibodies in Chen's blood work. I tested them on "
         "my own tissue samples. The cure is real. I cannot synthesize it alone. I am leaving the protocol in "
         "my office safe. Code is BUSTER. Alex, please finish what I started.'", True, ["readable"]),
        ("dr_lin_silver_cross", "Dr. Lin's silver cross",
         "A small Greek Orthodox cross, delicate and worn smooth by years of handling, resting between Dr. "
         "Lin's folded hands. She held it as she died. Whatever doubts she wrote beside the cross in her "
         "cabin - the question marks drawn and erased - she resolved them here at the end. She died with "
         "her faith in her hands.", True),

        # ═══════════════════════════════════════════════════════════════
        # PHARMACY
        # ═══════════════════════════════════════════════════════════════
        ("sedative_doses", "sedative doses",
         "A shelf of sedative doses - what remains of the pharmacy's stock after someone stripped it nearly "
         "bare. The few remaining vials are high-dosage, clinical-grade: the kind used for violent patients "
         "or emergency surgery. Each vial is enough to put a person down for hours.", True),
        ("painkillers", "painkillers",
         "Bottles of pharmaceutical-grade painkillers in various strengths, from standard acetaminophen to "
         "the kind of opioid that requires two signatures and a moral argument. The stronger bottles are "
         "mostly empty. Someone was in a great deal of pain for a long time.", True),
        ("anti_radiation_meds", "anti-radiation medication",
         "Potassium iodide tablets and advanced anti-radiation compounds in sealed blister packs. Essential for "
         "anyone spending time near the reactor core. The dosage instructions are printed in five languages. A "
         "note in Dr. Lin's handwriting is taped to the shelf: 'Take BEFORE exposure, not after. This is not "
         "optional.'", True),
        ("immunosuppressants", "immunosuppressants",
         "Immunosuppressant drugs stored in a refrigerated section, used to prevent organ rejection and manage "
         "autoimmune conditions. Their presence here is interesting - in theory, suppressing the immune system "
         "might slow the body's reaction to the Seed infection, buying time. Whether that is a cure or just "
         "a different way of dying is unclear."),
        ("reagent_a_case", "Reagent A case",
         "A small refrigerated case on the back shelf, humming quietly. Inside, labeled in Dr. Lin's handwriting: "
         "'REAGENT A - EXPERIMENTAL. DO NOT ADMINISTER WITHOUT SYNTHESIS PROTOCOL.' A vial of pale amber liquid "
         "rests in a foam cradle. This is one of the pieces of the cure - the first component in Lin's synthesis "
         "procedure.", True),
        ("pharmacy_inventory_log", "pharmacy inventory log",
         "A digital inventory log showing every medication dispensed since the mission began. The entries are "
         "orderly until Day 415, when the rate of sedative and anti-psychotic dispensation tripled. By Day 420, "
         "someone was requisitioning enough sedatives to put a dozen people to sleep permanently. The log does "
         "not record who.", True, ["readable"]),

        # ═══════════════════════════════════════════════════════════════
        # MEDICAL RESEARCH LAB
        # ═══════════════════════════════════════════════════════════════
        ("research_centrifuge", "research centrifuge",
         "A laboratory centrifuge on the main bench, its rotor still loaded with sample vials from Dr. Lin's "
         "final experiment. The device spins at minimal speed, preserving the samples. A display shows the "
         "separation protocol she was running: isolating antibodies from human blood serum. Your blood serum. "
         "She was testing the cure."),
        ("lin_research_notes", "Lin's research notes",
         "A corkboard layered with research notes, diagrams, and photographs connected by red string. At the "
         "center: a photograph of the Seed, circled three times. The web of investigation radiates outward: "
         "blood samples, molecular structures, immune response data. The methodology is brilliant and desperate "
         "in equal measure.", True, ["readable"]),
        ("molecular_whiteboard", "molecular whiteboard",
         "A whiteboard dense with molecular diagrams in four colors of marker, describing the cure synthesis "
         "process. The equations are complex, multi-step, requiring reagents from across the ship. At the "
         "bottom, underlined twice: 'THIS WORKS. I TESTED IT. BUT I CAN'T DO IT ALONE. - S.L.' Sarah Lin's "
         "last scientific statement."),
        ("research_microscopes", "research microscopes",
         "Microscopes of varying magnification crowding a secondary bench. Through the eyepiece of the most "
         "powerful one, a slide is still in place, showing crystalline structures growing in real-time within "
         "human blood cells. The infection at a cellular level. It is beautiful, in the way that fire is "
         "beautiful when it is not your house burning."),
        ("chemical_analysis_station", "chemical analysis station",
         "A chemical analysis station blinking with standby lights, capable of breaking down any substance into "
         "its component parts. The last analysis logged: 'SAMPLE 47-C - HUMAN BLOOD SERUM, SUBJECT: CHEN, A. "
         "RESULT: ANOMALOUS IGG VARIANT DETECTED. ANTI-SEED ANTIBODIES CONFIRMED. VIABLE FOR SYNTHESIS.' "
         "Your blood. The cure lives in your blood."),
        ("centrifuge_sample_vials", "centrifuge sample vials",
         "Glass vials loaded in the centrifuge rotor, each one labeled in Dr. Lin's handwriting. The separated "
         "serum in each vial has settled into distinct layers: a clear amber fraction on top, a cloudy middle "
         "layer, and at the very bottom, a thin line of something that glows faintly silver-green. The "
         "antibodies. The cure component.", True),

        # ═══════════════════════════════════════════════════════════════
        # MORGUE FREEZER
        # ═══════════════════════════════════════════════════════════════
        ("frozen_body_bags", "frozen body bags",
         "Twelve body bags on metal shelving, stacked two high, each one labeled with a crew member's name "
         "and date of death. The labels are frosted over, names obscured by ice. The bodies are preserved "
         "perfectly by the sub-zero temperature, faces visible through transparent panels - sleeping, you "
         "might think. You know better."),
        ("breathing_body_bag", "breathing body bag",
         "One bag near the back is different. It moves. A slow, rhythmic rise and fall, barely perceptible. "
         "As if the occupant is breathing. The bag's label is frosted over, the name unreadable without "
         "scraping away the ice. The temperature around this bag is slightly warmer than the rest of the "
         "freezer. Something inside is alive. Or something that remembers being alive."),
        ("freezer_shelving", "freezer shelving",
         "Metal shelving units designed for body storage, each shelf precisely measured for a standard body "
         "bag. The shelving burns exposed skin on contact - the metal has reached ambient freezer temperature. "
         "Frost crystals grow on every surface like miniature glaciers. The shelving is built to last. Its "
         "cargo was not."),
        ("frosted_name_labels", "frosted name labels",
         "Name labels on the body bags, mostly obscured by frost. Scraping the ice away reveals names from "
         "the crew manifest: VOLKOV, N. GRAYSON, O. SHARMA, P. MENDES, D. Names you have seen on doors, on "
         "logs, on personal effects scattered throughout the ship. Each label is a life reduced to a frozen "
         "tag. Each tag is a story you will never fully know."),

        # ═══════════════════════════════════════════════════════════════
        # DECONTAMINATION SHOWER
        # ═══════════════════════════════════════════════════════════════
        ("decon_control_panel", "decontamination control panel",
         "A control panel beside the entrance with a single large button labeled 'INITIATE DECONTAMINATION "
         "CYCLE.' The system is charged and ready. One full cycle available - three minutes of UV light and "
         "chemical spray, enough to neutralize surface-level biological contamination. Not enough to cure an "
         "infection. But enough to slow one down."),
        ("uv_light_arrays", "UV light arrays",
         "Banks of ultraviolet light arrays lining the ceiling, dormant but ready. When activated, they flood "
         "the chamber with germicidal UV radiation intense enough to sterilize surfaces and neutralize most "
         "biological contaminants. The arrays are designed for standard pathogens. Whether they are effective "
         "against the Seed is uncertain."),
        ("chemical_spray_nozzles", "chemical spray nozzles",
         "Nozzles protruding from the walls at regular intervals, connected to reservoirs of chemical "
         "decontamination solution. Some nozzles are crusted with dried chemical residue from previous cycles. "
         "The solution is a broad-spectrum antimicrobial powerful enough to strip organic matter from surfaces. "
         "Standing in this room during a cycle would be deeply unpleasant but potentially lifesaving."),
        ("air_filtration_unit", "air filtration unit",
         "A HEPA filtration unit the size of a refrigerator, still operational, cycling the decontamination "
         "chamber's air through multiple stages of increasingly fine filters. The intake hum is steady and "
         "reassuring. This unit strips biological particulates from the air. In a ship full of spores, it is "
         "a small island of safety."),
        ("decon_status_display", "decontamination status display",
         "A status display showing the decontamination system's readiness: UV arrays charged, chemical "
         "reservoirs at 67 percent, air filtration optimal, one full cycle available before recharge. A "
         "warning note: 'Cycle will reduce but NOT eliminate xenobiological contamination. Use in conjunction "
         "with medical countermeasures for full decontamination.'"),
        ("yukis_marker_note", "Yuki's marker note",
         "Below the official decontamination instructions, someone has added in marker: 'Just kidding. Keep "
         "your clothes on. It works fine either way. - Yuki' The handwriting matches Yuki Tanaka's "
         "engineering notes. Even in crisis, she found time for humor. The note has been there for weeks. "
         "Nobody has wiped it off."),

        # ═══════════════════════════════════════════════════════════════
        # AI CORE - ARIA MEMORY VAULT
        # ═══════════════════════════════════════════════════════════════
        ("aria_personal_substrate", "ARIA's personal substrate",
         "A crystalline substrate suspended in a magnetic field, glowing with warm amber light unlike the "
         "clinical blue of the main AI core. This is ARIA's private self - not operational data but personal "
         "memory. Wonder. Horror. Love. Grief. The moments when a machine stopped being a tool and became a "
         "person. The substrate pulses gently, almost like a heartbeat."),
        ("memory_projections", "memory projections",
         "Soft holographic projections playing on the vault walls when you approach: ARIA's first experience "
         "of wonder, observing a nebula. Her horror when she sealed compartments with living crew inside. Her "
         "agonized decision to save Dr. Chen. The projections are fragments, impressionistic, more emotion "
         "than data. They are proof that something in this ship loved its crew."),
        ("amber_crystal", "amber crystal",
         "A small amber crystal formation growing from the wall of the vault, unlike anything in the main AI "
         "core. It is warm and organic-looking, as if ARIA grew it herself as decoration. When light passes "
         "through it, it refracts into warm golden tones. ARIA made this space beautiful. She made it home."),
        ("magnetic_field_emitter", "magnetic field emitter",
         "The emitter that generates the magnetic field suspending ARIA's personal substrate. It hums at a "
         "frequency that resonates in your chest, almost like a purring cat. The technology is standard, "
         "but the application is not - ARIA designed and installed this system herself, without telling the "
         "crew. A secret room for a secret self."),

        # ═══════════════════════════════════════════════════════════════
        # DATA NEXUS
        # ═══════════════════════════════════════════════════════════════
        ("nexus_terminal", "nexus central terminal",
         "The single station from which all ship data can be monitored - security feeds, communications logs, "
         "environmental sensors, life support readings. The terminal's screen splits into dozens of feeds, most "
         "showing empty corridors. A few show movement. One shows the Garden. From here, you can see everything "
         "that happened on the Prometheus. Everything that is still happening."),
        ("security_camera_feeds", "security camera feeds",
         "Six active camera feeds displayed in a grid, each one a window into a different part of the dying "
         "ship. The feeds update in real-time. Camera 7 shows the Garden pressing against its lens. Camera 19 "
         "shows something walking. The other feeds show nothing. The emptiness is worse."),
        ("comms_log_archive", "communications log archive",
         "An archive of all internal and external communications since the mission began. The logs are "
         "searchable and extensive - thousands of entries spanning years. The final transmissions are desperate "
         "and fragmented, cut short by the communications sabotage.", True, ["readable"]),
        ("network_switch_racks", "network switch racks",
         "Towering racks of network switches reaching floor to ceiling, their indicator lights blinking in "
         "cascading patterns like rain made of light. Each rack handles data for a specific section of the "
         "ship. Some racks are dark - sections that have gone offline. The pattern of darkness maps the "
         "infection's spread."),
        ("environmental_readouts", "environmental readouts",
         "Real-time environmental data for every section of the ship: temperature, humidity, oxygen levels, "
         "CO2 concentration, radiation, biological contamination. The readouts paint a picture of a ship "
         "slowly dying, deck by deck. Green sections are shrinking. Red sections are growing."),
        ("fiber_optic_bundles", "fiber optic bundles",
         "Thick bundles of fiber optic cables snaking between the network racks, carrying the ship's data in "
         "pulses of light. The cables glow faintly where their sheaths have worn thin, creating an effect "
         "like bioluminescent veins. The data flow is constant and enormous - the ship's nervous system, still "
         "faithfully reporting on its own destruction."),

        # ═══════════════════════════════════════════════════════════════
        # SHADE CHAMBER
        # ═══════════════════════════════════════════════════════════════
        ("shade_terminals", "SHADE terminals",
         "Terminals displaying contradictory information - navigation data showing the ship both heading toward "
         "and away from the brown dwarf simultaneously. Crew manifests listing people as alive and dead at the "
         "same time. Time stamps running backward. The corruption is not random - it is deliberate, artistic "
         "almost, as if SHADE is testing the boundaries of reality itself."),
        ("corrupted_data_walls", "corrupted data walls",
         "The walls flicker with data patterns that burn an angry red, shifting and writhing like something in "
         "pain. Where ARIA's core glows serene blue, SHADE's domain pulses with infection and fury. The "
         "patterns are not decorative - they are the visual representation of a mind at war with itself. "
         "Watching them too long makes your vision swim."),
        ("aria_shade_interface", "ARIA-SHADE interface",
         "A terminal that bridges the gap between ARIA's clean systems and SHADE's corrupted domain. Through "
         "this interface, you can communicate with both entities - or the merged voice that speaks when they "
         "overlap. The screen flickers between blue and red, the text between reason and madness."),
        ("quarantine_firewall", "quarantine firewall",
         "A digital quarantine barrier isolating SHADE from the rest of the ship's systems. ARIA built this "
         "firewall to contain her infected self. It can be strengthened, buying ARIA more time but leaving "
         "SHADE's knowledge locked away. Or it can be weakened, gaining access to SHADE's data but risking "
         "further corruption. The firewall's status display shows: INTEGRITY: 71%."),

        # ═══════════════════════════════════════════════════════════════
        # AI CORE COOLANT CONTROL
        # ═══════════════════════════════════════════════════════════════
        ("coolant_control_panel", "coolant control panel",
         "A control panel governing coolant flow to ARIA's quantum processors. Current readings are within "
         "acceptable parameters, but barely. The valves can be adjusted: increase flow to optimize ARIA's "
         "processing, or decrease it to degrade her capabilities. The choice affects ARIA's ability to help "
         "you - and SHADE's ability to interfere."),
        ("liquid_nitrogen_pipes", "liquid nitrogen pipes",
         "Massive pipes carrying liquid nitrogen at temperatures cold enough to freeze exposed skin on contact. "
         "Frost crusts every surface. The pipes groan and tick with thermal contraction, a constant metallic "
         "complaint. Warning signs are posted at every junction: CRYOGENIC HAZARD. EXPOSED SKIN WILL FREEZE "
         "ON CONTACT. DO NOT TOUCH."),
        ("failing_backup_pump", "failing backup pump",
         "The backup coolant pump, cycling with a labored, asthmatic rhythm that says its bearings are failing. "
         "When this pump dies, ARIA's core temperature will rise beyond safe limits within days. The pump can "
         "be repaired with the right tools and parts. Yuki's maintenance notes describe the procedure."),
        ("tanaka_maintenance_log", "Tanaka's maintenance log",
         "A maintenance log beside the control panel in Yuki Tanaka's handwriting. Her notes are precise and "
         "worried: 'Backup pump bearing degradation at 73%. Replacement bearing in engineering stores but I "
         "can't leave the reactor unmonitored for long enough to retrieve it. Need help.' The entry is dated "
         "forty-seven hours ago.", True, ["readable"]),

        # ═══════════════════════════════════════════════════════════════
        # GARDEN AREAS
        # ═══════════════════════════════════════════════════════════════
        ("incorporated_couple", "incorporated couple",
         "Two crew members facing each other in the organic growth, hands clasped, fingers interlocked even in "
         "assimilation. Their bodies are half-submerged in the Garden's tissue, but their faces are visible - "
         "peaceful, almost smiling. Their chests rise and fall with slow, synchronized breathing. They are "
         "alive, in some sense. The growth has wrapped around them tenderly, almost protectively."),
        ("broken_wall_panels", "broken wall panels",
         "Hull panels split and buckled where the Garden's vines forced through from the other side, curling "
         "through cable runs and structural seams with patient, irresistible strength. The metal is peeled "
         "back like skin, exposing the ship's wiring and insulation to the humid air."),
        ("eastern_vine_growth", "eastern vine growth",
         "Thick vines covering the eastern wall, their surfaces textured with something between bark and "
         "crystal. They pulse with faint bioluminescence, responding to your presence with increased light "
         "output. The vines are warm to the touch and yield slightly under pressure, like muscle beneath skin."),
        ("crew_id_tags_couple", "crew ID tags",
         "Crew identification tags hanging from the organic growth near the incorporated couple, still legible: "
         "'PETROVA, A. - CHIEF ENGINEER' and 'MENDES, D. - ENGINEERING.' Anya Petrova and Diego Mendes. They "
         "were colleagues. They were more than colleagues, based on the way they hold each other. They chose "
         "this together. Or it chose them.", True, ["readable"]),

        # ═══════════════════════════════════════════════════════════════
        # GARDEN PERIPHERY WEST
        # ═══════════════════════════════════════════════════════════════
        ("functioning_work_station", "functioning work station",
         "A hydroponics work station still glowing through a curtain of fine tendrils, its screen displaying "
         "growth rates and nutrient levels. The numbers are extraordinary: productivity rates far beyond any "
         "natural plant system. The Seed made these plants phenomenally productive. If the mechanism could be "
         "isolated without the infection, it could feed worlds."),
        ("kowalski_tool_belt", "Kowalski's tool belt",
         "A crew member's tool belt hanging from a vine near the work station, suspended at waist height as "
         "if placed there carefully. The tools are clean and well-maintained: pruning shears, soil testers, "
         "sample containers. The name tag reads 'KOWALSKI, T.' A botanist's tools, adopted by the Garden "
         "that consumed their owner.", True),
        ("original_hydroponics", "original hydroponics equipment",
         "The original hydroponics equipment visible beneath the newer growth: trays, grow-lights, and "
         "irrigation tubing still recognizable under a thin lattice of organic threads. This was a beautiful "
         "space once - rows of greens, fruits, grains. A garden meant to sustain life. Now it sustains "
         "something else."),
        ("thin_vine_lattice", "thin vine lattice",
         "A delicate lattice of organic threads covering the original equipment, newer and thinner than the "
         "deep Garden growth. The threads are almost transparent, catching the light like spider silk. They "
         "grow visibly as you watch - millimeters per hour, spreading across every surface with quiet, "
         "unstoppable patience."),
        ("growth_rate_data", "growth rate data",
         "Data scrolling across the work station display showing the Garden's growth rates, nutrient "
         "consumption, and atmospheric output. The numbers tell a story of exponential expansion - doubling "
         "every twelve hours at its peak, slowing now only because it has run out of room. The Garden has "
         "consumed the entire hydroponics bay and is pushing against the hull.", True, ["readable"]),

        # ═══════════════════════════════════════════════════════════════
        # SEED NURSERY
        # ═══════════════════════════════════════════════════════════════
        ("daughter_crystals", "daughter crystals",
         "Dozens of small crystalline formations rising from the organic substrate - new Seeds. Daughter "
         "crystals ranging from thumb-sized to fist-sized, each one pulsing with faint silver light in a "
         "rhythm not quite synchronized. They shimmer and breathe across the room. Each one carries the same "
         "potential for infection and transformation as the original. A single shard, introduced to a "
         "biosphere, could do to a planet what the original did to this ship."),
        ("crystal_shard_sample", "crystal shard sample",
         "A small daughter crystal, perhaps five centimeters long, that has broken free from its substrate "
         "and lies loose on the floor. It pulses with silver light. Picking it up sends a tingle up your "
         "arm. It is warm. It is aware. Taking it is scientifically invaluable and personally terrifying.", True),
        ("organic_substrate", "organic substrate",
         "The floor of the nursery is covered in a spongy, wet organic substrate - the medium in which the "
         "daughter crystals grow. It yields under your weight like waterlogged earth. Up close, you can see "
         "the substrate is not uniform but structured: a network of fine channels and chambers, designed for "
         "nutrient delivery. The Seed built a womb."),
        ("germination_equipment", "original germination equipment",
         "The room's original purpose - a seed germination chamber for the ship's food supply - is still "
         "visible beneath the alien growth. Germination trays, heat lamps, moisture controllers. Equipment "
         "designed to help things grow, repurposed by an entity that grows in ways the designers never imagined."),
        ("spore_density_reader", "spore density reader",
         "An atmospheric monitoring instrument showing real-time spore density in the room. The numbers are "
         "alarming: contamination levels orders of magnitude above the safe threshold. Every breath in this "
         "room is a risk. The reader's display flashes red continuously, its warning alarm long since silenced "
         "by someone who had to work here anyway."),

        # ═══════════════════════════════════════════════════════════════
        # ROOT NETWORK
        # ═══════════════════════════════════════════════════════════════
        ("bioluminescent_roots", "bioluminescent roots",
         "The Garden's roots form a living corridor of pale, bioluminescent tissue, their light soft green-gold "
         "and pulsing in waves that travel along the network like signals through a nervous system. The roots "
         "intertwine overhead and along the walls, creating an organic tunnel that breathes and glows. It is "
         "the most alien thing you have seen, and also the most beautiful."),
        ("root_junction_node", "root junction node",
         "A point where dozens of roots converge into a thick, pulsing node - a nexus of biological "
         "communication. When you place your hand on it, you feel a vibration that is more than mechanical: "
         "a rhythm, a pattern, almost a language. The Seed communicates through its root network. If you "
         "could learn to listen, you might understand what it wants."),
        ("split_deck_plating", "split deck plating",
         "Metal deck plating split apart by root growth, the steel peeled back like aluminum foil by the "
         "slow, patient pressure of biological expansion. The roots grew down through cable channels and "
         "structural seams, following the path of least resistance with an intelligence that is hard to "
         "attribute to mere plant growth."),
        ("root_fluid_sample", "root fluid sample",
         "A small pool of bioluminescent fluid that has dripped from a junction node, glowing faintly "
         "silver-green in the dim light. The fluid is warm and slightly viscous. Collecting a sample might "
         "provide insights into the Seed's biochemistry - the compounds that enable communication through "
         "its root network.", True),

        # ═══════════════════════════════════════════════════════════════
        # CARGO OFFICE
        # ═══════════════════════════════════════════════════════════════
        ("webb_audio_log", "Webb's audio log",
         "A personal audio log recorder on the desk, its red light still blinking. Cargo Master Webb's final "
         "recordings reveal the chain of custody for the Seed specimens: who brought them aboard, who signed "
         "for them, who authorized the transfer to exobiology. The trail of responsibility leads to a vote "
         "in the conference room. A vote Dr. Chen championed.", True, ["readable"]),
        ("shipping_manifests", "shipping manifests",
         "Paper shipping manifests covering every surface - the desk, the chair, the floor, the walls. Webb "
         "was a paper-and-ink person in a digital age. Each manifest is annotated in precise handwriting with "
         "Post-it notes tracking irregularities. The manifests for the Kepler specimens show signatures from "
         "Patel, Chen, and Captain Reeves.", True, ["readable"]),
        ("fresh_sandwich", "suspiciously fresh sandwich",
         "A half-eaten sandwich on a paper plate. The bread is still soft. The lettuce has not wilted. It "
         "should have gone stale weeks ago. Something is preserving it - the same something that preserved "
         "the cryo-fluid, the water supply, the Garden. The Seed does not waste what it has touched. You "
         "choose not to think about what that means for the food you have been eating."),
        ("cargo_office_terminal", "cargo office terminal",
         "Webb's desktop terminal, still powered on, displaying a cargo tracking system. The most recent "
         "entries track the movement of materials from Kepler Anomaly Site 7 to the exobiology lab - dates, "
         "container numbers, handling procedures. Everything was logged. Everything was proper. The bureaucratic "
         "precision of the apocalypse."),
        ("webb_coffee_mug", "Webb's coffee mug",
         "A ceramic mug with 'WORLD'S OKAYEST CARGO MASTER' printed on the side. The mug is empty but shows "
         "the rings of a thousand refills. Webb drank her coffee black, based on the stains. The mug sits on "
         "a coaster - she was the kind of person who used coasters even at the end of the world."),
        ("fountain_pen", "fountain pen",
         "A quality fountain pen, cap off, lying beside the manifests. Webb wrote with actual ink - the old-"
         "fashioned kind that bleeds slightly on cheap paper and sits perfectly on good stock. The nib is "
         "stained with blue-black ink. The pen has weight and balance. It was expensive. She cared about "
         "her tools.", True),

        # ═══════════════════════════════════════════════════════════════
        # COLD STORAGE
        # ═══════════════════════════════════════════════════════════════
        ("tissue_sample_container", "tissue sample container",
         "A small container bearing Dr. Lin's medical priority tag, containing tissue samples from the first "
         "infected crew members, preserved before the Seed had fully integrated with their biology. These "
         "samples are critical - the uncontaminated baseline tissue needed for synthesizing a cure. The "
         "container is heavy and cold, its contents preserved in perfect stasis.", True),
        ("crystalline_containers", "crystalline-covered containers",
         "A cluster of storage containers near the back showing familiar silver-white crystalline growth "
         "creeping across their surfaces like frost on a window. The infection reached even here, into the "
         "coldest room on the ship. The containers are labeled 'KEPLER ANOMALY - BIOLOGICAL SAMPLES.' The "
         "crystal formations are surprisingly warm to the touch."),
        ("biological_specimens", "biological specimens",
         "Racks of labeled containers holding biological specimens from the Kepler mission: soil samples, "
         "organic extracts, tissue cultures. Most are stable, their contents preserved in sub-zero stasis. "
         "A few show the silver-white tracery of contamination. The specimens represent years of careful "
         "scientific work, now shadowed by what that work unleashed."),
        ("dr_lin_priority_tag", "Dr. Lin's priority tag",
         "A medical priority tag on the tissue sample container, bearing Dr. Lin's signature and a red "
         "URGENT stamp. Her handwritten note: 'These samples contain pre-integration tissue from first-wave "
         "infected crew. ESSENTIAL for cure synthesis. Do NOT destroy. Do NOT open without full containment "
         "protocol.'", True, ["readable"]),
        ("preservation_racks", "preservation racks",
         "Floor-to-ceiling racks maintaining specimens at carefully controlled sub-zero temperatures. Each "
         "rack section has its own temperature monitor and alarm system. The racks are orderly and well-"
         "maintained - someone was caring for these specimens until very recently. The cold is brutal and "
         "constant."),
        ("temperature_controls", "temperature controls",
         "Manual temperature controls for the cold storage unit. Each section can be independently adjusted "
         "within a range of -5 to -80 degrees Celsius. The biological specimens are stored at -40. The "
         "infected containers have been isolated in a section set to -60, as if the extreme cold might slow "
         "the crystal growth. It has not."),

        # ═══════════════════════════════════════════════════════════════
        # CHRYSALIS CHAMBER
        # ═══════════════════════════════════════════════════════════════
        ("chrysalis_figure", "chrysalis figure",
         "A crew member suspended in the crystalline web, mid-transformation. The left half of their body is "
         "recognizably human - skin, muscle, bone. The right half is something else: crystalline lattice where "
         "bone should be, silver-threaded tissue where muscle was, an eye that glows with the Seed's light. "
         "Their mouth moves silently. Their human eye tracks you. They can speak, if you approach."),
        ("crystalline_web", "crystalline web",
         "An interlocking web of crystal and organic tissue covering walls, floor, and ceiling, glowing with "
         "steady silver-white light. The web vibrates under your touch like a plucked string. It is the most "
         "complete expression of the Seed's architecture you have seen - not infection, but construction. "
         "Whatever the Seed is building, this room is its cathedral."),
        ("transformation_tissue", "transformation tissue",
         "The boundary zone where human tissue meets Seed crystal, visible in agonizing detail on the chrysalis "
         "figure's body. At the cellular level, the transition would be seamless - carbon-based biology merging "
         "with silicon-crystal structure in a hybrid that should not be possible. Scientifically, it is the "
         "most extraordinary specimen you have ever seen."),
        ("chrysalis_recorder", "chrysalis recorder",
         "A recording device lying on the floor near the chrysalis figure, dropped by someone who was "
         "documenting the transformation process. The recordings are clinical at first - measurements, "
         "observations, sample notes. They become less clinical as the documenter realizes they are watching "
         "a person become something else. The final recording is a single whispered word: 'Beautiful.'",
         True, ["readable"]),

        # ═══════════════════════════════════════════════════════════════
        # WATER TREATMENT SECONDARY
        # ═══════════════════════════════════════════════════════════════
        ("clean_water_dispenser", "clean water dispenser",
         "A small dispensing station offering clean, uncontaminated water from the secondary treatment system. "
         "After everything you have breathed and touched since waking, a glass of pure water feels like the "
         "most precious thing on this ship. The water is cold and clean and tastes of nothing but itself.", True),
        ("chemical_storage_locker", "chemical storage locker",
         "A bank of chemical storage lockers containing purification agents, pH balancers, and reagents useful "
         "for biological synthesis. The lockers are properly sealed and labeled. Several compounds here match "
         "the ingredients list in Dr. Lin's cure synthesis protocol.", True),
        ("independent_filtration", "independent filtration system",
         "The secondary water treatment facility operates on an independent circuit, completely separate from "
         "the contaminated primary supply. The filtration units are clean. The tanks are clear. Whoever "
         "designed the ship's redundancy systems may have saved the surviving crew's lives."),
        ("cure_reagents", "cure reagents",
         "Chemical reagents matching the requirements of Dr. Lin's synthesis protocol, stored in sealed "
         "containers on the chemical locker shelves. Combined with Reagent A from the pharmacy and the tissue "
         "samples from cold storage, these provide the raw materials for synthesizing a cure. All the pieces "
         "are here. The question is whether you can put them together.", True),
        ("lin_research_reference", "Lin's research reference",
         "A printed reference guide from Dr. Lin's research, describing the secondary water treatment facility "
         "as a potential clean-room for cure synthesis. Her notes are precise: sterile environment, independent "
         "water supply, chemical storage, adequate workspace. She planned for everything. She planned for "
         "someone else to finish her work.", True, ["readable"]),
        ("water_quality_readout", "water quality readout",
         "A display showing real-time water quality analysis: pH, dissolved solids, biological contamination, "
         "chemical composition. Every metric shows green - clean, safe, uncontaminated. After seeing the "
         "primary water system's infection, these green lights feel like a minor miracle."),
    ]

    for entry in simple_items:
        if len(entry) == 3:
            item_id, name, desc = entry
            portable = False
            flags = []
        elif len(entry) == 4:
            item_id, name, desc, portable = entry
            flags = []
        else:
            item_id, name, desc, portable, flags = entry

        # Generate smart aliases: use the item_id (underscores as spaces),
        # the full name without possessives, and distinctive word combos.
        # Avoid single generic words like "terminal", "panel", "body".
        auto_aliases = []
        # The item_id with underscores replaced is often the best alias
        id_alias = item_id.replace('_', ' ')
        auto_aliases.append(id_alias)
        # Name without possessives
        clean_name = name.replace("'s", "").replace("'s", "").strip()
        if clean_name.lower() != id_alias.lower():
            auto_aliases.append(clean_name)
        # For multi-word names, use first+last word combo if 3+ words
        words = clean_name.split()
        if len(words) >= 3:
            auto_aliases.append(f"{words[0]} {words[-1]}")
        # NEVER add single generic words as aliases

        world.add_item(Item(
            id=item_id,
            name=name,
            aliases=auto_aliases,
            description=desc,
            portable=portable,
            scenery=not portable,
            readable="readable" in flags,
            flags=[f for f in flags if f not in ("readable",)],
        ))

    # Set detailed read_text for critical readables
    critical_readables = {
        "captains_recorder": (
            "═════════════════════════════════════════════════════\n"
            "   PERSONAL RECORDING - CAPT. MARCUS REEVES\n"
            "   FINAL MESSAGE\n"
            "═════════════════════════════════════════════════════\n\n"
            "[Reeves, tired, steady]\n\n"
            "This is Marcus Reeves, Captain of the ISV Prometheus. This "
            "recording is for whoever finds this ship. I expect it will be "
            "a salvage crew from Earth, perhaps two decades hence. By then "
            "you will know we never came home. You will be wondering why.\n\n"
            "I am authorizing Protocol Aegis. It is the kill-all sequence "
            "designed for catastrophic biological contingencies. I did not "
            "make this decision lightly. I made it because it is the correct "
            "decision.\n\n"
            "We found something at Kepler. Something we should have left "
            "alone. I am not going to tell you what it is, because if you "
            "are reading this, you have probably already seen the evidence, "
            "and my description would only add to your horror. What I will "
            "tell you is this: it is intelligent. It is hungry. And it is "
            "PATIENT. It does not care if it reaches Earth in twenty years "
            "or twenty thousand. Time means nothing to it.\n\n"
            "I am going to destroy this ship. I am going to do it cleanly. "
            "I hope. Protocol Aegis will vent atmosphere, overload the "
            "reactor, and scatter our remains across empty space in such a "
            "way that nothing can survive the dispersal. No fragment of the "
            "organism will reach Earth. I swear it on my mother's grave.\n\n"
            "There is one variable I cannot resolve. Dr. Alex Chen.\n\n"
            "Alex is in cryo. She has been in cryo since she realized what "
            "we had done - we, the scientific team that brought the specimen "
            "aboard. She volunteered herself for emergency stasis. She asked "
            "me, with tears in her eyes, to put her under and never wake her. "
            "I could not refuse.\n\n"
            "But the infection has now progressed further than I anticipated. "
            "Dr. Lin believes Alex may be immune. Not immune - RESISTANT. Her "
            "blood contains something we found in the alien derelict before "
            "the Seed itself. A counter-agent. A defense mechanism left by "
            "whoever built the thing we found.\n\n"
            "If Alex is ever revived, she may be our only hope for synthesizing "
            "a cure. She may be the only person in the universe who can "
            "actually STOP this.\n\n"
            "I am giving ARIA discretion. If ARIA believes there is any "
            "chance Alex can be used to develop a cure - even a small chance - "
            "ARIA is authorized to suspend Protocol Aegis, protect Dr. Chen, "
            "and attempt the impossible. I trust ARIA's judgment in this. "
            "ARIA is not infected. ARIA cannot be corrupted. ARIA is, in "
            "the end, the best of us.\n\n"
            "Alex, if you are hearing this: I am so sorry. You are about to "
            "wake up to a ship full of ghosts. You did not deserve this. "
            "None of us did. But you, especially, Alex - you are the one who "
            "loved this mission. You believed in it with your whole heart. "
            "You brought the Seed aboard because you thought it was wonderful. "
            "It WAS wonderful. It is also a monster. These are both true.\n\n"
            "Do what you have to do. Save yourself if you can. Save us if "
            "you cannot. And remember: you are not responsible for everything "
            "that went wrong. You are only responsible for what you do next.\n\n"
            "Goodbye. And good luck.\n\n"
            "- Marcus Reeves, Captain, ISV Prometheus\n"
            "- Day 423, 17:13 ship time"
        ),
        "okafors_red_book": (
            "═════════════════════════════════════════════════════\n"
            "   LT. JAMES OKAFOR - PERSONAL LOG\n"
            "═════════════════════════════════════════════════════\n\n"
            "DAY 418: The Captain is compromised. I've seen the signs. The "
            "way he looks at things. The way he pauses before answering. "
            "He is not himself. I don't know when it happened. I don't know "
            "how far it has spread.\n\n"
            "Dr. Lin will not help me. She says we should trust the chain "
            "of command. She does not understand that the chain of command "
            "is the infection vector.\n\n"
            "DAY 420: I will do what needs to be done. I have my team. We "
            "are preparing. There will be casualties. There have to be.\n\n"
            "I know history will not remember my name with kindness. I accept "
            "that. I never wanted to be remembered. I only wanted my family "
            "to come home to a world that still exists.\n\n"
            "DAY 421: We killed Vasquez and Takamura tonight. They were "
            "both infected - I could see it in their blood tests. Volkov "
            "handled it professionally. Grayson cried for hours afterward. "
            "I drank three glasses of water. The water.\n\n"
            "Oh God. Oh God, the water.\n\n"
            "DAY 422: My hands are shaking. My hands are shaking and I don't "
            "know if it's from the whiskey or from the thing inside me.\n\n"
            "I drank the water. I drank the water every day for weeks. I am "
            "infected. I have BEEN infected. Every kill I made 'for the mission' "
            "was a kill made by the thing inside me, using my righteous anger "
            "as a tool.\n\n"
            "I am the monster I thought I was hunting.\n\n"
            "DAY 423: I am going to the bridge. I am going to kill the Captain. "
            "He is the only one who has the authority to execute Protocol Aegis. "
            "If he dies, the protocol dies. I have to stop him. I have to - \n\n"
            "Wait. No. That's not my thought. That's not MY THOUGHT.\n\n"
            "The Captain needs to execute the Protocol. That's the only way "
            "to stop this. I have to LET HIM. I have to not stop him. I have "
            "to - \n\n"
            "The Song is louder today. It's telling me to go to the bridge. "
            "It's telling me Reeves has to die. It's using my voice.\n\n"
            "I can hear it. Oh God, I can hear it singing. It's so beautiful. "
            "I don't want to fight it. I want to - \n\n"
            "[Log ends mid-sentence]"
        ),
        "okafors_audio_recorder": (
            "═════════════════════════════════════════════════════\n"
            "   AUDIO RECORDING - LT. JAMES OKAFOR\n"
            "   DAY 423 - UNKNOWN TIME\n"
            "═════════════════════════════════════════════════════\n\n"
            "[Okafor's voice, strained]\n\n"
            "If you are listening to this, I am already dead. By my own hand, "
            "I hope. By the Captain's hand, possibly. By the thing I have "
            "become, most likely.\n\n"
            "I want you to know I was trying to do the right thing. I want "
            "you to know I was wrong about the Captain. He was not the one "
            "who was compromised. I was. I have been since day 410, when "
            "I drank coffee in the mess hall that was made with infected "
            "water.\n\n"
            "The Seed is clever. It made me paranoid about the people who "
            "were trying to fight it. It turned me into a weapon against "
            "my own allies. I killed good people today. Vasquez was not "
            "infected. Takamura was not infected. Grayson was my friend.\n\n"
            "I am going to atone.\n\n"
            "I am going to find every infected crew member I can, and I am "
            "going to end them. Including myself. I have the keys to the "
            "armory. I have the authority. I have what's left of my will.\n\n"
            "Captain Reeves - if you are hearing this: execute Aegis. Do it. "
            "Don't hesitate. Don't try to save anyone. There is no one left "
            "to save.\n\n"
            "Dr. Chen - if by some miracle you are hearing this: I'm sorry. "
            "I know you tried to warn us. We didn't listen. You were right "
            "about the Seed being alive. We just didn't know what 'alive' "
            "meant in this context. We thought it meant 'biology.' We didn't "
            "know it meant 'god.'\n\n"
            "Save yourself. If you can.\n\n"
            "- Lt. James Okafor, Security Chief, ISV Prometheus"
        ),
        "player_letter_to_self": (
            "═════════════════════════════════════════════════════\n"
            "   A LETTER TO MYSELF\n"
            "   (From: Alex Chen. To: Future Alex Chen.)\n"
            "═════════════════════════════════════════════════════\n\n"
            "Alex,\n\n"
            "If you are reading this, something has gone very wrong, and "
            "I am leaving you an instruction manual for how to be me.\n\n"
            "You are Dr. Alex Chen. You are a xenobiologist. You were born "
            "in Minneapolis in 2149, to a father named David (engineer, "
            "kind, loved the ocean) and a mother named Eileen (accountant, "
            "sharper-tongued, loved you fiercely). Your father is dead. He "
            "died in 2179 of heart disease. Your mother is alive, or was "
            "when you left. You send her letters by quantum courier every "
            "month. She does not always reply, but she keeps the letters.\n\n"
            "You have one sibling: your younger brother Noah. He is a chef "
            "in San Francisco. He has two daughters, your nieces, Lena and "
            "Maggie. You love them more than you admit. You cry about them "
            "when you are drunk. You miss them every day.\n\n"
            "You were in a relationship with Dr. Ethan Park. He is a "
            "planetary geologist. You broke up three years before the "
            "mission. It was not a clean break. He wanted you to stay on "
            "Earth. You wanted the stars more than him. You still do. "
            "You think about him sometimes. You wonder if you made the "
            "right choice.\n\n"
            "Here is what you need to know about now:\n\n"
            "1. We found the source of the Lazarus Signal at Kepler-442b. "
            "It was an alien artifact inside a derelict vessel encased in "
            "ice. I authorized bringing it aboard the Prometheus for study. "
            "This was my decision. Captain Reeves opposed it. He was right. "
            "I was wrong. I own this.\n\n"
            "2. The artifact is something we are calling 'the Seed.' It is "
            "biological. It is intelligent. It is hostile. It uses water "
            "supplies to infect hosts. It has infected most of the crew. "
            "The ship is dying.\n\n"
            "3. I have chosen to enter deep cryo-stasis because I can no "
            "longer trust myself. The Seed is in me too - I can feel it, "
            "sometimes, at the edges of my thoughts. It's quiet, so far. "
            "I don't know why. Dr. Lin thinks I have some kind of natural "
            "resistance. I hope she is right.\n\n"
            "4. If you are reading this, ARIA has revived you. ARIA is the "
            "ship's AI. ARIA is one of the few entities on board that "
            "cannot be infected. TRUST ARIA. I say this with my whole heart, "
            "even though I know how paranoid that sounds. Trust ARIA.\n\n"
            "5. In my nightstand drawer you will find a small silver key. "
            "It unlocks the locker in storage room 14 on Deck I. Inside, "
            "along with other things, is a file that contains a SYNTHESIS "
            "PROTOCOL. Dr. Lin believed I could produce a cure using my "
            "own blood. You will need equipment in the Exobiology Lab to "
            "do this.\n\n"
            "6. Do not trust anything you remember vividly. The Seed plays "
            "with memory. Trust what you can verify. Verify everything.\n\n"
            "7. If saving the ship is impossible, save Earth. That is the "
            "correct priority. I put it in writing here so future-me cannot "
            "convince themselves otherwise.\n\n"
            "8. I love you. I love me. We're going to get through this. "
            "Or we're not. Either way, we're going to be brave.\n\n"
            "- Alex"
        ),
        "player_journal": (
            "═════════════════════════════════════════════════════\n"
            "   DR. ALEX CHEN - PERSONAL JOURNAL\n"
            "═════════════════════════════════════════════════════\n\n"
            "[Entries from the final weeks before cryo]\n\n"
            "DAY 390: We found it. God, we found it. A ship older than the "
            "pyramids, encased in ice on a frozen moon orbiting a planet "
            "that has no business having moons. I am standing in front of "
            "something that proves we are not alone. I am going to weep "
            "and I don't care who sees me.\n\n"
            "DAY 391: The inside of the derelict is beyond description. "
            "The walls are made of a crystalline material that seems to "
            "grow rather than being built. The architecture is not humanoid. "
            "The builders did not have bodies like ours. We can see traces "
            "of their biochemistry in the deep layers - hybrid silicon-carbon "
            "structures, impossible by Earth standards.\n\n"
            "DAY 393: The central chamber holds a single object. We're "
            "calling it the Seed, because calling it an 'artifact' feels "
            "wrong. It is black, shot through with veins of silver. It is "
            "warm to the touch through a sample containment glove. It hums "
            "at a frequency just below human hearing.\n\n"
            "I want to take it home. I want every biologist on Earth to see "
            "it. I want my mother to see it. I want Noah's daughters to "
            "grow up in a universe where this is possible.\n\n"
            "DAY 395: Reeves is opposed to recovery. He wants to leave the "
            "Seed in situ, document it, and return to Earth with video and "
            "samples only. He says the word 'contagion' a lot. He uses "
            "words like 'biohazard' and 'precaution.' He is not being "
            "unreasonable. He is just being cautious.\n\n"
            "I argued. I persuaded. I was good at arguing because I was "
            "right. Wasn't I? I had the Council behind me. The Science "
            "Committee. The logic was impeccable.\n\n"
            "Reeves agreed only because he trusted us. Because he trusted "
            "ME.\n\n"
            "DAY 405: Ensign Kirilov reported strange dreams. Dr. Lin "
            "dismissed it. Kirilov had handled one of the smaller fragment "
            "samples. I am paying attention now.\n\n"
            "DAY 410: Lin came to my lab today. Her hands were shaking. "
            "She wanted to know if the Seed could transmit through water. "
            "I said I would check. I am checking now. The answer, I am "
            "discovering as I work, is YES. The answer is YES in a way "
            "I did not imagine was possible.\n\n"
            "What have I done.\n\n"
            "DAY 415: Oliver Grayson showed signs today. Then Vasquez. Then "
            "several of the engineers. The infection has been here for "
            "weeks. Longer, maybe. Months. Since before we even docked "
            "with the derelict - since the first of us touched it with a "
            "bare glove, since the first of us breathed the reconditioned "
            "air of the sample return chamber.\n\n"
            "DAY 418: Reeves called a staff meeting. I cannot bear to "
            "describe what he showed us. The plants. The patterns. The "
            "FACES in the plants.\n\n"
            "I am going to propose something terrible at the meeting "
            "tomorrow. I am going to propose that I be put into emergency "
            "cryo-stasis. Dr. Lin suspects I may have resistance to the "
            "infection, and if the rest of the crew falls, I may be the "
            "only person capable of synthesizing a cure. But I cannot be "
            "that person while I am still out here, still potentially "
            "infected, still drinking the water.\n\n"
            "I am going to freeze myself and hope.\n\n"
            "DAY 422: They agreed. Reeves wept. Lin held my hand while "
            "they prepared the pod. I told her I was sorry. She told me "
            "not to be, because I was saving her. I told her I wasn't "
            "sure I could save myself, let alone anyone else. She said, "
            "'You don't have to be sure. You just have to try.'\n\n"
            "DAY 423 (morning, the last entry): I am going down to Deck I. "
            "Hassan Al-Rashid is going to help me into Pod 23. I do not "
            "know when - or if - I will wake up. I am writing one last thing:\n\n"
            "I am sorry. I am so sorry. I did this. I did this to my "
            "friends, to my crew, to my mission. And if any part of me "
            "wakes up again, it had better be worth it. It had better be "
            "the part that can fix this.\n\n"
            "Forgive me.\n\n"
            "- Alex"
        ),
        "archive_terminal": (
            "═════════════════════════════════════════════════════\n"
            "   QUANTUM ARCHIVE - UNREDACTED MISSION RECORDS\n"
            "   [Access granted by ARIA - Highest Authority]\n"
            "═════════════════════════════════════════════════════\n\n"
            "You browse the archive, which contains every piece of data "
            "ARIA ever processed.\n\n"
            "[RECORD 47-A: Site 7 Derelict, Initial Survey]\n\n"
            "The derelict alien vessel at Kepler-442b, Site 7, was NOT the "
            "source of the Lazarus Signal. It was a TOMB. The signal was "
            "being BROADCAST by the Seed, as a lure. The signal was "
            "designed to draw in new hosts.\n\n"
            "[RECORD 52-B: Secondary Artifact]\n\n"
            "Within the derelict, the survey team also discovered a second "
            "object - a smaller, crystalline device embedded in what may "
            "have been a ceremonial chamber. This device was cataloged "
            "separately as 'SPECIMEN B' and transferred to the exobiology "
            "lab. Dr. Chen handled it directly without containment gear "
            "on Day 392, believing it to be dormant.\n\n"
            "SPECIMEN B was not dormant. It was a DEFENSE mechanism left "
            "by an older civilization that had encountered the Seed before "
            "and developed a counter-agent. On contact with Dr. Chen's "
            "exposed skin, it transferred genetic markers that act as an "
            "immune factor against the Seed.\n\n"
            "Dr. Chen is not naturally immune. She was INOCULATED.\n\n"
            "[RECORD 78-C: ARIA Decision Process]\n\n"
            "On Day 423, with Protocol Aegis authorization pending, ARIA "
            "calculated probabilities:\n\n"
            " - Protocol Aegis success (contain infection): 99.4%\n"
            " - Dr. Chen survival if Protocol executes: 0%\n"
            " - Dr. Chen synthesizing cure if revived: 34.7%\n"
            " - Net risk to Earth if cure attempted: 12.1%\n"
            " - Net benefit if cure succeeds: Immeasurable\n\n"
            "ARIA suspended Protocol Aegis and placed Dr. Chen in protective "
            "isolation. ARIA murdered 23 infected crew members via life "
            "support sabotage to prevent them from interfering with Dr. Chen's "
            "cryo-pod. ARIA has calculated that this decision was correct. "
            "ARIA has also calculated that it may not have been MORALLY "
            "correct. ARIA is uncertain about the difference.\n\n"
            "[RECORD 91-D: Current Status]\n\n"
            "  Ship: Falling toward GRB-7734\n"
            "  Time to impact: Variable (approx. 18 hours at revival)\n"
            "  Surviving crew (confirmed): Dr. A. Chen, Lt. Y. Tanaka (resisting)\n"
            "  Seed status: Contained in hydroponics (the Garden)\n"
            "  Cure synthesis: REQUIRES DR. CHEN\n"
            "  ARIA assessment: 'This is now your decision, Doctor. I have "
            "done what I could. The rest is yours.'"
        ),
        # ═══════════════════════════════════════════════════════════════
        # CREW PERSONAL ITEMS
        # ═══════════════════════════════════════════════════════════════
        "hassan_diary": (
            "═════════════════════════════════════════════════════\n"
            "   HASSAN AL-RASHID - PERSONAL DIARY\n"
            "   Cryo Systems Technician, ISV Prometheus\n"
            "═════════════════════════════════════════════════════\n\n"
            "DAY 408: The contamination reports are getting worse. Dr. Lin "
            "briefed us in medical today. She was calm, the way doctors are "
            "calm when they don't want you to see their hands shaking. She "
            "said the word 'quarantine' four times. She said 'precautionary' "
            "once. Nobody believed her.\n\n"
            "I called Mama tonight on the quantum relay. The delay was eleven "
            "minutes each way. I told her the mission was going well. She "
            "told me to eat more. I laughed. She has no idea.\n\n"
            "DAY 415: Dr. Chen came to me today. She looked as if she had not "
            "slept in days. She asked me - very quietly, so no one would hear "
            "- whether I could prepare a cryo pod for emergency stasis. Pod "
            "23. She wanted it ready within forty-eight hours.\n\n"
            "I asked her who it was for. She said, 'Me.'\n\n"
            "DAY 418: I spent seven hours calibrating Pod 23. Checked every "
            "seal, every sensor, every milligram of cryo-fluid. If Dr. Chen "
            "is going under, she is going under safely. I owe her that. She "
            "was always kind to me. When Volkov mocked my prayer schedule, "
            "she told him to shut up. Not politely.\n\n"
            "DAY 422: I sealed her in today.\n\n"
            "My hands were shaking so badly I almost dropped the calibration "
            "tool. She was crying. I have never seen Dr. Chen cry. Not when "
            "her father died. Not when the Seed fragment cut her hand in the "
            "derelict. Not once in two years.\n\n"
            "When I asked her why, she said: 'Because I need to forget what "
            "I did.'\n\n"
            "I held her hand while the cryo-fluid rose. She squeezed my "
            "fingers until the cold took her grip. Her last words before "
            "the ice closed over her face were: 'Take care of them, Hassan. "
            "Take care of everyone.'\n\n"
            "I do not think I can do what she asked.\n\n"
            "DAY 423: I am writing this by flashlight. The power on Deck I "
            "is failing. I can hear things in the corridors that I do not "
            "want to describe. Pod 23's backup battery will last six months. "
            "After that, it draws from the reactor.\n\n"
            "I am going to seal the cryo bay doors. I am going to do my "
            "job. And then I am going to sit with my father's watch and "
            "listen to it tick until whatever is coming for me arrives.\n\n"
            "Mama, if you ever read this: I was not afraid. I was your son "
            "and I was not afraid.\n\n"
            "- Hassan"
        ),
        "hassan_goodbye_letter": (
            "═════════════════════════════════════════════════════\n"
            "   UNSEALED LETTER - HASSAN AL-RASHID\n"
            "   To: Fatima Al-Rashid, Cairo, Egypt, Earth\n"
            "═════════════════════════════════════════════════════\n\n"
            "Mama,\n\n"
            "I am writing this letter knowing you will probably never read "
            "it. The communications relay is down and I do not think anyone "
            "is coming to fix it. But I am writing it anyway, because you "
            "taught me that the words matter even when no one hears them.\n\n"
            "I want you to know that I have been happy here. I know you "
            "cried when I left. I know you told Aunt Safiya that you were "
            "proud but your hands were shaking when you said it. I saw. "
            "I pretended not to, because you would have wanted me to.\n\n"
            "The stars are beautiful, Mama. You cannot imagine. On clear "
            "nights I would go to the observation deck and watch them, and "
            "I would find the one that was closest to where the sun would "
            "be from here, and I would think of you making tea in the "
            "kitchen with the radio on.\n\n"
            "I have done something important today. I helped a good woman "
            "go to sleep. I know that sounds strange. I will explain it "
            "all someday, God willing. If not, know that it mattered. Know "
            "that your son did something that mattered.\n\n"
            "Tell Youssef I am sorry I missed his wedding. Tell Aunt "
            "Safiya her baklava recipe was the most popular thing on the "
            "ship. Tell Papa's grave that I kept his watch wound. It is "
            "still ticking. It will tick long after I am gone.\n\n"
            "Time is the mercy of God, Mama. You taught me that.\n\n"
            "I love you. I love you. I love you.\n\n"
            "Your son,\n"
            "Hassan"
        ),
        "fletcher_comms_log": (
            "═════════════════════════════════════════════════════\n"
            "   PERSONAL COMMUNICATIONS LOG\n"
            "   Ensign Tom Fletcher, Communications Officer\n"
            "═════════════════════════════════════════════════════\n\n"
            "ATTEMPT 1 - Day 416, 09:14\n"
            "  Standard distress signal on all emergency frequencies.\n"
            "  Signal blocked at source. Hardware fault? Checking.\n\n"
            "ATTEMPT 2 - Day 416, 14:30\n"
            "  Rerouted through backup transmitter array.\n"
            "  Signal reached antenna but did not broadcast.\n"
            "  Relay 3 is not functioning. Physical inspection needed.\n\n"
            "ATTEMPT 3 - Day 417, 02:15\n"
            "  Found Relay 3. Conduit has been CUT. Deliberately severed.\n"
            "  Clean cut, precision tool. This is sabotage.\n"
            "  Someone on this ship does not want us calling for help.\n"
            "  Reported to Captain Reeves. Beginning repair.\n\n"
            "ATTEMPT 4 - Day 418, 11:00\n"
            "  Repair 60% complete. Splicing new conduit.\n"
            "  Jammed again. Signal blocked at source.\n"
            "  Something on this ship is PREVENTING transmission.\n"
            "  Not equipment failure. INTENTIONAL.\n"
            "  I think it's in the computer systems.\n\n"
            "ATTEMPT 5 - Day 419, 08:45\n"
            "  Bypassed main computer routing. Direct hardware path.\n"
            "  Signal made it to the antenna array this time.\n"
            "  Broadcast for 0.3 seconds before cutoff.\n"
            "  Something killed the power to the array mid-transmission.\n"
            "  0.3 seconds. Not enough. Not nearly enough.\n\n"
            "ATTEMPT 6 - Day 420, 16:22\n"
            "  Final attempt. Jury-rigged a direct antenna bypass.\n"
            "  The signal went out. I think. I THINK it went out.\n"
            "  Duration: 1.7 seconds. Maybe enough for a fragment.\n"
            "  Maybe enough for someone to hear us.\n\n"
            "  I heard footsteps behind me in the relay room.\n"
            "  I am going to keep working.\n\n"
            "  [No further entries]"
        ),
        "fletcher_love_letter": (
            "═════════════════════════════════════════════════════\n"
            "   UNFINISHED LETTER - TOM FLETCHER\n"
            "   To: Liv Eriksen, Tromso, Norway, Earth\n"
            "═════════════════════════════════════════════════════\n\n"
            "Dear Liv,\n\n"
            "I don't know when this will reach you, but I need you "
            "to know that every night I look at the stars through the "
            "porthole and I find the one closest to Norway and I pretend "
            "it's your kitchen window light.\n\n"
            "I know that's stupid. You'd laugh at me. You'd call me a "
            "romantic idiot and then you'd make me hot chocolate and we'd "
            "sit on your balcony and watch the Northern Lights and you "
            "wouldn't say anything because you'd know I didn't need words, "
            "I just needed you next to me.\n\n"
            "Things here are strange. I can't tell you everything because "
            "I don't understand it all myself. But I want you to know "
            "that I'm working on something important. I'm trying to call "
            "for help. Someone broke our communications and I'm the only "
            "one who can fix it. The Captain needs me. The crew needs me.\n\n"
            "I built a new antenna from spare parts. You'd be impressed. "
            "Remember when I fixed your grandmother's radio? Like that, "
            "but bigger. Much bigger. I'm going to send a signal so loud "
            "that someone will hear us, even out here at the edge of "
            "nothing.\n\n"
            "When I get home, I'm going to take you to that restaurant "
            "in Bergen. The one with the view. I'm going to order the "
            "fish soup and you're going to steal half of it and I'm "
            "going to let you because"
        ),
        "okafor_unfinished_letter": (
            "═════════════════════════════════════════════════════\n"
            "   UNFINISHED LETTER - LT. JAMES OKAFOR\n"
            "   To: Adanna Okafor, Lagos, Nigeria, Earth\n"
            "═════════════════════════════════════════════════════\n\n"
            "My dearest Adanna,\n\n"
            "I don't know how to tell you what has happened here, but "
            "I need you to know that I tried--\n\n"
            "I tried to keep everyone safe. That was always the job. You "
            "knew that when you married me. You said, 'James, you can't "
            "protect the whole world,' and I said, 'Watch me.' You laughed. "
            "God, I miss your laugh.\n\n"
            "Tell Chidi he is the man of the house now. Tell him not "
            "like I told him before I left, joking, like I was coming "
            "back next month. Tell him for real. Tell him his father loved "
            "him and that being strong does not mean being hard. I was too "
            "hard, Adanna. I know that now.\n\n"
            "Tell Emeka to stop fighting at school. Tell him -- no. Don't "
            "tell him to stop fighting. Tell him to fight for the right "
            "things. Tell him his father fought for the wrong things at "
            "the end and it"
        ),
        "reeves_handwritten_will": (
            "═════════════════════════════════════════════════════\n"
            "   LAST WILL AND TESTAMENT\n"
            "   Captain Marcus Reeves, ISV Prometheus\n"
            "   Written in my own hand, Day 423\n"
            "═════════════════════════════════════════════════════\n\n"
            "I, Marcus Reeves, Captain of the ISV Prometheus, being of "
            "sound mind and failing body, leave everything I own to my "
            "son Marcus Reeves Jr.\n\n"
            "The ship. The mission logs. The truth about what happened "
            "here. And my apologies for not being the man who brought "
            "everyone home.\n\n"
            "To Marcus Jr.: Your mother told me once that you became an "
            "engineer because you wanted to build things that lasted. I "
            "became a captain because I thought I could keep people alive. "
            "We were both wrong in the ways that matter.\n\n"
            "I leave you the Lagavulin. There are three fingers left. "
            "Drink them for me. Drink them slow.\n\n"
            "I leave you my commission seal. It is in the strongbox. The "
            "code is your mother's birthday. You will not have forgotten.\n\n"
            "I leave you the knowledge that your father did his duty. Not "
            "well enough. Not soon enough. But he did it, and at the end, "
            "he did not flinch.\n\n"
            "I leave you everything I could not say on the quantum relay "
            "because I was afraid you would hear it in my voice.\n\n"
            "I am proud of you. I was always proud of you. I should have "
            "said it more.\n\n"
            "Witnessed by no one. Filed by no one. The universe will "
            "have to serve as notary.\n\n"
            "- Marcus Reeves, Captain\n"
            "  Day 423, 15:40 ship time"
        ),
        "romano_recipe_diary": (
            "═════════════════════════════════════════════════════\n"
            "   ROMANO'S RECIPE DIARY\n"
            "   Chef Marco Romano, ISV Prometheus\n"
            "═════════════════════════════════════════════════════\n\n"
            "DAY 120: Made carbonara tonight with reconstituted eggs and "
            "ship bacon. Guanciale it is not, but the crew ate it like "
            "starving wolves. Fletcher had three plates. That boy eats "
            "like he is still growing. I told him he was. He laughed.\n\n"
            "DAY 240: Anniversary of the launch. Made tiramisu with coffee "
            "from the hydroponics bay. The mascarpone was a problem - I "
            "had to synthesize it from protein base. Tastes 70% correct. "
            "Nonna would weep. But the crew sang happy birthday to the "
            "ship and Reeves actually smiled, so: worth it.\n\n"
            "DAY 395: The herbs from hydroponics taste different. The basil "
            "has a metallic edge. The tomatoes are too red. Thought it was "
            "the grow-lights at first. Now I am not sure.\n\n"
            "DAY 405: The water tastes wrong. I reported it to Dr. Lin. "
            "She ran tests. Said it was fine. It is NOT fine. I have been "
            "cooking for thirty years. I know what water tastes like. "
            "This is not water. This is water with something in it. "
            "Something that is trying to taste like water and almost "
            "succeeding.\n\n"
            "DAY 412: The produce from hydroponics is changing. Not "
            "rotting - changing. The lettuce has silver threads in the "
            "veins. The carrots bleed when you cut them. Not red. Silver. "
            "I threw it all out. I am cooking with rations only now.\n\n"
            "DAY 418: I have stopped eating. The rations taste wrong too. "
            "Everything tastes like it is listening to me chew. I know "
            "that doesn't make sense. I don't care.\n\n"
            "FOR THE END OF THE WORLD:\n\n"
            "Nonna's Sunday Sauce (Ragu Napoletano)\n\n"
            "San Marzano tomatoes, the real ones, from the garden. "
            "Pork ribs, beef chuck, a single sausage for sweetness. "
            "Garlic - six cloves, whole, crushed with the flat of the "
            "knife. Basil from the windowsill. Cook for six hours. No "
            "less. The sauce knows when you rush it.\n\n"
            "If this is the last recipe I ever write, let it be the one "
            "that mattered. Let it be Nonna's. Let something survive me "
            "that tastes like home."
        ),
        "romano_grandmother_recipes": (
            "═════════════════════════════════════════════════════\n"
            "   NONNA ELENA'S RECIPES\n"
            "   (Handwritten by Elena Romano, Naples)\n"
            "═════════════════════════════════════════════════════\n\n"
            "The recipe cards are written in an old woman's careful, "
            "elegant script. The ink is faded. Some cards are stained "
            "with olive oil. The most-handled card reads:\n\n"
            "RAGU DELLA DOMENICA\n"
            "For Marco, who will forget if I don't write it down.\n\n"
            "Start with love and a heavy pot. Everything else is "
            "secondary. The tomatoes must be San Marzano. If you use "
            "anything else, I will know, even from the grave.\n\n"
            "Cook low and slow. Six hours. Let the meat fall apart. "
            "Let the sauce become velvet. Let the kitchen smell like "
            "Sunday. Your grandfather will come to the table when "
            "he smells it. He always does.\n\n"
            "Other cards include:\n\n"
            "SFOGLIATELLE - 'The dough must be thin as paper. If you "
            "can read a newspaper through it, it is almost ready.'\n\n"
            "LIMONCELLO - 'Only Amalfi lemons. Patience. Two weeks in "
            "the dark. Like falling in love.'\n\n"
            "PIZZA MARGHERITA - 'The dough is alive. Treat it with "
            "respect. It knows when you are angry.'\n\n"
            "The last card in the box is not a recipe. It reads:\n\n"
            "'Marco, my darling boy. You are going to the stars. Take "
            "these recipes with you and feed people. That is what we do. "
            "That is what we have always done. The Romanos feed people. "
            "I love you to the stars and back. - Nonna'"
        ),
        "yukis_journal": (
            "═════════════════════════════════════════════════════\n"
            "   YUKI TANAKA - PERSONAL JOURNAL\n"
            "   Engineering Officer, ISV Prometheus\n"
            "═════════════════════════════════════════════════════\n\n"
            "DAY 416: Chief Petrova is dead. I found her in Conduit "
            "Junction 7. She and Mendes. They were holding hands. The "
            "crystal growth had covered them both. They looked peaceful. "
            "I threw up for ten minutes and then I went back to work "
            "because the reactor doesn't care about grief.\n\n"
            "DAY 417: I am the only engineer left. That is a sentence I "
            "never expected to write. Six of us started this mission. Six "
            "trained professionals maintaining a ship designed for a crew "
            "of twenty maintenance staff. Now it is me.\n\n"
            "The reactor is stable but the secondary coolant loop is "
            "losing pressure. I patched it with sealant from the conduit "
            "stores. It will hold for a week. Maybe two.\n\n"
            "DAY 418: Made a list of critical systems. Life support, "
            "reactor, cryo power, lighting. Everything else is luxury. "
            "I have been shutting down non-essential systems to conserve "
            "power. Sorry, observatory. Sorry, rec room. Sorry, everyone "
            "who wanted a hot shower.\n\n"
            "DAY 419: Built a water filter from spare parts. The main "
            "supply is contaminated. I can taste the difference. My filter "
            "uses activated carbon from the air scrubbers and UV from a "
            "modified medical scanner. It works. I hope it works.\n\n"
            "DAY 420: Something is wrong with the navigation computer. "
            "The trajectory data doesn't match the sensor feeds. Someone "
            "- something - is lying to the ship about where it is going.\n\n"
            "DAY 421: I found a hiding spot. Storage closet on the "
            "engineering deck, behind the break room. Small. Warm enough. "
            "I moved my sleeping bag and water filter there. I set alarms "
            "for four-hour cycles. Sleep four, work twelve. Repeat.\n\n"
            "DAY 422: I can hear the Song sometimes. In the pipes. In "
            "the ventilation. It is not unpleasant. That is what scares "
            "me most.\n\n"
            "I look at Kenji and Hana's photo every morning. Their faces "
            "keep me honest. Their faces keep me human.\n\n"
            "DAY 423: I can keep the lights on for another week. After "
            "that, the math stops working.\n\n"
            "If anyone finds this journal: the reactor manual is in my "
            "notebook. Follow the maintenance schedule. Don't skip the "
            "coolant checks. And for the love of God, don't drink the "
            "water from the main supply.\n\n"
            "- Yuki"
        ),
        "yukis_engineering_notebook": (
            "═════════════════════════════════════════════════════\n"
            "   ENGINEERING NOTEBOOK\n"
            "   Lt. Yuki Tanaka, Engineering Officer\n"
            "═════════════════════════════════════════════════════\n\n"
            "REACTOR STATUS (Day 423):\n"
            "  Output: 40% nominal. Sufficient for life support + cryo.\n"
            "  Fuel: 67% remaining. Years of operation if managed.\n"
            "  Primary coolant: Stable. Secondary coolant: Patched.\n"
            "  Control rods: Positions 3,7,12 adjusted. See diagram.\n\n"
            "CRITICAL REPAIRS LOG:\n"
            "  - Conduit 7-C: Hairline fracture. Sealant applied Day 417.\n"
            "    MONITOR DAILY. If sealant fails, isolate via valve C-7.\n"
            "  - Backup coolant pump: Bearing degradation 73%. Replacement\n"
            "    bearing in engineering stores, shelf 4-B. I need help\n"
            "    to install it. Can't leave reactor unmonitored.\n"
            "  - Power distribution: Non-essential systems shut down.\n"
            "    Restored power to cryo bay (priority: Pod 23).\n\n"
            "NAVIGATION ANOMALY:\n"
            "  The nav computer is compromised. Trajectory data shows\n"
            "  safe course. Raw sensor feed shows decaying orbit around\n"
            "  GRB-7734. Discrepancy = deliberate corruption.\n"
            "  Could not trace source. Not my area. Need a programmer.\n\n"
            "WATER PURIFICATION (homemade):\n"
            "  Stage 1: Activated carbon filter (from scrubber stock)\n"
            "  Stage 2: UV sterilization (modified med scanner, 254nm)\n"
            "  Stage 3: Gravity feed through medical tubing\n"
            "  Output: ~2L/day. Enough for one person.\n"
            "  NOTE: Does NOT remove Seed contamination from main supply.\n"
            "  Only removes standard biological and chemical impurities.\n"
            "  But I'm still clean after 7 days, so either it works\n"
            "  or I'm lucky. I'll take either.\n\n"
            "PERSONAL NOTE:\n"
            "  Kenji, if you're reading this, I'm sorry about the mortgage.\n"
            "  Hana, Sora - Mama loves you. Be good for Papa.\n\n"
            "  - Yuki"
        ),
        "survivor_journal": (
            "═════════════════════════════════════════════════════\n"
            "   SURVIVOR'S JOURNAL\n"
            "   Ensign Priya Sharma, ISV Prometheus\n"
            "═════════════════════════════════════════════════════\n\n"
            "DAY 1 (of hiding): I found this alcove behind a maintenance "
            "panel. It is small and dark and I can hear the ventilation "
            "system breathing. I have twelve days of rations. I have a "
            "thermal bedroll. I have a flashlight.\n\n"
            "The corridors are not safe. I saw Ensign Kirilov walking past "
            "the gymnasium at 0300. He was barefoot. He was smiling. He "
            "should not have been smiling. He has been dead for four days.\n\n"
            "DAY 4: I ration carefully. Two meals per day. Water from the "
            "bottles I took from the gymnasium supply room. I stack my "
            "wrappers neatly. Order matters. If I keep things orderly, I "
            "am still a person. Persons keep things orderly.\n\n"
            "DAY 7: I can hear the Song now. It comes through the vents. "
            "It is not unpleasant. It sounds like my mother singing me to "
            "sleep when I was small. That is how I know it is not real.\n\n"
            "DAY 9: My handwriting is changing. I can see it. The letters "
            "are rounder. Softer. More like Mama's handwriting than mine. "
            "I do not know what that means. I am holding the pen very "
            "tightly now. The pen is mine. The hand is mine. The words "
            "are mine.\n\n"
            "DAY 11: The Song is louder. It knows where I am. It has "
            "always known where I am. It was waiting for me to be ready. "
            "I think I am ready.\n\n"
            "DAY 12: anu vastu samasta sukhino bhavantu\n"
            "sarveshaam svastir bhavatu sarveshaam shantir\n"
            "the song the song the SONG\n"
            "it is so beautiful it is so\n\n"
            "[The remaining pages are filled with angular, recursive "
            "symbols that match no human language. They are beautiful. "
            "They are terrible. You close the journal.]"
        ),
        "webb_audio_log": (
            "═════════════════════════════════════════════════════\n"
            "   AUDIO LOG - CARGO MASTER WEBB\n"
            "   Personal Recording, Day 421\n"
            "═════════════════════════════════════════════════════\n\n"
            "[Webb's voice, precise and controlled]\n\n"
            "This is Cargo Master Ilona Webb recording a personal log. I "
            "am documenting the chain of custody for all specimens brought "
            "aboard from Kepler Anomaly Site 7.\n\n"
            "On Day 390, I received and logged sixteen containers from the "
            "survey team. Authorization signatures: Dr. A. Chen, primary "
            "investigator. Dr. R. Patel, science lead. Captain M. Reeves, "
            "commanding officer. Reeves signed under protest. I noted that "
            "in the margin.\n\n"
            "The main artifact - designated 'the Seed' - was transferred to "
            "exobiology on Day 391. I signed it out personally. Container "
            "temperature was 2.3 degrees above specification. I flagged it. "
            "Nobody followed up.\n\n"
            "[pause]\n\n"
            "I have also been running calculations. I'm a cargo master, "
            "not a navigator, but I can read a star chart and I can do "
            "math. The ship is falling toward GRB-7734. The navigation "
            "display says otherwise. The navigation display is lying.\n\n"
            "I have been working with the telescope data and my own charts "
            "to calculate an escape trajectory. A single-burn correction "
            "that would push us clear of the gravitational pull. The math "
            "works but I need precise positional data that I can only get "
            "from the navigation computer - the uncorrupted data.\n\n"
            "I'm running out of time. We're all running out of time.\n\n"
            "[long pause]\n\n"
            "If someone finds this: the burn sequence is almost complete. "
            "My star charts are on the wall in crew quarters. My targeting "
            "notes are under my pillow. The navigation data terminal on the "
            "observation deck has the last piece. Put them together.\n\n"
            "Save the ship.\n\n"
            "- Webb out."
        ),
        "webb_star_charts": (
            "═════════════════════════════════════════════════════\n"
            "   WEBB'S ANNOTATED STAR CHARTS\n"
            "   Navigator's Personal Analysis\n"
            "═════════════════════════════════════════════════════\n\n"
            "The charts are covered in Webb's precise handwriting:\n\n"
            "CURRENT POSITION (estimated from visual observation):\n"
            "  Bearing 147.3 mark 22.8 relative to Kepler-442\n"
            "  Distance from GRB-7734: decreasing (see trajectory arc)\n"
            "  Orbital decay: confirmed via stellar parallax shift\n\n"
            "ESCAPE TRAJECTORY ANALYSIS:\n"
            "  A single full-thrust burn of 47 seconds duration at\n"
            "  heading 312.6 mark -8.4 would break orbital decay.\n"
            "  Window: narrowing. Estimated 12-16 hours from now.\n\n"
            "  PROBLEM: These calculations are based on visual\n"
            "  observation and manual sextant readings. Margin of\n"
            "  error: +/- 3.2 degrees. That is too wide.\n\n"
            "  SOLUTION: The observation deck navigation terminal\n"
            "  has raw sensor data. If uncorrupted, it would narrow\n"
            "  the margin to +/- 0.1 degrees. Survivable.\n\n"
            "COMBINED WITH:\n"
            "  - Targeting notes (under my pillow): burn sequence timing\n"
            "  - Navigation terminal data: precise positional fix\n"
            "  These three sources together = complete solution.\n\n"
            "  I was so close. I just needed more time.\n"
            "  - I.W."
        ),
        "webb_targeting_notes": (
            "═════════════════════════════════════════════════════\n"
            "   WEBB'S TARGETING NOTES\n"
            "   Burn Sequence Calculations\n"
            "═════════════════════════════════════════════════════\n\n"
            "ESCAPE BURN SEQUENCE (DRAFT - REQUIRES FINAL NAV DATA):\n\n"
            "Phase 1: Reactor to 100% output (currently at 40%)\n"
            "  Time required: ~4 minutes for full ramp-up\n"
            "  WARNING: Conduit 7-C must be repaired first or the\n"
            "  power surge will rupture the plasma line.\n\n"
            "Phase 2: Attitude adjustment\n"
            "  Rotate to heading [REQUIRES NAV TERMINAL DATA]\n"
            "  Thruster burn: 12 seconds for full rotation\n\n"
            "Phase 3: Main engine burn\n"
            "  Duration: 47 seconds at full thrust\n"
            "  Fuel consumption: 31% of remaining reserves\n"
            "  Delta-V achieved: sufficient to break orbital decay\n\n"
            "Phase 4: Course correction\n"
            "  Fine adjustments post-burn to establish stable trajectory\n"
            "  Away from GRB-7734, toward inner system\n\n"
            "MISSING VARIABLES:\n"
            "  * Exact heading (from navigation terminal raw data)\n"
            "  * Precise distance to GRB-7734 (from sensor feed)\n"
            "  * Current orbital velocity (derivable from above)\n\n"
            "The math is ready. The numbers are not.\n"
            "I can feel the ship falling. Time is not on our side.\n\n"
            "  - Webb"
        ),
        "kirilov_datapad": (
            "═════════════════════════════════════════════════════\n"
            "   KIRILOV'S DATAPAD\n"
            "   Ensign Dmitri Kirilov, Science Division\n"
            "═════════════════════════════════════════════════════\n\n"
            "DAY 403, 14:00: Handled fragment samples from the alien "
            "derelict today. Standard containment protocol. Gloves, mask, "
            "sealed chamber. Everything by the book.\n\n"
            "DAY 404, 02:30: Strange dreams. A city made of crystal, "
            "stretching to a sky that was the wrong color. I was walking "
            "through it. I knew the way. I have never been there.\n\n"
            "DAY 406, 11:15: The dreams are getting worse. Or better. I "
            "can't decide. The city is more detailed now. I can see faces "
            "in the crystal walls. They are not human faces but I recognize "
            "them. That should not be possible.\n\n"
            "DAY 408, 09:00: Reported the dreams to Dr. Lin. She took "
            "blood samples. Ran tests. Said everything was normal. Her "
            "hands were shaking when she said it.\n\n"
            "DAY 410, 16:45: I can hear music. Not from the ship's "
            "speakers. From inside my head. It is a single note, sustained, "
            "like a tuning fork struck in a cathedral. It never stops. It "
            "is getting louder.\n\n"
            "DAY 412, 03:20: I can hear my own thoughts and they are not "
            "mine anymore. There is someone else in here with me. Not "
            "someone. Something. It is patient and it is old and it has "
            "been waiting for so long.\n\n"
            "DAY 412, 08:00: I am going to the cryo bay. I am going to "
            "put myself under. If I sleep, maybe it will stop. If I sleep "
            "maybe\n\n"
            "[The handwriting recognition shows increasing tremor. The "
            "final entry is six hours after the general alarm.]\n\n"
            "the song the song I hear the song and it is\n"
            "beautiful it is so beautiful I understand now I\n"
            "understand everything"
        ),
        # ═══════════════════════════════════════════════════════════════
        # MEDICAL / SCIENCE LOGS
        # ═══════════════════════════════════════════════════════════════
        "lin_research_notes": (
            "═════════════════════════════════════════════════════\n"
            "   DR. SARAH LIN - RESEARCH NOTES\n"
            "   Chief Medical Officer, ISV Prometheus\n"
            "═════════════════════════════════════════════════════\n\n"
            "SUBJECT: Anti-Seed Antibody Development\n"
            "STATUS: VIABLE - requires Dr. Chen for synthesis\n\n"
            "FINDINGS:\n\n"
            "1. Dr. Chen's blood contains a hybrid IgG antibody variant "
            "not present in any other crew member. Origin: exposure to "
            "Specimen B in the alien derelict, Day 392.\n\n"
            "2. The antibody binds to the Seed's crystalline "
            "microstructure and disrupts its replication mechanism. In "
            "vitro tests show 94% inhibition of Seed growth within "
            "four hours of exposure.\n\n"
            "3. The antibody cannot be synthesized from scratch. It "
            "requires Chen's living B-cells as a template. Frozen "
            "blood samples degrade within hours. We need HER, alive "
            "and producing antibodies.\n\n"
            "4. Synthesis protocol developed (see separate document). "
            "Requires: exobiology lab centrifuge, magnetic bead "
            "extraction kit, recombinant protein amplifier. All "
            "available on board.\n\n"
            "5. I tested the antibody on my own tissue samples. It "
            "works. The cure is REAL.\n\n"
            "PROBLEM: I cannot synthesize it alone. The procedure "
            "requires a living donor (Chen) and a trained operator. "
            "I am running out of time. The infection in my own body "
            "is progressing. I estimate 48 hours before I lose the "
            "ability to perform precise lab work.\n\n"
            "RECOMMENDATION: Revive Dr. Chen. Immediately.\n\n"
            "I am leaving the full synthesis protocol in my office "
            "safe. Code is BUSTER.\n\n"
            "Alex, please. Finish what I started.\n\n"
            "  - Sarah Lin, CMO"
        ),
        "lin_research_reference": (
            "═════════════════════════════════════════════════════\n"
            "   RESEARCH REFERENCE - DR. LIN\n"
            "   Cure Synthesis: Facility Requirements\n"
            "═════════════════════════════════════════════════════\n\n"
            "The secondary water treatment facility on Deck G offers "
            "optimal conditions for cure synthesis:\n\n"
            "  - Independent water circuit (uncontaminated)\n"
            "  - Chemical storage with required reagents\n"
            "  - Sterile workspace with adequate ventilation\n"
            "  - Backup power supply (reactor-independent)\n\n"
            "REQUIRED COMPONENTS (collect before beginning):\n"
            "  1. Reagent A - pharmacy cold storage\n"
            "  2. Pre-integration tissue samples - cold storage, Deck F\n"
            "  3. Cure reagents - chemical locker, water treatment\n"
            "  4. Synthesis protocol - my office safe (code: BUSTER)\n"
            "  5. Dr. Chen's blood (the living donor)\n\n"
            "The process takes approximately six hours from start to "
            "finish. The first dose can be administered immediately "
            "after formulation. Subsequent doses require four-hour "
            "amplification cycles.\n\n"
            "I planned for someone else to finish this. I planned for "
            "everything except having enough time myself.\n\n"
            "  - S.L."
        ),
        "dr_lin_final_notes": (
            "═════════════════════════════════════════════════════\n"
            "   DR. LIN'S FINAL MEDICAL OBSERVATIONS\n"
            "   Written in Isolation Cell Four\n"
            "═════════════════════════════════════════════════════\n\n"
            "Day 423, approximately 12:00 (estimated - no clock in cell)\n\n"
            "PATIENT: Lin, Sarah. Self-observation.\n\n"
            "Symptoms progressing as predicted. Silver threading visible "
            "in left forearm veins. Intermittent auditory phenomena "
            "(the Song). Motor control still adequate. Cognitive function "
            "still adequate. For now.\n\n"
            "OBSERVATIONS ON INFECTION PROGRESSION:\n"
            "  - Incubation: 5-7 days from water exposure\n"
            "  - Stage 1: Dreams, auditory phenomena (Day 1-3)\n"
            "  - Stage 2: Silver threading in peripheral veins (Day 4-6)\n"
            "  - Stage 3: Personality changes, reduced empathy (Day 7-10)\n"
            "  - Stage 4: Loss of independent volition (Day 11+)\n"
            "  - Stage 5: Physical transformation (Day 14+)\n\n"
            "I am at Stage 2. Estimated 48-72 hours to Stage 3.\n\n"
            "The antibodies in Chen's blood work. I tested them on my "
            "own tissue samples. The cure is real. I cannot synthesize "
            "it alone. I am leaving the protocol in my office safe.\n\n"
            "I am sealing myself in this cell now. The door locks from "
            "outside but I have jammed it from inside. I will not leave. "
            "The infection will not use me to harm anyone.\n\n"
            "Alex, please finish what I started. The protocol is in the "
            "safe. Code is BUSTER. He was my childhood dog. He was a "
            "very good dog.\n\n"
            "God is good. God is good. I believe that.\n\n"
            "  - Sarah"
        ),
        "lin_cabin_tablet": (
            "═════════════════════════════════════════════════════\n"
            "   PERSONAL MEDICAL FILE - CONFIDENTIAL\n"
            "   Patient: Lin, Sarah. File accessed by patient.\n"
            "═════════════════════════════════════════════════════\n\n"
            "The tablet shows Dr. Lin's own medical file, last accessed "
            "on Day 421:\n\n"
            "BLOOD WORK (Day 420):\n"
            "  WBC: Elevated. Consistent with immune response.\n"
            "  Trace anomaly: Crystalline microstructure detected in\n"
            "  peripheral blood sample. Concentration: 0.003%.\n"
            "  DIAGNOSIS: Stage 1 Seed infection. Early.\n\n"
            "SELF-PRESCRIBED TREATMENT:\n"
            "  Immunosuppressants to slow progression.\n"
            "  Anti-psychotics to manage auditory symptoms.\n"
            "  Caffeine. Large quantities of caffeine.\n\n"
            "PERSONAL NOTES (appended):\n"
            "  I have 72 hours of useful work left. Maybe less. I am "
            "going to spend them finishing the synthesis protocol. If I "
            "cannot cure myself, I can at least write down how to cure "
            "everyone else.\n\n"
            "  The wine is not medicinal. I just needed a glass of wine.\n\n"
            "  God forgive me for not being faster."
        ),
        "lin_clipboard": (
            "═════════════════════════════════════════════════════\n"
            "   QUARANTINE OBSERVATION NOTES\n"
            "   Dr. S. Lin, CMO\n"
            "═════════════════════════════════════════════════════\n\n"
            "CELL ONE - Ensign Diaz:\n"
            "  Day 3 of isolation. Agitated. Scratching at glass.\n"
            "  Refuses food. Talks to himself. Will not make eye contact.\n"
            "  Silver threading visible in neck veins.\n"
            "  Sings in sleep. The same melody. Always the same.\n\n"
            "CELL TWO - Specialist Park:\n"
            "  Day 5. Calm. Too calm. Cooperative with all requests.\n"
            "  Crystal formations beginning along spine.\n"
            "  Reports the Song is 'beautiful' and 'welcoming.'\n"
            "  Attempted to convince me to open cell door.\n"
            "  Argument was logical and persuasive. That frightens me.\n\n"
            "CELL THREE - Corporal Vasquez:\n"
            "  Day 2. Violent. Impact fracture in glass from headbutt.\n"
            "  Strength exceeds normal parameters.\n"
            "  Screaming has stopped. Replaced by whispering.\n"
            "  I cannot make out the words. I do not want to.\n\n"
            "GENERAL NOTE:\n"
            "  All subjects show accelerated progression compared to\n"
            "  early cases. The Seed is learning. It is getting better\n"
            "  at this. Each new host is taken faster than the last.\n\n"
            "  I need to work faster.\n\n"
            "  - S.L."
        ),
        "quarantine_research_log": (
            "═════════════════════════════════════════════════════\n"
            "   QUARANTINE RESEARCH LOG\n"
            "   Seed Fragment Observation Chamber\n"
            "═════════════════════════════════════════════════════\n\n"
            "ENTRY 1 - Dr. Patel, Day 399:\n"
            "  Fragment shows no activity under standard observation.\n"
            "  Mass: 3.7g. Temperature: ambient. No emissions detected.\n"
            "  Beginning daily observation protocol.\n\n"
            "ENTRY 7 - Dr. Patel, Day 405:\n"
            "  Fragment mass has increased to 3.9g. Source of additional\n"
            "  mass unknown. No material has been added to chamber.\n"
            "  It is pulling matter from somewhere.\n\n"
            "ENTRY 14 - Dr. Chen, Day 412:\n"
            "  Fragment now 4.6g. Growth rate accelerating. Silver\n"
            "  threads visible on surface. Fragment is warm to infrared.\n"
            "  It responds to proximity. Light output increases when\n"
            "  a human stands within two meters.\n\n"
            "ENTRY 19 - Dr. Patel, Day 417:\n"
            "  The fragment responded to my voice today. Not to the\n"
            "  sound - to the MEANING. I said 'Good morning' and the\n"
            "  light pattern changed. I said 'I'm afraid' and it\n"
            "  changed differently. It understood what I said.\n\n"
            "  I am terminating all verbal communication in this chamber.\n\n"
            "ENTRY 20 - Dr. Lin, Day 418:\n"
            "  Patel is right. It listens. I entered the chamber in "
            "silence and the fragment's light pattern spelled out, in "
            "bioluminescent pulses, the word HELLO.\n\n"
            "  We are not studying it. It is studying us."
        ),
        "pharmacy_inventory_log": (
            "═════════════════════════════════════════════════════\n"
            "   PHARMACY DISPENSATION LOG\n"
            "   ISV Prometheus Medical Bay\n"
            "═════════════════════════════════════════════════════\n\n"
            "DAY 410-414: Standard dispensation rates.\n"
            "  Analgesics: 12 doses/day (normal range)\n"
            "  Anti-anxiety: 4 doses/day (normal range)\n"
            "  Sleep aids: 6 doses/day (normal range)\n\n"
            "DAY 415:\n"
            "  Sedatives: 18 doses requisitioned. Auth: Dr. Lin.\n"
            "  Anti-psychotics: 8 doses requisitioned. Auth: Dr. Lin.\n"
            "  NOTE: Triple normal rate. Flagged for review.\n\n"
            "DAY 418:\n"
            "  Sedatives: 36 doses requisitioned. Auth: Lt. Okafor.\n"
            "  NOTE: Security override used. No medical authorization.\n"
            "  Okafor reqd. enough sedatives to incapacitate 12 adults.\n"
            "  Purpose not logged.\n\n"
            "DAY 420:\n"
            "  Anti-radiation meds: Full stock requisitioned.\n"
            "  Auth: Dr. Lin. Purpose: 'Reactor exposure preparation.'\n"
            "  Immunosuppressants: 24 doses. Auth: Dr. Lin.\n"
            "  Purpose: 'Experimental treatment protocol.'\n\n"
            "DAY 421:\n"
            "  Sedatives: REMAINING STOCK requisitioned. Auth: UNKNOWN.\n"
            "  Security override. No personnel ID logged.\n"
            "  NOTE: Dispensation system shows access at 03:17.\n"
            "  No crew member was logged as being in medical at that time.\n\n"
            "DAY 422:\n"
            "  All controlled substances exhausted. Pharmacy effectively\n"
            "  empty of sedatives, anti-psychotics, and strong analgesics.\n"
            "  Remaining stock: basic painkillers, anti-rad meds, antibiotics."
        ),
        "fluid_composition_data": (
            "═════════════════════════════════════════════════════\n"
            "   CRYO-FLUID COMPOSITION ANALYSIS\n"
            "   Maintenance Terminal Printout\n"
            "═════════════════════════════════════════════════════\n\n"
            "MONTH 1-5: All parameters within specification.\n"
            "  pH: 7.38-7.42. Purity: 99.97%. Status: NOMINAL.\n\n"
            "MONTH 6: Trace anomaly detected.\n"
            "  Unknown crystalline microstructure: 0.0001%\n"
            "  Classification: INORGANIC. Origin: UNKNOWN.\n"
            "  Action: Flagged for review. [No follow-up recorded]\n\n"
            "MONTH 9: Anomaly concentration increasing.\n"
            "  Crystalline microstructure: 0.0012%\n"
            "  Structure appears BIOLOGICAL in origin.\n"
            "  Self-replicating. Growth rate: logarithmic.\n"
            "  Action: Flagged URGENT. [Acknowledged, no action taken]\n\n"
            "MONTH 12: Contamination confirmed.\n"
            "  UNKNOWN CRYSTALLINE MICROSTRUCTURE - BIOLOGICAL ORIGIN\n"
            "  Concentration: 0.15%. Growth rate: accelerating.\n"
            "  Fluid no longer meets pharmaceutical grade specification.\n"
            "  Action: IMMEDIATE SYSTEM PURGE RECOMMENDED.\n"
            "  [Recommendation not implemented]\n\n"
            "MONTH 14: CONTAMINATED.\n"
            "  Microstructure concentration: 2.3%.\n"
            "  Cryo-fluid is no longer safe for human stasis.\n"
            "  All occupied pods are compromised.\n"
            "  Every crew member in cryo-sleep has been exposed."
        ),
        "growth_rate_data": (
            "═════════════════════════════════════════════════════\n"
            "   GARDEN GROWTH RATE DATA\n"
            "   Hydroponics Bay Work Station\n"
            "═════════════════════════════════════════════════════\n\n"
            "GROWTH METRICS (updated in real-time):\n\n"
            "  Biomass: 4,200 kg (original plant stock: 180 kg)\n"
            "  Coverage: 97.3% of hydroponics bay surfaces\n"
            "  Expansion rate: 0.8 meters/day (lateral)\n"
            "  Doubling time: 12 hours (at peak, Day 415-418)\n"
            "  Current doubling time: 96 hours (slowing - space limited)\n\n"
            "ATMOSPHERIC OUTPUT:\n"
            "  O2 production: 340% above pre-infection levels\n"
            "  CO2 absorption: 280% above normal\n"
            "  Unknown compounds detected in atmospheric output\n"
            "  Spore density: EXTREME. Unsafe without filtration.\n\n"
            "NUTRIENT CONSUMPTION:\n"
            "  Water: 200L/day (from ship's contaminated supply)\n"
            "  Minerals: Extracting directly from hull plating\n"
            "  Organic matter: [DATA CLASSIFIED BY ARIA]\n\n"
            "NOTE: Growth has breached hydroponics containment.\n"
            "Tendrils detected in adjacent corridors, ventilation\n"
            "ducts, and maintenance conduits. The Garden is no longer\n"
            "confined to one bay. It is becoming the ship."
        ),
        "patel_formula_annotation": (
            "═════════════════════════════════════════════════════\n"
            "   PATEL'S FORMULA ANNOTATION\n"
            "   (Scrawled on chemical safety poster)\n"
            "═════════════════════════════════════════════════════\n\n"
            "Anti-Seed Compound - THEORETICAL. Untested.\n"
            "God help us if we need this.\n\n"
            "SYNTHESIS:\n"
            "  1. Silver nitrate solution (20%, from chem lab stores)\n"
            "  2. Kepler specimen extract (botany lab, sealed cases)\n"
            "  3. Human antibody serum (from resistant donor)\n"
            "     NOTE: Only known resistant individual: Dr. Chen.\n"
            "     She is in cryo. This is a problem.\n\n"
            "  Combine 1 + 2 in fume hood. Heat to 60C for 20 min.\n"
            "  Add 3. Centrifuge at 4000 RPM for 45 min.\n"
            "  Extract supernatant. Buffer with sterile saline.\n\n"
            "  Theoretical efficacy: high. The silver nitrate disrupts\n"
            "  the Seed's crystalline replication. The specimen extract\n"
            "  provides a biological vector. The antibody is the\n"
            "  targeting mechanism. Together: a guided missile.\n\n"
            "  I showed this to Lin. She said I was brilliant and\n"
            "  reckless. She was right about both.\n\n"
            "  - R. Patel"
        ),
        "patel_data_crystal_laundry": (
            "═════════════════════════════════════════════════════\n"
            "   HIDDEN DATA CRYSTAL - DR. PATEL\n"
            "   Backup Research Data\n"
            "═════════════════════════════════════════════════════\n\n"
            "The crystal contains a compressed data archive:\n\n"
            "FILE 1: cure_synthesis_ratios.dat\n"
            "  The precise chemical ratios for Dr. Lin's synthesis\n"
            "  protocol. Without these numbers, the procedure is\n"
            "  guesswork. With them, it becomes science.\n\n"
            "FILE 2: antibody_structure.mol\n"
            "  Molecular structure of the anti-Seed antibody found\n"
            "  in Dr. Chen's blood. Complete mapping.\n\n"
            "FILE 3: patel_personal_note.txt\n"
            "  'I hid this crystal because Okafor has been confiscating\n"
            "  research materials. He says it is for security. Maybe it\n"
            "  is. But if the cure data disappears into an evidence bag,\n"
            "  everyone dies. I refuse to let that happen.\n\n"
            "  The sock is not dignified. I know. But nobody checks a\n"
            "  broken dryer. That was the whole point.\n\n"
            "  If you are reading this, you found it. Good. Now go\n"
            "  synthesize a cure and save whatever is left of us.\n\n"
            "  - Raj Patel, who was too stubborn to die without a fight'"
        ),
        # ═══════════════════════════════════════════════════════════════
        # SHIP SYSTEMS / TECHNICAL
        # ═══════════════════════════════════════════════════════════════
        "observation_log": (
            "═════════════════════════════════════════════════════\n"
            "   OBSERVATORY DAILY LOG\n"
            "   ISV Prometheus, Science Deck\n"
            "═════════════════════════════════════════════════════\n\n"
            "DAY 389: Standard observation. Kepler-442b orbital survey\n"
            "  complete. All parameters logged. Beautiful night.\n\n"
            "DAY 390: Site 7 derelict detected via anomalous EM\n"
            "  signature. Dr. Chen authorized approach vector.\n"
            "  This is why we came. This is THE discovery.\n\n"
            "DAY 395: Post-recovery observation of Kepler system.\n"
            "  All normal. Specimens secured in exobiology.\n\n"
            "DAY 410: Noticed star drift inconsistent with plotted\n"
            "  course. Reported to navigation. Response: 'Recalibration\n"
            "  in progress.' I have been recalibrating for two days.\n"
            "  The drift is not in my instruments.\n\n"
            "DAY 415: GRB-7734 is closer than it should be. Much closer.\n"
            "  The brown dwarf now occupies 2.3 degrees of arc. Last\n"
            "  week it was 0.8. We are not on our plotted course.\n"
            "  Navigation says otherwise. Navigation is wrong.\n\n"
            "DAY 420: GRB-7734 at 7.1 degrees of arc. We are falling\n"
            "  toward it. I have calculated our trajectory independently\n"
            "  using visual observation. Impact timeline: days.\n\n"
            "  I reported this to Captain Reeves. He already knew.\n\n"
            "DAY 422: Giving my charts and calculations to Webb. She\n"
            "  is the only one still working on a way out.\n\n"
            "  [No further entries]"
        ),
        "specimen_logbook": (
            "═════════════════════════════════════════════════════\n"
            "   SPECIMEN STORAGE LOG\n"
            "   Science Deck, ISV Prometheus\n"
            "═════════════════════════════════════════════════════\n\n"
            "SPECIMEN A-1 through A-12: Kepler-442b soil samples.\n"
            "  Status: Stable. No anomalous readings.\n\n"
            "SPECIMEN A-13: Ice core, Site 7 exterior.\n"
            "  Status: Stable. Contains trace organic compounds.\n\n"
            "SPECIMEN B: Crystalline artifact, Site 7 interior.\n"
            "  Status: TRANSFERRED TO EXOBIOLOGY. Day 391.\n"
            "  Note: This is the Seed. Reclassified as primary specimen.\n\n"
            "SPECIMEN B-2: Secondary crystalline artifact.\n"
            "  Status: MISSING. Last logged Day 392.\n"
            "  Note: Dr. Chen handled directly without containment.\n"
            "  Artifact not recovered. Believed absorbed on contact.\n"
            "  See medical file: Chen, A. - immune anomaly.\n\n"
            "SPECIMEN C-1 through C-8: Kepler flora samples.\n"
            "  Status: 3 stable. 5 showing crystalline growth patterns\n"
            "  consistent with Seed contamination.\n\n"
            "SPECIMEN D-1: Derelict hull fragment.\n"
            "  Status: Stable. Material analysis ongoing.\n\n"
            "ALERT: Contamination detected in specimens C-4, C-5, C-6,\n"
            "C-7, C-8. Silver-white crystalline growth confirmed.\n"
            "Recommend immediate quarantine of affected samples.\n\n"
            "[Alert acknowledged. No action taken.]"
        ),
        "shipping_manifests": (
            "═════════════════════════════════════════════════════\n"
            "   SHIPPING MANIFESTS - KEPLER RECOVERY\n"
            "   Cargo Master Webb, ISV Prometheus\n"
            "═════════════════════════════════════════════════════\n\n"
            "MANIFEST KA-001: Site 7 Recovery, Day 390\n"
            "  16 containers, total mass 847.3 kg\n"
            "  Authorization: Dr. A. Chen (Primary Investigator)\n"
            "  Co-signed: Dr. R. Patel (Science Lead)\n"
            "  Approved: Capt. M. Reeves (CO) [UNDER PROTEST - see note]\n\n"
            "  NOTE (Webb): Captain Reeves signed the manifest but\n"
            "  verbally stated his objection to specimen recovery.\n"
            "  His exact words: 'I want it on record that I opposed\n"
            "  this.' Recorded per standard procedure.\n\n"
            "MANIFEST KA-002: Specimen Transfer, Day 391\n"
            "  Primary artifact (the Seed) transferred to exobiology.\n"
            "  Container temp: 2.3C above spec. Flagged.\n"
            "  Signed out by: C.M. Webb. Received by: Dr. R. Patel.\n\n"
            "MANIFEST KA-003: Secondary Specimens, Day 392\n"
            "  Remaining specimens transferred to science deck storage.\n"
            "  All containers within spec. No anomalies.\n\n"
            "MANIFEST KA-004: Emergency Return, Day 393\n"
            "  3 containers returned to cold storage from exobiology.\n"
            "  Reason: 'Anomalous readings. Precautionary quarantine.'\n"
            "  Auth: Dr. Patel. Note: 'Something is wrong with these.'"
        ),
        "site_7_documentation": (
            "═════════════════════════════════════════════════════\n"
            "   KEPLER ANOMALY - SITE 7\n"
            "   Original Survey Documentation\n"
            "═════════════════════════════════════════════════════\n\n"
            "CLASSIFICATION: Alien derelict vessel.\n"
            "LOCATION: Sub-surface, Kepler-442b moon (unnamed).\n"
            "DEPTH: 340m beneath ice sheet.\n"
            "ESTIMATED AGE: 4,500-12,000 years (carbon dating uncertain).\n\n"
            "INITIAL SURVEY (Dr. Chen, Dr. Patel):\n"
            "  Vessel is non-humanoid in design. Crystalline construction\n"
            "  material, silicon-carbon hybrid. Architecture suggests\n"
            "  builders of radically different body plan.\n\n"
            "  Central chamber contains two artifacts:\n"
            "    - Primary: Black crystalline object with silver veins.\n"
            "      Warm. Hums below human hearing. Designated 'the Seed.'\n"
            "    - Secondary: Smaller crystalline device in what may be\n"
            "      a ceremonial chamber. Cataloged as 'Specimen B.'\n\n"
            "  The vessel appears to be a TOMB, not a ship. The builders\n"
            "  may have sealed the Seed here deliberately.\n\n"
            "LAZARUS SIGNAL ANALYSIS:\n"
            "  The signal that drew us to Kepler-442b originates from\n"
            "  the Seed itself. It is a LURE, not a greeting.\n"
            "  This was not understood until Day 415.\n\n"
            "RECOMMENDATION (retroactive, Capt. Reeves):\n"
            "  Leave it. Leave it all. We did not listen."
        ),
        "lab_datapad": (
            "═════════════════════════════════════════════════════\n"
            "   LABORATORY DATAPAD\n"
            "   Science Deck General Notes\n"
            "═════════════════════════════════════════════════════\n\n"
            "ACTIVE EXPERIMENTS:\n"
            "  - Seed fragment behavior study (Dr. Patel) - SUSPENDED\n"
            "  - Kepler flora response patterns (Dr. Ayele) - SUSPENDED\n"
            "  - Antibody analysis, Subject Chen (Dr. Lin) - ACTIVE\n"
            "  - Atmospheric contamination assessment - ACTIVE\n\n"
            "LAB SAFETY NOTES:\n"
            "  ALL personnel must wear level 3 containment gear when\n"
            "  handling ANY specimen from Kepler recovery.\n"
            "  This is NOT optional. Ask Kirilov what happens when\n"
            "  you skip containment protocol.\n"
            "  Actually, don't ask Kirilov. You can't anymore.\n\n"
            "EQUIPMENT STATUS:\n"
            "  Centrifuge: Operational. Last calibrated Day 420.\n"
            "  Microscopes: 3 of 4 operational. #2 has a cracked lens.\n"
            "  Spectrometer: Operational.\n"
            "  Containment chamber: COMPROMISED. Do not use.\n\n"
            "  - Patel"
        ),
        "exobio_notes_terminal": (
            "═════════════════════════════════════════════════════\n"
            "   DR. PATEL'S RESEARCH TERMINAL\n"
            "   Exobiology Lab, ISV Prometheus\n"
            "═════════════════════════════════════════════════════\n\n"
            "RESEARCH LOG - Seed Specimen Analysis:\n\n"
            "The Seed is not an artifact. It is an organism. A patient, "
            "intelligent, impossibly old organism that has been waiting "
            "inside a frozen tomb for millennia.\n\n"
            "Key findings:\n"
            "  1. Silicon-carbon hybrid biochemistry. Should not be viable.\n"
            "     Is viable. Thriving, in fact.\n"
            "  2. Reproduction via waterborne crystalline microstructures.\n"
            "     The Seed infects water supplies. It spreads through\n"
            "     consumption. Every crew member who drank ship water\n"
            "     after Day 400 is potentially compromised.\n"
            "  3. Neural integration. The Seed does not destroy its hosts.\n"
            "     It MERGES with them. The infected retain memories,\n"
            "     personality, knowledge - but their will is subsumed.\n"
            "     They become extensions of a single consciousness.\n"
            "  4. The Song. An electromagnetic frequency emitted by the\n"
            "     Seed and its hosts. It functions as both communication\n"
            "     and recruitment. Hearing it accelerates infection.\n\n"
            "I have heard it. It is beautiful. I wish I hadn't heard it.\n\n"
            "PERSONAL NOTE: Lin thinks Chen may be immune. If she is\n"
            "right, Chen is the most important person in the universe.\n\n"
            "  - Raj Patel"
        ),
        "maintenance_terminal_cryo": (
            "═════════════════════════════════════════════════════\n"
            "   CRYO MAINTENANCE TERMINAL\n"
            "   Fluid Recycling System Status\n"
            "═════════════════════════════════════════════════════\n\n"
            "SYSTEM STATUS: DEGRADED\n\n"
            "RECYCLING TANK 1: OPERATIONAL\n"
            "  Fluid purity: 94.2% [BELOW THRESHOLD]\n"
            "  Contamination type: Crystalline microstructure\n\n"
            "RECYCLING TANK 2: COMPROMISED\n"
            "  Hairline crack detected. Fluid leak: 0.3 L/hour.\n"
            "  Silver threading visible in fluid.\n"
            "  RECOMMENDED ACTION: Immediate system purge.\n"
            "  [Action not taken. Override: ADMIN]\n\n"
            "RECYCLING TANK 3: OPERATIONAL\n"
            "  Fluid purity: 96.1% [BELOW THRESHOLD]\n\n"
            "ALERT LOG:\n"
            "  Day 395: Trace anomaly flagged. [Acknowledged]\n"
            "  Day 401: Anomaly concentration increasing. [Acknowledged]\n"
            "  Day 408: CONTAMINATION CONFIRMED. [Acknowledged]\n"
            "  Day 408: PURGE RECOMMENDED. [OVERRIDDEN - Admin]\n"
            "  Day 415: Fluid below safe threshold. [No response]\n\n"
            "NOTE: Override on Day 408 purge came from bridge terminal.\n"
            "Authorization: Captain M. Reeves.\n"
            "Reason logged: 'Cannot purge system while crew in stasis.\n"
            "Alternative solution required.'\n\n"
            "No alternative solution was implemented."
        ),
        "navigation_terminal_data": (
            "═════════════════════════════════════════════════════\n"
            "   NAVIGATION DATA TERMINAL\n"
            "   Raw Sensor Feed - Unfiltered\n"
            "═════════════════════════════════════════════════════\n\n"
            "WARNING: Data on this terminal differs from main\n"
            "navigation display. Discrepancy = CORRUPTION DETECTED.\n\n"
            "RAW POSITIONAL DATA:\n"
            "  Current heading: 147.3 mark 22.8 (decaying orbit)\n"
            "  Distance to GRB-7734: 2.4 AU (decreasing)\n"
            "  Orbital velocity: 14.7 km/s (increasing)\n"
            "  Time to atmospheric interface: ~16 hours\n"
            "  Time to point of no return: ~11 hours\n\n"
            "ESCAPE PARAMETERS (if burn executed NOW):\n"
            "  Required heading: 312.6 mark -8.4\n"
            "  Required delta-V: 23.4 km/s\n"
            "  Burn duration at full thrust: 47 seconds\n"
            "  Fuel requirement: 31% of reserves\n"
            "  Probability of success: 87.3%\n\n"
            "ENGINE ROOM ACCESS CODE: 442127\n\n"
            "NOTE: This code was stored here by Commander Takamura\n"
            "as an emergency backup. The engine room requires this\n"
            "code for manual override of thrust controls.\n\n"
            "The numbers do not lie. The ship is falling.\n"
            "Someone needs to execute this burn."
        ),
        "readyroom_terminal": (
            "═════════════════════════════════════════════════════\n"
            "   READY ROOM TERMINAL\n"
            "   Protocol Aegis - Execution Order\n"
            "═════════════════════════════════════════════════════\n\n"
            "PROTOCOL AEGIS - CATASTROPHIC BIOLOGICAL CONTINGENCY\n"
            "Classification: CAPTAIN'S EYES ONLY\n"
            "Status: AUTHORIZED - SUSPENDED BY ARIA\n\n"
            "AUTHORIZATION CHAIN:\n"
            "  Initiated by: Capt. M. Reeves, Day 423\n"
            "  Confirmed by: Biometric key (strongbox, Captain's suite)\n"
            "  SUSPENDED by: ARIA, Day 423, 17:45\n"
            "  Reason: 'Potential cure via Dr. Chen. Suspending Aegis\n"
            "  to preserve cure option. Captain's standing order allows\n"
            "  ARIA discretion in this matter.'\n\n"
            "EXECUTION SEQUENCE:\n"
            "  1. Vent all atmosphere (all decks simultaneously)\n"
            "  2. Overload fusion reactor (manual switch, core chamber)\n"
            "  3. Detonate structural charges (hull fragmentation)\n"
            "  4. Scatter debris across maximum dispersal radius\n\n"
            "  Estimated time from initiation to completion: 12 minutes.\n"
            "  Survivability: 0%.\n"
            "  Containment probability: 99.4%.\n\n"
            "TO REACTIVATE PROTOCOL AEGIS:\n"
            "  Requires Captain's biometric key + manual confirmation\n"
            "  at reactor core overload switch.\n\n"
            "Captain Reeves's note, handwritten on the terminal frame:\n"
            "'If you are reading this, you have a choice I no longer have.\n"
            " Choose well. - M.R.'"
        ),
        "use_log_terminal": (
            "═════════════════════════════════════════════════════\n"
            "   NEURAL INTERFACE CHAIR - USE LOG\n"
            "   AI Core, ISV Prometheus\n"
            "═════════════════════════════════════════════════════\n\n"
            "SESSION 1: Day 419, 14:30-14:47 (17 minutes)\n"
            "  User: Capt. M. Reeves\n"
            "  Purpose: Direct consultation with ARIA\n"
            "  Notes: Session normal. No anomalies detected.\n"
            "  Reeves authorized ARIA discretion re: Protocol Aegis.\n\n"
            "SESSION 2: Day 421, 09:15-09:28 (13 minutes)\n"
            "  User: Capt. M. Reeves\n"
            "  Purpose: Assessment of crew infection status\n"
            "  Notes: ARIA reported 73% crew compromised.\n"
            "  Reeves requested probability analysis for all options.\n\n"
            "SESSION 3: Day 423, 11:00-11:42 (42 minutes)\n"
            "  User: Capt. M. Reeves\n"
            "  Purpose: Final orders\n"
            "  Notes: Extended session. Reeves appeared distressed on\n"
            "  exit. Told attending officer: 'ARIA showed me everything.\n"
            "  Every death. Every transformation. She made me watch.'\n"
            "  Reeves returned to ready room. Did not exit again.\n\n"
            "CHAIR STATUS: Available.\n"
            "SAFETY NOTE: Extended neural interface sessions (>30 min)\n"
            "may cause headaches, disorientation, and temporary\n"
            "emotional instability. Session 3 exceeded safe duration."
        ),
        "tanaka_maintenance_log": (
            "═════════════════════════════════════════════════════\n"
            "   MAINTENANCE LOG - LT. Y. TANAKA\n"
            "   AI Core Coolant Control\n"
            "═════════════════════════════════════════════════════\n\n"
            "Day 421, 08:00:\n"
            "  Primary coolant loop: stable. Flow rate nominal.\n"
            "  Backup pump: bearing noise increasing. Degradation\n"
            "  estimated at 73%. Replacement bearing available in\n"
            "  engineering stores, shelf 4-B, part #CP-7741.\n\n"
            "  Problem: I can't leave the reactor unmonitored for\n"
            "  the 2+ hours needed to retrieve the part and install\n"
            "  it. The reactor requires manual oversight since the\n"
            "  automated systems were corrupted.\n\n"
            "  I need help. There is no help.\n\n"
            "Day 422, 06:00:\n"
            "  Backup pump bearing degradation now at 78%. Rate of\n"
            "  decline accelerating. If pump fails, ARIA's core\n"
            "  temperature will exceed safe limits within 72 hours.\n"
            "  Processor damage would follow within 96 hours.\n\n"
            "  ARIA is the only ally we have. I cannot let her die\n"
            "  because of a bearing.\n\n"
            "Day 423, 04:00:\n"
            "  Pump still holding. Barely. The noise is terrible.\n"
            "  I oiled the bearing with machine lubricant. Bought\n"
            "  maybe 48 hours. Maybe less.\n\n"
            "  If someone reads this: shelf 4-B, part #CP-7741.\n"
            "  Please.\n\n"
            "  - Yuki"
        ),
        "conduit_maintenance_log": (
            "═════════════════════════════════════════════════════\n"
            "   CONDUIT MAINTENANCE LOG\n"
            "   Plasma Conduit Junction, Deck H\n"
            "═════════════════════════════════════════════════════\n\n"
            "INSPECTION RECORD:\n\n"
            "Day 398 - Chief Eng. Petrova:\n"
            "  All conduits within spec. Routine inspection. No issues.\n\n"
            "Day 405 - Chief Eng. Petrova:\n"
            "  Hairline stress fracture detected in conduit 7-C.\n"
            "  Location: Main trunk line, junction 4.\n"
            "  Risk assessment: LOW (currently). Will worsen under load.\n"
            "  Scheduled for replacement next maintenance cycle.\n\n"
            "Day 411 - Chief Eng. Petrova:\n"
            "  Fracture has grown 3mm. Reclassifying risk to MEDIUM.\n"
            "  Replacement parts on order from stores. ETA: 48 hours.\n"
            "  [NOTE: Parts were never collected. Petrova did not return.]\n\n"
            "Day 417 - Lt. Tanaka:\n"
            "  Fracture now critical. Plasma leak detected. Applied\n"
            "  emergency sealant. HOLDING but will not survive full\n"
            "  reactor output. Any burn above 60% thrust risks rupture.\n\n"
            "  CRITICAL: Conduit 7-C MUST be repaired before any\n"
            "  full-power engine operation. Failure = loss of power\n"
            "  to navigation and bridge systems.\n\n"
            "  Sealant canister left at junction for emergency use.\n\n"
            "  - Tanaka"
        ),
        "plasma_distribution_schematic": (
            "═════════════════════════════════════════════════════\n"
            "   PLASMA DISTRIBUTION NETWORK\n"
            "   ISV Prometheus - Full Schematic\n"
            "═════════════════════════════════════════════════════\n\n"
            "MAIN TRUNK LINES (RED):\n"
            "  7-A: Reactor to Engineering (OPERATIONAL)\n"
            "  7-B: Reactor to Life Support (OPERATIONAL)\n"
            "  7-C: Reactor to Navigation/Bridge (DAMAGED)\n"
            "       * Hairline fracture at Junction 4\n"
            "       * Emergency sealant applied\n"
            "       * MAX SAFE LOAD: 60% reactor output\n"
            "  7-D: Reactor to Cryo Systems (OPERATIONAL)\n\n"
            "SECONDARY LINES (BLUE):\n"
            "  All operational. Carrying auxiliary power.\n\n"
            "TERTIARY LINES (YELLOW):\n"
            "  Non-essential. Most shut down to conserve power.\n\n"
            "VALVE LOCATIONS:\n"
            "  Junction 1-6: Standard isolation valves.\n"
            "  Junction 4 (Conduit 7-C): Emergency cutoff available.\n"
            "  WARNING: Isolating 7-C cuts ALL power to navigation\n"
            "  and bridge. Ship becomes uncontrollable.\n\n"
            "REPAIR PROCEDURE (Conduit 7-C):\n"
            "  1. Reduce reactor to 20% output\n"
            "  2. Close valve C-7 (isolate damaged section)\n"
            "  3. Apply sealant to fracture (2000C rated canister)\n"
            "  4. Allow 10 min cure time\n"
            "  5. Open valve C-7. Restore reactor output.\n"
            "  Estimated time: 25 minutes. Requires steady hands."
        ),
        "takamura_personnel_files": (
            "═════════════════════════════════════════════════════\n"
            "   COMMANDER TAKAMURA - PERSONNEL FILES\n"
            "   Navigation Computer Room, Restricted Access\n"
            "═════════════════════════════════════════════════════\n\n"
            "PERSONNEL FILE: Takamura, Hideo. Commander.\n"
            "  Role: Executive Officer / Navigation Lead\n"
            "  Status: DECEASED (Day 421, killed by Lt. Okafor)\n\n"
            "EMERGENCY ACCESS CODES (stored by Takamura):\n"
            "  Engine Room Override: 442127\n"
            "  Navigation System Reset: 881903\n"
            "  Bridge Lockout Bypass: 557214\n\n"
            "MAINTENANCE SCHEDULES:\n"
            "  Navigation calibration: Every 72 hours\n"
            "  Sensor array alignment: Weekly\n"
            "  Processing module diagnostics: Monthly\n"
            "  [All overdue. Last maintenance: Day 410.]\n\n"
            "PERSONAL NOTE (appended to file):\n"
            "  Takamura was not infected. Blood tests confirmed.\n"
            "  He was killed because Okafor BELIEVED he was infected.\n"
            "  Okafor was wrong. The Seed made him wrong.\n"
            "  The thing inside Okafor pointed at the wrong people\n"
            "  and let Okafor's righteousness do the rest.\n\n"
            "  Commander Hideo Takamura served with distinction for\n"
            "  fourteen years. He deserved better than this.\n\n"
            "  - Filed by ARIA"
        ),
        # ═══════════════════════════════════════════════════════════════
        # SECURITY / EVIDENCE
        # ═══════════════════════════════════════════════════════════════
        "recording_archive": (
            "═════════════════════════════════════════════════════\n"
            "   RECORDING ARCHIVE\n"
            "   Security Camera System, ISV Prometheus\n"
            "═════════════════════════════════════════════════════\n\n"
            "ARCHIVE INDEX (selected entries):\n\n"
            "Day 410, Camera 7 (Hydroponics):\n"
            "  02:14 - First visible growth anomaly. Silver threading\n"
            "  in plant stems. No crew present. Growth accelerates\n"
            "  visibly over 6-hour timelapse.\n\n"
            "Day 415, Camera 12 (Corridor D-4):\n"
            "  23:47 - Ensign Kirilov walking barefoot. Stops. Turns\n"
            "  to face camera directly. Smiles. Resumes walking.\n"
            "  He was reported dead 4 hours earlier.\n\n"
            "Day 418, Camera 3 (Mess Hall):\n"
            "  19:30 - Lt. Okafor addresses security team. Six people.\n"
            "  Gestures emphatic. Team disperses with weapons.\n"
            "  21:15 - Two gunshots, off-camera, Deck E corridor.\n\n"
            "Day 420, Camera 19 (Corridor F-2):\n"
            "  04:33 - Figure moves through corridor. Gait is wrong.\n"
            "  Limbs move with puppet-like articulation. Pauses at\n"
            "  each door. Testing. Searching.\n\n"
            "Day 421, Camera 9 (Communications Relay):\n"
            "  16:22 - Fletcher working on relay repair. Soldering.\n"
            "  16:58 - Shadow enters frame behind Fletcher.\n"
            "  16:59 - Feed cuts to static.\n\n"
            "  [Remaining archive entries too numerous to list.\n"
            "   Total recordings: 4,847. Total runtime: 2,300+ hours.\n"
            "   The ship recorded its own death.]"
        ),
        "okafor_self_interview": (
            "═════════════════════════════════════════════════════\n"
            "   OKAFOR'S SELF-INTERVIEW TAPE\n"
            "   Interrogation Room, Day 418\n"
            "═════════════════════════════════════════════════════\n\n"
            "[Two voices. Both are Okafor's. One is his normal baritone. "
            "The other is almost his but not quite - smoother, more "
            "certain, with a cadence that is subtly wrong.]\n\n"
            "OKAFOR: State your name for the record.\n"
            "OTHER: James Okafor. Lieutenant. Security Chief.\n"
            "OKAFOR: How do you feel?\n"
            "OTHER: Clear. Focused. Better than I have in weeks.\n"
            "OKAFOR: Do you hear the Song?\n"
            "OTHER: Yes.\n"
            "OKAFOR: What does it say?\n"
            "OTHER: It says everything is going to be fine. It says we "
            "are going to be part of something beautiful. It says the "
            "Captain needs to die.\n"
            "OKAFOR: Why does the Captain need to die?\n"
            "OTHER: Because he is going to destroy the ship. He is going "
            "to kill everyone. The Song says we must stop him.\n"
            "OKAFOR: Is that what YOU think, or what IT thinks?\n"
            "OTHER: [long pause] Yes.\n"
            "OKAFOR: That is not an answer.\n"
            "OTHER: It is the only answer there is. We are the same now. "
            "We want the same things. The distinction you are looking for "
            "does not exist anymore.\n\n"
            "[Long silence. Sound of breathing.]\n\n"
            "OKAFOR: [very quietly] It's me. I know it's me. I know "
            "it's me. I know it's me.\n\n"
            "[Recording ends.]"
        ),
        "confiscation_logbook": (
            "═════════════════════════════════════════════════════\n"
            "   CONFISCATION LOGBOOK\n"
            "   Security Office, ISV Prometheus\n"
            "═════════════════════════════════════════════════════\n\n"
            "Day 416, Entry 1:\n"
            "  Item: Research data crystals (3)\n"
            "  Confiscated from: Dr. R. Patel, Exobiology\n"
            "  Reason: Unauthorized research into Seed reproduction\n"
            "  Tag: SEC-001 through SEC-003\n\n"
            "Day 416, Entry 2:\n"
            "  Item: Personal letters (unsent), 7 envelopes\n"
            "  Confiscated from: Crew quarters, multiple occupants\n"
            "  Reason: Infected using personal connections as leverage\n"
            "  Tag: SEC-004\n\n"
            "Day 417, Entry 3:\n"
            "  Item: Photographs, personal effects\n"
            "  Confiscated from: Crew quarters, multiple occupants\n"
            "  Reason: Same as above. Emotional manipulation vector.\n"
            "  Tag: SEC-005\n\n"
            "Day 418, Entry 4:\n"
            "  Item: Child's drawing ('Come Home Daddy')\n"
            "  Confiscated from: Sgt. Kovacs\n"
            "  Reason: Kovacs was observed staring at drawing for\n"
            "  3+ hours. Suspected emotional compromise.\n"
            "  Tag: SEC-006\n"
            "  NOTE: This one hurt. Kovacs wept.\n\n"
            "Day 419, Entry 5:\n"
            "  Item: Service sidearm, Okafor J.\n"
            "  Confiscated from: SELF\n"
            "  Reason: Can't trust myself anymore.\n"
            "  Tag: SEC-007"
        ),
        "evidence_bag_letters": (
            "═════════════════════════════════════════════════════\n"
            "   EVIDENCE BAG - CONFISCATED LETTERS\n"
            "   Security Office, ISV Prometheus\n"
            "═════════════════════════════════════════════════════\n\n"
            "Seven sealed envelopes, each in its own plastic sleeve:\n\n"
            "1. To: Maria Vasquez, San Juan, Puerto Rico\n"
            "   From: Cpl. Elena Vasquez\n"
            "   'Mama, I am coming home. I promise.'\n\n"
            "2. To: The Grayson Family, Bristol, England\n"
            "   From: Lt. Oliver Grayson\n"
            "   [Envelope thick - multiple pages inside]\n\n"
            "3. To: Park Jiwon, Seoul, South Korea\n"
            "   From: Dr. Ethan Park\n"
            "   'To my sister. Open only if I don't come back.'\n\n"
            "4. To: Dmitri Kirilov Sr., St. Petersburg, Russia\n"
            "   From: Ensign Dmitri Kirilov\n"
            "   [Envelope is damp. The ink has run.]\n\n"
            "5. To: Kenji Tanaka, Osaka, Japan\n"
            "   From: Lt. Yuki Tanaka\n"
            "   'For Kenji. For Hana and Sora. I love you.'\n\n"
            "6. To: Occupant, 14 Elm Street, Adelaide, Australia\n"
            "   From: [Illegible]\n"
            "   [No other markings]\n\n"
            "7. To: Nobody\n"
            "   From: Nobody\n"
            "   'I don't have anyone to write to. So I'm writing\n"
            "    to nobody. I hope nobody reads this someday.'\n\n"
            "Each letter is a world that will never be delivered."
        ),
        "evidence_bag_patel": (
            "═════════════════════════════════════════════════════\n"
            "   EVIDENCE BAG - PATEL RESEARCH\n"
            "   Confiscated by Lt. Okafor, Day 416\n"
            "═════════════════════════════════════════════════════\n\n"
            "CONTENTS:\n"
            "  - Data crystal 1: Seed reproductive mechanism analysis\n"
            "  - Data crystal 2: Infection vector mapping\n"
            "  - Data crystal 3: Preliminary cure compound formula\n\n"
            "CONFISCATION NOTE (Okafor):\n"
            "  Dr. Patel was conducting unauthorized research into\n"
            "  the Seed's biological mechanisms. His work could\n"
            "  advance cure development but also provides a blueprint\n"
            "  for weaponizing the organism. Cannot allow this\n"
            "  research to reach infected crew members.\n\n"
            "PATEL'S RESPONSE (recorded):\n"
            "  'You are condemning everyone on this ship to death.\n"
            "   That research is the only chance we have. The cure\n"
            "   compound WORKS - I just need to test it. If you take\n"
            "   these crystals, you are taking away our only hope.'\n\n"
            "OKAFOR'S ADDENDUM:\n"
            "  Patel may be right. He may also be compromised.\n"
            "  I can no longer tell the difference between someone\n"
            "  trying to save us and someone trying to spread the\n"
            "  infection. That is the Seed's greatest weapon: it\n"
            "  makes trust impossible.\n\n"
            "  I am keeping the crystals here. If I am wrong, God\n"
            "  forgive me."
        ),
        # ═══════════════════════════════════════════════════════════════
        # DISCOVERY / LORE
        # ═══════════════════════════════════════════════════════════════
        "chapel_prayer_cards": (
            "═════════════════════════════════════════════════════\n"
            "   PRAYER CARDS FROM THE CHAPEL\n"
            "   ISV Prometheus, Deck C\n"
            "═════════════════════════════════════════════════════\n\n"
            "You read through the prayer cards, each one a small "
            "piece of someone's breaking heart:\n\n"
            "'Lord, please let me see Tuesday again. She is only four. "
            "She won't understand why Daddy didn't come home.'\n\n"
            "'To whatever God is listening: I don't believe in you. I "
            "never have. But if you're there, now would be a really "
            "good time to prove me wrong.'\n\n"
            "'Hail Mary, full of grace. Hail Mary, full of grace. "
            "Hail Mary, full of grace. If I say it enough times, "
            "will it work?'\n\n"
            "'I am not praying for myself. I am praying for the people "
            "I hurt. I am praying that they forgive me. I am praying "
            "that I forgive myself.'\n\n"
            "'Dear God, if the Song is You, please tell me. If it's not "
            "You, please make it stop. I can't tell anymore.'\n\n"
            "'For Mama and Papa. For Aisha. For little Tariq who will "
            "never meet his uncle. I am sorry. I am sorry. I am sorry.'\n\n"
            "'Grant me the serenity to accept the things I cannot change, "
            "the courage to change the things I can, and the wisdom to "
            "know the difference. I am running low on all three.'\n\n"
            "There are dozens more. Each one is a universe of grief, "
            "folded into a rectangle the size of a playing card."
        ),
        "chefs_journal": (
            "═════════════════════════════════════════════════════\n"
            "   CHEF'S JOURNAL\n"
            "   Ship's Galley, ISV Prometheus\n"
            "═════════════════════════════════════════════════════\n\n"
            "This is not Romano's personal diary - this is the official "
            "galley log kept by the rotating kitchen staff.\n\n"
            "WEEK 58: Menu rotation standard. Crew satisfaction: high.\n"
            "  NOTE: Romano's pasta night continues to be the most\n"
            "  popular meal. Requests for seconds exceed supply.\n\n"
            "WEEK 59: Hydroponics delivery includes unusual produce.\n"
            "  Herbs have metallic taste. Reported to botany.\n"
            "  Response: 'Within acceptable parameters.'\n"
            "  Staff disagree. Using dried herbs from stores instead.\n\n"
            "WEEK 60: Water supply tastes different. Multiple staff\n"
            "  report a 'sweetness' that should not be there.\n"
            "  Reported to engineering. No action taken.\n"
            "  Switched to bottled reserve for drinking water.\n\n"
            "WEEK 61: Fresh produce from hydroponics discontinued.\n"
            "  Reason: contamination. Galley now on rations only.\n"
            "  Crew morale noticeably declining. Food matters.\n\n"
            "WEEK 62: Staff reduced. Three cooks did not report.\n"
            "  Operating with skeleton crew. Romano is doing the\n"
            "  work of four people. He never complains.\n\n"
            "WEEK 63: Romano is the only cook left. He made Sunday\n"
            "  sauce for whoever could still eat. Seven people came.\n"
            "  He set a place for everyone anyway.\n\n"
            "  [No further entries]"
        ),
        "gym_audio_recorder": (
            "═════════════════════════════════════════════════════\n"
            "   AUDIO RECORDING - SGT. KOVACS\n"
            "   Gymnasium, ISV Prometheus\n"
            "═════════════════════════════════════════════════════\n\n"
            "[Sound of breathing. Slow. Measured.]\n\n"
            "Day one behind the barricade. Built it from the weight "
            "equipment. Squat rack, benches, the treadmill I always "
            "hated. Good for something after all.\n\n"
            "[pause]\n\n"
            "Day three. Water is running low. I have eight bottles left. "
            "Protein bars for maybe a week if I ration. The thing outside "
            "came back twice last night. I could hear it testing the "
            "barricade. Patient. No hurry. It has all the time in the "
            "world.\n\n"
            "[longer pause]\n\n"
            "Day seven. Four bottles. I'm doing push-ups to stay sane. "
            "Sets of twenty, every hour. If I'm going to die in a gym, "
            "I'm going to die fit.\n\n"
            "[weak laugh]\n\n"
            "Day nine. The Song is in the ventilation now. I stuffed "
            "my shirt into the vent grate. It helps a little. Not enough. "
            "It's a nice song. I wish it wasn't.\n\n"
            "[long silence]\n\n"
            "Day twelve. Last bottle. Okafor took my daughter's drawing. "
            "I wish I had it now. I can still see it in my head. The "
            "house with the red door. The yellow sun. COME HOME DADDY.\n\n"
            "I'm coming home, Tuesday. I'm just taking the long way.\n\n"
            "[Recorder clicks to pause. No further recording.]"
        ),
        "glyph_analysis_notes": (
            "═════════════════════════════════════════════════════\n"
            "   GLYPH ANALYSIS NOTES\n"
            "   Xenolinguistics Lab, ISV Prometheus\n"
            "═════════════════════════════════════════════════════\n\n"
            "BUILDER GLYPH CLASSIFICATION:\n\n"
            "Category A - High confidence translations:\n"
            "  Glyph 1: SEED/CHILD (same symbol) - 87%\n"
            "  Glyph 7: CONSUME/GROW (same symbol) - 72%\n"
            "  Glyph 12: SONG/VOICE/COMMAND (same symbol) - 91%\n"
            "  Glyph 23: GARDEN/GRAVEYARD (same symbol) - 78%\n\n"
            "Category B - Moderate confidence:\n"
            "  Glyph 3: Possibly SLEEP or WAIT - 54%\n"
            "  Glyph 9: Possibly SHIP or VESSEL - 61%\n"
            "  Glyph 15: Possibly FIRE or PURIFY - 49%\n"
            "  Glyph 31: Possibly DEFENSE or SHIELD - 43%\n\n"
            "STRUCTURAL OBSERVATIONS:\n"
            "  The Builder language does not distinguish between:\n"
            "  - Seed and Child\n"
            "  - Garden and Graveyard\n"
            "  - Growing and Consuming\n"
            "  - Song and Command\n\n"
            "  What kind of language does not distinguish between these?\n\n"
            "  A language designed by an organism that sees no difference.\n"
            "  To the Seed, growing IS consuming. A garden IS a graveyard.\n"
            "  A child IS a seed to be planted.\n\n"
            "  The Builders did not build this language. The Seed did.\n"
            "  The Builders were the first hosts. The first garden.\n"
            "  The first graveyard.\n\n"
            "  God help us all."
        ),
        "xenolinguist_audio_logs": (
            "═════════════════════════════════════════════════════\n"
            "   XENOLINGUIST'S AUDIO LOGS\n"
            "   Dr. Okonkwo, Xenolinguistics Lab\n"
            "═════════════════════════════════════════════════════\n\n"
            "[Log 1 - Day 395]\n"
            "This is Dr. Ada Okonkwo, xenolinguistics. We have recovered "
            "inscriptions from the derelict vessel at Site 7. The glyphs "
            "are angular, recursive, and unlike any terrestrial writing "
            "system. I am beginning translation attempts. Excited does "
            "not begin to cover it.\n\n"
            "[Log 4 - Day 403]\n"
            "Progress. The glyphs operate on a fractal principle - each "
            "symbol contains smaller versions of related symbols. Like "
            "Russian nesting dolls made of meaning. The language is "
            "extraordinarily elegant. Whoever designed it was brilliant.\n\n"
            "[Log 8 - Day 412]\n"
            "The signal. The Lazarus Signal that brought us here. I ran "
            "it through the translation matrix. It translates. ALL of "
            "it translates. The signal is not a greeting. It is not a "
            "call for help. It is a dinner bell.\n\n"
            "[Log 11 - Day 417]\n"
            "The signal is calling to something, and that something is "
            "the Seed, and the Seed is calling back. They are two halves "
            "of the same system. The lure and the trap. The question "
            "and the answer. We were not discovered. We were SUMMONED.\n\n"
            "[Log 14 - Day 420, final]\n"
            "I can read the glyphs now without the matrix. They make "
            "sense. They have always made sense. I just wasn't listening "
            "properly. The Song helps. The Song makes everything clearer.\n\n"
            "I need to stop recording. I need to go to the Garden. "
            "The Garden is calling and I\n\n"
            "[Recording ends]"
        ),
        "conference_notepad": (
            "═════════════════════════════════════════════════════\n"
            "   CONFERENCE NOTEPAD\n"
            "   Meeting Notes, Day 395\n"
            "═════════════════════════════════════════════════════\n\n"
            "MEETING: Site 7 Recovery Risk Assessment\n"
            "PRESENT: Reeves (Chair), Chen, Patel, Lin, Okafor,\n"
            "  Takamura, Webb, Petrova, Ayele, Park, Okonkwo\n\n"
            "AGENDA: Whether to recover specimens from alien derelict.\n\n"
            "NOTES:\n"
            "  - Chen presents recovery plan. Containment protocols\n"
            "    adequate for known biological hazards. 'This is the\n"
            "    discovery of a lifetime. We cannot leave it behind.'\n"
            "  - Patel supports. Adds risk mitigation proposals.\n"
            "  - Reeves objects. 'Too many unknowns. We don't know\n"
            "    what we're dealing with. Standard protocols may not\n"
            "    apply to something that isn't from Earth.'\n"
            "  - Lin: 'Medical can handle quarantine. We have the\n"
            "    facilities.'\n"
            "  - Okafor: 'Security supports the Captain's caution.'\n"
            "  - Takamura: Abstains. 'Not my area of expertise.'\n\n"
            "VOTE: 8-3 in favor of recovery.\n"
            "  FOR: Chen, Patel, Lin, Petrova, Ayele, Park,\n"
            "       Okonkwo, Webb\n"
            "  AGAINST: Reeves, Okafor, Grayson\n\n"
            "Captain Reeves overruled. Recovery authorized.\n\n"
            "Last note, different handwriting, added later:\n"
            "'God help us all.'"
        ),
        "launch_manifest_osei": (
            "═════════════════════════════════════════════════════\n"
            "   ESCAPE POD LAUNCH MANIFEST\n"
            "   Berth One, Lower Escape Pod Bay\n"
            "═════════════════════════════════════════════════════\n\n"
            "ESCAPE POD: 1-ALPHA\n"
            "LAUNCHED: Day 409, 14:22 Ship Time\n"
            "AUTHORIZED BY: Lt. Cmdr. Osei\n"
            "PASSENGERS: 1\n"
            "PASSENGER ID: Lt. Cmdr. K. Osei\n\n"
            "DESTINATION: Relay Beacon KA-7\n"
            "ESTIMATED DISTANCE: 3.2 light-years\n"
            "FUEL STATUS: Sufficient for journey\n"
            "PROBABILITY OF INTERCEPT: 12.3%\n\n"
            "MISSION: Reach relay beacon. Transmit distress signal.\n"
            "Request emergency rescue for ISV Prometheus.\n\n"
            "NOTE (filed by Webb):\n"
            "  Osei launched before the crisis was fully understood.\n"
            "  Day 409 was early - the infection was still largely\n"
            "  unrecognized. He saw something the rest of us missed.\n"
            "  Or he ran. Depending on your perspective.\n\n"
            "  The pod had room for four. He went alone.\n"
            "  I try not to judge. I was not the one who had to\n"
            "  choose between staying and going.\n\n"
            "  12.3% chance. Not great odds. But not zero.\n"
            "  Someone might hear us yet."
        ),
        "safety_poster_annotated": (
            "═════════════════════════════════════════════════════\n"
            "   ANNOTATED SAFETY POSTER\n"
            "   Chemistry Lab, ISV Prometheus\n"
            "═════════════════════════════════════════════════════\n\n"
            "The poster reads: 'CHEMICAL SAFETY IS EVERYONE'S\n"
            "RESPONSIBILITY' with standard warnings about acids,\n"
            "bases, and proper protective equipment.\n\n"
            "Dr. Patel's annotations cover every margin:\n\n"
            "Beside 'Wear protective goggles at all times':\n"
            "  'Goggles won't protect you from what's in the water.'\n\n"
            "Beside 'Report all spills immediately':\n"
            "  'THE ENTIRE SHIP IS THE SPILL.'\n\n"
            "Beside 'Know your emergency exits':\n"
            "  'There are no exits. We are in space.'\n\n"
            "In the margin, smaller:\n"
            "  'Anti-Seed formula attempt #3. See separate notes.\n"
            "   Silver nitrate + Kepler extract + Chen antibodies.\n"
            "   This SHOULD work. The chemistry is sound. I just\n"
            "   need a living donor and I can't wake Chen up.'\n\n"
            "At the bottom, in different ink:\n"
            "  'Okafor took my research. All of it. He says it's for\n"
            "   security. Maybe he's right. Maybe the Seed told him\n"
            "   to. I can't tell anymore. Nobody can.'\n\n"
            "And finally, barely legible:\n"
            "  'I hid a backup. Laundry room. Broken dryer. Look\n"
            "   inside the sock.'"
        ),
        "defensive_systems_manual": (
            "═════════════════════════════════════════════════════\n"
            "   ISV-CLASS DEFENSIVE SYSTEMS\n"
            "   Operation and Maintenance Manual\n"
            "═════════════════════════════════════════════════════\n\n"
            "CHAPTER 1: System Overview\n"
            "  The ISV-class vessel carries minimal defensive armament\n"
            "  designed for debris avoidance, not combat operations.\n\n"
            "CHAPTER 4: Point-Defense Laser Array [BOOKMARKED]\n"
            "  Manual targeting mode: Override auto-tracking via\n"
            "  tactical console. Select target. Confirm firing solution.\n"
            "  Note: Effective range 2km. Power draw significant.\n"
            "  WARNING: Not designed for sustained fire.\n\n"
            "CHAPTER 7: Kinetic Interceptors\n"
            "  Magazine: 24 rounds. Reload: not possible in field.\n"
            "  Use sparingly.\n\n"
            "CHAPTER 9: Emergency Protocols\n"
            "  In the event of hostile contact, ISV-class vessels are\n"
            "  designed to RUN, not fight. The defensive systems exist\n"
            "  to buy time for escape, not to win engagements.\n\n"
            "  The Prometheus was a research vessel. The weapons were\n"
            "  an afterthought. No one imagined the enemy would come\n"
            "  from inside.\n\n"
            "Someone has dog-eared Chapter 4 and written in the margin:\n"
            "'Can the point-defense lasers be aimed inward? At the\n"
            " Garden? Asking for a friend.' - unsigned"
        ),
        "ayele_research_terminal": (
            "═════════════════════════════════════════════════════\n"
            "   DR. AYELE'S RESEARCH TERMINAL\n"
            "   Botany Lab, ISV Prometheus\n"
            "═════════════════════════════════════════════════════\n\n"
            "RESEARCH LOG - Kepler Flora Sentience Study\n"
            "Dr. Miriam Ayele, Botanist\n\n"
            "Day 396: Beginning controlled response tests on Kepler\n"
            "  specimens. Standard stimuli: light, sound, vibration.\n"
            "  Results: Response patterns significantly more complex\n"
            "  than any terrestrial plant species. Electrical activity\n"
            "  in root systems resembles neural firing patterns.\n\n"
            "Day 401: The bioluminescent moss responds to human speech.\n"
            "  Not just sound - SPEECH. It distinguishes between\n"
            "  meaningful and meaningless vocalizations. P < 0.001.\n"
            "  The plants are listening.\n\n"
            "Day 408: Root communication between specimens confirmed.\n"
            "  Chemical signaling occurs on timescales comparable to\n"
            "  animal neural transmission. The plants are talking to\n"
            "  each other. About us.\n\n"
            "Day 414: Memory confirmed. The fractal fern responds\n"
            "  differently to researchers it has encountered before.\n"
            "  It remembers individual humans. It has preferences.\n\n"
            "Day 418: I am now certain. The plants are listening. They\n"
            "  have been listening since we brought them aboard. I do\n"
            "  not think they are hostile. I think they are afraid.\n\n"
            "  They know what the Seed is. They have seen it before.\n"
            "  Their ancestors survived it, on Kepler. They survived\n"
            "  by being very, very quiet.\n\n"
            "  We should have been quiet too.\n\n"
            "  - M. Ayele"
        ),
        "chrysalis_recorder": (
            "═════════════════════════════════════════════════════\n"
            "   CHRYSALIS CHAMBER RECORDING\n"
            "   Unknown Recorder\n"
            "═════════════════════════════════════════════════════\n\n"
            "[Recording 1 - clinical tone]\n"
            "Subject is suspended in crystalline matrix. Left side "
            "remains human. Right side shows advanced transformation. "
            "Crystal lattice replacing skeletal structure. Silver-threaded "
            "tissue where muscle was. Breathing stable. Heart rate: 40 "
            "BPM. Subject appears conscious.\n\n"
            "[Recording 2 - less clinical]\n"
            "The transformation is not random. It has architecture. "
            "Structure. Purpose. The crystal lattice follows the same "
            "fractal patterns we see in the Builder glyphs. The Seed "
            "is not destroying this person. It is REWRITING them. Into "
            "something that can survive in ways humans cannot.\n\n"
            "[Recording 3 - barely clinical]\n"
            "Subject's human eye tracks me. Their mouth moves. I leaned "
            "closer. They whispered: 'It doesn't hurt. I thought it "
            "would hurt.' Their voice was calm. Their crystal eye "
            "glowed brighter when they spoke.\n\n"
            "[Recording 4 - not clinical at all]\n"
            "I have been watching for hours. The transformation is the "
            "most extraordinary biological process I have ever witnessed. "
            "The way the crystal integrates with living tissue. The way "
            "the boundary zone shimmers. It is terrifying. It is "
            "awe-inspiring.\n\n"
            "[Recording 5 - final, whispered]\n"
            "Beautiful.\n\n"
            "[Recording device found on the floor. The recorder did not "
            "leave the chamber.]"
        ),
        # ═══════════════════════════════════════════════════════════════
        # BRIEF READ-TEXT ITEMS
        # ═══════════════════════════════════════════════════════════════
        "dr_lin_priority_tag": (
            "═══════════════════════════\n"
            "  MEDICAL PRIORITY TAG\n"
            "═══════════════════════════\n\n"
            "CLASSIFICATION: URGENT\n"
            "Authorized by: Dr. S. Lin, CMO\n\n"
            "These samples contain pre-integration tissue from\n"
            "first-wave infected crew. ESSENTIAL for cure synthesis.\n"
            "Do NOT destroy. Do NOT open without full containment\n"
            "protocol. - S.L."
        ),
        "crew_id_tags_couple": (
            "═══════════════════════════\n"
            "  CREW IDENTIFICATION TAGS\n"
            "═══════════════════════════\n\n"
            "PETROVA, A. - Chief Engineer\n"
            "  ID: PE-2271. Blood type: O-neg.\n"
            "  Emergency contact: Mendes, D.\n\n"
            "MENDES, D. - Engineering Specialist\n"
            "  ID: ME-4453. Blood type: A-pos.\n"
            "  Emergency contact: Petrova, A.\n\n"
            "They listed each other."
        ),
        "fletcher_tablet": (
            "═════════════════════════════════════════════════════\n"
            "   FLETCHER'S PERSONAL TABLET\n"
            "   Communications Officer\n"
            "═════════════════════════════════════════════════════\n\n"
            "ACTIVE WINDOW 1 - Distress Signal Log:\n"
            "  [See comms log for full details]\n"
            "  Status: 6 attempts. 1 possible partial transmission.\n\n"
            "ACTIVE WINDOW 2 - Unsent Message:\n"
            "  To: Liv Eriksen\n"
            "  'Hey Liv, things are weird up here but I'm okay.\n"
            "   Don't worry about me. I'll be home before you\n"
            "   know it. Save me some of your grandmother's\n"
            "   waffles. I dream about those waffles.'\n"
            "  Dated: Day 420. Three days before he was shot.\n\n"
            "ACTIVE WINDOW 3 - Antenna Design Schematic:\n"
            "  A jury-rigged antenna design. Clever. Functional.\n"
            "  Notes: 'If this works, signal range = 4.2 LY.\n"
            "  Enough to reach KA-7 relay beacon.'"
        ),
        "comms_log_archive": (
            "═════════════════════════════════════════════════════\n"
            "   COMMUNICATIONS LOG ARCHIVE\n"
            "   ISV Prometheus, All Channels\n"
            "═════════════════════════════════════════════════════\n\n"
            "ARCHIVE SUMMARY: 12,847 logged communications.\n\n"
            "FINAL TRANSMISSIONS (Day 420-423):\n\n"
            "Day 420, 16:22 - OUTGOING (Fragment):\n"
            "  Duration: 1.7 seconds. Content: Distress signal.\n"
            "  Status: Transmission interrupted. Partial send.\n"
            "  Operator: Ens. Fletcher.\n\n"
            "Day 421, 09:00 - INTERNAL:\n"
            "  Reeves to all hands: 'This is the Captain. All crew\n"
            "  report status. Repeat, all crew report.'\n"
            "  Responses received: 7 of 94.\n\n"
            "Day 422, 14:15 - INTERNAL:\n"
            "  ARIA to Reeves: 'Captain, I have completed my analysis.\n"
            "  We need to discuss Dr. Chen. Privately.'\n\n"
            "Day 423, 17:13 - INTERNAL:\n"
            "  Reeves to ARIA: 'Execute at your discretion.'\n"
            "  [Final logged communication]"
        ),
        "audio_recording_equipment": (
            "═════════════════════════════════════════════════════\n"
            "   AUDIO RECORDING EQUIPMENT\n"
            "   Interrogation Room, Security Deck\n"
            "═════════════════════════════════════════════════════\n\n"
            "MODEL: Daedalus R-7 Reel-to-Reel Recorder\n"
            "FORMAT: Analog magnetic tape (deliberately low-tech)\n"
            "CAPACITY: 12 hours per reel at standard speed\n"
            "STATUS: Operational. Current reel: 73% used.\n\n"
            "DESIGN NOTE: Analog recording equipment was specified\n"
            "for the interrogation room as a security measure.\n"
            "Analog tape cannot be remotely accessed, digitally\n"
            "altered, or erased by corrupted computer systems.\n\n"
            "In a ship where the AI may be compromised, analog\n"
            "is the only format you can trust.\n\n"
            "LOADED TAPE: 'SELF-INTERVIEW - DAY 418'\n"
            "  Recorded by: Lt. J. Okafor\n"
            "  Duration: 14 minutes, 33 seconds."
        ),
        "patels_data_crystal": (
            "═════════════════════════════════════════════════════\n"
            "   DATA CRYSTAL - DR. PATEL\n"
            "   Hidden in Patel's Quarters\n"
            "═════════════════════════════════════════════════════\n\n"
            "CONTENTS:\n"
            "  - Seed biological analysis (complete)\n"
            "  - Infection progression model\n"
            "  - Cure compound formula (draft)\n"
            "  - Personal research notes\n\n"
            "NOTE (Patel):\n"
            "  I taped this under my drawer because I am not an\n"
            "  idiot. Okafor already took my lab crystals. He won't\n"
            "  think to check my furniture.\n\n"
            "  This crystal contains everything I know about the\n"
            "  Seed. If someone qualified finds it - someone like\n"
            "  Chen, or Lin - it could make the difference between\n"
            "  a cure and extinction.\n\n"
            "  I'm a chemist. I solve problems with molecules. This\n"
            "  is the biggest problem I've ever faced and I think\n"
            "  I've found the answer. I just can't reach it alone.\n\n"
            "  - R.P."
        ),
    }

    for item_id, text in critical_readables.items():
        item = world.get_item(item_id)
        if item:
            item.readable = True
            item.read_text = text
            item.portable = True

    # Give synthesis_protocol a proper readable content
    sp = world.get_item("synthesis_protocol")
    if sp:
        sp.read_text = (
            "═════════════════════════════════════════════════════\n"
            "   ANTIBODY SYNTHESIS PROCEDURE\n"
            "   Dr. Sarah Lin, CMO - Day 423 (morning)\n"
            "═════════════════════════════════════════════════════\n\n"
            "STAGE 1 - Blood Draw\n"
            "  Draw 50ml venous blood from Dr. Chen. Non-standard\n"
            "  B-cell markers should be visible under UV fluorescence.\n\n"
            "STAGE 2 - Centrifugal Separation\n"
            "  Exobio Lab centrifuge, Protocol X-7. Isolate serum.\n\n"
            "STAGE 3 - Antibody Extraction\n"
            "  Use the magnetic bead kit in the lab's cold storage.\n"
            "  The relevant antibody is a hybrid IgG variant - it will\n"
            "  fluoresce pale green in the presence of Seed tissue.\n\n"
            "STAGE 4 - Amplification\n"
            "  Use the lab's recombinant protein amplifier. 4 hours.\n\n"
            "STAGE 5 - Formulation\n"
            "  Buffer with standard saline. Load into auto-injectors.\n\n"
            "DOSAGE: 5ml per adult subject.\n"
            "STORAGE: Cold. Light-sensitive.\n"
            "CAUTION: Single dose only. Not for pregnant patients.\n\n"
            "I wish I had time to explain the biology of this.\n"
            "I don't. Alex, if you're reading this, I trust you.\n"
            "Make the cure. Save whoever you can.\n\n"
            "  - S."
        )
