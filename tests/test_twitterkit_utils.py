import chai

from twitterkit import utils


class ExtractValueTest(chai.Chai):
    def test_extracted_key_present(self):
        fake_name = 'hank_williams'
        data = {
            'users': fake_name,
        }
        actual_output = utils.extract_value(data, 'users')
        self.assertEqual(fake_name, actual_output)

    def test_extracted_key_absent(self):
        fake_name = 'hank_williams'
        data = {
            'users': fake_name,
        }
        expected_output = 'null'
        actual_output = utils.extract_value(data, 'wat')
        self.assertEqual(expected_output, actual_output)

    def test_extracted_nested_key_value(self):
        data = {
            'users': {'first_name': 'hank', 'surname': 'williams'},
        }
        expected_output = 'hank'
        actual_output = utils.extract_value(data, 'users.first_name')
        self.assertEqual(expected_output, actual_output)


class ExtractUserTest(chai.Chai):
    def test_extract_user(self):
        fake_name = 'hank_williams'
        user_id = '111'
        created_at = 'whatever'
        data = {
            'user': {
                'id_str': user_id,
                'screen_name': fake_name,
                'created_at': created_at
            },
        }
        expected_output = {
            'user_id': user_id,
            'screen_name': fake_name,
            'created_at': created_at,
        }
        actual_output = utils.extract_user(data)
        self.assertEqual(expected_output, actual_output)


class ExtractTextTest(chai.Chai):
    def test_extract_text(self):
        id_str = 'blah'
        user_id = '111'
        created_at = 'whatever'
        source = 'null'
        coordinates = [1, 1]
        text = 'yolo'
        full_name = 'Shinjuku'
        country_code = 'jp'
        data = {
            'created_at': created_at,
            'id_str': id_str,
            'text': text,
            'source': source,
            'user': {
                'id_str': user_id,
            },
            'coordinates': {'coordinates': coordinates},
            'place': {'full_name': full_name, 'country_code': country_code}
        }
        expected_output = {
            'id_str': id_str,
            'user_id': user_id,
            'created_at': created_at,
            'source': source,
            'text': text,
            'longitude': 1,
            'latitude': 1,
            'full_name': full_name,
            'name': 'null',
            'country_code': country_code,
        }
        actual_output = utils.extract_text(data)
        self.assertEqual(expected_output, actual_output)

    def test_extract_text_sans_coordinates(self):
        id_str = 'blah'
        user_id = '111'
        created_at = 'whatever'
        source = 'null'
        text = 'yolo'
        data = {
            'created_at': created_at,
            'id_str': id_str,
            'text': text,
            'source': source,
            'user': {
                'id_str': user_id,
            },
        }
        expected_output = {
            'id_str': id_str,
            'user_id': user_id,
            'created_at': created_at,
            'source': source,
            'text': text,
            'longitude': 'null',
            'latitude': 'null',
            'full_name': 'null',
            'name': 'null',
            'country_code': 'null',
        }
        actual_output = utils.extract_text(data)
        self.assertEqual(expected_output, actual_output)


class ExtractEntityTest(chai.Chai):
    def test_extract_single_entity(self):
        entity_value = 'kanyewest'
        data = {
            'entities': {
                'hashtags': [{'text': entity_value}]
            }
        }
        actual_output = utils.extract_entity(data, 'entities.hashtags', 'text')
        self.assertEqual(entity_value, actual_output)

    def test_extract_multiple_entity(self):
        value_1 = 'kanyewest'
        value_2 = 'dannybrown'
        data = {
            'entities': {
                'hashtags': [{'text': value_1}, {'text': value_2}]
            }
        }
        expected_output = '{}/{}'.format(value_1, value_2)
        actual_output = utils.extract_entity(data, 'entities.hashtags', 'text')
        self.assertEqual(expected_output, actual_output)
