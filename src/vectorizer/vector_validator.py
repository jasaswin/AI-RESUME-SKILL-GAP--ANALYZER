def validate_vectors(vectors):
    """
    Validate TF-IDF vectors before similarity computation
    """
    if vectors is None:
        raise ValueError("Vectors are None")

    if vectors.shape[0] != 2:
        raise ValueError("Expected exactly 2 vectors (resume & JD)")

    if vectors.shape[1] == 0:
        raise ValueError("No features found in vector space")

    return True
