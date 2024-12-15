import spacy

# NLP 모델 로드
nlp = spacy.load("en_core_web_sm")

BEGINNER = "Beginner"
INTERMEDIATE = "Intermediate"
PRO = "Pro"

def generate_known_words(user_level, cefr):
   
    BASIC_WORDS = {
    # 관사
    "a", "an", "the",
    # 대명사
    "i", "you", "he", "she", "it", "we", "they", "me", "him", "her", "us", "them",
    "my", "your", "his", "her", "its", "our", "their", "mine", "yours", "ours", "theirs",
    "this", "that", "these", "those",
    # 전치사
    "in", "on", "at", "by", "with", "for", "to", "from", "of", "about", "over", "under",
    "between", "into", "through", "during", "before", "after", "above", "below",
    # 접속사
    "and", "but", "or", "because", "although", "however", "so", "while", "if", "as", "when", "then",
    # 동사
    "is", "am", "are", "was", "were", "be", "being", "been", "can", "could", "shall", "should",
    "will", "would", "may", "might", "must",
    # 의문사
    "what", "when", "where", "why", "how", "which", "who", "whom", "whose",
    # 숫자
    "one", "two", "three", "first", "second", "third", "many", "few", "some", "most", "all",
    # 기타
    "not", "no", "yes", "up", "down", "out", "there", "here", "now", "then", "just", "only",
    "oh", "wow", "hey", "oops", "ouch", "hmm", "ah", "well", "uh", "um", "hello", "hi",
    "bye", "goodbye", "please", "thank", "sorry", "excuse"
    }
        
    # 사용자 등급별 단어 범위 매핑
    if user_level == BEGINNER:
        levels = {"A1"}
    elif user_level == INTERMEDIATE:
        levels = {"A1", "A2", "B1"}
    elif user_level == PRO:
        levels = {"A1", "A2", "B1", "B2", "C1"}

    # 등급에 해당하는 단어 집합 생성
    known_words = BASIC_WORDS.copy()
    
    for level in levels:
        known_words.update(cefr.get(level, set()))
    
    return known_words

def identify_difficult_words(text, user_level, cefr):
   
    # 사용자 수준에 맞는 known_words 생성
    known_words = generate_known_words(user_level, cefr)

    doc = nlp(text)
    difficult_words = dict()
    person_names = {ent.text.lower() for ent in doc.ents if ent.label_ == "PERSON"}
    eliminate = known_words.union(person_names)
    
    for token in doc:
        lemma = token.lemma_.lower()
        pos = token.pos_
        
        if token.is_alpha and lemma not in eliminate:
            if pos not in difficult_words:
                difficult_words[pos] = set()
            difficult_words[pos].add(lemma)

    return difficult_words