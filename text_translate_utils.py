import os
from transformers import MarianMTModel, MarianTokenizer

def translate_text(text, model, tokenizer):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    translated = model.generate(**inputs)
    return tokenizer.batch_decode(translated, skip_special_tokens=True)[0]

if __name__ == "__main__":

    src_lang = "en"
    tgt_lang = "de"
    model_name = f"Helsinki-NLP/opus-mt-{src_lang}-{tgt_lang}"
    model = MarianMTModel.from_pretrained(model_name)
    tokenizer = MarianTokenizer.from_pretrained(model_name)

    text = """Tanzania, home to some of the most breathtaking wildlife on 
    earth. Here in the heart of East Africa, the great Serengeti National Park 
    hosts one of nature's greatest spectacles, the Great Migration. Over a 
    million wildebeest, zebras, and gazelles travel vast distances in search 
    of fresh grass, braving rivers filled with crocodiles. But predators are 
    never far behind. Lions, the kings of the savannah, stalk their prey with 
    patience and precision. Cheetahs, the fastest land animals, chase down 
    their targets in a thrilling display of speed. In the lush Teenager 
    National Park, giant elephants roam freely. These intelligent creatures 
    form strong family bonds, protecting their young from threats. And in the 
    ancient Ngorongoro crater, the endangered black rhino finds refuge, a rare 
    sight in the wild. Tanzania's wildlife is a treasure like no other, a 
    delicate balance of nature that reminds us of the beauty and power of the wild."""

    translated_text = translate_text(text, model, tokenizer)
    print(translated_text)
