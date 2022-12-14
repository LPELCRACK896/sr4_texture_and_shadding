from obj import Obj
from gl import Renderer, V2, V3, V4, NewColor
from shaders import fragmentShader
width = 1024
height = 1024

rend = Renderer(width, height)
rend.active_shader = fragmentShader
rend.glClear()
#rend.glTriangle_bc(V2(10, 70), V2(50, 300), V2(70, 100), NewColor(1, 0, 0))
rend.glLoadModel('model.obj', 
                    translate= V3(width/2, height/2, 0),
                    scale = V3(200, 200, 200), rotate=V3(0, 180, 0)
                    ) 

"""
rend.glLoadModel('Sting-Sword-lowpoly.obj', 
                    translate= V3(width/2, height/2, 0),
                    scale = V3(10, 10, 10)
                    )

rend.glFinish('3dObj.bmp')
 """
rend.glFinish('output.bmp')