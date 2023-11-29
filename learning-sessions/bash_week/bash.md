# Bash

## What is bash?

- Shell (sh) is a command interpreter in Unix based systems
- Bourne again shell (bash) is the same thing but improves upon sh
- Macs have zsh since Catalina

## How do you bash?

Shebang: line at the top of the script to specify which interpreter you want to run the script with by default

```bash
# if you put the shebang like so
#!/bin/bash

# and if you run the script like so
./script.sh
# it'll actually do
/bin/bash script.sh
```

Storing variables:

```bash
s="school"
echo $s
```

Storing cmds

```bash
files=$(ls)
echo $files
```

If condition

```bash
a=2
b=3
if [ "$a" -lt "$b" ]; then
    echo "a is bigger than b"
fi
```

For loop:

```bash
for i in $(ls); do echo $i; done

for i in $(ls); do
    echo $i
done
```

While loop:

```bash
value=0
while [ $value -lt 10 ]; do
    echo $value
    # note the different notation when manipulating numbers
    value=$((value+1))      
done
```

## Conditions

Bash is annoying for comparing things

Numbers

```bash
a=2
b=3
if [ "$a" -lt "$b" ]; then
    echo "a is lower than b"
fi

# this is not supported in every shell
if (( $a < $b )); then
    echo "a is lower than b"
fi

if [ "$b" -gt "$a" ]; then
    echo "b is greater than a"
fi

-eq # equal
-ne # not equal
-lt # less than
-le # less than or equal
-gt # greater than
-ge # greater than or equal
```

Strings (https://linuxize.com/post/how-to-compare-strings-in-bash/)

```bash
a="string_a"
b="string_b"

# simple equality test is simple square brackets
if [ "$a" = "$b" ]; then  
    echo "a is equal to b"
fi

if [ "$a" != "$b" ]; then
    echo "a is not equal to b"
fi

# double square brackets is used for pattern matching
if [[ "$a" == "string"* ]]; then  
    echo "a is kinda equal to b"
fi

# Everybody's favorite friend: regex (https://regexr.com/ )
if [[ "$a" =~ .*[_].* ]]; then
    echo "the regex works"
fi
```

## Useful commands to know in cmd line

- cat: output the whole file given
- zcat: output the compressed file given
- tar: archiving utility tool
- gzip: compress files to .gz
- gunzip: uncompress .gz files
- cut: get specific columns
- grep: find substring in a file
- ls: list files in a directory
- awk: manipulate file line by line (powerful tool that would require its dedicated session)
- sed: text manipulation

## Piping, stdout, stderr and more stuff

Piping is the act of combining cmds in the same line and using the output of the previous cmd for the next.

```bash
grep gentoo penguin.txt | cut -d"," -f2
```

You can capture that output using

```bash
grep gentoo penguin.txt | cut -d"," -f2 > output_file.txt
```

You can also capture errors

```bash
sh penguin.txt 2> error.log
```

## Scripting

Best practices: https://google.github.io/styleguide/shellguide.html

Use `set -e` as a bare minimum when writing a script. This will stop the script when it encounters an error.

Use `{}` when writing a variable name. `${variable}` will make clear which is a variable when you want to add a prefix or suffix to that variable.
