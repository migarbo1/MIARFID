this exercise asks to try MIRA for training the log-linear model weights.
we have tried with different -J values, wich changes the number of loops to pass over the data. larger loops can be better for smaller datasets.
(default) for -J = 60 BLEU = 90.88, 98.7/93.9/92.2/90.6 (BP=0.969, ratio=0.969, hyp_len=11425, ref_len=11786)
for -j = 100 BLEU = 90.91, 98.7/93.9/92.2/90.6 (BP=0.969, ratio=0.970, hyp_len=11429, ref_len=11786)
for -j = 200 BLEU = 90.95, 98.7/93.8/92.1/90.5 (BP=0.970, ratio=0.971, hyp_len=11439, ref_len=11786)

