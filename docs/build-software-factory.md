class: middle

<!--
Deck notes
- No full stops anywhere
- Deadpan, second-person, problem–solution chain
- Every slide: the fix you just made, then `--` reveals the problem it creates
- Short punchy lines, no adjectives, no drama
- Tell the story with SVG visuals and animations, not text
- `visual:` comments are placeholders for SVGs to add later
-->

.font-size-4.weight-700[
So you want to build a software .tc-underline[factory]?
]

---

class: diagram, story

## .icon[arrow-right] You call an LLM

![a prompt going into an LLM and code coming out as text, with nowhere to put it](./img/story/a01.svg)

<!-- Generates code -->

.text-center[

### .icon[circle-alert] Cannot write files

]

---

class: diagram, story

## .icon[arrow-right] So you give the LLM a write tool

![prompt → LLM → tool call → result → LLM, looping](./img/story/a02.svg)

.text-center[

### .icon[circle-alert] Sends broken JSON

]

---

class: diagram, story

## .icon[arrow-right] So you repair the JSON

![malformed JSON and a wrong schema go into a repair step and come out valid](./img/story/a03.svg)

.text-center[

### .icon[circle-alert] Rewrites the whole file to change one line

]

---

class: diagram, story

## .icon[arrow-right] So you give the agent an edit tool

![a 2,000 line rewrite shrinking to a one line find-and-replace diff](./img/story/a04.svg)

.text-center[

### .icon[circle-alert] Cannot run the code

]

---

class: diagram, story

## .icon[arrow-right] So you give the agent a shell

![the agent doing everything through one terminal: cat, grep, curl, git](./img/story/a05.svg)

.text-center[

### .icon[circle-alert] Cats a 10,000 line file

]

---

class: diagram, story

## .icon[arrow-right] So you add more tools

![a tool list growing: read, search, RAG over the codebase, fetch, git, browser, crowding the prompt](./img/story/a06.svg)

<!-- Read, search, RAG, fetch, git, browser -->

.text-center[

### .icon[circle-alert] Every service wants a dedicated tool

]

---

class: diagram, story

## .icon[arrow-right] So you add MCP

![GitHub, Slack, Jira, Postgres, Sentry plugging in over MCP, each dumping a pile of tools into the prompt](./img/story/a07.svg)

<!-- Another 100 tools -->

.text-center[

### .icon[circle-alert] Their schemas eat the context

]

---

class: diagram, story

## .icon[arrow-right] So you load tools dynamically

![a registry where only the tools for this task are loaded into the prompt](./img/story/a08.svg)

.text-center[

### .icon[circle-alert] Does not know which tools exist

]

---

class: diagram, story

## .icon[arrow-right] So you add a tool to search tools

![the agent queries the registry and gets back the few tools that match](./img/story/a09.svg)

<!-- Can call any tool -->

.text-center[

### .icon[circle-alert] One tool returns 50,000 lines and fills the context

]

---

class: diagram, story

## .icon[arrow-right] So you cap tool output

![a wall of text cut off before it reaches the model, then many turns stacking up until the window is full again](./img/story/a10.svg)

<!-- Runs for an hour -->

.text-center[

### .icon[circle-alert] The context is full again

]

---

class: diagram, story

## .icon[arrow-right] So you compact

![older turns squeezed into a summary, the run continuing for hours](./img/story/a11.svg)

<!-- Runs for hours -->

.text-center[

### .icon[circle-alert] The provider fails on a normal Tuesday

]

---

class: diagram, story

## .icon[arrow-right] So you add retries, limits and resume

![request fails, backs off, tries again](./img/story/a12.svg)

<!-- Runs all week -->

.text-center[

### .icon[circle-alert] A $1,000 bill arrives

]

---

class: diagram, story

## .icon[arrow-right] So you add open-weight models

![the same conversation routed to DeepSeek, Qwen and a self-hosted Llama, the cost meter dropping](./img/story/a13.svg)

<!-- Call the wrong tool -->

.text-center[

### .icon[circle-alert] With made-up arguments

]

---

class: diagram, story

## .icon[arrow-right] So you write evals

![a scoreboard built from real tasks in your own repos, one row per model, columns for right tool, right arguments, tests pass](./img/story/a14.svg)

