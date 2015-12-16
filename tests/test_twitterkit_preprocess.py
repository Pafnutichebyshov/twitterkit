import chai

from twitterkit import preprocess


class ConvertToLowerCaseTest(chai.Chai):
    def testConvertsCorrectly(self):
        input_data = ['HI', 'BYk']
        expected_output = ['hi', 'byk']
        actual_output = [i for i in preprocess.convertToLowerCase(input_data)]
        self.assertEqual(expected_output, actual_output)


class ReplaceUrlsTest(chai.Chai):
    pattern_matcher = preprocess.getPatternMatcher(preprocess.getUrlRegex())
    sentinel_value = 'URL'
    def testReplacesHttpUrl(self):
        input_text = 'http://www.blah.com'
        actual_output = preprocess.replacePattern(input_text, self.pattern_matcher, self.sentinel_value)
        self.assertEqual(self.sentinel_value, actual_output)

    def testReplacesHttpsUrl(self):
        input_text = 'https://www.blah.com'
        actual_output = preprocess.replacePattern(input_text, self.pattern_matcher, self.sentinel_value)
        self.assertEqual(self.sentinel_value, actual_output)

    def testReplacesUrlDoesNothingWithoutHttp(self):
        input_text = 'www.blah.com'
        actual_output = preprocess.replacePattern(input_text, self.pattern_matcher, self.sentinel_value)
        self.assertEqual(input_text, actual_output)


class ReplaceAtUserTest(chai.Chai):
    pattern_matcher = preprocess.getPatternMatcher(preprocess.getAtUserRegex())
    sentinel_value = 'AT_USER'
    def testReplacesAtUser(self):
        input_text = 'huh @hotlinebling'
        expected_output = 'huh AT_USER'
        actual_output = preprocess.replacePattern(input_text, self.pattern_matcher, self.sentinel_value)
        self.assertEqual(expected_output, actual_output)

    def testReplacesAtUserDoesNothing(self):
        input_text = 'now you can run for your life'
        actual_output = preprocess.replacePattern(input_text, self.pattern_matcher, self.sentinel_value)
        self.assertEqual(input_text, actual_output)
