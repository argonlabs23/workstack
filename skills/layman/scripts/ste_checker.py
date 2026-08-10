#!/usr/bin/env python3
"""
ASD-STE100 Text Checker & Readability Auditor
---------------------------------------------
Analyzes text against key ASD-STE100 rules:
- Sentence length limits (Procedural <= 20 words, Descriptive <= 25 words)
- Paragraph sentence limits (<= 6 sentences)
- Non-approved words and verbose phrase detection with replacement suggestions
- Potential passive voice and long noun cluster detection
"""

import sys
import re
import argparse
import json

# Unapproved words and verbose phrases dictionary
NON_APPROVED_MAP = {
    r"\butilize\b": "use",
    r"\butilizing\b": "using",
    r"\butilization\b": "use",
    r"\bemploy\b": "use",
    r"\bcommence\b": "start",
    r"\binitiate\b": "start",
    r"\bterminate\b": "stop",
    r"\bdiscontinue\b": "stop",
    r"\bperform\b": "do / (specific verb)",
    r"\bperformed\b": "did / (specific verb)",
    r"\bexecute\b": "do / run",
    r"\bobtain\b": "get",
    r"\bacquire\b": "get",
    r"\bdemonstrate\b": "show",
    r"\bdemonstrates\b": "shows",
    r"\bascertain\b": "find / check",
    r"\bfacilitate\b": "help",
    r"\bimplement\b": "do / put in place",
    r"\bdepress\b": "push",
    r"\binspect\b": "check",
    r"\bin order to\b": "to",
    r"\bprior to\b": "before",
    r"\bsubsequent to\b": "after",
    r"\bdue to the fact that\b": "because",
    r"\bat this point in time\b": "now",
    r"\bin the event that\b": "if",
    r"\bwith regard to\b": "about",
    r"\bwith respect to\b": "about",
    r"\bfor the purpose of\b": "for / to",
    r"\bin close proximity to\b": "near",
    r"\bin accordance with\b": "following",
    r"\bapproximately\b": "about",
    r"\bsufficient\b": "enough",
    r"\badditional\b": "more / extra",
    r"\boptimum\b": "best",
    r"\boptimal\b": "best",
}

PASSIVE_VOICE_PATTERN = re.compile(
    r"\b(am|is|are|was|were|be|been|being)\s+([a-z]+ed|[a-z]+en)\b",
    re.IGNORECASE
)

def split_sentences(text):
    # Split text into sentences using simple regex
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s.strip() for s in sentences if s.strip()]

def analyze_text(text, mode="descriptive"):
    max_len = 20 if mode == "procedural" else 25
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

    total_words = 0
    all_sentences = []
    long_sentences = []
    long_paragraphs = []
    found_unapproved = []
    passive_instances = []

    # Non-approved word scans
    for pattern, replacement in NON_APPROVED_MAP.items():
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            found_unapproved.append({
                "matched": match.group(0),
                "suggestion": replacement,
                "position": match.start()
            })

    # Paragraph & Sentence audit
    for p_idx, para in enumerate(paragraphs, 1):
        sents = split_sentences(para)
        if len(sents) > 6:
            long_paragraphs.append({
                "paragraph_index": p_idx,
                "sentence_count": len(sents),
                "limit": 6
            })
        for sent in sents:
            words = re.findall(r'\b\w+\b', sent)
            w_count = len(words)
            total_words += w_count
            all_sentences.append(sent)

            if w_count > max_len:
                long_sentences.append({
                    "sentence": sent,
                    "word_count": w_count,
                    "limit": max_len
                })

            # Passive voice check
            p_matches = PASSIVE_VOICE_PATTERN.findall(sent)
            if p_matches:
                passive_instances.append({
                    "sentence": sent,
                    "match": " ".join(p_matches[0])
                })

    avg_sentence_len = (total_words / len(all_sentences)) if all_sentences else 0

    return {
        "mode": mode,
        "total_words": total_words,
        "total_sentences": len(all_sentences),
        "total_paragraphs": len(paragraphs),
        "avg_sentence_length": round(avg_sentence_len, 2),
        "long_sentences": long_sentences,
        "long_paragraphs": long_paragraphs,
        "unapproved_terms_found": found_unapproved,
        "passive_voice_instances": passive_instances
    }

def print_report(result):
    print("==================================================")
    print("        ASD-STE100 READABILITY AUDIT REPORT       ")
    print("==================================================")
    print(f"Mode:                   {result['mode'].upper()}")
    print(f"Total Words:            {result['total_words']}")
    print(f"Total Sentences:        {result['total_sentences']}")
    print(f"Total Paragraphs:       {result['total_paragraphs']}")
    print(f"Avg Sentence Length:    {result['avg_sentence_length']} words")
    print("--------------------------------------------------")

    if result['long_sentences']:
        print(f"\n⚠️ LONG SENTENCES EXCEEDING LIMIT ({20 if result['mode'] == 'procedural' else 25} words):")
        for idx, item in enumerate(result['long_sentences'], 1):
            print(f"  {idx}. [{item['word_count']} words]: \"{item['sentence']}\"")
    else:
        print("\n✅ All sentences meet length limits.")

    if result['long_paragraphs']:
        print("\n⚠️ PARAGRAPHS EXCEEDING 6 SENTENCES:")
        for item in result['long_paragraphs']:
            print(f"  - Paragraph {item['paragraph_index']} has {item['sentence_count']} sentences.")
    else:
        print("✅ Paragraph sentence limits respected.")

    if result['unapproved_terms_found']:
        print("\n⚠️ UNAPPROVED / VERBOSE TERMS DETECTED:")
        seen = set()
        for item in result['unapproved_terms_found']:
            key = item['matched'].lower()
            if key not in seen:
                seen.add(key)
                print(f"  - Found '{item['matched']}' -> Suggest: '{item['suggestion']}'")
    else:
        print("✅ No common unapproved verbose terms found.")

    if result['passive_voice_instances']:
        print("\n⚠️ POTENTIAL PASSIVE VOICE (STE prefers Active Voice):")
        for item in result['passive_voice_instances'][:5]:
            print(f"  - Phrase: '{item['match']}' in sentence: \"{item['sentence']}\"")
    else:
        print("✅ No obvious passive voice detected.")
    print("==================================================\n")

def main():
    parser = argparse.ArgumentParser(description="ASD-STE100 Text Auditor")
    parser.add_argument("file", nargs="?", type=str, help="Path to text file to analyze")
    parser.add_argument("--mode", choices=["procedural", "descriptive"], default="descriptive", help="Text mode (default: descriptive)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON analysis")

    args = parser.parse_args()

    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        text = sys.stdin.read()

    if not text.strip():
        print("Error: No text provided.", file=sys.stderr)
        sys.exit(1)

    result = analyze_text(text, mode=args.mode)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_report(result)

if __name__ == "__main__":
    main()
