var cart_count = document.getElementById("cart_count")

fetch('/cart/count')
                .then(response => response.json())
                .then(data => {
                    cart_count.innerText = data.count
                })
                .catch(error => console.error('Error:', error));