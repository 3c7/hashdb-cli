# HashDB CLI
For information about hashdb take a look at https://hashdb.openanalysis.net. This is a small python CLI which allows querying for hashes/algorithms from the commandline.

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
  algorithms  Load and dump available algorithms.
  get         Get original strings for a given algorithm and a hash.
  hunt        Check if given hashes are available via different hash...
  resolve     Try to hunt for a single hash and grab the string afterwards.
```
