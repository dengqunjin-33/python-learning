import pathlib
import random

import matplotlib.pyplot as plt
import tensorflow as tf

AUTOTUNE = tf.data.experimental.AUTOTUNE
data_root_orig = tf.keras.utils.get_file(origin='https://storage.googleapis.com/download.tensorflow.org'
                                                '/example_images/flower_photos.tgz',
                                         fname='flower_photos', untar=True)

data_root = pathlib.Path(data_root_orig)
# for item in data_root.iterdir():
#     print(item)

all_image_paths = list(data_root.glob('*/*'))
all_image_paths = [str(path) for path in all_image_paths]

random.shuffle(all_image_paths)

image_count = len(all_image_paths)

# for item in all_image_paths[:10]:
#     print(item)

attributions = (data_root / "LICENSE.txt").open(encoding='utf-8').readlines()[4:]
attributions = [line.split('CC-BY') for line in attributions]
attributions = dict(attributions)


# print(attributions)
def caption_image(image_path):
    image_rel = pathlib.Path(image_path).relative_to(data_root)
    image_rel = str(image_rel).replace("\\", "/")
    q1 = attributions[str(image_rel) + ' ']
    temp = q1.split('-')[:-1]
    return "Image (CC BY 2.0)" + '-'.join(temp)


# for n in range(3):
#     image_path = random.choice(all_image_paths)
#     img = plt.imread(image_path)  # 读取图片
#     plt.imshow(img)  # 展示图片
#     plt.show()

label_names = sorted(item.name for item in data_root.glob('*/') if item.is_dir())

label_to_index = dict((name, index) for index, name in enumerate(label_names))

all_image_labels = [label_to_index[pathlib.Path(path).parent.name] for path in all_image_paths]

img_path = all_image_paths[0]
img_raw = tf.io.read_file(img_path)
img_tensor = tf.image.decode_image(img_raw)
img_final = tf.image.resize(img_tensor, [192, 192])
img_final = img_final / 255.0


def preprocess_image(image, xz, yz):
    image = tf.image.decode_jpeg(image, channels=3)
    image = tf.image.resize(image, [xz, yz])
    image /= 255.0

    return image


def load_and_preprocess_image(path):
    image = tf.io.read_file(path)
    return preprocess_image(image, 192, 192)


# image_path = all_image_paths[0]
# label = all_image_labels[0]
#
# img = load_and_preprocess_image(image_path)
# plt.imshow(img)
# plt.grid(False)
# plt.xlabel(caption_image(image_path))
# plt.title(label_names[label].title())
# plt.show()

path_ds = tf.data.Dataset.from_tensor_slices(all_image_paths)
# print(path_ds)
image_ds = path_ds.map(load_and_preprocess_image, num_parallel_calls=AUTOTUNE)

plt.figure(figsize=(8, 8))
for n, image in enumerate(image_ds.take(4)):
    plt.subplot(2, 2, n + 1)
    plt.imshow(image)
    plt.grid(False)
    plt.xticks([])
    plt.yticks([])
    plt.xlabel(caption_image(all_image_paths[n]))

# plt.show()
label_ds = tf.data.Dataset.from_tensor_slices(tf.cast(all_image_labels
                                                      , tf.int64))

# for label in label_ds.take(10):
#     print(label_names[label.numpy()])

image_label_ds = tf.data.Dataset.zip((image_ds, label_ds))

# print(image_label_ds)

ds = tf.data.Dataset.from_tensor_slices((all_image_paths, all_image_labels))


def load_and_preprocess_from_path_label(path, label):
    return load_and_preprocess_image(path), label


image_label_ds = ds.map(load_and_preprocess_from_path_label)
# print(image_label_ds)

BATCH_SIZE = 32

ds = image_label_ds.shuffle(buffer_size=image_count)
ds = ds.repeat()
ds = ds.batch(BATCH_SIZE)
ds = ds.prefetch(buffer_size=AUTOTUNE)
# print(ds)

# mobile_net = tf.keras.applications.MobileNetV2(input_shape=(192, 192, 3), include_top=False)
# mobile_net.trainable = False

mobile_net = tf.keras.applications.MobileNetV2(input_shape=(192, 192, 3), include_top=False)
mobile_net.trainable = False

