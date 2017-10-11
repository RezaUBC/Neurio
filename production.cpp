#include <python.h>

int main(int argc, char *argv[])
{
  //some other codes go here...
  // .
  // .
  // Starting with embedding the python module
  PyObject *pName, *pModule, *pDict, *pFunc;
  PyObject *pArgs, *pValue;

  if (argc < 3){
    fprintf(stderr,"usage: calling python filename [args]\n");
    return 1;
  }

  Py_Initialize();
  pName = PyString_FromString(argv[1]);

  pModule = PyImport_Import(pName);
  Py_DECREE(pName);

  if (pModule != NULL){
    pFunc = PyObject_GetAttrsting(pModule, argv[2]);

    if (pFunc && PyCallable_Check(pFunc)){
      pArgs = PyTuple_New(argc-3);
      for (i=0 ; i < argc-3 ; i++){
	pValue = PyInt_FromLong(atoi(argv[i+3]));
	if (!pValue) {
	  Py_DECREF(pArgs);
	  Py_DECREF(pModule);
	  fprintf(stderr,"Cannot convert argument\n");
	  return 1;
	}
	PyTuple_SetItem(pArgs, i, pValue);
      }
      pValue = PyObject_CallObject(pFunc, pArgs);
      PyDECREF(pArgs);
                  if (pValue != NULL) {
                printf("Result of call: %ld\n", PyInt_AsLong(pValue));
                Py_DECREF(pValue);
            }
            else {
                Py_DECREF(pFunc);
                Py_DECREF(pModule);
                PyErr_Print();
                fprintf(stderr,"Call failed\n");
                return 1;
            }
        }
        else {
            if (PyErr_Occurred())
                PyErr_Print();
            fprintf(stderr, "Cannot find function \"%s\"\n", argv[2]);
        }
        Py_XDECREF(pFunc);
        Py_DECREF(pModule);
    }
    else {
        PyErr_Print();
        fprintf(stderr, "Failed to load \"%s\"\n", argv[1]);
        return 1;
    }
    Py_Finalize();
    return 0;
}
