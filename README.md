### fan

A movie compilation and playback app for Windows. Fast. Lean. No weather widget.

**Download EXE for Windows 7/8:**  
[fan &raquo; Releases &raquo; 0.13.1.1]

[![YouTube video](https://raw.githubusercontent.com/nikola/fan/master/screenshots/screencap.png)](https://www.youtube.com/watch?v=d78GJJeES3c)

**Key features:**

* Browse your movie compilation in a highly interactive, fluid grid view, or switch to the detail browser with additional information about each movie.
* Find and access movies with hotkeys. Sort by title, rating, release year, budget, and more. Show the English title, or switch to the original title on-the-fly. *(Support for more UI languages coming soon!)*
* Watch YouTube trailers for each movie within _fan_, no separate browser needed.
* _fan_ automagically:
    * scans one or more drives for MKV movie files, and imports metadata, posters and backdrops from [The Movie Database (TMDb)], the #1 source for up-to-date movie information and artwork.
    * downscales poster artwork from the original full-resolution images at ultra-high quality (using [EWA RobidouxSharp])
    * detects when a movie belongs to a collection, and displays collections as expandable grids for a very compact overview of vast movie libraries.
    * installs best-of-breed third-party software for high-quality playback: [MPC-HC], [madVR] and [LAV Filters] \(not bundled with _fan_\).
    * calculates primary colors of poster images for artistic coherence in the UI (using a very fast, multithreaded [implementation] of [MMCQ], <25ms for a 350x500px poster)

**License:**  
[GPL v2]

**Documentation:**  
[fan &raquo; Wiki]

**FAQ:**  
[fan &raquo; Wiki &raquo; FAQ]

**Requirements:**

* Windows Vista, Windows 7 or Windows 8/8.1, 32-bit or 64-bit.
* Screen resolution of 1920x1080 (Full HD).

**Screenshots:**

[![Screenshot: Movie grid](https://raw.githubusercontent.com/nikola/fan/master/screenshots/movie-grid-thumb.png)](https://raw.githubusercontent.com/nikola/fan/master/screenshots/movie-grid.png)
  
[![Screenshot: Movie compilation](https://raw.githubusercontent.com/nikola/fan/master/screenshots/compilation-thumb.png)](https://raw.githubusercontent.com/nikola/fan/master/screenshots/compilation.png)
  
[![Screenshot: Detail browser](https://raw.githubusercontent.com/nikola/fan/master/screenshots/detail-browser-thumb.png)](https://raw.githubusercontent.com/nikola/fan/master/screenshots/detail-browser.png)
  
[![Screenshot: Movie detail](https://raw.githubusercontent.com/nikola/fan/master/screenshots/movie-detail-thumb.png)](https://raw.githubusercontent.com/nikola/fan/master/screenshots/movie-detail.png)
  
[![Screenshot: Menu](https://raw.githubusercontent.com/nikola/fan/master/screenshots/menu-thumb.png)](https://raw.githubusercontent.com/nikola/fan/master/screenshots/menu.png)

---

**Copyright 2013-2014 Nikola Klaric.**

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

[See it in action!]:https://www.youtube.com/watch?v=d78GJJeES3c
[GPL v2]:http://www.gnu.org/licenses/gpl-2.0.html
[The Movie Database (TMDb)]:http://www.themoviedb.org/
[MPC-HC]:http://mpc-hc.org/
[LAV Filters]:https://github.com/Nevcairiel/LAVFilters
[madVR]:http://madshi.net/
[EWA RobidouxSharp]:http://www.imagemagick.org/Usage/filter/nicolas/#downsample
[implementation]:https://github.com/nikola/MMCQ.js
[MMCQ]:http://www.leptonica.com/papers/mediancut.pdf
[fan &raquo; Releases &raquo; 0.13.1.1]:https://github.com/nikola/fan/releases/tag/v0.13.1.1
[fan &raquo; Wiki]:https://github.com/nikola/fan/wiki
[fan &raquo; Wiki &raquo; FAQ]:https://github.com/nikola/fan/wiki/FAQ
