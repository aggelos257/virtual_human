import subprocess

def speak_gr(text, voice="Microsoft Maria"):
    """
    Εκφωνεί ελληνικό κείμενο με τη φωνή Microsoft Maria ή Stefanos (offline).
    Χρησιμοποιεί τον μηχανισμό OneCore των Windows.
    """
    ps_command = f'''
    Add-Type -AssemblyName System.Speech
    $synth = New-Object -ComObject "SAPI.SpVoice"
    $voices = Get-ChildItem "HKLM:\\SOFTWARE\\Microsoft\\Speech_OneCore\\Voices\\Tokens"
    $voice = $voices | Where-Object {{$_.PSChildName -like "*elGR_{voice}*"}}
    if ($voice) {{
        $synth.Voice = $synth.GetVoices().Item(0)
    }}
    $synth.Speak("{text}")
    '''

    subprocess.run(["powershell", "-Command", ps_command], shell=True)

# Δοκιμή
if __name__ == "__main__":
    print("🔊 Δοκιμή φωνής Ζένια (Maria)...")
    speak_gr("Γεια σου! Είμαι η Ζένια, και μιλώ καθαρά ελληνικά, ακόμα και χωρίς σύνδεση στο διαδίκτυο.")
