class Warnings:
    def __init__(self, errors: list[str]):
        self.errors: list[str] = errors

    def __str__(self) -> str:
        """
         _____________________
        |        Avisos       |
        | essa é uma represen-|
        | tação de do quadro  |
        | de avisos           |
        |_____________________|
        """
        warnings: str = str().join((
            f" {' Avisos ':_^68}\n",
            f"|{68*' '}|\n"
        ))

        for error in self.errors:
            err_str: str = f"| {error:<66} |\n"
            warnings += err_str

        warnings += f"|{68*'_'}|"
        return warnings
