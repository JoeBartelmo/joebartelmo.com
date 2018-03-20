---
title: "Understanding 3D `Mat::at<T>` Accessors with OpenCV 3.4"
categories:
  - computer_vision
tags:
  - c++
  - c
  - opencv
  - opencv3.4
  - accessor
  - vision
  - computer vision
toc: true
toc_label: "Table of Contents"
toc_icon: "cog"
---
Some things simply do not come naturally when we attempt to process data in OpenCV. In this article we're going to focus on using `at<T>` in three dimensions and how I went about figuring out how to use it.

### Background
Ideally in image processing we want to access pixel by pixel information as fast as possible. OpenCV has for loops configured in the backend such that they are roughly 10x faster when iterating by rows first, then columns (tested on 1 HPC cluster and 1 standard laptop). Typically we are all taught to use indexing to access elements as it is the most safe way (eg: `Mat::at<T>(row, col)`). This works find for a matrix that has a single channel, however when we want to access a matrix with multiple channels we need to use our quick math skills.

_Matrix used for reader reference:_

| Bands | Rows  | Columns |
|--|--|--|
| 3 | 1 | 256 |


**Note:** that for this article, we are under the assumption that the `cv::Vec3b` is unacceptable when programming a solution because you are attempting to work around dynamic channels/bands.

### Naive Solutions
_Naive solution to indexing into a multi-dimensional matrix_
```c++
cv::Mat img = //process somehow
for (unsigned int band = 0; band < img.channels(); band++) {
	for (unsigned int row = 0; row < img.rows; row++) {
		for (unsigned int col = band;
			 col < img.cols * img.channels();
			 col += img.channels()) {
			//process pixel:
			img.at<double>(row, col)
		}
	}
}
```
Or, alternatively split the matrix and access:
```c++
cv::Mat img = //process somehow
std::vector<cv::Mat> bands;
cv::split(img, bands);
for (cv::Mat& band : bands) {
	for (unsigned int row = 0; row < img.rows; row++) {
		for (unsigned int col = 0; col < img.cols; col++) {
			//process pixel:
			band.at<double>(row, col)
		}
	}
}
```

### Incorrect Attempts and Finding a Solution
I think for most cases the above will perform fine, and you will not have an immense decrease in performance (though this remains untested). However I did some digging and found the little known `at<T>(i, j, k)` which supposedly processes the image as though there are 3 dimensions present. According to CV Docs:

> This is an overloaded member function, provided for convenience. It differs from the above function only in what argument(s) it accepts.
>
>Parameters
>
>i0: Index along the dimension 0
>
>i1: Index along the dimension 1
>
>i2: Index along the dimension 2

Although there are no instances in the documentation of its use, so i figure we are meant to use it with the band as the third dimensional, like so:

_Incorrect Accessing_

```c++
cv::Mat img = //process somehow
for (unsigned int band = 0; band < img.channels(); band++) {
	for (unsigned int row = 0; row < img.rows; row++) {
		for (unsigned int col = 0; col < img.cols; col++) {
			//process pixel:
			img.at<double>(row, col, band);
		}
	}
}
```

The above will through a segmentation fault if there is more than 1 band present. So the ordering here is incorrect, our assumption because of the matrix I am using (see above) is that the last index is the row, because we have only 1 row in this matrix. 

My life is wonderful. Let's try reordering: `img.at<double>(band, col, row);` This will compile and run successfully, but gives us complete garbage beyond the first band. We ended up with abstractly large double floating points, It turns out that we have the following layout for our dimensions:

_Matrix Information_

| Bands | Rows  | Columns |
|--|--|--|
| 3 | 1 | 256 |

_at(i0, i1) accessor output_

| i0 | i1  |
|--|--|--|
| 1 | 256 * 3 |

_at(i0, i1, i2) accessor output_

| i0 | i1  | i2 |
|--|--|--|
| 18 | 4422 | 1 |

Huh, well that's kinda horribly awkward. Did some more playing around with this and I found that `i1` is dependent on `i0`. The higher `i0` is the fewer numbers we have available in `i1`, `i2` is unaffected. They are linearly related by a subtraction of 256 in size except for the last index for `i0` (in this case 17). Which means that the extra X bands i found and the extra X columns i found are also garbage.

