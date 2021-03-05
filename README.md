# Symgrate2 Plugin (v1.0.0)
Author: atlas
Affiliation: GRIMM (SMFS)

_This is a client plugin for recovering symbols using the Symgrate2 server._

## Description:

Symgrate2 is a symbol recovery database with a publicly query-able
sever.  This client exposes two modes, one that checks a single
function and another that runs through every function of the current
project, querying the server and printing the names of
matches.

![](https://github.com/vivisect/plugin-symgrate2/blob/master/images/symgrate2.png?raw=true)


## Installation Instructions

### Linux, Darwin, Windows

Copy (or symlink) this directory into an appropriate Vivisect
Extensions directory (in the path indicated by your `$VIV_EXT_PATH`
environment variable) Vivisect will load on next start of the GUI.


## Minimum Version

This plugin requires the following minimum version of Vivisect:

* v1.0.0



## Required Dependencies

The following dependencies are required for this plugin:

* python requests library

```
$ python3 -m pip install requests
```


## License

This plugin is released under a MIT license.

## Metadata Version

2
