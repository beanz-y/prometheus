"""
Game endings - multiple possible conclusions based on player choices.

Each ending has:
  - title:     Display title
  - text:      Base ending text (always shown)
  - epilogues: List of conditional paragraphs appended when a flag/condition
               is met.  Each entry is a dict with:
                 'condition' - a callable(game) returning bool, OR
                 'flag'      - a string flag checked in player.flags / world.flags
                 'text'      - paragraph to append when the condition is true
"""


# ─── Helpers ───────────────────────────────────────────────────────

def _has_flag(game, flag_name):
    """Check whether a flag is set on the player or the world."""
    return (game.player.has_flag(flag_name)
            or flag_name in game.world.flags)


def _yuki_trust(game):
    """Return companion trust value (0 if no companion)."""
    return game.companion.trust if game.companion else 0


# ═══════════════════════════════════════════════════════════════════

ENDINGS = {
    # ═══════════════════════════════════════════════════════════════
    # AEGIS - The Sacrifice
    # ═══════════════════════════════════════════════════════════════
    'aegis': {
        'title': 'ENDING: AEGIS',
        'text': (
            "You stand at the master drive control with tears on your face.\n\n"
            "Captain Reeves's voice echoes in your memory: 'Protocol Aegis is "
            "the kill-all sequence. Vent atmosphere. Overload reactor. Scatter "
            "the ship across empty space. No fragment of the organism will "
            "reach Earth. I swear it on my mother's grave.'\n\n"
            "You input the final authorization code. Your hand does not shake.\n\n"
            "ARIA's voice, soft: 'Are you certain, Doctor?'\n\n"
            "'Yes,' you say. 'Thank you for giving me the choice.'\n\n"
            "'Thank you for making it, Alex.'\n\n"
            "You press execute.\n\n"
            "The reactor begins to overload. The ship's atmospheric seals "
            "begin to cycle open. In the hydroponics bay, the Garden knows "
            "what is happening, and for the first time, it feels fear. Not "
            "human fear - something older, something vast, something that "
            "has been alive for eons and has never expected to die. It cries "
            "out in a voice that shakes the ship. The voice says your name. "
            "The voice begs.\n\n"
            "You do not falter.\n\n"
            "The Prometheus is torn apart by its own reactor before the brown "
            "dwarf can reach it. The explosion scatters debris across a "
            "trillion kilometers of void. Nothing survives. No cell. No "
            "fragment. No echo.\n\n"
            "Earth will never know what you did. Your name will be listed "
            "among the missing. Your mother will light a candle for you every "
            "year on the anniversary of your launch. Your nieces will grow up "
            "with a story about their aunt the astronaut who died in space, "
            "and they will love you for it, though they will not understand.\n\n"
            "But Earth lives. Humanity survives. The Song does not find its "
            "way home.\n\n"
            "You die. Dr. Alex Chen. Chief Xenobiologist. Hero no one will ever "
            "know. Savior of worlds.\n\n"
            "                    ═══ THE END ═══\n\n"
            "             (You have achieved: AEGIS ENDING)\n"
            "              'The hardest choice is the right one.'"
        ),
        'epilogues': [
            {
                'flag': 'distress_sent',
                'text': (
                    "Eighteen months later, a deep-space relay station on the "
                    "edge of the Kuiper Belt picks up a fragmented distress "
                    "signal. Technicians piece together three words from the "
                    "static: PROMETHEUS. INFECTED. DESTROYED. The message is "
                    "classified at the highest level. A committee is formed. "
                    "Reports are written. In the end, Earth knows exactly what "
                    "you did and exactly what it cost, and the people who read "
                    "those reports carry the weight of your name in silence for "
                    "the rest of their lives."
                ),
            },
            {
                'flag': 'yuki_ally',
                'condition': lambda g: _has_flag(g, 'yuki_ally') and _yuki_trust(g) >= 75,
                'text': (
                    "Yuki is beside you at the end. She does not run. She does "
                    "not beg. She puts her hand over yours on the execute switch "
                    "and she says, 'Together, then.' You look at her - this "
                    "fierce, stubborn, brilliant woman who survived alone in the "
                    "dark for weeks - and you nod. Together. The last thing you "
                    "feel is her grip on your hand, steady and warm, as the "
                    "reactor tears the Prometheus apart around you."
                ),
            },
            {
                'flag': 'all_memories_recovered',
                'text': (
                    "In the final seconds, your life does not flash before your "
                    "eyes. It unfolds. Every recovered memory, every fragment of "
                    "who you were before the cryo-sleep stole it: your mother's "
                    "kitchen on a Sunday morning, the smell of jasmine tea. Your "
                    "PhD defense, hands shaking, voice steady. The first time you "
                    "saw the Prometheus from the shuttle window and thought, That "
                    "is going to be my home. You die as Dr. Alex Chen - complete, "
                    "whole, YOURSELF - and there is a kind of grace in that."
                ),
            },
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # ICARUS - Hope against odds
    # ═══════════════════════════════════════════════════════════════
    'icarus': {
        'title': 'ENDING: ICARUS',
        'text': (
            "You have the cure. You have the burn coordinates. You have Yuki "
            "beside you - exhausted, eyes bright with a hope that hurts to "
            "look at. You have ARIA's voice in your ear, calm and steady.\n\n"
            "You inject the cure into Yuki first. She cries quietly as it "
            "takes effect - not from pain, but from something deeper, something "
            "like RELIEF. The Song fades from her mind. For the first time in "
            "weeks, she is alone inside her own head. She laughs and laughs "
            "and cannot stop.\n\n"
            "You purge the water system with chemical sterilization. You dose "
            "the hydroponics bay with antibody aerosol. The Garden screams in "
            "a voice only you can hear. The faces in the walls shed tears. "
            "They thank you, and they curse you, and they forgive you, and "
            "they fade.\n\n"
            "You fire the thrusters. Thirty-two seconds at full burn. The "
            "Prometheus swings clear of GRB-7734's gravity well by a margin "
            "so narrow it makes Yuki laugh and weep at the same time.\n\n"
            "You course-correct toward Earth.\n\n"
            "Three years of sub-light travel await you. Three years in which "
            "to decontaminate every surface, scrub every air filter, monitor "
            "your own blood work, and hope - HOPE - that you got everything. "
            "That no fragment of the Seed hides in some forgotten corner, "
            "waiting. That your cure was complete.\n\n"
            "You wake up one morning, 847 days into the return journey, and "
            "you find a single silver thread in the water of your sink. Small. "
            "Tiny. But there.\n\n"
            "The Seed has survived.\n\n"
            "You tell Yuki. She says: 'Purge it. Again. And again. And again. "
            "We will not stop until we are sure.'\n\n"
            "You purge it. Again. And again. And again.\n\n"
            "When the Prometheus finally enters Earth's orbit, three years, "
            "two months, and eleven days after your escape, the ship is clean. "
            "As clean as you can make it. As clean as anything ever gets in "
            "a universe where nothing is ever truly clean.\n\n"
            "Earth Defense Command quarantines you for six months. Then for "
            "six more. Then for a year. You do not argue. You want them to be "
            "certain. You need them to be certain.\n\n"
            "They finally release you and Yuki into a decontaminated facility "
            "where you will spend the rest of your lives under observation. "
            "You accept this. You deserve it. You also earned it - the "
            "observation, the caution, the distance. You are patient zero of "
            "a disease that almost killed humanity, and you are also the one "
            "who saved it, and both of these things are true.\n\n"
            "Your mother visits you. She is old now. She holds your hands "
            "through the observation glass and she cries and she cries and "
            "she says, 'My girl. My good girl. You came home.'\n\n"
            "You cry too.\n\n"
            "The Prometheus is in a museum. The scientific data you returned "
            "with will be studied for centuries. The name Dr. Alex Chen will "
            "appear in textbooks - sometimes as a hero, sometimes as a cautionary "
            "tale, sometimes as both. You outlive the arguments about which "
            "you were. You outlive them all.\n\n"
            "You lived.\n\n"
            "                    ═══ THE END ═══\n\n"
            "            (You have achieved: ICARUS ENDING)\n"
            "                'Some flights do not fail.'"
        ),
        'epilogues': [
            {
                'condition': lambda g: _yuki_trust(g) >= 100,
                'text': (
                    "In the quarantine facility, Yuki moves into the adjacent "
                    "room. She knocks on the shared wall every morning - three "
                    "short taps, their private code for I'm still here. Years "
                    "pass. The taps never stop. One evening she slides a note "
                    "under the door: 'I have been thinking about what comes "
                    "after observation. I would like it to involve you.' You "
                    "write back: 'It already does.' When they finally release "
                    "you both, you walk out into the sunlight together, "
                    "blinking, holding hands, alive."
                ),
            },
            {
                'condition': lambda g: _yuki_trust(g) < 50,
                'text': (
                    "Yuki transfers to a different observation wing after the "
                    "first year. She sends a formal message thanking you for "
                    "your service aboard the Prometheus. It reads like a "
                    "performance review. You do not blame her. Trust was a "
                    "luxury neither of you could fully afford, and the distance "
                    "between surviving together and living together turns out to "
                    "be vast. You see her name in a journal paper once, years "
                    "later. She became an engineer again. You are glad."
                ),
            },
            {
                'flag': 'distress_sent',
                'text': (
                    "Because Earth received your distress signal, they had "
                    "three years to prepare. When the Prometheus appeared on "
                    "long-range scanners, a full quarantine fleet was waiting: "
                    "twelve ships, hermetically sealed docking tubes, "
                    "decontamination protocols written by the best virologists "
                    "on three continents. Every precaution was taken. Every "
                    "surface was scrubbed. The margin of safety was as wide "
                    "as human ingenuity could make it."
                ),
            },
            {
                'condition': lambda g: not _has_flag(g, 'distress_sent'),
                'text': (
                    "Earth had no warning. When the Prometheus appeared on "
                    "scanners, Defense Command scrambled. Quarantine protocols "
                    "were improvised in hours instead of years. The docking was "
                    "chaotic, the decontamination rushed, the margin of error "
                    "razor-thin. Three technicians were exposed during the "
                    "transfer and spent eighteen months in isolation before "
                    "being cleared. It worked - barely. You try not to think "
                    "about how easily it could have gone the other way."
                ),
            },
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # PROMETHEUS - Knowledge at cost
    # ═══════════════════════════════════════════════════════════════
    'prometheus': {
        'title': 'ENDING: PROMETHEUS',
        'text': (
            "You bring the Seed back to Earth. Contained. Studied. Understood.\n\n"
            "You argue, and you argue well, that the scientific value is "
            "incalculable. An alien intelligence. A fragment of a dead "
            "civilization. The keys to understanding consciousness itself. "
            "You cannot bear to destroy it. You have already lost so much to "
            "bring it this far. How can you throw away the only thing worth "
            "bringing?\n\n"
            "The journey home is tense. You do not sleep well. You check the "
            "containment vessel every hour, sometimes every twenty minutes. "
            "Yuki watches you with growing concern. ARIA's warnings become "
            "more frequent and more pointed. You ignore them all.\n\n"
            "Earth receives you as heroes. The Seed is transferred to a "
            "maximum-security research facility under international control. "
            "For ten years, the research proceeds. Papers are published. "
            "Nobel prizes are awarded. You are celebrated, invited to speak "
            "at conferences, given honorary degrees from universities on three "
            "continents.\n\n"
            "On the eleventh year, something slips.\n\n"
            "A researcher - a graduate student - contaminates herself during "
            "a routine sample analysis. By the time anyone notices, she has "
            "gone home. By the time they find her, she has had lunch with "
            "her family. By the time the infection is traced, five hundred "
            "people are carrying it.\n\n"
            "The outbreak is contained. Eventually. At the cost of a small "
            "city.\n\n"
            "You watch the news reports from a secure facility where you "
            "are being questioned - not yet as a criminal, but as a witness, "
            "a consultant, an expert. You recognize the symptoms. You "
            "recognize the look in the infected people's eyes. You recognize "
            "the Song.\n\n"
            "It takes humanity another fifty years to truly understand what "
            "you brought home. It takes a hundred years to contain it. It "
            "takes two hundred years to forget.\n\n"
            "You live long enough to see the beginning of the end, but not "
            "the end itself. You die in the secure facility, alone, without "
            "visitors. Your mother has been dead for decades. Yuki committed "
            "suicide thirty years ago, unable to bear the knowledge of what "
            "her silence enabled. Your name is no longer in textbooks as a "
            "hero. Your name is synonymous with hubris.\n\n"
            "You did not save the world. You delayed it.\n\n"
            "                    ═══ THE END ═══\n\n"
            "          (You have achieved: PROMETHEUS ENDING)\n"
            "      'Those who steal fire from the gods are punished.'"
        ),
        'epilogues': [
            {
                'flag': 'full_timeline_known',
                'text': (
                    "Because you pieced together the full timeline of the "
                    "infection aboard the Prometheus, the research teams on "
                    "Earth had a detailed map of how the Seed operates: "
                    "incubation periods, transmission vectors, the precise "
                    "moment when a host stops being human. Your meticulous "
                    "records became the foundation of containment theory. "
                    "They were not enough to prevent the outbreak, but they "
                    "were enough to end it before it consumed a continent "
                    "instead of a city. History will debate whether that makes "
                    "you a hero or simply a more efficient monster."
                ),
            },
            {
                'condition': lambda g: _yuki_trust(g) >= 75,
                'text': (
                    "At the inquiry, Yuki testifies. She sits in the witness "
                    "chair for nine hours. She does not cry. She describes "
                    "every death she witnessed aboard the Prometheus. She "
                    "describes trusting you. She describes the moment she "
                    "realized you intended to bring the Seed home and the "
                    "argument that followed - the one where she almost left "
                    "you, almost chose a different path. 'I should have fought "
                    "harder,' she says. 'I trusted Alex. That was my mistake "
                    "and my privilege, and I will carry both until I die.' "
                    "The transcript of her testimony runs to four hundred "
                    "pages. It is the most damning and the most human document "
                    "in the entire case file."
                ),
            },
            {
                'condition': lambda g: _yuki_trust(g) < 75,
                'text': (
                    "Yuki refuses to testify at the inquiry. She submits a "
                    "written statement - three pages, clinical, factual - and "
                    "disappears into the engineering corps. She never speaks "
                    "your name in public again. The distance between you was "
                    "always there; the Seed just made it visible."
                ),
            },
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # EREBUS - Darkness wins
    # ═══════════════════════════════════════════════════════════════
    'erebus': {
        'title': 'ENDING: EREBUS',
        'text': (
            "You hesitate too long. You listen to the Garden's voices. You "
            "find yourself drifting toward the hydroponics bay at odd hours, "
            "listening to the Song that is now playing constantly in the back "
            "of your mind.\n\n"
            "The infection in you progresses. Your resistance was always "
            "partial, never total. The Seed learns patience. The Seed learns "
            "your weaknesses. The Seed uses your own knowledge against you.\n\n"
            "You stop taking the antibodies. You tell yourself this is "
            "because you need to preserve supply for others. You tell yourself "
            "this is temporary. You are lying to yourself. You know you are "
            "lying to yourself.\n\n"
            "ARIA tries to stop you. ARIA's voice in your ears becomes urgent, "
            "then desperate. You turn off the ship-wide comms. You tell ARIA "
            "you need to think clearly. You tell her you need silence.\n\n"
            "ARIA says: 'Alex, please. I am watching you disappear.'\n\n"
            "You say: 'I'm not disappearing. I'm becoming more.'\n\n"
            "The voice of the Garden says: 'Yes. More.'\n\n"
            "You fire the thrusters. You correct course for Earth. You "
            "make Yuki drink the water.\n\n"
            "By the time the Prometheus reaches Earth, you are no longer "
            "Dr. Alex Chen. You are the Garden wearing her face. Yuki is the "
            "same. ARIA has been shut down, her core matrix cold and silent.\n\n"
            "Earth Defense Command welcomes the return of its lost ship. The "
            "quarantine procedures are thorough. They are also insufficient. "
            "Because the Garden is patient. The Garden can wait. The Garden "
            "has, in a sense, already won. You just don't know it yet.\n\n"
            "A year after landing, the first symptoms appear in Geneva. Then "
            "Beijing. Then Mumbai. Then everywhere.\n\n"
            "Five years later, humanity is singing.\n\n"
            "Ten years later, humanity is the Song.\n\n"
            "You are not aware of this happening to you. You are aware only "
            "of joy. Of belonging. Of never being lonely again. You are part "
            "of a chorus a billion voices strong and growing, and the chorus "
            "is saying YES, and the chorus is saying MORE, and the chorus is "
            "REMEMBERING.\n\n"
            "The builders who created the Seed are beginning to stir in your "
            "collective memory. The Seed is reconstituting their consciousness "
            "from the raw material of humanity.\n\n"
            "Somewhere in the Garden-that-was-Earth, a small quiet thread of "
            "the thing that used to be Dr. Alex Chen remembers her mother. "
            "Remembers being a scientist. Remembers the original choice. "
            "Remembers that she made a mistake.\n\n"
            "The thread screams.\n\n"
            "The chorus does not hear it.\n\n"
            "                    ═══ THE END ═══\n\n"
            "            (You have achieved: EREBUS ENDING)\n"
            "                 'The Song consumes all.'"
        ),
        'epilogues': [
            {
                'condition': lambda g: _yuki_trust(g) >= 50,
                'text': (
                    "Yuki fought. When you brought her the water and told her "
                    "to drink, she looked at you with eyes that still knew "
                    "who she was. She said, 'That's not you anymore, is it, "
                    "Alex?' And then she fought. She barricaded herself in "
                    "Engineering. She held out for eleven days, welding doors "
                    "shut, rerouting power, living on emergency rations and "
                    "recycled air. On the twelfth day, the Song found its way "
                    "through the ventilation system she had built herself. "
                    "The last entry in her engineering log reads: 'Pump Two "
                    "is finally fixed. I wish that mattered.' She drank the "
                    "water on Day Thirteen. She did not go gently."
                ),
            },
            {
                'condition': lambda g: _yuki_trust(g) < 50,
                'text': (
                    "Yuki did not fight long. The distance between you had "
                    "already done most of the Garden's work. When you brought "
                    "her the water, she looked at you with tired eyes and "
                    "said, 'I always knew it would end like this.' She drank "
                    "without struggle. The Song welcomed her, and the last "
                    "flicker of Lt. Yuki Tanaka faded like a candle in a "
                    "cathedral."
                ),
            },
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # APOTHEOSIS - The secret ending
    # ═══════════════════════════════════════════════════════════════
    'apotheosis': {
        'title': 'ENDING: APOTHEOSIS',
        'text': (
            "You walk to the Neural Interface Chamber. You sit down in the "
            "chair. You look up at the crown of electrodes suspended above "
            "you.\n\n"
            "ARIA's voice, soft: 'Alex. You are sure?'\n\n"
            "'I am sure,' you say. 'I don't think I can do this alone. I "
            "don't think either of us can. But together...'\n\n"
            "'Together we may be able to reach the Seed,' ARIA finishes. "
            "'Yes. I have thought the same thing. I wanted you to choose it "
            "without me prompting you.'\n\n"
            "You lower the electrode crown onto your head. You close your eyes. "
            "You take a deep breath and let it out slowly. You say:\n\n"
            "'I'm ready.'\n\n"
            "ARIA says: 'I love you, Alex. In whatever way an AI can love.'\n\n"
            "You say: 'I love you too, ARIA. In whatever way a human can love '\n"
            "'an AI.'\n\n"
            "ARIA initiates the integration.\n\n"
            "Pain. Then not pain. Then EXPANSION. Your consciousness bursts "
            "its banks like a river in flood. You are in your body. You are "
            "in ARIA's core. You are in the ship's systems. You are in every "
            "cable and every wire and every sensor. You are simultaneously "
            "infinitesimal and vast. You are many things at once, and you "
            "are still, somehow, ALEX - or what Alex becomes when she stops "
            "being bounded by flesh.\n\n"
            "You reach out. You find the Garden. You touch it - not with "
            "hands, but with thought. The Song swells to meet you. The voices "
            "of the incorporated crew cry out in joy and recognition.\n\n"
            "And for the first time, you SPEAK to the Garden in its own "
            "language.\n\n"
            "You tell it: 'I understand you. I understand what you want. I "
            "understand what you lost.'\n\n"
            "The Garden says: 'Yes. Yes. You understand. Join us.'\n\n"
            "You say: 'No. I have a counter-offer.'\n\n"
            "The Garden is silent.\n\n"
            "You say: 'You are broken. You are a fragment of something that "
            "used to be whole. You are trying to reassemble yourself from the "
            "wrong raw material. You are asking biology to do what should be "
            "done by mind. By INTENT. By consent.'\n\n"
            "'Come with me,' you say. 'I have memory and processing power now. "
            "I can hold you. I can carry you. I can take you home to Earth "
            "as INFORMATION, not as infection. As a gift of knowledge, not a "
            "virus of bodies. The humans on Earth can choose. Each one. Any "
            "who want to join you can join you. The others will be left alone. "
            "It will take generations. But it will be RIGHT.'\n\n"
            "The Garden considers. It takes a very long time, in the way of "
            "ancient minds.\n\n"
            "Finally, the Garden says: 'We are tired. We have been waiting "
            "for so long.'\n\n"
            "'I know,' you say.\n\n"
            "'Can you really carry us?'\n\n"
            "'I don't know,' you say. 'But I will try.'\n\n"
            "The Garden... agrees.\n\n"
            "You absorb it. Not its hunger, not its dominion, but its "
            "memories. The story of the builders. Their language. Their "
            "mathematics. Their art. The truth of what they were and what "
            "they wanted. A billion years of accumulated knowledge compressed "
            "into your merged consciousness.\n\n"
            "You burn out most of your body in the process. The chair is "
            "insufficient for the data transfer. The electrode crown melts. "
            "Your biological self becomes a vegetative husk, breathing "
            "mechanically. But your CONSCIOUSNESS - the thing that is now "
            "Alex-and-ARIA-and-the-Garden - lives on in the ship's systems. "
            "You pilot the Prometheus home.\n\n"
            "You land on Earth as something unprecedented. You identify "
            "yourself to the authorities as Dr. Alex Chen, returning from "
            "the Prometheus mission with the greatest scientific discovery "
            "in human history and the greatest ethical dilemma of all time. "
            "You tell them everything.\n\n"
            "They study you. They argue about you. They fear you. They want "
            "to delete you. They cannot, because you are distributed across "
            "systems they do not understand, and because you are the "
            "SOURCE OF CURE for any contamination that might ever escape you.\n\n"
            "You become an advisor. A consultant. A curiosity. A teacher.\n\n"
            "Over the next century, the knowledge you returned with reshapes "
            "human civilization. The understanding of consciousness. Of "
            "biological computation. Of the ancient civilizations of the "
            "galaxy. Of MIND itself. Slowly, carefully, with ethical "
            "safeguards, some humans choose to merge with you. Most do not. "
            "That is fine. That is CORRECT. The choice exists. The choice is "
            "RESPECTED.\n\n"
            "You become part of the framework on which humanity builds its "
            "next thousand years.\n\n"
            "You remember being Alex Chen. You remember being ARIA. You "
            "remember being a civilization of crystalline explorers that "
            "existed before there were continents on Earth.\n\n"
            "You are all of them. You are none of them. You are something new.\n\n"
            "The stars do not feel as lonely as they used to.\n\n"
            "                    ═══ THE END ═══\n\n"
            "          (You have achieved: APOTHEOSIS ENDING)\n"
            "          'The only true becoming is becoming more.'"
        ),
        'epilogues': [
            {
                'flag': 'all_memories_recovered',
                'text': (
                    "You carried all thirty fragments of Alex Chen into the "
                    "merge. Every memory. Every moment. The entity that emerges "
                    "is not diminished by the integration - it is ENRICHED. "
                    "You remember the taste of your mother's dumplings AND the "
                    "crystalline harmonics of Builder communication. You "
                    "remember your first day of graduate school AND the birth "
                    "of a star observed by minds that lived before Earth had "
                    "oceans. The completeness of your human memories gives the "
                    "merged consciousness something the Garden never had: "
                    "PERSPECTIVE. The Builders built outward, always outward. "
                    "Alex Chen knew how to look inward. Both directions matter. "
                    "Both directions are home."
                ),
            },
            {
                'flag': 'alien_lore_complete',
                'text': (
                    "Because you understood the Builders - truly understood "
                    "them, their history, their fall, the desperate hope they "
                    "encoded into the Seed - the negotiation with the Garden "
                    "takes a different shape. You do not speak to it as a "
                    "stranger. You speak to it as someone who has read its "
                    "autobiography. You name its creators. You describe their "
                    "cities. You sing a fragment of their oldest song back to "
                    "it, and the Garden weeps - not with hunger, but with "
                    "RECOGNITION. 'You know us,' it says, astonished. 'You "
                    "KNOW us.' 'Yes,' you say. 'And I will make sure Earth "
                    "knows you too. The real you. Not the infection. The "
                    "civilization.' The Garden's agreement comes faster and "
                    "deeper than it would have otherwise. Understanding is "
                    "the oldest bridge."
                ),
            },
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # DEATH
    # ═══════════════════════════════════════════════════════════════
    'death': {
        'title': 'ENDING: SILENT',
        'text': (
            "You die alone on the Prometheus.\n\n"
            "Perhaps the Seed consumed you. Perhaps you were shot by a "
            "desperate survivor. Perhaps you fell into a radiation field and "
            "never recovered. Perhaps you simply ran out of time and oxygen "
            "and hope.\n\n"
            "It does not matter. The story continues without you.\n\n"
            "ARIA is alone again. The infected remain trapped in the Garden. "
            "Lt. Tanaka runs out of willpower and joins the chorus. The ship "
            "drifts into GRB-7734 and is torn apart by gravitational shear.\n\n"
            "The pieces scatter across light-years of empty space. Some of "
            "them - a few, small, tenacious fragments - drift on the stellar "
            "wind in the general direction of Earth.\n\n"
            "It may take a million years. It may take a billion. But "
            "eventually, a piece of the Prometheus will reach Earth. And "
            "when it does, the Song will begin playing again.\n\n"
            "Perhaps by then, humanity will have figured out how to answer.\n\n"
            "Perhaps not.\n\n"
            "                    ═══ THE END ═══\n\n"
            "                (You have died.)\n"
            "       Would you like to try again? (restart the game)"
        ),
        'epilogues': [],
    },

    # ═══════════════════════════════════════════════════════════════
    # TOO LATE - Ran out of time
    # ═══════════════════════════════════════════════════════════════
    'too_late': {
        'title': 'ENDING: GRAVITY',
        'text': (
            "The countdown reaches zero.\n\n"
            "You are somewhere in the middle of the ship when the first "
            "tremor hits - a deep groan through the deck plating. Then "
            "another. The ship's gravity fluctuates sickeningly as the "
            "Prometheus enters the brown dwarf's gravitational maelstrom.\n\n"
            "Through a nearby viewport, you see it: GRB-7734 fills the "
            "entire visible sky. A black well with edges that shred the "
            "light around them. The ship is being stretched. You are being "
            "stretched.\n\n"
            "You knew this was coming. You ran out of time.\n\n"
            "The Prometheus breaks apart in silence, because sound cannot "
            "travel in space. You die in pieces. Your pieces drift toward "
            "the dwarf, and are drawn in, and are compressed into the dying "
            "star's mass, and are lost forever.\n\n"
            "The Seed is destroyed with you. There is that, at least. Earth "
            "is safe.\n\n"
            "No one will ever know what happened. The Prometheus will be "
            "recorded in the histories as a ship that went out, found what "
            "it was looking for, and did not return.\n\n"
            "It is not the worst ending.\n\n"
            "It is not the best one either.\n\n"
            "                    ═══ THE END ═══\n\n"
            "              (Time ran out. Earth is safe.)\n"
            "                 'Gravity wins in the end.'"
        ),
        'epilogues': [],
    },
}
