# -*- coding: utf-8 -*-
"""
Created on Sat Nov 12 00:05:14 2016

@author: TH

Q5
"""

import random
import numpy as np

class Point(object):
    x = 0.0
    y = 0.0
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def shuffle(self):
        self.x = random.uniform(-1.0, 1.0)
        self.y = random.uniform(-1.0, 1.0)
        return self
    def print_object(self):
        print(self.x, self.y)
        
class Line(object):
    w0 = 0.0
    w1 = 0.0
    w2 = 0.0
    
    def __init__(self, w0, w1, w2):
        self.w0 = w0
        self.w1 = w1
        self.w2 = w2
    def print_object(self):
        print(self.w0, self.w1, self.w2)
    
def slope (x1, y1, x2, y2):
    return float(y2-y1)/(x2-x1)
    
def intercept(x1, y1, x2, y2):
    return y2 - (slope(x1, y1, x2, y2)*x2)
    
def generate_random_line():
    x1, y1, x2, y2 = [random.uniform(-1.0, 1.0) for i in range(4)]
    return Line(-1*intercept(x1, y1, x2, y2), -1*slope(x1, y1, x2, y2), 1)
    
def generate_point():
    return Point(0.0, 0.0).shuffle()
    
def generate_points(number_of_points):
    return [generate_point() for i in range(number_of_points)]
    
def estimate_eout(hypothesis_line, target_line, number_of_points):
    return len(find_misclassified_points(hypothesis_line, target_line, generate_points(number_of_points)))/ float(number_of_points)

def estimate_ein(hypothesis_line, target_line, training_points):
     return len(find_misclassified_points(hypothesis_line, target_line, training_points))/ float(len(training_points))
    
def find_class(line, point):
    return (1 if (line.w1 * point.x + line.w2 * point.y + line.w0 > 0) else -1)

def generate_target_vector(line, points):
    return [find_class(line, point) for point in points]
    
def is_misclassified_point(hypothesis_line, target_line, point):
    return (find_class(hypothesis_line, point) != find_class(target_line, point))

def find_misclassified_points(hypothesis_line, target_line, points):
    return [point for point in points if is_misclassified_point(hypothesis_line, target_line, point)]
    
def aggregate_points_into_a_matrix(points):
    x = np.empty(shape=(len(points), 3))
    count = 0
    for point in points:
        x[count] = [1, point.x, point.y]
        count += 1
    return x
    
def run_linear_regression(training_points, target_line):
    x = aggregate_points_into_a_matrix(training_points)
    xdagger = np.dot(np.linalg.pinv(np.dot(np.transpose(x), x)), np.transpose(x))
    target_vector = generate_target_vector(target_line, training_points) # target_vector, aka y
    w = np.dot(xdagger, target_vector)
    return Line(w[0], w[1], w[2])

def pick_random_misclassified_point(hypothesis_line, target_line, points):
    return random.choice(find_misclassified_points(hypothesis_line, target_line, points))

def update_hypothesis(hypothesis_line, misclassified_point, target_line, learning_rate):
    sign = find_class(target_line, misclassified_point)
    #print sign
    hypothesis_line.w0 += learning_rate * sign
    hypothesis_line.w1 += learning_rate * (misclassified_point.x * sign)
    hypothesis_line.w2 += learning_rate * (misclassified_point.y * sign)    
    return hypothesis_line
    
def run_pla(target_line, hypothesis_line, training_points, max_number_of_iterations, learning_rate):
    number_of_iterations = 0
    for i in range(max_number_of_iterations):
        #print "iteration"
        number_of_iterations += 1       
        #hypothesis_line.print_object() 
        if len(find_misclassified_points(hypothesis_line, target_line, training_points)) == 0: break
        #print len(find_misclassified_points(hypothesis_line, target_line, training_points))
        misclassified_point = pick_random_misclassified_point(hypothesis_line, target_line, training_points)
        #misclassified_point.print_object()
        hypothesis_line = update_hypothesis(hypothesis_line, misclassified_point, target_line, learning_rate)
    return hypothesis_line, number_of_iterations
# A nice function to visualise the points and the line
def plot_linear_regression(points, target_labels, line):
    import matplotlib
    import matplotlib.pyplot as plt
    matplotlib.style.use('ggplot')
    x_list = []
    y_list = []

    for point in points:
        x_list.append(point.x)
        y_list.append(point.y) 
        
    slope = -(line.w1/line.w2)
    intercept = -(line.w0/line.w2)
    abline_values = [slope*i + intercept for i in x_list]
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_title('Linear Regression')
    ax.set_xlabel('x1')
    ax.set_ylabel('x2')        
    ax.scatter(x_list, y_list, c=target_labels, marker='x', alpha = 0.75)
    ax.plot(x_list, abline_values)
    

    
    
        
    
def experiment():
    max_number_of_iterations = 10000
    number_of_runs = 1000
    number_of_training_points = 100 # or 1000 for Q7
    learning_rate = 1.0
    total_number_of_iterations = 0
    total_generalization_error = 0
    for run_number in range(number_of_runs):
        target_line = generate_random_line()
        training_points = generate_points(number_of_training_points)
        target_line.print_object()
        hypothesis_line = run_linear_regression(training_points, target_line)
        hypothesis_line.print_object()
        target_vector = generate_target_vector(target_line, training_points)
        print('Here comes the plot.')
        #plot_linear_regression(training_points, target_vector, hypothesis_line)
        ein = estimate_ein(hypothesis_line, target_line, training_points)
        print(ein)
        eout = estimate_eout(hypothesis_line, target_line, 1000)
        print(eout)
        yield [ein, eout]
        
def experiment_Q7():
    max_number_of_iterations = 10000
    number_of_runs = 100
    number_of_training_points = 10
    learning_rate = 1.0
    total_number_of_iterations = 0
    total_generalization_error = 0

    target_line = generate_random_line()
    training_points = generate_points(number_of_training_points)
    target_line.print_object()
    hypothesis_line = run_linear_regression(training_points, target_line)
    hypothesis_line.print_object()
    ein = estimate_ein(hypothesis_line, target_line, training_points)
    print(ein)
    eout = estimate_eout(hypothesis_line, target_line, 1000)
    print(eout)      
    number_of_iterations = 0
    
    for run_number in range(number_of_runs):    
        hypothesis_line, number_of_iterations = run_pla(target_line, hypothesis_line, training_points, max_number_of_iterations, learning_rate)
        total_number_of_iterations += number_of_iterations
        #total_generalization_error += estimate_disagreement(hypothesis_line, target_line, 10000)
        #hypothesis_line.print_object()
    average_number_of_iterations = total_number_of_iterations / float(number_of_runs)
    average_generalization_error = total_generalization_error / float(number_of_runs)
    print('average_number_of_iterations: ', average_number_of_iterations)
    #print('average_generalization_error: ', average_generalization_error)

def main():
    
    sum_x = 0
    sum_y = 0
    for x,y in experiment():
        sum_x += x
        sum_y += y
    print("average for ein" , sum_x/1000)
    print("average for eout", sum_y/1000)
    
    experiment()
    experiment_Q7()
if __name__ == "__main__":
    assert(intercept(1, 6, 3, 12) == 3.0)
    assert(intercept(6, 1, 1, 6) == 7.0)
    assert(intercept(4, 6, 12, 8) == 5.0)
    
    # Start program
    main()
























