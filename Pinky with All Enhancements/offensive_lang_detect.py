# This module comprises an algorithm used by Pinky to detect and remove offensive language in messages, such as slurs
# List of offensive phrases to be used in this algorithm should be stored in the file with the path passed to the
# stringCheck function


import re  # Module for working with regular expressions


charSubstitutionMap = {  # Matches some characters with common substitutes - such as "a" and "@" - using regex
    # character classes. Other characters all follow a separate default pattern.
    "a": r"[-*._aA4@]",
    "b": r"[-*._bB86]",
    "e": r"[-*._eE3]",
    "i": r"[-*._iI1]",
    "l": r"[-*._lL1]",
    "o": r"[-*._oO0]",
    "s": r"[-*._sS5]"
}


def phraseToPattern(phrase: str):  # Converts given string to regex; useful in countering attempts to bypass filtering
    escapedPhrase = re.escape(phrase)
    pattern = []

    for i in escapedPhrase:  # For each character, use charSubstitutionMap to determine its regex pattern if applicable
        if (i in charSubstitutionMap):
            charExp: str = charSubstitutionMap[i] + r"+"
        else:  # Otherwise, use a default pattern, checking for dashes, asterisks, dots, and underscores
            charExp: str = r"[-*._{}]".format(i + i.swapcase()) + r"+"
        pattern.append(charExp)

    # Add check for non-alphanumeric characters used as separators, i.e. "b.a.d" or "b_a_d" in place of "bad"
    pattern = r"[^a-zA-Z0-9]*".join(pattern)
    # finalPattern = re.compile(r"(?=[^ ]*[a-zA-Z])" + pattern)

    # Use lookahead to ensure at least one letter is present, and use lookaround to prevent false positives from
    # seemingly offensive phrases that are actually part of benign ones
    # (i.e. "spat" would not trigger a filter for "spatula")
    finalPattern = re.compile(r"(?=[^ ]*[a-zA-Z])(?<![a-zA-Z0-9])" + pattern + r"(?![a-zA-Z0-9])")
    return finalPattern


def fileToReference(filepath: str):  # Converts file to usable form for algorithm by changing each word into regex patterns
    patternReference = set()  # A set is used because appending more items matters but ordering and indexing do not

    with open(filepath, 'r') as file:  # Open specified file and read each phrase line-by-line
        for line in file:
            phrase = line.strip()
            if (not phrase):
                continue
            pattern = phraseToPattern(phrase)  # Convert each phrase into regex pattern
            patternReference.add(pattern)  # Add each pattern to pattern set

    return patternReference


def containsOffensiveLanguage(text: str, patterns: set):
    try:
        for pattern in patterns:  # For each given phrase, check for presence in text
            if (pattern.search(text)):
                return True
        return False
    except:
        return False