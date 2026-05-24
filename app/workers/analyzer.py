def analyze_code(content):

    review = []

    if "print(" in content:
        review.append(
            "Found print statement"
        )

    if "password" in content.lower():
        review.append(
            "Possible hardcoded credential"
        )

    if len(content) > 1000:
        review.append(
            "Large file detected"
        )

    return review