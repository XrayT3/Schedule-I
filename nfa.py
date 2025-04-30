import time
from collections import defaultdict, deque

class My_NFA:
    def __init__(self):
        self.all_effects = ['Nothing',
            'Anti-Gravity', 'Athletic', 'Balding', 'Bright-Eyed', 'Calming', 'Calorie-Dense',
            'Cyclopean', 'Disorienting', 'Electrifying', 'Energizing', 'Euphoric', 'Explosive',
            'Focused', 'Foggy', 'Gingeritis', 'Glowing', 'Jennerising', 'Laxative', 'LongFaced',
            'Munchies', 'Paranoia', 'Refreshing', 'Schizophrenia', 'Sedating', 'Seizure-Inducing',
            'Shrinking', 'Slippery', 'Smelly', 'Sneaky', 'Spicy', 'Thought-Provoking', 'Toxic',
            'TropicThunder', 'Zombifying'
        ]
        self.all_ingredients = [
            "Cuke", "Banana", "Paracetamol", "Donut", "Viagra", "Mouth Wash",
            "Flu Medicine", "Gasoline", "Energy Drink", "Motor Oil",
            "Mega Bean", "Chili", "Battery", "Iodine", "Horse Semen", "Addy"
        ]
        self.transitions = defaultdict(lambda: defaultdict(set))
        self.initial_effects = ["Sedating", "Energizing", "Refreshing", "Calming"]
        self.ingredient_default_effects = {
            "Cuke": "Energizing",
            "Banana": "Gingeritis",
            "Paracetamol": "Sneaky",
            "Donut": "Calorie-Dense",
            "Viagra": "TropicThunder",
            "Mouth Wash": "Balding",
            "Flu Medicine": "Sedating",
            "Gasoline": "Toxic",
            "Energy Drink": "Athletic",
            "Motor Oil": "Slippery",
            "Mega Bean": "Foggy",
            "Chili": "Spicy",
            "Battery": "Bright-Eyed",
            "Iodine": "Jennerising",
            "Horse Semen": "LongFaced",
            "Addy": "TropicThunder",
        }
        # Add ingredient prices
        self.ingredient_prices = {
            "Cuke": 2.0,
            "Banana": 2.0,
            "Paracetamol": 3.0,
            "Donut": 3.0,
            "Viagra": 4.0,
            "Mouth Wash": 4.0,
            "Flu Medicine": 5.0,
            "Gasoline": 5.0,
            "Energy Drink": 6.0,
            "Motor Oil": 6.0,
            "Mega Bean": 7.0,
            "Chili": 7.0,
            "Battery": 8.0,
            "Iodine": 8.0,
            "Horse Semen": 9.0,
            "Addy": 9.0,
        }
        # Add effect price factors
        self.effect_price_factors = {
            'Nothing': 0.0,
            'Anti-Gravity': 0.54,
            'Athletic': 0.32,
            'Balding': 0.3,
            'Bright-Eyed': 0.4,
            'Calming': 0.1,
            'Calorie-Dense': 0.28,
            'Cyclopean': 0.56,
            'Disorienting': 0.0,
            'Electrifying': 0.5,
            'Energizing': 0.22,
            'Euphoric': 0.18,
            'Explosive': 0.0,
            'Focused': 0.16,
            'Foggy': 0.36,
            'Gingeritis': 0.2,
            'Glowing': 0.48,
            'Jennerising': 0.42,
            'Laxative': 0.0,
            'LongFaced': 0.52,
            'Munchies': 0.12,
            'Paranoia': 0.0,
            'Refreshing': 0.14,
            'Schizophrenia': 0.0,
            'Sedating': 0.26,
            'Seizure-Inducing': 0.0,
            'Shrinking': 0.6,
            'Slippery': 0.34,
            'Smelly': 0.0,
            'Sneaky': 0.24,
            'Spicy': 0.38,
            'Thought-Provoking': 0.44,
            'Toxic': 0.0,
            'TropicThunder': 0.46,
            'Zombifying': 0.58,
        }
        self.setup_graph()

    def add_edge(self, effect1, ingredient, effect2):
        self.transitions[effect1][ingredient].add(effect2)

    def setup_graph(self):
        # Add edges (effect1, ingredient, effect2) with default effects
        # This means: effect1 + ingredient = effect2 + default_effect

        # Using Cuke
        self.add_edge("Foggy", "Cuke", "Cyclopean")
        self.add_edge("Gingeritis", "Cuke", "Thought-Provoking")
        self.add_edge("Slippery", "Cuke", "Munchies")
        self.add_edge("Munchies", "Cuke", "Athletic")
        self.add_edge("Sneaky", "Cuke", "Paranoia")
        self.add_edge("Euphoric", "Cuke", "Laxative")
        self.add_edge("Toxic", "Cuke", "Euphoric")

        # Using Banana
        self.add_edge("Cyclopean", "Banana", "Energizing")
        self.add_edge("LongFaced", "Banana", "Refreshing")
        self.add_edge("Energizing", "Banana", "Thought-Provoking")
        self.add_edge("Paranoia", "Banana", "Jennerising")
        self.add_edge("Calming", "Banana", "Sneaky")
        self.add_edge("Disorienting", "Banana", "Focused")
        self.add_edge("Focused", "Banana", "Seizure-Inducing")
        self.add_edge("Toxic", "Banana", "Smelly")

        # Using Paracetamol
        self.add_edge("Munchies", "Paracetamol", "Anti-Gravity")
        self.add_edge("Electrifying", "Paracetamol", "Athletic")
        self.add_edge("Glowing", "Paracetamol", "Toxic")
        self.add_edge("Toxic", "Paracetamol", "TropicThunder")
        self.add_edge("Spicy", "Paracetamol", "Bright-Eyed")
        self.add_edge("Foggy", "Paracetamol", "Calming")
        self.add_edge("Calming", "Paracetamol", "Slippery")
        self.add_edge("Paranoia", "Paracetamol", "Balding")
        self.add_edge("Energizing", "Paracetamol", "Paranoia")

        # Using Donut
        self.add_edge("Shrinking", "Donut", "Energizing")
        self.add_edge("Anti-Gravity", "Donut", "Slippery")
        self.add_edge("Jennerising", "Donut", "Gingeritis")
        self.add_edge("Balding", "Donut", "Sneaky")
        self.add_edge("Calorie-Dense", "Donut", "Explosive")
        self.add_edge("Focused", "Donut", "Euphoric")

        # Using Viagra
        self.add_edge("Euphoric", "Viagra", "Bright-Eyed")
        self.add_edge("Athletic", "Viagra", "Sneaky")
        self.add_edge("Laxative", "Viagra", "Calming")
        self.add_edge("Explosive", "Viagra", "Toxic")

        # Using Mouth Wash
        self.add_edge("Calming", "Mouth Wash", "Anti-Gravity")
        self.add_edge("Focused", "Mouth Wash", "Jennerising")
        self.add_edge("Calorie-Dense", "Mouth Wash", "Sneaky")
        self.add_edge("Explosive", "Mouth Wash", "Sedating")

        # Using Flu Medicine
        self.add_edge("Shrinking", "Flu Medicine", "Paranoia")
        self.add_edge("Cyclopean", "Flu Medicine", "Foggy")
        self.add_edge("Electrifying", "Flu Medicine", "Refreshing")
        self.add_edge("Thought-Provoking", "Flu Medicine", "Gingeritis")
        self.add_edge("Calming", "Flu Medicine", "Bright-Eyed")
        self.add_edge("Munchies", "Flu Medicine", "Slippery")
        self.add_edge("Athletic", "Flu Medicine", "Munchies")
        self.add_edge("Laxative", "Flu Medicine", "Euphoric")
        self.add_edge("Euphoric", "Flu Medicine", "Toxic")
        self.add_edge("Focused", "Flu Medicine", "Calming")

        # Using Gasoline
        self.add_edge("Shrinking", "Gasoline", "Focused")
        self.add_edge("Electrifying", "Gasoline", "Disorienting")
        self.add_edge("Disorienting", "Gasoline", "Glowing")
        self.add_edge("Sneaky", "Gasoline", "TropicThunder")
        self.add_edge("Jennerising", "Gasoline", "Sneaky")
        self.add_edge("Euphoric", "Gasoline", "Spicy")
        self.add_edge("Laxative", "Gasoline", "Foggy")
        self.add_edge("Munchies", "Gasoline", "Sedating")
        self.add_edge("Energizing", "Gasoline", "Euphoric")
        self.add_edge("Gingeritis", "Gasoline", "Smelly")
        self.add_edge("Paranoia", "Gasoline", "Calming")

        # Using Energy Drink
        self.add_edge("Focused", "Energy Drink", "Shrinking")
        self.add_edge("Disorienting", "Energy Drink", "Electrifying")
        self.add_edge("Glowing", "Energy Drink", "Disorienting")
        self.add_edge("TropicThunder", "Energy Drink", "Sneaky")
        self.add_edge("Spicy", "Energy Drink", "Euphoric")
        self.add_edge("Foggy", "Energy Drink", "Laxative")
        self.add_edge("Schizophrenia", "Energy Drink", "Balding")
        self.add_edge("Sedating", "Energy Drink", "Munchies")

        # Using Motor Oil
        self.add_edge("Paranoia", "Motor Oil", "Anti-Gravity")
        self.add_edge("Foggy", "Motor Oil", "Toxic")
        self.add_edge("Euphoric", "Motor Oil", "Sedating")
        self.add_edge("Energizing", "Motor Oil", "Munchies")
        self.add_edge("Munchies", "Motor Oil", "Schizophrenia")

        # Using Mega Bean
        self.add_edge("Shrinking", "Mega Bean", "Electrifying")
        self.add_edge("Energizing", "Mega Bean", "Cyclopean")
        self.add_edge("Calming", "Mega Bean", "Glowing")
        self.add_edge("Thought-Provoking", "Mega Bean", "Energizing")
        self.add_edge("Jennerising", "Mega Bean", "Paranoia")
        self.add_edge("Slippery", "Mega Bean", "Toxic")
        self.add_edge("Athletic", "Mega Bean", "Laxative")
        self.add_edge("Sneaky", "Mega Bean", "Calming")
        self.add_edge("Focused", "Mega Bean", "Disorienting")
        self.add_edge("Seizure-Inducing", "Mega Bean", "Focused")

        # Using Chili
        self.add_edge("Shrinking", "Chili", "Refreshing")
        self.add_edge("Anti-Gravity", "Chili", "TropicThunder")
        self.add_edge("Laxative", "Chili", "LongFaced")
        self.add_edge("Sneaky", "Chili", "Bright-Eyed")
        self.add_edge("Athletic", "Chili", "Euphoric")
        self.add_edge("Munchies", "Chili", "Toxic")

        # Using Battery
        self.add_edge("Shrinking", "Battery", "Munchies")
        self.add_edge("Euphoric", "Battery", "Zombifying")
        self.add_edge("Electrifying", "Battery", "Euphoric")
        self.add_edge("Munchies", "Battery", "TropicThunder")
        self.add_edge("Laxative", "Battery", "Calorie-Dense")

        # Using Iodine
        self.add_edge("Refreshing", "Iodine", "Thought-Provoking")
        self.add_edge("Foggy", "Iodine", "Paranoia")
        self.add_edge("Calming", "Iodine", "Balding")
        self.add_edge("Calorie-Dense", "Iodine", "Gingeritis")
        self.add_edge("Toxic", "Iodine", "Sneaky")
        self.add_edge("Euphoric", "Iodine", "Seizure-Inducing")

        # Using Horse Semen
        self.add_edge("Anti-Gravity", "Horse Semen", "Calming")
        self.add_edge("Thought-Provoking", "Horse Semen", "Electrifying")
        self.add_edge("Gingeritis", "Horse Semen", "Refreshing")

        # Using Addy
        self.add_edge("LongFaced", "Addy", "Electrifying")
        self.add_edge("Glowing", "Addy", "Refreshing")
        self.add_edge("Foggy", "Addy", "Energizing")
        self.add_edge("Sedating", "Addy", "Gingeritis")
        self.add_edge("Explosive", "Addy", "Euphoric")

    def get_all_effects(self):
        return self.all_effects

    def find_shortest_path_from_initial(self, initial_effects, target_effects, max_time=3):
        start_time = time.time()  # Record the start time

        initial = frozenset(initial_effects)
        target_set = set(target_effects) - {'Nothing'}

        if target_set.issubset(initial):
            return [], set(initial) - target_set - {'Nothing'}

        visited = set()
        queue = deque([(initial, [])])
        visited.add(initial)

        while queue:
            # Check if 3 seconds have passed
            if time.time() - start_time > max_time:
                break

            current_state, path = queue.popleft()

            # Check if the current state meets target
            if target_set.issubset(current_state):
                side_effects = set(current_state) - target_set
                return path, side_effects - {'Nothing'}

            # Try all possible ingredients
            for ingredient in self.all_ingredients:
                # Compute next state from transitions + default effect
                next_state = set()
                for effect in current_state:
                    next_state.update(self.transitions[effect].get(ingredient, {effect}))

                # Add ingredient's default effect (MANDATORY)
                default_effect = self.ingredient_default_effects.get(ingredient)
                if default_effect:
                    next_state.add(default_effect)

                frozen_next = frozenset(next_state - {'Nothing'})
                if not next_state or frozen_next in visited:
                    continue

                # Format transition string
                sorted_current = ", ".join(sorted(current_state))
                sorted_next = ", ".join(sorted(next_state - {'Nothing'}))
                transition_str = f"{sorted_current} + {ingredient} = {sorted_next}"

                visited.add(frozen_next)
                queue.append((frozen_next, path + [transition_str]))

        return None, False  # No path found

    def solve_knapsack(self, budget=50.0, max_time=10, initial_state=frozenset({'Nothing'})):
        """
        Solves the knapsack problem to find the optimal combination of ingredients
        that maximizes the total effect price factor while staying within budget.

        Args:
            budget: Maximum cost of ingredients allowed
            max_time: Maximum time in seconds for the algorithm to run
            initial_state: starting state of the knapsack problem

        Returns:
            A tuple of (best_price_factor, best_ingredients, resulting_effects)
        """
        start_time = time.time()

        # Initialize with the initial state
        # initial_state = frozenset({'Nothing'})

        # Dictionary to store the best solution for each state (effect combination)
        # Key: frozenset of effects
        # Value: (total_price_factor, total_cost, list_of_ingredients)
        dp = {initial_state: (self._calculate_price_factor(initial_state), 0.0, [])}

        # Queue for BFS traversal
        queue = deque([initial_state])
        visited = {initial_state}

        # Best solution found so far
        best_solution = (self._calculate_price_factor(initial_state), 0.0, [], initial_state)

        while queue and time.time() - start_time < max_time:
            current_state = queue.popleft()

            current_factor, current_cost, current_ingredients = dp[current_state]

            # Try all possible ingredients
            for ingredient in self.all_ingredients:
                # Skip if adding this ingredient would exceed budget
                if current_cost + self.ingredient_prices[ingredient] > budget:
                    continue

                # Compute next state
                next_state = set()
                for effect in current_state:
                    next_state.update(self.transitions[effect].get(ingredient, {effect}))

                # Add ingredient's default effect
                default_effect = self.ingredient_default_effects.get(ingredient)
                if default_effect:
                    next_state.add(default_effect)

                # Remove 'Nothing' effect as it doesn't contribute
                next_state = next_state - {'Nothing'}
                frozen_next = frozenset(next_state)

                # Calculate new price factor and cost
                new_ingredients = current_ingredients + [ingredient]
                new_cost = current_cost + self.ingredient_prices[ingredient]
                new_factor = self._calculate_price_factor(next_state)

                # If this state hasn't been visited or we found a better solution
                if frozen_next not in dp or new_factor > dp[frozen_next][0] or \
                        (new_factor == dp[frozen_next][0] and new_cost < dp[frozen_next][1]):

                    dp[frozen_next] = (new_factor, new_cost, new_ingredients)

                    # Update best solution if needed
                    if new_factor > best_solution[0] or \
                            (new_factor == best_solution[0] and new_cost < best_solution[1]):
                        best_solution = (new_factor, new_cost, new_ingredients, frozen_next)

                    # Add to queue if not visited
                    if frozen_next not in visited:
                        visited.add(frozen_next)
                        queue.append(frozen_next)

        # Return the best solution found
        best_factor, best_cost, best_ingredients, best_effects = best_solution
        return {
            'price_factor': best_factor,
            'total_cost': best_cost,
            'ingredients': best_ingredients,
            'effects': sorted(best_effects)
        }

    def _calculate_price_factor(self, effects):
        """Calculate the total price factor for a set of effects"""
        return sum(self.effect_price_factors.get(effect, 0) for effect in effects)

    def print_solution_path(self, solution):
        """Print the solution path showing how effects evolve with each ingredient"""
        if not solution['ingredients']:
            print("No ingredients used. Initial effects only.")
            return

        current_effects = set(self.initial_effects)
        print(f"Starting with: {', '.join(sorted(current_effects))}")

        for ingredient in solution['ingredients']:
            # Compute next state
            next_effects = set()
            for effect in current_effects:
                next_effects.update(self.transitions[effect].get(ingredient, {effect}))

            # Add ingredient's default effect
            default_effect = self.ingredient_default_effects.get(ingredient)
            if default_effect:
                next_effects.add(default_effect)

            next_effects = next_effects - {'Nothing'}

            print(f"+ {ingredient} (${self.ingredient_prices[ingredient]:.2f}) → {', '.join(sorted(next_effects))}")
            current_effects = next_effects

        print(f"\nFinal effects: {', '.join(sorted(solution['effects']))}")
        print(f"Total price factor: {solution['price_factor']:.2f}")
        print(f"Total cost: ${solution['total_cost']:.2f}")

# Tests
if __name__ == "__main__":

    nfa = My_NFA()
    my_path, sides = nfa.find_shortest_path_from_initial(
        initial_effects={"Energizing"},
        target_effects={ "Euphoric", "Energizing"}
    )
    # Energizing + Banana -> (Thought-Provoking, Gingeritis) + Gasoline -> (Thought-Provoking, Toxic
    print(my_path, sides)

    # Solve it with different budgets
    budgets = [50, 100]

    for my_budget in budgets:
        print(f"\n=== Solving with budget ${my_budget:.2f} ===")
        my_solution = nfa.solve_knapsack(budget=my_budget)
        nfa.print_solution_path(my_solution)