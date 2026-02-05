"""
Classic NLP statistics for The Moonstone.
The stuff that wowed em at NeurIPS 2012.
"""

import re
import json
from pathlib import Path
from collections import Counter
import math


def load_text(src_dir: Path) -> str:
    """Load the source text."""
    text_path = src_dir / "pg155.txt"
    if text_path.exists():
        with open(text_path, encoding='utf-8') as f:
            return f.read()
    return ""


def basic_stats(text: str) -> dict:
    """Basic corpus statistics."""
    lines = text.split('\n')
    words = re.findall(r'\b\w+\b', text.lower())
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]

    word_lengths = [len(w) for w in words]
    sentence_lengths = [len(re.findall(r'\b\w+\b', s)) for s in sentences]

    return {
        "lines": len(lines),
        "words": len(words),
        "characters": len(text),
        "sentences": len(sentences),
        "unique_words": len(set(words)),
        "avg_word_length": sum(word_lengths) / len(word_lengths) if word_lengths else 0,
        "avg_sentence_length": sum(sentence_lengths) / len(sentence_lengths) if sentence_lengths else 0,
        "type_token_ratio": len(set(words)) / len(words) if words else 0,
        "hapax_legomena": sum(1 for w, c in Counter(words).items() if c == 1),
        "dis_legomena": sum(1 for w, c in Counter(words).items() if c == 2),
    }


def vocabulary_stats(text: str) -> dict:
    """Vocabulary analysis."""
    words = re.findall(r'\b\w+\b', text.lower())
    word_freq = Counter(words)

    # Top words
    top_50 = word_freq.most_common(50)

    # Zipf's law check (log rank vs log freq)
    zipf_data = []
    for rank, (word, freq) in enumerate(word_freq.most_common(100), 1):
        zipf_data.append({
            "rank": rank,
            "word": word,
            "freq": freq,
            "log_rank": math.log10(rank),
            "log_freq": math.log10(freq) if freq > 0 else 0,
        })

    return {
        "top_50": top_50,
        "zipf_data": zipf_data,
        "vocabulary_size": len(word_freq),
    }


def character_mentions(text: str) -> dict:
    """Character name frequency."""
    # Major character patterns
    characters = {
        "Franklin Blake": r'\b(Franklin|Mr\.?\s*Blake)\b',
        "Rachel Verinder": r'\b(Rachel|Miss\s+Verinder)\b',
        "Gabriel Betteredge": r'\b(Betteredge|Gabriel)\b',
        "Sergeant Cuff": r'\b(Cuff|Sergeant)\b',
        "Rosanna Spearman": r'\b(Rosanna|Spearman)\b',
        "Godfrey Ablewhite": r'\b(Godfrey|Ablewhite)\b',
        "Lady Verinder": r'\b(Lady\s+Verinder|my\s+lady)\b',
        "Ezra Jennings": r'\b(Jennings|Ezra)\b',
        "Miss Clack": r'\b(Clack|Miss\s+Clack)\b',
        "Mr. Bruff": r'\b(Bruff|Mr\.?\s*Bruff)\b',
        "Penelope": r'\b(Penelope)\b',
        "Dr. Candy": r'\b(Candy|Dr\.?\s*Candy)\b',
        "Mr. Murthwaite": r'\b(Murthwaite)\b',
        "Limping Lucy": r'\b(Lucy|Limping\s+Lucy)\b',
    }

    counts = {}
    for char, pattern in characters.items():
        counts[char] = len(re.findall(pattern, text, re.IGNORECASE))

    return dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))


def character_cooccurrence(text: str, window_size: int = 50) -> dict:
    """Character co-occurrence matrix (within N words)."""
    characters = [
        "Franklin", "Rachel", "Betteredge", "Cuff", "Rosanna",
        "Godfrey", "Jennings", "Clack", "Bruff", "Penelope"
    ]

    words = re.findall(r'\b\w+\b', text)
    words_lower = [w.lower() for w in words]

    # Find character positions
    char_positions = {c: [] for c in characters}
    for i, word in enumerate(words):
        for char in characters:
            if char.lower() in word.lower():
                char_positions[char].append(i)

    # Build co-occurrence matrix
    cooccurrence = {c1: {c2: 0 for c2 in characters} for c1 in characters}

    for c1 in characters:
        for pos in char_positions[c1]:
            window_start = max(0, pos - window_size)
            window_end = min(len(words), pos + window_size)

            for c2 in characters:
                if c1 != c2:
                    for pos2 in char_positions[c2]:
                        if window_start <= pos2 <= window_end:
                            cooccurrence[c1][c2] += 1

    return {
        "characters": characters,
        "matrix": cooccurrence,
    }


def ngram_frequencies(text: str, n: int = 2) -> list:
    """Top N-grams."""
    words = re.findall(r'\b\w+\b', text.lower())
    ngrams = [' '.join(words[i:i+n]) for i in range(len(words) - n + 1)]
    return Counter(ngrams).most_common(30)


def narrative_sections(text: str) -> list:
    """Word counts per narrative section."""
    sections = [
        ("Prologue", 118, 354),
        ("First Period: Betteredge", 355, 8488),
        ("Second Period: Miss Clack", 8489, 11500),
        ("Second Period: Bruff", 11500, 13000),
        ("Second Period: Franklin Blake", 13000, 18000),
        ("Second Period: Ezra Jennings", 18000, 19500),
        ("Second Period: Sergeant Cuff", 19500, 20770),
        ("Epilogue", 20771, 21377),
    ]

    lines = text.split('\n')
    results = []

    for name, start, end in sections:
        section_text = '\n'.join(lines[start-1:end])
        words = re.findall(r'\b\w+\b', section_text)
        results.append({
            "section": name,
            "words": len(words),
            "lines": end - start + 1,
        })

    return results


def get_all_stats(src_dir: Path) -> dict:
    """Compute all statistics."""
    text = load_text(src_dir)

    if not text:
        return {"error": "Source text not found"}

    return {
        "basic": basic_stats(text),
        "vocabulary": vocabulary_stats(text),
        "character_mentions": character_mentions(text),
        "cooccurrence": character_cooccurrence(text),
        "bigrams": ngram_frequencies(text, 2),
        "trigrams": ngram_frequencies(text, 3),
        "sections": narrative_sections(text),
    }
