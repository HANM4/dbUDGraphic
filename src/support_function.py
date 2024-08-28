# know in path extensions
def check_extensions_path(path: str, extensions: tuple[str, ...]) -> bool:
    for extension in extensions:
        if path.endswith(extension):
            return True
    return False
