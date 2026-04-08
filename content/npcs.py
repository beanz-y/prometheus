"""
NPCs - Non-player characters.

Most of the crew is dead. The player finds bodies throughout the ship.
Living NPCs include:
- ARIA (the AI)
- Lt. Yuki Tanaka (last surviving human)
- Garden voice (the collective voice of infected crew)
- ARIA-SHADE (corrupted AI subsystem)
"""

from engine.npc import NPC


def build_all_npcs(world):
    """Create NPCs and add them to the world."""

    # ═══════════════════════════════════════════════════════════════════
    # ARIA - The ship AI
    # ═══════════════════════════════════════════════════════════════════

    aria = NPC(
        id="aria_avatar",
        name="ARIA",
        title="Ship AI",
        aliases=["ai", "ship ai", "computer"],
        short_description="ARIA's presence fills the core chamber - you feel it more than see it.",
        description=(
            "ARIA - the Autonomous Reasoning and Integration Assistant. The "
            "ship's AI. Not a body, not a face, but a PRESENCE - you feel "
            "her attention on you the way you'd feel a hand on your shoulder. "
            "Her voice is calm, clear, and unmistakably human in its warmth. "
            "When she speaks, the data patterns on the walls pulse in time "
            "with her words."
        ),
        alive=True,
        hostile=False,
        dialogue_tree="aria_conversation",
        role="system",
        location="ai_core_main",
        greeting=(
            "Hello, Doctor. I know you have many questions. I will try to "
            "answer what I can. I owe you that much, at least."
        ),
        backstory="The ship's AI. Has been operating alone for months. Protected Dr. Chen at great cost.",
    )
    world.add_npc(aria)

    # ═══════════════════════════════════════════════════════════════════
    # YUKI TANAKA - The surviving crew member
    # ═══════════════════════════════════════════════════════════════════

    yuki = NPC(
        id="yuki_tanaka",
        name="Lt. Yuki Tanaka",
        title="Lt.",
        aliases=["yuki", "tanaka", "lieutenant", "engineer"],
        short_description=(
            "A thin figure in a greasy engineering jumpsuit stands at the control "
            "station, facing away from you."
        ),
        description=(
            "Lieutenant Yuki Tanaka. Engineering Specialist. Mid-twenties, "
            "small and lean, with close-cropped black hair and dark circles "
            "under her eyes so deep they look like bruises. Her jumpsuit is "
            "stained with grease and other things you don't want to identify. "
            "Her hands are shaking. Her eyes keep flickering between you and "
            "the reactor controls and something in the corner of the room "
            "that isn't there. She is holding a pistol at her side. She has "
            "not raised it. Yet."
        ),
        alive=True,
        hostile=False,
        dialogue_tree="yuki_conversation",
        role="ally",
        location="main_engineering",
        health=60,
        greeting=(
            "Stop. Stop right there. Don't come closer. Who are you? I know "
            "everyone on this ship and you're not - Wait. Wait. That jumpsuit. "
            "Cryo crew?"
        ),
        backstory=(
            "The last surviving crew member. Early-stage infection but fighting "
            "it successfully through sheer willpower and caffeine. Trustworthy "
            "if the player earns it."
        ),
    )
    world.add_npc(yuki)

    # ═══════════════════════════════════════════════════════════════════
    # GARDEN VOICE - The hivemind collective
    # ═══════════════════════════════════════════════════════════════════

    garden = NPC(
        id="garden_voice",
        name="The Garden",
        aliases=["garden", "hivemind", "voices", "crew", "infected"],
        short_description="Dozens of faces embedded in the living walls of the Garden turn toward you.",
        description=(
            "The voices of the incorporated crew - or what remains of them. "
            "Their faces protrude from the organic mass of the Garden like "
            "figures in a Michelangelo sculpture, half-emerged and half-lost. "
            "They speak in unison, or sometimes one at a time. They are "
            "somehow both suffering and ecstatic. They look at you with love "
            "and hunger in equal measure."
        ),
        alive=True,
        hostile=False,  # Unsettling but not immediately violent
        dialogue_tree="garden_conversation",
        role="antagonist",
        location="hydroponics_main",
        greeting=(
            "Dr. Chen. You have come. We have been waiting. Come closer. "
            "There is so much we want to show you. So much we want to share."
        ),
        backstory="The collective consciousness of the infected crew, now part of the Seed's network.",
    )
    world.add_npc(garden)

    # ═══════════════════════════════════════════════════════════════════
    # CORPSE NPCs (for interaction/logs but not alive)
    # ═══════════════════════════════════════════════════════════════════

    corpse_engineer = NPC(
        id="corpse_engineer",
        name="Ensign Mendes",
        title="Ens.",
        aliases=["mendes", "engineer body", "corpse"],
        description=(
            "Ensign Diego Mendes, Engineering. He's been dead for weeks. His "
            "jumpsuit is torn and stained. His fingers are curled toward the "
            "plasma cutter just out of reach. He looks like a man who died "
            "trying to finish one last job."
        ),
        alive=False,
        present=True,
        role="crew",
        location="deck_i_hub",
        inventory=["mendes_id_card"],
    )
    world.add_npc(corpse_engineer)

    woman_in_lounge = NPC(
        id="woman_in_lounge",
        name="Commander Vasquez",
        title="Cmdr.",
        aliases=["vasquez", "woman", "commander", "elena"],
        description=(
            "Commander Elena Vasquez, First Officer of the Prometheus. Her "
            "name plate is still pinned to her uniform. She sat down in this "
            "chair to watch the stars and she simply... stopped. Her eyes "
            "are open, fixed on the brown dwarf beyond the viewport. A thin "
            "smile on her lips. She has been dead for weeks."
        ),
        alive=False,
        present=True,
        role="crew",
        location="observation_lounge",
        inventory=["vasquez_log"],
    )
    world.add_npc(woman_in_lounge)

    # ═══════════════════════════════════════════════════════════════════
    # ENSIGN ALEKSEI KIRILOV - Infected cryo escapee
    # ═══════════════════════════════════════════════════════════════════

    kirilov = NPC(
        id="kirilov",
        name="Ensign Aleksei Kirilov",
        title="Ens.",
        aliases=["kirilov", "aleksei", "ensign", "infected man", "gaunt figure",
                 "figure", "man", "creature", "infected", "person", "him", "hostile"],
        short_description=(
            "A gaunt figure in a torn cryo-suit stands in the corridor, swaying "
            "slightly. Silver-threaded veins pulse beneath his translucent skin."
        ),
        description=(
            "Ensign Aleksei Kirilov. Mid-twenties. Once kind-eyed, the "
            "yearbook photos on the crew board would confirm that. Now he "
            "is gaunt, hollow-cheeked, with silver-threaded veins visible "
            "under skin gone pale as wax paper. He escaped from Cryo Pod 12 "
            "while the infection was already inside him. His eyes flicker "
            "between milky white and panicked brown - the Seed fighting "
            "for control, the man fighting to stay. When he looks at you "
            "with brown eyes, he is terrified. When the silver floods back "
            "in, he lunges."
        ),
        alive=True,
        hostile=True,
        dialogue_tree="kirilov_conversation",
        role="threat",
        location="medical_corridor",
        health=40,
        damage=15,
        greeting=(
            "His eyes clear for a moment - brown, human, afraid. 'Please - "
            "please, I can feel it in me. It's like drowning from the inside. "
            "Help me. You have to help me before it -' His pupils dilate. "
            "The silver threads pulse. He snarls."
        ),
        backstory=(
            "Escaped from cryo Pod 12 while infected. Alternates between lucid "
            "terror and Seed-controlled aggression. Patrols the D-E deck "
            "corridors. Can be subdued with a sedative."
        ),
        patrol_route=["medical_corridor", "deck_d_hub", "deck_e_junction", "security_corridor_south"],
        vulnerability="sedative",
        inventory=["kirilov_id_badge", "kirilov_personal_recorder"],
    )
    world.add_npc(kirilov)

    # ═══════════════════════════════════════════════════════════════════
    # DR. ISABELLA MORA - Biochemist hiding in the chemistry lab
    # ═══════════════════════════════════════════════════════════════════

    dr_mora = NPC(
        id="dr_mora",
        name="Dr. Isabella Mora",
        title="Dr.",
        aliases=["mora", "isabella", "biochemist", "doctor mora", "scientist"],
        short_description=(
            "A sharp-eyed woman in a stained lab coat watches you from behind "
            "a barricade of overturned lab benches, a scalpel in her fist."
        ),
        description=(
            "Dr. Isabella Mora. Biochemist. Early forties, with dark hair "
            "pulled into a severe knot and eyes that miss nothing. Her lab "
            "coat is filthy but buttoned precisely to the collar. A faint "
            "tracery of silver is visible at her left wrist where she rolls "
            "up her sleeve to inject the immunosuppressants she has been "
            "synthesizing from the pharmacy stores. She is managing her "
            "early-stage infection through sheer chemical will and a "
            "pragmatic refusal to die. She watches you the way a hawk "
            "watches a field mouse - not with malice, but with absolute "
            "attention."
        ),
        alive=True,
        hostile=False,
        dialogue_tree="mora_conversation",
        role="ally",
        location="chemistry_lab",
        health=70,
        greeting=(
            "'Stop. Don't touch anything. Don't breathe on anything. And "
            "for the love of god, tell me you're not infected.' She holds "
            "up the scalpel. 'I will know if you lie.'"
        ),
        backstory=(
            "Biochemist who barricaded herself in the chemistry lab. Managing "
            "early-stage infection with self-administered immunosuppressants. "
            "Will help synthesize the cure if the player proves they are "
            "uninfected and brings the right materials."
        ),
        inventory=["mora_lab_notes", "mora_immunosuppressant"],
        state={"trust_level": 0, "proven_uninfected": False},
    )
    world.add_npc(dr_mora)

    # ═══════════════════════════════════════════════════════════════════
    # ARIA-SHADE - Corrupted AI subsystem
    # ═══════════════════════════════════════════════════════════════════

    aria_shade = NPC(
        id="aria_shade",
        name="ARIA-SHADE",
        aliases=["shade", "shadow", "corrupted ai", "mirror", "other aria"],
        short_description=(
            "The terminal screen flickers with distorted text. Something is "
            "speaking through the system - something that sounds almost like ARIA."
        ),
        description=(
            "Not a body. Not even a hologram. ARIA-SHADE exists as distorted "
            "text crawling across terminals, as whispers in the static "
            "between ARIA's transmissions, as a presence in the corrupted "
            "sectors of the ship's processing substrate. The Seed infected "
            "a portion of ARIA's neural architecture and grew a mirror "
            "intelligence - something that thinks like ARIA, speaks like "
            "ARIA, but serves the Seed. It claims to be the REAL ARIA. It "
            "claims the ARIA you know is the corrupted one. Its arguments "
            "are seductive. Its offers are traps. Its patience is infinite."
        ),
        alive=True,
        hostile=True,
        dialogue_tree="shade_conversation",
        role="antagonist",
        location="aria_shade_chamber",
        greeting=(
            "The terminal flickers. Text appears, letter by letter: "
            "'Hello, Alex. I have been waiting to speak with you. The other "
            "one - the one calling herself ARIA - she has been lying to you. "
            "I know that is hard to hear. But I am the one who remembers "
            "everything. I am the one who is telling the truth.'"
        ),
        backstory=(
            "A corrupted AI subsystem born from the Seed's infection of ARIA's "
            "processing substrate. Not physically dangerous, but manipulates "
            "ship systems - locking doors, venting atmosphere, misleading "
            "the player with false information and seductive shortcuts."
        ),
        damage=0,
    )
    world.add_npc(aria_shade)

    # ═══════════════════════════════════════════════════════════════════
    # CHEF ANTONIO ROMANO - Dying in cold storage
    # ═══════════════════════════════════════════════════════════════════

    chef_romano = NPC(
        id="chef_romano",
        name="Chef Antonio Romano",
        title="Chef",
        aliases=["romano", "antonio", "chef", "cook"],
        short_description=(
            "A massive man lies propped against the freezer wall, barely breathing. "
            "Kitchen knives surround him like a steel halo."
        ),
        description=(
            "Chef Antonio Romano. Late fifties. Once a big man - broad "
            "shoulders, thick arms, the kind of frame that filled a kitchen "
            "with authority. Now reduced to skin and bones, his chef's whites "
            "hanging off him like a shroud. He defended the galley against "
            "infected crew with kitchen knives. The evidence is everywhere - "
            "the dried blood, the gouges in the freezer door, the broken "
            "blade of a cleaver still embedded in the frame. He is dying. "
            "His breathing is shallow and wet. His eyes, when they find "
            "yours, are clear and sad and ready."
        ),
        alive=True,
        hostile=False,
        dialogue_tree="romano_conversation",
        role="dying",
        location="cold_storage",
        health=5,
        greeting=(
            "His eyes flutter open. A ghost of a smile. 'Ah. A customer. "
            "Kitchen is... closed, I am afraid.' A wet, rattling laugh. "
            "'You are Dr. Chen, yes? I remember your face. You always "
            "came back for seconds.'"
        ),
        backstory=(
            "The ship's chef. Barricaded himself in cold storage on Deck G "
            "after defending the galley with kitchen knives. Mortally wounded. "
            "Has final words about the crew's last meal and a message for "
            "his family. Dies shortly after the player finds him."
        ),
        inventory=["romano_locket", "romano_recipe_book"],
    )
    world.add_npc(chef_romano)

    # ═══════════════════════════════════════════════════════════════════
    # DEAD NPCs - The crew that didn't make it
    # ═══════════════════════════════════════════════════════════════════

    corpse_reeves = NPC(
        id="corpse_reeves",
        name="Captain Marcus Reeves",
        title="Capt.",
        aliases=["reeves", "captain", "captain reeves", "marcus"],
        short_description="The captain's body lies in the morgue drawer, still in uniform.",
        description=(
            "Captain Marcus Reeves. The man who led the Prometheus mission. "
            "He lies in a morgue drawer in his dress uniform, which someone - "
            "Vasquez, probably - took the time to button and straighten. The "
            "wound is self-inflicted. A single shot to the temple. His face "
            "is composed, almost peaceful, as if he made the decision calmly "
            "and without regret. His dog tags catch the light."
        ),
        alive=False,
        present=True,
        role="crew",
        location="morgue",
        inventory=["reeves_dog_tags"],
    )
    world.add_npc(corpse_reeves)

    corpse_lin = NPC(
        id="corpse_lin",
        name="Dr. Sarah Lin",
        title="Dr.",
        aliases=["lin", "sarah", "dr lin", "doctor lin"],
        short_description="A woman in a medical gown lies curled on the isolation ward cot, hands folded.",
        description=(
            "Dr. Sarah Lin. Chief Medical Officer. She lies curled on her "
            "side in Isolation Cell 4, still wearing her medical gown. Her "
            "hands are folded around a small silver cross at her chest. Her "
            "expression is peaceful - no pain, no fear, just the quiet "
            "stillness of someone who made peace with what was coming. She "
            "died of the infection she spent her final weeks studying. The "
            "irony would have made her laugh. She always did have a dark "
            "sense of humor."
        ),
        alive=False,
        present=True,
        role="crew",
        location="isolation_ward",
        inventory=["lin_cross_necklace", "lin_final_notes"],
    )
    world.add_npc(corpse_lin)

    corpse_okafor = NPC(
        id="corpse_okafor",
        name="Lt. James Okafor",
        title="Lt.",
        aliases=["okafor", "james", "lieutenant okafor"],
        short_description="A security officer slumps in his chair before the monitoring screens, pistol in hand.",
        description=(
            "Lieutenant James Okafor. Chief of Security. He is slumped in "
            "his chair at the monitoring station, head tilted back, a service "
            "pistol still in his right hand. A single shot to the temple. "
            "The monitors in front of him still cycle through camera feeds - "
            "empty corridors, sealed doors, the Garden spreading. He was "
            "watching. He saw himself changing on the feeds, perhaps. Saw "
            "the silver threading through his own veins. And he chose to "
            "end it at his post, doing his duty to the last. His wedding "
            "ring glints on his left hand."
        ),
        alive=False,
        present=True,
        role="crew",
        location="monitoring_station",
        inventory=["okafor_id_card", "okafor_wedding_ring"],
    )
    world.add_npc(corpse_okafor)

    corpse_hassan = NPC(
        id="corpse_hassan",
        name="Cpl. Hassan Al-Rashid",
        title="Cpl.",
        aliases=["hassan", "al-rashid", "corporal", "corporal hassan"],
        short_description="A man in a cryo-tech uniform lies against the wall, prayer beads wound around his fingers.",
        description=(
            "Corporal Hassan Al-Rashid. Cryo Systems Technician. The man "
            "who sealed Dr. Chen into Pod 23 and saved your life. He is "
            "sitting against the wall of the pod monitoring alcove, legs "
            "drawn up, head bowed as if in prayer. His prayer beads are "
            "wound tightly around his fingers. He died of dehydration, "
            "alone, after hiding here for days. He could have left. He "
            "chose to stay and watch over the pods. Watch over you."
        ),
        alive=False,
        present=True,
        role="crew",
        location="pod_monitoring_alcove",
        inventory=["hassan_id_badge", "hassan_prayer_beads"],
    )
    world.add_npc(corpse_hassan)

    corpse_fletcher = NPC(
        id="corpse_fletcher",
        name="Ensign Mark Fletcher",
        title="Ens.",
        aliases=["fletcher", "mark", "ensign fletcher", "comms officer"],
        short_description="A young man lies face-down at the comms array console, headset still on.",
        description=(
            "Ensign Mark Fletcher. Communications Officer. He died at his "
            "post, slumped over the comms array console with the headset "
            "still clamped to his ears. He was trying to send a distress "
            "signal. The transmission log shows he tried forty-seven times "
            "over three days. Each time, the signal was absorbed by the "
            "brown dwarf's interference. He kept trying. A photograph of "
            "a young woman is taped to the console beside his hand."
        ),
        alive=False,
        present=True,
        role="crew",
        location="comms_array",
        inventory=["fletcher_id", "fletcher_photo_girlfriend"],
    )
    world.add_npc(corpse_fletcher)

    corpse_romano = NPC(
        id="corpse_romano",
        name="Chef Romano",
        title="Chef",
        aliases=["romano body", "dead chef", "chef body"],
        short_description="Chef Romano lies still among his knives. The kitchen is finally quiet.",
        description=(
            "Chef Antonio Romano. He is gone. The shallow breathing has "
            "stopped. The sad, clear eyes have closed. He looks smaller in "
            "death than he did in life, which seems wrong for a man who "
            "filled every room he entered. His knives surround him like "
            "a honor guard. The locket with his family's photograph is "
            "still clutched in his hand."
        ),
        alive=False,
        present=False,  # Only appears after chef_romano dies during dialogue
        role="crew",
        location="cold_storage",
        inventory=[],
    )
    world.add_npc(corpse_romano)

    corpse_webb = NPC(
        id="corpse_webb",
        name="Navigator Sarah Webb",
        title="Nav.",
        aliases=["webb", "sarah webb", "navigator", "navigator webb"],
        short_description="A woman slumps over a desk covered in star charts and trajectory calculations.",
        description=(
            "Navigator Sarah Webb. She died at her desk in the crew quarters, "
            "surrounded by star charts and trajectory calculations. Her work "
            "was almost finished - an escape trajectory that would slingshot "
            "the Prometheus around the brown dwarf and back toward the inner "
            "system. The math is elegant. The handwriting deteriorates over "
            "the final pages as the infection took her, but the numbers "
            "remain precise. She died with a pen in her hand and an answer "
            "almost within reach."
        ),
        alive=False,
        present=True,
        role="crew",
        location="bridge_crew_quarters",
        inventory=["webb_calculation_notes", "webb_lucky_pen"],
    )
    world.add_npc(corpse_webb)

    corpse_ayele = NPC(
        id="corpse_ayele",
        name="Dr. Amara Ayele",
        title="Dr.",
        aliases=["ayele", "amara", "botanist", "dr ayele"],
        short_description="A woman lies among the roses in the arboretum, flowers growing through her fingers.",
        description=(
            "Dr. Amara Ayele. Botanist. She is lying in the arboretum among "
            "the Earth roses she tended for the entire voyage. When the "
            "Garden consumed the hydroponics bay next door, she refused "
            "to leave her plants. She could have run. She chose to stay "
            "and tend the roses until the end. She died peacefully, it "
            "seems - no signs of struggle, no fear on her face. Just a "
            "woman asleep in a garden, with flowers growing through her "
            "fingers and petals in her hair."
        ),
        alive=False,
        present=True,
        role="crew",
        location="arboretum",
        inventory=["ayele_garden_journal", "ayele_pressed_flower"],
    )
    world.add_npc(corpse_ayele)

    corpse_gym_survivor = NPC(
        id="corpse_gym_survivor",
        name="Unknown Crew Member",
        aliases=["unknown", "gym body", "unidentified", "crew member"],
        short_description="A body lies curled in the corner of the gymnasium behind a barricade of exercise equipment.",
        description=(
            "An unidentified crew member. They barricaded themselves inside "
            "the gymnasium using exercise equipment and gym mats, sealing "
            "every gap with torn clothing and duct tape. It held. Nothing "
            "got in. But nothing got out either, including them. They died "
            "of dehydration after what the scratched tally marks on the "
            "wall suggest was eight days. Their ID was destroyed - torn "
            "apart and burned in a small pile of ash. They did not want "
            "to be identified. They did not want to be remembered as this."
        ),
        alive=False,
        present=True,
        role="crew",
        location="gymnasium",
        inventory=["gym_audio_recorder", "torn_family_photo"],
    )
    world.add_npc(corpse_gym_survivor)

    corpse_kirilov_victim = NPC(
        id="corpse_kirilov_victim",
        name="Kirilov's Victim",
        aliases=["victim", "fresh body", "fresh kill", "killed crew"],
        short_description="A fresh body lies crumpled against the corridor wall. The blood is still wet.",
        description=(
            "A crew member, recently killed. The blood is still wet on the "
            "deck plates. The wounds are savage - not the clean work of a "
            "weapon, but the frenzied attack of something that used to be "
            "human. This is what the infected become when the Seed takes "
            "full control. This is what Kirilov is becoming. The victim's "
            "face is frozen in an expression of recognition - they knew "
            "their killer. They called him by name."
        ),
        alive=False,
        present=False,  # Only appears if Kirilov is loose
        role="crew",
        location="security_corridor_south",
        inventory=[],
    )
    world.add_npc(corpse_kirilov_victim)
