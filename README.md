# README
This is (will be) a tool to build a callgraph 
from a number of source files.
It relies heavily on other python libraries 
(`pycparser`, `ast`)
to do the heavy-lifting 
related to parsing the code.

We will start targeting C
(using `pycparser` to get the AST)
but keeping in mind that 
we would like also to deal with Python.


# Design
These are the steps.

1. Get the AST of every compilation unit.
   
   For C:
   1. Preprocess compilation unit.
      This requires setting up all necessary
      `-D`s, 
      include paths,
      and also clearing all the non-standard
      stuff (e.g. `__attribute__` for GCC).
      For the include paths, 
      remember to use the mock of `libc`
      that comes included in the `pycparser` repo.
      
      NOTE: preprocessing the files
      so that `pycparser` does not choke on them
      is usually the most tedious part.
   2. Run `pycparser` and get the AST.
   
   For Python:
   1. Read in memory 
      the content of the source file.
      Then parse it using 
      the facilities contained in the `ast` module
      of the standard library.


2. Exctract the 
   function definition/function call information 
   of every module/compilation unit.
   Notice that the name of the function is not enough
   to determine exactly the function, 
   also the name of the compilation unit is necessary
   (e.g., for the `main()` function). 
   
3. Simulate the linking phase.
   For C, one needs to specify 
   which files are linked together.
   For python:  TODO
   
   
# TODO and to understand
  It is not yet clear how to exactly do things for python.
   
   
   
