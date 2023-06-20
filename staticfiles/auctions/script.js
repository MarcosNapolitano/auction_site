const buttons = document.querySelectorAll("[data-carousel-button]");
const slides = document.getElementsByClassName("slide");

if (slides.length > 0) {
  slides[0].dataset.active = true;
  slides[slides.length - 1].dataset.prev = true;

  buttons.forEach((button) => {
    button.addEventListener("click", () => {
      const offset = button.dataset.carouselButton === "next" ? 1 : -1;
      const slides = button
        .closest("[data-carousel]")
        .querySelector("[data-slides]");
      const activeSlide = slides.querySelector("[data-active]");
      const buttons = document.getElementsByTagName("button");

      for (let i = 0; i < buttons.length; i++) {
        button.disabled = true;
        setTimeout(() => {
          button.disabled = false;
        }, 1000);
      }

      let newIndex = [...slides.children].indexOf(activeSlide) + offset;
      let prevIndex = newIndex - offset;

      if (newIndex < 0) newIndex = slides.children.length - 1;
      if (newIndex >= slides.children.length) newIndex = 0;

      if (prevIndex == -1) prevIndex = slides.children.length - 1;

      if (offset === -1) {
        activeSlide.id = "an";
        slides.children[newIndex].id = "next";

        setTimeout(() => {
          activeSlide.id = "";
          slides.children[newIndex].id = "";
        }, 985);
      } else {
        activeSlide.id = "prev_current";
        slides.children[newIndex].id = "current";

        setTimeout(() => {
          activeSlide.id = "";
          slides.children[newIndex].id = "";
        }, 1000);
      }

      slides.children[newIndex].dataset.active = true;
      delete activeSlide.dataset.active;

      delete slides.querySelector("[data-prev]").dataset.prev;
      slides.children[prevIndex].dataset.prev = true;
    });
  });
}
