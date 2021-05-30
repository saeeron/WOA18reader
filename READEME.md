### This a tiny module to read World Ocean Atlas 2018 monthly climatology

### Installlation 
```shell
git clone 
```
### Example: 
```python
from WOA18reader import WOA18reader

ds, LON,LAT, DEPTH, M3d  = WOA18reader("Phosphate") 
 
 # ds is a numpy array of phosphate data with shape (180, 360, 102, 12), 
 # which are latitude, longitude, depth levels and months   
 # LON is longitude 
 # LAT is latitude 
 # DEPTH is depth
 # M3d is a mask (ocean = 1, land = 0)

```

