class TestLists(unittest.TestCase):
    def test_predictor():
        image = tf.placeholder(tf.float32, (None, 100, 100, 3)
        model = Model(image)
        sess = tf.Session()
        sess.run(tf.global_variables_initializer())
        before = sess.run(tf.trainable_variables())
        _ = sess.run(model.train, feed_dict={
            image: np.ones((1, 100, 100, 3)),
            })
            after = sess.run(tf.trainable_variables())
            for b, a, n in zip(before, after):
                # Make sure something changed.
                assert (b != a).any()