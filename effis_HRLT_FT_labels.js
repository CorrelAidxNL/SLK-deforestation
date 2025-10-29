var forest_type = "projects/slk-deforest-and-reforest/assets/HRL_ForestType_Kosovo_2021"
var effis = ee.FeatureCollection('projects/slk-deforest-and-reforest/assets/effis_layer');
var kosovo = ee.FeatureCollection('projects/slk-deforest-and-reforest/assets/HDX_Kosovo');

//Data used:
//forest_type : Locally Kosovo-clipped 10 m resolution Forest Type (HR) https://land.copernicus.eu/en/products/high-resolution-layer-forests-and-tree-cover/forest-type-2021-raster-10-m-100-m-europe-3-yearly
// effis : real-time updated Burnt Areas database from effis 
// kosovo : humanitarian data exchange shape file

var target_crs = 'EPSG:32634'
//print('Forest Type properties:', forest_type); // band "b1" holds tree type labels

print("Forest Type resolution", forest_type.projection().nominalScale())
var forest_type_res = forest_type.projection().nominalScale()
//////// filtering effis forest fires
var fires_start = '2022-01-01';
var fires_end = '2025-12-31';


// cut kosovo from effis filtered date
var effis_kosvo = effis.filterBounds(kosovo).filter(ee.Filter.gte('FIREDATE', fires_start))
  .filter(ee.Filter.lte('FIREDATE', fires_end));;

var kosovo_geom = kosovo.geometry();

//effis - kosovo intersection
var kosovo_burns = effis_kosvo.map(function(feature) {
  return feature.intersection(kosovo.geometry(), ee.ErrorMargin(1));
});



// remove null geometries (features that don't actually intersect)
var kosovo_burns_clean = kosovo_burns.filter(ee.Filter.notNull(['.geo'])).map(function(feature) {
                                    //geometry => true geometric area
                                    var areaHectares = feature.geometry().area({maxError: 1}).divide(10000);
                                    return feature.set('area_hectares', areaHectares);
                                  });



var kosovo_burns_dissolved = kosovo_burns.union();
var totalAreaNoOverlap = kosovo_burns_dissolved.geometry().area({maxError: 1}).divide(10000);




Map.addLayer(kosovo, {color: 'blue', crs: target_crs}, 'Kosovo Boundary');
Map.centerObject(kosovo, 7);




var totalAreaWithOverlaps = kosovo_burns_clean.aggregate_sum('area_hectares');
print('Total EFFIS burned area WITH overlaps (hectares):', totalAreaWithOverlaps);
print('Total EFFIS burned area WITHOUT overlaps (hectares):', totalAreaNoOverlap);


///////////////////////////////////////////////////////////////////////////////////////////

var forests_filtered = forest_type.eq(1).or(forest_type.eq(2));
var forest_mask = forest_type.updateMask(forests_filtered);
var vis = {
  palette: ['00FF00']  // green
};

Map.addLayer(forest_mask, vis, 'HR Forest Type Forests');






var kosovo_burns_with_forest = kosovo_burns_clean.map(function(feature) {
  var burnArea = feature.get('area_hectares');
  
  // forest area within this burn polygon
  var forestInBurn = forest_mask.clip(feature.geometry());
  var forestAreaPixels = forestInBurn.reduceRegion({
    reducer: ee.Reducer.count(),
    geometry: feature.geometry(),
    scale: forest_type_res,
    maxPixels: 1e9
  });
  
  // 10m pixels = 100 m² = 0.01 hectare per pixel
  var forestAreaHectares = ee.Number(forestAreaPixels.get('b1')).multiply(0.01);
  
  return feature.set({
    'forest_area_hectares': forestAreaHectares,
    'non_forest_area_hectares': ee.Number(burnArea).subtract(forestAreaHectares)
  });
});






var totalForestBurnArea = kosovo_burns_with_forest.aggregate_sum('forest_area_hectares');



print('Total forest burn area (hectares)  with HRFT forest label:', totalForestBurnArea);




//no overlaps
var forestInDissolvedBurns = forest_mask.clip(kosovo_burns_dissolved.geometry());

var forestAreaPixels = forestInDissolvedBurns.reduceRegion({
  reducer: ee.Reducer.count(),
  geometry: kosovo_burns_dissolved.geometry(),
  scale: forest_type_res,
  maxPixels: 1e9
});

var totalForestBurnAreaNoOverlap = ee.Number(forestAreaPixels.get('b1')).multiply(0.01);

print('Total forest burn area WITHOUT overlaps (hectares) with HRFT forest label:', totalForestBurnAreaNoOverlap);




