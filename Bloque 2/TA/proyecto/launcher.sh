export GIZA=/home/miguel/Documentos/TA/mgiza/mgizapp/bin
export MOSES=/home/miguel/Documentos/TA/mosesdecoder
export SCRIPTS_ROOTDIR=/home/miguel/Documentos/TA/mosesdecoder/scripts
export PATH=$PATH:/home/miguel/Documentos/TA/mosesdecoder/scripts/training/
export PATH=$PATH:/home/miguel/Documentos/TA/srilm/bin/i686-m64
export PATH=$PATH:/home/miguel/Documentos/TA/mosesdecoder/bin/
export TRAIN_SCRIPTS=${SCRIPTS_ROOTDIR}/training/

export CORPUS_PATH=~/projectTA/Corpus50000

echo $PATH

echo "global variables exported"

while getopts n:i:s:d:a: flag
do
    case "${flag}" in
        n) NGRAM=${OPTARG};;
        i) MAX_ITER=${OPTARG};;
        s) SMOOTHER=${OPTARG};;
	d) DISCOUNT=${OPTARG};;
	a) ALIGNMENT=${OPTARG};;
    esac
done

#tokenize corpus
${SCRIPTS_ROOTDIR}/tokenizer/tokenizer.perl -l en < ${CORPUS_PATH}/europarl-v7.es-en-train-red.en > ${CORPUS_PATH}/europarl-v7.es-en-train-red-tok.en
${SCRIPTS_ROOTDIR}/tokenizer/tokenizer.perl -l es < ${CORPUS_PATH}/europarl-v7.es-en-train-red.es > ${CORPUS_PATH}/europarl-v7.es-en-train-red-tok.es
${SCRIPTS_ROOTDIR}/tokenizer/tokenizer.perl -l en < ${CORPUS_PATH}/europarl-v7.es-en-dev-red.en > ${CORPUS_PATH}/europarl-v7.es-en-dev-red-tok.en
${SCRIPTS_ROOTDIR}/tokenizer/tokenizer.perl -l es < ${CORPUS_PATH}/europarl-v7.es-en-dev-red.es > ${CORPUS_PATH}/europarl-v7.es-en-dev-red-tok.es
${SCRIPTS_ROOTDIR}/tokenizer/tokenizer.perl -l en < ${CORPUS_PATH}/europarl-v7.es-en-test.en > ${CORPUS_PATH}/europarl-v7.es-en-test-tok.en
${SCRIPTS_ROOTDIR}/tokenizer/tokenizer.perl -l es < ${CORPUS_PATH}/europarl-v7.es-en-test.es > ${CORPUS_PATH}/europarl-v7.es-en-test-tok.es


#clean corpus
clean-corpus-n.perl ${CORPUS_PATH}/europarl-v7.es-en-train-red-tok es en ${CORPUS_PATH}/europarl-v7.es-en-train-red.clean 1 60

echo "Training corpus cleaned"

#train output language model
export LangModel=$PWD/models/model_n${NGRAM}_i${MAX_ITER}_interpolate_${DISCOUNT}_${ALIGNMENT}.lm
ngram-count -order $NGRAM -unk -interpolate -${DISCOUNT} -text ${CORPUS_PATH}/europarl-v7.es-en-train-red.clean.en -lm ${LangModel} 

echo $LangModel
echo "output language model trained!"

#train translation model
${TRAIN_SCRIPTS}train-model.perl -root-dir work -mgiza -mgiza-cpus 1 -corpus ${CORPUS_PATH}/europarl-v7.es-en-train-red.clean -f es -e en -alignment ${ALIGNMENT} -reordering msd-bidirectional-fe -lm 0:$NGRAM:$LangModel -external-bin-dir $GIZA> ${CORPUS_PATH}/europarl-v7.es-en-train-red.out
echo "translation model trained!"

# train log-linear model weights
${TRAIN_SCRIPTS}clean-corpus-n.perl ${CORPUS_PATH}/europarl-v7.es-en-dev-red-tok es en ${CORPUS_PATH}/europarl-v7.es-en-dev-red.clean 1 60
echo "development corpus cleaned"

${TRAINING_SCRIPTS}mert-moses.pl \
${CORPUS_PATH}/europarl-v7.es-en-dev-red.clean.es ${CORPUS_PATH}/europarl-v7.es-en-dev-red.clean.en \
$MOSES/bin/moses work/model/moses.ini \
--maximum-iterations=$MAX_ITER \
--mertdir $MOSES/bin/

echo "log-linear model weights adjusted"

#translation process
$MOSES/bin/moses \
-f mert-work/moses.ini < ${CORPUS_PATH}/europarl-v7.es-en-test-tok.es > test.hyp

echo "translation performed"

#evaluation
$MOSES/scripts/generic/multi-bleu.perl -lc ${CORPUS_PATH}/europarl-v7.es-en-test-tok.en < test.hyp > res_n${NGRAM}_i${MAX_ITER}_${SMOOTHER}_${DISCOUNT}_${ALIGNMENT}.txt
