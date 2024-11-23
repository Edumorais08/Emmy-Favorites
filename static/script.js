document.addEventListener("DOMContentLoaded", function () {
    const menuToggle = document.getElementById("menu-toggle");
    const navbar = document.getElementById("navbar");
    const mainContent = document.querySelector("main");

    // Função para alternar o menu
    menuToggle.addEventListener("click", function () {
        navbar.classList.toggle("hidden");
        navbar.classList.toggle("open");

        // Ajusta a margem superior do conteúdo principal
        const headerHeight = navbar.classList.contains("open") ? "0.3rem" : "0";
        mainContent.style.marginTop = headerHeight;
    });

    // Fechar o menu ao clicar fora
    document.addEventListener("click", function (event) {
        if (!navbar.contains(event.target) && event.target !== menuToggle) {
            navbar.classList.add("hidden");
            navbar.classList.remove("open");

            // Remove o espaço extra no conteúdo principal
            mainContent.style.marginTop = "0";
        }
    });
});