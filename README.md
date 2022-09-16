# HashDB CLI
For information about hashdb take a look at https://hashdb.openanalysis.net. This is a small python CLI which allows querying for hashes/algorithms from the commandline.

## Installation

```
pip install hashdb-cli
```

## Usage

```
Usage: hashdb [OPTIONS] COMMAND [ARGS]...

Options:
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.
  --help                          Show this message and exit.

Commands:
  add         Add a new string to hashdb
  algorithms  Load and dump available algorithms.
  get         Get original strings for a given algorithm and a hash.
  hunt        Check if given hashes are available via different hash...
  resolve     Try to hunt for a single hash and grab the string afterwards.
  string      Get information about a string which is already available...
```

### List algorithms

```
hashdb algorithms (--description)
```

### Get string
Hashdb requires the hash to be an unsigned integer, however, hex strings can be used in combination with `-h/--hex` parameter.

```
hashdb get (--hex) <algo_name> <hash>
```

### Hunt
Pass multiple hashes to the API in order to find a fitting algorithm.

```
hashdb hunt <h1> <h2> <h3> ... <hn> (--hex)
```

### Resolve
Combination of hunt and get.

```
hashdb resolve <h1> ... <hn>
```

### String
Get information about a string in the database

```
hashdb string <string>
```
