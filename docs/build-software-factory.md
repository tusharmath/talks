class: center middle

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

class: diagram

## You call an .tc-underline[LLM]

<!-- visual: a prompt going into an LLM and code coming out as text, with nowhere to put it -->

--

.text-center[

### Generates code

]

--

.text-center[

### .font-grey[.icon[circle-alert] Cannot write files]

]

---

class: diagram

## So you give the LLM a .tc-underline[write] tool

<!-- visual: prompt → LLM → tool call → result → LLM, looping -->

--

.text-center[

### .font-grey[.icon[circle-alert] Sends broken JSON]

]

---

class: diagram

## So you .tc-underline[repair] the JSON

<!-- visual: malformed JSON and a wrong schema go into a repair step and come out valid -->

--

.text-center[

### .font-grey[.icon[circle-alert] Rewrites the whole file to change one line]

]

---

class: diagram

## So you give the agent an .tc-underline[edit] tool

<!-- visual: a 2,000 line rewrite shrinking to a one line find-and-replace diff -->

--

.text-center[

### .font-grey[.icon[circle-alert] Cannot run the code]

]

---

class: diagram

## So you give the agent a .tc-underline[shell]

<!-- visual: the agent doing everything through one terminal: cat, grep, curl, git -->

--

.text-center[

### .font-grey[.icon[circle-alert] Cats a 10,000 line file]

]

---

class: diagram

## So you add more .tc-underline[tools]

<!-- visual: a tool list growing: read, search, RAG over the codebase, fetch, git, browser, crowding the prompt -->

--

.text-center[

### Read, search, RAG, fetch, git, browser

]

--

.text-center[

### .font-grey[.icon[circle-alert] Every service wants a dedicated tool]

]

---

class: diagram

## So you add .tc-underline[MCP]

<!-- visual: GitHub, Slack, Jira, Postgres, Sentry plugging in over MCP, each dumping a pile of tools into the prompt -->

--

.text-center[

### Another 100 tools

]

--

.text-center[

### .font-grey[.icon[circle-alert] Their schemas eat the context]

]

---

class: diagram

## So you load tools .tc-underline[dynamically]

<!-- visual: a registry where only the tools for this task are loaded into the prompt -->

--

.text-center[

### .font-grey[.icon[circle-alert] Does not know which tools exist]

]

---

class: diagram

## So you add a tool to .tc-underline[search] tools

<!-- visual: the agent queries the registry and gets back the few tools that match; then one of those tools returning 50,000 lines that pour into the context window -->

--

.text-center[

### Can call any tool

]

--

.text-center[

### .font-grey[.icon[circle-alert] One tool returns 50,000 lines and fills the context]

]

---

class: diagram

## So you .tc-underline[cap] tool output

<!-- visual: a wall of text cut off before it reaches the model, then many turns stacking up until the window is full again -->

--

.text-center[

### Runs for an hour

]

--

.text-center[

### .font-grey[.icon[circle-alert] The context is full again]

]

---

class: diagram

## So you .tc-underline[compact]

<!-- visual: older turns squeezed into a summary, the run continuing for hours; then a provider request failing mid-run -->

--

.text-center[

### Runs for hours

]

--

.text-center[

### .font-grey[.icon[circle-alert] The provider fails on a normal Tuesday]

]

---

class: diagram

## So you add .tc-underline[retries], limits and resume

<!-- visual: request fails, backs off, tries again; a retry counter, timeout and budget meter; state saved outside the process so a stopped run resumes; the cost meter climbing all week -->

--

.text-center[

### Runs all week

]

--

.text-center[

### .font-grey[.icon[circle-alert] A $1,000 bill arrives]

]

---

class: diagram

## So you add .tc-underline[open-weight] models

<!-- visual: the same conversation routed to DeepSeek, Qwen and a self-hosted Llama, the cost meter dropping; then their tool calls going wrong: the wrong tool picked, arguments that match no schema -->

