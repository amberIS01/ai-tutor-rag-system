"""
Compression Module
Data compression utilities with response compression support
"""

import gzip
import zlib
from typing import Tuple
from logger import logger
from starlette.middleware.gzip import GZipMiddleware


class Compressor:
    """Data compression utilities"""
    
    # Minimum response size for compression (bytes)
    MIN_SIZE_FOR_COMPRESSION = 1000
    
    @staticmethod
    def compress_gzip(data: bytes) -> Tuple[bool, bytes]:
        """Compress data using gzip"""
        try:
            compressed = gzip.compress(data, compresslevel=9)
            ratio = (1 - len(compressed) / len(data)) * 100 if data else 0
            logger.info(f"Gzip compression: {ratio:.1f}% reduction")
            return True, compressed
        except Exception as e:
            logger.error(f"Gzip compression failed: {str(e)}")
            return False, data
    
    @staticmethod
    def decompress_gzip(data: bytes) -> Tuple[bool, bytes]:
        """Decompress gzip data"""
        try:
            decompressed = gzip.decompress(data)
            return True, decompressed
        except Exception as e:
            logger.error(f"Gzip decompression failed: {str(e)}")
            return False, data
    
    @staticmethod
    def compress_zlib(data: bytes, level: int = 6) -> Tuple[bool, bytes]:
        """Compress data using zlib"""
        try:
            compressed = zlib.compress(data, level=level)
            ratio = (1 - len(compressed) / len(data)) * 100 if data else 0
            logger.info(f"Zlib compression: {ratio:.1f}% reduction")
            return True, compressed
        except Exception as e:
            logger.error(f"Zlib compression failed: {str(e)}")
            return False, data
    
    @staticmethod
    def decompress_zlib(data: bytes) -> Tuple[bool, bytes]:
        """Decompress zlib data"""
        try:
            decompressed = zlib.decompress(data)
            return True, decompressed
        except Exception as e:
            logger.error(f"Zlib decompression failed: {str(e)}")
            return False, data
    
    @staticmethod
    def get_compression_ratio(original_size: int, compressed_size: int) -> float:
        """Calculate compression ratio"""
        if original_size == 0:
            return 0.0
        return (1 - compressed_size / original_size) * 100
