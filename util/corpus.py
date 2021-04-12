

# keep_word = df1.job_d.apply(lambda x: x.split(' ')).tolist()[0]


def word_cor(word, keep_word):
    word = word.split(' ')
    word = [i for i in word if i in keep_word]
    return ' '.join(word)


# df2["resume"] = df2.resume.apply(lambda x: word_cor(x))

