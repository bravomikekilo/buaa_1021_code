# -*- coding:utf-8 -*-
from misc import *
import Func, vis, config
from interpolation import interpolation as inter
import numpy as np


[Rs, xs] = config.Rp.T  # get the data
ys = np.asarray([get_result(i) for i in Rs])  # get the temperature
head, body, tail = section_data(np.vstack([ys, xs]).T)  # section data
head_line = Func.LinearFunc(head)  # find the head section function
tail_line = Func.LinearFunc(tail)  # find the tail section function
body_xs = body[:, 1]  # get the body section time vector
lowerbound = np.min(body_xs)  # get the lowerbound of the time of the body section
upperbound = np.max(body_xs)  # get the upperbound ....
print head_line.k  # print the k
print tail_line.k
func_set = Func.FuncSet()  # build a empty function set
# interpolation the body section data to get the cubic functions and copy them to func_set
func_set.from_matrix(inter(body, tail=tail_line.k), body_xs)
print func_set  # print the func_set
con = vis.Canvas()  # get a canvas
con.func_set(func_set)  # draw func_set on the canvas
con.function(head_line.vec(), lowerbound, upperbound, style='r-')  # draw the head_line in red
con.function(tail_line.vec(), lowerbound, upperbound, style='g-')  # draw the tail_line in green
con.show()  # show the canvas
# get the balanced through binary search algorithm
l = lowerbound  # set the lowerbound
r = upperbound  # set the upperbound
pivot = (l + r) / 2.  # get the middle point
e = config.error  # get the expected time error from config
it = 0  # init the iteration counter
while r - l > e:
    it += 1
    if it > 2000:
        print 'too many iter, break!'
        break
    # integrate
    left_area = head_line.integrate(lowerbound, pivot) - func_set.integrate(lowerbound, pivot)
    right_area = func_set.integrate(pivot, upperbound) - tail_line.integrate(pivot, upperbound)

    print 'left_area %f | right_area %f' % (left_area, right_area)
    if left_area > right_area:
        r = pivot
        pivot = (l + r) / 2.
        print pivot
    if left_area < right_area:
        l = pivot
        pivot = (l + r) / 2.
        print pivot

print pivot
# get the corrected temperature
print 'T2 is %f | T3 is %f' % (head_line(pivot), tail_line(pivot))
input('press any key to end')
