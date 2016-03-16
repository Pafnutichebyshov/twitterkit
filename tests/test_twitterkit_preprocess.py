import chai

from twitterkit import preprocess


class ReplaceUrlsTest(chai.Chai):
    sentinel_value = 'url'

    def test_replaces_http_urls(self):
        input_text = 'http://www.blah.com'
        actual_output = preprocess.replace_url(input_text)
        self.assertEqual(self.sentinel_value, actual_output)

    def test_replaces_https_urls(self):
        input_text = 'https://www.t.co'
        actual_output = preprocess.replace_url(input_text)
        self.assertEqual(self.sentinel_value, actual_output)

    def test_replaces_urls_with_info_after_tld(self):
        input_text = 'https://www.t.co/kljkj787310#11/'
        actual_output = preprocess.replace_url(input_text)
        self.assertEqual(self.sentinel_value, actual_output)


class ReplaceAtUserTest(chai.Chai):
    sentinel_value = 'user'

    def test_replace_at_user(self):
        input_text = 'huh @hotlinebling'
        expected_output = 'huh user'
        actual_output = preprocess.replace_user(input_text)
        self.assertEqual(expected_output, actual_output)

    def test_replace_at_user_does_nothing(self):
        input_text = 'now you can run for your life'
        actual_output = preprocess.replace_user(input_text)
        self.assertEqual(input_text, actual_output)
