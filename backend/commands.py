# ============================================================
# NOVA — commands.py  (V2)
# This file's only job: take the raw text that voice.py heard,
# and turn it into a single, consistent Python dictionary that
# main.py can act on:
#
#   {
#       "intent": "...",   # WHAT Nova should do
#       "target": "...",   # WHAT the action applies to (or None)
#       "query": "...",    # free-form text, e.g. a search query (or None)
#   }
#
# Every possible command — known or not — returns this same
# shape. main.py never has to guess what TYPE of value it got
# back; it just reads result["intent"] and goes from there.
# ============================================================

import string


def _result(intent, target=None, query=None):
    """
    Small helper that builds a result dictionary in the exact
    shape every command should return. Using this everywhere
    means we can't accidentally misspell a key name or forget
    one of the three fields.
    """
    return {
        "intent": intent,
        "target": target,
        "query": query,
    }


# ------------------------------------------------------------
# Applications Nova can OPEN. Each target name maps to the set
# of words that should trigger it.
#
# To teach Nova a new application later, just add one more
# line here.
# ------------------------------------------------------------
APPLICATION_KEYWORDS = {
    "chrome": {"chrome"},
    "brave": {"brave"},
    "notepad": {"notepad"},
    "calculator": {"calculator", "calc"},
    "file_explorer": {"explorer", "files"},
}

# ------------------------------------------------------------
# Applications Nova can CLOSE. This is a smaller list than
# APPLICATION_KEYWORDS above — only apps we know how to safely
# close are included (matching Nova's V1.5 behavior).
#
# Only the word "close" triggers this — not "quit" or "stop",
# since those already mean "exit Nova" (see SIMPLE_INTENTS
# below). This keeps "quit chrome" and "quit Nova" from ever
# being confused with each other.
# ------------------------------------------------------------
CLOSE_APPLICATION_KEYWORDS = {
    "chrome": {"chrome"},
    "brave": {"brave"},
    "notepad": {"notepad"},
    "calculator": {"calculator", "calc"},
}

# ------------------------------------------------------------
# Windows folders Nova can open.
# ------------------------------------------------------------
FOLDER_KEYWORDS = {
    "downloads": {"downloads"},
    "documents": {"documents"},
    "desktop": {"desktop"},
}

# ------------------------------------------------------------
# Websites Nova can open directly (not search on) — e.g.
# "open YouTube" just opens youtube.com.
# ------------------------------------------------------------
WEBSITE_KEYWORDS = {
    "youtube": {"youtube"},
    "google": {"google"},
    "github": {"github"},
}

# ------------------------------------------------------------
# Commands with no target and no query — Nova just does the
# one thing. Each intent name maps to the words that trigger it.
# ------------------------------------------------------------
SIMPLE_INTENTS = {
    "exit": {"exit", "quit", "stop", "goodbye", "shutdown"},
    "take_screenshot": {"screenshot"},
    "get_time": {"time"},
    "get_battery": {"battery"},
    "lock_computer": {"lock"},
}

# ------------------------------------------------------------
# Phrasings for "search Google/YouTube for X". Each list holds
# phrases that come BEFORE the query, checked with
# str.startswith(). "search for X on <site>" is handled
# separately below, since that phrase wraps AROUND the query
# instead of just coming before it.
# ------------------------------------------------------------
GOOGLE_SEARCH_PREFIXES = ["search google for ", "google search "]
YOUTUBE_SEARCH_PREFIXES = ["search youtube for ", "youtube search "]
BRAVE_SEARCH_PREFIXES = ["search brave for ", "brave search ","searching brave for "]


def _extract_query_with_prefixes(cleaned_text, prefixes):
    """
    Checks if cleaned_text starts with one of the given prefixes,
    and if so, returns everything AFTER that prefix (the query).
    Returns None if none of the prefixes match.
    """
    for prefix in prefixes:
        if cleaned_text.startswith(prefix):
            return cleaned_text[len(prefix):].strip()
    return None


def _extract_query_wrapped(cleaned_text, prefix, suffix):
    """
    Checks if cleaned_text starts with `prefix` AND ends with
    `suffix`, and if so, returns whatever is in between (the
    query). Used for phrasings like "search for X on google".
    Returns None if the text doesn't match that shape.
    """
    if cleaned_text.startswith(prefix) and cleaned_text.endswith(suffix):
        start = len(prefix)
        end = len(cleaned_text) - len(suffix)
        return cleaned_text[start:end].strip()
    return None

def _extract_query_before_site(cleaned_text, prefixes, site):
    for prefix in prefixes:
        if cleaned_text.startswith(prefix) and cleaned_text.endswith(f" on {site}"):
            query = cleaned_text[len(prefix):-len(f" on {site}")].strip()

            if query:
                return query

    return None


