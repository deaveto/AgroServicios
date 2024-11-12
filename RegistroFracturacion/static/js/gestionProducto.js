(function (){
    const btnElimicacion = document.querySelectorAll(".btnElimicacion");

    btnElimicacion.forEach(btn =>{
        btn.addEventListener('click', (e)=>{
            const confirmacion =confirm('¿seguro de eliminar el producto?');
            if(!confirmacion){
                e.preventDefault();
            }
        });
    });
})
();