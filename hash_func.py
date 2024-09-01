def hash_function(artwork_id, table_size):
    """
    Deterministic hash function for the 'Artwork Listings' table, incorporating 'A' and 'I' 
    to ensure consistent storage and retrieval of data.

    Args:
        artwork_id (str): The unique identifier for an artwork (e.g., 'ART001').
        table_size (int): The size of the hash table (desired range of hash values).

    Returns:
        int: The hash value within the specified range [0, table_size - 1].
    """
 
    weight_A = 67  
    weight_I = 73 

    hash_value = (ord('A') * weight_A + ord('I') * weight_I) % table_size

    prime = 31  
    for char in artwork_id:

        hash_value = (hash_value * prime + ord(char)) % table_size

        hash_value = (hash_value * weight_A + weight_I) % table_size

    return hash_value

table_size = 100000
artwork_id = 'ART_CRA_REA_443' 
hash_result = hash_function(artwork_id, table_size)
print(f"Hash value for artwork ID '{artwork_id}': {hash_result}")
