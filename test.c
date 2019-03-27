# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 10:54:22 2019

@author: Guddu
"""

#include<Python.h>
static PyObject *
spam_system(PyObject *self, PyObject *args)
{
    const char *command;
    int sts;

    if (!PyArg_ParseTuple(args, "s", &command))
        return NULL;
    sts = system(command);
    return PyLong_FromLong(sts);
}
