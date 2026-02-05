"""
Character Voice Fingerprints for The Moonstone

Quantitative stylistic features for each narrator to enable:
- Voice consistency checking during generation
- Computational distinction between narrators
- Basis for TONE.md claims

Output: JSON with feature vectors per narrator
"""

import json
import re
from pathlib import Path
from collections import Counter

# Approximate line ranges for each narrator section in pg155.txt
NARRATOR_SECTIONS = {
    "prologue_cousin": (118, 354),
    "betteredge": (355, 8488),
    "miss_clack": (8489, 11500),  # Approximate
    "bruff": (11500, 13000),      # Approximate
    "franklin_blake": (13000, 18000),  # Combined narratives
    "ezra_jennings": (18000, 19500),   # Journal sections
    "sergeant_cuff": (19500, 20770),   # Final report
    "murthwaite": (20771, 21377),      # Epilogue
}

# Lexical markers specific to each narrator
LEXICAL_MARKERS = {
    "betteredge": {
        "robinson_crusoe": ["Robinson Crusoe", "Doondee", "Doondee Sultan", "Doomed"],
        "class_markers": ["my lady", "my young lady", "young mistress", "young master", "gentlefolk"],
        "superstition": ["Providence", "fate", "Doondee", "oracle", "omen"],
        "direct_address": ["you will ask", "you will say", "you will observe", "permit me"],
        "digression": ["here I must", "I beg to", "I may mention", "let me say"],
        "hedging": ["begging your pardon", "if I may make so bold", "saving your presence"],
    },
    "miss_clack": {
        "religious": ["Christian", "soul", "tract", "salvation", "sin", "pious", "godless", "Satan"],
        "tract_titles": ["tract", "pamphlet", "work"],  # She distributes these constantly
        "admiration": ["dear", "admirable", "excellent", "precious", "blessed"],
        "martyrdom": ["suffer", "trial", "burden", "duty", "cross"],
        "godfrey_worship": ["Mr. Godfrey", "Godfrey Ablewhite"],  # Her obsession
    },
    "bruff": {
        "legal": ["client", "trust", "instrument", "settlement", "bequest", "counsel"],
        "formal": ["I am instructed", "it appears", "I was informed", "the facts"],
        "professional": ["professionally", "in my opinion", "as a lawyer"],
    },
    "franklin_blake": {
        "self_analysis": ["I asked myself", "it struck me", "I couldn't help", "I felt"],
        "continental": ["French", "German", "Italy", "abroad", "foreign"],
        "investigation": ["evidence", "facts", "discovered", "inquiry", "investigation"],
        "emotional": ["miserable", "wretched", "hope", "despair"],
    },
    "ezra_jennings": {
        "medical": ["laudanum", "opium", "dose", "fever", "brain", "physiological", "experiment"],
        "melancholy": ["suffer", "die", "death", "lonely", "outcast"],
        "journal": ["today", "this morning", "tonight", "I record"],
        "compassion": ["poor", "friend", "sympathy"],
    },
    "sergeant_cuff": {
        "detective": ["evidence", "investigation", "inquiry", "suspect", "case"],
        "roses": ["rose", "roses", "garden", "bloom", "cultivation"],
        "professional": ["in my experience", "the facts", "I have no doubt", "my opinion"],
        "report": ["I beg to report", "I submit", "the result"],
    },
}

# Function words to analyze (high-frequency, style-indicating)
FUNCTION_WORDS = [
    "the", "a", "an", "and", "but", "or", "if", "then", "so",
    "i", "you", "he", "she", "it", "we", "they", "my", "your", "his", "her",
    "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did",
    "will", "would", "could", "should", "may", "might", "must",
    "not", "no", "yes", "very", "quite", "rather", "indeed",
    "here", "there", "now", "then", "when", "where", "how", "why",
]


def extract_text_section(full_text: str, start_line: int, end_line: int) -> str:
    """Extract a section of text by line numbers."""
    lines = full_text.split('\n')
    return '\n'.join(lines[start_line-1:end_line])


