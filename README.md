[Japanese](README_ja.md)/ English

# Low-rank approximation of Image with Singular-Value-Decomposition

## Summary

Performs low-rank approximation of a given image. It produces color and grayscale versions simultaneously.

## Usage

```
$ python image_svd.py filename rank
```

## Example

```
$ python image_svd.py stop.jpg 10
Saved as stop_r10_mono.jpg
Saved as stop_r10.jpg
```

Input image (Original)

![stop.jpg](stop.jpg)

Grayscale image (Converted from original image)

![stop.jpg](stop_mono.jpg)


Approximated image (Grayscale, Rank=10)

![stop_r10_mono.jpg](stop_r10_mono.jpg)

Approximated image (Color, Rank=10)

![stop_r10.jpg](stop_r10.jpg)

Approximated image (Color, HOSVD, Rank=30)

![stop_r10.jpg](stop_t10.jpg)