<!-- Real tasks from your own repos -->
<!-- Scored on right tool, right arguments, tests pass -->

.text-center[

### .icon[circle-alert] Every model fails differently

]

---

class: diagram, story

## .icon[arrow-right] So you tune for each model

![one agent core with a per-model layer of prompts and tool descriptions](./img/story/a15.svg)

<!-- Prompts and tool descriptions per model -->

.text-center[

### .icon[circle-alert] A fix for one model breaks another

]

---

class: diagram, story

## .icon[arrow-right] So you run the evals on every change

![every prompt, tool description and model version change running the full eval suite before it lands](./img/story/a16.svg)

<!-- Prompt, tool description, model version -->

.text-center[

### .icon[circle-alert] Passes the evals, still takes all day on a big task

]

---

class: diagram, story

## .icon[arrow-right] So you add sub-agents

![one long queue of steps split into pieces handed to hundreds of agents in a background lane while the main agent keeps chatting with you](./img/story/a17.svg)

<!-- Spawn 400 in the background -->
<!-- You keep talking while they work -->

.text-center[

### .icon[circle-alert] Every team wants the agent to work their way

]

---

class: diagram, story

## .icon[arrow-right] So you add hooks, permissions, AGENTS.md and skills

![four extension points around the agent core: hooks firing around tool calls, a permission gate, an AGENTS.md of project rules, a shelf of skills](./img/story/a18.svg)

<!-- Rules set per team -->

---

class: middle, shatter, celebrate

# 🎉 Congratulations

--

### You have built an .tc-underline[agent]

### .icon[circle-alert] Now build a Software Factory

---

class: middle

# Make it .tc-underline[autonomous]

---

class: diagram, story

## .icon[arrow-right] So you schedule agents

![schedules waking the agent on your laptop: a nightly dependency bump, a weekly cleanup](./img/story/f01.svg)

<!-- You close the laptop -->

.text-center[

### .icon[circle-alert] The nightly run never happens

]

---

class: diagram, story

## .icon[arrow-right] So you run the agent in the cloud

![the agent moving from the laptop to a machine in the cloud, the nightly run firing on time with the lid closed](./img/story/f02.svg)

<!-- Always on -->

.text-center[

### .icon[circle-alert] You can only reach the agent over SSH

]

---

class: diagram, story

## .icon[arrow-right] So you move the control plane out

![the UI, sessions and steering pulled out of the agent process into a control plane with an API](./img/story/f03.svg)

<!-- Any screen can drive the agent, even your phone -->

.text-center[

### .icon[circle-alert] Only responds when someone types

]

---

class: diagram, story

## .icon[arrow-right] So you add more triggers

![Slack messages, support tickets, prod alerts and failed deploys wired straight to the cloud agent](./img/story/f04.svg)

<!-- Slack, support tickets, prod alerts, failed deploys -->

.text-center[

### .icon[circle-alert] 100 untested PRs opened overnight

]

---

class: diagram, story

## .icon[arrow-right] So you set up verification agents

![a second set of agents picking up each PR: running the tests, recording a screen capture, attaching logs and a report as artifacts](./img/story/f05.svg)

<!-- Runs tests and generates artifacts -->

.text-center[

### .icon[circle-alert] Not everything needs a PR

]

---

class: diagram, story

## .icon[arrow-right] So you add a project board

![events landing on a board as cards, flowing through columns Triage → Spec → Dev → QA → Review](./img/story/f06.svg)

<!-- Triage → Spec → Dev → QA → Review -->

.text-center[

### .icon[circle-alert] You have to move every card by hand

]

---

class: diagram, story

## .icon[arrow-right] So you set up an agent to run the board

![an agent watching the project board and moving cards on its own: a finished spec starts dev, green QA opens review, a failure sends the card back](./img/story/f07.svg)

<!-- Every task moves itself -->
<!-- The agent crashes mid-run -->

.text-center[

### .icon[circle-alert] The task is lost

]

---

class: diagram, story

## .icon[arrow-right] So you make every step durable

![each step of each agent checkpointed as it finishes, the hand-offs between agents recorded](./img/story/f08.svg)

<!-- Tasks resume where they stopped -->
<!-- The cloud machine is replaced -->

