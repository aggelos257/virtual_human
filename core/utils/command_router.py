class CommandRouter:
    def __init__(self, voice=None, gui=None, system=None):
        self.voice = voice
        self.gui = gui
        self.system = system

    def route(self, command):
        action = command.get("action")
        if action == "say" and self.voice:
            return self.voice.speak(command.get("text", ""))
        return {"status": "unknown_action"}
