This repository contains code and data associated with “The
Diversity-Innovation Paradox in Science.” arXiv preprint and PDF can be
found [here](https://arxiv.org/abs/1909.02063).

![picture](fig_1.pdf)

Code
----

With the provided code provided the novelty, impactful novelty, and
distal novelty metrics can be constructed from the ProQuest dissertation
abstract data.

-   ***stms\_estimate\_at\_K.R***: Runs Structural Topic Models at
    specified range of K (50-1000 in the paper).
-   ***concepts\_k500\_50.R***: Extracts concepts from the structural
    topic model output, the number of words, topics, and FREX weighing
    can be adjusted in the code to get at the differend K/FREX
    scenarios.
-   ***novelty and impactful novelty***:
-   ***embeddings***:

Data
----

For the concepts extracted for the K = 500 Structural Topic Model where
we equally balance frequency and exclusivity (which we do in
**concepts\_k500\_50.R**), please see **k500\_wordcouds.zip** for
visualizations or **frexconcepts\_k500\_50.rda** for the data (second
element in the list).

For raw data of ProQuest or the Web of Science:

-   [ProQuest](https://www.proquest.com/)
-   [Web of Science](https://www.proquest.com/)

For inferring gender and race associated with names:

-   [US Census Data
    2000](https://census.gov/topics/population/genealogy/data/2000_surnames.html)
-   [US Census Data
    2010](https://census.gov/topics/population/genealogy/data/2010_surnames.html)
-   [Social Security Administration
    Data](https://www.ssa.gov/oact/babynames/limits.html)
    -   [*Hofstra et
        al. 2017*](https://journals.sagepub.com/doi/full/10.1177/0003122417705656):
        Method described here helps infer gender and race (with US
        Census and SSN).
-   [Florida Voter Registration
    Data](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/UBIG3F)
    -   [*ethnicolr*](https://github.com/appeler/ethnicolr) by [*Sood
        and Laohaprapanon*](https://arxiv.org/abs/1805.02109): Method
        used to further help infer race with the Florida Voter
        registration data.
-   [Genderize.io](https://genderize.io/) Method used to further help
    infer gender.
