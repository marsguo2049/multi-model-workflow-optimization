# Optimization problem

For workflow step \(i\), define an action

\[
a_i = (m_i, c_i, b_i)
\]

where \(m_i\) is the model or backend, \(c_i\) is its configuration, and \(b_i\) is the compute or reasoning budget.

A basic scalar objective is

\[
\max\; Q - \lambda C - \mu T - \gamma R
\]

where \(Q\) is end-to-end quality, \(C\) monetary cost, \(T\) latency, and \(R\) resource use. A constrained or Pareto formulation may be more appropriate when requirements are hard limits.

The problem is stochastic: identical calls can produce different outputs. Stages also interact, so the locally best choice may not yield the best complete workflow. Experiments should therefore use repeated runs, versioned task inputs, explicit seeds where supported, uncertainty estimates, and end-to-end as well as per-stage measurements.

The initial repository contains only data structures and baseline routing hooks. It does not claim to implement or solve this optimization problem yet.
