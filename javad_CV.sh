for i in {0..2};
do
    python3 train_local.py data/train$i;
    python3 formattrainingdata.py data/$i\.local.training;
    ~/libsvm-3.18/svm-train -q -b 1 -c 100 data/$i\.local.data data/$i\.local.m ;
    python3 train_global.py data/train$i data/$i\.local.m;
    ~/libsvm-3.18/svm-train -q -b 1 -c 1000 data/$i\.global.data data/$i\.global.m ;
    python3 inference.py data/test$i data/$i\.local.m data/$i\.global.m | tee results/fold$i\.txt ;
done
