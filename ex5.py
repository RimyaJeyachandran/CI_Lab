import random
from enum import Enum, auto

# --- Constants & Enums ---
class Direction(Enum):
    UP = ( -1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)

    def turn_left(self):
        # Human way to handle rotation: define a clear mapping
        mapping = {Direction.UP: Direction.LEFT, Direction.LEFT: Direction.DOWN, 
                   Direction.DOWN: Direction.RIGHT, Direction.RIGHT: Direction.UP}
        return mapping[self]

    def turn_right(self):
        mapping = {Direction.UP: Direction.RIGHT, Direction.RIGHT: Direction.DOWN, 
                   Direction.DOWN: Direction.LEFT, Direction.LEFT: Direction.UP}
        return mapping[self]

# --- Core Objects ---

class Room:
    def __init__(self):
        self.has_wumpus = False
        self.has_pit = False
        self.has_gold = False
        self.stench = False
        self.breeze = False
        self.glitter = False

    def __str__(self):
        if self.has_wumpus: return "W"
        if self.has_pit: return "P"
        if self.has_gold: return "G"
        return "."

class WumpusWorld:
    def __init__(self, size=4):
        self.size = max(4, size)
        self.grid = {(r, c): Room() for r in range(self.size) for c in range(self.size)}
        self.start_pos = (0, 0)
        self._populate_world()

    def _get_adjacent(self, r, c):
        adj = []
        for dr, dc in [(0,1), (0,-1), (1,0), (-1,0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.size and 0 <= nc < self.size:
                adj.append((nr, nc))
        return adj

    def _populate_world(self):
        # 1. Place Wumpus
        w_pos = self._get_random_empty_pos()
        self.grid[w_pos].has_wumpus = True
        for pos in self._get_adjacent(*w_pos):
            self.grid[pos].stench = True

        # 2. Place Gold
        g_pos = self._get_random_empty_pos()
        self.grid[g_pos].has_gold = True
        self.grid[g_pos].glitter = True

        # 3. Place Pits (20% coverage)
        num_pits = int(0.2 * (self.size**2))
        for _ in range(num_pits):
            p_pos = self._get_random_empty_pos()
            self.grid[p_pos].has_pit = True
            for pos in self._get_adjacent(*p_pos):
                self.grid[pos].breeze = True

    def _get_random_empty_pos(self):
        while True:
            pos = (random.randint(0, self.size-1), random.randint(0, self.size-1))
            room = self.grid[pos]
            if pos != self.start_pos and not (room.has_wumpus or room.has_pit or room.has_gold):
                return pos

    def display(self, agent_pos):
        print("\n--- World Map ---")
        for r in range(self.size):
            row_str = ""
            for c in range(self.size):
                if (r, c) == agent_pos:
                    row_str += "A "
                else:
                    row_str += f"{self.grid[(r, c)]} "
            print(row_str)

# --- Game Engine ---

def play_game():
    size = int(input("Enter grid size (min 4): ") or 4)
    world = WumpusWorld(size)
    
    pos = world.start_pos
    direction = Direction.RIGHT
    score = 100
    has_arrow = True
    
    print("\nObjective: Find the gold (G) and grab it. Avoid the Wumpus (W) and Pits (P)!")

    while True:
        room = world.grid[pos]
        world.display(pos)
        
        print(f"Pos: {pos} | Facing: {direction.name} | Score: {score}")
        
        # Sense surroundings
        if room.stench: print(">> You smell a terrible stench...")
        if room.breeze: print(">> You feel a cold breeze...")
        if room.glitter: print(">> Something is glittering nearby!")

        action = input("\nAction [F]orward, [L]eft, [R]ight, [G]rab, [S]hoot, [Q]uit: ").upper()

        if action == 'F':
            dr, dc = direction.value
            new_pos = (pos[0] + dr, pos[1] + dc)
            if new_pos in world.grid:
                pos = new_pos
                score -= 1
            else:
                print("!! BUMP! You hit a wall.")
        
        elif action == 'L': direction = direction.turn_left()
        elif action == 'R': direction = direction.turn_right()
        
        elif action == 'G':
            if room.has_gold:
                print("\n*** YOU FOUND THE GOLD! YOU WIN! ***")
                score += 1000
                break
            else:
                print("Nothing to grab here.")

        elif action == 'S':
            if has_arrow:
                score -= 10
                has_arrow = False
                print("You fire an arrow into the darkness...")
                # Simplified shoot logic: check line of sight
                dr, dc = direction.value
                check_r, check_c = pos[0] + dr, pos[1] + dc
                while (check_r, check_c) in world.grid:
                    if world.grid[(check_r, check_c)].has_wumpus:
                        print(">> A blood-curdling SCREAM echoes! The Wumpus is dead.")
                        world.grid[(check_r, check_c)].has_wumpus = False
                        break
                    check_r += dr
                    check_c += dc
            else:
                print("No arrows left!")

        elif action == 'Q': break

        # Check for death
        if world.grid[pos].has_wumpus:
            print("\nGAME OVER: The Wumpus had a delicious snack (you).")
            score -= 1000
            break
        if world.grid[pos].has_pit:
            print("\nGAME OVER: You fell into a bottomless pit.")
            score -= 1000
            break
        if score <= 0:
            print("\nGAME OVER: You ran out of energy.")
            break

    print(f"Final Score: {score}")

if __name__ == "__main__":
    play_game()