(function () {
  "use strict";

  function pad2(n) {
    return String(n).padStart(2, "0");
  }

  function makeTrackTitle(n, titles) {
    if (titles && titles[n]) {
      return pad2(n) + ". " + titles[n];
    }
    return "Track " + pad2(n);
  }

  function makeTrackUrl(repo, branch, albumFolder, filePrefix, n) {
    var file = filePrefix + pad2(n) + ".mp3";
    return (
      "https://media.githubusercontent.com/media/" +
      repo +
      "/" + branch + "/series/CCAG/" +
      encodeURIComponent(albumFolder) +
      "/assets/mp3/" +
      encodeURIComponent(file)
    );
  }

  function makeCoverUrl(repo, branch, albumFolder, coverFile) {
    return (
      "https://media.githubusercontent.com/media/" +
      repo +
      "/" + branch + "/series/CCAG/" +
      encodeURIComponent(albumFolder) +
      "/assets/cover/" +
      encodeURIComponent(coverFile)
    );
  }

  function buildTracks(cfg) {
    return cfg.trackNumbers.map(function (n) {
      return {
        no: n,
        title: makeTrackTitle(n, cfg.trackTitles || {}),
        url: makeTrackUrl(cfg.repo, cfg.branches[0], cfg.albumFolder, cfg.filePrefix, n),
      };
    });
  }

  function init() {
    var cfg = window.CCAG_PLAYER_CONFIG;
    if (!cfg) return;

    var tracks = buildTracks(cfg);
    var audio = document.getElementById("audio");
    var now = document.getElementById("nowPlaying");
    var list = document.getElementById("trackList");
    var prev = document.getElementById("prevBtn");
    var next = document.getElementById("nextBtn");
    var play = document.getElementById("playBtn");
    var coverWrap = document.getElementById("coverWrap");
    var coverImage = document.getElementById("coverImage");
    var index = 0;
    var branchIndex = 0;

    function setActiveButton() {
      Array.prototype.forEach.call(list.querySelectorAll(".track-btn"), function (btn, i) {
        btn.classList.toggle("active", i === index);
      });
    }

    function loadTrack(i, autoplay) {
      index = i;
      var t = tracks[index];
      branchIndex = 0;
      audio.src = t.url;
      now.textContent = "Now Playing: " + t.title;
      setActiveButton();
      if (autoplay) {
        audio.play().catch(function () {});
      }
    }

    function move(step, autoplay) {
      var nextIndex = index + step;
      if (nextIndex < 0) nextIndex = tracks.length - 1;
      if (nextIndex >= tracks.length) nextIndex = 0;
      loadTrack(nextIndex, autoplay);
    }

    tracks.forEach(function (t, i) {
      var li = document.createElement("li");
      li.className = "track";
      var btn = document.createElement("button");
      btn.className = "track-btn";
      btn.textContent = t.title;
      btn.addEventListener("click", function () {
        loadTrack(i, true);
      });
      li.appendChild(btn);
      list.appendChild(li);
    });

    prev.addEventListener("click", function () {
      move(-1, true);
    });
    next.addEventListener("click", function () {
      move(1, true);
    });
    play.addEventListener("click", function () {
      audio.play().catch(function () {});
    });

    audio.addEventListener("ended", function () {
      move(1, true);
    });

    audio.addEventListener("error", function () {
      var branches = cfg.branches || ["main", "master"];
      if (branchIndex + 1 >= branches.length) return;
      branchIndex += 1;
      var b = branches[branchIndex];
      var t = tracks[index];
      audio.src = makeTrackUrl(cfg.repo, b, cfg.albumFolder, cfg.filePrefix, t.no);
      audio.play().catch(function () {});
    });

    if (coverWrap && coverImage) {
      var coverFile = cfg.coverFile;
      if (!coverFile) {
        coverWrap.style.display = "none";
      } else {
        var coverBranchIndex = 0;
        var coverBranches = cfg.branches || ["main", "master"];

        function loadCover() {
          coverImage.src = makeCoverUrl(
            cfg.repo,
            coverBranches[coverBranchIndex],
            cfg.albumFolder,
            coverFile
          );
        }

        coverImage.addEventListener("error", function () {
          if (coverBranchIndex + 1 >= coverBranches.length) {
            coverWrap.style.display = "none";
            return;
          }
          coverBranchIndex += 1;
          loadCover();
        });

        loadCover();
      }
    }

    loadTrack(0, false);
  }

  document.addEventListener("DOMContentLoaded", init);
})();
