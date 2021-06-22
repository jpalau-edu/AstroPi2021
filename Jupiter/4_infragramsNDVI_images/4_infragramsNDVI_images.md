## NDVI calculations

In order to highlight water surfaces we then performed NDVI analysis on the selected images with the on-line tool INFRAGRAM by Public Lab.
>https://infragram.org/


NDVI (Normalized Difference Vegetation Index) takes advantage of the fact that healthy vegetation mostly absorbs blue and red light and reflects green and infrared. A camera that doesn't block IR, fitted with a blue filter that gets rid of green light, let us examine the ratio between blue and IR amounts, thus sorting areas according to photosynthetic activity. In that regard, water bodies should stand out against their surroundings.


On those selected images we used the INFRAGRAM tool, which performs NDVI calculation on every pixel and returns an image that can be either greyscale or false colored. NDVI formula is 

<img src="https://render.githubusercontent.com/render/math?math=\large NDVI=\frac{NIR - B}{NIR + B}">

but Infragam allows for some fine-tunning  
>https://publiclab.org/wiki/infragram-sandbox

so we made this change
<img src="https://render.githubusercontent.com/render/math?math=\large NDVI=\frac{NIR - B}{NIR + B}">

