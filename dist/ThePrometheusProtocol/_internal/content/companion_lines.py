"""
Companion commentary lines - contextual dialogue from Yuki Tanaka.

Yuki is a young engineer: practical, sharp, with dark humor as a
coping mechanism.  She knows the ship's systems intimately and is
fighting the early stages of Seed infection ("the Song").
"""


def build_companion_commentary(companion):
    """Populate the companion's commentary dict keyed by room_id.

    The companion system's spam-prevention (no comment within 3 turns)
    is handled by Companion.get_commentary(); we only need to supply
    the mapping here.
    """

    lines = {}

    # ═══════════════════════════════════════════════════════════════
    # DECK I - Cryogenics
    # ═══════════════════════════════════════════════════════════════

    lines['cryo_bay'] = (
        "Sixty pods. Fifty-eight dead. One escaped. And you. "
        "The universe has a sick sense of humor."
    )
    lines['cryo_storage'] = (
        "*says nothing, just touches a pod's glass gently*"
    )
    lines['cryo_control'] = (
        "Hassan was on duty here. He was... he was a good man. "
        "He used to bring me tea when I pulled double shifts."
    )
    lines['cryo_medical'] = (
        "The emergency thaw protocols are all wrong. Someone "
        "changed them. Someone didn't want the crew waking up."
    )
    lines['cryo_maintenance'] = (
        "These conduits are mine. I welded half of them myself "
        "when the originals cracked at Jupiter."
    )
    lines['cryo_corridor'] = (
        "It's too quiet. On a working ship there's always a hum. "
        "Without it the silence is... heavy."
    )

    # ═══════════════════════════════════════════════════════════════
    # DECK D - Medical
    # ═══════════════════════════════════════════════════════════════

    lines['medical_bay'] = (
        "Dr. Lin tried so hard. She ran this place like a fortress. "
        "Even fortresses fall."
    )
    lines['surgery'] = (
        "Patel. God, Patel. *She turns away.* He was funny. "
        "Did you know that? He told terrible puns."
    )
    lines['quarantine_airlock'] = (
        "Don't open that. Whatever you do, DON'T open that. "
        "We sealed it for a reason."
    )
    lines['quarantine_bay'] = (
        "I helped build the containment seals on this room. "
        "They were rated for biohazard level five. The Seed "
        "went through them like tissue paper."
    )
    lines['morgue'] = (
        "I can't. I'm sorry. I'll wait outside. "
        "*She won't enter the morgue.*"
    )
    lines['dr_lin_office'] = (
        "She kept that photo of her kids on the desk. "
        "They're on Mars. They don't know yet."
    )

    # ═══════════════════════════════════════════════════════════════
    # DECK E - Security
    # ═══════════════════════════════════════════════════════════════

    lines['security_office'] = (
        "Okafor wasn't wrong about the infection. "
        "He was wrong about who was infected."
    )
    lines['armory'] = (
        "Take what you need. We're past asking permission "
        "from dead men."
    )
    lines['brig'] = (
        "*reads the bloody message* Whoever wrote that was still "
        "in there. Still fighting. I hope it was enough."
    )
    lines['monitoring_station'] = (
        "Half these cameras are dead. The other half show things "
        "I wish I hadn't seen."
    )

    # ═══════════════════════════════════════════════════════════════
    # DECK F - Engineering
    # ═══════════════════════════════════════════════════════════════

    lines['main_engineering'] = (
        "This is MY deck. I know every bolt, every weld, every "
        "sound this reactor makes. And right now it sounds wrong."
    )
    lines['coolant_pump_room'] = (
        "Pump Two. I've been trying to fix it for weeks. "
        "Maybe together we can actually get it running."
    )
    lines['reactor_core_interior'] = (
        "Don't touch ANYTHING unless I say so. Seriously. "
        "One wrong valve and we're a cloud of ions."
    )
    lines['yuki_hideout'] = (
        "This is... my place. My space. Please don't judge the mess. "
        "It kept me alive when everything else was trying to kill me."
    )
    lines['reactor_antechamber'] = (
        "The radiation readings are higher than they should be. "
        "The shielding is degrading. We don't have long."
    )
    lines['engineering_workshop'] = (
        "I used to spend hours in here building things. "
        "Feels like a hundred years ago."
    )

    # ═══════════════════════════════════════════════════════════════
    # DECK G - Cargo / Garden
    # ═══════════════════════════════════════════════════════════════

    lines['hydroponics_entry'] = (
        "The Song is louder here. Can you hear it? "
        "No? Good. Don't try."
    )
    lines['hydroponics_main'] = (
        "Oh god. Oh god, that's... those are PEOPLE in the walls. "
        "I think I can see Nakamura's face."
    )
    lines['heart_of_garden'] = (
        "We shouldn't be here. We REALLY shouldn't be here. "
        "Everything in my gut says run."
    )
    lines['cold_storage'] = (
        "Romano. He fed us all. Even when rations were short "
        "he'd find a way to make something that tasted like hope."
    )
    lines['chrysalis_chamber'] = (
        "*Yuki grabs your arm* Don't look. Don't-- that could be "
        "ME. That could be what I become."
    )
    lines['cargo_bay_main'] = (
        "We stored the original samples down here. Triple-sealed. "
        "I wonder which container failed first."
    )
    lines['water_processing'] = (
        "The water recycler is how it spread. I figured that out "
        "too late. Everyone had already been drinking it for days."
    )
    lines['garden_periphery_east'] = (
        "The walls are breathing. Tell me you can see the walls "
        "breathing. Tell me I'm not imagining it."
    )

    # ═══════════════════════════════════════════════════════════════
    # DECK H - AI Core
    # ═══════════════════════════════════════════════════════════════

    lines['ai_core_main'] = (
        "She's beautiful, isn't she? ARIA. I never thought I'd "
        "call a computer beautiful. But she IS."
    )
    lines['aria_shade_chamber'] = (
        "Something's wrong here. The data patterns are... wrong. "
        "Like a mirror that doesn't reflect right."
    )
    lines['ai_core_antechamber'] = (
        "ARIA was the only one who kept talking to me. "
        "When everyone else was dead or singing, she was there."
    )
    lines['neural_interface_chamber'] = (
        "They used this to talk directly to ARIA. Mind to mind. "
        "It terrified me then. Now it just seems... inevitable."
    )

    # ═══════════════════════════════════════════════════════════════
    # DECK B - Science
    # ═══════════════════════════════════════════════════════════════

    lines['exobio_lab'] = (
        "So this is where it all started. This room. This... thing. "
        "One sample. That's all it took."
    )
    lines['observatory'] = (
        "Look at it. GRB-7734. It doesn't care about us. "
        "It doesn't even know we exist."
    )
    lines['main_lab'] = (
        "Your notes are still on the whiteboard. Your handwriting "
        "is terrible, by the way."
    )
    lines['specimen_storage'] = (
        "Please tell me we're not here to collect MORE alien samples. "
        "Because I will physically stop you."
    )

    # ═══════════════════════════════════════════════════════════════
    # DECK A - Command
    # ═══════════════════════════════════════════════════════════════

    lines['bridge'] = (
        "Captain's chair. Empty. It shouldn't be empty. "
        "He'd hate seeing it like this."
    )
    lines['captains_quarters'] = (
        "*quiet for a long time* He was a good captain. "
        "The best I've served under."
    )
    lines['comms_array'] = (
        "If we can get a signal out... Earth needs to know. "
        "Even if we don't make it, they need to KNOW."
    )
    lines['ready_room'] = (
        "The last briefing was about water rationing. "
        "We had no idea. None of us had any idea."
    )

    # ═══════════════════════════════════════════════════════════════
    # DECK C - Living Quarters
    # ═══════════════════════════════════════════════════════════════

    lines['mess_hall'] = (
        "Paella night. Day 423. I can still taste it. "
        "Romano outdid himself that night."
    )
    lines['observation_lounge'] = (
        "Vasquez. She's... she came here to watch the stars. "
        "I think she was already gone by then."
    )
    lines['cabin_chen'] = (
        "Your room. Does any of it feel familiar? "
        "...No? I'm sorry. I really am."
    )
    lines['arboretum'] = (
        "This is nice. This is... actually nice. "
        "Can we stay here a minute?"
    )
    lines['chapel'] = (
        "I'm not religious. But I've been praying a lot lately. "
        "Hedging my bets, I suppose."
    )
    lines['galley'] = (
        "Romano's knives are all still in the rack. "
        "He'd kill anyone who touched them. Well. He would have."
    )

    # ═══════════════════════════════════════════════════════════════
    # Special / Contextual Lines (keyed by pseudo-room or event)
    # ═══════════════════════════════════════════════════════════════

    # These are keyed with prefixed IDs so game code can look them
    # up contextually (e.g. after combat, when infection is high).

    lines['_event_dead_crew'] = (
        "Another one. I'm running out of tears."
    )
    lines['_event_after_combat'] = (
        "Are you okay? You're bleeding. Let me-- hold still."
    )
    lines['_event_infection_high'] = (
        "You're looking pale. The veins on your neck are... "
        "are you sure you're okay?"
    )
    lines['_event_sanity_low'] = (
        "Hey. Hey, look at me. Focus. What's my name? "
        "Say my name. Good. Stay with me."
    )
    lines['_event_after_log'] = (
        "...Did you know that about them? I didn't. "
        "I wish I had."
    )
    lines['_event_near_garden'] = (
        "*humming softly, then stopping abruptly* "
        "Sorry. I don't know why I... the Song. It's nothing."
    )
    lines['_event_dark_room'] = (
        "I can't see anything. Stay close. Please."
    )
    lines['_event_new_deck'] = (
        "New deck. Stay sharp. We don't know what's down here."
    )

    # ═══════════════════════════════════════════════════════════════
    # Additional rooms for coverage
    # ═══════════════════════════════════════════════════════════════

    lines['recreation_lounge'] = (
        "Movie night was Thursdays. We watched terrible old horror "
        "films. Nobody's laughing now."
    )
    lines['gymnasium'] = (
        "Fletcher worked out here every morning at 0500. "
        "Said discipline kept the darkness out."
    )
    lines['cabin_okafor'] = (
        "Okafor's room. He was so certain he was right. "
        "The worst part is, he almost was."
    )
    lines['cabin_hassan'] = (
        "Hassan kept a journal. Handwritten. Who does that "
        "anymore? I guess it didn't save him."
    )
    lines['cabin_fletcher'] = (
        "Fletcher. Security through and through. Even her "
        "quarters look like a barracks."
    )
    lines['cabin_romano'] = (
        "He kept recipes from every crew member's home country. "
        "Said food was the only real universal language."
    )
    lines['cabin_lin'] = (
        "Dr. Lin's room. Neat as a pin. Just like her. "
        "She deserved better than this."
    )
    lines['cabin_patel'] = (
        "Patel's room. There's a half-finished crossword on the desk. "
        "He'll never finish it."
    )

    # Apply all lines to the companion
    companion.commentary.update(lines)
