# HandSpell - Reading hands, one letter at a time

[HandSpell FrontEnd Streamlit Website](
  https://handspellfe.streamlit.app/).
Provides:
- Learn It, input a letter to get its sign language gesture
- Name It, get an image and guess what sign gesture it represents
- Read It, hand-sign tranlation via image either with file upload or camera input
- Sign It, get a random letter and making its respective gesture via image
- Spell It, complete a word that has a missing letter, using sign-language

![By Coloringbuddymike - Own work, CC BY-SA 3.0, https://commons.wikimedia.org/w/index.php?curid=24802810](.images/Asl-sign-language-coloring-at-coloring-pages-for-kids-boys-dotcom.svg)


## Why?
Around 70 million deaf people use sign language, yet most hearing people can't
read a single sign.
We want to build a bridge, one letter at a time.

## Who?

Originally an educational group project to practice Data Science & AI skills.


Project [presentation](
https://docs.google.com/presentation/d/1Xz8Q6KtlDj0mV3MGL5ygtARrU_AmtbRg9EsATKX838w/edit?usp=sharing)



Original team members:
- Afonso Silva - [LinkedIn](https://www.linkedin.com/in/notfonz/)
- Delphine Pessoa - [LinkedIn](https://www.linkedin.com/in/delphine-pessoa/)
- Maximilian Greger - [LinkedIn](https://www.linkedin.com/in/maximilian-greger-77595b289/)
- Kazim Hussain Mohammed - [LinkedIn](https://www.linkedin.com/in/kazim-mohammed-a7316856/)

Pitched project [presentation](
https://docs.google.com/presentation/d/1jcQMq_tmHvUgpGdeSIOcO710AYkrgIvgbfjN2BN1O7g/edit?slide=id.p1#slide=id.p1) by Afonso Silva in October 2026.






# Usage

HandSpell provides the following core functionalities:

- Hand Detection: Detects hands in images using MediaPipe.

- Landmark Extraction: Extracts the coordinates of 21 hand landmarks to represent hand poses as numerical features.

- Sign Language Classification: Uses a trained XGBoost classifier to predict the corresponding sign language letter based on the extracted hand landmarks.

- API Integration: Provides access to prediction functionality through a REST API.


# Setup Instructions

[Backend Repo](
  https://github.com/notFonz/HandSpell)


## License

- **Code** (`HandSpell.py`, `pages/`, `src/`, `style.py`, `utils.py`, `.streamlit/config.toml`, `Makefile`): [GPL-3.0](LICENSE)
- **Images and documentation** (`.images/`, `*.md`): [CC BY-SA 4.0](LICENSE-DATA), except the third-party files below.

### Third-party assets

These keep their original licenses:

- `.images/ASL Letter Reference/`: from the [American Sign Language dataset](https://www.kaggle.com/datasets/kapillondhe/american-sign-language) by Kapil Londhe on Kaggle, [GPL-2.0](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html)
- `.images/Asl-sign-language-coloring-at-coloring-pages-for-kids-boys-dotcom.svg`: "American Sign Language Chart Coloring Page Printable" by Coloringbuddymike, via [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Asl-sign-language-coloring-at-coloring-pages-for-kids-boys-dotcom.svg), [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/)
- `.images/question mark.png`: question mark icon by [Friconix](https://friconix.com), free to use with a link to Friconix
- `.images/le-wagon-logo.png`: © Le Wagon, used for identification only
