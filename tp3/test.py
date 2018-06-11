from collections import defaultdict

def get_shoots(shots, boats, c=None):
    if shots == 0:
        yield c
        return

    for i in range(boats):
        p = c or [0] * boats
        p[i] += 1
        for e in get_shoots(shots - 1, boats, p):
            yield e
        p[i] -= 1


def print_level(hitpoints, dmg_grid):
    assert len(hitpoints) == len(dmg_grid)
    for hp, row in zip(hitpoints, dmg_grid):
        print(hp, row)


def boats_left(hitpoints, damage):
    count = 0
    for hp, dmg in zip(hitpoints, damage):
        if hp > dmg:
            count += 1
    return count


def hit_boat(D, dmg, dmg_grid, hitpoints, turn, shots_left, total_shots, seq, points):
    column = turn % len(dmg_grid[0])
    if D['best_case'] <= points:
        return 999999999999999999999, tuple()
    if len(seq) > 0 and (turn, shots_left, tuple(dmg)) in D:
        return D[(column, shots_left, tuple(dmg))]

    if shots_left == 0 or boats_left(hitpoints, dmg) == 0:        
        new_pts = boats_left(hitpoints, dmg)
        if new_pts > 0:
            pts, prev_seq = hit_boat(D, dmg, dmg_grid, hitpoints, turn + 1, total_shots, total_shots, [], points + new_pts)
            D[(column, shots_left, tuple(dmg))] = (pts, tuple(seq) + prev_seq)
        else:
            D[(column, shots_left, tuple(dmg))] = (points, tuple(seq))
            if D['best_case'] > points:
                D['best_case'] = points
        return D[(column, shots_left, tuple(dmg))]
    else:
        min_pts = 999999999999999999999
        min_prev_seq = None
        for b in range(len(hitpoints)):
            if dmg[b] >= hitpoints[b]:
                continue
            seq.append(b)
            dmg[b] += dmg_grid[b][column]
            pts, prev_seq = hit_boat(D, dmg, dmg_grid, hitpoints, turn, shots_left - 1, total_shots, seq, points)
            if pts <= min_pts:
                min_pts = pts
                min_prev_seq = prev_seq
            dmg[b] -= dmg_grid[b][turn % len(dmg_grid[0])]
            seq.pop()
        assert min_prev_seq is not None, (turn, seq)
        D[(column, shots_left, tuple(dmg))] = (min_pts, min_prev_seq)
        return D[(column, shots_left, tuple(dmg))]


def solve_game(dmg_grid, hitpoints, num_shots):
    D = defaultdict(dict)
    D['best_case'] = 999999999999999999999999
    return hit_boat(D, [0] * len(hitpoints), dmg_grid, hitpoints, 0, num_shots, num_shots, [], 0)


if __name__ == '__main__':
    level = [
        [0, 0, 35, 1, 1, 15, 20, 40],
        [0, 105, 30, 20, 10, 25, 10, 40],
        [0, 5, 20, 40, 5, 1, 20, 20],
    ]
    boats_health = [35, 105, 41]
    print_level(boats_health, level)
    shots_per_turn = 1

    solution = solve_game(level, boats_health, shots_per_turn)
    print(solution)
    print()

    for turn, s in enumerate(solution[1]):
        dmg = level[s][(turn / shots_per_turn) % len(level[0])]
        boats_health[s] -= dmg
        print('{} ({})'.format(boats_health, dmg))
