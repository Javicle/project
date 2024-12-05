function onEntry(entries) {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("element-show");
      } 
      
    });
  }

  let options = {
    threshold: [0.3], 
  };
  let observer = new IntersectionObserver(onEntry, options);
  let elements = document.querySelectorAll(".element-animation");
  console.log(elements);
  elements.forEach((element) => observer.observe(element));