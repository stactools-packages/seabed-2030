# stactools-seabed-2030

- Name: seabed-2030
- Package: `stactools.seabed_2030`
- PyPI: https://pypi.org/project/stactools-seabed-2030/
- Dataset homepage: https://seabed2030.org/
- STAC extensions used:
  - [proj](https://github.com/stac-extensions/projection/)
- Extra fields:
  - `seabed-2030:institution`
  - `seabed-2030:source`
  - `seabed-2030:history`
  - `seabed-2030:comment`

**Seabed 2030 General Bathymetric Chart of the Oceans (GEBCO) Grid**
GEBCO's gridded bathymetric datasets are a global terrain model for ocean and land, providing elevation data, in meters, on a 15 arc-second interval grid.

### Command-line usage

Description of the command line functions

```bash
$ stac seabed-2030 create-collection destination.json
$ stac seabed-2030 create-cog source.nc cog_href.tif
$ stac seabed-2030 create-item source.ns destination.json cog_href.tif
```

Use `stac seabed-2030 --help` to see all subcommands and options.
