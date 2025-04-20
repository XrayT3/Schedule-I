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

    def find_shortest_path_from_specific_initial(self, initial_effects, target_effects):
        start_time = time.time()  # Record the start time

        initial = frozenset(initial_effects)
        target_set = set(target_effects)

        if target_set.issubset(initial):
            return [], set(initial) - target_set - {'Nothing'}

        visited = set()
        queue = deque([(initial, [])])
        visited.add(initial)

        while queue:
            # Check if 3 seconds have passed
            if time.time() - start_time > 3:
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


# Run all tests
# if __name__ == "__main__":
#
#     nfa = My_NFA()
#     path, sides = nfa.find_shortest_path_from_specific_initial(
#         initial_effects={"Energizing"},
#         target_effects={ "Euphoric", "Energizing"}
#     )
#     # Energizing + Banana -> (Thought-Provoking, Gingeritis) + Gasoline -> (Thought-Provoking, Toxic
#     print(path, sides)