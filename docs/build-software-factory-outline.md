# So you want to build a software factory? (story outline)

Format: `> So you ... (additional info) _problem_`

<!-- Review scores: how connected the story is at each step
4 The previous problem forces this step, and this step causes its own problem
3 Clear fix, but one side is loose (the problem is a new topic, or the fix is indirect)
2 Noticeable jump: the fix or the problem does not follow
1 No connection

Agent act: average 3.7, tight throughout
AI SDLC act: average 3.8; goals and Congratulations share a problem
Factory act: average 3.5; the headless and agent loop problems need a cause
Pieces to cover not in the story any more: Control Plane, Management Plane, Credentials (secrets vault, short-lived tokens)
-->

## Agent

> You call an LLM (Generates code) _Cannot write files_

<!-- Suggest: So you call an LLM (Generates code) _Cannot write files_ (starts the 'So you' rhythm, echoes the title) -->

> So you give the LLM a write tool _Sends broken JSON_

<!-- Suggest: So you give the LLM a write tool (Whole file as one JSON string) _Sends broken JSON_ (says why it breaks) -->

> So you repair the JSON _Rewrites the whole file to change one line_

<!-- Suggest: So you repair the JSON (Writes land now) _Still resends a 2,000-line file to change one line_ -->

> So you give the agent an edit tool _Cannot run the code_

<!-- Suggest: So you give the agent an edit tool (Search and replace) _Breaks the build and never finds out_ -->

> So you give the agent a shell _Cats a 10,000 line file_

<!-- Suggest: So you give the agent a shell (Runs, reads the error, tries again: the agent loop) _Cats a 10,000-line file_ (names the agent loop so Act 3 can move it out) -->

> So you add more tools (Read, search, RAG, fetch, git, browser) _Every service wants a dedicated tool_

<!-- Suggest: So you add more tools (Ranged read and grep, then fetch, git, browser) _Every service needs a hand-written tool_ (drop RAG) -->

> So you add MCP (Another 100 tools) _Their schemas eat the context_

<!-- Suggest: So you add MCP (Another 100 tools) _Tool schemas eat the context_ -->

> So you load tools dynamically _Does not know which tools exist_

> So you add a tool to search tools (Can call any tool) _One tool returns 50,000 lines and fills the context_

> So you cap tool output (Runs for an hour) _The context is full again_

> So you compact (Runs for hours) _The provider fails on a normal Tuesday_

> So you add retries, limits and resume (Runs all week) _A $1,000 bill arrives_

<!-- Suggest: So you add retries, fallbacks and resume (Runs all week) _A $1,000 bill arrives_ ('limits' reads as spend limits) -->

> So you add open-weight models (Call the wrong tool) _With made-up arguments_

<!-- Suggest: So you add open-weight models (A fraction of the cost) _Sometimes calls the wrong tool with made-up arguments_ -->

> So you write evals (Real tasks from your own repos; Scored on right tool, right arguments, tests pass) _Every model fails differently_

<!-- Suggest: So you write evals (Real tasks from your repos; Right tool, right arguments, tests pass) _Every model fails differently_ -->

> So you tune for each model (Prompts and tool descriptions per model) _A fix for one model breaks another_

<!-- Suggest: So you tune for each model (Per-model prompts on a shared harness) _A fix for one model breaks another_ -->

> So you run the evals on every change (Prompt, tool description, model version) _Passes the evals, still takes all day on a big task_

<!-- Suggest: So you run the evals on every change (Prompt, tool description, model version) _Correct, but a big task crawls one step at a time_ -->

> So you add sub-agents (Spawn 400 in the background; You keep talking while they work) _Every team wants the agent to work their way_

<!-- Suggest: So you add sub-agents (A dozen in the background; You keep talking while they work) _Now every team wants it, each their own way_ (400 moves to sandbox per task) -->

> So you add support for hooks, permissions, AGENTS.md and skills (Every team sets its own rules)

<!-- Suggest: So you add hooks, permissions, AGENTS.md and skills (Every team sets its own rules) -->

> Congratulations (You have built an agent) _Outcomes aren't reliable_

