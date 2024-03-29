import os

import tensorflow

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Dense, SimpleRNN, Input
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.text import Tokenizer, text_to_word_sequence
from tensorflow.keras.utils import to_categorical

with open('mess.txt', 'r', encoding='utf-8') as f:
    texts = f.read()
    texts = texts.replace('\ufeff', '')  # убираем первый невидимый символ

maxWordsCount = 25000
tokenizer = Tokenizer(num_words=maxWordsCount, filters='1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM!–"—#$%&amp;()*+,-./:;<=>?@[\\]^_`{|}~\t\n\r«»',
                      lower=True, split=' ', char_level=False)
tokenizer.fit_on_texts([texts])

dist = list(tokenizer.word_counts.items())
print(dist[:10])

data = tokenizer.texts_to_sequences([texts])
res = to_categorical(data[0], num_classes=maxWordsCount)
print(res.shape)

inp_words = 3
n = res.shape[0] - inp_words

X = np.array([res[i:i + inp_words, :] for i in range(n)])

Y = res[inp_words:]


# model = Sequential()
# model.add(Input((inp_words, maxWordsCount)))
# model.add(SimpleRNN(800, activation='tanh'))
# model.add(Dense(600, activation="relu"))
# model.add(Dense(maxWordsCount, activation='softmax'))
# model.summary()
#
# model.compile(loss='categorical_crossentropy', metrics=['accuracy'], optimizer='adam')
#
# history = model.fit(X, Y, batch_size=32, epochs=50)
# model.save("my_m_100k.h5")

model = tf.keras.models.load_model("my_m_100k.h5")
model.compile(loss='categorical_crossentropy', metrics=['accuracy'], optimizer='adam')


def buildPhrase(texts, str_len=20):
    res = texts

    data = tokenizer.texts_to_sequences([texts])[0]
    print(data)
    for i in range(str_len):
        x = to_categorical(data[i: i + inp_words], num_classes=maxWordsCount)  # преобразуем в One-Hot-encoding
        inp = x.reshape(1, inp_words, maxWordsCount)

        pred = model.predict(inp)
        indx = pred.argmax(axis=1)[0]
        data.append(indx)

        res += " " + tokenizer.index_word[indx]  # дописываем строку

    return res


res = buildPhrase("Вофка взял кабачок и")
print(res)