# -*- coding: utf-8 -*-
"""
Created on Fri Feb 01 11:11:46 2019

@author: DonB
"""

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from __future__ import division
import math
import matplotlib.pyplot as plt

class Section:
    
    def __init__(self, x, y, solid=True, n=1):
        '''
        A section defined by (x,y) vertices
        
        the vertices should for a closed polygon. 
        initialization will check is first and last coordinate are equal
        and if not will add an additional vertex equal to the first
        
        Inputs:
        
        x = a list of x coordinate values 
        y = a list of y coordinate values
        
        Assumptions:
        
        x and y are of consistent units
        x and y form a closed polygon with no segment overlaps
        
        If solid = 1 then the coordinates will be ordered so the signed area
        is positive
        
        n = property multiplier
        '''
        
        # check if a closed polygon is formed from the coordinates
        # if not add another x and y coordinate equal to the firts 
        # coordinate x and y
        
        self.warnings = ''
        if x[0] == x[-1] and y[0] == y[-1]:
            pass
        else:
            x.append(x[0])
            y.append(y[0])
            
            self.warnings = self.warnings + '**User Verify** Shape was not closed, program attempted to close it.\p'
        
        # check the signed area of the coordinates, should be positive
        # for a solid shape. If not reverse the coordinate order
        
        self.area = sum([(x[i]*y[i+1])-(x[i+1]*y[i]) for i in range(len(x[:-1]))])/2.0
        self.area = self.area*n
        
        if self.area < 0 and solid == True:
            x.reverse()
            y.reverse()
            self.warnings = self.warnings + '**User Verify** Coordinate order reversed to make signed area positive for a solid.\n'
            
            self.area = sum([(x[i]*y[i+1])-(x[i+1]*y[i]) for i in range(len(x[:-1]))])/2.0
            self.area = self.area*n
            
        elif self.area > 0 and solid == False:
            x.reverse()
            y.reverse()
            self.warnings = self.warnings + '**User Verify** Coordinate order reversed to make signed area negative for a void.\n'
            
            self.area = sum([(x[i]*y[i+1])-(x[i+1]*y[i]) for i in range(len(x[:-1]))])/2.0
            self.area = self.area*n
            
        elif self.area == 0:
            self.warnings = self.warnings + '**User Verify** Area = 0 - verify defined shape has no overlapping segments.\n'
            
        else:
            pass
        
        self.x = [i for i in x]
        self.y = [j for j in y]
        self.n = n
        
        if self.area == 0:
            pass
        else:
            self.calc_props()
            
    def calc_props(self):
            x = self.x
            y = self.y
            n = self.n
            
            self.output = []
            self.output_strings = []
            
            self.area = sum([(x[i]*y[i+1])-(x[i+1]*y[i]) for i in range(len(x[:-1]))])/2.0
            self.area = self.area*n
            
            self.output.append(self.area)
            self.output_strings.append('Area')

            # properties about the global x and y axis
            
            self.cx = sum([(x[i]+x[i+1])*((x[i]*y[i+1])-(x[i+1]*y[i])) for i in range(len(x[:-1]))])/(6*self.area)
            self.cx = self.cx*n
            self.output.append(self.cx)
            self.output_strings.append('Cx')
            self.cy = sum([(y[i]+y[i+1])*((x[i]*y[i+1])-(x[i+1]*y[i])) for i in range(len(x[:-1]))])/(6*self.area)
            self.cy = self.cy*n
            self.output.append(self.cy)
            self.output_strings.append('Cy')
            
            self.Ix = sum([((y[i]*y[i])+(y[i]*y[i+1])+(y[i+1]*y[i+1]))*((x[i]*y[i+1])-(x[i+1]*y[i])) for i in range(len(x[:-1]))])/(12.0)
            self.Ix = self.Ix*n
            self.output.append(self.Ix)
            self.output_strings.append('Ix')
            self.Iy = sum([((x[i]*x[i])+(x[i]*x[i+1])+(x[i+1]*x[i+1]))*((x[i]*y[i+1])-(x[i+1]*y[i])) for i in range(len(x[:-1]))])/(12.0)
            self.Iy = self.Iy*n
            self.output.append(self.Iy)
            self.output_strings.append('Iy')
            self.Ixy = sum([((x[i]*y[i+1])+(2*x[i]*y[i])+(2*x[i+1]*y[i+1])+(x[i+1]*y[i]))*(x[i]*y[i+1]-x[i+1]*y[i]) for i in range(len(x[:-1]))])/(24.0)
            self.Ixy = self.Ixy*n
            self.output.append(self.Ixy)
            self.output_strings.append('Ixy')
            self.Jz = self.Ix + self.Iy
            self.output.append(self.Jz)
            self.output_strings.append('Jz')
            self.sx_top = self.Ix / abs(max(y) - self.cy)
            self.output.append(self.sx_top)
            self.output_strings.append('Sx,top')
            self.sx_bottom = self.Ix / abs(min(y) - self.cy)
            self.output.append(self.sx_bottom)
            self.output_strings.append('Sx,botom')
            self.sy_right = self.Iy / abs(max(x) - self.cx)
            self.output.append(self.sy_right)
            self.output_strings.append('Sy,right')
            self.sy_left = self.Iy / abs(min(x) - self.cx)
            self.output.append(self.sy_left)
            self.output_strings.append('Sy,left')
            
            self.rx = math.sqrt(self.Ix/self.area)
            self.output.append(self.rx)
            self.output_strings.append('rx')
            self.ry = math.sqrt(self.Iy/self.area)
            self.output.append(self.ry)
            self.output_strings.append('ry')
            self.rz = math.sqrt(self.Jz/self.area)
            self.output.append(self.rz)
            self.output_strings.append('rz')
            
            # properties about the cross section centroidal x and y axis
            # parallel axis theorem Ix = Ixx + A*d^2
            # therefore to go from the global axis to the local
            # Ixx = Ix - A*d^2
            
            self.Ixx = self.Ix - (self.area*self.cy*self.cy)
            self.output.append(self.Ixx)
            self.output_strings.append('Ixx')
            self.Iyy = self.Iy - (self.area*self.cx*self.cx)
            self.output.append(self.Iyy)
            self.output_strings.append('Iyy')
            self.Ixxyy = self.Ixy - (self.area*self.cx*self.cy)
            self.output.append(self.Ixxyy)
            self.output_strings.append('Ixxyy')
            self.Jzz = self.Ixx + self.Iyy
            self.output.append(self.Jzz)
            self.output_strings.append('Jzz')
            self.sxx_top = self.Ixx / abs(max(y) - self.cy)
            self.output.append(self.sxx_top)
            self.output_strings.append('Sxx,top')
            self.sxx_bottom = self.Ixx / abs(min(y) - self.cy)
            self.output.append(self.sxx_bottom)
            self.output_strings.append('Sxx,bottom')
            self.syy_right = self.Iyy / abs(max(x) - self.cx)
            self.output.append(self.syy_right)
            self.output_strings.append('Syy,right')
            self.syy_left = self.Iyy / abs(min(x) - self.cx)
            self.output.append(self.syy_left)
            self.output_strings.append('Syy,left')
            
            self.rxx = math.sqrt(self.Ixx/self.area)
            self.output.append(self.rxx)
            self.output_strings.append('rxx')
            self.ryy = math.sqrt(self.Iyy/self.area)
            self.output.append(self.ryy)
            self.output_strings.append('ryy')
            self.rzz = math.sqrt(self.Jzz/self.area)
            self.output.append(self.rzz)
            self.output_strings.append('rzz')
            
            # Cross section principle Axis
            
            two_theta = math.atan((-1.0*2.0*self.Ixxyy)/(1E-16+(self.Ixx - self.Iyy)))
            temp = (self.Ixx+self.Iyy)/2.0
            temp2 = (self.Ixx-self.Iyy)/2.0
            I1 = temp + math.sqrt((temp2*temp2)+(self.Ixxyy*self.Ixxyy))
            I2 = temp - math.sqrt((temp2*temp2)+(self.Ixxyy*self.Ixxyy))
            
            self.Iuu = temp + temp2*math.cos(two_theta) - self.Ixxyy*math.sin(two_theta)
            self.output.append(self.Iuu)
            self.output_strings.append('Iuu')
            self.Ivv = temp - temp2*math.cos(two_theta) + self.Ixxyy*math.sin(two_theta)
            self.output.append(self.Ivv)
            self.output_strings.append('Ivv')
            self.Iuuvv = temp2*math.sin(two_theta) + self.Ixxyy*math.cos(two_theta)
            self.output.append(self.Iuuvv)
            self.output_strings.append('Iuuvv')
            
            if I1-0.000001 <= self.Iuu <= I1+0.000001:
                self.theta1 = math.degrees(two_theta/2.0)
                self.theta2 = self.theta1 + 90.0
            elif I2-0.000001 <= self.Iuu <= I2+0.000001:
                self.theta2 = math.degrees(two_theta/2.0)
                self.theta1 = self.theta2 - 90.0
            
            self.output.append(self.theta1)
            self.output_strings.append('Theta1,u')
            self.output.append(self.theta2)
            self.output_strings.append('Theta2,v')
                
    def parallel_axis_theorem(self, x, y):
        '''
        given a new global x,y coordinate for a new
        set of x, y axis return the associated Ix, Iy, and Ixy
        '''
        if self.area == 0:
            return [0,0,0]
        else:
            dx = self.cx - x
            dy = self.cy - y
            
            Ix = self.Ixx + (self.area*dy*dy)
            Iy = self.Iyy + (self.area*dx*dx)
            Ixy = self.Ixxyy + (self.area*dx*dy)
            
            return [Ix,Iy,Ixy]
    
    def transformed_vertices(self, xo, yo, angle):
        '''
        given an angle in degrees
        and coordinate to translate about
        return the transformed values of the shape vertices       
        '''
        theta = math.radians(angle)
        
        x_t = [(x-xo)*math.cos(theta)+(y-yo)*math.sin(theta) for x,y in zip(self.x, self.y)]
        y_t = [-1.0*(x-xo)*math.sin(theta)+(y-yo)*math.cos(theta) for x,y in zip(self.x, self.y)]
        
        x_t = [i+xo for i in x_t]
        y_t = [j+yo for j in y_t]
        
        self.x = x_t
        self.y = y_t
        
        self.calc_props()
        
        return [x_t, y_t]
    
    def translate_vertices(self, xo, yo):
        '''
        give an x and y translation
        shift the shape vertices by the x and y amount
        '''
        x_t = [x+xo for x in self.x]
        y_t = [y+yo for y in self.y]
        
        self.x = x_t
        self.y = y_t
        
        self.calc_props()
        
        return [x_t, y_t]
        
    def transformed_properties(self, x, y, angle):
        '''
        given a new global x,y coordinate for a new
        set of x, y axis and the axis angle. Return full set of transformed properties
        at the new axis
        
        input angle as degrees
        '''
        if self.area == 0:
            return [0,0,0,0,0,0,0]
        
        else:
            Ix, Iy, Ixy = self.parallel_axis_theorem(x,y)
            
            two_theta = 2*math.radians(angle)
            # I on principle Axis
            
            temp = (Ix+Iy)/2.0
            temp2 = (Ix-Iy)/2.0
            
            Iu = temp + temp2*math.cos(two_theta) - Ixy*math.sin(two_theta)
            Iv = temp - temp2*math.cos(two_theta) + Ixy*math.sin(two_theta)
            Iuv = temp2*math.sin(two_theta) + Ixy*math.cos(two_theta)
    
            Jw = Iu + Iv
            
            ru = math.sqrt(Iu/self.area)
            rv = math.sqrt(Iv/self.area)
            rw = math.sqrt(Jw/self.area)
            
            trans_coords = self.transformed_vertices(angle)
            
            return [Iu,Iv,Iuv,Jw,ru,rv,rw,trans_coords]
        

