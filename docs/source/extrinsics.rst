Extrinsic Orientation
=====================

The extrinsics submodule is for rotating and translating the camera. It handles all the neccesary coordinate transformations.  

We use our cameras on UAVs. So we additionally  have a gimbal. The coordinate systems of the UAV and the gimbal are different to the cameras coordinate system. In the camera coordinate system z points through the lens. It is a right hand sided coordinate system. X describes the width and y the height of the image and [0,0] is not where the optical axis goes through the image plane. It is on the upper left corner of the image. 
The UAV coordinate system is normally right hand, with x pointing in front direction, y is pointing to the right side and z is pointing down.

Our real world geodetic coordinate system is a left handed one. Z points up and the compas orientation turns right. 0 degree is north, 90 degree is east, 180 degree is south and so on. So if you want to use real altitude above sea level values and normal compass orientation, you have to use the left handed coordinate system, where x points north and y points east and z to the sky. 

But now we should just look at the code to rotate or translate the camera ::

    ext = camproject.Extrinsics()
    ext.setPose(X=0,Y=2,Z=10)
    ext.setGimbal(roll=0,pitch=-90,yaw=0)
    print(np.around(ext.transform(),2))
        [[ 0.  1.  0. -2.]
        [-1.  0. -0.  0.]
        [ 0.  0. -1. 10.]
        [ 0.  0.  0.  1.]]
    
    
In this example we position the UAV at postion [0,2,10] and let the camera point down (nadir).
With ext.transform() we generate a 4 by 4 rotation and translation matrix. the rounding function np.around is just to get easy readable values, else you have very long float numbers with a lot of zeros.  
 
This matrix can be used to set our Camera attitude matrix ::
 
    cam.attitudeMat(ext.transform())

With this we reposition and reorientate the camera in our scene. So whenever you make a new picture with your drone and have new coordinates use ext.setPosition() and/or ext.setGimbal() and set cam.attitudeMat(ext.transform()).

Okay, back to the code. setPose is clear, X is the geodetic north direction, Y is geodetic east and Z is any sky pointing altitude. I prefer the barometric altitude, which starts with 0 at starting position. But never use latitude and longitude for Y and X, 'coz these are not orthogonal to each other. Convert them to UTM or another orthogonal system.
Roll, pitch and yaw are in dregree (0 to 360). have alook at https://en.wikipedia.org/wiki/Aircraft_principal_axes for the uav orientations.

If you wonder why there is not a diagonal matrix, like in the quickstart example. It is due to the coordinate system transformation. Using the extrinsics module allows you to set in coordinates and orientations from a left hand coordinate system.

     




