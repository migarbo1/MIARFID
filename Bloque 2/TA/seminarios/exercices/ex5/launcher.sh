export GIZA=/home/miguel/Documentos/TA/mgiza/mgizapp/bin
export MOSES=/home/miguel/Documentos/TA/mosesdecoder
export SCRIPTS_ROOTDIR=/home/miguel/Documentos/TA/mosesdecoder/scripts
export PATH=$PATH:/home/miguel/Documentos/TA/mosesdecoder/scripts/training/
export PATH=$PATH:/home/miguel/Documentos/TA/srilm/bin/i686-m64
export PATH=$PATH:/home/miguel/Documentos/TA/mosesdecoder/bin/

echo $PATH

echo "global variables exported"


export MAX_ITER=5
export NGRAM=3

#download train data
wget --no-check-certificate \
http://www.prhlt.upv.es/~fcn/Students/ta/train.tgz
tar xzvf train.tgz
rm train.tgz

echo "Training data downloaded"

#clean corpus
clean-corpus-n.perl train/training es en train/training.clean 1 60

echo "Training corpus cleaned"

#train output language model
cd train
ngram-count -order $NGRAM -unk -interpolate -ukndiscount $NGRAM -text training.clean.en -lm model.lm
export LangModel=$PWD/model.lm

echo $LangModel
echo "output language model trained!"

#train translation model
$SCRIPTS_ROOTDIR/training/train-model.perl -root-dir work -mgiza -mgiza-cpus 1 -corpus training.clean -f es -e en -alignment grow-diag-final-and -reordering msd-bidirectional-fe -lm 0:3:$LangModel -external-bin-dir $GIZA> training.out
echo "translation model trained!"

# train log-linear model weights
wget --no-check-certificate \
http://www.prhlt.upv.es/~fcn/Students/ta/dev.tgz
tar xzvf dev.tgz
rm dev.tgz
mv dev/development.e* .
echo "development corpus downloaded"

clean-corpus-n.perl development es en development.clean 1 60
echo "development corpus cleaned"

cd ..
$MOSES/scripts/training/mert-moses.pl \
train/development.clean.es train/development.clean.en \
$MOSES/bin/moses train/work/model/moses.ini \
--maximum-iterations=$MAX_ITER \
--mertdir $MOSES/bin/

echo "log-linear model weights adjusted"

#translation process
wget --no-check-certificate \
http://www.prhlt.upv.es/~fcn/Students/ta/test.tgz
tar xzvf test.tgz
rm test.tgz
echo "test data downloaded"

cd test
$MOSES/bin/moses \
-f ../mert-work/moses.ini < test.es > test.hyp

echo "translation performed"

#evaluation
$MOSES/scripts/generic/multi-bleu.perl -lc test.en < test.hyp
