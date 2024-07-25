var cart_count = document.getElementById("cart_count")

fetch('/cart/count')
                .then(response => response.json())
                .then(data => {
                    cart_count.innerText = data.count
                })
                .catch(error => console.error('Error:', error));


                // Tento kód najde prvek na stránce, který ukazuje počet položek v košíku, pak se zeptá serveru, kolik položek je v košíku.
                // Pak aktualizuje tento prvek na stránce s aktuálním počtem položek. Pokud se něco pokazí, vypíše chybu do konzole.





