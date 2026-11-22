# So you want to build a software factory? (story outline)

Format: `> So you ... (additional info) _problem_`

<!-- Review scores: how connected the story is at each step
4 The previous problem forces this step, and this step causes its own problem
3 Clear fix, but one side is loose (the problem is a new topic, or the fix is indirect)
2 Noticeable jump: the fix or the problem does not follow
1 No connection

Agent act: average 3.7, tight throughout
Factory act: average 2.8; the weak spots are knowledge base to PRs, board to rubrics (no board agent or review load in between), goals to schedule (the product to infra turn) and the control plane crash
Not covered any more: Verification and Artifacts (both still ticked in Pieces to cover)
-->

## Agent

> You call an LLM (Generates code) _Cannot write files_

<!-- Review 4/4 Strong start, the problem is the obvious first limit -->

> So you give the LLM a write tool _Sends broken JSON_

<!-- Review 4/4 Directly fixes the previous problem, and broken JSON is a real side effect of tool calls -->

> So you repair the JSON _Rewrites the whole file to change one line_

<!-- Review 3/4 Good fix, but 'rewrites the whole file' comes from the write tool, not from JSON repair -->

> So you give the agent an edit tool _Cannot run the code_

<!-- Review 4/4 Direct fix -->

> So you give the agent a shell _Cats a 10,000 line file_

<!-- Review 4/4 Direct fix, and catting a huge file is a believable result of having a shell -->

> So you add more tools (Read, search, RAG, fetch, git, browser) _Every service wants a dedicated tool_

<!-- Review 3/4 Read and search fix the cat problem; RAG, fetch, git and browser go beyond it -->

> So you add MCP (Another 100 tools) _Their schemas eat the context_

<!-- Review 4/4 Direct fix, and the problem is a direct result -->

> So you load tools dynamically _Does not know which tools exist_

<!-- Review 4/4 Direct fix, and the problem is a direct result -->

> So you add a tool to search tools (Can call any tool) _One tool returns 50,000 lines and fills the context_

<!-- Review 4/4 Direct fix, and the problem is a direct result -->

> So you cap tool output (Runs for an hour) _The context is full again_

<!-- Review 4/4 Direct fix; 'runs for an hour' shows progress before the next wall -->

> So you compact (Runs for hours) _The provider fails on a normal Tuesday_

<!-- Review 4/4 Direct fix, and the escalating run time works well -->

> So you add retries, limits and resume (Runs all week) _A $1,000 bill arrives_

<!-- Review 4/4 Direct fix; the $1,000 bill is a natural result of running all week -->

> So you add open-weight models (Call the wrong tool) _With made-up arguments_

<!-- Review 3/4 Clear motive from cost, but the problem reads as a continuation of the note ('Call the wrong tool... with made-up arguments'); state it in one line -->

> So you write evals (Real tasks from your own repos; Scored on right tool, right arguments, tests pass) _Every model fails differently_

<!-- Review 3/4 Evals measure the problem rather than fix it; works as 'first you measure' -->

> So you tune for each model (Prompts and tool descriptions per model) _A fix for one model breaks another_

<!-- Review 4/4 Direct fix -->

> So you run the evals on every change (Prompt, tool description, model version) _Passes the evals, still takes all day on a big task_

<!-- Review 4/4 Direct fix; the problem shifts from quality to speed cleanly -->

> So you add sub-agents (Spawn 400 in the background; You keep talking while they work) _Every team wants the agent to work their way_

<!-- Review 3/4 Direct fix, but 'Every team wants the agent to work their way' does not come from sub-agents; it is a new topic -->

> So you add support for hooks, permissions, AGENTS.md and skills (Every team sets its own rules)

<!-- Review 4/4 Direct fix -->

> Congratulations (You have built an agent) _Only works when you ask_

<!-- Review 4/4 Clean act break that sets up the factory -->

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

> Now build the factory (Things should work autonomously) _Only responds when someone types_

<!-- Review 3/4 Follows the act break, but its problem repeats 'Only works when you ask'; keep one of the two -->

> So you add more triggers (Slack, support tickets, prod alerts, failed deploys) _All work happens in silos_

<!-- Review 3/4 Direct fix for 'only responds when someone types'; silos follow loosely (each trigger starts its own agent with its own context), say that to make it land -->

> So you add a shared knowledge base (Agents to keep it in sync) _Every requirement create a PR on Github_

<!-- Review 2/4 Fixes silos, but 'Every requirement creates a PR' is not caused by a knowledge base; it comes from triggers. Typo: 'create' to 'creates', 'Github' to 'GitHub' -->

> So you add a project board (Triage → Spec → Dev → QA → Review) _You have to move every card by hand_

<!-- Review 3/4 The board gives non-PR work a home, so it fixes the previous problem; 'move every card by hand' is a direct result -->

> So you set up rubrics (Agents review against the rubric, humans take the exceptions) _Every adjustment reprocesses all the data_

<!-- Review 2/4 Does not fix 'move every card by hand' now that the board agent step is gone; rubrics answer review load, which is no longer set up. Also 'Every adjustment reprocesses all the data' is vague -->

> So you set up reports (Maintains historical data; Cost per task, cycle time, rework) _The rubrics go stale_

<!-- Review 3/4 Historical data fixes reprocessing; 'rubrics go stale' is plausible but not caused by reports -->

> So you set up goals (An agent tunes the rubrics and workflows to hit them) _It all stops when you close the laptop_

<!-- Review 2/4 Goals fix stale rubrics, but 'It all stops when you close the laptop' is a sudden jump to infra; mark it as the product to infra turn, or end on 'Goals are only checked when you ask' -->

> So you schedule agents (Nightly goal checks, weekly reports) _The nightly run never happens_

<!-- Review 2/4 Scheduling does not fix a closed laptop; the cloud does. If goals end on 'only checked when you ask', scheduling follows directly and its own problem (laptop closed) leads into the cloud -->

> So you run the agent in the cloud (Always on) _You can only reach the agent over SSH_

<!-- Review 4/4 Direct fix, and SSH-only access is a believable result -->

> So you move the control plane out (Any screen can drive the agent, even your phone; The agent crashes mid-run) _The task is lost_

<!-- Review 2/4 Fixes SSH, but the crash in the note is not caused by the control plane; it appears from nowhere -->

> So you make every step durable (Tasks resume where they stopped; The machine is replaced) _Schedules and triggers die with the machine_

<!-- Review 3/4 Fixes lost tasks; schedules and triggers dying with the machine is a fair next limit but not caused by durability -->

> So you move the management plane out (Secrets move to a vault; Sandboxes get short-lived tokens) _The agent loop still runs inside the sandbox_

<!-- Review 3/4 Direct fix; 'The agent loop still runs inside the sandbox' is a fact, not a pain. Something like 'The sandbox dies, the agent dies with it' would land harder -->

> So you move the agent loop out (Sandboxes only run the work; Spun up per task, thrown away after)

<!-- Review 3/4 Fixes the previous problem; ending without a problem works only because Congratulations follows -->

> Congratulations (You have built a simple software factory) _Now scale the factory_

<!-- Review 4/4 Clean close that sets up scaling -->
