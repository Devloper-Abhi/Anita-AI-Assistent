
## Starting Steps :


Install modules

```bash
  pip install pywhatkit SpeechRecognition pyttsx3 wikipedia transformers torch beautifulsoup4 requests pyaudio

```
Also you can make this requirement.txt file and run it:


         modules = [
            "pywhatkit",
            "SpeechRecognition",
            "pyttsx3",
            "wikipedia-api",
            "transformers",
            "torch",
            "beautifulsoup4",
            "requests"
            ]

        with open('requirements.txt', 'w') as f:
            for module in modules:
                f.write(f"{module}\n")

Run this :

```bash
  pip install -r requirements.txt
```
