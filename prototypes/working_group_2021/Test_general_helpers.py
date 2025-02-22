import numpy as np
import netCDF4 as nc
from unittest import TestCase, skip
from numpy.core.fromnumeric import shape
from pathlib import Path
from testinfrastructure.InDirTest import InDirTest
import general_helpers as gh

class Test_general_helpers(InDirTest):

    #def test_make_fluxrates_from_kf(,xi_d):    
    
    @skip
    def test_month_2_day_index(self):
        self.assertEqual(
                month_2_day_index([0]),
                [0]
        ) 
        self.assertEqual(
                month_2_day_index([1]),
                [31]
        ) 
        self.assertEqual(
                month_2_day_index([2]),
                [59]
        ) 
        self.assertEqual(
                month_2_day_index([3]),
                [90]
        ) 
        self.assertEqual(
                month_2_day_index([1,3]),
                [31,90]
        ) 
    
    def test_day_2_month_index(self):
        # note that days are counted from zero so day 29 is January 30.
        self.assertEqual(gh.day_2_month_index( 0), 0) 
        self.assertEqual(gh.day_2_month_index(30), 1) 
        self.assertEqual(gh.day_2_month_index(31), 1) 
        self.assertEqual(gh.day_2_month_index(60), 2) 

    
    def test_month_2_day_index_vm(self):
        self.assertEqual(
                gh.month_2_day_index_vm([0]),
                [0]
        ) 
        self.assertEqual(
                gh.month_2_day_index_vm([1]),
                [31]
        ) 
        self.assertEqual(
                gh.month_2_day_index_vm([2]),
                [59]
        ) 
        self.assertEqual(
                gh.month_2_day_index_vm([3]),
                [90]
        ) 
        self.assertEqual(
                gh.month_2_day_index_vm([1,3]),
                [31,90]
        ) 
    
    def test_day_2_month_index_vm(self):
        # note that days are counted from zero so day 30 is January 31.
        self.assertEqual(gh.day_2_month_index_vm( 0), 0) 
        self.assertEqual(gh.day_2_month_index_vm(30), 0) 
        self.assertEqual(gh.day_2_month_index_vm(31), 1) 
        self.assertEqual(gh.day_2_month_index_vm(60), 2) 


    def test_pixel_area_on_unit_sphere(self):
        # we test that the pixel areas for a whole
        # grid sum up to 1
        #lat_len=181
        #lon_len=360
        lat_len=19
        lon_len=360
        lats=np.ma.masked_array(np.linspace(-90,90,lat_len))
        lons=np.ma.masked_array(np.linspace(-179.5,179.5,lon_len))
        delta_lat=(lats.max()- lats.min())/(len(lats)-1)
        delta_lon=(lons.max() -lons.min())/(len(lons)-1)

        puaf_sym= gh.make_pixel_area_on_unit_spehre(delta_lat, delta_lon,sym=True)
        puaf= gh.make_pixel_area_on_unit_spehre(delta_lat, delta_lon)

        # assert identical values
        lw=np.array(
            [
                puaf(lats[lat_ind])
                for lat_ind in range(len(lats))
            ],
            dtype=np.float64
        )
        lws=np.array(
            [
                puaf_sym(lats[lat_ind])
                for lat_ind in range(len(lats))
            ],
            dtype=np.float64
        )
        # check for equivalence of our manually solved integral with sympy
        # (found typos this way....)
        self.assertTrue(np.allclose(lw,lws))

        # check for symetrie (the weighs for pos and negative latitudes should
        # be the same
        pres = np.array([puaf(lat)  for lat in lats ],dtype=np.float64)
        nres = np.array([puaf(-lat)  for lat in lats ],dtype=np.float64)
        self.assertTrue(np.allclose(pres,nres))
       
        
        # having established the equality of the two ways to compute the
        # weights we check that they add up to 1
        self.assertTrue(
            np.allclose(
                np.sum(
                    [
                        np.sum(
                            [   
                                puaf(lats[lat_ind])
                                for lon_ind in range(len(lons))    
                            ]
                        )
                        for lat_ind in range(len(lats))    
                    ],
                    dtype=np.float64
                ),
                4*np.pi #surface area of the unit sphere
            )
        )
        
    def test_global_average(self):
        # we create data similar to cmip6 and trendy. These are masked arrays:
        # the lat lon combinations that have no landpoints are marked with 
        # False in the mask which is a boolean array of the same shape as 
        # the actual value array) the
        # 
        # The following commented lines show how to get the 
        # lats and longs are as in jon_yibs 
        # lat_name = 'latitude'
        # lon_name = 'longitude'
        # lats=nds.variables[lat_name].__array__()
        # longs=nds.variables[lon_name].__array__()
        # target_var_names=set(nds.variables.keys()).difference([lat_name,lon_name,'time'])
        # arr = target_var_names[0] 
        lat_len_1=3
        lat_len_2=3
        lat_len_3=3
        lat_len=sum(
            [
                lat_len_1,
                lat_len_2,
                lat_len_3
            ]
        )
        lon_len_1=120
        lon_len_2=120
        lon_len_3=120
        lon_len=sum(
            [
                lon_len_1,
                lon_len_2,
                lon_len_3
            ]
        )
        time_len=3
        lats=np.ma.masked_array(np.linspace(-90,90,lat_len))
        lons=np.ma.masked_array(np.linspace(-179.5,179.5,lon_len))
        arr=np.ma.ones(shape=(time_len,lat_len,lon_len))
        
        res = gh.global_mean(lats,lons,arr)
        self.assertEqual(
            res.shape,
            (time_len,)
        )

        # we assert that the average of a constant field is the constant value
        self.assertTrue(
            np.allclose(
                res,
                np.ones((time_len,))
            )
        )

        # now we test the same properties with a masked array
        # as e.g the CMIP6 files that Kostia uses
        # dataPath = Path(conf_dict['dataPath'])
        # ds=nc.Dataset('cLeaf_Lmon_MIROC-ES2L_1pctCO2-bgc_r1i1p1f2_gn_185001-199912.nc')
        # pwd
        # dataPath
        # ds=nc.Dataset(dataPath.joinpath('cLeaf_Lmon_MIROC-ES2L_1pctCO2-bgc_r1i1p1f2_gn_185001-199912.nc'))
        # cLeaf = ds.variables['cLeaf'].__array__()
        # in this array many fields are masked
         
        # note that in python boolean values are equivalent to integers
        # 1 = True , 0 = False
        mask=np.stack(
            [
                np.ones(shape=(time_len,lat_len_1,lon_len)),
                np.zeros(shape=(time_len,lat_len_2,lon_len)),
                np.ones(shape=(time_len,lat_len_3,lon_len))
            ],
            axis=1
        )
        arr=np.ma.array(
            np.ones(shape=(time_len,lat_len,lon_len)),
            mask=mask
        )
        res = gh.global_mean(lats,lons,arr)
        self.assertTrue(
            np.allclose(
                res,
                np.ones((time_len,))
            )
        )
        # now we block out some longitudes
        mask=np.stack(
            [
                np.ones(shape=(time_len,lat_len,lon_len_1)),
                np.zeros(shape=(time_len,lat_len,lon_len_2)),
                np.ones(shape=(time_len,lat_len,lon_len_3))
            ],
            axis=2
        )
        arr=np.ma.array(
            np.ones(shape=(time_len,lat_len,lon_len)),
            mask=mask
        )
        # we assert that the average of a constant field is the constant value
        self.assertTrue(
            np.allclose(
                gh.global_mean(lats,lons,arr),
                np.ones((time_len,))
            )
        )

    def test_get_nan_pixels(self):
        n_t=2
        n_lats=3
        n_lons=4
        ref= np.zeros((n_t,n_lats,n_lons))
        ref[0,2,3]=np.nan
        ref[1,1,3]=np.nan
        mask=np.zeros((n_t,n_lats,n_lons))
        ma_arr=np.ma.array(ref,mask=mask)
        ds = nc.Dataset('diskless_example.nc','w',diskless=True,persist=True)
        time = ds.createDimension('time',size=n_t)
        lat = ds.createDimension('lat',size=n_lats)
        lon = ds.createDimension('lon',size=n_lons)
        test=ds.createVariable("test",np.float64,['time','lat','lon'])
        test[:,:,:]=ma_arr

        self.assertEqual(
            ((1,3),(2,3)),
            gh.get_nan_pixels(test)
        )

    def test_get_nan_pixel_mask(self):
        n_t=2
        n_lats=3
        n_lons=4
        arg= np.zeros((n_t,n_lats,n_lons))
        arg[0,2,3]=np.nan
        arg[1,1,3]=np.nan
        mask=np.zeros((n_t,n_lats,n_lons),dtype=np.bool_)
        mask[:,0,0]=True
        ma_arr=np.ma.array(arg,mask=mask)
        ds = nc.Dataset('diskless_example.nc','w',diskless=True,persist=False)
        time = ds.createDimension('time',size=n_t)
        lat = ds.createDimension('lat',size=n_lats)
        lon = ds.createDimension('lon',size=n_lons)
        test_var=ds.createVariable("test_var",np.float64,['time','lat','lon'])
        test_var[:,:,:]=ma_arr

        ref_mask=np.zeros((n_lats,n_lons),dtype=np.bool_) #2 dimensional
        ref_mask[0,0]=True
        ref_mask[2,3]=True
        ref_mask[1,3]=True
        res = gh.get_nan_pixel_mask(test_var)
        self.assertTrue(
            (ref_mask == res).all()
        )

        ma_arr=np.ma.array(arg,mask=False)
        ds = nc.Dataset('diskless_example1.nc','w',diskless=True,persist=False)
        time = ds.createDimension('time',size=n_t)
        lat = ds.createDimension('lat',size=n_lats)
        lon = ds.createDimension('lon',size=n_lons)
        test_var=ds.createVariable("test_var",np.float64,['time','lat','lon'])
        test_var[:,:,:]=ma_arr
        ref_mask=np.zeros((n_lats,n_lons),dtype=np.bool_) #2 dimensional
        ref_mask[2,3]=True
        ref_mask[1,3]=True
        res = gh.get_nan_pixel_mask(test_var)
        self.assertTrue(
            (ref_mask == res).all()
        )

    def test_globalmean_var(self):
        # we create data similar to cmip6 and trendy. These are masked arrays:
        # the lat lon combinations that have no landpoints are marked with 
        # False in the mask which is a boolean array of the same shape as 
        # the actual value array) the
        # 
        # The following commented lines show how to get the 
        # lats and longs are as in jon_yibs 
        # lat_name = 'latitude'
        # lon_name = 'longitude'
        # lats=nds.variables[lat_name].__array__()
        # longs=nds.variables[lon_name].__array__()
        # target_var_names=set(nds.variables.keys()).difference([lat_name,lon_name,'time'])
        # arr = target_var_names[0] 
        lat_len_1=3
        lat_len_2=3
        lat_len_3=3
        lat_len=sum(
            [
                lat_len_1,
                lat_len_2,
                lat_len_3
            ]
        )
        lon_len_1=120
        lon_len_2=120
        lon_len_3=120
        lon_len=sum(
            [
                lon_len_1,
                lon_len_2,
                lon_len_3
            ]
        )
        time_len=3
        lats=np.ma.masked_array(np.linspace(-90,90,lat_len))
        lons=np.ma.masked_array(np.linspace(-179.5,179.5,lon_len))
        arr=np.ma.ones(shape=(time_len,lat_len,lon_len))
        vn='test_var'
        trunk='{}_1'.format(vn)
        ds = nc.Dataset(Path('{}.nc'.format(trunk)), 'w',diskless=True,persist=False)
        time = ds.createDimension('time',size=time_len)
        lat = ds.createDimension('lat',size=lat_len)
        lon = ds.createDimension('lon',size=lon_len)
        test_var=ds.createVariable(vn, np.float64, ['time','lat','lon'])
        test_var[:,:,:]=arr

        res_arr=gh.global_mean(
            lats,
            lons,
            arr
        )
        res_var=gh.global_mean_var(
            lats,
            lons,
            np.zeros( (lat_len,lon_len), dtype=np.bool_),
            arr
        )
        self.assertTrue(
            (res_arr == res_var).all()
        )
        cache_path = Path('{}_gm.nc'.format(trunk))

        gh.write_global_mean_cache(
            cache_path,
            res_var,
            vn
        )
        #def get_cached_global_mean(gm_path, vn):
        #    return nc.Dataset(str(gm_path)).variables[vn].__array__()

        res_cache = gh.get_cached_global_mean(
            cache_path,
            vn
        )
        #from IPython import embed;embed() 
        self.assertTrue(
            (res_cache==res_var).all()
        )
        
        ds.close()

       # now we test the same properties with a masked array
       # as e.g the CMIP6 files that Kostia uses
       # dataPath = Path(conf_dict['dataPath'])
       # ds=nc.Dataset('cLeaf_Lmon_MIROC-ES2L_1pctCO2-bgc_r1i1p1f2_gn_185001-199912.nc')
       # pwd
       # dataPath
       # ds=nc.Dataset(dataPath.joinpath('cLeaf_Lmon_MIROC-ES2L_1pctCO2-bgc_r1i1p1f2_gn_185001-199912.nc'))
       # cLeaf = ds.variables['cLeaf'].__array__()
       # in this array many fields are masked
        
       # note that in python boolean values are equivalent to integers
       # 1 = True , 0 = False
        mask=np.stack(
            [
                np.ones(shape=(time_len,lat_len_1,lon_len)),
                np.zeros(shape=(time_len,lat_len_2,lon_len)),
                np.ones(shape=(time_len,lat_len_3,lon_len))
            ],
            axis=1
        )
        arr=np.ma.array(
            np.ones(shape=(time_len,lat_len,lon_len)),
            mask=mask
        )
        vn='test_var'
        trunk='{}_2'.format(vn)
        ds = nc.Dataset(Path('{}.nc'.format(trunk)), 'w',diskless=True,persist=False)
        time = ds.createDimension('time',size=time_len)
        lat = ds.createDimension('lat',size=lat_len)
        lon = ds.createDimension('lon',size=lon_len)
        test_var=ds.createVariable(vn, np.float64, ['time','lat','lon'])
        test_var[:,:,:]=arr
        res_arr=gh.global_mean(
            lats,
            lons,
            arr
        )
        res_var=gh.global_mean_var(
            lats,
            lons,
            mask.sum(axis=0),
            arr
        )
        self.assertTrue(
            (res_arr == res_var).all()
        )
        cache_path = Path('{}_gm.nc'.format(trunk))

        gh.write_global_mean_cache(
            cache_path,
            res_var,
            vn
        )
        res_cache = gh.get_cached_global_mean(
            cache_path,
            vn
        )
        self.assertTrue(
            (res_cache==res_var).all()
        )
        
        ds.close()

        # now we block out some longitudes
        mask=np.stack(
            [
                np.ones(shape=(time_len,lat_len,lon_len_1)),
                np.zeros(shape=(time_len,lat_len,lon_len_2)),
                np.ones(shape=(time_len,lat_len,lon_len_3))
            ],
            axis=2
        )
        arr=np.ma.array(
            np.ones(shape=(time_len,lat_len,lon_len)),
            mask=mask
        )
        vn='test_var'
        trunk='{}_3'.format(vn)
        ds = nc.Dataset(Path('{}.nc'.format(trunk)), 'w',diskless=True,persist=False)
        time = ds.createDimension('time',size=time_len)
        lat = ds.createDimension('lat',size=lat_len)
        lon = ds.createDimension('lon',size=lon_len)
        test_var=ds.createVariable(vn, np.float64, ['time','lat','lon'])
        test_var[:,:,:]=arr
        res_arr=gh.global_mean(
            lats,
            lons,
            arr
        )
        res_var=gh.global_mean_var(
            lats,
            lons,
            mask.sum(axis=0),
            arr
        )
        self.assertTrue(
            (res_arr == res_var).all()
        )
        cache_path = Path('{}_gm.nc'.format(trunk))

        gh.write_global_mean_cache(
            cache_path,
            res_var,
            vn
        )
        res_cache = gh.get_cached_global_mean(
            cache_path,
            vn
        )
        self.assertTrue(
            (res_cache==res_var).all()
        )
        
        ds.close()