--

.text-center[

### Call the wrong tool

]

--

.text-center[

### .font-grey[.icon[circle-alert] With made-up arguments]

]

---

class: diagram

## So you write .tc-underline[evals]

<!-- visual: a scoreboard built from real tasks in your own repos, one row per model, columns for right tool, right arguments, tests pass; every row red in a different column -->

--

.text-center[

### Real tasks from your own repos

]

--

.text-center[

### Scored on right tool, right arguments, tests pass

]

--

.text-center[

### .font-grey[.icon[circle-alert] Every model fails differently]

]

---

class: diagram

## So you .tc-underline[tune] for each model

<!-- visual: one agent core with a per-model layer of prompts and tool descriptions; one row on the scoreboard turning green while another turns red -->

--

.text-center[

### Prompts and tool descriptions per model

]

--

.text-center[

### .font-grey[.icon[circle-alert] A fix for one model breaks another]

]

---

class: diagram

## So you run the evals on every .tc-underline[change]

<!-- visual: every prompt, tool description and model version change running the full eval suite before it lands; all green, next to a single big task still grinding through its steps one at a time -->

--

.text-center[

### Prompt, tool description, model version

]

--

.text-center[

### .font-grey[.icon[circle-alert] Passes the evals, still takes all day on a big task]

]

---

class: diagram

## So you add .tc-underline[sub-agents]

<!-- visual: one long queue of steps split into pieces handed to hundreds of agents in a background lane while the main agent keeps chatting with you; then several teams each pulling the agent toward their own conventions -->

--

.text-center[

### Spawn 400 in the background

]

--

.text-center[

### You keep talking while they work

]

--

.text-center[

### .font-grey[.icon[circle-alert] Every team wants the agent to work their way]

]

---

class: diagram

## So you add hooks, permissions, AGENTS.md and .tc-underline[skills]

<!-- visual: four extension points around the agent core: hooks firing around tool calls, a permission gate, an AGENTS.md of project rules, a shelf of skills; each team plugging in its own -->

--

.text-center[

### Rules set per team

]

---

class: center middle, shatter

# Congratulations

--

### You have built an .tc-underline[agent]

--

### .font-grey[.icon[circle-alert] Now build a Software Factory]

---

class: middle

# Make it .tc-underline[autonomous]

---

class: diagram

## So you .tc-underline[schedule] agents

<!-- visual: schedules waking the agent on your laptop: a nightly dependency bump, a weekly cleanup; then the lid closing and the nightly run silently skipped -->

--

.text-center[

### You close the laptop

]

--

.text-center[

### .font-grey[.icon[circle-alert] The nightly run never happens]

]

---

class: diagram

## So you run the agent in the .tc-underline[cloud]

<!-- visual: the agent moving from the laptop to a machine in the cloud, the nightly run firing on time with the lid closed; then you, away from your desk, with no way in except an SSH session -->

--

.text-center[

### Always on

]

--

.text-center[

### .font-grey[.icon[circle-alert] You can only reach the agent over SSH]

]

---

class: diagram

## So you move the .tc-underline[control plane] out

<!-- visual: the UI, sessions and steering pulled out of the agent process into a control plane with an API; terminal, web and phone connect to it as separate clients; the agent idle until someone types -->

--

.text-center[

### Any screen can drive the agent, even your phone

]

--

.text-center[

### .font-grey[.icon[circle-alert] Only responds when someone types]

]

---

class: diagram

## So you add more .tc-underline[triggers]

<!-- visual: Slack messages, support tickets, prod alerts and failed deploys wired straight to the cloud agent; every event going straight to a pull request with nothing run against it, the PR counter reaching 100 by morning -->

--

.text-center[

### Slack, support tickets, prod alerts, failed deploys

]

--

.text-center[

### .font-grey[.icon[circle-alert] 100 untested PRs opened overnight]

]

---

class: diagram

## So you set up .tc-underline[verification] agents

