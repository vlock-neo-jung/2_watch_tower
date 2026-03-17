# Computational Photography

Computational photography techniques in OpenCV combine image processing algorithms with computational methods to enhance, restore, and manipulate images in sophisticated ways. This module provides tools for inpainting damaged regions, denoising images, seamless cloning, applying artistic effects, and working with High Dynamic Range (HDR) imaging.

## Capabilities

### Inpainting

Image inpainting restores damaged or missing regions of an image using information from surrounding areas.

```python { .api }
cv2.inpaint(src, inpaintMask, inpaintRadius, flags, dst=None) -> dst
```

Restores the selected region in an image using the region neighborhood.

**Parameters:**
- `src` - Input 8-bit, 16-bit unsigned or 32-bit float 1-channel or 8-bit 3-channel image
- `inpaintMask` - Inpainting mask, 8-bit 1-channel image. Non-zero pixels indicate areas to be inpainted
- `inpaintRadius` - Radius of circular neighborhood of each point inpainted
- `flags` - Inpainting method
- `dst` - Output image with the same size and type as src

**Returns:**
- `dst` - Output inpainted image

**Inpainting Methods:**

```python { .api }
cv2.INPAINT_NS       # Navier-Stokes based method
cv2.INPAINT_TELEA    # Fast Marching Method by Telea
```

### Denoising

Non-local means denoising algorithms remove noise while preserving image details and edges.

```python { .api }
cv2.fastNlMeansDenoising(src, h=None, templateWindowSize=None,
                         searchWindowSize=None, dst=None) -> dst
```

Performs image denoising using Non-local Means Denoising algorithm.

**Parameters:**
- `src` - Input 8-bit 1-channel, 2-channel, 3-channel or 4-channel image
- `h` - Filter strength. Higher h value removes more noise but also removes image details (10 is recommended)
- `templateWindowSize` - Size in pixels of template patch (should be odd, default 7)
- `searchWindowSize` - Size in pixels of area used to compute weighted average (should be odd, default 21)
- `dst` - Output image with the same size and type as src

**Returns:**
- `dst` - Output denoised image

```python { .api }
cv2.fastNlMeansDenoisingColored(src, h=None, hColor=None,
                                templateWindowSize=None,
                                searchWindowSize=None, dst=None) -> dst
```

Modification of fastNlMeansDenoising function for colored images.

**Parameters:**
- `src` - Input 8-bit 3-channel image
- `h` - Filter strength for luminance component (10 is recommended)
- `hColor` - Filter strength for color components (10 is recommended)
- `templateWindowSize` - Size in pixels of template patch (should be odd, default 7)
- `searchWindowSize` - Size in pixels of area used to compute weighted average (should be odd, default 21)
- `dst` - Output image with the same size and type as src

**Returns:**
- `dst` - Output denoised colored image

```python { .api }
cv2.fastNlMeansDenoisingMulti(srcImgs, imgToDenoiseIndex,
                              temporalWindowSize, h=None,
                              templateWindowSize=None,
                              searchWindowSize=None, dst=None) -> dst
```

Modification of fastNlMeansDenoising function for image sequences where consecutive frames have been captured in a short period of time.

**Parameters:**
- `srcImgs` - Input 8-bit 1-channel, 2-channel, 3-channel or 4-channel images sequence
- `imgToDenoiseIndex` - Target image to denoise index in srcImgs sequence
- `temporalWindowSize` - Number of surrounding images to use for denoising (should be odd)
- `h` - Filter strength (10 is recommended)
- `templateWindowSize` - Size in pixels of template patch (should be odd, default 7)
- `searchWindowSize` - Size in pixels of area used to compute weighted average (should be odd, default 21)
- `dst` - Output image with the same size and type as srcImgs images

**Returns:**
- `dst` - Output denoised image

```python { .api }
cv2.fastNlMeansDenoisingColoredMulti(srcImgs, imgToDenoiseIndex,
                                     temporalWindowSize, h=None,
                                     hColor=None, templateWindowSize=None,
                                     searchWindowSize=None, dst=None) -> dst
```

