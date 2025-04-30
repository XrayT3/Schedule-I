import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, ConversationHandler
from nfa import My_NFA

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Conversation states - Add new states for knapsack problem
SELECT_MODE, SELECT_INITIAL, SELECT_TARGET, SELECT_MAX_TIME, SELECT_BUDGET = range(5)


class BotHandler:
    def __init__(self):
        self.nfa = My_NFA()

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Initialize a new session and ask user which mode they want to use"""
        context.user_data.clear()
        context.user_data.update({
            'initial': set(),
            'target': set(),
            'page': 0,
            'current_state': SELECT_MODE,  # Changed initial state to mode selection
            'max_time': 10,  # Default value
            'budget': 50.0,  # Default value
        })

        # Create keyboard for mode selection
        keyboard = [
            [InlineKeyboardButton("🧪 Find Recipe", callback_data="mode_recipe")],
            [InlineKeyboardButton("💰 Maximize Price", callback_data="mode_knapsack")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            "🧪 Alchemy Bot 🧪\n\nChoose operation mode:",
            reply_markup=reply_markup
        )
        return SELECT_MODE

    async def select_mode(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int | None:
        """Handle mode selection"""
        query = update.callback_query
        await query.answer()

        mode = query.data
        if mode == "mode_recipe":
            context.user_data['mode'] = 'recipe'
            await query.edit_message_text(
                "🧪 Recipe Mode 🧪\n\nFirst, select effects you CURRENTLY HAVE:",
                reply_markup=self.create_effects_keyboard(context)
            )
            context.user_data['current_state'] = SELECT_INITIAL
            return SELECT_INITIAL

        elif mode == "mode_knapsack":
            context.user_data['mode'] = 'knapsack'
            await query.edit_message_text(
                "💰 Maximization Mode 💰\n\nSelect your INITIAL EFFECTS:",
                reply_markup=self.create_effects_keyboard(context)
            )
            context.user_data['current_state'] = SELECT_INITIAL
            return SELECT_INITIAL

    async def restart(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Restart the conversation after clicking the restart button"""
        query = update.callback_query
        await query.answer()

        # Clear and reinitialize user data
        context.user_data.clear()
        context.user_data.update({
            'initial': set(),
            'target': set(),
            'page': 0,
            'current_state': SELECT_MODE,  # Changed to mode selection
            'max_time': 10,  # Default value
            'budget': 50.0,  # Default value
        })

        # Create keyboard for mode selection
        keyboard = [
            [InlineKeyboardButton("🧪 Find Recipe", callback_data="mode_recipe")],
            [InlineKeyboardButton("💰 Maximize Price", callback_data="mode_knapsack")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Edit the current message instead of sending a new one
        await query.edit_message_text(
            "🧪 Alchemy Bot 🧪\n\nChoose operation mode:",
            reply_markup=reply_markup
        )

        return SELECT_MODE

    def create_effects_keyboard(self, context, page=None):
        """Create paginated keyboard with effects"""
        if page is None:
            page = context.user_data.get('page', 0)

        effects = self.nfa.get_all_effects()
        keyboard = []
        per_page = 9
        start = page * per_page
        end = start + per_page

        # Add effect buttons
        current_state = context.user_data['current_state']

        # if current_state in [SELECT_INITIAL, SELECT_TARGET]:
        selected = context.user_data['initial'] if current_state == SELECT_INITIAL else context.user_data['target']

        for effect in effects[start:end]:
            emoji = "✅" if effect in selected else "⚪"
            keyboard.append([InlineKeyboardButton(f"{emoji} {effect}", callback_data=f"toggle_{effect}")])

        # Navigation buttons
        nav_buttons = []
        if page > 0:
            nav_buttons.append(InlineKeyboardButton("⬅️ Prev", callback_data="prev_page"))
        if end < len(effects):
            nav_buttons.append(InlineKeyboardButton("Next ➡️", callback_data="next_page"))
        if nav_buttons:
            keyboard.append(nav_buttons)

        # Done button - depends on state
        if current_state in [SELECT_INITIAL, SELECT_TARGET]:
            if context.user_data.get(('initial' if current_state == SELECT_INITIAL else 'target')):
                keyboard.append([InlineKeyboardButton("🚀 Done", callback_data="done")])

        return InlineKeyboardMarkup(keyboard)

    def create_max_time_keyboard(self):
        """Create keyboard for max_time selection"""
        keyboard = [
            [InlineKeyboardButton("3 seconds", callback_data="time_3")],
            [InlineKeyboardButton("10 seconds", callback_data="time_10")],
            [InlineKeyboardButton("30 seconds", callback_data="time_30")],
            [InlineKeyboardButton("60 seconds", callback_data="time_60")]
        ]
        return InlineKeyboardMarkup(keyboard)

    def create_budget_keyboard(self):
        """Create keyboard for budget selection"""
        keyboard = [
            [InlineKeyboardButton("$5", callback_data="budget_5")],
            [InlineKeyboardButton("$15", callback_data="budget_15")],
            [InlineKeyboardButton("$50", callback_data="budget_50")],
            [InlineKeyboardButton("$100", callback_data="budget_100")]
        ]
        return InlineKeyboardMarkup(keyboard)

    async def handle_interaction(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle all callbacks"""
        query = update.callback_query
        await query.answer()
        data = query.data

        # Handle restart
        if data == "restart":
            return await self.restart(update, context)

        # Handle mode selection
        if context.user_data.get('current_state') == SELECT_MODE:
            if data.startswith("mode_"):
                return await self.select_mode(update, context)

        # Handle max_time selection
        if context.user_data.get('current_state') == SELECT_MAX_TIME:
            if data.startswith("time_"):
                context.user_data['max_time'] = int(data.split('_')[1])
                context.user_data['current_state'] = SELECT_BUDGET
                await query.edit_message_text(
                    "Select your budget limit:",
                    reply_markup=self.create_budget_keyboard()
                )
                return SELECT_BUDGET

        # Handle budget selection
        # if context.user_data.get('current_state') == SELECT_BUDGET:
        #     if data.startswith("budget_"):
        #         context.user_data['budget'] = float(data.split('_')[1])
        #         return await self.show_knapsack_result(update, context)
        if context.user_data.get('current_state') == SELECT_BUDGET:
            if data.startswith("budget_"):
                budget = float(data.split('_')[1])
                context.user_data['budget'] = budget
                max_time = context.user_data['max_time']

                # Show waiting message
                await query.edit_message_text(
                    f"⏳ Computing optimal ingredients...\nThis might take up to {max_time} seconds."
                )

                return await self.show_knapsack_result(update, context)

        # Handle other actions
        current_state = context.user_data['current_state']
        mode = context.user_data.get('mode', 'recipe')
        collection = 'initial' if current_state == SELECT_INITIAL else 'target'

        # Process actions
        if data.startswith("toggle_"):
            effect = data[7:]
            if effect in context.user_data[collection]:
                context.user_data[collection].remove(effect)
            else:
                context.user_data[collection].add(effect)
        elif data == "prev_page":
            context.user_data['page'] = max(0, context.user_data['page'] - 1)
        elif data == "next_page":
            context.user_data['page'] += 1
        elif data == "done":
            if current_state == SELECT_INITIAL:
                if not context.user_data['initial']:
                    await query.edit_message_text("❗ Please select at least one initial effect!")
                    return current_state

                if mode == 'recipe':
                    context.user_data['current_state'] = SELECT_TARGET
                    context.user_data['page'] = 0
                    await query.edit_message_text(
                        "Now select effects you NEED TO ACHIEVE:",
                        reply_markup=self.create_effects_keyboard(context)
                    )
                    return SELECT_TARGET
                else:  # knapsack mode
                    context.user_data['current_state'] = SELECT_MAX_TIME
                    await query.edit_message_text(
                        "Select maximum computation time:",
                        reply_markup=self.create_max_time_keyboard()
                    )
                    return SELECT_MAX_TIME
            else:  # current_state == SELECT_TARGET
                if not context.user_data['target']:
                    await query.edit_message_text("❗ Please select at least one target effect!")
                    return current_state
                return await self.show_recipe_result(update, context)

        # Update display
        mode_text = "Recipe" if mode == 'recipe' else "Maximizing"
        prompt_text = {
            SELECT_INITIAL: f"🧪 {mode_text} Mode 🧪\n\nSelect effects you CURRENTLY HAVE:",
            SELECT_TARGET: "Select effects you NEED TO ACHIEVE:"
        }.get(current_state, "Select effects:")

        await query.edit_message_text(
            text=prompt_text,
            reply_markup=self.create_effects_keyboard(context)
        )
        return current_state

    async def show_recipe_result(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show results for recipe path finding with restart option"""
        query = update.callback_query
        user_data = context.user_data

        path, side_effects = self.nfa.find_shortest_path_from_initial(
            user_data['initial'],
            user_data['target']
        )

        response = ["🔮 Recipe Result 🔮"]
        if path is None:
            response.append("❌ Impossible to achieve these effects!")
        else:
            if path:
                response.append("✨ Recipe found:")
                for i, step in enumerate(path, 1):
                    response.append(f"{i}. {step}")
            else:
                response.append("✅ You already have all target effects!")

            if side_effects:
                response.append(f"\n⚠️ Side effects: {', '.join(side_effects)}")
            else:
                response.append("\n🍃 No side effects!")

        # Create restart button keyboard
        keyboard = [[InlineKeyboardButton("🔄 Restart", callback_data="restart")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            text="\n".join(response),
            reply_markup=reply_markup
        )

    async def show_knapsack_result(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show results for knapsack problem with restart option"""
        query = update.callback_query
        user_data = context.user_data

        # Get parameters from user data
        initial_effects = user_data['initial']
        max_time = user_data['max_time']
        budget = user_data['budget']

        # Solve knapsack problem
        solution = self.nfa.solve_knapsack(
            budget=budget,
            max_time=max_time,
            initial_state=frozenset(initial_effects) if initial_effects else frozenset({'Nothing'})
        )

        response = ["💰 Result 💰"]
        response.append(f"Budget: ${budget:.2f} | Computation time: {max_time}s")

        if not solution['ingredients']:
            response.append("\n📋 No ingredients were used (initial effects only)")
        else:
            response.append("\n📋 Optimal ingredients:")
            for i, ingredient in enumerate(solution['ingredients'], 1):
                price = self.nfa.ingredient_prices.get(ingredient, 0)
                response.append(f"{i}. {ingredient} (${price:.2f})")

        response.append(f"\n💎 Final effects: {', '.join(solution['effects'])}")
        response.append(f"💰 Total cost: ${solution['total_cost']:.2f}")
        response.append(f"✨ Effect multiplication: {solution['price_factor']:.2f}")

        # Create restart button keyboard
        keyboard = [[InlineKeyboardButton("🔄 Restart", callback_data="restart")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            text="\n".join(response),
            reply_markup=reply_markup
        )

    def get_handlers(self):
        return [
            ConversationHandler(
                entry_points=[CommandHandler('start', self.start)],
                states={
                    SELECT_MODE: [CallbackQueryHandler(self.handle_interaction)],
                    SELECT_INITIAL: [CallbackQueryHandler(self.handle_interaction)],
                    SELECT_TARGET: [CallbackQueryHandler(self.handle_interaction)],
                    SELECT_MAX_TIME: [CallbackQueryHandler(self.handle_interaction)],
                    SELECT_BUDGET: [CallbackQueryHandler(self.handle_interaction)]
                },
                fallbacks=[],
                map_to_parent={ConversationHandler.END: ConversationHandler.END},
                allow_reentry=True
            ),
            CallbackQueryHandler(self.restart, pattern="^restart$")
        ]


def main():
    token = ""
    application = Application.builder().token().build()
    handler = BotHandler()

    application.add_handlers(handler.get_handlers())
    application.run_polling()


if __name__ == "__main__":
    main()