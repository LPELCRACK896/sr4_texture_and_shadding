import lpmath as lpm

def fragmentShader(render, **kwargs):
    u, v, w = kwargs["baryCoords"]
    b, g, r = kwargs['vColor']
    triangleNormal = kwargs['triangleNormal']
    b /= 255
    g /= 255
    r /= 255

    intensity = lpm.productoPunto(triangleNormal, [-a for a in render.dirLight])
    
    b *= intensity
    g *= intensity
    r *= intensity

    if intensity>0:
        return r, g, b
    return 0, 0, 0