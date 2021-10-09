# concurrency

Terminology for code reading

* CPU: piece of hardware executing code
* OS: handles the scheduling of CPU among processes
* Process: program executed
* Thread: part of a process; a separate flow of execution
* Daemon: a process that runs in the background
* I/O bound: network, database, user inputs ops
* CPU bound: task, jobs, calculation
* time.sleep() artificial delay for switching between threads

~~~
## Multithreading in a nutshell:

 1 Process => 1 Interpreter => 1 GIL 

 __ Process ___________________________________________________         
|  _________               I/O              I/O                |
| |         |     lock     | |              | |     lock       |
| | Thread1 | ==========>  | |              | | ==========>    |
| |_________|              | |              | |                |
|  _________               | |              | |                |
| |         |              | |     lock     | |                |
| | Thread2 |              | | ==========>  | |                |
| |_________|              | |              | |                |
|______________________________________________________________|

I/O: something outside the interpreter domain;  while waiting for these external events, \ 
the interpreter can switch and execute another thread. \
lock: when the interpreter switch to a thread, GIL locks the interpreter and memory for that thread.
Despite the execution is slower, threads setup is faster ("light" processes)


## Multiprocessing in a nutshell:

n Processes => n Interpreters => n GILs

 __ (Parent) Process ___________________________________________
|  __________                                                   |
| |          |       lock                                       |
| | Process1 | =====================================>           |
| |__________|                                                  |
|  __________                                                   |
| |          |       lock                                       |
| | Process2 | =====================================>           |
| |__________|                                                  |
|_______________________________________________________________|                          

Each process has its own interpreter, memory share and lock. 
Despite the execution is faster, processes setup (instance generation) is slower.

~~~

_The rigth tool for the job:_ \
threads are useless in Python for parallel processing (CPU bound) but optimal for I/O bound cases. \
Depending on what kind of concurrency is needed (tending toward I/O versus tending toward CPU) \
multithreading or multiprocessing should be adopted.
