# EmulationStation to RetroArch playlists converter

This is a collection of scripts for converting EmulationStation gamelist.xml to RetroArch playlists. Works on Windows and Linux.

## Usage

es-to-retroarch-playlists.py
```
usage: es-to-retroarch-playlists.py [-h] [-folder FOLDER] [-subfolders] [-favonly] [-includehidden] [-checkfiles] [-crc32] [-basepath BASEPATH] [-dbname DBNAME] [-copypics FIELD DIR] [-header JSON]
                                    gamelist.xml output.lpl

Convert EmulationStation gamelist.xml to RetroArch playlists.

positional arguments:
  gamelist.xml         name of input file in EmulationStation gamelist.xml format
  output.lpl           name of file to be created in RetroArch playlist .lpl format

options:
  -h, --help           show this help message and exit
  -folder FOLDER       only include games in folder FOLDER
  -subfolders          include games in subfolders
  -favonly             only include games marked as favorites
  -includehidden       include games marked as hidden
  -checkfiles          only include game files that are present (check is always done in working directory)
  -crc32               calculate CRC32 of game files
  -basepath BASEPATH   use BASEPATH instead of working directory for paths to games in the output file
  -dbname DBNAME       include db_name field with value DBNAME in the output file
  -copypics FIELD DIR  copy pictures/videos from gamelist.xml field FIELD (e.g. image) to directory DIR
  -header JSON         place JSON in header of output.lpl
```

jpeg-to-png.py
```
usage: jpeg-to-png.py [-h] input.jpg [input.jpg ...]

Convert JPEG images to PNG.

positional arguments:
  input.jpg   names of input files in JPEG format, supports glob syntax

options:
  -h, --help  show this help message and exit
```

## Examples

On Windows for RetroArch on Windows:
```
es-to-retroarch-playlists.py -folder "NESDev19" -subfolders -checkfiles -crc32 -basepath C:\retroarch\roms\nes -dbname "Nintendo - Nintendo Entertainment System.lpl" -copypics image "C:\\retroarch\\thumbnails\\Nintendo - Nintendo Entertainment System\\Named_Titles" -header "{ ""default_core_path"": ""C:\\retroarch\\cores\\fceumm_libretro.dll"", ""default_core_name"": ""Nintendo - NES / Famicom (FCEUmm)"" }" gamelist.xml C:\retroarch\playlists\NESDev19.lpl
```

On Linux for RetroArch on Linux:
```
es-to-retroarch-playlists.py -folder "NESDev19" -subfolders -checkfiles -crc32 -basepath /home/gamer/retroarch/roms/nes -dbname "Nintendo - Nintendo Entertainment System.lpl" -copypics image "/home/gamer/retroarch/thumbnails/Nintendo - Nintendo Entertainment System/Named_Titles" -header '{ "default_core_path": "/home/gamer/retroarch/cores/fceumm_libretro.so", "default_core_name": "Nintendo - NES / Famicom (FCEUmm)" }' gamelist.xml /home/gamer/retroarch/playlists/NESDev19.lpl
```

On Linux for RetroArch on Windows:
```
es-to-retroarch-playlists.py -folder "NESDev19" -subfolders -checkfiles -crc32 -basepath C:\\retroarch\\roms\\nes -dbname "Nintendo - Nintendo Entertainment System.lpl" -copypics image /tmp/thumbs/nes -header '{ "default_core_path": "C:\\retroarch\\cores\\fceumm_libretro.dll", "default_core_name": "Nintendo - NES / Famicom (FCEUmm)" }' gamelist.xml /tmp/NESDev19.lpl
```

On Windows and Linux:
```
jpeg-to-png.py *.jpg
```

## References

- For list of possible `-dbname` values that are also in image folder names, see [here](https://github.com/libretro/libretro-database/tree/master/rdb). In `-dbname` the `.rdb` extension must be replaced with `.lpl`. In image folder names the `.rdb` extension must be removed.
- Core file names depend on platform. Here are file names for [Linux 64-bit](https://buildbot.libretro.com/nightly/linux/x86_64/latest/), [Windows 64-bit](https://buildbot.libretro.com/nightly/windows/x86_64/latest/) and [Android 64-bit](https://buildbot.libretro.com/nightly/android/latest/arm64-v8a/). The `.zip` extension must be removed.
- For values of `default_core_name` header, see `display_name` field in [core info files](https://github.com/libretro/libretro-core-info/tree/master).