def composite_shape_properties(sections):
    '''
    give a list of sections defined using the Sections class above
    return the composite section properties
    
    Limitation: any specified voids must be entirely enclosed inside solid sections
    
    given a list of modifiers n
    '''
       
    # determine the global centroid location and total composite area
    # cx = sum A*dx / sum A
    # cy = sum A*dy / sum A
    # dx = section cx
    # dy = section cy
    # A = section area
    
    output = []
    output_strings = []    
    
    area = sum([section.area for section in sections])
    
    output.append(area)
    output_strings.append('Area')
    
    sum_A_dx = sum([section.area*section.cx for section in sections])
    sum_A_dy = sum([section.area*section.cy for section in sections])
    
    cx = sum_A_dx / area
    
    output.append(cx)
    output_strings.append('cx')
    
    cy = sum_A_dy / area
    
    output.append(cy)
    output_strings.append('cy')
    
    # determine moment of inertias about the centroid coordinates
    
    Ix = sum([section.parallel_axis_theorem(cx,cy)[0] for section in sections])

    output.append(Ix)
    output_strings.append('Ix')
    
    Iy = sum([section.parallel_axis_theorem(cx,cy)[1] for section in sections])

    output.append(Iy)
    output_strings.append('Iy')
    
    Ixy = sum([section.parallel_axis_theorem(cx,cy)[2] for section in sections])

    output.append(Ixy)
    output_strings.append('Ixy')
    
    Jz = Ix + Iy
    
    output.append(Jz)
    output_strings.append('Jz')
    
    # radii of gyration - centroidal axis
    rx = math.sqrt(Ix/area)
    output.append(rx)
    output_strings.append('rx')
    ry = math.sqrt(Iy/area)
    output.append(ry)
    output_strings.append('ry')
    rz = math.sqrt(Jz/area)
    output.append(rz)
    output_strings.append('rz')
    
    # composite section principle Axis
    
    two_theta = math.atan((-1.0*2.0*Ixy)/(1E-16+(Ix - Iy)))
    temp = (Ix+Iy)/2.0
    temp2 = (Ix-Iy)/2.0
    I1 = temp + math.sqrt((temp2*temp2)+(Ixy*Ixy))
    I2 = temp - math.sqrt((temp2*temp2)+(Ixy*Ixy))
    
    Iu = temp + temp2*math.cos(two_theta) - Ixy*math.sin(two_theta)
    output.append(Iu)
    output_strings.append('Iu')
    Iv = temp - temp2*math.cos(two_theta) + Ixy*math.sin(two_theta)
    output.append(Iv)
    output_strings.append('Iv')
    Iuv = temp2*math.sin(two_theta) + Ixy*math.cos(two_theta)
    output.append(Iuv)
    output_strings.append('Iuv')
    
    if I1-0.000001 <= Iu <= I1+0.000001:
        theta1 = math.degrees(two_theta/2.0)
        theta2 = theta1 + 90.0
    elif I2-0.000001 <= Iu <= I2+0.000001:
        theta2 = math.degrees(two_theta/2.0)
        theta1 = theta2 - 90.0
    
    output.append(theta1)
    output_strings.append('theta,u')
    output.append(theta2)
    output_strings.append('theta,v')
    
    Jw = Iu + Iv
    output.append(Jw)
    output_strings.append('Jw')
    
    ru = math.sqrt(Iu/area)
    output.append(ru)
    output_strings.append('ru')
    rv = math.sqrt(Iv/area)
    output.append(rv)
    output_strings.append('rv')
    rw = math.sqrt(Jw/area)
    output.append(rw)
    output_strings.append('rw')
    
    return output, output_strings

