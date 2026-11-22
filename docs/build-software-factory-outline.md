# So you want to build a software factory? (story outline)

Format: `> So you ... (additional info) _problem_`

<!-- Review scores: how connected the story is at each step
4 The previous problem forces this step, and this step causes its own problem
3 Clear fix, but one side is loose (the problem is a new topic, or the fix is indirect)
2 Noticeable jump: the fix or the problem does not follow
1 No connection

Agent act: rewritten from the independent review (names the agent loop at the shell step, 400 sub-agents moved to the Factory act)
AI SDLC act: average 3.8; goals and Congratulations share a problem
Factory act: reworked from the independent review; open point is the messaging complexity of moving the agent loop out
Control Plane, Credentials and sandbox reuse are now in the Factory act; Management Plane only through sandbox groups; Accountability not covered yet
-->

## Agent

> So you call an LLM (Generates code) _Cannot write files_

> So you give the LLM a write tool (Whole file as one JSON string) _Sends broken JSON_

> So you repair the JSON (Writes land now) _Still resends a 2,000-line file to change one line_

> So you give the agent an edit tool (Search and replace) _Breaks the build and never finds out_

> So you give the agent a shell (Runs, reads the error, tries again: the agent loop) _Cats a 10,000-line file_

> So you add more tools (Ranged read and grep, then fetch, git, browser) _Every service needs a hand-written tool_

> So you add MCP (Another 100 tools) _Tool schemas eat the context_

> So you load tools dynamically _Does not know which tools exist_

> So you add a tool to search tools (Can call any tool) _One tool returns 50,000 lines and fills the context_

> So you cap tool output (Runs for an hour) _The context is full again_

> So you compact (Runs for hours) _The provider fails on a normal Tuesday_

> So you add retries, fallbacks and resume (Runs all week) _A $1,000 bill arrives_

> So you add open-weight models (A fraction of the cost) _Sometimes calls the wrong tool with made-up arguments_

> So you write evals (Real tasks from your repos; Right tool, right arguments, tests pass) _Every model fails differently_

> So you tune for each model (Per-model prompts on a shared harness) _A fix for one model breaks another_

> So you run the evals on every change (Prompt, tool description, model version) _Correct, but a big task crawls one step at a time_

> So you add sub-agents (A dozen in the background; You keep talking while they work) _Now every team wants it, each their own way_

> So you add hooks, permissions, AGENTS.md and skills (Every team sets its own rules)

> Congratulations (You have built an agent) _Works only for whoever is driving it_

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
- [x] Self Improving -> Skills
- [ ] Accountability
- [x] Credentials

### Story

> Now build the factory (Ship with quality consistently) _Every agent starts from zero_

> So you add a shared knowledge base (Agents keep it in sync; Every agent now has enough context to act) _Every request becomes a PR on GitHub_

> So you integrate a project board (Triage → Spec → Dev → QA → Review; Not everything needs a PR) _You have to move every card by hand_

> So you set up an agent to run the board (Every card moves itself; Verification agents run QA and attach artifacts) _Agents repeat the same mistakes_

> So you set up rubrics (Agents grade every task; Humans take the exceptions) _Failures are recorded, nothing learns from them_

> So you turn failures into skills (Agents write a skill from each repeated fix; The next agent loads it) _You cannot tell if a skill helped_

> So you set up reports (Cost per task, cycle time, rework, per skill; Kept over time) _Someone has to read them and decide what to change_

> So you set up goals (An agent tunes rubrics, skills and workflows to hit them; Rework is the guardrail)

> Congratulations (You have set up an AI SDLC) _Works only when you ask_

## Factory

> So you add more triggers (Schedule, Slack, support tickets, prod alerts, failed deploys) _It all stops when you close the laptop_

> So you run the agent on a cloud machine (Always on; Your keys live on it now) _You can only reach it over SSH_

> So you make the agent headless (Anyone can drive it from any screen, even a phone) _A heavy build freezes the agent and nobody can connect_

<!-- FIXME: Complexity of the messaging infra required to move the agent loop out is under appreciated here -->

<!-- Proposal: give the messaging its own beat instead of hiding it in one step. Moving the loop out turns every tool call into a remote call, and that is where the real engineering is:

> So you move the agent loop to a control plane (The machine becomes a sandbox that only runs the work; Every tool call is now a message) _Output streams arrive out of order, connections drop mid-command_

> So you put a message bus between them (Ordered streams per task; Sandboxes reconnect and resume the stream) _A retried command runs twice_

> So you make every call durable (Each call has an ID; Replays are safe; Files survive a crash) _Every trigger and agent queues for the same sandbox_

Replaces the current 'move the agent loop' and 'make the sandbox state durable' steps (two steps become three); 'Sandboxes are disposable, and so is their work' folds into the durable step -->

> So you move the agent loop to a control plane (The machine becomes a sandbox that only runs the work) _Sandboxes are disposable, and so is their work_

> So you make the sandbox state durable (Files survive a crash; The loop retries the step) _Every trigger and agent queues for the same sandbox_

> So you spin up a sandbox per task (400 at once; Scale to zero when idle) _A typo fix gets the same 64 GB box and prod keys as a migration_

> So you create sandbox groups (Each sets machine size, network access and short-lived credentials; Warm pools per repo skip clone and install)

> Congratulations (You have built a simple software factory) _Still want to build one?_
