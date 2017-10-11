# Integrating prototype to production code

Please discard the python notebook file. To make it easier and more readible, I have migrated everything to prototype.py and I have added some helper classes and modules.

## Project Details
### Part 1-Unit testing and regression testing
Testing extensively the functionality of the prototype before and after merging with the production code! Test one small thing at a time!

Testing the results of the prototype code after and before merging with the prodution code; in this way the new results are compared with the previously stored results to check the consistency. Test the functionality of the entire module or pipeline at once.

### Part 2- Inputing and Outputting Structured JSON files
Reading and writting instructions and data between different parts of the production code as they are run in different environments and languages. Best practise is using general protocols which can move through different APIs such as JSON structured files. These can be the only points of entry to and exit from the prototype code.

### part 3- Embedding with C++:
If most of the production code is written in C/C++, python modules can be embedded within the production code!

### part 4- Separate the interface of the code from implementation:
Interface is:
	  opening/closing of files
	  Reading/Writting of Files

Implementation is:
	  modules and classes to do Math and Modification of data

### part 5- Adding RESTful APIs (Not Done)

