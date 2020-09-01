# wordstag
Today with the rise of social media and popularity of internet and phonetic typing many sers are using various new methods to type in various places like in social media chatting or reviewing some products. In many places where English is not the primary language are tending to mix their own language with English as their convenience. Like in India people tend to mix Hindi language with English whenever they want to write something in a blog or a forum or in some website’s review page. They present problem when we would want to access the sentiment of the user’s data for big data application.

This is a Toy Project which is a renewed version of the thesis work that I did while completing my M.Tech curriculam. The link to the report of my thesis is: https://1drv.ms/b/s!AprejcxE1cmCjNAp3ZJfZ7HlKt8Fyw?e=cFFlxR.

Machine Translation have become a popular and useful tool for understanding the mixed languages in bilingual communication. To ease up the translation from those code mixed languages to a common language like English we would tag the languages of any specific words in a context so that one would know which words belongs to the base language and which belongs to the second language, also which defines universal, code-mixed or the ones we cannot define.

This perticular repisatory contains the Programs that would convert a bilingual text corpus into a readable feature vector sets to be used as a Training Set for machine learning predictions. The vectors comprises of the below entries for which we have the following functions.

N-gram frequency (300 Entries) (Function Name: ngram_frequency): n this entry, we would make a vector list of 300 entries that we would find in our training corpus acquired by process presented by (Cavner & Trenkle, 1994). Then we would break the words of the given contexts in training corpus in n-grams (from bigram to 5-grams) and count their occurrences. Then if that n-gram matches with an n-gram presents in that vector the frequency of that n-gram would then get multiplied by the occurrences presents in the given word. This would create a 300 sized vector. I take reference from "Python for NLP: Developing an Automatic Text Filler using N-Grams" - StackAbuse(https://stackabuse.com/python-for-nlp-developing-an-automatic-text-filler-using-n-grams/) and "N-Gram-Based Text Categorization: Categorizing Text With Python" - Alejandro Nolla Blog (http://blog.alejandronolla.com/2013/05/20/n-gram-based-text-categorization-categorizing-text-with-python/)

English Dictionary Lookup(Function Name: is_english): In this entry, we would find the given word in an English dictionary. If the word is found the value of the entry would be 1, otherwise it would be 0.

Hindi Dictionary Lookup(Function Name: is_hindi): In this entry, we would find the given word in a transliterated Hindi dictionary. If the word is found the value of the entry would be 1, otherwise it would be 0.

Whether it is abbreviation Lookup(Function Name: is_abbr): In this entry we would find the given word in a dictionary consisted of various abbreviations used in daily life. If the word is found the entry would be 1, otherwise it would be 0.

MED value for English(Function Name: med_in_english): This entry consists of minimum edit distance (The number of changes needed in that word so that the word becomes a word that exists in a dictionary.) for English dictionary. I take reference from "Minimum Edit Distance Dynamic Programming" - Youtube(https://www.youtube.com/watch?v=We3YDTzNXEk)

MED value for Hindi(Function Name: med_in_hindi): This entry consists of minimum edit distance for Hindi dictionary. I too reference from "How to Write a Spelling Corrector" - Norvig Blog(https://norvig.com/spell-correct.html)

Word Context(Function Name: get_word_context): In this entry, we would take a 6 window entry which will be consists of the previous and next three words and would input their tag that is been saved in a word frequency profile.

To obtain n-gram frequecy profile and word context profile we use the files "creating_ngrams.py" and "word_context.py" respectively which are available in modules package.