def compute_basic_stats(text: str) -> dict:
    """Compute basic text statistics."""
    # Clean text
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]

    words = re.findall(r'\b\w+\b', text.lower())
    word_count = len(words)

    if not sentences or not words:
        return {}

    # Sentence lengths
    sentence_lengths = [len(re.findall(r'\b\w+\b', s)) for s in sentences]

    # Word lengths
    word_lengths = [len(w) for w in words]

    # Unique words
    unique_words = set(words)

    stats = {
        "word_count": word_count,
        "sentence_count": len(sentences),
        "avg_sentence_length": sum(sentence_lengths) / len(sentence_lengths),
        "max_sentence_length": max(sentence_lengths),
        "min_sentence_length": min(sentence_lengths),
        "sentence_length_std": (sum((l - sum(sentence_lengths)/len(sentence_lengths))**2 for l in sentence_lengths) / len(sentence_lengths)) ** 0.5,
        "avg_word_length": sum(word_lengths) / len(word_lengths),
        "vocabulary_size": len(unique_words),
        "type_token_ratio": len(unique_words) / word_count if word_count else 0,
    }

    return stats


def compute_function_word_profile(text: str) -> dict:
    """Compute frequency profile of function words."""
    words = re.findall(r'\b\w+\b', text.lower())
    word_count = len(words)
    if not word_count:
        return {}

    word_freq = Counter(words)
    profile = {}
    for fw in FUNCTION_WORDS:
        profile[fw] = word_freq.get(fw, 0) / word_count * 1000  # Per 1000 words

    return profile


def compute_lexical_markers(text: str, narrator: str) -> dict:
    """Count occurrences of narrator-specific lexical markers."""
    markers = LEXICAL_MARKERS.get(narrator, {})
    results = {}

    text_lower = text.lower()
    word_count = len(re.findall(r'\b\w+\b', text))

    for category, terms in markers.items():
        count = 0
        for term in terms:
            count += len(re.findall(re.escape(term.lower()), text_lower))
        results[category] = count
        results[f"{category}_per_1k"] = count / word_count * 1000 if word_count else 0

    return results


def compute_punctuation_profile(text: str) -> dict:
    """Analyze punctuation usage patterns."""
    word_count = len(re.findall(r'\b\w+\b', text))
    if not word_count:
        return {}

    return {
        "exclamation_per_1k": text.count('!') / word_count * 1000,
        "question_per_1k": text.count('?') / word_count * 1000,
        "semicolon_per_1k": text.count(';') / word_count * 1000,
        "colon_per_1k": text.count(':') / word_count * 1000,
        "dash_per_1k": (text.count('—') + text.count('--')) / word_count * 1000,
        "parenthetical_per_1k": text.count('(') / word_count * 1000,
    }


def compute_discourse_markers(text: str) -> dict:
    """Analyze discourse/digression patterns."""
    word_count = len(re.findall(r'\b\w+\b', text))
    if not word_count:
        return {}

    text_lower = text.lower()

    # Direct address to reader
    direct_address = len(re.findall(r'\byou\s+will\b', text_lower))
    direct_address += len(re.findall(r'\bthe\s+reader\b', text_lower))

    # Digressions (parenthetical asides)
    parentheticals = text.count('(')

    # Self-reference
    first_person = len(re.findall(r'\bI\b', text))

    # Hedging expressions
    hedges = len(re.findall(r'\bperhaps\b|\bpossibly\b|\bit\s+seems\b|\bI\s+think\b|\bI\s+believe\b', text_lower))

    return {
        "direct_address_per_1k": direct_address / word_count * 1000,
        "parentheticals_per_1k": parentheticals / word_count * 1000,
        "first_person_per_1k": first_person / word_count * 1000,
        "hedging_per_1k": hedges / word_count * 1000,
    }


def build_fingerprint(text: str, narrator: str) -> dict:
    """Build complete voice fingerprint for a narrator."""
    fingerprint = {
        "narrator": narrator,
        "basic_stats": compute_basic_stats(text),
        "function_words": compute_function_word_profile(text),
        "lexical_markers": compute_lexical_markers(text, narrator),
        "punctuation": compute_punctuation_profile(text),
        "discourse": compute_discourse_markers(text),
    }
    return fingerprint


def build_all_fingerprints(source_path: Path) -> dict:
    """Build fingerprints for all narrators."""
    # Read source text
    with open(source_path, 'r', encoding='utf-8') as f:
        full_text = f.read()

    fingerprints = {}
    for narrator, (start, end) in NARRATOR_SECTIONS.items():
        text = extract_text_section(full_text, start, end)
        fingerprints[narrator] = build_fingerprint(text, narrator)

    return fingerprints


