# So you want to build a software factory? (story outline)

Format: `> So you ... (additional info) _problem_`

## Agent

> You call an LLM (Generates code) _Cannot write files_

> So you give the LLM a write tool _Sends broken JSON_

> So you repair the JSON _Rewrites the whole file to change one line_

> So you give the agent an edit tool _Cannot run the code_

> So you give the agent a shell _Cats a 10,000 line file_

> So you add more tools (Read, search, RAG, fetch, git, browser) _Every service wants a dedicated tool_

> So you add MCP (Another 100 tools) _Their schemas eat the context_

> So you load tools dynamically _Does not know which tools exist_

> So you add a tool to search tools (Can call any tool) _One tool returns 50,000 lines and fills the context_

> So you cap tool output (Runs for an hour) _The context is full again_

> So you compact (Runs for hours) _The provider fails on a normal Tuesday_

> So you add retries, limits and resume (Runs all week) _A $1,000 bill arrives_

> So you add open-weight models (Call the wrong tool) _With made-up arguments_

> So you write evals (Real tasks from your own repos; Scored on right tool, right arguments, tests pass) _Every model fails differently_

> So you tune for each model (Prompts and tool descriptions per model) _A fix for one model breaks another_

> So you run the evals on every change (Prompt, tool description, model version) _Passes the evals, still takes all day on a big task_

> So you add sub-agents (Spawn 400 in the background; You keep talking while they work) _Every team wants the agent to work their way_

> So you add support for hooks, permissions, AGENTS.md and skills (Every team sets its own rules)

> Congratulations (You have built an agent) _Only works when you ask_

## Factory

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
- [x] Credentials

### Story

> Now build the factory (Things should work autonomously)

> So you schedule agents (You close the laptop) _The nightly run never happens_

> So you run the agent in the cloud (Always on) _You can only reach the agent over SSH_

> So you move the control plane out (Any screen can drive the agent, even your phone) _Only responds when someone types_

> So you add more triggers (Slack, support tickets, prod alerts, failed deploys) _100 untested PRs opened overnight_

> So you set up verification agents (Runs tests and generates artifacts) _Not everything needs a PR_

> So you add a project board (Triage → Spec → Dev → QA → Review) _You have to move every card by hand_

<!-- SHIP TO PROD: the pipeline stops at Review, nothing deploys, watches production or rolls back. Options:
1. Extend the stages: > So you add a project board (Triage → Spec → Dev → QA → Review → Deploy) _You have to move every card by hand_
2. Own step after verification or the board agent: > So you let the factory deploy (Canary first; Rolls back on a bad signal) _..._
3. Use it as the "simple factory" signal at the end: _Still stops at a merged PR_
-->

> So you set up an agent to run the board (Every task moves itself; The agent crashes mid-run) _The task is lost_

> So you make every step durable (Tasks resume where they stopped; The machine is replaced) _Schedules and triggers die with the machine_

> So you move the management plane out (Secrets move to a vault; Sandboxes get short-lived tokens) _The agent loop still runs inside the sandbox_

> So you move the agent loop out (Sandboxes only run the work; Spun up per task, thrown away after; Everyone has their own machines) _All working in silos_

> So you add a shared knowledge base (Agents to keep it in sync) _Agents now ship faster than you can review_

> So you set up rubrics (Agents review against the rubric, humans take the exceptions) _Every adjustment reprocesses all the data_

> So you set up reports (Maintains historical data; Cost per task, cycle time, rework) _The rubrics go stale_

> So you set up goals (An agent tunes the rubrics and workflows to hit them)

> Congratulations (You have built a simple software factory) _Now scale the factory_

<!-- SCALING THE FACTORY (speaking pointers for "Now scale the factory")

1. Many teams, one factory
- Conflicting goals: one team wants speed, another stability; needs a goal hierarchy, company goals above team goals
- Shared vs local: what is shared across the org (knowledge, rubrics, workflows) and what each team can override
- Cross-team work: a task touching three repos owned by three teams needs one owner and one board

2. Capacity and cost
- Budgets: per team, per project, per task; the factory stops work that is not worth the spend
- Scheduling: thousands of agents compete for sandboxes, rate limits and CI runners; queues, priorities, fairness
- Model routing: cheap work to cheap models, hard work to frontier models; the evals make that safe

3. Production safety
- Blast radius: one bad rubric change affects every team; roll factory changes out gradually, with canaries and rollbacks
- Accountability: someone is on call when the factory ships a bad fix; every change has a named human owner
- Audit trail: which trigger, which agent, which rubric version, who approved

4. Security and compliance
- Permissions per team and per task: an agent working on billing cannot read HR data
- Untrusted input at scale: every ticket and alert is text an attacker can write
- Regulated work: some changes legally need a human sign-off; the workflow has to know which

5. Keeping knowledge true
- Drift: 10,000 conversations a day write to the knowledge base; it goes stale faster than agents can clean it
- Ownership: every page needs an owner and an expiry, or the factory learns from its own old mistakes

6. Tracing every change
- Who changed what: every commit, deploy and config edit is tied to the trigger, agent, model, prompt and rubric version behind it, plus the human who approved it
- Agents and humans side by side: the log shows which changes were made by people and which by agents, so incidents and reverts can be traced to their source
- Replayable: from any line in production you can walk back to the task, the conversation and the decision that produced it

7. The factory as a product (the highlight: to scale, the factory has to be run as a product)
- It needs its own team: uptime, upgrades and a roadmap for the factory itself
- Model upgrades: a new model version shifts every rubric score and eval; treat it as a migration
- Measuring the factory: from tasks completed to business outcomes (idea-to-production cycle time, defects reaching customers)

Closing line: a simple factory replaces the work; a scaled factory has to replace the coordination, which is the harder part
If short on time, pick three: the factory as a product (7), tracing every change (6), conflicting goals (1)
-->