def _extract_search_query(cleaned_text, prefixes, wrapped_suffix):
    """
    Tries both search phrasings (prefix-based, then wrapped)
    and returns the query text if either matches — otherwise
    returns None.
    """
    query = _extract_query_with_prefixes(cleaned_text, prefixes)
    if query:
        return query
    return _extract_query_wrapped(cleaned_text, "search for ", wrapped_suffix)


def _detect_volume_intent(spoken_words):
    """
    Volume commands need TWO words together ("increase" AND
    "volume"), not just one — so they can't use the simple
    OR-style matching the other keyword dictionaries use. This
    function checks for that combination directly.
    Returns an intent name, or None if it's not a volume command.
    """
    if "volume" not in spoken_words:
        return None

    if "mute" in spoken_words:
        return "mute_volume"
    if spoken_words & {"increase", "up", "raise"}:
        return "increase_volume"
    if spoken_words & {"decrease", "down", "lower"}:
        return "decrease_volume"

    return None


def clean_command(text):
    """
    Takes raw recognized speech (or typed text) and returns a
    dictionary in the shape:

        {"intent": "...", "target": "...", "query": "..."}

    Every branch below returns through the _result() helper, so
    the shape is always exactly the same no matter which kind
    of command was spoken.

    Examples:
        "Nova, open Brave"
            -> {"intent": "open_application", "target": "brave", "query": None}
        "Nova, search Google for Python tutorials"
            -> {"intent": "search_google", "target": "google", "query": "python tutorials"}
        "Nova, close Chrome"
            -> {"intent": "close_application", "target": "chrome", "query": None}
        "blah blah unrecognized"
            -> {"intent": "unknown", "target": None, "query": "blah blah unrecognized"}
    """

    # Step 1: Make everything lowercase so "Nova", "NOVA", and
    # "nova" are all treated the same way.
    cleaned = text.lower()

    # Step 2: Remove punctuation (commas, periods, etc).
    cleaned = cleaned.translate(str.maketrans("", "", string.punctuation))

    # Step 3: Split the text into individual words.
    words = cleaned.split()

    # Step 4: Remove the wake word "nova" if it's the first word.
    if words and words[0] == "nova":
        words = words[1:]

    # Step 5: Join the remaining words back into one string —
    # the fully cleaned text, before we try to match a command.
    cleaned_text = " ".join(words)
    spoken_words = set(words)

    # Step 6: Check for a Google search command FIRST, since a
    # phrase like "search google for cats" contains the word
    # "google" and would otherwise be wrongly matched later as
    # "open the Google website".
    query = _extract_search_query(cleaned_text, GOOGLE_SEARCH_PREFIXES, " on google")
    if query:
        return _result("search_google", target="google", query=query)

    # Step 7: Same idea for YouTube searches, checked before the
    # plain "open youtube" website match for the same reason.
    query = _extract_search_query(cleaned_text, YOUTUBE_SEARCH_PREFIXES, " on youtube")
    if query:
        return _result("search_youtube", target="youtube", query=query)

    query = _extract_search_query(cleaned_text, BRAVE_SEARCH_PREFIXES, " on brave")
    if query:
     return _result("search_brave", target="brave", query=query)

    query = _extract_query_before_site(cleaned_text, ["search "], "brave")
    if query:
     return _result("search_brave", target="brave", query=query)

    # Step 8: Check for a volume command, since it needs the
    # two-word AND-style check from _detect_volume_intent().
    volume_intent = _detect_volume_intent(spoken_words)
    if volume_intent:
        return _result(volume_intent)

    # Step 9: Check for a "close <app>" command. This has to
    # come before the "open application" matching in Step 11,
    # because "close chrome" also contains the word "chrome" and
    # would otherwise be mistaken for "open chrome".
    if "close" in spoken_words:
        for app_name, keywords in CLOSE_APPLICATION_KEYWORDS.items():
            if spoken_words & keywords:
                return _result("close_application", target=app_name)
        # The user said "close" but didn't name an app Nova
        # knows how to close — treat it as unrecognized rather
        # than guessing and accidentally opening something.
        return _result("unknown", query=cleaned_text)

    # Step 10: Check Nova's simple, target-less commands (exit,
    # screenshot, time, battery, lock).
    for intent, keywords in SIMPLE_INTENTS.items():
        if spoken_words & keywords:
            return _result(intent)

    # Step 11: Check for "open <application>".
    for app_name, keywords in APPLICATION_KEYWORDS.items():
        if spoken_words & keywords:
            return _result("open_application", target=app_name)

    # Step 12: Check for "open <folder>".
    for folder_name, keywords in FOLDER_KEYWORDS.items():
        if spoken_words & keywords:
            return _result("open_folder", target=folder_name)

    # Step 13: Check for "open <website>".
    for site_name, keywords in WEBSITE_KEYWORDS.items():
        if spoken_words & keywords:
            return _result("open_website", target=site_name)

    # Step 14: Nothing matched anything Nova knows — return the
    # cleaned text as the query, so main.py can report it as
    # "I don't know that command yet."
    return _result("unknown", query=cleaned_text)