/* hero background video: muted YouTube loop; only visible while it really plays, photos stay as fallback.
   Whenever YouTube would show its own UI (paused, buffering, ended, play button), the video fades out. */
if (!matchMedia('(prefers-reduced-motion: reduce)').matches && innerWidth > 700) {
  window.onYouTubeIframeAPIReady = () => {
    const v = document.getElementById('vid');
    let showT = null, loopT = null, p = null;
    const hide = () => { clearTimeout(showT); showT = null; v.classList.remove('on'); };
    const show = () => { if (!showT && !v.classList.contains('on')) showT = setTimeout(() => { showT = null; v.classList.add('on'); }, 1200); };
    p = new YT.Player('yt', {videoId: '{{VIDEO}}',
      playerVars: {autoplay:1, mute:1, controls:0, loop:1, playlist:'{{VIDEO}}', start:{{VIDEO_START}}, playsinline:1, rel:0, origin: location.origin, modestbranding:1, iv_load_policy:3, disablekb:1, fs:0},
      events: {
        onReady: e => { e.target.mute(); e.target.playVideo();
          /* jump back before the end so YouTube never shows its end screen or replay button */
          loopT = setInterval(() => { try { const d = p.getDuration(), t = p.getCurrentTime();
            if (d && t > d - 2.5) { hide(); p.seekTo({{VIDEO_START}}, true); } } catch (_) {} }, 500); },
        onStateChange: e => { if (e.data === 1) show(); else hide(); if (e.data === 0) { p.seekTo({{VIDEO_START}}, true); p.playVideo(); } },
        onError: () => { clearInterval(loopT); v.remove(); }}});
    document.addEventListener('visibilitychange', () => { if (!document.hidden && p && p.playVideo) p.playVideo(); });
  };
  const s = document.createElement('script'); s.src = 'https://www.youtube.com/iframe_api'; document.body.appendChild(s);
}
