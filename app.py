import numpy as np
import random

operators = [['+', '-'], ['*', '/']]

for i in range(80):
	# we want to make addition and subtraction a little harder than * and /
	mode = random.randint(0, 1)
	operator = operators[mode][random.randint(0, 1)]
	if mode == 0:
		a = round(random.uniform(-100,100), 2)
		b = round(random.uniform(-100,100), 2)
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
		a = round(random.uniform(-100, 100), random.randint(1, 2))
		if operator == '*':
			b = actual_ans / a
		else:
			b = a / actual_ans
		b = round(b, 2)
	question = str(a) + ' ' + operator + ' ' + str(b)
	ans = input(str(i + 1) + ') ' + question + ': ')
	if abs(float(ans) - actual_ans) < 0.001:
		print('good job dude')
	print(actual_ans)
print('test complete')

