---
name: ideation
description: Captures raw, unfiltered ideas and friction observations into a standardized structured format and appends them to ideas.md or a user-specified file. Supports the 'add' command. Trigger when asked to add an idea, run 'ideation add', or record friction observations.
---

# 🧠 Ideation & Friction Capture

## 1. Overview & Purpose
The **Ideation** skill captures raw, unfiltered ideas, unstructured thoughts, or observations of friction and transforms them into a clean, standardized taxonomy format. 

Its primary command is `add`, which processes raw user inputs, automatically infers and populates missing metadata fields (Industry, Pain Point, Target Audience, Rating, Title, Date) according to an internal taxonomy, and appends the structured entry to `ideas.md` (or a user-specified target file).

---

## 2. When to Use
Invoke this skill when:
- The user issues a command like `ideation add <raw text or idea>` or `/ideation add ...`.
- The user provides an unfiltered idea, thought, or observation and asks to add, record, capture, or log it to an ideas file.
- The user requests structuring an observation following the ideation schema/template.

---

## 3. Input Requirements
1. **Command**: `add` (explicit or implied by the request to record an idea).
2. **Raw Idea / Observation Input**: The unfiltered text, voice note transcript, or bullet points provided by the user.
3. **Target File (Optional)**: Defaults to `ideas.md` in the current working directory unless the user specifies a custom destination file (e.g. `Workstak_PUB/workflows/ideation/ideas.md`).

---

## 4. Step-by-Step Execution Workflow

Follow this deterministic workflow when executing `ideation add`:

### Step 1: Identify Target Output File
- Check if the user specified a custom file path for the ideas repository.
- If specified, target that file path.
- If not specified, default to `ideas.md` in the workspace root or current directory.

### Step 2: Parse and Infer Metadata Fields
Examine the user's raw input and extract or infer the following fields using the reference taxonomy in `./resources/idea_template.md`:

1. **Title (`### [Brief, Punchy Title of Observation]`)**:
   - Synthesize a short, punchy headline summarizing the core idea or friction (e.g., `### 📝 The "Print and Pen" ERP Workaround`).
2. **Date (`- **Date:** YYYY-MM-DD`)**:
   - Use the current date (in `YYYY-MM-DD` format) unless a specific date was mentioned in the user's input.
3. **Industry (`- **Industry:** #Tag`)**:
   - Infer the relevant industry tag(s) (e.g. `#Logistics`, `#FinTech`, `#B2BSaaS`, `#HealthTech`, `#ECommerce`, `#Construction`, `#LegalTech`). Format as `#CamelCaseTag`.
4. **Pain Point (`- **Pain Point:** #Tag`)**:
   - Infer the core nature of friction (e.g. `#TooManual`, `#Fragmented`, `#TooExpensive`, `#HighLatency`, `#Opaque`, `#ComplianceHeavy`, `#HighChurn`).
5. **Target Audience (`- **Target Audience:** #Tag`)**:
   - Infer who experiences the pain (e.g. `#OperationsManagers`, `#EngineeringManagers`, `#Freelancers`, `#SoloFounders`, `#AgencyOwners`, `#EnterpriseSales`).
6. **Initial Rating (`- **Initial Rating (1-5):** ⭐⭐⭐`)**:
   - Evaluate friction severity on a 1–5 scale based on the taxonomy criteria (1=vitamin, 3=solid problem, 5=hair-on-fire) and render as star emojis (e.g., ⭐⭐⭐⭐).
7. **The Breadcrumb (`- **The Breadcrumb (Observation):**`)**:
   - **STRICT RULE**: If observation details/text were provided in the user input, format as a blockquote (`> *[User observation text]*`).
   - **STRICT RULE**: If no observation/breadcrumb content was provided in the user's input, **LEAVE THIS FIELD EMPTY** (e.g., `- **The Breadcrumb (Observation):**` followed by an empty line or `> ` with no content). Do NOT infer or hallucinate breadcrumb observation text if none was provided.

### Step 3: Format Entry According to Reference Spec
Format the output entry strictly matching the template in [idea_example.md](./resources/idea_example.md):

```markdown
### 📝 [Brief, Punchy Title of Observation]
- **Date:** YYYY-MM-DD
- **Industry:** `#Tag`
- **Pain Point:** `#Tag`
- **Target Audience:** `#Tag`
- **Initial Rating (1-5):** ⭐⭐⭐⭐
- **The Breadcrumb (Observation):** 
  > *[User observation text, or left empty if no input provided]*

---
```

### Step 4: Append Entry to Target File
- Read the target file (`ideas.md` or specified file) if it exists.
- Append the formatted entry to the end of the file, ensuring proper newline spacing and separating entries with `---`.
- If the target file does not exist yet, create it and write the entry (with optional header `# 🧠 Idea & Friction Repository`).

---

## 5. Helper References & Templates
- Standard Ideation Template & Taxonomy: `./resources/idea_template.md`
- Reference Formatted Example: `./resources/idea_example.md`

---

## 6. Output Specifications

When executing `ideation add`, output a confirmation summary to the user indicating:
1. The title and inferred tags of the newly added idea.
2. The target file where the entry was appended (e.g., `ideas.md`).
3. A preview of the appended entry block.

---

## 7. Error Handling & Edge Cases

| Issue / Edge Case | Action / Fallback |
| :--- | :--- |
| **No observation text in input** | Fill in Title, Date, Industry, Pain Point, Target Audience, and Rating based on any brief title/topic provided, but **leave "The Breadcrumb" field empty**. |
| **Target file missing** | Automatically create `ideas.md` (or the specified target file path) and append the entry. |
| **Ambiguous industry/pain point** | Infer the closest matching `#CamelCaseTag` from `./resources/idea_template.md` or create a fitting domain tag using `#CamelCase`. |
| **Multiple ideas in single input** | Split into multiple distinct entries, formatting and appending each individually to the target file. |
