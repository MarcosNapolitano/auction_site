const buttons = document.querySelectorAll("[data-carousel-button]")


buttons.forEach(button => {
    button.addEventListener("click", ()=>{

        const offset = button.dataset.carouselButton === "next" ? 1 : -1
        const slides = button.closest("[data-carousel]").querySelector("[data-slides]")
        const activeSlide = slides.querySelector("[data-active]")


        let newIndex = [...slides.children].indexOf(activeSlide)+offset
        let prevIndex = newIndex-1

        if (newIndex<0) newIndex  = slides.children.length -1 
        if (newIndex >= slides.children.length) newIndex = 0

        if (prevIndex ==-1) prevIndex  = slides.children.length -1 
        if (prevIndex ==-2) prevIndex  = slides.children.length -2

        if(offset===-1){
            setTimeout(()=>{
                activeSlide.id= "an"
                slides.children[newIndex].id="next"
           
            },10)

            setTimeout(()=>{
                activeSlide.id= ""
                slides.children[newIndex].id=""
            },1000)
            
        }else{
            setTimeout(()=>{
                slides.children[newIndex].id="current"
                slides.children[prevIndex].id="prev_current"
           
            },10)

            setTimeout(()=>{
                activeSlide.id= ""
                slides.children[newIndex].id=""
            },1000)
        }

       

        slides.children[newIndex].dataset.active = true
        delete activeSlide.dataset.active

        delete slides.querySelector("[data-prev]").dataset.prev
        slides.children[prevIndex].dataset.prev = true


    })

})