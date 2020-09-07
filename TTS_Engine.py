from gtts import gTTS
from pygame import mixer, time
from io import BytesIO


def playGTTS(text):
    f = BytesIO()
    gTTS(text=text, lang="en").write_to_fp(f)
    f.seek(0)

    mixer.init()
    mixer.music.load(f)
    mixer.music.play(0)

    clock = time.Clock()
    while mixer.music.get_busy():
        clock.tick(10)


def playMaryTTS(text):
    import wave, struct
    from io import BytesIO
    from marytts import MaryTTS

    marytts = MaryTTS()
    marytts.locale = "en-GB"
    marytts.voice = "dfki-prudence"

    wavs = marytts.synth_wav(text)

    f=BytesIO(wavs)
    f.seek(0)

    mixer.init(wave.open(BytesIO(wavs)).getframerate())
    mixer.music.load(f)
    mixer.music.play(0)

    clock = time.Clock()
    while mixer.music.get_busy():
        clock.tick(10)