.text-center[

### .icon[circle-alert] Schedules and triggers die with the machine

]

---

class: diagram, story

## .icon[arrow-right] So you move the management plane out

![three layers: control plane (UI, sessions, steering), management plane (triggers, schedules, lifecycle, a secrets vault) running as its own service, and cloud machines below as disposable sandboxes receiving short-lived tokens per task](./img/story/f09.svg)

<!-- Secrets move to a vault -->
<!-- Sandboxes get short-lived tokens -->
<!-- Everyone has their own machines -->

.text-center[

### .icon[circle-alert] All working in silos

]

---

class: diagram, story

## .icon[arrow-right] So you add a shared knowledge base

![every person and agent reading from and writing to one knowledge base, agents merging duplicates and fixing stale pages](./img/story/f10.svg)

<!-- Kept in sync by agents -->

.text-center[

### .icon[circle-alert] Agents now ship faster than you can review

]

---

class: diagram, story

## .icon[arrow-right] So you set up rubrics

![a rubric scoring every change](./img/story/f11.svg)

<!-- Agents review against the rubric, humans take the exceptions -->

.text-center[

### .icon[circle-alert] Every adjustment reprocesses all the data

]

---

class: diagram, story

## .icon[arrow-right] So you set up reports

![dashboards kept up to date from history: cost per task, cycle time, rework](./img/story/f12.svg)

<!-- Maintains historical data -->
<!-- Cost per task, cycle time, rework -->

.text-center[

### .icon[circle-alert] The rubrics go stale

]

---

class: diagram, story

## .icon[arrow-right] So you set up goals

![targets pinned over the reports](./img/story/f13.svg)

<!-- An agent tunes the rubrics and workflows to hit them -->

---

class: middle, celebrate

# 🎉 Congratulations

--

### You have built a simple .tc-underline[software factory]

---

class: diagram, spaced

## .icon[arrow-right] Now Scale the Factory

.two-columns[
.column[

- .icon[users] Many Teams, One Factory
- .icon[gauge] Capacity and Cost
- .icon[eye] Review Becomes the Limit
- .icon[shield-alert] Production Safety

]
.column[

- .icon[lock] Security and Compliance
- .icon[book-open] Keeping Knowledge True
- .icon[package] The Factory as a Product

]
]

???

1. Many teams, one factory

- Conflicting goals: one team wants speed, another stability; needs a goal hierarchy, company goals above team goals
- Shared vs local: what is shared across the org (knowledge, rubrics, workflows) and what each team can override
- Cross-team work: a task touching three repos owned by three teams needs one owner and one board

2. Capacity and cost

- Budgets: per team, per project, per task; the factory stops work that is not worth the spend
- Scheduling: thousands of agents compete for sandboxes, rate limits and CI runners; queues, priorities, fairness
- Model routing: cheap work to cheap models, hard work to frontier models; the evals make that safe

3. Review becomes the limit

- Human attention is the scarce resource: output grows with compute, review grows with headcount
- Risk-based review: sort changes by blast radius; low-risk ships on agent verification, humans see the risky ones
- Trust is earned per area: track revert rates per part of the codebase, widen autonomy where the record is good

4. Production safety

- Blast radius: one bad rubric change affects every team; roll factory changes out gradually, with canaries and rollbacks
- Accountability: someone is on call when the factory ships a bad fix; every change has a named human owner
- Audit trail: which trigger, which agent, which rubric version, who approved

5. Security and compliance

- Permissions per team and per task: an agent working on billing cannot read HR data
- Untrusted input at scale: every ticket and alert is text an attacker can write
- Regulated work: some changes legally need a human sign-off; the workflow has to know which

6. Keeping knowledge true

- Drift: 10,000 conversations a day write to the knowledge base; it goes stale faster than agents can clean it
- Ownership: every page needs an owner and an expiry, or the factory learns from its own old mistakes

7. The factory as a product

- It needs its own team: uptime, upgrades and a roadmap for the factory itself
- Model upgrades: a new model version shifts every rubric score and eval; treat it as a migration
- Measuring the factory: from tasks completed to business outcomes (idea-to-production cycle time, defects reaching customers)

Closing line: a simple factory replaces the work; a scaled factory has to replace the coordination, which is the harder part
