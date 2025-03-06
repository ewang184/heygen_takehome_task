### Setup
For a given input video_file, run the following

Note: It will be necessary to agree to coqui terms of non-commercial CPML when running setup_translate

```
docker build -t heygen_docker . --no-cache
docker run -it --name heygen_container heygen_docker /bin/bash
./setup.sh
./setup_translate.sh
./setup_hift.sh
./setup_musetalk.sh
```

### Execution

While inside the docker container

```
./run_translate.sh path_to_video
./run_hift.sh
python replace_audio.py
./run_musetalk.sh path_to_video
```

### Assumptions made
I assumed that translating into German from English would mostly preserve the order of the meaning. 
That is, the order of things mentioned in English would approximately be the order of things mentioned in the german.
Another assumption made is that the time it takes to speak the German translation is approximately that which is
required by the English.

### Limitations
I used a less powerful lip-sync model due to computational constraints. This results in less realistic lip-syncing. 

The assumptions that I made are necessary for realistic-sounding output. Firstly, I assumed that translating into 
German from English would mostly preserve the order of the meaning. This is required for my solution, since I do 
sentence-level alignment and warping, so each sentence is matched together and the German sentence is stretched 
to fit to the English sentence. If this assumption was not made, then it would be possible for the video and audio 
to become extremely unaligned.

I also assumed that the time it takes to speak the English, and the German translation is similar. This is also 
required due to the fact that I used sentence-level alignment and warping. If the times taken to speak in English 
and German were too different, then the shortened/lengthened German speaking would become extremely unnatural.

Another limitation is that due to the sentence level alignment, it is possible for words inside the same sentence
to become misaligned. For example, "Crocodile" might be mentioned at the beginning of an English sentence but
be mentioned at the end of the translation to German.

### Commands to test functionality

## For the following, assume that the setup code has already been run

Test speech-to-text in English

```
python speech_to_text_utils.py
```

Test English to German translation

```
python text_translate_utils.py
```

Test German text to speech

```
python text_to_speech_utils.py
```

Test re-synthesizing speech

```
./run_hift
```

Test lip-syncing

