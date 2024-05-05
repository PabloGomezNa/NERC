#! /bin/bash

BASEDIR=../

 #./C:/Users/andre/Downloads/stanford-corenlp-4.5.6/stanford-corenlp-4.5.6/corenlp.sh -quiet true -port 9000 -timeout 15000  &
 #sleep 1

# extract features
echo "Extracting features"
echo "Devel"
time python extract-features.py $BASEDIR/data/devel/ > devel.cod &
time python extract-features.py $BASEDIR/data/test/ > test.cod &
time python extract-features.py $BASEDIR/data/train/ | tee train.cod | cut -f4- > train.cod.cl
# time python extract-features.py $BASEDIR/data/train/ > train.cod
# time cat train.cod | tee train.cod.cl
# time cut -f4- train.cod > train.cod.cl

# # python extract-features.py $BASEDIR/data/train/ | tee train.cod | awk '{print substr($0, index($0, "\t") + 1)}' > train.cod.cl


# # kill `cat /tmp/corenlp-server.running`


# #NB model
# # train NB model
# echo "Training NB model"
# python train-nb.py model.joblib vectorizer.joblib < train.cod.cl
# # run model
# echo "Running NB model devel..."
# python predict-sklearn.py model.joblib vectorizer.joblib < devel.cod > devel-nb.out
# # evaluate results
# echo "Evaluating NB results devel..."
# python evaluator.py DDI $BASEDIR/data/devel/ devel-nb.out > devel-nb.stats

# train NB model
echo "Training NB model for test"
python train-nb.py model.joblib vectorizer.joblib < train.cod.cl
# run model
echo "Running NB model test..."
python predict-sklearn.py model.joblib vectorizer.joblib < test.cod > test-nb.out
# evaluate results
echo "Evaluating NB results test..."
python evaluator.py DDI $BASEDIR/data/test/ test-nb.out > test-nb.stats


# #SVM model
# # train model
# echo "Training SVM model"
# time python train-svm.py model.joblib vectorizer.joblib < train.cod.cl
# # run model
# echo "Running SVM model..."
# python predict-sklearn.py model.joblib vectorizer.joblib < devel.cod > devel-svm.out
# # evaluate results
# echo "Evaluating SVM results..."
# python evaluator.py DDI $BASEDIR/data/devel/ devel-svm.out > devel-svm.stats

# Train SVM model
# train model
echo "Training SVM model"
time python train-svm.py model.joblib vectorizer.joblib < train.cod.cl
# run model
echo "Running SVM model..."
python predict-sklearn.py model.joblib vectorizer.joblib < test.cod > test-svm.out
# evaluate results
echo "Evaluating SVM results..."
python evaluator.py DDI $BASEDIR/data/test/ test-svm.out > test-svm.stats


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



# #linear model
# # train linear model
# echo "Training linear model"
# python train-linear.py model.joblib vectorizer.joblib < train.cod.cl
# # run model
# echo "Running linear model devel..."
# python predict-sklearn.py model.joblib vectorizer.joblib < devel.cod > devel-linear.out
# # evaluate results
# echo "Evaluating NB results devel..."
# python evaluator.py DDI $BASEDIR/data/devel/ devel-linear.out > devel-linear.stats