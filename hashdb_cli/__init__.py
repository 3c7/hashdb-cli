from sys import stderr
from typing import List

import requests
import typer
from typer import Typer

app = Typer()
sess = requests.Session()
sess.headers.update({
    "User-Agent": "hashdb-cli/0.1.0"
})


@app.command()
def algorithms(
        description: bool = typer.Option(False, "-d", "--description")
) -> None:
    """Load and dump available algorithms."""
    response = sess.get("https://hashdb.openanalysis.net/hash")

    if response.status_code != 200:
        typer.echo("Response code was not 200.", file=stderr)

    data = response.json()
    for algo in data.get("algorithms", []):
        typer.echo(algo.get('algorithm'), nl=False)
        if not description:
            typer.echo()
        else:
            description = algo.get('description').replace('\n', ' ')
            typer.echo(f"\t\t{description}({algo.get('type')})")


@app.command()
def get(
        algorithm: str = typer.Argument(..., help="The algorithm to use for lookup."),
        hash: str = typer.Argument(..., help="The hash to use for lookup."),
        hex: bool = typer.Option(False, "-h", "--hex", help="Given hash is in hex notation."),
        verbose: bool = typer.Option(False, "-v", "--verbose", help="Dump responses")
) -> None:
    """Get original strings for a given algorithm and a hash."""
    if not hex:
        hash = int(hash, 10)
    else:
        hash = int(hash, 16)
    response = sess.get(f"https://hashdb.openanalysis.net/hash/{algorithm}/{hash}")

    if response.status_code != 200:
        typer.echo("Response code was not 200 - probably algorithm or hash missing.", file=stderr)

    if verbose:
        typer.echo(response.json())

    data = response.json()
    for result in data.get("hashes", []):
        typer.echo(f"{result.get('hash')}: {result.get('string', {}).get('string')}")


@app.command()
def hunt(
        hashes: List[str] = typer.Argument(..., help="List of hashes."),
        hex: bool = typer.Option(False, "-h", "--hex", help="Given hashes are in hex notation."),
        verbose: bool = typer.Option(False, "-v", "--verbose", help="Dump responses")
):
    """Check if given hashes are available via different hash algorithms in the hashdb database."""
    data = []
    for h in hashes:
        if hex:
            data.append(int(h, 16))
        else:
            data.append(int(h, 10))

    response = sess.post("https://hashdb.openanalysis.net/hunt", json={"hashes": data})

    if response.status_code != 200:
        typer.echo("Response code was not 200 - probably algorithm or hash missing.", file=stderr)

    if verbose:
        typer.echo(response.json())

    data = response.json()
    for hit in data.get("hits", []):
        typer.echo(f"{hit.get('algorithm')}: {hit.get('count')}")


@app.command()
def resolve(
        hash: str = typer.Argument(..., help="Hash to resolve."),
        hex: bool = typer.Option(False, "-h", "--hex", help="Given hashes are in hex notation."),
        verbose: bool = typer.Option(False, "-v", "--verbose", help="Dump responses")
) -> None:
    """Try to hunt for a single hash and grab the string afterwards."""
    if not hex:
        hash = int(hash, 10)
    else:
        hash = int(hash, 16)

    response = sess.post("https://hashdb.openanalysis.net/hunt", json={"hashes": [hash]})

    if response.status_code != 200:
        typer.echo("Response code was not 200 - probably algorithm or hash missing.", file=stderr)

    if verbose:
        typer.echo(response.json())

    data = response.json().get("hits", [])
    if len(data) == 0:
        typer.echo("No hash found.")
    elif len(data) > 1:
        typer.echo("Multiple algorithms produce this hash.")
    else:
        response = sess.get(f"https://hashdb.openanalysis.net/hash/{data[0].get('algorithm')}/{hash}")

        if response.status_code != 200:
            typer.echo("Response code was not 200 - probably algorithm or hash missing.", file=stderr)

        if verbose:
            typer.echo(response.json())

        data = response.json()

        for result in data.get("hashes", []):
            typer.echo(f"{result.get('hash')}: {result.get('string', {}).get('string')}")


if __name__ == "__main__":
    app()
