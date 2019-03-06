import tensorflow as tf

from mygen import Generator
from poem_translate import poem_translate

BATCH_SIZE = 128
EMB_DIM = 128           # embedding dimension
HIDDEN_DIM = 128        # hidden state dimension of lstm cell
SEQ_LENGTH = 28         # sequence length
START_TOKEN = 0
vocab_size = 4987       # max idx of word token = 4986


def generate_samples(batch_size, generated_num, output_file):
    with tf.Session() as sess:
        generator_model = Generator(vocab_size, BATCH_SIZE, EMB_DIM, HIDDEN_DIM, SEQ_LENGTH, START_TOKEN)
        # saver = tf.train.import_meta_graph('Model/model.meta')
        saver = tf.train.Saver()
        saver.restore(sess, tf.train.latest_checkpoint("Model/"))
        sess.run(tf.local_variables_initializer())
        generated_samples = []
        for i in range(generated_num // batch_size):
            one_batch = generator_model.generate(sess)
            generated_samples.extend(one_batch)
    with open(output_file, 'w') as fout:
        for poem in generated_samples:
            buffer = ' '.join([str(x) for x in poem]) + '\n'
            fout.write(buffer)


def generate_poem():
    # 输出文件名，注意输出的是纯数字，便于做处理
    int_file = "./i_output.txt"
    # 输出文件名，这里是输出的绝句
    poem_file = "./poem_output.txt"
    # 生成诗歌的数量，不用刻意写成128的倍数
    generated_num = 10000
    # BATCH_SIZE=128，即一次写128首诗，即写的数量是128的整数倍，余数自动去掉
    generate_samples(BATCH_SIZE, generated_num, int_file)
    poem_translate(int_file, poem_file)
    # generate_samples生成纯数字文本，poem_translate生成诗歌文本，输出文件在根目录


if __name__ == '__main__':
    generate_poem()
