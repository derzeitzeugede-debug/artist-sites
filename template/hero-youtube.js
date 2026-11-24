/* hero background video: muted YouTube loop; only visible while the picture really moves, photos stay as fallback.
   A watchdog checks every 250 ms that playback time advances. As soon as it stalls (pause, buffering spinner,
   play button, end screen) the video is hidden at once; it fades back in after 1.5 s of smooth playback. */
if (!matchMedia('(prefers-reduced-motion: reduce)').matches && innerWidth > 700) {
  window.onYouTubeIframeAPIReady = () => {
    const v = document.getElementById('vid');
    let p = null, last = -1, smooth = 0, dog = null;
    const START = {{VIDEO_START}};
    const tick = () => {
      let t, d, s;
      try { t = p.getCurrentTime(); d = p.getDuration(); s = p.getPlayerState(); } catch (_) { return; }
      const moving = s === 1 && t > last + 0.05;
      last = t;
      if (d && t > d - 3) { v.classList.remove('on'); smooth = 0; p.seekTo(START, true); last = -1; return; }
      if (moving) { smooth += 250; if (smooth >= 1500) v.classList.add('on'); }
      else { smooth = 0; v.classList.remove('on'); if (s !== 1 && s !== 3 && !document.hidden) p.playVideo(); }
    };
    p = new YT.Player('yt', {videoId: '{{VIDEO}}',
      playerVars: {autoplay:1, mute:1, controls:0, loop:1, playlist:'{{VIDEO}}', start:START, playsinline:1, rel:0, origin: location.origin, modestbranding:1, iv_load_policy:3, disablekb:1, fs:0},
      events: {
        onReady: e => { e.target.mute(); e.target.playVideo(); dog = setInterval(tick, 250); },
        onStateChange: e => { if (e.data !== 1) { smooth = 0; v.classList.remove('on'); } },
        onError: () => { clearInterval(dog); v.remove(); }}});
  };
  const s = document.createElement('script'); s.src = 'https://www.youtube.com/iframe_api'; document.body.appendChild(s);
}
