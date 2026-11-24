/* hero background video: muted YouTube loop; only shown once it really plays, photos stay as fallback */
if (!matchMedia('(prefers-reduced-motion: reduce)').matches && innerWidth > 700) {
  window.onYouTubeIframeAPIReady = () => {
    const v = document.getElementById('vid');
    new YT.Player('yt', {videoId: '{{VIDEO}}',
      playerVars: {autoplay:1, mute:1, controls:0, loop:1, playlist:'{{VIDEO}}', start:{{VIDEO_START}}, playsinline:1, rel:0, origin: location.origin, modestbranding:1, iv_load_policy:3, disablekb:1, fs:0},
      events: {onReady: e => { e.target.mute(); e.target.playVideo(); },
               onStateChange: e => { if (e.data === 1) v.classList.add('on'); if (e.data === 0) e.target.seekTo({{VIDEO_START}}); },
               onError: () => v.remove()}});
  };
  const s = document.createElement('script'); s.src = 'https://www.youtube.com/iframe_api'; document.body.appendChild(s);
}
