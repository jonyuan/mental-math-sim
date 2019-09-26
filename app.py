import numpy as np
import random
from threading import Thread, Event

# operators[0] are 'easy' operators, operators[1] are 'hard'
operators = [['+', '-'], ['*', '/']]

TIME = 240

# Event object used to send stop signals between threads
stop_event = Event()

# Event object used to send restart signal between threads
# restart_event = Event()

def save_run(filename, data):
    # function for saving performance data
    # data should be a tuple (problems, minutes, score)
    storage_string = ','.join([str(d) for d in list(data)])
    f = open(filename, "a+")
    f.write(storage_string + '\n')
    f.close()
    return

def simulate(problems = 40):
    points = 0
    incorrect = []
    for i in range(1, problems + 1):
        # Here we make the check if the other thread sent a signal to stop execution.
        if stop_event.is_set():
            # restart_event.set()
            break

        # we want to make addition and subtraction a little harder than * and /
        mode = random.randint(0, 1)
        operator = operators[mode][random.randint(0, 1)]
        if mode == 0:
            a = round(random.normalvariate(0,200), 2)
            b = round(random.normalvariate(0,200), 2)
            if operator == '+':
                actual_ans = a + b
            elif operator == '-':
                actual_ans = a - b  
            else:
                raise Exception('Unknown Operator ' + operator)
            actual_ans = round(actual_ans, 2)
        else:
            # when multiplying or dividing, come up with an integer solution first
            actual_ans = random.randint(-50, 50)
            a = random.randint(-50, 50)
            b = round(random.normalvariate(0, 100), 1)
            if operator == '*':
                actual_ans = a * b
                actual_ans = round(actual_ans, 2)
            else:
                a = b * actual_ans
                a = round(a, 2)
        question = str(a) + ' ' + operator + ' ' + str(b)
        formatted_question = str(i) + ') ' + question + ' = '
        ans = input(formatted_question)
        if ans == str(actual_ans):
            # print('good job dude')
            points += 1
            continue
        else:
            incorrect.append(formatted_question + str(actual_ans) + '. Your answer: ' + ans)
            points = max(points - 1, 0)
            continue
    print('\ntest complete. you scored ' + str(points) + ' out of ' + str(problems))
    print('Incorrect Answers:')
    [print(problem) for problem in incorrect]
    # save performance data
    save_data = (problems, TIME, points)
    save_run('log.csv', save_data)


def main():
    print('40 questions, 4 minutes...')
    alive = True
    # simulate(problems = 4)
    while alive:
        action_thread = Thread(target=simulate)
        action_thread.start()
        action_thread.join(timeout=TIME)
        if action_thread.is_alive():
            stop_event.set()
            action_thread.join()
            print('\nTime is up! ')
        restart = input('Press enter to try again, and any other key to exit\n')
        if restart != '':
            alive = False
        else:
            stop_event.clear()

main()

