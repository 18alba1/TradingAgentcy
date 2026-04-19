'''
Purpose:
Defines how system runs step-by-step.

Example responsibilities:

run technical agent
run sentiment agent
run fundamental agent
run debate
run decision agent

Think of it as:

“the manager of all agents”

If using LangGraph:

This file defines:

nodes (agents)
edges (flow between them)
state (shared data object)

Defines:

nodes (functions)
edges (flow)
entry point
final output'''