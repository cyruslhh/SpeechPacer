def transcribe_file(speech_file):
    """Transcribe the given audio file. Returns a list of transcribed words and their timestamps"""
    from google.cloud import speech
    import io

    client = speech.SpeechClient()


    with io.open(speech_file, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
        sample_rate_hertz=16000,
        language_code="en-US",
        enable_word_time_offsets=True,
    )

    response = client.recognize(config=config, audio=audio)
    output = []
    # Each result is for a consecutive portion of the audio. Iterate through
    for result in response.results:
        alternative = result.alternatives[0]
        for word in alternative.words:
            output.append(word)
    return output

if __name__ == "__main__":
    print(transcribe_file("/Users/Cyrus2021262_1/Desktop/Coding stuff/SpeechPacer/sample-0.mp3"))