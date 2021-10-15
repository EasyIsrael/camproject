Quick Start
===========

Projection
----------

this library has two main methods::

    project()
    reproject()
 
to use this library you need just a few lines of code.
This projects the Point P(1,0,10) on to the camera image plane. We call the projected point p(u,v) ::

    >>>import numpy as np
    >>>import camproject
    
    >>>P = np.array([1,0,10,1])   
    >>>cam = camproject.Camera()
    >>>cam.intrinsics(640,512,1000,320,260)
    >>>cam.attitudeMat(np.eye(4))
    >>>p = cam.project(P)
    >>>print(p)
        [420 260]
        
With cam.intrinsics you define the most important inner parameters of the camera. so 640 and 512 means that the image plane has a width of 640 and a height of 512 pixels. The third parameter describes the focal distance :math:`f_{px}` in pixels. 

.. math::
    f_{px} = \frac{f_{mm}}{s} , \qquad  s = \frac{w_{mm}}{w_{px}}
   
where  :math:`w_{mm}` is the camera sensor width in mm, :math:`w_{px}` is the image width in pixels and :math:`s` is the image detector element size.
The last two parameters describe the center pixels [cx cy] where the optical axis hits the image plane.
    
Until now we don't have rotated or moved the camera somewhere, so with cam.attitudeMat(np.eye(4)) it is positioned at the coordinates origin and the lens points to the positive z-axis. Later you will see how to change the camera orientation.

Our point P is directly centered in front of the camera with a distance of 10 units (for example meters).
The point p will be projected exactly to the optical center pixels. In our example this is [320 260]. 

Reprojection
------------

To reproject the point back to the 3D world we use this code ::    

    >>>Q = cam.reprojectToPlane(p) 
    >>>print(Q)
        [-0. -0. -0.  1.]
        
The default plane is the xy-plane (z=0). that makes not much sense when the camera itself also is at these coordinates. Thats why we get [0 0 0 1]. So if we want to reproject the point to its real origin, we need a little more information, for example the z-coordinate of the point. So we could define a plane with z=10. For our plane parameter we need to write this: [0,0,1,-10]. The first three elements define the normal vector of the plane and the last element the negative distance.
Then our reprojection code is ::

    >>>plane = np.array([0,0,1,-10])
    >>>Q = cam.reprojectToPlane(p,plane) 
    >>>print(Q)
        [ 1. -0. 10.  1.]
     
Multiple points
---------------

You can also project or reproject multiple points. ::

    >>>PM = np.array([[2,0,10],[1,0,10],[0,0,10],[-1,0,10]])
    >>>pm = cam.project(PM)
    >>>print(pm)
        [[520. 256.]
        [420. 256.]
        [320. 256.]
        [220. 256.]]
    >>>Q = cam.reprojectToPlane(pm,plane)
    >>>print(np.around(Q,2))
        [[ 2. -0. 10.  1.]
        [ 1. -0. 10.  1.]
        [-0. -0. 10.  1.]
        [-1. -0. 10.  1.]]
 
If this easy reprojection does not fit your needs, you can use reproject(p) which returns a direction vector
and write your own reprojection wrapper.   

.. note::

    reprojectToPlane returns a 3D Vector [X Y Z 1] in homogeneous coordinates. They are normalized, so the last element is always 1. You can use just the x,y,z-coordinates with Q[0:3]
    
            
