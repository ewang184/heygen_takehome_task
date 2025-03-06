# Overview

This is the repository for the HeyGen takehome task - translation of the audio of a video from English to German.

The methodology is as follows:

The code is broken into three stages - English speech to German speech, speech re-synthesis, and lip-syncing

For the English speech to German speech, this is further broken down into English speech->English text, text translation, and German text->German speech

For English speech->English text, a whisper model is used for transcription.

For text translation, the MarianMT model is used.

For German text->German speech, the following is done: 
- First, each sentence is spoken in German by the XTTS-V2 model from coqui. The original English speech is passed in as reference input to maintain vocal quality, tone, etc.

- Then, the English sentence timings are found. This is done through [forced alignment](https://pytorch.org/audio/stable/tutorials/forced_alignment_tutorial.html). Specifically, the english is time-aligned, and the timings of the ends of the sentences are found.

- Finally, the sentences spoken in German are stretched/compressed in order to align with their English counterparts. 

Speech re-synthesis is done with a vocoder. I chose to use a neural vocoder called HiFTNet.

Lip-syncing is done with MuseTalk. This is a model with U-net backbone, VAE encoders, and whisper time synchronization.

# Setup
For a given input video_file, move the file to the root directory and run the following.

Note: It will be necessary to agree to coqui terms of non-commercial CPML when running setup_translate

```
docker build -t heygen_docker .
docker run -it --name heygen_container heygen_docker /bin/bash
source setup_translate.sh
source setup_hift.sh
source setup_musetalk.sh path_to_video
```

# Execution
While inside the docker container

```
source run_translate.sh
source run_hift.sh
source run_musetalk.sh path_to_video
```



# Assumptions made
I assumed that translating into German from English would mostly preserve the order of the meaning. 
That is, the order of things mentioned in English would approximately be the order of things mentioned in the german.
Another assumption made is that the time it takes to speak the German translation is approximately that which is
required by the English. 

The major assumption made is that the number of sentences in the translated German is the same as the English.
This assumption is made due to time constraints in implementation - I realized this issue at the end of the allotted 
time frame. In view of the fact that it takes me quite a while to re-test everything I decided to leave this issue
in, since the current code runs. 

This issue can actually be resolved by doing sentence-level translation, and if the English is translated into
multiple sentences in German, it is possible to just align the multiple German sentences to the single English one. 
However, this would reduce translation quality.

# Limitations
I used a less powerful lip-sync model due to computational constraints. This results in less realistic lip-syncing. 

In addition, this model has the downside that it appears that mouth size in inference is strongly affected by a
hyperparameter that must be provided at runtime. I manually searched for a good hyperparameter since their 
recommended ones do not appear to be natural for this specific video (in my opinion). However, there is no guarantee
that any fixed hyperparameter is good over all videos, so it may be necessary to repeat this process for different videos

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

# Commands to test functionality

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
Also, please make sure that Tanzania-2.mp4 is in the root directory.
Also note that running German text to speech demo may overwrite current stored data.

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
