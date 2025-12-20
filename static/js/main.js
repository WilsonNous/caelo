(() => {
  /* ===============================
     Utilidades
  =============================== */

  // Atualiza o ano automaticamente (se existir no HTML)
  const yearEl = document.getElementById("year");
  if (yearEl) {
    yearEl.textContent = new Date().getFullYear();
  }

  /* ===============================
     Header shrink on scroll
  =============================== */

  const header = document.querySelector(".header");
  const onScroll = () => {
    if (!header) return;
    if (window.scrollY > 10) header.classList.add("shrink");
    else header.classList.remove("shrink");
  };

  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* ===============================
     Mobile menu
  =============================== */

  const navToggle = document.getElementById("navToggle");
  const navList = document.getElementById("navList");

  const setExpanded = (val) => {
    if (navToggle) navToggle.setAttribute("aria-expanded", String(val));
  };

  navToggle?.addEventListener("click", () => {
    const isOpen = navList.classList.toggle("open");
    setExpanded(isOpen);
  });

  // Fecha menu ao clicar em link
  navList?.addEventListener("click", (e) => {
    const a = e.target.closest("a");
    if (!a) return;
    navList.classList.remove("open");
    setExpanded(false);
  });

  /* ===============================
     Reveal on scroll
  =============================== */

  const items = document.querySelectorAll(".reveal");

  if (items.length) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("in");
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12 }
    );

    items.forEach((el) => io.observe(el));
  }

  /* ===============================
     Observação importante
  =============================== */

  /*
    - O formulário agora envia via POST para /lead (Flask)
    - Não interceptamos submit aqui
    - WhatsApp permanece como CTA nos botões
    - Código mais limpo, profissional e escalável
  */

})();
