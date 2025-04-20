import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, ConversationHandler
from nfa import My_NFA

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Conversation states
SELECT_INITIAL, SELECT_TARGET = range(2)


class BotHandler:
    def __init__(self):
        self.nfa = My_NFA()
        # Add this to track active conversations
        self.active_conversations = set()

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Initialize a new session"""
        context.user_data.clear()
        context.user_data.update({
            'initial': set(),
            'target': set(),
            'page': 0,
            'current_state': SELECT_INITIAL
        })

        await update.message.reply_text(
            "🧪 Alchemy Bot 🧪\n\nFirst, select effects you CURRENTLY HAVE:",
            reply_markup=self.create_effects_keyboard(context)
        )
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
            'current_state': SELECT_INITIAL
        })

        # Edit the current message instead of sending a new one
        await query.edit_message_text(
            "🧪 Alchemy Bot 🧪\n\nFirst, select effects you CURRENTLY HAVE:",
            reply_markup=self.create_effects_keyboard(context)
        )

        return SELECT_INITIAL

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

        # Done button
        if selected:
            keyboard.append([InlineKeyboardButton("🚀 Done", callback_data="done")])

        return InlineKeyboardMarkup(keyboard)

    async def handle_interaction(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle all callbacks"""
        query = update.callback_query
        await query.answer()
        data = query.data

        # Handle restart
        if data == "restart":
            return await self.restart(update, context)

        # Handle state transitions
        current_state = context.user_data['current_state']
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
                context.user_data['current_state'] = SELECT_TARGET
                context.user_data['page'] = 0
                await query.edit_message_text(
                    "Now select effects you NEED TO ACHIEVE:",
                    reply_markup=self.create_effects_keyboard(context)
                )
                return SELECT_TARGET
            else:
                if not context.user_data['target']:
                    await query.edit_message_text("❗ Please select at least one target effect!")
                    return current_state
                return await self.show_result(update, context)

        # Update display
        await query.edit_message_text(
            text="Select effects you CURRENTLY HAVE:" if current_state == SELECT_INITIAL
            else "Select effects you NEED TO ACHIEVE:",
            reply_markup=self.create_effects_keyboard(context)
        )
        return current_state

    async def show_result(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show results with restart option"""
        query = update.callback_query
        user_data = context.user_data

        path, side_effects = self.nfa.find_shortest_path_from_specific_initial(
            user_data['initial'],
            user_data['target']
        )

        response = ["🔮 Result 🔮"]
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
            reply_markup=reply_markup  # Add the keyboard to the message
        )
        # return ConversationHandler.END

    def get_handlers(self):
        return [
            ConversationHandler(
                entry_points=[CommandHandler('start', self.start)],
                states={
                    SELECT_INITIAL: [CallbackQueryHandler(self.handle_interaction)],
                    SELECT_TARGET: [CallbackQueryHandler(self.handle_interaction)]
                },
                fallbacks=[],
                map_to_parent={ConversationHandler.END: ConversationHandler.END},
                allow_reentry=True
            ),
            CallbackQueryHandler(self.restart, pattern="^restart$")
        ]


def main():
    application = Application.builder().token("").build()
    handler = BotHandler()

    application.add_handlers(handler.get_handlers())
    application.run_polling()


if __name__ == "__main__":
    main()