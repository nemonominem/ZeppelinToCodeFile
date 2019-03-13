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
    - what          : python | scala | r | sql | sh
    - mdascomment   : whether to use md blocks as comments

    Examples:
    - python ./zep2code.py 2E27K8X9M python /tmp/test3.py   -> produces a .py file runable in interactive mode
    - python ./zep2code.py 2E27K8X9M r      /tmp/test3.r    -> produces a .r  file runable in interactive mode
    - python ./zep2code.py 2E27K8X9M all    /tmp/test3.all  -> produces a likely not runable file useful for checking code differences
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
    else:
        print("The target interpreter should be one of: python | scala | r | sql | sh")
        print("Do 'python zep2code.py' to get help\n")

        raise Exception("Unknown target interpreter")

    # Tell what you are doing
    if debug:
        print("Processing {} for {}".format(infile, what))
        print("Output: {} ".format(outfile))

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
## - python ./zep2code.py 2E27K8X9M python /tmp/test3.py   -> produces a .py file runable in interactive mode
## - python ./zep2code.py 2E27K8X9M r      /tmp/test3.r    -> produces a .r  file runable in interactive mode
## - python ./zep2code.py 2E27K8X9M all    /tmp/test3.all  -> produces a likely not runable file useful for checking code differences
############################################################################

if __name__ == '__main__':


    # Help
    if len(sys.argv) == 1:
        help(exportNotebook)
        import sys; sys.exit(0)

    # Check arguments
    if len(sys.argv) > 4:
        raise Exception("no more than 3 arguments: infile, outfile, list of interprenters")

    # File signature
    filesig = {'r': 'r', 'python': 'py', 'all': 'all'}

    # Get input / output
    if (sys.argv[1].find('/') == -1) and (sys.argv[1].find('json') == -1):

        # No '/' in name => directory not given, so use defaults location for JSON file given by key
        infile     = "/opt/zeppelin/notebook/" + sys.argv[1] + "/note.json"

        if len(sys.argv) == 4:
            # Output file provided
            outfile        = sys.argv[3]
        else:
            # No output file provided
            outfile        = "{}.{}".format(sys.argv[1], filesig[sys.argv[2]])
    else:
        # An explicit json file given
        infile     = sys.argv[1]

        if len(sys.argv) == 4:
            # Output file provided
            outfile        = sys.argv[3]
        else:
            # No output file provided
            if (sys.argv[1].find('/') == -1):
                # Input is without dir
                outfile        = "{}.{}".format(sys.argv[1][0:-5], filesig[sys.argv[2]])
            else:
                # Input is with dir
                k              = sys.argv[1].rfind('/')
                outfile        = "{}.{}".format(sys.argv[1][k:-5], filesig[sys.argv[2]])

    # Export Notebook
    exportNotebook(infile, outfile, sys.argv[2], debug=False)
