import numpy as np
import xarray as xr

def WOA18reader(var = 'Temperature'):
    """
    This function loads NetCDF data from NODC/NOAA (nodc.noaa.gov) using OpenDAP and xarray
    """
    urls = []
    ds = []
    if var == 'Temperature':
        for i in range(1,13):
            urls.append('https://data.nodc.noaa.gov/thredds/dodsC/ncei/woa/temperature/decav/1.00/woa18_decav_t' +str(i//10) + str(i%10) + \
                                                        '_01.nc')
        urls.append('https://data.nodc.noaa.gov/thredds/dodsC/ncei/woa/temperature/decav/1.00/woa18_decav_t00_01.nc') # annual mean to get below 1,500 m
    elif var == 'Salinity':
        for i in range(1,13):
            urls.append('https://data.nodc.noaa.gov/thredds/dodsC/ncei/woa/salinity/decav/1.00/woa18_decav_s' +str(i//10) + str(i%10) + \
                                                        '_01.nc')
        urls.append('https://data.nodc.noaa.gov/thredds/dodsC/ncei/woa/salinity/decav/1.00/woa18_decav_s00_01.nc')
    elif var == 'Oxygen':
        for i in range(1,13):
            urls.append('https://data.nodc.noaa.gov/thredds/dodsC/ncei/woa/oxygen/all/1.00/woa18_all_o' +str(i//10) + str(i%10) + \
                                                        '_01.nc')
        urls.append('https://data.nodc.noaa.gov/thredds/dodsC/ncei/woa/oxygen/all/1.00/woa18_all_o00_01.nc')
    elif var == 'AOU':
        for i in range(1,13):
            urls.append('https://data.nodc.noaa.gov/thredds/dodsC/ncei/woa/AOU/all/1.00/woa18_all_A' + str(i//10) + str(i%10) + \
                                                        '_01.nc')
        urls.append('https://data.nodc.noaa.gov/thredds/dodsC/ncei/woa/AOU/all/1.00/woa18_all_A00_01.nc')
    elif var == 'Silicate':
        for i in range(1,13):
            urls.append('https://data.nodc.noaa.gov/thredds/dodsC/ncei/woa/silicate/all/1.00/woa18_all_i' + str(i//10) + str(i%10) + \
                                                        '_01.nc')
        urls.append('https://data.nodc.noaa.gov/thredds/dodsC/ncei/woa/silicate/all/1.00/woa18_all_i00_01.nc')
    elif var == 'Nitrate':
        for i in range(1,13):
            urls.append('https://data.nodc.noaa.gov/thredds/dodsC/ncei/woa/nitrate/all/1.00/woa18_all_n'+ str(i//10) + str(i%10) + \
                                                        '_01.nc')
        urls.append('https://data.nodc.noaa.gov/thredds/dodsC/ncei/woa/nitrate/all/1.00/woa18_all_n00_01.nc')
    elif var == 'Phosphate':
        for i in range(1,13):
            urls.append('https://data.nodc.noaa.gov/thredds/dodsC/ncei/woa/phosphate/all/1.00/woa18_all_p'+ str(i//10) + str(i%10) + \
                                                        '_01.nc')
        urls.append('https://data.nodc.noaa.gov/thredds/dodsC/ncei/woa/phosphate/all/1.00/woa18_all_p00_01.nc') # annual mean to get below 1,500 m

    else:
        raise ValueError('This variable is not in WOA18 repository: Temperature, Salinity, Oxygen, AOU, Silicate, Nitrate, Phosphate')

    vardict = {'Temperature': 't_an', 'Salinity': 's_an','Oxygen': 'o_an','AOU': 'A_an', 'Silicate': 'i_an', 'Nitrate': 'n_an',\
                'Phosphate' : 'p_an' } # mapping complete var name to var name in data files

    month_dict = {1 : "JAN", 2 : "FEB", 3: "MAR", 4 : "APR" , 5 : "MAY", 6: "JUN", 7: "JUL", 8 : "AUG", 9 : "SEP", 10 : "OCT", 11 : "NOV", 12 : "DEC"}

    tmp_below_ = xr.open_dataset(urls[-1],decode_times = False)
    tmp_below = tmp_below_[vardict.get(var)].isel(time = 0).values #
    lon = tmp_below_.coords['lon'].values
    lat = tmp_below_.coords['lat'].values
    depth = tmp_below_.coords['depth'].values
    LON, LAT, DEPTH  = np.meshgrid(lon,lat,depth)
    #

    i = 0 
    for url in urls[:-1]:
        i += 1
        print('reading monthly mean of',var,'for month: ', month_dict[i], 'from NODC/NOAA through:\n', url)
        tmp = xr.open_dataset(url,decode_times = False)[vardict.get(var)].isel(time = 0).values
        ds.append(np.concatenate((tmp, tmp_below[tmp.shape[0]:]),axis = 0).swapaxes(0,1).swapaxes(1,2))
    ds = np.stack(ds, axis = 3)
    M3d = LON * 0 
    M3d[~np.isnan(ds[:,:,:,0])] = 1  

    return ds, LON, LAT, DEPTH, M3d 
