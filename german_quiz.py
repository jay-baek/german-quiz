# german_quiz.py
# Vocabulary database and quiz engine.

import random

# ---------------------------------------------------------------------------
# Word bank
# Each entry is a uniform dict with at minimum:
#   "de"   : German word (str)
#   "en"   : English gloss (str)
#   "type" : part of speech ("noun", "verb", "adj", "pronoun")
#
# Nouns additionally carry:
#   "gender"     : "m", "f", or "n"
#   "plural"     : plural form (str)
#
# Verbs additionally carry:
#   "class"      : "weak", "strong", or "irregular"
#   "separable"  : True if the verb has a detachable prefix (optional)
#   "prefix"     : the detachable prefix, e.g. "ab-" (optional)
#   "reflexive"  : True if the verb is reflexive (optional)
#
# Pronouns additionally carry:
#   "subtype"    : "personal" or "possessive"
#   "note"       : usage note shown in hint (optional)
#   "declines"   : True if the pronoun declines like an ein-word (possessives)
#
# Adjectives additionally carry (optional):
#   "note"       : usage note, e.g. polysemy or indeclinability
#   "indeclinable" : True if the adjective does not take case endings
# ---------------------------------------------------------------------------

WORDS = [
    # -------------------------------------------------------------------------
    # Nouns
    # -------------------------------------------------------------------------
    {"type": "noun", "en": "man",    "de": "Mann",    "gender": "m", "plural": "Männer"},
    {"type": "noun", "en": "boy",    "de": "Junge",   "gender": "m", "plural": "Jungen"},
    {"type": "noun", "en": "woman",  "de": "Frau",    "gender": "f", "plural": "Frauen"},
    {"type": "noun", "en": "girl",   "de": "Mädchen", "gender": "n", "plural": "Mädchen"},
    {"type": "noun", "en": "book",   "de": "Buch",    "gender": "n", "plural": "Bücher"},
    {"type": "noun", "en": "house",  "de": "Haus",    "gender": "n", "plural": "Häuser"},
    {"type": "noun", "en": "day",    "de": "Tag",     "gender": "m", "plural": "Tage"},
    {"type": "noun", "en": "church", "de": "Kirche",  "gender": "f", "plural": "Kirchen"},

    # -------------------------------------------------------------------------
    # Verbs — non-separable
    # -------------------------------------------------------------------------
    {"type": "verb", "en": "to fly",     "de": "fliegen",  "class": "strong"},
    {"type": "verb", "en": "to come",    "de": "kommen",   "class": "strong"},
    {"type": "verb", "en": "to go",      "de": "gehen",    "class": "weak"},
    {"type": "verb", "en": "to say",     "de": "sagen",    "class": "weak"},
    {"type": "verb", "en": "to be",      "de": "sein",     "class": "irregular"},
    {"type": "verb", "en": "to have",    "de": "haben",    "class": "irregular"},
    {"type": "verb", "en": "to breathe", "de": "atmen",    "class": "weak"},
    {"type": "verb", "en": "to work",    "de": "arbeiten", "class": "weak"},
    {"type": "verb", "en": "to eat",     "de": "essen",    "class": "strong"},
    {"type": "verb", "en": "to drive",   "de": "fahren",   "class": "strong"},
    {"type": "verb", "en": "to give",    "de": "geben",    "class": "strong"},
    {"type": "verb", "en": "to help",    "de": "helfen",   "class": "strong"},
    {"type": "verb", "en": "to cost",    "de": "kosten",   "class": "weak"},
    {"type": "verb", "en": "to kiss",    "de": "küssen",   "class": "weak"},
    {"type": "verb", "en": "to read",    "de": "lesen",    "class": "strong"},
    {"type": "verb", "en": "to mix",     "de": "mixen",    "class": "weak"},
    {"type": "verb", "en": "to talk",    "de": "reden",    "class": "weak"},
    {"type": "verb", "en": "to rain",    "de": "regnen",   "class": "weak"},
    {"type": "verb", "en": "to travel",  "de": "reisen",   "class": "weak"},
    {"type": "verb", "en": "to sleep",   "de": "schlafen", "class": "strong"},
    {"type": "verb", "en": "to see",     "de": "sehen",    "class": "strong"},
    {"type": "verb", "en": "to speak",   "de": "sprechen", "class": "strong"},
    {"type": "verb", "en": "to dance",   "de": "tanzen",   "class": "weak"},
    {"type": "verb", "en": "to carry",   "de": "tragen",   "class": "strong"},
    {"type": "verb", "en": "to meet",    "de": "treffen",  "class": "strong"},
    {"type": "verb", "en": "to wander",  "de": "wandern",  "class": "weak"},
    {"type": "verb", "en": "to wash",    "de": "waschen",  "class": "strong"},
    {"type": "verb", "en": "to throw",   "de": "werfen",   "class": "strong"},

    # -------------------------------------------------------------------------
    # Verbs — separable
    # -------------------------------------------------------------------------
    {"type": "verb", "en": "to depart",           "de": "abfahren",        "class": "strong",    "separable": True, "prefix": "ab-"},
    {"type": "verb", "en": "to pick up",           "de": "abholen",         "class": "weak",      "separable": True, "prefix": "ab-"},
    {"type": "verb", "en": "to wash up",           "de": "abwaschen",       "class": "strong",    "separable": True, "prefix": "ab-"},
    {"type": "verb", "en": "to start",             "de": "anfangen",        "class": "strong",    "separable": True, "prefix": "an-"},
    {"type": "verb", "en": "to arrive",            "de": "ankommen",        "class": "strong",    "separable": True, "prefix": "an-"},
    {"type": "verb", "en": "to phone",             "de": "anrufen",         "class": "strong",    "separable": True, "prefix": "an-"},
    {"type": "verb", "en": "to stop",              "de": "aufhören",        "class": "weak",      "separable": True, "prefix": "auf-"},
    {"type": "verb", "en": "to tidy up",           "de": "aufräumen",       "class": "weak",      "separable": True, "prefix": "auf-"},
    {"type": "verb", "en": "to stand up",          "de": "aufstehen",       "class": "strong",    "separable": True, "prefix": "auf-"},
    {"type": "verb", "en": "to go out",            "de": "ausgehen",        "class": "strong",    "separable": True, "prefix": "aus-"},
    {"type": "verb", "en": "to switch off",        "de": "ausschalten",     "class": "weak",      "separable": True, "prefix": "aus-"},
    {"type": "verb", "en": "to go shopping",       "de": "einkaufen",       "class": "weak",      "separable": True, "prefix": "ein-"},
    {"type": "verb", "en": "to invite",            "de": "einladen",        "class": "strong",    "separable": True, "prefix": "ein-"},
    {"type": "verb", "en": "to fall asleep",       "de": "einschlafen",     "class": "strong",    "separable": True, "prefix": "ein-"},
    {"type": "verb", "en": "to watch TV",          "de": "fernsehen",       "class": "strong",    "separable": True, "prefix": "fern-"},
    {"type": "verb", "en": "to bring along",       "de": "mitbringen",      "class": "irregular", "separable": True, "prefix": "mit-"},
    {"type": "verb", "en": "to come along",        "de": "mitkommen",       "class": "strong",    "separable": True, "prefix": "mit-"},
    {"type": "verb", "en": "to join in",           "de": "mitmachen",       "class": "weak",      "separable": True, "prefix": "mit-"},
    {"type": "verb", "en": "to take place",        "de": "stattfinden",     "class": "strong",    "separable": True, "prefix": "statt-"},
    {"type": "verb", "en": "to prepare",           "de": "vorbereiten",     "class": "weak",      "separable": True, "prefix": "vor-"},
    {"type": "verb", "en": "to introduce oneself", "de": "sich vorstellen", "class": "weak",      "separable": True, "prefix": "vor-", "reflexive": True},
    {"type": "verb", "en": "to close",             "de": "zumachen",        "class": "weak",      "separable": True, "prefix": "zu-"},

    # -------------------------------------------------------------------------
    # Adjectives — general
    # -------------------------------------------------------------------------
    {"type": "adj", "en": "big",                "de": "groß"},
    {"type": "adj", "en": "long",               "de": "lang"},
    {"type": "adj", "en": "small",              "de": "klein"},
    {"type": "adj", "en": "old",                "de": "alt"},
    {"type": "adj", "en": "new",                "de": "neu"},
    {"type": "adj", "en": "fresh",              "de": "frisch"},
    {"type": "adj", "en": "cold",               "de": "kalt"},
    {"type": "adj", "en": "beautiful",          "de": "schön"},
    {"type": "adj", "en": "hot",                "de": "heiß"},
    {"type": "adj", "en": "short",              "de": "kurz"},
    {"type": "adj", "en": "thick / fat",        "de": "dick"},
    {"type": "adj", "en": "thin / slim",        "de": "dünn"},
    {"type": "adj", "en": "fast",               "de": "schnell"},
    {"type": "adj", "en": "slow",               "de": "langsam"},
    {"type": "adj", "en": "intelligent",        "de": "intelligent"},
    {"type": "adj", "en": "stupid",             "de": "dumm"},
    {"type": "adj", "en": "sharp / spicy",      "de": "scharf",      "note": "means both sharp (knife) and spicy (food)"},
    {"type": "adj", "en": "dull / blunt",       "de": "stumpf"},
    {"type": "adj", "en": "ugly",               "de": "hässlich"},
    {"type": "adj", "en": "interesting",        "de": "interessant"},
    {"type": "adj", "en": "boring",             "de": "langweilig"},
    {"type": "adj", "en": "expensive",          "de": "teuer"},
    {"type": "adj", "en": "cheap",              "de": "billig"},
    {"type": "adj", "en": "happy",              "de": "glücklich"},
    {"type": "adj", "en": "sad",                "de": "traurig"},
    {"type": "adj", "en": "loud",               "de": "laut"},
    {"type": "adj", "en": "quiet / soft",       "de": "leise"},
    {"type": "adj", "en": "heavy / difficult",  "de": "schwer",      "note": "means both heavy (weight) and difficult (task)"},
    {"type": "adj", "en": "light / easy",       "de": "leicht",      "note": "opposite of both meanings of schwer"},
    {"type": "adj", "en": "tired",              "de": "müde"},
    {"type": "adj", "en": "clean",              "de": "sauber"},
    {"type": "adj", "en": "dirty",              "de": "schmutzig"},
    {"type": "adj", "en": "dangerous",          "de": "gefährlich"},
    {"type": "adj", "en": "safe / certain",     "de": "sicher",      "note": "means both safe and certain depending on context"},
    {"type": "adj", "en": "rich",               "de": "reich"},
    {"type": "adj", "en": "poor",               "de": "arm"},
    {"type": "adj", "en": "funny",              "de": "lustig"},

    # -------------------------------------------------------------------------
    # Adjectives — colors
    # Indeclinable colors (lila, rosa, orange, beige, creme, türkis) do not
    # take case endings — flagged for the future declension quiz mode.
    # -------------------------------------------------------------------------
    {"type": "adj", "en": "red",        "de": "rot"},
    {"type": "adj", "en": "blue",       "de": "blau"},
    {"type": "adj", "en": "green",      "de": "grün"},
    {"type": "adj", "en": "yellow",     "de": "gelb"},
    {"type": "adj", "en": "orange",     "de": "orange",   "indeclinable": True},
    {"type": "adj", "en": "purple",     "de": "lila",     "indeclinable": True},
    {"type": "adj", "en": "pink",       "de": "rosa",     "indeclinable": True},
    {"type": "adj", "en": "brown",      "de": "braun"},
    {"type": "adj", "en": "black",      "de": "schwarz"},
    {"type": "adj", "en": "white",      "de": "weiß"},
    {"type": "adj", "en": "gray",       "de": "grau"},
    {"type": "adj", "en": "silver",     "de": "silber"},
    {"type": "adj", "en": "golden",     "de": "golden"},
    {"type": "adj", "en": "beige",      "de": "beige",    "indeclinable": True},
    {"type": "adj", "en": "cream",      "de": "creme",    "indeclinable": True},
    {"type": "adj", "en": "turquoise",  "de": "türkis",   "indeclinable": True},
    {"type": "adj", "en": "dark",       "de": "dunkel",   "note": "stem drops -e- before endings: dunkle, dunkler etc."},
    {"type": "adj", "en": "light",      "de": "hell",     "note": "used for light-colored as well as bright"},

    # -------------------------------------------------------------------------
    # Pronouns — personal
    # -------------------------------------------------------------------------
    {"type": "pronoun", "subtype": "personal", "en": "I",                  "de": "ich"},
    {"type": "pronoun", "subtype": "personal", "en": "you (informal sg.)", "de": "du"},
    {"type": "pronoun", "subtype": "personal", "en": "he",                 "de": "er"},
    {"type": "pronoun", "subtype": "personal", "en": "she",                "de": "sie", "note": "identical form to 'they' and formal 'Sie' — context disambiguates"},
    {"type": "pronoun", "subtype": "personal", "en": "it",                 "de": "es"},
    {"type": "pronoun", "subtype": "personal", "en": "we",                 "de": "wir"},
    {"type": "pronoun", "subtype": "personal", "en": "you (informal pl.)", "de": "ihr"},
    {"type": "pronoun", "subtype": "personal", "en": "they",               "de": "sie", "note": "identical form to 'she' — context disambiguates"},
    {"type": "pronoun", "subtype": "personal", "en": "you (formal)",       "de": "Sie", "note": "always capitalised; used for both singular and plural formal address"},

    # -------------------------------------------------------------------------
    # Pronouns — possessive (nominative base form, masc. sg.)
    # -------------------------------------------------------------------------
    {"type": "pronoun", "subtype": "possessive", "en": "my",            "de": "mein",  "declines": True, "note": "1st person sg."},
    {"type": "pronoun", "subtype": "possessive", "en": "your (sg.)",    "de": "dein",  "declines": True, "note": "2nd person sg. informal"},
    {"type": "pronoun", "subtype": "possessive", "en": "his",           "de": "sein",  "declines": True, "note": "3rd person sg. masc./neut. — also used for 'its'"},
    {"type": "pronoun", "subtype": "possessive", "en": "her",           "de": "ihr",   "declines": True, "note": "3rd person sg. fem. — identical base to 'their' and formal 'your'"},
    {"type": "pronoun", "subtype": "possessive", "en": "its",           "de": "sein",  "declines": True, "note": "same form as 'his' — German doesn't distinguish"},
    {"type": "pronoun", "subtype": "possessive", "en": "our",           "de": "unser", "declines": True, "note": "1st person pl. — stem unser-, drops -e- before endings in some forms"},
    {"type": "pronoun", "subtype": "possessive", "en": "your (pl.)",    "de": "euer",  "declines": True, "note": "2nd person pl. informal — stem eur-, drops -e- before endings"},
    {"type": "pronoun", "subtype": "possessive", "en": "their",         "de": "ihr",   "declines": True, "note": "3rd person pl. — identical base to 'her' and formal 'your'"},
    {"type": "pronoun", "subtype": "possessive", "en": "your (formal)", "de": "Ihr",   "declines": True, "note": "formal address, sg. and pl. — always capitalised"},
]

