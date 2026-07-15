// Tabs
  const tabBtns = document.querySelectorAll('.tab-btn');
  const panels = document.querySelectorAll('.menu-panel');
  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      tabBtns.forEach(b => b.classList.remove('active'));
      panels.forEach(p => p.classList.remove('active'));
      btn.classList.add('active');
      document.querySelector('.menu-panel[data-panel="' + btn.dataset.tab + '"]').classList.add('active');
    });
  });

  // Reveal on scroll
  const revealEls = document.querySelectorAll('.reveal');
  const io = new IntersectionObserver((entries) => {
    entries.forEach(e => { if(e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target); } });
  }, {threshold:0.15});
  revealEls.forEach(el => io.observe(el));

  // Mobile menu toggle (simple show/hide of links as a dropdown)
  const toggle = document.querySelector('.menu-toggle');
  const links = document.querySelector('.nav-links');
  if (toggle && links) {
    toggle.addEventListener('click', () => {
      const isOpen = links.style.display === 'flex';
      links.style.display = isOpen ? 'none' : 'flex';
      links.style.cssText += isOpen ? '' : 'position:absolute; top:70px; left:0; right:0; background:var(--cream); flex-direction:column; padding:20px 32px; gap:18px; box-shadow:0 10px 20px rgba(0,0,0,0.08);';
    });
  }

  // Menu search — filters items by name within the active category
  const searchInput = document.getElementById('menu-search-input');
  if (searchInput) {
    searchInput.addEventListener('input', () => {
      const q = searchInput.value.trim().toLowerCase();
      panels.forEach(panel => {
        const items = panel.querySelectorAll('.menu-item');
        let visibleCount = 0;
        items.forEach(item => {
          const name = item.dataset.name || '';
          const match = name.includes(q);
          item.style.display = match ? '' : 'none';
          if (match) visibleCount++;
        });
        const noResults = panel.querySelector('.no-results');
        if (noResults) noResults.hidden = visibleCount !== 0;
      });
    });
  }
