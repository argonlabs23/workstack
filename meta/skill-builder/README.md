# Skill Builder Meta Prompt Guide

A guide on using the **Skill Builder Meta Prompt** (`skill-builder.md`) to quickly design, structure, and generate standardized, cross-model compatible Agent Skills adhering to the [`agentskills.io`](https://agentskills.io) open specification.

---

## 📌 Overview

The **Skill Builder Meta Prompt** transforms any capable LLM (such as Claude, ChatGPT etc.) into an expert AI Systems Architect. By using this system prompt, you can feed in raw workflow ideas, documentation, or task descriptions, and receive a fully formatted, production-ready Agent Skill directory package complete with `SKILL.md`, scripts, templates, and reference docs.

---

## 🚀 How to Use the Meta Prompt

### Step 1: Copy the Meta System Prompt
Open [`skill-builder.md`](./skill-builder.md) and copy the system prompt contained within the markdown code block.

### Step 2: Set Up Your LLM or Workspace Agent
Pass the system prompt into your LLM or agent environment:
- **Workspace Agent Customization (`.agent` / `.agents`)**: Place `skill-builder` inside your project's `.agent/skills/` directory (e.g., `.agent/skills/skill-builder/SKILL.md`) or global agent configuration directory so AI coding agents automatically discover and use it.
- **System Prompt / Custom Instructions**: Paste the copied meta prompt as the system prompt or custom instructions in tools like ChatGPT, Claude, or Gemini.
- **Direct Chat**: Alternatively, paste it at the beginning of a fresh conversation session.

### Step 3: Provide Your Task & Context Input
Replace the `[USER TASK & CONTEXT INPUT]` placeholder in the prompt (or append your prompt) with:
1. **Skill Goal / Purpose**: What task should the agent automate?
2. **Context & Rules**: Specific workflows, coding standards, APIs, or formatting constraints.
3. **Helper Tools**: Any scripts, CLI tools, or templates you want included.

---

## 💡 Example Use Cases

### Use Case 1: Automating Code Review & Refactoring

**Input to LLM:**
> **[USER TASK & CONTEXT INPUT]**  
> I need an Agent Skill named `pr-reviewer` that performs structured GitHub PR code reviews.  
> - **Inputs**: PR diff or PR URL.  
> - **Steps**: Analyze security flaws, check against TypeScript best practices, verify test coverage, and output a structured markdown review summary with severity levels (Critical, Major, Minor).  
> - Include a helper script in `./scripts/` to calculate line diff stats using Python.

**Expected Generated Output Package:**
```
pr-reviewer/
├── SKILL.md                 # Includes YAML frontmatter, execution workflow, and output template
└── scripts/
    └── diff_stats.py        # Python script for line change breakdown
```

---

### Use Case 2: Database Migration & Schema Generator

**Input to LLM:**
> **[USER TASK & CONTEXT INPUT]**  
> Create a skill named `supabase-migration-builder` that generates raw SQL migrations for Supabase projects.  
> - **Inputs**: Entity models or feature requirements in text.  
> - **Steps**: Generate RLS policies, index definitions, and migration SQL files with rollback instructions.  
> - Add a SQL template in `./resources/migration_template.sql`.

**Expected Generated Output Package:**
```
supabase-migration-builder/
├── SKILL.md
└── resources/
    └── migration_template.sql
```

---

### Use Case 3: Converting Internal API Docs into an Agent Skill

**Input to LLM:**
> **[USER TASK & CONTEXT INPUT]**  
> Build a skill called `stripe-refund-handler` based on Stripe's refund API documentation.  
> - **Trigger**: When a user asks to issue, check, or audit Stripe refunds.  
> - **References**: Include API rate limits and status definitions in `./references/api_specs.md`.  
> - **Scripts**: Include a curl helper script in `./scripts/issue_refund.sh`.

**Expected Generated Output Package:**
```
stripe-refund-handler/
├── SKILL.md
├── references/
│   └── api_specs.md
└── scripts/
    └── issue_refund.sh
```

---

## 🛠 Best Practices for Skill Generation

1. **Be Explicit About Triggers**: Make sure the `description` field in the frontmatter contains clear intent keywords so LLMs know exactly when to invoke the skill.
2. **Modular Helper Scripts**: Keep scripts in `./scripts/` light and reliant on standard libraries to maintain cross-platform compatibility.
3. **Use Relative Paths**: Ensure all references within `SKILL.md` point to `./scripts/`, `./resources/`, or `./references/` using relative paths.
4. **Iterative Polish**: Test the generated skill with your AI agent and refine instructions based on execution edge cases.