GENDER_ARTICLE = {"m": "der", "f": "die", "n": "das"}

# ---------------------------------------------------------------------------
# Prompt builders — one per part of speech
# Returns (prompt_string, correct_answer_string, hint_string)
# ---------------------------------------------------------------------------

def prompt_noun(word):
    article = GENDER_ARTICLE[word["gender"]]
    prompt  = f'Auf Deutsch, bitte: "{word["en"]}" (noun)'
    answer  = word["de"]
    hint    = f'{article} {word["de"]} — plural: {word["plural"]}'
    return prompt, answer, hint

def prompt_verb(word):
    tags = [word["class"]]
    if word.get("separable"):
        tags.append(f'separable, prefix: {word["prefix"]}')
    if word.get("reflexive"):
        tags.append("reflexive")
    prompt  = f'Auf Deutsch, bitte: "{word["en"]}" (verb)'
    answer  = word["de"]
    hint    = f'{word["de"]}  [{", ".join(tags)}]'
    return prompt, answer, hint

def prompt_adj(word):
    prompt  = f'Auf Deutsch, bitte: "{word["en"]}" (adjective)'
    answer  = word["de"]
    tags    = []
    if word.get("indeclinable"):
        tags.append("indeclinable")
    if word.get("note"):
        tags.append(word["note"])
    hint = f'{word["de"]}  [{", ".join(tags)}]' if tags else word["de"]
    return prompt, answer, hint

