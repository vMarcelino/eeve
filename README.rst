eeve
====

.. image:: https://img.shields.io/pypi/v/eeve.svg
    :target: https://pypi.python.org/pypi/eeve
    :alt: Latest PyPI version

.. image::  https://travis-ci.org/vMarcelino/eeve.svg?branch=master
   :target:  https://travis-ci.org/vMarcelino/eeve
   :alt: Latest Travis CI build status

A simple, flexible and powerfull event trigger

Usage
-----
:code:`python -m eeve`

Or from the project folder:

:code:`python run.py`

Default GUI Usage
-----------------
The program flow is split in 3 main components:
Actions, triggers and events. 

**Actions** are the execution, they can vary from opening an app to 
sending a keystroke to the OS. They are *what* happens. 

**Triggers** make events happen. They usually run in background 
and activate events. They are *when* it happens. 

**Events** are the glue between triggers and actions. 
It can contain many triggers and many actions. When
an event is activated, it runs its actions in sequence. 
You can add many triggers to an event and every time one of the
added triggers fires, the event is activated and will run all its actions in order. 


Actions and triggers can also accept arguments, which documentation 
can be accessed using the (?) button on the editing page. The 
documentation is up to the trigger or action's developer to write.
However, eeve also shows what arguments the action or trigger accepts
by analyzing the code. 

**Variables** can also be used in actions. They can be from one of the three types:
*local variables*, that live while the event is running and are deleted as soon as the
last action is run. They can be accessed only by the actions inside that single run.
You can access them in a argument by a single $. 
Eg: $count

*event variables* (AKA task variables), that are accessible from any action from the event and are deleted when
eeve stops running or the event is deleted. You can access them by using two $
Eg: $$count

*global variables*, that are accessible by any action running, regardless of the 
event. They are deleted when eeve stops running. You can access them by using three $
Eg: $$$count


Installation
------------
From pip:

:code:`pip install -U eeve`

From source:

:code:`pip install -e .` or :code:`python setup.py install`

Requirements
^^^^^^^^^^^^

Compatibility
-------------

Only tested on windows x64, but should work on any other OS just fine. Actions and triggers, however, have their own compatibility


Licence
-------
MIT Licence

Authors
-------

`eeve` was written by `Victor Marcelino <victor.fmarcelino@gmail.com>`_.
