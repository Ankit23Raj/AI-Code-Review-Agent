def get_file_content(
    repo_name,
    file_path
):

    repo = get_repository(
        repo_name
    )

    file = repo.get_contents(
        file_path
    )

    return file.decoded_content.decode(
        "utf-8"
    )