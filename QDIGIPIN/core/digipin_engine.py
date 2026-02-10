"""
DIGIPIN Encoder and Decoder Engine
Core functionality for encoding coordinates to DIGIPIN and decoding back
"""

from .constants import DIGIPIN_GRID, BOUNDS, VALID_CHARS


class DigipinEncoder:
    """Encode latitude/longitude coordinates to DIGIPIN codes"""
    
    @staticmethod
    def encode(lat, lon, precision=10):
        """
        Encode a coordinate pair to DIGIPIN
        
        Args:
            lat (float): Latitude
            lon (float): Longitude
            precision (int): Precision level (1-10)
            
        Returns:
            str: DIGIPIN code
            
        Raises:
            ValueError: If coordinates are out of range
        """
        if lat < BOUNDS['minLat'] or lat > BOUNDS['maxLat']:
            raise ValueError(f'Latitude {lat} out of range [{BOUNDS["minLat"]}, {BOUNDS["maxLat"]}]')
        if lon < BOUNDS['minLon'] or lon > BOUNDS['maxLon']:
            raise ValueError(f'Longitude {lon} out of range [{BOUNDS["minLon"]}, {BOUNDS["maxLon"]}]')
        
        if precision < 1 or precision > 10:
            raise ValueError(f'Precision must be between 1 and 10, got {precision}')
        
        min_lat = BOUNDS['minLat']
        max_lat = BOUNDS['maxLat']
        min_lon = BOUNDS['minLon']
        max_lon = BOUNDS['maxLon']
        
        digipin = ''
        
        for level in range(1, precision + 1):
            lat_div = (max_lat - min_lat) / 4
            lon_div = (max_lon - min_lon) / 4
            
            # REVERSED row logic (to match original)
            row = 3 - int((lat - min_lat) / lat_div)
            col = int((lon - min_lon) / lon_div)
            
            # Clamp to valid range
            row = max(0, min(row, 3))
            col = max(0, min(col, 3))
            
            digipin += DIGIPIN_GRID[row][col]
            
            # Add hyphens at positions 3 and 6
            if level == 3 or level == 6:
                digipin += '-'
            
            # Update bounds (reverse logic for row)
            max_lat = min_lat + lat_div * (4 - row)
            min_lat = min_lat + lat_div * (3 - row)
            
            min_lon = min_lon + lon_div * col
            max_lon = min_lon + lon_div
        
        return digipin
    
    @staticmethod
    def encode_batch(coordinates, precision=10):
        """
        Encode multiple coordinate pairs
        
        Args:
            coordinates (list): List of (lat, lon) tuples
            precision (int): Precision level
            
        Returns:
            list: List of DIGIPIN codes
        """
        results = []
        for lat, lon in coordinates:
            try:
                digipin = DigipinEncoder.encode(lat, lon, precision)
                results.append(digipin)
            except ValueError as e:
                results.append(None)
        return results


