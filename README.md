## What is this?
This is a simple utility to extract nicely formated code from a Zeppelin notebook

## How does it work
The utility extract the code for the given interpreters and tries to nicdely format comments based on Zeppelin
interpreter titles and md blocks.

## Usage Cases
1) You want to extract all code blocks from all interpreters. The result may not be able to run as it is likely a mix of different languages
   but it is convenenient if you want to diff your changes. Use 'all' for extract option.
2) You want to extract the code blocks specific to a given language. The result may be able to run. Stiill, you typically have to deal with 
   graphing outputs in a non interactive way when you move from a notebook to a script. You will have to handle this yourself. 

## Limitations
* You may have to customize the interpreters list for your target languages and for 'all'
* Change the default Zeppelin notebook directory if it does not match yours

## Possible developments
Add this under Zeppelin menu with an interactive list of intepretersd to include

## Examples
* zep2code all  *.json                                 -> produces a file for each .json notebook into a code subfolder, add them to git
* python ./zep2code.py 2E27K8X9M /tmp/test3.py  python -> produces a .py file runable in interactive mode
* python ./zep2code.py 2E27K8X9M /tmp/test3.r   r      -> produces a .r  file runable in interactive mode
* python ./zep2code.py 2E27K8X9M /tmp/test3.all all    -> produces a likely not runable file useful for checking code differences

## Author(s)
Initial idea from https://github.com/sat28/zeppelin_notebook_to_script/blob/master/zeppelin_to_script.py
Then all improvements by G. Demaneuf.