def circle_coordinates(x,y,r,start,end):
    '''
    given a center point x,y
    and a radius
    return the x,y coordinate list for a circle
    '''
    
    x_out = []
    y_out = []
    
    for a in range(start,end+1):
        x0 = r*math.cos(math.radians(a))
        y0 = r*math.sin(math.radians(a))
        
        x_out.append(x0+x)
        y_out.append(y0+y)
    
    return [x_out,y_out]

def line_x_at_y(x1,y1,x2,y2,at_y):
    '''
    given two points and a y coordinate
    return the corresponding x coordinate
    '''
    if x2 == x1:
        x_out = x1
    
    else:
        m = (y2-y1) / (x2-x1)
        
        # y = mx + b
        # b = y - mx
        b = y1 - (m*x1)
        
        # y = mx+b
        # x = y-b / m
        if m == 0:
            x_out = 0
        else:
            x_out = (at_y - b) / m
    
    return x_out

def dist_btwn_point_and_plane(point, xy, plane='H'):
    '''
    given a point as a list = [x,y]
    a plane elevation/location
    a plane orientation
    H = horizontal
    V = vertical
    
    return if the the point is in front, behind, or on
    the plane
    '''
    
    # General tolerance
    tol = 1E-16
    if plane=='H':
        dist = point[1] - xy
        
        if dist > tol:
            return 'over'
        elif dist < tol:
            return 'under'
        else:
            return 'on'
    
    elif plane == 'V':
        dist = point[0] - xy
        
        if dist > tol:
            return 'left'
        elif dist < tol:
            return 'right'
        else:
            return 'on'    

