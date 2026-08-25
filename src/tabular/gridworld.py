import random

ROWS, COLS = 3, 4
WALLS = {(1, 1)}
TERMINALS = {(0, 3): +1.0, (1, 3): -1.0}
STEP_REWARD = -0.04
ACTIONS = ["^", ">", "v", "<"]
DELTAS = [(-1, 0), (0, 1), (1, 0), (0, -1)]

STATES = [(r, c) for r in range(ROWS) for c in range(COLS) if (r, c) not in WALLS]


def _move(s, a):
    nr, nc = s[0] + DELTAS[a][0], s[1] + DELTAS[a][1]
    if 0 <= nr < ROWS and 0 <= nc < COLS and (nr, nc) not in WALLS:
        return (nr, nc)
    return s  # bump into wall/edge -> stay


def transitions(s, a):
    """The MDP model. Returns list of (prob, next_state, reward, done)."""
    if s in TERMINALS:
        return []
    probs = {}
    for p, act in [(0.8, a), (0.1, (a - 1) % 4), (0.1, (a + 1) % 4)]:
        ns = _move(s, act)
        probs[ns] = probs.get(ns, 0.0) + p
    return [
        (p, ns, TERMINALS.get(ns, STEP_REWARD), ns in TERMINALS)
        for ns, p in probs.items()
    ]


def show(V=None, pi=None):
    for r in range(ROWS):
        row = []
        for c in range(COLS):
            s = (r, c)
            if s in WALLS:
                row.append("  ##  ")
            elif s in TERMINALS:
                row.append(f"{TERMINALS[s]:+.2f} ")
            elif V is not None:
                row.append(f"{V[s]:+.2f} ")
            else:
                row.append(f"  {ACTIONS[pi[s]]}   ")
        print(" ".join(row))
    print()


START = (2, 0)


def reset(explore=False):
    if explore:
        return random.choice([s for s in STATES if s not in TERMINALS])
    return START



def sample_step(s, a):
    """Sample ONE outcome. This is all the agent gets to see."""
    outcomes = transitions(s, a)
    p, ns, r, done = random.choices(outcomes, weights=[o[0] for o in outcomes])[0]
    return ns, r, done
