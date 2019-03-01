##
## Initial idea from https://github.com/sat28/zeppelin_notebook_to_script/blob/master/zeppelin_to_script.py
## Then all improvements by G. Demaneuf.

# Libs
import sys
import json
import codecs

def exportNotebook( infile,
                    outfile,
                    what            = 'all',
                    mdiscomment     = True,
                    blocktype       = False,
                    debug           = False):
    """
    A utility to convert Zeppelin notebooks to files.

    How does that work?
    - The paragraphs which texts start with the chosen interpreter keys (what) will be included in the output.
    - Comments are taken from:
        The titles of the what sections
        The content of the md sections

    Arguments:
    - infile        : infile, either full pathname or just zeppelin notebook ID as in /opt/zeppelin/notebooks/ID/note.json
    - outfile       : output file
    - what          : an iterable of interpreters to include without the %
    - mdascomment   : whether to use md blocks as comments
    """

    # Process arguments
    # There may be a better way to do that - for the time being make sure that your interpreters of interest
    # are listed below
    what = what.lower()
    if what    == 'python':
        what   = ['python', 'spark.pyspark', 'pyspark', 'python2', 'python3', 'spark_test.pyspark']
    elif what  == 'scala':
        what   = ['scala']
    elif what  == 'r':
        what   = ['r', 'spark.r', 'spark-gf.r', 'spark_test.r'] 
    elif what  == 'sql':
        what   = ['sql', 'spark-nlp.sql', 'spark.sql'] 
    elif what  == 'sh':
        what   = ['sh', 'sh_zepp']

    if debug:
        print("0: {}".format(what))
    
    # Load notebook
    notebook = json.load(codecs.open(infile, 'r', 'utf-8-sig'))
    
    # Build script
    script = []
    
    for paragraph in notebook["paragraphs"]:
        # Paragraph Content
        lines       = paragraph["text"].splitlines()

        if len(lines) > 0:
            interpreter  = lines[0][1:].strip() 
            block        = lines[1:]

            # Ignore blank line after interpreter
            if (len(block) > 0) and (block[0] == ''):
                block = block[1:]

            if debug:
                print("1: [{}]".format(interpreter))
                print("2: {}".format(block))

            text = ''

            if (interpreter in what) or (what == 'all'):
                # Paragraph interpreter
                if (blocktype is True) or (what == 'all'):
                    text        = text + '# <{}>\n'.format(interpreter)

                # Paragraph Title
                if "title" in paragraph.keys():
                    text        = text + "## {}\n".format(paragraph["title"])

                # Paragraph Text
                text     = text + '\n'.join(block)

                # Everything together for that block
                script.append(text)

                if debug:
                    print("3: {}".format(text))
            elif (interpreter == "md") and mdiscomment and ('<style>' not in block) and ('%%%' not in block) and (what != 'all'):
                # md treated as comment
                # We do not process <style> or %%% blocks
                # We do not process <div> lines
                text     = ["# " + s.replace('# ', '').replace('#', '') for s in block if s[:4] != '<div']
                text     = '\n'.join(text)
                script.append(text)

                if debug:
                    print("3: {}".format(text))
    
    # Final script
    script_f = '\n\n'.join(script)
    
    # Save script
    with open(outfile, 'w') as the_file:
        the_file.write(script_f)


############################################################################
## Can be run directlty as a scrip over a notebook
##
## Usage Cases:
## - python ./zep2code.py 2E27K8X9M /tmp/test3.py  python -> produces a .py file runable in interactive mode
## - python ./zep2code.py 2E27K8X9M /tmp/test3.r   r      -> produces a .r  file runable in interactive mode
## - python ./zep2code.py 2E27K8X9M /tmp/test3.all all    -> produces a likely not runable file useful for checking code differences
############################################################################

if __name__ == '__main__':

    # Check arguments
    if len(sys.argv) > 4:
        raise Exception("no more than 3 arguments: infile, outfile, list of interprenters")

    # Get input / output
    if sys.argv[1].find('/') == -1:
        # No '/' in name => directory not given, so use defaults
        infile     = "/opt/zeppelin/notebook/" + sys.argv[1] + "/note.json"
    else:
        infile     = sys.argv[1]

    outfile        = sys.argv[2]

    # Export Notebook
    if len(sys.argv) == 4:
        exportNotebook(infile, outfile, sys.argv[3])
    else:
        exportNotebook(infile, outfile)