Modification of fastNlMeansDenoisingMulti function for colored image sequences.

**Parameters:**
- `srcImgs` - Input 8-bit 3-channel images sequence
- `imgToDenoiseIndex` - Target image to denoise index in srcImgs sequence
- `temporalWindowSize` - Number of surrounding images to use for denoising (should be odd)
- `h` - Filter strength for luminance component (10 is recommended)
- `hColor` - Filter strength for color components (10 is recommended)
- `templateWindowSize` - Size in pixels of template patch (should be odd, default 7)
- `searchWindowSize` - Size in pixels of area used to compute weighted average (should be odd, default 21)
- `dst` - Output image with the same size and type as srcImgs images

**Returns:**
- `dst` - Output denoised colored image

```python { .api }
cv2.denoise_TVL1(observations, result, lambda_=None, niters=None) -> result
```

Primal-dual algorithm for Total Variation (TV) L1 denoising.

**Parameters:**
- `observations` - Noisy observations (grayscale or color images)
- `result` - Output denoised image
- `lambda_` - Regularization parameter (default 1.0)
- `niters` - Number of iterations (default 30)

**Returns:**
- `result` - Denoised image

### Seamless Cloning

Seamless cloning techniques blend source images into destination images without visible seams.

```python { .api }
cv2.seamlessClone(src, dst, mask, p, flags, blend=None) -> blend
```

Image editing tasks concern either global changes (color/intensity corrections, filters, deformations) or local changes concerned to a selection. Seamless cloning blends the source image into the destination image.

**Parameters:**
- `src` - Input 8-bit 3-channel image
- `dst` - Input 8-bit 3-channel image
- `mask` - Input 8-bit 1 or 3-channel image
- `p` - Point in dst image where object is placed (center of the cloned region)
- `flags` - Cloning method
- `blend` - Output image with the same size and type as dst

**Returns:**
- `blend` - Output blended image

**Seamless Clone Flags:**

```python { .api }
cv2.NORMAL_CLONE          # The power of the method is fully preserved
cv2.MIXED_CLONE           # Mixing the gradients from both images for best results
cv2.MONOCHROME_TRANSFER   # Monochrome transfer
```

```python { .api }
cv2.colorChange(src, mask, red_mul=None, green_mul=None,
                blue_mul=None, dst=None) -> dst
```

Given an original color image, two differently colored versions of this image can be mixed seamlessly.

**Parameters:**
- `src` - Input 8-bit 3-channel image
- `mask` - Input 8-bit 1 or 3-channel image
- `red_mul` - R-channel multiply factor (default 1.0)
- `green_mul` - G-channel multiply factor (default 1.0)
- `blue_mul` - B-channel multiply factor (default 1.0)
- `dst` - Output image with the same size and type as src

**Returns:**
- `dst` - Output color changed image

```python { .api }
cv2.illuminationChange(src, mask, alpha=None, beta=None, dst=None) -> dst
```

Applying an appropriate non-linear transformation to the gradient field inside the selection and then integrating back with a Poisson solver, modifies locally the apparent illumination of an image.

**Parameters:**
- `src` - Input 8-bit 3-channel image
- `mask` - Input 8-bit 1 or 3-channel image
- `alpha` - Value ranges between 0-2 (default 0.2)
- `beta` - Value ranges between 0-2 (default 0.4)
- `dst` - Output image with the same size and type as src

**Returns:**
- `dst` - Output illumination changed image

```python { .api }
cv2.textureFlattening(src, mask, low_threshold=None,
                      high_threshold=None, kernel_size=None,
                      dst=None) -> dst
```

By retaining only the gradients at edge locations, before integrating with the Poisson solver, one washes out the texture of the selected region, giving its contents a flat aspect.

**Parameters:**
- `src` - Input 8-bit 3-channel image
- `mask` - Input 8-bit 1 or 3-channel image
- `low_threshold` - Range from 0 to 100 (default 30)
- `high_threshold` - Value > 100 (default 45)
- `kernel_size` - The size of the Sobel kernel (default 3)
- `dst` - Output image with the same size and type as src

