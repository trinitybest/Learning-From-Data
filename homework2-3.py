# -*- coding: utf-8 -*-
"""
Created on Sat Nov 12 00:05:14 2016

@author: TH

Q8
.
"""

import random
import numpy as np
import math

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
    
def estimate_eout(hypothesis_line, number_of_points):
    return len(find_misclassified_points(hypothesis_line, generate_points(number_of_points)))/ float(number_of_points)

def estimate_ein(hypothesis_line, training_points):
     return len(find_misclassified_points(hypothesis_line, training_points))/ float(len(training_points))
    
def find_class(line, point):
    return (1 if (line.w1 * point.x + line.w2 * point.y + line.w0 > 0) else -1)


    
def is_misclassified_point(hypothesis_line, point):
    return (find_class(hypothesis_line, point) != target_function(point))

def find_misclassified_points(hypothesis_line, points):
    return [point for point in points if is_misclassified_point(hypothesis_line, point)]
    
def aggregate_points_into_a_matrix(points):
    x = np.empty(shape=(len(points), 3))
    count = 0
    for point in points:
        x[count] = [1, point.x, point.y]
        count += 1
    return x

def pick_random_misclassified_point(hypothesis_line, target_line, points):
    return random.choice(find_misclassified_points(hypothesis_line, target_line, points))

def update_hypothesis(hypothesis_line, misclassified_point, target_line, learning_rate):
    sign = find_class(target_line, misclassified_point)
    #print sign
    hypothesis_line.w0 += learning_rate * sign
    hypothesis_line.w1 += learning_rate * (misclassified_point.x * sign)
    hypothesis_line.w2 += learning_rate * (misclassified_point.y * sign)    
    return hypothesis_line

def generate_target_vector0(line, points):
    return [find_class(line, point) for point in points]

def generate_target_vector(points):
    return [target_function(point) for point in points]  

def target_function(point):
    x1 = point.x
    x2 = point.y
    return (1 if ((math.pow(x1,2) + math.pow(x2, 2) -0.6)>0) else -1)
  
def run_linear_regression(training_points):
    x = aggregate_points_into_a_matrix(training_points)
    xdagger = np.dot(np.linalg.pinv(np.dot(np.transpose(x), x)), np.transpose(x))
    target_vector = generate_target_vector(training_points)
    w = np.dot(xdagger, target_vector)
    return Line(w[0], w[1], w[2])
    
def plot_linear_regression(points, target_labels, line):
    import matplotlib
    import matplotlib.pyplot as plt
    matplotlib.style.use('ggplot')
    x_list = []
    y_list = []
    color_list = []
    for point in points:
        x_list.append(point.x)
        y_list.append(point.y) 
    for label in target_labels:
        if label == 1:
            color_list.append('red')
        else:
            color_list.append('blue')
        
    slope = -(line.w1/line.w2)
    intercept = -(line.w0/line.w2)
    abline_values = [slope*i + intercept for i in x_list]
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_title('Linear Regression')
    ax.set_xlabel('x1')
    ax.set_ylabel('x2')        
    ax.scatter(x_list, y_list, c=color_list, marker='x', alpha = 0.75)
    ax.plot(x_list, abline_values)
    ax.legend()
    
    
def experiment():
    max_number_of_iterations = 10000
    number_of_runs = 1000
    number_of_training_points = 100 
    learning_rate = 1.0
    total_number_of_iterations = 0
    total_generalization_error = 0
    for run_number in range(number_of_runs):
        training_points = generate_points(number_of_training_points)
        target_labels = generate_target_vector(training_points)             
        hypothesis_line = run_linear_regression(training_points)
        print('-------------')
        print(hypothesis_line.w0, hypothesis_line.w1, hypothesis_line.w2)
        #plot_linear_regression(training_points, target_labels, hypothesis_line)
        hypothesis_line.print_object()
        ein = estimate_ein(hypothesis_line, training_points)
        print(ein)
        eout = estimate_eout(hypothesis_line, 1000)
        print(eout)
        yield [ein, eout]
       

def main():

    sum_x = 0
    sum_y = 0
    for x,y in experiment():
        sum_x += x
        sum_y += y
    print("average for ein" , sum_x/1000)
    print("average for eout", sum_y/1000)

if __name__ == "__main__":
    assert(intercept(1, 6, 3, 12) == 3.0)
    assert(intercept(6, 1, 1, 6) == 7.0)
    assert(intercept(4, 6, 12, 8) == 5.0)
    
    # Start program
    main()
