def split_shape_above_horizontal_line(shape, line_y, solid=True, n=1):
    
    '''
    given a shape and horizontal line y value
    return all the sub shapes above the line
    
    assumption:
        shape has been translated so its centroid is at 0,0
        shape has been rotated to align with the horizontal
    '''
    # new shapes above
    sub_shapes = []
        
    xy = [[x,y] for x,y in zip(shape.x,shape.y)]
    
    list_above = []
    list_below = []
    
    i=0
    for point in xy:
        if i == len(xy)-1:
            pass
        else:
            p1 = point
            p2 = xy[i+1]
            
            p1_test = dist_btwn_point_and_plane(p1, line_y,'H')
            p2_test = dist_btwn_point_and_plane(p2, line_y,'H')
            
            if p1_test=='over' and p2_test=='over':
                list_above.append(p2)
            
            elif p1_test=='on' and p2_test=='over':
                list_above.append(p2)
                
            elif p1_test=='under' and p2_test=='over':
                x_int = line_x_at_y(p1[0],p1[1],p2[0],p2[1],line_y)
                list_above.append([x_int,line_y])
                list_above.append(p2)
                list_below.append(p1)
                list_below.append([x_int,line_y])
                
            elif p1_test=='over' and p2_test=='on':
                list_above.append(p2)
            
            elif p1_test=='on' and p2_test=='on':
                list_above.append(p2)
                
            elif p1_test=='under' and p2_test=='on':
                list_above.append(p2)
                list_below.append(p2)
            
            elif p1_test=='over' and p2_test=='under':
                x_int = line_x_at_y(p1[0],p1[1],p2[0],p2[1],line_y)
                list_above.append([x_int,line_y])
                list_below.append([x_int,line_y])
                list_below.append(p2)
            
            elif p1_test=='on' and p2_test=='under':
                list_below.append(p1)
                list_below.append(p2)
            
            elif p1_test=='uder' and p2_test=='under':
                list_below.append(p2)
        i+=1
        
    xover = [p[0] for p in list_above]
    yover = [p[1] for p in list_above]
    
    xunder = [p[0] for p in list_below]
    yunder = [p[1] for p in list_below]
    
    plt.plot(xover,yover,'co')
    #plt.plot(xunder, yunder,'ko')
     
    #print list_above

    int_count = 0
    xsub = []
    ysub = []
    xsub2 = []
    ysub2 = []
    if len(list_above) >=3:
        if list_above[0][1] == list_above[1][1] and list_above[0][1]==line_y:
            
            xsub = [p[0] for p in list_above]
            ysub = [p[1] for p in list_above]
            sub = Section(xsub,ysub,solid,n)
            sub_shapes.append(sub)
        else:
            xsub = []
            ysub = []
            xsub2 = []
            ysub2 = []
            i=0
            for point in list_above:
                print int_count
                if list_above[0][1]!=line_y and int_count<1:
                    xsub2.append(point[0])
                    ysub2.append(point[1])
                
                else:
                    if int_count > 2:
                        xsub2.append(point[0])
                        ysub2.append(point[1])
                    else:
                        xsub.append(point[0])
                        ysub.append(point[1])

                
                if point != list_above[-1]:
                    next_point = list_above[i+1]
                    next_point_check = next_point[1] == line_y and point[1] == line_y and next_point[0]> point[0]
                    
                else:
                    next_point_check = False
                
                if point[1] == line_y:
                    int_count +=1
                
                
                if int_count == 2 and len(xsub)>2 and list_above[0][1]==line_y and next_point_check==False:
                    sub = Section(xsub,ysub,solid,n)
                    int_count = 0
                    xsub = []
                    ysub = []
                    
                    sub_shapes.append(sub)
                
                elif point == list_above[-1] and len(xsub)>2:  
                    sub = Section(xsub,ysub,solid,n)
                    int_count = 0
                    xsub = []
                    ysub = []
                    
                    sub_shapes.append(sub)
                
                i+=1
                
    if len(xsub2)>2:
        print xsub2, ysub2
        sub = Section(xsub2,ysub2,solid,n)
        int_count = 0
        xsub = []
        ysub = []
        
        sub_shapes.append(sub)      
                    
    return sub_shapes       
       
        
