from ocr import *
from nlp import *
from translate import *
from cefr import *

usage = ["Beginner", "Intermediate", "Pro"]

def main(image_path):
    while(True):
        user_level = input("Write Your English Level: Beginner, Intermediate, Pro\n")
        if(user_level in usage):
            break
        print("Wrong Usage\n")
    
    merged_df = load_and_merge_cefr_data("data/A1A2B1B2.csv", "data/C1C2.csv")
    cefr = group_words_by_cefr(merged_df)
    
    # 1. OCR로 텍스트 추출
    text = extract_text(image_path)
    print("Extracted Text:\n", text)
    for _ in range(3):
        print()

    # 2. NLP로 어려운 단어 식별
    difficult_words = identify_difficult_words(text, user_level, cefr)
    print("Difficult Words:")
    for pos in difficult_words:
        print(pos)
        print(difficult_words[pos])

    # 3. 번역 및 출력
    
    for pos in difficult_words:
        print(pos)
        words = difficult_words[pos]
        for word in words:
            #sentences = get_sentence_examples(word)
            translation = translate_word(word)
            print(f"{word}: {translation}")
            #for sentence in sentences:
            #    print(f"{sentence}")
    

# 테스트 실행
if __name__ == "__main__":
    IMAGE_PATH = "sample_images/paragraph1.jpg"
    main(IMAGE_PATH)
