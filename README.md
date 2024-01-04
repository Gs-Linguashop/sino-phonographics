# Phonetic Sino Ideographs&mdash;a font generator that converts Chinese characters into their phonographemes 

## What is a phonographeme? 

A phonographeme is a component in Chinese writing system that governs the pronunciation aspect of a character. 

Since ancient times, Chinese people use pictograms, symbols directly resembling the shapes of what they represent, as well as several other strategies to represent words. The majority of words, rather, were created as phono-semantic compounds. Usually, another character is borrowed to represent the pronunciation of such a compound, while a semantic component is added along to clarify the meaning. 

For example, character "和 *hé*-and" is composed of character "禾 *hé*-grain plant" and character "口 *kǒu*-mouth". "禾" represents the pronunciation of "和", while "口" clarifies that it is a phonetically borrowed character used for something else, e.g. as a connection word. Unlike in alphabetic writing systems used in languages such as English, where spelling out the pronunciation is enough to distinguish words, the phonetically borrowed components, or *phonographemes*, wasn't quite enough to tell words apart. Hence, it was necessary for the ancient Chhinese to add a semantic component. 

Phono-semantic compounds comprise ~90% of Chinese characters. This is because creating characters using other strategies is laborious (one needs to coin new forms to represent new ideas), whereas phono-semantic compounds simply borrow from existing forms. 

## What does this project do? 

In modern Chinese language, many syllables from the ancient time merge into the same ones due to phonetic shifts. To compensate, modern Chinese vocabulary incorporates much more two-syllable and multi-syllable words than before, so that one does not confuse the one-syllable words with one another. As a consequence, the forms of most Chinese characters contain more information in writing than it is necessary to decode texts written in modern Chinese. 

Indeed, it is possible to throw away the semantic components of phono-semantic characters and leave only the phonographeme in modern Chinese writings. One can still understand the text! This project does exact that. Modify the input/output font paths in main.py and engineer any font to get a phonographic font. 

Writing with only phonographemes has the following features, and one can always return to the old-school style if there is possibilities of confusion: 
* characters are less dense and easier to write; 
* the total set of characters in regular use can be reduced to ~1000, compared to 3000 to 5000 needed now to understand most modern texts; 
* it better fits the etymology of modern Chinese vocabulary in the sense that it retains just enough information, less that the writing system used now; 
* it emphasizes the phonetic aspect of most characters&mdash;those used to be phono-semantic anyway. 

The idea of writing Chinese with only phonographeme aligns with the historic development of alphabets. Usually, a original writing system is created as ideographs. Then, a foreign language borrow some of the ideographs to represent their corresponding concepts, while others to represent sound of their language. Finally, developments or yet another borrowing of the writing system into new languages discards the ideographic aspect completely. The Chinese language is one of the lucky languages that created their own ideographs, but since the Chinese language was never discontinued, the characters hardly have any chance to go through further stages of developments. This project reveals a possibility where the Chinese writing system moves on and gets simplified from a ideographic system into a syllabic alphabet, suited for writing the modern Chinese language (or more). 

## Dependencies 

* [fontTools](https://github.com/fonttools/fonttools)
* [chinese_converter](https://github.com/zachary822/chinese-converter), might switch to [OpenCC](https://github.com/BYVoid/OpenCC) later
