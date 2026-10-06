(() => {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)');
  const film = document.querySelector('#hero-film');
  const toggle = document.querySelector('.motion-toggle');
  let userPaused = false;
  let playbackRequest = 0;
  const allowed = () => !reduce.matches && !navigator.connection?.saveData && !userPaused;
  function label() { toggle.textContent = film.paused ? 'Reproducir animación' : 'Pausar animación'; toggle.setAttribute('aria-label', toggle.textContent); }
  async function play(explicit = false) {
    if (!explicit && !allowed()) return;
    const request = ++playbackRequest;
    if (!film.src) film.src = film.dataset.src;
    try { await film.play(); if (request !== playbackRequest || userPaused || document.hidden) { film.pause(); } else film.classList.add('playing'); } catch { film.classList.remove('playing'); }
    label();
  }
  if (film && toggle) {
    toggle.hidden = false;
    toggle.addEventListener('click', () => { if (film.paused) { userPaused = false; play(true); } else { userPaused = true; ++playbackRequest; film.pause(); label(); } });
    film.addEventListener('error', () => { film.classList.remove('playing'); toggle.hidden = true; });
    film.addEventListener('play', label); film.addEventListener('pause', label);
    reduce.addEventListener('change', () => { if (reduce.matches) { film.pause(); film.classList.remove('playing'); } else play(); });
    document.addEventListener('visibilitychange', () => { if (document.hidden) film.pause(); else play(); });
    if ('IntersectionObserver' in window) new IntersectionObserver(entries => { for (const e of entries) { if (e.isIntersecting) play(); else film.pause(); } }, {threshold:.1}).observe(film);
    else play();
  }
  if ('IntersectionObserver' in window && !reduce.matches) {
    const io = new IntersectionObserver(entries => { for (const e of entries) if(e.isIntersecting) { e.target.classList.remove('pending'); e.target.classList.add('ready'); io.unobserve(e.target); } }, {threshold:.1});
    document.querySelectorAll('.reveal').forEach(e => { if (e.getBoundingClientRect().top > innerHeight) e.classList.add('pending'); io.observe(e); });
  }
  const progress = document.querySelector('.reading-progress');
  let ticking = false;
  function update() { const max = document.documentElement.scrollHeight-innerHeight; progress.style.transform = `scaleX(${max>0?scrollY/max:0})`; ticking=false; }
  addEventListener('scroll',()=>{if(!ticking){ticking=true;requestAnimationFrame(update)}},{passive:true}); update();
  if ('IntersectionObserver' in window) {
    const quick=document.querySelector('.quick-contact');new IntersectionObserver(entries=>{quick.hidden=entries[0].isIntersecting},{threshold:0}).observe(document.querySelector('#contacto'));
  }
  if (matchMedia('(pointer: fine)').matches && !reduce.matches) {
    const hero = document.querySelector('.hero');const poster=document.querySelector('.hero-poster');let frame;
    hero.addEventListener('pointermove', e => { if(frame) return; frame=requestAnimationFrame(()=>{const r=hero.getBoundingClientRect();const x=(e.clientX-r.left)/r.width-.5;const y=(e.clientY-r.top)/r.height-.5;poster.style.transform=`scale(1.035) translate(${x*8}px,${y*6}px)`;frame=null;}); });
    hero.addEventListener('pointerleave',()=>{poster.style.transform='scale(1.035)';});
  }
})();
