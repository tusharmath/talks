# So you want to build a software factory? (story outline)

Format: `> So you ... (additional info) _problem_`

<!-- Review scores: how connected the story is at each step
4 The previous problem forces this step, and this step causes its own problem
3 Clear fix, but one side is loose (the problem is a new topic, or the fix is indirect)
2 Noticeable jump: the fix or the problem does not follow
1 No connection

Agent act: average 3.7, tight throughout
Factory act: average 3.8; product track (triggers to goals), then infra track (schedule to agent loop). Remaining 3s: the PR flood leans on a note, goals mark the turn to infra, and the control plane restart
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

> Now build the factory (Things should work without you asking)

<!-- Review 4/4 Picks up 'Only works when you ask' from the act break without repeating it -->

> So you add more triggers (Slack, support tickets, prod alerts, failed deploys; Each trigger starts its own agent from zero) _All work happens in silos_

<!-- Review 4/4 Direct fix for 'only works when you ask'; the note says why the silos happen -->

> So you add a shared knowledge base (Agents keep it in sync; Every agent now has enough context to act) _Every request becomes a PR on GitHub_

<!-- Review 3/4 Fixes silos; the PR flood follows from agents now being able to act on everything, though it leans on the note -->

> So you add a project board (Triage → Spec → Dev → QA → Review; Not everything needs a PR) _You have to move every card by hand_

<!-- Review 4/4 Direct fix, and moving cards by hand is a direct result -->

> So you set up an agent to run the board (Every card moves itself; Verification agents run QA and attach artifacts) _Agents now ship faster than you can review_

<!-- Review 4/4 Direct fix; review load is a direct result of cards moving on their own -->

> So you set up rubrics (Agents review against the rubric, humans take the exceptions) _You cannot tell if the rubrics are working_

<!-- Review 4/4 Direct fix for review load; a rubric is only as good as its results, which sets up reports -->

> So you set up reports (Cost per task, cycle time, rework; Kept over time) _Someone has to read them and tune the rubrics_

<!-- Review 4/4 Direct fix; the numbers create work for a human, which sets up goals -->

> So you set up goals (An agent tunes the rubrics and workflows to hit them) _Goals are only checked when you ask_

<!-- Review 3/4 Direct fix; the problem is the product to infra turn and echoes the act break, which helps the audience see the shift -->

> So you schedule agents (Nightly goal checks, weekly reports) _It all stops when you close the laptop_

<!-- Review 4/4 Direct fix, and the laptop is the obvious next limit -->

> So you run the agent in the cloud (Always on) _You can only reach the agent over SSH_

<!-- Review 4/4 Direct fix, and SSH-only access is a believable result -->

> So you move the control plane out (Any screen can drive the agent, even your phone; Tasks now run for days) _The machine restarts and the task is lost_

<!-- Review 3/4 Direct fix; longer tasks make a restart likely, though the restart itself is not caused by the control plane -->

> So you make every step durable (Tasks resume where they stopped) _Schedules and triggers die with the machine_

<!-- Review 4/4 Direct fix; tasks survive but what lives on the machine does not -->

> So you move the management plane out (Schedules and triggers run as their own service; Secrets move to a vault; Sandboxes get short-lived tokens) _The sandbox dies, the agent dies with it_

<!-- Review 4/4 Direct fix; the agent loop is the last thing still tied to the machine -->

> So you move the agent loop out (Sandboxes only run the work; Spun up per task, thrown away after)

<!-- Review 4/4 Direct fix, and it ends the infra track cleanly before the close -->

> Congratulations (You have built a simple software factory) _Now scale the factory_

<!-- Review 4/4 Clean close that sets up scaling -->
