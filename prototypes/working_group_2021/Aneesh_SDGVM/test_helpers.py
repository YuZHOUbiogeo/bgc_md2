# this file provides some variables for testing.
from collections import namedtuple
from sympy import Symbol, Function
from pathlib import Path
import json 
def make_test_args(conf_dict,msh,mvs):
    TestArgs=namedtuple(
        "TestArgs",
        [
            "V_init",
            "par_dict",
            "func_dict",
            "mvs",
            "dvs",
            "svs",
            "epa_0",
            "epa_min",
            "epa_max",
            "cpa"
        ]
    )
    par_dict={
        Symbol(k): v for k,v in {
             'beta_leaf':0.5, 
             'beta_wood':0.4, 
             'r_C_leaf2abvstrlit' :0.0003*0.85,
             'r_C_leaf2abvmetlit':0.0003*0.85,
             'r_C_wood2abvmetlit':0.00006*1.9,
             'r_C_wood2abvstrlit':0.00006*1.9,
             'r_C_root2belowmetlit':0.000034*2.105,
             'r_C_root2belowstrlit':0.000032*2.105,
             'r_C_abvstrlit2slowsom':0.00003*1.8,
             'r_C_abvstrlit2surface_microbe':0.00005*2,
             'r_C_abvmetlit2surface_microbe':0.00005,
             'r_C_belowmetlit2soil_microbe':0.00002*50,
             'r_C_belowstrlit2slowsom':0.00006*60,
             'r_C_belowstrlit2soil_microbe':0.0003*60,
             'r_C_passsom2soil_microbe':0.00005*100,
             'r_C_slowsom2passsom':0.0005*100,
             'r_C_slowsom2soil_microbe':0.0005*100,
             'r_C_soil_microbe2passsom':0.006*100,
             'r_C_soil_microbe2slowsom':0.006*105,
             'r_C_surface_microbe2slowsom':0.006*100,
            
             'r_C_abvstrlit_rh':0.00975/11,
             'r_C_abvmetlit_rh':0.024667/10,
             'r_C_belowstrlit_rh':0.011333/10,
             'r_C_belowmetlit_rh':0.028264/10,
             'r_C_soil_microbe_rh':0.0003*2.2,
             'r_C_slowsom_rh':0.00004*2,
             'r_C_passsom_rh':0.000006875*2,
             'r_C_surface_microbe_rh':0.000003*2.2,
             'C_leaf_0': 0.18,
             'C_abvstrlit_0': 0.59,    #svs_0.cLitter/4,
             'C_abvmetlit_0': 0.24,    #svs_0.cLitter/4,
             'C_blwstrlit_0': 0.00287261,    #svs_0.cLitter/4,
             'C_surfacemic_0': 9.4e-5,    #svs_0.cSoil/4,
             'C_soilmic_0': 0.049,      #svs_0.cSoil/4,
             'C_slow_0': 0.29828058     #svs_0.cSoil/4
        }.items()
    }
    svs,dvs=msh.get_example_site_vars(dataPath=Path(conf_dict["dataPath"]))
    func_dict={
        Function(k):v
        for k,v in {
            'NPP':msh.make_npp_func(dvs),
            'xi':msh.make_xi_func(dvs)
        }.items()
    }
    svs_0=msh.Observables(*map(lambda v: v[0],svs))
    # create a start parameter tuple for the mcmc.
    epa_0=msh.EstimatedParameters(
         beta_leaf=0.5, 
         beta_wood=0.4, 
         r_C_leaf2abvstrlit= 0.0003*0.85,
         r_C_leaf2abvmetlit=0.0003*0.85,
         r_C_wood2abvmetlit=0.00006*1.9,
         r_C_wood2abvstrlit=0.00006*1.9,
         r_C_root2belowmetlit=0.000034*2.105,
         r_C_root2belowstrlit=0.000032*2.105,
         r_C_abvstrlit2slowsom=0.00003*1.8,
         r_C_abvstrlit2surface_microbe=0.00005*2,
         r_C_abvmetlit2surface_microbe=0.00005,
         r_C_belowmetlit2soil_microbe=0.00002*50,
         r_C_belowstrlit2slowsom=0.00006*60,
         r_C_belowstrlit2soil_microbe=0.0003*60,
         #r_C_leached=0.0001,
         r_C_passsom2soil_microbe=0.00005*100,
         r_C_slowsom2passsom=0.0005*100,
         r_C_slowsom2soil_microbe=0.0005*100,
         r_C_soil_microbe2passsom=0.006*100,
         r_C_soil_microbe2slowsom=0.006*105,
         r_C_surface_microbe2slowsom=0.006*100,
         r_C_abvstrlit_rh=0.00975/11,
         r_C_abvmetlit_rh=0.024667/10,
         r_C_belowstrlit_rh=0.011333/10,
         r_C_belowmetlit_rh=0.028264/10,
         r_C_soil_microbe_rh=0.0003*2.2,
         r_C_slowsom_rh=0.00004*2,
         r_C_passsom_rh=0.000006875*2,
         r_C_surface_microbe_rh=0.000003*2.2,
         C_leaf_0=svs_0.cVeg/3,
         C_abvstrlit_0= 0.59,    #svs_0.cLitter/4,
         C_abvmetlit_0= 0.24,    #svs_0.cLitter/4,
         C_blwstrlit_0= 0.00287261,    #svs_0.cLitter/4,
         C_surfacemic_0= 9.4e-5,    #svs_0.cSoil/4,
         C_soilmic_0= 0.049,      #svs_0.cSoil/4,
         C_slow_0= 0.29828058     #svs_0.cSoil/4
    )
    epa_min=msh.EstimatedParameters(
         beta_leaf=0, 
         beta_wood=0, 
         r_C_leaf2abvstrlit= epa_0.r_C_leaf2abvmetlit/100,
         r_C_abvmetlit2surface_microbe= epa_0.r_C_abvmetlit2surface_microbe/100,
         r_C_abvstrlit2slowsom=epa_0.r_C_abvstrlit2slowsom/100,
         r_C_abvstrlit2surface_microbe=epa_0.r_C_abvstrlit2surface_microbe/100,
         r_C_belowmetlit2soil_microbe=epa_0.r_C_belowmetlit2soil_microbe/100,
         r_C_belowstrlit2slowsom=epa_0.r_C_belowstrlit2slowsom/100,
         r_C_belowstrlit2soil_microbe=epa_0.r_C_belowstrlit2soil_microbe/100,
         #r_C_leached=epa_0.r_C_leached/100,
         r_C_leaf2abvmetlit=epa_0.r_C_leaf2abvmetlit/100,
         r_C_passsom2soil_microbe=epa_0.r_C_passsom2soil_microbe/100,
         r_C_root2belowmetlit=epa_0.r_C_root2belowmetlit/100,
         r_C_root2belowstrlit=epa_0.r_C_root2belowstrlit/100,
         r_C_slowsom2passsom=epa_0.r_C_slowsom2passsom/100,
         r_C_slowsom2soil_microbe=epa_0.r_C_slowsom2soil_microbe/100,
         r_C_soil_microbe2passsom=epa_0.r_C_soil_microbe2passsom/100,
         r_C_soil_microbe2slowsom=epa_0.r_C_soil_microbe2slowsom/100,
         r_C_surface_microbe2slowsom=epa_0.r_C_surface_microbe2slowsom/100,
         r_C_wood2abvmetlit=epa_0.r_C_wood2abvmetlit/100,
         r_C_wood2abvstrlit=epa_0.r_C_wood2abvstrlit/100,
         r_C_abvstrlit_rh=epa_0.r_C_abvstrlit_rh/100,
         r_C_abvmetlit_rh=epa_0.r_C_abvmetlit_rh/100,
         r_C_belowstrlit_rh=epa_0.r_C_belowstrlit_rh/100,
         r_C_belowmetlit_rh=epa_0.r_C_belowmetlit_rh/100,
         r_C_soil_microbe_rh=epa_0.r_C_soil_microbe_rh/100,
         r_C_surface_microbe_rh=epa_0.r_C_surface_microbe_rh/100,
         r_C_slowsom_rh=epa_0.r_C_slowsom_rh/100,
         r_C_passsom_rh=epa_0.r_C_passsom_rh/100,
         C_leaf_0=0,
         #C_root_0=svs_0.cVeg/3,
         C_abvstrlit_0=0,
         C_abvmetlit_0=0,
         C_blwstrlit_0=0,
         C_surfacemic_0=0,
         C_soilmic_0=0,
         C_slow_0=0
    )


    epa_max=msh.EstimatedParameters(
        beta_leaf=1, 
        beta_wood=1, 
         r_C_leaf2abvstrlit= epa_0.r_C_leaf2abvmetlit*100,
         r_C_abvmetlit2surface_microbe= epa_0.r_C_abvmetlit2surface_microbe*100,
         r_C_abvstrlit2slowsom=epa_0.r_C_abvstrlit2slowsom*100,
         r_C_abvstrlit2surface_microbe=epa_0.r_C_abvstrlit2surface_microbe*100,
         r_C_belowmetlit2soil_microbe=epa_0.r_C_belowmetlit2soil_microbe*100,
         r_C_belowstrlit2slowsom=epa_0.r_C_belowstrlit2slowsom*100,
         r_C_belowstrlit2soil_microbe=epa_0.r_C_belowstrlit2soil_microbe*100,
         #r_C_leached=epa_0.r_C_leached*100,
         r_C_leaf2abvmetlit=epa_0.r_C_leaf2abvmetlit*100,
         r_C_passsom2soil_microbe=epa_0.r_C_passsom2soil_microbe*100,
         r_C_root2belowmetlit=epa_0.r_C_root2belowmetlit*100,
         r_C_root2belowstrlit=epa_0.r_C_root2belowstrlit*100,
         r_C_slowsom2passsom=epa_0.r_C_slowsom2passsom*100,
         r_C_slowsom2soil_microbe=epa_0.r_C_slowsom2soil_microbe*100,
         r_C_soil_microbe2passsom=epa_0.r_C_soil_microbe2passsom*100,
         r_C_soil_microbe2slowsom=epa_0.r_C_soil_microbe2slowsom*100,
         r_C_surface_microbe2slowsom=epa_0.r_C_surface_microbe2slowsom*100,
         r_C_wood2abvmetlit=epa_0.r_C_wood2abvmetlit*100,
         r_C_wood2abvstrlit=epa_0.r_C_wood2abvstrlit*100,
         r_C_abvstrlit_rh=epa_0.r_C_abvstrlit_rh*100,
         r_C_abvmetlit_rh=epa_0.r_C_abvmetlit_rh*100,
         r_C_belowstrlit_rh=epa_0.r_C_belowstrlit_rh*100,
         r_C_belowmetlit_rh=epa_0.r_C_belowmetlit_rh*100,
         r_C_soil_microbe_rh=epa_0.r_C_soil_microbe_rh*100,
         r_C_surface_microbe_rh=epa_0.r_C_surface_microbe_rh*100,
         r_C_slowsom_rh=epa_0.r_C_slowsom_rh*100,
         r_C_passsom_rh=epa_0.r_C_passsom_rh*100,
         C_leaf_0=svs_0.cVeg,
         #C_root_0=svs_0_0.cVeg/3,
         C_abvstrlit_0=svs_0.cLitter,
         C_abvmetlit_0=svs_0.cLitter,
         C_blwstrlit_0=svs_0.cLitter,
         C_surfacemic_0=svs_0.cSoil,
         C_soilmic_0=svs_0.cSoil,
         C_slow_0=svs_0.cSoil
    )    
    cpa = msh.Constants(
         cVeg_0=svs_0.cVeg,
         cLitter_0=svs_0.cLitter,
         cSoil_0=svs_0.cSoil,
         cRoot_0 = svs_0.cRoot,
         npp_0=dvs.npp[0],
         rh_0=svs_0.rh,
         number_of_months=len(svs.rh)
    )

    StartVector = msh.make_StartVector(mvs) 
    V_init= StartVector(
        C_leaf = svs_0.cVeg/3,
        C_root= svs_0.cRoot,
        C_wood = svs_0.cVeg/3,
        C_abvstrlit = 0.59,
        C_abvmetlit = 0.24,
        C_belowstrlit = 0.00287261,
        C_belowmetlit = svs_0.cLitter - 0.59 - 0.24 - 0.00287261,
        C_surface_microbe =9.4e-5,
        C_soil_microbe = 0.049,
        C_slowsom =0.29828058,
        C_passsom= svs_0.cSoil - 9.4e-5 - 0.049 - 0.29828058,
        rh=svs_0.rh
    )
    return TestArgs(
        V_init=V_init,
        par_dict=par_dict,
        func_dict=func_dict,
        dvs=dvs,
        svs=svs,
        mvs=mvs,
        epa_0=epa_0,
        epa_min=epa_min,
        epa_max=epa_max,
        cpa=cpa
    )
