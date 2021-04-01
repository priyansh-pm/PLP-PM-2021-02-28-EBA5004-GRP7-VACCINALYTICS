import string
import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Embedding
from tensorflow.keras.preprocessing.sequence import pad_sequences

f = open("vaccine-facts.txt", "r", encoding='utf-8')
file_read = f.read()

data = file_read.split('\n')

dead_list = file_read.split(" ")
print(len(set(dead_list)))

data = " ".join(data)


# Data pre-processing and cleaning
def clean_text(doc):
    tokens = doc.split()
    table = str.maketrans('', '', string.punctuation)
    tokens = [w.translate(table) for w in tokens]
    tokens = [word for word in tokens if word.isalpha()]
    tokens = [word.lower() for word in tokens]
    return tokens


tokens = clean_text(data)

length = 8 + 1
lines = []

for i in range(length, len(tokens)):
    seq = tokens[i - length: i]
    line = ' '.join(seq)
    lines.append(line)

# Build LSTM model as well as prepare X and Y

tokenizer = Tokenizer()
tokenizer.fit_on_texts(lines)
sequences = tokenizer.texts_to_sequences(lines)

sequences = np.array(sequences)
X, y = sequences[:, :-1], sequences[:, -1]

vocab_size = len(tokenizer.word_index) + 1
y = to_categorical(y, num_classes=vocab_size)

seq_length = X.shape[1]

# LSTM model
model = Sequential()
model.add(Embedding(vocab_size, 8, input_length=seq_length))
model.add(LSTM(100, return_sequences=True))
model.add(LSTM(100))
model.add(Dense(100, activation='relu'))
model.add(Dense(vocab_size, activation='softmax'))

print(model.summary())

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

model.fit(X, y, batch_size=256, epochs=500)


def generate_sequence(model, tokenizer, text_seq_length, seed_text, n_words):
    text = []
    for _ in range(n_words):
        encoded = tokenizer.texts_to_sequences([seed_text])[0]
        encoded = pad_sequences([encoded], maxlen=text_seq_length, truncating='pre')

        y_predict = model.predict_classes(encoded)

        predicted_word = ''
        for word, index in tokenizer.word_index.items():
            if index == y_predict:
                predicted_word = word
                break
        seed_text = seed_text + ' ' + predicted_word
        text.append(predicted_word)
    return ' '.join(text)


seed_text = 'Pfizer vaccine efficacy is'
generate_sequence(model, tokenizer, seq_length, seed_text, 10)
