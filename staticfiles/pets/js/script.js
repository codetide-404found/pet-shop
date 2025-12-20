document.addEventListener("DOMContentLoaded", () => {

  const cartBtn = document.getElementById("cartBtn");
  const cartModal = document.getElementById("cartModal");
  const closeCart = document.getElementById("closeCart");
  const cartItems = document.getElementById("cartItems");
  const checkoutBtn = document.getElementById("checkoutBtn");

  let cart = JSON.parse(localStorage.getItem("cart")) || [];
  updateCartCount();
  renderCart();

  // === Open/Close Cart ===
  if (cartBtn && cartModal && closeCart) {
    cartBtn.addEventListener("click", () => {
      cartModal.style.display = "flex";
    });

    closeCart.addEventListener("click", () => {
      cartModal.style.display = "none";
    });

    window.addEventListener("click", e => {
      if (e.target === cartModal) cartModal.style.display = "none";
    });
  }

  // === Add to Cart ===
  document.querySelectorAll(".addCart").forEach(btn => {
    btn.addEventListener("click", () => {
      const name = btn.dataset.name;
      cart.push({ name });
      localStorage.setItem("cart", JSON.stringify(cart));
      updateCartCount();
      renderCart();
      showNotification(`${name} added to cart 🛒`);
    });
  });

  // === Update Cart Count ===
  function updateCartCount() {
    const cartCount = document.getElementById("cartCount");
    if (cartCount) cartCount.textContent = cart.length;
  }

  // === Render Cart Items ===
  function renderCart() {
    if (!cartItems) return;
    cartItems.innerHTML = "";

    cart.forEach((item, index) => {
      const li = document.createElement("li");
      li.innerHTML = `
        <span>${item.name}</span>
        <button class="remove-btn">Remove</button>
      `;
      li.querySelector(".remove-btn").onclick = () => {
        cart.splice(index, 1);
        localStorage.setItem("cart", JSON.stringify(cart));
        updateCartCount();
        renderCart();
      };
      cartItems.appendChild(li);
    });
  }

  // === Checkout via WhatsApp ===
  if (checkoutBtn) {
    checkoutBtn.addEventListener("click", () => {
      if (cart.length === 0) {
        alert("Cart is empty!");
        return;
      }
      let orderMessage = "Hello, I want to order the following:%0A";
      cart.forEach(item => orderMessage += `- ${item.name}%0A`);
      const whatsappNumber = "233123456789"; // replace with your number
      window.open(`https://wa.me/${whatsappNumber}?text=${orderMessage}`, "_blank");
      cart = [];
      localStorage.setItem("cart", JSON.stringify(cart));
      updateCartCount();
      renderCart();
    });
  }

  // === Notification Toast ===
  function showNotification(message) {
    let notification = document.getElementById("notification");
    if (!notification) {
      notification = document.createElement("div");
      notification.id = "notification";
      Object.assign(notification.style, {
        position: "fixed",
        bottom: "20px",
        right: "20px",
        background: "#ff6600",
        color: "#fff",
        padding: "10px 20px",
        borderRadius: "8px",
        boxShadow: "0 5px 15px rgba(0,0,0,0.2)",
        zIndex: "9999",
        opacity: "0",
        transition: "opacity 0.5s",
      });
      document.body.appendChild(notification);
    }
    notification.textContent = message;
    notification.style.opacity = "1";
    setTimeout(() => { notification.style.opacity = "0"; }, 2000);
  }

});
