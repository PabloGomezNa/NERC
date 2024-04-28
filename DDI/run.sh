#! /bin/bash

BASEDIR=../

 #./C:/Users/andre/Downloads/stanford-corenlp-4.5.6/stanford-corenlp-4.5.6/corenlp.sh -quiet true -port 9000 -timeout 15000  &
 #sleep 1

# extract features
echo "Extracting features"
python extract-features.py $BASEDIR/data/devel/ > devel.cod &
python extract-features.py $BASEDIR/data/train/ | tee train.cod | cut -f4- > train.cod.cl

# kill `cat /tmp/corenlp-server.running`


#NB model
# train NB model
echo "Training NB model"
python train-nb.py model.joblib vectorizer.joblib < train.cod.cl
# run model
echo "Running NB model..."
python predict-sklearn.py model.joblib vectorizer.joblib < devel.cod > devel-nb.out
# evaluate results
echo "Evaluating NB results..."
python evaluator.py DDI $BASEDIR/data/devel/ devel-nb.out > devel-nb.stats


# #SVM model
# # train model
# echo "Training SVM model"
# python train-svm.py model.joblib vectorizer.joblib < train.cod.cl
# # run model
# echo "Running SVM model..."
# python predict-sklearn.py model.joblib vectorizer.joblib < devel.cod > devel-svm.out
# # evaluate results
# echo "Evaluating SVM results..."
# python evaluator.py DDI $BASEDIR/data/devel/ devel-svm.out > devel-svm.stats


# #RF model
# # train model
# echo "Training RF model"
# python train-rf.py model.joblib vectorizer.joblib < train.cod.cl
# # run model
# echo "Running RF model..."
# python predict-sklearn.py model.joblib vectorizer.joblib < devel.cod > devel-rf.out
# # evaluate results
# echo "Evaluating RF results..."
# python evaluator.py DDI $BASEDIR/data/devel/ devel-rf.out > devel-rf.stats



# #CRF model
# # train model
# echo "Training CRF model"
# python train-crf.py model.joblib vectorizer.joblib < train.cod.cl
# # run model
# echo "Running CRF model..."
# python predict-sklearn.py model.joblib vectorizer.joblib < devel.cod > devel-crf.out
# # evaluate results
# echo "Evaluating CRF results..."
# python evaluator.py DDI $BASEDIR/data/devel/ devel-crf.out > devel-crf.stats

