#! /bin/bash

BASEDIR='.'

# convert datasets to feature vectors
echo "Extracting features..."
py extract-features.py $BASEDIR/data/train/ > train.feat
py extract-features.py $BASEDIR/data/devel/ > devel.feat

# train CRF model
echo "Training CRF model..."
py train-crf.py model.crf < train.feat
# run CRF model
echo "Running CRF model..."
py predict.py model.crf < devel.feat > devel-CRF.out
# evaluate CRF results
echo "Evaluating CRF results..."
py evaluator.py NER $BASEDIR/data/devel devel-CRF.out > devel-CRF.stats


#Extract Classification Features
cat train.feat | cut -f5- | grep -v ^$ > train.clf.feat


# train Naive Bayes model
echo "Training Naive Bayes model..."
py train-sklearn.py model.joblib vectorizer.joblib < train.clf.feat
# run Naive Bayes model
echo "Running Naive Bayes model..."
py predict-sklearn.py model.joblib vectorizer.joblib < devel.feat > devel-NB.out
# evaluate Naive Bayes results 
echo "Evaluating Naive Bayes results..."
py evaluator.py NER $BASEDIR/data/devel devel-NB.out > devel-NB.stats


# # train SVM model
# echo "Training SVM model..."
# python train-SVM.py model.joblib vectorizer.joblib < train.clf.feat
# # run SVM model
# echo "Running SVM model..."
# python predict-sklearn.py model.joblib vectorizer.joblib < devel.feat > devel-SVM.out
# # evaluate Naive Bayes results 
# echo "Evaluating Naive Bayes results..."
# python evaluator.py NER $BASEDIR/data/devel devel-SVM.out > devel-SVM.stats

# remove auxiliary files.
rm train.clf.feat
