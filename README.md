# concurrency

Terminology for code reading

* concurrency: simultaneous occurrence
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

I/O: something outside the interpreter domain;  while waiting for these external events,
the interpreter can switch and execute another thread.
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

In multithreading (multitasking), the way the threads take turn of execution (_appearing_ to run at the same time) \
allows differentiating further in pre-emptive multitasking and cooperative multitasking.
* Pre-emptive: OS knows and anticipate each thread interrupting/starting different threads at any time.
* Cooperative: Threads must cooperate by announcing when they are ready to be switched out.

~~~
      Concurrency Type       |   Number of CPU   |              Switching Decision                  |       Libs
_____________________________|___________________|__________________________________________________|___________________
                             |                   |                                                  |
    Pre-emptive multitasking |         1         |  OS decides when to switch tasks                 |  threading
    Cooperative multitasking |         1         |  Tasks decide when to give up control            |  asyncio
    Multiprocessing          |         N         |  N processes running at the same time on N CPUs  |  multiprocessing
~~~


In short:

~~~
if io_bound:
    if io_very_slow:
        print("Use Asyncio")
    else:
       print("Use Threads")
else:
    print("Use Multi Processing")
~~~

* CPU Bound => multiprocessing
* I/O Bound, Slow I/O, Many connections => asyncio
* I/O Bound, Fast I/O, Limited Number of Connections => threading


# asyncio

Specifically designed for server side network applications (spending a lot of time waiting for data to come in from the network). \
It handles each client as a separate thread and uses coroutines to lightweight the threads burden (in terms of memory and resources).

* coroutine: a function that can suspend its execution before reaching return, and can indirectly pass control to another coroutine for some time (use _async_ and _await_ syntax to return control to the event loop)
* event loop: takes care of checking whether calls have completed and performing any subsequent tasks
