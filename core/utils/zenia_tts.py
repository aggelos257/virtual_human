import pyttsx3

engine = pyttsx3.init()

# Επιλογή φωνής OneCore (Maria)
for voice in engine.getProperty('voices'):
    if 'Maria' in voice.name or 'el-gr' in voice.id.lower():
        engine.setProperty('voice', voice.id)
        break

engine.setProperty('rate', 160)
engine.setProperty('volume', 1.0)

engine.say("Γεια σου! Είμαι η Ζένια και τώρα μιλάω καθαρά ελληνικά.")
engine.runAndWait()
