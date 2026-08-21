<div data-testid="assistant-message" class="message_07S1Yg timelineMessage_07S1Yg  "><span class="root_-a7MRw"><p>Yes, it's a good plan — and the screenshot tells me why. Your LLM series already has the thing most from-scratch series lack: each notebook poses a <strong>claim and then measures whether it survives</strong> ("10's collapse argument, and why it stops at the product", "is it the gate, or is it the parameters?"). That's the asset. Carry it over directly.</p>
<p>Three honest notes before the roadmap:</p>
<p><strong>RL from scratch is the most-written subject in ML.</strong> Sutton &amp; Barto, Spinning Up, Lilian Weng, a thousand Medium posts. A notebook that explains value iteration on a gridworld competes with all of them and loses. A notebook that says <em>"policy iteration converged in 4 iterations and value iteration took 180 — here's why that comparison is a lie"</em> does not. Every notebook needs a question whose answer you didn't know before you ran it.</p>
<p><strong>Aim the series at RLHF/GRPO.</strong> You already have an LLM series. If the RL series terminates in RL-for-language-models, the two arcs join and you own an unusual position: someone who built the transformer <em>and</em> the policy-gradient machinery from scratch, and can explain GRPO without hand-waving either half. That's the part researchers actually care about right now, and almost nobody arriving at RLHF has the tabular foundation underneath it. Notebooks 01–13 are the setup; the last stretch is the payoff.</p>
<p><strong>On X, for the goal you stated:</strong> tutorial threads get likes from learners, not replies from researchers. What gets replies is a surprising measurement, a clean plot, or a mild contradiction of received wisdom. Post the <em>finding</em>, and let the blog link be where the explanation lives. Also — consistency compounds far more than any single post. 20 posts over 5 months beats one that does well.</p>
<hr>
<h2 aria-level="5">Roadmap</h2>
<p><strong>Phase 1 — Tabular</strong> (the whole phase on one gridworld you write yourself)</p>
<table><thead><tr><th>#</th><th>Topic</th><th>The question</th></tr></thead><tbody><tr><td>01</td><td>Value &amp; policy iteration</td><td>Are they two algorithms or one?</td></tr><tr><td>02</td><td>Monte Carlo control</td><td>What does it cost to drop the model?</td></tr><tr><td>03</td><td>TD(0), SARSA, Q-learning</td><td>Why does bootstrapping beat waiting for the return?</td></tr><tr><td>04</td><td>Exploration</td><td>ε-greedy vs optimism vs UCB — does the fancy one earn it?</td></tr><tr><td>05</td><td>n-step &amp; TD(λ)</td><td>Where's the bias/variance optimum, empirically?</td></tr><tr><td>06</td><td>Dyna-Q, model-based</td><td>How many real steps does a learned model buy you?</td></tr></tbody></table>
<p><strong>Phase 2 — Approximation</strong></p>
<table><thead><tr><th>#</th><th>Topic</th><th>The question</th></tr></thead><tbody><tr><td>07</td><td>Linear FA, tile coding, the deadly triad</td><td>Can you <em>make</em> it diverge on purpose?</td></tr><tr><td>08</td><td>DQN</td><td>Which of replay/target-net is load-bearing?</td></tr><tr><td>09</td><td>Double, dueling, PER</td><td>Rainbow's ablation, reproduced small</td></tr></tbody></table>
<p><strong>Phase 3 — Policy gradient</strong></p>
<table><thead><tr><th>#</th><th>Topic</th><th>The question</th></tr></thead><tbody><tr><td>10</td><td>REINFORCE, the score function</td><td>Why is the gradient estimator so noisy?</td></tr><tr><td>11</td><td>Baselines &amp; actor-critic</td><td>Baseline = variance reduction with zero bias — verify it</td></tr><tr><td>12</td><td>GAE</td><td>λ as the same knob as notebook 05</td></tr><tr><td>13</td><td>TRPO → PPO</td><td>What is the clip actually protecting you from?</td></tr><tr><td>14</td><td>SAC / continuous control</td><td>Entropy as a first-class objective</td></tr></tbody></table>
<p><strong>Phase 4 — RL for LLMs</strong> (the join with your LLM series)</p>
<table><thead><tr><th>#</th><th>Topic</th><th>The question</th></tr></thead><tbody><tr><td>15</td><td>Bandits → preference learning</td><td>Bradley-Terry, reward models from pairs</td></tr><tr><td>16</td><td>RLHF with PPO</td><td>The full loop on a tiny LM</td></tr><tr><td>17</td><td>DPO</td><td>Is the RL step removable?</td></tr><tr><td>18</td><td>GRPO &amp; verifiable rewards</td><td>Why did the critic get deleted?</td></tr></tbody></table>
<p>Commit publicly to Phase 1 only. Six notebooks is a finishable promise; eighteen is how series die at number four.</p>
<p><strong>One structural decision that pays off all series long:</strong> write a single tiny gridworld — deterministic and slippery variants, with <code>p(s',r|s,a)</code> exposed as an actual array — and reuse it through notebook 06 at minimum. Don't reach for Gymnasium yet; DP needs the transition table visible, and having identical environments and seeds means notebook 05 can plot against notebook 03's curve. Your LLM series already does this ("same data skeleton as 03–10"). Same move here.</p>
<hr>
<h2 aria-level="5">Notebook 01 — Value &amp; policy iteration</h2>
<p><strong>Title candidate:</strong> <em>RL · 01 — Value iteration and policy iteration are the same algorithm</em></p>
<p>That's the punchline, and it's true: they're the two endpoints of modified policy iteration with <code>k</code> evaluation sweeps. <code>k=1</code> is value iteration, <code>k=∞</code> is policy iteration. Most treatments present them as siblings and never close the loop. You close it with a measurement.</p>
<p><strong>Structure</strong></p>
<ol>
<li><strong>The gridworld</strong> — 5×5 or so, one goal, one pit, walls. Show <code>P</code> and <code>R</code> as arrays. Step-cost of −1 so shortest-path behavior is visible.</li>
<li><strong>Policy evaluation</strong> — iterative, until <code>Δ &lt; θ</code>. Plot <code>V</code> as a heatmap after sweeps 1, 2, 5, 20. The value visibly spreads outward from the goal.</li>
<li><strong>Policy iteration</strong> — evaluate to convergence, act greedily, repeat. Report iterations to convergence (it'll be tiny — 3 to 6).</li>
<li><strong>Value iteration</strong> — one backup, max over actions. Report iterations (much larger).</li>
<li><strong>The correction</strong> — that comparison is unfair. Count <em>Bellman backups</em>, not outer iterations. Re-plot. This is the notebook's first real finding.</li>
<li><strong>The grid</strong> — your SwiGLU-style 2×2, except make it <code>k ∈ {1, 2, 5, 20, ∞} × γ ∈ {0.9, 0.99}</code>, measuring total backups to optimality. The minimum usually sits at small-but-not-1 <code>k</code>, and the two named algorithms are just the edges of your table.</li>
</ol>
<p><strong>Findings worth building the notebook around</strong> (all of them are real, all cheap to measure):</p>
<ul>
<li><strong>The policy is optimal long before the values are.</strong> Extract the greedy policy after every VI sweep and plot two curves: <code>‖V − V*‖∞</code> and "is the greedy policy optimal yet". The policy locks in dramatically earlier. This is the single best plot in the notebook, and it justifies the entire rest of the field — nobody in deep RL has accurate values, and it doesn't matter.</li>
<li><strong>γ controls convergence rate, not just horizon.</strong> Iterations scale roughly as <code>1/(1−γ)</code>. γ=0.99 costs ~10× γ=0.9. And it changes the <em>answer</em>: put a risky shortcut next to the pit and low γ takes it.</li>
<li><strong>Sweep order matters, and nobody mentions it.</strong> In-place (Gauss-Seidel) updates beat synchronous ones, and sweeping states in reverse order from the goal propagates value across the whole grid in a single pass. Same algorithm, order-of-magnitude difference. Good animated-heatmap material.</li>
</ul>
<p><strong>Keep out of 01:</strong> the full MDP formalism (a paragraph, not a section), function approximation, anything stochastic beyond a slippery variant. Save exploration entirely — DP doesn't explore, and noticing that out loud sets up notebook 02.</p>
<p><strong>The X post for it:</strong></p>
<blockquote>
<p>Most RL courses teach value iteration and policy iteration as two algorithms.</p>
<p>They're one algorithm with a knob.</p>
<p>[heatmap grid image: backups-to-optimality across k × γ]</p>
<p>Also: the optimal policy appears ~4x earlier than converged values. Which is why deep RL works at all despite never having accurate values.</p>
<p>Notebook 01 of a from-scratch RL series → [link]</p>
</blockquote>
<p>Lead with the claim, put the plot second, link last. Don't thread it unless you have three genuinely separate findings.</p></span></div>
