class PromptBuilder:
    def __init__(self, system_instruction: str = None):
        self.system_instruction = system_instruction or "You are Zenia, a helpful assistant."

    def build(self, user_text: str, intent, history):
        history_text = "\n".join([f"{h['role']}: {h['text']}" for h in history[-10:]])
        return f"{self.system_instruction}\n\nConversation history:\n{history_text}\n\nUser: {user_text}\nIntent: {intent}\nResponse:"
