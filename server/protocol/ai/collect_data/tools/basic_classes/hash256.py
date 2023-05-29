import hashlib

class Hashing:
    """
    A class for generating hash values using various algorithms.
    """

    @staticmethod
    def sha256(string: str) -> str:
        """
        Generates the SHA-256 hash value of the input string.

        Args:
            string (str): The string to be hashed.

        Returns:
            str: The hexadecimal representation of the hash value.
        """
        return hashlib.sha256(string.encode()).hexdigest()
