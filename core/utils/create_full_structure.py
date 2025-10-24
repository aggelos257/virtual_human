import os

# === Ορισμός όλων των φακέλων που πρέπει να υπάρχουν ===
folders = [
    "core",
    "core/reasoning",
    "core/memory",
    "core/emotion",
    "core/perception",
    "core/perception/vision",
    "core/dialogue",
    "core/action",
    "core/self",
    "core/learning",
    "core/web",
    "core/utils",
    "voice",
    "gui",
    "data/logs",
    "tools",
]

# === Αρχεία και βασικό placeholder περιεχόμενο ===
files = {
    # Reasoning
    "core/reasoning/world_model.py": "class WorldModel:\n    def __init__(self):\n        pass\n",
    "core/reasoning/reasoner_advanced.py": "class ReasonerAdvanced:\n    def __init__(self, world_model):\n        self.world_model = world_model\n",
    "core/reasoning/meta_reasoner.py": "class MetaReasoner:\n    pass\n",
    "core/reasoning/goal_planner.py": "class GoalPlanner:\n    pass\n",

    # Memory
    "core/memory/memory_episodic.py": "class EpisodicMemory:\n    pass\n",
    "core/memory/memory_semantic.py": "class SemanticMemory:\n    pass\n",
    "core/memory/memory_emotional.py": "class EmotionalMemory:\n    pass\n",
    "core/memory/memory_consolidator.py": "class MemoryConsolidator:\n    pass\n",

    # Emotion
    "core/emotion/emotion_engine.py": "class EmotionEngine:\n    pass\n",
    "core/emotion/emotion_analyzer.py": "class EmotionAnalyzer:\n    pass\n",
    "core/emotion/emotion_responder.py": "class EmotionResponder:\n    pass\n",
    "core/emotion/emotion_state.py": "class EmotionState:\n    pass\n",

    # Perception
    "core/perception/audio_perception.py": "class AudioPerception:\n    pass\n",
    "core/perception/system_awareness.py": "class SystemAwareness:\n    pass\n",
    "core/perception/spatial_awareness.py": "class SpatialAwareness:\n    pass\n",
    "core/perception/vision/vision_manager.py": "class VisionManager:\n    pass\n",
    "core/perception/vision/face_analyzer.py": "class FaceAnalyzer:\n    pass\n",
    "core/perception/vision/object_detector.py": "class ObjectDetector:\n    pass\n",
    "core/perception/vision/gesture_recognizer.py": "class GestureRecognizer:\n    pass\n",

    # Dialogue
    "core/dialogue/dialogue_manager.py": "class DialogueManager:\n    pass\n",
    "core/dialogue/coherence_checker.py": "class CoherenceChecker:\n    pass\n",
    "core/dialogue/dialogue_context.py": "class DialogueContext:\n    pass\n",
    "core/dialogue/conversation_memory.py": "class ConversationMemory:\n    pass\n",

    # Action
    "core/action/action_executor.py": "class ActionExecutor:\n    pass\n",
    "core/action/rpa_controller.py": "class RPAController:\n    pass\n",
    "core/action/system_controller.py": "class SystemController:\n    pass\n",
    "core/action/feedback_monitor.py": "class FeedbackMonitor:\n    pass\n",

    # Self / Consciousness
    "core/self/self_model.py": "class SelfModel:\n    pass\n",
    "core/self/introspection_engine.py": "class IntrospectionEngine:\n    pass\n",
    "core/self/value_system.py": "class ValueSystem:\n    pass\n",

    # Learning
    "core/learning/adaptive_learner.py": "class AdaptiveLearner:\n    pass\n",
    "core/learning/intent_growth.py": "class IntentGrowth:\n    pass\n",
    "core/learning/self_improvement_cycle.py": "class SelfImprovementCycle:\n    pass\n",

    # Web
    "core/web/web_explorer.py": "class WebExplorer:\n    pass\n",
    "core/web/file_explorer.py": "class FileExplorer:\n    pass\n",
    "core/web/api_connector.py": "class APIConnector:\n    pass\n",
    "core/web/knowledge_integrator.py": "class KnowledgeIntegrator:\n    pass\n",

    # Utils
    "core/utils/logger.py": "class Logger:\n    pass\n",
    "core/utils/config_loader.py": "class ConfigLoader:\n    pass\n",
    "core/utils/text_tools.py": "class TextTools:\n    pass\n",
    "core/utils/helper_functions.py": "class HelperFunctions:\n    pass\n",

    # Voice
    "voice/voice_emotion.py": "class VoiceEmotion:\n    pass\n",

    # GUI
    "gui/avatar_controller.py": "class AvatarController:\n    pass\n",
    "gui/face_engine.py": "class FaceEngine:\n    pass\n",

    # Data / Tools
    "data/persona_profile.yaml": "name: Zenia\npersonality: kind\n",
    "tools/diagnostics.py": "print('Diagnostics initialized')\n",
    "tools/maintenance.py": "print('Maintenance module')\n",
}

# === Εκτέλεση δημιουργίας ===
for folder in folders:
    os.makedirs(folder, exist_ok=True)

for path, content in files.items():
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ Created: {path}")
    else:
        print(f"⏩ Exists: {path}")

print("\n🎯 Professional Zenia AI structure created successfully.")
