# Phonetic Sino Ideographs&mdash;a font generator that converts Chinese characters into their phonographemes 

## What is a phonographeme? 

A phonographeme is a component in Chinese writing system that governs the pronunciation aspect of a character. 

Since ancient times, Chinese people use pictograms, symbols directly resembling the shapes of what they represent, as well as several other strategies to represent words. The majority of words, rather, were created as phono-semantic compounds. Usually, another character is borrowed to represent the pronunciation of such a compound, while a semantic component is added along to clarify the meaning. 

For example, character "和 *hé*-and" is composed of character "禾 *hé*-grain plant" and character "口 *kǒu*-mouth". "禾" represents the pronunciation of "和", while "口" clarifies that it is a phonetically borrowed character used for something else, e.g. as a connection word. Unlike in alphabetic writing systems used in languages such as English, where spelling out the pronunciation is enough to distinguish words, the phonetically borrowed components, or *phonographemes*, wasn't quite enough to tell words apart in ancient Chinese. Hence, it was necessary for the ancient Chinese to add a semantic component. 

Phono-semantic compounds comprise ~90% of Chinese characters. This is because creating characters using other strategies is laborious (one needs to coin new forms to represent new ideas), whereas phono-semantic compounds simply borrow from existing forms. 

## What does this project do? 

In modern Chinese language, many syllables from the ancient time merge into same ones due to phonetic shifts. To compensate, modern Chinese vocabulary incorporates much more two-syllable and multi-syllable words than before, so that one doesn't have to deal with many monosyllabic words with indistinguishable pronuncations. As a consequence, the forms of most Chinese characters contain more information than necessary to understand regular texts written in modern Chinese. 

Indeed, it is possible to throw away the semantic components of phono-semantic characters and leave only the phonographeme in modern Chinese writings. One can still understand the text! 

This project does exact that. Modify the input/output font paths in main.py and convert any font to get a phonographic font. The converted font shows only the phonographemes of digitized characters. 

## Why write Chinese in phonographemes? 

Writing with only phonographemes has the following perks (and one can always return to an old-school character if needed): 
* characters are less dense and simpler to write; 
* the total set of characters in regular use can be reduced to ~1000, compared to 3000 to 5000 usually needed to understand most modern texts; 
* it better fits the large amount of bi- and multi-syllabic vocabulary of modern Chinese in the sense that it retains just enough information, throws away the unnecessary, and eats less entropy than the contemporary Chinese writing systems; 
* it emphasizes the phonetic aspect of most characters&mdash;those used to be phono-semantic anyway. 

The idea of writing Chinese with only phonographeme aligns with the historic development of alphabets. Usually, an original writing system is created as ideographs. Then, a foreign language borrows some of the ideographs to represent their corresponding concepts, while others to represent sounds of their language. Finally, further developments or yet another borrowing of the writing system discards the ideographic part completely. 

The Chinese language is one of the lucky languages that got their original ideographs, but since the language was never discontinued, the characters hardly have any chance to go through following stages of developments (one may argue whether that's a good thing). This project reveals a possibility where the Chinese writing system moves on to become a syllabic alphabet, suited for writing the modern Chinese language, or more. 

## Dependencies 

* [fontTools](https://github.com/fonttools/fonttools)
* [chinese_converter](https://github.com/zachary822/chinese-converter), might switch to [OpenCC](https://github.com/BYVoid/OpenCC) later
