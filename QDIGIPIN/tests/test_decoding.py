"""
Test suite for DIGIPIN decoding
"""

import unittest
from core.digipin_engine import DigipinDecoder, DigipinValidator, DigipinEncoder


class TestDigipinDecoding(unittest.TestCase):
    """Test DIGIPIN decoding functionality"""
    
    def test_decode_valid_digipin(self):
        """Test decoding valid DIGIPIN"""
        digipin = "FCJ-3K4-LM9"
        result = DigipinDecoder.decode(digipin)
        
        self.assertIn('latitude', result)
        self.assertIn('longitude', result)
        self.assertIn('bounds', result)
    
    def test_decode_without_hyphens(self):
        """Test decoding DIGIPIN without hyphens"""
        digipin = "FCJ3K4LM9"
        result = DigipinDecoder.decode(digipin)
        
        self.assertIsNotNone(result)
        self.assertIn('latitude', result)
    
    def test_decode_different_precisions(self):
        """Test decoding DIGIPINs of different lengths"""
        digipins = [
            "F",
            "FC",
            "FCJ",
            "FCJ3",
            "FCJ3K",
            "FCJ3K4",
            "FCJ3K4L",
            "FCJ3K4LM",
            "FCJ3K4LM9",
            "FCJ3K4LM92"
        ]
        
        for digipin in digipins:
            result = DigipinDecoder.decode(digipin)
            self.assertIsNotNone(result)
    
    def test_decode_invalid_digipin(self):
        """Test decoding invalid DIGIPIN"""
        # Invalid character
        with self.assertRaises(ValueError):
            DigipinDecoder.decode("ABC123")
        
        # Too long
        with self.assertRaises(ValueError):
            DigipinDecoder.decode("FCJ3K4LM9287P")
    
    def test_encode_decode_roundtrip(self):
        """Test that encoding and decoding are consistent"""
        # Original coordinates
        orig_lat, orig_lon = 28.6139, 77.2090
        
        # Encode
        digipin = DigipinEncoder.encode(orig_lat, orig_lon, 10)
        
        # Decode
        result = DigipinDecoder.decode(digipin)
        
        # The decoded center should be close to original
        # (within the precision of level 10, which is ~3.4m)
        self.assertAlmostEqual(result['latitude'], orig_lat, places=4)
        self.assertAlmostEqual(result['longitude'], orig_lon, places=4)
    
    def test_validate_digipin(self):
        """Test DIGIPIN validation"""
        # Valid DIGIPIN
        is_valid, msg = DigipinValidator.validate_digipin("FCJ-3K4-LM9")
        self.assertTrue(is_valid)
        
        # Invalid character
        is_valid, msg = DigipinValidator.validate_digipin("ABC-123-XYZ")
        self.assertFalse(is_valid)
        
        # Too long
        is_valid, msg = DigipinValidator.validate_digipin("FCJ3K4LM9287P56")
        self.assertFalse(is_valid)
    
    def test_format_digipin(self):
        """Test DIGIPIN formatting"""
        # Add hyphens
        formatted = DigipinValidator.format_digipin("FCJ3K4LM92", add_hyphens=True)
        self.assertEqual(formatted, "FCJ-3K4-LM92")
        
        # Remove hyphens
        formatted = DigipinValidator.format_digipin("FCJ-3K4-LM92", add_hyphens=False)
        self.assertEqual(formatted, "FCJ3K4LM92")


if __name__ == '__main__':
    unittest.main()
