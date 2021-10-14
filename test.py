import camproject
import numpy as np

#print(camproject.__version__)
cam = camproject.Camera()
ext = camproject.Extrinsics()
cam.intrinsics(640,512,1000,320,260)

ext.setPose(X=0,Y=0,Z=10)
ext.setGimbal(roll=0,pitch=90,yaw=0)
cam.attitudeMat(ext.transform())


P = np.array([[1],[2],[0],[1]])   

p = cam.project(P)

print("my 3D-Point P: ",P)
print("Camera is here: ", np.around(cam.position(),4))
print("projected on pixel: ",p)

RPvecH = cam.reproject(p)
if RPvecH.ndim==1:
    RPvecH = RPvecH.reshape(1,RPvecH.shape[0]).T
rayDirection = RPvecH #/ np.linalg.norm(RPvecH)
rayPoint = cam.position()
plane = np.array([[0,0,1,0]]).T

print("my reprojection vector, rayDirection: ",np.around(rayDirection,4))
print("cam position, rayPoint",np.around(rayPoint,4))
print("plane",plane)

print("reprojectToPlane:", cam.reprojectToPlane(p,plane))

#Q = cam.reprojectToPlane(p,15,np.array([0,0,-1]))

#print("my reprojected 3D-Point:", np.around(Q,4))