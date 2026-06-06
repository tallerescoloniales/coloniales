document.addEventListener("DOMContentLoaded", function () {
  var reveals = document.querySelectorAll(".col26-reveal");
  if (reveals.length && "IntersectionObserver" in window) {
    var revealObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          revealObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 });
    reveals.forEach(function (node) { revealObserver.observe(node); });
  } else {
    reveals.forEach(function (node) { node.classList.add("is-visible"); });
  }

  var stack = document.querySelector("[data-parallax-stack]");
  if (stack) {
    var cards = stack.querySelectorAll(".col26-photo-card");
    stack.addEventListener("mousemove", function (event) {
      var rect = stack.getBoundingClientRect();
      var x = (event.clientX - rect.left) / rect.width - 0.5;
      var y = (event.clientY - rect.top) / rect.height - 0.5;
      cards.forEach(function (card, index) {
        var depth = (index + 1) * 10;
        card.style.transform = "translate(" + (x * depth) + "px," + (y * depth) + "px)";
      });
    });
    stack.addEventListener("mouseleave", function () {
      cards.forEach(function (card, index) {
        if (card.classList.contains("col26-photo-b")) card.style.transform = "rotate(4deg)";
        else if (card.classList.contains("col26-photo-c")) card.style.transform = "rotate(-4deg)";
        else card.style.transform = "";
      });
    });
  }

  var modal = document.querySelector("[data-celdas-modal]");
  if (modal) {
    var modalTitle = modal.querySelector("[data-celda-title]");
    var modalText = modal.querySelector("[data-celda-text]");
    var modalConcept = modal.querySelector("[data-celda-concept]");
    var modalMaterials = modal.querySelector("[data-celda-materials]");
    var modalMeta = modal.querySelector("[data-celda-meta]");
    var close = modal.querySelector("[data-celdas-close]");
    var search = document.querySelector("[data-celdas-search]");
    var filters = document.querySelectorAll("[data-celdas-filter]");
    var cards = document.querySelectorAll("[data-celda-card]");
    var empty = document.querySelector("[data-celdas-empty]");
    var activeFilter = "all";

    function renderVisibility() {
      var term = search ? search.value.trim().toLowerCase() : "";
      var visible = 0;
      cards.forEach(function (card) {
        var haystack = (card.dataset.search || "").toLowerCase();
        var categories = (card.dataset.category || "").split(",");
        var passesFilter = activeFilter === "all" || categories.indexOf(activeFilter) !== -1;
        var passesSearch = !term || haystack.indexOf(term) !== -1;
        var show = passesFilter && passesSearch;
        card.style.display = show ? "" : "none";
        if (show) visible += 1;
      });
      if (empty) empty.classList.toggle("is-visible", visible === 0);
    }

    cards.forEach(function (card) {
      card.addEventListener("click", function () {
        modalTitle.textContent = card.dataset.title || "";
        modalText.textContent = card.dataset.text || "";
        modalConcept.textContent = card.dataset.concept || "";
        modalMaterials.textContent = card.dataset.materials || "";
        modalMeta.textContent = card.dataset.meta || "";
        modal.classList.add("is-open");
        document.body.style.overflow = "hidden";
      });
    });

    filters.forEach(function (filter) {
      filter.addEventListener("click", function () {
        filters.forEach(function (item) { item.classList.remove("is-active"); });
        filter.classList.add("is-active");
        activeFilter = filter.dataset.celdasFilter || "all";
        renderVisibility();
      });
    });

    if (search) search.addEventListener("input", renderVisibility);

    function closeModal() {
      modal.classList.remove("is-open");
      document.body.style.overflow = "";
    }

    close.addEventListener("click", closeModal);
    modal.addEventListener("click", function (event) {
      if (event.target === modal) closeModal();
    });
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape") closeModal();
    });

    renderVisibility();
  }

  // Overlay menú móvil
  try{(function(){
    var h=document.getElementById('mainHamburger'),o=document.getElementById('wpOverlay'),c=document.getElementById('wpCloseBtn');
    function m(){if(h)h.classList.remove('active');o.classList.remove('open');document.body.style.overflow=''}
    function p(){if(h)h.classList.add('active');o.classList.add('open');document.body.style.overflow='hidden'}
    if(h){h.addEventListener('click',function(){o.classList.contains('open')?m():p()})}
    if(c)c.addEventListener('click',m);
    o.querySelectorAll('a').forEach(function(a){a.addEventListener('click',m)});
  })();}catch(e){}
});
