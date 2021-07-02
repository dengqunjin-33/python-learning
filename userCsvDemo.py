import numpy as np
import tensorflow as tf

TRAIN_DATA_URL = "https://storage.googleapis.com/tf-datasets/titanic/train.csv"
TEST_DATA_URL = "https://storage.googleapis.com/tf-datasets/titanic/eval.csv"

train_file_path = tf.keras.utils.get_file("train.csv", TRAIN_DATA_URL)
test_file_path = tf.keras.utils.get_file("eval.csv", TEST_DATA_URL)

np.set_printoptions(precision=3, suppress=True)

CSV_COLUMNS = ['survived',
               'sex',
               'age',
               'n_siblings_spouses',
               'parch',
               'fare',
               'class',
               'deck',
               'embark_town',
               'alone']


def get_dataset(file_path):
    dataset = tf.data.experimental.make_csv_dataset(file_path,
                                                    batch_size=12,
                                                    label_name=CSV_COLUMNS[0],
                                                    na_value="?",
                                                    num_epochs=1,
                                                    ignore_errors=True)
    return dataset


raw_train_data = get_dataset(train_file_path)
raw_test_data = get_dataset(test_file_path)

examples, labels = next(iter(raw_train_data)) # 第一个批次
print("EXAMPLES: \n", examples, "\n")
print("LABELS: \n", labels)