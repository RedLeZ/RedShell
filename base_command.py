class BaseCommand:
    """
    Optional base class for RedShell commands.

    Contract:
    - Provide attributes:
        - name: str
        - flags: list[str]
        - description: str
    - Implement:
        - run(self, *args) -> str | None

    The shell prints returned strings. Return None or an empty string to print nothing.
    Avoid printing inside commands to keep UX consistent and enable redirection.
    """

    name: str = ""
    flags: list[str] = []
    description: str = ""

    def run(self, *args):
        raise NotImplementedError