<!-- Suggest: Congratulations (You have built an agent) _Works only for whoever is driving it_ ('Outcomes aren't reliable' clashes with 'Passes the evals') -->

## AI SDLC

### Pieces to cover

- [x] Project Boards
- [x] Reports
- [x] Durability
- [x] Cloud Sandboxes
- [x] Control Plane
- [x] Management Plane
- [x] Verification
- [x] Knowledge
- [x] Artifacts
- [x] Rubrics
- [x] Cost
- [ ] Self Improving -> Skills
- [ ] Accountability
- [x] Credentials

### Story

> Now build the factory (Ship with quality consistently) _Every agent starts from zero_

<!-- Suggest: So you roll it out to every team (Ship with quality, every time) _What one agent learns, the next one never sees_ ('starts from zero' contradicts AGENTS.md; 'factory' is Act 3's name) -->

> So you add a shared knowledge base (Agents keep it in sync; Every agent now has enough context to act) _Every request becomes a PR on GitHub_

<!-- Suggest: So you add a shared knowledge base (Agents keep it in sync; Every agent has enough context to act) _Every request goes straight to a PR, with no triage or spec_ -->

> So you integrate a project board (Triage → Spec → Dev → QA → Review; Not everything needs a PR) _You have to move every card by hand_

> So you set up an agent to run the board (Every card moves itself; Verification agents run QA and attach artifacts) _Agents now ship faster than you can review_

<!-- Suggest: So you hand the board to an agent (Every card moves itself; Verification agents run QA and attach artifacts) _Agents open PRs faster than you can review_. For the FIXME (signal self-improvement instead of review): _The same mistakes come back every week_, then rubrics + skills as the way the factory learns -->

<!-- FIXME: Too much of focus on review - should signal self improvement -->

> So you set up rubrics (Agents review against the rubric, humans take the exceptions) _You cannot tell if the rubrics are working_

<!-- Suggest: So you write rubrics (Agents review against the rubric, humans take the exceptions) _You cannot tell if the rubrics work_ -->

> So you set up reports (Cost per task, cycle time, rework; Kept over time) _Someone has to read them and tune the rubrics_

<!-- Suggest: So you add reports (Cost per task, cycle time, rework; Kept over time) _Someone has to read them and tune the rubrics_ -->

> So you set up goals (An agent tunes the rubrics and workflows to hit them) _Goals are only checked when you ask_

<!-- Suggest: So you set goals (An agent tunes rubrics, workflows and skills to hit them; Rework is the guardrail) with no problem line, so Congratulations carries it (avoids gaming the metric and the duplicate problem) -->

> Congratulations (You have setup an AI SDLC) _Works only when you ask_

<!-- Suggest: Congratulations (You have set up an AI SDLC) _Works only when you ask_ -->

## Factory

> So you add more triggers (Schedule, Slack, support tickets, prod alerts, failed deploys; Each trigger starts its own agent from zero) _It all stops when you close the laptop_

<!-- Suggest: So you add more triggers (Schedule, Slack, support tickets, prod alerts, failed deploys) _It all stops when you close the laptop_ (drop 'starts its own agent from zero', it contradicts the knowledge base) -->

> So you run the agent in the cloud machine (Always on) _You can only reach the agent over SSH_

<!-- Suggest: So you run the agent on a cloud machine (Always on; Your keys live on it now) _You can only reach it over SSH_ -->

> So you make the agent headless (Any screen can drive the agent, even your phone; Tasks now run for days) _Can't connect when its is under load/offline_

<!-- Suggest: So you make the agent headless (Anyone can drive it from any screen, even a phone) _A heavy build freezes the agent and nobody can connect_ (the cause has to be work starving the loop, or the next fix would be more machines) -->

> So you move the agent loop out (Sandboxes only run the work) _Sandbox keeps crashing_

<!-- Suggest: So you move the agent loop to a control plane (The machine becomes a sandbox that only runs the work) _Sandboxes are disposable, and so is their work_ (introduces 'sandbox' and the control plane) -->

> So you make the sandbox state durable (A crashed sandbox comes back where it stopped) _Everyone queues for the same sandbox_

<!-- Suggest: So you make the sandbox state durable (Files survive a crash; The loop retries the step) _Every trigger and agent queues for the same sandbox_ -->

> So you dynamically creates sandboxes for each task _Each sandbox has the same size and privileges_

<!-- Suggest: So you spin up a sandbox per task (400 at once; Scale to zero when idle) _A typo fix gets the same 64 GB box and prod keys as a migration_. For the FIXME (reuse): keep warm sandboxes per repo so a task skips clone and install -->

<!-- FIXME: Use case for sandbox reuse -->

> So you create a group of sandboxes _Groups control resource type_

<!-- Suggest: So you create sandbox groups (Each sets machine size, network access and short-lived credentials), with no problem line (covers Credentials and the Management Plane) -->

> Congratulations (You have built a simple software factory) _Now scale the factory_

<!-- Suggest: Congratulations (You have built a simple software factory) _Still want to build one?_ -->
