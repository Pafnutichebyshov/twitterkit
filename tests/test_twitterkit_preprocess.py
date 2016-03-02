import chai

from twitterkit import preprocess


class ConvertToLowerCaseTest(chai.Chai):
    def testConvertsCorrectly(self):
        input_data = ['HI', 'BYk']
        expected_output = ['hi', 'byk']
        actual_output = [i for i in preprocess.convert_to_lowercase(input_data)]
        self.assertEqual(expected_output, actual_output)


class ReplaceUrlsTest(chai.Chai):
    pattern_matcher = preprocess.get_pattern_matcher(preprocess.get_url_regex())
    sentinel_value = 'URL'
    def test_replaces_http_urls(self):
        input_text = 'http://www.blah.com'
        actual_output = preprocess.replace_pattern(
            input_text, self.pattern_matcher, self.sentinel_value)
        self.assertEqual(self.sentinel_value, actual_output)

    def test_replaces_https_urls(self):
        input_text = 'https://www.t.co'
        actual_output = preprocess.replace_pattern(
            input_text, self.pattern_matcher, self.sentinel_value)
        self.assertEqual(self.sentinel_value, actual_output)

    def test_replaces_when_link_lacks_http(self):
        input_text = 'www.blah.com'
        actual_output = preprocess.replace_pattern(input_text, self.pattern_matcher, self.sentinel_value)
        self.assertEqual(self.sentinel_value, actual_output)

    def test_replaces_urls_with_info_after_tld(self):
        input_text = 'https://www.t.co/kljkj787310#11/'
        actual_output = preprocess.replace_pattern(
            input_text, self.pattern_matcher, self.sentinel_value)
        self.assertEqual(self.sentinel_value, actual_output)



class ReplaceAtUserTest(chai.Chai):
    pattern_matcher = preprocess.get_pattern_matcher(preprocess.get_at_user_regex())
    sentinel_value = 'AT_USER'

    def test_replace_at_user(self):
        input_text = 'huh @hotlinebling'
        expected_output = 'huh AT_USER'
        actual_output = preprocess.replace_pattern(
            input_text, self.pattern_matcher, self.sentinel_value)
        self.assertEqual(expected_output, actual_output)

    def test_replace_at_user_does_nothing(self):
        input_text = 'now you can run for your life'
        actual_output = preprocess.replace_pattern(
            input_text, self.pattern_matcher, self.sentinel_value)
        self.assertEqual(input_text, actual_output)


class RemoveStringPatternsTest(chai.Chai):
    def test_removes_at_users(self):
        pattern_matcher = preprocess.get_pattern_matcher(preprocess.get_at_user_regex())
        test_input = '@sleep @holymountain'
        expected_output = ''
        actual_output = preprocess.remove_pattern(test_input, pattern_matcher)
        self.assertEqual(expected_output, actual_output)

    def test_removes_nothing(self):
        pattern_matcher = preprocess.get_pattern_matcher(preprocess.get_at_user_regex())
        test_input = 'watch the throne'
        expected_output = 'watch the throne'
        actual_output = preprocess.remove_pattern(test_input, pattern_matcher)
        self.assertEqual(expected_output, actual_output)

    def test_removes_single_user(self):
        pattern_matcher = preprocess.get_pattern_matcher(preprocess.get_at_user_regex())
        test_input = '@nas watch the throne'
        expected_output = 'watch the throne'
        actual_output = preprocess.remove_pattern(test_input, pattern_matcher)
        self.assertEqual(expected_output, actual_output)

    def test_removes_multiple_users(self):
        pattern_matcher = preprocess.get_pattern_matcher(preprocess.get_at_user_regex())
        test_input = '@nas watch the throne @jayz'
        expected_output = 'watch the throne'
        actual_output = preprocess.remove_pattern(test_input, pattern_matcher)
        self.assertEqual(expected_output, actual_output)

    def test_removes_urls(self):
        pattern_matcher = preprocess.get_pattern_matcher(preprocess.get_url_regex())
        test_input = 'http://t.co watch the throne http://ny.com'
        expected_output = 'watch the throne'
        actual_output = preprocess.remove_pattern(test_input, pattern_matcher)
        self.assertEqual(expected_output, actual_output)

    def test_removes_users_and_urls(self):
        url_matcher = preprocess.get_pattern_matcher(preprocess.get_url_regex())
        user_matcher = preprocess.get_pattern_matcher(preprocess.get_at_user_regex())
        test_input = '@jayz http://t.co watch the throne'
        expected_output = 'watch the throne'
        tmp_output = preprocess.remove_pattern(test_input, url_matcher)
        actual_output = preprocess.remove_pattern(tmp_output, user_matcher)
        self.assertEqual(expected_output, actual_output)
