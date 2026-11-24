/* hero background video: muted YouTube loop; only visible while the picture really moves, photos stay as fallback.
   A watchdog checks every 100 ms that playback time advances. As soon as it stalls (pause, buffering spinner,
   play button, end screen) the video is hidden at once; it fades back in after 1.5 s of smooth playback. */
if (!matchMedia('(prefers-reduced-motion: reduce)').matches && innerWidth > 700) {
  window.onYouTubeIframeAPIReady = () => {
    const v = document.getElementById('vid');
    let p = null, last = -1, lastMove = 0, firstMove = 0, dog = null, seeking = false;
    const START = {{VIDEO_START}};
    const tick = () => {
      let t, d, s;
      try { t = p.getCurrentTime(); d = p.getDuration(); s = p.getPlayerState(); } catch (_) { return; }
      const now = Date.now();
      if (s === 1 && t > last + 0.01) { if (!firstMove) firstMove = now; lastMove = now; }
      last = t;
      const moving = s === 1 && now - lastMove < 450;
      if (d && t > d - 3) { if (!seeking) { seeking = true; v.classList.remove('on'); firstMove = 0; setTimeout(() => { p.seekTo(START, true); last = -1; seeking = false; }, 400); } return; }
      if (seeking) return;
      if (moving) { if (firstMove && now - firstMove >= 1500) v.classList.add('on'); }
      else { firstMove = 0; v.classList.remove('on'); if (s !== 1 && s !== 3 && !document.hidden) p.playVideo(); }
    };
    p = new YT.Player('yt', {videoId: '{{VIDEO}}',
      playerVars: {autoplay:1, mute:1, controls:0, loop:1, playlist:'{{VIDEO}}', start:START, playsinline:1, rel:0, origin: location.origin, modestbranding:1, iv_load_policy:3, disablekb:1, fs:0},
      events: {
        onReady: e => { e.target.mute(); e.target.playVideo(); dog = setInterval(tick, 100); },
        onStateChange: e => { if (e.data !== 1) { firstMove = 0; v.classList.remove('on'); } },
        onError: () => { clearInterval(dog); v.remove(); }}});
  };
  const s = document.createElement('script'); s.src = 'https://www.youtube.com/iframe_api'; document.body.appendChild(s);
}