**Returns:**
- `dst` - Output texture flattened image

### Edge-Preserving Filters

Edge-preserving filters smooth images while maintaining sharp edges.

```python { .api }
cv2.edgePreservingFilter(src, flags=None, sigma_s=None,
                         sigma_r=None, dst=None) -> dst
```

Filtering is the fundamental operation in image and video processing. Edge-preserving smoothing filters are used in many different applications.

**Parameters:**
- `src` - Input 8-bit 3-channel image
- `flags` - Edge preserving filter type
- `sigma_s` - Range between 0 to 200 (default 60)
- `sigma_r` - Range between 0 to 1 (default 0.4)
- `dst` - Output image with the same size and type as src

**Returns:**
- `dst` - Output edge-preserving filtered image

**Edge-Preserving Filter Flags:**

```python { .api }
cv2.RECURS_FILTER     # Recursive filter
cv2.NORMCONV_FILTER   # Normalized convolution filter
```

```python { .api }
cv2.detailEnhance(src, sigma_s=None, sigma_r=None, dst=None) -> dst
```

This filter enhances the details of a particular image.

**Parameters:**
- `src` - Input 8-bit 3-channel image
- `sigma_s` - Range between 0 to 200 (default 10)
- `sigma_r` - Range between 0 to 1 (default 0.15)
- `dst` - Output image with the same size and type as src

**Returns:**
- `dst` - Output detail enhanced image

### Stylization Effects

Non-photorealistic rendering techniques that create artistic effects.

```python { .api }
cv2.pencilSketch(src, sigma_s=None, sigma_r=None,
                 shade_factor=None, dst1=None, dst2=None) -> dst1, dst2
```

Pencil-like non-photorealistic line drawing.

**Parameters:**
- `src` - Input 8-bit 3-channel image
- `sigma_s` - Range between 0 to 200 (default 60)
- `sigma_r` - Range between 0 to 1 (default 0.07)
- `shade_factor` - Range between 0 to 0.1 (default 0.02)
- `dst1` - Output 8-bit 1-channel image (grayscale sketch)
- `dst2` - Output 8-bit 3-channel image (colored sketch)

**Returns:**
- `dst1` - Grayscale pencil sketch
- `dst2` - Colored pencil sketch

```python { .api }
cv2.stylization(src, sigma_s=None, sigma_r=None, dst=None) -> dst
```

Stylization aims to produce digital imagery with a wide variety of effects not focused on photorealism. Edge-aware filters are ideal for stylization, as they abstract regions of low contrast while preserving high-contrast features.

**Parameters:**
- `src` - Input 8-bit 3-channel image
- `sigma_s` - Range between 0 to 200 (default 60)
- `sigma_r` - Range between 0 to 1 (default 0.45)
- `dst` - Output image with the same size and type as src

**Returns:**
- `dst` - Output stylized image

### HDR Imaging

High Dynamic Range (HDR) imaging techniques capture and merge multiple exposures to create images with greater dynamic range.

```python { .api }
cv2.createAlignMTB(max_bits=None, exclude_range=None, cut=None) -> retval
```

Creates AlignMTB object for HDR image alignment using median threshold bitmap.

**Parameters:**
- `max_bits` - Logarithm to base 2 of maximal shift in each dimension (default 6)
- `exclude_range` - Range for exclusion of pixels with big contrast (default 4)
- `cut` - If true, cut images, otherwise fill the new regions with zeros (default True)

**Returns:**
- `retval` - AlignMTB object

```python { .api }
cv2.createCalibrateDebevec(samples=None, lambda_=None,
                           random=None) -> retval
```

Creates CalibrateDebevec object for camera response calibration.

**Parameters:**
- `samples` - Number of pixel locations to use (default 70)
- `lambda_` - Smoothness term weight (default 10.0)
- `random` - Use random sample locations (default False)

**Returns:**
- `retval` - CalibrateDebevec object

