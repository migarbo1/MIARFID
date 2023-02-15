try the model obtained in the section 6 without adjusting the weights

first clone the data, unzip it and clean the files. with clean-corpus-n.perl
then train the output language model with ngran-coun -order 3
next step ist o train the translation model with train-model.perl
after that we clone the test set and proceed to translate it
finally we compute the bleu rate. in this case we have obtained: BLEU = 88.65, 94.1/89.7/86.9/84.3 (BP=1.000, ratio=1.037, hyp_len=12227, ref_len=11786)


