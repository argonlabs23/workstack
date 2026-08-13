---
name: layman
description: Simplify verbose, complex, or jargon-heavy text into clear, unambiguous, layperson-friendly English strictly following the ASD-STE100 (Simplified Technical English) specification rules and controlled vocabulary. Trigger this skill whenever asked to simplify text, convert jargon into layman's terms, rewrite complex documents simply, or apply ASD-STE100 standards.
---

# Layman - simplify verbose, complex, or jargon-heavy text into clear, unambiguous, layperson-friendly English

## 1. Overview & Purpose

The **layman** skill converts verbose, overly complex, academic, legal, or technical text into clear, easy-to-understand English by applying the international standard **ASD-STE100 (Simplified Technical English)**. 

ASD-STE100 eliminates ambiguity, reduces cognitive load, and improves readability for non-experts, non-native English speakers, and general audiences by enforcing strict controlled vocabulary, active voice, simple verb tenses, short sentences, and structured paragraphs.

---

## 2. When to Use

Invoke this skill when the user requests:
- "Simplify this text" or "Explain this in layman's terms"
- "Rewrite this document using ASD-STE100 / Simplified Technical English"
- "De-jargonize this technical, legal, or corporate document"
- "Make this manual / guide / article easy to read for beginners"

---

## 3. Input Requirements

Before executing the simplification process, identify or collect:
1. **Source Text**: The original text, paragraph, file path, or document provided by the user.
2. **Text Mode** (Default: `descriptive`):
   - `procedural`: Step-by-step instructions, standard operating procedures, guides (Max 20 words/sentence).
   - `descriptive`: Explanations, overview, concepts, background information (Max 25 words/sentence).
3. **Audience / Technical Context**: Any specific domain terms (Technical Names) that should be preserved for accuracy (e.g., specific software names, machine model numbers).
4. **Verbosity Mode** (Default: `standard`):
   - `standard`: Output only the simplified text.
   - `verbose` (triggered by `--verbose` or requesting "verbose"): Output simplified text along with Key Rule Adjustments (Section 2) and Audit Metrics Summary (Section 3).

---

## 4. Step-by-Step Execution Workflow

Follow this deterministic sequence of steps:

1. **Analyze Source Text & Classify Mode**:
   - Determine whether the text is **procedural** (instructions) or **descriptive** (explanations).
   - Identify domain-specific nouns (Technical Names) to preserve.

2. **Execute ASD-STE100 Audit Script**:
   - Write the input text to a temporary scratch file or pass it to `./scripts/ste_checker.py`.
   - Run: `python3 ./scripts/ste_checker.py --mode <procedural|descriptive> <input_file>`
   - Review the output report for sentence length violations, unapproved words, passive voice, and paragraph density.

3. **Apply ASD-STE100 Writing Rules**:
   - **Sentence Length**: Break sentences into single-idea statements <= 20 words (procedural) or <= 25 words (descriptive).
   - **Vocabulary Control**: Consult `./references/asd-ste100-dictionary.md`. Replace verbose terms (`utilize` -> `use`, `in order to` -> `to`, `prior to` -> `before`, `commence` -> `start`).
   - **Active Voice**: Convert passive constructions into active voice ("The button is pushed" -> "Push the button").
   - **Condition First**: Move conditional clauses to the beginning ("If X occurs, do Y").
   - **Noun Clusters**: Break long noun chains into maximum 3 consecutive nouns.
   - **Paragraph Limit**: Keep paragraphs to 6 sentences or fewer.

4. **Validate Transformed Text**:
   - Re-run `./scripts/ste_checker.py` on the transformed output to ensure zero rule violations.
   - Cross-check against `./resources/ste_rule_checklist.md`.

5. **Format & Deliver Output**:
   - Present the output using the format defined in `./resources/output_template.md`.

---

## 5. Helper Scripts & Automation

This skill includes an automated Python auditing tool in `./scripts/ste_checker.py`:

```bash
# Analyze descriptive text file
python3 ./scripts/ste_checker.py --mode descriptive path/to/text.txt

# Analyze procedural text file
python3 ./scripts/ste_checker.py --mode procedural path/to/steps.txt

# Output JSON analysis
python3 ./scripts/ste_checker.py --json path/to/text.txt
```

The script checks word counts, sentence lengths, paragraph counts, passive voice patterns, and flags non-approved STE words.

---

## 6. Output Specifications

The final output MUST follow the layout in `./resources/output_template.md`:

- **Default Mode**: Output **only** the simplified text (clean, plain English rewritten to ASD-STE100 standard). Do not include Sections 2 or 3.
- **Verbose Mode** (when user includes `verbose` or `--verbose`): Include:
  1. **Simplified Text**: Clean, plain English rewritten to ASD-STE100 standard.
  2. **Key Rule Adjustments & Substitutions**: A table summarizing major word/phrase substitutions and sentence restructuring.
  3. **ASD-STE100 Audit & Metrics Summary**: Before vs. after statistics (word count reduction percentage, sentence length averages, compliance checks).

---

## 7. Error Handling & Edge Cases

- **Ambiguous Original Text**: If the original text is so vague or poorly written that its intent cannot be determined, state the ambiguity clearly and provide the two most logical simplified interpretations.
- **Strict Domain Terminology**: Do not replace critical legal or specialized industry terms if doing so alters legal compliance or engineering safety. Treat them as approved Technical Names (TNs) as permitted under ASD-STE100 Rule 1.4.
- **Short Texts (< 20 words)**: Skip statistical comparison tables for single short sentences; provide direct simplification and a quick breakdown of changes.
