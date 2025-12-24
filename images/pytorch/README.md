# Gnosys PyTorch Container Image

This is a Fedora based Linux container image that installs pytorch with DNF and has a small test script to ensure
pytorch is properly working (very basic, more of a sanity test).

The test script is based on the following source code: https://github.com/rasbt/stat453-deep-learning-ss21/blob/main/L08/code/cross-entropy-pytorch.ipynb

## Building the Image

The Containerfile uses an `IMG` build argument that defines which base image to use. The reason for doing so is to easily
switch to different flavors (base fedora image, centos, toolbox, etc).

The following command builds a pytorch image using Fedora as its base image:

```
$ podman build -t localhost/pytorch:latest .
```

Now, let's say we also want an image that can be used with [Toolbox](https://containertoolbx.org/):

```
$ podman build --build-arg IMG=quay.io/fedora/fedora-toolbox:43 -t localhost/pytorch-box:latest .
$ toolbox create --image localhost/pytorch-box:latest pytorch-box
$ toolbox enter pytorch-box
```

It should work with any image, given that:

* It has RPM support and `dnf` can be used to install RPMs
* A `python3-torch` RPM package is available
