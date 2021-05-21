# 기존 VGG16 비교 - keras 책 p.202
import tensorflow as tf
# 함수형 api로 재구현
from tensorflow.keras import layers
from tensorflow.keras import Input
from tensorflow.keras.models import Model
# 사용 데이터셋 읽기
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import callbacks

# ResNet

# 함수형 api로 재구성
res_input = Input(shape=(150,150,3)) # input_layer / 150x150xRGB
# block1
# block1_conv1 : Conv2D layer / 64_filter, kenel 7x7, 이미지 크기 변하지 않도록 same padding
x = layers.Conv2D(filters=64, kernel_size=7, strides=2)(image_input)
output = layers.Dense(6, activation='softmax')(x) # 최종 클래스 6개