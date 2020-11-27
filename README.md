```
reclink - link files recursively
-s, --source {{PATH}}             path to source directory
-t, --target {{PATH}}             path to target directory
-i, --ignore {{PATH}} {{PATH}}    relative paths to be ignored
-r, --replace                     replace existing targets
-l, --links                       link to softlinks
-q, --quiet                       skip user confirmation
-h, --help                        display this help message and exit
```
```
./reclink.py -rq --source "/wormhole/dotfiles" --target "/home/user" --ignore ".git" "foo/bar"
```
