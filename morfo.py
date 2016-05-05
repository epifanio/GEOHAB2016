import grass.script as grass

def makemorfo(input, nnwin=9, pmwin=15, resolution=None, overwrite=True, remove=False):
    r_elevation = input
    #if resolution is not None:
    #    grass.run_command('g.region', rast = r_elevation, flags = 'ap')
    #else :
    #    grass.run_command('g.region', rast = r_elevation, res=resolution, flags = 'ap')
    suffix = str(r_elevation)+'_'
    xavg = suffix+'avg'
    xmin = suffix+'min'
    xmax = suffix+'max'
    xslope = suffix+'slope'
    xprofc = suffix+'profc'
    xcrosc = suffix+'crosc'
    xminic = suffix+'minic'
    xmaxic = suffix+'maxic'
    xlongc = suffix+'longc'
    xer = suffix+'er'
    img = [suffix+'avg', suffix+'min', suffix+'max', suffix+'er', suffix+'slope', suffix+'profc', suffix+'crosc', suffix+'minic', suffix+'maxic', suffix+'longc']
    if remove is True:
        rast = '%s,%s,%s,%s,%s,%s,%s,%s,%s' % (xavg, xmin, xmax, xslope, xprofc, xcrosc, xminic, xmaxic, xlongc)
        grass.run_command('g.remove', type='rast', name=rast, flags='f')
    else :
        grass.run_command('r.neighbors', input=r_elevation, output=xavg, size=nnwin, method='average', overwrite=overwrite)
        print("average done")
        grass.run_command('r.neighbors', input=r_elevation, output=xmin, size=nnwin, method='minimum', overwrite=overwrite)
        print("minimum done")
        grass.run_command('r.neighbors', input=r_elevation, output=xmax, size=nnwin, method='maximum', overwrite=overwrite)
        print("maximum done")
        grass.run_command('r.mapcalc' , expression='%s = 1.0 * (%s - %s)/(%s - %s)' % (xer, xavg, xmin, xmax, xmin) , overwrite=True)
        #!r.fillnulls input={xer} output={xer} --o --q
        print("er done")
        
        grass.run_command('r.param.scale', input=r_elevation, output=xslope, size=nnwin, slope_tolerance=0.1, curvature_tolerance =0.0001, method='slope', exponent =0.0, zscale=1.0, overwrite=True) 
        print("slope done")
        grass.run_command('r.param.scale', input=r_elevation, output=xprofc, size=nnwin, slope_tolerance=0.1, curvature_tolerance =0.0001, method='profc', exponent =0.0, zscale=1.0, overwrite=True) 
        print("profc done")
        grass.run_command('r.param.scale', input=r_elevation, output=xcrosc, size=nnwin, slope_tolerance=0.1, curvature_tolerance =0.0001, method='crosc', exponent =0.0, zscale=1.0, overwrite=True) 
        print("crosc done")
        grass.run_command('r.param.scale', input=r_elevation, output=xminic, size=nnwin, slope_tolerance=0.1, curvature_tolerance =0.0001, method='minic', exponent =0.0, zscale=1.0, overwrite=True) 
        print("minic done")
        grass.run_command('r.param.scale', input=r_elevation, output=xmaxic, size=nnwin, slope_tolerance=0.1, curvature_tolerance =0.0001, method='maxic', exponent =0.0, zscale=1.0, overwrite=True) 
        print("maxic done")
        grass.run_command('r.param.scale', input=r_elevation, output=xlongc, size=nnwin, slope_tolerance=0.1, curvature_tolerance =0.0001, method='longc', exponent =0.0, zscale=1.0, overwrite=True) 
        print("longc done")
        vrange = grass.read_command('r.info', map=xslope, flags='r').strip().split('\n')
        vmin = vrange[0].split('=')[1]
        vmax = vrange[1].split('=')[1]
        grass.run_command('r.mapcalc' , expression = '%s = (%s/%s)' % (xslope, xslope, vmax), overwrite=True)
        print("xslope done")
    return img