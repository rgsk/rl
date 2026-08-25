from gridworld import STATES, TERMINALS, show, transitions


def q_value(s, a, V, gamma=1.0):
    total = 0.0
    for p, ns, r, d in transitions(s, a):
        total += p * (r + gamma * V[ns])
    return total

def value_iteration(gamma=1.0, theta=1e-6, verbose=False):
    V = {s: 0.0 for s in STATES}
    for sweep in range(1000):
        delta = 0.0
        for s in STATES:
            if s in TERMINALS:
                continue  # terminals are worth 0 by definition
            old = V[s]
            V[s] = max(
                q_value(s, a, V, gamma) for a in range(4)
            )  # max q_value over the 4 actions
            delta = max(delta, abs(V[s] - old))
        if verbose:
            print(f"sweep {sweep + 1}, delta={delta:.4f}")
            show(V=V)
        if delta < theta:
            print(f"converged in {sweep + 1} sweeps")
            break
    return V

def greedy_policy(V, gamma=1.0):
    pi = {}
    for s in STATES:
        if s in TERMINALS:
            continue
        pi[s] = max(range(4), key=lambda a: q_value(s, a, V, gamma))
    return pi