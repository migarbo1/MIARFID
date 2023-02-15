#!/usr/bin/env bash
cd /home/miguel/Documentos/TA/exercices/ex5/mert-work
/home/miguel/Documentos/TA/mosesdecoder/bin/extractor --sctype BLEU --scconfig case:true  --scfile run5.scores.dat --ffile run5.features.dat -r /home/miguel/Documentos/TA/exercices/ex5/train/development.clean.en -n run5.best100.out.gz
