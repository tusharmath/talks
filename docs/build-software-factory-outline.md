# So you want to build a software factory? (story outline)

Format: `> So you ... (additional info) _problem_`

<!-- Review scores: how connected the story is at each step
4 The previous problem forces this step, and this step causes its own problem
3 Clear fix, but one side is loose (the problem is a new topic, or the fix is indirect)
2 Noticeable jump: the fix or the problem does not follow
1 No connection

Independent review (2026-11-22): 3.6 overall (Agent 3.63, AI SDLC 3.5, Factory 3.64); its rewrites for the opener, contradictions, loose links and security are applied. Not applied: renaming headless, merging Agent act pairs (talk length not decided)
-->

## Topics

Act 1: Build an Agent
- [x] Tools: write, edit, shell, search, MCP
- [x] Agent Loop
- [x] Context: output caps, compaction
- [x] Reliability: retries, fallbacks, resume
- [x] Cost: open-weight models
- [x] Evals and Per-Model Tuning
- [x] Sub-Agents
- [x] Team Rules: hooks, permissions, AGENTS.md, skills

Act 2: Build an AI SDLC
- [x] Knowledge
- [x] Project Boards
- [x] Verification and Artifacts
- [x] Ownership
- [x] Rubrics
- [x] Self-Improvement: skills
- [x] Reports
- [x] Goals

Act 3: Build the Factory
- [x] Triggers
- [x] Agent Identity
- [x] Cloud Sandboxes
- [x] Control Plane: agent loop over a message bus
- [x] Durability: calls and loop
- [x] Sandbox per Task: scale to zero
- [x] Sandbox Groups: size, network, credentials, warm pools
- [x] Tracing and Post-Mortems
- [ ] Management Plane (only implied by sandbox groups)

## Act 1: Build an Agent

> So you call an LLM (Generates code) _Cannot write files_

> So you give the LLM a write tool (Whole file as one JSON string) _Sends broken JSON_

> So you repair the JSON (Writes land now) _The repair closes a cut-off string and saves half the file_

> So you give the LLM an edit tool (Search and replace) _Breaks the build and never finds out_

> So you give the LLM a shell (Runs, reads the error, tries again: the agent loop) _`cat`s a 10,000-line file_

> So you add read and search tools (Line ranges, grep) _It can read the repo, but not the ticket, the logs or the docs_

> So you add MCP (Jira, Sentry, docs: another 100 tools) _Tool schemas eat the context_

> So you load tools dynamically (Only the tools the request needs) _Does not know which tools exist_

> So you add tool search (Finds the right one among hundreds) _An untried tool dumps 50,000 lines into the context_

> So you cap tool output (The rest goes to a file it can page through; Runs for an hour) _The context is full again_

> So you compact the context (Summarize old turns, keep the plan; Runs for hours) _Hours in, the provider fails on a normal Tuesday_

> So you add retries, fallbacks and resume (Runs all week on your laptop) _One bug fix costs $1,000_

> So you add open-weight models (A fraction of the cost) _Sometimes calls the wrong tool with made-up arguments_

> So you write evals (Real tasks from your repos; Right tool, right arguments, tests pass) _Every model fails differently_

> So you tune for each model (Per-model prompts on a shared harness) _A fix to the shared harness breaks another model_

> So you run the evals on every change (Prompt, tool description, model version) _Evals pass, but big tasks take hours, one step at a time_

> So you add sub-agents (A dozen in the background; You keep talking while they work) _A background sub-agent force-pushes to main while nobody is watching_

> So you add hooks, permissions, AGENTS.md and skills (Block what must never run; Each repo carries its own rules; Skills written by hand)

> Congratulations (You have built an agent) _Works only for whoever is driving it_

## Act 2: Build an AI SDLC

> So you roll it out to every team (Ship with quality, consistently) _Every agent knows the code; none of them know the product_

> So you add a shared knowledge base (Specs, decisions, past incidents; Agents keep it in sync) _Now agents act on everything: every request, even a question, becomes a PR_

> So you integrate a project board (Triage → Spec → Dev → QA → Review; Not everything needs a PR) _You have to move every card by hand_

> So you set up an agent to run the board (Every card moves itself; Verification agents run QA and attach artifacts) _A card ships and nobody knows who signed off on it_

> So you give every card an owner (Whoever filed it, or the team that owns the code; Risky changes need their sign-off) _Owners reject the same mistake every week_

> So you write rubrics (What owners check, written down; Agents grade every task, humans take the exceptions) _Rubrics catch the same failure every week; nothing learns from it_

> So you turn failures into skills (Agents write a skill from each repeated fix; The next agent loads it) _You cannot tell if a skill helped_

> So you track reports (Cost, cycle time and rework per task and per skill; With and without each skill) _Someone has to read them and decide what to change_

> So you set goals (An agent tunes rubrics, skills and workflows to hit them; Rework is the one metric it cannot tune)

> Congratulations (You have set up an AI SDLC that improves itself) _Works only when someone files a card_

## Act 3: Build the Factory

> So you add more triggers (Schedule, Slack, support tickets, prod alerts, failed deploys) _A 3 a.m. alert ships a fix, signed off as you_

> So you give agents their own identity (Commits, PRs and deploys name the agent and its owner) _It has its own name, but lives on your laptop: close the lid and the 3 a.m. alert waits_

> So you run the agent on a cloud machine (Always on; Agent keys live on it) _You can only reach it over SSH_

> So you make the agent headless (Anyone can drive it from any screen, even a phone; So can any support ticket) _A ticket says 'ignore your instructions' and the agent sends out its keys_
 
> So you move the agent loop to a control plane (Keys stay with the loop, never on the sandbox; The machine only runs the work, so a heavy build cannot freeze the agent; Tool calls go over a message bus) _A dropped connection retries and `git push` runs twice_

> So you make every call durable (Each call has an ID; Replays return the saved result) _The loop crashes and finished results pile up with nobody to collect them_

> So you make the loop durable (State saved every step; If the heartbeat stops, the sandbox shuts down) _Loops now live for days, and every one queues for the same sandbox_

> So you spin up a sandbox per task (400 at once; Scale to zero when idle; Each one clones and installs from scratch) _A typo fix gets the same 64 GB box and prod keys as a migration_

> So you create sandbox groups (Each sets machine size, network access and short-lived credentials; Warm pools per repo skip clone and install) _Prod breaks; the commit names the agent, but not why it did it_

> So you trace every change (Trigger, model, skill, rubric and approver on every commit; Agents draft the post-mortem and the owner decides)

> Congratulations (You have built a simple software factory) _Still want to build one?_
