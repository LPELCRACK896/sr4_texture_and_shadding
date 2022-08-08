from obj import Obj
from gl import Renderer, V2, V3, V4, NewColor

width = 1024
height = 1500

rend = Renderer(width, height)
rend.glClear()
#rend.glTriangle_std(V2(10, 70), V2(50, 160), V2(70, 80), NewColor(1, 0, 0))
rend.glLoadModel('Sting-Sword-lowpoly.obj', 
                    translate= V3(width/2, height/2, 0),
                    scale = V3(20, 20, 20),
                    rotate=V3(90, 0, 0)
                    )

""" 
rend.glLoadModel('Sting-Sword-lowpoly.obj', 
                    translate= V3(width/2, height/2, 0),
                    scale = V3(10, 10, 10)
                    )

rend.glFinish('3dObj.bmp')
 """
rend.glFinish('output.bmp')