import simpleaudio as sa


class PlayAudio:
    def run(self, audiofile:str):
        waveobject = sa.WaveObject.from_wave_file(audiofile)
        p = waveobject.play()


actions = {'play audio': PlayAudio}
