import boto3
import mercantile
from datetime import datetime
from rio_tiler.io import cogeo

s3 = boto3.resource('s3')
buckets = dict(no2='omi-no2-nasa', aod='modis-aod-nasa', vi='modis-vi-nasa')
# Regions of interest
# NASA Covid Dashboard Supersites
beijing = dict(lat=39.916668, lon=116.383331)
la = dict(lat=34.05, lon=-118.25)
new_york = dict(lat=40.661, lon=-73.944)
san_fran = dict(lat=37.7775, lon=-122.416389)
tokyo = dict(lat=35.689722, lon=139.692222)

latlons = dict(
    beijing=beijing,
    los_angeles=la,
    new_york=new_york,
    san_fran=san_fran,
    tokyo=tokyo
)

# Collection configuration
nodata_values = dict(no2=-1.26765060000000006e+30, aod=-28672, vi=-3000)

def generate_modis_dates():
    modis_dates = {
        'MOD13A2.006': { 2018: [], 2019: [], 2020: [] },
        'MYD13A2.006': { 2018: [], 2019: [], 2020: [] }
    }
    # MODIS VI data is every 16 days, so create a dictionary of dates for looking up the nearest date
    modis_vi_bucket = s3.Bucket(buckets['vi'])
    for year in range(2018, 2021):
        for collection in modis_dates.keys():
            for tif in list(modis_vi_bucket.objects.filter(Prefix=f'{collection}/{year}')):
                date = datetime.strptime(tif.key, f'{collection}/%Y.%m.%d.tif')
                modis_dates[collection][year].append(date)
    return modis_dates

modis_dates = generate_modis_dates()

def city_title(city_key):
    return ' '.join(city_key.split('_')).title()
    
def nearest(items, pivot):
    """
    Return the nearest item to 'pivot' from a list of items
    Used to find the nearest date from MODIS VI collections
    """
    return min(items, key=lambda x: abs(x - pivot))    

def get_tile_url(opts={}):
    collection = opts.get('collection')
    date = opts.get('date')
    bucket_name = buckets[collection]
    bucket = s3.Bucket(bucket_name)
    if collection == 'no2':
        tif_url_prefix = f'OMI-Aura_L3-OMNO2d_{date.year}m{date.month:02}{date.day:02}'
        tif = list(bucket.objects.filter(Prefix=tif_url_prefix))[0]
        tile_url = f's3://{bucket_name}/{tif.key}'
    elif collection == 'aod':
        tile_url = f's3://{bucket_name}/{date.year}.{date.month:02}.{date.day:02}.tif'
    elif collection == 'vi':
        # VI is every 16 days, so return the closest day
        closest_terra_day = nearest(modis_dates['MOD13A2.006'][date.year], date)
        closest_aqua_day = nearest(modis_dates['MYD13A2.006'][date.year], date)
        if abs(date - closest_terra_day) < abs(date - closest_aqua_day):
            nearest_date = closest_terra_day
            vi_collection = 'MOD13A2.006'
        else:
            nearest_date = closest_aqua_day
            vi_collection = 'MYD13A2.006'
        tile_url = f's3://{bucket_name}/{vi_collection}/{nearest_date.year}.{nearest_date.month:02}.{nearest_date.day:02}.tif'
    return tile_url

def get_city_tile(opts={}):
    """ Return tile for city on date """
    city = opts.get('city')
    zoom = opts.get('zoom')
    city_tile = mercantile.tile(latlons[city]['lon'], latlons[city]['lat'], zoom)
    tile_url = get_tile_url(opts)
    tile, mask = cogeo.tile(
        tile_url,
        city_tile.x,  # mercator tile X value (arbitrary map tile location within the source image)
        city_tile.y,  # mercator tile Y value
        zoom,  # mercator tile Z value
        tilesize=256
    )
    return tile