def compute_distinctive_features(fingerprints: dict) -> dict:
    """Identify features that most distinguish each narrator."""
    narrators = list(fingerprints.keys())
    distinctive = {}

    for narrator in narrators:
        fp = fingerprints[narrator]
        narrator_distinctive = []

        # Check lexical markers
        if "lexical_markers" in fp:
            for marker, value in fp["lexical_markers"].items():
                if "_per_1k" in marker and value > 1.0:  # At least 1 per 1000 words
                    narrator_distinctive.append({
                        "feature": marker,
                        "value": value,
                        "type": "lexical"
                    })

        # Check punctuation distinctiveness
        if "punctuation" in fp:
            for punc, value in fp["punctuation"].items():
                # Compare to average
                avg = sum(fingerprints[n].get("punctuation", {}).get(punc, 0)
                         for n in narrators) / len(narrators)
                if value > avg * 1.5:  # 50% above average
                    narrator_distinctive.append({
                        "feature": punc,
                        "value": value,
                        "avg": avg,
                        "type": "punctuation"
                    })

        distinctive[narrator] = narrator_distinctive

    return distinctive


def export_fingerprints(output_dir: Path, source_path: Path):
    """Export all fingerprints."""
    output_dir.mkdir(parents=True, exist_ok=True)

    if not source_path.exists():
        print(f"Warning: Source file not found at {source_path}")
        print("Generating placeholder fingerprints based on known characteristics...")

        # Generate placeholder fingerprints based on our TONE.md analysis
        fingerprints = {
            "betteredge": {
                "narrator": "betteredge",
                "characteristics": {
                    "avg_sentence_length": "long",
                    "digression_rate": "high",
                    "robinson_crusoe_references": "frequent",
                    "class_markers": "high",
                    "first_person": "high",
                    "direct_address": "moderate",
                },
                "distinctive_markers": [
                    "Robinson Crusoe references",
                    "Class-conscious language (my lady, young master)",
                    "Digressions and parentheticals",
                    "Providence/fate attributions",
                ]
            },
            "miss_clack": {
                "narrator": "miss_clack",
                "characteristics": {
                    "religious_vocabulary": "very high",
                    "exclamation_rate": "high",
                    "godfrey_mentions": "frequent",
                    "self_righteousness": "pervasive",
                },
                "distinctive_markers": [
                    "Religious tract vocabulary",
                    "Godfrey Ablewhite admiration",
                    "Martyrdom language",
                    "Exclamation marks",
                ]
            },
            "bruff": {
                "narrator": "bruff",
                "characteristics": {
                    "avg_sentence_length": "short",
                    "legal_vocabulary": "high",
                    "emotional_language": "low",
                    "hedging": "low",
                },
                "distinctive_markers": [
                    "Legal terminology",
                    "Short declarative sentences",
                    "Professional distance",
                ]
            },
            "franklin_blake": {
                "narrator": "franklin_blake",
                "characteristics": {
                    "self_analysis": "high",
                    "emotional_vocabulary": "moderate",
                    "continental_references": "present",
                    "question_rate": "moderate",
                },
                "distinctive_markers": [
                    "Self-questioning",
                    "Continental/foreign references",
                    "Investigation vocabulary",
                    "Emotional vulnerability",
                ]
            },
            "ezra_jennings": {
                "narrator": "ezra_jennings",
                "characteristics": {
                    "medical_vocabulary": "very high",
                    "melancholy_tone": "pervasive",
                    "journal_format": "yes",
                    "compassion_markers": "high",
                },
                "distinctive_markers": [
                    "Medical/scientific vocabulary",
                    "Journal date stamps",
                    "Melancholic self-awareness",
                    "Opium/laudanum references",
                ]
            },
            "sergeant_cuff": {
                "narrator": "sergeant_cuff",
                "characteristics": {
                    "detective_vocabulary": "high",
                    "rose_references": "present",
                    "report_format": "yes",
                    "emotional_language": "very low",
                },
                "distinctive_markers": [
                    "Rose-growing references",
                    "Detective report format",
                    "Professional detachment",
                    "Evidence-focused vocabulary",
                ]
            },
        }
    else:
        fingerprints = build_all_fingerprints(source_path)

    # Export fingerprints
    with open(output_dir / "voice_fingerprints.json", "w") as f:
        json.dump(fingerprints, f, indent=2)

    # Compute and export distinctive features
    if source_path.exists():
        distinctive = compute_distinctive_features(fingerprints)
        with open(output_dir / "distinctive_features.json", "w") as f:
            json.dump(distinctive, f, indent=2)

    print(f"Voice Fingerprints: {len(fingerprints)} narrators analyzed")

    return fingerprints


if __name__ == "__main__":
    output_dir = Path(__file__).parent.parent / "graphs"
    source_path = Path(__file__).parent.parent / "src" / "pg155.txt"
    export_fingerprints(output_dir, source_path)
    print(f"\nVoice fingerprints exported to {output_dir}")