```python { .api }
cv2.createCalibrateRobertson(max_iter=None, threshold=None) -> retval
```

Creates CalibrateRobertson object for camera response calibration.

**Parameters:**
- `max_iter` - Maximal number of Gauss-Seidel solver iterations (default 30)
- `threshold` - Target difference between results of two successive steps of the minimization (default 0.01)

**Returns:**
- `retval` - CalibrateRobertson object

```python { .api }
cv2.createMergeDebevec() -> retval
```

Creates MergeDebevec object for merging exposures into HDR image.

**Returns:**
- `retval` - MergeDebevec object

```python { .api }
cv2.createMergeMertens(contrast_weight=None, saturation_weight=None,
                       exposure_weight=None) -> retval
```

Creates MergeMertens object for exposure fusion (without HDR conversion).

**Parameters:**
- `contrast_weight` - Contrast measure weight (default 1.0)
- `saturation_weight` - Saturation measure weight (default 1.0)
- `exposure_weight` - Well-exposedness measure weight (default 0.0)

**Returns:**
- `retval` - MergeMertens object

```python { .api }
cv2.createMergeRobertson() -> retval
```

Creates MergeRobertson object for merging exposures into HDR image.

**Returns:**
- `retval` - MergeRobertson object

### Tone Mapping

Tone mapping operators convert HDR images to displayable low dynamic range (LDR) images.

```python { .api }
cv2.createTonemapDrago(gamma=None, saturation=None,
                       bias=None) -> retval
```

Creates TonemapDrago object for adaptive logarithmic mapping.

**Parameters:**
- `gamma` - Gamma value for gamma correction (default 1.0)
- `saturation` - Saturation enhancement value (default 1.0)
- `bias` - Value for bias function in [0, 1] range (default 0.85)

**Returns:**
- `retval` - TonemapDrago object

```python { .api }
cv2.createTonemapDurand(gamma=None, contrast=None,
                        saturation=None, sigma_space=None,
                        sigma_color=None) -> retval
```

Creates TonemapDurand object for bilateral filtering based tone mapping.

**Parameters:**
- `gamma` - Gamma value for gamma correction (default 1.0)
- `contrast` - Resulting contrast on logarithmic scale (default 4.0)
- `saturation` - Saturation enhancement value (default 1.0)
- `sigma_space` - Spatial sigma for bilateral filter (default 2.0)
- `sigma_color` - Color sigma for bilateral filter (default 2.0)

**Returns:**
- `retval` - TonemapDurand object

```python { .api }
cv2.createTonemapMantiuk(gamma=None, scale=None,
                         saturation=None) -> retval
```

Creates TonemapMantiuk object for gradient domain high dynamic range compression.

**Parameters:**
- `gamma` - Gamma value for gamma correction (default 1.0)
- `scale` - Contrast scale factor (default 0.7)
- `saturation` - Saturation enhancement value (default 1.0)

**Returns:**
- `retval` - TonemapMantiuk object

```python { .api }
cv2.createTonemapReinhard(gamma=None, intensity=None,
                          light_adapt=None, color_adapt=None) -> retval
```

Creates TonemapReinhard object for global tone mapping operator.

**Parameters:**
- `gamma` - Gamma value for gamma correction (default 1.0)
- `intensity` - Result intensity in [-8, 8] range (default 0.0)
- `light_adapt` - Light adaptation in [0, 1] range (default 1.0)
- `color_adapt` - Chromatic adaptation in [0, 1] range (default 0.0)

**Returns:**
- `retval` - TonemapReinhard object

## Additional Functions

```python { .api }
cv2.decolor(src, grayscale=None, color_boost=None) -> grayscale, color_boost
```

Transforms a color image to a grayscale image while preserving contrast and enhancing details.

**Parameters:**
- `src` - Input 8-bit 3-channel image
- `grayscale` - Output 8-bit 1-channel grayscale image
- `color_boost` - Output 8-bit 3-channel contrast-enhanced color image

**Returns:**
- `grayscale` - Grayscale output with enhanced contrast
- `color_boost` - Contrast-enhanced color output
