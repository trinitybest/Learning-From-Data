# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 20:59:40 2016

@author:TH

Q9 and Q10
..
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
    w3 = 0.0
    w4 = 0.0
    w5 = 0.0
    
    def __init__(self, w0, w1, w2, w3, w4, w5):
        self.w0 = w0
        self.w1 = w1
        self.w2 = w2
        self.w3 = w3
        self.w4 = w4
        self.w5 = w5
    def print_object(self):
        print(self.w0, self.w1, self.w2, self.w3, self.w4, self.w5)
    
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
# Compare two hypothesis lines
def compare_lines(base_line, comparison_line, number_of_points):
    return len(find_misclassified_points_compare_lines(base_line, comparison_line, generate_points(number_of_points)))/ float(number_of_points)

# Find class for points after transformation  
def find_class(line, point):
    return (1 if (line.w0 + line.w1 * point.x + line.w2 * point.y +line.w3 * point.x * point.y + line.w4 * math.pow(point.x, 2) + line.w5 * math.pow(point.y, 2) > 0) else -1)
  
def is_misclassified_point(hypothesis_line, point):
    return (find_class(hypothesis_line, point) != target_function(point))
    
def is_misclassified_point_compare_lines(base_line, comparison_line, point):
    return (find_class(base_line, point) != find_class(comparison_line, point))

def find_misclassified_points(hypothesis_line, points):
    return [point for point in points if is_misclassified_point(hypothesis_line, point)]
    
def find_misclassified_points_compare_lines(base_line, comparison_line, points):
    return [point for point in points if is_misclassified_point_compare_lines(base_line, comparison_line, point)]
  
# Transform points and aggregate them into a matrix  
def aggregate_points_into_a_matrix(points):
    x = np.empty(shape=(len(points), 6))
    count = 0
    for point in points:
        x[count] = [1, point.x, point.y, point.x * point.y, math.pow(point.x, 2), math.pow(point.y, 2)]
        count += 1
    #print(x)
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
# Add a random noise for the function, it's not perfect, but it serves the purpose
def target_function(point):
    x1 = point.x
    x2 = point.y
    result = (1 if ((math.pow(x1,2) + math.pow(x2, 2) -0.6)>0) else -1)
    if random.randint(1,10) == 1:
        result = -result
    return result
  
def run_linear_regression(training_points):
    x = aggregate_points_into_a_matrix(training_points)
    xdagger = np.dot(np.linalg.pinv(np.dot(np.transpose(x), x)), np.transpose(x))
    target_vector = generate_target_vector(training_points)
    w = np.dot(xdagger, target_vector)
    return Line(w[0], w[1], w[2], w[3], w[4], w[5])
    
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
    number_of_runs = 100
    number_of_training_points = 1000 
    learning_rate = 1.0
    total_number_of_iterations = 0
    total_generalization_error = 0
    for run_number in range(number_of_runs):
        training_points = generate_points(number_of_training_points)
        target_labels = generate_target_vector(training_points)             
        hypothesis_line = run_linear_regression(training_points)
        print('-------------')        
        #print(hypothesis_line.w0, hypothesis_line.w1, hypothesis_line.w2)
        #plot_linear_regression(training_points, target_labels, hypothesis_line)
        hypothesis_line.print_object()
        ein = estimate_ein(hypothesis_line, training_points)
        print(ein)
        eout = estimate_eout(hypothesis_line, 1000)
        print(eout)
        comparison_line_1 = Line(-1, -0.05, 0.08, 0.13, 1.5, 1.5)
        comparison_line_2 = Line(-1, -0.05, 0.08, 0.13, 1.5, 15)
        comparison_line_3 = Line(-1, -0.05, 0.08, 0.13, 15, 1.5)
        comparison_line_4 = Line(-1, -1.5, 0.08, 0.13, 0.05, 0.05)
        comparison_line_5 = Line(-1, -0.05, 0.08, 1.5, 0.15, 0.15)
        cl1 = compare_lines(hypothesis_line, comparison_line_1, 1000)
        cl2 = compare_lines(hypothesis_line, comparison_line_2, 1000)
        cl3 = compare_lines(hypothesis_line, comparison_line_3, 1000)
        cl4 = compare_lines(hypothesis_line, comparison_line_4, 1000)
        cl5 = compare_lines(hypothesis_line, comparison_line_5, 1000)
        yield [ein, eout, cl1, cl2, cl3, cl4, cl5]
        
       

def main():

    sum_x = 0
    sum_y = 0
    sum_cl1 = 0
    sum_cl2 = 0
    sum_cl3 = 0
    sum_cl4 = 0
    sum_cl5 = 0
    for x,y, cl1, cl2, cl3, cl4, cl5 in experiment():
        sum_x += x
        sum_y += y
        sum_cl1 += cl1
        sum_cl2 += cl2
        sum_cl3 += cl3
        sum_cl4 += cl4
        sum_cl5 += cl5
    print("average for ein" , sum_x/1000)
    print("average for eout", sum_y/1000)
    print(sum_cl1/1000)
    print(sum_cl2/1000)
    print(sum_cl3/1000)
    print(sum_cl4/1000)
    print(sum_cl5/1000)
    """
    average for ein 0.012436999999999998
    average for eout 0.012581999999999998
    0.003808999999999997
    0.033731
    0.03388
    0.037145000000000004
    0.04415800000000001
    """


if __name__ == "__main__":
    assert(intercept(1, 6, 3, 12) == 3.0)
    assert(intercept(6, 1, 1, 6) == 7.0)
    assert(intercept(4, 6, 12, 8) == 5.0)
    
    # Start program
    main()