<!-- visual: a second set of agents picking up each PR: running the tests, recording a screen capture, attaching logs and a report as artifacts; then a support question that only needed an answer sitting in the queue as a PR -->

--

.text-center[

### Runs tests and generates artifacts

]

--

.text-center[

### .font-grey[.icon[circle-alert] Not everything needs a PR]

]

---

class: diagram

## So you add a .tc-underline[project board]

<!-- visual: events landing on a board as cards, flowing through columns Triage → Spec → Dev → QA → Review; you dragging every card from one column to the next by hand while the inbox keeps growing -->

--

.text-center[

### Triage → Spec → Dev → QA → Review

]

--

.text-center[

### .font-grey[.icon[circle-alert] You have to move every card by hand]

]

---

class: diagram

## So you set up an .tc-underline[agent] to run the board

<!-- visual: an agent watching the project board and moving cards on its own: a finished spec starts dev, green QA opens review, a failure sends the card back; then the agent process crashing mid-run and the card it was working on going blank -->

--

.text-center[

### Every task moves itself

]

--

.text-center[

### The agent crashes mid-run

]

--

.text-center[

### .font-grey[.icon[circle-alert] The task is lost]

]

---

class: diagram

## So you make every step .tc-underline[durable]

<!-- visual: each step of each agent checkpointed as it finishes, the hand-offs between agents recorded; the agent restarts and resumes the task from its last finished step; then the cloud machine being replaced and the schedules and triggers living on it vanishing with it -->

--

.text-center[

### Tasks resume where they stopped

]

--

.text-center[

### The machine is replaced

]

--

.text-center[

### .font-grey[.icon[circle-alert] Schedules and triggers die with the machine]

]

---

class: diagram

## So you move the .tc-underline[management plane] out

<!-- visual: three layers: control plane (UI, sessions, steering), management plane (triggers, schedules, lifecycle, a secrets vault) running as its own service, and cloud machines below as disposable sandboxes receiving short-lived tokens per task; then every person with their own set of machines, walled off from each other -->

--

.text-center[

### Secrets move to a vault

]

--

.text-center[

### Sandboxes get short-lived tokens

]

--

.text-center[

### Everyone has their own machines

]

--

.text-center[

### .font-grey[.icon[circle-alert] All working in silos]

]

---

class: diagram

## So you add a shared .tc-underline[knowledge base]

<!-- visual: every person and agent reading from and writing to one knowledge base, agents merging duplicates and fixing stale pages; work speeding up until the review column overflows -->

--

.text-center[

### Kept in sync by agents

]

--

.text-center[

### .font-grey[.icon[circle-alert] Agents now ship faster than you can review]

]

---

class: diagram

## So you set up .tc-underline[rubrics]

<!-- visual: a rubric scoring every change; agents review against it and pass most work, humans see only the exceptions; then one rubric tweak sending the whole history of work back through for re-scoring -->

--

.text-center[

### Agents review against the rubric, humans take the exceptions

]

--

.text-center[

### .font-grey[.icon[circle-alert] Every adjustment reprocesses all the data]

]

---

class: diagram

## So you set up .tc-underline[reports]

<!-- visual: dashboards kept up to date from history: cost per task, cycle time, rework; the numbers drifting while the rubrics stay the same -->

--

.text-center[

### Maintains historical data

]

--

.text-center[

### Cost per task, cycle time, rework

]

--

.text-center[

### .font-grey[.icon[circle-alert] The rubrics go stale]

]

---

class: diagram

## So you set up .tc-underline[goals]

<!-- visual: targets pinned over the reports; an agent reading the reports, changing a rubric or a workflow, measuring against the goals and keeping what helped -->

--

.text-center[

### An agent tunes the rubrics and workflows to hit them

]

---

class: center middle

# Congratulations

--

### You have built a simple .tc-underline[software factory]

---

class: diagram, spaced

## Now .tc-underline[Scale] the Factory

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
