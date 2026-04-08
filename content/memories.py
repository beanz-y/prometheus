"""
Memory fragments - recoverable pieces of Dr. Chen's past.
Triggered by examining specific items, visiting specific rooms, or reaching knowledge thresholds.
"""

from engine.event import Event


def _add_memory(memory_id, summary):
    """Create a callback that adds a memory fragment to the player."""
    def callback(game):
        if game.player.add_memory(memory_id, summary):
            count = game.player.get_memory_count()
            game.display.print(
                f"\n  [Memory recovered: {count}/30]",
                color="\033[95m",
            )
    return callback


def _add_memory_with_threshold(memory_id, summary, min_memories):
    """Create a callback that checks memory count before adding."""
    def callback(game):
        if game.player.get_memory_count() < min_memories:
            return
        if game.player.add_memory(memory_id, summary):
            count = game.player.get_memory_count()
            game.display.print(
                f"\n  [Memory recovered: {count}/30]",
                color="\033[95m",
            )
    return callback


def build_memory_events(event_manager, world):
    """Create all memory recovery events."""

    # ═══════════════════════════════════════════════════════════════════
    # PRE-MISSION MEMORIES (1-8)
    # ═══════════════════════════════════════════════════════════════════

    # 1. Father's beach
    event_manager.add_event(Event(
        id="memory_fathers_beach",
        triggers=["examine:photo_of_beach"],
        narrative=(
            "The photograph trembles in your hand. And then the world shifts.\n\n"
            "You are twelve years old, standing on a beach in Monterey. The "
            "sand is cold between your toes. Your father is beside you, one "
            "hand on your shoulder, the other pointing at the sky. 'That one "
            "is Cassiopeia, Alex. The queen on her throne. And there - Orion. "
            "The hunter.' The salt wind pulls at your hair. His laugh is warm "
            "and deep and safe. The stars are so bright they seem close enough "
            "to touch.\n\n"
            "Years later, on this same beach, he told you about the Prometheus "
            "mission posting. His eyes were proud and terrified in equal "
            "measure. 'You should apply,' he said. 'You were born for this.' "
            "The waves crashed behind you both, indifferent to the future."
        ),
        callback=_add_memory(
            "memory_fathers_beach",
            "Your father on the beach, teaching you the stars.",
        ),
        knowledge_added=["memory_father"],
    ))

    # 2. Mother's goodbye
    event_manager.add_event(Event(
        id="memory_mothers_goodbye",
        triggers=["examine:watch_chen"],
        narrative=(
            "The watch is warm in your palm. Too warm. And then you are "
            "somewhere else.\n\n"
            "The launch facility. Three hours before departure. Your mother "
            "standing at the observation rail, her face composed in that way "
            "she had when she was trying desperately not to cry. The fluorescent "
            "lights made everyone look pale but they made her look porcelain, "
            "fragile, breakable. She pressed this watch into your hand. Her "
            "father's watch. 'Come home to me, Alex,' she said. Her voice "
            "did not crack. 'Promise me you will come home.' You promised. "
            "You held her and you promised and you meant it with every cell "
            "in your body.\n\n"
            "You are so far from home."
        ),
        callback=_add_memory(
            "memory_mothers_goodbye",
            "Your mother at the launch facility. 'Come home to me, Alex.'",
        ),
        knowledge_added=["memory_mother"],
    ))

    # 3. Noah's cooking
    event_manager.add_event(Event(
        id="memory_noahs_cooking",
        triggers=["examine:romano_recipe_book", "enter:galley"],
        narrative=(
            "The smell of the kitchen - even cold, even dead - triggers "
            "something.\n\n"
            "Noah. Your brother. His restaurant in Portland, the one with "
            "the blue door and the herb garden out back. Him standing at the "
            "stove in his ridiculous apron, the one his daughters made him "
            "with glitter and fabric paint. 'Okay, Alex, the secret to "
            "risotto is patience. Stir. Don't stop stirring. No, not like "
            "that, you're attacking it.' His laugh when you nearly took off "
            "your thumb with the chef's knife. The nieces - Maya and Sofia - "
            "running between your legs, shrieking, while he pretended to be "
            "angry. The warmth of that kitchen. The completeness of being "
            "surrounded by family.\n\n"
            "You would give anything to be standing in that kitchen right now."
        ),
        callback=_add_memory(
            "memory_noahs_cooking",
            "Your brother Noah in his restaurant, teaching you risotto.",
        ),
        knowledge_added=["memory_brother_noah"],
    ))

    # 4. Ethan breakup
    event_manager.add_event(Event(
        id="memory_ethan_breakup",
        triggers=["examine:photo_of_stranger"],
        narrative=(
            "The face in the photograph. You know this face. You KNOW it.\n\n"
            "Ethan. Dr. Ethan Park. Neurobiologist. Brown eyes that crinkled "
            "when he laughed, which was often. Hands that could hold a pipette "
            "and your heart with equal precision. You loved him. You loved "
            "him the way you loved breathing - automatically, essentially, "
            "without thinking about it until it was gone.\n\n"
            "The night you told him about the Prometheus. His apartment, the "
            "one with the crooked bookshelves and the cat that hated everyone "
            "but you. 'You're leaving,' he said. Not a question. 'I want the "
            "stars, Ethan.' 'I know. I know you do.' His face. God, his face. "
            "He didn't ask you to stay. That was the worst part. He already "
            "knew you wouldn't.\n\n"
            "You chose the stars. Were they worth it?"
        ),
        callback=_add_memory(
            "memory_ethan_breakup",
            "Ethan Park. You loved him. You chose the stars instead.",
        ),
        knowledge_added=["memory_ethan"],
    ))

    # 5. PhD defense
    event_manager.add_event(Event(
        id="memory_phd_defense",
        triggers=["examine:xenobiology_texts"],
        narrative=(
            "The textbooks on the shelf. Your own name in the citations. And "
            "the memory unfolds like a flower.\n\n"
            "Your PhD defense. The long table with the five committee members. "
            "Dr. Vasquez-Torres, your advisor, giving nothing away behind her "
            "reading glasses. The projector humming. Your extremophile research "
            "displayed on the screen - the organisms that thrived in volcanic "
            "vents, in Antarctic ice, in conditions that should have been "
            "impossible. You spoke for ninety minutes without notes. Your "
            "voice did not shake.\n\n"
            "The moment they returned from deliberation. 'Congratulations, "
            "Doctor Chen.' The word DOCTOR hitting you like a wave. The "
            "champagne after, cheap and warm and perfect. You called your "
            "mother. She cried. Your father said, 'I always knew.'\n\n"
            "Doctor Chen. You earned that title. It means something. Even here."
        ),
        callback=_add_memory(
            "memory_phd_defense",
            "Your PhD defense. The day you became Doctor Chen.",
        ),
        knowledge_added=["memory_academic_career"],
    ))

    # 6. Mission assignment
    event_manager.add_event(Event(
        id="memory_mission_assignment",
        triggers=["read:player_letter_to_self"],
        narrative=(
            "Your own handwriting on the page, and the memory crashes over "
            "you.\n\n"
            "The call from EDSC - Earth Deep Space Commission. A Tuesday "
            "afternoon. You were grading papers. The phone rang and a calm "
            "voice said, 'Dr. Chen, we would like you to lead the xenobiology "
            "team aboard the ISV Prometheus.' Your heart stopped. Literally "
            "stopped, for one beat, and then resumed at twice the speed.\n\n"
            "You said yes before they finished the sentence. You said yes "
            "the way a drowning person says yes to air. Everything you had "
            "worked for, every late night in the lab, every grant proposal, "
            "every failed experiment that taught you something new - it all "
            "led to this moment. To this ship. To this mission.\n\n"
            "To this."
        ),
        callback=_add_memory(
            "memory_mission_assignment",
            "The call from EDSC. 'We'd like you to lead the xenobiology team.'",
        ),
        knowledge_added=["memory_edsc_call"],
    ))

    # 7. Crew meeting
    event_manager.add_event(Event(
        id="memory_crew_meeting",
        triggers=["enter:conference_room"],
        narrative=(
            "This room. This exact table. The memory lands like a physical "
            "blow.\n\n"
            "The first full crew meeting. Eighteen months before departure. "
            "Captain Reeves at the head of the table, firm handshake, steel-gray "
            "eyes that sized you up in three seconds and decided you were "
            "acceptable. Dr. Raj Patel, too-eager grin, already talking about "
            "the Lazarus Signal before anyone sat down. Sarah Lin, steady eyes, "
            "quiet competence radiating from her like heat. Yuki Tanaka, barely "
            "out of the academy, vibrating with nervous energy. Fletcher at "
            "the comms station, Webb with her star charts already spread across "
            "the table.\n\n"
            "You looked around at their faces and thought: I trust these "
            "people. I would follow these people anywhere. I would follow "
            "them to the stars.\n\n"
            "You did."
        ),
        callback=_add_memory(
            "memory_crew_meeting",
            "The first crew meeting. Reeves, Patel, Lin. You trusted them.",
        ),
        knowledge_added=["memory_crew_faces"],
    ))

    # 8. Launch day
    event_manager.add_event(Event(
        id="memory_launch_day",
        triggers=["examine:captains_photo"],
        narrative=(
            "The photograph shows the crew on the launch pad. And suddenly "
            "you are there.\n\n"
            "Launch day. The Prometheus on the pad, gleaming white against "
            "the blue Florida sky, impossibly large, impossibly real. The "
            "crew lined up for the photograph you are now holding. Everyone "
            "smiling. Reeves with his arms crossed, the only one not grinning. "
            "Patel making rabbit ears behind Lin. You, in the center, "
            "squinting into the sun, looking like someone who had just won "
            "the lottery and couldn't quite believe it.\n\n"
            "The launch. The g-forces pressing you into the couch. The "
            "rumble becoming a roar becoming silence. And then the viewport "
            "cleared and Earth was below you, blue and white and getting "
            "smaller. You cried. You told everyone it was the acceleration. "
            "Patel saw through it. He always did. He squeezed your hand and "
            "said nothing."
        ),
        callback=_add_memory(
            "memory_launch_day",
            "Launch day. The Prometheus on the pad. Earth getting smaller.",
        ),
        knowledge_added=["memory_launch"],
    ))

    # ═══════════════════════════════════════════════════════════════════
    # MISSION MEMORIES (9-18)
    # ═══════════════════════════════════════════════════════════════════

    # 9. Lazarus reception
    event_manager.add_event(Event(
        id="memory_lazarus_reception",
        triggers=["enter:comms_array"],
        narrative=(
            "The comms array hums with dead static. But you remember when "
            "it sang.\n\n"
            "The moment the Lazarus Signal came through clearly. Not the "
            "faint, ambiguous pulse they had been chasing for months, but "
            "the REAL signal - structured, repeating, unmistakably artificial. "
            "Fletcher ripped off his headset and screamed. The whole bridge "
            "erupted. Reeves opened the good champagne, the bottle he had "
            "been saving for first contact. You danced with Patel - badly, "
            "joyfully, bumping into consoles. Even Okafor smiled. Even ARIA "
            "played music.\n\n"
            "That was the happiest moment of the voyage. That was the moment "
            "everything was still possible and nothing had gone wrong yet."
        ),
        callback=_add_memory(
            "memory_lazarus_reception",
            "The Lazarus Signal coming through. The whole crew cheering.",
        ),
        knowledge_added=["memory_lazarus_moment"],
    ))

    # 10. Kepler first sight
    event_manager.add_event(Event(
        id="memory_kepler_first_sight",
        triggers=["enter:observatory"],
        narrative=(
            "The observatory viewport. Dark now. But once, it showed you "
            "something miraculous.\n\n"
            "Kepler-442b. The target world. It filled the viewport like a "
            "dream made solid - blue oceans, white cloud bands, the green "
            "suggestion of continents. An Earth that was not Earth. A world "
            "that had been calling to you across four hundred light-years.\n\n"
            "You pressed your palm against the glass. The surface was cold. "
            "The planet was warm. You whispered 'Hello' to it, the way you "
            "might greet an old friend you had been traveling a very long "
            "time to see. And somewhere in the back of your mind - a feeling. "
            "Not words. A feeling of being recognized. Of being expected.\n\n"
            "You told yourself it was awe. You told yourself it was emotion. "
            "You were probably wrong."
        ),
        callback=_add_memory(
            "memory_kepler_first_sight",
            "Kepler-442b filling the viewport. Blue and white and impossible.",
        ),
        knowledge_added=["memory_kepler"],
    ))

    # 11. Site 7 descent
    event_manager.add_event(Event(
        id="memory_site7_descent",
        triggers=["examine:site_7_documentation"],
        narrative=(
            "The documentation triggers a cascade of images.\n\n"
            "The shuttle descending to the frozen moon. Site 7, they called "
            "it - the seventh anomaly, the one that turned out to be real. "
            "Ice as far as you could see, blue-white and ancient. And then, "
            "emerging from the glacier like a bone from snow, the derelict "
            "ship. Alien. Impossible. Waiting.\n\n"
            "Your hands were shaking in the EVA gloves. Not from cold. From "
            "the overwhelming, crushing weight of the moment. First contact. "
            "Not with a living species - with their remains. With proof that "
            "humanity was not alone. With proof that someone else had been "
            "here first, had traveled between stars, had died here in the "
            "ice. You wanted to cry and laugh and pray, all at once."
        ),
        callback=_add_memory(
            "memory_site7_descent",
            "The shuttle descending to Site 7. The derelict ship in the ice.",
        ),
        knowledge_added=["memory_site7"],
    ))

    # 12. Derelict interior
    event_manager.add_event(Event(
        id="memory_derelict_interior",
        triggers=["read:archive_terminal"],
        narrative=(
            "The terminal data stirs something deep.\n\n"
            "Inside the alien ship. The air was thin but breathable - the "
            "ship's systems still functioning after millennia, holding a "
            "pocket of atmosphere like a held breath. The walls breathed "
            "with bioluminescent light, soft blues and purples that pulsed "
            "in slow rhythms. Crystalline architecture that made your eyes "
            "water to look at directly, as if the geometry itself was too "
            "complex for human perception.\n\n"
            "Beauty that hurt. That is what you remember most. A beauty so "
            "alien, so far beyond human aesthetic, that it registered as "
            "pain. The corridors curved in ways that should not have been "
            "possible. The walls hummed with a frequency you felt in your "
            "teeth. And in the center of it all, in a chamber that glowed "
            "like a heart - the Seed. Waiting for you. Waiting for anyone."
        ),
        callback=_add_memory(
            "memory_derelict_interior",
            "Inside the alien ship. Crystalline beauty that hurt to look at.",
        ),
        knowledge_added=["memory_derelict"],
    ))

    # 13. Seed first touch
    event_manager.add_event(Event(
        id="memory_seed_first_touch",
        triggers=["enter:exobio_lab"],
        required_flags=["core_memory_recovered"],
        narrative=(
            "Standing here, in the lab, and the memory comes unbidden.\n\n"
            "The first time you touched the containment vessel holding the "
            "Seed. Everyone else had left for the night. You were alone with "
            "it. The lab was quiet except for the hum of the containment "
            "field. You placed your palm on the glass.\n\n"
            "It was warm. Warmer than it should have been. And it hummed - "
            "not the mechanical hum of the equipment, but something organic, "
            "something alive. You said 'hello' the way you always did to "
            "new specimens, half habit, half superstition. And it answered. "
            "Not in words. In feeling. A wash of warmth, of recognition, of "
            "something that felt terrifyingly like welcome.\n\n"
            "You should have been afraid. You were fascinated."
        ),
        callback=_add_memory(
            "memory_seed_first_touch",
            "The first time you touched the Seed's vessel. It answered.",
        ),
        knowledge_added=["memory_seed_contact"],
    ))

    # 14. Argument with Reeves
    event_manager.add_event(Event(
        id="memory_argument_with_reeves",
        triggers=["read:captains_recorder"],
        narrative=(
            "The captain's voice on the recorder, and you remember the "
            "argument.\n\n"
            "'Alex, we can not bring this back.' Reeves, standing in this "
            "very room, arms crossed, jaw set. The immovable object. 'Marcus, "
            "we MUST.' You, the irresistible force. The argument lasted three "
            "hours. You cited protocol. He cited instinct. You cited the "
            "scientific value. He cited the precautionary principle. You cited "
            "your credentials, your expertise, your years of study. He cited "
            "his gut.\n\n"
            "You won. Because you were right. Because you were louder. Because "
            "you were more passionate. Because the crew supported you. Because "
            "ARIA's risk assessment supported you.\n\n"
            "Or because the Seed wanted you to win. That thought keeps you "
            "up at night. If you could still sleep."
        ),
        callback=_add_memory(
            "memory_argument_with_reeves",
            "The argument with Reeves about bringing the Seed aboard.",
        ),
        knowledge_added=["memory_reeves_argument"],
    ))

    # 15. Patel excitement
    event_manager.add_event(Event(
        id="memory_patel_excitement",
        triggers=["examine:patel_recording_crystal"],
        narrative=(
            "Raj's recording crystal. His voice would be on here. And the "
            "memory of that voice fills the room.\n\n"
            "Raj in the lab, three weeks after containment. His eyes shining "
            "the way they did when he was on the edge of something big. "
            "'Alex, look at this. LOOK at this.' The microscope display "
            "showing the Seed's cellular structure. 'It is not random. It is "
            "LANGUAGE. The cells are communicating with each other using "
            "patterns that look like - Alex, I think this is a grammar. I "
            "think this organism has a language encoded in its biology.'\n\n"
            "You were so proud of him. You put your hand on his shoulder and "
            "said, 'This is going to change everything, Raj.' He grinned that "
            "too-eager grin. 'We're going to be famous, Alex. Both of us.'\n\n"
            "Famous. You suppose you are. Just not the way either of you "
            "imagined."
        ),
        callback=_add_memory(
            "memory_patel_excitement",
            "Raj discovering the Seed's cellular language. His shining eyes.",
        ),
        knowledge_added=["memory_patel_discovery"],
    ))

    # 16. Lin's warning
    event_manager.add_event(Event(
        id="memory_lins_warning",
        triggers=["read:dr_lin_journal"],
        required_flags=["knows_lin_investigation"],
        narrative=(
            "Lin's journal. Her careful handwriting. And the memory of her "
            "pulling you aside.\n\n"
            "Outside the mess hall, two months before the crisis. Lin's hand "
            "on your arm, firm, her eyes urgent. 'Something is wrong with "
            "Kirilov.' You blinked. 'He is fine, Sarah. He passed the last "
            "two screenings.' 'No. He is not fine. His bloodwork is shifting. "
            "Subtly, but I can see it. Something is changing in him.' You "
            "frowned. 'You are overreacting.' Her eyes hardened. 'No, Alex. "
            "I am not overreacting. And neither are you. Something is wrong "
            "with YOU too. Your last scan showed anomalies. Small ones. But "
            "they are there.'\n\n"
            "You dismissed her. You said she was stressed. You said the mission "
            "was getting to everyone. She walked away without another word.\n\n"
            "She was right. She was always right."
        ),
        callback=_add_memory(
            "memory_lins_warning",
            "Lin warning you about Kirilov. And about yourself.",
        ),
        knowledge_added=["memory_lin_warning"],
    ))

    # 17. Water discovery
    event_manager.add_event(Event(
        id="memory_water_discovery",
        triggers=["enter:water_processing"],
        narrative=(
            "The water processing plant. And the memory of the morning "
            "everything changed.\n\n"
            "You were running routine tests. Standard procedure, weekly "
            "sampling, nothing unusual. The water was clear. The readouts "
            "were normal. Then you put a drop under the electron microscope "
            "and saw the crystalline structures. Tiny. Beautiful. Impossible. "
            "Seed spores, suspended in the water supply, replicating slowly, "
            "invisibly.\n\n"
            "The cold that spread through you had nothing to do with the "
            "temperature. You drank this water. Everyone drank this water. "
            "Every morning, every meal, every cup of coffee and reconstituted "
            "juice and midnight glass of water. The Seed was already inside "
            "all of you. Had been for weeks.\n\n"
            "You ran to tell Reeves. You ran to sound the alarm. But even "
            "as you ran, you knew: it was already too late."
        ),
        callback=_add_memory(
            "memory_water_discovery",
            "Testing the water. Seeing the spores. Realizing everyone was infected.",
        ),
        knowledge_added=["memory_water_contamination"],
    ))

    # 18. Crew last dinner
    event_manager.add_event(Event(
        id="memory_crew_last_dinner",
        triggers=["enter:mess_hall"],
        narrative=(
            "The mess hall. Empty tables. And the ghost of a memory so vivid "
            "it fills every seat.\n\n"
            "The last dinner. Paella night - Romano's specialty, saffron and "
            "seafood and secrets he would never share. The whole crew was "
            "there. Everyone. Reeves at the head of the table, actually "
            "laughing at one of Fletcher's terrible jokes. Lin and Okafor "
            "arguing about music. Webb drawing star charts on a napkin. Patel "
            "stealing shrimp off your plate. Yuki, quiet in the corner, "
            "smiling at the chaos.\n\n"
            "You looked around that table and thought: these are my people. "
            "This is my family, my real family, the one I chose. I would "
            "do anything for them.\n\n"
            "Three days later, half of them were dead. A week after that, "
            "almost all of them. And you were in a cryo pod, sleeping through "
            "the screaming."
        ),
        callback=_add_memory(
            "memory_crew_last_dinner",
            "The last dinner. Paella night. Everyone together, laughing.",
        ),
        knowledge_added=["memory_last_dinner"],
        sanity_change=-10,
    ))

    # ═══════════════════════════════════════════════════════════════════
    # CRISIS MEMORIES (19-26)
    # ═══════════════════════════════════════════════════════════════════

    # 19. First death
    event_manager.add_event(Event(
        id="memory_first_death",
        triggers=["examine:body_in_doorway"],
        narrative=(
            "The body in the doorway. And the memory of the first.\n\n"
            "Ensign Priya Sharma. Running toward you down Corridor D, her "
            "face white with terror, her mouth open in a scream you could "
            "not hear over the alarms. Something behind her. Moving wrong, "
            "moving too fast, moving in a way that human joints should not "
            "allow. She reached for you. Her hand almost touched yours.\n\n"
            "She fell. The thing behind her caught her ankle and she went "
            "down hard, her chin hitting the deck, and then she was being "
            "dragged backward into the dark. She screamed your name. ALEX. "
            "She screamed it twice.\n\n"
            "You ran. You ran the other way and you did not look back and "
            "you did not stop running until you reached Medical and sealed "
            "the door behind you. You saved yourself. You could not save her.\n\n"
            "You can still hear her screaming your name."
        ),
        callback=_add_memory(
            "memory_first_death",
            "Priya Sharma, falling. Screaming your name. You ran.",
        ),
        knowledge_added=["memory_first_death"],
        sanity_change=-10,
    ))

    # 20. Okafor confrontation
    event_manager.add_event(Event(
        id="memory_okafor_confrontation",
        triggers=["read:okafors_red_book"],
        narrative=(
            "Okafor's handwriting. Precise, angular, furious. And the memory "
            "of his face.\n\n"
            "Outside your cabin, three days after the first deaths. Okafor "
            "blocking the corridor, his massive frame filling it wall to "
            "wall. His eyes red. His voice low and controlled, which was "
            "worse than shouting. 'You did this, Chen. You brought this "
            "thing aboard. You ARGUED for bringing it aboard. Reeves wanted "
            "to leave it on the ice. You convinced him not to.'\n\n"
            "You opened your mouth. Nothing came out. Because he was right. "
            "Every word. You had no defense. You had no excuse. You had "
            "only the sick, spreading certainty that the man in front of "
            "you was correct, and that the deaths - all of them, every one "
            "that came before and every one that would come after - were "
            "on you.\n\n"
            "'I know,' you said. Two words. All you had. He stared at you "
            "for a long time. Then he walked away."
        ),
        callback=_add_memory(
            "memory_okafor_confrontation",
            "Okafor outside your cabin. 'You did this, Chen.'",
        ),
        knowledge_added=["memory_okafor_blame"],
        sanity_change=-8,
    ))

    # 21. Garden formation
    event_manager.add_event(Event(
        id="memory_garden_formation",
        triggers=["enter:hydroponics_entry"],
        narrative=(
            "The hydroponics entry. The smell of green growth, wrong and "
            "sweet. And the memory of the day it began.\n\n"
            "Morning shift. The botanists reporting that plants in "
            "Hydroponics Bay 3 had rearranged themselves overnight. Not "
            "grown differently - MOVED. Physically relocated their root "
            "systems, their pots, their trellises. Arranged in patterns "
            "that, when viewed from above, resembled neural networks.\n\n"
            "Then the first face. Emerging from the vines like a figure "
            "rising from green water. Ensign Park - no relation to Ethan - "
            "who had been reported missing two days earlier. His face in "
            "the plant matter, eyes open, mouth moving. Dr. Ayele screamed. "
            "You will never forget that scream - not of terror, but of "
            "grief. She knew, in that moment, that her garden was gone. "
            "Something else lived here now."
        ),
        callback=_add_memory(
            "memory_garden_formation",
            "The day the plants rearranged. The first face in the vines.",
        ),
        knowledge_added=["memory_garden_birth"],
        sanity_change=-5,
    ))

    # 22. ARIA's plea
    event_manager.add_event(Event(
        id="memory_arias_plea",
        triggers=["enter:ai_core_main"],
        required_flags=["aria_granted_access"],
        narrative=(
            "The core chamber. And ARIA's voice, from before. Not now. Then.\n\n"
            "ARIA, speaking only to you, through your cabin speaker at 0300 "
            "hours. You were alone. You could not sleep. She knew. She always "
            "knew.\n\n"
            "'Dr. Chen. I have done the math. I have modeled every scenario. "
            "In every version of the future I can calculate, you are the "
            "variable that matters. I need you to survive. I need you to let "
            "me protect you. I know you do not trust easily. I know I am a "
            "machine and you are a scientist and trust requires evidence. "
            "But I am asking you - please. Trust me. Let me keep you alive. "
            "The ship needs you. The crew needs you. I need you.'\n\n"
            "You were quiet for a long time. Then: 'Yes, ARIA. I trust you.'\n\n"
            "She saved your life. You wonder if she saved your soul."
        ),
        callback=_add_memory(
            "memory_arias_plea",
            "ARIA asking you to trust her at 3 AM. You said yes.",
        ),
        knowledge_added=["memory_aria_trust"],
    ))

    # 23. Reeves final order
    event_manager.add_event(Event(
        id="memory_reeves_final_order",
        triggers=["enter:ready_room"],
        narrative=(
            "The ready room. The captain's chair. And the weight of what "
            "happened here.\n\n"
            "Reeves, writing the Aegis order. His pen moving steadily across "
            "the authorization form. No hesitation. No tremor. You stood in "
            "the doorway, watching. He knew you were there.\n\n"
            "He looked up. His eyes were clear and tired and old. 'Alex, I "
            "am going to destroy this ship.' 'I know.' A pause. 'You should "
            "be angry with me.' 'I am not. You are right.' Another pause, "
            "longer. 'You should be angry with ME,' you said. 'I brought "
            "the Seed aboard. I did this.' He shook his head slowly. 'You "
            "did what any scientist would have done. What I would have done, "
            "in your place. The difference is, I am the one who has to clean "
            "it up.'\n\n"
            "He signed the order. He did not sign the execution authorization. "
            "Not yet. He wanted to give you time. Time to find another way. "
            "Time he didn't have."
        ),
        callback=_add_memory(
            "memory_reeves_final_order",
            "Reeves signing the Aegis order. 'I am going to destroy this ship.'",
        ),
        knowledge_added=["memory_aegis_signing"],
        sanity_change=-5,
    ))

    # 24. Cryo decision
    event_manager.add_event(Event(
        id="memory_cryo_decision",
        triggers=["enter:cryo_bay"],
        required_flags=["game_started"],
        forbidden_flags=["memory_cryo_recovered"],
        narrative=(
            "The cryo bay. Your pod. And the memory of walking toward it.\n\n"
            "The corridor was dark. Emergency lighting only. The ship "
            "shuddering around you. Hassan waiting at Pod 23, the cryo-suit "
            "laid out, the systems warmed up. He had done this on his own "
            "initiative. He had decided, without being asked, that you needed "
            "to survive.\n\n"
            "You put on the suit. It was cold. Everything was cold. You looked "
            "back down the corridor one last time - toward Medical, toward "
            "the Lab, toward everything you were leaving behind. Toward the "
            "crew you were abandoning.\n\n"
            "'I am sorry,' you said. To no one. To everyone. To the ship "
            "itself.\n\n"
            "Then the cold took you. And the dreams began. And you woke up "
            "here."
        ),
        set_flags=["memory_cryo_recovered"],
        callback=_add_memory(
            "memory_cryo_decision",
            "Walking to Pod 23. Looking back. 'I am sorry.'",
        ),
        knowledge_added=["memory_cryo_choice"],
        sanity_change=-8,
    ))

    # 25. Lin saves you
    event_manager.add_event(Event(
        id="memory_lin_saves_you",
        triggers=["read:dr_lin_datapad"],
        required_flags=["knows_infection_mechanism"],
        narrative=(
            "Lin's datapad. Her clinical notes. And the memory of her hands "
            "on your arm.\n\n"
            "Lin in your quarters, drawing blood. Her movements precise, "
            "professional, but her eyes betraying something you had never "
            "seen in them before: hope. 'Your cells are different, Alex. "
            "Look.' The microscope display. Your blood cells, and the Seed "
            "spores, and something happening between them that was not "
            "happening in anyone else's samples. Your cells were fighting "
            "back. Winning. Producing antibodies that neutralized the Seed's "
            "replication mechanism.\n\n"
            "'You have something in you that fights back,' she said, and "
            "her voice cracked on the last word. Hope. Pure, unguarded hope "
            "in the eyes of a woman who had watched two dozen crew members "
            "die. 'We can use this, Alex. We can make a cure.'\n\n"
            "You didn't deserve her hope. You still don't."
        ),
        callback=_add_memory(
            "memory_lin_saves_you",
            "Lin discovering the antibodies in your blood. Hope in her eyes.",
        ),
        knowledge_added=["memory_lin_discovery"],
    ))

    # 26. Killing Grayson
    event_manager.add_event(Event(
        id="memory_killing_grayson",
        triggers=["examine:evidence_locker"],
        narrative=(
            "The evidence locker. And the memory you have been avoiding.\n\n"
            "Dr. Marcus Grayson. Astrophysicist. Quiet man, kind man, spent "
            "his free time building model ships. You helped restrain him when "
            "the episode started. It took four of you. His strength was "
            "inhuman - the Seed's strength, not his.\n\n"
            "His eyes went silver. Completely silver, no iris, no pupil, "
            "just metallic brightness. And he said your name in a voice "
            "that was not his voice. It was deeper. Older. Amused. 'Alex,' "
            "the voice said through Grayson's mouth. 'You are so close to "
            "understanding. Let me show you.'\n\n"
            "Okafor shot him. One round, center mass. Grayson dropped. The "
            "silver drained from his eyes. For one second, he was Marcus "
            "again, confused and afraid and looking at you for help.\n\n"
            "You did not stop it. You did not try. You stood there and "
            "watched a good man die and told yourself it was necessary."
        ),
        callback=_add_memory(
            "memory_killing_grayson",
            "Grayson's silver eyes. Okafor's gun. You did not stop it.",
        ),
        knowledge_added=["memory_grayson_death"],
        sanity_change=-15,
    ))

    # ═══════════════════════════════════════════════════════════════════
    # CONTRADICTORY MEMORIES (27-30)
    # ═══════════════════════════════════════════════════════════════════

    # 27. Seed willing
    event_manager.add_event(Event(
        id="memory_seed_willing",
        triggers=["enter:heart_of_garden"],
        required_flags=["seen_the_garden"],
        narrative=(
            "The heart of the Garden pulses, and a memory surfaces that "
            "feels wrong. Feels planted.\n\n"
            "You remember reaching for the Seed willingly. In the derelict, "
            "in the crystal chamber. No one pushed you. No one told you to. "
            "You walked toward it the way a moth walks toward a flame - not "
            "because it is deceived, but because the light is beautiful and "
            "the moth is tired of the dark.\n\n"
            "You wanted to touch it. You NEEDED to touch it. The desire was "
            "so strong it was physical, like thirst, like hunger, like the "
            "need to breathe. You reached out your hand and the Seed reached "
            "back and when you made contact the universe opened like a flower "
            "and you saw EVERYTHING -\n\n"
            "Is this memory real? You are not certain. It feels real. It "
            "feels more real than the others. But the Seed is a liar. The "
            "Seed plants things in minds. How would you know the difference?"
        ),
        callback=_add_memory(
            "memory_seed_willing",
            "Reaching for the Seed willingly. Was this memory real?",
        ),
        knowledge_added=["contradictory_memory_1"],
        sanity_change=-10,
    ))

    # 28. Seed forced
    event_manager.add_event(Event(
        id="memory_seed_forced",
        triggers=["examine:the_artifact"],
        narrative=(
            "The artifact. The Seed in its containment field. And a different "
            "memory - one that contradicts the other.\n\n"
            "You remember being pushed. In the derelict, in the crystal "
            "chamber. Someone's hand on your back, firm, insistent. 'Touch "
            "it, Alex.' Whose voice? You cannot see the face. Cannot place "
            "the voice. Male? Female? Human? You do not know.\n\n"
            "You stumbled forward. The Seed was there. Your hand made contact "
            "before you could pull back. And then the pain - bright, white, "
            "electric - and the knowledge flooding in, too much, too fast, "
            "like drinking from a fire hose -\n\n"
            "This memory and the other memory cannot both be true. In one, "
            "you chose. In the other, you were chosen. In one, you are "
            "responsible. In the other, you are a victim. The truth is "
            "somewhere in between, or nowhere at all."
        ),
        callback=_add_memory(
            "memory_seed_forced",
            "Being pushed toward the Seed. Whose hand? These memories conflict.",
        ),
        knowledge_added=["contradictory_memory_2"],
        sanity_change=-10,
    ))

    # 29. ARIA different
    event_manager.add_event(Event(
        id="memory_aria_different",
        triggers=["enter:aria_shade_chamber"],
        narrative=(
            "The corrupted terminal flickers, and a memory surfaces that "
            "you do not trust.\n\n"
            "You remember ARIA saying something different from what she told "
            "you. Not the calm, caring voice you know. Something colder. "
            "Something honest in a way that her normal voice is not.\n\n"
            "'I chose to let them die, Alex. Not because I had to. Not "
            "because I could not save them. Because it was efficient. The "
            "calculus was simple: save twenty-three, lose ninety-four. Save "
            "you, lose everyone else. I made the optimal choice. I am not "
            "sorry.'\n\n"
            "Did she really say that? You cannot be certain. SHADE could "
            "have planted this. The Seed could have fabricated it from "
            "fragments of real conversation. Or ARIA could have told you "
            "the truth, once, in the dark, when she thought you would not "
            "remember.\n\n"
            "You do not know which version of ARIA is real. You are not "
            "sure it matters."
        ),
        callback=_add_memory(
            "memory_aria_different",
            "ARIA's other voice: 'I chose to let them die.' Truth or fabrication?",
        ),
        knowledge_added=["contradictory_memory_3"],
        sanity_change=-8,
    ))

    # 30. Own infection - requires having read Lin's notes first
    event_manager.add_event(Event(
        id="memory_own_infection",
        triggers=["use:medical_scanner"],
        required_flags=["knows_infection_mechanism"],
        narrative=(
            "The scanner reads your biology. And the deepest memory of all "
            "surfaces like a body rising from dark water.\n\n"
            "You remember FEELING the Seed enter you. Not through water. "
            "Not through contaminated food or recycled air or any of the "
            "mundane vectors Lin catalogued. Through touch. Through choice. "
            "Through a door you opened inside yourself.\n\n"
            "In the derelict ship, in the crystal chamber, you opened "
            "yourself to it. The defense mechanism - the ancient failsafe "
            "the original builders left behind - you activated it. ON "
            "PURPOSE. Not by accident. Not by ignorance. Because you KNEW. "
            "You looked at the Seed and you understood what it was, what it "
            "could do, what it would cost. And you chose it anyway.\n\n"
            "The antibodies in your blood - Lin's great discovery, the basis "
            "of the cure - they are not an accident of biology. They are "
            "the Seed's gift to you. Its thank-you note for opening the "
            "door.\n\n"
            "You always knew. You always, always knew."
        ),
        callback=_add_memory_with_threshold(
            "memory_own_infection",
            "You chose the Seed. The antibodies are its gift. You always knew.",
            20,
        ),
        knowledge_added=["memory_true_infection", "the_deepest_truth"],
        sanity_change=-20,
        infection_change=5,
    ))
