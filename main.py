import functools
import os

from matplotlib import gridspec
import matplotlib.pylab as plt
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub


def load_img(path_to_img, size):
  max_dim = size
  img = tf.io.read_file(path_to_img)
  img = tf.image.decode_image(img, channels=3)
  img = tf.image.convert_image_dtype(img, tf.float32)

  shape = tf.cast(tf.shape(img)[:-1], tf.float32)
  long_dim = max(shape)
  scale = max_dim / long_dim

  new_shape = tf.cast(shape * scale, tf.int32)

  img = tf.image.resize(img, new_shape)
  img = img[tf.newaxis, :]
  return img

def show_n(images, titles=('',)):
  n = len(images)
  image_sizes = [image.shape[1] for image in images]
  w = (image_sizes[0] * 6) // 320
  plt.figure(figsize=(w  * n, w))
  gs = gridspec.GridSpec(1, n, width_ratios=image_sizes)
  for i in range(n):
    plt.subplot(gs[i])
    plt.imshow(images[i][0], aspect='equal')
    plt.axis('off')
    plt.title(titles[i] if len(titles) > i else '')
  plt.savefig('result.jpg')

# 'https://artforum.com/uploads/upload.002/id16263/article00_1064x.jpg'
def transferStyle(stylePath = 'https://artforum.com/uploads/upload.002/id16263/article00_1064x.jpg', contentPath = 'https://cdn.ca.emap.com/wp-content/uploads/sites/9/2016/06/Tower-Bridge-1024x682.jpg'):
    content_image_url = tf.keras.utils.get_file('curFile.jpg', contentPath)
    style_image_url = tf.keras.utils.get_file('curFile2.jpg', stylePath)
    output_image_size = 512
    content_img_size = (output_image_size, output_image_size)
    style_img_size = (256, 256)

    content_image = load_img(content_image_url, content_img_size)
    style_image = load_img(style_image_url, style_img_size)
    style_image = tf.nn.avg_pool(style_image, ksize=[3,3], strides=[1,1], padding='SAME')

    hub_handle = 'https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2'
    hub_module = hub.load(hub_handle)

    outputs = hub_module(tf.constant(content_image), tf.constant(style_image))
    stylized_image = outputs[0]
    os.remove(style_image_url)
    os.remove(content_image_url)
    show_n([stylized_image])
    return 'result.jpg'