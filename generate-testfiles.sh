#!/usr/bin/env bash

set -e

cd "$(dirname "${BASH_SOURCE[0]}")"

mkdir -p test/source/conflict
mkdir -p test/target/conflict

mkdir test/source/conflict/a
mkdir test/source/conflict/b
touch test/source/conflict/a/x
touch test/source/conflict/b/x

touch test/target/conflict/a
mkdir -p test/target/conflict/b/x

cd test/source

mkdir .git
touch .git/a

mkdir .gita
touch .gita/b

cp -R "$(dirname "${BASH_SOURCE[0]}")"/.git ./test
rm -rf test/objects
rm -rf test/hooks
rm -rf test/refs
rm -rf test/logs

touch file
mkdir empty
ln -s . loop

mkdir -p "deep/dumb path"
touch "deep/dumb path/dumb name 💩"

mkdir full
cd full
touch file
ln -s file soft
ln file hard
