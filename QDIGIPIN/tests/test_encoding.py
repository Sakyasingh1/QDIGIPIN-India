"""
Test suite for DIGIPIN encoding
"""

import unittest
from core.digipin_engine import DigipinEncoder, DigipinValidator


class TestDigipinEncoding(unittest.TestCase):
    """Test DIGIPIN encoding functionality"""
    
    def test_encode_valid_coordinates(self):
        """Test encoding valid coordinates"""
        # New Delhi coordinates
        lat, lon = 28.6139, 77.2090
        digipin = DigipinEncoder.encode(lat, lon, 10)
        
        self.assertIsNotNone(digipin)
        self.assertEqual(len(digipin.replace('-', '')), 10)
    
    def test_encode_precision_levels(self):
        """Test different precision levels"""
        lat, lon = 28.6139, 77.2090
        
        for precision in range(1, 11):
            digipin = DigipinEncoder.encode(lat, lon, precision)
            self.assertEqual(len(digipin.replace('-', '')), precision)
    
    def test_encode_boundary_coordinates(self):
        """Test encoding at boundary coordinates"""
        # Test corners of India bounds
        test_coords = [
            (2.5, 63.5),    # SW corner
            (2.5, 99.5),    # SE corner
            (38.5, 63.5),   # NW corner
            (38.5, 99.5)    # NE corner
        ]
        
        for lat, lon in test_coords:
            digipin = DigipinEncoder.encode(lat, lon, 10)
            self.assertIsNotNone(digipin)
    
    def test_encode_invalid_coordinates(self):
        """Test encoding invalid coordinates"""
        # Out of India bounds
        with self.assertRaises(ValueError):
            DigipinEncoder.encode(0, 50, 10)  # Too far south
        
        with self.assertRaises(ValueError):
            DigipinEncoder.encode(40, 100, 10)  # Too far north/east
    
    def test_encode_batch(self):
        """Test batch encoding"""
        coords = [
            (28.6139, 77.2090),  # Delhi
            (19.0760, 72.8777),  # Mumbai
            (13.0827, 80.2707)   # Chennai
        ]
        
        digipins = DigipinEncoder.encode_batch(coords, 10)
        self.assertEqual(len(digipins), 3)
        
        for digipin in digipins:
            self.assertIsNotNone(digipin)
    
    def test_validate_coordinates(self):
        """Test coordinate validation"""
        # Valid coordinates
        is_valid, msg = DigipinValidator.validate_coordinates(28.6139, 77.2090)
        self.assertTrue(is_valid)
        
        # Invalid latitude
        is_valid, msg = DigipinValidator.validate_coordinates(100, 77.2090)
        self.assertFalse(is_valid)
        
        # Invalid longitude
        is_valid, msg = DigipinValidator.validate_coordinates(28.6139, 200)
        self.assertFalse(is_valid)


if __name__ == '__main__':
    unittest.main()
