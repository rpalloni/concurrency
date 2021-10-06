# I/O-bound processes (user input)

from threading import Thread, current_thread

class InputReader(Thread):
    '''
    To construct a thread, we must extend the Thread class and implement the run method.
    Any code executed by the run method happens in a separate thread.
    '''

    def run(self):
        self.line_of_text = input()
        print(current_thread().name)


if __name__ == "__main__":
    print(current_thread().name)

    # (2) input
    print("Enter some text and press enter: ")
    thread = InputReader()
    thread.start()

    # (1) main
    number = result = 1
    while thread.is_alive():
        result = number * number
        number += 1
    

    print(f"calculated squares up to {number} * {number} = {result}")
    print(f"while you typed '{thread.line_of_text}'")
    

'''
These threads allows to (1) calculate squares while (2) getting input from keyboard.
Thread (2) doesn't start running until we call the start() method on the object.
It starts and immediately pauses to wait for input from the keyboard.
In the meantime, the original thread continues executing from the point start() was called.
It starts calculating squares inside a while loop. The condition in the while loop checks
whether the InputReader thread has exited its run method yet; once it does, it outputs
some summary information to the screen.
'''
