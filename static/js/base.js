var cart_count = document.getElementById("cart_count") // Získá HTML element s ID 'cart_count' a uloží ho do proměnné

fetch('/cart/count') // Provádí HTTP GET požadavek na server na URL '/cart/count'
                .then(response => response.json())  // Zpracovává odpověď serveru jako JSON
                .then(data => { // Po úspěšném zpracování JSON odpovědi nastaví text elementu 'cart_count' na hodnotu 'count' z JSON odpovědi
                    cart_count.innerText = data.count
                }) // Pokud dojde k chybě během požadavku nebo zpracování, vypíše chybu do konzole
                .catch(error => console.error('Error:', error));


                // Tento kód najde prvek na stránce, který ukazuje počet položek v košíku, pak se zeptá serveru, kolik položek je v košíku.
                // Pak aktualizuje tento prvek na stránce s aktuálním počtem položek. Pokud se něco pokazí, vypíše chybu do konzole.