class DigipinDecoder:
    """Decode DIGIPIN codes to latitude/longitude coordinates"""
    
    @staticmethod
    def decode(digipin):
        """
        Decode a DIGIPIN to its center coordinates and bounds
        
        Args:
            digipin (str): DIGIPIN code (with or without hyphens)
            
        Returns:
            dict: Dictionary with 'latitude', 'longitude', 'bounds'
            
        Raises:
            ValueError: If DIGIPIN is invalid
        """
        # Remove hyphens
        pin = digipin.replace('-', '')
        
        if len(pin) < 1 or len(pin) > 10:
            raise ValueError(f'Invalid DIGIPIN length: {len(pin)}. Must be 1-10 characters.')
        
        # Validate characters
        for char in pin:
            if char not in VALID_CHARS:
                raise ValueError(f'Invalid character in DIGIPIN: {char}')
        
        min_lat = BOUNDS['minLat']
        max_lat = BOUNDS['maxLat']
        min_lon = BOUNDS['minLon']
        max_lon = BOUNDS['maxLon']
        
        for i, char in enumerate(pin):
            # Locate character in DIGIPIN grid
            found = False
            ri, ci = -1, -1
            
            for r in range(4):
                for c in range(4):
                    if DIGIPIN_GRID[r][c] == char:
                        ri, ci = r, c
                        found = True
                        break
                if found:
                    break
            
            if not found:
                raise ValueError(f'Invalid character in DIGIPIN: {char}')
            
            lat_div = (max_lat - min_lat) / 4
            lon_div = (max_lon - min_lon) / 4
            
            lat1 = max_lat - lat_div * (ri + 1)
            lat2 = max_lat - lat_div * ri
            lon1 = min_lon + lon_div * ci
            lon2 = min_lon + lon_div * (ci + 1)
            
            # Update bounding box for next level
            min_lat = lat1
            max_lat = lat2
            min_lon = lon1
            max_lon = lon2
        
        center_lat = (min_lat + max_lat) / 2
        center_lon = (min_lon + max_lon) / 2
        
        return {
            'latitude': round(center_lat, 6),
            'longitude': round(center_lon, 6),
            'bounds': {
                'minLat': round(min_lat, 6),
                'maxLat': round(max_lat, 6),
                'minLon': round(min_lon, 6),
                'maxLon': round(max_lon, 6)
            }
        }
    
    @staticmethod
    def decode_batch(digipins):
        """
        Decode multiple DIGIPIN codes
        
        Args:
            digipins (list): List of DIGIPIN codes
            
        Returns:
            list: List of decoded dictionaries
        """
        results = []
        for digipin in digipins:
            try:
                decoded = DigipinDecoder.decode(digipin)
                results.append(decoded)
            except ValueError:
                results.append(None)
        return results


class DigipinValidator:
    """Validate DIGIPIN codes and coordinates"""
    
    @staticmethod
    def validate_coordinates(lat, lon):
        """
        Validate latitude and longitude
        
        Returns:
            tuple: (is_valid, error_message)
        """
        if not isinstance(lat, (int, float)):
            return False, "Latitude must be a number"
        if not isinstance(lon, (int, float)):
            return False, "Longitude must be a number"
        
        if lat < BOUNDS['minLat'] or lat > BOUNDS['maxLat']:
            return False, f"Latitude must be between {BOUNDS['minLat']} and {BOUNDS['maxLat']}"
        if lon < BOUNDS['minLon'] or lon > BOUNDS['maxLon']:
            return False, f"Longitude must be between {BOUNDS['minLon']} and {BOUNDS['maxLon']}"
        
        return True, ""
    
    @staticmethod
    def validate_digipin(digipin):
        """
        Validate DIGIPIN format
        
        Returns:
            tuple: (is_valid, error_message)
        """
        if not isinstance(digipin, str):
            return False, "DIGIPIN must be a string"
        
        # Remove hyphens
        pin = digipin.replace('-', '')
        
        if len(pin) < 1 or len(pin) > 10:
            return False, f"DIGIPIN must be 1-10 characters (got {len(pin)})"
        
        # Check for invalid characters
        invalid_chars = [c for c in pin if c not in VALID_CHARS]
        if invalid_chars:
            return False, f"Invalid characters: {', '.join(invalid_chars)}"
        
        return True, ""
    
    @staticmethod
    def format_digipin(digipin, add_hyphens=True):
        """
        Format DIGIPIN with or without hyphens
        
        Args:
            digipin (str): DIGIPIN code
            add_hyphens (bool): Whether to add hyphens
            
        Returns:
            str: Formatted DIGIPIN
        """
        # Remove existing hyphens
        pin = digipin.replace('-', '')
        
        if not add_hyphens or len(pin) <= 3:
            return pin
        
        # Add hyphens at positions 3 and 6
        formatted = pin[:3]
        if len(pin) > 3:
            formatted += '-' + pin[3:6]
        if len(pin) > 6:
            formatted += '-' + pin[6:]
        
        return formatted
