```
reclink - link files recursively
-r, --replace               replace existing targets
-l, --links                 link to softlinks
-s, --source {{PATH}}       path to source directory
-t, --target {{PATH}}       path to target directory
-i, --ignore {{PATH,PATH}}  relative paths to be ignored
-q, --quiet                 skip user confirmation
-h, --help                  display this help message and exit
-v, --version               display version message and exit
```
```
./reclink.py -rlq --source /wormhole/dotfiles --target /home/user --ignore ".git, foo/bar"
```