# zig zag    
x1 = [0,30,30,25,20,15,10,5,0,0]
y1 = [0,0,10,20,10,20,10,20,10,0]

# L
#x1 = [0,120,120,12,12,0,0]
#y1 = [0,0,12,12,120,120,0]

# C
#x1 = [0,120,120,12,12,120,120,0,0]
#y1 = [0,0,12,12,108,108,120,120,0]

#U 
#x1 = [0,30,30,20,20,10,10,0,0]
#y1 = [0,0,30,30,10,10,20,20,0]
shape1 = Section(x1,y1)
#shape2 = Section(x2,y2, False, 1)

shape1.transformed_vertices(shape1.cx,shape1.cy,-130)
#shape2.transformed_vertices(shape1.cx,shape1.cy,45)

#shape1.translate_vertices(0,120)
#shape2.translate_vertices(10,0)

line_y = 5

cut1 = split_shape_above_horizontal_line(shape1, line_y)
#cut2 = split_shape_above_horizontal_line(shape2, line_y, False, 1)

plt.plot(shape1.x,shape1.y,'r-')
#plt.plot(shape2.x,shape2.y,'b-')

plt.axhline(y=line_y, color='g', linestyle='--')

for c1 in cut1:
    plt.plot(c1.x,c1.y,'c+-')

#for c2 in cut2:
#    plt.plot(c2.x,c2.y,'k-')

plt.show()