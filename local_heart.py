from transformers import pipeline

# This downloads the model to your computer (one-time setup)
classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=True)

def get_emotion(text):
    results = classifier(text)
    # Sort to get the strongest emotion
    strongest = max(results[0], key=lambda x: x['score'])
    return strongest

# Test it
# print(get_emotion("I am so excited to build this locally!"))