def prompt_pronoun(word):
    subtype = word["subtype"]
    prompt  = f'Auf Deutsch, bitte: "{word["en"]}" ({subtype} pronoun)'
    answer  = word["de"]
    note    = word.get("note", "")
    if word.get("declines"):
        hint = f'{word["de"]}  [declines like ein-word — {note}]' if note else f'{word["de"]}  [declines like ein-word]'
    else:
        hint = f'{word["de"]}  [{note}]' if note else word["de"]
    return prompt, answer, hint

PROMPT_BUILDERS = {
    "noun":    prompt_noun,
    "verb":    prompt_verb,
    "adj":     prompt_adj,
    "pronoun": prompt_pronoun,
}

# ---------------------------------------------------------------------------
# Quiz loop
# ---------------------------------------------------------------------------

def run_quiz():
    print("\nWillkommen! Drücke Ctrl+C jederzeit zum Beenden.\n")
    correct = total = 0
    interrupted = False

    while True:
        print("Bereiten Sie sich auf 10 Fragen vor.\n")
        for _ in range(10):
            word    = random.choice(WORDS)
            builder = PROMPT_BUILDERS[word["type"]]
            prompt, answer, hint = builder(word)

            print(prompt)
            try:
                response = input("Your answer: ").strip()
            except KeyboardInterrupt:
                interrupted = True
                break

            total += 1
            if response.lower() == answer.lower():
                print("Richtig! :)\n")
                correct += 1
            else:
                print(f"Leider falsch. Richtige Antwort: {hint}\n")

        if interrupted:
            break

        print("Sie haben 10 Fragen beantwortet.")
        again = input("Möchten Sie 10 mehr? [y/n] ").strip().lower()
        if again != "y":
            break

    if total:
        print(f"\nAuf Wiedersehen! Score: {correct}/{total} "
              f"({100 * correct // total}%)")
    else:
        print("\nAuf Wiedersehen!")

if __name__ == "__main__":
    run_quiz()