Freaking Fantastic. So all we know so far is that our 0th band is correct, we have to find out how to get bands 1 and 2.  
### Digging Intensifies and Saddens
After staring at this data for an increasingly depressing amount of time, I determined that only the first dimension is stored in this data buffer we are observing. Meaning that our channels are not contiguous. It appears that the rest of this data is garbage. I was unable to do any bit twiddling or engineering to determine the original data from the source. So, let's look into how we can get the proper references to the real data.

Defeated, I decided to look at their source code [here](https://github.com/opencv/opencv/blob/379ea15d1664a37a2f8851ce00e5feb8ce5b8d8d/modules/core/include/opencv2/core/mat.inl.hpp#L1175-L1180)
```c++
template<typename _Tp> inline
const _Tp& Mat::at(int i0) const
{
    CV_DbgAssert(dims <= 2);
    CV_DbgAssert(data);
    CV_DbgAssert((unsigned)i0 < (unsigned)(size.p[0] * size.p[1]));
    CV_DbgAssert(elemSize() == sizeof(_Tp));
    if( isContinuous() || size.p[0] == 1 )
        return ((const _Tp*)data)[i0];
    if( size.p[1] == 1 )
        return *(const _Tp*)(data + step.p[0] * i0);
    int i = i0 / cols, j = i0 - i * cols;
    return ((const _Tp*)(data + step.p[0] * i))[j];
}

template<typename _Tp> inline
_Tp& Mat::at(int i0, int i1)
{
    CV_DbgAssert(dims <= 2);
    CV_DbgAssert(data);
    CV_DbgAssert((unsigned)i0 < (unsigned)size.p[0]);
    CV_DbgAssert((unsigned)(i1 * DataType<_Tp>::channels) < (unsigned)(size.p[1] * channels()));
    CV_DbgAssert(CV_ELEM_SIZE1(traits::Depth<_Tp>::value) == elemSize1());
    return ((_Tp*)(data + step.p[0] * i0))[i1];
}

template<typename _Tp> inline
_Tp& Mat::at(int i0, int i1, int i2)
{
    CV_DbgAssert( elemSize() == sizeof(_Tp) );
    return *(_Tp*)ptr(i0, i1, i2);
}
```

Let's take a look at the immense implementation differences between `at(i0)`, `at(i0,i1)` and `at(i0,i1,i2)`. Look past the obscure OpenCV debug assertions and take a look at the math to compute the point we are referencing. We're simply accessing at the ptr which looks to be a reference to [this](https://github.com/opencv/opencv/blob/66f3c1ae79030ab3cd36add4246a97f92920af84/modules/core/include/opencv2/core/mat.hpp#L2811-L2812) line of code linking to [this](https://github.com/opencv/opencv/blob/379ea15d1664a37a2f8851ce00e5feb8ce5b8d8d/modules/core/include/opencv2/core/mat.inl.hpp#L1002-L1010) block of code
```c++
(_Tp*)(data + i0 * step.p[0] + i1 * step.p[1] + i2 * step.p[2]);
```
Fantastic. ~~Please end me~~. Now let's  ~~Guess and check to find the answer~~ figure out this scary math that requires knowledge of OpenCV's internals.

We can derive that the math is identical for `at(i0, i1)` take a look at the similarity:
2d: `((_Tp*)(data + step.p[0] * i0))[i1]`
3d: `(_Tp*)(data + i0 * step.p[0] + i1 * step.p[1] + i2 * step.p[2])`

So it's completely dependent on the step size, **our original incorrect ordering (row, col, band) is actually correct** but we have an incorrect answer here. Let's take a look at the step sizes:

| p[0] | p[1] | p[2] |
|--|--|--|
| 6144 | 24 | 9223372036854775808 |

Well, from our Naive approach, that p[2] is wildly incorrect. Almost looks like unallocated space that someone left to play with me.

I added the line `step.p[2] = sizeof(double);` and wouldn't you know it, worked fine. Does this mean that OpenCV is not assigning the step size properly?

### Result
```c++
lut.step.p[2] = sizeof(double);  
for (unsigned int band = 0; band < lut.channels(); band++) {  
    for (unsigned int row = 0; row < lut.rows; row++) {  
        for (unsigned int col = 0; col < lut.cols; col++) {  
            lut.at<double>(row, col, band);  
        }  
    }  
}
```
**Note:** It's possible that the above solution is improper, if you're paranoid use one of the naive solutions, i will follow up with the OpenCV team to see if this is a possible bug.

### Lesson's Learned

* Never trust open source documentation
* If you can look at the source code first
* Try not to hate yourself


