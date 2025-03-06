### Setup
For a given input video_file, move the file to the root directory and run the following

Note: It will be necessary to agree to coqui terms of non-commercial CPML when running setup_translate

```
docker build -t heygen_docker .
docker run -it --name heygen_container heygen_docker /bin/bash
source setup_translate.sh
source setup_hift
source setup_musetalk
```

### Execution

While inside the docker container

```
python translate_audio path_to_video
./run_hift.sh
python replace_audio.py
./run_musetalk.sh path_to_video output_resynthesized.wav
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

Also, there is some crackling heard throughout the video due to the time-warping of the sentences. I attempted to address
this issue by doing audio re-synthesis with a vocoder, with limited success.

Another issue is that the lipsync generation, even after switching to a more lightweight model, is still quite slow.

Finally, some of the resources I used require different versions of the same python libraries. This results in 
using multiple venvs and switching between them, and the ease of using the program can be improved here.

### Commands to test functionality

## For the following, assume that the setup code has already been run

Test re-synthesizing speech

```
./run_hift
```

Test lip-syncing

```
./run_musetalk path_to_video path_to_audio
```

In addition, before running the following, make sure that heygen_env from running setup_translate.sh is activated

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

Test speech to text alignment

```
python speech_to_text_align.py
```
