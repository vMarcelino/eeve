import simpleaudio as sa


class PlayAudio:
    def run(self, audiofile:str):
        """Plays selected audio file
        
        Arguments:
            audiofile {str} -- audio file path
        """
        waveobject = sa.WaveObject.from_wave_file(audiofile)
        p = waveobject.play()


actions = {'play audio': PlayAudio}
