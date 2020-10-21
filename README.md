The Diversity-Innovation Paradox in Science
===========================================

This repository contains code and data associated with “The
Diversity-Innovation Paradox in Science.” arXiv preprint and PDF can be
found [here](https://arxiv.org/abs/1909.02063), published paper in
*Proceedings of the National Academy of Sciences of the United States of
America* can be found [here](https://www.pnas.org/content/117/17/9284)

If you use any of the code or ideas presented here, please cite our
paper:

-   Hofstra, Bas, Vivek V. Kulkarni, Sebastian Munoz-Najar Galvez, Bryan
    He, Dan Jurafsky, & Daniel A. McFarland. (2020). The
    Diversity-Innovation Paradox in Science. *Proceedings of the
    National Academy of Sciences of the United States of America
    117*(17), 9284-9291.

In a nutshell
-------------

By analyzing data from nearly all US PhD-recipients and their
dissertations across three decades, this paper finds demographically
underrepresented students innovate at higher rates than majority
students, but their novel contributions are discounted and less likely
to earn them academic positions. The discounting of minorities’
innovations may partly explain their underrepresentation in influential
positions of academia.

![picture](fig_1.png) ***Figure 1***. The introduction of innovations
and their subsequent uptake.

Code
----

With the provided code the novelty, impactful novelty, and distal
novelty metrics can be constructed from the ProQuest dissertation
abstract data.

-   ***stms\_estimate\_at\_K.R***: Runs Structural Topic Models at
    specified range of K (50-1000 in the paper).
-   ***concepts\_k500\_50.R***: Extracts concepts from the structural
    topic model output, the number of words, topics, and FREX weighing
    can be adjusted in the code to get at the differend K/FREX
    scenarios.
-   ***proquest-skipgrams.py***: Code to learn the concept embeddings to
    find out which are distal or proximal linkages.
-   ***elastic\_search\_proquest\_hyphen\_removed\_filtered\_concepts.py***:
    Sample code to put documents into Elastic Search (see
    <a href="https://marcobonzanini.com/2015/02/02/how-to-query-elasticsearch-with-python/" class="uri">https://marcobonzanini.com/2015/02/02/how-to-query-elasticsearch-with-python/</a>)
-   ***obtain\_innovation\_years\_proquest\_msearch\_chunks\_only\_hits\_filtered.py***:
    Looks up each dyad and dumps when it was first introduced,
    introduced thesis ID and future uptakes for that dyad.
-   ***merge\_innovations\_uptakes\_files.py***: Aggregates uptakes etc.
    by thesis ID.

Logic for computing novelty and uptake
--------------------------------------

We seek to compute the number of uptakes for each dyad and then
aggregate across a document. To find the number of uptakes of a concept
dyad, we first find the first theses in which the dyad was introduced
which in turn needs us to identify all theses that used the link and
then obtain the thesis that is the earliest as the introducing thesis
(by graduation year). The rest of the dyads are the future uptakes. This
logic an be implemented in many ways based on your needs. Below we point
to one such implementation that was suited for compute infrastructure.
Note that the below implementation by its design requires customization
because of the heavy setup needed. We chose this approach because
envisioned future projects that needed this anyways where we needed
efficient ways of identifying theses that contained a given set of
terms.

We implement the above by building a search engine that returns
documents (theses) that contain a term. In particular, we query the
search engine (Elastic Search) for each dyad and obtain number of
documents/theses that are hits (i.e., that contain the dyad) as well as
their publication years sorted in ascending order by year. The first is
the thesis that introduced the link (dyad) (ties are broken arbitrarily)
and the rest of hits correspond to the total number of uptakes for that
dyad. The idea is to store each thesis (document) in Elastic search
along with meta data (like graduation year, identifier, etc.). Then we
can efficiently use Elastic Search’s functionality to retrieve theses
that contain a given dyad:
obtain\_innovation\_years\_proquest\_msearch\_chunks\_only\_hits\_filtered.py.
We had to do this in chunks because of restricted memory/compute
requirements. The outputs of these are then just aggregated across each
thesis to obtain (a) The number of links (b) the total uptakes of dyads
and the (c) mean distal score introduced by the thesis.

Data
----

For the concepts extracted for the K = 500 Structural Topic Model where
we equally balance frequency and exclusivity (which we extract in
**concepts\_k500\_50.R**), please see **k500\_wordcouds\_n\_to\_n.zip**
for visualizations or **frexconcepts\_k500\_50.rda** for the data
(second element in the list).

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
