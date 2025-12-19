
(() => {
  // Year
  document.getElementById("year").textContent = new Date().getFullYear();

  // Header shrink
  const header = document.querySelector(".header");
  const onScroll = () => {
    if (window.scrollY > 10) header.classList.add("shrink");
    else header.classList.remove("shrink");
  };
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  // Mobile menu
  const navToggle = document.getElementById("navToggle");
  const navList = document.getElementById("navList");

  const setExpanded = (val) => navToggle.setAttribute("aria-expanded", String(val));

  navToggle?.addEventListener("click", () => {
    const isOpen = navList.classList.toggle("open");
    setExpanded(isOpen);
  });

  // Close menu on link click
  navList?.addEventListener("click", (e) => {
    const a = e.target.closest("a");
    if (!a) return;
    navList.classList.remove("open");
    setExpanded(false);
  });

  // Reveal on scroll
  const items = document.querySelectorAll(".reveal");
  const io = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        if (entry.isIntersecting) {
          entry.target.classList.add("in");
          io.unobserve(entry.target);
        }
      }
    },
    { threshold: 0.12 }
  );
  items.forEach((el) => io.observe(el));

  // Accordion (Missão & Chamado)
  document.querySelectorAll("[data-accordion]").forEach((acc) => {
    const btn = acc.querySelector(".accordion__btn");
    const panel = acc.querySelector(".accordion__panel");
    const icon = acc.querySelector(".accordion__icon");

    btn?.addEventListener("click", () => {
      const expanded = btn.getAttribute("aria-expanded") === "true";
      btn.setAttribute("aria-expanded", String(!expanded));

      if (expanded) {
        panel.hidden = true;
        icon.textContent = "+";
      } else {
        panel.hidden = false;
        icon.textContent = "–";
      }
    });
  });

  // Lead form -> WhatsApp
  const form = document.getElementById("leadForm");
  form?.addEventListener("submit", (e) => {
    e.preventDefault();

    const nome = document.getElementById("nome").value.trim();
    const fone = document.getElementById("fone").value.trim();
    const msg = document.getElementById("msg").value.trim();

    const text = encodeURIComponent(
      `Olá! Meu nome é ${nome}.\nMeu telefone/WhatsApp: ${fone}\n\nMensagem: ${msg}\n\nVim pelo portal CAELO.`
    );

    window.open(`https://wa.me/554199642685?text=${text}`, "_blank", "noopener");
  });
})();
