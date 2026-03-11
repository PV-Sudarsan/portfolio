const tabs = document.querySelectorAll(".tab");
const panels = document.querySelectorAll(".tab-panel");

tabs.forEach((tab) => {
  tab.addEventListener("click", () => {
    const target = tab.dataset.target;

    tabs.forEach((item) => {
      item.classList.toggle("is-active", item === tab);
      item.setAttribute("aria-selected", String(item === tab));
    });

    panels.forEach((panel) => {
      panel.classList.toggle("is-active", panel.id === target);
    });
  });
});

const counters = document.querySelectorAll("[data-count]");

const counterObserver = new IntersectionObserver((entries, observer) => {
  entries.forEach((entry) => {
    if (!entry.isIntersecting) {
      return;
    }

    const element = entry.target;
    const target = Number(element.dataset.count);
    const duration = 900;
    const startTime = performance.now();

    const tick = (now) => {
      const progress = Math.min((now - startTime) / duration, 1);
      element.textContent = String(Math.floor(progress * target));

      if (progress < 1) {
        requestAnimationFrame(tick);
        return;
      }

      element.textContent = String(target);
    };

    requestAnimationFrame(tick);
    observer.unobserve(element);
  });
});

counters.forEach((counter) => counterObserver.observe(counter));

const shell = document.querySelector(".page-shell");

window.addEventListener("pointermove", (event) => {
  const x = event.clientX / window.innerWidth;
  const y = event.clientY / window.innerHeight;
  shell.style.setProperty("--pointer-x", x.toFixed(3));
  shell.style.setProperty("--pointer-y", y.toFixed(3));
});
