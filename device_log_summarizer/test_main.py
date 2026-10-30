import unittest
from main import clean_sensor_readings


class TestCleanSensorReadings(unittest.TestCase):
    def test_converts_and_clips(self):
        self.assertEqual(clean_sensor_readings(["12.5", 700]), [12.5, 500.0])

    def test_drops_invalid_none_and_negative(self):
        self.assertEqual(clean_sensor_readings([None, "bad", -2, 0, "4"]), [0.0, 4.0])

    def test_empty_input(self):
        self.assertEqual(clean_sensor_readings([]), [])


if __name__ == "__main__":
    unittest.main()
